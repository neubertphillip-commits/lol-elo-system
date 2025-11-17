# PowerShell script to start import with credentials

$env:LEAGUEPEDIA_BOT_USERNAME = "Ekwo98@Elo"
$env:LEAGUEPEDIA_BOT_PASSWORD = "n7d9rsiccg7hujkg2hvtnglg4h93480r"

Write-Host "Starting import with credentials..." -ForegroundColor Green
Write-Host "Bot User: $env:LEAGUEPEDIA_BOT_USERNAME" -ForegroundColor Cyan
Write-Host ""

python scripts/import_all_historical_data.py
