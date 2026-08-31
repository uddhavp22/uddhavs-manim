"""A static 2-D counterpart to sigreg_explainer's ``CloudProjectionRig``.

Chapter C's projection rig lives in a ``ThreeDScene`` and drives a turning
``ValueTracker``.  LeNEPA's temporal-SIGReg scene needs the same *picture* --
cloud, direction, shadow, score -- inside a plain 2-D scene, at one fixed
direction per instance (no updaters).  Reusing ``CloudProjectionRig``'s
method names, rather than inventing a new vocabulary, keeps the two chapters
reading as one visual grammar even though nothing else is shared code.

The direction arrow is drawn unlabeled on purpose: the SIGReg chapter already
calls the projection direction ``u``, and LeNEPA calls its tokens ``u`` too --
a label here would collide with that established meaning rather than
reinforce it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import Arrow, DashedLine, Line, ParametricFunction, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from projects.sigreg_explainer.common.layout import stack_levels
from projects.sigreg_explainer.common.score import EP_GRID, EP_LAMBDA, epps_pulley

from .palette import MUTED, SIGREG
from .visuals import scalar_dot


class PlaneProjectionRig:
    """One set of latent points, projected onto one fixed direction.

    ``values``: (N, 2) latent coordinates, in *data* units (i.e. already
    passed through ``common/data.py::latent``).  ``origin``: (3,) world
    point.  ``scale``: world units per data unit.  ``direction``: (2,)
    nonzero vector, normalized internally.
    """

    def __init__(self, values, *, origin, scale: float, direction,
                 line_offset: float = 0.0,
                 lam: float = EP_LAMBDA, grid=EP_GRID):
        self.values = np.asarray(values, dtype=float)
        self.origin = np.asarray(origin, dtype=float)
        self.scale = float(scale)
        direction = np.asarray(direction, dtype=float)
        norm = float(np.linalg.norm(direction))
        if norm == 0.0:
            raise ValueError("direction must be nonzero")
        self.direction = direction / norm
        self._direction3 = np.array([self.direction[0], self.direction[1], 0.0])
        self._normal3 = np.array([-self.direction[1], self.direction[0], 0.0])
        # Slide the readout axis along its own normal.  A projection is
        # constant along that normal, so every foot keeps the coordinate it
        # had -- this moves where the line is *drawn*, not what it measures,
        # and the guide lines stay exactly perpendicular to it.  Without it
        # the line has to run through the middle of the cloud, where a stack
        # of coincident shadows collides with the points casting them.
        self.line_offset = float(line_offset)
        self._offset3 = self.line_offset * self._normal3

        self._projected = self.values @ self.direction
        self._score = epps_pulley(self._projected, lam, grid)

    def world_points(self) -> np.ndarray:
        pts = np.zeros((len(self.values), 3))
        pts[:, :2] = self.values * self.scale
        return pts + self.origin[None, :]

    def projected_values(self) -> np.ndarray:
        return self._projected

    def _line_origin(self) -> np.ndarray:
        return self.origin + self._offset3

    def _feet(self) -> np.ndarray:
        """Unstacked feet, exactly on the projection line."""
        return (
            self._line_origin()[None, :]
            + (self._projected * self.scale)[:, None] * self._direction3[None, :]
        )

    def foot_points(self) -> np.ndarray:
        """Where each value lands on the line, before dot-plot stacking.

        The honest source for "how far does this subset spread along the
        direction": the bounding box of the drawn shadow *dots* is inflated by
        one dot diameter, which turns a genuinely zero spread into a visible
        box and makes a degenerate case look like a small measurement instead
        of no measurement at all.
        """
        return self._feet()

    def shadow_points(self, *, stack_min_dx: float = 0.13,
                       stack_step: float = 0.11) -> np.ndarray:
        levels = np.array(
            stack_levels(self._projected * self.scale, stack_min_dx),
            dtype=float,
        )
        return self._feet() + levels[:, None] * stack_step * self._normal3[None, :]

    def direction_arrow(self, *, color: str = SIGREG, length: float = 1.0,
                        at: float | None = None) -> Arrow:
        """The unit direction, by default drawn from the line's own origin.

        ``at`` places its tail at a given projected coordinate along the line
        instead, so the arrow can start clear of the shadows rather than in
        the middle of them.
        """
        tail = self._line_origin()
        if at is not None:
            tail = tail + at * self.scale * self._direction3
        return Arrow(
            tail,
            tail + length * self._direction3,
            buff=0.0,
            stroke_width=4.5,
            max_tip_length_to_length_ratio=0.22,
        ).set_color(color)

    def projection_line(self, *, color: str = SIGREG,
                        pad: float = 0.30) -> Line:
        half_length = max(
            1.3, float(np.max(np.abs(self._projected))) * self.scale + pad,
        )
        origin = self._line_origin()
        return Line(
            origin - half_length * self._direction3,
            origin + half_length * self._direction3,
        ).set_stroke(color, 1.8, opacity=0.40)

    def guide_lines(self, *, color: str = MUTED) -> VGroup:
        return VGroup(*(
            DashedLine(start, end, dash_length=0.06)
            .set_stroke(color, 1.15, opacity=0.40)
            for start, end in zip(self.world_points(), self._feet())
        ))

    def shadow_dots(self, *, radius: float = 0.055, color: str = SIGREG) -> VGroup:
        return VGroup(*(
            scalar_dot(color, radius=radius).move_to(point)
            for point in self.shadow_points()
        ))

    def target_bell(self, *, height: float = 0.55, gap: float = 0.45,
                     color: str = MUTED) -> ParametricFunction:
        """A standard-normal density silhouette, offset beside the line.

        ``gap`` pushes the whole curve a fixed distance off the line before
        the density bulge starts, so it reads as a reference sitting beside
        the axis rather than a stroke crossing through the projected points.
        """
        def point(x: float) -> np.ndarray:
            density = np.exp(-x * x / 2.0)
            return (
                self._line_origin()
                + x * self.scale * self._direction3
                + (gap + height * density) * self._normal3
            )

        curve = ParametricFunction(point, t_range=(-3.0, 3.0, 0.05))
        curve.set_stroke(color, 1.6, opacity=0.45)
        return curve

    def score(self) -> float:
        return self._score
