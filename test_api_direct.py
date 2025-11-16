"""
Direct API test to diagnose the issue - Tests both space and underscore variants
"""

from core.leaguepedia_loader import LeaguepediaLoader
import time

def test_different_formats():
    """Test queries with different tournament name formats"""

    loader = LeaguepediaLoader()

    # Test both space and underscore variants
    test_cases = [
        # Spaces (MediaWiki standard display)
        ("LEC/2024 Season/Summer Season", "LEC 2024 Summer (spaces)"),
        # Underscores (URL format)
        ("LEC/2024_Season/Summer_Season", "LEC 2024 Summer (underscores)"),

        # Try older year to confirm format
        ("LEC/2023 Season/Summer Season", "LEC 2023 Summer (spaces)"),
        ("LEC/2023_Season/Summer_Season", "LEC 2023 Summer (underscores)"),

        # International events
        ("Mid-Season Invitational/2024 Season/Main Event", "MSI 2024 (spaces)"),
        ("Mid-Season_Invitational/2024_Season/Main_Event", "MSI 2024 (underscores)"),
    ]

    for tournament_name, description in test_cases:
        print(f"\n{'='*70}")
        print(f"Testing: {description}")
        print(f"Tournament: {tournament_name}")
        print(f"{'='*70}")

        # Use debug mode
        games = loader._query_cargo(
            tables="ScoreboardGames",
            fields="GameId, Team1, Team2, DateTime_UTC, OverviewPage",
            where=f"ScoreboardGames.OverviewPage='{tournament_name}'",
            limit=3,
            debug=True  # Enable debug output
        )

        print(f"Result: {len(games)} games found")

        if games:
            print(f"First game: {games[0].get('GameId')} - {games[0].get('Team1')} vs {games[0].get('Team2')}")
            print(f"OverviewPage in DB: '{games[0].get('OverviewPage')}'")

        time.sleep(3)  # Rate limiting

    loader.close()

if __name__ == "__main__":
    test_different_formats()
