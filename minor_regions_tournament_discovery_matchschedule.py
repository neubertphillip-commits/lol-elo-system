#!/usr/bin/env python3
"""
MINOR REGIONS TOURNAMENT DISCOVERY - MatchSchedule Edition
Testet Minor Region Turniere in der MatchSchedule Tabelle

WICHTIG: Verwendet SPACES in URLs (nicht Underscores)!
Beispiel: "LJL/2020 Season/Spring Season" (nicht "LJL/2020_Season/Spring_Season")
"""

import os
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.leaguepedia_loader import LeaguepediaLoader

def test_tournament(loader, name, url_with_underscores):
    """
    Test if tournament exists in MatchSchedule table

    Args:
        loader: LeaguepediaLoader instance
        name: Tournament display name
        url_with_underscores: URL with underscores (will be converted to spaces)

    Returns:
        dict: Result with name, url, found status, match count
    """
    # Convert underscores to spaces for MatchSchedule
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
            return {
                'name': name,
                'url': url,
                'found': True,
                'sample_matches': len(matches)
            }
        else:
            print(f"❌ {name:70} NOT FOUND")
            return {
                'name': name,
                'url': url,
                'found': False
            }

    except Exception as e:
        print(f"❌ {name:70} ERROR: {e}")
        return {
            'name': name,
            'url': url,
            'found': False,
            'error': str(e)
        }

