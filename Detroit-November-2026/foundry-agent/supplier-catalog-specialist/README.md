# CorpDev Supplier Catalog Specialist

This is the Foundry-hosted adaptation of the existing catalog processor, not
the CAIS REST API and not a replacement of the earlier conference assets.
It uses the official [Activity host sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/activity/echo)
and requests authenticated Activity connectivity for native Copilot Studio delegation.

**Status:** CorpDev infrastructure and hosted specialist version 2 are deployed.
The specialist is `active` with Activity 2.0.0, `AzureRbac` (Entra isolation),
and legacy `BotService` (explicitly approved for this demo only). The local
Activity host returns HTTP 200 from `/readiness`. The native Studio connection
and connected-agent draft entry are saved. Earlier calls failed as described
below; after deploying v2, the presenter reported successful processing in the
GitHub Copilot harness. Field-level rehearsal and a saved actual result are
still required before the conference. Use the working GitHub-harness agent,
not the earlier standard-harness agent by assumption.

**Authentication correction applied November 9, 2026:** the user separately
approved adding `AzureRbac` with Entra isolation alongside `BotServiceRbac`.
The source definition and live endpoint now contain both schemes. Read-back
confirmed Activity, routing, and publication state were unchanged; version 1
remains active. No role, consent, Bot, or connection change was made.
The user's subsequent Studio test failed with a different HTTP 403:
`BotServiceRbac authorization requires a valid Entra tenant id for the activity caller`
(November 9, 2026, 22:39:15 UTC). Both endpoint schemes remain configured,
and Studio already has Authenticate with Microsoft selected. Activity caller
identity propagation is unresolved; no additional role is indicated by this
error. End-to-end processing remains unverified. Do not weaken authorization,
publish, or send another test without approval.

**Demo-only authorization exception:** after reviewing the security consequence,
the user explicitly approved replacing `BotServiceRbac` with `BotService` on
this specialist. The endpoint-only update succeeded, and live read-back
confirmed `AzureRbac` with Entra isolation plus `BotService`; Activity, routing,
publication state, and active version 1 were unchanged. Bot Service tokens
remain required, but the Bot Service path no longer checks the end user's
tenant identity or Foundry role. This is a legacy compatibility setting, not a
production recommendation. Direct Foundry-token access still uses Azure RBAC.
No new test has been sent by this session. Restore `BotServiceRbac` in source
and live configuration after resolving identity propagation and obtaining
approval; do not retain this exception for production.

**Hosted SDK failure identified:** a subsequent GitHub Copilot harness call
returned connector HTTP 502 (`clientRequestId`
`1270c46b-113a-4411-8293-cd12aa34c688`). Hosted session logs show the Activity
reached the container but failed before the handler:
`ClaimsIdentity.__init__() got an unexpected keyword argument 'is_authenticated'`.
Activity SDK `1.0.0b1` uses a constructor argument removed by Agents SDK 1.9.0.
The source now pins Activity SDK `1.0.0b4`, which removes that argument, and
the Agents SDK packages to 1.9.0. The installed-SDK compatibility regression
reproduced the old failure and passes after upgrading. The user approved the
dependency-only redeployment; version 2 is now active and receives new sessions
through the existing `@latest` route. The runtime identity, role, Activity
protocol and approved authorization settings are unchanged. Existing version 1
sessions are not upgraded in place; start a new Studio conversation for the
next user-run test. This session has not sent a test message.
Earlier logs contained a placeholder Studio callback URL. The subsequent
user-reported success means this observation is not a confirmed remaining
blocker. Preserve that distinction; no captured successful tool payload has
been inspected by this session.

Project endpoint:
https://cog-b6qdlbxyhq22k.services.ai.azure.com/api/projects/detroit-catalog

The approved project-scoped Foundry User assignment to the demo author is
present and authenticated agent-list access succeeds. A separately approved
Cognitive Services OpenAI User role grants the agent instance identity
`3d45a377-6dfd-44d8-9a22-3ef913a7e974` inference access on this account only.
The current CLI's Activity deploy path also
creates an Azure Bot and Teams channel; do not run it under the original
Studio-only approval. Deployment preview does not report those side effects.

