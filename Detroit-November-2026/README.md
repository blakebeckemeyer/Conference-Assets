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

**Presenter start:** [the 30-minute stage run sheet](attendee-guide.html#foundry-rehearsal) has the exact routing prompt, screen order, field-level pass criteria and 60-second presentation fallback. The presenter reported successful GitHub-harness execution after specialist v2 deployment. A saved result/recording and a timed field-level rehearsal are still required; none is fabricated by these docs. Use the actual working GitHub-harness agent, not the earlier standard-harness agent by assumption. Do not provision, publish, change security or use the older CAIS custom-connector route during this demo.

See `data/run-of-show.json` for talk-relative segment schedules and slide coverage. The complete walkthroughs, setup requirements, source documents and rehearsal boundaries are in `attendee-guide.html`.

## Readiness and boundaries

Local product data and launch-package examples are synthetic deterministic references. `fixtures/foundry-catalog-processing.json` defines five designed source bundles, not five implemented bundles or evaluation results. The current [CorpDev specialist](foundry-agent/supplier-catalog-specialist/README.md) packages FC-03 and the shared processor; v2 is active and the presenter reports successful native delegation in the GitHub Copilot harness. Keep the actual returned evidence distinct from the abbreviated expected example. The other four bundles, review application, CSV export, tracing UI and measured A/B comparison remain unbuilt. Diagrams illustrate those broader designs, not deployed interfaces. The real SDK failure can be taught from a redacted captured log, not by labeling the conceptual failure diagram as telemetry.

For Studio, choose two models actually allowed in the tenant, hold sources/instructions/tools/question fixed, and use fresh conversations. Record real response evidence and elapsed time; no winner or benchmark is prefilled. Prepare actual solution-version, environment, test and release evidence for the lifecycle walkthrough; no additional DEV/TEST/PROD targets have been selected or created by editing the deck. The supported web-app lane uses an iframe in an approved host, not an assumed embedding in the Cowork app. Verify authentication, sharing and publication separately. The confirmed Power Platform target remains `https://dtw-innovation.crm.dynamics.com/` (environment ID `428fc189-ef8f-e8ff-bfc1-ac1aadb32905`); this is not the managed-app environment or an inferred Azure subscription. Old Dataverse registration, copy/upgrade and app-release walkthroughs have been removed from the attendee guide; their unrelated source assets have not been deleted.

Cowork's App skill and other preview functionality must be rechecked in the actual Frontier tenant at rehearsal. Follow current Microsoft Learn guidance and narrate only controls visible in that tenant. The CorpDev Foundry specialist/model and native connection now exist; saved live-result evidence and field-level rehearsal remain prerequisites, while Foundry evaluations remain deferred. The deck makes no cloud calls. The approved legacy BotService exception does not check end-user tenant/role on that path; direct access retains AzureRbac. Present this as demo-only, not production-ready access. Confirm spend and do not represent a synthetic fixture as live evidence.

The Foundry guide walks through source inspection, one delegated request and its JSON result, then the code/SDK boundary and future test design. Keep the answer key out of model context. Code implements spreadsheet reading, reconciliation, decimal normalization and validation. FC-03 should remain in review; the other cases are still designed expectations. A fixed pipeline calling model APIs may be sufficient; hosting is an implementation choice, not a requirement imposed to showcase a feature.

The stage Foundry target is CorpDev `cog-b6qdlbxyhq22k / detroit-catalog` in `Detroit-InnoHubDemo`, subscription `eaabd6a6-7835-447a-aff4-629066fdeb75`, East US, model `gpt-6.1-sol`. The older CAIS API and `foundry-demo/config.json` remain historical/alternative routes; they are not the stage deployment. Do not run that direct-model command as an invisible fallback to native delegation. Use actual run IDs and distinguish inner processing time, outer tool duration, token usage and unknown total cost. No benchmark or production-quality claim follows from one demo case.

The visuals retain AIS branding. `assets/visuals/` contains original SVG artwork (launch journey, IQ map, brief/app specimens, theme edit, model comparison, channels, lifecycle, catalog input/evidence/pipeline/review/scorecard/failure and service boundary) and one bounded app-runtime conference-figure excerpt. Source filenames, SHA-256 versions, authors, pages, adaptations and affected slides are recorded in `assets/conference-visual-sources.json`; no complete conference slide is embedded. The broader AIS template, logo and Arial fallback authority is in `assets/brand-sources.json`.

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
| `scripts/check-deck.py`, `scripts/check-motion.mjs` | Dependency-light structure, timing, link and motion checks |
| `assets/conference-visual-sources.json` | Attribution and adaptation register for conference visuals |
| `assets/brand-sources.json` | AIS brand source and visual-system record |
