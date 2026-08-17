"""Stateful distribution pictures used by Chapter B.

The mathematical state lives here with the mobjects that display it. Scenes
choose *why* the state changes; this object keeps bars, guides, and samples on
one coordinate system and preserves their identity through those changes.
"""

from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup, DashedLine, Dot, NumberLine, Rectangle, Transform,
    ValueTracker, VGroup, always_redraw, DOWN, UP,
)

from .palette import CLOUD, COLLAPSE, MUTED, TARGET


class HistogramDiagram:
    """A histogram whose visual state follows its samples and bin edges."""

    def __init__(self, samples, bin_edges, *, moving_index: int,
                 x_range=(-3, 3, 0.5), length: float = 9.4,
                 line_y: float = -1.55):
        self.samples = np.asarray(samples, dtype=float)
        self.bin_edges = np.asarray(bin_edges, dtype=float)
        self.moving_index = moving_index
        self.moving_x = ValueTracker(float(self.samples[moving_index]))

        self.number_line = NumberLine(
            x_range=x_range, length=length, include_numbers=False,
            numbers_to_include=np.arange(
                np.ceil(x_range[0]), np.floor(x_range[1]) + 1, 1),
            line_to_number_buff=0.38, include_tip=False,
        ).set_stroke(MUTED, 2)
        self.number_line.move_to([0.0, line_y, 0.0])

        self.fixed_dots = VGroup(*(
            Dot(self.number_line.n2p(value) + 0.20 * DOWN, radius=0.045)
            .set_fill(CLOUD, 0.9)
            for index, value in enumerate(self.samples)
            if index != self.moving_index
        ))
        self.moving_dot = always_redraw(lambda: Dot(
            self.number_line.n2p(self.moving_x.get_value()) + 0.20 * DOWN,
            radius=0.075,
        ).set_fill(TARGET, 1))

        self.bars = self._bars_for(self.samples, self.bin_edges)
        self.guides = self._guides_for(self.bin_edges)

    def current_samples(self) -> np.ndarray:
        values = self.samples.copy()
        values[self.moving_index] = self.moving_x.get_value()
        return values

    def _bars_for(self, values, bin_edges) -> VGroup:
        counts, _ = np.histogram(values, bins=bin_edges)
        bars = VGroup()
        baseline_y = self.number_line.n2p(0)[1]
        for left, right, count in zip(bin_edges[:-1], bin_edges[1:], counts):
            x0 = self.number_line.n2p(left)[0]
            x1 = self.number_line.n2p(right)[0]
            height = max(0.01, count * 0.23)
            bar = (
                Rectangle(width=0.94 * (x1 - x0), height=height)
                .set_fill(COLLAPSE, 0.55)
                .set_stroke(COLLAPSE, 1.5)
                # Anchor against the coordinate axis itself. NumberLine.get_y()
                # includes its labels and therefore sits below the actual line.
                .move_to([(x0 + x1) / 2, baseline_y, 0.0], DOWN)
            )
            if count == 0:
                bar.set_opacity(0)
            bars.add(bar)
        return bars

    def _guides_for(self, bin_edges) -> VGroup:
        return VGroup(*(
            DashedLine(
                self.number_line.n2p(edge),
                self.number_line.n2p(edge) + 3.0 * UP,
                dash_length=0.08,
            ).set_stroke(MUTED, 1, opacity=0.35)
            for edge in bin_edges[1:-1]
        ))

    def rebin(self, bin_edges) -> AnimationGroup:
        """Animate a bin-choice change without replacing the chart object."""
        new_edges = np.asarray(bin_edges, dtype=float)
        bars_target = self._bars_for(self.samples, new_edges)
        guides_target = self._guides_for(new_edges)
        self.bin_edges = new_edges
        return AnimationGroup(
            Transform(self.bars, bars_target),
            Transform(self.guides, guides_target),
            lag_ratio=0.0,
        )

    def follow_moving_sample(self) -> None:
        """Make the existing bars derive continuously from the sample state."""
        self.bars.add_updater(lambda bars: bars.become(
            self._bars_for(self.current_samples(), self.bin_edges)
        ))
        self.bars.update(0)
