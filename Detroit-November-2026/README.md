# From spec sheet to shelf

Detroit, November 10, 2026. Two-hour conference foundation for business leaders,
makers and developers. One recurring new-product introduction evolves across
M365 declarative agents, **Microsoft 365 Copilot Cowork's Frontier App skill**,
Copilot Studio and Foundry. The second product proves reuse rather than a new,
unrelated demo.

**Current state:** local source data, contracts, templates, deterministic reference
artifacts and a functional HTML deck. No cloud resources, installed plugins,
deployed agents, approval flows, email sends or retailer submissions exist here.
User-confirmed tenant, Power Platform environment, Azure subscription and Frontier
Preview access do not establish any particular integration's availability.

## Open and run

Open `index.html` directly in a current browser: no server, build step, CDN,
network request or package installation is required. Arrow keys / Page Up / Page
Down / Space navigate; Home and End jump; P opens a **separate presenter window**;
F requests full screen. Controls also work with mouse or keyboard. The URL hash
preserves a slide link. Print produces all slides without notes. Without
JavaScript the deck becomes a readable document; note templates remain inert.

Navigation uses short directional sheet transitions, with a distinct wipe when
the chapter changes and a restrained arrival for the main prompt/code/diagram.
There are no automatic advances, loops or extra reveal clicks. Rapid navigation
interrupts the previous transition. The operating system's Reduce motion setting
disables animation; print and window resizing cancel active motion. Inactive
slides cannot receive keyboard focus. The AIS design and motion are retained;
the user-directed runtime correction updates Studio, evaluation and handoff content.

**Screen sharing:** open Presenter view before presenting, move that window to
a private display, and share only the audience window. Sharing an entire screen
can expose any window on it; no separate-window feature can prevent that. The
audience window has no inline-notes mode. The console shows the current/next
title, private speaker notes, navigation controls and a session timer. Allow
popups if prompted. Open the console from the deck, not as a standalone file.

The revised 48-slide deck explains each tool and its relevant features, gives
concrete build/demo/check steps, and links to `attendee-guide.html`. That
browser-readable guide includes source text, copyable prompts, prerequisites,
repeatable exercises and official references. It is attendee-facing; this README
remains the technical setup/readiness ledger. Documentation links require the
internet, but local slides, guide and sample files work offline. Cloud exercises
remain planned until their actual builds and integrations are verified.

Exactly three HTML files remain: `index.html`, `attendee-guide.html` and the
necessary private `presenter.html`. Lifecycle, Studio and Foundry instructions
are sections of the same guide; the three former standalone exercise files are
removed. Deck/guide links now use scoped section anchors, including compatibility
anchors for the migrated validation/skill sections. No hidden duplicate guides
or redirect endpoints are retained.

The dedicated `attendee-guide.html#lifecycle` lab adds a 25-minute hands-on
continuation of the Cowork app: source retrieval, the actual React/Vite/Bun
setup, a one-file theme edit, review/commit/push, hosted preview and explicitly
approved live release. The user's existing Launch Review source was identified
through read-only coordinator inspection. Its app was not created by this repo,
and successful local execution or deployment has not been verified here.

From the repository root, with Node.js 22+:

```powershell
node .\Detroit-November-2026\scripts\launch-demo.mjs build
node .\Detroit-November-2026\scripts\launch-demo.mjs check
node --check .\Detroit-November-2026\deck.js
node --check .\Detroit-November-2026\presenter.js
python .\Detroit-November-2026\scripts\check-deck.py
node .\Detroit-November-2026\scripts\check-motion.mjs
python .\Detroit-November-2026\scripts\workshop-evaluation.py check
```

`build` intentionally overwrites only the five named generated files in each
product's `examples` directory and the four generated Markdown/TXT knowledge
documents in `knowledge`. Do not put hand edits in those files. `check`
does not write: it verifies the checked-in files are fresh, compares exact
facts against the independent fixture, checks knowledge-document freshness,
resolves evidence pointers, enforces the
contract and retailer limits, and runs 36 negative checks across two products.
The Python 3 deck check uses only the standard library.

