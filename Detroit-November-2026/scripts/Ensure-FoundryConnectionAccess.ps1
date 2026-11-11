<#
.SYNOPSIS
Checks or repairs the administrative ACL of one native Foundry connection.
.DESCRIPTION
Requires Azure CLI authentication as the connection owner or a Power Platform
administrator in TenantId. Checks only unless -Repair is supplied. Does not
prove token-exchange access, sign in, switch profiles, deploy, publish, or invoke
the specialist. Refuses to add grants to a non-shareable connection.
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory = $true)]
    [guid]$TenantId,

    [Parameter(Mandatory = $true)]
    [guid]$EnvironmentId,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-zA-Z0-9][a-zA-Z0-9-]*$')]
    [string]$ConnectionName,

    [switch]$Repair
)

$ErrorActionPreference = 'Stop'
$azureCli = Get-Command az -ErrorAction Stop
$powerAppsResource = 'https://service.powerapps.com/'
$runtimeAppId = '9d8f559b-5984-46a4-902a-ad4271e83efa'
$connectionUrl = "https://api.powerapps.com/providers/Microsoft.PowerApps/scopes/admin/environments/$EnvironmentId/apis/shared_azureagentservice/connections/$ConnectionName"
$permissionsUrl = "$connectionUrl/permissions?api-version=2017-06-01"
$accessRoles = @('Owner', 'CanView', 'CanViewWithShare', 'CanEdit', 'CanUse', 'CanUseAndShare')

function Invoke-AzureCliJson {
    param([string[]]$Arguments)

    # az.cmd uses legacy Windows argument parsing, even under PowerShell 7.
    if ($azureCli.Source -like '*.cmd') {
        $Arguments = @($Arguments | ForEach-Object { $_.Replace('"', '\"') })
    }
    $output = & $azureCli @Arguments --only-show-errors --output json
    if ($LASTEXITCODE -ne 0) {
        throw "Azure CLI failed (exit code $LASTEXITCODE): $($Arguments[0]). No automatic retry was made."
    }
    if ($output) {
        $output | ConvertFrom-Json -ErrorAction Stop
    }
}

function Get-ConnectionPermissions {
    $url = $permissionsUrl
    do {
        $uri = [uri]$url
        if ($uri.Scheme -ne 'https' -or $uri.Authority -ne 'api.powerapps.com' -or
            $uri.AbsolutePath -ne ([uri]$permissionsUrl).AbsolutePath) {
            throw 'Unexpected permissions pagination URL; refusing to send credentials.'
        }
        $page = Invoke-AzureCliJson -Arguments @(
            'rest', '--method', 'get', '--url', $url, '--resource', $powerAppsResource
        )
        if ($null -eq $page -or $page.value -isnot [array]) {
            throw 'Power Platform returned no permissions collection.'
        }
        $page.value
        $url = $page.nextLink
    } while ($url)
}

$account = Invoke-AzureCliJson -Arguments @('account', 'show')
if ($account.tenantId -ne $TenantId.ToString()) {
    throw "Azure CLI tenant '$($account.tenantId)' does not match '$TenantId'. Sign in with an authorized, preferably isolated profile first."
}

$runtime = Invoke-AzureCliJson -Arguments @('ad', 'sp', 'show', '--id', $runtimeAppId)
$runtimeId = [guid]::Empty
if ($runtime.appId -ne $runtimeAppId -or
    -not [guid]::TryParse($runtime.id, [ref]$runtimeId) -or $runtimeId -eq [guid]::Empty) {
    throw 'Could not resolve the Power Virtual Agents Service principal in the selected tenant.'
}

$connection = Invoke-AzureCliJson -Arguments @(
    'rest', '--method', 'get', '--url', "$connectionUrl`?api-version=2017-06-01",
    '--resource', $powerAppsResource
)
if ($connection.name -ne $ConnectionName -or
    $connection.properties.environment.name -ne $EnvironmentId.ToString() -or
    $connection.properties.allowSharing -isnot [bool]) {
    throw 'Power Platform returned an unexpected connection or no sharing capability. No permissions were changed.'
}
if (@($connection.properties.statuses | Where-Object { $_.status -eq 'Connected' }).Count -eq 0) {
    throw 'The connection is not Connected. Have its owner inspect authentication before changing its ACL.'
}

$before = @(Get-ConnectionPermissions)
$existing = @($before | Where-Object { $_.properties.principal.id -eq $runtimeId.ToString() })
$status = 'AdministrativeGrantPresent'
if ($existing.Count -gt 0) {
    if (@($existing | Where-Object { $_.properties.roleName -in $accessRoles }).Count -eq 0) {
        throw "The runtime has an unrecognized connection role. Inspect the ACL before changing it."
    }
} else {
    if (-not $connection.properties.allowSharing) {
        throw "The connection is non-shareable and has no administrative runtime grant. -Repair cannot establish delegated token access. Inspect the actual agent's connection binding and user authentication; obtain approval before reauthorizing or changing consent."
    }
    if (-not $Repair) {
        throw "Administrative runtime grant is missing on '$ConnectionName'. Rerun with -Repair to add CanView to Power Virtual Agents Service ($runtimeId). This does not verify token exchange."
    }
    if (-not $PSCmdlet.ShouldProcess(
        "$ConnectionName in environment $EnvironmentId",
        "Grant CanView to Power Virtual Agents Service ($runtimeId)"
    )) {
        $status = 'NotApplied'
    } else {
        $body = @{
            delete = @()
            put = @(@{
                properties = @{
                    roleName = 'CanView'
                    principal = @{ id = $runtimeId.ToString() }
                }
            })
        } | ConvertTo-Json -Depth 6 -Compress
        $null = Invoke-AzureCliJson -Arguments @(
            'rest', '--method', 'post',
            '--url', "$connectionUrl/modifyPermissions?api-version=2017-06-01",
            '--resource', $powerAppsResource,
            '--headers', 'Content-Type=application/json', '--body', $body
        )

        $after = @(Get-ConnectionPermissions)
        $saved = @($after | Where-Object {
            $_.properties.principal.id -eq $runtimeId.ToString() -and
            $_.properties.roleName -eq 'CanView'
        })
        if ($saved.Count -ne 1) {
            throw 'Permission update returned, but the runtime CanView grant could not be verified. No automatic retry was made.'
        }
        foreach ($permission in $before) {
            $preserved = @($after | Where-Object {
                $_.name -eq $permission.name -and
                $_.properties.principal.id -eq $permission.properties.principal.id -and
                $_.properties.roleName -eq $permission.properties.roleName
            })
            if ($preserved.Count -eq 0) {
                throw 'An existing connection permission changed during repair. Inspect the ACL; no rollback or automatic retry was made.'
            }
        }
        $status = 'AdministrativeGrantAdded'
    }
}

Write-Warning 'Administrative ACL inspection does not verify token exchange or specialist execution. A recurring 403 despite a saved grant requires investigation of the actual harness connection binding and delegated authentication, not repeated grants or broader roles.'
if (-not $connection.properties.allowSharing) {
    Write-Warning 'This connection is non-shareable. An existing administrative grant does not make its Entra user credentials shareable. Native Foundry delegation supports user-login connections; this flag alone does not establish the cause of a runtime denial.'
}

[pscustomobject]@{
    Status = $status
    TenantId = $TenantId.ToString()
    EnvironmentId = $EnvironmentId.ToString()
    ConnectionName = $ConnectionName
    RuntimePrincipalId = $runtimeId.ToString()
    AllowSharing = $connection.properties.allowSharing
    ExecutionVerified = $false
}
