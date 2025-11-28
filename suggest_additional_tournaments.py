#!/usr/bin/env python3
"""
Suggest additional tournaments that might exist in MatchSchedule table
Based on Leaguepedia structure and known minor region history
"""

def suggest_tournaments():
    """
    Generate comprehensive list of potentially missing tournaments
    Organized by category
    """
    suggestions = {
        "2025_SEASONS": [],
        "LATIN_AMERICA_LEGACY": [],
        "SOUTHEAST_ASIA_LEGACY": [],
        "EUROPEAN_REGIONAL_LEAGUES": [],
        "ACADEMY_LEAGUES": [],
        "INTERNATIONAL_EVENTS": [],
        "REGIONAL_QUALIFIERS": [],
        "OTHER_MINOR_REGIONS": []
    }

    # ========================================================================
    # 2025 SEASONS (noch nicht getestet)
    # ========================================================================
    # CBLOL 2025
    suggestions["2025_SEASONS"].extend([
        ("CBLOL 2025 Split 1", "CBLOL/2025_Season/Split_1"),
        ("CBLOL 2025 Split 1 Playoffs", "CBLOL/2025_Season/Split_1_Playoffs"),
        ("CBLOL 2025 Split 2", "CBLOL/2025_Season/Split_2"),
        ("CBLOL 2025 Split 2 Playoffs", "CBLOL/2025_Season/Split_2_Playoffs"),
    ])

    # LLA 2025
    suggestions["2025_SEASONS"].extend([
        ("LLA 2025 Opening", "LLA/2025_Season/Opening_Season"),
        ("LLA 2025 Opening Playoffs", "LLA/2025_Season/Opening_Playoffs"),
        ("LLA 2025 Closing", "LLA/2025_Season/Closing_Season"),
        ("LLA 2025 Closing Playoffs", "LLA/2025_Season/Closing_Playoffs"),
    ])

    # VCS 2026 (falls schon geplant)
    suggestions["2025_SEASONS"].extend([
        ("VCS 2026 Spring", "VCS/2026_Season/Spring_Season"),
        ("VCS 2026 Summer", "VCS/2026_Season/Summer_Season"),
    ])

    # ========================================================================
    # LATIN AMERICA LEGACY (vor LLA/LLN)
    # ========================================================================
    # LAS (Latin America South) - 2014-2018
    for year in range(2014, 2019):
        suggestions["LATIN_AMERICA_LEGACY"].extend([
            (f"LAS {year} Opening", f"LAS/{year}_Season/Opening_Season"),
            (f"LAS {year} Opening Playoffs", f"LAS/{year}_Season/Opening_Playoffs"),
            (f"LAS {year} Closing", f"LAS/{year}_Season/Closing_Season"),
            (f"LAS {year} Closing Playoffs", f"LAS/{year}_Season/Closing_Playoffs"),
        ])

    # LAN 2014 (vor 2015)
    suggestions["LATIN_AMERICA_LEGACY"].extend([
        ("LAN 2014 Opening", "LAN/2014_Season/Opening_Season"),
        ("LAN 2014 Closing", "LAN/2014_Season/Closing_Season"),
    ])

    # LAN 2017-2018 (zwischen 2016 und LLN)
    for year in range(2017, 2019):
        suggestions["LATIN_AMERICA_LEGACY"].extend([
            (f"LAN {year} Opening", f"LAN/{year}_Season/Opening_Season"),
            (f"LAN {year} Closing", f"LAN/{year}_Season/Closing_Season"),
        ])

    # ========================================================================
    # SOUTHEAST ASIA LEGACY
    # ========================================================================
    # GPL 2019 (letztes Jahr vor Auflösung)
    suggestions["SOUTHEAST_ASIA_LEGACY"].extend([
        ("GPL 2019 Spring", "GPL/2019_Season/Spring_Season"),
        ("GPL 2019 Summer", "GPL/2019_Season/Summer_Season"),
    ])

    # LST (LoL SEA Tour)
    for year in range(2013, 2016):
        suggestions["SOUTHEAST_ASIA_LEGACY"].extend([
            (f"LST {year}", f"LST/{year}_Season/Main_Event"),
        ])

    # GPL Alternative URLs (könnte andere Struktur haben)
    suggestions["SOUTHEAST_ASIA_LEGACY"].extend([
        ("Garena Premier League 2015 Spring", "Garena_Premier_League/2015_Season/Spring_Season"),
        ("GPL SEA 2015 Spring", "GPL_SEA/2015_Season/Spring_Season"),
    ])

    # ========================================================================
    # EUROPEAN REGIONAL LEAGUES (falls als "Minor Region" gezählt)
    # ========================================================================
    # ERL könnte relevant sein für Elo-System
    for year in range(2019, 2026):
        # Prime League (Deutschland)
        suggestions["EUROPEAN_REGIONAL_LEAGUES"].extend([
            (f"Prime League {year} Spring", f"Prime_League/{year}_Season/Spring_Season"),
            (f"Prime League {year} Summer", f"Prime_League/{year}_Season/Summer_Season"),
        ])

        # LFL (Frankreich)
        suggestions["EUROPEAN_REGIONAL_LEAGUES"].extend([
            (f"LFL {year} Spring", f"LFL/{year}_Season/Spring_Season"),
            (f"LFL {year} Summer", f"LFL/{year}_Season/Summer_Season"),
        ])

        # Ultraliga (Polen)
        suggestions["EUROPEAN_REGIONAL_LEAGUES"].extend([
            (f"Ultraliga {year} Spring", f"Ultraliga/{year}_Season/Spring_Season"),
            (f"Ultraliga {year} Summer", f"Ultraliga/{year}_Season/Summer_Season"),
        ])

        # NLC (Northern League)
        suggestions["EUROPEAN_REGIONAL_LEAGUES"].extend([
            (f"NLC {year} Spring", f"NLC/{year}_Season/Spring_Season"),
            (f"NLC {year} Summer", f"NLC/{year}_Season/Summer_Season"),
        ])

        # LVP (Spanien)
        suggestions["EUROPEAN_REGIONAL_LEAGUES"].extend([
            (f"LVP {year} Spring", f"LVP/{year}_Season/Spring_Season"),
            (f"LVP {year} Summer", f"LVP/{year}_Season/Summer_Season"),
        ])

    # ========================================================================
    # ACADEMY LEAGUES
    # ========================================================================
    for year in range(2018, 2026):
        suggestions["ACADEMY_LEAGUES"].extend([
            (f"CBLOL Academy {year} Split 1", f"CBLOL_Academy/{year}_Season/Split_1"),
            (f"CBLOL Academy {year} Split 2", f"CBLOL_Academy/{year}_Season/Split_2"),
            (f"LLA Academy {year} Opening", f"LLA_Academy/{year}_Season/Opening_Season"),
            (f"LLA Academy {year} Closing", f"LLA_Academy/{year}_Season/Closing_Season"),
        ])

    # ========================================================================
    # INTERNATIONAL MINOR REGION EVENTS
    # ========================================================================
    for year in range(2015, 2025):
        suggestions["INTERNATIONAL_EVENTS"].extend([
            # MSI Play-In
            (f"MSI {year} Play-In", f"MSI/{year}_Season/Play-In"),
            # Worlds Play-In
            (f"Worlds {year} Play-In", f"Worlds/{year}_Season/Play-In"),
            # Rift Rivals
            (f"Rift Rivals {year} LAN-LAS-BR", f"Rift_Rivals/{year}_Season/LAN-LAS-BR"),
            (f"Rift Rivals {year} SEA", f"Rift_Rivals/{year}_Season/SEA"),
            (f"Rift Rivals {year} TCL-CIS", f"Rift_Rivals/{year}_Season/TCL-CIS"),
        ])

    # All-Star Events
    for year in range(2013, 2024):
        suggestions["INTERNATIONAL_EVENTS"].extend([
            (f"All-Star {year}", f"All-Star/{year}_Season/Main_Event"),
        ])

    # ========================================================================
    # REGIONAL QUALIFIERS
    # ========================================================================
    for year in range(2015, 2025):
        suggestions["REGIONAL_QUALIFIERS"].extend([
            (f"MSI {year} CBLOL Qualifier", f"CBLOL/{year}_Season/MSI_Qualifier"),
            (f"Worlds {year} CBLOL Qualifier", f"CBLOL/{year}_Season/Worlds_Qualifier"),
            (f"MSI {year} LLA Qualifier", f"LLA/{year}_Season/MSI_Qualifier"),
            (f"Worlds {year} LLA Qualifier", f"LLA/{year}_Season/Worlds_Qualifier"),
            (f"MSI {year} VCS Qualifier", f"VCS/{year}_Season/MSI_Qualifier"),
            (f"Worlds {year} VCS Qualifier", f"VCS/{year}_Season/Worlds_Qualifier"),
        ])

    # ========================================================================
    # OTHER MINOR REGIONS
    # ========================================================================
    # OCE (nach OPL 2020)
    for year in range(2021, 2026):
        suggestions["OTHER_MINOR_REGIONS"].extend([
            (f"LCO {year} Split 1", f"LCO/{year}_Season/Split_1"),
            (f"LCO {year} Split 2", f"LCO/{year}_Season/Split_2"),
        ])

    # MENA (Middle East North Africa)
    for year in range(2020, 2026):
        suggestions["OTHER_MINOR_REGIONS"].extend([
            (f"MENA {year} Split 1", f"MENA/{year}_Season/Split_1"),
            (f"MENA {year} Split 2", f"MENA/{year}_Season/Split_2"),
        ])

    # VCT (Vietnam Championship Series - Alternative Name)
    suggestions["OTHER_MINOR_REGIONS"].extend([
        ("VCT 2017 Spring", "VCT/2017_Season/Spring_Season"),
    ])

    return suggestions


