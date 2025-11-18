#!/usr/bin/env python3
"""
Part 2: Teste MSI, LCK, LPL, kleinere Regionen und Regional Cups
"""

import os
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from core.leaguepedia_loader import LeaguepediaLoader

# Set bot credentials
os.environ['LEAGUEPEDIA_BOT_USERNAME'] = 'ekwo98@Elo'
os.environ['LEAGUEPEDIA_BOT_PASSWORD'] = 'n7d9rsiccg7hujkg2hvtnglg4h93480r'

def test_url_variant(loader, name, url_variant):
    """Test a single URL variant"""
    try:
        games = loader._query_cargo(
            tables="ScoreboardGames",
            fields="Team1,Team2,Winner,DateTime_UTC,GameId",
            where=f"OverviewPage='{url_variant}'",
            limit=1
        )

        if games and len(games) > 0:
            game = games[0]
            sample = f"{game.get('Team1', 'N/A')} vs {game.get('Team2', 'N/A')}"
            date = game.get('DateTime UTC', 'N/A')
            print(f"    ✅ FOUND! Sample: {sample} ({date})")
            return True, sample, date
        else:
            print(f"    ⚠️  No data")
            return False, None, None
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False, None, None

def find_tournament_data(loader, tournament_name, url_variants):
    """Test multiple URL variants until data is found"""
    print(f"\n{'='*80}")
    print(f"SEARCHING: {tournament_name}")
    print(f"{'='*80}")

    for i, variant in enumerate(url_variants, 1):
        print(f"\n[{i}/{len(url_variants)}] Testing: {variant}")
        found, sample, date = test_url_variant(loader, tournament_name, variant)

        if found:
            print(f"\n✅✅✅ SUCCESS! Found data for {tournament_name}")
            print(f"    Working URL: {variant}")
            print(f"    Sample: {sample} ({date})")
            return variant, sample, date

        time.sleep(4)  # 4 second delay to avoid rate limiting

    print(f"\n❌ NOT FOUND: No data for {tournament_name} after {len(url_variants)} variants")
    return None, None, None

