from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from openpyxl import Workbook

import api
from demo import (
    Extraction, Observation, ROOT, SOURCE_FILES, SPEC_LINES, SPREADSHEET_HEADERS,
    execute, load_spreadsheet, process_bundle, run, validate,
)

SHEET_CELLS = {
    "sku": {"cell": "A2", "value": "NL-300"},
    "color": {"cell": "B2", "value": "black"},
    "width_mm": {"cell": "C2", "value": 250},
    "warranty_months": {"cell": "D2", "value": 24},
}


def sample(image_color="red"):
    values = {"sku": "NL-300", "color": "black", "width_mm": "250", "warranty_months": "24"}
    lines = {"sku": SPEC_LINES[2], "color": SPEC_LINES[4], "width_mm": SPEC_LINES[5], "warranty_months": SPEC_LINES[6]}
    observations = []
    for source in SOURCE_FILES:
        for field in values:
            if source == "spec-001":
                value, evidence = values[field], lines[field]
            elif source == "spreadsheet-001":
                value = str(SHEET_CELLS[field]["value"])
                evidence = f"Products!{SHEET_CELLS[field]['cell']} = {value}"
            else:
                value = "NL-300" if field == "sku" else image_color if field == "color" else None
                evidence = (
                    'Visible label reads "Model: NL-300".' if field == "sku"
                    else "The depicted desk lamp is red." if field == "color"
                    else f"No {field} is stated in the image."
                )
            observations.append(Observation(source_id=source, field=field, value=value, evidence=evidence))
    return Extraction(observations=observations)


