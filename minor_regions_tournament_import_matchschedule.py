#!/usr/bin/env python3
"""
MINOR REGIONS TOURNAMENT DATA IMPORT - Using MatchSchedule Table
Importiert Match-Daten für Minor Region Turniere

WICHTIG: Nutzt MatchSchedule statt ScoreboardGames!
- MatchSchedule hat bereits Match-level Daten (kein Game-Aggregation nötig)
- Verwendet SPACES in OverviewPage (z.B. "PCS/2024 Season/Spring Season")
- Importiert nur Minor Regions: CBLOL, PCS, LMS, VCS, LJL, TCL, LLA, LLN, OPL
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
from core.team_resolver import TeamResolver

def import_tournament(loader, db, team_resolver, name, url, stats, include_players=True):
    """
    Import all matches for a single tournament from MatchSchedule table

    Args:
        loader: LeaguepediaLoader instance
        db: DatabaseManager instance
        team_resolver: TeamResolver instance
        name: Tournament name
        url: Tournament URL (WITH SPACES!)
        stats: Statistics dictionary
        include_players: Whether to import player data (default True)

    Returns:
        bool: True if successful
    """
    print(f"\n{'='*80}")
    print(f"Importing: {name}")
    print(f"URL: {url}")
    print(f"{'='*80}")

    try:
        # Query matches from MatchSchedule (uses SPACES in OverviewPage)
        matches = loader._query_cargo(
            tables="MatchSchedule",
            fields="Team1,Team2,Team1Score,Team2Score,Winner,DateTime_UTC,BestOf,Phase,Round,Tab,OverviewPage,Patch,MatchId,UniqueMatch",
            where=f"OverviewPage='{url}'",
            limit=500,
            order_by="DateTime_UTC ASC"
        )

        if not matches:
            print(f"⚠️  No matches found for {name}")
            stats['tournaments_no_data'] += 1
            return False

        print(f"📥 Found {len(matches)} matches")
        stats['total_matches_found'] += len(matches)

        # Player data lookup - convert URL to underscores for ScoreboardPlayers
        players_by_match = {}
        if include_players:
            # ScoreboardPlayers uses UNDERSCORES in OverviewPage
            url_underscores = url.replace(' ', '_')

            try:
                players = loader._query_cargo(
                    tables="ScoreboardPlayers",
                    fields="UniqueMatch,Link,Role,Team",
                    where=f"OverviewPage='{url_underscores}'",
                    limit=500,
                    order_by="DateTime_UTC ASC"
                )

                # Group by UniqueMatch
                for player in players:
                    unique_match = player.get('UniqueMatch', '')
                    if unique_match:
                        if unique_match not in players_by_match:
                            players_by_match[unique_match] = []
                        players_by_match[unique_match].append(player)

                if players:
                    print(f"👥 Found {len(players)} player records")

            except Exception as e:
                print(f"⚠️  Could not fetch player data: {e}")

        # Insert matches
        matches_inserted = 0
        matches_failed = 0
        players_inserted = 0

        for match in matches:
            team1_orig = match.get('Team1', '').strip()
            team2_orig = match.get('Team2', '').strip()

            if not team1_orig or not team2_orig:
                stats['matches_skipped'] += 1
                continue

            # Resolve team names
            match_date = match.get('DateTime_UTC', '')
            team1_resolved = team_resolver.resolve(team1_orig, match_date)
            team2_resolved = team_resolver.resolve(team2_orig, match_date)

            # Parse date
            try:
                if match_date:
                    date_obj = datetime.strptime(match_date, "%Y-%m-%d %H:%M:%S")
                else:
                    date_obj = None
            except:
                date_obj = None

            # Determine Bo format
            best_of = match.get('BestOf', '')
            bo_format = f"Bo{best_of}" if best_of else None

            # Create external ID
            unique_match = match.get('UniqueMatch', '')
            match_id_field = match.get('MatchId', '')
            tab = match.get('Tab', '')
            external_id = unique_match or match_id_field or f"{url}_{tab}_{match_date}_{team1_orig}_{team2_orig}"

            # Insert match
            match_id = db.insert_match(
                team1_name=team1_resolved,
                team2_name=team2_resolved,
                team1_score=int(match.get('Team1Score', 0) or 0),
                team2_score=int(match.get('Team2Score', 0) or 0),
                date=date_obj,
                tournament_name=name,
                stage=match.get('Tab', '') or match.get('Phase', '') or match.get('Round', ''),
                patch=match.get('Patch', ''),
                bo_format=bo_format,
                external_id=external_id,
                source='leaguepedia'
            )

            if match_id:
                matches_inserted += 1
                stats['matches_inserted'] += 1

                # Insert players for this match
                if include_players and unique_match in players_by_match:
                    match_players = players_by_match[unique_match]

                    # Deduplicate by (player_name, role)
                    unique_players = {}
                    for player in match_players:
                        player_name = player.get('Link', '').strip()
                        role = player.get('Role', '').strip()
                        team_orig = player.get('Team', '').strip()

                        if not player_name:
                            continue

                        # Resolve player's team
                        team_resolved = team_resolver.resolve(team_orig, match_date)

                        key = (player_name, role)
                        if key not in unique_players:
                            unique_players[key] = (player_name, role, team_resolved)

                    # Insert unique players
                    for player_name, role, team_name in unique_players.values():
                        db.insert_match_player(
                            match_id=match_id,
                            player_name=player_name,
                            team_name=team_name,
                            role=role
                        )
                        players_inserted += 1
                        stats['players_inserted'] += 1
            else:
                matches_failed += 1
                stats['matches_failed'] += 1

        print(f"✅ Inserted: {matches_inserted} matches, {players_inserted} players")
        if matches_failed > 0:
            print(f"⚠️  Failed: {matches_failed} matches")

        stats['tournaments_imported'] += 1
        return True

    except Exception as e:
        print(f"❌ ERROR importing {name}: {e}")
        import traceback
        traceback.print_exc()
        stats['tournaments_failed'] += 1
        return False

def main():
    """Main import function"""

    # Check for results file
    results_file = Path(__file__).parent / "minor_regions_discovery_results.json"
    if not results_file.exists():
        print(f"❌ Discovery results file not found: {results_file}")
        print(f"   Please run minor_regions_tournament_discovery_matchschedule.py first!")
        return 1

    # Load discovery results
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    tournaments = results.get('found_tournaments', [])
    if not tournaments:
        print("❌ No tournaments found in results file!")
        return 1

    print(f"📋 Loaded {len(tournaments)} tournaments from discovery results")

    # Initialize components
    bot_username = os.getenv("LEAGUEPEDIA_BOT_USERNAME", "Ekwo98@Elo")
    bot_password = os.getenv("LEAGUEPEDIA_BOT_PASSWORD")

    if not bot_password:
        print("❌ LEAGUEPEDIA_BOT_PASSWORD environment variable not set!")
        return 1

    print("\n🔧 Initializing components...")
    loader = LeaguepediaLoader(bot_username=bot_username, bot_password=bot_password)
    db = DatabaseManager()
    team_resolver = TeamResolver()

    # Statistics
    stats = {
        'tournaments_total': len(tournaments),
        'tournaments_imported': 0,
        'tournaments_failed': 0,
        'tournaments_no_data': 0,
        'total_matches_found': 0,
        'matches_inserted': 0,
        'matches_failed': 0,
        'matches_skipped': 0,
        'players_inserted': 0
    }

    # Import each tournament
    print(f"\n{'='*80}")
    print(f"STARTING IMPORT OF {len(tournaments)} TOURNAMENTS")
    print(f"{'='*80}")

    start_time = time.time()

    for i, tournament in enumerate(tournaments, 1):
        name = tournament['name']
        url = tournament['url']

        print(f"\n[{i}/{len(tournaments)}] {name}")

        import_tournament(
            loader=loader,
            db=db,
            team_resolver=team_resolver,
            name=name,
            url=url,
            stats=stats,
            include_players=True
        )

        # Progress update every 10 tournaments
        if i % 10 == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = (len(tournaments) - i) * avg_time
            print(f"\n⏱️  Progress: {i}/{len(tournaments)} tournaments")
            print(f"   Elapsed: {elapsed/60:.1f}m, Estimated remaining: {remaining/60:.1f}m")

    # Final statistics
    elapsed_total = time.time() - start_time

    print(f"\n{'='*80}")
    print(f"IMPORT COMPLETE")
    print(f"{'='*80}")
    print(f"Time elapsed: {elapsed_total/60:.1f} minutes")
    print(f"\nTournaments:")
    print(f"  Total:       {stats['tournaments_total']}")
    print(f"  Imported:    {stats['tournaments_imported']}")
    print(f"  Failed:      {stats['tournaments_failed']}")
    print(f"  No data:     {stats['tournaments_no_data']}")
    print(f"\nMatches:")
    print(f"  Found:       {stats['total_matches_found']}")
    print(f"  Inserted:    {stats['matches_inserted']}")
    print(f"  Failed:      {stats['matches_failed']}")
    print(f"  Skipped:     {stats['matches_skipped']}")
    print(f"\nPlayers:")
    print(f"  Inserted:    {stats['players_inserted']}")

    # Save import log
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'duration_seconds': elapsed_total,
        'statistics': stats
    }

    log_file = Path(__file__).parent / "import_log.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)

    print(f"\n📄 Import log saved to: {log_file}")

    return 0

if __name__ == "__main__":
    exit(main())
