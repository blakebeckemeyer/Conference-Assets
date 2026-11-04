# First Foundry slice: PDF + image to a review record

This is a local Python application calling the existing `gpt-6.1-sol`
deployment on `dtw-tool-demo`. It is not a deployed agent or a web application.
No new Azure resources, uploaded-file resources, roles or shared CLI profiles
are created or changed by the script.

## What to look at first

The generated `inputs\specification.pdf` says **NL-300, black, 250 mm,
24-month warranty**. `inputs\packaging.png` shows a **red** lamp with the
same model label. This deliberately demonstrates the image-conflict portion
of FC-03, not the complete three-source case: the spreadsheet is not built.
The PDF is a single rasterized page, so this first extraction also needs vision.

The model returns observations independently for each source using an enforced
JSON schema. Python checks coverage, evidence references, PDF value support,
types and conflicts, then converts millimeters to centimeters with Decimal.
An unresolved color must be null, with both candidates retained and
`status: needs_review`. Nothing is published or automatically corrected.

**First live result:** November 4 run `20261104T194827Z-de4b3c40` completed
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
The successful run emitted an SDK/Pydantic serialization warning when saving
the parsed response; the response, extraction, manifest and locally validated
record were all saved. Offline unit-test data is never labeled a model result.

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

`prepare` refuses to overwrite existing files; if the two inputs already exist,
reuse and inspect them. Open the PDF and PNG before making a live call.
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

This sends the actual synthetic PDF and PNG inline to the configured Responses
endpoint. It makes at most one model request, with no automatic retries, a
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

Expected for these two sources: SKU `NL-300`, color null, width `"25.0"`,
warranty `24`, issue `color-conflict`. The first successful run matched these
values. PDF line/value checks use the generated supplier source;
image meaning still needs visual review. Schema validity does not prove
factual correctness. Failed authentication/API/parsing/validation is explicit,
retains a failed manifest and exits nonzero; partial artifacts are not success.
Token usage is recorded when returned, but cost stays unknown without pricing.

Still outside this slice: spreadsheet ingestion, other source bundles,
review UI, CSV export, service hosting, tracing instrumentation, implementation
B and measured A/B evaluation. The five-case fixture remains a design oracle,
not evidence that those capabilities exist.

References: [Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses),
[Azure OpenAI inference roles](https://learn.microsoft.com/azure/ai-services/openai/how-to/role-based-access-control).
