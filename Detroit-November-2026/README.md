# Detroit 2026: two independent conference talks

**Date:** November 10, 2026
**Audience:** business leaders, makers and developers
**Format:** one offline HTML deck, two self-contained presentations, 90 minutes total. The inter-talk break is intentionally unscheduled.

## Open and present

Open `index.html#talk-a` for the 60-minute Microsoft 365 Copilot, Cowork and Copilot Studio talk, or `index.html#talk-b` for the separate 30-minute Foundry talk. The buttons at the top of the deck and presenter console jump to either talk. Each has its own slide range and clock; switching talks resets the private presenter timer.

Use Arrow keys, Page Up/Down or Space to navigate. Home/End jump within the active talk. Press **P** to open the private presenter console, **F** for full screen, and use the on-screen controls as an alternative. Move Presenter view to a private display and share only the audience window. Speaker notes exist only in inert templates in `index.html` and are sent to the separate console; they are not rendered as audience content. Print creates a slide-per-page handout without presenter notes.

The deck works from local files without a server, build step, package installation, network access or CDN. Navigation includes short, interruptible transitions; reduced-motion, resize and print states cancel motion. The single attendee guide covers only the selected demos: launch brief, Cowork app, IDE color edit, Studio lifecycle/model/web walkthrough and standalone Foundry catalog processing.

## Talk outlines

**Talk A · 60 minutes** — product-launch facts become a sourced M365 brief, a Cowork Launch Review app, and a one-color IDE edit of that same app. Studio's reason to enter the story is governed business operation: environment security, full DEV/TEST/PROD ALM in both harnesses, deeper actions/workflows and supported channels. The selected GitHub Copilot-harness walkthrough compares models, inspects a prepared version/release and shows web delivery. No custom MCP server, Dataverse write or app-to-agent conversion is needed.

**Talk B · 30 minutes — Beyond chat: engineering with Foundry.** Six slides: recap where Copilot/Cowork/Studio left us (3 minutes), why add Foundry (4), platform highlights versus our hosted agent's actual features (4), a continuous product demo (14), then takeaway and questions (5). In the demo show the FC-03 lamp sources, Foundry project/hosted specialist, shared Python code, Studio delegation and actual JSON review record. The recap supplies enough context for newcomers; the lamp remains a separate synthetic example. Repeated pipeline/review diagrams, unbuilt benchmarks and SDK history are removed from the main flow; engineering details remain optional guide references.

