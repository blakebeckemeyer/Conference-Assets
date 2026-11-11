# Catalog Deployment Record

## Teardown status: demo unavailable, Azure group deletion still verifying

**Closeout update, November 11, 2026 01:31 UTC:** the teardown coordinator
reported verified removal of the hosted specialist and sessions, its two
blueprint applications and four principals (absent from active and deleted
Graph collections), today's Studio parent and all nine components, both
connection references, and the new `b3547013461c46ebb920b8bd97bc04c6`
connection. Dataverse creation evidence established that `DTW Tool Demo`
itself was created November 10 at 17:36:29 UTC; it was not an older tenant
asset to preserve. The demo is no longer available.

The original September-created connection was preserved. Today's `CanView`
grant was revoked through the official owner-scoped `modifyPermissions` route
after the admin-scoped route returned `ConnectionSharingNotAllowed`; read-back
showed the owner as its sole grant. Key Vault and Foundry soft-deleted objects
were purged and their lists were empty. The Azure Power Platform account and
the separate tenant billing policy `fe05b4d4-f15a-401f-8523-8a8262b95e1c`
(`DTWDemoNovember`) were deleted; the policy deletion returned HTTP 204 and its
list was empty.

**Not yet complete at this checkpoint:** resource group `dtw-tool-demo`
remained `Deleting`, with only Container Apps environment
`cae-supplier-dev-b571` remaining and a bounded ARM wait in progress. Do not
equate the removals above with verified resource-group deletion or zero
remaining charges. Final verification and the detailed
`Detroit-November-2026/TEARDOWN.md` runbook are owned by the separate closeout
change. No cloud cleanup was performed by this documentation update.

The deployment, user-reported success and temporary exception below are
historical evidence, not current availability. The exception ended with agent
deletion; no policy rollback on a live endpoint is claimed. Do not run these
historical provisioning commands to recreate the demo during closeout.

## Historical demo target: DTW hosted catalog specialist

On November 10 the user explicitly directed migration away from CorpDev to
the existing DTW project. This supersedes the historical CorpDev target below,
not the restrictions on unapproved roles, consent, publication or live tests.

- Tenant `f32b97f0-efb8-4bc3-91ee-18a6e5f635c9`, subscription
  `b571e36c-4e62-4175-b8c1-062a4cf87b16`, existing group `dtw-tool-demo`.
- Existing account/project `dtw-tool-demo-b571 / detroit-catalog`, East US.
- DTW version 1 already contained the shared processor, compatible SDK pins
  and FC-03 sources. Do not infer a missing hosted deployment from an unrelated
  classic Assistant page.
- Updated the repository adapter to require a validated `AZURE_TENANT_ID`,
  removing the hard-coded CorpDev fallback; aligned canonical source/setup
  with DTW and `AzureRbac`/Entra plus `BotServiceRbac`.
- Used the supported multipart source-version API through `Deploy-Agent.ps1`
  to update the existing specialist, without provisioning or AZD side effects.
- `supplier-catalog-specialist:2` is active. Uploaded/downloaded ZIP SHA-256:
  `7a8af1165a25909ff5221603a19dfba4c43b02549decc824b2b5e1ebf832bce7`.
  Seven allowlisted files contain the processor, adapter, requirements and
  three synthetic sources, without credentials, local config or runs.
- Endpoint configuration and runtime identity were unchanged. Activity 2.0.0,
  routing 100% `@latest`, `AzureRbac` with Entra isolation, `BotServiceRbac`
  and `not_published` were confirmed by read-back. The existing model is
  `Succeeded`; the runtime already has account-scoped Cognitive Services
  OpenAI User. No role, consent, Bot, project or model creation was needed.
- Local shared processor/adapter regressions: 40 passed; real installed-SDK
  compatibility: 1 passed; source-deployment safeguard regressions: 8 passed.
- No CorpDev writes/deletes, Studio draft edits, publication or specialist
  invocation occurred. Active deployment is not successful delegated processing.

An earlier user-run call failed Activity caller-tenant validation with
`BotServiceRbac`, request `5ecc66ee0c1e39d247d9e3c2005d7989`. This differs from
the earlier token-exchange ACL failure. Neither redeployment nor setting the
container's tenant supplies missing incoming Activity caller identity.

Subsequent authenticated Studio inspection confirmed the saved native entry
`Supplier Catalog Specialist DTW`, Agent ID `supplier-catalog-specialist`, and
connection `azureagentservice_1` / `b3547013461c46ebb920b8bd97bc04c6`.
The connection's saved resource parameter is the exact DTW project endpoint
and its authentication set is `entraIDUserLogin`. This is a different connection
from the original token-exchange error. Under the user's explicit Studio-update
authorization, main draft instructions were saved and read back after reload:
route the fixed bundle once to this specialist, preserve actual evidence and
conflicts, and do not retry, approve or publish. No processing call or
publication was made. Caller-context propagation remains unverified; no
matching gateway trace was found in the available DTW workspace query.
The historical CorpDev `BotService` exception was not copied during migration;
the later DTW-only approval and live change are recorded below.

Subsequent read-only Studio History inspection resolved the current failure
time: November 10, 2026 19:05:02 UTC (14:05 Eastern), request
`f1f5a9730707119738f159d6f4268968`. The existing Preview run selected
`SupplierCatalogSpecialistDTW`, passed `{"task":"process FC-03-NL300"}`, and its
`ToolCallTrace` recorded `Failed`, `Http403`, duration 3407 ms. The raw trace
does not expose the outgoing Foundry Activity or its normalized caller.
Studio Safety & access already selects Authenticate with Microsoft; DLP
disables No authentication, and that mode exposes no tenant input.
An exact-ID query over six DTW log tables for the preceding 24 hours returned
no rows; account/project diagnostic exports remained absent. These observations
do not establish a supported customer-side tenant-setting repair. Microsoft
needs to correlate caller identity across SendActivityV2, Bot Service and
Foundry. No additional processing attempt or configuration change was made
during this inspection.

### Approved DTW-only live compatibility exception

The user explicitly approved replacing only this specialist's `BotServiceRbac`
with legacy `BotService`, retaining direct-client `AzureRbac` with Entra
isolation. A supported endpoint-only PATCH returned HTTP 200 on November 10,
2026 at **19:18:37 UTC**. The sole configuration change was
`agent_endpoint.authorization_schemes[1].type`. Bot Service still validates
the channel, but its additional per-user RBAC/tenant check is removed.
This is a temporary synthetic-demo workaround, not a caller-context repair,
anonymous/public access or an expansion of network access.

