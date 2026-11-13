"""
Phase Intelligence View for IPL Batter Intelligence & Strategy Platform.
Analyzes Powerplay (Gold), Middle (Purple), and Death (Red) overs with quadrant matrices,
empirical Bayes shrinkage comparisons, and leaderboard rankings.
"""

import streamlit as st
import pandas as pd
from dashboard.config import PHASES, PHASE_COLORS, COLORS
from dashboard.styles import render_section_header, render_kpi
from dashboard.data_service import (
    load_phase_ratings,
    get_phase_data,
    load_validation_summary,
)
from dashboard.components.charts import (
    create_phase_quadrant_chart,
    create_top_batters_bar_chart,
    create_rating_distribution_chart,
)


def render_phase_intelligence_view():
    """Renders the Phase Intelligence analysis view with distinct phase colors."""
    st.markdown(
        render_section_header(
            "Phase Intelligence Engine",
            "Contextual evaluation of batter efficiency across distinct match phases",
        ),
        unsafe_allow_html=True,
    )

    # 1. Innings Phase Selection Tabs with Gold, Purple, Red Identifiers
    tab_pp, tab_mid, tab_death, tab_all = st.tabs([
        "⚡ Powerplay (Overs 1–6) — Gold", 
        "🌀 Middle Overs (Overs 7–15) — Purple", 
        "💥 Death Overs (Overs 16–20) — Red",
        "📊 All Phases Distribution"
    ])

    ratings_df = load_phase_ratings()

    with tab_pp:
        _render_single_phase_tab("Powerplay", ratings_df)

    with tab_mid:
        _render_single_phase_tab("Middle", ratings_df)

    with tab_death:
        _render_single_phase_tab("Death", ratings_df)

    with tab_all:
        _render_all_phases_overview(ratings_df)


def _render_single_phase_tab(phase_key: str, ratings_df: pd.DataFrame):
    """Renders deep dive analytics for a selected phase."""
    meta = PHASES[phase_key]
    phase_color = meta["color"]
    
    # Phase Description Callout with Phase Color Border
    st.markdown(
        f'<div class="info-callout" style="border-left-color: {phase_color};">'
        f'<b>{meta["label"]}:</b> {meta["description"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Phase Baseline KPIs
    phase_all = ratings_df[ratings_df["phase"] == phase_key]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi("League Baseline SR", f"{meta['league_sr']:.1f}", f"Phase Benchmark", accent_color=phase_color), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi("League Baseline Avg", f"{meta['league_avg']:.1f}", f"Runs per Dismissal", accent_color=phase_color), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi("League Boundary %", f"{meta['league_boundary_pct']:.1f}%", f"Balls to Boundary", accent_color=phase_color), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi("Eligible Batters", f"{len(phase_all)}", f"Min 200 Balls Faced", accent_color=phase_color), unsafe_allow_html=True)

    # Interactive Controls Row
    st.markdown("<br>", unsafe_allow_html=True)
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 1.5, 1])
    
    with ctrl_col1:
        min_balls = st.slider(
            f"Minimum Balls Faced ({phase_key})",
            min_value=200,
            max_value=int(phase_all["balls_faced"].max()),
            value=200,
            step=50,
            key=f"slider_{phase_key}"
        )
    
    with ctrl_col2:
        rating_choice = st.radio(
            "Evaluation Metric",
            options=["Reliability-Adjusted Rating", "Raw Phase Rating"],
            index=0,
            horizontal=True,
            key=f"rating_choice_{phase_key}",
            help="Reliability-Adjusted applies Empirical Bayes shrinkage (+10 prior dismissals) to prevent sample noise from skewing averages."
        )
        rating_col = "reliability_adjusted_rating" if "Reliability" in rating_choice else "phase_aware_batting_rating"

    with ctrl_col3:
        search_batter = st.text_input(
            "Search Batter",
            placeholder="e.g., Kohli, Klaasen...",
            key=f"search_{phase_key}"
        )

    # Filtered Dataset
    filtered_df = phase_all[phase_all["balls_faced"] >= min_balls].copy()
    if search_batter.strip():
        filtered_df = filtered_df[filtered_df["batter"].str.contains(search_batter.strip(), case=False, na=False)]

    if filtered_df.empty:
        st.warning("No batters meet the selected filter criteria.")
        return

    # Visualizations Row: Quadrant Scatter & Top 10 Bar
    v_col1, v_col2 = st.columns([1.2, 1.0])
    
    with v_col1:
        fig_quad = create_phase_quadrant_chart(filtered_df, phase_key, rating_col=rating_col)
        st.plotly_chart(fig_quad, use_container_width=True)

    with v_col2:
        fig_bar = create_top_batters_bar_chart(filtered_df, phase_key, top_n=10, rating_col=rating_col)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Top 3 Podium Cards for this Phase
    sorted_df = filtered_df.sort_values(rating_col, ascending=False).reset_index(drop=True)
    if len(sorted_df) >= 3:
        from dashboard.styles import render_player_card
        from dashboard.data_service import get_batter_team_mapping
        team_map = get_batter_team_mapping()
        
        st.markdown(render_section_header(f"Top 3 {meta['label']} Specialists", "Elite phase performers with portrait intelligence"), unsafe_allow_html=True)
        pod_col1, pod_col2, pod_col3 = st.columns(3)
        for col, (_, row) in zip([pod_col1, pod_col2, pod_col3], sorted_df.head(3).iterrows()):
            with col:
                st.markdown(
                    render_player_card(
                        batter_name=row["batter"],
                        team_name=team_map.get(row["batter"], "IPL Franchise"),
                        runs=int(row["total_runs"]),
                        balls=int(row["balls_faced"]),
                        sr=float(row["strike_rate"]),
                        avg=float(row["batting_average"]),
                        rating=float(row[rating_col]),
                        avatar_size=56,
                    ),
                    unsafe_allow_html=True,
                )

    # Interactive Leaderboard Table
    st.markdown(render_section_header(f"{meta['label']} Leaderboard", f"{len(filtered_df)} qualified batters sorted by {rating_choice}"), unsafe_allow_html=True)
    
    display_df = filtered_df.sort_values(rating_col, ascending=False).reset_index(drop=True)
    display_df["Rank"] = display_df.index + 1

    table_view = display_df[[
        "Rank", "batter", "total_runs", "balls_faced", "dismissals",
        "batting_average", "adjusted_batting_average", "strike_rate",
        "boundary_percentage", "phase_aware_batting_rating", "reliability_adjusted_rating"
    ]].copy()

    table_view.columns = [
        "Rank", "Batter", "Runs", "Balls", "Dismissals",
        "Batting Avg", "Adjusted Avg", "Strike Rate",
        "Boundary %", "Raw Rating", "Reliability Rating"
    ]

    st.dataframe(
        table_view.style.format({
            "Batting Avg": "{:.1f}",
            "Adjusted Avg": "{:.1f}",
            "Strike Rate": "{:.1f}",
            "Boundary %": "{:.1f}%",
            "Raw Rating": "{:.1f}",
            "Reliability Rating": "{:.1f}",
        }),
        use_container_width=True,
        height=380,
    )

    # Methodology & Academic Transparency Card
    _render_methodology_card(phase_key)


