"""
Test Leaguepedia API to find correct tournament names and query format
"""

import requests
import json
from urllib.parse import urlencode

API_ENDPOINT = "https://lol.fandom.com/api.php"

def test_query(tournament_name):
    """Test query for a specific tournament"""

    params = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'ScoreboardGames',
        'fields': 'GameId, Team1, Team2, DateTime_UTC, OverviewPage, Tab',
        'where': f"ScoreboardGames.OverviewPage='{tournament_name}'",
        'limit': 5
    }

    print(f"\n{'='*70}")
    print(f"Testing: {tournament_name}")
    print(f"{'='*70}")
    print(f"URL: {API_ENDPOINT}?{urlencode(params)}")

    response = requests.get(API_ENDPOINT, params=params, headers={
        'User-Agent': 'LOL-ELO-System/1.0 (Educational Research)'
    })

    data = response.json()

    if 'error' in data:
        print(f"[ERROR] {data['error']}")
        return

    if 'cargoquery' in data:
        results = data['cargoquery']
        print(f"[OK] Found {len(results)} games")

        if results:
            print("\nFirst result:")
            print(json.dumps(results[0]['title'], indent=2))
    else:
        print(f"[WARN] No cargoquery in response")
        print(f"Response keys: {data.keys()}")


def find_tournament_variations():
    """Try to find the correct tournament name by testing variations"""

    # Test different possible formats
    test_names = [
        "LEC/2024 Season/Summer Season",
        "LEC/2024_Season/Summer_Season",
        "LEC/2024 Season/Summer",
        "LEC 2024 Summer",
        "League of Legends EMEA Championship/2024 Season/Summer Season",
    ]

    for name in test_names:
        test_query(name)


def search_tournaments_by_year():
    """Search for all tournaments in 2024"""

    params = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'Tournaments',
        'fields': 'OverviewPage, Name, DateStart, Region, League',
        'where': 'Tournaments.DateStart >= "2024-01-01" AND Tournaments.DateStart < "2025-01-01"',
        'order_by': 'Tournaments.DateStart',
        'limit': 50
    }

    print(f"\n{'='*70}")
    print(f"Searching all 2024 tournaments...")
    print(f"{'='*70}")

    response = requests.get(API_ENDPOINT, params=params, headers={
        'User-Agent': 'LOL-ELO-System/1.0 (Educational Research)'
    })

    data = response.json()

    if 'cargoquery' in data:
        results = data['cargoquery']
        print(f"[OK] Found {len(results)} tournaments")

        # Filter for major leagues
        major_leagues = ['LEC', 'LCK', 'LCS', 'LPL', 'MSI', 'Worlds', 'World Championship']

        print("\nMajor tournaments found:")
        for item in results:
            t = item['title']
            league = t.get('League', t.get('Name', ''))
            if any(major in league for major in major_leagues):
                print(f"\nOverviewPage: {t.get('OverviewPage')}")
                print(f"  Name: {t.get('Name')}")
                print(f"  League: {t.get('League')}")
                print(f"  Region: {t.get('Region')}")
                print(f"  DateStart: {t.get('DateStart')}")


if __name__ == "__main__":
    print("Leaguepedia API Tournament Name Tester")
    print("="*70)

    # First, search for all 2024 tournaments to see actual names
    search_tournaments_by_year()

    # Then test specific variations
    # find_tournament_variations()
