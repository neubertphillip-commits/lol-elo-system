"""
Test script to check if old tournament data exists in Leaguepedia
"""
import sys
import os
import requests
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader
from core.database import DatabaseManager


def test_tournament_data(tournament_name: str):
    """Test if tournament data exists in various tables"""

    print(f"\n{'='*80}")
    print(f"Testing: {tournament_name}")
    print('='*80)

    # Initialize loader with bot credentials
    loader = LeaguepediaLoader(
        bot_username="Ekwo98@Elo",
        bot_password="5i8ntnp2aki8culomjov3kajm0ude52p"
    )

    # Test 1: ScoreboardGames table
    print("\n[1] Checking ScoreboardGames table...")
    try:
        games = loader._query_cargo(
            tables='ScoreboardGames',
            fields='GameId, MatchId, Team1, Team2',
            where=f'OverviewPage="{tournament_name}"',
            limit=5
        )
        print(f"  ✓ Found {len(games)} games in ScoreboardGames")
        if games:
            print(f"  Sample: {games[0]}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: MatchSchedule table
    print("\n[2] Checking MatchSchedule table...")
    try:
        matches = loader._query_cargo(
            tables='MatchSchedule',
            fields='Team1, Team2, BestOf, Winner',
            where=f'OverviewPage="{tournament_name}"',
            limit=5
        )
        print(f"  ✓ Found {len(matches)} matches in MatchSchedule")
        if matches:
            print(f"  Sample: {matches[0]}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Check if tournament exists in Tournaments table
    print("\n[3] Checking Tournaments table...")
    try:
        tournaments = loader._query_cargo(
            tables='Tournaments',
            fields='Name, DateStart, Region, League',
            where=f'Name="{tournament_name}"',
            limit=1
        )
        print(f"  ✓ Found {len(tournaments)} tournament entries")
        if tournaments:
            print(f"  Data: {tournaments[0]}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: Try fuzzy search for similar tournament names
    print("\n[4] Searching for similar tournament names...")
    try:
        # Extract key parts (e.g., "EU LCS" and "2013")
        parts = tournament_name.split()
        league = parts[0] + ' ' + parts[1] if len(parts) > 1 else parts[0]

        tournaments = loader._query_cargo(
            tables='Tournaments',
            fields='Name, DateStart, League',
            where=f'League="{league}"',
            limit=10,
            order_by='DateStart'
        )
        print(f"  ✓ Found {len(tournaments)} tournaments for league '{league}'")
        for t in tournaments:
            print(f"    - {t.get('Name', 'N/A')} ({t.get('DateStart', 'N/A')})")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def main():
    # Test a few old tournaments
    old_tournaments = [
        "EU LCS 2013 Spring",
        "EU LCS 2014 Summer",
        "EU LCS 2015 Spring",
    ]

    for tournament in old_tournaments:
        test_tournament_data(tournament)

    print("\n" + "="*80)
    print("Testing complete!")
    print("="*80)


if __name__ == "__main__":
    main()
