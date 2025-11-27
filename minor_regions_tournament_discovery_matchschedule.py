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
            print(f"✅ {name:70} {len(matches)} matches (sample)")
            return {
                'name': name,
                'url': url,  # Save with SPACES
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
    Generate comprehensive list of ALL Minor Region tournaments

    Returns:
        list: List of (name, url) tuples
    """
    tournaments = []

    # ========================================================================
    # CBLOL (Brazil) - 2015-2025
    # ========================================================================
    for year in range(2015, 2026):
        tournaments.append((f"CBLOL {year} Split 1", f"CBLOL/{year}_Season/Split_1"))
        tournaments.append((f"CBLOL {year} Split 2", f"CBLOL/{year}_Season/Split_2"))
        # CBLOL Playoffs and Regional Finals - NOT IN MATCHSCHEDULE

    # ========================================================================
    # PCS (Pacific) - 2020-2025
    # ========================================================================
    for year in range(2020, 2025):
        tournaments.append((f"PCS {year} Spring", f"PCS/{year}_Season/Spring_Season"))
        tournaments.append((f"PCS {year} Spring Playoffs", f"PCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"PCS {year} Summer", f"PCS/{year}_Season/Summer_Season"))
        tournaments.append((f"PCS {year} Summer Playoffs", f"PCS/{year}_Season/Summer_Playoffs"))
        tournaments.append((f"PCS {year} Regional Finals", f"PCS/{year}_Season/Regional_Finals"))

    # PCS 2025: New 3-split structure
    tournaments.append(("PCS 2025 Spring", "PCS/2025_Season/Spring_Season"))
    tournaments.append(("PCS 2025 Spring Playoffs", "PCS/2025_Season/Spring_Playoffs"))
    tournaments.append(("PCS 2025 Summer", "PCS/2025_Season/Summer_Season"))
    tournaments.append(("PCS 2025 Summer Playoffs", "PCS/2025_Season/Summer_Playoffs"))
    tournaments.append(("PCS 2025 Split 3", "PCS/2025_Season/Split_3"))
    tournaments.append(("PCS 2025 Split 3 Playoffs", "PCS/2025_Season/Split_3_Playoffs"))
    tournaments.append(("PCS 2025 Regional Finals", "PCS/2025_Season/Regional_Finals"))

    # LMS (Taiwan, predecessor to PCS) - 2015-2019
    for year in range(2015, 2020):
        tournaments.append((f"LMS {year} Spring", f"LMS/{year}_Season/Spring_Season"))
        tournaments.append((f"LMS {year} Spring Playoffs", f"LMS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LMS {year} Summer", f"LMS/{year}_Season/Summer_Season"))
        tournaments.append((f"LMS {year} Summer Playoffs", f"LMS/{year}_Season/Summer_Playoffs"))
        if year >= 2015:
            tournaments.append((f"LMS {year} Regional Finals", f"LMS/{year}_Season/Regional_Finals"))

    # ========================================================================
    # VCS (Vietnam) - 2018-2025 (started in 2018, not 2017)
    # ========================================================================
    for year in range(2018, 2026):
        tournaments.append((f"VCS {year} Spring", f"VCS/{year}_Season/Spring_Season"))
        tournaments.append((f"VCS {year} Spring Playoffs", f"VCS/{year}_Season/Spring_Playoffs"))

        # VCS 2021 Summer was cancelled due to COVID
        if year != 2021:
            tournaments.append((f"VCS {year} Summer", f"VCS/{year}_Season/Summer_Season"))
            tournaments.append((f"VCS {year} Summer Playoffs", f"VCS/{year}_Season/Summer_Playoffs"))

        if year >= 2020:
            tournaments.append((f"VCS {year} Regional Finals", f"VCS/{year}_Season/Regional_Finals"))

    # ========================================================================
    # LJL (Japan) - 2014, 2016-2025 (2015 not in MatchSchedule)
    # ========================================================================
    # LJL 2014 (no playoffs)
    tournaments.append(("LJL 2014 Spring", "LJL/2014_Season/Spring_Season"))
    tournaments.append(("LJL 2014 Summer", "LJL/2014_Season/Summer_Season"))

    # LJL 2016-2024 (with playoffs)
    for year in range(2016, 2025):
        tournaments.append((f"LJL {year} Spring", f"LJL/{year}_Season/Spring_Season"))
        tournaments.append((f"LJL {year} Spring Playoffs", f"LJL/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LJL {year} Summer", f"LJL/{year}_Season/Summer_Season"))
        tournaments.append((f"LJL {year} Summer Playoffs", f"LJL/{year}_Season/Summer_Playoffs"))
        if year >= 2020:
            tournaments.append((f"LJL {year} Regional Finals", f"LJL/{year}_Season/Regional_Finals"))

    # LJL 2025: New structure (Forge, Storm, Ignite, Finals)
    tournaments.append(("LJL 2025 Forge", "LJL/2025_Season/Forge"))
    tournaments.append(("LJL 2025 Storm", "LJL/2025_Season/Storm"))
    tournaments.append(("LJL 2025 Ignite", "LJL/2025_Season/Ignite"))
    tournaments.append(("LJL 2025 Finals", "LJL/2025_Season/Finals"))

    # ========================================================================
    # TCL (Turkey) - 2015-2025 (started in 2015, not 2013)
    # ========================================================================
    for year in range(2015, 2025):
        tournaments.append((f"TCL {year} Winter", f"TCL/{year}_Season/Winter_Season"))
        tournaments.append((f"TCL {year} Winter Playoffs", f"TCL/{year}_Season/Winter_Playoffs"))
        tournaments.append((f"TCL {year} Summer", f"TCL/{year}_Season/Summer_Season"))
        tournaments.append((f"TCL {year} Summer Playoffs", f"TCL/{year}_Season/Summer_Playoffs"))
        if year >= 2020:
            tournaments.append((f"TCL {year} Regional Finals", f"TCL/{year}_Season/Regional_Finals"))

    # TCL 2025: Added Spring split
    tournaments.append(("TCL 2025 Spring", "TCL/2025_Season/Spring_Season"))
    tournaments.append(("TCL 2025 Spring Playoffs", "TCL/2025_Season/Spring_Playoffs"))
    tournaments.append(("TCL 2025 Winter", "TCL/2025_Season/Winter_Season"))
    tournaments.append(("TCL 2025 Winter Playoffs", "TCL/2025_Season/Winter_Playoffs"))
    tournaments.append(("TCL 2025 Summer", "TCL/2025_Season/Summer_Season"))
    tournaments.append(("TCL 2025 Summer Playoffs", "TCL/2025_Season/Summer_Playoffs"))
    tournaments.append(("TCL 2025 Regional Finals", "TCL/2025_Season/Regional_Finals"))

    # ========================================================================
    # LLA (Latin America) - 2019-2025
    # ========================================================================
    for year in range(2019, 2026):
        tournaments.append((f"LLA {year} Opening", f"LLA/{year}_Season/Opening_Season"))
        tournaments.append((f"LLA {year} Opening Playoffs", f"LLA/{year}_Season/Opening_Playoffs"))
        tournaments.append((f"LLA {year} Closing", f"LLA/{year}_Season/Closing_Season"))
        tournaments.append((f"LLA {year} Closing Playoffs", f"LLA/{year}_Season/Closing_Playoffs"))
        if year >= 2020:
            tournaments.append((f"LLA {year} Regional Finals", f"LLA/{year}_Season/Regional_Finals"))

    # LLN (predecessor to LLA) - 2017-2018 only (2014-2016 not in MatchSchedule)
    for year in range(2017, 2019):
        tournaments.append((f"LLN {year} Opening", f"LLN/{year}_Season/Opening_Season"))
        tournaments.append((f"LLN {year} Closing", f"LLN/{year}_Season/Closing_Season"))

    # ========================================================================
    # Historical Regions
    # ========================================================================
    # GPL (Southeast Asia) - NOT IN MATCHSCHEDULE, REMOVED

    # OPL (Oceania) - 2015-2020
    for year in range(2015, 2021):
        tournaments.append((f"OPL {year} Split 1", f"OPL/{year}_Season/Split_1"))
        tournaments.append((f"OPL {year} Split 2", f"OPL/{year}_Season/Split_2"))

    # LCL (Russia) - NOT IN MATCHSCHEDULE, REMOVED

    return tournaments

def main():
    """Main discovery function"""
    print("=" * 80)
    print("MINOR REGIONS TOURNAMENT DISCOVERY - MatchSchedule Edition")
    print("=" * 80)

    # Get credentials from environment
    bot_username = os.getenv("LEAGUEPEDIA_BOT_USERNAME")
    bot_password = os.getenv("LEAGUEPEDIA_BOT_PASSWORD")

    if not bot_username or not bot_password:
        print("ERROR: Missing credentials!")
        print("Set LEAGUEPEDIA_BOT_USERNAME and LEAGUEPEDIA_BOT_PASSWORD")
        return

    # Initialize loader
    loader = LeaguepediaLoader(bot_username, bot_password)
    print(f"\n✅ Authenticated as {bot_username}\n")

    # Generate all tournaments
    tournaments = generate_all_tournaments()
    print(f"Testing {len(tournaments)} minor region tournaments...\n")

    # Test each tournament
    results = []
    for i, (name, url) in enumerate(tournaments, 1):
        print(f"[{i}/{len(tournaments)}] ", end="")
        result = test_tournament(loader, name, url)
        results.append(result)
        time.sleep(0.1)  # Rate limiting

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    found = [r for r in results if r['found']]
    not_found = [r for r in results if not r['found']]

    print(f"✅ Found: {len(found)}")
    print(f"❌ Not Found: {len(not_found)}")
    print(f"📊 Total: {len(results)}")
    print(f"🎯 Success Rate: {len(found)/len(results)*100:.1f}%")

    # Save results
    output_file = "minor_regions_discovery_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            'found': found,
            'not_found': not_found,
            'summary': {
                'total': len(results),
                'found': len(found),
                'not_found': len(not_found),
                'success_rate': len(found)/len(results)*100
            }
        }, f, indent=2)

    print(f"\n💾 Results saved to {output_file}")

if __name__ == "__main__":
    main()
