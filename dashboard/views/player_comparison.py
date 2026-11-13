"""
Player Comparison View for IPL Batter Intelligence & Strategy Platform.
Enables side-by-side head-to-head radar analysis, franchise color styling,
and phase-by-phase tactical matrices.
"""

import streamlit as st
import pandas as pd
from dashboard.config import TEAM_COLORS, PHASES, PHASE_COLORS
from dashboard.styles import render_section_header, render_player_card, render_kpi
from dashboard.data_service import (
    get_all_batters_list,
    get_batter_career_summary,
    get_batter_team_mapping,
)
from dashboard.components.charts import create_player_radar_comparison


def render_player_comparison_view():
    """Renders the multi-batter comparative intelligence module."""
    st.markdown(
        render_section_header(
            "Player Comparison Engine",
            "Multi-batter head-to-head radar analysis and phase performance breakdown",
        ),
        unsafe_allow_html=True,
    )

    all_batters = get_all_batters_list()
    
    # Selector Controls
    col_sel1, col_sel2, col_sel3 = st.columns(3)
    with col_sel1:
        batter1 = st.selectbox("Select Batter 1", options=all_batters, index=0)
    with col_sel2:
        batter2 = st.selectbox("Select Batter 2", options=all_batters, index=1 if len(all_batters) > 1 else 0)
    with col_sel3:
        include_third = st.checkbox("Add 3rd Batter", value=True)
        batter3 = None
        if include_third:
            batter3 = st.selectbox("Select Batter 3", options=all_batters, index=4 if len(all_batters) > 4 else 0)

    selected_names = [b for b in [batter1, batter2, batter3] if b]
    # Remove duplicates preserving order
    selected_names = list(dict.fromkeys(selected_names))

    if len(selected_names) < 2:
        st.warning("Please select at least two distinct batters to compare.")
        return

    # Load career summaries
    players_data = [get_batter_career_summary(name) for name in selected_names]

    # 1. Player Profile Cards Row (with official franchise colors)
    st.markdown("<br>", unsafe_allow_html=True)
    card_cols = st.columns(len(players_data))
    for col, p_dict in zip(card_cols, players_data):
        with col:
            st.markdown(
                render_player_card(
                    batter_name=p_dict["batter"],
                    team_name=p_dict["team"],
                    runs=p_dict["runs"],
                    balls=p_dict["balls"],
                    sr=p_dict["strike_rate"],
                    avg=p_dict["batting_average"],
                ),
                unsafe_allow_html=True,
            )

    # 2. Interactive Radar / Spider Chart
    st.markdown("<br>", unsafe_allow_html=True)
    radar_col, insight_col = st.columns([1.3, 1.0])
    
    with radar_col:
        fig_radar = create_player_radar_comparison(players_data)
        st.plotly_chart(fig_radar, use_container_width=True)

    with insight_col:
        st.markdown(render_section_header("Tactical Edge Highlights"), unsafe_allow_html=True)
        
        # Compare highest runs, SR, Avg, and Phase Ratings
        best_runs = max(players_data, key=lambda x: x["runs"])
        best_sr = max(players_data, key=lambda x: x["strike_rate"])
        best_avg = max(players_data, key=lambda x: x["batting_average"])
        best_b = max(players_data, key=lambda x: x["boundary_pct"])

        st.markdown(
            f'<div style="display: flex; flex-direction: column; gap: 12px; margin-top: 10px;">'
            f'<div class="kpi-card" style="border-left: 3px solid #FFB800;">'
            f'<div class="kpi-label">Highest Career Volume</div>'
            f'<div class="kpi-value" style="font-size: 1.5rem;">{best_runs["batter"]}</div>'
            f'<div class="kpi-sub" style="color: #FFB800;">{best_runs["runs"]:,} Runs in {best_runs["matches"]} Matches</div>'
            f'</div>'
            f'<div class="kpi-card" style="border-left: 3px solid #8A4FFF;">'
            f'<div class="kpi-label">Superior Strike Velocity</div>'
            f'<div class="kpi-value" style="font-size: 1.5rem;">{best_sr["batter"]}</div>'
            f'<div class="kpi-sub" style="color: #8A4FFF;">SR {best_sr["strike_rate"]:.1f} ({best_b["boundary_pct"]:.1f}% Boundaries)</div>'
            f'</div>'
            f'<div class="kpi-card" style="border-left: 3px solid #E63946;">'
            f'<div class="kpi-label">Wicket Preservation Master</div>'
            f'<div class="kpi-value" style="font-size: 1.5rem;">{best_avg["batter"]}</div>'
            f'<div class="kpi-sub" style="color: #E63946;">Batting Average {best_avg["batting_average"]:.1f} Runs / Dismissal</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # 3. Phase-by-Phase Performance Matrix
    st.markdown(render_section_header("Phase Dominance Matrix", "Detailed breakdown across Powerplay, Middle, and Death overs"), unsafe_allow_html=True)
    
    matrix_rows = []
    for phase_key, meta in PHASES.items():
        phase_label = meta["label"]
        for p_dict in players_data:
            b_name = p_dict["batter"]
            p_stats = p_dict["phase_ratings"].get(phase_key)
            if p_stats:
                matrix_rows.append({
                    "Phase": phase_label,
                    "Batter": b_name,
                    "Franchise": p_dict["team"],
                    "Runs": p_stats["runs"],
                    "Balls": p_stats["balls"],
                    "Strike Rate": f"{p_stats['sr']:.1f}",
                    "Batting Avg": f"{p_stats['avg']:.1f}",
                    "Boundary %": f"{p_stats['boundary_pct']:.1f}%",
                    "Reliability Rating": f"{p_stats['rating']:.1f}",
                })
            else:
                matrix_rows.append({
                    "Phase": phase_label,
                    "Batter": b_name,
                    "Franchise": p_dict["team"],
                    "Runs": 0,
                    "Balls": "< 200",
                    "Strike Rate": "N/A",
                    "Batting Avg": "N/A",
                    "Boundary %": "N/A",
                    "Reliability Rating": "Unranked (<200 balls)",
                })
                
    st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True)

