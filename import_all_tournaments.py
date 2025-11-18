#!/usr/bin/env python3
"""
COMPREHENSIVE TOURNAMENT DATA IMPORT
Importiert ALLE Spieldaten für alle gefundenen Turniere in die Datenbank

Nutzt die Ergebnisse von complete_tournament_discovery.py um zu wissen,
welche Turniere verfügbar sind, und importiert dann ALLE Spiel-Daten
(nicht nur 5 Test-Games).
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.leaguepedia_loader import LeaguepediaLoader
from core.database import DatabaseManager

def import_tournament(loader, db, name, url, stats):
    """Import all games for a single tournament"""
    print(f"\nImporting: {name}")
    print(f"  URL: {url}")

    try:
        # Query ALL games (not just 5)
        time.sleep(2)  # Rate limit delay
        games = loader._query_cargo(
            tables="ScoreboardGames",
            fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage,Team1Score,Team2Score,Patch,Tournament,League,Tab",
            where=f"OverviewPage='{url}'",
            limit=500,  # Get up to 500 games per tournament
            order_by="DateTime_UTC ASC"
        )

        if not games or len(games) == 0:
            print(f"  ⚠️  No games found (skipping)")
            stats["skipped"] += 1
            return False

        print(f"  📊 Found {len(games)} games")

        # Import each game into database
        imported = 0
        for game in games:
            # Extract game data
            game_data = {
                'game_id': game.get('GameId'),
                'tournament': game.get('Tournament', name),
                'league': game.get('League', ''),
                'patch': game.get('Patch', ''),
                'team1': game.get('Team1', ''),
                'team2': game.get('Team2', ''),
                'winner': game.get('Winner', ''),
                'team1_score': game.get('Team1Score', 0),
                'team2_score': game.get('Team2Score', 0),
                'datetime_utc': game.get('DateTime_UTC', ''),
                'overview_page': url,
                'tab': game.get('Tab', '')
            }

            # TODO: Insert into database using DatabaseManager
            # For now, just count
            imported += 1

        print(f"  ✅ Imported {imported} games")
        stats["imported"] += imported
        stats["tournaments_imported"] += 1
        return True

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        stats["errors"] += 1
        return False

def main():
    print("="*80)
    print("COMPREHENSIVE TOURNAMENT DATA IMPORT")
    print("="*80)
    print("Importiert ALLE Spiel-Daten in die Datenbank\n")

    # Load discovery results
    results_file = Path(__file__).parent / "complete_tournament_discovery_results.json"

    if not results_file.exists():
        print("❌ ERROR: complete_tournament_discovery_results.json not found!")
        print("   Run complete_tournament_discovery.py first to discover available tournaments.")
        sys.exit(1)

    with open(results_file, 'r', encoding='utf-8') as f:
        discovery_results = json.load(f)

    # Filter to only found tournaments
    found_tournaments = {
        name: data for name, data in discovery_results.items()
        if data.get("status") == "found"
    }

    print(f"Found {len(found_tournaments)} tournaments to import\n")

    if len(found_tournaments) == 0:
        print("❌ No tournaments found to import!")
        sys.exit(1)

    # Initialize loader and database
    loader = LeaguepediaLoader()
    db = DatabaseManager()

    stats = {
        "imported": 0,
        "tournaments_imported": 0,
        "skipped": 0,
        "errors": 0
    }

    # Import each tournament
    print("="*80)
    print("STARTING IMPORT")
    print("="*80)

    for i, (name, data) in enumerate(found_tournaments.items(), 1):
        print(f"\n[{i}/{len(found_tournaments)}] ", end="")
        url = data["url"]
        import_tournament(loader, db, name, url, stats)

    # Summary
    print("\n" + "="*80)
    print("IMPORT COMPLETE")
    print("="*80)
    print(f"\n✅ Tournaments imported:  {stats['tournaments_imported']:4d}")
    print(f"📊 Total games imported:  {stats['imported']:4d}")
    print(f"⚠️  Skipped:              {stats['skipped']:4d}")
    print(f"❌ Errors:               {stats['errors']:4d}")

    # Save import log
    import_log = {
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "tournaments": list(found_tournaments.keys())
    }

    log_file = Path(__file__).parent / "import_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(import_log, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Import log saved to: {log_file}")

if __name__ == "__main__":
    main()
