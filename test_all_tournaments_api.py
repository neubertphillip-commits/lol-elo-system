#!/usr/bin/env python3
"""
Test all tournaments to see which have data in Leaguepedia API
Tests one game per tournament/stage to validate data availability
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://lol.fandom.com/api.php"
DELAY = 10  # seconds between requests

def test_tournament(tournament_name, overview_page, category="Unknown"):
    """Test if tournament data exists"""
    params = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'ScoreboardGames',
        'fields': 'Team1,Team2,Winner,DateTime_UTC,OverviewPage,GameId',
        'where': f"OverviewPage='{overview_page}'",
        'limit': '1'
    }

    try:
        print(f"\n[TEST] {tournament_name}")
        print(f"  Path: {overview_page}")

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Check for errors
        if 'error' in data:
            error_code = data['error'].get('code', 'unknown')
            error_info = data['error'].get('info', 'no info')
            print(f"  ❌ ERROR: {error_code} - {error_info}")
            return {
                'category': category,
                'name': tournament_name,
                'path': overview_page,
                'status': 'ERROR',
                'error': f"{error_code}: {error_info}"
            }

        # Check for data
        if 'cargoquery' in data and len(data['cargoquery']) > 0:
            game = data['cargoquery'][0]['title']
            sample = f"{game.get('Team1', 'N/A')} vs {game.get('Team2', 'N/A')}"
            date = game.get('DateTime UTC', 'N/A')
            game_id = game.get('GameId', 'N/A')

            print(f"  ✅ SUCCESS")
            print(f"     Sample: {sample}")
            print(f"     Date: {date}")
            print(f"     GameId: {game_id}")

            return {
                'category': category,
                'name': tournament_name,
                'path': overview_page,
                'status': 'SUCCESS',
                'sample': sample,
                'date': date,
                'game_id': game_id
            }
        else:
            print(f"  ⚠️  NO_DATA (no matches found)")
            return {
                'category': category,
                'name': tournament_name,
                'path': overview_page,
                'status': 'NO_DATA'
            }

    except Exception as e:
        print(f"  ❌ EXCEPTION: {e}")
        return {
            'category': category,
            'name': tournament_name,
            'path': overview_page,
            'status': 'EXCEPTION',
            'error': str(e)
        }

def main():
    results = []
    start_time = datetime.now()

    print("="*80)
    print("LEAGUEPEDIA API TOURNAMENT DATA AVAILABILITY TEST")
    print("="*80)
    print(f"Start time: {start_time}")
    print(f"Delay between requests: {DELAY}s")
    print("="*80)

    # ==================================================================
    # INTERNATIONAL TOURNAMENTS
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: WORLD CHAMPIONSHIP")
    print("="*80)

    worlds_tests = [
        ("Worlds 2024 - Play-In", "2024 Season World Championship/Play-In"),
        ("Worlds 2024 - Swiss Stage", "2024 Season World Championship/Swiss Stage"),
        ("Worlds 2024 - Knockout", "2024 Season World Championship/Knockout Stage"),
        ("Worlds 2023 - Play-In", "2023 Season World Championship/Play-In"),
        ("Worlds 2023 - Main Event", "2023 Season World Championship/Main Event"),
        ("Worlds 2023 - Knockout", "2023 Season World Championship/Knockout Stage"),
        ("Worlds 2020 - Play-In", "2020 Season World Championship/Play-In"),
        ("Worlds 2020 - Main Event", "2020 Season World Championship/Main Event"),
        ("Worlds 2017 - Play-In", "2017 Season World Championship/Play-In"),
        ("Worlds 2017 - Group Stage", "2017 Season World Championship/Group Stage"),
        ("Worlds 2016 - Group Stage", "2016 Season World Championship/Group Stage"),
        ("Worlds 2015 - Group Stage", "2015 Season World Championship/Group Stage"),
        ("Worlds 2014", "2014 Season World Championship"),
        ("Worlds 2013", "Season 3 World Championship"),
    ]

    for name, path in worlds_tests:
        result = test_tournament(name, path, "Worlds")
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    print("\n" + "="*80)
    print("TESTING: MID-SEASON INVITATIONAL")
    print("="*80)

    msi_tests = [
        ("MSI 2024 - Play-In", "2024 Mid-Season Invitational/Play-In"),
        ("MSI 2024 - Bracket", "2024 Mid-Season Invitational/Bracket Stage"),
        ("MSI 2023 - Play-In", "2023 Mid-Season Invitational/Play-In"),
        ("MSI 2023 - Main Event", "2023 Mid-Season Invitational/Main Event"),
        ("MSI 2021", "2021 Mid-Season Invitational"),
        ("MSI 2019 - Play-In", "2019 Mid-Season Invitational/Play-In"),
        ("MSI 2019 - Main Event", "2019 Mid-Season Invitational/Main Event"),
        ("MSI 2017 - Play-In", "2017 Mid-Season Invitational/Play-In"),
        ("MSI 2017 - Main Event", "2017 Mid-Season Invitational/Main Event"),
        ("MSI 2015", "2015 Mid-Season Invitational"),
    ]

    for name, path in msi_tests:
        result = test_tournament(name, path, "MSI")
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # REGIONAL LEAGUES - LEC/EU LCS
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LEC / EU LCS (EUROPE)")
    print("="*80)

    lec_tests = [
        # LEC (2019+)
        ("LEC 2024 Winter Season", "LEC/2024 Season/Winter Season"),
        ("LEC 2024 Winter Playoffs", "LEC/2024 Season/Winter Playoffs"),
        ("LEC 2024 Spring Season", "LEC/2024 Season/Spring Season"),
        ("LEC 2024 Spring Playoffs", "LEC/2024 Season/Spring Playoffs"),
        ("LEC 2023 Spring Season", "LEC/2023 Season/Spring Season"),
        ("LEC 2023 Spring Playoffs", "LEC/2023 Season/Spring Playoffs"),
        ("LEC 2020 Spring Season", "LEC/2020 Season/Spring Season"),
        ("LEC 2019 Spring Season", "LEC/2019 Season/Spring Season"),
        # EU LCS (pre-2019)
        ("EU LCS 2018 Spring Season", "EU LCS/2018 Season/Spring Season"),
        ("EU LCS 2018 Spring Playoffs", "EU LCS/2018 Season/Spring Playoffs"),
        ("EU LCS 2017 Summer Season", "EU LCS/2017 Season/Summer Season"),
        ("EU LCS 2015 Spring Season", "EU LCS/2015 Season/Spring Season"),
        ("EU LCS 2014 Spring Season", "EU LCS/2014 Season/Spring Season"),
        ("EU LCS 2013 Summer (Season 3)", "EU LCS/Season 3/Summer Season"),
        ("EU LCS 2013 Spring (Season 3)", "EU LCS/Season 3/Spring Season"),
    ]

    for name, path in lec_tests:
        result = test_tournament(name, path, "LEC/EU LCS")
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # REGIONAL LEAGUES - LCS/NA LCS
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LCS / NA LCS (NORTH AMERICA)")
    print("="*80)

    lcs_tests = [
        # LCS (2019+)
        ("LCS 2024 Spring Season", "LCS/2024 Season/Spring Season"),
        ("LCS 2024 Spring Playoffs", "LCS/2024 Season/Spring Playoffs"),
        ("LCS 2023 Summer Season", "LCS/2023 Season/Summer Season"),
        ("LCS 2020 Spring Season", "LCS/2020 Season/Spring Season"),
        ("LCS 2019 Summer Season", "LCS/2019 Season/Summer Season"),
        # NA LCS (pre-2019)
        ("NA LCS 2018 Spring Season", "NA LCS/2018 Season/Spring Season"),
        ("NA LCS 2018 Spring Playoffs", "NA LCS/2018 Season/Spring Playoffs"),
        ("NA LCS 2017 Summer Season", "NA LCS/2017 Season/Summer Season"),
        ("NA LCS 2015 Spring Season", "NA LCS/2015 Season/Spring Season"),
        ("NA LCS 2014 Spring Season", "NA LCS/2014 Season/Spring Season"),
        ("NA LCS 2013 Summer (Season 3)", "NA LCS/Season 3/Summer Season"),
        ("NA LCS 2013 Spring (Season 3)", "NA LCS/Season 3/Spring Season"),
    ]

    for name, path in lcs_tests:
        result = test_tournament(name, path, "LCS/NA LCS")
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # REGIONAL LEAGUES - LCK/CHAMPIONS
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LCK / CHAMPIONS (KOREA)")
    print("="*80)

    lck_tests = [
        # LCK (2015+)
        ("LCK 2024 Spring Season", "LCK/2024 Season/Spring Season"),
        ("LCK 2024 Spring Playoffs", "LCK/2024 Season/Spring Playoffs"),
        ("LCK 2024 Summer Season", "LCK/2024 Season/Summer Season"),
        ("LCK 2023 Spring Season", "LCK/2023 Season/Spring Season"),
        ("LCK 2020 Spring Season", "LCK/2020 Season/Spring Season"),
        ("LCK 2019 Summer Season", "LCK/2019 Season/Summer Season"),
        ("LCK 2018 Spring Season", "LCK/2018 Season/Spring Season"),
        ("LCK 2017 Summer Season", "LCK/2017 Season/Summer Season"),
        ("LCK 2015 Spring Season", "LCK/2015 Season/Spring Season"),
        # OGN Champions (pre-2015)
        ("Champions 2014 Summer", "Champions Summer 2014"),
        ("Champions 2014 Spring", "Champions Spring 2014"),
        ("Champions 2013 Summer", "Champions Summer 2013"),
        ("Champions 2013 Spring", "Champions Spring 2013"),
    ]

    for name, path in lck_tests:
        result = test_tournament(name, path, "LCK/Champions")
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # REGIONAL LEAGUES - LPL
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LPL (CHINA)")
    print("="*80)

    lpl_tests = [
        ("LPL 2024 Spring Season", "LPL/2024 Season/Spring Season"),
        ("LPL 2024 Spring Playoffs", "LPL/2024 Season/Spring Playoffs"),
        ("LPL 2024 Summer Season", "LPL/2024 Season/Summer Season"),
        ("LPL 2023 Spring Season", "LPL/2023 Season/Spring Season"),
        ("LPL 2020 Spring", "LPL/2020 Season/Spring"),
        ("LPL 2019 Summer", "LPL/2019 Season/Summer"),
        ("LPL 2018 Spring", "LPL/2018 Season/Spring"),
        ("LPL 2017 Summer", "LPL/2017 Season/Summer"),
        ("LPL 2015 Spring", "LPL/2015 Season/Spring"),
        ("LPL 2014 Summer", "LPL/2014 Season/Summer"),
        ("LPL 2013 Spring", "LPL/2013 Season/Spring"),
    ]

    for name, path in lpl_tests:
        result = test_tournament(name, path, "LPL")
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # OTHER REGIONS
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: OTHER REGIONS")
    print("="*80)

    other_tests = [
        # CBLOL (Brazil)
        ("CBLOL 2024 Split 1", "CBLOL/2024 Season/Split 1", "CBLOL"),
        ("CBLOL 2024 Split 1 Playoffs", "CBLOL/2024 Season/Split 1 Playoffs", "CBLOL"),
        ("CBLOL 2020 Split 1", "CBLOL/2020 Season/Split 1", "CBLOL"),

        # LLA (Latin America)
        ("LLA 2024 Opening", "LLA/2024 Season/Opening", "LLA"),
        ("LLA 2024 Closing", "LLA/2024 Season/Closing", "LLA"),
        ("LLA 2020 Opening", "LLA/2020 Season/Opening", "LLA"),

        # PCS (Pacific)
        ("PCS 2024 Spring", "PCS/2024 Season/Spring", "PCS"),
        ("PCS 2023 Summer", "PCS/2023 Season/Summer", "PCS"),
        ("PCS 2020 Spring", "PCS/2020 Season/Spring", "PCS"),

        # VCS (Vietnam)
        ("VCS 2024 Spring", "VCS/2024 Season/Spring", "VCS"),
        ("VCS 2023 Summer", "VCS/2023 Season/Summer", "VCS"),
        ("VCS 2020 Spring", "VCS/2020 Season/Spring", "VCS"),

        # LJL (Japan)
        ("LJL 2024 Spring", "LJL/2024 Season/Spring", "LJL"),
        ("LJL 2023 Summer", "LJL/2023 Season/Summer", "LJL"),
        ("LJL 2020 Spring", "LJL/2020 Season/Spring", "LJL"),

        # TCL (Turkey)
        ("TCL 2024 Winter", "TCL/2024 Season/Winter", "TCL"),
        ("TCL 2023 Summer", "TCL/2023 Season/Summer", "TCL"),
        ("TCL 2020 Winter", "TCL/2020 Season/Winter", "TCL"),
    ]

    for name, path, category in other_tests:
        result = test_tournament(name, path, category)
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # REGIONAL CUPS
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: REGIONAL CUPS")
    print("="*80)

    cups_tests = [
        ("Kespa Cup 2024", "LoL KeSPA Cup/2024", "Kespa Cup"),
        ("Kespa Cup 2021", "LoL KeSPA Cup/2021", "Kespa Cup"),
        ("Kespa Cup 2019", "LoL KeSPA Cup/2019", "Kespa Cup"),
        ("Demacia Cup 2024 Winter", "Demacia Cup/2024 Winter", "Demacia Cup"),
        ("Demacia Cup 2023 Winter", "Demacia Cup/2023 Winter", "Demacia Cup"),
        ("Demacia Cup 2020 Winter", "Demacia Cup/2020 Winter", "Demacia Cup"),
    ]

    for name, path, category in cups_tests:
        result = test_tournament(name, path, category)
        results.append(result)
        time.sleep(DELAY)

    # ==================================================================
    # SUMMARY
    # ==================================================================

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("TEST COMPLETE - GENERATING SUMMARY")
    print("="*80)
    print(f"End time: {end_time}")
    print(f"Duration: {duration}")
    print(f"Total tests: {len(results)}")

    # Count by status
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    no_data_count = sum(1 for r in results if r['status'] == 'NO_DATA')
    error_count = sum(1 for r in results if r['status'] in ['ERROR', 'EXCEPTION'])

    print(f"\n✅ SUCCESS: {success_count}")
    print(f"⚠️  NO_DATA: {no_data_count}")
    print(f"❌ ERROR: {error_count}")

    # Group by category
    print("\n" + "="*80)
    print("RESULTS BY CATEGORY")
    print("="*80)

    categories = {}
    for result in results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = {'success': 0, 'no_data': 0, 'error': 0}

        if result['status'] == 'SUCCESS':
            categories[cat]['success'] += 1
        elif result['status'] == 'NO_DATA':
            categories[cat]['no_data'] += 1
        else:
            categories[cat]['error'] += 1

    for cat, counts in sorted(categories.items()):
        total = counts['success'] + counts['no_data'] + counts['error']
        print(f"\n{cat}:")
        print(f"  ✅ {counts['success']}/{total} have data")
        print(f"  ⚠️  {counts['no_data']}/{total} no data")
        print(f"  ❌ {counts['error']}/{total} errors")

    # Save results
    output_file = 'tournament_api_test_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'metadata': {
                'test_time': start_time.isoformat(),
                'duration': str(duration),
                'total_tests': len(results),
                'success': success_count,
                'no_data': no_data_count,
                'errors': error_count
            },
            'results': results,
            'summary_by_category': categories
        }, f, indent=2)

    print(f"\n📄 Detailed results saved to: {output_file}")

    # Print tournaments with data
    print("\n" + "="*80)
    print("TOURNAMENTS WITH DATA (for import)")
    print("="*80)

    for result in results:
        if result['status'] == 'SUCCESS':
            print(f"✅ {result['name']}")
            print(f"   Path: {result['path']}")
            print(f"   Sample: {result['sample']}")
            print()

if __name__ == '__main__':
    main()
