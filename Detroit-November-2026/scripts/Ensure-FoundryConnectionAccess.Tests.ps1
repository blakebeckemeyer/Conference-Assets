Describe 'Native Foundry connection access' {
    BeforeEach {
        $script:repairScript = Join-Path $PSScriptRoot 'Ensure-FoundryConnectionAccess.ps1'
        $script:parameters = @{
            TenantId = '11111111-1111-1111-1111-111111111111'
            EnvironmentId = '22222222-2222-2222-2222-222222222222'
            ConnectionName = 'shared-azureagentser-test'
        }
        # The fake CLI is invoked from another script; share state across scopes.
        $global:FoundryConnectionAccessTestState = @{
            tenant = $script:parameters.TenantId
            runtimeId = '33333333-3333-3333-3333-333333333333'
            appId = '9d8f559b-5984-46a4-902a-ad4271e83efa'
            environmentId = $script:parameters.EnvironmentId
            connectionName = $script:parameters.ConnectionName
            allowSharing = $true
            connectionStatus = 'Connected'
            posts = 0
            reads = 0
            body = $null
            failRead = $false
            failWrite = $false
            malformedAcl = $false
            nextLink = $null
            secondPage = @()
            urls = @()
        }
        $script:owner = @{
            name = 'owner'
            properties = @{ roleName = 'Owner'; principal = @{ id = 'owner' } }
        }
        $script:editor = @{
            name = 'editor'
            properties = @{ roleName = 'CanEdit'; principal = @{ id = 'editor' } }
        }
        $script:grant = @{
            name = $global:FoundryConnectionAccessTestState.runtimeId
            properties = @{
                roleName = 'CanView'
                principal = @{ id = $global:FoundryConnectionAccessTestState.runtimeId }
            }
        }
        $global:FoundryConnectionAccessTestState.before = @($script:owner, $script:editor, $script:grant)
        $global:FoundryConnectionAccessTestState.after = @($script:owner, $script:editor, $script:grant)

        function az {
            param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)
            $global:LASTEXITCODE = 0
            $state = $global:FoundryConnectionAccessTestState
            switch ($Arguments[0]) {
                'account' { @{ tenantId = $state.tenant } | ConvertTo-Json }
                'ad' { @{ id = $state.runtimeId; appId = $state.appId } | ConvertTo-Json }
                'rest' {
                    $url = $Arguments[[array]::IndexOf($Arguments, '--url') + 1]
                    $state.urls += $url
                    if ($Arguments -contains 'post') {
                        $state.posts++
                        $state.body = $Arguments[[array]::IndexOf($Arguments, '--body') + 1] | ConvertFrom-Json
                        if ($state.failWrite) { $global:LASTEXITCODE = 1 }
                    } elseif ($url -notmatch '/permissions\?') {
                        if ($state.failRead) {
                            $global:LASTEXITCODE = 1
                        } else {
                            @{
                                name = $state.connectionName
                                properties = @{
                                    environment = @{ name = $state.environmentId }
                                    allowSharing = $state.allowSharing
                                    statuses = @(@{ status = $state.connectionStatus })
                                }
                            } | ConvertTo-Json -Depth 8
                        }
                    } else {
                        $state.reads++
                        if ($state.failRead) {
                            $global:LASTEXITCODE = 1
                        } elseif ($state.malformedAcl) {
                            '{"value":null}'
                        } elseif ($url -like '*skiptoken=*') {
                            @{ value = $state.secondPage } | ConvertTo-Json -Depth 8
                        } elseif ($state.posts -eq 0) {
                            @{ value = $state.before; nextLink = $state.nextLink } | ConvertTo-Json -Depth 8
                        } else {
                            @{ value = $state.after } | ConvertTo-Json -Depth 8
                        }
                    }
                }
                default { throw "Unexpected CLI operation: $Arguments" }
            }
        }
    }

    AfterEach {
        Remove-Variable -Name FoundryConnectionAccessTestState -Scope Global
    }

    It 'checks existing access without writing' {
        $result = & $script:repairScript @script:parameters
        $result.Status | Should Be 'AdministrativeGrantPresent'
        $result.RuntimePrincipalId | Should Be $global:FoundryConnectionAccessTestState.runtimeId
        $result.ExecutionVerified | Should Be $false
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'does not rewrite an existing grant when repair is requested' {
        (& $script:repairScript @script:parameters -Repair).Status | Should Be 'AdministrativeGrantPresent'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'retains existing stronger runtime access' {
        $script:grant.properties.roleName = 'CanViewWithShare'
        (& $script:repairScript @script:parameters -Repair).Status | Should Be 'AdministrativeGrantPresent'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'fails preflight when access is missing rather than silently repairing' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner, $script:editor)
        { & $script:repairScript @script:parameters } | Should Throw 'Administrative runtime grant is missing'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'repairs only the runtime grant and verifies existing permissions' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner, $script:editor)
        $result = & $script:repairScript @script:parameters -Repair
        $result.Status | Should Be 'AdministrativeGrantAdded'
        $result.ExecutionVerified | Should Be $false
        $global:FoundryConnectionAccessTestState.posts | Should Be 1
        $global:FoundryConnectionAccessTestState.reads | Should Be 2
        $global:FoundryConnectionAccessTestState.body.delete.Count | Should Be 0
        $global:FoundryConnectionAccessTestState.body.put.Count | Should Be 1
        $global:FoundryConnectionAccessTestState.body.put[0].properties.roleName | Should Be 'CanView'
        $global:FoundryConnectionAccessTestState.body.put[0].properties.principal.id | Should Be $global:FoundryConnectionAccessTestState.runtimeId
        $global:FoundryConnectionAccessTestState.urls[2] | Should Match '/shared_azureagentservice/connections/shared-azureagentser-test/modifyPermissions'
    }

    It 'supports WhatIf without modifying permissions' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner)
        (& $script:repairScript @script:parameters -Repair -WhatIf).Status | Should Be 'NotApplied'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'refuses a different signed-in tenant before reading or writing ACLs' {
        $global:FoundryConnectionAccessTestState.tenant = '44444444-4444-4444-4444-444444444444'
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'does not match'
        $global:FoundryConnectionAccessTestState.reads | Should Be 0
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'requires the expected service application' {
        $global:FoundryConnectionAccessTestState.appId = '44444444-4444-4444-4444-444444444444'
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'Could not resolve'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'does not replace an unrecognized existing runtime role' {
        $script:grant.properties.roleName = 'UnexpectedRole'
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'unrecognized connection role'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'surfaces permission-read failure without attempting repair' {
        $global:FoundryConnectionAccessTestState.failRead = $true
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'Azure CLI failed'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'refuses a malformed permissions response without writing' {
        $global:FoundryConnectionAccessTestState.malformedAcl = $true
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'no permissions collection'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'surfaces write failure without retrying' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner)
        $global:FoundryConnectionAccessTestState.failWrite = $true
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'Azure CLI failed'
        $global:FoundryConnectionAccessTestState.posts | Should Be 1
        $global:FoundryConnectionAccessTestState.reads | Should Be 1
    }

    It 'does not report success when the grant is absent after writing' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner)
        $global:FoundryConnectionAccessTestState.after = @($script:owner)
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'could not be verified'
        $global:FoundryConnectionAccessTestState.posts | Should Be 1
    }

    It 'detects changes to existing access during repair' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner, $script:editor)
        $global:FoundryConnectionAccessTestState.after = @($script:owner, $script:grant)
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'existing connection permission changed'
    }

    It 'finds an existing runtime grant on a later permissions page' {
        $global:FoundryConnectionAccessTestState.before = @($script:owner)
        $global:FoundryConnectionAccessTestState.nextLink = "https://api.powerapps.com/providers/Microsoft.PowerApps/scopes/admin/environments/$($script:parameters.EnvironmentId)/apis/shared_azureagentservice/connections/$($script:parameters.ConnectionName)/permissions?api-version=2017-06-01&skiptoken=next"
        $global:FoundryConnectionAccessTestState.secondPage = @($script:grant)
        (& $script:repairScript @script:parameters -Repair).Status | Should Be 'AdministrativeGrantPresent'
        $global:FoundryConnectionAccessTestState.reads | Should Be 2
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'does not send credentials to an unexpected pagination host' {
        $global:FoundryConnectionAccessTestState.nextLink = 'https://example.invalid/permissions'
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'Unexpected permissions pagination URL'
        $global:FoundryConnectionAccessTestState.reads | Should Be 1
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'does not label the observed non-shareable connection and saved grant as runtime compliant' {
        $global:FoundryConnectionAccessTestState.allowSharing = $false
        $result = & $script:repairScript @script:parameters -Repair
        $result.Status | Should Be 'AdministrativeGrantPresent'
        $result.AllowSharing | Should Be $false
        $result.ExecutionVerified | Should Be $false
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'refuses a new grant on a non-shareable connection even with Repair' {
        $global:FoundryConnectionAccessTestState.allowSharing = $false
        $global:FoundryConnectionAccessTestState.before = @($script:owner)
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'connection is non-shareable'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'refuses repair when sharing capability is unknown' {
        $global:FoundryConnectionAccessTestState.allowSharing = $null
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'no sharing capability'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'refuses a connection from another environment' {
        $global:FoundryConnectionAccessTestState.environmentId = '44444444-4444-4444-4444-444444444444'
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'unexpected connection'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }

    It 'refuses repair of a disconnected connection' {
        $global:FoundryConnectionAccessTestState.connectionStatus = 'Error'
        { & $script:repairScript @script:parameters -Repair } | Should Throw 'connection is not Connected'
        $global:FoundryConnectionAccessTestState.posts | Should Be 0
    }
}
