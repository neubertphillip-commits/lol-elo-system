"""
Test when ScoreboardGames data becomes available
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader


def test_year_range():
    """Test data availability across different years"""

    loader = LeaguepediaLoader(
        bot_username="Ekwo98@Elo",
        bot_password="5i8ntnp2aki8culomjov3kajm0ude52p"
    )

    # Test EU LCS/LEC from 2013 to 2024
    test_tournaments = [
        ("EU LCS 2013 Spring", 2013),
        ("EU LCS 2014 Spring", 2014),
        ("EU LCS 2015 Spring", 2015),
        ("EU LCS 2016 Spring", 2016),
        ("EU LCS 2017 Spring", 2017),
        ("EU LCS 2018 Spring", 2018),
        ("LEC/2019 Season/Spring Season", 2019),
        ("LEC/2020 Season/Spring Season", 2020),
    ]

    print("="*80)
    print("Testing ScoreboardGames data availability by year")
    print("="*80)
    print(f"\n{'Year':<8} {'Tournament':<40} {'Games':<10} {'Matches':<10}")
    print("-"*80)

    for tournament, year in test_tournaments:
        # Check ScoreboardGames
        try:
            games = loader._query_cargo(
                tables='ScoreboardGames',
                fields='GameId',
                where=f'OverviewPage="{tournament}"',
                limit=500
            )
            game_count = len(games)
        except:
            game_count = 0

        # Check MatchSchedule
        try:
            matches = loader._query_cargo(
                tables='MatchSchedule',
                fields='Team1',
                where=f'OverviewPage="{tournament}"',
                limit=500
            )
            match_count = len(matches)
        except:
            match_count = 0

        status = "✓" if game_count > 0 or match_count > 0 else "✗"
        print(f"{year:<8} {tournament:<40} {game_count:<10} {match_count:<10} {status}")


if __name__ == "__main__":
    test_year_range()
