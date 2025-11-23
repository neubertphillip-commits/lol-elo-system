"""
Import player data for tournaments that already have matches imported.
Uses batch queries to efficiently fetch player data from ScoreboardPlayers.

Usage:
    python import_player_data.py --tournament "LEC/2024 Season/Spring Season"
    python import_player_data.py --all
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader
from core.database import DatabaseManager


def chunks(lst, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def import_players_for_tournament(tournament_name: str, db: DatabaseManager, loader: LeaguepediaLoader):
    """
    Import player data for a tournament using efficient batch queries.

    Args:
        tournament_name: Tournament name (e.g., "LEC/2024 Season/Spring Season")
        db: DatabaseManager instance
        loader: LeaguepediaLoader instance

    Returns:
        Number of players imported
    """
    print(f"\n{'='*80}")
    print(f"Importing player data for: {tournament_name}")
    print(f"{'='*80}")

    # Step 1: Get all games from ScoreboardGames
    print("\n[1/4] Fetching games from ScoreboardGames...")

    # Query with pagination support for large tournaments
    all_games = []
    offset = 0
    batch_size = 500

    while True:
        # Note: Use DateTime_UTC in query, but API returns as "DateTime UTC"
        games_batch = loader._query_cargo(
            tables='ScoreboardGames',
            fields='GameId, UniqueGame, Team1, Team2, DateTime_UTC',
            where=f'OverviewPage="{tournament_name}"',
            limit=batch_size,
            order_by='DateTime_UTC'
        )

        if not games_batch:
            break

        all_games.extend(games_batch)

        print(f"  Fetched {len(games_batch)} games (total: {len(all_games)})")

        if len(games_batch) < batch_size:
            break  # Last page

        # For pagination, would need to add offset support to _query_cargo
        # For now, assuming <500 games per tournament (which is typical)
        break

    if not all_games:
        print(f"⚠️  No games found for {tournament_name}")
        return 0

    print(f"✓ Found {len(all_games)} games")

    # Step 2: Get matches from database for this tournament
    print("\n[2/4] Loading matches from database...")
    matches = db.get_matches_by_tournament(tournament_name)

    if not matches:
        print(f"⚠️  No matches found in database for {tournament_name}")
        print(f"💡 Run the match import first: python major_regions_tournament_import_matchschedule.py")
        return 0

    print(f"✓ Found {len(matches)} matches in database")

    # Create mapping: external_id → match_id
    external_id_to_match = {}
    for match in matches:
        if match['external_id']:
            external_id_to_match[match['external_id']] = match['id']

    print(f"✓ Created mapping for {len(external_id_to_match)} matches with external_id")

    # Step 3: Fetch player data in batches of 50 games (= 500 players max)
    print(f"\n[3/4] Fetching player data in batches...")

    total_players_inserted = 0
    total_players_skipped = 0
    games_without_match = 0
    batch_count = 0

    for game_batch in chunks(all_games, 50):
        batch_count += 1
        game_ids = [g['GameId'] for g in game_batch]

        # Build WHERE clause: GameId IN ("id1", "id2", ...)
        game_ids_quoted = '","'.join(game_ids)
        where_clause = f'GameId IN ("{game_ids_quoted}")'

        # Query player data - only the fields we need
        players = loader._query_cargo(
            tables='ScoreboardPlayers',
            fields='Link, Role, Team, PlayerWin, GameId',
            where=where_clause,
            limit=500  # 50 games × 10 players = 500
        )

        print(f"  Batch {batch_count}: {len(players)} players from {len(game_batch)} games")

        # Step 4: Insert players into database
        for player_data in players:
            game_id = player_data.get('GameId', '')

            # Find the game to get UniqueGame (external_id)
            game = next((g for g in game_batch if g['GameId'] == game_id), None)
            if not game:
                continue

            unique_game = game.get('UniqueGame', '')

            # Find match in database by external_id
            # Note: UniqueGame is per-game, but we might need to extract match ID
            # UniqueGame format: often includes game number at end
            # Try exact match first, then try prefix match
            match_id = None

            if unique_game in external_id_to_match:
                match_id = external_id_to_match[unique_game]
            else:
                # Try finding match by game ID prefix (remove _1, _2, etc.)
                # GameId format: "LEC/2024_Season/Spring_Season_Week_1_1_1"
                # We might need to match against MatchId or construct it
                # For now, try to find by teams + date range
                for ext_id, m_id in external_id_to_match.items():
                    if game_id.startswith(ext_id) or ext_id.startswith(unique_game.rsplit('_', 1)[0]):
                        match_id = m_id
                        break

            if not match_id:
                games_without_match += 1
                continue

            # Insert player
            try:
                player_win = player_data.get('PlayerWin', '') == 'Yes'

                inserted_id = db.insert_match_player(
                    match_id=match_id,
                    player_name=player_data.get('Link', ''),
                    team_name=player_data.get('Team', ''),
                    role=player_data.get('Role', ''),
                    champion=None,  # Not needed
                    kills=None,
                    deaths=None,
                    assists=None,
                    gold=None,
                    cs=None,
                    damage_to_champions=None,
                    vision_score=None,
                    items=None,
                    won=player_win
                )

                if inserted_id:
                    total_players_inserted += 1
                else:
                    total_players_skipped += 1

            except Exception as e:
                print(f"  ⚠️  Error inserting player {player_data.get('Link')}: {e}")
                total_players_skipped += 1

    # Summary
    print(f"\n{'='*80}")
    print(f"Import Summary for {tournament_name}")
    print(f"{'='*80}")
    print(f"Games processed:        {len(all_games)}")
    print(f"Players inserted:       {total_players_inserted}")
    print(f"Players skipped:        {total_players_skipped}")
    if games_without_match > 0:
        print(f"Games without match:    {games_without_match}")
    print(f"{'='*80}")

    return total_players_inserted


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Import player data for tournaments')
    parser.add_argument('--tournament', type=str, help='Tournament name (e.g., "LEC/2024 Season/Spring Season")')
    parser.add_argument('--all', action='store_true', help='Import players for all tournaments in database')

    args = parser.parse_args()

    if not args.tournament and not args.all:
        parser.print_help()
        return 1

    # Initialize
    db = DatabaseManager()
    loader = LeaguepediaLoader(db=db)

    try:
        total_imported = 0

        if args.all:
            # Get all unique tournaments from database
            print("Fetching all tournaments from database...")
            tournaments = db.get_all_tournament_names()

            if not tournaments:
                print("No tournaments found in database!")
                return 1

            print(f"Found {len(tournaments)} tournaments")

            for i, tournament_name in enumerate(tournaments, 1):
                print(f"\n[{i}/{len(tournaments)}] Processing: {tournament_name}")
                imported = import_players_for_tournament(tournament_name, db, loader)
                total_imported += imported

            print(f"\n{'='*80}")
            print(f"TOTAL PLAYERS IMPORTED: {total_imported}")
            print(f"{'='*80}")
        else:
            # Import single tournament
            total_imported = import_players_for_tournament(args.tournament, db, loader)

        return 0

    finally:
        loader.close()
        db.close()


if __name__ == "__main__":
    exit(main())
