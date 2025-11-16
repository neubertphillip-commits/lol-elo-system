#!/bin/bash
# Monitor import progress every 5 minutes

INTERVAL=300  # 5 minutes in seconds

echo "=========================================="
echo "Import Monitor - Updates alle 5 Minuten"
echo "=========================================="
echo ""
echo "Drücke Ctrl+C zum Beenden"
echo ""

while true; do
    # Current timestamp
    echo ""
    echo "=========================================="
    date '+%Y-%m-%d %H:%M:%S'
    echo "=========================================="
    echo ""

    # Check if process is running
    if ps aux | grep -q "[p]ython.*import_all_historical_data"; then
        echo "✓ Import-Prozess läuft"
        PID=$(ps aux | grep "[p]ython.*import_all_historical_data" | awk '{print $2}')
        echo "  Process ID: $PID"
    else
        echo "✗ Import-Prozess läuft NICHT"
        echo "  Import könnte beendet sein!"
    fi
    echo ""

    # Database stats
    python3 << 'EOF'
from core.database import DatabaseManager

db = DatabaseManager()
cursor = db.conn.cursor()

# Total matches
cursor.execute('SELECT COUNT(*) FROM matches')
total = cursor.fetchone()[0]
print(f'📊 Matches in DB: {total}')
print()

# Matches by year
cursor.execute('''
    SELECT strftime('%Y', date) as year, COUNT(*) as count
    FROM matches
    GROUP BY year
    ORDER BY year DESC
''')

print('Matches pro Jahr:')
for row in cursor.fetchall():
    year = row[0] if row[0] else 'Unknown'
    count = row[1]
    bar = '█' * (count // 50)
    print(f'  {year}: {count:4d} {bar}')

# Latest matches
cursor.execute('''
    SELECT t.name, COUNT(m.id)
    FROM matches m
    LEFT JOIN tournaments t ON m.tournament_id = t.id
    GROUP BY t.name
    ORDER BY MAX(m.date) DESC
    LIMIT 3
''')

print()
print('Zuletzt importierte Turniere:')
for row in cursor.fetchall():
    tournament = row[0] if row[0] else 'Unknown'
    count = row[1]
    print(f'  - {tournament}: {count} matches')
EOF

    # Last 5 lines of log
    echo ""
    echo "Letzte Log-Einträge:"
    tail -5 import_log.txt 2>/dev/null | sed 's/^/  /'

    echo ""
    echo "Nächstes Update in 5 Minuten..."
    echo "=========================================="

    # Wait 5 minutes
    sleep $INTERVAL
done
