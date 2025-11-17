# Expected Match Counts - Reference List

Diese Liste zeigt, wie viele Matches ungefähr pro Saison/Turnier erwartet werden.

## Regional Leagues (Pro Split)

### LEC / EU LCS (Europa)
**Format:** 10 Teams, Best-of-1 Regular Season (2013-2018), Best-of-2/3 (ab 2016)

| Jahr | Split | Regular Season | Playoffs | Total pro Split |
|------|-------|----------------|----------|-----------------|
| 2013 | Spring/Summer | N/A | N/A | N/A (keine Daten) |
| 2014 | Spring/Summer | 112 | ~10 | ~120 |
| 2015 | Spring/Summer | 90-95 | ~10 | ~100-105 |
| 2016 | Spring/Summer | 90-95 | ~10 | ~100-105 |
| 2017 | Spring/Summer | 65-70 | ~10 | ~75-80 |
| 2018 | Spring/Summer | 90-95 | ~15 | ~105-110 |
| 2019-2024 | Spring/Summer | 90 | ~15-20 | ~105-110 |

**Erwartete Gesamt:** ~2,200 matches (2014-2024)

---

### LCS (North America)
**Format:** 10 Teams, ähnlich wie LEC

| Jahr | Split | Regular Season | Playoffs | Total pro Split |
|------|-------|----------------|----------|-----------------|
| 2013 | Spring/Summer | N/A | N/A | N/A (keine Daten) |
| 2014 | Spring/Summer | 112 | ~10 | ~120 |
| 2015-2018 | Spring/Summer | 90-95 | ~10-15 | ~100-110 |
| 2019-2024 | Spring/Summer | 90 | ~15-20 | ~105-110 |

**Erwartete Gesamt:** ~2,200 matches (2014-2024)

---

### LCK (Korea)
**Format:** 10 Teams, Best-of-3 seit Anfang (mehr Spiele = mehr Matches)

| Jahr | Split | Regular Season | Playoffs | Total pro Split |
|------|-------|----------------|----------|-----------------|
| 2013 | Winter/Spring/Summer | 100-150 | ~15 | ~120-170 |
| 2014-2018 | Spring/Summer | 100-120 | ~15-20 | ~120-140 |
| 2019-2024 | Spring/Summer | 90-100 | ~20 | ~110-120 |

**Erwartete Gesamt:** ~2,500-3,000 matches (2013-2024)

---

### LPL (China)
**Format:** 16-17 Teams (größte Liga!), Best-of-3

| Jahr | Split | Regular Season | Playoffs | Total pro Split |
|------|-------|----------------|----------|-----------------|
| 2013-2015 | Spring/Summer | 80-100 | ~10 | ~90-110 |
| 2016-2018 | Spring/Summer | 120-150 | ~15 | ~135-165 |
| 2019-2024 | Spring/Summer | 130-160 | ~20 | ~150-180 |

**Erwartete Gesamt:** ~3,000-3,500 matches (2013-2024)

---

## International Tournaments

### MSI (Mid-Season Invitational)
**Format:** 11-13 Teams, Play-In + Main Event

| Jahr | Format | Matches |
|------|--------|---------|
| 2015 | Main Event | ~15 |
| 2016 | Main Event | ~20 |
| 2017-2024 | Play-In + Main | ~40-50 |

**Erwartete Gesamt:** ~400 matches (2015-2024)

---

### Worlds (World Championship)
**Format:** 22-24 Teams, Play-In + Group Stage + Knockouts

| Jahr | Format | Matches |
|------|--------|---------|
| 2013-2014 | Group + Knockouts | ~40-50 |
| 2015-2017 | Group + Knockouts | ~60-70 |
| 2018-2024 | Play-In + Group + Knockouts | ~80-100 |

**Erwartete Gesamt:** ~900 matches (2013-2024)

---

## Grand Total (All Leagues, 2013-2024)

| Liga | Erwartete Matches |
|------|-------------------|
| LEC | ~2,200 |
| LCS | ~2,200 |
| LCK | ~2,700 |
| LPL | ~3,200 |
| MSI | ~400 |
| Worlds | ~900 |
| **TOTAL** | **~11,600 matches** |

---

## Notes

1. **Match vs Game:** Ein "Match" ist eine Serie (z.B. Best-of-3). Ein "Game" ist ein einzelnes Spiel.
   - 1 Match Best-of-3 = bis zu 3 Games
   - Dieses System zählt **Matches**, nicht Games

2. **Format-Änderungen:** Die Ligen haben ihre Formate über die Jahre geändert:
   - Bo1 (Best-of-1): Jedes Spiel ist 1 Match
   - Bo2 (Best-of-2): 2 Games = 1 Match
   - Bo3 (Best-of-3): 2-3 Games = 1 Match

3. **Variabilität:** Die genauen Zahlen variieren je nach:
   - Anzahl der Teams
   - Playoff-Format
   - Tiebreaker-Spiele
   - Format-Änderungen innerhalb der Saison

4. **Datenverfügbarkeit:**
   - 2013 hat oft unvollständige Daten (frühe Esports-Jahre)
   - Einige kleinere Turniere/Qualifiers sind nicht inkludiert
   - Nur Tier 1 Leagues (keine Regional Qualifiers, Academy, etc.)

---

## Verwendung

Diese Liste dient als **Referenz** um zu prüfen, ob der Datenimport vollständig ist.

**Beispiel Check:**
- Wenn LEC 2022 Spring nur 50 Matches hat → fehlen ~40-50 Matches
- Wenn Worlds 2023 nur 30 Matches hat → fehlen ~50-60 Matches
- Wenn LPL komplett 0 Matches hat → gesamte Liga fehlt

**Vergleich mit Ist-Zustand:**
```bash
python scripts/import_coverage_report.py
```
