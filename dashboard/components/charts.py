"""
Interactive Plotly charts styled for the IPL sports-tech visual identity.
Features stadium charcoal palette, franchise color mapping, and gold/purple/red phase colors.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboard.config import COLORS, PHASES, TEAM_COLORS, PHASE_COLORS


def apply_sports_theme(fig: go.Figure, height: int = 500) -> go.Figure:
    """Applies stadium charcoal sports-tech aesthetic to any Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(14, 18, 28, 0.6)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0", size=12),
        margin=dict(l=40, r=40, t=50, b=40),
        height=height,
        hoverlabel=dict(
            bgcolor="#121722",
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor="#FFB800",
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 184, 0, 0.25)",
        tickfont=dict(color="#94a3b8"),
        title_font=dict(color="#FFB800", size=13),
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 184, 0, 0.25)",
        tickfont=dict(color="#94a3b8"),
        title_font=dict(color="#FFB800", size=13),
    )
    return fig


def create_phase_quadrant_chart(
    df: pd.DataFrame, 
    phase_name: str, 
    rating_col: str = "reliability_adjusted_rating"
) -> go.Figure:
    """Interactive quadrant scatter plot with phase-specific colors and baseline crosshairs."""
    phase_meta = PHASES.get(phase_name, {})
    league_sr = phase_meta.get("league_sr", 130.0)
    league_avg = phase_meta.get("league_avg", 30.0)
    phase_color = phase_meta.get("color", "#FFB800")
    
    rating_label = "Reliability-Adjusted Rating" if rating_col == "reliability_adjusted_rating" else "Raw Phase Rating"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["batting_average"],
            y=df["strike_rate"],
            mode="markers",
            marker=dict(
                size=df["balls_faced"],
                sizemode="area",
                sizeref=2.0 * max(df["balls_faced"]) / (28.0 ** 2),
                sizemin=6,
                color=df[rating_col],
                colorscale=[
                    [0.0, "#254AA5"],     # Deep Royal Blue
                    [0.4, phase_color],   # Phase Primary (Gold/Purple/Red)
                    [1.0, "#FFD700"],     # Bright Trophy Gold
                ],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Rating", font=dict(color="#FFB800", size=12)),
                    tickfont=dict(color="#94a3b8"),
                    thickness=12,
                    len=0.8,
                ),
                line=dict(width=1, color="rgba(255, 255, 255, 0.4)"),
                opacity=0.9,
            ),
            text=df["batter"],
            customdata=df[[
                "total_runs", "balls_faced", "dismissals", 
                "boundary_percentage", rating_col
            ]],
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Strike Rate: <b>%{y:.1f}</b> (League: " + f"{league_sr:.1f})<br>" +
                "Batting Avg: <b>%{x:.1f}</b> (League: " + f"{league_avg:.1f})<br>" +
                "Total Runs: %{customdata[0]:,}<br>" +
                "Balls Faced: %{customdata[1]:,}<br>" +
                "Dismissals: %{customdata[2]}<br>" +
                "Boundary %: %{customdata[3]:.1f}%<br>" +
                f"{rating_label}: <b>" + "%{customdata[4]:.1f}</b>" +
                "<extra></extra>"
            ),
        )
    )

    # League Baseline Crosshairs in Phase Color
    fig.add_vline(
        x=league_avg, 
        line_dash="dash", 
        line_color=phase_color,
        opacity=0.65,
        annotation_text=f"League Avg: {league_avg:.1f}",
        annotation_position="top left",
        annotation_font=dict(color=phase_color, size=11),
    )
    fig.add_hline(
        y=league_sr, 
        line_dash="dash", 
        line_color=phase_color,
        opacity=0.65,
        annotation_text=f"League SR: {league_sr:.1f}",
        annotation_position="bottom right",
        annotation_font=dict(color=phase_color, size=11),
    )

    # Quadrant Strategy Watermark Labels
    max_x = df["batting_average"].max() * 0.95
    min_x = df["batting_average"].min() * 1.05
    max_y = df["strike_rate"].max() * 0.98
    min_y = df["strike_rate"].min() * 1.02

    fig.add_annotation(
        x=max_x, y=max_y,
        text="⚡ ELITE DOMINATORS<br>(High SR & High Avg)",
        showarrow=False,
        font=dict(color="rgba(255, 184, 0, 0.5)", size=12, family="Rajdhani"),
        align="right"
    )
    fig.add_annotation(
        x=min_x, y=max_y,
        text="🚀 ACCELERATORS<br>(High Impact / Lower Avg)",
        showarrow=False,
        font=dict(color="rgba(230, 57, 70, 0.5)", size=12, family="Rajdhani"),
        align="left"
    )
    fig.add_annotation(
        x=max_x, y=min_y,
        text="🛡️ STABLE ANCHORS<br>(Wicket Preservation)",
        showarrow=False,
        font=dict(color="rgba(138, 79, 255, 0.5)", size=12, family="Rajdhani"),
        align="right"
    )

    fig.update_layout(
        title=dict(
            text=f"Phase Quadrant Matrix — {phase_name} Overs (Balls Faced $\\ge$ min)",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        xaxis_title="Batting Average",
        yaxis_title="Strike Rate",
    )

    return apply_sports_theme(fig, height=520)


def create_top_batters_bar_chart(
    df: pd.DataFrame, 
    phase_name: str, 
    top_n: int = 10,
    rating_col: str = "reliability_adjusted_rating"
) -> go.Figure:
    """Horizontal bar chart showing top N batters by rating in the selected phase."""
    top_df = df.sort_values(rating_col, ascending=False).head(top_n).copy()
    top_df = top_df.sort_values(rating_col, ascending=True)

    phase_color = PHASE_COLORS.get(phase_name, "#FFB800")
    label = "Reliability-Adjusted Rating" if rating_col == "reliability_adjusted_rating" else "Raw Phase Rating"

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=top_df["batter"],
            x=top_df[rating_col],
            orientation="h",
            marker=dict(
                color=top_df[rating_col],
                colorscale=[
                    [0.0, "rgba(22, 28, 42, 0.8)"],
                    [0.5, phase_color],
                    [1.0, "#FFD700"],
                ],
                line=dict(color="rgba(255, 184, 0, 0.4)", width=1),
            ),
            text=[f"{v:.1f} (SR: {sr:.0f})" for v, sr in zip(top_df[rating_col], top_df["strike_rate"])],
            textposition="inside",
            insidetextanchor="end",
            textfont=dict(color="#000000", family="Rajdhani", size=12, weight="bold"),
            customdata=top_df[["total_runs", "balls_faced", "strike_rate", "batting_average"]],
            hovertemplate=(
                "<b>%{y}</b><br>" +
                f"{label}: <b>" + "%{x:.2f}</b><br>" +
                "Strike Rate: %{customdata[2]:.1f}<br>" +
                "Batting Avg: %{customdata[3]:.1f}<br>" +
                "Total Runs: %{customdata[0]:,}<br>" +
                "Balls Faced: %{customdata[1]:,}" +
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Top {top_n} Batters — {phase_name} ({label})",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        xaxis_title=label,
        yaxis_title="",
        xaxis=dict(range=[40, max(top_df[rating_col].max() * 1.08, 80)]),
    )

    return apply_sports_theme(fig, height=440)


def create_rating_distribution_chart(ratings_df: pd.DataFrame) -> go.Figure:
    """Boxplot of ratings across all 3 match phases using Gold, Purple, Red."""
    fig = go.Figure()
    
    color_map = {
        "Powerplay": PHASE_COLORS["Powerplay"],  # Gold
        "Middle": PHASE_COLORS["Middle"],        # Purple
        "Death": PHASE_COLORS["Death"],          # Red
    }
    
    for phase in ["Powerplay", "Middle", "Death"]:
        sub = ratings_df[ratings_df["phase"] == phase]
        fig.add_trace(
            go.Box(
                y=sub["reliability_adjusted_rating"],
                name=phase,
                marker_color=color_map.get(phase, "#FFB800"),
                boxmean=True,
                boxpoints="outliers",
                customdata=sub[["batter", "strike_rate", "batting_average"]],
                hovertemplate=(
                    "<b>%{name} Phase</b><br>" +
                    "Rating: <b>%{y:.1f}</b>" +
                    "<extra></extra>"
                ),
            )
        )
        
    fig.update_layout(
        title=dict(
            text="Rating Distribution & Spread by Innings Phase",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        yaxis_title="Reliability-Adjusted Rating",
        showlegend=False,
    )
    return apply_sports_theme(fig, height=360)


def create_all_time_runs_chart(top_scorers_df: pd.DataFrame) -> go.Figure:
    """Bar chart for top 10 all-time run scorers on homepage with trophy gold accents."""
    df_sorted = top_scorers_df.sort_values("runs", ascending=True)
    
    fig = go.Figure(
        go.Bar(
            y=df_sorted["batter"],
            x=df_sorted["runs"],
            orientation="h",
            marker=dict(
                color=df_sorted["runs"],
                colorscale=[[0, "#3A225D"], [0.5, "#004BA0"], [1, "#FFB800"]],
                line=dict(color="rgba(255, 184, 0, 0.4)", width=1),
            ),
            text=[f"{int(r):,} runs ({sr:.1f} SR)" for r, sr in zip(df_sorted["runs"], df_sorted["strike_rate"])],
            textposition="inside",
            insidetextanchor="end",
            textfont=dict(color="#0a0c12", family="Rajdhani", size=12, weight="bold"),
            hovertemplate="<b>%{y}</b><br>Runs: %{x:,}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="IPL All-Time Leading Run Scorers", font=dict(color="#ffffff", size=16, family="Rajdhani")),
        xaxis_title="Total Runs Scored",
        yaxis_title="",
    )
    return apply_sports_theme(fig, height=440)


def create_franchise_win_chart(team_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart for historical franchise win percentages using franchise colors."""
    df_sorted = team_df.sort_values("Win Percentage", ascending=True).copy()
    
    # Map each team to its primary franchise color
    bar_colors = [
        TEAM_COLORS.get(team, {}).get("primary", "#FFB800")
        for team in df_sorted["Team"]
    ]
    
    fig = go.Figure(
        go.Bar(
            y=df_sorted["Team"],
            x=df_sorted["Win Percentage"],
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(color="rgba(255, 255, 255, 0.2)", width=1)
            ),
            text=[f"{p:.1f}% ({w}/{m} W)" for p, w, m in zip(
                df_sorted["Win Percentage"], df_sorted["Matches Won"], df_sorted["Matches Played"]
            )],
            textposition="auto",
            textfont=dict(family="Rajdhani", size=11, color="#ffffff"),
            hovertemplate="<b>%{y}</b><br>Win Rate: %{x:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Franchise Historical Win Percentages (Official Team Colors)", font=dict(color="#ffffff", size=16, family="Rajdhani")),
        xaxis_title="Win Percentage (%)",
        yaxis_title="",
    )
    return apply_sports_theme(fig, height=520)


# ==============================================================================
# STAGE 2 CHARTS
# ==============================================================================

def create_player_radar_comparison(players_data: list) -> go.Figure:
    """
    Creates an interactive Radar / Spider chart comparing 2 or 3 batters.
    Metrics: Powerplay Rating, Middle Rating, Death Rating, Strike Rate, Batting Avg, Boundary %.
    """
    categories = [
        "Powerplay Rating", 
        "Middle Rating", 
        "Death Rating", 
        "Overall SR Index", 
        "Batting Avg Index", 
        "Boundary % Index"
    ]
    
    fig = go.Figure()
    
    for p_dict in players_data:
        batter = p_dict["batter"]
        team = p_dict["team"]
        team_color = TEAM_COLORS.get(team, {}).get("primary", "#FFB800")
        
        pp_r = p_dict["phase_ratings"].get("Powerplay")
        mid_r = p_dict["phase_ratings"].get("Middle")
        death_r = p_dict["phase_ratings"].get("Death")
        
        # Scale traditional stats to 0-100 index for radar alignment
        sr_idx = min(p_dict["strike_rate"] / 2.0, 100)        # SR 200 = 100 index
        avg_idx = min(p_dict["batting_average"] * 2.0, 100)    # Avg 50 = 100 index
        b_idx = min(p_dict["boundary_pct"] * 3.5, 100)        # Boundary 28% = 100 index
        
        values = [
            pp_r["rating"] if pp_r else 40,
            mid_r["rating"] if mid_r else 40,
            death_r["rating"] if death_r else 40,
            sr_idx,
            avg_idx,
            b_idx
        ]
        # close the radar loop
        values.append(values[0])
        radar_categories = categories + [categories[0]]
        
        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=radar_categories,
                fill="toself",
                name=f"{batter} ({team})",
                line=dict(color=team_color, width=2.5),
                fillcolor=f"rgba({int(team_color[1:3], 16)}, {int(team_color[3:5], 16)}, {int(team_color[5:7], 16)}, 0.25)" if len(team_color) == 7 else "rgba(255, 184, 0, 0.25)",
            )
        )
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[20, 100],
                gridcolor="rgba(255, 255, 255, 0.08)",
                linecolor="rgba(255, 255, 255, 0.15)",
                tickfont=dict(color="#94a3b8", size=9),
            ),
            angularaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.08)",
                linecolor="rgba(255, 184, 0, 0.3)",
                tickfont=dict(color="#FFB800", size=11, family="Rajdhani"),
            ),
            bgcolor="rgba(14, 18, 28, 0.6)",
        ),
        title=dict(
            text="Head-to-Head Batter Radar Profile",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color="#cbd5e1"),
        ),
    )
    return apply_sports_theme(fig, height=480)


def create_season_trajectory_chart(season_df: pd.DataFrame, batter_name: str, team_name: str) -> go.Figure:
    """Dual-axis season trajectory chart: Runs (Bars in Team Color) and Strike Rate (Gold Line)."""
    team_color = TEAM_COLORS.get(team_name, {}).get("primary", "#FFB800")
    
    fig = go.Figure()
    
    # Bar trace: Runs Scored
    fig.add_trace(
        go.Bar(
            x=season_df["season"],
            y=season_df["runs"],
            name="Runs Scored",
            marker=dict(
                color=team_color,
                line=dict(color="rgba(255, 255, 255, 0.3)", width=1),
            ),
            text=season_df["runs"],
            textposition="auto",
            textfont=dict(family="Rajdhani", size=11, color="#ffffff"),
            customdata=season_df[["matches", "batting_average", "fours", "sixes"]],
            hovertemplate=(
                "<b>Season %{x}</b><br>" +
                "Runs: <b>%{y}</b><br>" +
                "Matches: %{customdata[0]}<br>" +
                "Average: %{customdata[1]:.1f}<br>" +
                "Boundaries: %{customdata[2]} 4s, %{customdata[3]} 6s" +
                "<extra></extra>"
            ),
            yaxis="y1",
        )
    )
    
    # Line trace: Strike Rate
    fig.add_trace(
        go.Scatter(
            x=season_df["season"],
            y=season_df["strike_rate"],
            name="Strike Rate",
            mode="lines+markers",
            line=dict(color="#FFB800", width=3),
            marker=dict(size=7, color="#FFB800", symbol="diamond"),
            hovertemplate="<b>Season %{x}</b><br>Strike Rate: <b>%{y:.1f}</b><extra></extra>",
            yaxis="y2",
        )
    )
    
    fig.update_layout(
        title=dict(
            text=f"Career Season Trajectory — {batter_name}",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        xaxis=dict(title="IPL Season", tickangle=-45),
        yaxis=dict(
            title="Total Runs",
            title_font=dict(color=team_color),
            tickfont=dict(color="#94a3b8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        yaxis2=dict(
            title="Strike Rate",
            title_font=dict(color="#FFB800"),
            tickfont=dict(color="#FFB800"),
            overlaying="y",
            side="right",
            range=[60, max(season_df["strike_rate"].max() * 1.15, 200)],
            showgrid=False,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#cbd5e1"),
        ),
    )
    return apply_sports_theme(fig, height=450)


def create_season_phase_stack_chart(phase_season_df: pd.DataFrame, batter_name: str) -> go.Figure:
    """Stacked bar chart showing runs scored across Powerplay (Gold), Middle (Purple), Death (Red)."""
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=phase_season_df["season"],
            y=phase_season_df["Powerplay"],
            name="Powerplay (1–6)",
            marker_color=PHASE_COLORS["Powerplay"],
            hovertemplate="Powerplay: %{y} runs<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=phase_season_df["season"],
            y=phase_season_df["Middle"],
            name="Middle (7–15)",
            marker_color=PHASE_COLORS["Middle"],
            hovertemplate="Middle: %{y} runs<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=phase_season_df["season"],
            y=phase_season_df["Death"],
            name="Death (16–20)",
            marker_color=PHASE_COLORS["Death"],
            hovertemplate="Death: %{y} runs<extra></extra>",
        )
    )
    
    fig.update_layout(
        barmode="stack",
        title=dict(
            text=f"Season Run Distribution by Match Phase — {batter_name}",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        xaxis=dict(title="IPL Season", tickangle=-45),
        yaxis=dict(title="Runs Scored"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#cbd5e1"),
        ),
    )
    return apply_sports_theme(fig, height=420)


def create_team_phase_run_rate_chart(sql_df: pd.DataFrame, target_season: int = 2024) -> go.Figure:
    """
    Grouped bar chart for 2024-2025 team phase run rates.
    Powerplay=Gold, Middle=Purple, Death=Red.
    """
    sub = sql_df[sql_df["season"] == target_season].copy()
    
    # Sort teams by season overall run rate descending
    teams_order = sub.drop_duplicates(subset=["batting_team"]).sort_values("season_run_rate", ascending=False)["batting_team"].tolist()
    
    fig = go.Figure()
    
    phase_keys = [
        ("Powerplay", PHASE_COLORS["Powerplay"]),
        ("Middle Overs", PHASE_COLORS["Middle"]),
        ("Death Overs", PHASE_COLORS["Death"]),
    ]
    
    for phase_name, color in phase_keys:
        phase_sub = sub[sub["match_phase"] == phase_name].set_index("batting_team").reindex(teams_order).reset_index()
        fig.add_trace(
            go.Bar(
                x=phase_sub["batting_team"],
                y=phase_sub["phase_run_rate"],
                name=phase_name,
                marker_color=color,
                text=[f"{r:.2f}" for r in phase_sub["phase_run_rate"]],
                textposition="auto",
                textfont=dict(family="Rajdhani", size=11, color="#ffffff"),
                customdata=phase_sub[["phase_runs", "legal_balls", "wickets_lost"]],
                hovertemplate=(
                    "<b>%{x} — " + phase_name + "</b><br>" +
                    "Run Rate: <b>%{y:.2f}</b> RPO<br>" +
                    "Runs: %{customdata[0]}<br>" +
                    "Legal Balls: %{customdata[1]}<br>" +
                    "Wickets Lost: %{customdata[2]}" +
                    "<extra></extra>"
                ),
            )
        )
        
    fig.update_layout(
        barmode="group",
        title=dict(
            text=f"Franchise Phase Run Rates ({target_season}) — SQL Analytics Output",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        xaxis=dict(title="Franchise", tickangle=-30),
        yaxis=dict(title="Run Rate (Runs per Over)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#cbd5e1"),
        ),
    )
    return apply_sports_theme(fig, height=480)


def create_team_boundary_dependency_chart(sql_df: pd.DataFrame, target_season: int = 2024) -> go.Figure:
    """Stacked bar chart comparing Boundary Runs vs Running Runs across phases for a season."""
    sub = sql_df[sql_df["season"] == target_season].copy()
    sub["running_runs"] = sub["phase_runs"] - sub["boundary_runs"]
    sub["boundary_pct"] = (sub["boundary_runs"] / sub["phase_runs"].replace(0, 1)) * 100
    
    # Aggregate across teams by phase
    phase_agg = sub.groupby("match_phase").agg(
        boundary_runs=("boundary_runs", "sum"),
        running_runs=("running_runs", "sum"),
        total_runs=("phase_runs", "sum")
    ).reset_index()
    
    phase_agg["boundary_pct"] = (phase_agg["boundary_runs"] / phase_agg["total_runs"]) * 100
    phase_agg["running_pct"] = (phase_agg["running_runs"] / phase_agg["total_runs"]) * 100
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=phase_agg["match_phase"],
            y=phase_agg["boundary_pct"],
            name="Boundary Runs (4s & 6s)",
            marker_color="#FFB800",
            text=[f"{v:.1f}%" for v in phase_agg["boundary_pct"]],
            textposition="auto",
            textfont=dict(family="Rajdhani", size=12, color="#0a0c12", weight="bold"),
        )
    )
    fig.add_trace(
        go.Bar(
            x=phase_agg["match_phase"],
            y=phase_agg["running_pct"],
            name="Running Runs (1s, 2s, 3s)",
            marker_color="#254AA5",
            text=[f"{v:.1f}%" for v in phase_agg["running_pct"]],
            textposition="auto",
            textfont=dict(family="Rajdhani", size=12, color="#ffffff"),
        )
    )
    
    fig.update_layout(
        barmode="stack",
        title=dict(
            text=f"Boundary vs Running Dependency by Phase ({target_season})",
            font=dict(color="#ffffff", size=16, family="Rajdhani"),
        ),
        xaxis=dict(title="Match Phase"),
        yaxis=dict(title="Share of Runs (%)", range=[0, 100]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#cbd5e1"),
        ),
    )
    return apply_sports_theme(fig, height=420)
