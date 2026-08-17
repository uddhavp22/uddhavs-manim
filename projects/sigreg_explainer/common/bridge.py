"""Shared visual handoffs between explainer chapters."""

from __future__ import annotations

import numpy as np
from manim import Arrow, DOWN, ORIGIN, RIGHT, UP, VGroup

from . import layout
from . import type as ty
from .palette import CLOUD, INK, MUTED, TARGET


def vector_bridge() -> VGroup:
    """Chapter B's scalar-score-to-vector-batch handoff."""

    def vector_column(label, entries):
        name = ty.maths(label, size=ty.EQ, color=CLOUD)
        column = ty.maths(
            Rf"\begin{{bmatrix}}{entries}\\\vdots\end{{bmatrix}}",
            size=ty.EQ,
            color=CLOUD,
        )
        return VGroup(name, column).arrange(DOWN, buff=0.12)

    vector_samples = VGroup(
        vector_column(R"\mathbf z_1", R"0.4\\-0.7\\1.1"),
        vector_column(R"\mathbf z_2", R"-0.2\\0.8\\0.5"),
        ty.maths(R"\cdots", size=ty.EQ, color=MUTED),
        vector_column(R"\mathbf z_N", R"1.0\\0.1\\-0.6"),
    ).arrange(RIGHT, buff=0.38)
    question_arrow = Arrow(
        ORIGIN, 1.0 * RIGHT, buff=0,
        stroke_width=2.6,
        max_tip_length_to_length_ratio=0.16,
    ).set_color(TARGET)
    question = ty.maths("?", size=ty.EQ, color=TARGET)
    question.next_to(question_arrow, UP, buff=0.06)
    question_link = VGroup(question_arrow, question)
    vector_score = ty.maths(
        R"\mathcal T\in\mathbb R",
        size=ty.EQ_DISPLAY,
        color=INK,
    )
    bridge = VGroup(
        vector_samples,
        question_link,
        vector_score,
    ).arrange(RIGHT, buff=0.42)
    bridge.move_to(np.array([0.0, -0.15, 0.0]))
    layout.fit_in_frame(bridge)
    return bridge
