"""
Test API queries for player data from Leaguepedia
"""
import requests
import json
from urllib.parse import urlencode

def test_player_query():
    """Test various player data queries"""

    base_url = "https://lol.fandom.com/api.php"

    # Test 1: Query ScoreboardPlayers for a specific tournament
    print("="*80)
    print("TEST 1: ScoreboardPlayers for LCS 2024 Spring")
    print("="*80)

    params = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'ScoreboardPlayers',
        'where': 'OverviewPage="LCS/2024 Season/Spring Season"',
        'limit': '5',  # Just get first 5 to see structure
        'fields': '_pageName,Name,Link,Team,Role,Champion,Kills,Deaths,Assists,Gold,CS,UniqueMatch,GameId,MatchId'
    }

    query_string = urlencode(params)
    url = f"{base_url}?{query_string}"

    print(f"\nQuery URL: {url}\n")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'cargoquery' in data:
            players = [item['title'] for item in data['cargoquery']]
            print(f"Found {len(players)} player records\n")

            if players:
                print("Sample player data:")
                print(json.dumps(players[0], indent=2, ensure_ascii=False))
            else:
                print("No player records found")
        else:
            print("No cargoquery in response")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Query all fields from ScoreboardPlayers to see what's available
    print("\n" + "="*80)
    print("TEST 2: All available fields in ScoreboardPlayers")
    print("="*80)

    params2 = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'ScoreboardPlayers',
        'where': 'OverviewPage="LCS/2024 Season/Spring Season"',
        'limit': '1',
        'fields': '_pageName,Name,Link,Team,Role,Champion,Kills,Deaths,Assists,Gold,CS,DamageToChampions,UniqueMatch,GameId,MatchId,OverviewPage,DateTime_UTC,Side,PlayerWin,SummonerSpells,Items,Trinket,KeystoneMastery,KeystoneRune,PrimaryTree,SecondaryTree'
    }

    query_string2 = urlencode(params2)
    url2 = f"{base_url}?{query_string2}"

    print(f"\nQuery URL: {url2}\n")

    try:
        response = requests.get(url2, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'cargoquery' in data and data['cargoquery']:
            player = data['cargoquery'][0]['title']
            print("All fields from one player record:")
            print(json.dumps(player, indent=2, ensure_ascii=False))
        else:
            print("No data found")
    except Exception as e:
        print(f"Error: {e}")

    # Test 3: Query ScoreboardGames to see if there's player data there
    print("\n" + "="*80)
    print("TEST 3: ScoreboardGames for comparison")
    print("="*80)

    params3 = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'ScoreboardGames',
        'where': 'OverviewPage="LCS/2024 Season/Spring Season"',
        'limit': '2',
        'fields': '_pageName,Team1,Team2,Winner,Team1Score,Team2Score,DateTime_UTC,UniqueGame,MatchId,OverviewPage,Patch,Team1Players,Team2Players,Team1Bans,Team2Bans'
    }

    query_string3 = urlencode(params3)
    url3 = f"{base_url}?{query_string3}"

    print(f"\nQuery URL: {url3}\n")

    try:
        response = requests.get(url3, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'cargoquery' in data and data['cargoquery']:
            games = [item['title'] for item in data['cargoquery']]
            print(f"Found {len(games)} game records\n")
            print("Sample game data:")
            print(json.dumps(games[0], indent=2, ensure_ascii=False))
        else:
            print("No data found")
    except Exception as e:
        print(f"Error: {e}")

    # Test 4: Query Players table for player info
    print("\n" + "="*80)
    print("TEST 4: Players table (player profiles)")
    print("="*80)

    params4 = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'Players',
        'where': 'Team="Cloud9"',
        'limit': '5',
        'fields': '_pageName,Player,Name,NameFull,Country,Age,Team,Role,IsRetired,IsSubstitute,ResidencyFormer,ResidencyCurrent'
    }

    query_string4 = urlencode(params4)
    url4 = f"{base_url}?{query_string4}"

    print(f"\nQuery URL: {url4}\n")

    try:
        response = requests.get(url4, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'cargoquery' in data and data['cargoquery']:
            players = [item['title'] for item in data['cargoquery']]
            print(f"Found {len(players)} player profiles\n")
            print("Sample player profile:")
            print(json.dumps(players[0], indent=2, ensure_ascii=False))
        else:
            print("No data found")
    except Exception as e:
        print(f"Error: {e}")

    # Test 5: Check with older tournament (2020)
    print("\n" + "="*80)
    print("TEST 5: ScoreboardPlayers for older tournament (LCS 2020 Spring)")
    print("="*80)

    params5 = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'ScoreboardPlayers',
        'where': 'OverviewPage="LCS/2020 Season/Spring Season"',
        'limit': '3',
        'fields': '_pageName,Name,Link,Team,Role,Champion,Kills,Deaths,Assists,Gold,CS,UniqueMatch,GameId,MatchId'
    }

    query_string5 = urlencode(params5)
    url5 = f"{base_url}?{query_string5}"

    print(f"\nQuery URL: {url5}\n")

    try:
        response = requests.get(url5, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'cargoquery' in data:
            players = [item['title'] for item in data['cargoquery']]
            print(f"Found {len(players)} player records\n")

            if players:
                print("Sample player data from 2020:")
                print(json.dumps(players[0], indent=2, ensure_ascii=False))
            else:
                print("No player records found")
        else:
            print("No cargoquery in response")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_player_query()
