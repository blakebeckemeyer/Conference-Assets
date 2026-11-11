# Foundry slice: PDF + spreadsheet + image to a review record

**Post-demo closeout:** the hosted specialist and today's Studio demo assets
were removed; the demo is no longer available. Resource-group deletion and
retained workspace cleanup are still being verified. See the
[teardown checkpoint](../../.azure/deployment-plan.md#teardown-status-demo-unavailable-azure-group-deletion-still-verifying)
and [teardown runbook](../TEARDOWN.md).
The route/status notes below are historical, not authorization to reprovision.

**Conference route update:** the stage demo now uses the
[DTW hosted specialist v2](../foundry-agent/supplier-catalog-specialist/README.md)
through Studio's GitHub Copilot harness. DTW deployment is active and its source
package and saved Studio binding are verified. The approved temporary DTW
`BotService` exception was applied at 19:18:37 UTC on November 10, retaining
`AzureRbac`/Entra, source v2/package, environment, identity, routing and
publication state. It bypasses additional Bot-user authorization, not channel
authentication, and does not repair caller-tenant propagation. The user
subsequently reported **"Demo is working"** under that exception; no successful
JSON, run ID, model/token metadata or field-level capture was supplied. The
coordinator did not execute its approved Studio call or retry. Do not substitute
earlier CorpDev evidence or expected fixture values for a captured DTW result.
Use the [stage run sheet](../attendee-guide.html#foundry-rehearsal), not the
historical CAIS API/custom-connector hookup below. This folder's processor and
FC-03 sources are reused by that specialist; its `config.json` still targets
the older direct-model route. No new deployment or consent is required by
opening the rehearsal guide.
The repository default remains `BotServiceRbac`; its source updater deliberately
refuses the live legacy mode. Follow the specialist guide's full-array rollback
before normal source deployment, real supplier data or production. This is
not an anonymous/public endpoint or a change to this folder's historical API.

This is a local Python application calling the existing `gpt-6.1-sol`
deployment on `dtw-tool-demo`. It is a model-calling service, not a Foundry
agent. The API can run locally or as a container. The container endpoint is
deployed at `https://ca-supplier-dev-f736.bluedesert-75e2f545.eastus.azurecontainerapps.io`.
The API's replacement registration is single-tenant and owned by the Studio
tenant (`1b37c04e-260e-4189-a11b-0b8609ed3df0`), with client ID
`c1cfcc13-f250-45d7-ad61-03d4c72677c1`. Its local service principal was
created successfully. Source/IaC and the connector contract use this new v2
audience. Healthy hosted revision `ca-supplier-dev-f736--0000004` uses it too;
the deployed image and Foundry managed identity were retained. Detailed
deployment and consent status are recorded in
`../../.azure/deployment-plan.md`. The previous resource-tenant registration
remains untouched; it is not the identity for new connector configuration.
No authenticated Studio API processing has succeeded yet. The repo
contains one fixed synthetic bundle (`FC-03-NL300`) for reproducible demo
runs; it is not a storage design for real supplier documents.

## How the end-to-end path works

1. The Copilot Studio GitHub-harness agent invokes a workflow with
   `sourceBundleId=FC-03-NL300`.
2. The workflow invokes a custom connector that sends the ID to this API.
3. The API resolves only that fixed synthetic bundle from its own deployment,
   verifies the caller's Entra token and `catalog.process` permission, and
   sends the PDF, spreadsheet facts, and image to the existing Foundry model
   deployment.
4. The Python service validates source evidence, reconciles conflicts, saves
   an auditable run, and returns a draft with `needs_review` when sources
   disagree. It never approves or publishes a catalog record.

The service has two separate identity hops: the Power Platform connector's
Entra token is validated for the incoming API call; the container uses its
Azure managed identity to call Foundry. In local development only, Foundry
access uses the isolated Azure CLI profile and the API's auth bypass is bound
to loopback.

`catalog-api.openapi.json` is the OpenAPI 2.0 contract for
`POST /v1/catalog/process`, prefilled with the deployed host, Studio tenant
authorization endpoints, and delegated scope
(`api://c1cfcc13-f250-45d7-ad61-03d4c72677c1/catalog.process`). For v2 tokens,
the API validates the bare app client ID as `aud`; the scope still uses the
application ID URI.
The scope requires admin consent. Local application ownership resolves the
foreign-service-principal creation restriction, not tenant consent policy:
the intended connector client still needs approved delegated access. No
connector client, secret, preauthorization, or consent grant was created.
`Dockerfile` packages the API and synthetic bundle; hosted startup requires
managed identity and the configured Entra API settings. Do not expose the
local unauthenticated mode.

**Verified tool route for the selected GitHub Copilot harness:** a custom REST
API isn't a direct custom-tool type. The harness supports workflows as tools;
the workflow designer supports connector actions. The proposed route for this
API is:

1. Deploy the container to an HTTPS endpoint, configure a managed identity,
   and grant that identity only the Foundry inference role needed for the
   existing deployment.
2. Register the API in Entra with the `catalog.process` delegated scope and
   configure the connector's OAuth client against that API.
3. Import the finalized OpenAPI v2 definition as a Power Platform custom
   connector.
4. In Copilot Studio's **Workflows**, create a workflow with a **When an agent
   calls the flow** trigger and **Respond to the agent** output.
5. Add the custom connector action between the trigger and response, pass the
   opaque bundle ID, and map the returned record.
6. Publish the workflow and add it to the GitHub-harness agent as a workflow
   tool.
7. In Preview/activity trace, verify the arguments, connector result, run ID and
   review status; verify unrelated questions do not invoke it.

The API caps each inference request at 70 seconds, leaving up to 30 seconds for
workflow and connector overhead within the harness's 100-second action limit.
Slow runs return an explicit failure for a human to retry deliberately; no
automatic retries are made.

Microsoft documents both the GitHub harness's custom-tool choices (MCP or
workflow) and the workflow designer's connector actions. A REST API tool is
documented for the **standard** harness, not this one. A custom MCP server that
wraps the same service is another GitHub-harness route, but adds an MCP adapter;
the workflow + custom connector path is the narrower fit for this one-shot
process-and-return operation. This verifies the tool/workflow building blocks, not tenant licensing, DLP
product documentation proves the tool/workflow building blocks, not tenant
licensing, DLP, connector import, OAuth consent, or a live Studio test. A
published workflow must respond synchronously within the documented 100-second
action limit; monitor the real inference time and keep the returned payload
small. A custom MCP server could also expose the service, but the workflow +
connector route is narrower for this request/response operation.

Official references: [GitHub-harness tools](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/add-tools-custom-agent),
[workflow tools](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/tools-add-workflow),
[workflow designer actions](https://learn.microsoft.com/microsoft-copilot-studio/workflows-experience/flow-designer),
[GitHub-harness attachments](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/attachments-overview),
[file forwarding scope](https://learn.microsoft.com/microsoft-copilot-studio/guidance/pass-files-to-connectors),
and [direct REST API tools (standard harness)](https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api).

## Run the API locally

The repo stores the generated synthetic specification PDF, workbook, and image
under `bundles\FC-03`. Regenerate them only if they are missing:

```powershell
python demo.py prepare --output-dir .\bundles\FC-03
```

In the terminal that will run the API, use the session-isolated Foundry login
and explicitly enable local-only API auth bypass. The server must bind to
loopback:

```powershell
$env:AZURE_CONFIG_DIR = 'C:\Users\<you>\.copilot\session-state\<session>\files\detroit-azure-auth'
$env:FOUNDRY_AUTH_MODE = 'azure_cli'
$env:CATALOG_ENV = 'local'
$env:CATALOG_LOCAL_AUTH_BYPASS = 'true'
.\.venv\Scripts\uvicorn.exe api:app --host 127.0.0.1 --port 8000
```

In another terminal, POST the fixed bundle ID. This makes one real, potentially
billable inference request:

```powershell
curl.exe -sS -X POST http://127.0.0.1:8000/v1/catalog/process `
  -H 'Content-Type: application/json' `
  -d '{"sourceBundleId":"FC-03-NL300","clientRequestId":"local-test-1"}'
```

The response contains the reconciled record, model/token metadata, source
bundle ID and run ID. Open `runs\<run-id>` to inspect the manifest, actual
provider response, extraction and locally validated record. Unknown bundle
IDs return 404; invalid requests return 400; Foundry failures return an error,
not a success-shaped record. The API performs no automatic retries.

For hosted use, set `CATALOG_ALLOWED_TENANT_IDS` to a comma-separated,
explicit tenant allowlist, `CATALOG_API_AUDIENCE` to the API app client ID
(GUID), and optionally `CATALOG_API_SCOPE`; leave
`CATALOG_LOCAL_AUTH_BYPASS` unset. The container uses
`ManagedIdentityCredential` for Foundry. Do not give the container developer
credentials, and do not expose the local bypass on a network.

## What to look at first

The generated `inputs\specification.pdf` says **NL-300, black, 250 mm,
24-month warranty**. `inputs\supplier.xlsx` repeats those values in the
`Products` worksheet cells A2:D2. `inputs\packaging.png` shows a **red** lamp
with the same model label. This implements the three-source FC-03 example.
The PDF is a single rasterized page, so extraction uses vision.

The model returns observations independently for each source using an enforced
JSON schema. Python parses the workbook locally, sends its values and cell
locators as text alongside the PDF and image, then checks coverage, evidence
references, PDF value support, workbook cell/value support, types and conflicts.
The XLSX is hashed in the manifest but is not uploaded as a separate model file.
Application code converts millimeters to centimeters with Decimal.
An unresolved color must be null, with both candidates retained and
`status: needs_review`. Nothing is published or automatically corrected.

**First live result (PDF + image only):** November 4 run `20261104T194827Z-de4b3c40` completed
using `https://dtw-tool-demo.openai.azure.com/openai/v1/` and deployment
`gpt-6.1-sol`. The model read black from the PDF and red from the image.
Local reconciliation produced SKU `NL-300`, color null, width `"25.0"` cm,
warranty `24`, status `needs_review` and issue `color-conflict`. Both color
candidates and their source evidence are retained. The run took 8.875 seconds
including token acquisition; reported usage was 4,184 input and 232 output
tokens. This single two-source result is not five-case coverage or an A/B
benchmark. Cost is uncalculated.

The earlier requests to the `services.ai.azure.com` gateway returned HTTP 401,
including after role assignment. The dedicated OpenAI endpoint reported by
Azure for the same resource succeeded; `config.json` now uses it.
The exact cause of the gateway rejection was not established.
Failed attempts and the successful response are retained separately in `runs`.
The first run emitted an SDK/Pydantic serialization warning. Later response
dumps suppress that union-serializer warning; the JSON payloads from both runs
were checked and their embedded parsed observations exactly match
`extraction.json` (8 and 12 observations). Offline unit-test data is never
labeled a model result.

**Three-source live result:** November 5 run `20261105T142431Z-b7940a9e`
completed on the same deployment. The model cited PDF lines, exact
`Products!A2:D2` cells and the packaging image independently. The spreadsheet
agreed with the PDF on SKU, black color, 250 mm and 24 months; the image
disagreed on color. Local reconciliation again returned `color: null`,
`color-conflict`, and `needs_review`, retaining all three color observations.
It took 17.52 seconds including token acquisition; usage was 4,282 input and
346 output tokens. The saved result was checked against the FC-03 oracle and
replayed through local validation without another model call. Cost remains
uncalculated. This is one synthetic case, not five-case coverage or an A/B
benchmark.

**For a new identity:** an authorized administrator can assign **Cognitive Services OpenAI
User** to the intended demo user at the **dtw-tool-demo resource** scope
(resource group `CAIS_016_InnovationHub`, subscription
`c4fb1c99-fb99-4dc1-9926-a3a4356fd44a`).
In Azure portal: open that resource, **Access control (IAM) > Add > Add role
assignment**, select the role, select the intended user, then review and assign.
The role's definition was checked read-only and includes `OpenAI/responses/*`.
Do not grant subscription-wide access or a broader Contributor role just for
this inference call. Resource management/playground access does not prove
Entra data-plane inference access. No role was assigned by this demo.

## Prepare locally

From the repository root, with Python 3.12 and Azure CLI installed:

```powershell
Set-Location .\Detroit-November-2026\foundry-demo
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe demo.py prepare
```

`prepare` creates only missing inputs and preserves existing files. Open the
PDF, workbook and PNG to inspect them before making a live call.
The current local slice was exercised with Python 3.12.10, openai 3.1.0,
azure-identity 1.25.3, Pydantic 2.11.5 and Pillow 11.3.0.
Generated inputs and runs persist locally but are gitignored; source generation
is versioned in `demo.py`.

## Authenticate separately and run deliberately

The current assisted session already has an isolated authenticated CLI store;
reuse its process-local `AZURE_CONFIG_DIR` when continuing there.
Do not reset or select a global shared CLI profile.
For a new terminal/machine without that session store, create a separate login:

```powershell
$env:AZURE_CONFIG_DIR = Join-Path $env:LOCALAPPDATA 'DetroitFoundryDemo\AzureCLI'
az login --tenant 6aab181b-a190-4247-a5d7-cb792347c7fb --use-device-code --output none
```

Complete sign-in only at the Microsoft URL shown by Azure CLI, using the
intended demo identity. Never put passwords, API keys or tokens in this folder,
chat or configuration. `AzureCliCredential` explicitly uses this tenant;
it has no default-credential fallback and does not change subscription selection.
Keep `AZURE_CONFIG_DIR` set in each terminal that runs the application.

With inference access granted and propagated:

```powershell
.\.venv\Scripts\python.exe demo.py run --live
```

This sends the actual synthetic PDF and PNG inline, plus spreadsheet cell text,
to the configured Responses endpoint. It makes at most one model request, with no automatic retries, a
180-second timeout and 5,000-output-token ceiling. `store=False` disables
Responses conversation storage, not applicable service security/abuse retention.
A rerun is another potentially billable request. A timeout does not prove the
service did no work; inspect the failure before deliberately rerunning.
The answer-key fixture and local validation rules are not sent as model input.

## Read the result

On success, the printed path identifies a new `runs\<run-id>` directory:

| File | Meaning |
|---|---|
| `manifest.json` | Input/code/prompt hashes, deployment, actual returned model, elapsed time, token usage and completion/failure state |
| `response.json` | Actual SDK response; never a prefilled example |
| `extraction.json` | Schema-constrained source observations |
| `record.json` | Locally reconciled record, evidence, candidates and review reasons |

Expected for all three sources: SKU `NL-300`, color null, width `"25.0"`,
warranty `24`, issue `color-conflict`. The November 5 successful run matched
these values. PDF line/value checks use the generated supplier source;
image meaning still needs visual review. Schema validity does not prove
factual correctness. Failed authentication/API/parsing/validation is explicit,
retains a failed manifest and exits nonzero; partial artifacts are not success.
Token usage is recorded when returned, but cost stays unknown without pricing.

Still outside this slice: multi-bundle storage, user-upload flow, custom
connector, Copilot Studio workflow/agent wiring, review UI, CSV export, tracing
instrumentation and measured A/B evaluation. The five-case fixture remains a
design oracle, not evidence that those capabilities exist. The Azure host and
API resource registration exist, but the live container still runs the
pre-cross-tenant revision. The updated API code and IaC have passed local
validation only; deploying them and obtaining Studio-tenant consent are
separate remaining steps.

References: [Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses),
[Azure OpenAI inference roles](https://learn.microsoft.com/azure/ai-services/openai/how-to/role-based-access-control).

## Copilot Studio hookup: explicit 30-minute path

Use this when you need to show the real bridge from Studio to the deployed API.
This assumes the API deployment above is already healthy.
For copy/paste values, use `copilot-studio-connector-values.json`.

### 1) Verify API readiness (2 minutes)

1. `GET /health` must return `200 {"status":"ok"}`.
2. `POST /v1/catalog/process` without a bearer token must return `401 invalid_token` (not `503 auth_not_configured`).

These checks confirm the API is up and Entra audience validation is turned on;
they do not prove that a Studio-tenant token is accepted.

### 2) Create connector client app registration (7 minutes)

The API app registration already exists:

- **API app (resource):** `supplier-catalog-processor-api`
- **Application (client) ID:** `bddf150f-1313-4e96-bf90-922f25ee29b8`
- **Audience URI:** `api://bddf150f-1313-4e96-bf90-922f25ee29b8`
- **Delegated scope:** `catalog.process`
- **Supported account types:** organizational directories (multitenant)
- **Studio tenant:** `1b37c04e-260e-4189-a11b-0b8609ed3df0`

Create a separate Entra app registration for the Power Platform custom connector
OAuth client:

1. Entra ID → App registrations → New registration.
2. Name it `supplier-catalog-connector-client`.
3. Supported account type: Single tenant.
4. After creation, add a **Web** redirect URI using the exact redirect URL shown
   in the custom connector OAuth setup screen.
5. Create one client secret and save it securely.
6. API permissions → Add permission → My APIs → `supplier-catalog-processor-api`
   → delegated permission `catalog.process` → Add.
7. Ask the Studio-tenant administrator to grant consent for this delegated
   permission. The API resource app is registered in the Foundry tenant and
   must be represented by a service principal in the Studio tenant.

### 3) Import custom connector (8 minutes)

1. In Power Apps, go to **Custom connectors** and choose **Import OpenAPI file**.
2. Upload `foundry-demo/catalog-api.openapi.json`.
3. Configure OAuth 2.0:
   - **Identity provider:** Azure Active Directory
   - **Client ID / Secret:** from `supplier-catalog-connector-client`
   - **Authorize URL:** `https://login.microsoftonline.com/1b37c04e-260e-4189-a11b-0b8609ed3df0/oauth2/v2.0/authorize`
   - **Token URL:** `https://login.microsoftonline.com/1b37c04e-260e-4189-a11b-0b8609ed3df0/oauth2/v2.0/token`
   - **Scope:** `api://bddf150f-1313-4e96-bf90-922f25ee29b8/catalog.process`
4. Create the connector and run **Test** with body:
   `{"sourceBundleId":"FC-03-NL300"}`.
5. Confirm you receive `status: completed` and `record.status: needs_review`.

### 4) Add workflow tool in Copilot Studio (8 minutes)

1. Open the target GitHub-harness agent in Copilot Studio.
2. Tools → **Add tool** → **Workflow**.
3. Create a workflow with trigger **When an agent calls the flow**.
4. Add the custom connector action (`processSupplierCatalogBundle`).
5. Pass through `sourceBundleId` from workflow input.
6. Add **Respond to the agent** and map:
   - `runId`
   - `record.status`
   - `record.issues`
   - `record.candidates`
7. Publish workflow, then publish the agent.

### 5) Live validation prompt (5 minutes)

In the agent test pane, use:

`Process FC-03-NL300 and return only runId, status, issues, and color candidates.`

Expected outcome:

- Tool call occurs (workflow trace visible).
- Connector call succeeds.
- Response includes `status=needs_review` with a color conflict.
