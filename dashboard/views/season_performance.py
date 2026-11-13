
"""
Season-wise Player Performance View for IPL Batter Intelligence & Strategy Platform.
Tracks career trajectories, phase adaptation across seasons, and milestone progressions.
"""

import streamlit as st
import pandas as pd

from dashboard.config import TEAM_COLORS
from dashboard.styles import (
    render_section_header,
    render_player_card,
    render_kpi,
)

from dashboard.data_service import (
    get_all_batters_list,
    get_batter_career_summary,
    get_batter_season_trajectory,
    get_batter_phase_by_season,
)

from dashboard.components.charts import (
    create_season_trajectory_chart,
    create_season_phase_stack_chart,
)


def render_season_performance_view():
    """Renders the player season-by-season trajectory and career breakdown module."""

    st.markdown(
        render_section_header(
            "Season-wise Career Trajectory",
            "Trace year-by-year evolution, boundary rates, and phase adaptation of any IPL batter",
        ),
        unsafe_allow_html=True,
    )

    all_batters = get_all_batters_list()

    # --------------------------------------------------------
    # 1. PLAYER SELECTION
    # --------------------------------------------------------

    c_sel1, c_sel2 = st.columns([2, 1])

    with c_sel1:
        selected_batter = st.selectbox(
            "Select or Search Batter",
            options=all_batters,
            index=0,
            help="Search among historical and contemporary IPL batters.",
        )

    summary = get_batter_career_summary(selected_batter)

    if not summary:
        st.error("No historical data found for the selected player.")
        return

    # Load season-wise data
    season_df = get_batter_season_trajectory(selected_batter)
    phase_season_df = get_batter_phase_by_season(selected_batter)

    if season_df.empty:
        st.warning("No season-wise records available for this player.")
        return

    # --------------------------------------------------------
    # 2. SEASON SELECTOR
    # --------------------------------------------------------

    available_seasons = sorted(
        season_df["season"].astype(str).unique().tolist(),
        reverse=True,
    )

    with c_sel2:
        selected_season = st.selectbox(
            "Select IPL Season",
            options=available_seasons,
            index=0,
            key="season_performance_selected_season",
        )

    selected_season_row = season_df[
        season_df["season"].astype(str) == str(selected_season)
    ]

    if selected_season_row.empty:
        st.error("No statistics found for the selected season.")
        return

    season_stats = selected_season_row.iloc[0]

    # Use the team recorded in the player's season-wise data.
    team_name = str(season_stats["team"])

    team_color = TEAM_COLORS.get(
        team_name, {}
    ).get("primary", "#FFB800")

    # --------------------------------------------------------
    # 3. SEASON-SPECIFIC PLAYER PROFILE
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        render_section_header(
            f"{selected_season} Season Profile",
            f"{selected_batter} | {team_name}",
        ),
        unsafe_allow_html=True,
    )

    card_col, kpi_col1, kpi_col2, kpi_col3 = st.columns(
        [1.5, 1, 1, 1]
    )

    with card_col:
        st.markdown(
            render_player_card(
                batter_name=selected_batter,
                team_name=team_name,
                runs=int(season_stats["runs"]),
                balls=int(season_stats["balls"]),
                sr=float(season_stats["strike_rate"]),
                avg=float(season_stats["batting_average"]),
                season=selected_season,
            ),
            unsafe_allow_html=True,
        )

        st.caption(
            f"Season-specific player profile · IPL {selected_season}"
        )

    with kpi_col1:
        st.markdown(
            render_kpi(
                "Matches",
                f"{int(season_stats['matches']):,}",
                "Matches played",
                accent_color=team_color,
            ),
            unsafe_allow_html=True,
        )

    with kpi_col2:
        st.markdown(
            render_kpi(
                "Fours / Sixes",
                f"{int(season_stats['fours'])} / {int(season_stats['sixes'])}",
                "Boundary count",
                accent_color="#FFB800",
            ),
            unsafe_allow_html=True,
        )

    with kpi_col3:
        st.markdown(
            render_kpi(
                "50s / 100s",
                f"{int(season_stats['fifties'])} / {int(season_stats['hundreds'])}",
                "Major milestones",
                accent_color="#E63946",
            ),
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # 4. CAREER SUMMARY
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        render_section_header(
            "Overall Career Summary",
            "Combined performance across all IPL seasons",
        ),
        unsafe_allow_html=True,
    )

    career_col1, career_col2, career_col3 = st.columns(3)

    with career_col1:
        st.markdown(
            render_kpi(
                "Career Runs",
                f"{summary['runs']:,}",
                "Total IPL runs",
                accent_color="#FFB800",
            ),
            unsafe_allow_html=True,
        )

    with career_col2:
        st.markdown(
            render_kpi(
                "Career Strike Rate",
                f"{summary['strike_rate']:.1f}",
                "Overall scoring rate",
                accent_color="#00B4D8",
            ),
            unsafe_allow_html=True,
        )

    with career_col3:
        st.markdown(
            render_kpi(
                "Career Average",
                f"{summary['batting_average']:.1f}",
                "Overall batting average",
                accent_color="#E63946",
            ),
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # 5. SEASON TRAJECTORY AND PHASE ANALYSIS
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    v_col1, v_col2 = st.columns([1.2, 1.0])

    with v_col1:
        fig_traj = create_season_trajectory_chart(
            season_df,
            selected_batter,
            team_name,
        )

        st.plotly_chart(
            fig_traj,
            use_container_width=True,
        )

    with v_col2:
        fig_stack = create_season_phase_stack_chart(
            phase_season_df,
            selected_batter,
        )

        st.plotly_chart(
            fig_stack,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # 6. SEASON-BY-SEASON STATISTICAL LOGBOOK
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        render_section_header(
            "Season-by-Season Statistical Logbook"
        ),
        unsafe_allow_html=True,
    )

    display_season_df = season_df[
        [
            "season",
            "team",
            "matches",
            "runs",
            "balls",
            "dismissals",
            "strike_rate",
            "batting_average",
            "fours",
            "sixes",
            "fifties",
            "hundreds",
        ]
    ].copy()

    display_season_df.columns = [
        "Season",
        "Team",
        "Matches",
        "Runs",
        "Balls",
        "Dismissals",
        "Strike Rate",
        "Batting Avg",
        "4s",
        "6s",
        "50s",
        "100s",
    ]

    st.dataframe(
        display_season_df.style.format(
            {
                "Strike Rate": "{:.1f}",
                "Batting Avg": "{:.1f}",
            }
        ),
        use_container_width=True,
        height=340,
    )
