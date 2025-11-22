#!/usr/bin/env python3
"""
COMPLETE TOURNAMENT DISCOVERY - MatchSchedule Edition
Testet ALLE möglichen Turniere in der MatchSchedule Tabelle

WICHTIG: Verwendet SPACES in URLs (nicht Underscores)!
Beispiel: "LEC/2024 Season/Spring Season" (nicht "LEC/2024_Season/Spring_Season")
"""

import os
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.leaguepedia_loader import LeaguepediaLoader

def test_tournament(loader, name, url_with_underscores):
    """
    Test if tournament exists in MatchSchedule table

    Args:
        loader: LeaguepediaLoader instance
        name: Tournament display name
        url_with_underscores: URL with underscores (will be converted to spaces)

    Returns:
        dict: Result with name, url, found status, match count
    """
    # Convert underscores to spaces for MatchSchedule
    url = url_with_underscores.replace('_', ' ')

    try:
        matches = loader._query_cargo(
            tables="MatchSchedule",
            fields="Team1,Team2",
            where=f"OverviewPage='{url}'",
            limit=5
        )

        if matches and len(matches) > 0:
            print(f"✅ {name:70} {len(matches)} matches (sample)")
            return {
                'name': name,
                'url': url,  # Save with SPACES
                'found': True,
                'sample_matches': len(matches)
            }
        else:
            print(f"❌ {name:70} NOT FOUND")
            return {
                'name': name,
                'url': url,
                'found': False
            }

    except Exception as e:
        print(f"❌ {name:70} ERROR: {e}")
        return {
            'name': name,
            'url': url,
            'found': False,
            'error': str(e)
        }