Fresh read-back and an independent verification at **19:19:29 UTC** confirmed:

- Active `supplier-catalog-specialist:2` and the downloaded ZIP SHA-256 above
  are unchanged, as are all version objects, the source definition and runtime
  environment.
- Runtime identity `64fc7e7c-43fe-4f48-bc23-caa4541ede3d`, Activity, 100% `@latest`
  routing, Entra isolation and `not_published` are unchanged.
- The full agent comparison allowed only the approved policy change and
  service `updated_at` metadata. Two fresh pre-write reads checked for drift;
  no ETag was returned, so atomic `If-Match` protection is not claimed.
- No resources, roles, network configuration, consent, Studio binding/draft
  or publication were changed, and this policy operation invoked no processing.

Sanitized before/after state and the original full rollback array were retained
in session artifacts without tokens or headers. The
[specialist rollback procedure](../Detroit-November-2026/foundry-agent/supplier-catalog-specialist/README.md#roll-back-the-demo-exception)
restores exactly `AzureRbac`/Entra plus `BotServiceRbac` after checking for drift.
Repository `azure.yaml` keeps that default; `Deploy-Agent.ps1` deliberately
refuses legacy mode. Restore normal policy before a source deployment, real
supplier data or production; do not relax the guard.

### User-reported working demo

After the live policy change, the user reported **"Demo is working"** and asked
for documentation and a draft PR. This records user-reported operation of the
native Studio route under the approved compatibility exception. No successful
tool JSON, run ID, source-evidence record, model/token metadata, elapsed-time
capture or field-level pass result was supplied. Expected fixture values are
not substituted for that missing output.

The coordinator did not execute its separately approved Studio processing call
and made no retry. Configuration preservation is independently verified;
successful operation is user-reported. The original caller-tenant propagation
defect is not repaired or independently traced by this workaround. Restore the
secure policy as described above before normal source deployment, real supplier
data or production; separately authorize any additional processing verification.

### Access side effects to reconcile at closeout

The connector investigation made one Power Platform administrative ACL change
before the later Activity caller-tenant failure:

- Environment: `0343907b-5031-ed09-acc8-5e9701b25f1d`.
- Original connection:
  `shared-azureagentser-02b35a76-7231-4904-84d9-67d8be3d9764`.
- Added `CanView` for **Power Virtual Agents Service**, service principal
  `e4af4ca3-101d-42f7-9628-57b4ea081da5`, application
  `9d8f559b-5984-46a4-902a-ad4271e83efa`.

Read-back confirmed the grant persisted, but the reported token-exchange
denial continued. The later verified Studio binding uses connection
`b3547013461c46ebb920b8bd97bc04c6`; this session added no ACL grant to that
connection. Treat these as distinct Power Platform objects. Deleting Azure
resources does not verify removal of a Studio agent, a connection, its
credentials or the original connection's grant. These required separate
inventory and dependency checks; their subsequently verified removals are
recorded in [the teardown checkpoint above](#teardown-status-demo-unavailable-azure-group-deletion-still-verifying).

The known connection owner `87ff0a40-0f7d-4311-b847-67d416c1e258` already had
subscription-inherited **Owner** and **Foundry User** without assignment
conditions. Runtime `64fc7e7c-43fe-4f48-bc23-caa4541ede3d` already had
**Cognitive Services OpenAI User** on the DTW account. These existing grants
were reused, not created during the DTW migration or compatibility change.
Do not delete inherited owner permissions or unrelated tenant service
principals as if they were demo-created access. Restoring `BotServiceRbac`
removes the live compatibility exception but does not decommission hosting,
models or other billable resources.

Canonical setup:
`Detroit-November-2026/foundry-agent/supplier-catalog-specialist/README.md`.

## Historical CorpDev Foundry migration

The user explicitly authorized a new Foundry-hosted catalog specialist in the
existing `Detroit-InnoHubDemo` resource group, callable by Copilot Studio through
native Foundry connectivity or A2A. The earlier API-only plan below is historical;
it is not authorization to provision the root CAIS infrastructure again.

- Tenant: `1b37c04e-260e-4189-a11b-0b8609ed3df0`.
- Subscription: `ST Business Applications`
  (`eaabd6a6-7835-447a-aff4-629066fdeb75`).
- Existing resource group: `Detroit-InnoHubDemo`; resource region initially
  `eastus`, subject to hosted-agent availability verification.
- Isolated project:
  `Detroit-November-2026/foundry-agent/supplier-catalog-specialist`.
- Recipe: Foundry AZD provider, code deployment, Python 3.13; reuse the existing
  deterministic catalog extraction and validation implementation.
- Connectivity: authenticated Activity protocol with `BotServiceRbac`; no
  anonymous endpoint or workaround for tenant consent policy.
- Model: retain `gpt-6.1-sol`, version `2026-09-29`, if quota permits.
  The regional catalog lists it; usable subscription quota is not established.
- Scope: new Foundry account/project/model and minimum hosting dependencies in
  the existing CorpDev resource group only. No CAIS updates/deletes, sibling
  resource group, API app registration, client secret, or consent change.
- RBAC: inspect generated assignments before provisioning; do not apply
  unapproved assignments. The earlier Key Vault Secrets Officer grant is
  outside this work and remains unchanged.
- Cost: inference tokens, hosted CPU/memory, and any generated telemetry/storage
  incur usage charges. Concrete resources and capacity must be reviewed from
  the generated preview before provisioning; no reliable cost estimate yet.

The user approved this scoped paid plan explicitly. Infrastructure is now the
minimal `infra/corpdev.bicep` in the nested project, deployed with
`az deployment group` to the exact existing group. Do not run `azd provision`:
the ejected provider default is subscription-scoped. The approved template
creates exactly one account, one project, and one model deployment, with local
key authentication disabled and no role assignments. Code is staged from the
shared processor by `Prepare-Agent.ps1`; existing CAIS `config.json`, runs,
credentials, API configuration, and virtual environments are not packaged.

Preflight evidence: official hosted-agent documentation lists East US.
`corpdev.bicep` what-if returned exactly the account
`cog-b6qdlbxyhq22k`, its `gpt-6.1-sol` deployment (capacity 3,
GlobalStandard), and `detroit-catalog` project, all in the approved group.
No ACR, Azure Bot, Teams channel, telemetry resource, storage account, or
role assignment is in this infrastructure template. The live model call and
hosted runtime cannot be verified before the new project exists. Activity
hosting's deployment-time dependencies must still be inspected before deployment;
do not let tooling silently add Bot/channel resources or RBAC.

Execution gates:

- [x] User selected CorpDev subscription and existing resource group.
- [x] User completed isolated CorpDev AZD authentication.
- [x] Read-only East US model catalog check.
- [x] Inspect and adapt official Activity sample; scaffold only, not deployed.
- [x] Confirm hosted region and generated resource/RBAC scope; quota remains unproven until provider validation.
- [x] Review scoped plan and infrastructure preview: exactly three Create operations under the approved CorpDev group, no RBAC, deletes, or CAIS changes.
- [x] Run targeted local processor and Activity-handler checks (37 passing, model call mocked).
- [x] Complete infrastructure azure-validate, then azure-deploy retry.
- [ ] Verify deployed specialist and actual Studio delegation separately.

### CorpDev validation checklist

- [x] All infrastructure validation checks pass
  - [x] Core validation: CLI, authentication, Bicep build, group validation, what-if.
  - [x] Bicep linting (included in build).
  - [x] Azure Policy validation at the exact CorpDev group (no assignments returned).
  - [x] Static role review: no assignments in infrastructure; hosted inference
    identity permissions remain a separate runtime deployment gate.

### CorpDev Section 7: Validation Proof and Role Review

The current validation gate covers infrastructure creation only. Account and
project system identities are created by the service but this template gives
them no data access. The hosted specialist identity does not exist until code
deployment. Its inference permission and the Studio caller's project access
must be checked separately; RG Owner is not proof of data-plane access.
No new role is authorized by the current infrastructure approval.

The required `validate-deployment.ps1` passed CLI installation, isolated CorpDev
authentication, compilation, provider-side group validation and what-if.
Its compact change counter reported 4 Create; the full payload preview is the
authority for resource inventory and will be rechecked before apply.
The tests passed 37 cases across the shared processor and Activity adapter.
The policy query at the group with inherited scopes returned no assignments.

Commands (isolated `AZURE_CONFIG_DIR`, subscription explicitly pinned):

```powershell
validate-deployment.ps1 -Scope group -ResourceGroup Detroit-InnoHubDemo -Subscription eaabd6a6-7835-447a-aff4-629066fdeb75 -Template Detroit-November-2026\foundry-agent\supplier-catalog-specialist\infra\corpdev.bicep -Parameters Detroit-November-2026\foundry-agent\supplier-catalog-specialist\infra\corpdev.parameters.json
az policy assignment list --scope /subscriptions/eaabd6a6-7835-447a-aff4-629066fdeb75/resourceGroups/Detroit-InnoHubDemo --disable-scope-strict-match --subscription eaabd6a6-7835-447a-aff4-629066fdeb75
.\.venv\Scripts\python.exe -m unittest test_demo test_activity_agent -q
```

The explicit parameter-file path intentionally does not exist: the helper skips
it and uses `corpdev.bicep` defaults, never the CAIS root parameter file.

First infrastructure apply created the CorpDev account and model successfully.
Project creation failed with `RequestConflict` while the model operation held
the account lock (correlation `9442478a-181e-4239-8aa6-ac7ce08defec`).
The template now serializes project creation after the model, matching the
upstream template's ordering. Revalidate and preview this ordering-only change
before retrying. No roles or extra resources were added.

Reconnect validation, 2026-11-09 16:47 -05:00: the earlier DNS failure is resolved.
CLI/authentication, Bicep compilation, provider validation, and structured what-if
all passed again. The model's existing `Microsoft.DefaultV2` policy and
`OnceNewDefaultVersionAvailable` upgrade setting are now explicit to preserve
them. The final preview contains account NoChange, model Modify solely for
service-reported `properties.currentCapacity` (requested SKU capacity remains 3),
and project Create. There are no resource deletes or role assignments. The
helper's text-based Delete counter describes nested properties, not resources.
Policy query still returns no assignments. Runtime/code deployment is not
covered by this infrastructure validation.

Infrastructure retry `detroit-foundry-corpdev` succeeded on 2026-11-09. Live
project lookup confirms `Succeeded`, project identity
`e57131a1-3e7f-478e-a892-f52ae2927d88`, and endpoint
`https://cog-b6qdlbxyhq22k.services.ai.azure.com/api/projects/detroit-catalog`.
The isolated nested AZD environment is bound to this resolved project. No CAIS
resources were changed. Canvas synchronization returned `canvas_not_open`;
the work continues in Chat and Canvas was not reopened.

The initial hosted deployment preview returned HTTP 403. The user separately
approved exactly one Foundry User assignment (`53ca6127-db72-4b80-b1b0-d745d6d5456d`)
for their CorpDev user `d3dd5b9e-4ee4-4f82-8b9d-536885870abc`, at this project only.
Assignment `91e305cb-64ca-477c-924d-feb73112ea4d` was created and persisted.
At 17:00 -05:00 the project agents GET succeeded with an empty list after
propagation. No runtime identity role is approved or assigned.

The Activity SDK was installed in the nested ignored virtual environment after
an import check found it missing. The staged host started and `/readiness`
returned HTTP 200, `{"status":"healthy"}`; the temporary process was stopped.
The 37 targeted regression tests still pass. This is not a live inference test.

Hosted deployment scope gate: reviewed official CLI `service_target_agent.go`
deploys the code, then unconditionally ensures an Azure Bot for simple Activity
agents; its postdeploy listener also prepares Teams setup. No supported no-Bot
switch was found in that path. Do not execute it under the original approval.
Deployment preview covers only selected agent properties, not Bot/channel
side effects. No specialist version, Azure Bot, or Teams channel was created.

The user subsequently approved adding the automatic Azure Bot and Teams channel
inside `Detroit-InnoHubDemo`, acknowledging potential charges. This does not
approve runtime roles, tenant consent, or publishing/sideloading a Teams app.
The successful read-only hosted preview now shows one new specialist, Activity
2.0.0, CPU 0.5, memory 1Gi, explicit CorpDev endpoint/model bindings, and no other
agent changes. The package allowlist and `.agentignore` were reviewed; SDK import,
local host startup/readiness and processor/handler regressions pass. The
infrastructure validation is complete; hosted deployment is approved with this
additional Bot/channel boundary and no automatic RBAC.

Hosted deployment succeeded: `supplier-catalog-specialist:1` is `active`, using
Python 3.13 remote code build, CPU 0.5 and memory 1Gi. The actual endpoint
configuration advertises Activity with `BotServiceRbac`. Agent instance
identity is `3d45a377-6dfd-44d8-9a22-3ef913a7e974`. The Bot
`supplier-catalog-specialist-bot-9c0d1855` is provisioned at F0; channel inventory
includes the approved Teams channel plus service-created WebChat and DirectLine
defaults. No Teams app was published or sideloaded.

The user separately approved one runtime Cognitive Services OpenAI User role
(`5e0bd9bd-7b93-4f28-af87-19fc36ad61bd`) for that agent instance identity at the
new account only. Assignment `4598ac5a-3a72-422f-b6a0-063eb7cd3df0` is present.
The project managed identity has no newly assigned role. The official hosted
token-service contract confirms `ManagedIdentityCredential()` selects the
current agent instance, not the project identity.

Evaluation-suite generation was offered after deployment; the user chose to
defer it and finish connectivity. No paid evaluation job was started.
The retail pricing lookup for the exact GlobalStandard gpt-6.1-sol deployment
returned no rows, so no verified price quote is available; this does not imply
free inference or hosting. Capacity 3 is a rate allocation, not provisioned
throughput. Hosting CPU/memory, inference tokens, and Studio usage remain
billable under the applicable subscription terms.

### Studio connection and failed end-to-end test

The user approved creating native Entra-user connection
`Detroit CorpDev Catalog Foundry` in Blake-DTW Innovation
(`61ac6c9117e2412ab2e926e85f3ebf62`), pointing only to the new project.
Sign-in completed without an observed new permission-consent prompt. The user
then separately approved adding Supplier Catalog Specialist to the existing
`Product Launch (copy)` Studio draft
(`a579be29-2cc6-41d7-b176-7092013096d9`). Connected-agent component
`9dfe3998-d389-41fa-bea8-3c6bf5575961` is saved and enabled. The Studio agent was
not published.

The user ran a test and reported failure at `2026-11-09T22:27:20.773Z`:
HTTP 403, "Endpoint doesn't support Azure RBAC and no valid bot service token
was provided, failing authorization", request
`f0645b812280d8c58eac60ff496ed807`, conversation
`1e6838ef-a155-4819-a567-0f0bb19be3a3`. End-to-end processing is NOT verified.
No retry was sent by this session.

Read-only diagnosis: live agent GET confirms the complete endpoint
authorization array contains only `BotServiceRbac`. This was a configuration
omission in our hosted definition: the native Studio connection uses the
signed-in user's Foundry token, which requires the `AzureRbac` scheme (or its
supported `Entra` alias). Foundry User at project scope already covers the
interaction data action; the runtime's OpenAI role governs a different,
outbound call and does not resolve inbound endpoint authorization.

Official references:

- https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/add-agent-foundry
  documents Entra user login and shows `Entra` retained beside `BotServiceRbac`.
- https://learn.microsoft.com/azure/foundry/agents/how-to/configure-agent-endpoint-authorization
  documents `AzureRbac` as the preferred current name, `Entra` as an alias,
  and preserving the full authorization array when updating.

At diagnosis, the proposed correction was NOT applied: obtain separate approval to add
`AzureRbac` with `isolation_key_source.kind: Entra` alongside the existing
`BotServiceRbac`, preserving Activity and all other endpoint settings. Then
use the supported `azd ai agent endpoint update` path; no new agent version,
Bot, connection, role, app registration, or consent is required by that
configuration correction. Do not retry the synthetic test without approval.

### Approved endpoint-authentication correction applied

On November 9, 2026, the user approved: "Ok, go ahead and make that correction."
Updated the specialist's durable `azure.yaml` to retain `BotServiceRbac` and
add `AzureRbac` with `isolationKeySource.kind: Entra`. Using the isolated
AZD/CLI stores and environment `detroit-corpdev`, ran:

```text
azd ai agent endpoint update supplier-catalog-specialist -e detroit-corpdev --no-prompt
```

The endpoint-only update succeeded. Authenticated read-back confirmed exactly
two schemes: `AzureRbac` with `isolation_key_source.kind: Entra`, and
`BotServiceRbac`. Comparison against the saved pre-update endpoint confirmed
all other endpoint fields were unchanged, including Activity, version routing,
and `not_published` status. Version `supplier-catalog-specialist:1` remains
`active`; no new version was deployed.

No roles, consent, Bot, connection, CAIS resources, or Studio publication were
changed. No synthetic test was retried. End-to-end processing remains
unverified pending a separately authorized Studio test.

### Second user-run Studio test: Activity caller tenant missing

The user reported another failed test at `2026-11-09T22:39:15.284Z`:
HTTP 403, "BotServiceRbac authorization requires a valid Entra tenant id for
the activity caller", request `26438ebac48a82b2b0ffa13af6cde872`,
conversation `c7134eaa-0414-4868-b8d4-622c83676879`.

Read-only inspection confirmed the live endpoint still contains both approved
schemes (`AzureRbac` with Entra isolation and `BotServiceRbac`). Studio
Settings > Security > Authentication already has Authenticate with Microsoft
selected; multi-tenant support is unchecked and Save is disabled. Thus,
enabling Microsoft authentication is not an outstanding configuration fix.

The second error identifies missing/invalid Activity-caller tenant context,
not a missing model role or proof of successful agent execution. The connector
connection's Entra identity and the Activity's end-user identity are distinct.
The available connector reference exposes no documented tenant-ID input for
the native SendActivity operation. The exact outgoing server-side Activity
payload has not been captured, so whether this is preview-context propagation
or a connector/service compatibility defect remains unresolved.

Do not fabricate tenant claims, grant additional roles, switch to legacy
BotService, or broaden access to BotServiceTenant as a workaround. No further
authentication, publication, connection, or deployment changes were made, and
this session sent no test message. An authenticated-channel comparison would
require separate publication/test approval; otherwise escalate to Microsoft
with both request IDs and the verified endpoint/authentication configuration.

### Explicitly approved demo-only Bot Service exception

The user requested broader Foundry security for the demo. Before applying any
change, this session explained the exact consequence: replace only this
specialist's `BotServiceRbac` with legacy `BotService`, retaining `AzureRbac`;
Bot Service tokens remain required, but no end-user tenant/Foundry-role check
is applied on that path. The user selected "Approve demo-only BotService change".
This approval did not include publication, roles, or another test.

Updated durable `azure.yaml` and applied the supported endpoint-only update
with the isolated auth stores and environment `detroit-corpdev`. Live GET
confirmed exactly `AzureRbac` with Entra isolation and `BotService`.
Comparison with the pre-update endpoint confirmed Activity, routing, and
`not_published` status were unchanged; version 1 remains active.

No roles, connections, Bot resources, consent, CAIS resources, or agent versions
were created or changed. No test message was sent. End-to-end connectivity is
still unverified. This legacy compatibility exception is demo-only; restore
`BotServiceRbac` in source/live configuration after addressing identity
propagation and obtaining approval, rather than carrying it into production.

### GitHub Copilot harness HTTP 502: concrete hosted SDK failure

The user supplied a failed `SupplyCatalogue` tool call for
`process FC-03-NL300`, duration 10,477 ms, connector client request ID
`1270c46b-113a-4411-8293-cd12aa34c688`, HTTP 502 with upstream internal_error.
This generic response alone does not establish that it has the same root
cause as the earlier blueprint mismatch.

Read-only status and session inspection found active version 1 and hosted
session `a41c99a8798d38aef92401acfa70a8aea8d06e1919e4fd3960ac7e6aeb632d6`.
Logs at `2026-11-10T03:31:23Z` show inbound Activity on channel `pva-studio`,
then HTTP 500 before the application handler:
`ClaimsIdentity.__init__() got an unexpected keyword argument 'is_authenticated'`.
The stack is Activity SDK `_m365_bridge.py`, `_build_outbound_claims`.
Startup/readiness succeeded; this is a turn-path failure, not proof of catalog
processing or an additional permission requirement.

The deployed Activity SDK is pinned to 1.0.0b1; installed Agents SDK 1.9.0
has no `is_authenticated` constructor parameter. Inspection of published
Activity SDK wheels confirms b1-b3 pass that argument while b4 removes it.
Updated local requirements to Activity SDK 1.0.0b4 and pinned the three direct
Agents SDK packages to 1.9.0. Added `test_activity_sdk.py` using the real SDK
classes: reproduced the old TypeError, then passed after the upgrade.
`pip check` passed and all 37 shared processor/adapter regressions passed in
their existing environment. No live deployment or additional test was sent.

Logs also show `https://placeholder.copilot-studio.local/callback` as the
Activity service URL. That is a potential later reply-delivery blocker, not
the exception that caused this captured request to fail. Do not claim that
the SDK correction proves end-to-end integration. Await approval before
deploying a new specialist version; retain the existing approved scope.

The user subsequently approved the dependency-fix deployment as one new
version of the existing specialist, with no new infrastructure, roles,
publication, or security changes.

Dependency-only validation checklist (existing environment, no provisioning):

- [x] All validation checks pass.
  - [x] AZD installation and Foundry service schema/preview.
  - [x] Existing environment, authentication, subscription/location.
  - [x] Build verification: real SDK compatibility test and shared regressions.
  - [x] Package validation: staging allowlist and code-deploy preview.
  - [x] Provision preview, Docker, Aspire and new-resource policy checks:
    not applicable; infrastructure unchanged and provisioning prohibited.
  - [x] Static role verification: no role resources changed or added.

#### Section 7: Dependency-fix validation proof (November 10, 2026 UTC)

- Isolated AZD 1.37.3 `auth login --check-status`: authenticated CorpDev.
- Existing `detroit-corpdev` environment: exact approved tenant/subscription
  and project ARM ID/endpoint, East US. The empty generic AZURE_RESOURCE_GROUP
  value is not used to provision; the project ARM ID binds the deployment to
  the existing Detroit-InnoHubDemo group.
- `python -m unittest test_activity_sdk -q`: 1 passed with real SDK classes
  after reproducing the deployed TypeError before upgrading.
- `pip check`: no broken requirements.
- Shared `python -m unittest test_demo test_activity_agent -q`: 37 passed.
- `Prepare-Agent.ps1`: exact allowlist staged without credentials/config.
- `azd deploy supplier-catalog-specialist --preview --no-prompt -e detroit-corpdev`:
  no service-configuration changes. Preview explicitly excludes dependency
  contents, which were separately inspected in the package.
- `azd package supplier-catalog-specialist --no-prompt -e detroit-corpdev`:
  succeeded. ZIP inspection: only ignore file, demo.py, main.py,
  requirements.txt and the three synthetic sources. Requirements contain
  Activity 1.0.0b4 and Agents SDK 1.9.0 pins.
- Static RBAC review: no infrastructure edits in this correction and no
  new role assignments. Existing model/user roles are preserved.
- No provision/up command, new infrastructure, publication, or security
  change is authorized by this dependency-only deployment.

#### Dependency-fix deployment result

After completing azure-validate and invoking azure-deploy, ran the approved
single-service `azd deploy supplier-catalog-specialist --no-prompt -e detroit-corpdev`.
It succeeded in 1 minute 24 seconds. Read-back confirmed
`supplier-catalog-specialist:2` is `active`, using the new package hash
`3f643c5a87a025e88684832f24d1e9e90bd093ae0e88c4d7f692b68f66aee331`.
The endpoint retains Activity, `@latest` 100% routing, `AzureRbac` with Entra
isolation, legacy `BotService`, and `not_published`.

Instance identity remains `3d45a377-6dfd-44d8-9a22-3ef913a7e974`; its existing
account-scoped Cognitive Services OpenAI User role is still present.
The deployment reused the existing Bot; inventory contains only the same
`supplier-catalog-specialist-bot-9c0d1855`. No provision/up command, new role,
connection, security change, Teams publication, or CAIS change occurred.
Evaluations remain deferred per the user's prior decision.

No live invocation was sent. The existing session is pinned to version 1,
so the next user-run comparison needs a new Studio conversation to select
version 2. A successful dependency deployment is not end-to-end catalog
processing; the potential placeholder callback issue remains unverified.

#### Presenter-reported success and conference preparation

The user subsequently reported: "It now works in the github copilot harness."
Record this as user-confirmed working delegation after v2, not a successful
payload independently inspected here. Earlier placeholder-callback observations
are not a confirmed remaining blocker. The exact working GitHub-harness agent
must be used for rehearsal; do not assume the standard-harness Product Launch
(copy) draft is the one that succeeded.

The user selected preparation of the standalone 30-minute Foundry talk.
Updated the existing attendee guide, slide speaker notes, run-of-show and
README to show the actual single FC-03 route and distinguish broader design
illustrations from built features. Actual run capture, field-level checks and
timed rehearsal remain required. No cloud changes or model calls were made
as part of presentation preparation.

Scaffold note: sample adoption copied local files but then reported that
`--agent-name` could not be applied. No provisioning command was executed.
Inspect and correct the generated project rather than reinitializing the
existing CAIS project or assuming initialization succeeded.

Generated: 2026-11-09 10:06 -05:00

---

## 1. Project Overview

**Goal:** Prepare an AZD path to deploy the updated Supplier Catalog Processor API image and its approved Entra authentication configuration to the existing Container App only.

**Path:** Modify Existing

**Deployment boundary:** The plan-preparation request did not authorize deployment. A later explicit approval authorized one existing Container App revision and its image in the existing ACR only. No resource creation, broad infrastructure provisioning, identity/RBAC/consent changes, or unrelated deployment was authorized or performed.

## 2. Requirements

| Attribute | Value |
|-----------|-------|
| Classification | Conference proof of concept |
| Scale | Small; one existing app, max 1 replica |
| Budget | Reuse existing resources; no new recurring resources |
| Subscription | CAIS-I-T-SUB-01 (`c4fb1c99-fb99-4dc1-9926-a3a4356fd44a`) |
| Resource group | `CAIS_016_InnovationHub` (existing group location: `centralus`) |
| Resource location | `eastus` (existing Container App and dependencies) |

### Policy constraints

The Azure Policy assignment query including inherited scopes returned no assignments. Recheck if the target policy configuration changes before deployment.

## 3. Components Detected

| Component | Type | Technology | Path |
|-----------|------|------------|------|
| Supplier Catalog Processor | API | Python 3.12, FastAPI, Docker | `Detroit-November-2026/foundry-demo` |

## 4. Recipe Selection

**Selected:** AZD with Bicep for the completed image deployment. For the Studio-owned identity migration, Azure CLI configuration-only update of the existing Container App; reuse the deployed image without building or pushing another one.

**Rationale:** Microsoft Learn documents a dedicated per-service Bicep module for revision-based `azd deploy`. The root `infra/main.bicep` provisions six infrastructure/role-assignment modules and is expressly excluded from this API-only path. `azure.yaml` pins both the service's resource name and resource group, and selects `infra/api.bicep`; the deployed Container App currently lacks an `azd-service-name` tag, so the name is explicit rather than discovered by tag.

The installed AZD version is 1.33.0. Its versioned schema supports the `module`, `resourceName`, and `resourceGroup` service properties used here. Microsoft Learn's current Container Apps workflow documents the dedicated Bicep revision-based deployment. No Container Apps Express features are used. AZD authentication was performed in a separate `AZD_CONFIG_DIR` under session state; the shared AZD login was checked afterward and remained unchanged.

References: [AZD Container Apps workflows](https://learn.microsoft.com/azure/developer/azure-developer-cli/container-apps-workflows) and [azure.yaml schema](https://learn.microsoft.com/azure/developer/azure-developer-cli/azd-schema).

## 5. Architecture

**Stack:** Existing Azure Container Apps deployment

### Service mapping

| Component | Azure Service | Existing configuration |
|-----------|---------------|------------------------|
| Supplier Catalog Processor | Container App `ca-supplier-dev-f736` | East US; 0.5 vCPU / 1 GiB; `Single` revision mode; min 0 / max 1 replica; ingress port 8000 |

### Existing dependencies (referenced, not provisioned)

| Resource | Purpose | Planned change |
|----------|---------|----------------|
| `cae-supplier-dev-f736` | Container Apps environment | None |
| `crsupplierdevf736` | Existing image registry | Push updated API image only |
| System-assigned Container App identity | ACR pull and Foundry access | None |
| Existing `AcrPull` assignment | Pull images from existing ACR | None |
| Existing Foundry account `dtw-tool-demo` | API's managed-identity inference target | None |

The new API configuration sets `CATALOG_ALLOWED_TENANT_IDS` to the confirmed Studio tenant, `CATALOG_API_AUDIENCE` to the API client ID GUID, and `CATALOG_API_SCOPE` to `catalog.process`; it removes the old `CATALOG_TENANT_ID` setting. No token, secret, registration, consent, role, or Key Vault changes are included. The existing Key Vault Secrets Officer grant is out of scope and remains untouched.

### Deployment and rollback boundary

The approved deployment used `azd deploy api --no-prompt` from the repository root with the isolated AZD environment. `AZURE_CONTAINER_REGISTRY_ENDPOINT` was set there to the existing registry login server after AZD reported it missing; shared authentication state was not changed. Because no local Docker/Podman runtime is installed, `docker.remoteBuild: true` built the image remotely. The service applied only `infra/api.bicep` to the named existing app. Azure reports the new revision ready and healthy. Do not run `azd up`, `azd provision`, the root `infra/main.bicep`, or any role-assignment template as part of this API-only update.

Before any future deployment, rerun a resource-group what-if against `infra/api.bicep`. Proceed only if it reports exactly one `Modify` for `Microsoft.App/containerApps/ca-supplier-dev-f736`, with no create/delete and no other resource type. The current revision is ready and healthy, `/health` responds successfully, and missing-token requests are rejected with HTTP 401. Authenticated processing is not yet verified: isolated sign-in succeeded in the Studio tenant, but scoped token acquisition returned `AADSTS65001` and `AADSTS650052`, indicating the requested API scope is not currently issuable there without tenant-side consent/configuration. No consent was granted and no authenticated processing request was sent. Do not change identity, consent, RBAC, or deployment scope without separate approval.

## 6. Provisioning Limit Checklist

This plan updates an existing resource and creates no Azure resources.

| Resource Type | Number to Deploy | Total After Deployment | Limit/Quota | Notes |
|---------------|------------------|------------------------|-------------|-------|
| `Microsoft.App/containerApps` | 0 new; 1 update | 1 existing app | `az quota list` returned no quota rows for Microsoft.App in East US; no new app/environment quota is requested | A revision rollout may briefly use an additional replica. The quota response does not establish spare replica capacity. |
| `Microsoft.App/managedEnvironments` | 0 | Existing environment unchanged | Not applicable to this update | Existing environment is `cae-supplier-dev-f736`. |
| `Microsoft.ContainerRegistry/registries` | 0 | Existing registry unchanged | Not applicable to this update | Updated API image is pushed to the existing ACR. |
| `Microsoft.Authorization/roleAssignments` | 0 | Existing assignments unchanged | Not applicable to this update | No RBAC changes. |

**Status:** No new Azure resource quota is consumed by the planned resource set. A transient extra revision/replica is possible; available Container Apps quota/capacity could not be established from the empty quota response and must not be assumed.

### Execution Checklist

### Phase 1: Plan
- [x] Analyze workspace and current Container App.
- [x] Confirm target subscription, resource group, and region from the previously approved deployment scope.
- [x] Inspect the existing Container App, ACR identity binding, and `AcrPull` assignment read-only.
- [x] Check subscription-scope Azure Policy assignments.
- [x] Select an API-only AZD/Bicep service module; exclude the broad root module.
- [x] User authorized this local plan preparation and validation only.

### Phase 2: Local preparation
- [x] Add an AZD service definition pinned to the existing app and resource group.
- [x] Add an API-only Bicep module and parameters for the existing app.
- [x] Create a local AZD environment with the confirmed subscription, location, resource group, and current image reference; its files are ignored by Git.
- [x] Run AZD schema, Bicep, policy, and direct read-only deployment validation.
- [x] Run the focused API tests and inspect the Docker context; validate the Docker build remotely with `--no-push`.

### Phase 3: Validation
- [x] AZD 1.33.0 is installed; `azure.yaml` passed official schema validation.
- [x] Local AZD environment contains the exact approved subscription, region, resource group, and current deployed image.
- [x] Isolated AZD sign-in succeeded in the target resource tenant; the shared AZD login remains unchanged.
- [x] `azd provision --preview --no-prompt` succeeded and showed one Container App modification; all other listed existing resources were skipped.
- [x] Direct `az deployment group validate` succeeded and the read-only what-if showed one app deployment and eight ignored existing resources.
- [x] Bicep compilation, 29 Python unit tests, Docker context path inspection, and app-only RBAC review passed.
- [x] Azure Policy assignment query, including inherited scopes, returned no assignments.
- [x] `azd package api` completed successfully; no local artifacts were produced for the remote-build Container App service.
- [x] ACR remote Docker build completed successfully using `--no-push`; the build returned no output image.
- [x] Read-only verification confirmed the deployed app is still on revision `ca-supplier-dev-f736--0000002` with its existing `:latest` image; only the existing `latest` tag is present.
- [x] Record commands and outcomes in Section 7.
- [x] All plan-validation checks completed; at that point no image had been pushed and no app deployment had been performed.

### Phase 4: Deployment
- [x] Separate approval received for the API-only image push and deployment; no connector, client, consent, role, or unrelated resource changes were authorized.
- [x] Set the existing ACR endpoint in the isolated AZD environment and successfully ran `azd deploy api --no-prompt`.
- [x] Verify exact target, image, active revision readiness, `/health`, and no-token rejection.
- [ ] Authenticated synthetic FC-03 processing remains blocked pending Studio-tenant admin review and any separately approved consent/configuration; no token was issued, no consent was granted, and no authenticated request was sent.

### Phase 5: Studio-owned API identity migration

The user authorized implementing the Studio-tenant-owned API identity. Created
single-tenant application `c1cfcc13-f250-45d7-ad61-03d4c72677c1` (object
`3411ab4f-4fbe-4bcc-bf6f-ad01476342d0`) and its local service principal
`156ab316-88c8-4e3f-9900-885b354a3943` in Studio tenant
`1b37c04e-260e-4189-a11b-0b8609ed3df0`. Exposed only admin-controlled delegated
`catalog.process`, scope ID `64ed37ef-d850-4cb0-9846-985a5d52470f`, with v2
access tokens. No credentials, downstream Graph permissions, client
preauthorization, or consent grants were added. The old registration and
Key Vault grant remain untouched.

Planned rollout: change only `CATALOG_API_AUDIENCE` on
`ca-supplier-dev-f736` to the new client ID, retaining current image
`crsupplierdevf736.azurecr.io/supplier-catalog-api/api-supplier-dev-f736:azd-deploy-1794245037`,
Studio tenant issuer allowlist, required scope, and resource-tenant managed
identity. No new Azure resources, image build/push, role changes, or connector
creation. Rollback, if authorized, restores the previous audience
`bddf150f-1313-4e96-bf90-922f25ee29b8`; do not delete either registration.

- [x] All validation checks pass:
  - [x] Core CLI/auth, Bicep compile, target ARM validation and what-if.
  - [x] Existing-image reuse; no Docker build required for an environment-only update.
  - [x] Azure Policy validation.
  - [x] Focused Python API/contract tests using the existing virtual environment.
- [x] Deploy only the audience configuration change and verify live settings, image, identity, readiness, health, and no-token rejection.
- [ ] Obtain an authorized scoped Studio token before the FC-03 request. Local app ownership does not waive admin consent policy.

## 7. Validation Proof

| Check | Command Run | Result | Timestamp |
|-------|-------------|--------|-----------|
| AZD install | `azd version` | ✅ Pass: 1.33.0 | 2026-11-09 10:12 -05:00 |
| AZD schema | `azure-azd validate_azure_yaml` on `azure.yaml` | ✅ Pass: valid against stable schema | 2026-11-09 10:12 -05:00 |
| AZD local target environment | `azd env get-values` | ✅ Pass: exact subscription, East US, resource group, and existing image reference | 2026-11-09 10:12 -05:00 |
| Isolated AZD sign-in | `AZD_CONFIG_DIR=<session-state>\azd-isolated; azd auth login --tenant-id 6aab181b-a190-4247-a5d7-cb792347c7fb --use-device-code` | ✅ Pass: target tenant sign-in succeeded; shared AZD profile unchanged | 2026-11-09 12:06 -05:00 |
| AZD provision preview | `AZD_CONFIG_DIR=<session-state>\azd-isolated; azd provision --preview --no-prompt` | ✅ Pass: one Modify for `ca-supplier-dev-f736`; existing dependencies skipped; no resource create/delete | 2026-11-09 12:10 -05:00 |
| Bicep compile | `az bicep build --file infra\api.bicep --stdout` | ✅ Pass | 2026-11-09 10:12 -05:00 |
| ARM template validation | `az deployment group validate` for `infra\api.bicep` and the temporary target parameters | ✅ Pass: provisioning state `Succeeded` | 2026-11-09 10:12 -05:00 |
| ARM what-if | `az deployment group what-if` for `infra\api.bicep` | ✅ Pass: one `Microsoft.App/containerApps/ca-supplier-dev-f736` update; eight existing resources ignored; no create/delete | 2026-11-09 10:12 -05:00 |
| API tests | `python -m unittest discover -s Detroit-November-2026\foundry-demo -p test_demo.py` | ✅ Pass: 29 tests | 2026-11-09 10:12 -05:00 |
| Docker context | Required source paths checked; no `docker build` run | ✅ Pass: required files present | 2026-11-09 10:12 -05:00 |
| Static RBAC review | Search `infra\api.bicep` for role assignments | ✅ Pass: no role-assignment resource | 2026-11-09 10:12 -05:00 |
| Subscription and inherited policy | `az policy assignment list --scope /subscriptions/<id> --disable-scope-strict-match` | ✅ Pass: no assignments returned | 2026-11-09 12:12 -05:00 |
| AZD packaging | `AZD_CONFIG_DIR=<session-state>\azd-isolated; azd package api --output-path .azure\package-check\api` | ✅ Completed; AZD reported no package artifacts for this remote-build service | 2026-11-09 12:11 -05:00 |
| Remote Docker build | `az acr build --subscription <id> --resource-group CAIS_016_InnovationHub --registry crsupplierdevf736 --file Dockerfile --platform linux --no-push --no-logs .` from the API directory | ✅ Pass: ACR run `ca2` succeeded; no image output/push | 2026-11-09 12:13 -05:00 |
| Post-build app/registry check | `az containerapp show` and `az acr repository show-tags` | ✅ Pass: revision `ca-supplier-dev-f736--0000002` and deployed image unchanged; repository still has only `latest` | 2026-11-09 12:14 -05:00 |
| Isolated AZD registry endpoint | `azd env set AZURE_CONTAINER_REGISTRY_ENDPOINT crsupplierdevf736.azurecr.io` | ✅ Pass: set only in the isolated AZD environment after the first deploy attempt identified it as missing | 2026-11-09 |
| API deployment | `azd deploy api --no-prompt` | ✅ Pass: deployed only the approved API service; endpoint `https://ca-supplier-dev-f736.bluedesert-75e2f545.eastus.azurecontainerapps.io`; image `crsupplierdevf736.azurecr.io/supplier-catalog-api/api-supplier-dev-f736:azd-deploy-1794245037` | 2026-11-09 |
| Post-deployment Container App state | Azure Container Apps list and isolated `az containerapp show` / revision list | ✅ Pass: exact subscription and app; provisioning `Succeeded`; revision `ca-supplier-dev-f736--0000003` active, `Healthy`, 100% traffic; system-assigned identity retained | 2026-11-09 12:24 -05:00 |
| API health | `GET /health` | ✅ Pass: HTTP 200, `{"status":"ok"}` | 2026-11-09 |
| Missing-token handling | `POST /v1/catalog/process` without Authorization | ✅ Pass: HTTP 401; no processing request was authorized or sent | 2026-11-09 |
| Isolated Studio-tenant sign-in | `az login --tenant 1b37c04e-260e-4189-a11b-0b8609ed3df0 --use-device-code --allow-no-subscriptions` using isolated Azure CLI configuration | ✅ Pass: signed in as the previously identified Studio connection identity; isolated profile only | 2026-11-09 |
| Studio-scoped token acquisition | `az account get-access-token --tenant 1b37c04e-260e-4189-a11b-0b8609ed3df0 --scope api://bddf150f-1313-4e96-bf90-922f25ee29b8/catalog.process` using isolated Azure CLI configuration | ⚠️ Blocked: AADSTS65001 and AADSTS650052; Studio-tenant consent/configuration is needed before a token can be issued. No consent was granted, no token was returned, and no authenticated API request was made. | 2026-11-09 |
| Studio-owned application and service principal | Explicit-tenant Graph application create, `az ad app update --identifier-uris`, `az ad sp create`, then `az ad app show` | Pass: local single-tenant app and service principal created; v2 tokens, only admin-controlled `catalog.process`; no credentials, client preauthorization, consent, or Graph API permissions added | 2026-11-09 |
| Audience migration validation | azure-validate `validate-deployment.ps1`, group scope, `infra/api.bicep`, resolved session parameters with the existing image | Pass: CLI/auth, Bicep compile, ARM validation and what-if. Parsed resource-level JSON confirms one Container App Modify, no resource Create/Delete. Text helper counts nested property changes, not resources. Registry reference and probe ordering are what-if artifacts; rollout uses `az containerapp update --set-env-vars` for the audience only, not a full-template apply | 2026-11-09 |
| Audience migration policy and tests | Subscription/inherited policy query; existing `.venv\Scripts\python.exe -m unittest discover` | Pass: no policy assignments returned; 29 tests passed. Default system Python lacked FastAPI; existing project virtual environment succeeded without installing dependencies | 2026-11-09 |
| Audience-only rollout | `az containerapp update --set-env-vars CATALOG_API_AUDIENCE=c1cfcc13-f250-45d7-ad61-03d4c72677c1` against the exact existing app/subscription | Pass: revision `ca-supplier-dev-f736--0000004` ready, Healthy, 100% traffic. Image and managed identity unchanged. No build/push, role changes, or full-template deployment | 2026-11-09 |
| Post-rollout endpoint verification | `GET /health`; no-token `POST /v1/catalog/process` | Pass: HTTP 200 `{"status":"ok"}` and HTTP 401 `invalid_token`. First health request timed out during cold start; subsequent request succeeded after readiness. Health is not an authenticated processing test | 2026-11-09 |
| New local API consent inventory | Read-only Graph `oauth2PermissionGrants` filter by resource service principal `156ab316-88c8-4e3f-9900-885b354a3943` | No grants returned. Silent CLI token request did not complete and was stopped; no token returned and no processing call sent. Admin approval remains necessary for the new local API's delegated scope; creating its registration does not waive consent policy | 2026-11-09 |
| Identity consistency regression | Existing `.venv\Scripts\python.exe -m unittest discover` | Pass: 30 tests, including consistency between single-tenant connector metadata, OpenAPI scope, and both IaC parameter files | 2026-11-09 |

**Validated by:** azure-validate workflow
**Validation timestamp:** 2026-11-09 12:15 -05:00

## 8. Files to Generate

| File | Purpose | Status |
|------|---------|--------|
| `.azure/deployment-plan.md` | API-only scope, resource inventory, safeguards, and validation record | ✅ |
| `.azure/validate-status.json` | Azure validation workflow checkpoint | ✅ |
| `.azure/.gitignore` | Keeps local AZD environment state out of Git while exposing the plan and validation record | ✅ |
| `azure.yaml` | Single-service AZD deployment pinned to the existing Container App | ✅ |
| `infra/api.bicep` | Dedicated app-only revision deployment template | ✅ |
| `infra/api.parameters.json` | Existing app parameters and AZD image reference | ✅ |
| `infra/main.bicep` | Existing broad infrastructure entry point; unchanged and excluded | Unchanged |

## 9. Next Steps

> Current: Studio-owned API registration and service principal created; audience-only rollout complete. Authenticated processing and Studio connector remain pending.

1. Obtain policy-compliant approval for the intended client to use the new local API scope `api://c1cfcc13-f250-45d7-ad61-03d4c72677c1/catalog.process`. No grant or preauthorization was added. If consent is prohibited even for local applications, stop: local ownership solves foreign service-principal creation, not the policy restriction.
2. Verify the scoped token and run FC-03 only after that approval. A Studio connector client and workflow have not been created.
