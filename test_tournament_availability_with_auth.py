#!/usr/bin/env python3
"""
Comprehensive API test with Bot Authentication
Tests tournament data availability with proper authentication
"""

import os
import sys
from pathlib import Path
import time
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.leaguepedia_loader import LeaguepediaLoader

# Set bot credentials
os.environ['LEAGUEPEDIA_BOT_USERNAME'] = 'ekwo98@Elo'
os.environ['LEAGUEPEDIA_BOT_PASSWORD'] = 'n7d9rsiccg7hujkg2hvtnglg4h93480r'

def test_tournament(loader, name, tournament_path, category):
    """Test if tournament has data"""
    print(f"\n[TEST] {name}")
    print(f"  Path: {tournament_path}")

    try:
        # Query for exactly 1 game to test availability
        games = loader._query_cargo(
            tables="ScoreboardGames",
            fields="Team1,Team2,Winner,DateTime_UTC,GameId",
            where=f"OverviewPage='{tournament_path}'",
            limit=1
        )

        if games and len(games) > 0:
            game = games[0]
            sample = f"{game.get('Team1', 'N/A')} vs {game.get('Team2', 'N/A')}"
            date = game.get('DateTime UTC', 'N/A')
            print(f"  ✅ SUCCESS - {sample} ({date})")

            return {
                'category': category,
                'name': name,
                'path': tournament_path,
                'status': 'SUCCESS',
                'sample': sample,
                'date': date
            }
        else:
            print(f"  ⚠️  NO_DATA")
            return {
                'category': category,
                'name': name,
                'path': tournament_path,
                'status': 'NO_DATA'
            }
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return {
            'category': category,
            'name': name,
            'path': tournament_path,
            'status': 'ERROR',
            'error': str(e)
        }

