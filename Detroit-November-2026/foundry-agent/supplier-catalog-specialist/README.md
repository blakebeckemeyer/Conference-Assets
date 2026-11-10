# DTW Supplier Catalog Specialist

This is the Foundry-hosted adaptation of the existing catalog processor, not
the CAIS REST API and not a replacement of the earlier conference assets.
It uses the official [Activity host sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/activity/echo)
and requests authenticated Activity connectivity for native Copilot Studio delegation.

**Current status (November 10, 2026):** DTW is the canonical deployment target.
The existing `supplier-catalog-specialist:2` is active with Activity 2.0.0;
routing remains 100% to `@latest`. The repository default is `AzureRbac` (Entra
isolation) plus `BotServiceRbac`. Since 19:18:37 UTC, the live DTW endpoint uses
the separately approved [temporary `BotService` exception](#approved-temporary-demo-compatibility-exception)
alongside unchanged `AzureRbac`/Entra. The deployed ZIP was downloaded and its SHA-256 verified as
`7a8af1165a25909ff5221603a19dfba4c43b02549decc824b2b5e1ebf832bce7`.
It contains the shared catalog processor, Activity adapter, compatible SDK
requirements and all three synthetic FC-03 sources. No CorpDev fallback tenant
is used; the DTW live exception has its own explicit approval.

Deployment and the live policy change are verified. **The user now reports
the demo is working under the compatibility exception**; no successful tool
JSON or field-level verification artifact was supplied. Before the exception,
the November 10 19:05:02 UTC Studio
call returned `BotServiceRbac authorization requires a valid Entra tenant id
for the activity caller`, request `f1f5a9730707119738f159d6f4268968`.
The exception bypasses that additional check rather than repairing incoming
Activity identity. No Studio/Teams publication was performed.

## Canonical DTW target

| Setting | Value |
|---|---|
| Tenant | `f32b97f0-efb8-4bc3-91ee-18a6e5f635c9` |
| Subscription | `b571e36c-4e62-4175-b8c1-062a4cf87b16` |
| Existing resource group / region | `dtw-tool-demo` / East US |
| Existing account / project | `dtw-tool-demo-b571` / `detroit-catalog` |
| Project endpoint | `https://dtw-tool-demo-b571.services.ai.azure.com/api/projects/detroit-catalog` |
| Agent name / current version | `supplier-catalog-specialist` / `supplier-catalog-specialist:2` |
| Model deployment | `gpt-6.1-sol`, model version `2026-09-29`, GlobalStandard capacity 3 |
| Model endpoint | `https://dtw-tool-demo-b571.openai.azure.com/` |

The existing runtime identity is unchanged and already has Cognitive Services
OpenAI User on this DTW account. The model deployment is `Succeeded`. These
read-backs verify configuration, not a model call or an Activity turn.
CorpDev resources and the separate CAIS API remain untouched.

## Repeat a source-only deployment

While the live compatibility exception is active, the updater deliberately
refuses both preview and deployment. First [restore `BotServiceRbac`](#roll-back-the-demo-exception);
do not change the source defaults or guard to accept legacy mode.

Use PowerShell 7.1 or later and an Azure CLI profile already signed in to the exact DTW
tenant/subscription above. Use an isolated profile for a different account;
the script refuses a mismatch and never switches shared authentication.

```powershell
# From this folder. Preview stages/packages locally but makes no cloud write.
.\Deploy-Agent.ps1 -WhatIf

# After deployment approval, update only the existing hosted specialist.
.\Deploy-Agent.ps1
```

The script uses Microsoft's supported
[source ZIP update API](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent-code#update-or-version-an-agent),
not the AZD provisioning/publishing path. It packages an explicit seven-file
allowlist, fixes ZIP timestamps for repeatable hashes, posts a version update,
waits for `active`, and downloads that exact version to verify its hash.
It preserves the endpoint configuration and runtime identity and detects
unexpected changes. It never grants roles/consent, creates a Bot, publishes,
invokes the agent, or changes CorpDev. Existing `@latest` routing selects the
new version for new sessions; existing sessions can remain pinned to an older
version. Source deployment and hosting incur normal Foundry usage charges.

`azure.yaml` retains the corresponding source configuration, with
`AZURE_TENANT_ID` and `AZURE_OPENAI_ENDPOINT` explicitly supplied. Do not use
`azd up`/`provision` or the historical infrastructure template for this update.
The adapter rejects missing/invalid tenant configuration and the original CAIS
model endpoint instead of silently falling back to CorpDev or local config.

## Approved temporary demo compatibility exception

On November 10 the user explicitly approved replacing only this DTW endpoint's
`BotServiceRbac` with legacy `BotService` for the fixed synthetic demo, retaining
`AzureRbac` with Entra isolation and every other endpoint/runtime setting.
The supported endpoint-only PATCH returned HTTP 200 at **19:18:37 UTC**.
Only `agent_endpoint.authorization_schemes[1].type` changed. Independent
read-back at **19:19:29 UTC** confirmed the same active v2 and downloaded ZIP
hash above, unchanged source definition/environment and runtime identity
`64fc7e7c-43fe-4f48-bc23-caa4541ede3d`, Activity, 100% `@latest` routing and
`not_published`. No resources, roles, network configuration, consent, Studio
binding or publication were changed. See the
[deployment record](../../../.azure/deployment-plan.md) for the read-back and
processing outcome. Approval and configuration read-back are not evidence
that delegated processing succeeds.

Microsoft documents
[`BotService` as legacy compatibility](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-endpoint-authorization#bot-service-channel-authorization):
Azure Bot Service still validates the channel request, but Foundry applies no
additional user authorization rule on that channel. This removes the per-user
RBAC/tenant check; it does not repair missing caller identity. Direct clients
still need Azure RBAC. It is not anonymous access, a network-public change,
or a grant of additional Azure roles. Keep Studio's Microsoft authentication,
existing sharing, fixed synthetic inputs and prohibition on approval/publication.
Do not use this exception for real supplier data or production.

`azure.yaml` retains the secure `BotServiceRbac` default. The source-only updater
intentionally refuses a live `BotService` endpoint. Restore the normal policy
before source updates; do not weaken that safeguard to deploy during the exception.

### Reported demo outcome

After the live change, the user reported **"Demo is working"** for the native
Studio demonstration. This is user-reported success in the explicit compatibility
exception, not an independently captured successful tool response. No actual
JSON, run ID, source-evidence record, model/token metadata or measured elapsed
time was supplied; the expected fixture fields below are not observed results.
The coordinator did not execute its separately approved processing call and
did not retry. Preserve that distinction when presenting the outcome.

The original caller-context defect remains unresolved: success with the
additional check bypassed does not establish that `BotServiceRbac` now works.
Capture a real returned record for field-level rehearsal evidence; any further
processing call still needs its own approval.

### Roll back the demo exception

With the same explicitly selected DTW tenant/subscription and a Foundry-audience
management token, restore the saved original authorization array using
[Microsoft's endpoint update API](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-agent-endpoint-authorization#inspect-the-current-endpoint-configuration).
The fixed target is:

```http
PATCH https://dtw-tool-demo-b571.services.ai.azure.com/api/projects/detroit-catalog/agents/supplier-catalog-specialist?api-version=v1
Content-Type: application/merge-patch+json
Authorization: Bearer <Foundry-audience-token>

{
  "agent_endpoint": {
    "authorization_schemes": [
      {
        "type": "AzureRbac",
        "isolation_key_source": { "kind": "Entra" }
      },
      { "type": "BotServiceRbac" }
    ]
  }
}
```

The update replaces the whole scheme array. Read the current agent immediately
before applying it; expect exactly `AzureRbac`/Entra plus `BotService` and the
recorded v2, identity, routing and publication state. Stop and review any drift
rather than overwriting a concurrent change. The array above matches the saved
original in full. Read back the
agent afterward and confirm `BotServiceRbac`, Entra isolation, Activity,
unchanged routing/version/identity, source/environment and publication state.
The service returned no ETag during this change; pre-write comparison is not
an atomic conditional-update guarantee. Never log the token.
Do not add another Bot Service scheme alongside the existing one.

## Native Studio integration and remaining verification

The user-confirmed caller is
[DTW Tool Demo](https://copilotstudio.microsoft.com/environments/0343907b-5031-ed09-acc8-5e9701b25f1d/agents/781a5f55-6bc3-473d-b085-455c881026c5),
using the GitHub Copilot harness. Its saved connected agent is
`Supplier Catalog Specialist DTW` (previously observed as `supply-cat`).
Authenticated Studio read-back verified Agent ID `supplier-catalog-specialist`,
connection alias `azureagentservice_1` and connection ID
`b3547013461c46ebb920b8bd97bc04c6`, named `Detroit DTW Catalog Foundry`.
The connection uses Entra ID User Login and its saved resource parameter is
the exact canonical DTW project endpoint above. No rebind was needed.

The main Studio draft instructions now route `FC-03-NL300` to that specialist
with exactly `process FC-03-NL300`, allow one call per requested attempt,
prohibit automatic retries and fabricated results/diagnoses, and preserve
returned conflicts without approval/publication. The saved instructions
survived reload. This was a draft update, not publication or a processing test.

Read-only inspection of the user's November 10, 2026 19:05 UTC Preview history
confirms `SupplierCatalogSpecialistDTW` received exactly
`{"task":"process FC-03-NL300"}` and its tool trace failed `Http403`.
The reported caller-tenant error has request ID
`f1f5a9730707119738f159d6f4268968`. The prompt's historical tool name did not
prevent correct selection. Studio already uses **Authenticate with Microsoft**;
**No authentication** is disabled by DLP, and the selected mode exposes no
tenant field. The history is not the outgoing Foundry Activity payload and
does not establish which caller identity its gateway validated.

For an approved binding update, use the DTW project endpoint above, Microsoft
Entra ID User Login, and Agent ID `supplier-catalog-specialist` (the current
hosted agent name, not a classic `asst_` assistant ID). Follow Microsoft's
[native GH-harness Foundry instructions](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/add-agent-foundry).
Use the documented `BotServiceRbac` scheme outside the separately approved demo
exception above; neither another role nor a container tenant setting repairs
missing incoming caller-tenant context. Recheck the saved
binding before any future change, and obtain approval for draft changes, consent,
publication or a live `process FC-03-NL300` test.

The DTW workspace's last-day telemetry query had no match for the failed request
ID, and the account/project had no diagnostic export settings. No exact outgoing
Activity payload was captured. If the correct binding still fails, escalate the
request ID, failure time and endpoint/authentication evidence to Microsoft;
do not fabricate tenant claims or make further unapproved authorization changes.

Offline checks use a local virtual environment with both this folder's and
`..\..\foundry-demo\requirements.txt` dependencies installed:

```powershell
# From the repository root.
.\Detroit-November-2026\foundry-demo\.venv\Scripts\python.exe -m unittest discover `
  -s .\Detroit-November-2026\foundry-demo -p 'test_*.py' -q
.\Detroit-November-2026\foundry-demo\.venv\Scripts\python.exe -m unittest discover `
  -s .\Detroit-November-2026\foundry-agent\supplier-catalog-specialist -p 'test_activity_sdk.py' -q
Invoke-Pester .\Detroit-November-2026\foundry-agent\supplier-catalog-specialist\Deploy-Agent.Tests.ps1
```

## Historical CorpDev deployment evidence

The following records the previous deployment and its separately approved
demo-only exception. It is not DTW setup guidance, a current binding assertion,
or authorization to modify/delete CorpDev or copy its legacy security setting.

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

Historical CorpDev project endpoint:
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

Historical CorpDev Studio connection values:

- Project endpoint: the HTTPS endpoint above.
- Agent name / ID: `supplier-catalog-specialist`
  (current Foundry version object ID: `supplier-catalog-specialist:2`).
- Authentication: Microsoft Entra ID User Login.
- Supported command: `process FC-03-NL300`.
- Saved connection: `Detroit CorpDev Catalog Foundry`.
- Studio draft: `Product Launch (copy)`, agent
  `a579be29-2cc6-41d7-b176-7092013096d9`; connected-agent component
  `9dfe3998-d389-41fa-bea8-3c6bf5575961`.

### Historical CorpDev boundaries

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

The adapter requires an explicit GUID `AZURE_TENANT_ID`, `AZURE_OPENAI_ENDPOINT` and
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

Installed-SDK compatibility regression from this folder, using the shared
`foundry-demo\.venv` with both dependency manifests installed:

```powershell
..\..\foundry-demo\.venv\Scripts\python.exe -m unittest test_activity_sdk -q
```

Activity is asynchronous: `azd ai agent invoke` does not test this protocol.
A local Activity handler check does not prove a deployed Studio connection.
Native Studio connection needs the resolved project endpoint, deployed agent
identity, Activity endpoint with the explicitly approved authorization schemes, Entra user login and project
access. Record a real delegated FC-03 result before calling it end-to-end.

See the repository-root `.azure/deployment-plan.md` for approval, preview,
validation, deployment evidence and unresolved blockers.
