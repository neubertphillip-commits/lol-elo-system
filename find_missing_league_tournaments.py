#!/usr/bin/env python3
"""
Comprehensive search for remaining missing league tournaments
Testing ALL possible URL patterns for historical tournaments
"""

import os
import sys
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader

def test_url_variant(loader, url):
    """Test a single URL variant"""
    try:
        print(f"    Testing: {url}")

        games = loader._query_cargo(
            tables="ScoreboardGames",
            fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage",
            where=f"OverviewPage='{url}'",
            limit=3
        )

        if games and len(games) > 0:
            print(f"    ✅ FOUND! {len(games)} games")
            for i, game in enumerate(games, 1):
                team1 = game.get('Team1', 'N/A')
                team2 = game.get('Team2', 'N/A')
                date = game.get('DateTime UTC', 'N/A')
                print(f"       Game {i}: {team1} vs {team2} ({date})")
            return True, games
        else:
            print(f"    ⚠️  No data")
            return False, None

    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg or "Service Unavailable" in error_msg:
            print(f"    ⚠️  503 error")
        elif "Rate" in error_msg or "limited" in error_msg:
            print(f"    ⚠️  Rate limited")
        else:
            print(f"    ❌ Error: {error_msg[:100]}")
        return False, None

def search_tournaments(loader):
    """Search for all missing tournaments"""
    results = {}

    searches = [
        # LCK/Champions Historical
        {
            "name": "LCK 2015 Spring",
            "variants": [
                "LCK/2015 Season/Spring Season",
                "LCK/2015 Season/Spring",
                "LCK 2015 Spring",
                "Champions Spring 2015",
                "HOT6iX Champions Spring 2015",
                "SBENU Champions Spring 2015",
                "2015 LCK Spring",
            ]
        },
        {
            "name": "Champions 2014 Summer",
            "variants": [
                "Champions Summer 2014",
                "OGN Champions Summer 2014",
                "HOT6iX Champions Summer 2014",
                "Champions/2014/Summer",
                "LCK/Champions/2014 Summer",
                "2014 Champions Summer",
                "Korea/2014 Season/Summer",
            ]
        },
        {
            "name": "Champions 2014 Spring",
            "variants": [
                "Champions Spring 2014",
                "OGN Champions Spring 2014",
                "HOT6iX Champions Spring 2014",
                "Champions/2014/Spring",
                "2014 Champions Spring",
            ]
        },
        {
            "name": "Champions 2014 Winter",
            "variants": [
                "Champions Winter 2013-2014",
                "Champions Winter 2014",
                "OGN Champions Winter 2013-2014",
                "Champions/Winter 2014",
                "2014 Champions Winter",
            ]
        },
        {
            "name": "Champions 2013 Summer",
            "variants": [
                "Champions Summer 2013",
                "OGN Champions Summer 2013",
                "HOT6iX Champions Summer 2013",
                "Champions/2013/Summer",
                "2013 Champions Summer",
                "Korea/Season 3/Summer",
            ]
        },
        {
            "name": "Champions 2013 Spring",
            "variants": [
                "Champions Spring 2013",
                "OGN Champions Spring 2013",
                "Champions/2013/Spring",
                "2013 Champions Spring",
                "Korea/Season 3/Spring",
            ]
        },
        {
            "name": "Champions 2013 Winter",
            "variants": [
                "Champions Winter 2012-2013",
                "Champions Winter 2013",
                "OGN Champions Winter 2012-2013",
                "Champions/Winter 2013",
            ]
        },
        # LPL Historical (earlier years)
        {
            "name": "LPL 2017 Spring",
            "variants": [
                "LPL/2017 Season/Spring Season",
                "LPL/2017 Season/Spring",
                "LPL 2017 Spring",
                "LPL Spring 2017",
            ]
        },
        {
            "name": "LPL 2016 Spring",
            "variants": [
                "LPL/2016 Season/Spring Season",
                "LPL/2016 Season/Spring",
                "LPL 2016 Spring",
                "LPL Spring 2016",
            ]
        },
        {
            "name": "LPL 2015 Spring",
            "variants": [
                "LPL/2015 Season/Spring Season",
                "LPL/2015 Season/Spring",
                "LPL 2015 Spring",
                "LPL Spring 2015",
            ]
        },
        {
            "name": "LPL 2014 Spring",
            "variants": [
                "LPL/2014 Season/Spring Season",
                "LPL/2014 Season/Spring",
                "LPL 2014 Spring",
                "LPL Spring 2014",
            ]
        },
        {
            "name": "LPL 2013 Spring",
            "variants": [
                "LPL/2013 Season/Spring Season",
                "LPL/Season 3/Spring Season",
                "LPL 2013 Spring",
                "LPL Spring 2013",
            ]
        },
        # Kleinere Regionen - 2020 (von initial test)
        {
            "name": "PCS 2020 Spring",
            "variants": [
                "PCS/2020 Season/Spring Season",
                "PCS/2020 Season/Spring",
                "PCS 2020 Spring",
                "PCS Spring 2020",
            ]
        },
        {
            "name": "VCS 2020 Spring",
            "variants": [
                "VCS/2020 Season/Spring Season",
                "VCS/2020 Season/Spring",
                "VCS 2020 Spring",
                "VCS Spring 2020",
            ]
        },
        {
            "name": "LJL 2020 Spring",
            "variants": [
                "LJL/2020 Season/Spring Season",
                "LJL/2020 Season/Spring",
                "LJL 2020 Spring",
                "LJL Spring 2020",
            ]
        },
        {
            "name": "TCL 2020 Winter",
            "variants": [
                "TCL/2020 Season/Winter Season",
                "TCL/2020 Season/Winter",
                "TCL 2020 Winter",
                "TCL Winter 2020",
            ]
        },
        {
            "name": "LLA 2020 Opening",
            "variants": [
                "LLA/2020 Season/Opening Season",
                "LLA/2020 Season/Opening",
                "LLA 2020 Opening",
                "LLA Opening 2020",
            ]
        },
        # Regional Cups
        {
            "name": "Kespa Cup 2024",
            "variants": [
                "LoL KeSPA Cup/2024",
                "KeSPA Cup/2024",
                "KeSPA Cup 2024",
                "2024 KeSPA Cup",
                "Kespa Cup/2024",
                "LoL KeSPA Cup 2024",
            ]
        },
        {
            "name": "Kespa Cup 2021",
            "variants": [
                "LoL KeSPA Cup/2021",
                "KeSPA Cup/2021",
                "KeSPA Cup 2021",
                "2021 KeSPA Cup",
            ]
        },
        {
            "name": "Kespa Cup 2019",
            "variants": [
                "LoL KeSPA Cup/2019",
                "KeSPA Cup/2019",
                "KeSPA Cup 2019",
                "2019 KeSPA Cup",
            ]
        },
        {
            "name": "Demacia Cup 2024 Winter",
            "variants": [
                "Demacia Cup/2024/Winter",
                "Demacia Cup 2024 Winter",
                "2024 Demacia Cup Winter",
                "Demacia Cup/Winter 2024",
            ]
        },
        {
            "name": "Demacia Cup 2020 Winter",
            "variants": [
                "Demacia Cup/2020/Winter",
                "Demacia Cup 2020 Winter",
                "2020 Demacia Cup Winter",
                "Demacia Cup/Winter 2020",
            ]
        },
        # Worlds Group Stages (maybe under different names)
        {
            "name": "Worlds 2017 Groups",
            "variants": [
                "2017 Season World Championship/Main Event/Group Stage",
                "2017 Season World Championship/Main Event",  # Already found, but retest
            ]
        },
        {
            "name": "Worlds 2016 Groups",
            "variants": [
                "2016 Season World Championship/Group Stage",
                "2016 Season World Championship",  # Already found
            ]
        },
        {
            "name": "Worlds 2015 Groups",
            "variants": [
                "2015 Season World Championship/Group Stage",
                "2015 Season World Championship",  # Already found
            ]
        },
        # Try Worlds 2024 one more time with different patterns
        {
            "name": "Worlds 2024 Main Event",
            "variants": [
                "2024 Season World Championship/Main Event",
                "2024 Season World Championship",  # Without any stage
            ]
        },
        {
            "name": "Worlds 2023 Quarterfinals",
            "variants": [
                "2023 Season World Championship/Quarterfinals",
                "2023 Season World Championship/Quarter Finals",
                "2023 Season World Championship/Main Event/Quarterfinals",
            ]
        },
    ]

    for search in searches:
        print("\n" + "="*80)
        print(f"SEARCHING: {search['name']}")
        print("="*80)

        found = False
        for i, variant in enumerate(search['variants'], 1):
            print(f"\n[{i}/{len(search['variants'])}]")
            success, games = test_url_variant(loader, variant)

            if success:
                results[search['name']] = {
                    "url": variant,
                    "games": games,
                    "count": len(games)
                }
                print(f"\n✅✅✅ SUCCESS! Found {search['name']}")
                print(f"    Working URL: {variant}")
                found = True
                break

            time.sleep(4)  # Longer delay to avoid rate limiting

        if not found:
            print(f"\n❌ NOT FOUND: {search['name']} after testing {len(search['variants'])} variants")
            results[search['name']] = None

        time.sleep(2)

    return results

