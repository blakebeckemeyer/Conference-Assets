#requires -Version 7.1
[CmdletBinding(SupportsShouldProcess)]
param()

$ErrorActionPreference = 'Stop'
$tenant = 'f32b97f0-efb8-4bc3-91ee-18a6e5f635c9'
$subscription = 'b571e36c-4e62-4175-b8c1-062a4cf87b16'
$endpoint = 'https://dtw-tool-demo-b571.services.ai.azure.com/api/projects/detroit-catalog'
$agentName = 'supplier-catalog-specialist'
$agentUrl = "$endpoint/agents/${agentName}?api-version=v1"

$accountJson = az account show --output json
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect the current Azure CLI account.' }
$account = $accountJson | ConvertFrom-Json
if ($account.tenantId -ne $tenant -or $account.id -ne $subscription) {
    throw "Use an isolated Azure CLI profile for DTW tenant $tenant, subscription $subscription. No profile was changed."
}
$token = az account get-access-token --tenant $tenant --resource https://ai.azure.com/ --query accessToken --output tsv
if ($LASTEXITCODE -ne 0 -or -not $token) { throw 'Cannot obtain a DTW Foundry token.' }
$headers = @{ Authorization = "Bearer $token" }
$existing = Invoke-RestMethod -Uri $agentUrl -Headers $headers
if ($existing.name -ne $agentName -or $existing.versions.latest.status -ne 'active') {
    throw 'The existing DTW specialist must be active before a source-only update.'
}
$schemes = @($existing.agent_endpoint.authorization_schemes)
if ($schemes.Count -ne 2 -or
    @($schemes | Where-Object { $_.type -eq 'AzureRbac' -and $_.isolation_key_source.kind -eq 'Entra' }).Count -ne 1 -or
    @($schemes | Where-Object { $_.type -eq 'BotServiceRbac' }).Count -ne 1 -or
    $existing.agent_endpoint.protocols -notcontains 'activity') {
    throw 'Expected existing Activity authorization: AzureRbac with Entra isolation and BotServiceRbac. No authorization was changed.'
}
$beforeEndpoint = $existing.agent_endpoint | ConvertTo-Json -Depth 20 -Compress
$beforeIdentity = $existing.instance_identity.principal_id
$beforeVersion = $existing.versions.latest.id

& {
    $WhatIfPreference = $false
    & (Join-Path $PSScriptRoot 'Prepare-Agent.ps1') | Write-Verbose
}
$source = Join-Path $PSScriptRoot 'src\catalog'
$files = @('.agentignore', 'demo.py', 'main.py', 'requirements.txt',
    'bundles/FC-03/packaging.png', 'bundles/FC-03/specification.pdf', 'bundles/FC-03/supplier.xlsx')