## Source and output map

| Path | Purpose |
|---|---|
| `data\manufacturer-products.json` | Authoritative synthetic manufacturer facts for the drill and impact driver |
| `data\retailer-requirements.json` | Fictional retailer taxonomy, copy limits, required fields and review policy |
| `knowledge\manufacturer-products.txt`, `knowledge\retailer-requirements.txt` | Generated readable documents for Agent Builder knowledge uploads; use these instead of JSON |
| `knowledge\manufacturer-products.md`, `knowledge\retailer-requirements.md` | Same source content in Markdown for reading or authoring surfaces that support it |
| `data\run-of-show.json` | Nine contiguous segments totaling 120 minutes, including a five-minute break |
| `contracts\launch-package.schema.json` | Versioned shared output boundary; not a deployed API |
| `templates\launch-brief.md` | Reusable readable business brief |
| `templates\retailer-listing.csv` | CSV columns and row slot; rendered values are quoted and escaped |
| `templates\handoff-email.md` | Buyer/category reviewer email draft, never sent |
| `fixtures\expected-facts.json` | Hand-authored regression oracle; never automatically regenerate from source |
| `examples\drill-kit\` | Five reference artifacts for LM-D1820-K2 |
| `examples\impact-driver-kit\` | Same five artifacts for LM-I1820-K2 |
| `scripts\launch-demo.mjs` | Offline reference generator and bounded schema/fact validator |
| `index.html`, `deck.css`, `deck.js` | Forty-eight-slide audience deck with navigation and print layout; notes are inert templates |
| `presenter.html`, `presenter.css`, `presenter.js` | Separate private console, synchronized slide control and timer |
| `attendee-guide.html`, `guide.css` | The single instructional HTML: all exercises, source text, prompts and official references, with section navigation |
| `attendee-guide.html#lifecycle` | Exercise 3B: supported commands, actual project scripts/theme preset, source/release boundaries, governance handoff and recovery |
| `attendee-guide.html#studio` | Exercise 5: GitHub Copilot harness preview, one onboarding skill, selected Dataverse connector actions, server-validation design and create/reload evidence |
| `attendee-guide.html#foundry` | Exercise 6: version-scoped policy evidence pipeline, offline retrieval experiment, gated structured-output model recipe and independent regression scoring |
| `fixtures\studio-evaluation.csv`, `fixtures\studio-tests.json` | Five local no-write factual questions (map to the new Evaluate template); eleven separate business/action cases; neither is an executed Studio result |
| `fixtures\retailer-policy-corpus.json`, `fixtures\policy-tests.json` | Synthetic approved-v1 excerpts plus explicitly test-only archive/draft distractors; eight source/citation/abstention cases |
| `contracts\policy-answer.schema.json` | Strict five-field model response contract; separate from the launch-package contract |
| `scripts\workshop-evaluation.py` | Standard-library offline business oracle, lexical context selector and actual-response scorer; no authentication/network calls |
| `scripts\check-deck.py` | Offline deck/guide links, note separation, structure, timing and artifact CSV checks |

Each example directory contains **`package.json`, `launch-brief.md`,
`retailer-listing.csv`, `handoff-email.md`, `review.json`**. The package file is
business data, not an npm dependency manifest. The generator is not an agent or
an integration mock. Its `generationMode` is `deterministic-local-reference`.

Both kits share the 18V nominal platform, two 2.0 Ah batteries, charger and carry
bag. Their category, holder, speed, torque, mass and MSRP differ. GTIN, images and
warranty are deliberately absent for both: preserve null/empty values and the
three blockers. No real product identifiers, addresses or customer data are used.
No certifications, safety performance, runtime or battery chemistry are asserted.