def main():
    print("="*80)
    print("ALTERNATIVE URL TESTING - PART 2")
    print("MSI, LCK/Champions, LPL, Kleinere Regionen, Regional Cups")
    print("="*80)

    loader = LeaguepediaLoader()

    if not loader.authenticated:
        print("⚠️  Bot authentication failed")
    else:
        print("✅ Bot authenticated successfully")

    results = {}

    # ========================================================================
    # MSI 2024, 2023, 2021
    # ========================================================================

    tournament_name = "MSI 2024 Main Event"
    variants = [
        "2024 Mid-Season Invitational",  # Without stage
        "2024 Mid-Season Invitational/Main Event",
        "2024 Mid-Season Invitational/Bracket",
        "MSI 2024",
        "Mid-Season Invitational 2024",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "MSI 2023 Main Event"
    variants = [
        "2023 Mid-Season Invitational",
        "2023 Mid-Season Invitational/Main Event",
        "2023 Mid-Season Invitational/Bracket",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "MSI 2021"
    variants = [
        "2021 Mid-Season Invitational",
        "2021 Mid-Season Invitational/Main Event",
        "2021 Mid-Season Invitational/Rumble Stage",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # LCK 2017, 2015 Spring
    # ========================================================================

    tournament_name = "LCK 2017 Spring Season"
    variants = [
        "LCK/2017 Season/Spring Season",
        "LCK/2017 Season/Spring",
        "LCK 2017 Spring",
        "LCK/2017/Spring",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "LCK 2015 Spring Season"
    variants = [
        "LCK/2015 Season/Spring Season",
        "LCK/2015 Season/Spring",
        "LCK 2015 Spring",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # OGN Champions 2013-2014
    # ========================================================================

    tournament_name = "Champions 2014 Summer"
    variants = [
        "Champions Summer 2014",
        "OGN Champions Summer 2014",
        "Champions/Summer 2014",
        "LCK/Champions/Summer 2014",
        "2014 Champions Summer",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "Champions 2013 Summer"
    variants = [
        "Champions Summer 2013",
        "OGN Champions Summer 2013",
        "Champions/Summer 2013",
        "2013 Champions Summer",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # LPL Regular Seasons - KRITISCH!
    # ========================================================================

    tournament_name = "LPL 2024 Spring Regular Season"
    variants = [
        "LPL/2024 Season/Spring Season",
        "LPL/2024 Season/Spring",  # Without "Season" suffix
        "LPL 2024 Spring",
        "LPL/2024/Spring",
        "LPL/2024 Season/Spring Regular Season",
        "LPL/2024 Spring Season",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "LPL 2020 Spring Regular Season"
    variants = [
        "LPL/2020 Season/Spring",
        "LPL/2020 Season/Spring Season",
        "LPL 2020 Spring",
        "LPL/2020/Spring",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "LPL 2018 Summer Regular Season"
    variants = [
        "LPL/2018 Season/Summer",
        "LPL/2018 Season/Summer Season",
        "LPL 2018 Summer",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # Kleinere Regionen - PCS, VCS, LJL, TCL, LLA
    # ========================================================================

    tournament_name = "PCS 2024 Spring"
    variants = [
        "PCS/2024 Season/Spring",
        "PCS/2024 Season/Spring Season",
        "PCS/2024 Season/Spring Split",
        "PCS 2024 Spring",
        "Pacific Championship Series/2024/Spring",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "VCS 2024 Spring"
    variants = [
        "VCS/2024 Season/Spring",
        "VCS/2024 Season/Spring Season",
        "VCS/2024 Season/Spring Split",
        "VCS 2024 Spring",
        "Vietnam Championship Series/2024/Spring",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "LJL 2024 Spring"
    variants = [
        "LJL/2024 Season/Spring",
        "LJL/2024 Season/Spring Season",
        "LJL/2024 Season/Spring Split",
        "LJL 2024 Spring",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "TCL 2024 Winter"
    variants = [
        "TCL/2024 Season/Winter",
        "TCL/2024 Season/Winter Season",
        "TCL/2024 Season/Winter Split",
        "TCL 2024 Winter",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "LLA 2024 Opening"
    variants = [
        "LLA/2024 Season/Opening",
        "LLA/2024 Season/Opening Season",
        "LLA/2024 Season/Opening Split",
        "LLA 2024 Opening",
        "Liga Latinoamerica/2024/Opening",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # Regional Cups
    # ========================================================================

    tournament_name = "Kespa Cup 2024"
    variants = [
        "LoL KeSPA Cup/2024",
        "KeSPA Cup 2024",
        "2024 KeSPA Cup",
        "Kespa Cup/2024",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    tournament_name = "Demacia Cup 2024 Winter"
    variants = [
        "Demacia Cup/2024 Winter",
        "Demacia Cup 2024 Winter",
        "2024 Demacia Cup Winter",
        "Demacia Cup/2024/Winter",
    ]
    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # Summary
    # ========================================================================

    print("\n" + "="*80)
    print("PART 2 SEARCH RESULTS")
    print("="*80)

    found_count = sum(1 for r in results.values() if r['url'] is not None)
    not_found_count = len(results) - found_count

    print(f"\n✅ Found: {found_count}/{len(results)}")
    print(f"❌ Not Found: {not_found_count}/{len(results)}")

    if found_count > 0:
        print("\n" + "="*80)
        print("NEWLY DISCOVERED URLS")
        print("="*80)

        for name, data in results.items():
            if data['url']:
                print(f"\n✅ {name}")
                print(f"   URL: {data['url']}")
                print(f"   Sample: {data['sample']} ({data['date']})")

    if not_found_count > 0:
        print("\n" + "="*80)
        print("STILL NOT FOUND")
        print("="*80)

        for name, data in results.items():
            if not data['url']:
                print(f"❌ {name}")

    # Save results
    import json
    with open('alternative_urls_part2_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Results saved to: alternative_urls_part2_results.json")

    loader.close()

if __name__ == '__main__':
    main()
