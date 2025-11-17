"""
Import Coverage Report
Shows what SHOULD be imported vs what IS imported
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import DatabaseManager


def get_expected_coverage():
    """Define expected coverage for all leagues and years"""

    expected = {}

    # Regional Leagues
    regional_leagues = {
        'LEC': (2013, 2024, ['Spring', 'Summer']),
        'LPL': (2013, 2024, ['Spring', 'Summer']),
        'LCK': (2013, 2024, ['Spring', 'Summer']),
        'LCS': (2013, 2024, ['Spring', 'Summer']),
    }

    for league, (start, end, splits) in regional_leagues.items():
        for year in range(start, end + 1):
            for split in splits:
                key = f"{league}/{year}/{split}"
                expected[key] = {
                    'league': league,
                    'year': year,
                    'split': split,
                    'type': 'Regional'
                }

    # International Tournaments
    for year in range(2015, 2025):
        key = f"MSI/{year}"
        expected[key] = {
            'league': 'MSI',
            'year': year,
            'split': 'Main Event',
            'type': 'International'
        }

    for year in range(2013, 2025):
        key = f"WORLDS/{year}"
        expected[key] = {
            'league': 'WORLDS',
            'year': year,
            'split': 'Main Event',
            'type': 'International'
        }

    return expected


def get_actual_coverage():
    """Get actual imported data from database"""

    db = DatabaseManager()
    cursor = db.conn.cursor()

    # Get all tournaments with their match counts
    cursor.execute('''
        SELECT
            t.name,
            COUNT(m.id) as match_count
        FROM tournaments t
        LEFT JOIN matches m ON m.tournament_id = t.id
        GROUP BY t.name
        HAVING match_count > 0
        ORDER BY t.name
    ''')

    actual = {}
    for row in cursor.fetchall():
        tournament_name = row[0]
        match_count = row[1]

        # Parse tournament name to extract league/year/split
        # Examples: "LEC/2022 Season/Spring Season", "MSI/2023"
        actual[tournament_name] = match_count

    return actual


def generate_report():
    """Generate import coverage report"""

    print('=' * 100)
    print('IMPORT COVERAGE REPORT')
    print('=' * 100)
    print()
    print('Zeigt was SOLLTE importiert werden vs. was IST importiert')
    print()

    expected = get_expected_coverage()
    actual = get_actual_coverage()

    # Get database stats
    db = DatabaseManager()
    cursor = db.conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM matches')
    total_matches = cursor.fetchone()[0]

    cursor.execute('''
        SELECT strftime('%Y', date) as year, COUNT(*) as count
        FROM matches
        GROUP BY year
        ORDER BY year DESC
    ''')

    print('=' * 100)
    print('AKTUELLER STATUS')
    print('=' * 100)
    print(f'Total Matches in DB: {total_matches}')
    print()
    print('Matches pro Jahr:')
    for row in cursor.fetchall():
        year = row[0] if row[0] else 'Unknown'
        count = row[1]
        bar = '█' * (count // 20)
        print(f'  {year}: {count:4d} {bar}')

    print()
    print('=' * 100)
    print('COVERAGE BY LEAGUE')
    print('=' * 100)
    print()

    # Group by league
    leagues = ['LEC', 'LPL', 'LCK', 'LCS', 'MSI', 'WORLDS']

    for league in leagues:
        print(f'--- {league} ---')

        # Count expected
        expected_count = sum(1 for k in expected.keys() if k.startswith(league))

        # Count actual (rough estimate based on tournament names)
        actual_tournaments = [name for name in actual.keys() if league in name or
                            (league == 'LEC' and 'EU LCS' in name)]
        actual_count = len(actual_tournaments)
        actual_matches = sum(actual[t] for t in actual_tournaments)

        coverage_pct = (actual_count / expected_count * 100) if expected_count > 0 else 0

        status = '✓' if coverage_pct > 80 else '⚠' if coverage_pct > 20 else '✗'

        print(f'  {status} Coverage: {coverage_pct:.1f}% ({actual_count}/{expected_count} seasons)')
        print(f'     Matches: {actual_matches}')

        if coverage_pct < 100 and actual_count > 0:
            print(f'     Importierte Seasons: {actual_count}')
            if actual_count < 5:
                for t in actual_tournaments[:5]:
                    print(f'       - {t}: {actual[t]} matches')

        print()

    print('=' * 100)
    print('MISSING DATA')
    print('=' * 100)
    print()

    # Check which data is missing
    missing_by_league = {league: [] for league in leagues}

    for league in ['LEC', 'LPL', 'LCK', 'LCS']:
        for year in range(2013, 2025):
            for split in ['Spring', 'Summer']:
                # Check if we have this season
                found = any(
                    league in name and str(year) in name and split in name
                    for name in actual.keys()
                )

                if league == 'LEC' and year < 2019:
                    # LEC was EU LCS before 2019
                    found = any(
                        'EU LCS' in name and str(year) in name and split in name
                        for name in actual.keys()
                    )

                if not found:
                    missing_by_league[league].append(f'{year} {split}')

    # Check MSI
    for year in range(2015, 2025):
        found = any('MSI' in name and str(year) in name for name in actual.keys())
        if not found:
            missing_by_league['MSI'].append(str(year))

    # Check Worlds
    for year in range(2013, 2025):
        found = any('World' in name and str(year) in name for name in actual.keys())
        if not found:
            missing_by_league['WORLDS'].append(str(year))

    for league in leagues:
        missing = missing_by_league[league]
        if missing:
            print(f'{league}:')
            print(f'  Fehlend: {len(missing)} seasons')
            if len(missing) <= 10:
                for item in missing:
                    print(f'    - {item}')
            else:
                print(f'    First 10: {", ".join(missing[:10])}')
                print(f'    ... und {len(missing) - 10} mehr')
            print()

    print('=' * 100)
    print('ZUSAMMENFASSUNG')
    print('=' * 100)
    print()

    total_expected = len(expected)
    total_actual_seasons = sum(1 for league in leagues for _ in missing_by_league[league])
    total_imported_seasons = total_expected - total_actual_seasons

    overall_coverage = (total_imported_seasons / total_expected * 100) if total_expected > 0 else 0

    print(f'Erwartete Seasons:   {total_expected}')
    print(f'Importierte Seasons: {total_imported_seasons}')
    print(f'Fehlende Seasons:    {total_actual_seasons}')
    print(f'Coverage:            {overall_coverage:.1f}%')
    print()

    if overall_coverage < 50:
        print('⚠ STATUS: Import läuft noch oder ist unvollständig')
        print('  → Lass den Import weiterlaufen mit ./start_import.ps1')
    elif overall_coverage < 90:
        print('⚠ STATUS: Import größtenteils vollständig, aber es fehlen noch Daten')
        print('  → Prüfe ob der Import-Prozess noch läuft')
    else:
        print('✓ STATUS: Import vollständig!')

    print()
    print('=' * 100)


if __name__ == '__main__':
    generate_report()
