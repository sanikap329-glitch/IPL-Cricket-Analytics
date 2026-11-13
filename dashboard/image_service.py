
"""
Image Service for IPL Batter Intelligence & Strategy Platform.

Uses one latest IPL franchise photograph per player.
Season-wise image support can be added later.
"""

from typing import Optional
from html import escape

from dashboard.config import TEAM_COLORS


# ============================================================
# LATEST IPL PLAYER PHOTOGRAPHS
# ============================================================

# Add verified direct image URLs here.
# Only use photographs showing the player's latest IPL jersey.
#
# Example:
# "Player Name": "https://example.com/player-photo.jpg"

PLAYER_IMAGES = {
    # Add verified 2026 IPL player image URLs here.
}


# ============================================================
# PLAYER IMAGE LOOKUP
# ============================================================

def get_player_image_url(
    batter_name: str,
    season: Optional[str] = None
) -> Optional[str]:
    """
    Returns the latest available IPL photograph for a player.

    The season argument is retained for compatibility with
    existing dashboard files. It is not used for image lookup.
    """

    if not batter_name:
        return None

    return PLAYER_IMAGES.get(batter_name.strip())


# ============================================================
# PLAYER AVATAR HTML
# ============================================================

def render_player_avatar_html(
    batter_name: str,
    team_name: str,
    size: int = 56,
    border_radius: str = "50%",
    season: Optional[str] = None
) -> str:
    """
    Displays the latest IPL player photograph.

    If no photograph is available, displays
    a franchise-coloured initials avatar.
    """

    team_info = TEAM_COLORS.get(team_name, {
        "primary": "#415C77",
        "secondary": "#FFB800",
        "text": "#ffffff"
    })

    primary_color = team_info.get("primary", "#415C77")
    secondary_color = team_info.get("secondary", "#FFB800")
    text_color = team_info.get("text", "#ffffff")

    # Generate initials
    parts = [p for p in batter_name.split() if p]

    if len(parts) >= 2:
        initials = (
            parts[0][0] + parts[-1][0]
        ).upper()
    elif len(parts) == 1:
        initials = parts[0][:2].upper()
    else:
        initials = "IPL"

    safe_initials = escape(initials)
    safe_name = escape(batter_name, quote=True)

    font_size = max(int(size * 0.38), 11)

    # Latest player photograph
    img_url = get_player_image_url(batter_name)

    if img_url:
        safe_url = escape(img_url, quote=True)

        return (
            f'<div class="player-avatar-wrapper" '
            f'style="width:{size}px;height:{size}px;'
            f'min-width:{size}px;border-radius:{border_radius};'
            f'border:2px solid {primary_color};overflow:hidden;'
            f'position:relative;background:{primary_color};'
            f'display:inline-block;vertical-align:middle;">'

            f'<img src="{safe_url}" alt="{safe_name}" '
            f'style="width:100%;height:100%;'
            f'object-fit:cover;display:block;" '
            f'onerror="this.style.display=\'none\';'
            f'this.nextElementSibling.style.display=\'flex\';" />'

            f'<div style="display:none;width:100%;height:100%;'
            f'background:{primary_color};color:{text_color};'
            f'align-items:center;justify-content:center;'
            f'font-weight:800;font-size:{font_size}px;">'
            f'{safe_initials}</div>'

            f'</div>'
        )

    # Initials fallback
    return (
        f'<div class="player-avatar-direct" '
        f'style="width:{size}px;height:{size}px;'
        f'min-width:{size}px;border-radius:{border_radius};'
        f'border:2px solid {secondary_color};'
        f'background:{primary_color};color:{text_color};'
        f'display:inline-flex;align-items:center;'
        f'justify-content:center;font-weight:800;'
        f'font-size:{font_size}px;vertical-align:middle;">'
        f'{safe_initials}'
        f'</div>'
    )
