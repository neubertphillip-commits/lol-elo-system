#!/usr/bin/env python3
"""
Helper script to find database files and show their contents
"""
import os
import sys
from pathlib import Path

print("="*80)
print("DATABASE FINDER")
print("="*80)

# Search for database files
print("\nSearching for database files...")

search_paths = [
    Path.cwd(),
    Path.home(),
    Path("/home/user/lol-elo-system"),
]

found_dbs = []

for search_path in search_paths:
    if search_path.exists():
        for ext in [".db", ".sqlite", ".sqlite3"]:
            for db_file in search_path.rglob(f"*{ext}"):
                if db_file.stat().st_size > 0:
                    found_dbs.append(db_file)

if found_dbs:
    print(f"\nFound {len(found_dbs)} database file(s):")
    for db in found_dbs:
        size_mb = db.stat().st_size / (1024 * 1024)
        print(f"  - {db} ({size_mb:.2f} MB)")
else:
    print("\nNo database files found.")
    print("\nWhere is your database with 13,000 matches?")
    print("Please provide the full path.")
