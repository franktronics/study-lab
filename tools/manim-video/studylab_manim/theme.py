"""Color themes and typography shared by every video."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    text: str
    muted: str
    primary: str
    secondary: str
    accent: str
    highlight: str
    positive: str
    negative: str
    grid: str

    def color(self, key_or_hex: str | None, default: str = "text") -> str:
        """Resolve a semantic key ("primary", "accent", ...) or pass a hex color through."""
        if key_or_hex is None:
            return getattr(self, default)
        if key_or_hex.startswith("#"):
            return key_or_hex
        return getattr(self, key_or_hex)


DARK = Theme(
    name="dark",
    background="#15171C",
    text="#ECEFF4",
    muted="#8B93A6",
    primary="#58C4DD",
    secondary="#C39BD3",
    accent="#F4A261",
    highlight="#FFD166",
    positive="#83C167",
    negative="#FC6255",
    grid="#2E3440",
)

LIGHT = Theme(
    name="light",
    background="#FBFAF7",
    text="#1F2328",
    muted="#6B7280",
    primary="#1F6FEB",
    secondary="#8250DF",
    accent="#D9480F",
    highlight="#D4A017",
    positive="#2F9E44",
    negative="#D1242F",
    grid="#D8DEE4",
)

THEMES = {t.name: t for t in (DARK, LIGHT)}

# Environment variable set by the render script (--theme).
THEME_ENV = "STUDYLAB_THEME"


def current_theme() -> Theme:
    return THEMES[os.environ.get(THEME_ENV, "dark")]


# Font sizes (Text) by role.
FONT_SIZES = {
    "title": 60,
    "subtitle": 34,
    "heading": 34,
    "body": 30,
    "caption": 26,
    "small": 20,
}

# Font sizes (MathTex) by role.
MATH_SIZES = {
    "display": 56,
    "math": 44,
    "small": 34,
}

# Generic family resolved by Pango to the system sans-serif font (full Unicode: accents, umlauts, ß...).
FONT = "sans-serif"
