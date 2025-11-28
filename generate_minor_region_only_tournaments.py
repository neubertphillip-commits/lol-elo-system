#!/usr/bin/env python3
"""
Generate tournament list for MINOR REGIONS ONLY
- Main regional leagues (2025, LAS, LCO)
- International events WITHOUT major region participation
- GPL URL fixes (to be added later)
"""

def generate_minor_region_tournaments():
    """
    Generate tournaments for minor regions only
    Excludes: Tier 2 leagues, academy, qualifiers, events with major regions
    """
    tournaments = []

    # ========================================================================
    # 2025 SEASONS - MAIN LEAGUES
    # ========================================================================
    # CBLOL 2025
    tournaments.append(("CBLOL 2025 Split 1", "CBLOL/2025_Season/Split_1"))
    tournaments.append(("CBLOL 2025 Split 1 Playoffs", "CBLOL/2025_Season/Split_1_Playoffs"))
    tournaments.append(("CBLOL 2025 Split 2", "CBLOL/2025_Season/Split_2"))
    tournaments.append(("CBLOL 2025 Split 2 Playoffs", "CBLOL/2025_Season/Split_2_Playoffs"))

    # LLA 2025
    tournaments.append(("LLA 2025 Opening", "LLA/2025_Season/Opening_Season"))
    tournaments.append(("LLA 2025 Opening Playoffs", "LLA/2025_Season/Opening_Playoffs"))
    tournaments.append(("LLA 2025 Closing", "LLA/2025_Season/Closing_Season"))
    tournaments.append(("LLA 2025 Closing Playoffs", "LLA/2025_Season/Closing_Playoffs"))

    # ========================================================================
    # LAS (Latin America South) - 2014-2018
    # ========================================================================
    for year in range(2014, 2019):
        tournaments.append((f"LAS {year} Opening", f"LAS/{year}_Season/Opening_Season"))
        tournaments.append((f"LAS {year} Opening Playoffs", f"LAS/{year}_Season/Opening_Playoffs"))
        tournaments.append((f"LAS {year} Closing", f"LAS/{year}_Season/Closing_Season"))
        tournaments.append((f"LAS {year} Closing Playoffs", f"LAS/{year}_Season/Closing_Playoffs"))

    # LAS 2013 (falls vorhanden)
    tournaments.append(("LAS 2013 Opening", "LAS/2013_Season/Opening_Season"))
    tournaments.append(("LAS 2013 Closing", "LAS/2013_Season/Closing_Season"))

    # ========================================================================
    # LCO (League of Legends Circuit Oceania) - 2021-2025
    # ========================================================================
    for year in range(2021, 2026):
        tournaments.append((f"LCO {year} Split 1", f"LCO/{year}_Season/Split_1"))
        tournaments.append((f"LCO {year} Split 1 Playoffs", f"LCO/{year}_Season/Split_1_Playoffs"))
        tournaments.append((f"LCO {year} Split 2", f"LCO/{year}_Season/Split_2"))
        tournaments.append((f"LCO {year} Split 2 Playoffs", f"LCO/{year}_Season/Split_2_Playoffs"))

    # ========================================================================
    # RIFT RIVALS - MINOR REGIONS ONLY
    # ========================================================================
    # Rift Rivals: Latin America (LAN-LAS-BR / LLA-CBLOL)
    for year in range(2017, 2020):
        tournaments.append((f"Rift Rivals {year} LAN-LAS-BR", f"Rift_Rivals/{year}_Season/LAN-LAS-BR"))

    # Rift Rivals: SEA (GPL/VCS/PCS teams)
    for year in range(2017, 2020):
        tournaments.append((f"Rift Rivals {year} SEA", f"Rift_Rivals/{year}_Season/SEA"))

    # Rift Rivals: TCL-CIS (Turkey-Russia)
    for year in range(2017, 2020):
        tournaments.append((f"Rift Rivals {year} TCL-CIS", f"Rift_Rivals/{year}_Season/TCL-CIS"))

    # Rift Rivals: OCE-SEA (falls vorhanden)
    for year in range(2017, 2019):
        tournaments.append((f"Rift Rivals {year} OCE-SEA", f"Rift_Rivals/{year}_Season/OCE-SEA"))

    # ========================================================================
    # ALL-STAR EVENTS - MINOR REGION SPECIFIC
    # ========================================================================
    # All-Star: Separate minor region events (falls vorhanden)
    for year in range(2014, 2024):
        tournaments.append((f"All-Star {year} Wildcard", f"All-Star/{year}_Season/Wildcard"))
        tournaments.append((f"All-Star {year} IWC", f"All-Star/{year}_Season/IWC"))

    # ========================================================================
    # IWC (INTERNATIONAL WILDCARD) EVENTS
    # ========================================================================
    # IWC Tournaments (vor Play-Ins)
    for year in range(2013, 2016):
        tournaments.append((f"IWC {year}", f"IWC/{year}_Season/Main_Event"))
        tournaments.append((f"IWCI {year}", f"IWCI/{year}_Season/Main_Event"))  # IWC Invitational

    # ========================================================================
    # MSI/WORLDS PLAY-IN (nur wenn minor region only)
    # ========================================================================
    # Play-In Stage (2017+) - könnte minor regions enthalten
    for year in range(2017, 2025):
        tournaments.append((f"MSI {year} Play-In", f"MSI/{year}_Season/Play-In"))
        tournaments.append((f"Worlds {year} Play-In", f"Worlds/{year}_Season/Play-In"))

    # ========================================================================
    # REGIONAL FINALS - MINOR REGIONS
    # ========================================================================
    # Wildcard Regional Finals
    for year in range(2014, 2017):
        tournaments.append((f"IWCQ {year}", f"IWCQ/{year}_Season/Main_Event"))

    # ========================================================================
    # ANDERE INTERNATIONALE MINOR REGION EVENTS
    # ========================================================================
    # Copa Latinoamérica (Latin America Cup)
    for year in range(2013, 2016):
        tournaments.append((f"Copa Latinoamérica {year}", f"Copa_Latinoamérica/{year}_Season/Main_Event"))

    # SEA Regional Championships
    for year in range(2013, 2018):
        tournaments.append((f"GPL Finals {year}", f"GPL/{year}_Season/Finals"))
        tournaments.append((f"GPL Playoffs {year}", f"GPL/{year}_Season/Playoffs"))

    # Demacia Cup für TCL/VCS/etc (falls relevant)
    for year in range(2015, 2020):
        tournaments.append((f"TCL vs VCS {year}", f"TCL_vs_VCS/{year}_Season/Main_Event"))

    return tournaments


