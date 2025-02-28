param name string
param location string
param tags object = {}
param sku string = 'PerGB2018'
param retentionInDays int = 30

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      name: sku
    }
    retentionInDays: retentionInDays
    features: {
      searchVersion: 1
    }
  }
}

output id string = logAnalytics.id
output name string = logAnalytics.name 