## Shared contract and validation boundary

`listing` holds retailer-facing values; `brief` holds launch context and gaps;
`handoff` holds an unsent draft. `evidence` maps output JSON pointers to exact
manufacturer source pointers. Title construction and retailer category mapping
are deterministic derivations verified against the manufacturer brand/name and
retailer taxonomy; they are not direct manufacturer quotations. Source provenance
for those derivations is described here and checked by the script.

`review.status` is always `needs_review` and `approvedBy` is always null in v1.
The package is a **retailer-ready format target**, not an approved or
submission-ready claim. A real approval process requires a deliberately extended
contract and enforced identity/state transitions, not changing a sample string.

The schema is standard JSON Schema 2020-12. The dependency-free local validator
supports only the keywords used in this schema and rejects unknown keywords;
it is not a general-purpose JSON Schema engine. Exact fixture matching is a
strict regression baseline for these two synthetic products, not a semantic
judge of arbitrary future prose. A banned-phrase check is only a guardrail, not a
comprehensive claim/safety/compliance assessment. Human fact review remains
required. No live-agent evaluation has run.

To evolve the facts, update the source and independently review the fixture,
then rebuild and check. Future agent outputs may use `agent-draft` generation
mode, but must not be placed in the deterministic reference folders as if the
local generator produced them. Use a future dedicated capture/evaluation path.

## Chapter-by-chapter rehearsal

| Elapsed | Planned chapter | Preserve / add | Inspectable result |
|---|---|---|---|
| 00:00-00:08 | Establish the recurring launch job | Source facts and retailer policy | Baseline drill package |
| 00:08-00:23 | M365 Product Launch declarative agent | Grounding + original agent | Sourced brief with gaps |
| 00:23-00:36 | Cowork Launch Review app build | Same facts and package files | Read-only product/package review and comparison |
| 00:36-01:01 | Managed-app lifecycle hands-on | Existing generated app and source history | Reviewed color diff, Git SHA, preview and gated release evidence |
| 01:01-01:06 | Copy to Copilot Studio | Preserve original configuration; re-upload embedded TXT knowledge | Saved and retested snapshot |
| 01:06-01:11 | Break | Keep the assets | Reset |
| 01:11-01:35 | Studio Dataverse registration and evaluation | Confirmed operation + shared request | Real row evidence; separate factual/rule/action tests |
| 01:35-01:53 | Foundry engineering experiment | Version-scoped policy evidence and strict output | Actual-source citations, regression scores and measured model tradeoffs |
| 01:53-02:00 | Reuse proof and discussion | Same method, impact-driver input | Correct second-product package |

**Explicit reallocation:** the prior lifecycle revision made room for 25 minutes
of app maintenance. This revision further reduces Cowork build/refinement from
15 to 13 and copy from 7 to 5 to increase Studio from 20 to 24 for concrete
registration and evaluation. Opening 8, M365 15, Cowork 13, lifecycle 25,
copy 5, break 5, Studio 24, Foundry 18, close 7 = 120. Prepare
authentication, source access and dependency restore before the hands-on slot.
The private notes allocate each slide within these chapter budgets. Do not wait
unboundedly for approval/builds on stage: stop at preview or show a labelled
recording if the live release has not been authorized/completed.

These are **planned demos**, not product capability verification. In particular:

- **Chapter decision (October 22):** skills are documented directly in
  M365 declarative agents in Frontier preview; they are not a unique Cowork
  capability. The user selected Cowork's documented Frontier App skill for an
  interactive Launch Review app. The user now has an existing app checkout;
  source/config inspection is not runtime acceptance. It should consume the
  same source facts/package files as a read-only interface.
  It does not implement approval or saved workflow state. The user-selected
  continuity step is Copy to Copilot Studio, followed by a confirmed Dataverse
  registration operation. A separate Retailer Requirements Reviewer agent was
  removed because it duplicates deterministic checks without a business need.
