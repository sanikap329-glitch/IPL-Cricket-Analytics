"""
Configuration and constants for IPL Batter Intelligence & Strategy Platform.
Features IPL franchise-inspired color palettes, phase color standards, and analytical parameters.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "Data"
OUTPUTS_DIR = PROJECT_ROOT / "Outputs"
DATA_OUTPUTS_DIR = DATA_DIR / "outputs"

# CSV Data Paths
PATH_ALL_MATCHES = DATA_OUTPUTS_DIR / "ipl_all_matches_with_metadata.csv"
PATH_PHASE_RATINGS = OUTPUTS_DIR / "phase_aware_batting_ratings.csv"
PATH_TEMPORAL_VALIDATION = OUTPUTS_DIR / "phase_aware_temporal_validation.csv"
PATH_COMBINED_VALIDATION = OUTPUTS_DIR / "combined_validation_summary.csv"
PATH_CORRELATIONS = OUTPUTS_DIR / "temporal_validation_correlations.csv"
PATH_TEAM_PERFORMANCE_SQL = DATA_OUTPUTS_DIR / "final summary of team performance (2024 & 2025)corrected.csv"
PATH_TEAM_PERFORMANCE_HIST = DATA_OUTPUTS_DIR / "team_performance.csv"
CHARTS_DIR = OUTPUTS_DIR / "Charts"

# Branding
APP_TITLE = "IPL INSIGHT"
APP_SUBTITLE = "Batter Intelligence & Strategy Platform"
APP_DESCRIPTION = "Professional T20 Batter Intelligence, Phase-Aware Impact Modeling & Strategy Analytics"

# IPL Franchise Color Palette
TEAM_COLORS = {
    "Mumbai Indians": {
        "primary": "#004BA0",
        "secondary": "#D1AB3E",
        "text": "#ffffff",
        "short": "MI"
    },
    "Rajasthan Royals": {
        "primary": "#EA1A85",
        "secondary": "#254AA5",
        "text": "#ffffff",
        "short": "RR"
    },
    "Royal Challengers Bengaluru": {
        "primary": "#D71920",
        "secondary": "#C99222",
        "text": "#ffffff",
        "short": "RCB"
    },
    "Royal Challengers Bangalore": {
        "primary": "#D71920",
        "secondary": "#C99222",
        "text": "#ffffff",
        "short": "RCB"
    },
    "Chennai Super Kings": {
        "primary": "#FFCB05",
        "secondary": "#0081E8",
        "text": "#111827",
        "short": "CSK"
    },
    "Sunrisers Hyderabad": {
        "primary": "#F26522",
        "secondary": "#000000",
        "text": "#ffffff",
        "short": "SRH"
    },
    "Kolkata Knight Riders": {
        "primary": "#3A225D",
        "secondary": "#D4AF37",
        "text": "#ffffff",
        "short": "KKR"
    },
    "Delhi Capitals": {
        "primary": "#17479E",
        "secondary": "#A7D5F2",
        "text": "#ffffff",
        "short": "DC"
    },
    "Delhi Daredevils": {
        "primary": "#17479E",
        "secondary": "#A7D5F2",
        "text": "#ffffff",
        "short": "DD"
    },
    "Punjab Kings": {
        "primary": "#B72025",
        "secondary": "#DCDDDF",
        "text": "#ffffff",
        "short": "PBKS"
    },
    "Kings XI Punjab": {
        "primary": "#B72025",
        "secondary": "#DCDDDF",
        "text": "#ffffff",
        "short": "KXIP"
    },
    "Gujarat Titans": {
        "primary": "#1B2133",
        "secondary": "#D4AF37",
        "text": "#ffffff",
        "short": "GT"
    },
    "Lucknow Super Giants": {
        "primary": "#3873B8",
        "secondary": "#A0E6FF",
        "text": "#ffffff",
        "short": "LSG"
    },
    "Rising Pune Supergiant": {
        "primary": "#D11D5B",
        "secondary": "#800080",
        "text": "#ffffff",
        "short": "RPS"
    },
    "Rising Pune Supergiants": {
        "primary": "#D11D5B",
        "secondary": "#800080",
        "text": "#ffffff",
        "short": "RPS"
    },
    "Gujarat Lions": {
        "primary": "#E04F16",
        "secondary": "#2B3C56",
        "text": "#ffffff",
        "short": "GL"
    },
    "Pune Warriors": {
        "primary": "#2F9BE3",
        "secondary": "#111111",
        "text": "#ffffff",
        "short": "PWI"
    },
    "Deccan Chargers": {
        "primary": "#415C77",
        "secondary": "#D4AF37",
        "text": "#ffffff",
        "short": "DCG"
    },
    "Kochi Tuskers Kerala": {
        "primary": "#6B3FA0",
        "secondary": "#F36F21",
        "text": "#ffffff",
        "short": "KTK"
    },
}

# Distinct Phase Colors (Rule 4: Powerplay=Gold, Middle=Purple, Death=Red)
PHASE_COLORS = {
    "Powerplay": "#FFB800",   # Gold
    "Middle": "#8A4FFF",      # Purple
    "Death": "#E63946",       # Red
}

# Charcoal / Black Stadium Palette (Rule 1 & 8: Charcoal/Black, no plain blue)
COLORS = {
    "bg_dark": "#0a0c12",
    "bg_secondary": "#11151f",
    "bg_card": "rgba(18, 23, 34, 0.82)",
    "bg_card_solid": "#121722",
    "bg_card_hover": "#1a2130",
    "border_gold": "rgba(255, 184, 0, 0.28)",
    "border_subtle": "rgba(255, 255, 255, 0.08)",
    "gold": "#FFB800",
    "amber": "#FF9F1C",
    "powerplay": "#FFB800",   # Gold
    "middle": "#8A4FFF",      # Purple
    "death": "#E63946",       # Red
    "text_primary": "#ffffff",
    "text_secondary": "#cbd5e1",
    "text_muted": "#7888a3",
    "grid_line": "rgba(255, 255, 255, 0.06)",
}

# Phase Definitions with distinct IPL Phase Colors
PHASES = {
    "Powerplay": {
        "overs": (0, 5),
        "label": "Powerplay (Overs 1–6)",
        "color": PHASE_COLORS["Powerplay"],
        "badge_border": "rgba(255, 184, 0, 0.5)",
        "description": "Field restrictions active (max 2 fielders outside 30-yard circle). Exploiting the new ball & power hitting.",
        "league_sr": 122.75,
        "league_avg": 30.77,
        "league_boundary_pct": 19.57,
    },
    "Middle": {
        "overs": (6, 14),
        "label": "Middle Overs (Overs 7–15)",
        "color": PHASE_COLORS["Middle"],
        "badge_border": "rgba(138, 79, 255, 0.5)",
        "description": "5 fielders back. Dominated by spin bowlers, strike rotation, risk management and platform building.",
        "league_sr": 123.74,
        "league_avg": 28.84,
        "league_boundary_pct": 13.65,
    },
    "Death": {
        "overs": (15, 19),
        "label": "Death Overs (Overs 16–20)",
        "color": PHASE_COLORS["Death"],
        "badge_border": "rgba(230, 57, 70, 0.5)",
        "description": "High-leverage acceleration. Pure maximum boundary intent against specialist yorker and changeup bowling.",
        "league_sr": 155.92,
        "league_avg": 18.59,
        "league_boundary_pct": 20.17,
    },
}

# Rating Methodology Parameters
MIN_BALLS_FACED_DEFAULT = 200
RATING_WEIGHTS = {
    "strike_rate": 0.40,
    "batting_average": 0.40,
    "boundary_pct": 0.20,
}
RATING_CENTER = 50.0
RATING_SCALE = 10.0
PRIOR_DISMISSALS = 10  # Empirical Bayes reliability adjustment
