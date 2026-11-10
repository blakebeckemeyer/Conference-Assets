param location string
param name string
param environmentId string
param registryServer string
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param catalogAllowedTenantIds array
param catalogApiAudience string
param tags object

var placeholderImage = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
var isPlaceholder = containerImage == placeholderImage
var effectivePort = isPlaceholder ? 80 : 8000

resource containerApp 'Microsoft.App/containerApps@2025-01-01' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    environmentId: environmentId
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: effectivePort
        transport: 'auto'
        allowInsecure: false
      }
      registries: isPlaceholder ? [] : [
        {
          server: registryServer
          identity: 'system'
        }
      ]
      secrets: []
    }
    template: {
      scale: {
        minReplicas: 0
        maxReplicas: 1
      }
      containers: [
        {
          name: 'supplier-catalog-processor'
          image: containerImage
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'CATALOG_ENV'
              value: 'production'
            }
            {
              name: 'CATALOG_ALLOWED_TENANT_IDS'
              value: join(catalogAllowedTenantIds, ',')
            }
            {
              name: 'CATALOG_API_AUDIENCE'
              value: catalogApiAudience
            }
            {
              name: 'FOUNDRY_AUTH_MODE'
              value: 'managed_identity'
            }
          ]
          probes: isPlaceholder ? [] : [
            {
              type: 'Startup'
              httpGet: {
                path: '/health'
                port: effectivePort
                scheme: 'HTTP'
              }
              initialDelaySeconds: 2
              periodSeconds: 5
              timeoutSeconds: 2
              failureThreshold: 12
            }
            {
              type: 'Liveness'
              httpGet: {
                path: '/health'
                port: effectivePort
                scheme: 'HTTP'
              }
              periodSeconds: 30
              timeoutSeconds: 5
              failureThreshold: 3
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/health'
                port: effectivePort
                scheme: 'HTTP'
              }
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            }
          ]
        }
      ]
    }
  }
}

output id string = containerApp.id
output name string = containerApp.name
output principalId string = containerApp.identity.principalId
output fqdn string = containerApp.properties.configuration.ingress.fqdn
