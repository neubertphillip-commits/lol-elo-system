"""
Unit test for RosterManager - tests the logic without API calls
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.roster_manager import RosterManager

def test_roster_manager_logic():
    """Test roster manager logic with mock data"""

    print("="*70)
    print("RosterManager Unit Test (No API Calls)")
    print("="*70)

    # Create a mock roster manager
    # We'll manually populate the roster data to test the logic
    class MockSession:
        def get(self, *args, **kwargs):
            pass

    roster_mgr = RosterManager(
        api_endpoint="mock",
        session=MockSession(),
        rate_limit_delay=0
    )

    # Manually add test roster data
    roster_mgr.team_rosters = {
        'G2 Esports': [
            {'player': 'BrokenBlade', 'role': 'Top', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Yike', 'role': 'Jungle', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Caps', 'role': 'Mid', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Hans sama', 'role': 'Bot', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Mikyx', 'role': 'Support', 'start_date': '2024-01-01', 'end_date': ''},
        ],
        'Fnatic': [
            {'player': 'Oscarinin', 'role': 'Top', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Razork', 'role': 'Jungle', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Humanoid', 'role': 'Mid', 'start_date': '2024-01-01', 'end_date': ''},
            {'player': 'Noah', 'role': 'Bot', 'start_date': '2024-01-01', 'end_date': '2024-06-15'},  # Transfer mid-season
            {'player': 'Jun', 'role': 'Bot', 'start_date': '2024-06-16', 'end_date': ''},  # New player
            {'player': 'Rhuckz', 'role': 'Support', 'start_date': '2024-01-01', 'end_date': ''},
        ]
    }

    # Test 1: Get roster for G2 in Summer 2024
    print("\nTest 1: G2 Esports roster on 2024-07-01")
    print("-" * 70)

    g2_roster = roster_mgr.get_players_for_game(
        team='G2 Esports',
        game_date=datetime(2024, 7, 1)
    )

    expected = {
        'Top': 'BrokenBlade',
        'Jungle': 'Yike',
        'Mid': 'Caps',
        'Bot': 'Hans sama',
        'Support': 'Mikyx'
    }

    success = True
    for role, expected_player in expected.items():
        actual_player = g2_roster.get(role)
        match = "✓" if actual_player == expected_player else "✗"
        print(f"  {role:10s}: {actual_player:15s} (expected: {expected_player:15s}) {match}")
        if actual_player != expected_player:
            success = False

    print(f"\nTest 1: {'PASSED ✓' if success else 'FAILED ✗'}")

    # Test 2: Fnatic roster BEFORE mid-season transfer (Noah playing)
    print("\nTest 2: Fnatic roster on 2024-05-01 (before transfer)")
    print("-" * 70)

    fnc_roster_early = roster_mgr.get_players_for_game(
        team='Fnatic',
        game_date=datetime(2024, 5, 1)
    )

    expected_bot = 'Noah'
    actual_bot = fnc_roster_early.get('Bot')
    match = "✓" if actual_bot == expected_bot else "✗"
    print(f"  Bot:       {actual_bot:15s} (expected: {expected_bot:15s}) {match}")

    test2_success = actual_bot == expected_bot
    print(f"\nTest 2: {'PASSED ✓' if test2_success else 'FAILED ✗'}")

    # Test 3: Fnatic roster AFTER mid-season transfer (Jun playing)
    print("\nTest 3: Fnatic roster on 2024-07-01 (after transfer)")
    print("-" * 70)

    fnc_roster_late = roster_mgr.get_players_for_game(
        team='Fnatic',
        game_date=datetime(2024, 7, 1)
    )

    expected_bot = 'Jun'
    actual_bot = fnc_roster_late.get('Bot')
    match = "✓" if actual_bot == expected_bot else "✗"
    print(f"  Bot:       {actual_bot:15s} (expected: {expected_bot:15s}) {match}")

    test3_success = actual_bot == expected_bot
    print(f"\nTest 3: {'PASSED ✓' if test3_success else 'FAILED ✗'}")

    # Summary
    print("\n" + "="*70)
    all_success = success and test2_success and test3_success
    if all_success:
        print("ALL TESTS PASSED ✓")
        print("\nRosterManager logic is working correctly!")
        print("- Can retrieve player rosters by date")
        print("- Handles mid-season roster changes correctly")
        print("- Ready for use with real API data")
    else:
        print("SOME TESTS FAILED ✗")
        print("Please check the RosterManager implementation")
    print("="*70)

    return all_success

if __name__ == "__main__":
    success = test_roster_manager_logic()
    sys.exit(0 if success else 1)
