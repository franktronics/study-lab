"""StudyScene: base class with themed factories and layout-aware helpers."""

from __future__ import annotations

import textwrap
from collections.abc import Callable, Sequence

from manim import (
    DOWN,
    DR,
    LEFT,
    ORIGIN,
    RIGHT,
    UL,
    UP,
    Axes,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    Mobject,
    Scene,
    SurroundingRectangle,
    Text,
    TransformMatchingTex,
    VGroup,
    Write,
)

from . import config as cfg
from .theme import FONT, FONT_SIZES, MATH_SIZES, Theme, current_theme


class StudyScene(Scene):
    """Base class for every studio scene.

    Gives a themed background, factories for text/math/axes, and persistent
    layout elements (section header, caption, citation) that replace themselves.
    """

    theme: Theme

    def setup(self) -> None:
        self.theme = current_theme()
        self.camera.background_color = self.theme.background
        MathTex.set_default(tex_template=cfg.TEX_TEMPLATE)
        self._section: Mobject | None = None
        self._caption: Mobject | None = None
        self._cite: Mobject | None = None

    # --- Factories ---------------------------------------------------------

    def c(self, key_or_hex: str | None = None, default: str = "text") -> str:
        """Theme color by semantic key ("primary", "accent", ...) or hex."""
        return self.theme.color(key_or_hex, default)

    def text(self, s: str, size: str | int = "body", color: str | None = None, **kwargs) -> Text:
        font_size = FONT_SIZES[size] if isinstance(size, str) else size
        return Text(s, font=FONT, font_size=font_size, color=self.c(color), **kwargs)

    def tex(self, *parts: str, size: str | int = "math", color: str | None = None, **kwargs) -> MathTex:
        font_size = MATH_SIZES[size] if isinstance(size, str) else size
        return MathTex(*parts, font_size=font_size, color=self.c(color), **kwargs)

    def axes(
        self,
        x_range: Sequence[float] = (-5, 5, 1),
        y_range: Sequence[float] = (-3, 3, 1),
        x_length: float = 10,
        y_length: float = 5,
        x_label: str | None = None,
        y_label: str | None = None,
        numbers: bool = True,
        **kwargs,
    ) -> Axes:
        """Themed axes centered in the content area. Labels are LaTeX strings."""
        ax = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "color": self.theme.muted,
                "include_numbers": numbers,
                "font_size": 22,
                "include_tip": True,
                "tip_length": 0.2,
            },
            **kwargs,
        )
        if numbers:
            for axis in (ax.x_axis, ax.y_axis):
                axis.numbers.set_color(self.theme.muted)
        if x_label or y_label:
            labels = ax.get_axis_labels(
                x_label=self.tex(x_label or "", size="small"),
                y_label=self.tex(y_label or "", size="small"),
            )
            ax.add(labels)
        return self.fit(ax)

    def plot(self, ax: Axes, fn: Callable[[float], float], color: str = "primary", **kwargs):
        kwargs.setdefault("stroke_width", 4)
        return ax.plot(fn, color=self.c(color), **kwargs)

    # --- Layout ------------------------------------------------------------

    def fit(self, mob: Mobject, center: bool = True) -> Mobject:
        """Scale mob down (never up) to fit the content area, optionally center it there."""
        if mob.width > cfg.CONTENT_WIDTH:
            mob.scale_to_fit_width(cfg.CONTENT_WIDTH)
        if mob.height > cfg.CONTENT_HEIGHT:
            mob.scale_to_fit_height(cfg.CONTENT_HEIGHT)
        if center:
            mob.move_to([0, cfg.CONTENT_CENTER_Y, 0])
        return mob

    def content(self) -> list[Mobject]:
        """Mobjects on screen except the persistent header/caption/citation."""
        persistent = {self._section, self._caption, self._cite}
        return [m for m in self.mobjects if m not in persistent]

    def clear_content(self, run_time: float = 0.6) -> None:
        mobs = self.content()
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def clear_all(self, run_time: float = 0.6) -> None:
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)
        self._section = self._caption = self._cite = None

    def _replace(self, old: Mobject | None, new: Mobject | None, run_time: float) -> None:
        anims = []
        if old is not None:
            anims.append(FadeOut(old))
        if new is not None:
            anims.append(FadeIn(new))
        if anims:
            self.play(*anims, run_time=run_time)

    def section(self, title: str | None, run_time: float = 0.5) -> None:
        """Persistent header in the top-left corner. None removes it."""
        new = None
        if title:
            new = self.text(title, size="heading", color="primary", weight="BOLD")
            new.to_corner(UL, buff=cfg.MARGIN).set_y(cfg.HEADER_Y)
        self._replace(self._section, new, run_time)
        self._section = new

    def caption(self, s: str | None, run_time: float = 0.5, width_chars: int = 90) -> None:
        """Explanatory text at the bottom of the screen, replacing the previous one. None removes it."""
        new = None
        if s:
            wrapped = "\n".join(textwrap.wrap(s, width_chars))
            new = self.text(wrapped, size="caption", line_spacing=0.8)
            if new.width > cfg.CAPTION_MAX_WIDTH:
                new.scale_to_fit_width(cfg.CAPTION_MAX_WIDTH)
            new.move_to([0, cfg.CAPTION_Y, 0])
        self._replace(self._caption, new, run_time)
        self._caption = new

    def cite(self, source: str | None, run_time: float = 0.3) -> None:
        """Small source reference in the bottom-right corner (e.g. "Lecture 5, p. 12"). None removes it."""
        new = None
        if source:
            new = self.text(source, size="small", color="muted", slant="ITALIC")
            new.to_corner(DR, buff=cfg.MARGIN).set_y(cfg.CITE_Y)
        self._replace(self._cite, new, run_time)
        self._cite = new

    # --- Sequences ---------------------------------------------------------

    def title_card(self, title: str, subtitle: str | None = None, hold: float = 1.5) -> None:
        t = self.text(title, size="title", weight="BOLD")
        group = VGroup(t)
        if subtitle:
            group.add(self.text(subtitle, size="subtitle", color="muted"))
        group.arrange(DOWN, buff=0.4).move_to(ORIGIN)
        if group.width > cfg.CONTENT_WIDTH:
            group.scale_to_fit_width(cfg.CONTENT_WIDTH)
        self.play(Write(t), *[FadeIn(m, shift=UP * 0.2) for m in group[1:]])
        self.wait(hold)
        self.play(FadeOut(group))

    def end_card(self, points: Sequence[str], title: str = "Key points", hold: float = 3.0) -> None:
        """Recap screen with bullet points. Clears everything first."""
        self.clear_all()
        heading = self.text(title, size="heading", color="primary", weight="BOLD")
        bullets = VGroup(
            *[
                VGroup(self.text("•", color="accent"), self.text(p)).arrange(RIGHT, buff=0.25)
                for p in points
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        group = VGroup(heading, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        if group.width > cfg.CONTENT_WIDTH:
            group.scale_to_fit_width(cfg.CONTENT_WIDTH)
        group.move_to(ORIGIN)
        self.play(FadeIn(heading))
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(hold)
        self.play(FadeOut(group))

    def step_equation(
        self,
        steps: Sequence[str],
        stacked: bool = False,
        hold: float = 1.0,
        color: str | None = None,
    ) -> Mobject:
        """Reveal a derivation step by step.

        stacked=False: each step morphs into the next (TransformMatchingTex), one line on screen.
        stacked=True:  steps accumulate as aligned lines (use "&=" in steps for alignment).
        Returns what stays on screen.
        """
        if stacked:
            lines = MathTex(
                r"\begin{aligned}" + r" \\ ".join(steps) + r"\end{aligned}",
                font_size=MATH_SIZES["math"],
                color=self.c(color),
            )
            self.fit(lines)
            self.play(Write(lines), run_time=1.0 + 0.6 * len(steps))
            self.wait(hold)
            return lines

        current = self.fit(self.tex(steps[0], color=color))
        self.play(Write(current))
        self.wait(hold)
        for step in steps[1:]:
            nxt = self.fit(self.tex(step, color=color))
            self.play(TransformMatchingTex(current, nxt))
            self.wait(hold)
            current = nxt
        return current

    def highlight(self, mob: Mobject, color: str = "highlight", label: str | None = None, buff: float = 0.12):
        """Draw a box around mob (optionally with a label below). Returns the box (and label) group."""
        box = SurroundingRectangle(mob, color=self.c(color), buff=buff, corner_radius=0.08, stroke_width=3)
        group = VGroup(box)
        anims = [Create(box)]
        if label:
            lab = self.text(label, size="small", color=color).next_to(box, DOWN, buff=0.15)
            group.add(lab)
            anims.append(FadeIn(lab))
        self.play(*anims)
        return group

