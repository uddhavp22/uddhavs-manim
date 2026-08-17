"""Reusable visual model for a characteristic-function plot.

This is intentionally a lightweight holder rather than a VGroup subclass.
Manim CE can then animate individual parts without restructuring a parent
mobject's scene family, while every scene still uses the same semantic object.
"""

from __future__ import annotations

import numpy as np
from manim import DashedLine, Dot, VGroup, VMobject, always_redraw

from . import layout
from .palette import EMPIRICAL, MUTED, TARGET


class CharacteristicFunctionPlot:
    """Own the shared frequency axes and factories for curves and probes."""

    def __init__(self, *, show_window: bool = False):
        self.axes = layout.frequency_axes()
        self.furniture = layout.frequency_axis_labels(self.axes)
        self.window = layout.frequency_window(self.axes) if show_window else None

    def mount(self, scene) -> None:
        scene.add(self.axes, self.furniture)
        if self.window is not None:
            scene.add(self.window)

    def curve(self, xs, ys, colour=EMPIRICAL, *, width: float = 4,
              opacity: float = 1.0) -> VMobject:
        curve = VMobject().set_stroke(colour, width, opacity=opacity)
        curve.set_points_as_corners([
            self.axes.c2p(x, y) for x, y in zip(xs, ys)
        ])
        return curve

    def partial_curve(self, xs, ys, tracker, colour=TARGET, *,
                      width: float = 4):
        xs = np.asarray(xs)
        ys = np.asarray(ys)

        def current_curve():
            mask = xs <= max(tracker.get_value(), 1e-4)
            shown_xs, shown_ys = xs[mask], ys[mask]
            if len(shown_xs) < 2:
                shown_xs = np.array([0.0, 1e-4])
                shown_ys = np.array([ys[0], ys[0]])
            return self.curve(shown_xs, shown_ys, colour, width=width)

        return always_redraw(current_curve)

    def probe(self, t: float, value: float, colour=EMPIRICAL) -> VGroup:
        return VGroup(
            DashedLine(
                self.axes.c2p(t, 0), self.axes.c2p(t, value),
                dash_length=0.07,
            ).set_stroke(MUTED, 1.5),
            Dot(self.axes.c2p(t, value), radius=0.085).set_fill(colour, 1),
        )

    def gaussian_curve(self):
        return layout.gaussian_frequency_curve(self.axes)

    def gaussian_probe(self, t: float) -> VGroup:
        return layout.gaussian_frequency_probe(self.axes, t)

    def make_window(self) -> VGroup:
        if self.window is None:
            self.window = layout.frequency_window(self.axes)
        return self.window
