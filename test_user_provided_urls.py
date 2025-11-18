#!/usr/bin/env python3
"""
Test user-provided URL patterns with 10 retries
- KeSPA Cup: {YEAR} LoL KeSPA Cup
- Champions: Champions/2012_Season (and other variations)
"""

import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader

def exponential_backoff_query(loader, url, max_retries=10):
    """Query with exponential backoff - 10 retries"""
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
                print(f"    [ERROR] Failed after {max_retries} retries")
                return None
    return None

loader = LeaguepediaLoader()

print("="*80)
print("TESTING USER-PROVIDED URL PATTERNS")
print("="*80)

# ============================================================================
# KeSPA Cup URLs
# ============================================================================
print("\n" + "="*80)
print("KESPA CUP TESTS")
print("="*80)

kespa_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2024, 2025]
for year in kespa_years:
    url = f"{year} LoL KeSPA Cup"
    print(f"\nTesting: {url}")
    time.sleep(4)  # Base delay
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

# ============================================================================
# Champions URLs - Test multiple patterns
# ============================================================================
print("\n" + "="*80)
print("CHAMPIONS TESTS - Multiple patterns")
print("="*80)

champions_tests = [
    # Pattern 1: Champions/YEAR_Season (from user's link)
    ("Champions/2012_Season", "Pattern: Champions/YEAR_Season"),
    ("Champions/2013_Season", "Pattern: Champions/YEAR_Season"),
    ("Champions/2014_Season", "Pattern: Champions/YEAR_Season"),
    ("Champions/2015_Season", "Pattern: Champions/YEAR_Season"),

    # Pattern 2: YEAR_Season/Champions
    ("2012_Season/Champions", "Pattern: YEAR_Season/Champions"),
    ("2013_Season/Champions", "Pattern: YEAR_Season/Champions"),

    # Pattern 3: Champions YEAR Season (with spaces)
    ("Champions 2012 Season", "Pattern: Champions YEAR Season"),
    ("Champions 2013 Season", "Pattern: Champions YEAR Season"),

    # Pattern 4: YEAR Champions
    ("2012 Champions", "Pattern: YEAR Champions"),
    ("2013 Champions", "Pattern: YEAR Champions"),

    # Pattern 5: OGN Champions YEAR
    ("OGN Champions 2012", "Pattern: OGN Champions YEAR"),
    ("OGN Champions 2013", "Pattern: OGN Champions YEAR"),
]

for url, description in champions_tests:
    print(f"\nTesting: {url}")
    print(f"  ({description})")
    time.sleep(4)  # Base delay
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

# ============================================================================
# Demacia Cup URLs
# ============================================================================
print("\n" + "="*80)
print("DEMACIA CUP TESTS")
print("="*80)

demacia_years = [2017, 2018, 2019, 2020, 2021, 2024]
for year in demacia_years:
    url = f"Demacia_Championship/{year}_Season"
    print(f"\nTesting: {url}")
    time.sleep(4)  # Base delay
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
