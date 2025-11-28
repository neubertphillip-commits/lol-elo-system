#!/usr/bin/env python3
"""
Analyze missing events from minor regions discovery results
"""
import json
from pathlib import Path

def main():
    # Load results
    results_file = Path(__file__).parent / 'minor_regions_discovery_results.json'
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("=" * 100)
    print("FEHLENDE EVENTS - KOMPLETTE LISTE")
    print("=" * 100)
    print(f"\nTotal: {data['summary']['not_found']} fehlende Events\n")

    missing = data['not_found']

    for i, event in enumerate(missing, 1):
        print(f"{i:3}. {event['name']:70} | URL: {event['url']}")

    print("\n" + "=" * 100)
    print("EVENTS AB INDEX 296 (in der Gesamt-Liste)")
    print("=" * 100)
    print()

    # Get all events (found + not found) from original order
    found = data['found']
    total_events = found + missing  # This won't preserve original order

    print(f"Hinweis: Die Discovery-Liste enthält insgesamt {data['summary']['total']} Events.")
    print(f"Die letzten Events in der Found-Liste sind:")
    print()

    # Show last 50 found events (assuming events 296+ are mostly found)
    start_idx = max(0, len(found) - 50)
    for i in range(start_idx, len(found)):
        event = found[i]
        print(f"Event {i+1:3}: {event['name']:70} | Matches: {event.get('sample_matches', 0)}")

    print("\n" + "=" * 100)
    print("KATEGORISIERUNG DER FEHLENDEN EVENTS")
    print("=" * 100)
    print()

    # Categorize missing events
    categories = {}
    for event in missing:
        league = event['name'].split()[0]
        if league not in categories:
            categories[league] = []
        categories[league].append(event)

    for league, events in sorted(categories.items()):
        print(f"\n{league}: {len(events)} fehlende Events")
        print("-" * 100)
        for event in events:
            print(f"  • {event['name']:70} | URL: {event['url']}")

if __name__ == "__main__":
    main()