- Current declarative-agent skills documentation says embedded knowledge files
  and skills cannot be combined yet. Exercise 2 uses embedded TXT knowledge
  without skills; adding a skill to that exact configuration is not a supported
  continuation. Reuse across agents is also currently unsupported in the preview.
  Verify a compatible source-delivery approach before revising the arc.
- Cowork App access, billing, file/data binding and generated app behavior must be
  tested in the actual tenant. Stop for authorization before new connectors,
  schemas, writes, publishing or sharing. The Cowork app is not transferred by
  Copy to Copilot Studio; an app-to-process integration is separate work.
- Copy to Copilot Studio is documented, not yet run in this tenant. It creates a
  snapshot; the original remains available and edits do not synchronize.
  Embedded TXT knowledge must be re-uploaded; capability and connector setup
  must be checked separately. Do not promise skill/plugin transfer.
- Exercise 5 selects the GitHub Copilot harness preview and user-selected Dataverse.
  Tables, server validation, narrow tools and actual tenant availability are not
  created or verified. Copy does not establish this harness. Exercise 6 is a custom evidence/model pipeline, not a deployed
  Foundry Agent Service agent. Its local schema/scorer work now; authenticated
  hosting/Studio invocation remains separate work.
- The current reference must never silently replace a failed live integration
  while being presented as live output. Announce the failure and show the
  reference explicitly as an offline comparison.

Use the deck notes as prompt/demo acceptance guidance. During rehearsal, record
actual generated artifact paths, source versions, observed behavior, adaptations
and failure paths before removing any "planned/unverified" labels.

## Studio and Foundry evaluation readiness

The user selected **Dataverse in the confirmed demo environment**. The latest
correction selects **GitHub Copilot harness preview**, not standard topics/flows.
First-party documentation supports connectors, skills, grounding and Foundry
connected agents on this runtime; tenant availability is still unverified.
This authorizes local teaching design, not agent/table creation, plug-in
deployment, connection changes, writes, publication or paid tests.

Exercise 5 uses `Retail Launch Onboarding`, skill `register-retail-launch-draft`,
and selected Dataverse `ListRecords`, `CreateRecord`, `GetItem` actions. The
single-SKU `Retail Launch Request` schema preserves package/source versions,
category and gaps, adding a snapshot and rule version. A stable key identifies
one SKU/retailer/source revision; an active alternate key prevents duplicate
inserts. Lookup/reload reconciles retries rather than generating a fresh key.
It registers an internal draft, never approves or submits to a retailer.

AI orchestration/skill instructions govern conversation, not database security.
The guide specifies synchronous Dataverse PreValidation/PreOperation enforcement:
exact reviewed snapshot, identifiers, copy/length/category rules and derived
`needs_review`/gap codes. The local Python oracle validates those packages and
prints stable proposed payloads:

```powershell
python .\Detroit-November-2026\scripts\workshop-evaluation.py prepare --sku LM-D1820-K2
python .\Detroit-November-2026\scripts\workshop-evaluation.py prepare --sku LM-I1820-K2
```

These are local proposed fields, not saved records or connector responses. No
Dataverse plug-in/adapter is implemented or deployed. A platform maintainer must
implement/review server enforcement and actual schema bindings before the live
write is described as governed. A successful demonstration requires the actual
create primary GUID, subsequent Get and independently refreshed matching row.
Create returned ID plus failed reload means verification incomplete; ambiguous
timeout requires reconciliation. Conversation confirmation is not an enforced
authorization gate. Do not silently run under a powerful maker identity.

Copy to Studio remains a snapshot demonstration, not a new-harness guarantee.
Inspect the destination. If standard, documented upgrade preview creates another
copy with a migration report; knowledge, Power Fx and child agents do not migrate.
Reattach approved sources and retest. If upgrade is unavailable, explicitly port
reviewed instructions/prompts/sources to a new-harness agent; preserve both prior
agents. If the harness is absent, stop rather than revert to the old recipe.
There is no direct cross-harness Studio-agent delegation or automatic Cowork app
connection being claimed.