**Presenter start:** [the 30-minute stage run sheet](attendee-guide.html#foundry-rehearsal) has the routing prompt, screen order, field-level pass criteria and 60-second presentation fallback. DTW specialist v2, the saved Studio binding and the approved temporary live `BotService` exception are verified. The exception was applied at 19:18:37 UTC on November 10; the user subsequently reported **"Demo is working"**. No successful tool JSON, run ID or field-level capture was supplied, and Activity caller-tenant propagation is not repaired. Describe the outcome as user-reported working under this exception, not an independently verified result. Save the actual DTW result/recording before claiming its field checks passed. Do not provision, publish, make further security changes or use the older CAIS custom-connector route during this demo.

See `data/run-of-show.json` for talk-relative segment schedules and slide coverage. The complete walkthroughs, setup requirements, source documents and rehearsal boundaries are in `attendee-guide.html`.

## Readiness and boundaries

Local product data and launch-package examples are synthetic deterministic references. `fixtures/foundry-catalog-processing.json` defines five designed source bundles, not five implemented bundles or evaluation results. The current [DTW specialist](foundry-agent/supplier-catalog-specialist/README.md) packages FC-03 and the shared processor; v2 is active. The initial migration did not verify delegation; the user later reported the demo working with the approved live compatibility exception. No successful output or field-level capture was supplied. Keep actual returned evidence distinct from the abbreviated expected example. The other four bundles, review application, CSV export, tracing UI and measured A/B comparison remain unbuilt. Diagrams illustrate those broader designs, not deployed interfaces. The historical SDK failure can be taught from a redacted captured log, not by labeling the conceptual failure diagram as telemetry.

For Studio, choose two models actually allowed in the tenant, hold sources/instructions/tools/question fixed, and use fresh conversations. Record real response evidence and elapsed time; no winner or benchmark is prefilled. Prepare actual solution-version, environment, test and release evidence for the lifecycle walkthrough; no additional DEV/TEST/PROD targets have been selected or created by editing the deck. The supported web-app lane uses an iframe in an approved host, not an assumed embedding in the Cowork app. Verify authentication, sharing and publication separately. The confirmed Power Platform target remains `https://dtw-innovation.crm.dynamics.com/` (environment ID `428fc189-ef8f-e8ff-bfc1-ac1aadb32905`); this is not the managed-app environment or an inferred Azure subscription. Old Dataverse registration, copy/upgrade and app-release walkthroughs have been removed from the attendee guide; their unrelated source assets have not been deleted.

Cowork's App skill and other preview functionality must be rechecked in the actual Frontier tenant at rehearsal. Follow current Microsoft Learn guidance and narrate only controls visible in that tenant. The DTW Foundry specialist/model exist; saved live-result evidence and field-level rehearsal remain prerequisites, while Foundry evaluations remain deferred. The deck makes no cloud calls. The repository's secure default is AzureRbac with Entra isolation plus BotServiceRbac. The approved reversible DTW-only legacy BotService exception is now live for this synthetic demo; it retains channel authentication but removes additional Bot-user authorization. Source v2/package, environment, identity, Activity, routing and publication state are unchanged. See the [specialist guide](foundry-agent/supplier-catalog-specialist/README.md#approved-temporary-demo-compatibility-exception) for the scope, live evidence and rollback. The source updater deliberately refuses legacy mode; restore BotServiceRbac before normal source deployment, real supplier data or production. Confirm spend and do not represent a synthetic fixture as live evidence.

The Foundry guide walks through source inspection, one delegated request and its JSON result, then the code/SDK boundary and future test design. Keep the answer key out of model context. Code implements spreadsheet reading, reconciliation, decimal normalization and validation. FC-03 should remain in review; the other cases are still designed expectations. A fixed pipeline calling model APIs may be sufficient; hosting is an implementation choice, not a requirement imposed to showcase a feature.

The stage Foundry target is DTW `dtw-tool-demo-b571 / detroit-catalog` in `dtw-tool-demo`, tenant `f32b97f0-efb8-4bc3-91ee-18a6e5f635c9`, subscription `b571e36c-4e62-4175-b8c1-062a4cf87b16`, East US, model `gpt-6.1-sol`. Use the source-only deployment script in the specialist guide; do not provision duplicates. CorpDev, the older CAIS API and `foundry-demo/config.json` remain historical/alternative routes, not the stage target. Do not run a direct-model command as an invisible fallback to native delegation. Use actual run IDs and distinguish inner processing time, outer tool duration, token usage and unknown total cost. No benchmark or production-quality claim follows from one demo case.

The visuals retain AIS branding. `assets/visuals/` contains original SVG artwork (launch journey, IQ map, brief/app specimens, theme edit, model comparison, channels, lifecycle, catalog input/evidence/pipeline/review/scorecard/failure and service boundary) and one bounded app-runtime conference-figure excerpt. Source filenames, SHA-256 versions, authors, pages, adaptations and affected slides are recorded in `assets/conference-visual-sources.json`; no complete conference slide is embedded. The broader AIS template, logo and Arial fallback authority is in `assets/brand-sources.json`.

## Native Foundry connection access

A connector `403` reporting **missing connection ACL** during token exchange
occurs before the specialist runs. The November 10 failure identified the
**Power Virtual Agents Service** service principal, not the interactive user.
The connection owner already had access. An administrative `CanView` grant for
the runtime was added and persisted, but the user subsequently reported the
**same token-exchange denial**. The execution failure is unresolved; neither
`Connected` nor a saved management permission proves runtime access.

Current read-only investigation found the same service-principal grant through
both the administrative and maker-facing permission endpoints at API version
`2017-06-01`, including the regional maker endpoint. The older `2016-11-01`
maker response omitted this grant; comparing different API versions is not
evidence of separate administrative and runtime ACL stores. Microsoft's
administrative cmdlet uses the same grant body and route as the helper below.
Repeating that grant is not an established repair.

The connection and live connector authentication schema both report
`allowSharing=false`. The connector's
[Entra user-login authentication is non-shareable](https://learn.microsoft.com/en-us/connectors/azureagentservice/#microsoft-entra-id-user-login).
However, [native GitHub-harness Foundry delegation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/add-agent-foundry)
explicitly uses Entra user-login connections, so non-shareability alone does
**not** explain the denial or justify switching to application credentials.

The Power Platform connection in that error belongs to tenant
`f32b97f0-efb8-4bc3-91ee-18a6e5f635c9`, environment
`0343907b-5031-ed09-acc8-5e9701b25f1d`. That tenant also owns the canonical DTW
Foundry project, but the connection ACL is still a separate authorization
boundary. This environment is **not** the `dtw-innovation` environment above
or the historical CorpDev tenant; do not substitute those targets.

The example below audits the original token-exchange connection, not the
different connection now saved in Studio. From the repository root, with Azure
CLI signed in as its owner or an authorized Power Platform administrator:

```powershell
$connection = @{
    TenantId = 'f32b97f0-efb8-4bc3-91ee-18a6e5f635c9'
    EnvironmentId = '0343907b-5031-ed09-acc8-5e9701b25f1d'
    ConnectionName = 'shared-azureagentser-02b35a76-7231-4904-84d9-67d8be3d9764'
}

# Read-only administrative ACL inspection, NOT a runtime access test.
.\Detroit-November-2026\scripts\Ensure-FoundryConnectionAccess.ps1 @connection

# Only for a missing grant on a shareable connection; -WhatIf previews.
# The current non-shareable connection cannot receive a new grant this way.
.\Detroit-November-2026\scripts\Ensure-FoundryConnectionAccess.ps1 @connection -Repair
```

The script checks the signed-in tenant without switching accounts or profiles.
It resolves Microsoft application `9d8f559b-5984-46a4-902a-ad4271e83efa` to its
service principal in that tenant instead of hard-coding a tenant-specific object
ID. It verifies connection identity, environment, Connected status and sharing
capability before inspecting permissions. On shareable connections, explicit
repair adds only a missing `CanView` and preserves existing grants (including
ownership). Results are `AdministrativeGrantPresent`,
`AdministrativeGrantAdded`, or `NotApplied`, always with
`ExecutionVerified=false`. They are deliberately not called `Compliant` or
`Repaired`. A non-shareable connection with an existing grant is reported with
a warning and never rewritten; a missing grant on a non-shareable connection
stops with an error. The script never upgrades access to edit, share, or
tenant-wide rights, stores no tokens or credentials, and does not retry failures.

Run the preflight after creating, importing, or rebinding the native
`shared_azureagentservice` connection and before rehearsal. If the connection is
recreated, use its **new connection name**; if it moves, supply its actual tenant
and environment as well. A grant on the old connection does not transfer.
Repair requires the owner's/admin's authority; Azure subscription RBAC alone
does not grant Power Platform connection-sharing rights. Use an isolated CLI
profile for a different tenant rather than changing a shared login.

This is an explicit Power Platform setup/recovery step, not an `azd` hook or
Foundry infrastructure role assignment. It does not change consent, endpoint
authorization, publication, or the specialist, and never invokes
`process FC-03-NL300`.

The user-confirmed failed-call caller is
[DTW Tool Demo](https://copilotstudio.microsoft.com/environments/0343907b-5031-ed09-acc8-5e9701b25f1d/agents/781a5f55-6bc3-473d-b085-455c881026c5),
using the GitHub Copilot harness. Its saved connected agent is now
`Supplier Catalog Specialist DTW` (previously observed as `supply-cat`).
Studio read-back confirms Agent ID `supplier-catalog-specialist` and connection
`azureagentservice_1`, ID `b3547013461c46ebb920b8bd97bc04c6`, named
`Detroit DTW Catalog Foundry`. That connection uses Entra ID User Login and
the exact DTW project endpoint in the specialist guide. This is not the original
`shared-azureagentser-02b35a76-7231-4904-84d9-67d8be3d9764` connection; its
administrative grant is not evidence about the current connection.

Read-only RBAC checks during the investigation showed that the known connection
owner already had **Owner** and **Foundry User**, inherited from the DTW
subscription with no assignment conditions. The hosted runtime already had
account-scoped **Cognitive Services OpenAI User**. No additional DTW Azure role
was needed or assigned by this session. These grants do not identify the user
or tenant represented in the failed Activity; another owner grant is not a
repair for invalid caller-tenant context. Network reachability is separate:
the request already reached Foundry and received an authorization response.

The Studio draft instructions were saved to route this bundle to the named
specialist once, preserve returned evidence/conflicts, and stop on failure
without an automatic retry, approval or publication. They survived reload;
the draft was not published and no processing call was sent.

A later user-run call failed `BotServiceRbac` Activity caller-tenant validation,
request `5ecc66ee0c1e39d247d9e3c2005d7989`. Authenticated Studio history now
also confirms the November 10, 2026 19:05 UTC Preview failure, request
`f1f5a9730707119738f159d6f4268968`: its tool trace selected
`SupplierCatalogSpecialistDTW`, passed exactly `{"task":"process FC-03-NL300"}`,
and returned `Http403`. The stale name in the pasted prompt did not prevent
correct routing. Studio already has **Authenticate with Microsoft** selected;
its DLP policy disables **No authentication**. No tenant input is exposed for
that selected mode. Changing the prompt, turning authentication on, or
publishing is not an established repair.

The saved binding is confirmed, but the Activity identity received by Foundry
remains unverified. Before the compatibility exception, the bounded DTW telemetry query
had no matching request; it is not a trace of the gateway's caller validation.
Microsoft support needs to correlate the Studio `SendActivityV2` call through
Bot Service to Foundry and identify where tenant/user context becomes invalid.
Supply the request ID, failure time/time zone and the verified binding; request
a sanitized caller-context trace, not bearer tokens.
Do not silently substitute another environment or connection. No rebinding or
reauthorization repair has been established for the caller-tenant error.
Obtain approval before further configuration changes, consent or a live test.
The user subsequently approved only the reversible DTW demo `BotService`
exception described in the specialist guide, plus one separately approved
Studio processing attempt. The policy PATCH succeeded at 19:18:37 UTC and
independent read-back at 19:19:29 UTC verified the intended one-field change
with version/package, environment, identity, routing and publication preserved.
The user subsequently reported "Demo is working"; no successful JSON/run ID,
model/token metadata or field-level artifact was supplied. The coordinator did
not execute its separately approved test or retry. This is user-reported
operation with the exception, which bypasses the additional Bot-user check
rather than repairing identity propagation. It does not authorize
anonymous/public access, additional roles, tenant-wide access or publication.
Do not delete the connection, elevate the runtime to `CanViewWithShare`/`CanEdit`,
or make other unapproved endpoint changes.

API reference: [Microsoft's connection permission command](https://learn.microsoft.com/en-us/powershell/module/microsoft.powerapps.administration.powershell/set-adminpowerappconnectionroleassignment).
The script uses its Power Platform `modifyPermissions` API through `az rest`;
the Power Apps PowerShell module is not required.

## Local checks

From the repository root, with Python 3 and Node.js available:

```powershell
node --check .\Detroit-November-2026\deck.js
node --check .\Detroit-November-2026\presenter.js
python .\Detroit-November-2026\scripts\check-deck.py
node .\Detroit-November-2026\scripts\check-motion.mjs
node .\Detroit-November-2026\scripts\launch-demo.mjs check
```

`check-deck.py` verifies slide and note counts, two independent talk ranges, schedule coverage and timing, local links, the three-page HTML inventory, private presenter controls, visual-source records and the synthetic Foundry fixture. `check-motion.mjs` exercises navigation, chapter transitions, reduced motion, printing and fallbacks with a small DOM harness. `launch-demo.mjs check` validates the two generated product examples against the independently maintained expected-facts fixture without changing them.

Offline connection-access regressions use Pester and mock every Azure CLI call:

```powershell
Invoke-Pester .\Detroit-November-2026\scripts\Ensure-FoundryConnectionAccess.Tests.ps1
```

## Key paths

| Path | Purpose |
|---|---|
| `index.html`, `deck.css`, `deck.js` | Audience deck: 19 Talk A slides and 6 Talk B slides |
| `attendee-guide.html`, `guide.css` | One demo-only guide with `#m365`, `#cowork`, `#lifecycle`, `#studio` and step-by-step `#foundry` sections |
| `presenter.html`, `presenter.css`, `presenter.js` | Private notes, talk-relative navigation, separate talk timer |
| `data/run-of-show.json` | Independent 60- and 30-minute schedules mapped to slides |
| `data/manufacturer-products.json`, `data/retailer-requirements.json` | Canonical synthetic source facts and retailer rules |
| `knowledge/` | Readable Markdown/TXT versions for supported authoring surfaces |
| `contracts/launch-package.schema.json`, `templates/` | Reusable output contract and brief, listing and handoff templates |
| `fixtures/expected-facts.json`, `examples/` | Independent exact-fact oracle and two deterministic product references |
| `fixtures/foundry-catalog-processing.json` | Catalog source-bundle design, expected fields/routing, rules and unmeasured implementation-comparison plan |
| `foundry-demo/` | First local PDF/image generator, structured extraction, reconciliation, offline tests and exact run/auth instructions |
| `scripts/launch-demo.mjs` | Offline product-reference generator/checker |
| `scripts/Ensure-FoundryConnectionAccess.ps1` | Administrative connection ACL audit; guarded, idempotent grant addition, not a token-exchange test |
| `scripts/check-deck.py`, `scripts/check-motion.mjs` | Dependency-light structure, timing, link and motion checks |
| `assets/conference-visual-sources.json` | Attribution and adaptation register for conference visuals |
| `assets/brand-sources.json` | AIS brand source and visual-system record |
