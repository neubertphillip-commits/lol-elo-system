# Quick Start: Team Name Mapping

## 🚀 Schnellstart für 13,000 Matches

### 1. Automatisches Bulk-Mapping (empfohlen)

```bash
python generate_bulk_mappings.py
```

Dann:
- Minimum matches: `10` eingeben
- Option wählen: `3` (beide: export + merge)
- Bei "Speichern?": `y`

✅ **Ergebnis**: 80-90% aller Teams automatisch gemappt!

---

### 2. Restliche Teams analysieren

```bash
python analyze_team_mappings.py
```

Dann:
- Option wählen: `1` (interaktiver Modus)
- Für jedes unmapped Team:
  - `alias` - wenn es zu bestehendem Team gehört
  - `new` - wenn es ein neues Team ist
  - `skip` - überspringen
- Am Ende: `s` (save) oder `q` (quit)

---

### 3. Fertig! 🎉

Deine Mappings sind jetzt in `config/team_name_mappings.json`

---

## Beispiel-Workflow

```bash
# Schritt 1: Bulk-Mapping
$ python generate_bulk_mappings.py
Minimum matches: 10
Wähle [1/2/3/4]: 3
Merge? [y/n]: y
✓ Gespeichert!

# Schritt 2: Überprüfen
$ python analyze_team_mappings.py
Total: 250 teams
✓ Mapped: 220 (88%)
⚠ Unmapped: 30 (12%)

# Schritt 3: Wichtige Teams manuell mappen
Option [1/2/3]: 1
Team: "SKT T1 K" (45 matches)
  Ähnliche: T1 (95%)
[alias/new/skip]: alias
Zu welchem Team?: T1
✓ Alias hinzugefügt

# Fertig!
```

---

## Quick Tips

### Wenn du unsicher bist:

- **Alias oder New?**
  - Ist es eine Variation eines bekannten Teams? → `alias`
  - Ist es ein komplett anderes Team? → `new`

- **Welcher canonical name?**
  - Nutze den modernen/aktuellen Namen
  - Bei Rebrands: Neuer Name = canonical

- **Region?**
  - CN = China (LPL)
  - KR = Korea (LCK)
  - EU = Europa (LEC)
  - NA = Nordamerika (LCS)

### Häufige Rebrands:

| Alt                  | Neu      |
|----------------------|----------|
| SK Telecom T1        | T1       |
| Samsung Galaxy       | Gen.G    |
| Longzhu Gaming       | DRX      |
| Moscow Five          | Gambit   |

---

## Probleme?

### "Database not found"
→ Import zuerst Daten:
```bash
python major_regions_tournament_import_matchschedule.py
```

### "Too many unmapped teams"
→ Reduziere minimum matches in bulk generator (z.B. 5 statt 10)

### "Wrong mapping"
→ Editiere `config/team_name_mappings.json` manuell

---

Mehr Details: Siehe **TEAM_MAPPING_GUIDE.md**
