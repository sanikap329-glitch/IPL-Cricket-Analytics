
"""
CSS styles and HTML component templates for the IPL Franchise-inspired Sports-Tech UI.
Dark stadium charcoal/black background, franchise accents, and gold/purple/red phase colors.
Includes clean HTML formatting to prevent markdown code block rendering issues.
"""

from dashboard.config import TEAM_COLORS, PHASE_COLORS, PHASES


def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% -10%, #171d2b 0%, #0a0c12 55%, #050609 100%) !important;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Rajdhani', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0c0f17 !important;
        border-right: 1px solid rgba(255, 184, 0, 0.15) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFB800 !important;
        letter-spacing: 1.5px;
    }

    /* TOP NAVIGATION */
    .top-navbar-wrapper {
        background: rgba(14, 18, 28, 0.95);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 184, 0, 0.25);
        border-radius: 14px;
        padding: 12px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7), 0 0 20px rgba(255, 184, 0, 0.08);
    }

    .top-navbar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        min-width: 210px;
    }

    .top-navbar-logo {
        font-size: 1.9rem;
        line-height: 1;
    }

    .top-navbar-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1.5px;
        line-height: 1;
    }

    .top-navbar-title span {
        color: #FFB800;
    }

    .top-navbar-sub {
        font-size: 0.68rem;
        color: #94a3b8;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 2px;
    }

    .top-navbar-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 184, 0, 0.1);
        border: 1px solid rgba(255, 184, 0, 0.35);
        padding: 6px 14px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        color: #FFB800;
        letter-spacing: 0.8px;
        white-space: nowrap;
    }

    .live-pulse {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00e676;
        box-shadow: 0 0 8px #00e676;
    }

    div[data-testid="stRadio"]:has(input[aria-label="top_navbar_page"]) > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        justify-content: center !important;
        align-items: center !important;
        background: rgba(10, 13, 20, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 5px 8px !important;
        border-radius: 30px !important;
    }

    div[data-testid="stRadio"]:has(input[aria-label="top_navbar_page"]) > div[role="radiogroup"] label {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 20px !important;
        padding: 7px 16px !important;
        color: #94a3b8 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"]:has(input[aria-label="top_navbar_page"]) > div[role="radiogroup"] label:hover {
        color: #ffffff !important;
        background: rgba(255, 184, 0, 0.1) !important;
    }

    div[data-testid="stRadio"]:has(input[aria-label="top_navbar_page"]) > div[role="radiogroup"] label:has(input:checked) {
        background: rgba(255, 184, 0, 0.2) !important;
        color: #FFB800 !important;
        border: 1px solid rgba(255, 184, 0, 0.55) !important;
        box-shadow: 0 0 14px rgba(255, 184, 0, 0.25) !important;
    }

    div[data-testid="stRadio"]:has(input[aria-label="top_navbar_page"]) > div[role="radiogroup"] label input[type="radio"],
    div[data-testid="stRadio"]:has(input[aria-label="top_navbar_page"]) > div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    /* HERO */
    .stadium-hero {
        position: relative;
        background: linear-gradient(180deg, rgba(22, 28, 42, 0.95) 0%, rgba(10, 13, 20, 0.98) 100%),
                    radial-gradient(ellipse at 50% -20%, rgba(255, 184, 0, 0.22) 0%, transparent 65%);
        border: 1px solid rgba(255, 184, 0, 0.25);
        border-radius: 16px;
        padding: 34px 30px 28px 30px;
        margin-bottom: 24px;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7), 0 0 30px rgba(255, 184, 0, 0.08);
    }

    .stadium-hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #D71920 0%, #EA1A85 20%, #004BA0 40%, #FFCB05 60%, #F26522 80%, #3A225D 100%);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255, 184, 0, 0.12);
        color: #FFB800;
        border: 1px solid rgba(255, 184, 0, 0.4);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.9rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 0 0 10px 0;
        background: linear-gradient(90deg, #ffffff 45%, #FFB800 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1.5px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 840px;
        line-height: 1.5;
        margin: 0;
    }

    /* KPI */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: rgba(18, 23, 34, 0.82);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px 18px;
        transition: all 0.25s ease-in-out;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        border-color: rgba(255, 184, 0, 0.45);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5), 0 0 20px rgba(255, 184, 0, 0.1);
    }

    .kpi-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 4px;
    }

    .kpi-sub {
        font-size: 0.78rem;
        color: #FFB800;
        font-weight: 500;
    }

    /* SECTION HEADER */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 28px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .section-indicator {
        width: 4px;
        height: 24px;
        background: #FFB800;
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(255, 184, 0, 0.6);
    }

    .section-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 1px;
        margin: 0;
        text-transform: uppercase;
    }

    .section-desc {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-left: auto;
    }

    /* FEATURE CARDS */
    .feature-card {
        background: rgba(18, 23, 34, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 22px 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.25s ease-in-out;
    }

    .feature-card:hover {
        background: rgba(24, 30, 46, 0.85);
        border-color: rgba(255, 184, 0, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }

    .feature-badge {
        display: inline-block;
        background: rgba(255, 184, 0, 0.12);
        color: #FFB800;
        border: 1px solid rgba(255, 184, 0, 0.35);
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: fit-content;
        margin-bottom: 10px;
    }

    .feature-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 8px 0;
    }

    .feature-desc {
        font-size: 0.88rem;
        color: #94a3b8;
        line-height: 1.45;
        margin-bottom: 14px;
        flex-grow: 1;
    }

    .feature-stat {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05rem;
        color: #FFB800;
        font-weight: 600;
        border-top: 1px dashed rgba(255, 255, 255, 0.08);
        padding-top: 10px;
    }

    /* PLAYER PROFILE CARD */
    .player-card {
        background: rgba(18, 23, 34, 0.85);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease-in-out;
    }

    .player-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
    }

    .player-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 14px;
    }

    .player-info-name {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.15;
    }

    .player-info-team {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 3px;
    }

    .player-stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: 12px;
    }

    .player-stats-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-top: 12px;
    }

    .player-stat-box {
        background: rgba(10, 13, 20, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 8px 4px;
        text-align: center;
    }

    .player-stat-num {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }

    .player-stat-lbl {
        font-size: 0.68rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        margin-top: 2px;
    }

    /* CALLOUTS */
    .info-callout {
        background: rgba(18, 23, 34, 0.65);
        border-left: 4px solid #FFB800;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 16px 0;
        font-size: 0.88rem;
        line-height: 1.5;
        color: #cbd5e1;
    }

    .warning-callout {
        background: rgba(30, 22, 18, 0.65);
        border-left: 4px solid #E63946;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 16px 0;
        font-size: 0.88rem;
        line-height: 1.5;
        color: #fca5a5;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(18, 23, 34, 0.6) !important;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #94a3b8 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        border-radius: 6px !important;
        padding: 8px 16px !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 184, 0, 0.15) !important;
        color: #FFB800 !important;
        border: 1px solid rgba(255, 184, 0, 0.4) !important;
    }

    /* STREAMLIT WIDGETS */
    div[data-testid="stMetricValue"] {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.9rem !important;
        color: #ffffff !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stSelectbox label, .stSlider label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    </style>
    """


def render_hero(title: str, subtitle: str, badge: str = "T20 ANALYTICS ENGINE") -> str:
    return (
        f'<div class="stadium-hero">'
        f'<div class="hero-badge">{badge}</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-subtitle">{subtitle}</div>'
        f'</div>'
    )


def render_kpi(label: str, value: str, sub: str = "", accent_color: str = "#FFB800") -> str:
    return (
        f'<div class="kpi-card" style="border-left: 3px solid {accent_color};">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub" style="color: {accent_color};">{sub}</div>'
        f'</div>'
    )


def render_section_header(title: str, description: str = "") -> str:
    desc_html = f'<div class="section-desc">{description}</div>' if description else ""
    return (
        f'<div class="section-header">'
        f'<div class="section-indicator"></div>'
        f'<div class="section-title">{title}</div>'
        f'{desc_html}'
        f'</div>'
    )


def render_player_card(
    batter_name: str,
    team_name: str,
    runs: int,
    balls: int,
    sr: float,
    avg: float,
    rating: float = None,
    avatar_size: int = 72,
    season: int = None,
) -> str:
    """
    Renders a player profile card.
    Uses a verified player image for the selected season.
    Displays initials if a verified season image is unavailable.
    """

    team_info = TEAM_COLORS.get(team_name, {
        "primary": "#415C77",
        "secondary": "#FFB800",
        "text": "#ffffff",
        "short": team_name[:3].upper() if team_name else "IPL"
    })

    primary_color = team_info["primary"]
    secondary_color = team_info.get("secondary", "#FFB800")
    text_color = team_info.get("text", "#ffffff")
    short_name = team_info.get("short", "IPL")

    from dashboard.image_service import get_player_image_url

    img_url = get_player_image_url(
        batter_name,
        season=season
    )

    parts = [p for p in batter_name.split() if p]
    initials = (
        (parts[0][0] + parts[-1][0]).upper()
        if len(parts) >= 2
        else (parts[0][:2].upper() if parts else "??")
    )

    # Rating pill
    rating_pill = ""
    if rating is not None:
        rating_pill = (
            f'<div style="display:inline-flex; align-items:center; gap:5px; '
            f'background:rgba(255,184,0,0.15); '
            f'border:1px solid rgba(255,184,0,0.5); '
            f'border-radius:20px; padding:2px 10px; margin-bottom:8px;">'
            f'<span style="font-family:\'Rajdhani\',sans-serif; '
            f'font-weight:800; font-size:1.05rem; color:#FFB800;">'
            f'{rating:.1f}</span>'
            f'<span style="font-size:0.65rem; font-weight:700; '
            f'color:#94a3b8; letter-spacing:0.8px; text-transform:uppercase;">'
            f'Rating</span>'
            f'</div>'
        )

    # Player statistics
    stats_html = (
        f'<div style="display:grid; grid-template-columns:1fr 1fr; '
        f'gap:6px 10px; margin-top:10px;">'
        f'<div><div style="font-family:\'Rajdhani\',sans-serif; '
        f'font-size:1.25rem; font-weight:800; color:#ffffff; line-height:1;">'
        f'{runs:,}</div><div style="font-size:0.65rem; color:#94a3b8; '
        f'font-weight:600; text-transform:uppercase; letter-spacing:0.8px;">'
        f'Runs</div></div>'
        f'<div><div style="font-family:\'Rajdhani\',sans-serif; '
        f'font-size:1.25rem; font-weight:800; color:#ffffff; line-height:1;">'
        f'{sr:.1f}</div><div style="font-size:0.65rem; color:#94a3b8; '
        f'font-weight:600; text-transform:uppercase; letter-spacing:0.8px;">'
        f'Strike Rate</div></div>'
        f'<div><div style="font-family:\'Rajdhani\',sans-serif; '
        f'font-size:1.25rem; font-weight:800; color:#ffffff; line-height:1;">'
        f'{avg:.1f}</div><div style="font-size:0.65rem; color:#94a3b8; '
        f'font-weight:600; text-transform:uppercase; letter-spacing:0.8px;">'
        f'Average</div></div>'
        f'<div><div style="font-family:\'Rajdhani\',sans-serif; '
        f'font-size:1.25rem; font-weight:800; color:#ffffff; line-height:1;">'
        f'{balls:,}</div><div style="font-size:0.65rem; color:#94a3b8; '
        f'font-weight:600; text-transform:uppercase; letter-spacing:0.8px;">'
        f'Balls</div></div>'
        f'</div>'
    )

    left_panel = (
        f'<div style="position:relative; z-index:2; padding:16px 0 16px 16px; '
        f'width:60%; display:flex; flex-direction:column; '
        f'justify-content:center; min-height:200px;">'
        f'{rating_pill}'
        f'<div style="font-family:\'Rajdhani\',sans-serif; '
        f'font-size:1.45rem; font-weight:800; color:#ffffff; '
        f'line-height:1.1; margin-bottom:4px;">{batter_name}</div>'
        f'<div style="font-size:0.72rem; font-weight:700; '
        f'color:{secondary_color}; text-transform:uppercase; '
        f'letter-spacing:1px; margin-bottom:4px;">● {short_name}</div>'
        f'{stats_html}'
        f'</div>'
    )

    # Right-side image panel
    if img_url:
        right_panel = (
            f'<div style="position:absolute; top:0; right:0; bottom:0; '
            f'width:46%; z-index:1;">'
            f'<div style="position:absolute; inset:0; '
            f'background:linear-gradient(90deg, {primary_color}ff 0%, '
            f'{primary_color}99 25%, {primary_color}22 60%, transparent 100%); '
            f'z-index:2;"></div>'
            f'<div style="position:absolute; inset:0; display:flex; '
            f'align-items:center; justify-content:center; '
            f'background:{primary_color}44;">'
            f'<span style="font-family:Rajdhani,sans-serif; font-weight:800; '
            f'font-size:3rem; color:{text_color}; opacity:0.4;">'
            f'{initials}</span></div>'
            f'<img src="{img_url}" alt="{batter_name}" '
            f'style="position:relative; z-index:1; width:100%; height:100%; '
            f'object-fit:cover; object-position:top center; display:block;" '
            f'onerror="this.remove();" />'
            f'</div>'
        )
    else:
        right_panel = (
            f'<div style="position:absolute; top:0; right:0; bottom:0; '
            f'width:46%; z-index:1; display:flex; align-items:center; '
            f'justify-content:center;">'
            f'<div style="position:absolute; inset:0; '
            f'background:linear-gradient(90deg, {primary_color}ff 0%, '
            f'transparent 100%); z-index:2;"></div>'
            f'<span style="font-family:Rajdhani,sans-serif; font-weight:800; '
            f'font-size:4rem; color:{text_color}; opacity:0.18; '
            f'letter-spacing:4px; z-index:1;">{initials}</span>'
            f'</div>'
        )

    return (
        f'<div style="position:relative; overflow:hidden; border-radius:14px; '
        f'background:linear-gradient(135deg, {primary_color} 0%, '
        f'{primary_color}cc 50%, {primary_color}88 100%); '
        f'border:1px solid {primary_color}66; '
        f'border-left:4px solid {secondary_color}; '
        f'box-shadow:0 8px 28px rgba(0,0,0,0.5), '
        f'0 0 0 1px rgba(255,255,255,0.04); '
        f'margin-bottom:4px; min-height:200px;">'
        f'{right_panel}'
        f'{left_panel}'
        f'</div>'
    )
