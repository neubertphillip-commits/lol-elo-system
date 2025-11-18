#!/usr/bin/env python3
"""
Systematisches Testen alternativer URL-Patterns für fehlende Turniere
Testet verschiedene Varianten bis Daten gefunden werden
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

        time.sleep(3)  # Bot auth delay

    print(f"\n❌ NOT FOUND: No data found for {tournament_name} after testing {len(url_variants)} variants")
    return None, None, None

def main():
    print("="*80)
    print("SYSTEMATIC ALTERNATIVE URL PATTERN TESTING")
    print("="*80)

    loader = LeaguepediaLoader()

    if not loader.authenticated:
        print("⚠️  Warning: Bot authentication failed - tests will be slower")
    else:
        print("✅ Bot authenticated successfully")

    results = {}

    # ========================================================================
    # EU LCS 2018 Spring Season
    # ========================================================================

    tournament_name = "EU LCS 2018 Spring Season"
    variants = [
        "EU LCS/2018 Season/Spring Season",  # Original (failed)
        "EU LCS/2018 Season/Spring",  # Without "Season" suffix
        "EU LCS 2018 Spring",  # Without slashes
        "EU LCS/2018/Spring",  # Different slash pattern
        "EULCS/2018 Season/Spring Season",  # No space
        "LCS EU/2018 Season/Spring Season",  # Reversed
        "EU LCS/2018 Season/Spring Regular Season",  # With "Regular"
        "EU LCS/2018 Spring Season",  # Without "Season" in middle
        "2018 EU LCS Spring Season",  # Year first
        "League of Legends Championship Series/EU/2018/Spring",  # Full name
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # EU LCS 2013 Spring Season (Season 3)
    # ========================================================================

    tournament_name = "EU LCS 2013 Spring Season (Season 3)"
    variants = [
        "EU LCS/Season 3/Spring Season",  # Original (failed)
        "EU LCS/Season 3/Spring",  # Without "Season" suffix
        "EU LCS/2013 Season/Spring Season",  # With 2013 instead of Season 3
        "EU LCS/2013 Season/Spring",
        "EU LCS Season 3 Spring",  # Without slashes
        "Season 3/EU LCS/Spring Season",  # Different order
        "LCS/EU/Season 3/Spring",
        "EU LCS/Season 3/Spring Regular Season",
        "EU LCS 2013 Spring",
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # NA LCS 2018 Spring Season
    # ========================================================================

    tournament_name = "NA LCS 2018 Spring Season"
    variants = [
        "NA LCS/2018 Season/Spring Season",  # Original (failed)
        "NA LCS/2018 Season/Spring",
        "NA LCS 2018 Spring",
        "NA LCS/2018/Spring",
        "NALCS/2018 Season/Spring Season",
        "LCS NA/2018 Season/Spring Season",
        "NA LCS/2018 Season/Spring Regular Season",
        "NA LCS/2018 Spring Season",
        "2018 NA LCS Spring Season",
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # NA LCS 2013 Spring Season (Season 3)
    # ========================================================================

    tournament_name = "NA LCS 2013 Spring Season (Season 3)"
    variants = [
        "NA LCS/Season 3/Spring Season",  # Original (failed)
        "NA LCS/Season 3/Spring",
        "NA LCS/2013 Season/Spring Season",
        "NA LCS/2013 Season/Spring",
        "NA LCS Season 3 Spring",
        "Season 3/NA LCS/Spring Season",
        "NA LCS/Season 3/Spring Regular Season",
        "NA LCS 2013 Spring",
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # LEC 2024 Spring Season
    # ========================================================================

    tournament_name = "LEC 2024 Spring Season"
    variants = [
        "LEC/2024 Season/Spring Season",  # Original (failed)
        "LEC/2024 Season/Spring",
        "LEC 2024 Spring",
        "LEC/2024/Spring",
        "LEC/2024 Season/Spring Regular Season",
        "2024 LEC Spring Season",
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # Worlds 2024 Swiss Stage
    # ========================================================================

    tournament_name = "Worlds 2024 Swiss Stage"
    variants = [
        "2024 Season World Championship/Swiss Stage",  # Original (failed)
        "2024 Season World Championship/Swiss",
        "2024 Season World Championship",  # Main event without stage
        "2024 World Championship/Swiss Stage",
        "Worlds 2024/Swiss Stage",
        "2024 Season World Championship/Main Event/Swiss",
        "2024 Season World Championship/Group Stage",  # Maybe called Group Stage
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # Worlds 2024 Knockout Stage
    # ========================================================================

    tournament_name = "Worlds 2024 Knockout Stage"
    variants = [
        "2024 Season World Championship/Knockout Stage",  # Original (failed)
        "2024 Season World Championship/Knockout",
        "2024 Season World Championship/Finals",
        "2024 Season World Championship/Bracket",
        "2024 World Championship/Knockout Stage",
    ]

    url, sample, date = find_tournament_data(loader, tournament_name, variants)
    results[tournament_name] = {"url": url, "sample": sample, "date": date}

    # ========================================================================
    # Continue with more patterns...
    # ========================================================================

    # Print summary
    print("\n" + "="*80)
    print("SEARCH RESULTS SUMMARY")
    print("="*80)

    found_count = sum(1 for r in results.values() if r['url'] is not None)
    not_found_count = len(results) - found_count

    print(f"\n✅ Found: {found_count}/{len(results)}")
    print(f"❌ Not Found: {not_found_count}/{len(results)}")

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
    with open('alternative_urls_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Results saved to: alternative_urls_results.json")

    loader.close()

if __name__ == '__main__':
    main()
