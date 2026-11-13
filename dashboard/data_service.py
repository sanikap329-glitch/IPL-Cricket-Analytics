
"""
Data loader and caching service for IPL Batter Intelligence & Strategy Platform.
All computations and CSV loads are cached for fast, high-performance interactions.
"""

import streamlit as st
import pandas as pd
import numpy as np

from dashboard.config import (
    PATH_ALL_MATCHES,
    PATH_PHASE_RATINGS,
    PATH_TEMPORAL_VALIDATION,
    PATH_COMBINED_VALIDATION,
    PATH_CORRELATIONS,
    PATH_TEAM_PERFORMANCE_SQL,
    PATH_TEAM_PERFORMANCE_HIST,
    PHASES,
)


# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data(show_spinner="Loading IPL delivery records...")
def load_all_matches() -> pd.DataFrame:
    """Loads the complete delivery dataset."""
    if not PATH_ALL_MATCHES.exists():
        raise FileNotFoundError(
            f"Missing match deliveries dataset at {PATH_ALL_MATCHES}"
        )

    df = pd.read_csv(PATH_ALL_MATCHES, low_memory=False)
    df["season"] = df["season"].astype(str)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


@st.cache_data(show_spinner=False)
def load_phase_ratings() -> pd.DataFrame:
    """Loads precomputed phase-aware batting ratings."""
    if not PATH_PHASE_RATINGS.exists():
        raise FileNotFoundError(
            f"Missing phase batting ratings at {PATH_PHASE_RATINGS}"
        )

    return pd.read_csv(PATH_PHASE_RATINGS)


@st.cache_data(show_spinner=False)
def load_validation_summary() -> pd.DataFrame:
    """Loads temporal validation summary across phases."""
    if not PATH_COMBINED_VALIDATION.exists():
        return pd.DataFrame()

    return pd.read_csv(PATH_COMBINED_VALIDATION)


@st.cache_data(show_spinner=False)
def load_temporal_correlations() -> pd.DataFrame:
    """Loads detailed season/phase temporal validation correlations."""
    if not PATH_CORRELATIONS.exists():
        return pd.DataFrame()

    return pd.read_csv(PATH_CORRELATIONS)


@st.cache_data(show_spinner=False)
def load_team_performance() -> pd.DataFrame:
    """Loads franchise win-percentage history."""
    if not PATH_TEAM_PERFORMANCE_HIST.exists():
        return pd.DataFrame()

    return pd.read_csv(PATH_TEAM_PERFORMANCE_HIST)


@st.cache_data(show_spinner=False)
def load_sql_team_phase_summary() -> pd.DataFrame:
    """Loads SQL analytical summary of team phase performance."""
    if not PATH_TEAM_PERFORMANCE_SQL.exists():
        return pd.DataFrame()

    return pd.read_csv(PATH_TEAM_PERFORMANCE_SQL)


# ============================================================
# GENERAL BATTER FUNCTIONS
# ============================================================

@st.cache_data(show_spinner=False)
def get_all_batters_list() -> list:
    """Returns sorted list of all unique batters."""
    df = load_all_matches()

    runs_by_batter = (
        df.groupby("batter")["batter_runs"]
        .sum()
        .sort_values(ascending=False)
    )

    return runs_by_batter.index.tolist()


@st.cache_data(show_spinner=False)
def get_batter_team_mapping() -> dict:
    """Maps each batter to their latest franchise."""
    df = load_all_matches()

    sorted_df = df.sort_values("date") if "date" in df.columns else df

    return (
        sorted_df.groupby("batter")["batting_team"]
        .last()
        .to_dict()
    )


# ============================================================
# HEADLINE METRICS
# ============================================================

@st.cache_data(show_spinner=False)
def get_headline_metrics() -> dict:
    """Computes headline summary metrics."""
    df = load_all_matches()

    total_deliveries = len(df)
    total_matches = df["match_id"].nunique()
    total_batters = df["batter"].nunique()

    total_runs = int(
        (df["batter_runs"] + df["total_extras"].fillna(0)).sum()
    )

    total_fours = int((df["batter_runs"] == 4).sum())
    total_sixes = int((df["batter_runs"] == 6).sum())

    seasons = sorted(df["season"].unique())
    season_range = f"{seasons[0]} – {seasons[-1]}"

    return {
        "total_deliveries": total_deliveries,
        "total_matches": total_matches,
        "total_batters": total_batters,
        "total_runs": total_runs,
        "total_fours": total_fours,
        "total_sixes": total_sixes,
        "total_seasons": len(seasons),
        "season_range": season_range,
    }


# ============================================================
# TOP RUN SCORERS
# ============================================================

