#!/usr/bin/env python3
"""
Check which events are at index 296+ in the original tournament list
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Import the tournament generation function
from minor_regions_tournament_discovery_matchschedule import generate_all_tournaments

def main():
    # Generate the full tournament list
    tournaments = generate_all_tournaments()

    print("=" * 100)
    print(f"EVENTS AB INDEX 296 (von insgesamt {len(tournaments)} Events)")
    print("=" * 100)
    print()

    # Show events from index 295 (296th event, 0-indexed) onwards
    if len(tournaments) > 295:
        print(f"Zeige Events {296}-{len(tournaments)}:\n")

        for i in range(295, len(tournaments)):
            name, url = tournaments[i]
            url_with_spaces = url.replace('_', ' ')
            print(f"Event {i+1:3}: {name:70} | URL: {url_with_spaces}")
    else:
        print(f"Die Liste hat nur {len(tournaments)} Events, es gibt keine Events ab Index 296.")

    print()
    print("=" * 100)
    print("VERGLEICH MIT DISCOVERY RESULTS")
    print("=" * 100)
    print()

    # Load discovery results
    results_file = Path(__file__).parent / 'minor_regions_discovery_results.json'
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    print(f"Discovery Results:")
    print(f"  - Total getestet: {results['summary']['total']}")
    print(f"  - Gefunden: {results['summary']['found']}")
    print(f"  - Nicht gefunden: {results['summary']['not_found']}")
    print()

    if len(tournaments) > results['summary']['total']:
        print(f"⚠️  ACHTUNG: Es gibt {len(tournaments) - results['summary']['total']} Events mehr in der Liste als getestet wurden!")
        print()
        print("Nicht getestete Events:")
        for i in range(results['summary']['total'], len(tournaments)):
            name, url = tournaments[i]
            url_with_spaces = url.replace('_', ' ')
            print(f"  Event {i+1:3}: {name:70} | URL: {url_with_spaces}")
    elif len(tournaments) < results['summary']['total']:
        print(f"⚠️  WARNUNG: Mehr Events getestet ({results['summary']['total']}) als in der Liste ({len(tournaments)})")
    else:
        print(f"✅ Alle {len(tournaments)} Events aus der Liste wurden getestet.")

if __name__ == "__main__":
    main()
