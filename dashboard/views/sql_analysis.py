"""
SQL Analysis Insights View for IPL Batter Intelligence & Strategy Platform.
Focuses strictly on 2024-2025 team phase dynamics generated via MySQL relational aggregations.
"""

import streamlit as st
import pandas as pd
from dashboard.config import PHASES, PHASE_COLORS, TEAM_COLORS
from dashboard.styles import render_section_header, render_kpi
from dashboard.data_service import load_sql_team_phase_summary
from dashboard.components.charts import (
    create_team_phase_run_rate_chart,
    create_team_boundary_dependency_chart,
)


def render_sql_analysis_view():
    """Renders the SQL relational analytical insights module (2024–2025 focus)."""
    st.markdown(
        render_section_header(
            "SQL Relational Phase Intelligence",
            "Deep franchise phase dynamics derived via MySQL queries against ipl_analytics",
        ),
        unsafe_allow_html=True,
    )

    # 1. Mandatory Data Architecture Separation Callout
    st.markdown(
        '<div class="info-callout" style="border-left-color: #FFB800;">'
        '<div style="font-size: 0.78rem; font-weight: 700; color: #FFB800; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 4px;">'
        'Data Architecture & Scope Notice'
        '</div>'
        '<div style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.5;">'
        '• <b>Relational Database:</b> MySQL <code>ipl_analytics</code> (Table: <code>ipl_deliveries_python</code>)<br>'
        '• <b>Analytical Window:</b> 2024 & 2025 Tournament Editions<br>'
        '• <b>Distinct Purpose:</b> While the Python pipeline analyzes macro historical batter statistics through 2026, this SQL module examines tactical team-level phase run rates, boundary dependency, and wicket attrition across modern IPL seasons.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    sql_df = load_sql_team_phase_summary()
    if sql_df.empty:
        st.error("SQL analytical summary dataset could not be loaded.")
        return

    # Filter Controls
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        selected_season = st.radio(
            "Select Tournament Season",
            options=[2024, 2025],
            index=0,
            horizontal=True,
            key="sql_season_radio"
        )
    with f_col2:
        selected_team = st.selectbox(
            "Filter Specific Franchise (Optional)",
            options=["All Franchises"] + sorted(sql_df["batting_team"].unique().tolist()),
            index=0,
            key="sql_team_select"
        )

    season_df = sql_df[sql_df["season"] == selected_season].copy()
    
    # Season Highlights KPIs
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        top_pp = season_df[season_df["match_phase"] == "Powerplay"].sort_values("phase_run_rate", ascending=False).iloc[0]
        st.markdown(render_kpi("Highest Powerplay Run Rate", f"{top_pp['phase_run_rate']:.2f}", f"{top_pp['batting_team']}", accent_color=PHASE_COLORS["Powerplay"]), unsafe_allow_html=True)
    with kpi_col2:
        top_mid = season_df[season_df["match_phase"] == "Middle Overs"].sort_values("phase_run_rate", ascending=False).iloc[0]
        st.markdown(render_kpi("Highest Middle Overs Run Rate", f"{top_mid['phase_run_rate']:.2f}", f"{top_mid['batting_team']}", accent_color=PHASE_COLORS["Middle"]), unsafe_allow_html=True)
    with kpi_col3:
        top_death = season_df[season_df["match_phase"] == "Death Overs"].sort_values("phase_run_rate", ascending=False).iloc[0]
        st.markdown(render_kpi("Highest Death Overs Run Rate", f"{top_death['phase_run_rate']:.2f}", f"{top_death['batting_team']}", accent_color=PHASE_COLORS["Death"]), unsafe_allow_html=True)
    with kpi_col4:
        total_runs_season = season_df.groupby("batting_team")["season_total_runs"].first().sum()
        st.markdown(render_kpi(f"Season Total Runs ({selected_season})", f"{total_runs_season:,}", "Across 10 Franchises", accent_color="#FFB800"), unsafe_allow_html=True)

    
    # ============================================================
    # VISUALIZATIONS
    # ============================================================

    st.markdown("<br>", unsafe_allow_html=True)

    # Apply selected season and franchise to chart data
    chart_df = season_df.copy()

    if selected_team != "All Franchises":
        chart_df = chart_df[
            chart_df["batting_team"] == selected_team
        ].copy()

    if chart_df.empty:
        st.warning("No phase data available for this selection.")
    else:
        v_col1, v_col2 = st.columns([1.3, 1.0])

        with v_col1:
            fig_rates = create_team_phase_run_rate_chart(
                chart_df,
                target_season=selected_season
            )
            st.plotly_chart(
                fig_rates,
                use_container_width=True
            )

        with v_col2:
            fig_dep = create_team_boundary_dependency_chart(
                chart_df,
                target_season=selected_season
            )
            st.plotly_chart(
                fig_dep,
                use_container_width=True
            )


    # Tabular Breakdown
    st.markdown(render_section_header("SQL Relational Phase Summary Table"), unsafe_allow_html=True)
    
    table_filtered = season_df.copy()
    if selected_team != "All Franchises":
        table_filtered = table_filtered[table_filtered["batting_team"] == selected_team]

    display_sql_df = table_filtered[[
        "batting_team", "match_phase", "innings_batted", "phase_runs", "legal_balls",
        "phase_run_rate", "boundary_runs", "fours", "sixes", "singles", "doubles",
        "wickets_lost", "season_run_rate"
    ]].copy()

    display_sql_df.columns = [
        "Franchise", "Match Phase", "Innings", "Phase Runs", "Legal Balls",
        "Phase Run Rate", "Boundary Runs", "4s", "6s", "1s", "2s",
        "Wickets Lost", "Season Run Rate"
    ]

    st.dataframe(
        display_sql_df.style.format({
            "Phase Run Rate": "{:.2f}",
            "Season Run Rate": "{:.2f}",
        }),
        use_container_width=True,
        height=340,
    )

    # SQL Query Inspector
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💻 View SQL Query Used for 2024–2025 Relational Phase Aggregations", expanded=False):
        st.code("""
-- Query: Team-Level Phase Aggregation for Modern IPL Seasons (2024 & 2025)
-- Database: ipl_analytics | Table: ipl_deliveries_python

SELECT 
    season,
    batting_team,
    CASE 
        WHEN delivery_number < 6.0 THEN 'Powerplay'
        WHEN delivery_number >= 6.0 AND delivery_number < 15.0 THEN 'Middle Overs'
        WHEN delivery_number >= 15.0 THEN 'Death Overs'
    END AS match_phase,
    SUM(batter_runs + total_extras) AS phase_runs,
    COUNT(DISTINCT match_id, innings) AS innings_batted,
    SUM(CASE WHEN batter_runs = 4 THEN 1 ELSE 0 END) AS fours,
    SUM(CASE WHEN batter_runs = 6 THEN 1 ELSE 0 END) AS sixes,
    SUM(CASE WHEN batter_runs IN (4, 6) THEN batter_runs ELSE 0 END) AS boundary_runs,
    SUM(CASE WHEN batter_runs = 1 THEN 1 ELSE 0 END) AS singles,
    SUM(CASE WHEN batter_runs = 2 THEN 1 ELSE 0 END) AS doubles,
    COUNT(CASE WHEN dismissal_method IS NOT NULL THEN 1 END) AS wickets_lost,
    SUM(CASE WHEN wides IS NULL OR wides = 0 THEN 1 ELSE 0 END) AS legal_balls,
    ROUND(SUM(batter_runs + total_extras) / (SUM(CASE WHEN wides IS NULL OR wides = 0 THEN 1 ELSE 0 END) / 6.0), 2) AS phase_run_rate
FROM ipl_deliveries_python
WHERE season IN ('2024', '2025')
GROUP BY season, batting_team, match_phase
ORDER BY season DESC, phase_run_rate DESC;
        """, language="sql")