@st.cache_data(show_spinner=False)
def get_top_run_scorers(top_n: int = 10) -> pd.DataFrame:
    """Calculates all-time top run scorers."""
    df = load_all_matches()

    legal_balls = df[df["wides"].fillna(0) == 0]
    balls_faced = legal_balls.groupby("batter")["delivery_number"].count()

    runs_scored = df.groupby("batter")["batter_runs"].sum()
    matches_played = df.groupby("batter")["match_id"].nunique()

    fours = (
        df[df["batter_runs"] == 4]
        .groupby("batter")["batter_runs"]
        .count()
    )

    sixes = (
        df[df["batter_runs"] == 6]
        .groupby("batter")["batter_runs"]
        .count()
    )

    dismissal_methods = [
        "caught", "bowled", "run out", "lbw",
        "caught and bowled", "stumped", "hit wicket",
        "retired out", "obstructing the field"
    ]

    dismissal_df = df[
        df["dismissal_method"].isin(dismissal_methods)
    ].copy()

    dismissal_df["dismissed_batter"] = (
        dismissal_df["dismissed_players"]
        .fillna(dismissal_df["batter"])
    )

    dismissals = dismissal_df.groupby("dismissed_batter").size()

    summary = pd.DataFrame({
        "matches": matches_played,
        "runs": runs_scored,
        "balls": balls_faced,
        "dismissals": dismissals,
        "fours": fours,
        "sixes": sixes,
    }).fillna(0)

    summary.index.name = "batter"

    summary["batting_average"] = (
        summary["runs"] /
        summary["dismissals"].replace(0, np.nan)
    )

    summary["strike_rate"] = (
        summary["runs"] /
        summary["balls"].replace(0, np.nan)
    ) * 100

    summary["boundary_pct"] = (
        (summary["fours"] + summary["sixes"]) /
        summary["balls"].replace(0, np.nan)
    ) * 100

    return (
        summary.sort_values("runs", ascending=False)
        .head(top_n)
        .reset_index()
    )


# ============================================================
# PHASE DATA
# ============================================================

@st.cache_data(show_spinner=False)
def get_phase_data(
    phase_name: str,
    min_balls: int = 200
) -> pd.DataFrame:
    """Returns filtered phase-aware batting ratings."""
    ratings_df = load_phase_ratings()

    filtered = ratings_df[
        (ratings_df["phase"] == phase_name) &
        (ratings_df["balls_faced"] >= min_balls)
    ].copy()

    return filtered


# ============================================================
# BATTER CAREER SUMMARY
# ============================================================

@st.cache_data(show_spinner=False)
def get_batter_career_summary(batter_name: str) -> dict:
    """Returns comprehensive career stats for one batter."""
    df = load_all_matches()

    b_df = df[df["batter"] == batter_name].copy()

    if b_df.empty:
        return {}

    b_df["is_legal"] = (
        b_df["wides"].fillna(0) == 0
    ).astype(int)

    runs = int(b_df["batter_runs"].sum())
    balls = int(b_df["is_legal"].sum())

    fours = int((b_df["batter_runs"] == 4).sum())
    sixes = int((b_df["batter_runs"] == 6).sum())

    matches = int(b_df["match_id"].nunique())

    valid_d = [
        "caught", "bowled", "run out", "lbw",
        "caught and bowled", "stumped", "hit wicket",
        "retired out", "obstructing the field"
    ]

    dismissals = int(
        len(
            df[
                (df["dismissal_method"].isin(valid_d)) &
                (
                    df["dismissed_players"].fillna(df["batter"])
                    == batter_name
                )
            ]
        )
    )

    match_scores = b_df.groupby("match_id")["batter_runs"].sum()

    fifties = int(
        ((match_scores >= 50) & (match_scores < 100)).sum()
    )

    hundreds = int((match_scores >= 100).sum())

    team_mapping = get_batter_team_mapping()
    primary_team = team_mapping.get(
        batter_name, "IPL Franchise"
    )

    sr = (runs / balls * 100) if balls > 0 else 0.0
    avg = (runs / dismissals) if dismissals > 0 else float(runs)

    boundary_pct = (
        ((fours + sixes) / balls * 100)
        if balls > 0 else 0.0
    )

    ratings_df = load_phase_ratings()
    p_df = ratings_df[ratings_df["batter"] == batter_name]

    phase_ratings = {}

    for p in ["Powerplay", "Middle", "Death"]:
        match_row = p_df[p_df["phase"] == p]

        if not match_row.empty:
            phase_ratings[p] = {
                "rating": float(
                    match_row["reliability_adjusted_rating"].iloc[0]
                ),
                "raw_rating": float(
                    match_row["phase_aware_batting_rating"].iloc[0]
                ),
                "sr": float(match_row["strike_rate"].iloc[0]),
                "avg": float(match_row["batting_average"].iloc[0]),
                "runs": int(match_row["total_runs"].iloc[0]),
                "balls": int(match_row["balls_faced"].iloc[0]),
                "boundary_pct": float(
                    match_row["boundary_percentage"].iloc[0]
                ),
            }
        else:
            phase_ratings[p] = None

    return {
        "batter": batter_name,
        "team": primary_team,
        "matches": matches,
        "runs": runs,
        "balls": balls,
        "dismissals": dismissals,
        "strike_rate": sr,
        "batting_average": avg,
        "fours": fours,
        "sixes": sixes,
        "fifties": fifties,
        "hundreds": hundreds,
        "boundary_pct": boundary_pct,
        "phase_ratings": phase_ratings,
    }


