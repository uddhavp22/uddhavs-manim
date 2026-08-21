"""Chapter C.05 — coordinate checks can miss a bad joint cloud.

The scene has one job: make the failure of a tempting shortcut obvious.  For
Z=(X,X), each coordinate is a standard-Gaussian scalar batch, yet the joint
cloud has collapsed onto a line.  Looking only at x and y therefore misses the
dependence between them; one mixed direction exposes it immediately.

Render:
    SIGREG_VOICE=eleven ./render.sh \
        projects/sigreg_explainer/chapterC/c05_gaussian_marginals.py C05
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data
from common.beat import ActScene
from common.cloud import CloudRig
from common.palette import AXIS, CLOUD, COLLAPSE, DIRECTION, GRID, INK, MUTED, TARGET
from common.project import TurningProjection
from common.score import EP_GRID, EP_LAMBDA
from common import type as ty


FIRST_AXIS = 0.0
SECOND_AXIS = np.pi / 2
COLLAPSED = 3 * np.pi / 4

# The plane occupies the left two-thirds of the frame; the checks it produces
# sit to its right.  The camera remains locked in a genuinely two-dimensional
# view, so turning u is mathematical motion rather than camera decoration.
CAMERA_CENTRE = np.array([1.175, 0.0, 0.0])
SCALE = 0.78
DOT_RADIUS = 0.033
STACK_MIN_DX = 0.085
STACK_STEP = 0.058
STACK_MAX_LEVEL = 15
LINE_HALF_LENGTH = 3.30
ARROW_UNITS = 2.0


def _framed(x: float, y: float) -> np.ndarray:
    """A fixed-frame point that lands at screen coordinate ``(x, y)``."""
    return np.array([x, y, 0.0]) + CAMERA_CENTRE


def _score_row(symbol: str, value: float, verdict: str, colour: str):
    """Keep the tested scalar and its score explicit in the same row."""
    score = ty.maths(
        Rf"\operatorname{{score}}({symbol})={value:.3f}",
        size=ty.EQ,
        color=colour,
    )
    meaning = ty.words(verdict, size=ty.LABEL, color=colour)
    return VGroup(score, meaning).arrange(
        RIGHT, aligned_edge=DOWN, buff=0.26,
    )


class C05(ActScene, ThreeDScene):
    """Show why two passing coordinate shadows are not a joint test."""

    def construct(self):
        self.set_camera_orientation(
            phi=0.0, theta=-90 * DEGREES, frame_center=CAMERA_CENTRE,
        )

        sample = data.diagonal_2d()
        points = np.column_stack([sample, np.zeros(len(sample))])
        angle = ValueTracker(FIRST_AXIS)
        cloud = CloudRig(
            points, scale=SCALE, dot_colour=CLOUD, dot_radius=DOT_RADIUS,
        )

        # TurningProjection's arrow measures the visible axes, even though the
        # NumberPlane is the actual drawn coordinate system.  Align its hidden
        # axes' zeros first, then make one arrow unit equal one grid square.
        for axis in cloud.axes.axes:
            axis.shift(-axis.number_to_point(0))
        cloud.axes.scale(
            ARROW_UNITS * SCALE / (
                cloud.axes.x_axis.number_to_point(1)[0]
                - cloud.axes.x_axis.number_to_point(0)[0]
            ),
            about_point=ORIGIN,
        )

        plane = NumberPlane(
            x_range=(-3, 3, 1), y_range=(-3, 3, 1),
            x_length=6 * SCALE, y_length=6 * SCALE,
            background_line_style={
                "stroke_color": GRID, "stroke_width": 1.0,
                "stroke_opacity": 0.9,
            },
            axis_config={"stroke_color": AXIS, "stroke_width": 1.8,
                         "include_ticks": False},
        )
        self.add(plane)
        cloud.mount(self, axes=False, ellipsoid=False)
        for dot in cloud.dots:
            dot.set_opacity(0.88)

        # The geometry is visible before the test begins.  This is the
        # counterexample, not a later surprise: the viewer can see from frame
        # one that a line is not the round two-dimensional target cloud.
        diagonal_label = ty.maths(R"y=x", size=ty.EQ_DISPLAY, color=MUTED)
        diagonal_label.move_to(_framed(-3.45, 2.62))
        self.add_fixed_in_frame_mobjects(diagonal_label)

        projection = TurningProjection(
            cloud, angle, lam=EP_LAMBDA, grid=EP_GRID,
            stack_min_dx=STACK_MIN_DX, stack_step=STACK_STEP,
            stack_max_level=STACK_MAX_LEVEL,
        )
        arrow = projection.direction_arrow()
        line = projection.projection_line(half_length=LINE_HALF_LENGTH)
        self.add(line)
        self.add(arrow)
        for mob in (arrow, line):
            mob.set_opacity(0.0)

        # A projected point first lands at its literal perpendicular foot.
        # Only after that correspondence is established do the dots spread
        # normally into the project's readable one-dimensional dot plot.
        def foot_positions() -> np.ndarray:
            values = projection.values()
            direction = projection.direction()
            return values[:, None] * SCALE * direction[None, :]

        feet = foot_positions()
        shadow = VGroup(*(
            Dot(point, radius=DOT_RADIUS).set_fill(DIRECTION, 0.96)
            for point in feet
        ))
        stack_mix = ValueTracker(0.0)

        def move_shadow(group):
            mix = stack_mix.get_value()
            positions = (
                (1.0 - mix) * foot_positions()
                + mix * projection.shadow_positions()
            )
            for dot, point in zip(group, positions):
                dot.move_to(point)

        guide_indices = np.linspace(
            0, len(cloud.dots) - 1, 32, dtype=int,
        )
        guides = VGroup(*(
            DashedLine(
                cloud.current_points()[index], feet[index], dash_length=0.055,
            ).set_stroke(MUTED, 1.15, opacity=0.42)
            for index in guide_indices
        ))

        # One target curve survives every change of direction.  Its updater
        # changes only points, so opacity animation remains well-defined.
        target = VMobject().set_stroke(TARGET, 2.5).set_fill(opacity=0.0)
        target_xs = np.linspace(-3.0, 3.0, 151)
        target_edge = np.exp(-0.5 * 3.0 ** 2)
        target_height = (STACK_MAX_LEVEL + 1) * STACK_STEP

        def move_target(mob):
            direction = projection.direction()
            normal = np.array([-direction[1], direction[0], 0.0])
            heights = target_height * (
                np.exp(-0.5 * target_xs ** 2) - target_edge
            ) / (1.0 - target_edge)
            points_now = (
                target_xs[:, None] * SCALE * direction[None, :]
                + heights[:, None] * normal[None, :]
            )
            mob.set_points_smoothly(points_now)

        move_target(target)
        target.add_updater(move_target)
        target.set_stroke(opacity=0.0)
        self.add(target)
        zero_ring = Circle(radius=0.14).set_stroke(DIRECTION, 3.0, opacity=0.0)
        zero_ring.move_to(ORIGIN)
        self.add(zero_ring)

        x_score = projection.score_at(FIRST_AXIS)
        y_score = projection.score_at(SECOND_AXIS)
        collapsed_score = projection.score_at(COLLAPSED)
        x_row = _score_row("x", x_score, "low", DIRECTION)
        y_row = _score_row("y", y_score, "same low score", DIRECTION)
        axis_results = VGroup(x_row, y_row).arrange(
            DOWN, aligned_edge=LEFT, buff=0.30,
        ).move_to(_framed(3.62, 1.90))
        mixed_row = _score_row("u", collapsed_score, "all at zero", COLLAPSE)
        mixed_row.move_to(_framed(3.62, 0.35))
        self.add_fixed_in_frame_mobjects(axis_results, mixed_row)
        x_row.set_opacity(0.0)
        y_row.set_opacity(0.0)
        mixed_row.set_opacity(0.0)

        # --- project onto x before calling it a coordinate check ----------
        with self.voiceover(
            text="One direction wasn't enough, so a natural shortcut is to "
                 "try the two coordinate axes. <bookmark mark='x_drop'/>Start "
                 "with the horizontal coordinate: project every point straight "
                 "onto that axis. <bookmark mark='x_stack'/>Those projected "
                 "values line up closely with the standard bell, so its score "
                 "is low."
        ) as tracker:
            self.play(
                Indicate(plane.get_x_axis(), color=DIRECTION, scale_factor=1.03),
                Indicate(plane.get_y_axis(), color=DIRECTION, scale_factor=1.03),
                run_time=max(0.8, tracker.time_until_bookmark("x_drop")),
            )
            self.wait_until_bookmark("x_drop")
            self.play(
                AnimationGroup(
                    arrow.animate.set_opacity(1.0),
                    line.animate.set_opacity(0.36),
                    LaggedStart(
                        *(Create(guide) for guide in guides),
                        lag_ratio=0.012,
                    ),
                    TransformFromCopy(cloud.dots, shadow),
                    *(dot.animate.set_opacity(0.34) for dot in cloud.dots),
                    lag_ratio=0.0,
                ),
                run_time=max(1.4, tracker.time_until_bookmark("x_stack")),
                rate_func=smooth,
            )
            self.add_fixed_orientation_mobjects(*shadow)
            self.add(shadow)
            shadow.add_updater(move_shadow)
            shadow.update(0)
            self.wait_until_bookmark("x_stack")
            self.across(
                tracker,
                AnimationGroup(
                    stack_mix.animate.set_value(1.0),
                    FadeOut(guides),
                    target.animate.set_stroke(opacity=0.92),
                    x_row.animate.set_opacity(1.0),
                    lag_ratio=0.0,
                ),
                floor=1.4,
                rate_func=smooth,
            )

        # --- rotate the same apparatus onto y -----------------------------
        with self.voiceover(
            text="Now <bookmark mark='y_turn'/>turn the same projection onto "
                 "the vertical axis. <bookmark mark='y_settle'/>Nothing "
                 "changes, because each vertical coordinate copies its "
                 "horizontal partner. It is the same batch, with the same low "
                 "score."
        ) as tracker:
            self.wait_until_bookmark("y_turn")
            self.play(
                angle.animate.set_value(SECOND_AXIS),
                run_time=max(1.8, tracker.time_until_bookmark("y_settle")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("y_settle")
            self.across(
                tracker,
                y_row.animate.set_opacity(1.0),
                floor=1.0,
            )

        # --- one mixed direction exposes the dependence ------------------
        with self.voiceover(
            text="But those two checks never compare the coordinates. "
                 "<bookmark mark='mix'/>So turn the line forty-five degrees, "
                 "toward the diagonal that subtracts one from the other. "
                 "<bookmark mark='zero'/>Since the coordinates are equal, every "
                 "projection lands at zero. <bookmark mark='verdict'/>Both "
                 "coordinate scores were low while the cloud still lay on a "
                 "line. The axes miss this dependence, so we have to test "
                 "directions that mix the coordinates."
        ) as tracker:
            self.play(
                axis_results.animate.set_opacity(0.48),
                *(dot.animate.set_opacity(0.76) for dot in cloud.dots),
                run_time=max(0.8, tracker.time_until_bookmark("mix")),
            )
            self.wait_until_bookmark("mix")
            self.play(
                angle.animate.set_value(COLLAPSED),
                run_time=max(1.5, tracker.time_until_bookmark("zero")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("zero")
            self.play(
                stack_mix.animate.set_value(0.0),
                mixed_row.animate.set_opacity(1.0),
                zero_ring.animate.set_stroke(opacity=1.0),
                *(dot.animate.set_opacity(0.28) for dot in cloud.dots),
                run_time=max(0.9, tracker.time_until_bookmark("verdict")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("verdict")
            self.across(
                tracker,
                AnimationGroup(
                    FadeOut(arrow), FadeOut(line), FadeOut(shadow),
                    target.animate.set_stroke(opacity=0.0),
                    zero_ring.animate.set_stroke(opacity=0.0),
                    FadeOut(axis_results), FadeOut(mixed_row),
                    *(dot.animate.set_opacity(0.88) for dot in cloud.dots),
                    diagonal_label.animate.set_color(INK),
                    lag_ratio=0.0,
                ),
                floor=1.5,
            )

        self.freeze(arrow, line, shadow, target, zero_ring)
        self.remove_fixed_in_frame_mobjects(axis_results, mixed_row)
        cloud.freeze()
        self.settle_frame()
