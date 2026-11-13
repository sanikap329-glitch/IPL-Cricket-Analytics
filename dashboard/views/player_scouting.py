"""
Player Scouting Insights View for IPL Batter Intelligence & Strategy Platform.
Defines rule-based player archetypes using transparent statistical criteria and displays
the peer-review temporal validation report with Spearman/Pearson correlation findings.
"""

import streamlit as st
import pandas as pd
from dashboard.config import PHASES, PHASE_COLORS, TEAM_COLORS
from dashboard.styles import render_section_header, render_kpi, render_player_card
from dashboard.data_service import (
    get_scouting_archetypes,
    load_validation_summary,
    load_temporal_correlations,
)


def render_player_scouting_view():
    """Renders the player scouting archetypes and validation audit module."""
    st.markdown(
        render_section_header(
            "Player Scouting & Role Intelligence",
            "Rule-based player archetypes with explicit sample thresholds and empirical validation",
        ),
        unsafe_allow_html=True,
    )

    archetypes = get_scouting_archetypes()
    
    # Archetype Selection Tabs
    tab_pp, tab_mid, tab_death, tab_eff, tab_val = st.tabs([
        "⚡ Powerplay Enforcers",
        "🌀 Middle Overs Spin Tacklers",
        "💥 Elite Death Finishers",
        "🎯 High-Efficiency Assets",
        "🔬 Temporal Validation Report",
    ])

    with tab_pp:
        _render_archetype_panel(archetypes["Powerplay Enforcers"])

    with tab_mid:
        _render_archetype_panel(archetypes["Middle Overs Spin Tacklers"])

    with tab_death:
        _render_archetype_panel(archetypes["Elite Death Overs Finishers"])

    with tab_eff:
        _render_archetype_panel(archetypes["High-Efficiency Assets"])

    with tab_val:
        _render_temporal_validation_panel()


