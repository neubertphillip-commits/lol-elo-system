#!/usr/bin/env python3
"""
TEST NEW MINOR REGION EVENTS
Test all 88 proposed new events before adding to main discovery script
"""

import os
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.leaguepedia_loader import LeaguepediaLoader

def test_tournament(loader, name, url_with_underscores):
    """Test if tournament exists in MatchSchedule table"""
    url = url_with_underscores.replace('_', ' ')

    try:
        matches = loader._query_cargo(
            tables="MatchSchedule",
            fields="Team1,Team2",
            where=f"OverviewPage='{url}'",
            limit=5
        )

        if matches and len(matches) > 0:
            print(f"✅ {name:70} {len(matches)} matches")
            return {'name': name, 'url': url, 'found': True, 'sample_matches': len(matches)}
        else:
            print(f"❌ {name:70} NOT FOUND")
            return {'name': name, 'url': url, 'found': False}

    except Exception as e:
        print(f"❌ {name:70} ERROR: {e}")
        return {'name': name, 'url': url, 'found': False, 'error': str(e)}

def generate_test_tournaments():
    """Generate the 88 proposed new tournaments"""
    tournaments = []

    # ========================================================================
    # 2025 SEASONS (8 Events)
    # ========================================================================
    tournaments.append(("CBLOL 2025 Split 1", "CBLOL/2025_Season/Split_1"))
    tournaments.append(("CBLOL 2025 Split 1 Playoffs", "CBLOL/2025_Season/Split_1_Playoffs"))
    tournaments.append(("CBLOL 2025 Split 2", "CBLOL/2025_Season/Split_2"))
    tournaments.append(("CBLOL 2025 Split 2 Playoffs", "CBLOL/2025_Season/Split_2_Playoffs"))

    tournaments.append(("LLA 2025 Opening", "LLA/2025_Season/Opening_Season"))
    tournaments.append(("LLA 2025 Opening Playoffs", "LLA/2025_Season/Opening_Playoffs"))
    tournaments.append(("LLA 2025 Closing", "LLA/2025_Season/Closing_Season"))
    tournaments.append(("LLA 2025 Closing Playoffs", "LLA/2025_Season/Closing_Playoffs"))

    # ========================================================================
    # LAS (Latin America South) 2013-2018 (22 Events)
    # ========================================================================
    for year in range(2014, 2019):
        tournaments.append((f"LAS {year} Opening", f"LAS/{year}_Season/Opening_Season"))
        tournaments.append((f"LAS {year} Opening Playoffs", f"LAS/{year}_Season/Opening_Playoffs"))
        tournaments.append((f"LAS {year} Closing", f"LAS/{year}_Season/Closing_Season"))
        tournaments.append((f"LAS {year} Closing Playoffs", f"LAS/{year}_Season/Closing_Playoffs"))

    tournaments.append(("LAS 2013 Opening", "LAS/2013_Season/Opening_Season"))
    tournaments.append(("LAS 2013 Closing", "LAS/2013_Season/Closing_Season"))

    # ========================================================================
    # LCO (Oceania) 2021-2025 (20 Events)
    # ========================================================================
    for year in range(2021, 2026):
        tournaments.append((f"LCO {year} Split 1", f"LCO/{year}_Season/Split_1"))
        tournaments.append((f"LCO {year} Split 1 Playoffs", f"LCO/{year}_Season/Split_1_Playoffs"))
        tournaments.append((f"LCO {year} Split 2", f"LCO/{year}_Season/Split_2"))
        tournaments.append((f"LCO {year} Split 2 Playoffs", f"LCO/{year}_Season/Split_2_Playoffs"))

    # ========================================================================
    # RIFT RIVALS - MINOR REGIONS ONLY (11 Events)
    # ========================================================================
    for year in range(2017, 2020):
        tournaments.append((f"Rift Rivals {year} LAN-LAS-BR", f"Rift_Rivals/{year}_Season/LAN-LAS-BR"))

    for year in range(2017, 2020):
        tournaments.append((f"Rift Rivals {year} SEA", f"Rift_Rivals/{year}_Season/SEA"))

    for year in range(2017, 2020):
        tournaments.append((f"Rift Rivals {year} TCL-CIS", f"Rift_Rivals/{year}_Season/TCL-CIS"))

    for year in range(2017, 2019):
        tournaments.append((f"Rift Rivals {year} OCE-SEA", f"Rift_Rivals/{year}_Season/OCE-SEA"))

    # ========================================================================
    # IWC (International Wildcard) (9 Events)
    # ========================================================================
    for year in range(2013, 2016):
        tournaments.append((f"IWC {year}", f"IWC/{year}_Season/Main_Event"))
        tournaments.append((f"IWCI {year}", f"IWCI/{year}_Season/Main_Event"))

    for year in range(2014, 2017):
        tournaments.append((f"IWCQ {year}", f"IWCQ/{year}_Season/Main_Event"))

    # ========================================================================
    # REGIONAL CUPS & FINALS (18 Events)
    # ========================================================================
    # Copa Latinoamérica
    for year in range(2013, 2016):
        tournaments.append((f"Copa Latinoamérica {year}", f"Copa_Latinoamérica/{year}_Season/Main_Event"))

    # GPL Finals & Playoffs
    for year in range(2013, 2018):
        tournaments.append((f"GPL Finals {year}", f"GPL/{year}_Season/Finals"))
        tournaments.append((f"GPL Playoffs {year}", f"GPL/{year}_Season/Playoffs"))

    # TCL vs VCS
    for year in range(2015, 2020):
        tournaments.append((f"TCL vs VCS {year}", f"TCL_vs_VCS/{year}_Season/Main_Event"))

    return tournaments

def main():
    """Main test function"""
    print("=" * 80)
    print("TESTING 88 NEW MINOR REGION EVENTS")
    print("=" * 80)
    print()

    loader = LeaguepediaLoader()
    tournaments = generate_test_tournaments()

    print(f"Testing {len(tournaments)} new tournaments...")
    print()

    found_tournaments = []
    not_found_tournaments = []

    for i, (name, url) in enumerate(tournaments, 1):
        print(f"[{i}/{len(tournaments)}] ", end="")
        result = test_tournament(loader, name, url)

        if result['found']:
            found_tournaments.append(result)
        else:
            not_found_tournaments.append(result)

        time.sleep(0.1)

    results = {
        'found': found_tournaments,
        'not_found': not_found_tournaments,
        'summary': {
            'total': len(tournaments),
            'found': len(found_tournaments),
            'not_found': len(not_found_tournaments),
            'success_rate': (len(found_tournaments) / len(tournaments)) * 100
        }
    }

    output_file = Path(__file__).parent / 'new_events_test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Total tested: {len(tournaments)}")
    print(f"✅ Found: {len(found_tournaments)} ({(len(found_tournaments)/len(tournaments)*100):.1f}%)")
    print(f"❌ Not found: {len(not_found_tournaments)} ({(len(not_found_tournaments)/len(tournaments)*100):.1f}%)")
    print()
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()
