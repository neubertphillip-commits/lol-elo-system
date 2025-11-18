#!/usr/bin/env python3
"""Test Champions split patterns"""

import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader

def exponential_backoff_query(loader, url, max_retries=10):
    """Query with exponential backoff"""
    for retry in range(max_retries):
        try:
            games = loader._query_cargo(
                tables="ScoreboardGames",
                fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage",
                where=f"OverviewPage='{url}'",
                limit=5
            )
            return games
        except Exception as e:
            if retry < max_retries - 1:
                delay = 3 * (2 ** retry)
                print(f"    [RETRY {retry+1}/{max_retries}] Waiting {delay}s...")
                time.sleep(delay)
            else:
                print(f"    [FAILED] After {max_retries} retries")
                return None
    return None

loader = LeaguepediaLoader()

print("="*80)
print("TESTING CHAMPIONS SPLIT PATTERNS")
print("="*80)

# Test Champions splits for 2013-2015
# Patterns to test:
# - Champions/YEAR_Season/Spring
# - Champions/YEAR_Season/Summer
# - Champions/YEAR_Season/Winter
# - Champions/YEAR_Season/Spring_Qualifiers
# - Champions/YEAR_Season/Spring_Season
# - Champions/YEAR_Season/Spring_Playoffs

champions_tests = []

for year in [2012, 2013, 2014, 2015]:
    # Winter (usually at start of year)
    champions_tests.append((f"Champions/{year}_Season/Winter", f"Champions {year} Winter"))
    champions_tests.append((f"Champions/{year}_Season/Winter_Season", f"Champions {year} Winter Season"))

    # Spring
    for suffix in ["Spring", "Spring_Season", "Spring_Playoffs", "Spring_Qualifiers"]:
        champions_tests.append((f"Champions/{year}_Season/{suffix}", f"Champions {year} {suffix}"))

    # Summer
    for suffix in ["Summer", "Summer_Season", "Summer_Playoffs", "Summer_Qualifiers"]:
        champions_tests.append((f"Champions/{year}_Season/{suffix}", f"Champions {year} {suffix}"))

# Test each pattern
for url, name in champions_tests:
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    time.sleep(4)
    games = exponential_backoff_query(loader, url, max_retries=10)

    if games and len(games) > 0:
        print(f"  ✅ FOUND! {len(games)} games")
        for i, game in enumerate(games[:3], 1):
            team1 = game.get('Team1', 'N/A')
            team2 = game.get('Team2', 'N/A')
            date = game.get('DateTime UTC', 'N/A')
            print(f"     Game {i}: {team1} vs {team2} ({date})")
    else:
        print(f"  ❌ No data")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
