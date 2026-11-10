import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import activity_agent
import demo
from test_demo import SHEET_CELLS, sample


ENV = {
    "AZURE_OPENAI_ENDPOINT": "https://corpdev-catalog.openai.azure.com/",
    "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-6.1-sol",
}


class ConfigurationTests(unittest.TestCase):
    def test_explicit_corpdev_endpoint(self):
        with patch.dict(os.environ, ENV, clear=True):
            config = activity_agent.inference_config()
        self.assertEqual(config["base_url"], ENV["AZURE_OPENAI_ENDPOINT"] + "openai/v1/")
        self.assertEqual(config["tenant_id"], activity_agent.TENANT_ID)

    def test_missing_endpoint_never_uses_local_cais_config(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(KeyError):
            activity_agent.inference_config()

    def test_rejects_cais_and_invalid_endpoints(self):
        for endpoint in [
            "https://dtw-tool-demo.openai.azure.com/",
            "http://corpdev-catalog.openai.azure.com/",
            "https://corpdev-catalog.openai.azure.com.evil.invalid/",
            "https://user:password@corpdev-catalog.openai.azure.com/",
            "https://corpdev-catalog.openai.azure.com/?key=not-a-key",
        ]:
            with self.subTest(endpoint=endpoint), patch.dict(os.environ, {**ENV, "AZURE_OPENAI_ENDPOINT": endpoint}):
                with self.assertRaises(ValueError):
                    activity_agent.inference_config()

    def test_explicit_configuration_and_output_preserve_shared_validation(self):
        record = demo.validate(sample(), SHEET_CELLS)
        config = {"base_url": "https://test.invalid", "deployment": "test", "tenant_id": "test"}
        inputs = {source: demo.ROOT / "bundles" / "FC-03" / name for source, name in demo.SOURCE_FILES.items()}
        credential = object()
        with tempfile.TemporaryDirectory() as directory, patch("demo.execute", return_value={"record": record}) as execute:
            result = demo.process_bundle("FC-03-NL300", inputs, "test-activity", config=config, credential=credential, runs_root=directory)
            manifest = json.loads((Path(directory) / result["runId"] / "manifest.json").read_text())
        self.assertIs(execute.call_args.args[0], config)
        self.assertIs(execute.call_args.kwargs["credential"], credential)
        self.assertEqual(manifest["config"], config)
        self.assertEqual(record["status"], "needs_review")
        self.assertIsNone(record["color"])
        self.assertEqual(record["width_cm"], "25.0")
        self.assertFalse(record["published"])


class ActivityTests(unittest.IsolatedAsyncioTestCase):
    async def test_supported_message_returns_real_processor_result(self):
        context = SimpleNamespace(activity=SimpleNamespace(text=activity_agent.COMMAND, id="activity-1"), send_activity=AsyncMock())
        expected = {"runId": "unit-test", "record": {"published": False}}
        with patch.dict(os.environ, ENV), patch("activity_agent.process_bundle", return_value=expected) as process:
            await activity_agent.handle_message(context, None)
        self.assertEqual(process.call_args.args[:3], ("FC-03-NL300", {
            source: demo.ROOT / "bundles" / "FC-03" / name for source, name in demo.SOURCE_FILES.items()
        }, "activity-1"))
        self.assertEqual(json.loads(context.send_activity.call_args.args[0]), expected)

    async def test_unknown_command_has_no_model_request(self):
        context = SimpleNamespace(activity=SimpleNamespace(text="publish everything"), send_activity=AsyncMock())
        with patch("activity_agent.process_bundle") as process:
            await activity_agent.handle_message(context, None)
        process.assert_not_called()
        self.assertIn(activity_agent.COMMAND, context.send_activity.call_args.args[0])

    async def test_processing_failure_is_not_reported_as_success(self):
        context = SimpleNamespace(activity=SimpleNamespace(text=activity_agent.COMMAND, id="activity-2"), send_activity=AsyncMock())
        with patch("activity_agent.process_request", side_effect=ValueError("inference failed")):
            with self.assertRaisesRegex(ValueError, "inference failed"):
                await activity_agent.handle_message(context, None)
        self.assertEqual(context.send_activity.await_count, 1)


if __name__ == "__main__":
    unittest.main()
