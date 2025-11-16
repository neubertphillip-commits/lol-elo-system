"""
Rankings Page - Team & Player Rankings
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.database import DatabaseManager
from core.unified_data_loader import UnifiedDataLoader
from variants.with_tournament_context import TournamentContextElo


def show():
    """Display rankings page"""

    st.title("📊 Team & Player Rankings")
    st.markdown("Current ELO ratings and historical performance")

    # Tab selection
    tab1, tab2, tab3 = st.tabs(["🏆 Team Rankings", "👤 Player Rankings", "📈 Historical Charts"])

    # === TAB 1: TEAM RANKINGS ===
    with tab1:
        st.subheader("🏆 Team Rankings")

        try:
            db = DatabaseManager()

            # Filters
            col1, col2, col3 = st.columns(3)

            with col1:
                # Get unique regions
                cursor = db.conn.cursor()
                cursor.execute("SELECT DISTINCT region FROM teams WHERE region IS NOT NULL ORDER BY region")
                regions = [r[0] for r in cursor.fetchall()]

                region_filter = st.selectbox(
                    "Filter by Region",
                    ["All Regions"] + regions
                )

            with col2:
                limit = st.number_input("Show Top N Teams", min_value=5, max_value=100, value=20, step=5)

            with col3:
                sort_by = st.selectbox(
                    "Sort By",
                    ["ELO Rating", "Team Name", "Region", "Matches Played"]
                )

            # Calculate current ELO for all teams
            st.info("📊 Calculating current ELO ratings from match history...")

            # Load matches
            loader = UnifiedDataLoader()
            matches_df = loader.load_matches(source='auto')

            if matches_df.empty:
                st.warning("No match data available. Import data first!")
                db.close()
                return

            # Calculate ELO
            elo = TournamentContextElo(k_factor=24)
            team_elos = {}

            # Sort by date
            matches_df = matches_df.sort_values('date')

            for _, match in matches_df.iterrows():
                team1 = match['team1']
                team2 = match['team2']

                # Initialize teams if not seen before
                if team1 not in team_elos:
                    team_elos[team1] = {'elo': 1500, 'matches': 0, 'wins': 0, 'losses': 0}
                if team2 not in team_elos:
                    team_elos[team2] = {'elo': 1500, 'matches': 0, 'wins': 0, 'losses': 0}

                # Determine tournament context
                tournament = match.get('tournament', '')
                if 'world' in tournament.lower():
                    context = 'worlds'
                elif 'playoff' in tournament.lower() or 'final' in tournament.lower():
                    context = 'playoffs'
                else:
                    context = 'regular_season'

                # Get current ratings
                elo1_before = team_elos[team1]['elo']
                elo2_before = team_elos[team2]['elo']

                # Determine winner
                winner = match['winner']

                # Update ratings
                score1 = 1 if winner == team1 else 0
                score2 = 1 if winner == team2 else 0

                elo1_after, elo2_after = elo.update_ratings_with_context(
                    elo1_before, elo2_before, score1, score2, context
                )

                team_elos[team1]['elo'] = elo1_after
                team_elos[team2]['elo'] = elo2_after

                # Update stats
                team_elos[team1]['matches'] += 1
                team_elos[team2]['matches'] += 1

                if score1 == 1:
                    team_elos[team1]['wins'] += 1
                    team_elos[team2]['losses'] += 1
                else:
                    team_elos[team2]['wins'] += 1
                    team_elos[team1]['losses'] += 1

            # Get team regions from database
            cursor.execute("SELECT name, region FROM teams")
            team_regions = {row[0]: row[1] for row in cursor.fetchall()}

            # Create rankings DataFrame
            rankings_data = []
            for team, stats in team_elos.items():
                rankings_data.append({
                    'Team': team,
                    'ELO': int(stats['elo']),
                    'Region': team_regions.get(team, 'Unknown'),
                    'Matches': stats['matches'],
                    'Wins': stats['wins'],
                    'Losses': stats['losses'],
                    'Win Rate': f"{stats['wins'] / max(stats['matches'], 1) * 100:.1f}%"
                })

            rankings_df = pd.DataFrame(rankings_data)

            # Apply region filter
            if region_filter != "All Regions":
                rankings_df = rankings_df[rankings_df['Region'] == region_filter]

            # Sort
            if sort_by == "ELO Rating":
                rankings_df = rankings_df.sort_values('ELO', ascending=False)
            elif sort_by == "Team Name":
                rankings_df = rankings_df.sort_values('Team')
            elif sort_by == "Region":
                rankings_df = rankings_df.sort_values(['Region', 'ELO'], ascending=[True, False])
            elif sort_by == "Matches Played":
                rankings_df = rankings_df.sort_values('Matches', ascending=False)

            # Limit results
            rankings_df = rankings_df.head(limit)

            # Add rank column
            rankings_df.insert(0, 'Rank', range(1, len(rankings_df) + 1))

            # Display
            st.dataframe(
                rankings_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn(format="%d"),
                    "ELO": st.column_config.NumberColumn(format="%d"),
                    "Matches": st.column_config.NumberColumn(format="%d"),
                    "Wins": st.column_config.NumberColumn(format="%d"),
                    "Losses": st.column_config.NumberColumn(format="%d"),
                }
            )

            # Top 5 highlight
            st.markdown("---")
            st.subheader("🏅 Top 5 Teams")

            top5 = rankings_df.head(5)
            cols = st.columns(5)

            for idx, (_, row) in enumerate(top5.iterrows()):
                with cols[idx]:
                    medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][idx]
                    st.markdown(f"### {medal}")
                    st.markdown(f"**{row['Team']}**")
                    st.metric("ELO", row['ELO'])
                    st.caption(f"{row['Region']} | {row['Win Rate']}")

            db.close()

        except Exception as e:
            st.error(f"Error loading rankings: {str(e)}")

    # === TAB 2: PLAYER RANKINGS ===
    with tab2:
        st.subheader("👤 Player Rankings")

        try:
            db = DatabaseManager()

            # Check if player data exists
            cursor = db.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM players")
            player_count = cursor.fetchone()[0]

            if player_count == 0:
                st.info("""
                **Player rankings coming soon!**

                Currently, the system tracks team-level ELO. Player-level ratings require:
                - Complete roster data
                - Player participation tracking
                - Individual performance metrics

                To enable player rankings:
                1. Import player data via API
                2. Run player ELO calculation
                3. View individual player ratings here

                See `docs/SCIENTIFIC_BLOG.md` Section 7.2 for details on player-level ELO implementation.
                """)
            else:
                # Display player data (if available)
                query = """
                    SELECT
                        p.name,
                        p.role,
                        COUNT(mp.match_id) as matches_played
                    FROM players p
                    LEFT JOIN match_players mp ON p.id = mp.id
                    GROUP BY p.id
                    ORDER BY matches_played DESC
                    LIMIT 50
                """

                cursor.execute(query)
                players = cursor.fetchall()

                if players:
                    df_players = pd.DataFrame(players, columns=[
                        'Player', 'Role', 'Matches Played'
                    ])

                    st.dataframe(
                        df_players,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.caption("Note: Player ELO calculations not yet implemented. Showing participation data only.")
                else:
                    st.info("No player data found.")

            db.close()

        except Exception as e:
            st.error(f"Error loading player data: {str(e)}")

    # === TAB 3: HISTORICAL CHARTS ===
    with tab3:
        st.subheader("📈 Historical ELO Charts")

        try:
            db = DatabaseManager()

            # Team selection
            cursor = db.conn.cursor()
            cursor.execute("SELECT name FROM teams ORDER BY name")
            all_teams = [row[0] for row in cursor.fetchall()]

            if not all_teams:
                st.warning("No teams found. Import data first!")
                db.close()
                return

            # Select teams to chart
            selected_teams = st.multiselect(
                "Select teams to visualize (max 5)",
                all_teams,
                default=all_teams[:min(3, len(all_teams))],
                max_selections=5
            )

            if not selected_teams:
                st.info("Select at least one team to view historical ELO chart.")
                db.close()
                return

            # Load matches
            loader = UnifiedDataLoader()
            matches_df = loader.load_matches(source='auto')

            if matches_df.empty:
                st.warning("No match data available.")
                db.close()
                return

            # Calculate ELO history for selected teams
            st.info("📊 Calculating ELO history...")

            elo = TournamentContextElo(k_factor=24)
            team_elos = {}
            elo_history = {team: [] for team in selected_teams}
            date_history = {team: [] for team in selected_teams}

            # Sort by date
            matches_df = matches_df.sort_values('date')

            for _, match in matches_df.iterrows():
                team1 = match['team1']
                team2 = match['team2']
                match_date = pd.to_datetime(match['date'])

                # Initialize teams if not seen before
                if team1 not in team_elos:
                    team_elos[team1] = 1500
                if team2 not in team_elos:
                    team_elos[team2] = 1500

                # Determine tournament context
                tournament = match.get('tournament', '')
                if 'world' in tournament.lower():
                    context = 'worlds'
                elif 'playoff' in tournament.lower() or 'final' in tournament.lower():
                    context = 'playoffs'
                else:
                    context = 'regular_season'

                # Get current ratings
                elo1_before = team_elos[team1]
                elo2_before = team_elos[team2]

                # Determine winner
                winner = match['winner']
                score1 = 1 if winner == team1 else 0
                score2 = 1 if winner == team2 else 0

                # Update ratings
                elo1_after, elo2_after = elo.update_ratings_with_context(
                    elo1_before, elo2_before, score1, score2, context
                )

                team_elos[team1] = elo1_after
                team_elos[team2] = elo2_after

                # Record history for selected teams
                if team1 in selected_teams:
                    elo_history[team1].append(elo1_after)
                    date_history[team1].append(match_date)

                if team2 in selected_teams:
                    elo_history[team2].append(elo2_after)
                    date_history[team2].append(match_date)

            # Create chart DataFrame
            chart_data = pd.DataFrame()

            for team in selected_teams:
                if elo_history[team]:  # Only if team has data
                    team_df = pd.DataFrame({
                        'Date': date_history[team],
                        'ELO': elo_history[team],
                        'Team': team
                    })
                    chart_data = pd.concat([chart_data, team_df], ignore_index=True)

            if not chart_data.empty:
                # Display line chart
                st.line_chart(
                    chart_data,
                    x='Date',
                    y='ELO',
                    color='Team',
                    use_container_width=True
                )

                # Show current ELO values
                st.markdown("---")
                st.subheader("📊 Current ELO Values")

                cols = st.columns(len(selected_teams))
                for idx, team in enumerate(selected_teams):
                    with cols[idx]:
                        current_elo = team_elos.get(team, 1500)
                        st.metric(team, int(current_elo))

                # Export option
                st.markdown("---")
                if st.button("📥 Export Chart Data"):
                    csv = chart_data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"elo_history_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("No data available for selected teams.")

            db.close()

        except Exception as e:
            st.error(f"Error generating charts: {str(e)}")


if __name__ == "__main__":
    show()
