# Coding Agent Instructions

This project was built with the microsoft-foundry skill. Before working on or answering questions about foundry agents, read the microsoft-foundry skill first.

## Detroit scope overrides

- The original CorpDev deployment uses the existing `Detroit-InnoHubDemo`
  resource group only. The separately authorized DTW infrastructure deployment
  uses subscription `b571e36c-4e62-4175-b8c1-062a4cf87b16`, resource group
  `dtw-tool-demo`, and `infra/dtw.parameters.json`. Do not mix the two targets.
- DTW hosted deployment uses `dtw/azure.yaml`, not the original CorpDev manifest.
  The user also approved the hosted agent, supporting Bot/channels, and one
  account-scoped Cognitive Services OpenAI User role for its runtime identity.
  Studio targets the existing `DTW Tool Demo` draft in the Jones-Evans, KC
  developer environment (`0343907b-5031-ed09-acc8-5e9701b25f1d`) with a new
  connection, preserving existing connections. Do not publish the Studio agent.
  Do not publish a Teams app or copy the CorpDev legacy BotService exception.
- Infrastructure is `infra/corpdev.bicep`, applied with a resource-group
  deployment after validation and what-if. Do not run `azd provision`, `azd up`,
  or `azd down`; the root CAIS application is a separate deployment.
- Run `Prepare-Agent.ps1` to stage the shared processor and adapter from
  `../../foundry-demo`. Do not edit the generated `src/catalog` copies.
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
azd deploy                       # Deploy to Foundry (creates the Azure Bot + Teams channel)
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