New-harness **Evaluate > New evaluation** supports conversations, manual authoring
and CSV up to **5 MB**. Download its current CSV template; the supplied two-column
`Question,Expected response` file is local baseline data, not a verified upload
schema. **General quality does not compare expected answers.** Compare all five
questions manually against exact facts before/after extending. Do not carry
standard-harness Compare meaning, case-count/retention settings or flow response
limits into this runtime. Runs use the signed-in profile and tool connections;
tools are not assumed mocked. No cloud evaluation has run.

Eleven action/business cases cover both SKUs, unknown identifiers, injected
claim/long title, denied create, cancellation, failed reload, same-key retry and
out-of-scope approval/submission. No ready product is fabricated. Preview tool
arguments/results plus independently checked rows prove side effects; local
expected outcomes are not simulated Dataverse results. Full instructions and
runtime-specific citations are in the single attendee guide.

Exercise 6 adds engineering control, not Foundry exclusivity. Generic RAG is
already available elsewhere. The local lexical selector compares mixed archived/
draft context against an approved retailer/revision filter. The structured-output
model recipe uses Foundry Models and an independent strict value/citation/version
oracle, with actual usage/time capture. It does not duplicate the Studio save
gate, provision Search, create an agent or pretend local fixture checks are model
evaluations. The eight test cases use the same current policy; only archived/draft
distractors are test-only extensions. Original source data/contracts stay intact.

**Cloud/model prerequisites still open:** authorized project/resource/region,
existing structured-output deployment and compatible SDK, data-plane identity,
network/quota, spend limit and approval for model/judge calls. The embedded Python
recipe is syntax-checked only; no SDK installation, inference or benchmark ran.
Model/API compatibility and measured results must be rehearsed before presentation.
Studio connection remains unimplemented. **New-harness-specific documentation**
supports Build > Connected agents > Add > Add Foundry agent: current-portal
Agent ID, project endpoint, Entra ID user-login connection and enabled Activity
protocol. Activity is off by default; enabling it via documented preview API or
M365/Teams publication requires separate authorization. A plain model endpoint
is insufficient; the local Python pipeline has not been packaged/hosted as that
compatible agent. Actual delegation and response mapping require rehearsal.
Standalone evidence inspection is explicitly manual until built/authorized.

First-party runtime references: [overview](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/overview),
[create](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/authoring-first-bot),
[skills](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/skills-create),
[tools](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/add-tools-custom-agent),
[Evaluate](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-create),
[Foundry route](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/add-agent-foundry).

## Managed-app lab readiness

CLI commands were checked against official Managed Runtime preview docs and
installed `ms --help` / auth/app/git subcommand help. Current inspected versions:
`@microsoft/managed-apps-cli 0.30.0`, Node `24.22.1`, npm `12.0.0`, GCM `2.9.0`;
CLI/SDK prerequisites are Node 24.11.0+ and Git 2.27+. No tools were installed
or auth changed by this materials revision. Older `0.9.1` keytar troubleshooting
is retained only as a historical, version-specific failure, not current setup.

Coordinator confirmed this **separate existing app target**, not a deployment
authorization:

| Field | Read-only source/config finding |
|---|---|
| App display name / ID | Launch Review / `709ff27e-269a-46b8-843a-c4eae1d9fe83` |
| App environment ID | `71ea881b-016d-ec46-bde0-6d4b574f6012` |
| Native Git repository ID | `0a58bc13-e477-41e1-b243-cbc26a3c8e78` |
| Build | React/Vite; `npm run build` → `vite build`; entry `index.html`, output `dist` |
| Checks | `npm run check` → `bun run --parallel typecheck build:check lint` |
| Restore evidence | Both `bun.lock` and `package-lock.json` tracked; no packageManager field. Proposed npm-ci path requires maintainer confirmation; preserve both locks |
| Color edit | `src\index.css`, Green preset from the app's local THEMING guide, consistently across root, explicit-dark and OS-dark blocks |

