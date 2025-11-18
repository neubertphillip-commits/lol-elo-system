#!/usr/bin/env python3
"""Quick test for Champions/{YEAR}_Season pattern"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.leaguepedia_loader import LeaguepediaLoader

loader = LeaguepediaLoader()

# Test Champions URL pattern from user
years = [2012, 2013, 2014, 2015]
for year in years:
    url = f'Champions/{year}_Season'
    print(f'\nTesting: {url}')
    games = loader._query_cargo(
        tables="ScoreboardGames",
        fields="Team1,Team2,Winner,DateTime_UTC,GameId,OverviewPage",
        where=f"OverviewPage='{url}'",
        limit=5
    )
    if games and len(games) > 0:
        print(f'  ✅ FOUND! {len(games)} games')
        for i, game in enumerate(games[:3], 1):
            team1 = game.get('Team1', 'N/A')
            team2 = game.get('Team2', 'N/A')
            date = game.get('DateTime UTC', 'N/A')
            print(f'     Game {i}: {team1} vs {team2} ({date})')
    else:
        print(f'  ❌ No data')
