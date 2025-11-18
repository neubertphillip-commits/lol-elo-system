#!/usr/bin/env python3
"""
COMPLETE TOURNAMENT DISCOVERY - WIRKLICH ALLES
Testet JEDEN Split, JEDES Playoff, JEDE Region, ALLE Jahre

Das umfasst:
- Champions 2012-2015 (alle 4 Stufen × 3 Splits)
- KeSPA Cup 2015-2025
- Demacia Cup 2017-2024
- MSI 2015-2024
- Worlds 2013-2024 (Play-In + Main Event)
- LPL 2013-2024 (Spring + Summer + Playoffs)
- LCK 2016-2024 (Spring + Summer + Playoffs)
- LEC/EU LCS 2013-2024 (Spring + Summer + Playoffs)
- LCS/NA LCS 2013-2024 (Spring + Summer + Playoffs)
- CBLOL 2015-2024 (Split 1 + Split 2 + Playoffs)
- PCS, VCS, LJL, TCL, LLA 2020-2024 (beide Splits + Playoffs)
"""

import json
import time
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.leaguepedia_loader import LeaguepediaLoader

def test_tournament(loader, name, url, results, category):
    """Test a single tournament URL"""
    print(f"Testing: {name:<60}", end="")

    time.sleep(2)  # Base delay between queries (with bot auth)
    games = loader._query_cargo(
        tables="ScoreboardGames",
        fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage",
        where=f"OverviewPage='{url}'",
        limit=5
    )

    if games and len(games) > 0:
        print(f" ✅ FOUND ({len(games)} games)")
        results[name] = {
            "url": url,
            "count": len(games),
            "category": category,
            "status": "found"
        }
        return True
    else:
        print(f" ❌ NOT FOUND")
        results[name] = {
            "url": url,
            "category": category,
            "status": "not_found"
        }
        return False

