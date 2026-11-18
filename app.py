
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Pressure Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. RAJASTHAN ROYALS INSPIRED THEME
# ============================================================

PINK = "#E83E8C"
NAVY = "#172B4D"
GOLD = "#E6B84A"
LIGHT_BG = "#F6F7FB"
WHITE = "#FFFFFF"
GREY = "#718096"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {LIGHT_BG};
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NAVY}, #263E65);
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    .main-title {{
        font-size: 34px;
        font-weight: 850;
        color: {NAVY};
        margin-bottom: 0;
    }}

    .sub-title {{
        color: {GREY};
        font-size: 15px;
        margin-top: 4px;
        margin-bottom: 22px;
    }}

    .section-title {{
        color: {NAVY};
        font-size: 23px;
        font-weight: 750;
        margin-top: 15px;
        margin-bottom: 12px;
    }}

    .metric-card {{
        background: {WHITE};
        padding: 18px;
        border-radius: 13px;
        border-left: 5px solid {PINK};
        box-shadow: 0 2px 9px rgba(0,0,0,0.06);
        min-height: 90px;
    }}

    .metric-label {{
        color: {GREY};
        font-size: 13px;
        font-weight: 600;
    }}

    .metric-value {{
        color: {NAVY};
        font-size: 27px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }}

    .info-card {{
        background: {WHITE};
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #E5E7EB;
        margin-bottom: 10px;
    }}

    div.stButton > button {{
        background-color: {PINK};
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 700;
    }}

    div.stButton > button:hover {{
        background-color: {NAVY};
        color: white;
    }}

    h1, h2, h3 {{
        color: {NAVY};
    }}
    </style>
    """,
    unsafe_allow_html=True
)




# ============================================================
# 3. DATA PATHS AND GOOGLE DRIVE CONFIGURATION
# ============================================================

from pathlib import Path
import gdown

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)

GOOGLE_DRIVE_FILES = {
    "delivery_leverage_pressure.csv": "1vHEIld5-k96yOKYzE42tvnSGOGDXlMkh",
    "match_pressure_index.csv": "1U2N9XAcfk_T66sBz6YOYmehw2p-3USdb",
    "final_player_pressure_ranking.csv": "1qhRmBZGfp-UCFaFNQ40p2zBV0vg4d1Vb",
    "player_value_under_pressure.csv": "1ClPYp98mPO5ucfsjNSmG7AvVi9AidZ6Z",
    "all_bowler_pressure_rankings.csv": "1qyfN_-deJXF-Irt9OuCCCUna192KKZbR",
    "win_probability_model_metrics.csv": "1mX7DMsHOOBvGyyjNUKGCGWqQN0Mmi9Jg"
}



# ============================================================
# 4. DOWNLOAD AND LOAD DATASETS
# ============================================================

def download_from_google_drive(filename):

    file_path = DATA_DIR / filename
    file_id = GOOGLE_DRIVE_FILES.get(filename)

    # Check whether Google Drive ID is configured
    if not file_id:
        raise FileNotFoundError(
            f"Google Drive ID is not configured for {filename}"
        )

    try:
        # Remove old downloaded file to force fresh download
        if file_path.exists():
            file_path.unlink()

        # Google Drive download URL
        url = f"https://drive.google.com/uc?id={file_id}"

        with st.spinner(f"Downloading {filename} from Google Drive..."):

            downloaded_file = gdown.download(
                url,
                str(file_path),
                quiet=False
            )

        # Verify download
        if (
            downloaded_file is None
            or not file_path.exists()
            or file_path.stat().st_size == 0
        ):
            raise RuntimeError(
                f"Google Drive download failed for {filename}"
            )

        # ====================================================
        # VALIDATE BOWLER RANKING FILE
        # ====================================================

        if filename == "all_bowler_pressure_rankings.csv":

            required_columns = {
                "reliability_adjusted_score",
                "final_rank",
                "sample_reliability"
            }

            downloaded_columns = set(
                pd.read_csv(file_path, nrows=0).columns
            )

            missing_columns = (
                required_columns - downloaded_columns
            )

            if missing_columns:
                file_path.unlink()

                raise ValueError(
                    "Incorrect bowler ranking file. "
                    f"Missing required columns: {missing_columns}"
                )

        return file_path

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        raise RuntimeError(
            f"Unable to download {filename}: {error}"
        )


# ============================================================
# LOAD CSV WITH STREAMLIT CACHING
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv(file_path, modified_time):

    path = Path(file_path)

    try:
        df = pd.read_csv(
            path,
            low_memory=False
        )

        return df

    except Exception as error:

        return {
            "_load_error": str(error)
        }


# ============================================================
# LOAD DATASET FUNCTION
# ============================================================

def load_data(filename):

    try:

        path = download_from_google_drive(filename)

        return load_csv(
            str(path),
            path.stat().st_mtime
        )

    except Exception as error:

        return {
            "_load_error": str(error)
        }


# ============================================================
# LOAD ALL REQUIRED DATASETS
# ============================================================

delivery_pressure = load_data(
    "delivery_leverage_pressure.csv"
)

match_pressure = load_data(
    "match_pressure_index.csv"
)

player_ranking = load_data(
    "final_player_pressure_ranking.csv"
)

player_value = load_data(
    "player_value_under_pressure.csv"
)

bowler_ranking = load_data(
    "all_bowler_pressure_rankings.csv"
)

model_metrics = load_data(
    "win_probability_model_metrics.csv"
)


# ============================================================
# DATASET COLLECTION
# ============================================================

datasets = {

    "delivery_pressure": delivery_pressure,

    "match_pressure": match_pressure,

    "player_ranking": player_ranking,

    "player_value": player_value,

    "bowler_ranking": bowler_ranking,

    "model_metrics": model_metrics

}


# ============================================================
# BOWLER RANKING VALIDATION
# ============================================================

if isinstance(bowler_ranking, pd.DataFrame):

    required_bowler_columns = [
        "reliability_adjusted_score",
        "final_rank",
        "sample_reliability"
    ]

    missing_columns = [
        col for col in required_bowler_columns
        if col not in bowler_ranking.columns
    ]

    if missing_columns:

        st.error(
            "Bowler ranking file is missing required columns: "
            + ", ".join(missing_columns)
        )

    else:

        st.success(
            f"Bowler ranking loaded successfully: "
            f"{len(bowler_ranking)} bowlers."
        )

elif isinstance(bowler_ranking, dict):

    st.error(
        "Bowler ranking could not be loaded: "
        + bowler_ranking.get("_load_error", "Unknown error")
    )


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def is_valid_dataframe(data):

    return isinstance(data, pd.DataFrame)


def find_column(df, candidates):

    if not is_valid_dataframe(df):
        return None

    mapping = {
        str(col).lower(): col
        for col in df.columns
    }

    for candidate in candidates:

        if candidate.lower() in mapping:
            return mapping[candidate.lower()]

    return None


def numeric_column(df, candidates):

    col = find_column(df, candidates)

    if col is None:
        return None

    return pd.to_numeric(
        df[col],
        errors="coerce"
    )


def metric_card(label, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_heading(text):

    st.markdown(
        f'<div class="section-title">{text}</div>',
        unsafe_allow_html=True
    )


def show_missing_message(dataset_name):

    st.warning(
        f"{dataset_name} is not available. "
        f"Check the file inside: {DATA_DIR}"
    )


def safe_download(df, filename):

    if is_valid_dataframe(df):

        st.download_button(
            label=f"Download {filename}",
            data=df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name=filename,
            mime="text/csv"
        )


def clean_player_names(df):

    if not is_valid_dataframe(df):
        return df

    name_col = find_column(
        df,
        [
            "striker_name",
            "player_name",
            "batter_name",
            "bowler_name",
            "name"
        ]
    )

    if name_col:

        df = df.copy()

        df[name_col] = (
            df[name_col]
            .fillna("Unknown")
            .astype(str)
        )

    return df


def get_player_name_column(df):

    return find_column(
        df,
        [
            "striker_name",
            "player_name",
            "batter_name",
            "bowler_name",
            "name"
        ]
    )


def format_number(value, decimals=2):

    try:

        value = float(value)

        if not np.isfinite(value):
            return "N/A"

        return f"{value:,.{decimals}f}"

    except (ValueError, TypeError):
        return "N/A"


def pressure_color_map():

    return {
        "Low": "#55B87A",
        "Below Average": "#9CCB8B",
        "Average": GOLD,
        "High": "#F28C45",
        "Very High": PINK,
        "Not Available": "#A0AEC0"
    }


def show_load_error(data, dataset_name):

    if isinstance(data, dict) and "_load_error" in data:

        st.error(
            f"Error loading {dataset_name}: "
            f"{data['_load_error']}"
        )

        return True

    return False


def get_valid_player_ranking(df, score_column, rank_column=None):

    df = df.copy()

    df[score_column] = pd.to_numeric(
        df[score_column],
        errors="coerce"
    )

    df = df.dropna(
        subset=[score_column]
    )

    df = df.sort_values(
        score_column,
        ascending=False
    ).reset_index(drop=True)

    if rank_column and rank_column in df.columns:

        df[rank_column] = pd.to_numeric(
            df[rank_column],
            errors="coerce"
        )

    return df


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:12px 4px 20px 4px;">
        <div style="font-size:42px;">🏏</div>
        <div style="font-size:21px;font-weight:850;">
            PRESSURE ANALYTICS
        </div>
        <div style="font-size:12px;opacity:0.8;">
            CRICKET PERFORMANCE INTELLIGENCE
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


pages = [
    "Overview",
    "Pressure Explorer",
    "Player Pressure Index",
    "Batter Profiles",
    "Bowler Profiles",
    "MPI Analysis",
    "Model & Validation"
]

page = st.sidebar.radio(
    "NAVIGATION",
    pages
)


st.sidebar.markdown("---")

st.sidebar.markdown("### DATA STATUS")

for name, data in datasets.items():

    if is_valid_dataframe(data):

        st.sidebar.success(
            f"{name}: Loaded ({len(data):,})"
        )

    elif isinstance(data, dict) and "_load_error" in data:

        st.sidebar.error(
            f"{name}: Read error"
        )

    else:

        st.sidebar.warning(
            f"{name}: Missing"
        )


st.sidebar.markdown("---")

st.sidebar.caption(
    f"Data directory: {DATA_DIR}"
)

st.sidebar.caption(
    "Pressure Performance Analytics | T20 Cricket"
)


# ============================================================
# 7. MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    'PRESSURE PERFORMANCE ANALYTICS'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Measuring player performance, match pressure and '
    'decision-making under high-pressure situations.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PAGE 1: OVERVIEW
# ============================================================

if page == "Overview":

    section_heading(
        "Tournament Analytics Overview"
    )

    total_deliveries = (
        len(pressure_data)
        if is_valid_dataframe(pressure_data)
        else 0
    )

    total_matches = 0
    total_batters = 0
    total_bowlers = 0
    high_pressure_deliveries = 0

    if is_valid_dataframe(pressure_data):

        match_col = find_column(
            pressure_data,
            ["match_id"]
        )

        if match_col:

            total_matches = (
                pressure_data[match_col].nunique()
            )

        category_col = find_column(
            pressure_data,
            ["pressure_category"]
        )

        if category_col:

            high_pressure_deliveries = (
                pressure_data[category_col]
                .astype(str)
                .str.lower()
                .isin(["high", "very high"])
                .sum()
            )

    if is_valid_dataframe(batter_ranking):

        name_col = get_player_name_column(
            batter_ranking
        )

        if name_col:

            total_batters = (
                batter_ranking[name_col].nunique()
            )

    if is_valid_dataframe(bowler_ranking):

        total_bowlers = (
            bowler_ranking["bowler_id"].nunique()
            if "bowler_id" in bowler_ranking.columns
            else len(bowler_ranking)
        )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        metric_card(
            "DELIVERIES",
            f"{total_deliveries:,}"
        )

    with col2:

        metric_card(
            "MATCHES",
            f"{total_matches:,}"
        )

    with col3:

        metric_card(
            "BATTERS RANKED",
            f"{total_batters:,}"
        )

    with col4:

        metric_card(
            "BOWLERS RANKED",
            f"{total_bowlers:,}"
        )

    with col5:

        metric_card(
            "HIGH PRESSURE BALLS",
            f"{high_pressure_deliveries:,}"
        )

    st.markdown("---")

    left, right = st.columns(2)

    # PRESSURE CATEGORY DISTRIBUTION

    with left:

        section_heading(
            "Pressure Category Distribution"
        )

        if is_valid_dataframe(pressure_data):

            category_col = find_column(
                pressure_data,
                ["pressure_category"]
            )

            if category_col:

                category_counts = (
                    pressure_data[category_col]
                    .fillna("Not Available")
                    .value_counts()
                    .rename_axis("Pressure Category")
                    .reset_index(name="Deliveries")
                )

                fig = px.pie(
                    category_counts,
                    names="Pressure Category",
                    values="Deliveries",
                    hole=0.52,
                    color="Pressure Category",
                    color_discrete_map=pressure_color_map()
                )

                fig.update_layout(
                    template="plotly_white",
                    height=380,
                    legend_title=""
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            show_missing_message(
                "Delivery Pressure"
            )

    # PRESSURE BY INNINGS

    with right:

        section_heading(
            "Pressure by Innings"
        )

        if is_valid_dataframe(pressure_data):

            innings_col = find_column(
                pressure_data,
                ["innings"]
            )

            pressure_col = find_column(
                pressure_data,
                ["delivery_pressure_score"]
            )

            if innings_col and pressure_col:

                temp = pressure_data.copy()

                temp[pressure_col] = pd.to_numeric(
                    temp[pressure_col],
                    errors="coerce"
                )

                innings_summary = (
                    temp.groupby(innings_col)[pressure_col]
                    .mean()
                    .reset_index()
                )

                fig = px.bar(
                    innings_summary,
                    x=innings_col,
                    y=pressure_col,
                    color=innings_col,
                    text_auto=".3f",
                    title="Average Delivery Pressure by Innings",
                    color_discrete_sequence=[
                        PINK,
                        NAVY
                    ]
                )

                fig.update_layout(
                    template="plotly_white",
                    height=380,
                    showlegend=False
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    st.markdown("---")

    section_heading(
        "Project Methodology"
    )

    methodology = [
        (
            "01",
            "Data Preprocessing",
            "Clean and prepare ball-by-ball match data."
        ),
        (
            "02",
            "Match State Calculation",
            "Calculate runs, wickets, overs and match situation."
        ),
        (
            "03",
            "Win Probability",
            "Estimate the batting team's probability of winning."
        ),
        (
            "04",
            "Delivery Outcomes",
            "Model expected runs and wicket probability."
        ),
        (
            "05",
            "Delivery Pressure",
            "Measure pressure using changes in win probability."
        ),
        (
            "06",
            "Match Pressure Index",
            "Aggregate delivery pressure into a match-level index."
        ),
        (
            "07",
            "Player Evaluation",
            "Compare batting and bowling performance under pressure."
        ),
        (
            "08",
            "Player Rankings",
            "Rank eligible players using composite performance scores."
        )
    ]

    for number, title, description in methodology:

        st.markdown(
            f"""
            <div class="info-card">
                <span style="color:{PINK};font-weight:850;">
                    {number}
                </span>
                &nbsp;&nbsp;
                <b style="color:{NAVY};">{title}</b>
                <br>
                <span style="color:{GREY};font-size:13px;">
                    {description}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Research scope: IPL-specific filtering, validation "
        "and performance evaluation have not yet been "
        "conducted separately."
    )


