"""
Simple Table Overview: What you have vs. what's expected
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import DatabaseManager


def print_table():
    """Print simple table of what's imported vs expected"""

    db = DatabaseManager()
    cursor = db.conn.cursor()

    # Get total
    cursor.execute('SELECT COUNT(*) FROM matches')
    total = cursor.fetchone()[0]

    print()
    print("="*80)
    print(f"OVERVIEW: {total} Matches in Database")
    print("="*80)
    print()

    # Regional Leagues
    leagues = [
        ('LEC', 'EU LCS', 2014, 2024, 100),
        ('LPL', 'LPL', 2013, 2024, 120),
        ('LCK', 'LCK', 2016, 2024, 90),
        ('LCS', 'NA LCS', 2014, 2024, 90),
    ]

    print("REGIONAL LEAGUES:")
    print("-" * 80)
    print(f"{'Liga':<8} {'Jahr':<6} {'Split':<8} {'Erwartet':<10} {'Vorhanden':<10} {'Status':<10}")
    print("-" * 80)

    for league, db_name, start_year, end_year, expected_per_split in leagues:
        for year in range(start_year, end_year + 1):
            for split in ['Spring', 'Summer']:
                # Query database
                cursor.execute('''
                    SELECT COUNT(m.id)
                    FROM matches m
                    JOIN tournaments t ON m.tournament_id = t.id
                    WHERE (t.name LIKE ? OR t.name LIKE ?)
                    AND t.name LIKE ?
                    AND t.name LIKE ?
                ''', (f'%{league}%', f'%{db_name}%', f'%{year}%', f'%{split}%'))

                actual = cursor.fetchone()[0]

                # Determine status
                if actual == 0:
                    status = "❌ FEHLT"
                elif actual < expected_per_split * 0.8:
                    status = f"⚠️  {actual}"
                else:
                    status = f"✅ {actual}"

                # Only show if missing or partial
                if actual == 0 or actual < expected_per_split * 0.8:
                    print(f"{league:<8} {year:<6} {split:<8} {expected_per_split:<10} {actual:<10} {status:<10}")

    print()
    print("INTERNATIONAL TOURNAMENTS:")
    print("-" * 80)
    print(f"{'Turnier':<15} {'Jahr':<6} {'Erwartet':<10} {'Vorhanden':<10} {'Status':<10}")
    print("-" * 80)

    # MSI
    for year in range(2015, 2025):
        expected = 50 if year >= 2017 else 20

        cursor.execute('''
            SELECT COUNT(m.id)
            FROM matches m
            JOIN tournaments t ON m.tournament_id = t.id
            WHERE t.name LIKE ?
            AND t.name LIKE ?
        ''', (f'%Mid-Season%', f'%{year}%'))

        actual = cursor.fetchone()[0]

        if actual == 0:
            status = "❌ FEHLT"
        elif actual < expected * 0.6:
            status = f"⚠️  {actual}"
        else:
            status = f"✅ {actual}"

        if actual < expected * 0.6:
            print(f"{'MSI':<15} {year:<6} {expected:<10} {actual:<10} {status:<10}")

    # Worlds
    for year in range(2013, 2025):
        expected = 80 if year >= 2018 else 60

        cursor.execute('''
            SELECT COUNT(m.id)
            FROM matches m
            JOIN tournaments t ON m.tournament_id = t.id
            WHERE t.name LIKE ?
            AND t.name LIKE ?
        ''', (f'%World%', f'%{year}%'))

        actual = cursor.fetchone()[0]

        if actual == 0:
            status = "❌ FEHLT"
        elif actual < expected * 0.6:
            status = f"⚠️  {actual}"
        else:
            status = f"✅ {actual}"

        if actual < expected * 0.6:
            print(f"{'Worlds':<15} {year:<6} {expected:<10} {actual:<10} {status:<10}")

    print()
    print("="*80)
    print("SUMMARY BY LEAGUE:")
    print("="*80)
    print(f"{'Liga':<10} {'Matches':<10} {'Erwartete':<12} {'Coverage':<10}")
    print("-" * 80)

    summaries = [
        ('LEC', 2200),
        ('LPL', 3200),
        ('LCK', 2700),
        ('LCS', 2200),
        ('MSI', 400),
        ('Worlds', 900),
    ]

    for league, expected_total in summaries:
        if league == 'LEC':
            search_terms = ['%LEC%', '%EU LCS%']
        elif league == 'LCS':
            search_terms = ['%LCS%', '%NA LCS%']
        elif league == 'MSI':
            search_terms = ['%Mid-Season%']
        elif league == 'Worlds':
            search_terms = ['%World%']
        else:
            search_terms = [f'%{league}%']

        # Build query
        conditions = ' OR '.join(['t.name LIKE ?' for _ in search_terms])
        query = f'''
            SELECT COUNT(m.id)
            FROM matches m
            JOIN tournaments t ON m.tournament_id = t.id
            WHERE {conditions}
        '''

        cursor.execute(query, search_terms)
        actual_total = cursor.fetchone()[0]

        coverage = (actual_total / expected_total * 100) if expected_total > 0 else 0

        if coverage >= 80:
            status_icon = "✅"
        elif coverage >= 50:
            status_icon = "⚠️ "
        else:
            status_icon = "❌"

        print(f"{status_icon} {league:<8} {actual_total:<10} {expected_total:<12} {coverage:>5.1f}%")

    print("="*80)
    print()

    # Overall summary
    total_expected = sum(s[1] for s in summaries)
    overall_coverage = (total / total_expected * 100) if total_expected > 0 else 0

    print(f"GESAMT: {total} / {total_expected} Matches ({overall_coverage:.1f}% Coverage)")
    print()

    if overall_coverage >= 90:
        print("✅ Import ist vollständig!")
    elif overall_coverage >= 70:
        print("⚠️  Import ist fast vollständig, aber es fehlen noch einige Daten")
    else:
        print("❌ Import ist noch nicht vollständig - lass den Import weiterlaufen!")

    print()


if __name__ == '__main__':
    print_table()
