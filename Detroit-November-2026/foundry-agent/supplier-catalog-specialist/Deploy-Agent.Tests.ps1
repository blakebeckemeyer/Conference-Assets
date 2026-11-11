Describe 'DTW source-only specialist deployment' {
    BeforeEach {
        $script:deployScript = Join-Path $PSScriptRoot 'Deploy-Agent.ps1'
        $global:DtwDeploymentTestState = @{
            tenant = 'f32b97f0-efb8-4bc3-91ee-18a6e5f635c9'
            subscription = 'b571e36c-4e62-4175-b8c1-062a4cf87b16'
            status = 'active'
            botScheme = 'BotServiceRbac'
            isolation = 'Entra'
            protocols = @('activity')
        }
        function az {
            param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)
            $global:LASTEXITCODE = 0
            $state = $global:DtwDeploymentTestState
            if ($Arguments[1] -eq 'show') {
                @{ tenantId = $state.tenant; id = $state.subscription } | ConvertTo-Json
            } elseif ($Arguments[1] -eq 'get-access-token') {
                'offline-test-token'
            } else {
                throw "Unexpected CLI operation: $Arguments"
            }
        }
        Mock Invoke-RestMethod {
            $state = $global:DtwDeploymentTestState
            @{
                name = 'supplier-catalog-specialist'
                versions = @{ latest = @{ id = 'supplier-catalog-specialist:1'; status = $state.status } }
                instance_identity = @{ principal_id = 'unchanged-test-identity' }
                agent_endpoint = @{
                    authorization_schemes = @(
                        @{ type = 'AzureRbac'; isolation_key_source = @{ kind = $state.isolation } }
                        @{ type = $state.botScheme }
                    )
                    protocols = $state.protocols
                }
            } | ConvertTo-Json -Depth 10 | ConvertFrom-Json
        }
        Mock Invoke-WebRequest { throw 'A preview must not upload or download code.' }
    }

    AfterEach {
        Remove-Variable DtwDeploymentTestState -Scope Global
    }

    It 'previews only the existing DTW agent without a cloud write' {
        $result = & $script:deployScript -WhatIf
        $result.Status | Should Be 'NotApplied'
        $result.ProjectEndpoint | Should Be 'https://dtw-tool-demo-b571.services.ai.azure.com/api/projects/detroit-catalog'
        $result.PackageHash | Should Match '^[a-f0-9]{64}$'
        $result.ExecutionVerified | Should Be $false
        Assert-MockCalled Invoke-RestMethod -Times 1 -Exactly -Scope It
        Assert-MockCalled Invoke-WebRequest -Times 0 -Exactly -Scope It
    }

    It 'produces the same package hash for unchanged source' {
        $first = & $script:deployScript -WhatIf
        $second = & $script:deployScript -WhatIf
        $first.PackageHash | Should Be $second.PackageHash
    }

    It 'rejects another tenant before accessing the project' {
        $global:DtwDeploymentTestState.tenant = '11111111-1111-1111-1111-111111111111'
        { & $script:deployScript -WhatIf } | Should Throw 'Use an isolated Azure CLI profile'
        Assert-MockCalled Invoke-RestMethod -Times 0 -Exactly -Scope It
    }

    It 'rejects another subscription before accessing the project' {
        $global:DtwDeploymentTestState.subscription = '11111111-1111-1111-1111-111111111111'
        { & $script:deployScript -WhatIf } | Should Throw 'Use an isolated Azure CLI profile'
        Assert-MockCalled Invoke-RestMethod -Times 0 -Exactly -Scope It
    }

    It 'refuses source updates while the BotService demo exception is active' {
        $global:DtwDeploymentTestState.botScheme = 'BotService'
        { & $script:deployScript -WhatIf } | Should Throw 'Expected existing Activity authorization'
        Assert-MockCalled Invoke-RestMethod -Times 1 -Exactly -Scope It
        Assert-MockCalled Invoke-WebRequest -Times 0 -Exactly -Scope It
    }

    It 'requires Entra isolation' {
        $global:DtwDeploymentTestState.isolation = 'None'
        { & $script:deployScript -WhatIf } | Should Throw 'Expected existing Activity authorization'
    }

    It 'requires an already active specialist' {
        $global:DtwDeploymentTestState.status = 'creating'
        { & $script:deployScript -WhatIf } | Should Throw 'must be active'
    }

    It 'requires the existing Activity protocol' {
        $global:DtwDeploymentTestState.protocols = @('responses')
        { & $script:deployScript -WhatIf } | Should Throw 'Expected existing Activity authorization'
    }
}
