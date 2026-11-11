# Coding Agent Instructions

This project was built with the microsoft-foundry skill. Before working on or answering questions about foundry agents, read the microsoft-foundry skill first.

## Detroit scope overrides

- The canonical target is DTW tenant `f32b97f0-efb8-4bc3-91ee-18a6e5f635c9`,
  subscription `b571e36c-4e62-4175-b8c1-062a4cf87b16`, existing resource group
  `dtw-tool-demo`, account `dtw-tool-demo-b571`, project `detroit-catalog`.
- Reuse the existing `supplier-catalog-specialist`. `Deploy-Agent.ps1` performs
  only a source-version update and verifies unchanged endpoint authorization,
  routing and identity. Preview with `-WhatIf`; it does not provision resources,
  assign roles, create Bots/channels, publish or invoke the specialist.
- Keep `AzureRbac` with Entra isolation and `BotServiceRbac` as the repository
  default. On November 10 the user explicitly approved a reversible, live
  DTW-only `BotService` compatibility exception for the synthetic demo. It was
  applied at 19:18:37 UTC and independently verified at 19:19:29 UTC, retaining
  active v2/package, environment, identity, Activity, routing and `not_published`.
  The exception retains Bot channel authentication but removes additional Bot-user
  RBAC/tenant checks; it is not anonymous access or a caller-context repair.
  Preserve all other endpoint settings. Do not extend it to other agents,
  real supplier data, network access, roles, consent or publication.
- `Deploy-Agent.ps1` deliberately refuses source updates while that legacy
  exception is active. Restore `BotServiceRbac` using the specialist README's
  rollback procedure before a normal source deployment; do not relax the guard
  or silently persist the exception in `azure.yaml`.
- The user subsequently reported the demo working under this exception, but no
  successful tool JSON/run ID or field-level capture was supplied. Distinguish
  that user report from independently verified configuration and expected
  fixtures. Do not treat caller-context propagation as repaired or invoke
  additional processing without separate approval.
- Historical initial DTW provisioning used the group-scoped
  `infra/corpdev.bicep` template with `infra/dtw.parameters.json`, the isolated
  `dtw/azure.yaml` manifest, supporting Bot/channels and approved account-scoped
  runtime inference access. Retain these reproducibility assets, not an
  instruction to recreate resources during closeout. The main `azure.yaml`
  now also uses the canonical explicit DTW configuration.
- Do not run `azd provision`, `azd up`, or `azd down`; the root CAIS application
  is a separate deployment. CorpDev resources must not be changed or deleted
  as part of this migration. Studio uses the existing `DTW Tool Demo` draft in
  environment `0343907b-5031-ed09-acc8-5e9701b25f1d`; do not publish it.
- Run `Prepare-Agent.ps1` to stage the shared processor and adapter from
  `../../foundry-demo` into `src/catalog`. `-Dtw` stages the same seven files
  into the isolated `dtw/src/catalog` directory. Do not edit generated copies.
- Native Copilot Studio delegation, not Teams publication, is the target.
  Do not create Bot/channel resources or role assignments without approval.
- Use isolated CLI/AZD authentication; never change shared profiles.

The upstream sample guidance below describes Activity hosting in general; it
does not expand this deployment's authorization or prove Studio connectivity.

This project is a **Microsoft Foundry hosted agent** — a containerized AI agent that runs in [Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents). The platform handles containerization, hosting, security, scaling, and observability so you can focus on agent logic.

This agent uses the **Activity protocol** (M365 Agents SDK). The conference
caller is Copilot Studio's native Foundry connection, not a Teams app.
The responses/invocations `azd ai agent invoke` path does not test this host.

## Key files

- `../../foundry-demo/activity_agent.py` — source Activity adapter.
- `../../foundry-demo/demo.py` — shared catalog processor.
- `Prepare-Agent.ps1` — stages the allowlisted code and synthetic sources.
- `requirements.txt` — tested Activity/Agents SDK versions.

## Development workflow

The **Azure Developer CLI (`azd`)** manages the full lifecycle:

```bash
azd ai agent run
pwsh -File .\Deploy-Agent.ps1 -WhatIf
pwsh -File .\Deploy-Agent.ps1      # Existing DTW source update only
```

Use the prepared GitHub-harness Studio agent for separately authorized live
tests and verify the actual tool result, not only the orchestrator's summary.
Do not publish or sideload a Teams app to test this conference route.

## Microsoft Foundry Skill

Install the **Microsoft Foundry Skill** for guided deployment, evaluation, and troubleshooting workflows.

Direct install (preferred, works with any coding agent):

```bash
npx skills add https://github.com/microsoft/azure-skills --skill microsoft-foundry
```

Or install the Azure Skills Plugin:

- **Copilot CLI**: `/plugin marketplace add microsoft/azure-skills` then `/plugin install azure@azure-skills`
- **Claude Code**: `/plugin install azure@claude-plugins-official`

Then ask naturally, e.g. `Use the Microsoft Foundry Skill to deploy this agent.`

## References

- [Hosted agents overview](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents)
- [Microsoft Foundry Skill](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/use-microsoft-foundry-skill)
