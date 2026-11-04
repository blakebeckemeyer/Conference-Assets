from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from demo import Extraction, Observation, SOURCE_FILES, SPEC_LINES, execute, run, validate


def sample(image_color="red", warranty="24"):
    values = {"sku": "NL-300", "color": "black", "width_mm": "250", "warranty_months": warranty}
    lines = {"sku": SPEC_LINES[2], "color": SPEC_LINES[4], "width_mm": SPEC_LINES[5], "warranty_months": SPEC_LINES[6]}
    observations = []
    for source in ("spec-001", "image-001"):
        for field in values:
            value = values[field] if source == "spec-001" else (
                "NL-300" if field == "sku" else image_color if field == "color" else None
            )
            observations.append(Observation(source_id=source, field=field, value=value,
                                            evidence=lines[field] if source == "spec-001" else "Visible image evidence"))
    return Extraction(observations=observations)


class ValidationTests(unittest.TestCase):
    def test_conflict_keeps_candidates(self):
        record = validate(sample())
        self.assertIsNone(record["color"])
        self.assertEqual(record["issues"], ["color-conflict"])
        self.assertEqual(record["status"], "needs_review")
        self.assertEqual(record["width_cm"], "25.0")
        self.assertEqual(record["warranty_months"], 24)
        self.assertFalse(record["published"])

    def test_consistent(self):
        self.assertEqual(validate(sample("black"))["status"], "validated_draft")

    def test_missing(self):
        record = validate(sample("black", None))
        self.assertIsNone(record["warranty_months"])
        self.assertIn("warranty-missing", record["issues"])

    def test_incomplete_sources(self):
        data = sample()
        data.observations.pop()
        with self.assertRaisesRegex(ValueError, "Missing source"):
            validate(data)

    def test_bad_evidence(self):
        data = sample()
        data.observations[0].evidence = "invented"
        with self.assertRaisesRegex(ValueError, "exact source"):
            validate(data)

    def test_invalid_number(self):
        data = sample()
        data.observations[2].value = "NaN"
        with self.assertRaisesRegex(ValueError, "numeric"):
            validate(data)

    def test_value_must_match_pdf_evidence(self):
        data = sample()
        data.observations[0].value = "NL-999"
        with self.assertRaisesRegex(ValueError, "not supported"):
            validate(data)

    def test_no_invented_image_warranty(self):
        data = sample()
        data.observations[-1].value = "24"
        with self.assertRaisesRegex(ValueError, "no dimension or warranty"):
            validate(data)

    def test_duplicate(self):
        data = sample()
        data.observations.append(data.observations[0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(data)

    def test_decimal_representation(self):
        data = sample()
        data.observations[2].value = "250.0"
        self.assertEqual(validate(data)["width_cm"], "25.0")


class RequestTests(unittest.TestCase):
    def test_one_inline_request_with_schema(self):
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
                    patch("demo.OpenAI") as client, redirect_stdout(StringIO()):
                api = client.return_value.__enter__.return_value
                api.responses.parse.return_value = response
                execute({"tenant_id": "test-tenant", "base_url": "https://example.invalid", "deployment": "test"},
                        inputs, output, {})
                credential.assert_called_once_with(tenant_id="test-tenant")
                api.responses.parse.assert_called_once()
                request = api.responses.parse.call_args.kwargs
                self.assertFalse(request["store"])
                self.assertEqual(request["max_output_tokens"], 5000)
                self.assertIs(request["text_format"], Extraction)
                content = request["input"][0]["content"]
                self.assertTrue(content[1]["file_data"].startswith("data:application/pdf;base64,"))
                self.assertTrue(content[2]["image_url"].startswith("data:image/png;base64,"))
                self.assertEqual(client.call_args.kwargs["max_retries"], 0)
            record = json.loads((output / "record.json").read_text())
            self.assertEqual(record["issues"], ["color-conflict"])

    def test_failed_run_is_not_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "inputs").mkdir()
            for name in SOURCE_FILES.values():
                (root / "inputs" / name).write_bytes(b"offline-test-only")
            (root / "config.json").write_text("{}")
            with patch("demo.ROOT", root), patch.dict("os.environ", {"AZURE_CONFIG_DIR": directory}), \
                    patch("demo.execute", side_effect=ValueError("offline test failure")), redirect_stdout(StringIO()):
                with self.assertRaisesRegex(ValueError, "offline test failure"):
                    run()
            manifest = json.loads(next((root / "runs").glob("*\\manifest.json")).read_text())
            self.assertEqual(manifest["status"], "failed")
            self.assertEqual(manifest["model_requests_attempted"], 0)
            self.assertFalse(list((root / "runs").glob("*\\record.json")))


if __name__ == "__main__":
    unittest.main()
