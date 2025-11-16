"""
Analysis Tools Page - Feature importance and error analysis
"""

import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def show():
    """Display analysis tools page"""

    st.title("🔍 Analysis Tools")
    st.markdown("Deep dive into model performance and error patterns")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Feature Importance",
        "Error Patterns",
        "Regional Offsets",
        "Custom Analysis"
    ])

    # === TAB 1: FEATURE IMPORTANCE ===
    with tab1:
        st.subheader("🎯 Feature Importance")
        st.markdown("Ablation study showing impact of each feature")

        st.info("""
        **What is Feature Importance?**

        We test each feature by removing it and measuring accuracy drop.
        Larger accuracy drop = more important feature.

        **Method: Ablation Study**
        1. Start with baseline (simple ELO, K=24)
        2. Add one feature at a time
        3. Measure accuracy improvement
        4. Compare configurations
        """)

        # Check for results
        feature_path = Path("analysis/feature_importance.json")

        if feature_path.exists():
            try:
                with open(feature_path, 'r') as f:
                    results = json.load(f)

                # Extract feature data
                features = results.get('features', {})

                if features:
                    # Create DataFrame
                    feature_data = []
                    for name, data in features.items():
                        feature_data.append({
                            'Configuration': name,
                            'Accuracy': data.get('accuracy', 0),
                            'Description': data.get('description', '')
                        })

                    df_features = pd.DataFrame(feature_data)
                    df_features = df_features.sort_values('Accuracy', ascending=False)

                    # Display metrics
                    st.markdown("---")
                    st.subheader("📊 Feature Comparison")

                    # Bar chart
                    st.bar_chart(
                        df_features.set_index('Configuration')['Accuracy'],
                        use_container_width=True
                    )

                    # Table
                    df_display = df_features.copy()
                    df_display['Accuracy'] = df_display['Accuracy'].apply(lambda x: f"{x:.2%}")

                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Configuration": st.column_config.TextColumn(width="medium"),
                            "Accuracy": st.column_config.TextColumn(width="small"),
                            "Description": st.column_config.TextColumn(width="large")
                        }
                    )

                    # Incremental improvement
                    st.markdown("---")
                    st.subheader("📈 Incremental Improvements")

                    # Calculate deltas
                    baseline_acc = features.get('Baseline', {}).get('accuracy', 0)

                    for name, data in features.items():
                        if name != 'Baseline':
                            acc = data.get('accuracy', 0)
                            delta = acc - baseline_acc
                            color = "green" if delta > 0 else "red"

                            st.markdown(f"**{name}**: {acc:.2%} (<span style='color: {color};'>{'+'if delta > 0 else ''}{delta:.2%} vs Baseline</span>)", unsafe_allow_html=True)
                            st.caption(data.get('description', ''))
                            st.progress((acc - 0.5) / 0.5)  # Scale from 50% to 100%

                    # Recommendations
                    st.markdown("---")
                    st.subheader("💡 Recommendations")

                    best_config = max(features.items(), key=lambda x: x[1].get('accuracy', 0))
                    best_name = best_config[0]
                    best_acc = best_config[1].get('accuracy', 0)

                    st.success(f"""
                    **Recommended Configuration: {best_name}**

                    - Accuracy: **{best_acc:.2%}**
                    - Improvement over baseline: **+{(best_acc - baseline_acc):.2%}**

                    {best_config[1].get('description', '')}
                    """)

            except Exception as e:
                st.error(f"Error loading feature importance: {str(e)}")

        else:
            st.warning("No feature importance results found.")
            st.markdown("""
            **To generate feature importance analysis:**

            ```bash
            python analysis/feature_importance.py
            ```

            Or navigate to **📈 Validation Suite** → **⚙️ Run Validation** to run master validation report.
            """)

    # === TAB 2: ERROR PATTERNS ===
    with tab2:
        st.subheader("📉 Error Pattern Analysis")
        st.markdown("Understanding where and why the model makes mistakes")

        st.info("""
        **Why Analyze Errors?**

        Understanding failure patterns helps:
        - Identify model limitations
        - Guide future improvements
        - Set realistic expectations
        - Debug issues

        **Analysis Dimensions:**
        - ELO difference (toss-up vs stomp)
        - Tournament type (Worlds vs Regular)
        - Match closeness (3-0 vs 3-2)
        """)

        # Check for results
        error_path = Path("analysis/error_patterns.json")

        if error_path.exists():
            try:
                with open(error_path, 'r') as f:
                    results = json.load(f)

                # BY ELO DIFFERENCE
                st.markdown("---")
                st.subheader("📊 Accuracy by ELO Difference")

                elo_patterns = results.get('by_elo_difference', {})

                if elo_patterns:
                    elo_data = []
                    for range_name, data in elo_patterns.items():
                        elo_data.append({
                            'ELO Range': range_name,
                            'Match Type': data.get('match_type', ''),
                            'Accuracy': data.get('accuracy', 0),
                            'Sample Size': data.get('count', 0)
                        })

                    df_elo = pd.DataFrame(elo_data)

                    # Chart
                    st.bar_chart(
                        df_elo.set_index('Match Type')['Accuracy'],
                        use_container_width=True
                    )

                    # Table
                    df_elo_display = df_elo.copy()
                    df_elo_display['Accuracy'] = df_elo_display['Accuracy'].apply(lambda x: f"{x:.1%}")

                    st.dataframe(
                        df_elo_display,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Insights
                    st.markdown("""
                    **Insights:**
                    - **Toss-ups (0-50 ELO)**: Lower accuracy is expected - teams are evenly matched
                    - **Clear favorites (100+)**: High accuracy shows model correctly identifies stronger teams
                    - **Heavy favorites (200+)**: Very high accuracy - model excels at obvious predictions
                    """)

                # BY TOURNAMENT TYPE
                st.markdown("---")
                st.subheader("🏆 Accuracy by Tournament Type")

                tournament_patterns = results.get('by_tournament', {})

                if tournament_patterns:
                    tournament_data = []
                    for tournament, data in tournament_patterns.items():
                        tournament_data.append({
                            'Tournament': tournament,
                            'Accuracy': data.get('accuracy', 0),
                            'Sample Size': data.get('count', 0)
                        })

                    df_tournament = pd.DataFrame(tournament_data)
                    df_tournament = df_tournament.sort_values('Accuracy', ascending=False)

                    # Chart
                    st.bar_chart(
                        df_tournament.set_index('Tournament')['Accuracy'],
                        use_container_width=True
                    )

                    # Table
                    df_tournament_display = df_tournament.copy()
                    df_tournament_display['Accuracy'] = df_tournament_display['Accuracy'].apply(lambda x: f"{x:.1%}")

                    st.dataframe(
                        df_tournament_display,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Insights
                    st.markdown("""
                    **Insights:**
                    - **Worlds/MSI**: Higher accuracy - teams play closer to true strength in high-stakes matches
                    - **Regular Season**: Moderate accuracy - more variance due to experimentation, less motivation
                    - **Playoffs**: Intermediate - teams try harder but may use new strategies
                    """)

                # BY MATCH CLOSENESS
                st.markdown("---")
                st.subheader("🎯 Accuracy by Match Closeness")

                closeness_patterns = results.get('by_closeness', {})

                if closeness_patterns:
                    closeness_data = []
                    for score, data in closeness_patterns.items():
                        closeness_data.append({
                            'Score': score,
                            'Type': data.get('type', ''),
                            'Accuracy': data.get('accuracy', 0),
                            'Sample Size': data.get('count', 0)
                        })

                    df_closeness = pd.DataFrame(closeness_data)

                    # Chart
                    st.bar_chart(
                        df_closeness.set_index('Score')['Accuracy'],
                        use_container_width=True
                    )

                    # Table
                    df_closeness_display = df_closeness.copy()
                    df_closeness_display['Accuracy'] = df_closeness_display['Accuracy'].apply(lambda x: f"{x:.1%}")

                    st.dataframe(
                        df_closeness_display,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Insights
                    st.markdown("""
                    **Insights:**
                    - **3-0 / 2-0 (Stomps)**: High accuracy - model correctly predicts dominant victories
                    - **3-2 / 2-1 (Close)**: Lower accuracy - inherent uncertainty in close matches
                    - **Pattern**: Accuracy inversely correlated with match closeness (as expected)
                    """)

                # Overall summary
                st.markdown("---")
                st.subheader("📝 Summary & Takeaways")

                overall_acc = results.get('overall_accuracy', 0)

                st.markdown(f"""
                **Overall Model Performance: {overall_acc:.2%}**

                **Strengths:**
                - ✅ Excellent at predicting matches with large ELO differences (200+)
                - ✅ High accuracy in high-stakes tournaments (Worlds, MSI)
                - ✅ Correctly identifies dominant victories (3-0, 2-0)

                **Limitations:**
                - ⚠️ Lower accuracy on toss-ups (expected - teams evenly matched)
                - ⚠️ Struggles with close series (3-2, 2-1) - inherent unpredictability
                - ⚠️ Regular season has more variance (experimental picks, motivation)

                **Recommendations:**
                - Use confidence intervals for close matches (ELO diff < 50)
                - Higher confidence in tournament predictions
                - Consider series format when interpreting predictions
                """)

            except Exception as e:
                st.error(f"Error loading error patterns: {str(e)}")

        else:
            st.warning("No error pattern analysis found.")
            st.markdown("""
            **To generate error pattern analysis:**

            ```bash
            python analysis/error_patterns.py
            ```

            Or run master validation report to generate all analyses.
            """)

    # === TAB 3: REGIONAL OFFSETS ===
    with tab3:
        st.subheader("Regional Strength Offsets")
        st.markdown("Dynamic regional power rankings based on cross-regional match performance")

        st.info("""
        **What are Regional Offsets?**

        When teams from different regions play each other, we learn about relative regional strength.
        Dynamic Offset ELO tracks these adjustments automatically:

        - **Positive offset** → Region is stronger than expected
        - **Negative offset** → Region is weaker than expected
        - **Zero offset** → Region performs as expected

        Example: If LCK teams consistently beat LEC teams, LCK gets +offset, LEC gets -offset.
        """)

        # Load DynamicOffsetElo with data
        try:
            from core.database import DatabaseManager
            from core.elo_calculator_service import EloCalculatorService

            db = DatabaseManager()
            service = EloCalculatorService(db)

            # Calculate DynamicOffsetElo
            with st.spinner('Calculating regional offsets...'):
                config_id, ratings = service.calculate_or_load_elos(
                    variant='dynamic_offset',
                    k_factor=24,
                    use_scale_factors=True
                )

            # Load the actual calculator to get offsets
            from variants.with_dynamic_offsets import DynamicOffsetElo

            elo = DynamicOffsetElo(k_factor=24, use_scale_factors=True)

            # Reload all matches to populate offsets
            matches = db.get_all_matches(limit=None)
            for match in matches:
                elo.update_ratings(
                    match['team1_name'],
                    match['team2_name'],
                    match['team1_score'],
                    match['team2_score']
                )

            # Get offsets
            offsets = elo.calculator.offsets
            confidence = elo.calculator.confidence
            sample_counts = elo.calculator.sample_counts

            if offsets:
                # Create DataFrame
                offset_data = []
                for region, offset_value in offsets.items():
                    offset_data.append({
                        'Region': region,
                        'Offset': round(offset_value, 1),
                        'Confidence': f"{confidence.get(region, 0)*100:.0f}%",
                        'Samples': sum(count for pair, count in sample_counts.items() if region in pair)
                    })

                df_offsets = pd.DataFrame(offset_data)
                df_offsets = df_offsets.sort_values('Offset', ascending=False)

                # Display
                st.markdown("---")
                st.subheader("Current Regional Offsets")

                # Metrics in columns
                cols = st.columns(min(4, len(df_offsets)))
                for i, (_, row) in enumerate(df_offsets.iterrows()):
                    if i < len(cols):
                        with cols[i]:
                            delta_color = "normal" if row['Offset'] >= 0 else "inverse"
                            st.metric(
                                row['Region'],
                                f"{row['Offset']:+.1f}",
                                delta=f"{row['Confidence']} confidence"
                            )

                # Table
                st.markdown("---")
                st.dataframe(
                    df_offsets,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'Offset': st.column_config.NumberColumn(
                            'ELO Offset',
                            help='Positive = stronger than expected',
                            format='%+.1f'
                        ),
                        'Samples': st.column_config.NumberColumn(
                            'Cross-Regional Matches',
                            help='Number of matches used to calculate offset'
                        )
                    }
                )

                # Explanation
                st.markdown("---")
                st.subheader("Interpretation")

                strongest = df_offsets.iloc[0]
                weakest = df_offsets.iloc[-1]

                st.markdown(f"""
                **Strongest Region:** {strongest['Region']} (+{strongest['Offset']:.1f} ELO)
                - Teams from this region perform ~{abs(strongest['Offset'])/20:.0f} points better than expected
                - Based on {strongest['Samples']} cross-regional matches

                **Weakest Region:** {weakest['Region']} ({weakest['Offset']:+.1f} ELO)
                - Teams from this region perform ~{abs(weakest['Offset'])/20:.0f} points worse than expected
                - Based on {weakest['Samples']} cross-regional matches

                **Gap:** {strongest['Offset'] - weakest['Offset']:.1f} ELO points
                - This equals ~{(strongest['Offset'] - weakest['Offset'])*2.5:.0f}% win probability swing
                """)

            else:
                st.warning("No regional offset data available. Need more cross-regional matches!")

        except Exception as e:
            st.error(f"Error loading regional offsets: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

    # === TAB 4: CUSTOM ANALYSIS ===
    with tab4:
        st.subheader("📊 Custom Analysis")
        st.markdown("Build custom queries and analyses")

        st.info("🚧 Custom analysis tools coming soon!")

        st.markdown("""
        **Planned Features:**

        1. **Custom SQL Queries**
           - Query database directly
           - Export results to CSV
           - Save favorite queries

        2. **Data Explorer**
           - Interactive data filtering
           - Pivot tables
           - Custom visualizations

        3. **Cohort Analysis**
           - Compare team performance over time
           - Regional comparisons
           - Tournament-specific analysis

        4. **Export Tools**
           - Export to Excel
           - Generate PDF reports
           - API endpoint for programmatic access

        **Current Workaround:**

        Use the command-line tools or Python directly:

        ```python
        from core.database import DatabaseManager
        import pandas as pd

        db = DatabaseManager()

        # Custom query
        query = '''
            SELECT
                t.name,
                COUNT(m.id) as matches,
                SUM(CASE WHEN m.winner_id = t.id THEN 1 ELSE 0 END) as wins
            FROM teams t
            JOIN matches m ON t.id IN (m.team1_id, m.team2_id)
            GROUP BY t.id
            ORDER BY wins DESC
            LIMIT 10
        '''

        df = pd.read_sql_query(query, db.conn)
        print(df)

        db.close()
        ```

        Or use the interactive database viewer:

        ```bash
        python scripts/view_database.py
        > sql SELECT * FROM matches WHERE tournament LIKE '%Worlds%' LIMIT 10
        ```
        """)

        # File browser for existing analyses
        st.markdown("---")
        st.subheader("📁 Existing Analysis Files")

        analysis_dir = Path("analysis")
        if analysis_dir.exists():
            json_files = list(analysis_dir.glob("*.json"))

            if json_files:
                selected_file = st.selectbox(
                    "View analysis file",
                    json_files,
                    format_func=lambda x: x.name
                )

                if st.button("Load File"):
                    try:
                        with open(selected_file, 'r') as f:
                            data = json.load(f)

                        st.json(data)

                        # Download button
                        st.download_button(
                            "📥 Download JSON",
                            data=json.dumps(data, indent=2),
                            file_name=selected_file.name,
                            mime="application/json"
                        )

                    except Exception as e:
                        st.error(f"Error loading file: {str(e)}")
            else:
                st.info("No analysis files found. Run validation to generate analyses.")


if __name__ == "__main__":
    show()
