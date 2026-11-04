"""Smoke test and reference example for StudyScene helpers.

    uv run python -m studylab_manim.render examples/demo.py
"""

import numpy as np
from manim import *

from studylab_manim import StudyScene


class Intro(StudyScene):
    def construct(self):
        self.title_card("Fourier series", "Square wave approximation")


class Main(StudyScene):
    def construct(self):
        self.section("Partial sums")
        self.cite("Lecture 5, p. 12")
        self.caption("A square wave is a sum of odd harmonics with amplitudes 4/(πk).")
        formula = self.step_equation(
            [
                r"f(t) = \frac{4}{\pi} \sum_{k \text{ odd}} \frac{\sin(k t)}{k}",
                r"S_N(t) = \frac{4}{\pi} \sum_{k=1,3,\dots}^{N} \frac{\sin(k t)}{k}",
            ]
        )
        self.highlight(formula, label="partial sum")
        self.clear_content()

        ax = self.axes(x_range=(-4, 4, 1), y_range=(-1.5, 1.5, 0.5), x_label="t", y_label="S_N(t)")
        self.play(Create(ax))
        self.caption("More harmonics → closer to the square wave, but the overshoot remains (Gibbs).")

        def partial(n):
            return lambda t: 4 / np.pi * sum(np.sin(k * t) / k for k in range(1, n + 1, 2))

        curve = self.plot(ax, partial(1))
        self.play(Create(curve))
        for n, color in [(3, "secondary"), (9, "accent"), (31, "highlight")]:
            nxt = self.plot(ax, partial(n), color=color)
            self.play(Transform(curve, nxt))
            self.wait(0.5)


class Recap(StudyScene):
    def construct(self):
        self.end_card(
            [
                "Odd harmonics only, amplitude ∝ 1/k",
                "Partial sums converge to the square wave",
                "Overshoot ≈ 9 % stays near jumps (Gibbs)",
            ]
        )
