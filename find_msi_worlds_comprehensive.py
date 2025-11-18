#!/usr/bin/env python3
"""
Comprehensive MSI and Worlds Tournament URL Discovery
Testing ALL possible URL patterns for missing stages
"""

import os
import sys
import time
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader

def test_url_variant(loader, tournament_name, url, description=""):
    """Test a single URL variant"""
    try:
        print(f"    Testing: {url}")
        if description:
            print(f"    ({description})")

        games = loader._query_cargo(
            tables="ScoreboardGames",
            fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage",
            where=f"OverviewPage='{url}'",
            limit=5  # Get 5 games to see stage variety
        )

        if games and len(games) > 0:
            print(f"    ✅ FOUND! {len(games)} games")
            for i, game in enumerate(games, 1):
                team1 = game.get('Team1', 'N/A')
                team2 = game.get('Team2', 'N/A')
                date = game.get('DateTime UTC', 'N/A')
                overview = game.get('OverviewPage', 'N/A')
                print(f"       Game {i}: {team1} vs {team2} ({date})")
                if i == 1:
                    print(f"       OverviewPage: {overview}")
            return True, games
        else:
            print(f"    ⚠️  No data")
            return False, None

    except Exception as e:
        print(f"    ❌ Error: {str(e)}")
        return False, None

def search_msi_comprehensive(loader):
    """Comprehensive MSI search with all possible variants"""
    results = {}

    msi_searches = [
        # MSI 2024
        {
            "name": "MSI 2024 Play-In",
            "variants": [
                "2024 Mid-Season Invitational/Play-In",
                "Mid-Season Invitational 2024/Play-In",
                "MSI 2024/Play-In",
                "2024 Mid-Season Invitational/Play-In Stage",
                "2024 Mid-Season Invitational Play-In",
                "2024 MSI/Play-In",
                "MSI/2024/Play-In",
                "Mid-Season Invitational/2024/Play-In",
                "2024 Season Mid-Season Invitational/Play-In",
            ]
        },
        {
            "name": "MSI 2024 Bracket Stage",
            "variants": [
                "2024 Mid-Season Invitational/Bracket Stage",
                "2024 Mid-Season Invitational/Bracket",
                "2024 Mid-Season Invitational/Knockout",
                "2024 Mid-Season Invitational/Knockout Stage",
                "2024 Mid-Season Invitational/Main Event",
                "2024 Mid-Season Invitational/Playoffs",
                "MSI 2024/Bracket Stage",
                "2024 MSI/Bracket",
            ]
        },
        # MSI 2023
        {
            "name": "MSI 2023 Play-In",
            "variants": [
                "2023 Mid-Season Invitational/Play-In",
                "Mid-Season Invitational 2023/Play-In",
                "MSI 2023/Play-In",
                "2023 Mid-Season Invitational/Play-In Stage",
                "2023 Mid-Season Invitational Play-In",
                "2023 MSI/Play-In",
            ]
        },
        {
            "name": "MSI 2023 Bracket Stage",
            "variants": [
                "2023 Mid-Season Invitational/Bracket Stage",
                "2023 Mid-Season Invitational/Bracket",
                "2023 Mid-Season Invitational/Knockout",
                "2023 Mid-Season Invitational/Main Event",
            ]
        },
        # MSI 2021
        {
            "name": "MSI 2021 Groups",
            "variants": [
                "2021 Mid-Season Invitational/Group Stage",
                "2021 Mid-Season Invitational/Groups",
                "2021 Mid-Season Invitational/Main Event",
            ]
        },
        {
            "name": "MSI 2021 Knockout",
            "variants": [
                "2021 Mid-Season Invitational/Knockout Stage",
                "2021 Mid-Season Invitational/Knockout",
                "2021 Mid-Season Invitational/Bracket",
                "2021 Mid-Season Invitational/Playoffs",
            ]
        },
    ]

    for search in msi_searches:
        print("\n" + "="*80)
        print(f"SEARCHING: {search['name']}")
        print("="*80)

        found = False
        for i, variant in enumerate(search['variants'], 1):
            print(f"\n[{i}/{len(search['variants'])}]")
            success, games = test_url_variant(loader, search['name'], variant)

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

            time.sleep(3)  # Bot auth delay

        if not found:
            print(f"\n❌ NOT FOUND: {search['name']} after testing {len(search['variants'])} variants")
            results[search['name']] = None

        time.sleep(2)

    return results

