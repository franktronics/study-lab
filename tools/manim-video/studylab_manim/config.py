"""Canvas, layout zones, render qualities, paths and the LaTeX template."""

from __future__ import annotations

import os
import platform
from pathlib import Path

from manim import TexTemplate, config

# --- Paths -----------------------------------------------------------------

TOOL_ROOT = Path(__file__).resolve().parents[1]
STUDIO_DIR = TOOL_ROOT / "studio"
CACHE_DIR = TOOL_ROOT / ".cache"

# --- Canvas (Manim units, 16:9 frame of 14.22 x 8) -------------------------

FRAME_WIDTH = config.frame_width
FRAME_HEIGHT = config.frame_height
MARGIN = 0.4

# Layout zones. Keep content inside CONTENT_* so it never collides with
# the section header (top), the caption (bottom) or the citation (bottom right).
HEADER_Y = FRAME_HEIGHT / 2 - MARGIN - 0.25
CAPTION_Y = -FRAME_HEIGHT / 2 + MARGIN + 0.55
CITE_Y = -FRAME_HEIGHT / 2 + MARGIN - 0.05

CONTENT_TOP = HEADER_Y - 0.55
CONTENT_BOTTOM = CAPTION_Y + 0.6
CONTENT_LEFT = -FRAME_WIDTH / 2 + MARGIN
CONTENT_RIGHT = FRAME_WIDTH / 2 - MARGIN
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT
CONTENT_HEIGHT = CONTENT_TOP - CONTENT_BOTTOM
CONTENT_CENTER_Y = (CONTENT_TOP + CONTENT_BOTTOM) / 2

CAPTION_MAX_WIDTH = FRAME_WIDTH - 2 * MARGIN - 1.0

# --- Render qualities ------------------------------------------------------

QUALITIES = {
    # name: (manim quality flag, fps, output subfolder manim uses)
    "preview": ("-ql", 15, "480p15"),
    "final": ("-qh", 30, "1080p30"),
}

# --- LaTeX -----------------------------------------------------------------

# Packages required by TEX_TEMPLATE (used by the check script and install hints).
TEX_PACKAGES = ["standalone", "preview", "amsmath", "amsfonts", "mathtools", "tools", "xcolor", "dvisvgm"]
TEX_FILES = ["standalone.cls", "preview.sty", "amsmath.sty", "amssymb.sty", "mathtools.sty", "bm.sty", "xcolor.sty"]

TEX_TEMPLATE = TexTemplate(
    documentclass=r"\documentclass[preview]{standalone}",
    preamble="\n".join(
        [
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\usepackage{mathtools}",
            r"\usepackage{bm}",
            r"\usepackage{xcolor}",
        ]
    ),
)


def tinytex_bin_dirs() -> list[Path]:
    """Default TinyTeX binary folders, so a fresh install works without a new shell."""
    home = Path.home()
    system = platform.system()
    if system == "Darwin":
        return [home / "Library/TinyTeX/bin/universal-darwin"]
    if system == "Windows":
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        return [appdata / "TinyTeX/bin/windows", appdata / "TinyTeX/bin/win32"]
    return [home / ".TinyTeX/bin/x86_64-linux", home / ".TinyTeX/bin/aarch64-linux"]


def ensure_tex_on_path() -> None:
    extra = [str(p) for p in tinytex_bin_dirs() if p.is_dir()]
    if extra:
        os.environ["PATH"] = os.pathsep.join([*extra, os.environ.get("PATH", "")])
