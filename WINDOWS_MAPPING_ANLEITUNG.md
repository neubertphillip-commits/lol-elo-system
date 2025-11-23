# Team Mapping - Windows Anleitung

## Du hast 13.000 Matches auf deinem Windows-PC

Hier ist, was du tun kannst:

## Option 1: Team-Namen exportieren (einfach!)

**In PowerShell auf deinem Windows-PC:**

```powershell
cd C:\Users\chris\source\repos\lol-elo-system

# Wo ist deine Datenbank mit den 13.000 Matches?
# Ersetze den Pfad mit deiner echten Datenbank:
python export_teams_for_mapping.py C:\pfad\zu\deiner\datenbank.db
```

Das erstellt eine `teams_to_map.json` Datei mit allen Team-Namen.

**Dann:**
1. Öffne die `teams_to_map.json` Datei
2. Kopiere den Inhalt hierher (oder sag mir die Top 20-50 Teams)
3. Ich helfe dir, alle Teams zu mappen!

---

## Option 2: Datenbank kopieren

Wenn deine Datenbank die gleiche Struktur wie `elo_system.db` hat:

```powershell
# Kopiere deine Datenbank hierher:
copy C:\pfad\zu\deiner\datenbank.db C:\Users\chris\source\repos\lol-elo-system\db\elo_system.db
```

Dann kann ich direkt mit der Datenbank arbeiten.

---

## Option 3: Mir sagen, wo die Datenbank ist

Sag mir einfach:
1. **Wo** ist die Datenbank? (vollständiger Pfad)
2. **Welche Tabellen** hat sie?
3. **Welche Spalten** enthalten die Team-Namen?

Zum Beispiel:
```
Pfad: C:\Users\chris\Documents\lol_matches.db
Tabelle: matches
Spalten: team1_name, team2_name
```

Dann erstelle ich einen Import-Script für dich.

---

## Option 4: Die häufigsten Teams manuell auflisten

Wenn du mir einfach die häufigsten 20-50 Team-Namen sagst, kann ich damit anfangen:

```
1. T1 - 450 matches
2. Gen.G - 420 matches
3. EDG - 380 matches
...
```

Dann mappe ich die wichtigsten Teams zuerst!

---

## Was ist am einfachsten für dich?

Sag mir einfach, welche Option du bevorzugst, und ich helfe dir weiter! 🚀