# ============================================================
# SEASON-BY-SEASON BATTER PERFORMANCE
# ============================================================

@st.cache_data(show_spinner=False)
def get_batter_season_trajectory(
    batter_name: str
) -> pd.DataFrame:
    """Calculates season-by-season trajectory for a batter."""
    df = load_all_matches()

    b_df = df[df["batter"] == batter_name].copy()

    if b_df.empty:
        return pd.DataFrame()

    b_df["is_legal"] = (
        b_df["wides"].fillna(0) == 0
    ).astype(int)

    valid_d = [
        "caught", "bowled", "run out", "lbw",
        "caught and bowled", "stumped", "hit wicket",
        "retired out", "obstructing the field"
    ]

    d_df = df[
        (df["dismissal_method"].isin(valid_d)) &
        (
            df["dismissed_players"].fillna(df["batter"])
            == batter_name
        )
    ]

    d_per_season = d_df.groupby("season").size()

    match_scores = (
        b_df.groupby(["season", "match_id"])["batter_runs"]
        .sum()
        .reset_index()
    )

    fifties = (
        match_scores[
            (match_scores["batter_runs"] >= 50) &
            (match_scores["batter_runs"] < 100)
        ]
        .groupby("season")
        .size()
    )

    hundreds = (
        match_scores[match_scores["batter_runs"] >= 100]
        .groupby("season")
        .size()
    )

    res = b_df.groupby("season").agg(
        runs=("batter_runs", "sum"),
        balls=("is_legal", "sum"),
        fours=("batter_runs", lambda x: int((x == 4).sum())),
        sixes=("batter_runs", lambda x: int((x == 6).sum())),
        matches=("match_id", "nunique"),
        team=(
            "batting_team",
            lambda x: x.mode().iloc[0] if not x.empty else "IPL"
        )
    ).reset_index()

    res["dismissals"] = (
        res["season"].map(d_per_season).fillna(0).astype(int)
    )

    res["fifties"] = (
        res["season"].map(fifties).fillna(0).astype(int)
    )

    res["hundreds"] = (
        res["season"].map(hundreds).fillna(0).astype(int)
    )

    res["strike_rate"] = (
        res["runs"] /
        res["balls"].replace(0, np.nan)
    ) * 100

    res["batting_average"] = (
        res["runs"] /
        res["dismissals"].replace(0, np.nan)
    )

    return res


# ============================================================
# NEW: BATTER'S FRANCHISE IN A PARTICULAR IPL SEASON
# ============================================================

@st.cache_data(show_spinner=False)
def get_batter_team_for_season(
    batter_name: str,
    season: int
) -> str:
    """
    Returns the franchise represented by a batter
    in the selected IPL season.

    Example:
        get_batter_team_for_season("V Kohli", 2024)
    """
    df = load_all_matches()

    season_df = df[
        (df["batter"] == batter_name) &
        (df["season"] == str(season))
    ]

    if season_df.empty:
        return "IPL"

    teams = season_df["batting_team"].mode()

    if teams.empty:
        return "IPL"

    return str(teams.iloc[0])


# ============================================================
# BATTER PHASE PERFORMANCE BY SEASON
# ============================================================

