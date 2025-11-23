#!/usr/bin/env python3
"""
Simple script to show all teams from database
Works without sqlite3 command-line tool
"""

import sqlite3
import sys

db_path = "db/elo_system.db"

if len(sys.argv) > 1:
    db_path = sys.argv[1]

print(f"Opening database: {db_path}\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get database stats
    cursor.execute("SELECT COUNT(*) FROM teams")
    total_teams = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM matches")
    total_matches = cursor.fetchone()[0]

    print(f"Total teams: {total_teams}")
    print(f"Total matches: {total_matches}")
    print("\n" + "="*70)
    print(f"{'Team Name':<50} {'Matches':>10}")
    print("="*70)

    # Get teams with match counts
    cursor.execute("""
        SELECT t.name, COUNT(*) as match_count
        FROM teams t
        LEFT JOIN matches m ON (m.team1_id = t.id OR m.team2_id = t.id)
        GROUP BY t.name
        ORDER BY match_count DESC
    """)

    teams = cursor.fetchall()

    for name, count in teams:
        print(f"{name:<50} {count:>10}")

    conn.close()

    print("\n" + "="*70)
    print(f"\nCopy this output and share it!")

except sqlite3.Error as e:
    print(f"Error: {e}")
except FileNotFoundError:
    print(f"Database file not found: {db_path}")
    print("Please provide the correct path:")
    print("  python show_teams.py <path_to_database>")
