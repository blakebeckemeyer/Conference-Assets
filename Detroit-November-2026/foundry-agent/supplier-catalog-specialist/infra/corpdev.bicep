// Based on the ejected microsoft.foundry account/project template.
// Deliberately resource-group scoped: no RG creation or role assignments.
targetScope = 'resourceGroup'

param location string = 'eastus'
param accountName string = 'cog-${uniqueString(resourceGroup().id, location)}'
param projectName string = 'detroit-catalog'
param modelCapacity int = 3

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: accountName
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: true
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
  }
}

resource model 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: 'gpt-6.1-sol'
  sku: {
    name: 'GlobalStandard'
    capacity: modelCapacity
  }
  properties: {
    raiPolicyName: 'Microsoft.DefaultV2'
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    model: {
      format: 'OpenAI'
      name: 'gpt-6.1-sol'
      version: '2026-09-29'
    }
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: account
  name: projectName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'Detroit catalog specialist'
    description: 'Synthetic catalog extraction with deterministic evidence validation; no publication.'
  }
  dependsOn: [
    model
  ]
}

output AZURE_AI_PROJECT_ID string = project.id
output AZURE_AI_ACCOUNT_NAME string = account.name
output AZURE_AI_PROJECT_NAME string = project.name
output AZURE_OPENAI_ENDPOINT string = 'https://${account.name}.openai.azure.com/'
output FOUNDRY_PROJECT_ENDPOINT string = 'https://${account.name}.services.ai.azure.com/api/projects/${project.name}'
