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

**Talk B · 30 minutes — Beyond chat: engineering with Foundry.** A fictional desk-lamp supplier's PDF, spreadsheet and packaging images become evidence-linked catalog drafts and a human review queue. Show why a developer-owned AI service may be useful, then compare general multimodal extraction to a format-specific pipeline using the same acceptance tests. The intended payoff is a measured quality/latency/cost decision, not a nicer chat answer. Studio can call the service; no platform-exclusivity claim or Studio integration is required. Pacing: need 5; pipeline 12; comparison/failure/evaluation evidence 8; platform/runtime decision and questions 5.

See `data/run-of-show.json` for talk-relative segment schedules and slide coverage. The complete walkthroughs, setup requirements, source documents and rehearsal boundaries are in `attendee-guide.html`.

## Readiness and boundaries

Local product data and launch-package examples are synthetic deterministic references. `fixtures/foundry-catalog-processing.json` defines five designed source bundles and expected catalog outcomes. It is not a collection of supplier files, model responses, generated exports or evaluation results. The [first runnable Foundry slice](foundry-demo/README.md) generates one NL-300 specification PDF and packaging image, requests structured observations and reconciles them locally. Its November 4 live run succeeded: black/red evidence was retained, color stayed null, width became `"25.0"` cm and the record routed to review. Actual response and run evidence persist locally under `foundry-demo/runs/20261104T194827Z-de4b3c40`. The full PDF/XLSX/image corpus, review application, export, tracing and A/B results remain unbuilt. Slide specimens visualize the design, not an existing deployed UI. The failure-path diagram is original scenario artwork inspired by the attributed conference lesson, not recorded telemetry.

For Studio, choose two models actually allowed in the tenant, hold sources/instructions/tools/question fixed, and use fresh conversations. Record real response evidence and elapsed time; no winner or benchmark is prefilled. Prepare actual solution-version, environment, test and release evidence for the lifecycle walkthrough; no additional DEV/TEST/PROD targets have been selected or created by editing the deck. The supported web-app lane uses an iframe in an approved host, not an assumed embedding in the Cowork app. Verify authentication, sharing and publication separately. The confirmed Power Platform target remains `https://dtw-innovation.crm.dynamics.com/` (environment ID `428fc189-ef8f-e8ff-bfc1-ac1aadb32905`); this is not the managed-app environment or an inferred Azure subscription. Old Dataverse registration, copy/upgrade and app-release walkthroughs have been removed from the attendee guide; their unrelated source assets have not been deleted.

Cowork's App skill and other preview functionality must be rechecked in the actual Frontier tenant at rehearsal. Follow current Microsoft Learn guidance and narrate only controls visible in that tenant. The Foundry project, model, tools, identity, trace and evaluation remain separate build/rehearsal prerequisites; this deck makes no cloud calls and provisions nothing. Confirm tenant policy, permissions, spend and approval before any live service use. Do not represent a generated response as a saved record or a synthetic fixture as live evidence.

The Foundry guide walks through source inspection, one bundle's processing, conflict review, validated-draft export, implementation comparison and trace diagnosis. Keep the fixture's answer key out of model context. Code—not a prompt or function schema—must implement adapters, reconciliation, decimal unit normalization and validation. FC-01 and FC-05 should pass; FC-02/03/04 should remain in review. Those are designed expectations, not measured success. A fixed pipeline calling Foundry models may be sufficient; prompt/hosted agents are optional implementation choices, not prerequisites imposed to showcase a feature.

The confirmed Foundry target is `dtw-tool-demo` in `eastus`, subscription `c4fb1c99-fb99-4dc1-9926-a3a4356fd44a`, with deployment `gpt-6.1-sol`; see `foundry-demo/config.json`. These values were supplied/verified separately from Power Platform. The first slice uses isolated Azure CLI authentication and no API keys. After the user's inference-role assignment, the resource's dedicated `openai.azure.com` endpoint succeeded; the `services.ai.azure.com` gateway continued returning HTTP 401. Application hosting and trace destination are not selected. Use actual input hashes, configuration versions and run IDs; compare the two candidate implementations without preselecting a winner. Separate attributed inference cost from full processing/hosting costs and use held-out cases before claiming production quality.

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
| `index.html`, `deck.css`, `deck.js` | Audience deck: 19 Talk A slides and 13 standalone Talk B slides |
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
