"""Foundry Activity adapter for the fixed, synthetic catalog-processing demo."""
import asyncio
import json
import logging
import os
from pathlib import Path
from urllib.parse import urlparse

from demo import ROOT, SOURCE_FILES, process_bundle

TENANT_ID = "1b37c04e-260e-4189-a11b-0b8609ed3df0"
BUNDLE_ID = "FC-03-NL300"
COMMAND = f"process {BUNDLE_ID}"
logger = logging.getLogger("supplier-catalog-specialist")


def inference_config():
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    parsed = urlparse(endpoint)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or not parsed.hostname.endswith(".openai.azure.com")
        or parsed.hostname == "dtw-tool-demo.openai.azure.com"
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or parsed.port is not None or parsed.path not in ("", "/")
    ):
        raise ValueError("A CorpDev Azure OpenAI account endpoint is required; the CAIS endpoint is excluded.")
    return {
        "base_url": endpoint.rstrip("/") + "/openai/v1/",
        "deployment": os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        "tenant_id": TENANT_ID,
    }


def process_request(text, client_request_id=None):
    if text.strip() != COMMAND:
        raise ValueError(f"Supported command: {COMMAND}. No arbitrary paths, uploads, approval or publishing.")
    inputs = {source: ROOT / "bundles" / "FC-03" / name for source, name in SOURCE_FILES.items()}
    return process_bundle(
        BUNDLE_ID, inputs, client_request_id,
        config=inference_config(),
        runs_root=Path.home() / "catalog-runs",
    )


async def handle_message(context, state):
    text = context.activity.text or ""
    if text.strip() != COMMAND:
        await context.send_activity(f"Send `{COMMAND}` to inspect the synthetic PDF, workbook and packaging image. Results are drafts, never published.")
        return
    await context.send_activity("Processing the three synthetic sources. One model request; no automatic retry.")
    result = await asyncio.to_thread(process_request, text, context.activity.id)
    await context.send_activity(json.dumps(result, indent=2))


async def handle_error(context, error):
    logger.error("Catalog Activity request failed", exc_info=(type(error), error, error.__traceback__))
    await context.send_activity("Catalog processing failed. No approval or publication occurred; inspect the agent logs and run manifest before retrying.")
    raise error


def main():
    from azure.ai.agentserver.activity import ActivityAgentServerHost

    logging.basicConfig(level=logging.INFO)
    inference_config()
    host = ActivityAgentServerHost()
    host.agent_app.activity("message")(handle_message)
    host.agent_app.error(handle_error)
    host.run()


if __name__ == "__main__":
    main()
