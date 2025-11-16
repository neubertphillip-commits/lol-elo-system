"""
Data Management Page - Import and manage data
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import subprocess

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.database import DatabaseManager


def show():
    """Display data management page"""

    st.title("📥 Data Management")
    st.markdown("Import, view, and manage your ELO system data")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Database Overview",
        "📥 Import Data",
        "🔍 Data Quality",
        "🗑️ Maintenance"
    ])

    # === TAB 1: DATABASE OVERVIEW ===
    with tab1:
        st.subheader("📊 Database Overview")

        try:
            db = DatabaseManager()
            stats = db.get_stats()

            # Main metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Matches", f"{stats['total_matches']:,}")

            with col2:
                st.metric("Total Teams", f"{stats['total_teams']:,}")

            with col3:
                st.metric("Total Players", f"{stats.get('total_players', 0):,}")

            with col4:
                db_path = Path("db/elo_system.db")
                if db_path.exists():
                    db_size_mb = db_path.stat().st_size / (1024 * 1024)
                    st.metric("Database Size", f"{db_size_mb:.1f} MB")
                else:
                    st.metric("Database Size", "N/A")

            # Date range
            if stats['date_range'][0]:
                st.markdown("---")
                st.subheader("📅 Data Range")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("First Match", stats['date_range'][0][:10])
                with col2:
                    st.metric("Last Match", stats['date_range'][1][:10])

            # Table statistics
            st.markdown("---")
            st.subheader("📋 Table Statistics")

            cursor = db.conn.cursor()

            # Get row counts for all tables
            tables = ['teams', 'matches', 'players', 'match_players', 'tournaments']
            table_stats = []

            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_stats.append({'Table': table.title(), 'Rows': count})
                except:
                    table_stats.append({'Table': table.title(), 'Rows': 0})

            df_tables = pd.DataFrame(table_stats)
            st.dataframe(df_tables, use_container_width=True, hide_index=True)

            # Recent activity
            st.markdown("---")
            st.subheader("🕒 Recent Activity")

            try:
                query = """
                    SELECT
                        m.date,
                        t1.name as team1,
                        t2.name as team2,
                        m.team1_score || '-' || m.team2_score as score,
                        tw.name as winner
                    FROM matches m
                    JOIN teams t1 ON m.team1_id = t1.id
                    JOIN teams t2 ON m.team2_id = t2.id
                    JOIN teams tw ON m.winner_id = tw.id
                    ORDER BY m.date DESC
                    LIMIT 5
                """

                df_recent = pd.read_sql_query(query, db.conn)

                if not df_recent.empty:
                    df_recent['date'] = pd.to_datetime(df_recent['date']).dt.strftime('%Y-%m-%d')
                    df_recent.columns = ['Date', 'Team 1', 'Team 2', 'Score', 'Winner']

                    st.dataframe(df_recent, use_container_width=True, hide_index=True)
                else:
                    st.info("No recent matches found")

            except Exception as e:
                st.warning(f"Could not load recent activity: {str(e)}")

            db.close()

        except Exception as e:
            st.error(f"Error accessing database: {str(e)}")
            st.info("Database may not be initialized. Import data to create it.")

    # === TAB 2: IMPORT DATA ===
    with tab2:
        st.subheader("📥 Import Data")
        st.markdown("Import match data from various sources")

        # Google Sheets import
        st.markdown("---")
        st.markdown("### 📄 Google Sheets Import")
        st.info("""
        Import data from your existing Google Sheets spreadsheet.

        **Requirements:**
        - Google Sheets configured in your environment
        - Spreadsheet with match data (team1, team2, scores, dates)
        """)

        if st.button("🚀 Import from Google Sheets", key="import_sheets"):
            with st.spinner("Importing from Google Sheets..."):
                try:
                    result = subprocess.run(
                        ["python", "scripts/import_google_sheets.py"],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )

                    if result.returncode == 0:
                        st.success("✓ Google Sheets import completed!")
                        with st.expander("View Import Log"):
                            st.code(result.stdout)
                    else:
                        st.error("❌ Import failed!")
                        st.code(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Import timed out")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        # Leaguepedia import
        st.markdown("---")
        st.markdown("### 🌐 Leaguepedia API Import")
        st.info("""
        Import professional match data from Leaguepedia (LOL Fandom Wiki).

        **Note:** API has rate limiting (3 second delay between requests).
        Large imports can take hours!
        """)

        col1, col2 = st.columns(2)

        with col1:
            import_mode = st.selectbox(
                "Import Mode",
                ["Test (Quick)", "Recent Data (2023-2024)", "Historical (2013-2024)", "Custom Range"],
                help="Test mode imports ~100 matches for testing. Full imports take hours!"
            )

        with col2:
            leagues = st.multiselect(
                "Select Leagues",
                ["LEC", "LCS", "LCK", "LPL", "Worlds", "MSI"],
                default=["LEC", "LCK", "LPL", "LCS", "Worlds", "MSI"],
                help="Tier-1 professional leagues"
            )

        # Custom range options
        if import_mode == "Custom Range":
            col1, col2 = st.columns(2)

            with col1:
                start_year = st.number_input("Start Year", min_value=2013, max_value=2024, value=2023)

            with col2:
                end_year = st.number_input("End Year", min_value=2013, max_value=2024, value=2024)
        else:
            start_year = None
            end_year = None

        if st.button("🚀 Import from Leaguepedia", key="import_leaguepedia"):
            # Build command
            cmd = ["python", "scripts/import_tier1_data.py"]

            if import_mode == "Test (Quick)":
                cmd.append("--test")
            elif import_mode == "Recent Data (2023-2024)":
                cmd.extend(["--start-year", "2023", "--end-year", "2024"])
            elif import_mode == "Historical (2013-2024)":
                cmd.extend(["--start-year", "2013", "--end-year", "2024"])
            elif import_mode == "Custom Range":
                cmd.extend(["--start-year", str(start_year), "--end-year", str(end_year)])

            if leagues:
                cmd.append("--leagues")
                cmd.extend(leagues)

            # Show command
            st.code(" ".join(cmd))

            st.warning("⚠️ This may take a while! Large imports can take hours due to API rate limiting.")

            with st.spinner("Importing from Leaguepedia..."):
                try:
                    # Longer timeout for large imports
                    timeout = 7200 if import_mode == "Historical (2013-2024)" else 1800

                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=timeout
                    )

                    if result.returncode == 0:
                        st.success("✓ Leaguepedia import completed!")
                        with st.expander("View Import Log"):
                            st.code(result.stdout)
                    else:
                        st.error("❌ Import failed!")
                        st.code(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Import timed out (>30 minutes)")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        # Command line reference
        st.markdown("---")
        st.markdown("### 💻 Command Line Reference")

        st.markdown("""
        **Import commands (run in terminal for better control):**

        ```bash
        # Google Sheets
        python scripts/import_google_sheets.py

        # Leaguepedia - Test
        python scripts/import_tier1_data.py --test

        # Leaguepedia - Recent
        python scripts/import_tier1_data.py --start-year 2023 --end-year 2024

        # Leaguepedia - Specific leagues
        python scripts/import_tier1_data.py --leagues LEC LCK --start-year 2024

        # Save logs
        python scripts/import_tier1_data.py --start-year 2023 2>&1 | tee import.log
        ```
        """)

    # === TAB 3: DATA QUALITY ===
    with tab3:
        st.subheader("🔍 Data Quality")
        st.markdown("Check data integrity and quality issues")

        # Duplicate detection
        st.markdown("### 🔍 Duplicate Detection")

        if st.button("🔎 Check for Duplicates", key="check_duplicates"):
            with st.spinner("Analyzing duplicates..."):
                try:
                    result = subprocess.run(
                        ["python", "scripts/diagnose_duplicates.py"],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )

                    if result.returncode == 0:
                        st.success("✓ Duplicate analysis completed!")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Analysis failed!")
                        st.code(result.stderr)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        # Data validation
        st.markdown("---")
        st.markdown("### ✅ Data Validation")

        if st.button("✓ Validate Data Integrity", key="validate_data"):
            try:
                db = DatabaseManager()
                cursor = db.conn.cursor()

                issues = []

                # Check for missing data
                cursor.execute("SELECT COUNT(*) FROM matches WHERE team1_id IS NULL OR team2_id IS NULL")
                missing_teams = cursor.fetchone()[0]
                if missing_teams > 0:
                    issues.append(f"⚠️ {missing_teams} matches with missing team IDs")

                # Check for invalid scores
                cursor.execute("SELECT COUNT(*) FROM matches WHERE team1_score < 0 OR team2_score < 0")
                invalid_scores = cursor.fetchone()[0]
                if invalid_scores > 0:
                    issues.append(f"⚠️ {invalid_scores} matches with invalid scores")

                # Check for future dates
                cursor.execute("SELECT COUNT(*) FROM matches WHERE match_date > datetime('now')")
                future_dates = cursor.fetchone()[0]
                if future_dates > 0:
                    issues.append(f"⚠️ {future_dates} matches with future dates")

                # Check for teams without matches
                cursor.execute("""
                    SELECT COUNT(*) FROM teams t
                    WHERE NOT EXISTS (
                        SELECT 1 FROM matches m
                        WHERE m.team1_id = t.id OR m.team2_id = t.id
                    )
                """)
                orphan_teams = cursor.fetchone()[0]
                if orphan_teams > 0:
                    issues.append(f"ℹ️ {orphan_teams} teams without matches")

                db.close()

                if issues:
                    st.warning("Data quality issues found:")
                    for issue in issues:
                        st.markdown(f"- {issue}")
                else:
                    st.success("✓ No data quality issues found!")

            except Exception as e:
                st.error(f"Error validating data: {str(e)}")

        # Team name mapping check
        st.markdown("---")
        st.markdown("### 🏷️ Team Name Mapping")

        if st.button("🔎 Test Team Name Resolver", key="test_resolver"):
            with st.spinner("Testing team name resolver..."):
                try:
                    result = subprocess.run(
                        ["python", "core/team_name_resolver.py"],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    if result.returncode == 0:
                        st.success("✓ Team name resolver test completed!")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Test failed!")
                        st.code(result.stderr)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # === TAB 4: MAINTENANCE ===
    with tab4:
        st.subheader("🗑️ Database Maintenance")
        st.markdown("Advanced database operations")

        st.warning("⚠️ **Caution:** These operations can modify or delete data. Use carefully!")

        # Export database
        st.markdown("### 📤 Export Data")

        export_format = st.selectbox(
            "Export Format",
            ["CSV", "JSON", "SQL Dump"]
        )

        if st.button("📥 Export Database", key="export_db"):
            try:
                from core.unified_data_loader import UnifiedDataLoader

                loader = UnifiedDataLoader()
                df = loader.load_matches(source='database')

                if not df.empty:
                    if export_format == "CSV":
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "Download CSV",
                            data=csv,
                            file_name=f"elo_matches_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )

                    elif export_format == "JSON":
                        json_data = df.to_json(orient='records', indent=2)
                        st.download_button(
                            "Download JSON",
                            data=json_data,
                            file_name=f"elo_matches_{pd.Timestamp.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )

                    elif export_format == "SQL Dump":
                        st.info("Use command line for SQL dump:")
                        st.code("sqlite3 db/elo_system.db .dump > backup.sql")

                    st.success("✓ Export ready!")
                else:
                    st.warning("No data to export")

            except Exception as e:
                st.error(f"Error exporting: {str(e)}")

        # Backup database
        st.markdown("---")
        st.markdown("### 💾 Backup & Restore")

        st.info("""
        **Manual Backup (Recommended):**

        ```bash
        # Backup
        cp db/elo_system.db db/elo_system_backup_$(date +%Y%m%d).db

        # Restore
        cp db/elo_system_backup_YYYYMMDD.db db/elo_system.db
        ```
        """)

        # Vacuum database
        st.markdown("---")
        st.markdown("### 🧹 Optimize Database")

        if st.button("🚀 Vacuum Database", key="vacuum_db"):
            try:
                db = DatabaseManager()
                cursor = db.conn.cursor()
                cursor.execute("VACUUM")
                db.conn.commit()
                db.close()

                st.success("✓ Database optimized!")
                st.info("VACUUM reclaims unused space and optimizes performance.")

            except Exception as e:
                st.error(f"Error optimizing database: {str(e)}")

        # Clear cache
        st.markdown("---")
        st.markdown("### 🗑️ Clear Cache")

        if st.button("🧹 Clear Streamlit Cache", key="clear_cache"):
            st.cache_data.clear()
            st.success("✓ Cache cleared! Reload page to see changes.")


if __name__ == "__main__":
    show()
