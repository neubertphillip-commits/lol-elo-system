#!/usr/bin/env python3
"""
Systematische Suche nach ALLEN League Playoffs mit 10 Retries
"""

import json
import time
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader

def exponential_backoff_query(loader, where_clause, max_retries=10):
    """
    Query with exponential backoff - 10 retries
    Delays: 3s, 6s, 12s, 24s, 48s, 96s, 192s, 384s, 768s, 1536s (max ~25min total)
    """
    for retry in range(max_retries):
        try:
            result = loader._query_cargo(
                where=where_clause,
                limit=3  # Just need to verify existence
            )
            return result
        except Exception as e:
            if retry < max_retries - 1:
                delay = 3 * (2 ** retry)  # 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536
                print(f"    [WARNING] Rate limited - waiting {delay}s before retry {retry+1}/{max_retries}")
                time.sleep(delay)
            else:
                print(f"    [ERROR] Rate limited after {max_retries} retries - giving up")
                return None
    return None

def search_playoffs(loader):
    """Search for all league playoffs with extensive URL variants"""

    results = {}

    searches = [
        # ========================================================================
        # LEC/EU LCS PLAYOFFS (2013-2024)
        # ========================================================================
        {
            "name": "LEC 2024 Spring Playoffs",
            "variants": [
                "LEC/2024 Season/Spring Playoffs",
                "LEC/2024 Season/Spring Season/Playoffs",
                "LEC/2024 Season/Spring/Playoffs",
            ]
        },
        {
            "name": "LEC 2024 Summer Playoffs",
            "variants": [
                "LEC/2024 Season/Summer Playoffs",
                "LEC/2024 Season/Summer Season/Playoffs",
            ]
        },
        {
            "name": "EU LCS 2018 Spring Playoffs",
            "variants": [
                "EU LCS/2018 Season/Spring Playoffs",
                "EU LCS/2018 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "EU LCS 2017 Spring Playoffs",
            "variants": [
                "EU LCS/2017 Season/Spring Playoffs",
                "EU LCS/2017 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "EU LCS 2016 Spring Playoffs",
            "variants": [
                "EU LCS/2016 Season/Spring Playoffs",
                "EU LCS/2016 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "EU LCS 2015 Spring Playoffs",
            "variants": [
                "EU LCS/2015 Season/Spring Playoffs",
                "EU LCS/2015 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "EU LCS 2014 Spring Playoffs",
            "variants": [
                "EU LCS/2014 Season/Spring Playoffs",
                "EU LCS/2014 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "EU LCS Season 3 Spring Playoffs",
            "variants": [
                "EU LCS/Season 3/Spring Playoffs",
                "EU LCS/Season 3/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # LCS/NA LCS PLAYOFFS (2013-2024)
        # ========================================================================
        {
            "name": "LCS 2024 Spring Playoffs",
            "variants": [
                "LCS/2024 Season/Spring Playoffs",
                "LCS/2024 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LCS 2024 Summer Playoffs",
            "variants": [
                "LCS/2024 Season/Summer Playoffs",
                "LCS/2024 Season/Summer Season/Playoffs",
            ]
        },
        {
            "name": "NA LCS 2018 Spring Playoffs",
            "variants": [
                "NA LCS/2018 Season/Spring Playoffs",
                "NA LCS/2018 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "NA LCS 2017 Spring Playoffs",
            "variants": [
                "NA LCS/2017 Season/Spring Playoffs",
                "NA LCS/2017 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "NA LCS 2016 Spring Playoffs",
            "variants": [
                "NA LCS/2016 Season/Spring Playoffs",
                "NA LCS/2016 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "NA LCS 2015 Spring Playoffs",
            "variants": [
                "NA LCS/2015 Season/Spring Playoffs",
                "NA LCS/2015 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "NA LCS 2014 Spring Playoffs",
            "variants": [
                "NA LCS/2014 Season/Spring Playoffs",
                "NA LCS/2014 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "NA LCS Season 3 Spring Playoffs",
            "variants": [
                "NA LCS/Season 3/Spring Playoffs",
                "NA LCS/Season 3/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # LPL PLAYOFFS (2013-2024)
        # ========================================================================
        {
            "name": "LPL 2024 Spring Playoffs",
            "variants": [
                "LPL/2024 Season/Spring Playoffs",
                "LPL/2024 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2024 Summer Playoffs",
            "variants": [
                "LPL/2024 Season/Summer Playoffs",
                "LPL/2024 Season/Summer Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2020 Spring Playoffs",
            "variants": [
                "LPL/2020 Season/Spring Playoffs",
                "LPL/2020 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2018 Spring Playoffs",
            "variants": [
                "LPL/2018 Season/Spring Playoffs",
                "LPL/2018 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2017 Spring Playoffs",
            "variants": [
                "LPL/2017 Season/Spring Playoffs",
                "LPL/2017 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2016 Spring Playoffs",
            "variants": [
                "LPL/2016 Season/Spring Playoffs",
                "LPL/2016 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2015 Spring Playoffs",
            "variants": [
                "LPL/2015 Season/Spring Playoffs",
                "LPL/2015 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2014 Spring Playoffs",
            "variants": [
                "LPL/2014 Season/Spring Playoffs",
                "LPL/2014 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LPL 2013 Spring Playoffs",
            "variants": [
                "LPL/2013 Season/Spring Playoffs",
                "LPL/2013 Season/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # LCK PLAYOFFS (2016-2024)
        # ========================================================================
        {
            "name": "LCK 2024 Spring Playoffs",
            "variants": [
                "LCK/2024 Season/Spring Playoffs",
                "LCK/2024 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LCK 2024 Summer Playoffs",
            "variants": [
                "LCK/2024 Season/Summer Playoffs",
                "LCK/2024 Season/Summer Season/Playoffs",
            ]
        },
        {
            "name": "LCK 2020 Spring Playoffs",
            "variants": [
                "LCK/2020 Season/Spring Playoffs",
                "LCK/2020 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LCK 2018 Spring Playoffs",
            "variants": [
                "LCK/2018 Season/Spring Playoffs",
                "LCK/2018 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LCK 2017 Spring Playoffs",
            "variants": [
                "LCK/2017 Season/Spring Playoffs",
                "LCK/2017 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LCK 2016 Spring Playoffs",
            "variants": [
                "LCK/2016 Season/Spring Playoffs",
                "LCK/2016 Season/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # CBLOL PLAYOFFS (2020-2024)
        # ========================================================================
        {
            "name": "CBLOL 2024 Split 1 Playoffs",
            "variants": [
                "CBLOL/2024 Split 1/Playoffs",
                "CBLOL 2024 Split 1/Playoffs",
                "CBLOL/2024 Split 1 Playoffs",
            ]
        },
        {
            "name": "CBLOL 2024 Split 2 Playoffs",
            "variants": [
                "CBLOL/2024 Split 2/Playoffs",
                "CBLOL 2024 Split 2/Playoffs",
            ]
        },
        {
            "name": "CBLOL 2020 Split 1 Playoffs",
            "variants": [
                "CBLOL/2020 Split 1/Playoffs",
                "CBLOL 2020 Split 1/Playoffs",
            ]
        },

        # ========================================================================
        # PCS PLAYOFFS (2020, 2024)
        # ========================================================================
        {
            "name": "PCS 2024 Spring Playoffs",
            "variants": [
                "PCS/2024 Season/Spring Playoffs",
                "PCS/2024 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "PCS 2020 Spring Playoffs",
            "variants": [
                "PCS/2020 Season/Spring Playoffs",
                "PCS/2020 Season/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # VCS PLAYOFFS (2020, 2024)
        # ========================================================================
        {
            "name": "VCS 2024 Spring Playoffs",
            "variants": [
                "VCS/2024 Season/Spring Playoffs",
                "VCS/2024 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "VCS 2020 Spring Playoffs",
            "variants": [
                "VCS/2020 Season/Spring Playoffs",
                "VCS/2020 Season/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # LJL PLAYOFFS (2020, 2024)
        # ========================================================================
        {
            "name": "LJL 2024 Spring Playoffs",
            "variants": [
                "LJL/2024 Season/Spring Playoffs",
                "LJL/2024 Season/Spring Season/Playoffs",
            ]
        },
        {
            "name": "LJL 2020 Spring Playoffs",
            "variants": [
                "LJL/2020 Season/Spring Playoffs",
                "LJL/2020 Season/Spring Season/Playoffs",
            ]
        },

        # ========================================================================
        # TCL PLAYOFFS (2020, 2024)
        # ========================================================================
        {
            "name": "TCL 2024 Winter Playoffs",
            "variants": [
                "TCL/2024 Season/Winter Playoffs",
                "TCL/2024 Season/Winter Season/Playoffs",
            ]
        },
        {
            "name": "TCL 2020 Winter Playoffs",
            "variants": [
                "TCL/2020 Season/Winter Playoffs",
                "TCL/2020 Season/Winter Season/Playoffs",
            ]
        },

        # ========================================================================
        # LLA PLAYOFFS (2020, 2024)
        # ========================================================================
        {
            "name": "LLA 2024 Opening Playoffs",
            "variants": [
                "LLA/2024 Season/Opening Playoffs",
                "LLA/2024 Season/Opening Season/Playoffs",
            ]
        },
        {
            "name": "LLA 2020 Opening Playoffs",
            "variants": [
                "LLA/2020 Season/Opening Playoffs",
                "LLA/2020 Season/Opening Season/Playoffs",
            ]
        },
    ]

    total = len(searches)
    found_count = 0
    not_found_count = 0

    for idx, search in enumerate(searches, 1):
        name = search["name"]
        variants = search["variants"]

        print(f"\n{'='*80}")
        print(f"SEARCHING: {name}")
        print(f"{'='*80}\n")

        found = False
        working_url = None
        sample_games = None

        for var_idx, variant in enumerate(variants, 1):
            print(f"[{var_idx}/{len(variants)}]")
            print(f"    Testing: {variant}")

            # Query with exponential backoff (10 retries)
            time.sleep(4)  # Base delay
            games = exponential_backoff_query(
                loader,
                f"OverviewPage='{variant}'",
                max_retries=10
            )

            if games and len(games) > 0:
                print(f"    ✅ FOUND! {len(games)} games")
                for i, game in enumerate(games[:3], 1):
                    print(f"       Game {i}: {game.team1} vs {game.team2} ({game.date})")
                found = True
                working_url = variant
                sample_games = [
                    {
                        "team1": game.team1,
                        "team2": game.team2,
                        "date": str(game.date)
                    }
                    for game in games[:3]
                ]
                break
            else:
                print(f"    ⚠️  No data")

        if found:
            print(f"\n✅✅✅ SUCCESS! Found {name}")
            print(f"    Working URL: {working_url}")
            results[name] = {
                "url": working_url,
                "count": len(games),
                "sample_games": sample_games
            }
            found_count += 1
        else:
            print(f"\n❌ NOT FOUND: {name} after testing {len(variants)} variants")
            results[name] = None
            not_found_count += 1

    print(f"\n{'='*80}")
    print(f"SEARCH RESULTS SUMMARY")
    print(f"{'='*80}\n")
    print(f"Found: {found_count}/{total}")
    print(f"Not Found: {not_found_count}/{total}")

    # Print found tournaments
    print(f"\n{'='*80}")
    print(f"FOUND PLAYOFFS")
    print(f"{'='*80}\n")
    for name, data in results.items():
        if data is not None:
            print(f"✅ {name}")
            print(f"   URL: {data['url']}")
            print(f"   Games found: {data['count']}\n")

    # Print not found
    print(f"{'='*80}")
    print(f"NOT FOUND")
    print(f"{'='*80}")
    for name, data in results.items():
        if data is None:
            print(f"❌ {name}")

    return results

def main():
    print("="*80)
    print("ALL LEAGUE PLAYOFFS COMPREHENSIVE SEARCH (10 RETRIES)")
    print("="*80)

    # Initialize loader
    loader = LeaguepediaLoader()
    print("[OK] Authenticated as ekwo98@Elo")

    # Verify bot authentication
    try:
        loader.authenticate_as_bot()
        print("[OK] Authenticated as ekwo98@Elo")
        print("✅ Bot authenticated successfully\n")
    except Exception as e:
        print(f"[ERROR] Bot authentication failed: {e}")
        return

    # Search for all playoffs
    results = search_playoffs(loader)

    # Save results to JSON
    output_file = Path(__file__).parent / "all_league_playoffs_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
