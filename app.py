"""
Main Application Entry Point for IPL Batter Intelligence & Strategy Platform.
Features a premium top horizontal navigation system, authentic player imagery,
and IPL franchise sports-tech visual identity.
"""

import streamlit as st

# Configure page metadata must be the first Streamlit command
st.set_page_config(
    page_title="IPL INSIGHT | Batter Intelligence & Strategy Platform",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from dashboard.styles import get_custom_css
from dashboard.views.home import render_home_view
from dashboard.views.phase_intelligence import render_phase_intelligence_view
from dashboard.views.player_comparison import render_player_comparison_view
from dashboard.views.season_performance import render_season_performance_view
from dashboard.views.player_scouting import render_player_scouting_view
from dashboard.views.sql_analysis import render_sql_analysis_view

# Inject IPL Franchise Sports-Tech Charcoal CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


def main():
    # =========================================================================
    # PREMIUM TOP HORIZONTAL NAVIGATION BAR
    # =========================================================================
    nav_col_logo, nav_col_menu, nav_col_badge = st.columns([1.5, 4.2, 1.3], vertical_alignment="center")

    with nav_col_logo:
        st.markdown(
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<div style="font-size: 1.85rem; line-height: 1;">🏏</div>'
            '<div>'
            '<div style="font-family: \'Rajdhani\', sans-serif; font-size: 1.55rem; font-weight: 800; color: #ffffff; letter-spacing: 1.5px; line-height: 1;">'
            'IPL <span style="color: #FFB800;">INSIGHT</span>'
            '</div>'
            '<div style="font-size: 0.65rem; color: #94a3b8; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; margin-top: 2px;">'
            'BATTER STRATEGY ENGINE'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with nav_col_menu:
        selected_page = st.radio(
            "top_navbar_page",
            options=[
                "Overview",
                "Phase Intelligence",
                "Player Comparison",
                "Season Performance",
                "Player Scouting",
                "SQL Insights",
            ],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            help="Navigate across the specialized IPL INSIGHT modules."
        )

    with nav_col_badge:
        st.markdown(
            '<div style="display: flex; justify-content: flex-end; align-items: center;">'
            '<div class="top-navbar-badge">'
            '<div class="live-pulse"></div>'
            '<span>2008–2026 | 1,243 M</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # Franchise Accent Bar separating navbar from body
    st.markdown(
        '<div style="height: 3px; background: linear-gradient(90deg, #D71920 0%, #EA1A85 15%, #004BA0 30%, #FFCB05 45%, #F26522 60%, #3A225D 75%, #1B2133 90%, #FFB800 100%); border-radius: 2px; margin: 8px 0 24px 0; opacity: 0.85;"></div>',
        unsafe_allow_html=True
    )

    # =========================================================================
    # SUPPLEMENTARY SIDEBAR (DATA AUDIT & ARCHITECTURE)
    # =========================================================================
    with st.sidebar:
        st.markdown(
            '<div style="padding: 10px 0 14px 0; border-bottom: 1px solid rgba(255, 184, 0, 0.2); margin-bottom: 14px;">'
            '<div style="font-family: \'Rajdhani\', sans-serif; font-size: 1.4rem; font-weight: 800; color: #ffffff; letter-spacing: 1px;">'
            'IPL <span style="color: #FFB800;">INSIGHT</span>'
            '</div>'
            '<div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600;">PLATFORM ARCHITECTURE</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="background: rgba(18, 23, 34, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px; margin-bottom: 14px;">'
            '<div style="font-size: 0.72rem; color: #FFB800; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 8px;">'
            'Match Phase Palette'
            '</div>'
            '<div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.78rem;">'
            '<div style="display: flex; align-items: center; gap: 8px;"><div style="width: 10px; height: 10px; border-radius: 50%; background: #FFB800;"></div><span style="color: #e2e8f0;">Powerplay (Overs 1–6)</span></div>'
            '<div style="display: flex; align-items: center; gap: 8px;"><div style="width: 10px; height: 10px; border-radius: 50%; background: #8A4FFF;"></div><span style="color: #e2e8f0;">Middle Overs (Overs 7–15)</span></div>'
            '<div style="display: flex; align-items: center; gap: 8px;"><div style="width: 10px; height: 10px; border-radius: 50%; background: #E63946;"></div><span style="color: #e2e8f0;">Death Overs (Overs 16–20)</span></div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="background: rgba(18, 23, 34, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px; margin-bottom: 14px;">'
            '<div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 6px;">'
            'Data Architecture'
            '</div>'
            '<div style="font-size: 0.78rem; color: #cbd5e1; line-height: 1.45;">'
            '• <b>Python Engine:</b> 295,732 Deliveries (2008–2026)<br>'
            '• <b>Phase Ratings:</b> 334 Qualified Batter Profiles<br>'
            '• <b>SQL Analytics:</b> 2024–2025 Team Phase Dynamics<br>'
            '• <b>Portraits:</b> Genuine CC / Wikimedia Commons'
            '</div>'
            '</div>'
            '<div style="font-size: 0.72rem; color: #7888a3; line-height: 1.35; padding: 0 4px;">'
            '<b>Academic Notice:</b> Developed as a Data Science portfolio project. Phase ratings incorporate Empirical Bayes shrinkage and out-of-sample temporal validation.'
            '</div>',
            unsafe_allow_html=True
        )

    # =========================================================================
    # ROUTE VIEWS VIA TOP HORIZONTAL NAVBAR
    # =========================================================================
    if selected_page == "Overview":
        render_home_view()
    elif selected_page == "Phase Intelligence":
        render_phase_intelligence_view()
    elif selected_page == "Player Comparison":
        render_player_comparison_view()
    elif selected_page == "Season Performance":
        render_season_performance_view()
    elif selected_page == "Player Scouting":
        render_player_scouting_view()
    elif selected_page == "SQL Insights":
        render_sql_analysis_view()


if __name__ == "__main__":
    main()