# ============================================================
# PAGE 2: PRESSURE EXPLORER
# ============================================================

elif page == "Pressure Explorer":

    section_heading(
        "Interactive Delivery Pressure Explorer"
    )

    if not is_valid_dataframe(pressure_data):

        show_missing_message(
            "Delivery Pressure"
        )

    else:

        df = pressure_data.copy()

        category_col = find_column(
            df,
            ["pressure_category"]
        )

        innings_col = find_column(
            df,
            ["innings"]
        )

        match_col = find_column(
            df,
            ["match_id"]
        )

        pressure_col = find_column(
            df,
            ["delivery_pressure_score"]
        )

        wp_col = find_column(
            df,
            ["win_probability_before"]
        )

        ball_col = find_column(
            df,
            ["innings_ball_num"]
        )

        st.markdown("### Filters")

        f1, f2, f3 = st.columns(3)

        with f1:

            if category_col:

                categories = sorted(
                    df[category_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_categories = st.multiselect(
                    "Pressure Category",
                    categories,
                    default=categories
                )

                df = df[
                    df[category_col]
                    .astype(str)
                    .isin(selected_categories)
                ]

        with f2:

            if innings_col:

                innings_values = sorted(
                    df[innings_col]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_innings = st.multiselect(
                    "Innings",
                    innings_values,
                    default=innings_values
                )

                df = df[
                    df[innings_col].isin(
                        selected_innings
                    )
                ]

        with f3:

            if match_col:

                matches = sorted(
                    df[match_col]
                    .dropna()
                    .unique()
                    .tolist(),
                    key=str
                )

                selected_match = st.selectbox(
                    "Select Match",
                    ["All Matches"] + matches,
                    format_func=lambda x: str(x)
                )

                if selected_match != "All Matches":

                    df = df[
                        df[match_col] == selected_match
                    ]

        st.markdown("---")

        st.metric(
            "Filtered Deliveries",
            f"{len(df):,}"
        )

        if pressure_col:

            df[pressure_col] = pd.to_numeric(
                df[pressure_col],
                errors="coerce"
            )

            chart_df = df.dropna(
                subset=[pressure_col]
            )

            if not chart_df.empty:

                fig = px.histogram(
                    chart_df,
                    x=pressure_col,
                    nbins=40,
                    title="Distribution of Delivery Pressure",
                    color_discrete_sequence=[PINK]
                )

                fig.update_layout(
                    template="plotly_white",
                    height=400
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        if innings_col and pressure_col:

            section_heading(
                "Pressure Comparison Across Innings"
            )

            chart_df = df.dropna(
                subset=[pressure_col]
            )

            if not chart_df.empty:

                fig = px.box(
                    chart_df,
                    x=innings_col,
                    y=pressure_col,
                    color=innings_col,
                    title="Delivery Pressure Distribution by Innings",
                    color_discrete_sequence=[
                        PINK,
                        NAVY
                    ]
                )

                fig.update_layout(
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        if wp_col and pressure_col:

            section_heading(
                "Win Probability vs Pressure"
            )

            scatter_df = df.copy()

            scatter_df[wp_col] = pd.to_numeric(
                scatter_df[wp_col],
                errors="coerce"
            )

            scatter_df[pressure_col] = pd.to_numeric(
                scatter_df[pressure_col],
                errors="coerce"
            )

            scatter_df = scatter_df.dropna(
                subset=[wp_col, pressure_col]
            )

            if not scatter_df.empty:

                hover_columns = [
                    col for col in [
                        match_col,
                        innings_col,
                        ball_col,
                        category_col
                    ]
                    if col is not None
                ]

                fig = px.scatter(
                    scatter_df,
                    x=wp_col,
                    y=pressure_col,
                    color=category_col if category_col else None,
                    hover_data=hover_columns,
                    title="Relationship Between Win Probability and Pressure",
                    color_discrete_map=pressure_color_map()
                )

                fig.update_layout(
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        section_heading(
            "Filtered Delivery Data"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=350
        )

        safe_download(
            df,
            "filtered_pressure_deliveries.csv"
        )


# ============================================================
# PAGE 3: PLAYER PRESSURE INDEX
# ============================================================

elif page == "Player Pressure Index":

    section_heading(
        "All Player Pressure Rankings"
    )

    st.caption(
        "Separate performance indices for batters and bowlers. "
        "Only eligible players are included in the main rankings."
    )

    role = st.radio(
        "Select Player Category",
        ["Batters", "Bowlers"],
        horizontal=True
    )

    # --------------------------------------------------------
    # SELECT DATASET AND SCORE COLUMN
    # --------------------------------------------------------

    if role == "Batters":

        source = (
            batter_ranking
            if is_valid_dataframe(batter_ranking)
            else batter_value
        )

        player_type = "Batter"

        score_candidates = [
            "reliability_adjusted_score",
            "adjusted_pressure_score",
            "adjusted_player_pressure_score",
            "final_pressure_score",
            "player_pressure_index",
            "player_value_under_pressure"
        ]

        high_balls_candidates = [
            "high_pressure_balls",
            "high_pressure_legal_balls"
        ]

        total_balls_candidates = [
            "total_balls",
            "overall_balls",
            "total_legal_balls"
        ]

        minimum_high_balls = 50
        minimum_total_balls = 100

    else:

        source = all_bowler_data

        player_type = "Bowler"

        # This is the exact final score from Notebook 10.
        score_candidates = [
            "reliability_adjusted_score"
        ]

        high_balls_candidates = [
            "high_pressure_legal_balls"
        ]

        total_balls_candidates = [
            "overall_legal_balls"
        ]

        minimum_high_balls = 30
        minimum_total_balls = 120

    if not is_valid_dataframe(source):

        show_missing_message(
            f"{player_type} ranking"
        )

    else:

        df = clean_player_names(
            source.copy()
        )

        name_col = get_player_name_column(df)

        if not name_col:

            st.error(
                f"Could not identify the {player_type.lower()} name column."
            )

        else:

            score_col = find_column(
                df,
                score_candidates
            )

            if score_col is None:

                st.error(
                    "The final pressure score column was not found. "
                    "Check the ranking CSV and its column names."
                )

                st.write(
                    "Available columns:",
                    df.columns.tolist()
                )

            else:

                df[name_col] = (
                    df[name_col]
                    .fillna("Unknown")
                    .astype(str)
                )

                high_balls_col = find_column(
                    df,
                    high_balls_candidates
                )

                total_balls_col = find_column(
                    df,
                    total_balls_candidates
                )

                # ------------------------------------------------
                # ELIGIBILITY
                # ------------------------------------------------

                eligible_col = find_column(
                    df,
                    ["eligible", "is_eligible"]
                )

                if eligible_col:

                    eligible_values = (
                        df[eligible_col]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1", "yes"])
                    )

                    df = df[
                        eligible_values
                    ].copy()

                else:

                    if high_balls_col:

                        df[high_balls_col] = pd.to_numeric(
                            df[high_balls_col],
                            errors="coerce"
                        )

                        df = df[
                            df[high_balls_col] >= minimum_high_balls
                        ].copy()

                    if total_balls_col:

                        df[total_balls_col] = pd.to_numeric(
                            df[total_balls_col],
                            errors="coerce"
                        )

                        df = df[
                            df[total_balls_col] >= minimum_total_balls
                        ].copy()

                # ------------------------------------------------
                # USE EXISTING PRESSURE INDEX
                # ------------------------------------------------

                df["pressure_index"] = pd.to_numeric(
                    df[score_col],
                    errors="coerce"
                )

                df = df.dropna(
                    subset=["pressure_index"]
                ).copy()

                # Do not apply another reliability adjustment.
                # The bowler score is already adjusted in Notebook 10.

                df["pressure_index"] = (
                    df["pressure_index"].clip(0, 100)
                )

                df = df.sort_values(
                    "pressure_index",
                    ascending=False
                ).reset_index(drop=True)

                # Preserve original notebook ranks when available.
                original_rank_col = find_column(
                    df,
                    ["final_rank", "rank"]
                )

                if original_rank_col:

                    df["pressure_rank"] = pd.to_numeric(
                        df[original_rank_col],
                        errors="coerce"
                    )

                    if df["pressure_rank"].isna().any():

                        df["pressure_rank"] = np.arange(
                            1,
                            len(df) + 1
                        )

                else:

                    df["pressure_rank"] = np.arange(
                        1,
                        len(df) + 1
                    )

                st.caption(
                    f"Index source: {score_col}"
                )

                # ------------------------------------------------
                # SUMMARY METRICS
                # ------------------------------------------------

                c1, c2, c3 = st.columns(3)

                with c1:

                    metric_card(
                        "ELIGIBLE PLAYERS",
                        f"{len(df):,}"
                    )

                with c2:

                    metric_card(
                        "AVERAGE INDEX",
                        format_number(
                            df["pressure_index"].mean()
                        )
                    )

                with c3:

                    metric_card(
                        "HIGHEST INDEX",
                        format_number(
                            df["pressure_index"].max()
                        )
                    )

                st.markdown("---")

                # ------------------------------------------------
                # SEARCH AND FILTER
                # ------------------------------------------------

                section_heading(
                    "Search and Filter Players"
                )

                search_text = st.text_input(
                    f"Search {player_type} by name",
                    placeholder="Enter player name..."
                )

                minimum_index = st.slider(
                    "Minimum Pressure Index",
                    min_value=0,
                    max_value=100,
                    value=0
                )

                filtered = df[
                    df["pressure_index"] >= minimum_index
                ].copy()

                if search_text:

                    filtered = filtered[
                        filtered[name_col].str.contains(
                            search_text,
                            case=False,
                            na=False
                        )
                    ]

                # ------------------------------------------------
                # COMPLETE PLAYER RANKING
                # ------------------------------------------------

                section_heading(
                    f"All Eligible {role} - Pressure Ranking"
                )

                display_columns = [
                    "pressure_rank",
                    name_col,
                    "pressure_index"
                ]

                for optional_col in [
                    high_balls_col,
                    total_balls_col
                ]:

                    if (
                        optional_col
                        and optional_col not in display_columns
                    ):

                        display_columns.append(
                            optional_col
                        )

                if role == "Bowlers":

                    for optional_col in [
                        "high_pressure_economy",
                        "high_pressure_dot_ball_percentage",
                        "high_pressure_wicket_rate",
                        "sample_reliability"
                    ]:

                        if (
                            optional_col in filtered.columns
                            and optional_col not in display_columns
                        ):

                            display_columns.append(
                                optional_col
                            )

                ranking_table = filtered[
                    display_columns
                ].rename(
                    columns={
                        "pressure_rank": "Rank",
                        name_col: "Player",
                        "pressure_index": "Pressure Index"
                    }
                )

                st.dataframe(
                    ranking_table,
                    use_container_width=True,
                    hide_index=True,
                    height=450
                )

                safe_download(
                    ranking_table,
                    f"all_{role.lower()}_pressure_index.csv"
                )

                # ------------------------------------------------
                # TOP 15 PLAYERS CHART
                # ------------------------------------------------

                section_heading(
                    "Top 15 Players"
                )

                top_players = (
                    filtered.head(15)
                    .sort_values(
                        "pressure_index",
                        ascending=True
                    )
                )

                if not top_players.empty:

                    fig = px.bar(
                        top_players,
                        x="pressure_index",
                        y=name_col,
                        orientation="h",
                        text="pressure_index",
                        color="pressure_index",
                        color_continuous_scale=[
                            NAVY,
                            PINK,
                            GOLD
                        ],
                        title=f"Top {role} by Pressure Index"
                    )

                    fig.update_traces(
                        texttemplate="%{text:.2f}",
                        textposition="outside"
                    )

                    fig.update_layout(
                        template="plotly_white",
                        height=550,
                        xaxis_title="Pressure Index (0–100)",
                        yaxis_title="Player",
                        coloraxis_showscale=False
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No players match the selected filters."
                    )

                # ------------------------------------------------
                # INDIVIDUAL PLAYER PROFILE
                # ------------------------------------------------

                st.markdown("---")

                section_heading(
                    "Individual Player Index"
                )

                if not filtered.empty:

                    selected_name = st.selectbox(
                        "Select a player",
                        filtered[name_col].tolist()
                    )

                    selected_player = filtered[
                        filtered[name_col] == selected_name
                    ].iloc[0]

                    p1, p2 = st.columns(2)

                    with p1:

                        metric_card(
                            "PLAYER",
                            selected_name
                        )

                    with p2:

                        metric_card(
                            "PRESSURE INDEX",
                            format_number(
                                selected_player["pressure_index"]
                            )
                        )

                    with st.expander(
                        "View complete player statistics"
                    ):

                        st.dataframe(
                            pd.DataFrame(
                                [selected_player]
                            ),
                            use_container_width=True
                        )

                # ------------------------------------------------
                # PLAYER COMPARISON
                # ------------------------------------------------

                st.markdown("---")

                section_heading(
                    "Compare Players"
                )

                if len(filtered) >= 2:

                    selected_players = st.multiselect(
                        "Choose players to compare",
                        filtered[name_col].tolist(),
                        max_selections=5
                    )

                    if selected_players:

                        comparison = filtered[
                            filtered[name_col].isin(
                                selected_players
                            )
                        ].sort_values(
                            "pressure_index",
                            ascending=False
                        )

                        fig = px.bar(
                            comparison,
                            x=name_col,
                            y="pressure_index",
                            color="pressure_index",
                            text="pressure_index",
                            color_continuous_scale=[
                                NAVY,
                                PINK
                            ],
                            title="Player Pressure Index Comparison"
                        )

                        fig.update_traces(
                            texttemplate="%{text:.2f}",
                            textposition="outside"
                        )

                        fig.update_layout(
                            template="plotly_white",
                            height=400,
                            xaxis_title="Player",
                            yaxis_title="Pressure Index (0–100)",
                            coloraxis_showscale=False
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                        st.dataframe(
                            comparison,
                            use_container_width=True
                        )

                else:

                    st.info(
                        "At least two eligible players are required."
                    )


# ============================================================
# PAGE 4: BATTER PROFILES
# ============================================================

elif page == "Batter Profiles":

    section_heading(
        "Batter Performance Under Pressure"
    )

    source = (
        batter_value
        if is_valid_dataframe(batter_value)
        else batter_ranking
    )

    if not is_valid_dataframe(source):

        show_missing_message(
            "Batter Value"
        )

    else:

        df = clean_player_names(
            source.copy()
        )

        name_col = get_player_name_column(df)

        if not name_col:

            st.error(
                "No player name column found in the batter dataset."
            )

        else:

            df[name_col] = (
                df[name_col]
                .fillna("Unknown")
                .astype(str)
            )

            player_names = sorted(
                df[name_col].unique().tolist()
            )

            selected_player = st.selectbox(
                "Select Batter",
                player_names
            )

            player = df[
                df[name_col] == selected_player
            ].iloc[0]

            st.markdown("---")

            # ------------------------------------------------
            # BATTER METRICS
            # ------------------------------------------------

            stat_columns = [
                ("Overall Runs", ["total_runs"]),
                ("Overall Balls", ["total_balls"]),
                ("Overall Strike Rate", ["overall_strike_rate"]),
                ("High Pressure Runs", ["high_pressure_runs"]),
                ("High Pressure Balls", ["high_pressure_balls"]),
                ("High Pressure Strike Rate", ["high_pressure_strike_rate"])
            ]

            cards = st.columns(3)

            for i, (label, candidates) in enumerate(
                stat_columns
            ):

                col = find_column(
                    df,
                    candidates
                )

                value = (
                    player[col]
                    if col
                    else np.nan
                )

                with cards[i % 3]:

                    metric_card(
                        label,
                        format_number(value)
                    )

            st.markdown("---")

            # ------------------------------------------------
            # HIGH VS LOW PRESSURE
            # ------------------------------------------------

            section_heading(
                "High Pressure vs Low Pressure"
            )

            comparison_metrics = {
                "Strike Rate": [
                    "high_pressure_strike_rate",
                    "low_pressure_strike_rate"
                ],
                "Boundary %": [
                    "high_pressure_boundary_percentage",
                    "low_pressure_boundary_percentage"
                ],
                "Dot Ball %": [
                    "high_pressure_dot_ball_percentage",
                    "low_pressure_dot_ball_percentage"
                ],
                "Dismissal Rate": [
                    "high_pressure_dismissal_rate",
                    "low_pressure_dismissal_rate"
                ]
            }

            comparison_rows = []

            for metric, columns in comparison_metrics.items():

                high_col = find_column(
                    df,
                    [columns[0]]
                )

                low_col = find_column(
                    df,
                    [columns[1]]
                )

                if high_col and low_col:

                    comparison_rows.append({
                        "Metric": metric,
                        "High Pressure": pd.to_numeric(
                            pd.Series([player[high_col]]),
                            errors="coerce"
                        ).iloc[0],
                        "Low Pressure": pd.to_numeric(
                            pd.Series([player[low_col]]),
                            errors="coerce"
                        ).iloc[0]
                    })

            if comparison_rows:

                comparison_df = pd.DataFrame(
                    comparison_rows
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        name="High Pressure",
                        x=comparison_df["Metric"],
                        y=comparison_df["High Pressure"],
                        marker_color=PINK
                    )
                )

                fig.add_trace(
                    go.Bar(
                        name="Low Pressure",
                        x=comparison_df["Metric"],
                        y=comparison_df["Low Pressure"],
                        marker_color=NAVY
                    )
                )

                fig.update_layout(
                    barmode="group",
                    title="Performance Comparison",
                    template="plotly_white",
                    height=420
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.dataframe(
                    comparison_df,
                    use_container_width=True
                )

            else:

                st.info(
                    "High-pressure and low-pressure comparison "
                    "columns were not found."
                )

            # ------------------------------------------------
            # PRESSURE SCORE
            # ------------------------------------------------

            score_col = find_column(
                df,
                [
                    "reliability_adjusted_score",
                    "adjusted_pressure_score",
                    "player_value_under_pressure"
                ]
            )

            if score_col:

                st.markdown("---")

                section_heading(
                    "Pressure Performance Score"
                )

                score = pd.to_numeric(
                    pd.Series([player[score_col]]),
                    errors="coerce"
                ).iloc[0]

                if pd.notna(score):

                    st.metric(
                        "Player Pressure Score",
                        format_number(score, 3)
                    )

            # ------------------------------------------------
            # COMPLETE PLAYER RECORD
            # ------------------------------------------------

            st.markdown("---")

            section_heading(
                "Complete Player Record"
            )

            st.dataframe(
                pd.DataFrame([player]),
                use_container_width=True
            )

            safe_download(
                pd.DataFrame([player]),
                "selected_batter_profile.csv"
            )


# ============================================================
# PAGE 5: BOWLER PROFILES
# ============================================================

elif page == "Bowler Profiles":

    section_heading(
        "Bowler Performance Under Pressure"
    )

    # Use the complete ranking file.
    source = all_bowler_data

    if not is_valid_dataframe(source):

        show_missing_message(
            "Complete Bowler Ranking"
        )

    else:

        df = clean_player_names(
            source.copy()
        )

        name_col = find_column(
            df,
            ["bowler_name"]
        )

        if not name_col:

            st.error(
                "Bowler name column not found."
            )

        else:

            required_columns = [
                "reliability_adjusted_score",
                "final_rank",
                "sample_reliability",
                "high_pressure_economy",
                "high_pressure_dot_ball_percentage",
                "high_pressure_wicket_rate"
            ]

            missing_columns = [
                col for col in required_columns
                if col not in df.columns
            ]

            if missing_columns:

                st.error(
                    "The bowler ranking file is missing required columns: "
                    + ", ".join(missing_columns)
                )

            else:

                # ------------------------------------------------
                # PREPARE RANKING
                # ------------------------------------------------

                df = get_valid_player_ranking(
                    df,
                    "reliability_adjusted_score",
                    "final_rank"
                )

                players = df[
                    name_col
                ].dropna().unique().tolist()

                st.caption(
                    f"Complete ranking: {len(df)} eligible bowlers"
                )

                # ------------------------------------------------
                # BOWLER SELECTION
                # ------------------------------------------------

                selected_bowler = st.selectbox(
                    "Search and select a bowler",
                    players
                )

                bowler = df[
                    df[name_col] == selected_bowler
                ].iloc[0]

                st.markdown("---")

                # ------------------------------------------------
                # MAIN PERFORMANCE METRICS
                # ------------------------------------------------

                section_heading(
                    "Bowler Pressure Performance"
                )

                c1, c2, c3 = st.columns(3)

                with c1:

                    metric_card(
                        "FINAL RANK",
                        int(bowler["final_rank"])
                    )

                with c2:

                    metric_card(
                        "PRESSURE INDEX",
                        format_number(
                            bowler["reliability_adjusted_score"]
                        )
                    )

                with c3:

                    metric_card(
                        "SAMPLE RELIABILITY",
                        f"{bowler['sample_reliability'] * 100:.1f}%"
                    )

                c4, c5, c6 = st.columns(3)

                with c4:

                    metric_card(
                        "HIGH PRESSURE ECONOMY",
                        format_number(
                            bowler["high_pressure_economy"]
                        )
                    )

                with c5:

                    metric_card(
                        "HIGH PRESSURE DOT BALL %",
                        format_number(
                            bowler["high_pressure_dot_ball_percentage"]
                        )
                    )

                with c6:

                    metric_card(
                        "HIGH PRESSURE WICKET RATE",
                        format_number(
                            bowler["high_pressure_wicket_rate"]
                        )
                    )

                st.markdown("---")

                # ------------------------------------------------
                # HIGH PRESSURE VS LOW PRESSURE
                # ------------------------------------------------

                section_heading(
                    "High Pressure vs Low Pressure"
                )

                comparison_metrics = [
                    (
                        "Economy",
                        "high_pressure_economy",
                        "low_pressure_economy"
                    ),
                    (
                        "Dot Ball %",
                        "high_pressure_dot_ball_percentage",
                        "low_pressure_dot_ball_percentage"
                    ),
                    (
                        "Wicket Rate",
                        "high_pressure_wicket_rate",
                        "low_pressure_wicket_rate"
                    ),
                    (
                        "Boundary Conceded %",
                        "high_pressure_boundary_percentage",
                        "low_pressure_boundary_percentage"
                    )
                ]

                comparison_rows = []

                for label, high_col, low_col in comparison_metrics:

                    if (
                        high_col in df.columns
                        and low_col in df.columns
                    ):

                        comparison_rows.append({
                            "Metric": label,
                            "High Pressure": pd.to_numeric(
                                pd.Series([bowler[high_col]]),
                                errors="coerce"
                            ).iloc[0],
                            "Low Pressure": pd.to_numeric(
                                pd.Series([bowler[low_col]]),
                                errors="coerce"
                            ).iloc[0]
                        })

                if comparison_rows:

                    comparison_df = pd.DataFrame(
                        comparison_rows
                    )

                    fig = go.Figure()

                    fig.add_trace(
                        go.Bar(
                            name="High Pressure",
                            x=comparison_df["Metric"],
                            y=comparison_df["High Pressure"],
                            marker_color=PINK
                        )
                    )

                    fig.add_trace(
                        go.Bar(
                            name="Low Pressure",
                            x=comparison_df["Metric"],
                            y=comparison_df["Low Pressure"],
                            marker_color=NAVY
                        )
                    )

                    fig.update_layout(
                        barmode="group",
                        title="Bowling Performance: High vs Low Pressure",
                        template="plotly_white",
                        height=430
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                # ------------------------------------------------
                # PRESSURE INDEX COMPONENTS
                # ------------------------------------------------

                st.markdown("---")

                section_heading(
                    "Pressure Index Components"
                )

                component_columns = {
                    "Economy Score": "economy_score",
                    "Dot Ball Score": "dot_ball_score",
                    "Wicket Rate Score": "wicket_rate_score",
                    "Boundary Prevention Score": "boundary_prevention_score",
                    "Consistency Score": "consistency_score"
                }

                component_rows = []

                for label, column in component_columns.items():

                    if column in df.columns:

                        component_value = pd.to_numeric(
                            pd.Series([bowler[column]]),
                            errors="coerce"
                        ).iloc[0]

                        if pd.notna(component_value):

                            component_rows.append({
                                "Component": label,
                                "Score": component_value
                            })

                if component_rows:

                    component_df = pd.DataFrame(
                        component_rows
                    )

                    fig = px.bar(
                        component_df,
                        x="Component",
                        y="Score",
                        text="Score",
                        color="Score",
                        color_continuous_scale=[
                            NAVY,
                            PINK
                        ]
                    )

                    fig.update_traces(
                        texttemplate="%{text:.2f}",
                        textposition="outside"
                    )

                    fig.update_layout(
                        title="Bowler Composite Score Breakdown",
                        template="plotly_white",
                        height=430,
                        yaxis_title="Component Score",
                        coloraxis_showscale=False
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                # ------------------------------------------------
                # COMPLETE PLAYER RECORD
                # ------------------------------------------------

                st.markdown("---")

                section_heading(
                    "Complete Bowler Statistics"
                )

                st.dataframe(
                    pd.DataFrame([bowler]),
                    use_container_width=True,
                    hide_index=True
                )

                safe_download(
                    pd.DataFrame([bowler]),
                    "selected_bowler_profile.csv"
                )

                # ------------------------------------------------
                # COMPLETE BOWLER RANKING
                # ------------------------------------------------

                st.markdown("---")

                section_heading(
                    "Complete Bowler Ranking"
                )

                ranking_columns = [
                    "final_rank",
                    "bowler_id",
                    "bowler_name",
                    "overall_matches",
                    "overall_legal_balls",
                    "high_pressure_legal_balls",
                    "high_pressure_economy",
                    "high_pressure_dot_ball_percentage",
                    "high_pressure_wicket_rate",
                    "bowler_value_under_pressure",
                    "sample_reliability",
                    "reliability_adjusted_score"
                ]

                ranking_columns = [
                    col for col in ranking_columns
                    if col in df.columns
                ]

                ranking_table = df[
                    ranking_columns
                ].copy()

                st.dataframe(
                    ranking_table,
                    use_container_width=True,
                    hide_index=True,
                    height=450
                )

                safe_download(
                    ranking_table,
                    "all_bowler_pressure_rankings.csv"
                )


# ============================================================
# PAGE 6: MATCH PRESSURE INDEX
# ============================================================

elif page == "MPI Analysis":

    section_heading(
        "Match Pressure Index Analysis"
    )

    if not is_valid_dataframe(mpi_data):

        show_missing_message(
            "Match Pressure Index"
        )

    else:

        df = mpi_data.copy()

        st.markdown(
            "### Dataset Overview"
        )

        col1, col2, col3 = st.columns(3)

        match_col = find_column(
            df,
            ["match_id"]
        )

        mpi_col = find_column(
            df,
            [
                "match_pressure_index",
                "mpi",
                "pressure_index",
                "match_mpi"
            ]
        )

        innings_col = find_column(
            df,
            ["innings"]
        )

        if match_col:

            with col1:

                metric_card(
                    "MATCHES / RECORDS",
                    f"{df[match_col].nunique():,}"
                )

        if mpi_col:

            df[mpi_col] = pd.to_numeric(
                df[mpi_col],
                errors="coerce"
            )

            with col2:

                metric_card(
                    "AVERAGE MPI",
                    format_number(
                        df[mpi_col].mean()
                    )
                )

            with col3:

                metric_card(
                    "HIGHEST MPI",
                    format_number(
                        df[mpi_col].max()
                    )
                )

            st.markdown("---")

            section_heading(
                "Match Pressure Index Distribution"
            )

            fig = px.histogram(
                df.dropna(
                    subset=[mpi_col]
                ),
                x=mpi_col,
                nbins=30,
                color_discrete_sequence=[PINK],
                title="Distribution of Match Pressure Index"
            )

            fig.update_layout(
                template="plotly_white",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if innings_col:

                section_heading(
                    "MPI by Innings"
                )

                fig = px.box(
                    df.dropna(
                        subset=[mpi_col]
                    ),
                    x=innings_col,
                    y=mpi_col,
                    color=innings_col,
                    color_discrete_sequence=[
                        PINK,
                        NAVY
                    ],
                    title="Match Pressure Index by Innings"
                )

                fig.update_layout(
                    template="plotly_white",
                    height=400
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            section_heading(
                "Highest Pressure Records"
            )

            top_records = df.nlargest(
                min(10, len(df)),
                mpi_col
            )

            st.dataframe(
                top_records,
                use_container_width=True
            )

            safe_download(
                top_records,
                "highest_pressure_matches.csv"
            )

        else:

            st.warning(
                "MPI score column was not detected."
            )

            st.write(
                df.columns.tolist()
            )

        section_heading(
            "MPI Dataset"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=350
        )


# ============================================================
# PAGE 7: MODEL & VALIDATION
# ============================================================

elif page == "Model & Validation":

    section_heading(
        "Model Performance and Validation"
    )

    if not is_valid_dataframe(model_metrics):

        show_missing_message(
            "Model Metrics"
        )

    else:

        df = model_metrics.copy()

        st.markdown(
            "### Win Probability Model Metrics"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        numeric_cols = [
            col for col in df.columns
            if pd.api.types.is_numeric_dtype(df[col])
        ]

        if numeric_cols:

            section_heading(
                "Model Metric Visualization"
            )

            metric_to_plot = st.selectbox(
                "Select Metric",
                numeric_cols
            )

            category_col = find_column(
                df,
                [
                    "innings",
                    "model",
                    "model_name",
                    "fold",
                    "dataset"
                ]
            )

            if category_col:

                fig = px.bar(
                    df,
                    x=category_col,
                    y=metric_to_plot,
                    color=category_col,
                    title=f"{metric_to_plot} Comparison",
                    color_discrete_sequence=[
                        PINK,
                        NAVY,
                        GOLD
                    ]
                )

            else:

                fig = px.bar(
                    df,
                    y=metric_to_plot,
                    title=f"{metric_to_plot} Values",
                    color_discrete_sequence=[PINK]
                )

            fig.update_layout(
                template="plotly_white",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        safe_download(
            df,
            "model_validation_metrics.csv"
        )

    st.markdown("---")

    section_heading(
        "Model Limitations and Research Scope"
    )

    limitations = [
        "Win probability predictions are available only for matches and deliveries covered by the out-of-fold prediction dataset.",
        "Delivery pressure is a match-state leverage proxy, not a direct measurement of a player's psychological stress.",
        "The Match Pressure Index is a relative percentile-based index, not an absolute measure of pressure.",
        "Player rankings depend on minimum-ball eligibility and the selected composite-score weights.",
        "IPL-specific filtering, validation and performance evaluation have not been conducted separately.",
        "Further validation is required to assess generalization across tournaments, teams and match conditions."
    ]

    for item in limitations:

        st.markdown(
            f"- {item}"
        )


# ============================================================
# 8. FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align:center;color:{GREY};padding:12px;">
        <b style="color:{NAVY};">
            PRESSURE PERFORMANCE ANALYTICS
        </b>
        <br>
        Cricket Intelligence Dashboard
        <br>
        <span style="font-size:12px;">
            Rajasthan Royals-inspired interface | Research Project
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
