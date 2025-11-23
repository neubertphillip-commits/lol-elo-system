"""
Test alternative approaches to get old tournament player data
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader


def test_alternative_tables():
    """Test various tables that might have old player data"""

    loader = LeaguepediaLoader(
        bot_username="Ekwo98@Elo",
        bot_password="5i8ntnp2aki8culomjov3kajm0ude52p"
    )

    tournament = "EU LCS 2015 Spring"

    print(f"{'='*80}")
    print(f"Testing alternative data sources for: {tournament}")
    print(f"{'='*80}\n")

    # Test 1: TournamentRosters table
    print("[1] TournamentRosters table:")
    try:
        rosters = loader._query_cargo(
            tables='TournamentRosters',
            fields='Team, Player, Role',
            where=f'OverviewPage="{tournament}"',
            limit=100
        )
        print(f"  ✓ Found {len(rosters)} roster entries")
        if rosters:
            print(f"  Sample: {rosters[0]}")
            for i, roster in enumerate(rosters[:5]):
                print(f"    {i+1}. {roster}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 2: PlayerRedirects (player names mapping)
    print("\n[2] PlayerRedirects table:")
    try:
        players = loader._query_cargo(
            tables='PlayerRedirects',
            fields='OverviewPage, AllName',
            where=f'OverviewPage LIKE "xPeke%"',
            limit=5
        )
        print(f"  ✓ Found {len(players)} entries")
        if players:
            for p in players:
                print(f"    {p}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: TournamentResults table
    print("\n[3] TournamentResults table:")
    try:
        results = loader._query_cargo(
            tables='TournamentResults',
            fields='Team, Place, OverviewPage',
            where=f'OverviewPage="{tournament}"',
            limit=20
        )
        print(f"  ✓ Found {len(results)} team results")
        if results:
            for r in results[:5]:
                print(f"    {r}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: Leagues table (to understand structure)
    print("\n[4] Available Cargo tables:")
    try:
        # Query to get all cargo tables
        response = loader.session.get(
            loader.API_ENDPOINT,
            params={
                'action': 'cargoquery',
                'format': 'json',
                'tables': '_pageData',
                'fields': '_pageName',
                'where': '_pageNamespace=0',
                'limit': 5
            }
        )
        data = response.json()
        print(f"  Sample pages: {data}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 5: Check what fields are available in MatchSchedule for old tournaments
    print("\n[5] MatchSchedule fields for old tournament:")
    try:
        matches = loader._query_cargo(
            tables='MatchSchedule',
            fields='Team1, Team2, Winner, DateTime UTC, BestOf, Team1Score, Team2Score',
            where=f'OverviewPage="{tournament}"',
            limit=5
        )
        print(f"  ✓ Found {len(matches)} matches")
        if matches:
            print(f"  Sample: {matches[0]}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 6: Check TournamentPlayers table
    print("\n[6] TournamentPlayers table:")
    try:
        players = loader._query_cargo(
            tables='TournamentPlayers',
            fields='Player, Team, Role, OverviewPage',
            where=f'OverviewPage="{tournament}"',
            limit=50
        )
        print(f"  ✓ Found {len(players)} player entries")
        if players:
            print(f"  Sample entries:")
            for i, p in enumerate(players[:10]):
                print(f"    {i+1}. {p}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    test_alternative_tables()
