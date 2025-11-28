#!/usr/bin/env python3
"""
Compare Minor Region events with Major Region events to avoid duplicates
"""

def main():
    print("=" * 100)
    print("VERGLEICH: MAJOR REGIONS vs MINOR REGIONS EVENTS")
    print("=" * 100)
    print()

    # Events ALREADY in Major Regions Script
    already_in_major = {
        "MSI/Worlds Play-In (2017-2024)": [
            "MSI 2017-2024 Play-In",
            "Worlds 2017-2024 Play-In"
        ],
        "Rift Rivals (Major Regions)": [
            "Rift Rivals 2017-2019 NA-EU",
            "Rift Rivals 2017-2019 LCK-LPL-LMS(-VCS)"
        ],
        "All-Star Events": [
            "❌ NOT IN MATCHSCHEDULE (commented out in major script)"
        ]
    }

    # Events UNIQUE to Minor Regions (not in major script)
    unique_to_minor = {
        "2025 Seasons": [
            "CBLOL 2025 Split 1 & 2 + Playoffs (4 events)",
            "LLA 2025 Opening & Closing + Playoffs (4 events)"
        ],
        "Main Regional Leagues": [
            "LAS 2013-2018 Opening & Closing + Playoffs (22 events)",
            "LCO 2021-2025 Split 1 & 2 + Playoffs (20 events)"
        ],
        "Rift Rivals (Minor Regions ONLY)": [
            "Rift Rivals 2017-2019 LAN-LAS-BR (3 events)",
            "Rift Rivals 2017-2019 SEA (3 events)",
            "Rift Rivals 2017-2019 TCL-CIS (3 events)",
            "Rift Rivals 2017-2018 OCE-SEA (2 events)"
        ],
        "IWC (International Wildcard)": [
            "IWC 2013-2015 (3 events)",
            "IWCI 2013-2015 (3 events)",
            "IWCQ 2014-2016 (3 events)"
        ],
        "Regional Cups & Finals": [
            "Copa Latinoamérica 2013-2015 (3 events)",
            "GPL Finals 2013-2017 (5 events)",
            "GPL Playoffs 2013-2017 (5 events)",
            "TCL vs VCS 2015-2019 (5 events)"
        ]
    }

    print("🔴 BEREITS IN MAJOR REGIONS SCRIPT (nicht nochmal hinzufügen):")
    print("=" * 100)
    for category, events in already_in_major.items():
        print(f"\n{category}:")
        for event in events:
            print(f"  ❌ {event}")

    print()
    print()
    print("✅ UNIQUE FÜR MINOR REGIONS (hinzufügen!):")
    print("=" * 100)

    total_unique = 0
    for category, events in unique_to_minor.items():
        print(f"\n{category}:")
        category_count = 0
        for event in events:
            # Extract count if present
            import re
            count_match = re.search(r'\((\d+) events?\)', event)
            if count_match:
                category_count += int(count_match.group(1))
            else:
                category_count += 1
            print(f"  ✅ {event}")
        print(f"     Subtotal: {category_count} events")
        total_unique += category_count

    print()
    print("=" * 100)
    print("ZUSAMMENFASSUNG")
    print("=" * 100)
    print(f"✅ Unique Minor Region Events: {total_unique}")
    print()
    print("EMPFEHLUNG:")
    print("  1. MSI/Worlds Play-In: ❌ NICHT hinzufügen (schon in Major Regions)")
    print("  2. Rift Rivals NA-EU, LCK-LPL-LMS: ❌ NICHT hinzufügen (schon in Major Regions)")
    print("  3. All-Star: ❌ NICHT hinzufügen (nicht in MatchSchedule verfügbar)")
    print()
    print(f"  4. Restliche {total_unique} Events: ✅ ZUR MINOR REGIONS LISTE HINZUFÜGEN")
    print()
    print("FINALE LISTE:")
    print("  • 2025 Seasons: 8 events")
    print("  • LAS + LCO: 42 events")
    print("  • Rift Rivals (minor only): 11 events")
    print("  • IWC/IWCI/IWCQ: 9 events")
    print("  • Regional Cups: 18 events")
    print(f"  TOTAL: {total_unique} zusätzliche Events")

if __name__ == "__main__":
    main()