The actual app environment **differs** from the confirmed Dataverse target below.
Do not conflate or retarget them. The lab keeps attendee target IDs as guarded
placeholders, uses a fresh isolated app checkout and does not bind the personal
Conference-Assets repo as a deployment source. A Git source push, hosted
preview and live deployment are different steps; a Cowork-chat reverse sync
has not been established. Native cloning does not apply to repo-less artifacts.

Coordinator reported `ms app dev` failed because Bun was missing. Their
authorized machine-tool repair succeeded with a scoped npm install-script
exception, and Bun `1.4.4` was verified. The lab documents the equivalent pinned
repair and avoids persistent npm policy changes. App source was not edited.
The user's local dev retry remains distinct from this revision; no competing
app server was started here.

**Remaining rehearsal inputs:** verify intended `ms` identity/access, source
restore policy for the dual-lock project, baseline checks and actual dev result;
approve the exact isolated checkout/repository/branch and release target before
any push/deploy. Confirm inventory entry, named owner and backup maintainer,
connection/data/secret review, publication approval, deployed SHA and live
verification. Runtime controls do not automatically establish these practices.

## Next environment inputs (no secrets)

**Confirmed Power Platform demo target:** <https://dtw-innovation.crm.dynamics.com/>
(user-provided). Read-only identity/access verification succeeded on October 22,
2026 using the user-designated existing PAC profile at index 7.

| Verified field | Value |
|---|---|
| Environment display name | Blake-DTW Innovation |
| Environment ID | `428fc189-ef8f-e8ff-bfc1-ac1aadb32905` |
| Organization ID | `bfb35481-39ce-f111-be85-6045bd050538` |
| Organization unique name | `unqbfb3548139cef111be856045bd050` |

Discovery used `pac auth list` followed by
`pac env who --environment 'https://dtw-innovation.crm.dynamics.com/'`.
Profile 7 was already active and matched the target; no selection change or new
login was needed. Profile indices are local and can change: recheck the current
list rather than treating index 7 as a portable environment identifier.

The earlier Forbidden response under the prior authentication context is
superseded for this identity check. Successful identity retrieval does not prove
maker, agent-editing, push or publish permissions. No cloud content was changed.
The Power Platform account does not establish the intended Microsoft 365 account
or Azure subscription. Do not supply credentials or tokens in chat or this repo.

Before any implementation or cloud actions, select the exact demo tenant and
confirm authorization and data policy. Provide identifiers/URLs through the
working session, not credentials or tokens in this repository:

1. Microsoft 365 tenant ID/domain, demo maker account, selected declarative-agent
   authoring route and permitted SharePoint site/library or other verified
   grounding location. Confirm agent creation and artifact export permissions.
2. Cowork access under that same account, Frontier App skill availability,
   approved billing and the supported source/file-binding options. Verify actual
   app creation and product-switching behavior before the live demonstration.
3. For the verified Power Platform environment above: authorized maker/table
   customization and row access, approved Dataverse connection identity,
   GitHub Copilot-harness preview availability, copy/upgrade boundaries,
   server-validation implementation permission, actual dynamic schema and
   applicable DLP/connector policies. Dataverse remains selected for teaching.
   No Copilot Studio YAML is included; use the author subagent when authorized.
4. Azure subscription ID, allowed region, resource-group choice (existing or
   separately authorized new), budget ceiling and Foundry project/model choice
   (existing or separately authorized). Agree on process-to-specialist identity
   and callable route before provisioning. This foundation starts no Foundry setup.

The real event start time, venue display aspect ratio and live-demo connectivity
are still open. Timing is elapsed rather than a guessed wall-clock schedule.
