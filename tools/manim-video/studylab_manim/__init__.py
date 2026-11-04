"""Shared Manim Community setup for study-lab explanation videos."""

from .config import ensure_tex_on_path
from .scene import StudyScene
from .theme import DARK, LIGHT, Theme

ensure_tex_on_path()

__all__ = ["StudyScene", "Theme", "DARK", "LIGHT"]
