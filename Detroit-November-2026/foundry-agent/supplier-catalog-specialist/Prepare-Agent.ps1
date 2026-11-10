$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot '..\..\foundry-demo'
$target = Join-Path $PSScriptRoot 'src\catalog'
$files = @{
    'demo.py' = 'demo.py'
    'activity_agent.py' = 'main.py'
    'bundles\FC-03\specification.pdf' = 'bundles\FC-03\specification.pdf'
    'bundles\FC-03\supplier.xlsx' = 'bundles\FC-03\supplier.xlsx'
    'bundles\FC-03\packaging.png' = 'bundles\FC-03\packaging.png'
}
foreach ($entry in $files.GetEnumerator()) {
    $inputFile = Join-Path $source $entry.Key
    if (-not (Test-Path -LiteralPath $inputFile -PathType Leaf)) {
        throw "Required source is missing: $inputFile"
    }
}
foreach ($entry in $files.GetEnumerator()) {
    $outputFile = Join-Path $target $entry.Value
    New-Item -ItemType Directory -Force -Path (Split-Path $outputFile) | Out-Null
    Copy-Item -LiteralPath (Join-Path $source $entry.Key) -Destination $outputFile
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'requirements.txt') -Destination (Join-Path $target 'requirements.txt')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot '.agentignore') -Destination (Join-Path $target '.agentignore')
Write-Output 'Staged shared processor, Activity adapter, dependencies, and three synthetic source files. No local inference config or credentials copied.'
