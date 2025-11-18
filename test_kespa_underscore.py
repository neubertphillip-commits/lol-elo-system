#!/usr/bin/env python3
"""Test KeSPA Cup with underscore vs space"""

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
print("TESTING KESPA CUP - UNDERSCORE vs SPACE")
print("="*80)

kespa_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2024, 2025]

for year in kespa_years:
    print(f"\n{'-'*80}")
    print(f"Year: {year}")
    print(f"{'-'*80}")

    # Test with UNDERSCORE (from user link)
    url_underscore = f"{year}_LoL_KeSPA_Cup"
    print(f"\n1. Testing UNDERSCORE: {url_underscore}")
    time.sleep(4)
    games = exponential_backoff_query(loader, url_underscore, max_retries=10)

    if games and len(games) > 0:
        print(f"   ✅ FOUND! {len(games)} games")
        for i, game in enumerate(games[:3], 1):
            team1 = game.get('Team1', 'N/A')
            team2 = game.get('Team2', 'N/A')
            date = game.get('DateTime UTC', 'N/A')
            print(f"      Game {i}: {team1} vs {team2} ({date})")
    else:
        print(f"   ❌ No data")

    # Test with SPACE (previously tested)
    url_space = f"{year} LoL KeSPA Cup"
    print(f"\n2. Testing SPACE: {url_space}")
    time.sleep(4)
    games = exponential_backoff_query(loader, url_space, max_retries=10)

    if games and len(games) > 0:
        print(f"   ✅ FOUND! {len(games)} games")
        for i, game in enumerate(games[:3], 1):
            team1 = game.get('Team1', 'N/A')
            team2 = game.get('Team2', 'N/A')
            date = game.get('DateTime UTC', 'N/A')
            print(f"      Game {i}: {team1} vs {team2} ({date})")
    else:
        print(f"   ❌ No data")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
