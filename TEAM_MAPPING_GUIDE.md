# Team Name Mapping Guide

Anleitung zum Mapping von Team-Namen für 13,000+ Matches

## Übersicht

Dieses System hilft dir, Team-Namen über verschiedene Datenquellen hinweg zu vereinheitlichen. Bei 13 Jahren Daten gibt es viele Variationen:
- **Rebrands**: SK Telecom T1 → T1, Samsung Galaxy → Gen.G
- **Abkürzungen**: Team SoloMid → TSM, Cloud 9 → C9
- **Suffixe**: "Fnatic" vs "Fnatic LoL" vs "Fnatic Esports"

## Verfügbare Tools

### 1. 🔍 `analyze_team_mappings.py` - Detaillierte Analyse

**Wann verwenden**: Wenn du genau sehen willst, welche Teams bereits gemappt sind und welche noch fehlen.

```bash
python analyze_team_mappings.py
```

**Features**:
- Zeigt mapped vs. unmapped Teams
- Schlägt ähnliche Teams vor (z.B. "T1" bei "SK Telecom T1")
- Interaktiver Modus zum manuellen Mapping
- Export von unmapped Teams

**Workflow**:
1. Script läuft und analysiert deine Datenbank
2. Zeigt Statistiken und unmapped Teams
3. Du kannst wählen:
   - **Interaktiver Modus**: Jedes Team einzeln mappen
   - **Export**: Unmapped Teams als JSON exportieren

### 2. 🚀 `generate_bulk_mappings.py` - Automatische Bulk-Generierung

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
4. Du kannst wählen:
   - Als neue Datei exportieren
   - Mit bestehenden Mappings mergen
   - Beides

### 3. ⚙️ Bestehende Systeme

- **`core/team_name_resolver.py`**: Löst Team-Namen zur Laufzeit auf
- **`config/team_name_mappings.json`**: Zentrale Mapping-Konfiguration

## Empfohlener Workflow für 13,000 Matches

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

1. Wähle minimum matches (empfohlen: 5-10)
2. Überprüfe die Zusammenfassung
3. Wähle Option 2 oder 3 (merge mit existierenden)
4. Speichere die Mappings

**Vorteil**: Mappt automatisch 80-90% der Teams basierend auf Patterns

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
print(r.resolve('SKT', 'test')); \
print(r.resolve('Samsung Galaxy', 'test'))"
```

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
  "region": "NA",
  "notes": "North American team"
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
  "region": "EU",
  "notes": "European team"
}
```

Das fuzzy matching entfernt automatisch "LoL", "Esports", etc.

## Best Practices

### 1. Canonical Name wählen

- Nutze den **aktuellen** Team-Namen als canonical
- Bei Rebrands: Neuer Name ist canonical, alter ist alias
- Bei Abkürzungen: Voller Name ist meist canonical (außer die Abkürzung ist offizieller)

### 2. Region zuweisen

Wichtig für das ELO-System (Regional Offsets):

- **CN**: LPL Teams
- **KR**: LCK Teams
- **EU**: LEC Teams (früher EU LCS)
- **NA**: LCS Teams
- **BR**: CBLOL Teams
- **TW**: PCS Teams (früher LMS)
- **VN**: VCS Teams
- **JP**: LJL Teams

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
    "similarity_threshold": 0.85  // 0.85 = 85% Ähnlichkeit
  }
}
```

- **0.90+**: Sehr konservativ, nur offensichtliche Matches
- **0.85**: Standard, gute Balance
- **0.80**: Aggressiver, mehr automatische Matches

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

### Problem: Zwei verschiedene Teams werden gemappt

**Beispiel**: "Rogue (NA)" vs "Rogue (EU)"

**Lösung**:
```json
[
  {
    "canonical_name": "Rogue",
    "aliases": ["RGE", "Rogue (European Team)"],
    "region": "EU"
  },
  {
    "canonical_name": "Rogue (NA)",
    "aliases": ["Rogue Warriors"],
    "region": "NA"
  }
]
```

Füge Region im canonical name hinzu wenn nötig!

## Tipps für 13 Jahre Daten

### 1. Historische Kontexte beachten

Teams ändern sich über die Jahre:
- **2013-2015**: Viele Team-Wechsel, M5/Gambit, Moscow Five
- **2016-2018**: LCS franchise, viele Orgs verschwinden
- **2019+**: Modernere, stabilere Namen

### 2. Regional-spezifische Besonderheiten

**China (CN)**:
- Häufige Rebrands und Sponsorenwechsel
- "Team WE" → "WE" → "Team WE" (mehrfach)

**Korea (KR)**:
- Sponsor im Namen: "SK Telecom T1", "KT Rolster"
- Viele Rebrands durch Sponsor-Wechsel

**Europa (EU)**:
- EU LCS → LEC Rebrand 2019
- Franchise führte zu vielen neuen Orgs

### 3. Internationale Turniere

Bei Worlds/MSI/IEM oft andere Namensgebung:
- "Team SoloMid" statt "TSM"
- "SK Telecom T1" statt "SKT"

→ Aliases sind hier besonders wichtig!

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

## Beispiel: Komplettes Mapping einer Region

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
    {"canonical_name": "Afreeca Freecs", "aliases": ["AF", "Afreeca"], "region": "KR"},
    {"canonical_name": "KingZone DragonX", "aliases": ["Longzhu Gaming", "LZ"], "region": "KR",
     "notes": "Longzhu (2017) → KingZone (2018) → DragonX (2019)"}
  ]
}
```

## Support

Bei Fragen oder Problemen:
1. Checke diese Anleitung
2. Siehe `core/team_name_resolver.py` Code
3. Laufe Test-Scripts um Beispiele zu sehen

Viel Erfolg beim Mapping! 🎮
