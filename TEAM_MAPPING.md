# Team Name Mapping Guide

Komplette Anleitung zum Mapping von Team-Namen für das ELO-System.

## 📋 Inhaltsverzeichnis

1. [Quick Start](#quick-start)
2. [Übersicht](#übersicht)
3. [Verfügbare Tools](#verfügbare-tools)
4. [Empfohlener Workflow](#empfohlener-workflow)
5. [Mapping-Struktur](#mapping-struktur)
6. [Häufige Szenarien](#häufige-szenarien)
7. [Best Practices](#best-practices)
8. [Platform-spezifische Hinweise](#platform-spezifische-hinweise)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Automatisches Bulk-Mapping (empfohlen)

```bash
python generate_bulk_mappings.py
```

**Eingaben:**
1. Minimum matches: `10` eingeben
2. Option wählen: `3` (export + merge)
3. Bei "Speichern?": `y`

**Ergebnis:** 80-90% aller Teams automatisch gemappt!

### Restliche Teams analysieren

```bash
python analyze_team_mappings.py
```

**Interaktiver Modus:**
- Option wählen: `1`
- Für jedes unmapped Team:
  - `alias` - wenn es zu bestehendem Team gehört
  - `new` - wenn es ein neues Team ist
  - `skip` - überspringen
- Am Ende: `s` (save)

### Fertig! 🎉

Deine Mappings sind jetzt in `config/team_name_mappings.json`

---

## Übersicht

### Was ist Team-Mapping?

Bei 13+ Jahren League of Legends Daten gibt es zahlreiche Team-Namen-Variationen:
- **Rebrands**: SK Telecom T1 → T1, Samsung Galaxy → Gen.G
- **Abkürzungen**: Team SoloMid → TSM, Cloud 9 → C9
- **Suffixe**: "Fnatic" vs "Fnatic LoL" vs "Fnatic Esports"

Das Mapping-System vereinheitlicht diese Namen für korrekte ELO-Berechnungen.

### Warum wichtig?

- **ELO-Kontinuität**: Ein Team muss über Rebrands hinweg konsistent sein
- **Datenqualität**: Vermeidet Duplikate und falsche Berechnungen
- **Regional Offsets**: Korrekte Region-Zuordnung für ELO-Anpassungen

---

## Verfügbare Tools

### 1. 🚀 `generate_bulk_mappings.py` - Automatische Bulk-Generierung

**Wann verwenden**: Für schnelles, automatisches Mapping großer Datenmengen.

```bash
python generate_bulk_mappings.py
```

**Features**:
- Automatische Gruppierung ähnlicher Namen
- Erkennt bekannte Rebrands (SKT → T1, Samsung → Gen.G, etc.)
- Pattern-basierte Normalisierung
- Merge mit existierenden Mappings

**Workflow**:
1. Analysiert alle Teams in der Datenbank
2. Gruppiert ähnliche Varianten automatisch
3. Generiert Mappings basierend auf Häufigkeit
4. Optionen:
   - Als neue Datei exportieren
   - Mit bestehenden Mappings mergen
   - Beides

### 2. 🔍 `analyze_team_mappings.py` - Detaillierte Analyse

**Wann verwenden**: Wenn du genau sehen willst, welche Teams bereits gemappt sind und welche noch fehlen.

```bash
python analyze_team_mappings.py
```

**Features**:
- Zeigt mapped vs. unmapped Teams
- Schlägt ähnliche Teams vor (z.B. "T1" bei "SK Telecom T1")
- Interaktiver Modus zum manuellen Mapping
- Export von unmapped Teams

**Modi**:
- **Interaktiver Modus**: Jedes Team einzeln mappen
- **Export**: Unmapped Teams als JSON exportieren
- **Statistik**: Übersicht über Mapping-Status

### 3. ⚙️ Bestehende Systeme

- **`core/team_name_resolver.py`**: Löst Team-Namen zur Laufzeit auf
- **`config/team_name_mappings.json`**: Zentrale Mapping-Konfiguration

---

## Empfohlener Workflow

### Schritt 1: Daten importieren

Falls noch nicht geschehen:

```bash
# Major Regions (LPL, LCK, LEC, LCS, International)
python major_regions_tournament_import_matchschedule.py

# Minor Regions (CBLOL, PCS, VCS, etc.)
python minor_regions_tournament_import_matchschedule.py
```

### Schritt 2: Bulk-Mapping generieren

```bash
python generate_bulk_mappings.py
```

1. Minimum matches: `10` (mappt wichtigste Teams)
2. Überprüfe die Zusammenfassung
3. Wähle Option `3` (merge mit existierenden)
4. Speichere die Mappings: `y`

**Vorteil**: Mappt automatisch 80-90% der Teams

### Schritt 3: Verbleibende Teams analysieren

```bash
python analyze_team_mappings.py
```

1. Überprüfe die unmapped Teams
2. Für wichtige Teams (viele Matches):
   - Nutze interaktiven Modus
   - Mappe sie als Alias oder neues Team

### Schritt 4: Validierung

Teste das Mapping-System:

```bash
python -c "from core.team_name_resolver import TeamNameResolver; \
r = TeamNameResolver(); \
r.print_stats(); \
print('SKT ->', r.resolve('SKT', 'test')); \
print('Samsung Galaxy ->', r.resolve('Samsung Galaxy', 'test'))"
```

### Beispiel: Kompletter Workflow

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

## Mapping-Struktur

Die `config/team_name_mappings.json` hat folgendes Format:

```json
{
  "mappings": [
    {
      "canonical_name": "T1",
      "aliases": [
        "SK Telecom T1",
        "SKT",
        "SKT T1"
      ],
      "region": "KR",
      "notes": "Korean team, formerly SK Telecom T1"
    }
  ],
  "fuzzy_matching_rules": {
    "enabled": true,
    "similarity_threshold": 0.85,
    "ignore_case": true,
    "remove_suffixes": ["LoL", "Esports", "Gaming"],
    "normalize_spaces": true
  }
}
```

### Felder erklärt:

- **canonical_name**: Der "offizielle" Name, auf den alles gemappt wird
- **aliases**: Alle Variationen dieses Team-Namens
- **region**: CN, KR, EU, NA, BR, TW, VN, JP, etc.
- **notes**: Zusätzliche Infos (Rebrands, Match-Count, etc.)

---

## Häufige Szenarien

### Szenario 1: Team-Rebrand

**Beispiel**: "Samsung Galaxy" wurde zu "Gen.G"

```json
{
  "canonical_name": "Gen.G",
  "aliases": [
    "GenG",
    "Gen.G Esports",
    "KSV",
    "Samsung Galaxy"
  ],
  "region": "KR",
  "notes": "Formerly Samsung Galaxy (2017), then KSV (2018)"
}
```

**Wichtig**: Beide Namen als EIN Team behandeln für korrekte ELO-Kontinuität!

### Szenario 2: Verschiedene Schreibweisen

**Beispiel**: "Cloud9" vs "Cloud 9" vs "C9"

```json
{
  "canonical_name": "Cloud9",
  "aliases": [
    "C9",
    "Cloud 9",
    "C9 LoL"
  ],
  "region": "NA"
}
```

### Szenario 3: Team mit Suffix-Variationen

**Beispiel**: "Fnatic" mit verschiedenen Suffixen

```json
{
  "canonical_name": "Fnatic",
  "aliases": [
    "FNC",
    "Fnatic LoL",
    "Fnatic Esports"
  ],
  "region": "EU"
}
```

Das fuzzy matching entfernt automatisch "LoL", "Esports", etc.

### Szenario 4: Zwei verschiedene Teams mit ähnlichem Namen

**Beispiel**: "Rogue (NA)" vs "Rogue (EU)"

```json
[
  {
    "canonical_name": "Rogue",
    "aliases": ["RGE"],
    "region": "EU"
  },
  {
    "canonical_name": "Rogue (NA)",
    "aliases": [],
    "region": "NA"
  }
]
```

Füge Region im canonical name hinzu wenn nötig!

---

## Best Practices

### 1. Canonical Name wählen

- Nutze den **aktuellen** Team-Namen als canonical
- Bei Rebrands: Neuer Name ist canonical, alter ist alias
- Bei Abkürzungen: Voller Name ist meist canonical (außer die Abkürzung ist offizieller)
  - Ausnahme: TSM, C9, T1 (Abkürzung ist offizieller Name)

### 2. Region zuweisen

Wichtig für das ELO-System (Regional Offsets):

| Region | Liga | Beispiele |
|--------|------|-----------|
| **CN** | LPL | EDG, RNG, JDG |
| **KR** | LCK | T1, Gen.G, DRX |
| **EU** | LEC | G2, Fnatic, MAD Lions |
| **NA** | LCS | Cloud9, TSM, Team Liquid |
| **BR** | CBLOL | LOUD, paiN Gaming |
| **TW** | PCS | PSG Talon, Beyond Gaming |
| **VN** | VCS | GAM Esports, Saigon Buffalo |
| **JP** | LJL | DetonatioN FocusMe |

### 3. Priorität bei Bulk-Mapping

Teams mit vielen Matches zuerst:

```bash
# In generate_bulk_mappings.py
min_matches = 20  # Nur wichtige Teams
```

Dann schrittweise kleinere Teams hinzufügen.

### 4. Fuzzy Matching nutzen

Das System hat automatisches Fuzzy Matching. Threshold anpassen:

```json
{
  "fuzzy_matching_rules": {
    "similarity_threshold": 0.85
  }
}
```

- **0.90+**: Sehr konservativ, nur offensichtliche Matches
- **0.85**: Standard, gute Balance
- **0.80**: Aggressiver, mehr automatische Matches

### 5. Quick Tips

**Alias oder New?**
- Ist es eine Variation eines bekannten Teams? → `alias`
- Ist es ein komplett anderes Team? → `new`

**Welcher canonical name?**
- Nutze den modernen/aktuellen Namen
- Bei Rebrands: Neuer Name = canonical

**Häufige Rebrands:**

| Alt | Neu |
|-----|-----|
| SK Telecom T1 | T1 |
| Samsung Galaxy | Gen.G |
| Longzhu Gaming / KingZone | DRX |
| Moscow Five | Gambit |
| DAMWON Gaming | DWG KIA |

---

## Platform-spezifische Hinweise

### Linux / macOS

Standard-Workflow wie oben beschrieben.

### Windows

#### Option 1: Direkt in PowerShell

```powershell
cd C:\Users\YourName\path\to\lol-elo-system

# Bulk-Mapping
python generate_bulk_mappings.py

# Analyse
python analyze_team_mappings.py
```

#### Option 2: Team-Namen exportieren (wenn DB auf Windows ist)

Wenn deine Datenbank nur auf Windows existiert:

```powershell
# Wo ist deine Datenbank?
python export_teams_for_mapping.py C:\pfad\zu\deiner\datenbank.db
```

Das erstellt eine `teams_to_map.json` Datei mit allen Team-Namen, die du dann auf Linux verwenden kannst.

#### Option 3: Datenbank kopieren

```powershell
# Kopiere deine Datenbank hierher:
copy C:\pfad\zu\deiner\datenbank.db .\db\elo_system.db
```

---

## Troubleshooting

### Problem: "No mapping found" Warnungen

**Lösung**:
1. Laufe `analyze_team_mappings.py`
2. Checke welche Teams häufig vorkommen
3. Mappe diese manuell oder mit bulk generator

### Problem: Falsche Mappings

**Lösung**:
1. Öffne `config/team_name_mappings.json`
2. Finde das falsche Mapping
3. Korrigiere canonical name oder aliases
4. Speichere und teste erneut

### Problem: "Database not found"

**Lösung**:
```bash
# Import zuerst Daten:
python major_regions_tournament_import_matchschedule.py
```

### Problem: "Too many unmapped teams"

**Lösung**:
- Reduziere minimum matches in bulk generator (z.B. 5 statt 10)
- Oder ignoriere Teams mit wenigen Matches

### Problem: Zwei verschiedene Teams werden zusammen gemappt

**Beispiel**: "Rogue (NA)" vs "Rogue (EU)"

**Lösung**: Füge Region im canonical name hinzu (siehe Szenario 4 oben)

---

## Maintenance

### Regelmäßige Updates

Alle 1-2 Splits:

```bash
# 1. Neue Matches importieren
python major_regions_tournament_import_matchschedule.py

# 2. Neue unmapped Teams finden
python analyze_team_mappings.py

# 3. Neue Mappings hinzufügen
# -> Interaktiver Modus oder manuell in JSON
```

### Mapping-Qualität prüfen

```bash
# Zeige alle Teams und ihre Resolutions
python -c "
from core.team_name_resolver import TeamNameResolver
from core.database import DatabaseManager

db = DatabaseManager()
resolver = TeamNameResolver()

teams = db.conn.execute('SELECT DISTINCT name FROM teams').fetchall()
for (name,) in teams:
    resolved = resolver.resolve(name, 'check')
    if name != resolved:
        print(f'{name:40s} → {resolved}')
"
```

---

## Beispiel: Komplettes Regional-Mapping

**LCK (Korea) 2013-2024**:

```json
{
  "mappings": [
    {"canonical_name": "T1", "aliases": ["SK Telecom T1", "SKT", "SKT T1"], "region": "KR"},
    {"canonical_name": "Gen.G", "aliases": ["Samsung Galaxy", "KSV", "GenG"], "region": "KR"},
    {"canonical_name": "DRX", "aliases": ["DragonX", "Dragon X"], "region": "KR"},
    {"canonical_name": "KT Rolster", "aliases": ["KT", "kt Rolster"], "region": "KR"},
    {"canonical_name": "Hanwha Life Esports", "aliases": ["HLE", "Hanwha"], "region": "KR"},
    {"canonical_name": "DWG KIA", "aliases": ["DAMWON Gaming", "DWG", "Damwon"], "region": "KR"},
    {"canonical_name": "Afreeca Freecs", "aliases": ["AF", "Afreeca"], "region": "KR"}
  ]
}
```

---

## Support

Bei Fragen oder Problemen:
1. Checke diese Anleitung
2. Siehe `core/team_name_resolver.py` Code
3. Laufe Test-Scripts um Beispiele zu sehen

Viel Erfolg beim Mapping! 🎮