def make_workbook(path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Products"
    sheet.append(SPREADSHEET_HEADERS)
    sheet.append(["NL-300", "black", 250, 24])
    workbook.save(path)
    workbook.close()


class ValidationTests(unittest.TestCase):
    def test_conflict_keeps_all_candidates(self):
        record = validate(sample(), SHEET_CELLS)
        self.assertIsNone(record["color"])
        self.assertEqual(record["issues"], ["color-conflict"])
        self.assertEqual(record["status"], "needs_review")
        self.assertEqual(record["width_cm"], "25.0")
        self.assertEqual(record["warranty_months"], 24)
        self.assertEqual(len(record["candidates"]["color"]), 3)
        self.assertFalse(record["published"])

    def test_consistent(self):
        self.assertEqual(validate(sample("black"), SHEET_CELLS)["status"], "validated_draft")

    def test_missing_image_color_is_routed_to_review(self):
        data = sample("black")
        image_color = next(item for item in data.observations if item.source_id == "image-001" and item.field == "color")
        image_color.value = None
        record = validate(data, SHEET_CELLS)
        self.assertEqual(record["color"], "black")
        self.assertEqual(record["status"], "needs_review")
        self.assertIn("image-color-missing", record["issues"])

    def test_incomplete_sources(self):
        data = sample()
        data.observations.pop()
        with self.assertRaisesRegex(ValueError, "Missing source"):
            validate(data, SHEET_CELLS)

    def test_bad_pdf_evidence(self):
        data = sample()
        data.observations[0].evidence = "invented"
        with self.assertRaisesRegex(ValueError, "exact source"):
            validate(data, SHEET_CELLS)

    def test_invalid_number(self):
        data = sample()
        data.observations[2].value = "NaN"
        with self.assertRaisesRegex(ValueError, "numeric"):
            validate(data, SHEET_CELLS)

    def test_value_must_match_pdf_evidence(self):
        data = sample()
        data.observations[0].value = "NL-999"
        with self.assertRaisesRegex(ValueError, "not supported"):
            validate(data, SHEET_CELLS)

    def test_source_field_present_in_pdf(self):
        data = sample()
        data.observations[3].value = None
        with self.assertRaisesRegex(ValueError, "Expected value missing"):
            validate(data, SHEET_CELLS)

    def test_source_field_present_in_spreadsheet(self):
        data = sample()
        data.observations[7].value = None
        with self.assertRaisesRegex(ValueError, "Expected value missing"):
            validate(data, SHEET_CELLS)

    def test_no_invented_image_warranty(self):
        data = sample()
        data.observations[-1].value = "24"
        with self.assertRaisesRegex(ValueError, "no dimension or warranty"):
            validate(data, SHEET_CELLS)

    def test_duplicate(self):
        data = sample()
        data.observations.append(data.observations[0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(data, SHEET_CELLS)

    def test_decimal_representation(self):
        data = sample()
        data.observations[2].value = "250.0"
        self.assertEqual(validate(data, SHEET_CELLS)["width_cm"], "25.0")

    def test_spreadsheet_value_must_match_cell(self):
        data = sample()
        item = next(item for item in data.observations if item.source_id == "spreadsheet-001" and item.field == "sku")
        item.value = "NL-999"
        with self.assertRaisesRegex(ValueError, "Spreadsheet value"):
            validate(data, SHEET_CELLS)

    def test_spreadsheet_cell_evidence_must_match(self):
        data = sample()
        item = next(item for item in data.observations if item.source_id == "spreadsheet-001" and item.field == "sku")
        item.evidence = "Products!B2 = NL-300"
        with self.assertRaisesRegex(ValueError, "Spreadsheet value"):
            validate(data, SHEET_CELLS)

    def test_spreadsheet_loader_reports_cell_locators(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "supplier.xlsx"
            make_workbook(path)
            cells, text = load_spreadsheet(path)
        self.assertEqual(cells, SHEET_CELLS)
        self.assertIn("Products!A2 = NL-300", text)
        self.assertIn("Products!D2 = 24", text)


class RequestTests(unittest.TestCase):
    def test_connector_and_infrastructure_share_studio_owned_api_identity(self):
        root = Path(__file__).resolve().parents[2]
        values = json.loads((Path(__file__).parent / "copilot-studio-connector-values.json").read_text())
        registration = values["apiRegistration"]
        self.assertEqual(registration["signInAudience"], "AzureADMyOrg")
        self.assertEqual(registration["tenantId"], values["oauth"]["tenantId"])
        self.assertEqual(registration["scopeConsentType"], "Admin")
        self.assertEqual(registration["identifierUri"], f"api://{registration['appId']}")
        scope = f"{registration['identifierUri']}/{registration['delegatedScope']}"
        self.assertEqual(values["oauth"]["scope"], scope)
        contract = json.loads((Path(__file__).parent / "catalog-api.openapi.json").read_text())
        self.assertEqual(contract["security"][0]["EntraOAuth2"], [scope])
        for name in ("api.parameters.json", "main.parameters.json"):
            parameters = json.loads((root / "infra" / name).read_text())["parameters"]
            self.assertEqual(parameters["catalogApiAudience"]["value"], registration["appId"])
            self.assertEqual(parameters["catalogAllowedTenantIds"]["value"], [registration["tenantId"]])

    def test_api_contract_for_workflow_connector(self):
        contract = json.loads((Path(__file__).parent / "catalog-api.openapi.json").read_text())
        self.assertEqual(contract["swagger"], "2.0")
        self.assertEqual(list(contract["paths"]), ["/catalog/process"])
        operation = contract["paths"]["/catalog/process"]
        self.assertEqual(list(operation), ["post"])
        self.assertEqual(operation["post"]["operationId"], "processSupplierCatalogBundle")
        request = contract["definitions"]["ProcessBundleRequest"]["required"]
        self.assertEqual(request, ["sourceBundleId"])
        self.assertNotIn("SupplierFile", contract["definitions"])
        self.assertEqual(contract["definitions"]["ProcessBundleRequest"]["properties"]["sourceBundleId"]["enum"], ["FC-03-NL300"])
        self.assertEqual(
            contract["security"][0]["EntraOAuth2"],
            ["api://c1cfcc13-f250-45d7-ad61-03d4c72677c1/catalog.process"],
        )
        self.assertIn(
            "1b37c04e-260e-4189-a11b-0b8609ed3df0",
            contract["securityDefinitions"]["EntraOAuth2"]["authorizationUrl"],
        )
        self.assertEqual(contract["definitions"]["CatalogRecord"]["properties"]["published"]["enum"], [False])
        self.assertIn("runId", contract["definitions"]["ProcessBundleResponse"]["required"])
        self.assertIn("sourceBundleId", contract["definitions"]["ProcessBundleResponse"]["required"])

    def test_one_model_request_with_schema_and_three_inputs(self):
        response = SimpleNamespace(
            id="offline-test", model="test-model", status="completed", usage=None,
            output_parsed=sample(), model_dump=lambda **kwargs: {"offline_test": True},
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            inputs = {source: output / name for source, name in SOURCE_FILES.items()}
            for path in inputs.values():
                path.write_bytes(b"offline-test-only")
            with patch("demo.AzureCliCredential") as credential, \
                    patch("demo.get_bearer_token_provider", return_value=lambda: "offline-test"), \
                    patch.dict("os.environ", {"AZURE_CONFIG_DIR": directory}), \
                    patch("demo.OpenAI") as client, redirect_stdout(StringIO()):
                api = client.return_value.__enter__.return_value
                api.responses.parse.return_value = response
                execute({"tenant_id": "test-tenant", "base_url": "https://example.invalid", "deployment": "test"},
                        inputs, output, {}, SHEET_CELLS, "Source spreadsheet: spreadsheet-001\nProducts!A2 = NL-300")
                credential.assert_called_once_with(tenant_id="test-tenant")
                api.responses.parse.assert_called_once()
                request = api.responses.parse.call_args.kwargs
                self.assertFalse(request["store"])
                self.assertEqual(request["max_output_tokens"], 5000)
                self.assertIs(request["text_format"], Extraction)
                self.assertEqual(client.call_args.kwargs["timeout"], 180)
                content = request["input"][0]["content"]
                self.assertTrue(content[1]["file_data"].startswith("data:application/pdf;base64,"))
                self.assertTrue(content[2]["image_url"].startswith("data:image/png;base64,"))
                self.assertIn("Products!A2 = NL-300", content[3]["text"])
                self.assertEqual(client.call_args.kwargs["max_retries"], 0)
            record = json.loads((output / "record.json").read_text())
            self.assertEqual(record["issues"], ["color-conflict"])

    def test_failed_run_is_not_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = root / "inputs"
            inputs.mkdir()
            (inputs / "specification.pdf").write_bytes(b"offline-test-only")
            (inputs / "packaging.png").write_bytes(b"offline-test-only")
            make_workbook(inputs / "supplier.xlsx")
            (root / "config.json").write_text("{}")
            with patch("demo.ROOT", root), patch.dict("os.environ", {"AZURE_CONFIG_DIR": directory}), \
                    patch("demo.execute", side_effect=ValueError("offline test failure")), redirect_stdout(StringIO()):
                with self.assertRaisesRegex(ValueError, "offline test failure"):
                    run()
            run_dir = next((root / "runs").iterdir())
            manifest = json.loads((run_dir / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "failed")
            self.assertEqual(manifest["model_requests_attempted"], 0)
            self.assertFalse((run_dir / "record.json").exists())


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(api.app)
        self.local_auth = patch.dict(os.environ, {
            "CATALOG_ENV": "local",
            "CATALOG_LOCAL_AUTH_BYPASS": "true",
        })
        self.local_auth.start()
        self.addCleanup(self.local_auth.stop)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_only_the_fixed_synthetic_bundle_is_resolvable(self):
        response = self.client.post("/v1/catalog/process", json={"sourceBundleId": "other"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["code"], "bundle_not_found")

    def test_authentication_is_required_outside_local_mode(self):
        with patch.dict(os.environ, {"CATALOG_ENV": "production"}, clear=False):
            os.environ.pop("CATALOG_LOCAL_AUTH_BYPASS", None)
            os.environ.pop("CATALOG_ALLOWED_TENANT_IDS", None)
            os.environ.pop("CATALOG_API_AUDIENCE", None)
            response = self.client.post("/v1/catalog/process", json={"sourceBundleId": api.DEMO_BUNDLE_ID})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["code"], "auth_not_configured")

    def test_v2_token_uses_allowed_studio_tenant_and_client_id_audience(self):
        studio_tenant = "1b37c04e-260e-4189-a11b-0b8609ed3df0"
        api_client_id = "c1cfcc13-f250-45d7-ad61-03d4c72677c1"
        verified_claims = {
            "tid": studio_tenant,
            "ver": "2.0",
            "scp": "catalog.process",
        }
        with patch.dict(os.environ, {
            "CATALOG_ENV": "production",
            "CATALOG_ALLOWED_TENANT_IDS": studio_tenant,
            "CATALOG_API_AUDIENCE": api_client_id,
            "CATALOG_API_SCOPE": "catalog.process",
        }, clear=True), patch("api.PyJWKClient") as jwks_client, patch("api.jwt.decode") as decode, \
                patch("api.process_bundle", return_value={"status": "completed"}) as process:
            decode.side_effect = [
                {"tid": studio_tenant, "ver": "2.0"},
                verified_claims,
            ]
            jwks_client.return_value.get_signing_key_from_jwt.return_value = SimpleNamespace(key="test-signing-key")

            response = self.client.post(
                "/v1/catalog/process",
                json={"sourceBundleId": api.DEMO_BUNDLE_ID},
                headers={"Authorization": "Bearer synthetic-test-token"},
            )

        self.assertEqual(response.status_code, 200)
        jwks_client.assert_called_once_with(
            f"https://login.microsoftonline.com/{studio_tenant}/discovery/v2.0/keys"
        )
        self.assertEqual(decode.call_args.kwargs["algorithms"], ["RS256"])
        self.assertEqual(decode.call_args.kwargs["audience"], api_client_id)
        self.assertEqual(
            decode.call_args.kwargs["issuer"],
            f"https://login.microsoftonline.com/{studio_tenant}/v2.0",
        )
        process.assert_called_once()

    def test_token_from_unlisted_tenant_is_rejected_before_key_lookup(self):
        unlisted_tenant = "6aab181b-a190-4247-a5d7-cb792347c7fb"
        with patch.dict(os.environ, {
            "CATALOG_ENV": "production",
            "CATALOG_ALLOWED_TENANT_IDS": "1b37c04e-260e-4189-a11b-0b8609ed3df0",
            "CATALOG_API_AUDIENCE": "c1cfcc13-f250-45d7-ad61-03d4c72677c1",
        }, clear=True), patch("api.PyJWKClient") as jwks_client, patch(
            "api.jwt.decode", return_value={"tid": unlisted_tenant, "ver": "2.0"}
        ):
            response = self.client.post(
                "/v1/catalog/process",
                json={"sourceBundleId": api.DEMO_BUNDLE_ID},
                headers={"Authorization": "Bearer synthetic-test-token"},
            )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["code"], "invalid_token")
        jwks_client.assert_not_called()

    def test_non_v2_token_is_rejected(self):
        studio_tenant = "1b37c04e-260e-4189-a11b-0b8609ed3df0"
        with patch.dict(os.environ, {
            "CATALOG_ENV": "production",
            "CATALOG_ALLOWED_TENANT_IDS": studio_tenant,
            "CATALOG_API_AUDIENCE": "c1cfcc13-f250-45d7-ad61-03d4c72677c1",
        }, clear=True), patch("api.PyJWKClient") as jwks_client, patch(
            "api.jwt.decode", return_value={"tid": studio_tenant, "ver": "1.0"}
        ):
            response = self.client.post(
                "/v1/catalog/process",
                json={"sourceBundleId": api.DEMO_BUNDLE_ID},
                headers={"Authorization": "Bearer synthetic-test-token"},
            )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["code"], "invalid_token")
        jwks_client.assert_not_called()

    def test_application_id_uri_is_not_accepted_as_v2_audience_configuration(self):
        with patch.dict(os.environ, {
            "CATALOG_ENV": "production",
            "CATALOG_ALLOWED_TENANT_IDS": "1b37c04e-260e-4189-a11b-0b8609ed3df0",
            "CATALOG_API_AUDIENCE": "api://c1cfcc13-f250-45d7-ad61-03d4c72677c1",
        }, clear=True):
            response = self.client.post(
                "/v1/catalog/process",
                json={"sourceBundleId": api.DEMO_BUNDLE_ID},
                headers={"Authorization": "Bearer synthetic-test-token"},
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["code"], "auth_not_configured")

    def test_missing_or_invalid_permission_is_rejected(self):
        with patch("api._authorize", return_value=False):
            response = self.client.post("/v1/catalog/process", json={"sourceBundleId": api.DEMO_BUNDLE_ID})
        self.assertEqual(response.status_code, 403)

    def test_invalid_request_uses_the_documented_error_shape(self):
        response = self.client.post("/v1/catalog/process", json={"unexpected": "value"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["code"], "invalid_request")
        self.assertIn("runId", response.json())

    def test_successful_api_response_preserves_run_and_review_fields(self):
        expected = {
            "runId": "offline-test-run",
            "sourceBundleId": api.DEMO_BUNDLE_ID,
            "clientRequestId": "request-1",
            "status": "completed",
            "record": {
                "sku": "NL-300", "color": None, "width_cm": "25.0",
                "warranty_months": 24, "status": "needs_review",
                "issues": ["color-conflict"], "candidates": {}, "evidence": [],
                "published": False,
            },
            "model": {
                "deployment": "test", "returnedModel": "test",
                "inputTokens": 1, "outputTokens": 1,
            },
            "elapsedMs": 1,
        }
        with patch("api.process_bundle", return_value=expected) as process:
            response = self.client.post(
                "/v1/catalog/process",
                json={"sourceBundleId": api.DEMO_BUNDLE_ID, "clientRequestId": "request-1"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
        process.assert_called_once()

    def test_bundle_run_uses_the_same_processor_and_returns_auditable_metadata(self):
        paths = {source: api.DEMO_BUNDLE_PATH / name for source, name in SOURCE_FILES.items()}
        result = {
            "record": validate(sample(), SHEET_CELLS),
            "model": {"deployment": "test", "returnedModel": "test", "inputTokens": 2, "outputTokens": 3},
            "elapsedMs": 4,
        }
        with patch("demo.execute", return_value=result) as execute_stub:
            response = process_bundle(api.DEMO_BUNDLE_ID, paths, "request-2")
        self.assertEqual(response["sourceBundleId"], api.DEMO_BUNDLE_ID)
        self.assertEqual(response["clientRequestId"], "request-2")
        self.assertEqual(response["record"]["issues"], ["color-conflict"])
        execute_stub.assert_called_once()
        run_dir = ROOT / "runs" / response["runId"]
        manifest = json.loads((run_dir / "manifest.json").read_text())
        self.assertEqual(manifest["source_bundle_id"], api.DEMO_BUNDLE_ID)
        self.assertEqual(manifest["status"], "completed")
        self.assertEqual(execute_stub.call_args.kwargs["timeout_seconds"], 70)


if __name__ == "__main__":
    unittest.main()
