#!/usr/bin/env python3
"""
Test Team Name Mappings
Quick test script to verify team name resolution works correctly
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.team_name_resolver import TeamNameResolver


def test_common_teams():
    """Test mapping of common teams and their variations"""

    resolver = TeamNameResolver()

    print("="*80)
    print("TEAM NAME MAPPING TEST")
    print("="*80)

    # Test cases: (input, expected_canonical)
    test_cases = [
        # Korean teams
        ("SK Telecom T1", "T1"),
        ("SKT", "T1"),
        ("SKT T1", "T1"),
        ("T1", "T1"),

        # Gen.G (rebrand history)
        ("Samsung Galaxy", "Gen.G"),
        ("GenG", "Gen.G"),
        ("Gen.G Esports", "Gen.G"),
        ("KSV", "Gen.G"),

        # European teams
        ("G2", "G2 Esports"),
        ("G2 LoL", "G2 Esports"),
        ("Fnatic", "Fnatic"),
        ("FNC", "Fnatic"),

        # North American teams
        ("TSM", "TSM"),
        ("Team SoloMid", "TSM"),
        ("C9", "Cloud9"),
        ("Cloud 9", "Cloud9"),
        ("TL", "Team Liquid"),

        # Chinese teams
        ("EDG", "EDward Gaming"),
        ("RNG", "Royal Never Give Up"),
        ("JDG", "JD Gaming"),

        # Brazilian teams
        ("LLL", "LOUD"),
        ("Los Loud", "LOUD"),

        # With suffixes (should be normalized)
        ("Fnatic Esports", "Fnatic"),
        ("G2 Esports LoL", "G2 Esports"),
    ]

    print("\n" + "="*80)
    print("RESOLUTION TESTS")
    print("="*80)
    print(f"\n{'Input':<30} {'Expected':<25} {'Got':<25} {'Status'}")
    print("-"*95)

    passed = 0
    failed = 0
    fuzzy = 0

    for input_name, expected in test_cases:
        resolved = resolver.resolve(input_name, source="test")

        # Check if it matches exactly or via fuzzy matching
        if resolved == expected:
            status = "✓ PASS"
            passed += 1
        elif resolved in resolver.canonical_teams:
            status = "⚠️ FUZZY"
            fuzzy += 1
        else:
            status = "✗ FAIL"
            failed += 1

        print(f"{input_name:<30} {expected:<25} {resolved:<25} {status}")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total = len(test_cases)
    print(f"\nTotal tests:    {total}")
    print(f"✓ Passed:       {passed} ({passed/total*100:.1f}%)")
    print(f"⚠️ Fuzzy match:  {fuzzy} ({fuzzy/total*100:.1f}%)")
    print(f"✗ Failed:       {failed} ({failed/total*100:.1f}%)")

    # Stats
    print("\n" + "="*80)
    print("RESOLVER STATISTICS")
    print("="*80)
    stats = resolver.get_stats()
    print(f"\nCanonical teams: {stats['canonical_teams']}")
    print(f"Total mappings:  {stats['total_mappings']}")
    print(f"Cache size:      {stats['cache_size']}")

    return passed, failed, fuzzy


def demo_fuzzy_matching():
    """Demonstrate fuzzy matching capabilities"""

    resolver = TeamNameResolver()

    print("\n" + "="*80)
    print("FUZZY MATCHING DEMONSTRATION")
    print("="*80)

    # Slightly different variations
    test_variations = [
        "T 1",
        "Gen G",
        "Cloud 9",
        "Fnatic LoL",
        "Team Liquid Esports",
        "SK Telecom T1 LoL",
    ]

    print("\n" + f"{'Input':<30} {'Resolved':<30} {'Confidence'}")
    print("-"*80)

    for name in test_variations:
        fuzzy_result = resolver.fuzzy_match(name)

        if fuzzy_result:
            canonical, confidence = fuzzy_result
            print(f"{name:<30} {canonical:<30} {confidence:.1%}")
        else:
            print(f"{name:<30} {'No match':<30} -")


def interactive_test():
    """Interactive mode for testing custom team names"""

    resolver = TeamNameResolver()

    print("\n" + "="*80)
    print("INTERACTIVE TESTING MODE")
    print("="*80)
    print("\nGib Team-Namen ein zum Testen (oder 'quit' zum Beenden)\n")

    while True:
        name = input("Team name: ").strip()

        if not name or name.lower() in ['quit', 'q', 'exit']:
            break

        resolved = resolver.resolve(name, source="interactive")
        print(f"  → Resolved to: {resolved}")

        # Show fuzzy match details
        fuzzy_result = resolver.fuzzy_match(name)
        if fuzzy_result:
            canonical, confidence = fuzzy_result
            print(f"  → Fuzzy match: {canonical} (confidence: {confidence:.1%})")

        print()


if __name__ == "__main__":
    # Run automated tests
    passed, failed, fuzzy = test_common_teams()

    # Show fuzzy matching demo
    demo_fuzzy_matching()

    # Check if tests passed
    if failed > 0:
        print(f"\n⚠️  {failed} tests failed!")
        print("   Check config/team_name_mappings.json for missing or incorrect mappings")

    # Offer interactive mode
    print("\n" + "="*80)
    choice = input("\nStarte interaktiven Test-Modus? [y/n]: ").strip().lower()

    if choice == 'y':
        interactive_test()

    print("\n✓ Tests abgeschlossen!")