def main():
    print("="*80)
    print("COMPREHENSIVE TOURNAMENT DATA AVAILABILITY TEST")
    print("WITH BOT AUTHENTICATION")
    print("="*80)
    print(f"Start time: {datetime.now()}")
    print("="*80)

    # Initialize loader with bot auth
    print("\n[INIT] Initializing Leaguepedia loader with bot authentication...")
    loader = LeaguepediaLoader()

    if not loader.authenticated:
        print("  ❌ Bot authentication failed!")
        print("  Continuing without authentication (slower)")
    else:
        print("  ✅ Bot authentication successful!")

    results = []

    # ==================================================================
    # WORLD CHAMPIONSHIP - Sample representative years
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: WORLD CHAMPIONSHIP")
    print("="*80)

    worlds_tests = [
        # Recent (Swiss format)
        ("Worlds 2024 Play-In", "2024 Season World Championship/Play-In"),
        ("Worlds 2024 Swiss Stage", "2024 Season World Championship/Swiss Stage"),
        ("Worlds 2024 Knockout", "2024 Season World Championship/Knockout Stage"),

        # 2023
        ("Worlds 2023 Play-In", "2023 Season World Championship/Play-In"),
        ("Worlds 2023 Main Event", "2023 Season World Championship/Main Event"),
        ("Worlds 2023 Knockout", "2023 Season World Championship/Knockout Stage"),

        # 2020 (COVID year)
        ("Worlds 2020 Play-In", "2020 Season World Championship/Play-In"),
        ("Worlds 2020 Main Event", "2020 Season World Championship/Main Event"),

        # 2017 (First Play-In)
        ("Worlds 2017 Play-In", "2017 Season World Championship/Play-In"),
        ("Worlds 2017 Group Stage", "2017 Season World Championship/Group Stage"),

        # Pre Play-In era
        ("Worlds 2016 Group Stage", "2016 Season World Championship/Group Stage"),
        ("Worlds 2015 Group Stage", "2015 Season World Championship/Group Stage"),
        ("Worlds 2014", "2014 Season World Championship"),
        ("Worlds 2013", "Season 3 World Championship"),
    ]

    for name, path in worlds_tests:
        result = test_tournament(loader, name, path, "Worlds")
        results.append(result)
        time.sleep(3)  # 3s delay with bot auth

    # ==================================================================
    # MID-SEASON INVITATIONAL - Sample years
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: MID-SEASON INVITATIONAL")
    print("="*80)

    msi_tests = [
        ("MSI 2024 Play-In", "2024 Mid-Season Invitational/Play-In"),
        ("MSI 2024 Bracket", "2024 Mid-Season Invitational/Bracket Stage"),
        ("MSI 2023 Play-In", "2023 Mid-Season Invitational/Play-In"),
        ("MSI 2021", "2021 Mid-Season Invitational"),
        ("MSI 2019 Play-In", "2019 Mid-Season Invitational/Play-In"),
        ("MSI 2017 Play-In", "2017 Mid-Season Invitational/Play-In"),
        ("MSI 2015", "2015 Mid-Season Invitational"),
    ]

    for name, path in msi_tests:
        result = test_tournament(loader, name, path, "MSI")
        results.append(result)
        time.sleep(3)

    # ==================================================================
    # LEC / EU LCS - Representative years
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LEC / EU LCS (EUROPE)")
    print("="*80)

    lec_tests = [
        # LEC Modern (2024)
        ("LEC 2024 Winter Season", "LEC/2024 Season/Winter Season"),
        ("LEC 2024 Winter Playoffs", "LEC/2024 Season/Winter Playoffs"),
        ("LEC 2024 Spring Season", "LEC/2024 Season/Spring Season"),
        ("LEC 2024 Spring Playoffs", "LEC/2024 Season/Spring Playoffs"),

        # LEC 2023 (3 splits)
        ("LEC 2023 Winter Season", "LEC/2023 Season/Winter Season"),
        ("LEC 2023 Spring Season", "LEC/2023 Season/Spring Season"),

        # LEC Early (2019-2020)
        ("LEC 2020 Spring Season", "LEC/2020 Season/Spring Season"),
        ("LEC 2019 Spring Season", "LEC/2019 Season/Spring Season"),

        # EU LCS (2018-2016)
        ("EU LCS 2018 Spring Season", "EU LCS/2018 Season/Spring Season"),
        ("EU LCS 2018 Spring Playoffs", "EU LCS/2018 Season/Spring Playoffs"),
        ("EU LCS 2017 Summer Season", "EU LCS/2017 Season/Summer Season"),
        ("EU LCS 2016 Spring Season", "EU LCS/2016 Season/Spring Season"),

        # EU LCS Early (2015-2013)
        ("EU LCS 2015 Spring Season", "EU LCS/2015 Season/Spring Season"),
        ("EU LCS 2014 Summer Season", "EU LCS/2014 Season/Summer Season"),
        ("EU LCS 2013 Spring (S3)", "EU LCS/Season 3/Spring Season"),
        ("EU LCS 2013 Summer (S3)", "EU LCS/Season 3/Summer Season"),
    ]

    for name, path in lec_tests:
        result = test_tournament(loader, name, path, "LEC/EU LCS")
        results.append(result)
        time.sleep(3)

    # ==================================================================
    # LCS / NA LCS - Representative years
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LCS / NA LCS (NORTH AMERICA)")
    print("="*80)

    lcs_tests = [
        # LCS Modern (2024)
        ("LCS 2024 Spring Season", "LCS/2024 Season/Spring Season"),
        ("LCS 2024 Spring Playoffs", "LCS/2024 Season/Spring Playoffs"),

        # LCS Mid (2020-2019)
        ("LCS 2020 Spring Season", "LCS/2020 Season/Spring Season"),
        ("LCS 2019 Summer Season", "LCS/2019 Season/Summer Season"),

        # NA LCS (2018-2016)
        ("NA LCS 2018 Spring Season", "NA LCS/2018 Season/Spring Season"),
        ("NA LCS 2018 Spring Playoffs", "NA LCS/2018 Season/Spring Playoffs"),
        ("NA LCS 2017 Summer Season", "NA LCS/2017 Season/Summer Season"),
        ("NA LCS 2016 Spring Season", "NA LCS/2016 Season/Spring Season"),

        # NA LCS Early (2015-2013)
        ("NA LCS 2015 Spring Season", "NA LCS/2015 Season/Spring Season"),
        ("NA LCS 2014 Summer Season", "NA LCS/2014 Season/Summer Season"),
        ("NA LCS 2013 Spring (S3)", "NA LCS/Season 3/Spring Season"),
        ("NA LCS 2013 Summer (S3)", "NA LCS/Season 3/Summer Season"),
    ]

    for name, path in lcs_tests:
        result = test_tournament(loader, name, path, "LCS/NA LCS")
        results.append(result)
        time.sleep(3)

    # ==================================================================
    # LCK / CHAMPIONS - Representative years
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LCK / CHAMPIONS (KOREA)")
    print("="*80)

    lck_tests = [
        # LCK Modern (2024)
        ("LCK 2024 Spring Season", "LCK/2024 Season/Spring Season"),
        ("LCK 2024 Spring Playoffs", "LCK/2024 Season/Spring Playoffs"),

        # LCK Mid (2020-2018)
        ("LCK 2020 Spring Season", "LCK/2020 Season/Spring Season"),
        ("LCK 2018 Summer Season", "LCK/2018 Season/Summer Season"),

        # LCK Early (2017-2015)
        ("LCK 2017 Spring Season", "LCK/2017 Season/Spring Season"),
        ("LCK 2015 Spring Season", "LCK/2015 Season/Spring Season"),

        # OGN Champions (2014-2013)
        ("Champions 2014 Summer", "Champions Summer 2014"),
        ("Champions 2014 Spring", "Champions Spring 2014"),
        ("Champions 2013 Summer", "Champions Summer 2013"),
        ("Champions 2013 Spring", "Champions Spring 2013"),
    ]

    for name, path in lck_tests:
        result = test_tournament(loader, name, path, "LCK/Champions")
        results.append(result)
        time.sleep(3)

    # ==================================================================
    # LPL - Representative years
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: LPL (CHINA)")
    print("="*80)

    lpl_tests = [
        # LPL Modern (2024)
        ("LPL 2024 Spring Season", "LPL/2024 Season/Spring Season"),
        ("LPL 2024 Spring Playoffs", "LPL/2024 Season/Spring Playoffs"),

        # LPL Mid (2020-2018)
        ("LPL 2020 Spring", "LPL/2020 Season/Spring"),
        ("LPL 2020 Spring Playoffs", "LPL/2020 Season/Spring Playoffs"),
        ("LPL 2018 Summer", "LPL/2018 Season/Summer"),

        # LPL Early (2017-2015-2013)
        ("LPL 2017 Spring", "LPL/2017 Season/Spring"),
        ("LPL 2015 Summer", "LPL/2015 Season/Summer"),
        ("LPL 2014 Spring", "LPL/2014 Season/Spring"),
        ("LPL 2013 Summer", "LPL/2013 Season/Summer"),
    ]

    for name, path in lpl_tests:
        result = test_tournament(loader, name, path, "LPL")
        results.append(result)
        time.sleep(3)

    # ==================================================================
    # OTHER REGIONS - Sample tests
    # ==================================================================

    print("\n" + "="*80)
    print("TESTING: OTHER REGIONS (SAMPLES)")
    print("="*80)

    other_tests = [
        # CBLOL
        ("CBLOL 2024 Split 1", "CBLOL/2024 Season/Split 1", "CBLOL"),
        ("CBLOL 2020 Split 1", "CBLOL/2020 Season/Split 1", "CBLOL"),

        # LLA
        ("LLA 2024 Opening", "LLA/2024 Season/Opening", "LLA"),
        ("LLA 2020 Opening", "LLA/2020 Season/Opening", "LLA"),

        # PCS
        ("PCS 2024 Spring", "PCS/2024 Season/Spring", "PCS"),
        ("PCS 2020 Spring", "PCS/2020 Season/Spring", "PCS"),

        # VCS
        ("VCS 2024 Spring", "VCS/2024 Season/Spring", "VCS"),
        ("VCS 2020 Spring", "VCS/2020 Season/Spring", "VCS"),

        # LJL
        ("LJL 2024 Spring", "LJL/2024 Season/Spring", "LJL"),
        ("LJL 2020 Spring", "LJL/2020 Season/Spring", "LJL"),

        # TCL
        ("TCL 2024 Winter", "TCL/2024 Season/Winter", "TCL"),
        ("TCL 2020 Winter", "TCL/2020 Season/Winter", "TCL"),
    ]

    for name, path, category in other_tests:
        result = test_tournament(loader, name, path, category)
        results.append(result)
        time.sleep(3)

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
        ("Demacia Cup 2020 Winter", "Demacia Cup/2020 Winter", "Demacia Cup"),
    ]

    for name, path, category in cups_tests:
        result = test_tournament(loader, name, path, category)
        results.append(result)
        time.sleep(3)

    # ==================================================================
    # GENERATE SUMMARY
    # ==================================================================

    end_time = datetime.now()

    print("\n" + "="*80)
    print("TEST COMPLETE - GENERATING SUMMARY")
    print("="*80)
    print(f"End time: {end_time}")

    # Count by status
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    no_data_count = sum(1 for r in results if r['status'] == 'NO_DATA')
    error_count = sum(1 for r in results if r['status'] == 'ERROR')

    print(f"\nTotal tests: {len(results)}")
    print(f"✅ SUCCESS: {success_count}")
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
            categories[cat] = {'success': 0, 'no_data': 0, 'error': 0, 'tests': []}

        if result['status'] == 'SUCCESS':
            categories[cat]['success'] += 1
        elif result['status'] == 'NO_DATA':
            categories[cat]['no_data'] += 1
        else:
            categories[cat]['error'] += 1

        categories[cat]['tests'].append(result)

    for cat, counts in sorted(categories.items()):
        total = counts['success'] + counts['no_data'] + counts['error']
        success_pct = (counts['success'] / total * 100) if total > 0 else 0

        print(f"\n{cat}:")
        print(f"  ✅ {counts['success']}/{total} have data ({success_pct:.1f}%)")
        print(f"  ⚠️  {counts['no_data']}/{total} no data")
        print(f"  ❌ {counts['error']}/{total} errors")

    # Save results
    output_file = 'tournament_availability_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'metadata': {
                'test_time': end_time.isoformat(),
                'total_tests': len(results),
                'success': success_count,
                'no_data': no_data_count,
                'errors': error_count,
                'bot_authenticated': loader.authenticated
            },
            'results': results,
            'summary_by_category': {
                cat: {
                    'total': counts['success'] + counts['no_data'] + counts['error'],
                    'success': counts['success'],
                    'no_data': counts['no_data'],
                    'errors': counts['error'],
                    'success_rate': f"{(counts['success'] / (counts['success'] + counts['no_data'] + counts['error']) * 100):.1f}%"
                }
                for cat, counts in categories.items()
            }
        }, f, indent=2)

    print(f"\n📄 Results saved to: {output_file}")

    # Print all successful tournaments
    print("\n" + "="*80)
    print("TOURNAMENTS WITH DATA (CONFIRMED AVAILABLE)")
    print("="*80)

    success_by_category = {}
    for result in results:
        if result['status'] == 'SUCCESS':
            cat = result['category']
            if cat not in success_by_category:
                success_by_category[cat] = []
            success_by_category[cat].append(result)

    for cat in sorted(success_by_category.keys()):
        print(f"\n### {cat} ###")
        for result in success_by_category[cat]:
            print(f"✅ {result['name']}")
            print(f"   Path: {result['path']}")
            print(f"   Sample: {result['sample']}")

    # Print no-data tournaments
    print("\n" + "="*80)
    print("TOURNAMENTS WITHOUT DATA")
    print("="*80)

    no_data_by_category = {}
    for result in results:
        if result['status'] == 'NO_DATA':
            cat = result['category']
            if cat not in no_data_by_category:
                no_data_by_category[cat] = []
            no_data_by_category[cat].append(result)

    if no_data_by_category:
        for cat in sorted(no_data_by_category.keys()):
            print(f"\n### {cat} ###")
            for result in no_data_by_category[cat]:
                print(f"⚠️  {result['name']}")
                print(f"   Path: {result['path']}")
    else:
        print("\n✅ All tested tournaments have data!")

    loader.close()

    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == '__main__':
    main()