def generate_all_tournaments():
    """
    Generate comprehensive list of ALL Minor Region tournaments based on Leaguepedia data

    Returns:
        list: List of (name, url) tuples
    """
    tournaments = []

    # ========================================================================
    # CBLOL (Brazil) - 2014-2024
    # ========================================================================
    # CBLOL 2014 - Special structure
    tournaments.append(("CBLOL 2014 Champions Series", "CBLOL/2014_Season/Champions_Series"))
    tournaments.append(("CBLOL 2014 Champions Series Playoffs", "CBLOL/2014_Season/Champions_Series_Playoffs"))

    # CBLOL 2015 - Has Post-Season
    tournaments.append(("CBLOL 2015 Split 1", "CBLOL/2015_Season/Split_1"))
    tournaments.append(("CBLOL 2015 Split 1 Playoffs", "CBLOL/2015_Season/Split_1_Playoffs"))
    tournaments.append(("CBLOL 2015 Split 2", "CBLOL/2015_Season/Split_2"))
    tournaments.append(("CBLOL 2015 Split 2 Playoffs", "CBLOL/2015_Season/Split_2_Playoffs"))
    tournaments.append(("CBLOL 2015 Post-Season", "CBLOL/2015_Season/Post-Season"))

    # CBLOL 2016-2024 - Standard structure with Playoffs
    for year in range(2016, 2025):
        tournaments.append((f"CBLOL {year} Split 1", f"CBLOL/{year}_Season/Split_1"))
        tournaments.append((f"CBLOL {year} Split 1 Playoffs", f"CBLOL/{year}_Season/Split_1_Playoffs"))
        tournaments.append((f"CBLOL {year} Split 2", f"CBLOL/{year}_Season/Split_2"))
        tournaments.append((f"CBLOL {year} Split 2 Playoffs", f"CBLOL/{year}_Season/Split_2_Playoffs"))

    # ========================================================================
    # PCS (Pacific) - 2020-2025
    # ========================================================================
    # PCS 2020-2024 - Standard Spring/Summer structure
    for year in range(2020, 2025):
        tournaments.append((f"PCS {year} Spring", f"PCS/{year}_Season/Spring_Season"))
        tournaments.append((f"PCS {year} Spring Playoffs", f"PCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"PCS {year} Summer", f"PCS/{year}_Season/Summer_Season"))
        tournaments.append((f"PCS {year} Summer Playoffs", f"PCS/{year}_Season/Summer_Playoffs"))

    # PCS 2025 - Three splits structure
    tournaments.append(("PCS 2025 Split 1", "PCS/2025_Season/Split_1"))
    tournaments.append(("PCS 2025 Split 1 Playoffs", "PCS/2025_Season/Split_1_Playoffs"))
    tournaments.append(("PCS 2025 Split 2", "PCS/2025_Season/Split_2"))
    tournaments.append(("PCS 2025 Split 2 Playoffs", "PCS/2025_Season/Split_2_Playoffs"))
    tournaments.append(("PCS 2025 Split 3", "PCS/2025_Season/Split_3"))
    tournaments.append(("PCS 2025 Split 3 Playoffs", "PCS/2025_Season/Split_3_Playoffs"))

    # ========================================================================
    # LMS (Taiwan, predecessor to PCS) - 2015-2019
    # ========================================================================
    for year in range(2015, 2020):
        tournaments.append((f"LMS {year} Spring", f"LMS/{year}_Season/Spring_Season"))
        tournaments.append((f"LMS {year} Spring Playoffs", f"LMS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LMS {year} Summer", f"LMS/{year}_Season/Summer_Season"))
        tournaments.append((f"LMS {year} Summer Playoffs", f"LMS/{year}_Season/Summer_Playoffs"))
        tournaments.append((f"LMS {year} Regional Finals", f"LMS/{year}_Season/Regional_Finals"))

    # ========================================================================
    # VCS (Vietnam) - 2013-2025
    # ========================================================================
    # VCS 2025 - New structure
    tournaments.append(("VCS 2025 Spring", "VCS/2025_Season/Spring_Season"))
    tournaments.append(("VCS 2025 Summer", "VCS/2025_Season/Summer_Season"))
    tournaments.append(("VCS 2025 Finals", "VCS/2025_Season/Finals"))

    # VCS 2024-2022 - Standard structure
    for year in range(2022, 2025):
        tournaments.append((f"VCS {year} Spring", f"VCS/{year}_Season/Spring_Season"))
        tournaments.append((f"VCS {year} Spring Playoffs", f"VCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"VCS {year} Summer", f"VCS/{year}_Season/Summer_Season"))
        tournaments.append((f"VCS {year} Summer Playoffs", f"VCS/{year}_Season/Summer_Playoffs"))

    # VCS 2021 - Has Winter split, Summer cancelled
    tournaments.append(("VCS 2021 Spring", "VCS/2021_Season/Spring_Season"))
    tournaments.append(("VCS 2021 Spring Playoffs", "VCS/2021_Season/Spring_Playoffs"))
    tournaments.append(("VCS 2021 Winter", "VCS/2021_Season/Winter_Season"))
    tournaments.append(("VCS 2021 Winter Playoffs", "VCS/2021_Season/Winter_Playoffs"))

    # VCS 2020-2018 - Standard structure
    for year in range(2018, 2021):
        tournaments.append((f"VCS {year} Spring", f"VCS/{year}_Season/Spring_Season"))
        tournaments.append((f"VCS {year} Spring Playoffs", f"VCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"VCS {year} Summer", f"VCS/{year}_Season/Summer_Season"))
        tournaments.append((f"VCS {year} Summer Playoffs", f"VCS/{year}_Season/Summer_Playoffs"))

    # VCS A 2017 - Different name
    tournaments.append(("VCS A 2017 Spring", "VCS_A/2017_Season/Spring_Season"))
    tournaments.append(("VCS A 2017 Spring Playoffs", "VCS_A/2017_Season/Spring_Playoffs"))
    tournaments.append(("VCS A 2017 Summer", "VCS_A/2017_Season/Summer_Season"))
    tournaments.append(("VCS A 2017 Summer Playoffs", "VCS_A/2017_Season/Summer_Playoffs"))

    # 2016 - Multiple name changes (MDCS, Coca-Cola Championship Series)
    tournaments.append(("MDCS 2016 Summer", "MDCS/2016_Season/Summer_Season"))
    tournaments.append(("MDCS 2016 Summer Playoffs", "MDCS/2016_Season/Summer_Playoffs"))
    tournaments.append(("Coca-Cola Championship Series 2016 Spring", "Coca-Cola_Championship_Series/2016_Season/Spring_Season"))
    tournaments.append(("Coca-Cola Championship Series 2016 Spring Playoffs", "Coca-Cola_Championship_Series/2016_Season/Spring_Playoffs"))

    # VCS A 2015-2013
    tournaments.append(("VCS A 2015 Spring", "VCS_A/2015_Season/Spring_Season"))
    tournaments.append(("VCS A 2015 Summer", "VCS_A/2015_Season/Summer_Season"))
    tournaments.append(("VCS A 2014 Spring", "VCS_A/2014_Season/Spring_Season"))
    tournaments.append(("VCS A 2014 Summer", "VCS_A/2014_Season/Summer_Season"))
    tournaments.append(("VCS A 2013 Winter", "VCS_A/2013_Season/Winter_Season"))

    # ========================================================================
    # LJL (Japan) - 2014-2025
    # ========================================================================
    # LJL 2025 - New structure
    tournaments.append(("LJL 2025 Forge", "LJL/2025_Season/Forge"))
    tournaments.append(("LJL 2025 Storm", "LJL/2025_Season/Storm"))
    tournaments.append(("LJL 2025 Ignite", "LJL/2025_Season/Ignite"))
    tournaments.append(("LJL 2025 Finals", "LJL/2025_Season/Finals"))

    # LJL 2024-2016 - Standard structure
    for year in range(2016, 2025):
        tournaments.append((f"LJL {year} Spring", f"LJL/{year}_Season/Spring_Season"))
        tournaments.append((f"LJL {year} Spring Playoffs", f"LJL/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LJL {year} Summer", f"LJL/{year}_Season/Summer_Season"))
        tournaments.append((f"LJL {year} Summer Playoffs", f"LJL/{year}_Season/Summer_Playoffs"))

    # LJL 2015 - Different structure
    tournaments.append(("LJL 2015 Season 1", "LJL/2015_Season/Season_1"))
    tournaments.append(("LJL 2015 Season 2", "LJL/2015_Season/Season_2"))
    tournaments.append(("LJL 2015 Grand Finals", "LJL/2015_Season/Grand_Finals"))

    # LJL 2014 - Has Winter split
    tournaments.append(("LJL 2014 Winter", "LJL/2014_Season/Winter_Season"))
    tournaments.append(("LJL 2014 Spring", "LJL/2014_Season/Spring_Season"))
    tournaments.append(("LJL 2014 Summer", "LJL/2014_Season/Summer_Season"))
    tournaments.append(("LJL 2014 Grand Finals", "LJL/2014_Season/Grand_Finals"))

    # ========================================================================
    # TCL (Turkey) - 2014-2025
    # ========================================================================
    # TCL 2025 - Has Spring split
    tournaments.append(("TCL 2025 Spring", "TCL/2025_Season/Spring_Season"))
    tournaments.append(("TCL 2025 Spring Playoffs", "TCL/2025_Season/Spring_Playoffs"))
    tournaments.append(("TCL 2025 Winter", "TCL/2025_Season/Winter_Season"))
    tournaments.append(("TCL 2025 Winter Playoffs", "TCL/2025_Season/Winter_Playoffs"))
    tournaments.append(("TCL 2025 Summer", "TCL/2025_Season/Summer_Season"))
    tournaments.append(("TCL 2025 Summer Playoffs", "TCL/2025_Season/Summer_Playoffs"))

    # TCL 2024-2015 - Standard Winter/Summer structure
    for year in range(2015, 2025):
        tournaments.append((f"TCL {year} Winter", f"TCL/{year}_Season/Winter_Season"))
        tournaments.append((f"TCL {year} Winter Playoffs", f"TCL/{year}_Season/Winter_Playoffs"))
        tournaments.append((f"TCL {year} Summer", f"TCL/{year}_Season/Summer_Season"))
        tournaments.append((f"TCL {year} Summer Playoffs", f"TCL/{year}_Season/Summer_Playoffs"))

    # TCL 2014 - Has all 3 splits
    tournaments.append(("TCL 2014 Winter", "TCL/2014_Season/Winter_Season"))
    tournaments.append(("TCL 2014 Winter Playoffs", "TCL/2014_Season/Winter_Playoffs"))
    tournaments.append(("TCL 2014 Spring", "TCL/2014_Season/Spring_Season"))
    tournaments.append(("TCL 2014 Spring Playoffs", "TCL/2014_Season/Spring_Playoffs"))
    tournaments.append(("TCL 2014 Summer", "TCL/2014_Season/Summer_Season"))
    tournaments.append(("TCL 2014 Summer Playoffs", "TCL/2014_Season/Summer_Playoffs"))

    # ========================================================================
    # LLA (Latin America) - 2019-2024
    # ========================================================================
    for year in range(2019, 2025):
        tournaments.append((f"LLA {year} Opening", f"LLA/{year}_Season/Opening_Season"))
        tournaments.append((f"LLA {year} Opening Playoffs", f"LLA/{year}_Season/Opening_Playoffs"))
        tournaments.append((f"LLA {year} Closing", f"LLA/{year}_Season/Closing_Season"))
        tournaments.append((f"LLA {year} Closing Playoffs", f"LLA/{year}_Season/Closing_Playoffs"))

    # ========================================================================
    # LLN (Latin America North, predecessor to LLA) - 2017-2018
    # ========================================================================
    for year in range(2017, 2019):
        tournaments.append((f"LLN {year} Opening", f"LLN/{year}_Season/Opening_Season"))
        tournaments.append((f"LLN {year} Opening Playoffs", f"LLN/{year}_Season/Opening_Playoffs"))
        tournaments.append((f"LLN {year} Closing", f"LLN/{year}_Season/Closing_Season"))
        tournaments.append((f"LLN {year} Closing Playoffs", f"LLN/{year}_Season/Closing_Playoffs"))

    # ========================================================================
    # LAN (Latin America North, predecessor to LLN) - 2015-2016
    # ========================================================================
    for year in range(2015, 2017):
        tournaments.append((f"LAN {year} Opening Cup", f"LAN/{year}_Season/Opening_Cup"))
        tournaments.append((f"LAN {year} Opening Cup Playoffs", f"LAN/{year}_Season/Opening_Cup_Playoffs"))
        tournaments.append((f"LAN {year} Closing Cup", f"LAN/{year}_Season/Closing_Cup"))
        tournaments.append((f"LAN {year} Closing Cup Playoffs", f"LAN/{year}_Season/Closing_Cup_Playoffs"))

    # ========================================================================
    # OPL (Oceania) - 2015-2020
    # ========================================================================
    for year in range(2015, 2021):
        tournaments.append((f"OPL {year} Split 1", f"OPL/{year}_Season/Split_1"))
        tournaments.append((f"OPL {year} Split 1 Playoffs", f"OPL/{year}_Season/Split_1_Playoffs"))
        tournaments.append((f"OPL {year} Split 2", f"OPL/{year}_Season/Split_2"))
        tournaments.append((f"OPL {year} Split 2 Playoffs", f"OPL/{year}_Season/Split_2_Playoffs"))

    # ========================================================================
    # LCL (Russia/CIS) - 2016-2021
    # ========================================================================
    for year in range(2016, 2022):
        tournaments.append((f"LCL {year} Spring", f"LCL/{year}_Season/Spring_Season"))
        tournaments.append((f"LCL {year} Spring Playoffs", f"LCL/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LCL {year} Summer", f"LCL/{year}_Season/Summer_Season"))
        tournaments.append((f"LCL {year} Summer Playoffs", f"LCL/{year}_Season/Summer_Playoffs"))

    # ========================================================================
    # GPL (Garena Premier League, Southeast Asia) - 2012-2018
    # ========================================================================
    tournaments.append(("GPL 2018 Spring", "GPL/2018_Season/Spring_Season"))
    tournaments.append(("GPL 2017 Spring", "GPL/2017_Season/Spring_Season"))
    tournaments.append(("GPL 2017 Summer", "GPL/2017_Season/Summer_Season"))
    tournaments.append(("GPL 2016 Spring", "GPL/2016_Season/Spring_Season"))
    tournaments.append(("GPL 2016 Summer", "GPL/2016_Season/Summer_Season"))
    tournaments.append(("GPL 2015 Spring", "GPL/2015_Season/Spring_Season"))
    tournaments.append(("GPL 2015 Spring Playoffs", "GPL/2015_Season/Spring_Playoffs"))
    tournaments.append(("GPL 2015 Summer", "GPL/2015_Season/Summer_Season"))
    tournaments.append(("GPL 2015 Summer Playoffs", "GPL/2015_Season/Summer_Playoffs"))
    tournaments.append(("GPL 2014 Winter", "GPL/2014_Season/Winter_Season"))
    tournaments.append(("GPL 2014 Spring", "GPL/2014_Season/Spring_Season"))
    tournaments.append(("GPL 2014 Summer", "GPL/2014_Season/Summer_Season"))
    tournaments.append(("GPL 2013 Spring", "GPL/2013_Season/Spring_Season"))
    tournaments.append(("GPL 2013 Summer", "GPL/2013_Season/Summer_Season"))
    tournaments.append(("GPL 2013 Championship", "GPL/2013_Season/Championship"))
    tournaments.append(("GPL 2012 Season 1", "GPL/2012_Season/Season_1"))
    tournaments.append(("GPL 2012 Season 1 Playoffs", "GPL/2012_Season/Season_1_Playoffs"))
    tournaments.append(("GPL 2012 Opening Event", "GPL/2012_Season/Opening_Event"))

    return tournaments

def main():
    """Main function to test all tournaments"""
    print("=" * 80)
    print("MINOR REGIONS TOURNAMENT DISCOVERY TEST")
    print("=" * 80)
    print()

    # Initialize loader with bot credentials
    loader = LeaguepediaLoader()

    # Generate all tournaments
    tournaments = generate_all_tournaments()

    print(f"Testing {len(tournaments)} tournaments...")
    print()

    # Test each tournament
    found_tournaments = []
    not_found_tournaments = []

    for i, (name, url) in enumerate(tournaments, 1):
        print(f"[{i}/{len(tournaments)}] ", end="")
        result = test_tournament(loader, name, url)

        if result['found']:
            found_tournaments.append(result)
        else:
            not_found_tournaments.append(result)

        # Small delay to avoid overwhelming the API
        time.sleep(0.1)

    # Save results
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

    output_file = Path(__file__).parent / 'minor_regions_discovery_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total tournaments tested: {len(tournaments)}")
    print(f"✅ Found: {len(found_tournaments)} ({(len(found_tournaments)/len(tournaments)*100):.1f}%)")
    print(f"❌ Not found: {len(not_found_tournaments)} ({(len(not_found_tournaments)/len(tournaments)*100):.1f}%)")
    print()
    print(f"Results saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()