def main():
    print("="*80)
    print("MISSING LEAGUE TOURNAMENTS COMPREHENSIVE SEARCH")
    print("="*80)

    # Setup loader with bot auth
    os.environ['LEAGUEPEDIA_BOT_USERNAME'] = 'ekwo98@Elo'
    os.environ['LEAGUEPEDIA_BOT_PASSWORD'] = 'n7d9rsiccg7hujkg2hvtnglg4h93480r'

    loader = LeaguepediaLoader()

    if hasattr(loader, 'session') and hasattr(loader.session, 'auth'):
        print(f"[OK] Authenticated as {os.environ.get('LEAGUEPEDIA_BOT_USERNAME')}")
        print("✅ Bot authenticated successfully\n")

    # Search all missing tournaments
    results = search_tournaments(loader)

    # Print summary
    print("\n" + "="*80)
    print("SEARCH RESULTS SUMMARY")
    print("="*80)

    found_count = sum(1 for v in results.values() if v is not None)
    total_count = len(results)

    print(f"\nFound: {found_count}/{total_count}")
    print(f"Not Found: {total_count - found_count}/{total_count}")

    # Print all found URLs
    print("\n" + "="*80)
    print("FOUND TOURNAMENTS")
    print("="*80)

    for name, data in results.items():
        if data:
            print(f"\n✅ {name}")
            print(f"   URL: {data['url']}")
            print(f"   Games found: {data['count']}")

    # Print not found
    print("\n" + "="*80)
    print("NOT FOUND")
    print("="*80)

    for name, data in results.items():
        if not data:
            print(f"❌ {name}")

    # Save results
    output_file = "missing_leagues_search_results.json"
    serializable_results = {}
    for name, data in results.items():
        if data:
            serializable_results[name] = {
                "url": data["url"],
                "count": data["count"],
                "sample_games": [
                    {
                        "team1": g.get("Team1"),
                        "team2": g.get("Team2"),
                        "date": g.get("DateTime UTC")
                    }
                    for g in data["games"][:3]
                ]
            }
        else:
            serializable_results[name] = None

    with open(output_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)

    print(f"\n📄 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
