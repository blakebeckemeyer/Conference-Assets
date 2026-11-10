targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
param environmentName string

@minLength(1)
param location string

param sessionId string
param deployedBy string = 'conference-demo'
param createdAt string

param containerAppsEnvironmentName string = 'cae-supplier-dev-f736'
param containerAppName string = 'ca-supplier-dev-f736'
param containerRegistryName string = 'crsupplierdevf736'
param logAnalyticsWorkspaceName string = 'log-supplier-dev-f736'
param applicationInsightsName string = 'appi-supplier-dev-f736'
param keyVaultName string = 'kv-supplier-dev-f736'
param foundryAccountName string = 'dtw-tool-demo'

@description('Explicit tenant allowlist for inbound v2 API tokens. Use the Copilot Studio tenant only unless another tenant is separately approved.')
param catalogAllowedTenantIds array = [
  '1b37c04e-260e-4189-a11b-0b8609ed3df0'
]
@description('For Microsoft Entra v2 access tokens, set this to the API application client ID (GUID), not its api:// application ID URI.')
param catalogApiAudience string = ''
@description('Override with the built image URI for phase 2. Phase 1 uses the public placeholder image.')
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
@description('Optional deployer object ID for Key Vault secret administration. Leave empty when no secret seeding is needed.')
param deployerObjectId string = ''

var tags = {
  'app-onboard-skill': 'true'
  'app-onboard-session-id': sessionId
  'created-at': createdAt
  environment: environmentName
  'deployed-by': deployedBy
}

module observability './modules/observability.bicep' = {
  name: 'supplier-observability'
  params: {
    location: location
    workspaceName: logAnalyticsWorkspaceName
    environmentName: containerAppsEnvironmentName
    tags: tags
  }
}

module registry './modules/container-registry.bicep' = {
  name: 'supplier-container-registry'
  params: {
    location: location
    name: containerRegistryName
    tags: tags
  }
}

module keyVault './modules/key-vault.bicep' = {
  name: 'supplier-key-vault'
  params: {
    location: location
    name: keyVaultName
    tags: tags
  }
}

module appInsights './modules/application-insights.bicep' = {
  name: 'supplier-application-insights'
  params: {
    location: location
    name: applicationInsightsName
    workspaceResourceId: observability.outputs.workspaceId
    tags: tags
  }
}

module containerApp './modules/container-app.bicep' = {
  name: 'supplier-catalog-api'
  params: {
    location: location
    name: containerAppName
    environmentId: observability.outputs.environmentId
    registryServer: registry.outputs.loginServer
    containerImage: containerImage
    catalogAllowedTenantIds: catalogAllowedTenantIds
    catalogApiAudience: catalogApiAudience
    tags: tags
  }
}

module roleAssignments './modules/role-assignments.bicep' = {
  name: 'supplier-role-assignments'
  params: {
    registryName: registry.outputs.name
    keyVaultName: keyVault.outputs.name
    foundryAccountName: foundryAccountName
    containerAppPrincipalId: containerApp.outputs.principalId
    deployerObjectId: deployerObjectId
  }
}

output resourceGroupName string = resourceGroup().name
output containerAppName string = containerApp.outputs.name
output containerAppFqdn string = containerApp.outputs.fqdn
output registryLoginServer string = registry.outputs.loginServer
output foundryRoleScope string = roleAssignments.outputs.foundryAccountId