def generate_all_tournaments():
    """
    Generate comprehensive list of ALL possible tournaments

    Returns:
        list: List of (name, url) tuples
    """
    tournaments = []

    # ========================================================================
    # LPL (China) - 2013-2025
    # ========================================================================
    for year in range(2013, 2026):
        tournaments.append((f"LPL {year} Spring", f"LPL/{year}_Season/Spring_Season"))
        tournaments.append((f"LPL {year} Spring Playoffs", f"LPL/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LPL {year} Summer", f"LPL/{year}_Season/Summer_Season"))
        tournaments.append((f"LPL {year} Summer Playoffs", f"LPL/{year}_Season/Summer_Playoffs"))
        if year >= 2015:
            tournaments.append((f"LPL {year} Regional Finals", f"LPL/{year}_Season/Regional_Finals"))

    # Demacia Cup (China) - 2019-2024 only
    for year in range(2019, 2025):
        tournaments.append((f"Demacia Cup {year}", f"Demacia_Cup_{year}"))

    # ========================================================================
    # LCK (Korea) - 2013-2025
    # ========================================================================
    # OGN Champions (2013-2015)
    # 2013: No suffix
    tournaments.append(("OGN 2013 Winter", "Champions/2013_Season/Winter"))
    tournaments.append(("OGN 2013 Spring", "Champions/2013_Season/Spring"))
    tournaments.append(("OGN 2013 Summer", "Champions/2013_Season/Summer"))

    # 2014: All splits with " Season" suffix
    tournaments.append(("OGN 2014 Winter", "Champions/2014_Season/Winter_Season"))
    tournaments.append(("OGN 2014 Spring", "Champions/2014_Season/Spring_Season"))
    tournaments.append(("OGN 2014 Summer", "Champions/2014_Season/Summer_Season"))

    # 2015: Only Spring and Summer (Winter doesn't exist)
    tournaments.append(("OGN 2015 Spring", "Champions/2015_Season/Spring_Season"))
    tournaments.append(("OGN 2015 Summer", "Champions/2015_Season/Summer_Season"))

    # OGN Promotion (2013-2015) - Testing multiple URL formats
    ogn_promotion_formats = [
        # 2013
        ("OGN 2013 Winter Promotion", "Champions/2013_Season/Winter/Promotion"),
        ("OGN 2013 Winter Promotion (F2)", "Champions/2013_Season/Winter_Promotion"),
        ("OGN 2013 Spring Promotion", "Champions/2013_Season/Spring/Promotion"),
        ("OGN 2013 Spring Promotion (F2)", "Champions/2013_Season/Spring_Promotion"),
        ("OGN 2013 Summer Promotion", "Champions/2013_Season/Summer/Promotion"),
        ("OGN 2013 Summer Promotion (F2)", "Champions/2013_Season/Summer_Promotion"),
        # 2014
        ("OGN 2014 Winter Promotion", "Champions/2014_Season/Winter_Season/Promotion"),
        ("OGN 2014 Winter Promotion (F2)", "Champions/2014_Season/Winter_Promotion"),
        ("OGN 2014 Spring Promotion", "Champions/2014_Season/Spring_Season/Promotion"),
        ("OGN 2014 Spring Promotion (F2)", "Champions/2014_Season/Spring_Promotion"),
        ("OGN 2014 Summer Promotion", "Champions/2014_Season/Summer_Season/Promotion"),
        ("OGN 2014 Summer Promotion (F2)", "Champions/2014_Season/Summer_Promotion"),
        # 2015
        ("OGN 2015 Spring Promotion", "Champions/2015_Season/Spring_Season/Promotion"),
        ("OGN 2015 Spring Promotion (F2)", "Champions/2015_Season/Spring_Promotion"),
        ("OGN 2015 Summer Promotion", "Champions/2015_Season/Summer_Season/Promotion"),
        ("OGN 2015 Summer Promotion (F2)", "Champions/2015_Season/Summer_Promotion"),
    ]
    tournaments.extend(ogn_promotion_formats)

    # OGN/LCK Preseason (2013-2017) - Testing multiple URL formats
    preseason_formats = [
        ("OGN 2013 Preseason", "Champions/2013_Season/Preseason"),
        ("OGN 2013 Preseason (F2)", "Champions/Preseason/2013"),
        ("OGN 2014 Preseason", "Champions/2014_Season/Preseason"),
        ("OGN 2014 Preseason (F2)", "Champions/Preseason/2014"),
        ("OGN 2015 Preseason", "Champions/2015_Season/Preseason"),
        ("OGN 2015 Preseason (F2)", "Champions/Preseason/2015"),
        ("LCK 2016 Preseason", "LCK/2016_Season/Preseason"),
        ("LCK 2016 Preseason (F2)", "LCK/Preseason/2016"),
        ("LCK 2017 Preseason", "LCK/2017_Season/Preseason"),
        ("LCK 2017 Preseason (F2)", "LCK/Preseason/2017"),
    ]
    tournaments.extend(preseason_formats)

    # LCK (2016+)
    for year in range(2016, 2026):
        # Promotion tournaments (2016-2020 only)
        if year <= 2020:
            tournaments.append((f"LCK {year} Spring Promotion", f"LCK/{year}_Season/Spring_Promotion"))
            tournaments.append((f"LCK {year} Summer Promotion", f"LCK/{year}_Season/Summer_Promotion"))

        tournaments.append((f"LCK {year} Spring", f"LCK/{year}_Season/Spring_Season"))
        tournaments.append((f"LCK {year} Spring Playoffs", f"LCK/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LCK {year} Summer", f"LCK/{year}_Season/Summer_Season"))
        tournaments.append((f"LCK {year} Summer Playoffs", f"LCK/{year}_Season/Summer_Playoffs"))
        tournaments.append((f"LCK {year} Regional Finals", f"LCK/{year}_Season/Regional_Finals"))

    # KeSPA Cup (Korea) - 2015-2021, 2024 (2022-2023 don't exist)
    for year in range(2015, 2022):
        tournaments.append((f"KeSPA Cup {year}", f"{year}_lol_KeSPA_CUP"))
    tournaments.append(("KeSPA Cup 2024", "2024_lol_KeSPA_CUP"))

    # ========================================================================
    # LEC (EU) - 2013-2025
    # ========================================================================
    # EU LCS 2013 (Season 3) - Testing multiple URL formats
    season3_eu_formats = [
        # Format 1: Riot League Championship Series path
        ("EU LCS 2013 Spring", "Riot_League_Championship_Series/Europe/Season_3/Spring_Season"),
        ("EU LCS 2013 Spring Playoffs", "Riot_League_Championship_Series/Europe/Season_3/Spring_Playoffs"),
        ("EU LCS 2013 Summer", "Riot_League_Championship_Series/Europe/Season_3/Summer_Season"),
        ("EU LCS 2013 Summer Playoffs", "Riot_League_Championship_Series/Europe/Season_3/Summer_Playoffs"),
        # Format 2: Season 3 parent directory
        ("EU LCS 2013 Spring (F2)", "Season_3/European_LCS/Spring_Season"),
        ("EU LCS 2013 Spring Playoffs (F2)", "Season_3/European_LCS/Spring_Playoffs"),
        ("EU LCS 2013 Summer (F2)", "Season_3/European_LCS/Summer_Season"),
        ("EU LCS 2013 Summer Playoffs (F2)", "Season_3/European_LCS/Summer_Playoffs"),
        # Format 3: LCS Europe path
        ("EU LCS 2013 Spring (F3)", "LCS/Europe/Season_3/Spring_Season"),
        ("EU LCS 2013 Spring Playoffs (F3)", "LCS/Europe/Season_3/Spring_Playoffs"),
        ("EU LCS 2013 Summer (F3)", "LCS/Europe/Season_3/Summer_Season"),
        ("EU LCS 2013 Summer Playoffs (F3)", "LCS/Europe/Season_3/Summer_Playoffs"),
        # Format 4: EU LCS with Season 3
        ("EU LCS 2013 Spring (F4)", "EU_LCS/Season_3/Spring_Season"),
        ("EU LCS 2013 Spring Playoffs (F4)", "EU_LCS/Season_3/Spring_Playoffs"),
        ("EU LCS 2013 Summer (F4)", "EU_LCS/Season_3/Summer_Season"),
        ("EU LCS 2013 Summer Playoffs (F4)", "EU_LCS/Season_3/Summer_Playoffs"),
    ]
    tournaments.extend(season3_eu_formats)

    # EU LCS (2014-2018)
    for year in range(2014, 2019):
        tournaments.append((f"EU LCS {year} Spring", f"EU_LCS/{year}_Season/Spring_Season"))
        tournaments.append((f"EU LCS {year} Spring Playoffs", f"EU_LCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"EU LCS {year} Summer", f"EU_LCS/{year}_Season/Summer_Season"))
        tournaments.append((f"EU LCS {year} Summer Playoffs", f"EU_LCS/{year}_Season/Summer_Playoffs"))
        if year >= 2015:
            tournaments.append((f"EU LCS {year} Regional Finals", f"EU_LCS/{year}_Season/Regional_Finals"))

    # LEC (2019+)
    for year in range(2019, 2026):
        tournaments.append((f"LEC {year} Spring", f"LEC/{year}_Season/Spring_Season"))
        tournaments.append((f"LEC {year} Spring Playoffs", f"LEC/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LEC {year} Summer", f"LEC/{year}_Season/Summer_Season"))
        tournaments.append((f"LEC {year} Summer Playoffs", f"LEC/{year}_Season/Summer_Playoffs"))
        # LEC Winter only exists for 2023+
        if year >= 2023:
            tournaments.append((f"LEC {year} Winter", f"LEC/{year}_Season/Winter_Season"))
        # LEC Regional Finals only for 2019
        if year == 2019:
            tournaments.append((f"LEC {year} Regional Finals", f"LEC/{year}_Season/Regional_Finals"))

    # ========================================================================
    # LCS (NA) - 2013-2025
    # ========================================================================
    # NA LCS 2013 (Season 3) - Testing multiple URL formats
    season3_na_formats = [
        # Format 1: Riot League Championship Series path
        ("NA LCS 2013 Spring", "Riot_League_Championship_Series/North_America/Season_3/Spring_Season"),
        ("NA LCS 2013 Spring Playoffs", "Riot_League_Championship_Series/North_America/Season_3/Spring_Playoffs"),
        ("NA LCS 2013 Summer", "Riot_League_Championship_Series/North_America/Season_3/Summer_Season"),
        ("NA LCS 2013 Summer Playoffs", "Riot_League_Championship_Series/North_America/Season_3/Summer_Playoffs"),
        # Format 2: Season 3 parent directory
        ("NA LCS 2013 Spring (F2)", "Season_3/North_American_LCS/Spring_Season"),
        ("NA LCS 2013 Spring Playoffs (F2)", "Season_3/North_American_LCS/Spring_Playoffs"),
        ("NA LCS 2013 Summer (F2)", "Season_3/North_American_LCS/Summer_Season"),
        ("NA LCS 2013 Summer Playoffs (F2)", "Season_3/North_American_LCS/Summer_Playoffs"),
        # Format 3: LCS North America path
        ("NA LCS 2013 Spring (F3)", "LCS/North_America/Season_3/Spring_Season"),
        ("NA LCS 2013 Spring Playoffs (F3)", "LCS/North_America/Season_3/Spring_Playoffs"),
        ("NA LCS 2013 Summer (F3)", "LCS/North_America/Season_3/Summer_Season"),
        ("NA LCS 2013 Summer Playoffs (F3)", "LCS/North_America/Season_3/Summer_Playoffs"),
        # Format 4: NA LCS with Season 3
        ("NA LCS 2013 Spring (F4)", "NA_LCS/Season_3/Spring_Season"),
        ("NA LCS 2013 Spring Playoffs (F4)", "NA_LCS/Season_3/Spring_Playoffs"),
        ("NA LCS 2013 Summer (F4)", "NA_LCS/Season_3/Summer_Season"),
        ("NA LCS 2013 Summer Playoffs (F4)", "NA_LCS/Season_3/Summer_Playoffs"),
    ]
    tournaments.extend(season3_na_formats)

    # NA LCS (2014-2018)
    for year in range(2014, 2019):
        tournaments.append((f"NA LCS {year} Spring", f"NA_LCS/{year}_Season/Spring_Season"))
        tournaments.append((f"NA LCS {year} Spring Playoffs", f"NA_LCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"NA LCS {year} Summer", f"NA_LCS/{year}_Season/Summer_Season"))
        tournaments.append((f"NA LCS {year} Summer Playoffs", f"NA_LCS/{year}_Season/Summer_Playoffs"))
        if year >= 2015:
            tournaments.append((f"NA LCS {year} Regional Finals", f"NA_LCS/{year}_Season/Regional_Finals"))

    # LCS 2019 - Traditional format with Regional Finals
    tournaments.append(("LCS 2019 Spring", "LCS/2019_Season/Spring_Season"))
    tournaments.append(("LCS 2019 Spring Playoffs", "LCS/2019_Season/Spring_Playoffs"))
    tournaments.append(("LCS 2019 Summer", "LCS/2019_Season/Summer_Season"))
    tournaments.append(("LCS 2019 Summer Playoffs", "LCS/2019_Season/Summer_Playoffs"))
    tournaments.append(("LCS 2019 Regional Finals", "LCS/2019_Season/Regional_Finals"))

    # LCS 2020 - No Regional Finals
    tournaments.append(("LCS 2020 Spring", "LCS/2020_Season/Spring_Season"))
    tournaments.append(("LCS 2020 Spring Playoffs", "LCS/2020_Season/Spring_Playoffs"))
    tournaments.append(("LCS 2020 Summer", "LCS/2020_Season/Summer_Season"))
    tournaments.append(("LCS 2020 Summer Playoffs", "LCS/2020_Season/Summer_Playoffs"))

    # LCS 2021 - Special formats (Mid-Season Showdown instead of Spring Playoffs, Championship instead of Summer Playoffs)
    tournaments.append(("LCS 2021 Spring", "LCS/2021_Season/Spring_Season"))
    tournaments.append(("LCS 2021 Mid-Season Showdown", "LCS/2021_Season/Mid-Season_Showdown"))
    tournaments.append(("LCS 2021 Summer", "LCS/2021_Season/Summer_Season"))
    tournaments.append(("LCS 2021 Championship", "LCS/2021_Season/Championship"))

    # LCS 2022 - Lock In + Championship (no Regional Finals, no Summer Playoffs)
    tournaments.append(("LCS 2022 Lock In", "LCS/2022_Season/Lock_In"))
    tournaments.append(("LCS 2022 Spring", "LCS/2022_Season/Spring_Season"))
    tournaments.append(("LCS 2022 Spring Playoffs", "LCS/2022_Season/Spring_Playoffs"))
    tournaments.append(("LCS 2022 Summer", "LCS/2022_Season/Summer_Season"))
    tournaments.append(("LCS 2022 Championship", "LCS/2022_Season/Championship"))

    # LCS (2023-2024) - No Lock In, Championship instead of Summer Playoffs
    for year in range(2023, 2025):
        tournaments.append((f"LCS {year} Spring", f"LCS/{year}_Season/Spring_Season"))
        tournaments.append((f"LCS {year} Spring Playoffs", f"LCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LCS {year} Summer", f"LCS/{year}_Season/Summer_Season"))
        tournaments.append((f"LCS {year} Championship", f"LCS/{year}_Season/Championship"))

    # LCS 2025 - Skip for now (new format with 3 splits)

    # ========================================================================
    # CBLOL (Brazil) - 2015-2025
    # ========================================================================
    for year in range(2015, 2026):
        tournaments.append((f"CBLOL {year} Split 1", f"CBLOL/{year}_Season/Split_1"))
        tournaments.append((f"CBLOL {year} Split 2", f"CBLOL/{year}_Season/Split_2"))
        # CBLOL Playoffs and Regional Finals - NOT IN MATCHSCHEDULE

    # ========================================================================
    # PCS (Pacific) - 2020-2025
    # ========================================================================
    for year in range(2020, 2026):
        tournaments.append((f"PCS {year} Spring", f"PCS/{year}_Season/Spring_Season"))
        tournaments.append((f"PCS {year} Spring Playoffs", f"PCS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"PCS {year} Summer", f"PCS/{year}_Season/Summer_Season"))
        tournaments.append((f"PCS {year} Summer Playoffs", f"PCS/{year}_Season/Summer_Playoffs"))
        tournaments.append((f"PCS {year} Regional Finals", f"PCS/{year}_Season/Regional_Finals"))

    # LMS (Taiwan, predecessor to PCS) - 2015-2019
    for year in range(2015, 2020):
        tournaments.append((f"LMS {year} Spring", f"LMS/{year}_Season/Spring_Season"))
        tournaments.append((f"LMS {year} Spring Playoffs", f"LMS/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LMS {year} Summer", f"LMS/{year}_Season/Summer_Season"))
        tournaments.append((f"LMS {year} Summer Playoffs", f"LMS/{year}_Season/Summer_Playoffs"))
        if year >= 2015:
            tournaments.append((f"LMS {year} Regional Finals", f"LMS/{year}_Season/Regional_Finals"))

    # ========================================================================
    # VCS (Vietnam) - 2018-2025 (started in 2018, not 2017)
    # ========================================================================
    for year in range(2018, 2026):
        tournaments.append((f"VCS {year} Spring", f"VCS/{year}_Season/Spring_Season"))
        tournaments.append((f"VCS {year} Spring Playoffs", f"VCS/{year}_Season/Spring_Playoffs"))

        # VCS 2021 Summer was cancelled due to COVID
        if year != 2021:
            tournaments.append((f"VCS {year} Summer", f"VCS/{year}_Season/Summer_Season"))
            tournaments.append((f"VCS {year} Summer Playoffs", f"VCS/{year}_Season/Summer_Playoffs"))

        if year >= 2020:
            tournaments.append((f"VCS {year} Regional Finals", f"VCS/{year}_Season/Regional_Finals"))

    # ========================================================================
    # LJL (Japan) - 2014, 2016-2025 (2015 not in MatchSchedule)
    # ========================================================================
    # LJL 2014 (no playoffs)
    tournaments.append(("LJL 2014 Spring", "LJL/2014_Season/Spring_Season"))
    tournaments.append(("LJL 2014 Summer", "LJL/2014_Season/Summer_Season"))

    # LJL 2016+ (with playoffs)
    for year in range(2016, 2026):
        tournaments.append((f"LJL {year} Spring", f"LJL/{year}_Season/Spring_Season"))
        tournaments.append((f"LJL {year} Spring Playoffs", f"LJL/{year}_Season/Spring_Playoffs"))
        tournaments.append((f"LJL {year} Summer", f"LJL/{year}_Season/Summer_Season"))
        tournaments.append((f"LJL {year} Summer Playoffs", f"LJL/{year}_Season/Summer_Playoffs"))
        if year >= 2020:
            tournaments.append((f"LJL {year} Regional Finals", f"LJL/{year}_Season/Regional_Finals"))

    # ========================================================================
    # TCL (Turkey) - 2015-2025 (started in 2015, not 2013)
    # ========================================================================
    for year in range(2015, 2026):
        tournaments.append((f"TCL {year} Winter", f"TCL/{year}_Season/Winter_Season"))
        tournaments.append((f"TCL {year} Winter Playoffs", f"TCL/{year}_Season/Winter_Playoffs"))
        tournaments.append((f"TCL {year} Summer", f"TCL/{year}_Season/Summer_Season"))
        tournaments.append((f"TCL {year} Summer Playoffs", f"TCL/{year}_Season/Summer_Playoffs"))
        if year >= 2020:
            tournaments.append((f"TCL {year} Regional Finals", f"TCL/{year}_Season/Regional_Finals"))

    # ========================================================================
    # LLA (Latin America) - 2019-2025
    # ========================================================================
    for year in range(2019, 2026):
        tournaments.append((f"LLA {year} Opening", f"LLA/{year}_Season/Opening_Season"))
        tournaments.append((f"LLA {year} Opening Playoffs", f"LLA/{year}_Season/Opening_Playoffs"))
        tournaments.append((f"LLA {year} Closing", f"LLA/{year}_Season/Closing_Season"))
        tournaments.append((f"LLA {year} Closing Playoffs", f"LLA/{year}_Season/Closing_Playoffs"))
        if year >= 2020:
            tournaments.append((f"LLA {year} Regional Finals", f"LLA/{year}_Season/Regional_Finals"))

    # LLN (predecessor to LLA) - 2017-2018 only (2014-2016 not in MatchSchedule)
    for year in range(2017, 2019):
        tournaments.append((f"LLN {year} Opening", f"LLN/{year}_Season/Opening_Season"))
        tournaments.append((f"LLN {year} Closing", f"LLN/{year}_Season/Closing_Season"))

    # ========================================================================
    # Historical Regions
    # ========================================================================
    # GPL (Southeast Asia) - NOT IN MATCHSCHEDULE, REMOVED

    # OPL (Oceania) - 2015-2020
    for year in range(2015, 2021):
        tournaments.append((f"OPL {year} Split 1", f"OPL/{year}_Season/Split_1"))
        tournaments.append((f"OPL {year} Split 2", f"OPL/{year}_Season/Split_2"))

    # LCL (Russia) - NOT IN MATCHSCHEDULE, REMOVED

    # ========================================================================
    # INTERNATIONAL TOURNAMENTS
    # ========================================================================

    # World Championship - 2013-2024
    # 2013: Special format (Season 3)
    tournaments.append(("Worlds 2013", "Season_3_World_Championship"))

    # 2014-2016: Standalone format (no Play-In)
    for year in range(2014, 2017):
        tournaments.append((f"Worlds {year}", f"{year}_Season_World_Championship"))

    # 2017-2024: Play-In + Main Event format
    for year in range(2017, 2025):
        tournaments.append((f"Worlds {year} Play-In", f"{year}_Season_World_Championship/Play-In"))
        tournaments.append((f"Worlds {year} Main Event", f"{year}_Season_World_Championship/Main_Event"))

    # MSI - 2015-2024 (complex pattern)
    # 2015-2016: Standalone only
    for year in [2015, 2016]:
        tournaments.append((f"MSI {year}", f"{year}_Mid-Season_Invitational"))

    # 2017-2019: Play-In + Main Event (no standalone)
    for year in range(2017, 2020):
        tournaments.append((f"MSI {year} Play-In", f"{year}_Mid-Season_Invitational/Play-In"))
        tournaments.append((f"MSI {year} Main Event", f"{year}_Mid-Season_Invitational/Main_Event"))

    # 2020: MSI cancelled (COVID-19)

    # 2021-2024: Standalone only (no Play-In/Main Event split)
    for year in range(2021, 2025):
        tournaments.append((f"MSI {year}", f"{year}_Mid-Season_Invitational"))

    # IEM Tournaments - 2012-2018
    iem_events = [
        # Season VI (2011-2012)
        ("IEM Season VI Global Challenge Cologne", "IEM_Season_VI_-_Global_Challenge_Cologne"),
        ("IEM Season VI World Championship", "IEM_Season_VI_-_World_Championship"),

        # Season VII (2012-2013)
        ("IEM Season VII Global Challenge Cologne", "IEM_Season_VII_-_Global_Challenge_Cologne"),
        ("IEM Season VII World Championship", "IEM_Season_VII_-_World_Championship"),

        # Season VIII (2013-2014)
        ("IEM Season VIII Cologne", "IEM_Season_VIII_-_Cologne"),
        ("IEM Season VIII Shanghai", "IEM_Season_VIII_-_Shanghai"),
        ("IEM Season VIII Singapore", "IEM_Season_VIII_-_Singapore"),
        ("IEM Season VIII Sao Paulo", "IEM_Season_VIII_-_Sao_Paulo"),
        ("IEM Season VIII World Championship", "IEM_Season_VIII_-_World_Championship"),

        # Season IX (2014-2015)
        ("IEM Season IX Cologne", "IEM_Season_IX_-_Cologne"),
        ("IEM Season IX San Jose", "IEM_Season_IX_-_San_Jose"),
        ("IEM Season IX World Championship", "IEM_Season_IX_-_World_Championship"),

        # Season X (2015-2016)
        ("IEM Season X Cologne", "IEM_Season_X_-_Cologne"),
        ("IEM Season X San Jose", "IEM_Season_X_-_San_Jose"),
        # IEM Season X-XII Katowice, Oakland, Gyeonggi - NOT IN MATCHSCHEDULE
    ]
    tournaments.extend(iem_events)

    # Rift Rivals - 2017-2019
    rift_rivals = [
        ("Rift Rivals 2017 NA-EU", "Rift_Rivals_2017/NA-EU"),
        ("Rift Rivals 2017 LCK-LPL-LMS", "Rift_Rivals_2017/LCK-LPL-LMS"),
        ("Rift Rivals 2018 NA-EU", "Rift_Rivals_2018/NA-EU"),
        ("Rift Rivals 2018 LCK-LPL-LMS", "Rift_Rivals_2018/LCK-LPL-LMS"),
        ("Rift Rivals 2019 NA-EU", "Rift_Rivals_2019/NA-EU"),
        ("Rift Rivals 2019 LCK-LPL-LMS-VCS", "Rift_Rivals_2019/LCK-LPL-LMS-VCS"),
    ]
    tournaments.extend(rift_rivals)

    # All-Star - NOT IN MATCHSCHEDULE, REMOVED

    return tournaments

def main():
    """Main discovery function"""

    bot_username = os.getenv("LEAGUEPEDIA_BOT_USERNAME", "Ekwo98@Elo")
    bot_password = os.getenv("LEAGUEPEDIA_BOT_PASSWORD")

    if not bot_password:
        print("❌ LEAGUEPEDIA_BOT_PASSWORD environment variable not set!")
        return 1

    loader = LeaguepediaLoader(bot_username=bot_username, bot_password=bot_password)

    print("=" * 80)
    print("COMPLETE TOURNAMENT DISCOVERY - MatchSchedule Edition")
    print("=" * 80)
    print("Generating tournament list...")

    all_tournaments = generate_all_tournaments()
    print(f"📋 Testing {len(all_tournaments)} tournaments\n")

    found_tournaments = []
    not_found_tournaments = []

    start_time = time.time()

    for i, (name, url) in enumerate(all_tournaments, 1):
        result = test_tournament(loader, name, url)

        if result['found']:
            found_tournaments.append(result)
        else:
            not_found_tournaments.append(result)

        # Progress update every 50 tournaments
        if i % 50 == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = (len(all_tournaments) - i) * avg_time
            print(f"\n⏱️  Progress: {i}/{len(all_tournaments)} | Found: {len(found_tournaments)} | Remaining: {remaining/60:.1f}m\n")

    elapsed_total = time.time() - start_time

    # Save results
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'duration_seconds': elapsed_total,
        'total_tested': len(all_tournaments),
        'total_found': len(found_tournaments),
        'total_not_found': len(not_found_tournaments),
        'success_rate': len(found_tournaments) / len(all_tournaments) * 100,
        'found_tournaments': found_tournaments,
        'not_found_tournaments': not_found_tournaments
    }

    output_file = Path(__file__).parent / "complete_tournament_discovery_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("DISCOVERY COMPLETE")
    print("=" * 80)
    print(f"Time elapsed: {elapsed_total/60:.1f} minutes")
    print(f"\nTotal tested:   {len(all_tournaments)}")
    print(f"Found:          {len(found_tournaments)}")
    print(f"Not Found:      {len(not_found_tournaments)}")
    print(f"Success rate:   {len(found_tournaments)/len(all_tournaments)*100:.1f}%")
    print(f"\n📄 Results saved to: {output_file}")

    return 0

if __name__ == "__main__":
    exit(main())
