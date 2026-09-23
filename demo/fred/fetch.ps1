# Run from the repository root to refresh the two public FRED series.
$ErrorActionPreference = 'Stop'
$outputDir = Join-Path (Get-Location).Path 'demo\fred\live'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
$outputFile = Join-Path $outputDir 'fred_latest.csv'
$url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL%2CFEDFUNDS'

& curl.exe -fL --retry 2 --max-time 30 -sS -o $outputFile $url
if ($LASTEXITCODE -ne 0) { throw "FRED download failed (curl exit code $LASTEXITCODE)." }
if ((Get-Item -LiteralPath $outputFile).Length -lt 100) { throw 'FRED download is unexpectedly short.' }
$header = Get-Content -LiteralPath $outputFile -TotalCount 1
if ($header -ne 'observation_date,CPIAUCSL,FEDFUNDS') { throw "Unexpected FRED CSV header: $header" }

Write-Output "Saved $outputFile"
