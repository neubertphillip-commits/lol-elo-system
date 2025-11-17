@echo off
REM Batch script to start import with credentials

set LEAGUEPEDIA_BOT_USERNAME=Ekwo98@Elo
set LEAGUEPEDIA_BOT_PASSWORD=n7d9rsiccg7hujkg2hvtnglg4h93480r

echo Starting import with credentials...
echo Bot User: %LEAGUEPEDIA_BOT_USERNAME%
echo.

python scripts\import_all_historical_data.py
