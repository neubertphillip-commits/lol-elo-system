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
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.leaguepedia_loader import LeaguepediaLoader
from core.database import DatabaseManager
from core.team_resolver import TeamResolver

def aggregate_games_to_matches(games):
    """
    Aggregate individual games into matches

    Groups games by (Team1, Team2, Date, Tab) to form matches,
    then calculates match scores (wins per team)

    Args:
        games: List of game dictionaries from ScoreboardGames

    Returns:
        List of match dictionaries with aggregated scores
    """
    # Group games by match identifier
    matches_dict = defaultdict(list)

    for game in games:
        team1 = game.get('Team1', '').strip()
        team2 = game.get('Team2', '').strip()
        date = game.get('DateTime_UTC', '')
        tab = game.get('Tab', '')

        if not team1 or not team2:
            continue

        # Extract date only (ignore time)
        game_date = date.split()[0] if date else ''

        # Create match key: teams + date + tab
        # Tab helps distinguish multiple matches on same day
        match_key = (team1, team2, game_date, tab)
        matches_dict[match_key].append(game)

    # Aggregate each match
    matches = []
    for (team1, team2, game_date, tab), match_games in matches_dict.items():
        # Count wins for each team
        team1_score = sum(1 for g in match_games if g.get('Winner') == '1')
        team2_score = sum(1 for g in match_games if g.get('Winner') == '2')

        # Use data from first game for shared fields
        first_game = match_games[0]

        match = {
            'team1': team1,
            'team2': team2,
            'team1_score': team1_score,
            'team2_score': team2_score,
            'date': first_game.get('DateTime_UTC', ''),
            'tournament': first_game.get('Tournament', ''),
            'league': first_game.get('League', ''),
            'patch': first_game.get('Patch', ''),
            'tab': tab,
            'overview_page': first_game.get('OverviewPage', ''),
            'num_games': len(match_games),
            'external_id': f"{first_game.get('OverviewPage', '')}_{tab}_{game_date}_{team1}_{team2}"
        }

        matches.append(match)

    return matches

def import_tournament(loader, db, team_resolver, name, url, stats, include_players=False):
    """
    Import all games for a single tournament

    Args:
        loader: LeaguepediaLoader instance
        db: DatabaseManager instance
        team_resolver: TeamResolver instance
        name: Tournament name
        url: Tournament URL
        stats: Statistics dictionary
        include_players: Whether to fetch player data (default: False to avoid query limits)
    """
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

        # Aggregate games into matches
        matches = aggregate_games_to_matches(games)
        print(f"  📊 Aggregated into {len(matches)} matches")

        # Import each match into database
        imported = 0
        duplicates = 0

        for match in matches:
            # Resolve team names using TeamResolver
            team1_resolved = team_resolver.resolve(match['team1'], match['date'])
            team2_resolved = team_resolver.resolve(match['team2'], match['date'])

            # Parse date
            try:
                match_date = datetime.strptime(match['date'], '%Y-%m-%d %H:%M:%S')
            except:
                # Fallback for different date formats
                try:
                    match_date = datetime.strptime(match['date'].split()[0], '%Y-%m-%d')
                except:
                    print(f"    ⚠️  Could not parse date: {match['date']}")
                    continue

            # Insert match into database
            match_id = db.insert_match(
                team1_name=team1_resolved,
                team2_name=team2_resolved,
                team1_score=match['team1_score'],
                team2_score=match['team2_score'],
                date=match_date,
                tournament_name=match['tournament'],
                stage=match['tab'],
                patch=match['patch'],
                external_id=match['external_id'],
                source='leaguepedia',
                region=None,  # Could be extracted from tournament name
                tournament_type=None  # Could be inferred from tournament name
            )

            if match_id:
                imported += 1

                # TODO: Optionally fetch player data if include_players=True
                # This would require additional Cargo queries to ScoreboardPlayers
                # Left disabled by default to avoid query limits

            else:
                duplicates += 1

        print(f"  ✅ Imported {imported} matches ({duplicates} duplicates skipped)")
        stats["imported"] += imported
        stats["duplicates"] += duplicates
        stats["tournaments_imported"] += 1
        return True

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        stats["errors"] += 1
        import traceback
        traceback.print_exc()
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

    # Initialize loader, database, and team resolver
    loader = LeaguepediaLoader()
    db = DatabaseManager()
    team_resolver = TeamResolver(loader=loader, db=db)

    stats = {
        "imported": 0,
        "duplicates": 0,
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
        import_tournament(loader, db, team_resolver, name, url, stats)

    # Summary
    print("\n" + "="*80)
    print("IMPORT COMPLETE")
    print("="*80)
    print(f"\n✅ Tournaments imported:  {stats['tournaments_imported']:4d}")
    print(f"📊 Total matches imported: {stats['imported']:4d}")
    print(f"🔄 Duplicates skipped:    {stats['duplicates']:4d}")
    print(f"⚠️  Skipped:              {stats['skipped']:4d}")
    print(f"❌ Errors:               {stats['errors']:4d}")

    # Save unknown teams for manual review
    unknown_teams = team_resolver.get_unknown_teams()
    if unknown_teams:
        print(f"\n⚠️  Found {len(unknown_teams)} unknown team names")
        unknown_file = Path(__file__).parent / "unknown_teams.txt"
        team_resolver.save_unknown_teams(str(unknown_file))

    # Get database statistics
    db_stats = db.get_stats()
    print(f"\n📊 Database Statistics:")
    print(f"  Total matches: {db_stats['total_matches']}")
    print(f"  Total teams: {db_stats['total_teams']}")
    print(f"  Total tournaments: {db_stats['total_tournaments']}")
    if db_stats['date_range'][0]:
        print(f"  Date range: {db_stats['date_range'][0]} to {db_stats['date_range'][1]}")

    # Save import log
    import_log = {
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "db_stats": db_stats,
        "tournaments": list(found_tournaments.keys()),
        "unknown_teams": unknown_teams
    }

    log_file = Path(__file__).parent / "import_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(import_log, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Import log saved to: {log_file}")

if __name__ == "__main__":
    main()
