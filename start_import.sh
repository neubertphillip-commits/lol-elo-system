#!/bin/bash
# Start import with credentials

export LEAGUEPEDIA_BOT_USERNAME="Ekwo98@Elo"
export LEAGUEPEDIA_BOT_PASSWORD="n7d9rsiccg7hujkg2hvtnglg4h93480r"

echo "Starting import with credentials..."
echo "Bot User: $LEAGUEPEDIA_BOT_USERNAME"
echo ""

python scripts/import_all_historical_data.py
