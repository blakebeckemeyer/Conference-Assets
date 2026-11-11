# November 10 DTW demo closeout

This runbook covers **only the resources created for the November 10, 2026
DTW deployment**. The user authorized removing everything created that day
after review of the Azure group, billing account, and Studio dependencies.
Older CorpDev/CAIS resources and existing Studio environments are not part
of this deletion. Dataverse subsequently confirmed that the DTW Tool Demo
parent agent itself was created that day, so the user's final instruction
includes that exact parent, not just its connected specialist.

## Lessons and review sequence

The initial deployment is recorded in [PR #7](https://github.com/blakebeckemeyer/Conference-Assets/pull/7);
the canonical deployment/access follow-up is [PR #8](https://github.com/blakebeckemeyer/Conference-Assets/pull/8).
Both owners reconciled their original session evidence during closeout.
PR #8 integrates #7's closeout commit and resolves their three overlapping
conflicts. Review #7 before #8; do not independently reapply historical
provisioning commands after teardown.

- Bicep provisioning, hosted source updates, native Studio binding and real
  delegated execution are separate gates. A healthy deployment, local tests
  or a saved connection is not proof of a successful tool result.
- Pin the tenant, subscription, resource group, model quota and project
  endpoint. Do not silently fall back to CorpDev. Preserve isolated staging
  and the seven-file source allowlist; never package local config or tokens.
- Connection ACL access, delegated token exchange and the Activity caller's
  tenant are distinct. Repeating grants to an already-authorized principal
  does not repair missing caller context. A classic assistant inspection
  does not prove a hosted agent's native integration.
- The explicitly approved legacy `BotService` exception bypassed the
  additional per-user RBAC/tenant check; it was not anonymous access or a
  production fix. Repository defaults remain `AzureRbac`/Entra plus
  `BotServiceRbac`. The user reported success, but no successful result JSON,
  run ID, token/model record or field-level verification was captured.
- Provisioning has side effects outside template outputs: Bot/channels,
  directory agent identities, Studio connections/references, a connection
  ACL grant and Power Platform billing. Resource-group deletion alone is not
  proof that the tenant is clean.

The specialist README on #8 retains the detailed SDK compatibility,
authentication investigation, source deployment and rollback evidence.
Historical "active" observations describe the rehearsal, not a guarantee
that these resources still exist.

## Bicep equivalent of apply and destroy

This repo uses resource-group-scoped **Bicep/ARM**, with Azure Developer CLI
configuration for selected deployments. It does not have Terraform state
or a generic Bicep `destroy` command.

For a future, separately approved deployment, compile and validate the
specific Bicep entry point and inspect `az deployment group what-if` before
`az deployment group create`. The initial DTW project/model entry point is
`foundry-agent\supplier-catalog-specialist\infra\corpdev.bicep` with
`infra\dtw.parameters.json` from #7/#8; the name is historical. That template
is not a complete reconstruction of every supporting or Studio resource.
The root `infra\main.bicep` and root `azure.yaml` have historical targets:
do not apply them with defaults to recreate this demo.

For this **dedicated disposable group**, the teardown operation is
`az group delete`, followed by checks for out-of-group artifacts below.
`az deployment group delete` only removes deployment history, not resources.
Do not use ARM complete mode or an empty template as an improvised destroy:
that obscures scope and does not cover directory/Power Platform objects.
Do not run an unscoped `azd down` against the older shared projects.

```powershell
$subscription = 'b571e36c-4e62-4175-b8c1-062a4cf87b16'
$tenant = 'f32b97f0-efb8-4bc3-91ee-18a6e5f635c9'
$group = 'dtw-tool-demo'
$account = az account show --output json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect Azure authentication.' }
if ($account.id -ne $subscription -or $account.tenantId -ne $tenant) {
    throw 'Wrong Azure CLI profile; select the approved DTW profile first.'
}

# Read-only preview: inspect every resource and any deletion locks.
az resource list --subscription $subscription --resource-group $group --output table
if ($LASTEXITCODE -ne 0) { throw 'Resource inventory failed.' }
az lock list --subscription $subscription --resource-group $group --output json
if ($LASTEXITCODE -ne 0) { throw 'Lock inventory failed.' }

# Destructive: only after approval and review of the exact inventory.
# Delete the hosted agent (including its sessions) using the API below first.
# Permanently delete the ACTIVE workspace before group deletion to avoid
# having to recover a soft-deleted workspace just to purge it afterward.
az monitor log-analytics workspace delete --subscription $subscription `
  --resource-group $group --workspace-name log-supplier-dev-b571 --force true --yes
if ($LASTEXITCODE -ne 0) { throw 'Workspace deletion failed.' }
az group delete --subscription $subscription --name $group --yes --no-wait
if ($LASTEXITCODE -ne 0) { throw 'Deletion request failed; inspect before retrying.' }
az group wait --subscription $subscription --name $group --deleted --interval 15 --timeout 1800
if ($LASTEXITCODE -ne 0) { throw 'Deletion is not verified; inspect current state.' }
az group exists --subscription $subscription --name $group
if ($LASTEXITCODE -ne 0) { throw 'Final existence check failed.' }
# Required result: false. An authorization error is not proof of absence.
```

The hosted agent initially refused deletion because idle/non-expired sessions
were present. The authorized full teardown used the documented cascading
delete, terminating those sessions as well:

```http
DELETE https://dtw-tool-demo-b571.services.ai.azure.com/api/projects/detroit-catalog/agents/supplier-catalog-specialist?api-version=v1&force=true
Authorization: Bearer <token for https://ai.azure.com/>
```

On Windows, `az.cmd` can misparse URLs containing `&` or parentheses, even
when PowerShell quoted them. Use `Invoke-RestMethod` with an in-memory token,
or invoke Azure CLI's actual Python entry point, for these REST calls.
Do not treat a shell-parsing failure as a cloud authorization failure.
Never print or save access tokens.

### Confirmed Azure inventory before deletion

The group was tagged `deployed-by=conference-demo`,
`environment=supplier-dev-b571`. The main deployment and Power Platform
billing deployment were dated November 10; there were no deletion locks.

| Resource | Purpose |
|---|---|
| `dtw-tool-demo-b571` / `detroit-catalog` | Foundry account/project, model `gpt-6.1-sol`, hosted specialist versions |
| `supplier-catalog-specialist-bot-f0ea37c8` | Azure Bot and Teams/WebChat/DirectLine channels |
| `ca-supplier-dev-b571`, `cae-supplier-dev-b571` | Placeholder Container App and managed environment |
| `crsupplierdevb571` | Container Registry |
| `log-supplier-dev-b571`, `appi-supplier-dev-b571` | Logs and Application Insights |
| `Application Insights Smart Detection` and its failure-anomaly rule | Automatically created monitoring |
| `kv-supplier-dev-b571` | Key Vault; soft delete enabled, seven-day retention |
| `DTWDemoNovember` | Power Platform billing account, created November 10 at 17:42 UTC |

The Container Apps environment reported no infrastructure resource group.
The Bot uses the specialist runtime identity below, not an independently
identified app registration. Role assignments scoped inside this group
must disappear with their scopes; preserve inherited subscription roles.

## Outside the Azure group

Inspect dependencies before removal, use exact IDs and retain unrelated
objects. Do not delete an entire Power Platform environment or older agent.
Do not revoke tenant-wide service principals or inherited owner access.

| Object | Scoped cleanup |
|---|---|
| Studio environment `0343907b-5031-ed09-acc8-5e9701b25f1d` | Preserve |
| DTW Tool Demo agent `781a5f55-6bc3-473d-b085-455c881026c5` | Created November 10 at 17:36:29 UTC; remove this demo parent and its components |
| Connected-agent component `3438d475-f38d-4140-8327-92561f46515e` | Remove today's `Supplier Catalog Specialist DTW` binding |
| Connection `b3547013461c46ebb920b8bd97bc04c6` | Remove today's `Detroit DTW Catalog Foundry` connection after detaching dependents |
| Reference `cr56a_dtwtooldemo_3GpJ0w.cr.shared_azureagentservice.b3547013461c46ebb920b8bd97bc04c6` | Inspect/remove today's orphan reference after detachment |
| Reference `new_sharedazureagentservice_f500d639` (`54c0e698-31dd-f111-84ea-0022480ba974`) | Second reference to the same new connection, created at 18:07:32 UTC; inspect/remove after detachment |
| Original connection `shared-azureagentser-02b35a76-7231-4904-84d9-67d8be3d9764` | Preserve; revoke only today's added `CanView` grant for principal `e4af4ca3-101d-42f7-9628-57b4ea081da5` |
| Power Virtual Agents Service app `9d8f559b-5984-46a4-902a-ad4271e83efa` | Preserve; this is not a demo-created principal |
| Billing policy `fe05b4d4-f15a-401f-8523-8a8262b95e1c` | Delete this November 10 `DTWDemoNovember` policy and its environment association separately from the Azure billing account |
| Hosted identity blueprint app `36a52b2c-90c8-44d4-afc1-5e8b4dbc015e`, principal `d2b9193b-42d2-4aba-85dd-e9836054f09c` | Inspect service-managed lifecycle and remove only confirmed orphan demo objects |
| Runtime service identity `64fc7e7c-43fe-4f48-bc23-caa4541ede3d` | Inspect after hosted resource removal; created November 10 at 17:54 UTC |
| Project blueprint app/object `cde51079-6416-4519-b590-fd630139ed37` / `d0e3049e-6a1f-4f76-b72a-5d465397b33f`, identity `7c8b6ed7-14d7-49eb-899d-7678e7ac7a01` | Historical provisioning IDs; verify existence, ownership and lifecycle before cleanup |

The older connection was created September 10, and the developer environment
August 21; preserve both. Delete only the confirmed November 10 demo parent;
do not publish or alter unrelated agents, tools, knowledge or connections.

### Studio, connection access and billing procedure

The authenticated Power Apps environment read-back identified this developer
environment's Dataverse URL as `https://org0333f422.crm.dynamics.com/`.
Do not confuse it with the older `dtw-innovation` exercise environment.
The Web API supports deletion of the `bot`, `botcomponent` and
`connectionreference` rows used here.

1. Read the exact bot and its components through `/api/data/v9.2/bots` and
   `/api/data/v9.2/botcomponents`. Verify parent IDs and creation dates, not
   display names alone. Delete the nine November 10 dependent components
   with their fresh `If-Match` ETags, then the parent with its fresh ETag.
   The initial parent-only delete correctly refused while nine dependencies
   existed; do not bypass dependency checks.
2. Query `/api/data/v9.2/connectionreferences` for `connectionid eq
   'b3547013461c46ebb920b8bd97bc04c6'`. The parent deletion cascaded the
   `cr56a` reference. Delete the remaining confirmed November 10
   `new_sharedazureagentservice_f500d639` reference using its ETag. Require
   successful empty bot/component/reference collections afterward.
3. Read, date-check and delete the new connection through the admin connection
   URL below with `api-version=2017-06-01`. A subsequent connector connection
   list must retain the September connection and exclude the new connection.
4. On the September connection, read `/permissions` and match the exact
   `CanView` role, permission name `b9345c78-bdd1-4c86-b5d0-fa261dc4c6c2`
   and runtime principal above. Revoke only its returned full permission
   `id`, using `{"delete":[{"id":"<returned-permission-id>"}]}`.
   Read back permissions and compare every unrelated grant.
5. Read the Power Platform billing policies, match the exact policy ID,
   November 10 creation date and Azure subscription/group, then delete that
   policy. Require its absence from a successful policy list; an Azure account
   deletion alone did **not** remove this policy during this teardown.

Admin connection API prefix (token audience `https://service.powerapps.com/`):

```text
https://api.powerapps.com/providers/Microsoft.PowerApps/scopes/admin/environments/0343907b-5031-ed09-acc8-5e9701b25f1d/apis/shared_azureagentservice/connections/
```

The admin-scoped `modifyPermissions` call rejected even revocation with
`ConnectionSharingNotAllowed` on this non-shareable connection. The official
**owner-scoped** `Remove-PowerAppConnectionRoleAssignment` route succeeded,
without changing `allowSharing`, consent, roles or the older connection:

```http
POST https://api.powerapps.com/providers/Microsoft.PowerApps/apis/shared_azureagentservice/connections/shared-azureagentser-02b35a76-7231-4904-84d9-67d8be3d9764/modifyPermissions?api-version=2017-06-01&$filter=environment%20eq%20%270343907b-5031-ed09-acc8-5e9701b25f1d%27
Content-Type: application/json

{"delete":[{"id":"<full-id-from-the-matching-permission-read>"}]}
```

This is the supported owner revocation interface, not a sharing-policy
workaround. The final ACL contained only the original Owner. Neither the
original connection nor the Power Virtual Agents Service principal was deleted.

Billing-policy API (token audience `https://api.powerplatform.com`):

```http
GET https://api.powerplatform.com/licensing/billingPolicies?api-version=2022-03-01-preview
DELETE https://api.powerplatform.com/licensing/billingPolicies/fe05b4d4-f15a-401f-8523-8a8262b95e1c?api-version=2022-03-01-preview
```

Deletion returned HTTP 204 and the subsequent policy list was empty.
The policy had linked only the preserved developer environment. Deleting its
association does not delete that environment. Charges already incurred can
still appear later; deletion does not reverse historical usage.

### Retained resources and directory lifecycle

Key Vault, Cognitive Services and Log Analytics can retain deleted objects. Inspect
the exact subscription, location and name after resource deletion. Purge
only these confirmed demo objects if permanent deletion is authorized;
never bulk-purge the tenant. Purge protection, retention and lack of
directory permissions can leave administrator follow-up. Verify service
responses, not just command submission or a vanished portal row.

```powershell
az keyvault purge --subscription $subscription --name kv-supplier-dev-b571 --location eastus
az cognitiveservices account purge --subscription $subscription `
  --resource-group $group --name dtw-tool-demo-b571 --location eastus
az keyvault list-deleted --subscription $subscription
az cognitiveservices account list-deleted --subscription $subscription
az monitor log-analytics workspace list-deleted-workspaces --subscription $subscription
```

Log Analytics requires special care: `workspace delete --force true` on an
**already soft-deleted** workspace can return success without removing its
retained entry. Microsoft's documented procedure is to recover that exact
workspace and then permanently delete it. If its group was also deleted,
re-create only the same empty group to recover/purge the workspace, then
delete that temporary group. Do not recover the whole demo or redeploy Bicep.
Prefer permanently deleting the active workspace before group deletion, as
shown above.

The Foundry service automatically removed both recorded identity blueprints
and their four principals. Successful, ID-filtered Microsoft Graph collection
reads confirmed no matching active applications/principals **or** recycled
applications/principals. The account and Container App managed-identity
principals were also absent. No manual directory deletes or shared-principal
permission changes were needed.

## Execution record

Closeout started November 10 local time (November 11 UTC). Cleanup status
will be recorded here from post-operation read-backs; an inventory or an
accepted deletion request is not a completed teardown.

| Area | Verified outcome |
|---|---|
| Azure resource group | Pending deletion |
| Power Platform billing | Azure account absent; separate policy deleted HTTP 204 and policy list empty at 01:30:38 UTC |
| Studio demo parent/components/connection/references | Parent and nine components deleted by 01:25:36 UTC; empty parent/component/reference reads and new-connection deletion at 01:26:04 UTC; connector list retained only the September connection at 01:28:58 UTC |
| Original-connection ACL grant | Revoked through owner interface at 01:29:59 UTC; original Owner preserved |
| Directory agent identities | Both blueprint apps/four principals absent from active and recycled collections at 01:29:20 UTC; both resource-managed principals absent at 01:31:05 UTC |
| Soft-deleted resources | Key Vault and Foundry purged; lists empty at 01:28:58 UTC. Log Analytics retained-workspace cleanup still in progress |
| CorpDev, CAIS, older connections and existing environments | Excluded from deletion |

References: [delete an Azure resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group),
[Key Vault recovery and purge](https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview),
[Cognitive Services recovery and purge](https://learn.microsoft.com/en-us/azure/ai-services/recover-purge-resources),
[hosted-agent lifecycle](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/manage-hosted-agent),
[Dataverse bot operations](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/reference/bot),
[billing-policy removal](https://learn.microsoft.com/en-us/power-platform/admin/pay-as-you-go-set-up#turn-off-pay-as-you-go),
[Log Analytics deletion and recovery](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/delete-workspace).
