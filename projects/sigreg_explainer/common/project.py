"""Projection geometry shared by Chapter C's cloud scenes.

C03 needs one fixed unit direction to own every representation of its shadow.
The later rotating-direction scenes can extend this state when they are built;
this first contract deliberately contains no direction fan or trace framework.
"""

from __future__ import annotations

import numpy as np
from manim import Arrow, DashedLine, Dot, Line, VGroup

from .cloud import CloudRig
from .palette import DIRECTION, MUTED
from .score import epps_pulley


class CloudProjectionRig:
    """One cloud projected onto one explicit unit-vector state."""

    def __init__(self, cloud: CloudRig, direction, *, lam: float, grid):
        self.cloud = cloud
        direction = np.asarray(direction, dtype=float)
        if direction.shape != (3,):
            raise ValueError("direction must have shape (3,)")
        norm = float(np.linalg.norm(direction))
        if norm == 0.0:
            raise ValueError("direction must be nonzero")

        # The sole direction state. Every object and number below is derived
        # from this normalized vector, never animated or evaluated separately.
        self.direction = np.array(direction / norm, copy=True)
        self.direction.setflags(write=False)

        # CloudRig stores display coordinates at `scale` world units per data
        # unit. Divide that visual scale back out before taking u^T z_i; the
        # scalar batch is mathematical data, not camera geometry.
        samples = cloud.current_points() / cloud.scale
        self.projected_values = np.asarray(
            samples @ self.direction,
            dtype=float,
        )
        self.projected_values.setflags(write=False)
        self.score_value = epps_pulley(self.projected_values, lam, grid)

    def shadow_points(self) -> np.ndarray:
        """Feet of the cloud points on the projection line, in world units."""
        return (
            self.projected_values[:, None]
            * self.cloud.scale
            * self.direction[None, :]
        )

    def direction_arrow(self) -> Arrow:
        # Draw the normalized vector at exactly one tick of the visible axes.
        # `cloud.scale` controls the sample cloud's standard deviation and is
        # not the axes' unit length, so using it here made a mathematically
        # normalized vector look longer than one unit on screen.
        origin = self.cloud.axes.c2p(0.0, 0.0, 0.0)
        tip = self.cloud.axes.c2p(*self.direction)
        return Arrow(
            origin,
            tip,
            buff=0.0,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.2,
        ).set_color(DIRECTION)

    def direction_tip(self) -> np.ndarray:
        """Visible endpoint of the exact one-axis-unit direction glyph."""
        return self.cloud.axes.c2p(*self.direction)

    def projection_line(self) -> Line:
        half_length = max(
            3.25,
            float(np.max(np.abs(self.projected_values))) * self.cloud.scale
            + 0.22,
        )
        return Line(
            -half_length * self.direction,
            half_length * self.direction,
        ).set_stroke(DIRECTION, 1.8, opacity=0.36)

    def guide_lines(self) -> VGroup:
        """Dashed point-to-foot guides, MUTED per the chapter's colour table

        (storyboard §4/C03) -- DIRECTION is reserved for u, its line, the
        shadow dots, and the score, so the guides must not compete with them.
        """
        return VGroup(*(
            DashedLine(start, end, dash_length=0.055)
            .set_stroke(MUTED, 1.15, opacity=0.35)
            for start, end in zip(
                self.cloud.current_points(),
                self.shadow_points(),
            )
        ))

    def shadow_dots(self, radius: float = 0.035) -> VGroup:
        return VGroup(*(
            Dot(point, radius=radius).set_fill(DIRECTION, 0.96)
            for point in self.shadow_points()
        ))

    def score(self) -> float:
        """The score of the exact array positioning ``shadow_dots``."""
        return self.score_value
