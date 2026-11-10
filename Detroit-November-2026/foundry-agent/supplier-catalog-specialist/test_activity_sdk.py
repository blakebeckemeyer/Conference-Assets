import unittest

from azure.ai.agentserver.activity._m365_bridge import _build_outbound_claims
from microsoft_agents.hosting.core import ClaimsIdentity


class ActivitySdkCompatibilityTests(unittest.TestCase):
    def test_hosted_outbound_claims_use_installed_agents_sdk(self):
        identity = _build_outbound_claims(
            ClaimsIdentity,
            digital_worker=False,
            is_hosted=True,
            bot_app_id="test-agent-instance",
        )
        self.assertIsInstance(identity, ClaimsIdentity)
        self.assertFalse(identity.allow_anonymous)
        self.assertEqual(identity.authentication_type, "Bearer")
        self.assertEqual(identity.claims["appid"], "test-agent-instance")


if __name__ == "__main__":
    unittest.main()
