# Tournament Discovery Improvements Summary

## Latest Changes (22.11.2025)

### ✅ FIXES APPLIED

#### 1. MSI 2021-2024 Formats Added
**Before:** Only tested standalone format `{year}_Mid-Season_Invitational`
**After:** Now tests BOTH:
- Standalone: `{year}_Mid-Season_Invitational`
- Play-In: `{year}_Mid-Season_Invitational/Play-In`
- Main Event: `{year}_Mid-Season_Invitational/Main_Event`

**Impact:** +12 tournament patterns tested (may find some that were missing)

#### 2. VCS 2021 Summer - Explicitly Excluded
**Reason:** Cancelled due to COVID-19
**Removed:**
- VCS 2021 Summer
- VCS 2021 Summer Playoffs

**Impact:** -2 from expected NOT FOUND list

#### 3. Regional Finals Clarification
**Corrected Understanding:** Regional Finals cancellation was ONLY for EU/NA regions
**Kept for 2020+:** LPL, LCK, PCS, VCS, LJL, TCL, LLA
**Limited to 2019:** LEC, LCS (EU and NA only)

---

## EXPECTED IMPACT ON NOT FOUND LIST

### Should be REMOVED from NOT FOUND (confirmed don't exist):
1. ❌ VCS 2021 Summer (COVID cancellation)
2. ❌ VCS 2021 Summer Playoffs (COVID cancellation)
3. ❌ LEC 2020-2024 Regional Finals (cancelled for EU)
4. ❌ LCS 2020-2024 Regional Finals (cancelled for NA)
5. ❌ EU LCS 2013 Spring/Summer (Season 3 - doesn't exist in MatchSchedule)
6. ❌ NA LCS 2013 Spring/Summer (Season 3 - doesn't exist in MatchSchedule)

### Should be FOUND now (if URLs are correct):
1. ✅ MSI 2021 Play-In (if it exists with this format)
2. ✅ MSI 2021 Main Event (if it exists with this format)
3. ✅ MSI 2022 Play-In (if it exists with this format)
4. ✅ MSI 2022 Main Event (if it exists with this format)
5. ✅ MSI 2023 Play-In (if it exists with this format)
6. ✅ MSI 2023 Main Event (if it exists with this format)
7. ✅ MSI 2024 Play-In (if it exists with this format)
8. ✅ MSI 2024 Main Event (if it exists with this format)

### Still in NOT FOUND (legitimately don't exist):
- All 2025 tournaments (haven't happened yet)
- LEC 2019-2022 Winter (Winter format started 2023)
- CBLOL Playoffs (all years - not in MatchSchedule)
- VCS 2017 (VCS started 2018)
- LJL 2014 Playoffs (LJL 2014 had no playoffs)
- LJL 2015 (entire year doesn't exist)
- TCL 2013-2014 (TCL started 2015)
- LLN 2014-2016 (not in MatchSchedule)
- GPL, LCL, All-Star (not in MatchSchedule)
- MSI 2020 (COVID cancellation)
- IEM Season X Katowice, Season XI-XII events (not in MatchSchedule)

### Unknown/To Be Verified:
- Regional Finals for non-EU/NA regions (LPL, LCK, PCS, VCS, LJL, TCL, LLA)
  - Currently testing 2020+ for these regions
  - Will show as NOT FOUND if they don't exist or have different URLs

---

## COMMIT HISTORY

1. **6374326** - Add Worlds 2014-2024, OGN fixes, and LCK Promotion tournaments
   - Fixed Worlds URL formats
   - Fixed OGN 2014-2015 URLs
   - Added LCK Promotion 2016-2020

2. **ab6e73a** - Fix tournament discovery script - remove non-existent tournaments
   - Initial cleanup of non-existent tournaments

3. **Latest** - Fix Regional Finals and MSI formats
   - Added MSI 2021-2024 Play-In/Main Event
   - Corrected Regional Finals (EU/NA only cancelled)
   - Excluded VCS 2021 Summer (COVID)

---

## NEXT STEPS

To generate a new NOT FOUND list, run:
```powershell
python complete_tournament_discovery_matchschedule.py > discovery_results.txt
```

Then analyze which tournaments are still NOT FOUND and whether they:
1. Don't exist (should be removed from script)
2. Have wrong URLs (need to find correct format)
3. Are future events (can be skipped for now)
