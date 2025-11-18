#!/usr/bin/env python3
"""
COMPREHENSIVE tournament search - ALL leagues, ALL years, ALL splits
With 10 retries exponential backoff

Based on confirmed patterns:
- Modern leagues: {LEAGUE}/{YEAR} Season/{SPLIT} Season
- Playoffs: {LEAGUE}/{YEAR} Season/{SPLIT} Playoffs
- OGN Champions: Champions/{YEAR}_Season
- KeSPA Cup: {YEAR} LoL KeSPA Cup
- Demacia Cup: Demacia_Championship/{YEAR}_Season
"""

import json
import time
import os
import sys
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
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*80}")

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
    print("COMPREHENSIVE ALL TOURNAMENTS SEARCH")
    print("Testing ALL leagues, ALL years, ALL splits with 10 retries")
    print("="*80)

    loader = LeaguepediaLoader()
    results = {}
    found = 0
    not_found = 0

    # ========================================================================
    # LPL Summer Splits (2013-2024)
    # ========================================================================
    print("\n" + "="*80)
    print("LPL SUMMER SPLITS")
    print("="*80)

    for year in range(2013, 2025):
        name = f"LPL {year} Summer"
        url = f"LPL/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # LPL Summer Playoffs
    for year in [2013, 2014, 2015, 2016, 2017, 2018, 2020, 2024]:
        name = f"LPL {year} Summer Playoffs"
        url = f"LPL/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # LCK Summer Splits (2016-2024)
    # ========================================================================
    print("\n" + "="*80)
    print("LCK SUMMER SPLITS")
    print("="*80)

    for year in range(2016, 2025):
        name = f"LCK {year} Summer"
        url = f"LCK/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # EU LCS / LEC Summer and additional years
    # ========================================================================
    print("\n" + "="*80)
    print("EU LCS / LEC SUMMER + ADDITIONAL YEARS")
    print("="*80)

    # EU LCS Season 3 Summer
    name = "EU LCS Season 3 Summer"
    url = "EU LCS/Season 3/Summer Season"
    if test_tournament(loader, name, url, results):
        found += 1
    else:
        not_found += 1

    # EU LCS 2014-2018 Summer
    for year in range(2014, 2019):
        name = f"EU LCS {year} Summer"
        url = f"EU LCS/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # LEC 2019-2024 Summer
    for year in range(2019, 2025):
        name = f"LEC {year} Summer"
        url = f"LEC/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # NA LCS / LCS Summer
    # ========================================================================
    print("\n" + "="*80)
    print("NA LCS / LCS SUMMER")
    print("="*80)

    # NA LCS Season 3 Summer
    name = "NA LCS Season 3 Summer"
    url = "NA LCS/Season 3/Summer Season"
    if test_tournament(loader, name, url, results):
        found += 1
    else:
        not_found += 1

    # NA LCS 2014-2018 Summer
    for year in range(2014, 2019):
        name = f"NA LCS {year} Summer"
        url = f"NA LCS/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # LCS 2019-2024 Summer
    for year in range(2019, 2025):
        name = f"LCS {year} Summer"
        url = f"LCS/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # Smaller Regions - ALL years 2020-2024
    # ========================================================================
    print("\n" + "="*80)
    print("SMALLER REGIONS - PCS 2020-2024")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"PCS {year} {split}"
            url = f"PCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Playoffs
            name_playoffs = f"PCS {year} {split} Playoffs"
            url_playoffs = f"PCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name_playoffs, url_playoffs, results):
                found += 1
            else:
                not_found += 1

    print("\n" + "="*80)
    print("SMALLER REGIONS - VCS 2020-2024")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"VCS {year} {split}"
            url = f"VCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Playoffs
            name_playoffs = f"VCS {year} {split} Playoffs"
            url_playoffs = f"VCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name_playoffs, url_playoffs, results):
                found += 1
            else:
                not_found += 1

    print("\n" + "="*80)
    print("SMALLER REGIONS - LJL 2020-2024")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"LJL {year} {split}"
            url = f"LJL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Playoffs
            name_playoffs = f"LJL {year} {split} Playoffs"
            url_playoffs = f"LJL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name_playoffs, url_playoffs, results):
                found += 1
            else:
                not_found += 1

    print("\n" + "="*80)
    print("SMALLER REGIONS - TCL 2020-2024")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Winter", "Summer"]:
            name = f"TCL {year} {split}"
            url = f"TCL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Playoffs
            name_playoffs = f"TCL {year} {split} Playoffs"
            url_playoffs = f"TCL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name_playoffs, url_playoffs, results):
                found += 1
            else:
                not_found += 1

    print("\n" + "="*80)
    print("SMALLER REGIONS - LLA 2020-2024")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Opening", "Closing"]:
            name = f"LLA {year} {split}"
            url = f"LLA/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Playoffs
            name_playoffs = f"LLA {year} {split} Playoffs"
            url_playoffs = f"LLA/{year} Season/{split} Playoffs"
            if test_tournament(loader, name_playoffs, url_playoffs, results):
                found += 1
            else:
                not_found += 1

    # ========================================================================
    # CBLOL Historical (2015-2019)
    # ========================================================================
    print("\n" + "="*80)
    print("CBLOL HISTORICAL 2015-2019")
    print("="*80)

    for year in range(2015, 2020):
        for split in [1, 2]:
            name = f"CBLOL {year} Split {split}"
            url = f"CBLOL/{year} Split {split}"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            # Playoffs
            name_playoffs = f"CBLOL {year} Split {split} Playoffs"
            url_playoffs = f"CBLOL/{year} Split {split}/Playoffs"
            if test_tournament(loader, name_playoffs, url_playoffs, results):
                found += 1
            else:
                not_found += 1

    # ========================================================================
    # OGN Champions (2012-2015)
    # ========================================================================
    print("\n" + "="*80)
    print("OGN CHAMPIONS 2012-2015")
    print("="*80)

    for year in range(2012, 2016):
        name = f"Champions {year} Season"
        url = f"Champions/{year}_Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("SEARCH COMPLETE")
    print("="*80)
    print(f"\nFound: {found}")
    print(f"Not Found: {not_found}")
    print(f"Total: {found + not_found}")
    print(f"Success Rate: {found/(found+not_found)*100:.1f}%")

    # Save results
    output_file = Path(__file__).parent / "comprehensive_all_tournaments_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_file}")

    # Print found summary
    print("\n" + "="*80)
    print("FOUND TOURNAMENTS SUMMARY")
    print("="*80)
    for name, data in results.items():
        if data is not None:
            print(f"✅ {name}")
            print(f"   URL: {data['url']}")

if __name__ == "__main__":
    main()