$zipPath = Join-Path ([IO.Path]::GetTempPath()) ("supplier-dtw-$([guid]::NewGuid()).zip")
try {
    $archive = [IO.Compression.ZipFile]::Open($zipPath, [IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($file in $files) {
            $path = Join-Path $source ($file.Replace('/', '\'))
            $entry = $archive.CreateEntry($file)
            $entry.LastWriteTime = [DateTimeOffset]::new(2000, 1, 1, 0, 0, 0, [TimeSpan]::Zero)
            $inputStream = [IO.File]::OpenRead($path)
            $outputStream = $entry.Open()
            try { $inputStream.CopyTo($outputStream) }
            finally { $outputStream.Dispose(); $inputStream.Dispose() }
        }
    } finally { $archive.Dispose() }
    $hash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if (-not $PSCmdlet.ShouldProcess("$endpoint / $agentName", "Deploy allowlisted source package $hash; preserve endpoint authorization, routing and identity")) {
        [pscustomobject]@{ Status = 'NotApplied'; ProjectEndpoint = $endpoint; Agent = $agentName; PackageHash = $hash; ExecutionVerified = $false }
        return
    }

    $current = Invoke-RestMethod -Uri $agentUrl -Headers $headers
    if ($current.versions.latest.id -ne $beforeVersion -or
        ($current.agent_endpoint | ConvertTo-Json -Depth 20 -Compress) -cne $beforeEndpoint -or
        $current.instance_identity.principal_id -ne $beforeIdentity) {
        throw 'The live agent changed during packaging; inspect it again before deploying.'
    }
    $environment = $existing.versions.latest.definition.environment_variables | ConvertTo-Json | ConvertFrom-Json -AsHashtable
    $environment.AZURE_TENANT_ID = $tenant
    $environment.AZURE_OPENAI_ENDPOINT = 'https://dtw-tool-demo-b571.openai.azure.com/'
    $environment.AZURE_AI_MODEL_DEPLOYMENT_NAME = 'gpt-6.1-sol'
    $environment.FOUNDRY_AUTH_MODE = 'managed_identity'
    $environment.PYTHONNOUSERSITE = '1'
    $metadata = @{
        description = $existing.versions.latest.description
        definition = @{
            kind = 'hosted'; cpu = '0.5'; memory = '1Gi'
            protocol_versions = @(@{ protocol = 'activity'; version = '2.0.0' })
            code_configuration = @{
                runtime = 'python_3_13'; entry_point = @('python', 'main.py'); dependency_resolution = 'remote_build'
            }
            environment_variables = $environment
        }
    } | ConvertTo-Json -Depth 20
    $client = [Net.Http.HttpClient]::new()
    $form = [Net.Http.MultipartFormDataContent]::new()
    try {
        $client.DefaultRequestHeaders.Authorization = [Net.Http.Headers.AuthenticationHeaderValue]::new('Bearer', $token)
        $client.DefaultRequestHeaders.Add('x-ms-code-zip-sha256', $hash)
        $form.Add([Net.Http.StringContent]::new($metadata, [Text.Encoding]::UTF8, 'application/json'), 'metadata')
        $code = [Net.Http.StreamContent]::new([IO.File]::OpenRead($zipPath))
        $code.Headers.ContentType = [Net.Http.Headers.MediaTypeHeaderValue]::new('application/zip')
        $form.Add($code, 'code', "$agentName.zip")
        $response = $client.PostAsync("$endpoint/agents/$agentName/versions?api-version=v1", $form).GetAwaiter().GetResult()
        try {
            $body = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
            if (-not $response.IsSuccessStatusCode) { throw "Source deployment failed ($([int]$response.StatusCode)): $body" }
            $version = $body | ConvertFrom-Json
        } finally { $response.Dispose() }
    } finally { $form.Dispose(); $client.Dispose() }
    if (-not $version.version) { throw 'The service did not return a deployment version.' }
    $deadline = [DateTime]::UtcNow.AddMinutes(10)
    do {
        $state = Invoke-RestMethod -Uri "$endpoint/agents/$agentName/versions/$($version.version)?api-version=v1" -Headers $headers
        if ($state.status -eq 'active') { break }
        if ($state.status -eq 'failed') { throw "Deployment failed: $($state.error | ConvertTo-Json -Depth 10 -Compress)" }
        if ([DateTime]::UtcNow -ge $deadline) { throw "Timed out waiting for $($state.id). Last status: $($state.status)." }
        Start-Sleep -Seconds 5
    } while ($true)
    $after = Invoke-RestMethod -Uri $agentUrl -Headers $headers
    if ($after.versions.latest.id -ne $state.id -or $after.versions.latest.status -ne 'active') {
        throw 'The latest deployment changed during verification; inspect the current version before proceeding.'
    }
    if (($after.agent_endpoint | ConvertTo-Json -Depth 20 -Compress) -cne $beforeEndpoint -or
        $after.instance_identity.principal_id -ne $beforeIdentity) {
        throw 'Deployment is active but endpoint or identity changed unexpectedly; inspect before proceeding.'
    }
    $download = Invoke-WebRequest -Uri "$endpoint/agents/$agentName/code:download?api-version=v1&agent_version=$($version.version)" -Headers $headers
    $downloadHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([byte[]]$download.Content)).ToLowerInvariant()
    if ($state.definition.code_configuration.content_hash -ne $hash -or $downloadHash -ne $hash) {
        throw 'The active deployed package does not match the uploaded source.'
    }
    [pscustomobject]@{ Status = 'DeploymentActive'; ProjectEndpoint = $endpoint; Agent = $agentName; Version = $state.id; PackageHash = $hash; ExecutionVerified = $false }
} finally {
    $token = $null
    if (Test-Path -LiteralPath $zipPath) {
        Remove-Item -LiteralPath $zipPath -WhatIf:$false -Confirm:$false
    }
}
