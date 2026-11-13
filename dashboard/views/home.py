"""
Homepage View for IPL Batter Intelligence & Strategy Platform.
Features stadium charcoal background, IPL franchise color identity, headline metrics, and module portals.
"""

import streamlit as st
import pandas as pd
from dashboard.styles import render_hero, render_kpi, render_section_header
from dashboard.data_service import (
    get_headline_metrics,
    get_top_run_scorers,
    load_team_performance,
)
from dashboard.components.charts import (
    create_all_time_runs_chart,
    create_franchise_win_chart,
)


def render_home_view():
    """Renders the executive homepage with IPL franchise visual identity."""
    # 1. Cinematic Hero Section
    st.markdown(
        render_hero(
            title="IPL INSIGHT",
            subtitle="Advanced T20 Batter Intelligence & Strategy Platform. Contextual player evaluation, Empirical Bayes reliability adjustments, and phase-specific strategic benchmarks derived from 1,243 IPL matches.",
            badge="IPL ANALYTICS SUITE",
        ),
        unsafe_allow_html=True,
    )

    # 2. Executive Headline KPI Bar
    metrics = get_headline_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi("Matches Analyzed", f"{metrics['total_matches']:,}", f"{metrics['season_range']}", accent_color="#FFB800"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi("Deliveries Tracked", f"{metrics['total_deliveries']:,}", "Ball-by-Ball Tracking", accent_color="#004BA0"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi("Batters Evaluated", f"{metrics['total_batters']:,}", "739 Career Profiles", accent_color="#8A4FFF"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi("Total Runs Scored", f"{metrics['total_runs']:,}", f"{metrics['total_fours'] + metrics['total_sixes']:,} Boundaries", accent_color="#E63946"), unsafe_allow_html=True)

    # 3. Data Source Distinction Notice
    st.markdown(
        '<div class="info-callout">'
        '<b>Data Architecture Notice:</b> Historical macro metrics are calculated from the consolidated ball-by-ball Python dataset (2008–2026). MySQL relational analysis focuses strictly on deep team phase dynamics for the 2024–2025 tournament editions.'
        '</div>',
        unsafe_allow_html=True
    )

    # 4. Interactive Historical Milestones & Franchises
    st.markdown(render_section_header("Historical Macro Intelligence", "Career run leaderboards and official franchise win percentages"), unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns([1, 1])
    
    with chart_col1:
        top_scorers = get_top_run_scorers(10)
        fig_runs = create_all_time_runs_chart(top_scorers)
        st.plotly_chart(fig_runs, use_container_width=True)

    with chart_col2:
        team_perf = load_team_performance()
        if not team_perf.empty:
            fig_teams = create_franchise_win_chart(team_perf)
            st.plotly_chart(fig_teams, use_container_width=True)
        else:
            st.info("Franchise performance data loading...")

    # 5. Core Platform Module Portals
    st.markdown(render_section_header("Analytics Modules", "Explore specialized batter intelligence tools"), unsafe_allow_html=True)
    
    mod_col1, mod_col2, mod_col3 = st.columns(3)
    
    with mod_col1:
        st.markdown(
            '<div class="feature-card">'
            '<div>'
            '<div class="feature-badge" style="background: rgba(255, 184, 0, 0.15); color: #FFB800; border-color: rgba(255, 184, 0, 0.4);">PHASE MODULE</div>'
            '<div class="feature-title">⚡ Phase Intelligence</div>'
            '<div class="feature-desc">'
            'Deconstruct batter impact across Powerplay (Gold), Middle (Purple), and Death (Red) overs against league baselines.'
            '</div>'
            '</div>'
            '<div class="feature-stat" style="color: #FFB800;">334 Qualified Batter-Phases</div>'
            '</div>',
            unsafe_allow_html=True
        )
        
    with mod_col2:
        st.markdown(
            '<div class="feature-card">'
            '<div>'
            '<div class="feature-badge" style="background: rgba(0, 75, 160, 0.2); color: #4B90E2; border-color: rgba(0, 75, 160, 0.5);">COMPARISON</div>'
            '<div class="feature-title">⚔️ Player Comparison</div>'
            '<div class="feature-desc">'
            'Side-by-side head-to-head radar analysis comparing phase dominance, boundary conversion, and consistency in franchise colors.'
            '</div>'
            '</div>'
            '<div class="feature-stat" style="color: #FFB800;">Multi-Batter Radar Matrix</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with mod_col3:
        st.markdown(
            '<div class="feature-card">'
            '<div>'
            '<div class="feature-badge" style="background: rgba(138, 79, 255, 0.2); color: #8A4FFF; border-color: rgba(138, 79, 255, 0.5);">TRAJECTORY</div>'
            '<div class="feature-title">📈 Season-wise Trajectory</div>'
            '<div class="feature-desc">'
            'Trace the career evolution, milestones, boundary rates, and phase adaptation of any IPL batter across 19 tournament editions.'
            '</div>'
            '</div>'
            '<div class="feature-stat" style="color: #8A4FFF;">739 Batter Profiles</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    mod_col4, mod_col5, mod_col6 = st.columns(3)
    
    with mod_col4:
        st.markdown(
            '<div class="feature-card">'
            '<div>'
            '<div class="feature-badge" style="background: rgba(230, 57, 70, 0.2); color: #E63946; border-color: rgba(230, 57, 70, 0.5);">SCOUTING</div>'
            '<div class="feature-title">🎯 Player Scouting & Roles</div>'
            '<div class="feature-desc">'
            'Data-driven player archetypes: Powerplay Enforcers, Spin Tacklers, Death Finishers, with explicit sample thresholds.'
            '</div>'
            '</div>'
            '<div class="feature-stat" style="color: #E63946;">Empirical Bayes Shrinkage</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with mod_col5:
        st.markdown(
            '<div class="feature-card">'
            '<div>'
            '<div class="feature-badge" style="background: rgba(255, 184, 0, 0.15); color: #FFB800; border-color: rgba(255, 184, 0, 0.4);">RELATIONAL SQL</div>'
            '<div class="feature-title">🗄️ SQL Analysis Insights</div>'
            '<div class="feature-desc">'
            'Explore 2024–2025 team phase run rates, boundary dependency, and wickets lost derived via relational SQL aggregations.'
            '</div>'
            '</div>'
            '<div class="feature-stat" style="color: #FFB800;">MySQL ipl_analytics Database</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with mod_col6:
        st.markdown(
            '<div class="feature-card">'
            '<div>'
            '<div class="feature-badge" style="background: rgba(255, 255, 255, 0.1); color: #cbd5e1; border-color: rgba(255, 255, 255, 0.2);">METHODOLOGY</div>'
            '<div class="feature-title">🔬 Scientific Validation</div>'
            '<div class="feature-desc">'
            'Transparent correlation audits testing historical rating persistence in out-of-sample seasons (Spearman r = 0.141).'
            '</div>'
            '</div>'
            '<div class="feature-stat" style="color: #cbd5e1;">Peer-Review Standard</div>'
            '</div>',
            unsafe_allow_html=True
        )