@st.cache_data(show_spinner=False)
def get_batter_phase_by_season(
    batter_name: str
) -> pd.DataFrame:
    """Returns runs scored per season across three phases."""
    df = load_all_matches()

    b_df = df[df["batter"] == batter_name].copy()

    if b_df.empty:
        return pd.DataFrame()

    b_df["over"] = np.floor(
        b_df["delivery_number"]
    ).astype(int)

    def assign_p(o):
        if 0 <= o <= 5:
            return "Powerplay"
        elif 6 <= o <= 14:
            return "Middle"
        elif 15 <= o <= 19:
            return "Death"

        return "Other"

    b_df["phase"] = b_df["over"].apply(assign_p)

    pivot = (
        b_df.groupby(["season", "phase"])["batter_runs"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    for expected in ["Powerplay", "Middle", "Death"]:
        if expected not in pivot.columns:
            pivot[expected] = 0

    return pivot[
        ["season", "Powerplay", "Middle", "Death"]
    ]


# ============================================================
# PLAYER SCOUTING ARCHETYPES
# ============================================================

@st.cache_data(show_spinner=False)
def get_scouting_archetypes() -> dict:
    """
    Defines rule-based player archetypes using
    transparent statistical criteria.
    """
    ratings_df = load_phase_ratings()
    team_map = get_batter_team_mapping()

    # 1. Powerplay Enforcers
    pp_df = ratings_df[
        ratings_df["phase"] == "Powerplay"
    ].copy()

    pp_enforcers = pp_df[
        (pp_df["strike_rate"] >= 140.0) &
        (pp_df["boundary_percentage"] >= 20.0) &
        (pp_df["balls_faced"] >= 200)
    ].sort_values(
        "reliability_adjusted_rating",
        ascending=False
    ).reset_index(drop=True)

    pp_enforcers["team"] = (
        pp_enforcers["batter"].map(team_map).fillna("IPL")
    )

    # 2. Middle Overs Anchors / Spin Controllers
    mid_df = ratings_df[
        ratings_df["phase"] == "Middle"
    ].copy()

    mid_anchors = mid_df[
        (mid_df["batting_average"] >= 35.0) &
        (mid_df["strike_rate"] >= 125.0) &
        (mid_df["balls_faced"] >= 200)
    ].sort_values(
        "reliability_adjusted_rating",
        ascending=False
    ).reset_index(drop=True)

    mid_anchors["team"] = (
        mid_anchors["batter"].map(team_map).fillna("IPL")
    )

    # 3. Elite Death Finishers
    death_df = ratings_df[
        ratings_df["phase"] == "Death"
    ].copy()

    death_finishers = death_df[
        (death_df["strike_rate"] >= 175.0) &
        (death_df["reliability_adjusted_rating"] >= 58.0) &
        (death_df["balls_faced"] >= 150)
    ].sort_values(
        "reliability_adjusted_rating",
        ascending=False
    ).reset_index(drop=True)

    death_finishers["team"] = (
        death_finishers["batter"].map(team_map).fillna("IPL")
    )

    # 4. High-Efficiency All-Phase Assets
    high_eff = ratings_df[
        (ratings_df["reliability_adjusted_rating"] >= 60.0) &
        (ratings_df["boundary_advantage"] >= 15.0)
    ].sort_values(
        "reliability_adjusted_rating",
        ascending=False
    ).drop_duplicates(
        subset=["batter"]
    ).reset_index(drop=True)

    high_eff["team"] = (
        high_eff["batter"].map(team_map).fillna("IPL")
    )

    return {
        "Powerplay Enforcers": {
            "df": pp_enforcers,
            "phase": "Powerplay",
            "phase_color": "#FFB800",
            "criteria": (
                "Powerplay SR ≥ 140.0, Boundary % ≥ 20.0%, "
                "Min 200 balls faced in Powerplay."
            ),
            "description": (
                "Specialists designed to exploit field restrictions "
                "in overs 1–6, clearing infielders and putting early "
                "pressure on opening bowlers."
            )
        },

        "Middle Overs Spin Tacklers": {
            "df": mid_anchors,
            "phase": "Middle",
            "phase_color": "#8A4FFF",
            "criteria": (
                "Middle Overs Avg ≥ 35.0, Middle Overs SR ≥ 125.0, "
                "Min 200 balls faced in Middle overs."
            ),
            "description": (
                "Master innings controllers who combine wicket "
                "preservation against spin with fluent strike rotation "
                "during overs 7–15."
            )
        },

        "Elite Death Overs Finishers": {
            "df": death_finishers,
            "phase": "Death",
            "phase_color": "#E63946",
            "criteria": (
                "Death Overs SR ≥ 175.0, Reliability-Adjusted "
                "Rating ≥ 58.0, Min 150 balls faced in Death overs."
            ),
            "description": (
                "High-leverage finishers capable of clearing "
                "boundaries against yorkers and slower balls "
                "in overs 16–20."
            )
        },

        "High-Efficiency Assets": {
            "df": high_eff,
            "phase": "All Phases",
            "phase_color": "#FF9F1C",
            "criteria": (
                "Reliability Rating ≥ 60.0, Boundary Advantage "
                "≥ +15% over league baseline."
            ),
            "description": (
                "Tactically efficient batters delivering "
                "disproportionate boundary value relative to balls "
                "consumed across their primary phase."
            )
        }
    }
