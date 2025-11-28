#!/usr/bin/env python3
"""
COMPREHENSIVE EVENT DISCOVERY
Tests multiple URL patterns for each event type until found
"""

import os
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.leaguepedia_loader import LeaguepediaLoader

def test_url_pattern(loader, name, url_with_underscores):
    """Test a single URL pattern"""
    url = url_with_underscores.replace('_', ' ')

    try:
        matches = loader._query_cargo(
            tables="MatchSchedule",
            fields="Team1,Team2",
            where=f"OverviewPage='{url}'",
            limit=5
        )

        if matches and len(matches) > 0:
            return {'found': True, 'url': url, 'matches': len(matches)}
        return {'found': False, 'url': url}
    except Exception as e:
        return {'found': False, 'url': url, 'error': str(e)}

def discover_event(loader, name, url_patterns):
    """
    Try multiple URL patterns for an event until one is found

    Args:
        loader: LeaguepediaLoader
        name: Event display name
        url_patterns: List of URL patterns to try

    Returns:
        dict: Result with found URL or None
    """
    for i, pattern in enumerate(url_patterns, 1):
        result = test_url_pattern(loader, name, pattern)
        if result['found']:
            print(f"✅ {name:60} | {result['url']}")
            return {'name': name, 'url': result['url'], 'found': True, 'matches': result['matches'], 'pattern_index': i}
        time.sleep(0.1)

    print(f"❌ {name:60} | Tested {len(url_patterns)} patterns")
    return {'name': name, 'found': False, 'patterns_tested': len(url_patterns)}