def print_tournament_list():
    """Print organized tournament list"""
    tournaments = generate_minor_region_tournaments()

    print("=" * 100)
    print("MINOR REGION TOURNAMENTS - NUR HAUPTLIGEN & INTERNATIONALE EVENTS")
    print("=" * 100)
    print(f"\nInsgesamt: {len(tournaments)} Events")
    print()

    # Organize by category
    categories = {
        "2025 Seasons": [],
        "LAS (2013-2018)": [],
        "LCO (2021-2025)": [],
        "Rift Rivals": [],
        "All-Star Wildcard": [],
        "IWC/IWCI": [],
        "MSI/Worlds Play-In": [],
        "Regional Finals": [],
        "Other International": []
    }

    for name, url in tournaments:
        if "2025" in name and ("CBLOL" in name or "LLA" in name):
            categories["2025 Seasons"].append((name, url))
        elif "LAS" in name:
            categories["LAS (2013-2018)"].append((name, url))
        elif "LCO" in name:
            categories["LCO (2021-2025)"].append((name, url))
        elif "Rift Rivals" in name:
            categories["Rift Rivals"].append((name, url))
        elif "All-Star" in name:
            categories["All-Star Wildcard"].append((name, url))
        elif "IWC" in name:
            categories["IWC/IWCI"].append((name, url))
        elif "Play-In" in name:
            categories["MSI/Worlds Play-In"].append((name, url))
        elif "IWCQ" in name:
            categories["Regional Finals"].append((name, url))
        else:
            categories["Other International"].append((name, url))

    for category, events in categories.items():
        if events:
            print()
            print("=" * 100)
            print(f"{category} ({len(events)} Events)")
            print("=" * 100)

            for name, url in events:
                url_display = url.replace('_', ' ')
                print(f"  • {name:70} | {url_display}")

    print()
    print("=" * 100)
    print("ZUSAMMENFASSUNG")
    print("=" * 100)
    total = sum(len(events) for events in categories.values())
    print(f"Gesamt: {total} zusätzliche Events")
    print()
    for category, events in categories.items():
        if events:
            print(f"  {len(events):3} - {category}")


if __name__ == "__main__":
    print_tournament_list()