def main():
    print("="*80)
    print("COMPLETE TOURNAMENT DISCOVERY - WIRKLICH ALLES")
    print("="*80)
    print("Testet JEDEN Split, JEDES Playoff, ALLE Jahre, ALLE Regionen")
    print("="*80)

    loader = LeaguepediaLoader()
    results = {}
    stats = {
        "found": 0,
        "not_found": 0,
        "total": 0
    }

    # ========================================================================
    # CHAMPIONS (2012-2015) - 4 Stufen × 3 Splits
    # ========================================================================
    print("\n" + "="*80)
    print("CHAMPIONS (2012-2015)")
    print("="*80)

    for year in [2012, 2013, 2014, 2015]:
        for split in ["Spring", "Summer", "Winter"]:
            for stage in ["Qualifiers", "Preseason", "Season", "Playoffs"]:
                name = f"Champions {year} {split} {stage}"
                url = f"Champions/{year}_Season/{split}_{stage}"
                if test_tournament(loader, name, url, results, "Champions"):
                    stats["found"] += 1
                else:
                    stats["not_found"] += 1
                stats["total"] += 1

    # ========================================================================
    # KESPA CUP (2015-2025)
    # ========================================================================
    print("\n" + "="*80)
    print("KESPA CUP (2015-2025)")
    print("="*80)

    for year in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2024, 2025]:
        # Try underscore pattern first
        name = f"KeSPA Cup {year}"
        url = f"{year}_LoL_KeSPA_Cup"
        if test_tournament(loader, name, url, results, "KeSPA Cup"):
            stats["found"] += 1
        else:
            # Try space pattern
            url = f"{year} LoL KeSPA Cup"
            if test_tournament(loader, name + " (space)", url, results, "KeSPA Cup"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
        stats["total"] += 1

    # ========================================================================
    # DEMACIA CUP (2017-2024)
    # ========================================================================
    print("\n" + "="*80)
    print("DEMACIA CUP (2017-2024)")
    print("="*80)

    for year in [2017, 2018, 2019, 2020, 2021, 2024]:
        name = f"Demacia Cup {year}"
        url = f"Demacia_Championship/{year}_Season"
        if test_tournament(loader, name, url, results, "Demacia Cup"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # ========================================================================
    # MSI (2015-2024)
    # ========================================================================
    print("\n" + "="*80)
    print("MSI (2015-2024)")
    print("="*80)

    for year in range(2015, 2025):
        if year == 2020:  # MSI 2020 was cancelled
            continue
        name = f"MSI {year}"
        url = f"{year} Mid-Season Invitational"
        if test_tournament(loader, name, url, results, "MSI"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # ========================================================================
    # WORLDS (2013-2024)
    # ========================================================================
    print("\n" + "="*80)
    print("WORLDS (2013-2024)")
    print("="*80)

    for year in range(2013, 2025):
        # Play-In (started 2017)
        if year >= 2017:
            name = f"Worlds {year} Play-In"
            url = f"{year} Season World Championship/Play-In"
            if test_tournament(loader, name, url, results, "Worlds"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

        # Main Event
        if year >= 2017:
            name = f"Worlds {year} Main Event"
            url = f"{year} Season World Championship/Main Event"
        else:
            name = f"Worlds {year}"
            url = f"{year} Season World Championship"

        if test_tournament(loader, name, url, results, "Worlds"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # ========================================================================
    # LPL (2013-2024) - Spring + Summer + Playoffs
    # ========================================================================
    print("\n" + "="*80)
    print("LPL (2013-2024) - Spring + Summer + Playoffs")
    print("="*80)

    for year in range(2013, 2025):
        for split in ["Spring", "Summer"]:
            # Regular Season
            name = f"LPL {year} {split}"
            url = f"LPL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LPL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            # Playoffs
            name = f"LPL {year} {split} Playoffs"
            url = f"LPL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LPL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # ========================================================================
    # LCK (2016-2024) - Spring + Summer + Playoffs
    # ========================================================================
    print("\n" + "="*80)
    print("LCK (2016-2024) - Spring + Summer + Playoffs")
    print("="*80)

    for year in range(2016, 2025):
        for split in ["Spring", "Summer"]:
            # Regular Season
            name = f"LCK {year} {split}"
            url = f"LCK/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LCK"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            # Playoffs
            name = f"LCK {year} {split} Playoffs"
            url = f"LCK/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LCK"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # ========================================================================
    # EU LCS / LEC (2013-2024) - Spring + Summer + Playoffs
    # ========================================================================
    print("\n" + "="*80)
    print("EU LCS / LEC (2013-2024) - Spring + Summer + Playoffs")
    print("="*80)

    # Season 3 (2013)
    for split in ["Spring", "Summer"]:
        name = f"EU LCS Season 3 {split}"
        url = f"EU LCS/Season 3/{split} Season"
        if test_tournament(loader, name, url, results, "LEC/EU LCS"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

        name = f"EU LCS Season 3 {split} Playoffs"
        url = f"EU LCS/Season 3/{split} Playoffs"
        if test_tournament(loader, name, url, results, "LEC/EU LCS"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # EU LCS (2014-2018)
    for year in range(2014, 2019):
        for split in ["Spring", "Summer"]:
            name = f"EU LCS {year} {split}"
            url = f"EU LCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LEC/EU LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"EU LCS {year} {split} Playoffs"
            url = f"EU LCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LEC/EU LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # LEC (2019-2024)
    for year in range(2019, 2025):
        for split in ["Spring", "Summer"]:
            name = f"LEC {year} {split}"
            url = f"LEC/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LEC/EU LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"LEC {year} {split} Playoffs"
            url = f"LEC/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LEC/EU LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # ========================================================================
    # NA LCS / LCS (2013-2024) - Spring + Summer + Playoffs
    # ========================================================================
    print("\n" + "="*80)
    print("NA LCS / LCS (2013-2024) - Spring + Summer + Playoffs")
    print("="*80)

    # Season 3 (2013)
    for split in ["Spring", "Summer"]:
        name = f"NA LCS Season 3 {split}"
        url = f"NA LCS/Season 3/{split} Season"
        if test_tournament(loader, name, url, results, "LCS/NA LCS"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

        name = f"NA LCS Season 3 {split} Playoffs"
        url = f"NA LCS/Season 3/{split} Playoffs"
        if test_tournament(loader, name, url, results, "LCS/NA LCS"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # NA LCS (2014-2018)
    for year in range(2014, 2019):
        for split in ["Spring", "Summer"]:
            name = f"NA LCS {year} {split}"
            url = f"NA LCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LCS/NA LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"NA LCS {year} {split} Playoffs"
            url = f"NA LCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LCS/NA LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # LCS (2019-2024)
    for year in range(2019, 2025):
        for split in ["Spring", "Summer"]:
            name = f"LCS {year} {split}"
            url = f"LCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LCS/NA LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"LCS {year} {split} Playoffs"
            url = f"LCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LCS/NA LCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # ========================================================================
    # CBLOL (2015-2024) - Split 1 + Split 2 + Playoffs
    # ========================================================================
    print("\n" + "="*80)
    print("CBLOL (2015-2024) - Split 1 + Split 2 + Playoffs")
    print("="*80)

    for year in range(2015, 2025):
        for split in [1, 2]:
            name = f"CBLOL {year} Split {split}"
            url = f"CBLOL/{year} Split {split}"
            if test_tournament(loader, name, url, results, "CBLOL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"CBLOL {year} Split {split} Playoffs"
            url = f"CBLOL/{year} Split {split}/Playoffs"
            if test_tournament(loader, name, url, results, "CBLOL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # ========================================================================
    # KLEINERE REGIONEN (2020-2024) - Beide Splits + Playoffs
    # ========================================================================
    print("\n" + "="*80)
    print("PCS (2020-2024) - Spring + Summer + Playoffs")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"PCS {year} {split}"
            url = f"PCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "PCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"PCS {year} {split} Playoffs"
            url = f"PCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "PCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    print("\n" + "="*80)
    print("VCS (2020-2024) - Spring + Summer + Playoffs")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"VCS {year} {split}"
            url = f"VCS/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "VCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"VCS {year} {split} Playoffs"
            url = f"VCS/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "VCS"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    print("\n" + "="*80)
    print("LJL (2020-2024) - Spring + Summer + Playoffs")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Spring", "Summer"]:
            name = f"LJL {year} {split}"
            url = f"LJL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LJL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"LJL {year} {split} Playoffs"
            url = f"LJL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LJL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    print("\n" + "="*80)
    print("TCL (2020-2024) - Winter + Summer + Playoffs")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Winter", "Summer"]:
            name = f"TCL {year} {split}"
            url = f"TCL/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "TCL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"TCL {year} {split} Playoffs"
            url = f"TCL/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "TCL"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    print("\n" + "="*80)
    print("LLA (2020-2024) - Opening + Closing + Playoffs")
    print("="*80)

    for year in range(2020, 2025):
        for split in ["Opening", "Closing"]:
            name = f"LLA {year} {split}"
            url = f"LLA/{year} Season/{split} Season"
            if test_tournament(loader, name, url, results, "LLA"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

            name = f"LLA {year} {split} Playoffs"
            url = f"LLA/{year} Season/{split} Playoffs"
            if test_tournament(loader, name, url, results, "LLA"):
                stats["found"] += 1
            else:
                stats["not_found"] += 1
            stats["total"] += 1

    # ========================================================================
    # REGIONAL FINALS (2015-2024) - Alle Regionen
    # ========================================================================
    print("\n" + "="*80)
    print("REGIONAL FINALS (2015-2024) - Alle Regionen")
    print("="*80)

    # EU LCS/LEC Regional Finals (2015-2024)
    for year in range(2015, 2025):
        league = "EU_LCS" if year <= 2018 else "LEC"
        name = f"{league.replace('_', ' ')} {year} Regional Finals"
        url = f"{league}/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # NA LCS/LCS Regional Finals (2015-2024)
    for year in range(2015, 2025):
        league = "NA_LCS" if year <= 2017 else "LCS"
        name = f"{league.replace('_', ' ')} {year} Regional Finals"
        url = f"{league}/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # LPL Regional Finals (2015-2024)
    for year in range(2015, 2025):
        name = f"LPL {year} Regional Finals"
        url = f"LPL/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # LCK Regional Finals (2016-2024)
    for year in range(2016, 2025):
        name = f"LCK {year} Regional Finals"
        url = f"LCK/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # CBLOL Regional Finals (2015-2024)
    for year in range(2015, 2025):
        name = f"CBLOL {year} Regional Finals"
        url = f"CBLOL/{year}/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # PCS Regional Finals (2020-2024)
    for year in range(2020, 2025):
        name = f"PCS {year} Regional Finals"
        url = f"PCS/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # VCS Regional Finals (2020-2024)
    for year in range(2020, 2025):
        name = f"VCS {year} Regional Finals"
        url = f"VCS/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # LJL Regional Finals (2020-2024)
    for year in range(2020, 2025):
        name = f"LJL {year} Regional Finals"
        url = f"LJL/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # TCL Regional Finals (2020-2024)
    for year in range(2020, 2025):
        name = f"TCL {year} Regional Finals"
        url = f"TCL/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # LLA Regional Finals (2020-2024)
    for year in range(2020, 2025):
        name = f"LLA {year} Regional Finals"
        url = f"LLA/{year}_Season/Regional_Finals"
        if test_tournament(loader, name, url, results, "Regional Finals"):
            stats["found"] += 1
        else:
            stats["not_found"] += 1
        stats["total"] += 1

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("COMPLETE DISCOVERY FINISHED")
    print("="*80)
    print(f"\n✅ Found:     {stats['found']:4d} tournaments")
    print(f"❌ Not Found: {stats['not_found']:4d} tournaments")
    print(f"📊 Total:     {stats['total']:4d} tournaments tested")
    print(f"📈 Success:   {stats['found']/stats['total']*100:.1f}%")

    # Save results
    output_file = Path(__file__).parent / "complete_tournament_discovery_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_file}")

    # Category summary
    print("\n" + "="*80)
    print("FOUND TOURNAMENTS BY CATEGORY")
    print("="*80)

    categories = {}
    for name, data in results.items():
        if data["status"] == "found":
            cat = data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)

    for category in sorted(categories.keys()):
        print(f"\n{category}: {len(categories[category])} tournaments found")

    # NOT FOUND LIST - for user to find links
    print("\n" + "="*80)
    print("NOT FOUND - Bitte Links suchen für:")
    print("="*80)

    not_found_by_category = {}
    for name, data in results.items():
        if data["status"] == "not_found":
            cat = data["category"]
            if cat not in not_found_by_category:
                not_found_by_category[cat] = []
            not_found_by_category[cat].append({
                "name": name,
                "url": data["url"]
            })

    for category in sorted(not_found_by_category.keys()):
        items = not_found_by_category[category]
        print(f"\n{category}: {len(items)} NOT FOUND")
        print("-" * 80)
        for item in items:
            print(f"  ❌ {item['name']}")
            print(f"     Tested URL: {item['url']}")

    # Save not found list to separate file
    not_found_file = Path(__file__).parent / "not_found_tournaments.txt"
    with open(not_found_file, "w", encoding="utf-8") as f:
        f.write("NOT FOUND TOURNAMENTS - Bitte Links suchen\n")
        f.write("="*80 + "\n\n")
        for category in sorted(not_found_by_category.keys()):
            items = not_found_by_category[category]
            f.write(f"{category}: {len(items)} NOT FOUND\n")
            f.write("-"*80 + "\n")
            for item in items:
                f.write(f"❌ {item['name']}\n")
                f.write(f"   Tested URL: {item['url']}\n\n")
            f.write("\n")

    print(f"\n📄 Not found list saved to: {not_found_file}")

if __name__ == "__main__":
    main()