def _render_archetype_panel(arch_data: dict):
    """Renders candidate leaderboard and criteria for a specific role archetype."""
    df = arch_data["df"]
    phase_color = arch_data["phase_color"]

    st.markdown(
        f'<div class="info-callout" style="border-left-color: {phase_color};">'
        f'<div style="font-weight: 700; color: #ffffff; font-size: 1.05rem; margin-bottom: 4px;">'
        f'{arch_data["description"]}'
        f'</div>'
        f'<div style="font-size: 0.82rem; color: {phase_color};">'
        f'<b>Qualification Criteria:</b> {arch_data["criteria"]}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(render_kpi("Qualified Batters", f"{len(df)}", "Meeting Exact Thresholds", accent_color=phase_color), unsafe_allow_html=True)
    with kpi_col2:
        top_name = df.iloc[0]["batter"] if not df.empty else "N/A"
        st.markdown(render_kpi("Leading Candidate", top_name, "Highest Reliability Rating", accent_color=phase_color), unsafe_allow_html=True)
    with kpi_col3:
        top_score = f"{df.iloc[0]['reliability_adjusted_rating']:.1f}" if not df.empty else "N/A"
        st.markdown(render_kpi("Peak Phase Rating", top_score, "Normalized Scale (Mean 50)", accent_color=phase_color), unsafe_allow_html=True)

    if df.empty:
        st.warning("No players currently meet these strict criteria.")
        return

    # Top Player Cards – hero banner style, up to 6 in two rows of 3
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(render_section_header("Top Archetype Candidates", f"Best {min(len(df), 6)} qualifiers by Reliability Rating"), unsafe_allow_html=True)

    top_players = df.head(6)
    n = len(top_players)

    # Row 1: first 3
    row1_data = top_players.head(3)
    row1_cols = st.columns(min(n, 3))
    for col, (_, row) in zip(row1_cols, row1_data.iterrows()):
        with col:
            st.markdown(
                render_player_card(
                    batter_name=row["batter"],
                    team_name=row.get("team", "IPL"),
                    runs=int(row["total_runs"]),
                    balls=int(row["balls_faced"]),
                    sr=float(row["strike_rate"]),
                    avg=float(row["batting_average"]),
                    rating=float(row["reliability_adjusted_rating"]),
                ),
                unsafe_allow_html=True,
            )

    # Row 2: players 4–6 (if they exist)
    if n > 3:
        row2_data = top_players.iloc[3:]
        row2_cols = st.columns(3)
        for col, (_, row) in zip(row2_cols, row2_data.iterrows()):
            with col:
                st.markdown(
                    render_player_card(
                        batter_name=row["batter"],
                        team_name=row.get("team", "IPL"),
                        runs=int(row["total_runs"]),
                        balls=int(row["balls_faced"]),
                        sr=float(row["strike_rate"]),
                        avg=float(row["batting_average"]),
                        rating=float(row["reliability_adjusted_rating"]),
                    ),
                    unsafe_allow_html=True,
                )

    # Full Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(render_section_header("Complete Archetype Roster"), unsafe_allow_html=True)
    
    display_df = df[[
        "batter", "team", "total_runs", "balls_faced", "dismissals",
        "strike_rate", "batting_average", "boundary_percentage",
        "reliability_adjusted_rating"
    ]].copy()
    display_df.columns = [
        "Batter", "Franchise", "Runs", "Balls", "Dismissals",
        "Strike Rate", "Batting Avg", "Boundary %", "Reliability Rating"
    ]
    display_df.insert(0, "Rank", range(1, len(display_df) + 1))

    st.dataframe(
        display_df.style.format({
            "Strike Rate": "{:.1f}",
            "Batting Avg": "{:.1f}",
            "Boundary %": "{:.1f}%",
            "Reliability Rating": "{:.1f}",
        }),
        use_container_width=True,
        height=320,
    )


def _render_temporal_validation_panel():
    """Renders the transparent academic validation and correlation audit."""
    st.markdown(
        '<div class="warning-callout">'
        '<b>Academic & Data Science Transparency Notice:</b> '
        'The Phase-Aware Batting Ratings and Reliability Adjustments shown in this dashboard are experimental research metrics. '
        'In full accordance with rigorous statistical practice, our out-of-sample temporal validation demonstrates that '
        '<b>historical performance in T20 match phases exhibits weak and statistically insignificant year-on-year correlation</b>. '
        'These ratings reflect contextual historical efficiency and must <b>NOT</b> be presented as official cricket ratings or validated predictive guarantees.'
        '</div>',
        unsafe_allow_html=True
    )

    summary_df = load_validation_summary()
    corr_df = load_temporal_correlations()

    col_val1, col_val2 = st.columns([1.1, 1.0])

    with col_val1:
        st.markdown(render_section_header("Combined Validation Summary"), unsafe_allow_html=True)
        if not summary_df.empty:
            st.dataframe(
                summary_df.style.format({
                    "spearman_correlation": "{:.3f}",
                    "spearman_p_value": "{:.3f}",
                    "pearson_correlation": "{:.3f}",
                    "pearson_p_value": "{:.3f}",
                }),
                use_container_width=True,
            )
        else:
            st.info("Combined validation summary data loading...")

    with col_val2:
        st.markdown(render_section_header("Seasonal Breakdown (Out-of-Sample)"), unsafe_allow_html=True)
        if not corr_df.empty:
            st.dataframe(
                corr_df.style.format({
                    "spearman_correlation": "{:.3f}",
                    "spearman_p_value": "{:.3f}",
                    "pearson_correlation": "{:.3f}",
                    "pearson_p_value": "{:.3f}",
                }),
                use_container_width=True,
            )
        else:
            st.info("Seasonal correlation data loading...")

    st.markdown(
        '<div class="info-callout">'
        '<h4>Key Scientific Takeaways:</h4>'
        '<ol style="margin: 8px 0; padding-left: 20px; line-height: 1.6;">'
        '<li><b>Weak Historical Persistence:</b> Overall Spearman rank correlation between historical rating and future performance was <b>r = 0.141 (p = 0.093)</b>, indicating modest predictive capability.</li>'
        '<li><b>Extreme Death Overs Volatility:</b> Death overs correlation was virtually zero (<b>r = 0.029, p = 0.887</b>), confirming that high-leverage late-innings batting is heavily influenced by match situation, bowler quality, and extreme variance rather than stable long-term averages.</li>'
        '<li><b>Why Empirical Bayes Shrinkage is Critical:</b> Without our +10 prior dismissals adjustment, lower-order batters with small sample sizes (2–3 not-outs) distort average-based rankings unrealistically.</li>'
        '</ol>'
        '</div>',
        unsafe_allow_html=True
    )

