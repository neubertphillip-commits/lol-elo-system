# Leaguepedia API - Best Practices Compliance

Unsere Implementierung wurde gegen die offizielle Dokumentation geprüft:
https://lol.fandom.com/wiki/Help:Leaguepedia_API

## ✅ Implementierte Best Practices

### 1. **Rate Limiting**
- ✅ 3 Sekunden Delay zwischen Requests (empfohlen: 1-2s)
- ✅ Automatische Erkennung von Rate-Limit-Fehlern
- ✅ Extra 10s Wartezeit bei Rate-Limit-Überschreitung

### 2. **Query Limits**
- ✅ Maximum 500 Ergebnisse pro Query (API-Limit für Non-Admins)
- ✅ Keine Verwendung von Wildcards

### 3. **Tabellen-Verwendung**
- ✅ Verwendung von `ScoreboardGames` für Match-Daten
- ✅ Verwendung von `ScoreboardPlayers` für Spieler-Daten
- ✅ NICHT direkte Abfrage der `Players`-Tabelle (wie empfohlen)
- ✅ Verwendung von `ScoreboardPlayers.Link` für Spielernamen (hat eingebaute Disambiguation)

### 4. **Feld-Konventionen**
- ✅ `__full` Suffix für List-Type-Felder: `Items__full`
- ✅ Korrekte Verarbeitung: API gibt "Items full" (mit Leerzeichen) zurück

### 5. **Joins & IDs**
- ✅ Verwendung von `GameId` für Joins (stabil)
- ✅ KEINE Verwendung von Row IDs als permanente Keys
  - Grund: Row IDs ändern sich bei jedem Cargo Rebuild

### 6. **Fehlerbehandlung**
- ✅ Timeout von 30s für Requests
- ✅ Graceful Handling von API-Fehlern
- ✅ Spezielle Behandlung von Rate-Limit-Fehlern

## 📋 Empfohlene Erweiterungen (Future)

### PlayerRedirects für Umbenennungen
Aktuell verwenden wir `ScoreboardPlayers.Link`, was für die meisten Fälle ausreicht.

Für 100% korrekte Player-Tracking bei Umbenennungen könnte man joinen:
```sql
ScoreboardPlayers → PlayerRedirects → Players
```

**Beispiel-Query:**
```python
tables = "ScoreboardPlayers, PlayerRedirects, Players"
join_on = """
    ScoreboardPlayers.Link = PlayerRedirects.AllName,
    PlayerRedirects.OverviewPage = Players.OverviewPage
"""
fields = "Players.ID, Players.Name, ScoreboardPlayers.Kills, ..."
```

**Wann nötig?**
- Wenn Spieler ihren Namen ändern (z.B. "Rekkles" → "Rekkles1")
- Wenn historische Player-IDs über Jahre hinweg getrackt werden sollen

**Aktueller Status:**
- Für Elo-System nicht kritisch, da wir nur aktuelle Namen brauchen
- `Link`-Feld hat bereits eingebaute Disambiguation
- Kann später bei Bedarf erweitert werden

## 🔍 Validierung

Alle Änderungen basieren auf:
- Offizielle Dokumentation: https://lol.fandom.com/wiki/Help:Leaguepedia_API
- Empfohlene Query-Practices
- Rate-Limiting-Guidelines
- Feld-Naming-Konventionen

## 📊 Performance

**Geschätzte Import-Zeit für volle Historie (2013-2024):**
- ~6 Ligen × ~2 Splits × ~12 Jahre = ~144 Turniere
- ~50-100 Matches pro Turnier-Split = ~7200-14400 Matches
- 3s Delay + ~1s Request = ~4s pro Turnier-Query
- **Gesamtzeit: ~10-30 Minuten** (abhängig von Spielerdaten)

**Optimierungsmöglichkeiten:**
- Parallel-Requests für verschiedene Regionen (nicht empfohlen wegen Rate-Limit)
- Nur Regular Season (ohne Playoffs) importieren
- Spielerdaten überspringen (`--no-players`)