def search_worlds_comprehensive(loader):
    """Comprehensive Worlds search with all possible variants"""
    results = {}

    worlds_searches = [
        # Worlds 2024
        {
            "name": "Worlds 2024 Play-In",
            "variants": [
                "2024 Season World Championship/Play-In",  # Already found
            ]
        },
        {
            "name": "Worlds 2024 Swiss Stage",
            "variants": [
                "2024 Season World Championship/Swiss Stage",
                "2024 Season World Championship/Swiss",
                "World Championship 2024/Swiss Stage",
                "Worlds 2024/Swiss Stage",
                "2024 World Championship/Swiss Stage",
                "2024 Season World Championship/Swiss Round",
                "2024 Worlds/Swiss",
                "Worlds/2024/Swiss Stage",
                "World Championship/2024/Swiss Stage",
                "2024 Season Worlds/Swiss Stage",
                "Season 2024 World Championship/Swiss Stage",
            ]
        },
        {
            "name": "Worlds 2024 Knockout Stage",
            "variants": [
                "2024 Season World Championship/Knockout Stage",
                "2024 Season World Championship/Knockout",
                "World Championship 2024/Knockout Stage",
                "Worlds 2024/Knockout Stage",
                "2024 World Championship/Knockout Stage",
                "2024 Season World Championship/Bracket",
                "2024 Season World Championship/Bracket Stage",
                "2024 Season World Championship/Playoffs",
                "2024 Worlds/Knockout",
                "2024 Season World Championship/Finals",
            ]
        },
        # Worlds 2023
        {
            "name": "Worlds 2023 Knockout Stage",
            "variants": [
                "2023 Season World Championship/Knockout Stage",
                "2023 Season World Championship/Knockout",
                "World Championship 2023/Knockout Stage",
                "Worlds 2023/Knockout Stage",
                "2023 World Championship/Knockout Stage",
                "2023 Season World Championship/Bracket",
            ]
        },
        # Worlds 2017
        {
            "name": "Worlds 2017 Main Event",
            "variants": [
                "2017 Season World Championship/Main Event",
                "2017 Season World Championship",  # Without stage
                "World Championship 2017/Main Event",
            ]
        },
        {
            "name": "Worlds 2017 Group Stage",
            "variants": [
                "2017 Season World Championship/Group Stage",
                "2017 Season World Championship/Groups",
                "World Championship 2017/Group Stage",
                "Worlds 2017/Group Stage",
            ]
        },
        # Worlds 2016
        {
            "name": "Worlds 2016 Main Event",
            "variants": [
                "2016 Season World Championship/Main Event",
                "2016 Season World Championship",
                "World Championship 2016/Main Event",
            ]
        },
        {
            "name": "Worlds 2016 Group Stage",
            "variants": [
                "2016 Season World Championship/Group Stage",
                "2016 Season World Championship/Groups",
                "World Championship 2016/Group Stage",
            ]
        },
        # Worlds 2015
        {
            "name": "Worlds 2015 Main Event",
            "variants": [
                "2015 Season World Championship/Main Event",
                "2015 Season World Championship",
                "World Championship 2015/Main Event",
            ]
        },
        {
            "name": "Worlds 2015 Group Stage",
            "variants": [
                "2015 Season World Championship/Group Stage",
                "2015 Season World Championship/Groups",
                "World Championship 2015/Group Stage",
                "Season 5 World Championship/Group Stage",
            ]
        },
    ]

    for search in worlds_searches:
        print("\n" + "="*80)
        print(f"SEARCHING: {search['name']}")
        print("="*80)

        found = False
        for i, variant in enumerate(search['variants'], 1):
            print(f"\n[{i}/{len(search['variants'])}]")
            success, games = test_url_variant(loader, search['name'], variant)

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

            time.sleep(3)  # Bot auth delay

        if not found:
            print(f"\n❌ NOT FOUND: {search['name']} after testing {len(search['variants'])} variants")
            results[search['name']] = None

        time.sleep(2)

    return results

def main():
    print("="*80)
    print("COMPREHENSIVE MSI AND WORLDS TOURNAMENT DISCOVERY")
    print("="*80)

    # Setup loader with bot auth
    os.environ['LEAGUEPEDIA_BOT_USERNAME'] = 'ekwo98@Elo'
    os.environ['LEAGUEPEDIA_BOT_PASSWORD'] = 'n7d9rsiccg7hujkg2hvtnglg4h93480r'

    loader = LeaguepediaLoader()

    # Check authentication
    if hasattr(loader, 'session') and hasattr(loader.session, 'auth'):
        print(f"[OK] Authenticated as {os.environ.get('LEAGUEPEDIA_BOT_USERNAME')}")
        print("✅ Bot authenticated successfully\n")

    # Search MSI
    print("\n" + "="*80)
    print("PART 1: MSI TOURNAMENTS")
    print("="*80)
    msi_results = search_msi_comprehensive(loader)

    # Search Worlds
    print("\n" + "="*80)
    print("PART 2: WORLDS TOURNAMENTS")
    print("="*80)
    worlds_results = search_worlds_comprehensive(loader)

    # Combine results
    all_results = {
        "msi": msi_results,
        "worlds": worlds_results
    }

    # Print summary
    print("\n" + "="*80)
    print("COMPREHENSIVE SEARCH RESULTS")
    print("="*80)

    msi_found = sum(1 for v in msi_results.values() if v is not None)
    msi_total = len(msi_results)
    worlds_found = sum(1 for v in worlds_results.values() if v is not None)
    worlds_total = len(worlds_results)

    print(f"\nMSI: {msi_found}/{msi_total} found")
    print(f"Worlds: {worlds_found}/{worlds_total} found")
    print(f"Total: {msi_found + worlds_found}/{msi_total + worlds_total} found")

    # Print all found URLs
    print("\n" + "="*80)
    print("FOUND TOURNAMENTS")
    print("="*80)

    for name, data in {**msi_results, **worlds_results}.items():
        if data:
            print(f"\n✅ {name}")
            print(f"   URL: {data['url']}")
            print(f"   Games found: {data['count']}")

    # Print not found
    print("\n" + "="*80)
    print("NOT FOUND")
    print("="*80)

    for name, data in {**msi_results, **worlds_results}.items():
        if not data:
            print(f"❌ {name}")

    # Save results
    output_file = "msi_worlds_comprehensive_results.json"
    with open(output_file, 'w') as f:
        # Convert games to serializable format
        serializable_results = {}
        for category, tournaments in all_results.items():
            serializable_results[category] = {}
            for name, data in tournaments.items():
                if data:
                    serializable_results[category][name] = {
                        "url": data["url"],
                        "count": data["count"],
                        "sample_games": [
                            {
                                "team1": g.get("Team1"),
                                "team2": g.get("Team2"),
                                "date": g.get("DateTime UTC")
                            }
                            for g in data["games"][:3]  # First 3 games
                        ]
                    }
                else:
                    serializable_results[category][name] = None

        json.dump(serializable_results, f, indent=2)

    print(f"\n📄 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
