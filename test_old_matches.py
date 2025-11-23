"""
Test if we can get basic match data for old tournaments
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader


def test_old_match_data():
    """Test basic match queries for old tournaments"""

    loader = LeaguepediaLoader(
        bot_username="Ekwo98@Elo",
        bot_password="5i8ntnp2aki8culomjov3kajm0ude52p"
    )

    tournaments = [
        "EU LCS 2015 Spring",
        "EU LCS 2016 Spring",
        "EU LCS 2017 Spring",
    ]

    for tournament in tournaments:
        print(f"\n{'='*80}")
        print(f"Testing: {tournament}")
        print(f"{'='*80}")

        # Try simple MatchSchedule query
        print("\n[1] Simple MatchSchedule query (Team1, Team2, Winner):")
        try:
            matches = loader._query_cargo(
                tables='MatchSchedule',
                fields='Team1, Team2, Winner',
                where=f'OverviewPage="{tournament}"',
                limit=10
            )
            print(f"  ✓ Found {len(matches)} matches")
            if matches:
                for i, m in enumerate(matches[:3]):
                    print(f"    {i+1}. {m}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # Try MatchScheduleGame table (might have game-level data)
        print("\n[2] MatchScheduleGame table:")
        try:
            games = loader._query_cargo(
                tables='MatchScheduleGame',
                fields='Team1, Team2, Winner, GameId',
                where=f'OverviewPage="{tournament}"',
                limit=10
            )
            print(f"  ✓ Found {len(games)} games")
            if games:
                for i, g in enumerate(games[:3]):
                    print(f"    {i+1}. {g}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # Check if there's data in the old PlayerStats table
        print("\n[3] Checking for team roster pages:")
        try:
            # Try to find team pages for this tournament
            # Most teams have roster data on their team pages
            teams = loader._query_cargo(
                tables='MatchSchedule',
                fields='Team1',
                where=f'OverviewPage="{tournament}"',
                limit=1,
                group_by='Team1'
            )
            if teams:
                team_name = teams[0].get('Team1')
                print(f"  Found team: {team_name}")

                # Try to get roster for this team
                print(f"  Checking roster for {team_name}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    test_old_match_data()
