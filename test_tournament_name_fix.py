"""
Test if tournament name fix works correctly
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader
from core.database import DatabaseManager
from core.team_resolver import TeamResolver
from major_regions_tournament_import_matchschedule import import_tournament

def main():
    # Initialize
    db = DatabaseManager()
    loader = LeaguepediaLoader(
        bot_username="Ekwo98@Elo",
        bot_password="5i8ntnp2aki8culomjov3kajm0ude52p"
    )
    team_resolver = TeamResolver()

    # Test tournament
    test_name = "LPL 2019 Spring"
    test_url = "LPL/2019 Season/Spring Season"

    print("="*80)
    print("TEST: Tournament Name Fix")
    print("="*80)
    print(f"Display Name: {test_name}")
    print(f"URL Format:   {test_url}")
    print()

    # Clear any existing data for this tournament
    print("Cleaning up any existing data...")
    db.conn.execute("DELETE FROM match_players WHERE match_id IN (SELECT id FROM matches WHERE tournament_id IN (SELECT id FROM tournaments WHERE name = ?))", (test_url,))
    db.conn.execute("DELETE FROM matches WHERE tournament_id IN (SELECT id FROM tournaments WHERE name = ?)", (test_url,))
    db.conn.execute("DELETE FROM tournaments WHERE name = ?", (test_url,))
    db.conn.commit()

    # Import tournament
    print("\nImporting tournament...")
    stats = {
        'tournaments_found': 0,
        'tournaments_no_data': 0,
        'tournaments_failed': 0,
        'total_matches_found': 0,
        'matches_inserted': 0,
        'matches_skipped': 0,
        'matches_with_estimated_dates': 0,
        'matches_with_real_dates': 0
    }

    import_tournament(
        loader=loader,
        db=db,
        team_resolver=team_resolver,
        name=test_name,
        url=test_url,
        stats=stats,
        include_players=False  # Don't import players yet
    )

    # Check what tournament name was saved
    print("\n" + "="*80)
    print("VERIFICATION: Tournament name in database")
    print("="*80)

    tournaments = db.conn.execute(
        "SELECT name FROM tournaments WHERE name LIKE '%LPL%2019%Spring%'"
    ).fetchall()

    if tournaments:
        saved_name = tournaments[0][0]
        print(f"✓ Tournament found in database")
        print(f"  Saved as: '{saved_name}'")
        print()

        # Check if it matches URL format
        if saved_name == test_url:
            print("✅ CORRECT: Name saved in URL format (with slashes)!")
        else:
            print(f"❌ WRONG: Expected '{test_url}' but got '{saved_name}'")
            return False
    else:
        print("❌ ERROR: Tournament not found in database!")
        return False

    # Test if ScoreboardGames can find games with this name
    print("\n" + "="*80)
    print("TEST: ScoreboardGames compatibility")
    print("="*80)

    games = loader._query_cargo(
        tables='ScoreboardGames',
        fields='GameId',
        where=f'OverviewPage="{saved_name}"',
        limit=5
    )

    if games and len(games) > 0:
        print(f"✅ SUCCESS: ScoreboardGames found {len(games)} games!")
        print(f"   Tournament name '{saved_name}' is compatible with player import!")
    else:
        print(f"❌ FAILED: ScoreboardGames found 0 games")
        print(f"   Tournament name '{saved_name}' won't work with player import!")
        return False

    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED - Fix is working correctly!")
    print("="*80)

    # Cleanup
    loader.close()
    db.close()

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