def _render_all_phases_overview(ratings_df: pd.DataFrame):
    """Renders cross-phase distribution analysis."""
    st.markdown(
        '<div class="info-callout" style="border-left-color: #FFB800;">'
        '<b>Cross-Phase Distribution Analysis:</b> How player ratings spread across Powerplay (Gold), Middle (Purple), and Death (Red) overs. '
        'Notice that Death overs features the highest variance and lowest correlation with traditional career statistics.'
        '</div>',
        unsafe_allow_html=True,
    )

    dist_fig = create_rating_distribution_chart(ratings_df)
    st.plotly_chart(dist_fig, use_container_width=True)

    # Summary table across phases
    st.markdown(render_section_header("Phase Comparison Matrix", "League baselines and participant volume"), unsafe_allow_html=True)
    
    summary_rows = []
    for p_name, meta in PHASES.items():
        sub = ratings_df[ratings_df["phase"] == p_name]
        summary_rows.append({
            "Phase": meta["label"],
            "Qualified Batters": len(sub),
            "League Strike Rate": f"{meta['league_sr']:.1f}",
            "League Batting Avg": f"{meta['league_avg']:.1f}",
            "League Boundary %": f"{meta['league_boundary_pct']:.1f}%",
            "Highest Rating Batter": sub.sort_values("reliability_adjusted_rating", ascending=False).iloc[0]["batter"],
            "Top Rating": f"{sub['reliability_adjusted_rating'].max():.1f}",
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)


def _render_methodology_card(phase_name: str):
    """Renders transparent documentation of the calculation methodology."""
    with st.expander(f"🔬 Methodology & Statistical Calculation Details — {phase_name}", expanded=False):
        st.markdown(f"""
        ### Phase-Aware Batting Rating Architecture
        
        **1. Relative Advantage Above League Baseline:**
        Each batter's traditional metrics are contextualized against the overall league baseline for that phase:
        - **Strike Rate Advantage (%):** `(Batter SR / League Phase SR - 1) * 100`
        - **Average Advantage (%):** `(Batter Avg / League Phase Avg - 1) * 100`
        - **Boundary Advantage (%):** `(Batter Boundary % / League Phase Boundary % - 1) * 100`
        
        **2. Standardization (Z-Scores):**
        Within each phase, each advantage metric is converted to a Z-score ($\mu=0, \sigma=1$):
        `Z = (Metric Advantage - Phase Mean) / Phase StdDev`
        
        **3. Composite Rating:**
        A weighted composite score is computed using domain weights:
        `Raw Score = 0.40 * Z_SR + 0.40 * Z_Avg + 0.20 * Z_Boundary`
        
        Rescaled to a familiar 0–100 index centered at 50 ($\mu=50, \sigma=10$):
        `Phase-Aware Batting Rating = 50 + 10 * Raw Score`
        
        **4. Empirical Bayes Reliability Adjustment:**
        To prevent lower-order batters with very few dismissals (e.g. 2–3 dismissals over a small sample) from achieving distorted infinite or extreme averages, a shrinkage prior of 10 dismissals is incorporated:
        
        $$\\text{{Adjusted Batting Average}} = \\frac{{\\text{{Total Runs}} + 10 \\times \\text{{League Batting Average}}}}{{\\text{{Dismissals}} + 10}}$$
        
        This penalizes high-variance small dismissal counts while retaining pure strike-rate impact.
        
        > **Academic Transparency Notice:** These ratings are experimental research metrics developed for contextual sports evaluation. As demonstrated in our temporal validation study, historical T20 phase ratings have modest persistence ($r_s = 0.141$), reflecting high natural variance in short-format cricket. They are not official ICC/IPL ratings.
        """)

