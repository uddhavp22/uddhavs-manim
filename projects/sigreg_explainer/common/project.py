"""Projection geometry shared by Chapter C's cloud scenes.

C03 needs one fixed unit direction to own every representation of its shadow.
C04 needs the same relationships while the direction turns, which is what
`TurningProjection` adds. There is still no direction fan and no trace
framework here: C04 draws its score-vs-angle panel from `TurningProjection`'s
table using scene-local axes, because the *numbers* are what C05 and C07 will
reuse and the panel's layout is not.
"""

from __future__ import annotations

import numpy as np
from manim import Arrow, DashedLine, Dot, Line, VGroup, VMobject

from .cloud import CloudRig
from .layout import stack_levels
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


class TurningProjection:
    """One cloud projected onto a direction turning in the world x-y plane.

    `CloudProjectionRig` above is a snapshot: one fixed direction, numbers
    computed once, geometry built on demand. Here the direction is a single
    angle `ValueTracker` and every mobject is built ONCE and moved by an
    updater -- never `always_redraw`, for the reason `common/cloud.py`'s
    docstring records: an `always_redraw` hands the camera a new instance every
    frame, which silently drops its `add_fixed_orientation_mobjects`
    registration and lets a billboard tumble away with the camera.

    Every updater below moves points and touches nothing else -- no colour, no
    opacity. That is what makes a plain `FadeIn` a legitimate reveal for these
    objects, and it is exactly the property an `always_redraw` mobject lacks:
    there the per-frame rebuild resets the opacity the animation is driving, so
    the fade silently does nothing and the object pops (C03's phase 6).
    Reveal them while the angle is held still, so the points a `Transform`-family
    animation captured at `begin()` are the points the updater keeps writing.

    The scores are tabulated once, at construction, from the cloud's current
    geometry. Construct this AFTER the cloud has reached the shape being
    scored: `cloud.current_points()` is read here and the table is not
    recomputed.
    """

    def __init__(self, cloud: CloudRig, angle, *, lam: float, grid,
                 samples: int = 361, stack_min_dx: float = 0.105,
                 stack_step: float = 0.075, stack_max_level: int | None = None):
        self.cloud = cloud
        self.angle = angle
        self._lam = lam
        self._grid = grid
        self.stack_min_dx = float(stack_min_dx)
        self.stack_step = float(stack_step)
        # A ceiling on the dot plot's pile height, in levels.
        #
        # The dot plot is a display of shape, and it degenerates when the
        # shadow does: a projection that sends every sample to the same value
        # gives every sample its own level, so N points build a column N levels
        # tall. C05 turns through exactly that direction -- the anti-diagonal of
        # `Z = (X, X)`, where u^T Z is identically zero -- and an uncapped stack
        # sends 200 dots straight off the top of the frame, which reads as a
        # bug rather than as a collapse. Capping folds the excess back into the
        # top of the column, so a point mass draws as a short dense bar: the
        # honest picture of "every point in the same place", at a height the
        # rest of the turn already established as the pile's own maximum.
        self.stack_max_level = (
            None if stack_max_level is None else int(stack_max_level)
        )

        # A half turn is every distinct direction in the plane: u and -u give
        # the same shadow up to sign, and the statistic is symmetric in it.
        self.angles = np.linspace(0.0, np.pi, samples)

        # One evaluator, tabulated once. The live readout interpolates this,
        # the trace plots it, and a settled label reads an exact node -- so no
        # number on screen can come from a second evaluation of the same thing
        # (handoff section 11, "verify numerical displays").
        self.scores = np.array([
            epps_pulley(self.values_at(a), lam, grid) for a in self.angles
        ])

    # --- state ------------------------------------------------------------
    @staticmethod
    def direction_at(angle: float) -> np.ndarray:
        return np.array([np.cos(angle), np.sin(angle), 0.0])

    def direction(self) -> np.ndarray:
        return self.direction_at(self.angle.get_value())

    def values_at(self, angle: float) -> np.ndarray:
        """The scalar batch this direction produces, in data units.

        `CloudRig` stores display coordinates at `scale` world units per data
        unit; divide that visual scale back out before taking u^T z_i.
        """
        return (self.cloud.current_points() / self.cloud.scale) @ \
            self.direction_at(angle)

    def values(self) -> np.ndarray:
        return self.values_at(self.angle.get_value())

    def score_at(self, angle: float) -> float:
        """Exact score for one angle -- what a settled on-screen label reads."""
        return epps_pulley(self.values_at(angle), self._lam, self._grid)

    def score_now(self) -> float:
        """The live score, interpolated between table nodes."""
        return float(np.interp(
            self.angle.get_value(), self.angles, self.scores,
        ))

    # --- geometry, built once and moved by updaters ------------------------
    def shadow_positions(self) -> np.ndarray:
        """Feet on the projection line, stacked along the line's normal.

        220 feet drawn straight onto the line pile into one indistinguishable
        bar, which hides the only thing this scene claims -- that the shadow's
        shape changes. `layout.stack_levels` is the project's dot-plot rule;
        stacking along the normal rather than a fixed screen axis keeps the
        whole plot attached to the direction as it turns.
        """
        values = self.values()
        u = self.direction()
        normal = np.array([-u[1], u[0], 0.0])
        levels = np.array(
            stack_levels(values * self.cloud.scale, self.stack_min_dx),
            dtype=float,
        )
        if self.stack_max_level is not None:
            levels = np.minimum(levels, float(self.stack_max_level))
        return (
            values[:, None] * self.cloud.scale * u[None, :]
            + levels[:, None] * self.stack_step * normal[None, :]
        )

    def shadow_dots(self, radius: float = 0.032) -> VGroup:
        dots = VGroup(*(
            Dot(point, radius=radius).set_fill(DIRECTION, 0.96)
            for point in self.shadow_positions()
        ))

        def move_shadow(group):
            for dot, point in zip(group, self.shadow_positions()):
                dot.move_to(point)

        dots.add_updater(move_shadow)
        return dots

    def direction_arrow(self) -> Arrow:
        # One tick of the visible axes, matching CloudProjectionRig: the arrow
        # is the unit vector, and `cloud.scale` is the cloud's spread, not the
        # axes' unit length.
        arrow = Arrow(
            self.cloud.axes.c2p(0.0, 0.0, 0.0),
            self.cloud.axes.c2p(*self.direction()),
            buff=0.0,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.2,
        ).set_color(DIRECTION)

        def turn_arrow(mob):
            mob.put_start_and_end_on(
                self.cloud.axes.c2p(0.0, 0.0, 0.0),
                self.cloud.axes.c2p(*self.direction()),
            )

        arrow.add_updater(turn_arrow)
        return arrow

    def projection_line(self, half_length: float | None = None) -> Line:
        if half_length is None:
            # Long enough for the widest shadow the turn ever produces, so the
            # line never has to grow mid-sweep: the extreme foot lies at the
            # in-plane radius of the furthest point.
            planar = self.cloud.current_points()[:, :2]
            half_length = float(np.max(np.linalg.norm(planar, axis=1))) + 0.3
        half_length = float(half_length)
        u = self.direction()
        line = Line(-half_length * u, half_length * u)
        line.set_stroke(DIRECTION, 1.8, opacity=0.36)

        def turn_line(mob):
            now = self.direction()
            mob.put_start_and_end_on(-half_length * now, half_length * now)

        line.add_updater(turn_line)
        return line

    def head_dot(self, axes, radius: float = 0.055) -> Dot:
        """The point of the score-vs-angle trace at the current angle."""
        dot = Dot(radius=radius).set_fill(DIRECTION, 1.0)

        def follow(mob):
            mob.move_to(axes.c2p(
                np.degrees(self.angle.get_value()), self.score_now(),
            ))

        follow(dot)
        dot.add_updater(follow)
        return dot

    def trace(self, axes, width: float = 3.2):
        """The score-vs-angle curve, drawn as far as the angle has turned.

        The fill is pinned off. A bare `VMobject` carries a fill colour, and
        `set_opacity` -- the obvious way to reveal it -- raises fill and stroke
        together, which paints the whole area under the curve solid white.
        Reveal this by animating `set_stroke(opacity=...)` instead.
        """
        curve = VMobject().set_stroke(DIRECTION, width).set_fill(opacity=0.0)

        def draw(mob):
            now = self.angle.get_value()
            keep = self.angles <= now
            xs = np.degrees(self.angles[keep])
            ys = self.scores[keep]
            points = [axes.c2p(x, y) for x, y in zip(xs, ys)]
            points.append(axes.c2p(np.degrees(now), self.score_now()))
            if len(points) < 2:                 # a curve needs two corners
                points = points * 2
            mob.set_points_as_corners(points)

        draw(curve)
        curve.add_updater(draw)
        return curve
