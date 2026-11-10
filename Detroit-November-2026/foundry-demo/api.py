import os
from uuid import UUID

from azure.core.exceptions import AzureError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from jwt import PyJWKClient, PyJWKClientConnectionError
import jwt
from openai import OpenAIError
from openpyxl.utils.exceptions import InvalidFileException
from pydantic import BaseModel, ConfigDict, Field
from zipfile import BadZipFile

from demo import ROOT, SOURCE_FILES, load_spreadsheet, process_bundle

DEMO_BUNDLE_ID = "FC-03-NL300"
DEMO_BUNDLE_PATH = ROOT / "bundles" / "FC-03"
app = FastAPI(title="Supplier Catalog Processor", version="1.0.0")


class ProcessBundleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sourceBundleId: str = Field(min_length=1, max_length=200)
    clientRequestId: str | None = Field(default=None, max_length=100)


def _error(status_code, code, message, retryable=False):
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "runId": None,
            "retryable": retryable,
        },
    )


@app.exception_handler(RequestValidationError)
async def invalid_request_handler(request, error):
    return _error(400, "invalid_request", "The request body does not match the catalog API contract.")


def _authorize(request: Request):
    if os.environ.get("CATALOG_LOCAL_AUTH_BYPASS") == "true":
        remote_addr = request.client.host if request.client else ""
        if os.environ.get("CATALOG_ENV") != "local" or remote_addr not in ("127.0.0.1", "::1", "testclient"):
            raise RuntimeError("Unauthenticated mode is allowed only for local development.")
        return None

    allowed_tenants = os.environ.get("CATALOG_ALLOWED_TENANT_IDS", "")
    audience = os.environ.get("CATALOG_API_AUDIENCE")
    scope = os.environ.get("CATALOG_API_SCOPE", "catalog.process")
    if not allowed_tenants or not audience:
        raise RuntimeError("Entra API authentication is not configured.")

    try:
        tenant_ids = {str(UUID(value.strip())) for value in allowed_tenants.split(",") if value.strip()}
        audience = str(UUID(audience))
    except ValueError as error:
        raise RuntimeError("Entra API authentication configuration is invalid.") from error
    if not tenant_ids or not scope:
        raise RuntimeError("Entra API authentication configuration is invalid.")

    authorization = request.headers.get("authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise jwt.InvalidTokenError("A bearer access token is required.")

    unverified_claims = jwt.decode(
        token,
        options={
            "verify_signature": False,
            "verify_exp": False,
            "verify_aud": False,
            "verify_iss": False,
        },
    )
    try:
        tenant_id = str(UUID(unverified_claims.get("tid", "")))
    except (AttributeError, ValueError) as error:
        raise jwt.InvalidTokenError("The token tenant is invalid.") from error
    if tenant_id not in tenant_ids or unverified_claims.get("ver") != "2.0":
        raise jwt.InvalidTokenError("The token tenant or version is not allowed.")

    issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
    jwks = PyJWKClient(f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys")
    signing_key = jwks.get_signing_key_from_jwt(token)
    claims = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience=audience, issuer=issuer)
    granted_scopes = claims.get("scp")
    try:
        verified_tenant_id = str(UUID(claims.get("tid", "")))
    except (AttributeError, ValueError) as error:
        raise jwt.InvalidTokenError("The verified token tenant is invalid.") from error
    if verified_tenant_id != tenant_id or claims.get("ver") != "2.0":
        raise jwt.InvalidTokenError("The verified token tenant or version is invalid.")
    if not isinstance(granted_scopes, str) or scope not in granted_scopes.split():
        return False
    return claims


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/catalog/process")
def process_catalog_bundle(body: ProcessBundleRequest, request: Request):
    try:
        claims = _authorize(request)
    except RuntimeError as error:
        return _error(503, "auth_not_configured", str(error), retryable=False)
    except PyJWKClientConnectionError:
        return _error(503, "identity_provider_unavailable", "Entra signing keys could not be retrieved.", retryable=True)
    except jwt.PyJWTError:
        return _error(401, "invalid_token", "The access token is invalid or expired.")

    if claims is False:
        return _error(403, "insufficient_scope", "The caller lacks the catalog.process permission.")

    if body.sourceBundleId != DEMO_BUNDLE_ID:
        return _error(404, "bundle_not_found", "The requested source bundle is unavailable.")

    inputs = {
        source_id: DEMO_BUNDLE_PATH / filename
        for source_id, filename in SOURCE_FILES.items()
    }
    if any(not path.is_file() for path in inputs.values()):
        return _error(503, "bundle_unavailable", "The synthetic demo bundle is not present in this service build.", retryable=True)

    try:
        load_spreadsheet(inputs["spreadsheet-001"])
    except (ValueError, InvalidFileException, BadZipFile):
        return _error(422, "invalid_bundle", "The synthetic workbook has an unsupported layout.")
    except OSError:
        return _error(503, "bundle_unavailable", "The synthetic demo bundle could not be read.", retryable=True)

    try:
        result = process_bundle(body.sourceBundleId, inputs, body.clientRequestId)
    except (AzureError, OpenAIError):
        return _error(502, "model_request_failed", "The Foundry model request failed.")
    except ValueError:
        return _error(502, "invalid_model_result", "The model result failed local validation.")
    except OSError:
        return _error(503, "processor_unavailable", "The processor could not save the run result.", retryable=True)
    return result