def main():
    """Main discovery function"""
    print("=" * 100)
    print("COMPREHENSIVE EVENT DISCOVERY - Testing multiple URL patterns")
    print("=" * 100)
    print()

    bot_username = os.getenv("LEAGUEPEDIA_BOT_USERNAME", "Ekwo98@Elo")
    bot_password = os.getenv("LEAGUEPEDIA_BOT_PASSWORD")

    if not bot_password:
        print("❌ LEAGUEPEDIA_BOT_PASSWORD not set!")
        return 1

    loader = LeaguepediaLoader(bot_username=bot_username, bot_password=bot_password)

    found_events = []
    not_found_events = []

    # ========================================================================
    # LAS (Latin America South) - Try different patterns
    # ========================================================================
    print("\n" + "="*100)
    print("TESTING: LAS (Latin America South)")
    print("="*100)

    for year in range(2013, 2019):
        # Opening Season
        name = f"LAS {year} Opening"
        patterns = [
            f"LAS/{year}_Season/Opening_Season",
            f"LAS/{year}/Opening",
            f"LAS_{year}/Opening",
            f"LAS/Season_{year}/Opening",
            f"LAS/{{{{year}}}}_Season/Opening_Season".replace("{{{{year}}}}", str(year)),
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

        # Opening Playoffs
        name = f"LAS {year} Opening Playoffs"
        patterns = [
            f"LAS/{year}_Season/Opening_Playoffs",
            f"LAS/{year}/Opening_Playoffs",
            f"LAS_{year}/Opening_Playoffs",
            f"LAS/Season_{year}/Opening_Playoffs",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

        # Closing Season
        name = f"LAS {year} Closing"
        patterns = [
            f"LAS/{year}_Season/Closing_Season",
            f"LAS/{year}/Closing",
            f"LAS_{year}/Closing",
            f"LAS/Season_{year}/Closing",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

        # Closing Playoffs
        name = f"LAS {year} Closing Playoffs"
        patterns = [
            f"LAS/{year}_Season/Closing_Playoffs",
            f"LAS/{year}/Closing_Playoffs",
            f"LAS_{year}/Closing_Playoffs",
            f"LAS/Season_{year}/Closing_Playoffs",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    # ========================================================================
    # RIFT RIVALS - Try different patterns
    # ========================================================================
    print("\n" + "="*100)
    print("TESTING: Rift Rivals")
    print("="*100)

    for year in range(2017, 2020):
        for region in ["LAN-LAS-BR", "SEA", "TCL-CIS"]:
            name = f"Rift Rivals {year} {region}"
            patterns = [
                f"Rift_Rivals/{year}_Season/{region}",
                f"Rift_Rivals_{year}/{region}",
                f"Rift_Rivals/{year}/{region}",
                f"RR_{year}/{region}",
                f"{year}_Rift_Rivals/{region}",
            ]
            result = discover_event(loader, name, patterns)
            (found_events if result['found'] else not_found_events).append(result)

    # OCE-SEA
    for year in range(2017, 2019):
        name = f"Rift Rivals {year} OCE-SEA"
        patterns = [
            f"Rift_Rivals/{year}_Season/OCE-SEA",
            f"Rift_Rivals_{year}/OCE-SEA",
            f"Rift_Rivals/{year}/OCE-SEA",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    # ========================================================================
    # IWC (International Wildcard)
    # ========================================================================
    print("\n" + "="*100)
    print("TESTING: IWC/IWCI/IWCQ")
    print("="*100)

    for year in range(2013, 2016):
        # IWC
        name = f"IWC {year}"
        patterns = [
            f"IWC/{year}_Season/Main_Event",
            f"IWC_{year}",
            f"IWC/{year}",
            f"{year}_IWC",
            f"International_Wildcard/{year}",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

        # IWCI
        name = f"IWCI {year}"
        patterns = [
            f"IWCI/{year}_Season/Main_Event",
            f"IWCI_{year}",
            f"IWCI/{year}",
            f"{year}_IWCI",
            f"International_Wildcard_Invitational/{year}",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    for year in range(2014, 2017):
        # IWCQ
        name = f"IWCQ {year}"
        patterns = [
            f"IWCQ/{year}_Season/Main_Event",
            f"IWCQ_{year}",
            f"IWCQ/{year}",
            f"{year}_IWCQ",
            f"International_Wildcard_Qualifier/{year}",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    # ========================================================================
    # REGIONAL CUPS
    # ========================================================================
    print("\n" + "="*100)
    print("TESTING: Regional Cups")
    print("="*100)

    # Copa Latinoamérica
    for year in range(2013, 2016):
        name = f"Copa Latinoamérica {year}"
        patterns = [
            f"Copa_Latinoamérica/{year}_Season/Main_Event",
            f"Copa_Latinoamerica/{year}_Season/Main_Event",
            f"Copa_Latinoamerica_{year}",
            f"Copa_Latinoamérica_{year}",
            f"Copa_LA/{year}",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    # GPL Finals & Playoffs
    for year in range(2013, 2018):
        # Finals
        name = f"GPL Finals {year}"
        patterns = [
            f"GPL/{year}_Season/Finals",
            f"GPL_{year}/Finals",
            f"GPL/{year}/Finals",
            f"{year}_GPL/Finals",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

        # Playoffs
        name = f"GPL Playoffs {year}"
        patterns = [
            f"GPL/{year}_Season/Playoffs",
            f"GPL_{year}/Playoffs",
            f"GPL/{year}/Playoffs",
            f"{year}_GPL/Playoffs",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    # TCL vs VCS
    for year in range(2015, 2020):
        name = f"TCL vs VCS {year}"
        patterns = [
            f"TCL_vs_VCS/{year}_Season/Main_Event",
            f"TCL_vs_VCS_{year}",
            f"TCL_vs_VCS/{year}",
            f"{year}_TCL_vs_VCS",
        ]
        result = discover_event(loader, name, patterns)
        (found_events if result['found'] else not_found_events).append(result)

    # Save results
    results = {
        'found': found_events,
        'not_found': not_found_events,
        'summary': {
            'total': len(found_events) + len(not_found_events),
            'found': len(found_events),
            'not_found': len(not_found_events),
            'success_rate': (len(found_events) / (len(found_events) + len(not_found_events))) * 100 if (len(found_events) + len(not_found_events)) > 0 else 0
        }
    }

    output_file = Path(__file__).parent / 'comprehensive_discovery_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "="*100)
    print("DISCOVERY COMPLETE")
    print("="*100)
    print(f"Total events: {results['summary']['total']}")
    print(f"✅ Found: {results['summary']['found']} ({results['summary']['success_rate']:.1f}%)")
    print(f"❌ Not found: {results['summary']['not_found']}")
    print(f"\nResults saved to: {output_file}")

    return 0

if __name__ == "__main__":
    exit(main())
