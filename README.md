# Conference-Assets
See what talks I've given, the slide decks as PDFs, and any code assets I shared.

- [Detroit - November 10, 2026: From spec sheet to shelf](Detroit-November-2026/README.md):
  an evolving product-launch use case and offline HTML deck spanning M365
  declarative agents, Microsoft 365 Copilot Cowork, Copilot Studio and Foundry.
  Initial local foundation; platform integrations are not yet deployed.

## Detroit Dataverse MCP

The repository-scoped server **`dataverse-dtw-innovation`** is configured in
`.github/mcp.json` using Streamable HTTP at
`https://dtw-innovation.crm.dynamics.com/api/mcp`. It targets the confirmed Studio
environment `428fc189-ef8f-e8ff-bfc1-ac1aadb32905`, **not** the separate managed-app
environment. This file configures a connection; it does not create tables,
records, an agent or server-side validation.

Review/trust the repository MCP configuration when prompted. In the GitHub
Copilot app, open **Settings > this project > Repository customizations >
MCP servers**, find **dataverse-dtw-innovation**, and choose **Sign in**.
Complete the client's browser-based OAuth sign-in using an account authorized
for this environment. No bearer token, client secret, password or authorization
header belongs in this file. PAC authentication is separate and does not prove
MCP authentication. If the server is not listed after the configuration is
accepted, reopen the project/session to reload repository MCP configuration;
if there is still no row or Sign in action, report that client limitation.

An administrator must verify **Power Platform admin center > Manage >
Environments > Blake-DTW Innovation > Settings > Product > Features >
Dataverse Model Context Protocol**. MCP access must be enabled and the
**Microsoft GitHub Copilot** client allowed under **Advanced Settings**.
Administrator consent, client allowlisting, connector policies and Dataverse
security privileges remain prerequisites; none is changed by this repository
configuration. Managing access through advanced connector policies requires a
Managed Environment. Do not broaden environment permissions to fix a login
without separate authorization.

The local tool allowlist includes current metadata `search`, `describe`,
`read_query`, `create_table`, `update_table` and `create_record` for the
authorized Exercise 5 setup. Delete tools, record updates, file-transfer and
skill-management tools are not enabled. This client filter is not a Dataverse
security role or proof that every enabled operation is authorized. Inspect
negotiated schemas and existing objects before any separately authorized
creation; no Dataverse calls or writes were used to validate this config.
Dataverse MCP calls from clients outside Studio can consume Copilot Credits;
check applicable licensing and billing before invoking tools.

References: [Microsoft Dataverse MCP endpoint and current tools](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-mcp),
[environment/client prerequisites](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-mcp-disable),
[Microsoft's HTTP configuration example](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-mcp-vscode),
and [GitHub's repository MCP configuration paths and schema](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers#adding-per-repository-mcp-servers).