def print_suggestions():
    """Print all suggestions organized by category"""
    suggestions = suggest_tournaments()

    total = sum(len(events) for events in suggestions.values())

    print("=" * 100)
    print("VORSCHLAG: ZUSÄTZLICHE TOURNAMENTS FÜR DISCOVERY")
    print("=" * 100)
    print(f"\nInsgesamt: {total} potenzielle zusätzliche Events")
    print()

    for category, events in suggestions.items():
        if events:
            print()
            print("=" * 100)
            print(f"{category.replace('_', ' ')} ({len(events)} Events)")
            print("=" * 100)

            for name, url in events[:10]:  # Show first 10 of each category
                url_display = url.replace('_', ' ')
                print(f"  • {name:70} | {url_display}")

            if len(events) > 10:
                print(f"  ... und {len(events) - 10} weitere")

    print()
    print("=" * 100)
    print("EMPFEHLUNG - PRIORISIERUNG")
    print("=" * 100)
    print()
    print("🔴 HOHE PRIORITÄT (sehr wahrscheinlich vorhanden):")
    print("  1. 2025_SEASONS: CBLOL 2025, LLA 2025")
    print("  2. LATIN_AMERICA_LEGACY: LAS 2014-2018 (vor LLA Merger)")
    print("  3. OTHER_MINOR_REGIONS: LCO 2021+ (Oceania nach OPL)")
    print()
    print("🟡 MITTLERE PRIORITÄT (könnte vorhanden sein):")
    print("  4. INTERNATIONAL_EVENTS: MSI/Worlds Play-Ins")
    print("  5. SOUTHEAST_ASIA_LEGACY: GPL alternative URLs")
    print()
    print("🟢 NIEDRIGE PRIORITÄT (optional):")
    print("  6. EUROPEAN_REGIONAL_LEAGUES: ERL (falls relevant)")
    print("  7. ACADEMY_LEAGUES: Academy Ligen")
    print("  8. REGIONAL_QUALIFIERS: Qualifier Tournaments")
    print()


if __name__ == "__main__":
    print_suggestions()
