#!/usr/bin/env python3
"""
Test Champions with CORRECT patterns based on user-provided links
Structure: Champions/{YEAR}_Season/{SPLIT}_{STAGE}
Where STAGE = Preseason, Season, Playoffs
"""

import os
import sys
import time
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.leaguepedia_loader import LeaguepediaLoader

def exponential_backoff_query(loader, url, max_retries=10):
    """Query with exponential backoff - 10 retries"""
    for retry in range(max_retries):
        try:
            games = loader._query_cargo(
                tables="ScoreboardGames",
                fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage",
                where=f"OverviewPage='{url}'",
                limit=5
            )
            return games
        except Exception as e:
            if retry < max_retries - 1:
                delay = 3 * (2 ** retry)
                print(f"    [RETRY {retry+1}/{max_retries}] Waiting {delay}s...")
                time.sleep(delay)
            else:
                print(f"    [FAILED] After {max_retries} retries")
                return None
    return None

def test_tournament(loader, name, url, results):
    """Test a single tournament URL"""
    print(f"\nTesting: {name}")
    print(f"URL: {url}")

    time.sleep(4)  # Base delay
    games = exponential_backoff_query(loader, url, max_retries=10)

    if games and len(games) > 0:
        print(f"✅ FOUND! {len(games)} games")
        for i, game in enumerate(games[:3], 1):
            team1 = game.get('Team1', 'N/A')
            team2 = game.get('Team2', 'N/A')
            date = game.get('DateTime UTC', 'N/A')
            print(f"   Game {i}: {team1} vs {team2} ({date})")

        results[name] = {
            "url": url,
            "count": len(games),
            "sample_games": [
                {
                    "team1": game.get('Team1', 'N/A'),
                    "team2": game.get('Team2', 'N/A'),
                    "date": game.get('DateTime UTC', 'N/A')
                }
                for game in games[:3]
            ]
        }
        return True
    else:
        print(f"❌ NOT FOUND")
        results[name] = None
        return False

def main():
    print("="*80)
    print("CHAMPIONS CORRECT PATTERNS TEST")
    print("Based on user-provided links:")
    print("- Champions/{YEAR}_Season/{SPLIT}_Preseason")
    print("- Champions/{YEAR}_Season/{SPLIT}_Season")
    print("- Champions/{YEAR}_Season/{SPLIT}_Playoffs")
    print("="*80)

    loader = LeaguepediaLoader()
    results = {}
    found = 0
    not_found = 0

    # Years and Splits to test
    years = [2012, 2013, 2014, 2015]
    splits = ["Spring", "Summer", "Winter"]

    for year in years:
        print(f"\n{'='*80}")
        print(f"TESTING CHAMPIONS {year}")
        print(f"{'='*80}")

        for split in splits:
            # Test Preseason
            name = f"Champions {year} {split} Preseason"
            url = f"Champions/{year}_Season/{split}_Preseason"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Test Season (Regular Season)
            name = f"Champions {year} {split} Season"
            url = f"Champions/{year}_Season/{split}_Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Test Playoffs
            name = f"Champions {year} {split} Playoffs"
            url = f"Champions/{year}_Season/{split}_Playoffs"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # Summary
    print(f"\n{'='*80}")
    print("SEARCH COMPLETE")
    print(f"{'='*80}")
    print(f"\nFound: {found}")
    print(f"Not Found: {not_found}")
    print(f"Total: {found + not_found}")
    print(f"Success Rate: {found/(found+not_found)*100:.1f}%")

    # Save results
    output_file = Path(__file__).parent / "champions_correct_patterns_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_file}")

    # Print found summary
    print(f"\n{'='*80}")
    print("FOUND TOURNAMENTS")
    print(f"{'='*80}")
    for name, data in results.items():
        if data is not None:
            print(f"✅ {name}")
            print(f"   URL: {data['url']}")

if __name__ == "__main__":
    main()