The user separately approved that Bot and Teams channel in the same resource
group. The deployed Bot is `supplier-catalog-specialist-bot-9c0d1855` (F0).
Channel inventory also includes service-created WebChat/DirectLine defaults.
Teams app publication/sideloading, further RBAC, and consent changes remain
excluded. Evaluations were explicitly deferred. An exact model retail-price
lookup returned no rows; inference, hosting and Studio usage are not free.

Native Studio connection values:

- Project endpoint: the HTTPS endpoint above.
- Agent name / ID: `supplier-catalog-specialist`
  (current Foundry version object ID: `supplier-catalog-specialist:2`).
- Authentication: Microsoft Entra ID User Login.
- Supported command: `process FC-03-NL300`.
- Saved connection: `Detroit CorpDev Catalog Foundry`.
- Studio draft: `Product Launch (copy)`, agent
  `a579be29-2cc6-41d7-b176-7092013096d9`; connected-agent component
  `9dfe3998-d389-41fa-bea8-3c6bf5575961`.

## Boundaries

- CorpDev tenant `1b37c04e-260e-4189-a11b-0b8609ed3df0`.
- Subscription `ST Business Applications`
  (`eaabd6a6-7835-447a-aff4-629066fdeb75`).
- Existing resource group `Detroit-InnoHubDemo`, East US.
- Subsequent approvals cover one Bot/Teams channel, the demo author's
  project-scoped Foundry User role, and the agent instance's account-scoped
  Cognitive Services OpenAI User role. No further roles or Teams app
  publication/sideloading is authorized.
- Preserve the CAIS API, registrations, resources, and prior Key Vault grant.

`infra/corpdev.bicep` is resource-group scoped. Do not run `azd up`,
`azd provision`, or `azd down` in this project. The upstream Foundry provider's
default infrastructure entry point was subscription-scoped and is intentionally
not retained. Deploy infrastructure only through the reviewed group-scoped
template after validation and what-if.

## Shared code and packaging

Run `.\Prepare-Agent.ps1` from this folder. It stages an explicit allowlist into
ignored `src\catalog`: shared `demo.py`, the `activity_agent.py` entry point,
the dependency manifest, and the synthetic FC-03 PDF, workbook, and image.
Do not edit these generated copies or add local config/credentials to them.
The existing CAIS `config.json` is neither copied nor read by the adapter.

The adapter requires `AZURE_OPENAI_ENDPOINT` and
`AZURE_AI_MODEL_DEPLOYMENT_NAME`. In hosted execution it uses managed identity.
No key, client secret, or shared login profile is required by the code.
Actual runtime identity access remains a deployment verification gate.

Send exactly `process FC-03-NL300`. The handler makes one extraction request,
then reuses deterministic evidence validation. It returns a review draft:
the black-versus-red conflict must remain unresolved, width is `"25.0"` cm,
and `published` stays false. It does not accept arbitrary paths, uploads,
approval commands, or publishing. Other messages return usage instructions
without a model call. Run evidence is saved under `$HOME/catalog-runs`.

Local regression command from `..\..\foundry-demo`:

```powershell
.\.venv\Scripts\python.exe -m unittest test_demo test_activity_agent -q
```

Installed-SDK compatibility regression from this folder, after installing
`requirements.txt` in the local `.venv`:

```powershell
.\.venv\Scripts\python.exe -m unittest test_activity_sdk -q
```

Activity is asynchronous: `azd ai agent invoke` does not test this protocol.
A local Activity handler check does not prove a deployed Studio connection.
Native Studio connection needs the resolved project endpoint, deployed agent
identity, Activity endpoint with the explicitly approved authorization schemes, Entra user login and project
access. Record a real delegated FC-03 result before calling it end-to-end.

See the repository-root `.azure/deployment-plan.md` for approval, preview,
validation, deployment evidence and unresolved blockers.
