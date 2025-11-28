#!/usr/bin/env python3
"""
Verify which events from 296-338 were found vs not found
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from minor_regions_tournament_discovery_matchschedule import generate_all_tournaments

def main():
    # Generate full list
    tournaments = generate_all_tournaments()

    # Load results
    results_file = Path(__file__).parent / 'minor_regions_discovery_results.json'
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Create lookup dictionaries
    found_names = {event['name']: event for event in results['found']}
    not_found_names = {event['name']: event for event in results['not_found']}

    print("=" * 100)
    print("DETAILLIERTE PRÜFUNG: EVENTS 296-338")
    print("=" * 100)
    print()

    found_count = 0
    not_found_count = 0

    for i in range(295, len(tournaments)):  # 295 = index for event 296
        name, url = tournaments[i]
        url_with_spaces = url.replace('_', ' ')

        if name in found_names:
            event = found_names[name]
            status = f"✅ GEFUNDEN ({event.get('sample_matches', 0)} matches)"
            found_count += 1
        elif name in not_found_names:
            status = "❌ NICHT GEFUNDEN"
            not_found_count += 1
        else:
            status = "⚠️  UNBEKANNT"

        print(f"Event {i+1:3}: {name:60} {status}")

    print()
    print("=" * 100)
    print(f"ZUSAMMENFASSUNG EVENTS 296-338 (insgesamt {len(tournaments) - 295} Events)")
    print("=" * 100)
    print(f"✅ Gefunden: {found_count}")
    print(f"❌ Nicht gefunden: {not_found_count}")
    print(f"📊 Erfolgsquote: {(found_count/(found_count+not_found_count)*100):.1f}%")

if __name__ == "__main__":
    main()
