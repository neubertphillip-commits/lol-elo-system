#!/usr/bin/env python3
"""
COMPREHENSIVE TOURNAMENT SEARCH - ALL IN ONE
Tests ALL tournament patterns discovered with user feedback:
- Champions (4 stages: Qualifiers, Preseason, Season, Playoffs)
- KeSPA Cup (underscore and space patterns)
- Demacia Cup
- All league playoffs
- Summer splits for all leagues
- Smaller regions 2020-2024
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
    print(f"\nTesting: {name}")
    print(f"  URL: {url}")

    time.sleep(4)  # Base delay
    games = exponential_backoff_query(loader, url, max_retries=10)

    if games and len(games) > 0:
        print(f"  ✅ FOUND! {len(games)} games")
        results[name] = {
            "url": url,
            "count": len(games),
            "status": "found"
        }
        return True
    else:
        print(f"  ❌ NOT FOUND")
        results[name] = {
            "url": url,
            "status": "not_found"
        }
        return False

def main():
    print("="*80)
    print("COMPREHENSIVE TOURNAMENT SEARCH - ALL IN ONE")
    print("="*80)

    loader = LeaguepediaLoader()
    results = {}
    found = 0
    not_found = 0

    # ========================================================================
    # CHAMPIONS (2012-2015) - 4 Stages per Split
    # ========================================================================
    print("\n" + "="*80)
    print("CHAMPIONS (2012-2015) - ALL 4 STAGES")
    print("="*80)

    for year in [2012, 2013, 2014, 2015]:
        print(f"\n{'─'*80}")
        print(f"Champions {year}")
        print(f"{'─'*80}")

        for split in ["Spring", "Summer", "Winter"]:
            for stage in ["Qualifiers", "Preseason", "Season", "Playoffs"]:
                name = f"Champions {year} {split} {stage}"
                url = f"Champions/{year}_Season/{split}_{stage}"
                if test_tournament(loader, name, url, results):
                    found += 1
                else:
                    not_found += 1

    # ========================================================================
    # KESPA CUP - Both patterns (underscore and space)
    # ========================================================================
    print("\n" + "="*80)
    print("KESPA CUP (2015-2025)")
    print("="*80)

    for year in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2024, 2025]:
        # Try underscore pattern first
        name = f"KeSPA Cup {year} (underscore)"
        url = f"{year}_LoL_KeSPA_Cup"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            # Try space pattern
            name = f"KeSPA Cup {year} (space)"
            url = f"{year} LoL KeSPA Cup"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # ========================================================================
    # DEMACIA CUP
    # ========================================================================
    print("\n" + "="*80)
    print("DEMACIA CUP")
    print("="*80)

    for year in [2017, 2018, 2019, 2020, 2021, 2024]:
        name = f"Demacia Cup {year}"
        url = f"Demacia_Championship/{year}_Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # LPL SUMMER + PLAYOFFS
    # ========================================================================
    print("\n" + "="*80)
    print("LPL SUMMER (2013-2024)")
    print("="*80)

    for year in range(2013, 2025):
        name = f"LPL {year} Summer"
        url = f"LPL/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

        name = f"LPL {year} Summer Playoffs"
        url = f"LPL/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # LCK SUMMER + PLAYOFFS
    # ========================================================================
    print("\n" + "="*80)
    print("LCK SUMMER (2016-2024)")
    print("="*80)

    for year in range(2016, 2025):
        name = f"LCK {year} Summer"
        url = f"LCK/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

        name = f"LCK {year} Summer Playoffs"
        url = f"LCK/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # EU LCS / LEC SUMMER + PLAYOFFS
    # ========================================================================
    print("\n" + "="*80)
    print("EU LCS / LEC SUMMER (2013-2024)")
    print("="*80)

    # Season 3
    name = "EU LCS Season 3 Summer"
    url = "EU LCS/Season 3/Summer Season"
    if test_tournament(loader, name, url, results):
        found += 1
    else:
        not_found += 1

    name = "EU LCS Season 3 Summer Playoffs"
    url = "EU LCS/Season 3/Summer Playoffs"
    if test_tournament(loader, name, url, results):
        found += 1
    else:
        not_found += 1

    # EU LCS 2014-2018
    for year in range(2014, 2019):
        name = f"EU LCS {year} Summer"
        url = f"EU LCS/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

        name = f"EU LCS {year} Summer Playoffs"
        url = f"EU LCS/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # LEC 2019-2024
    for year in range(2019, 2025):
        name = f"LEC {year} Summer"
        url = f"LEC/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

        name = f"LEC {year} Summer Playoffs"
        url = f"LEC/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # NA LCS / LCS SUMMER + PLAYOFFS
    # ========================================================================
    print("\n" + "="*80)
    print("NA LCS / LCS SUMMER (2013-2024)")
    print("="*80)

    # Season 3
    name = "NA LCS Season 3 Summer"
    url = "NA LCS/Season 3/Summer Season"
    if test_tournament(loader, name, url, results):
        found += 1
    else:
        not_found += 1

    name = "NA LCS Season 3 Summer Playoffs"
    url = "NA LCS/Season 3/Summer Playoffs"
    if test_tournament(loader, name, url, results):
        found += 1
    else:
        not_found += 1

    # NA LCS 2014-2018
    for year in range(2014, 2019):
        name = f"NA LCS {year} Summer"
        url = f"NA LCS/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

        name = f"NA LCS {year} Summer Playoffs"
        url = f"NA LCS/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # LCS 2019-2024
    for year in range(2019, 2025):
        name = f"LCS {year} Summer"
        url = f"LCS/{year} Season/Summer Season"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

        name = f"LCS {year} Summer Playoffs"
        url = f"LCS/{year} Season/Summer Playoffs"
        if test_tournament(loader, name, url, results):
            found += 1
        else:
            not_found += 1

    # ========================================================================
    # CBLOL HISTORICAL (2015-2019)
    # ========================================================================
    print("\n" + "="*80)
    print("CBLOL HISTORICAL (2015-2019)")
    print("="*80)

    for year in range(2015, 2020):
        for split in [1, 2]:
            name = f"CBLOL {year} Split {split}"
            url = f"CBLOL/{year} Split {split}"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            name = f"CBLOL {year} Split {split} Playoffs"
            url = f"CBLOL/{year} Split {split}/Playoffs"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # ========================================================================
    # SMALLER REGIONS (2020-2024) - ALL SPLITS
    # ========================================================================
    print("\n" + "="*80)
    print("SMALLER REGIONS (2020-2024)")
    print("="*80)

    # PCS
    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"PCS {year} {split}"
            url = f"PCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            name = f"PCS {year} {split} Playoffs"
            url = f"PCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # VCS
    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"VCS {year} {split}"
            url = f"VCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            name = f"VCS {year} {split} Playoffs"
            url = f"VCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # LJL
    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"LJL {year} {split}"
            url = f"LJL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            name = f"LJL {year} {split} Playoffs"
            url = f"LJL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # TCL
    for year in range(2020, 2025):
        for split in ["Winter", "Summer"]:
            name = f"TCL {year} {split}"
            url = f"TCL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            name = f"TCL {year} {split} Playoffs"
            url = f"TCL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

    # LLA
    for year in range(2020, 2025):
        for split in ["Opening", "Closing"]:
            name = f"LLA {year} {split}"
            url = f"LLA/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results):
                found += 1
            else:
                not_found += 1

            name = f"LLA {year} {split} Playoffs"
            url = f"LLA/{year} Season/{split} Playoffs"
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
    print(f"\n✅ Found: {found}")
    print(f"❌ Not Found: {not_found}")
    print(f"📊 Total: {found + not_found}")
    print(f"📈 Success Rate: {found/(found+not_found)*100:.1f}%")

    # Save results
    output_file = Path(__file__).parent / "comprehensive_tournament_search_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_file}")

    # Print found tournaments by category
    print("\n" + "="*80)
    print("FOUND TOURNAMENTS BY CATEGORY")
    print("="*80)

    categories = {
        "Champions": [],
        "KeSPA Cup": [],
        "Demacia Cup": [],
        "LPL": [],
        "LCK": [],
        "LEC/EU LCS": [],
        "LCS/NA LCS": [],
        "CBLOL": [],
        "PCS": [],
        "VCS": [],
        "LJL": [],
        "TCL": [],
        "LLA": []
    }

    for name, data in results.items():
        if data["status"] == "found":
            if "Champions" in name:
                categories["Champions"].append(name)
            elif "KeSPA" in name:
                categories["KeSPA Cup"].append(name)
            elif "Demacia" in name:
                categories["Demacia Cup"].append(name)
            elif "LPL" in name:
                categories["LPL"].append(name)
            elif "LCK" in name:
                categories["LCK"].append(name)
            elif "LEC" in name or "EU LCS" in name:
                categories["LEC/EU LCS"].append(name)
            elif "LCS" in name or "NA LCS" in name:
                categories["LCS/NA LCS"].append(name)
            elif "CBLOL" in name:
                categories["CBLOL"].append(name)
            elif "PCS" in name:
                categories["PCS"].append(name)
            elif "VCS" in name:
                categories["VCS"].append(name)
            elif "LJL" in name:
                categories["LJL"].append(name)
            elif "TCL" in name:
                categories["TCL"].append(name)
            elif "LLA" in name:
                categories["LLA"].append(name)

    for category, tournaments in categories.items():
        if tournaments:
            print(f"\n{category}: {len(tournaments)} tournaments")
            for t in tournaments[:5]:  # Show first 5
                print(f"  ✅ {t}")
            if len(tournaments) > 5:
                print(f"  ... and {len(tournaments)-5} more")

if __name__ == "__main__":
    main()
