"""Chapter C.06 — every direction produces a batch, and all batches identify the cloud.

The scene picks up directly from C05 and lets the wheel of shadows build while
`u` turns. One already-visible shadow's characteristic function is derived as
a radial slice through the cloud's own. A height-to-brightness legend then
moves that slice onto its ray, and sweeping `u` fills the Gaussian frequency
field before a ring cloud is compared through its shadows, curve, and signed
field. Their fields meet only when the clouds do, leading into Fourier
uniqueness and Cramér--Wold.

2026-08-24 revision: the radial slice becomes the shared comparison object for
a Gaussian cloud and a same-moments ring. The ring is built from copies of the
Gaussian points, then a single mixture tracker brings its points, shadow, and
population characteristic function back into agreement. C06 ends on the
Cramér--Wold payoff; the former continuum-of-directions
training narration is reserved for the opening of a future C07. C07 does not
exist yet, so the line is parked here verbatim rather than lost:

    "But in training, there is a continuum of possible directions, and we
    cannot compute all of them. So the loss needs a finite sample -- one that
    does not just settle for the convenient directions, like the coordinate
    axes."

It closed C06 until this revision; it belongs at the top of C07 because this
scene now ends on what Cramér--Wold buys, and that is the claim C07 pushes
back on.

Render:
    SIGREG_VOICE=eleven ./render.sh \
        projects/sigreg_explainer/chapterC/c06_every_direction.py C06 -qh
"""

import os
import sys

import numpy as np
from manim import *
from scipy.special import j0

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.cloud import CloudRig
from common.palette import (
    AXIS, CLOUD, COLLAPSE, DIRECTION, GRID, INK, MAGNITUDE, MUTED,
    RIVAL, TARGET,
)
from common import type as ty
from common.wrap import gaussian_cf


SCALE = 0.78
DOT_RADIUS = 0.033
COLLAPSED_DIRECTION = 3 * np.pi / 4

WHEEL_RADIUS = 2.86
SPOKE_RADIUS = 2.58
ACTIVE_ARROW_LENGTH = 1.55
ACTIVE_LINE_HALF_LENGTH = 2.56
N_SPOKES = 16
N_SHADOWS = 8

# The converse beat re-reads the wheel as frequency space: angle is u, radius
# is t. CF_T_MAX sets how far out that reading runs (gaussian_cf(4) ~ 3e-4, so
# the field has already decayed to nothing well inside SPOKE_RADIUS).
CF_T_MAX = 4.0
N_RAY_SEGMENTS = 16
N_SWEEP_RAYS = 48
FIELD_GRID = 384
FIELD_PROFILE_SAMPLES = 4096
FIELD_EDGE = 0.06
FIELD_GAMMA = 0.7
MINI_HALF_WIDTH = 0.72
MINI_X_SCALE = 0.18
MINI_STACK_STEP = 0.035
MINI_STACK_MAX = 7
MINI_DOT_RADIUS = 0.018
MINI_SAMPLE_COUNT = 36
COMPARISON_SCALE = 0.62
COMPARISON_LEFT = np.array([-4.85, 0.35, 0.0])
COMPARISON_RIGHT = np.array([4.85, 0.35, 0.0])
COMPARISON_AXES_CENTRE = np.array([0.0, -0.10, 0.0])
COMPARISON_FIELD_DIAMETER = 2.5
COMPARISON_FIELD_SCALE = COMPARISON_FIELD_DIAMETER / (2 * SPOKE_RADIUS)
MIX_WINDOW = 0.05


def _standardized_isotropic_points(n: int) -> np.ndarray:
    points = data.whiten(data.gaussian_2d(n=n))
    return np.column_stack([points, np.zeros(n)])


def hexrgb(value: str) -> np.ndarray:
    value = value.lstrip("#")
    return np.array(
        [int(value[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.uint8,
    )


def _field_lookup() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Index a fine radial profile into the square texture once, not per frame."""
    coords = np.linspace(-CF_T_MAX, CF_T_MAX, FIELD_GRID)
    x_grid, y_grid = np.meshgrid(coords, -coords)
    radius = np.hypot(x_grid, y_grid)
    profile_r = np.linspace(0.0, CF_T_MAX, FIELD_PROFILE_SAMPLES)
    indices = np.clip(
        np.rint(radius / CF_T_MAX * (FIELD_PROFILE_SAMPLES - 1)),
        0,
        FIELD_PROFILE_SAMPLES - 1,
    ).astype(np.int32)

    # The alpha, rather than RGB, goes smoothly to zero at the disc edge;
    # otherwise the bitmap announces itself as a black square over the scene.
    radial_fraction = radius / CF_T_MAX
    mask = np.clip((1.0 - radial_fraction) / FIELD_EDGE, 0.0, 1.0)
    mask = mask * mask * (3.0 - 2.0 * mask)
    return profile_r, indices, mask


FIELD_RADII, FIELD_INDICES, FIELD_MASK = _field_lookup()
GAUSSIAN_PROFILE = np.exp(-0.5 * FIELD_RADII ** 2)
RING_PROFILE = j0(np.sqrt(2.0) * FIELD_RADII)


def _field_alpha(signed_profile: np.ndarray) -> np.ndarray:
    values = np.clip(signed_profile[FIELD_INDICES], 0.0, 1.0)
    alpha = np.clip(values, 0.0, 1.0) ** FIELD_GAMMA * FIELD_MASK
    return np.rint(255.0 * alpha).astype(np.uint8)


def _field_image(signed_profile: np.ndarray, colour: str) -> ImageMobject:
    rgba = np.zeros((FIELD_GRID, FIELD_GRID, 4), dtype=np.uint8)
    rgba[..., :3] = hexrgb(colour)
    rgba[..., 3] = _field_alpha(signed_profile)
    image = ImageMobject(rgba)
    image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    image.height = 2 * SPOKE_RADIUS
    image.set_z_index(-1)
    return image


class C06(ActScene, ThreeDScene):
    """Make the collection of all shadows the scene's single visual idea."""

    def construct(self):
        self.set_camera_orientation(
            phi=0.0,
            theta=-90 * DEGREES,
            frame_center=ORIGIN,
        )

        diagonal = data.diagonal_2d()
        diagonal_points = np.column_stack([
            diagonal, np.zeros(len(diagonal)),
        ])
        gaussian_points = _standardized_isotropic_points(len(diagonal_points))
        cloud = CloudRig(
            diagonal_points,
            scale=SCALE,
            dot_colour=CLOUD,
            dot_radius=DOT_RADIUS,
        )
        plane = NumberPlane(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            x_length=6 * SCALE,
            y_length=6 * SCALE,
            background_line_style={
                "stroke_color": GRID,
                "stroke_width": 1.0,
                "stroke_opacity": 0.9,
            },
            axis_config={
                "stroke_color": AXIS,
                "stroke_width": 1.8,
                "include_ticks": False,
            },
        )
        plane.set_opacity(0.0)
        self.add(plane)
        cloud.mount(self, axes=False, ellipsoid=False)
        for dot in cloud.dots:
            dot.set_opacity(0.0)

        diagonal_label = ty.maths(R"y=x", size=ty.EQ_DISPLAY, color=INK)
        diagonal_label.move_to(3.8 * LEFT + 2.6 * UP)
        diagonal_label.set_opacity(0.0)
        self.add(diagonal_label)

        angle = ValueTracker(COLLAPSED_DIRECTION)

        def direction() -> np.ndarray:
            a = angle.get_value()
            return np.array([np.cos(a), np.sin(a), 0.0])

        active_line = Line(LEFT, RIGHT).set_stroke(
            DIRECTION, 2.0, opacity=0.0,
        )

        def turn_active_line(mob):
            u = direction()
            mob.put_start_and_end_on(
                -ACTIVE_LINE_HALF_LENGTH * u,
                ACTIVE_LINE_HALF_LENGTH * u,
            )

        active_line.add_updater(turn_active_line)
        active_arrow = Arrow(
            ORIGIN,
            ACTIVE_ARROW_LENGTH * direction(),
            buff=0.0,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.18,
        ).set_color(DIRECTION).set_opacity(0.0)

        def turn_active_arrow(mob):
            mob.put_start_and_end_on(
                ORIGIN,
                ACTIVE_ARROW_LENGTH * direction(),
            )

        active_arrow.add_updater(turn_active_arrow)
        active_label = ty.maths("u", size=ty.EQ, color=DIRECTION)

        def move_active_label(mob):
            u = direction()
            normal = np.array([-u[1], u[0], 0.0])
            mob.move_to(ACTIVE_ARROW_LENGTH * u + 0.20 * normal)

        move_active_label(active_label)
        active_label.add_updater(move_active_label)
        active_label.set_opacity(0.0)
        self.add(active_line, active_arrow, active_label)

        wheel_ring = Circle(radius=WHEEL_RADIUS).set_stroke(
            GRID, 1.5, opacity=0.0,
        )
        spoke_angles = (
            COLLAPSED_DIRECTION
            + np.linspace(0.0, np.pi, N_SPOKES, endpoint=False)
        )
        spokes = VGroup(*(
            Line(
                -SPOKE_RADIUS * np.array([np.cos(a), np.sin(a), 0.0]),
                SPOKE_RADIUS * np.array([np.cos(a), np.sin(a), 0.0]),
            ).set_stroke(DIRECTION, 1.1, opacity=0.0)
            for a in spoke_angles
        ))
        self.add(wheel_ring, spokes)

        # Each small plot is a snapshot of one directional projection.  The
        # baseline is tangent to the wheel and density grows radially outward,
        # so the eight plots read as one family rather than detached charts.
        shadow_angles = np.deg2rad(45 * np.arange(N_SHADOWS))
        shadow_indices = np.linspace(
            0, len(cloud.dots) - 1, MINI_SAMPLE_COUNT, dtype=int,
        )
        shadow_plots = VGroup()
        shadow_baselines = VGroup()
        shadow_dot_groups: list[VGroup] = []
        target_curves = VGroup()

        for shadow_angle in shadow_angles:
            radial = np.array([
                np.cos(shadow_angle), np.sin(shadow_angle), 0.0,
            ])
            tangent = np.array([-radial[1], radial[0], 0.0])
            centre = WHEEL_RADIUS * radial
            baseline = Line(
                centre - MINI_HALF_WIDTH * tangent,
                centre + MINI_HALF_WIDTH * tangent,
            ).set_stroke(AXIS, 1.1, opacity=0.60)
            shadow_baselines.add(baseline)

            dots = VGroup(*(
                Dot(radius=MINI_DOT_RADIUS).set_fill(DIRECTION, 0.90)
                for _ in shadow_indices
            ))

            def move_shadow(group, u=radial, along=tangent, out=radial,
                            anchor=centre):
                values = (
                    cloud.current_points()[shadow_indices] / SCALE
                ) @ u
                positions = values * MINI_X_SCALE
                levels = np.minimum(
                    np.asarray(
                        layout.stack_levels(positions, 0.046),
                        dtype=float,
                    ),
                    MINI_STACK_MAX,
                )
                for dot, position, level in zip(group, positions, levels):
                    dot.move_to(
                        anchor
                        + float(position) * along
                        + (level + 0.75) * MINI_STACK_STEP * out
                    )

            move_shadow(dots)
            dots.add_updater(move_shadow)
            shadow_dot_groups.append(dots)

            target = VMobject().set_stroke(
                TARGET, 2.0, opacity=0.0,
            ).set_fill(opacity=0.0)
            target_xs = np.linspace(-3.2, 3.2, 121)
            target_edge = np.exp(-0.5 * 3.2 ** 2)
            target.set_points_smoothly([
                centre
                + x * MINI_X_SCALE * tangent
                + 0.33
                * (np.exp(-0.5 * x * x) - target_edge)
                / (1.0 - target_edge)
                * radial
                for x in target_xs
            ])
            target_curves.add(target)

            plot = VGroup(baseline, dots, target)
            shadow_plots.add(plot)

        # --- pick up directly from C05: turn u, let the wheel build ---------
        # No recall of C02's failed matching (spent) or C03/C04's projection
        # mechanics (spent, twice): the viewer already knows what u^T z means.
        with self.voiceover(
            text="<bookmark mark='turn'/>Keep turning the direction u. "
                 "<bookmark mark='fill'/>Every new angle gives us another "
                 "shadow of the same cloud, and every shadow has its own "
                 "characteristic function. So if we let u go all the way "
                 "around, we get one characteristic function for every "
                 "direction there is. <bookmark mark='ask'/>One direction "
                 "was enough to catch this cloud lying on a line. Does the "
                 "whole family pin the cloud down completely?"
        ) as tracker:
            self.play(
                plane.animate.set_opacity(1.0),
                cloud.dots.animate.set_opacity(0.88),
                diagonal_label.animate.set_opacity(1.0),
                active_line.animate.set_stroke(opacity=0.50),
                active_arrow.animate.set_opacity(1.0),
                active_label.animate.set_opacity(1.0),
                run_time=max(0.7, tracker.time_until_bookmark("fill")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("fill")
            # Breathing room: let the established scene register before the
            # wheel starts moving, rather than launching straight into a full
            # rotation the instant the fade-in finishes.
            self.inspect(0.4)
            self.play(
                angle.animate.set_value(shadow_angles[0] + TAU),
                wheel_ring.animate.set_stroke(opacity=0.35),
                plane.animate.set_opacity(0.24),
                FadeOut(diagonal_label, shift=0.06 * UP),
                LaggedStart(*(
                    spoke.animate.set_stroke(opacity=0.14)
                    for spoke in spokes
                ), lag_ratio=0.02),
                LaggedStart(*(
                    FadeIn(plot, scale=0.97) for plot in shadow_plots
                ), lag_ratio=0.09),
                run_time=max(3.4, tracker.time_until_bookmark("ask")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("ask")
            self.wait(tracker.get_remaining_duration())

        # Let the eased turn settle before the cloud changes underneath it.
        self.inspect(0.25)

        # --- preserve the batches while the centre becomes Gaussian --------
        # The eight bells illustrate "every direction, same target"; this
        # equation is what actually earns it -- Z's covariance is the
        # identity, so u^T Z's variance is u^T I u = 1 for every unit u. A
        # live variance readout plus a couple of quick direction changes
        # (shown, never narrated directly) lets the viewer watch that claim
        # hold empirically while the equation states it symbolically.
        # Both live in the top-left corner, outside the wheel's content radius;
        # the old mid-left placement let the left shadow plot cut through them.
        forward_eq = ty.maths(
            R"u^\top Z\sim\mathcal N(0,\,u^\top I u)=\mathcal N(0,1)",
            size=ty.EQ,
            color=INK,
            isolate=[R"\mathcal N(0,1)"],
        )
        forward_eq.set_color_by_tex(R"\mathcal N(0,1)", TARGET)
        forward_eq.to_corner(UL, buff=0.5)
        layout.fit_in_frame(forward_eq)
        # Not pre-added at opacity 0: Manim's FadeIn animates toward the
        # mobject's opacity *at play() time*, so zeroing it here and then
        # calling FadeIn(forward_eq) later would fade from invisible to
        # invisible. FadeIn adds the mobject to the scene itself.

        variance_label = ty.maths(
            R"\mathrm{Var}[u^\top Z]\approx", size=ty.LABEL, color=MUTED,
        )
        variance_value = DecimalNumber(1.0, num_decimal_places=2)
        variance_value.set_color(TARGET)
        variance_value.match_height(variance_label)
        variance_readout = VGroup(variance_label, variance_value).arrange(
            RIGHT, buff=0.12,
        )
        variance_readout.next_to(
            forward_eq, DOWN, buff=0.35, aligned_edge=LEFT,
        )
        layout.fit_in_frame(variance_readout)
        variance_readout.set_opacity(0.0)

        def update_variance(mob):
            pts = cloud.current_points() / SCALE
            mob[1].set_value(float(np.var(pts @ direction())))

        variance_readout.add_updater(update_variance)
        self.add(variance_readout)

        with self.voiceover(
            text="<bookmark mark='gaussian'/>Suppose the cloud itself is "
                 "standard Gaussian. <bookmark mark='spread'/>Then its "
                 "covariance is the identity, so if we project onto any unit "
                 "direction, the variance is exactly one. <bookmark "
                 "mark='hold'/>We can turn u wherever we like, and that "
                 "number does not move. <bookmark mark='turn'/>So every "
                 "direction gives the same standard Gaussian shadow, and "
                 "that one bell is the target every shadow has to match."
        ) as tracker:
            self.wait_until_bookmark("gaussian")
            self.play(
                cloud.animate_base_points(gaussian_points),
                run_time=max(1.2, tracker.time_until_bookmark("spread")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("spread")
            # Let the Gaussian shape register before the equation that
            # explains it appears on top of it.
            self.inspect(0.4)
            self.play(
                FadeIn(forward_eq, shift=0.06 * UP),
                variance_readout.animate.set_opacity(1.0),
                run_time=max(0.5, tracker.time_until_bookmark("hold")),
            )
            self.wait_until_bookmark("hold")
            # Three readable direction samples share the whole spoken window:
            # motion, then a settle long enough to read the live variance.
            wiggle_base = angle.get_value()
            flick_budget = max(3.9, tracker.time_until_bookmark("turn"))
            motion_time = float(np.clip((flick_budget - 1.5) / 3, 0.8, 0.9))
            settle_time = max(0.35, (flick_budget - 3 * motion_time) / 3)
            for destination in (
                wiggle_base + np.deg2rad(71),
                wiggle_base - np.deg2rad(47),
                wiggle_base,
            ):
                self.play(
                    angle.animate.set_value(destination),
                    run_time=motion_time,
                    rate_func=smooth,
                )
                self.wait(settle_time)
            self.wait_until_bookmark("turn")
            variance_readout.clear_updaters()
            turn_transition_time = min(
                0.65,
                max(
                    1 / config.frame_rate,
                    0.2 * tracker.get_remaining_duration(),
                ),
            )
            self.play(
                target_curves.animate.set_stroke(opacity=0.94),
                FadeOut(forward_eq, shift=0.04 * UP),
                FadeOut(variance_readout),
                run_time=turn_transition_time,
            )
            self.across(
                tracker,
                angle.animate.set_value(shadow_angles[0] + 1.5 * TAU),
                LaggedStart(*(
                    Indicate(dots, color=DIRECTION, scale_factor=1.035)
                    for dots in shadow_dot_groups
                ), lag_ratio=0.07),
                floor=1.8,
                rate_func=linear,
            )

        # --- the converse: one visible shadow becomes one radial slice -----
        # The upper-left plot is already part of the wheel, so the derivation
        # starts from that existing batch rather than inventing a fresh example.
        # Brightness is deliberately absent here: this beat identifies xi = tu;
        # the next beat introduces the height-to-brightness encoding.
        converse_axes = layout.rig_cf_axes(
            t_max=CF_T_MAX, y_range=(-0.55, 1.15),
        )
        converse_panel_label = ty.maths(
            R"\varphi_{u^\top Z}(t)", size=ty.EQ, color=MAGNITUDE,
        ).next_to(converse_axes, UP, buff=0.18)
        converse_curve_ts = np.linspace(0, CF_T_MAX, 200)
        converse_curve = VMobject().set_stroke(
            MAGNITUDE, 3,
        ).set_fill(opacity=0.0)
        converse_curve.set_points_smoothly([
            converse_axes.c2p(t, v)
            for t, v in zip(converse_curve_ts, gaussian_cf(converse_curve_ts))
        ])

        converse_eq = VGroup(
            ty.maths(
                R"\varphi_{u^\top Z}(t)"
                R"=\mathbb E\!\left[e^{it(u^\top Z)}\right]"
                R"=\varphi_Z(tu)",
                size=ty.EQ,
                color=INK,
                isolate=[R"\varphi_Z(tu)"],
            ),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        converse_eq[0].set_color_by_tex(R"\varphi_Z(tu)", MAGNITUDE)
        converse_eq.to_corner(UL, buff=0.55)

        frequency_frame = VGroup(
            Line(SPOKE_RADIUS * LEFT, SPOKE_RADIUS * RIGHT),
            Line(SPOKE_RADIUS * DOWN, SPOKE_RADIUS * UP),
        ).set_stroke(AXIS, 1.4, opacity=0.72)
        # Both axis labels sit well inside the wheel rather than at the axis
        # tips. The tips are exactly the bands the rest of the scene writes
        # into: the right tip shares a narrow column with the CF panel's
        # y-axis for the whole derivation, and the top tip is where
        # `cw_label`, `specialize_eq` and `field_label` all land later. At the
        # tips the labels read as struck through that text; pulled inboard
        # they still read unambiguously as the axis they name.
        xi_one = ty.maths(R"\xi_1", size=ty.TICK, color=MUTED)
        xi_one.next_to(0.78 * SPOKE_RADIUS * RIGHT, UP, buff=0.10)
        xi_two = ty.maths(R"\xi_2", size=ty.TICK, color=MUTED)
        xi_two.next_to(0.80 * SPOKE_RADIUS * UP, RIGHT, buff=0.10)
        frequency_labels = VGroup(xi_one, xi_two)
        freq_tag = ty.caption("frequency space").to_corner(DL, buff=0.50)

        frequency_guide = DashedLine(
            ORIGIN, SPOKE_RADIUS * direction(), dash_length=0.08,
        ).set_stroke(DIRECTION, 2.2, opacity=0.78)

        def turn_frequency_guide(mob):
            mob.put_start_and_end_on(ORIGIN, SPOKE_RADIUS * direction())

        frequency_guide.add_updater(turn_frequency_guide)

        t_scale_wheel = SPOKE_RADIUS / CF_T_MAX
        t_samples = np.linspace(0, CF_T_MAX, N_RAY_SEGMENTS + 1)
        h_samples = gaussian_cf(t_samples)
        ray_opacities = [
            float(np.clip(h, 0.0, 1.0)) for h in h_samples[:-1]
        ]
        t_val = ValueTracker(0.0)
        freq_tracer = Dot(radius=0.055).set_fill(INK, 1.0).set_stroke(width=0)

        def update_freq_tracer(mob):
            t = t_val.get_value()
            mob.move_to(t * t_scale_wheel * direction())

        freq_tracer.add_updater(update_freq_tracer)
        graph_tracer = Dot(radius=0.055).set_fill(INK, 1.0).set_stroke(width=0)

        def update_graph_tracer(mob):
            t = t_val.get_value()
            mob.move_to(converse_axes.c2p(t, float(gaussian_cf(t))))

        graph_tracer.add_updater(update_graph_tracer)

        active_shadow_index = 3
        # shadow_angles[3] and spoke_angles[0] both lie on the 135-degree axis.
        active_spoke = spokes[0]
        inactive_shadow_plots = VGroup(*(
            plot for index, plot in enumerate(shadow_plots)
            if index != active_shadow_index
        ))

        with self.voiceover(
            text="<bookmark mark='one'/>Now take one shadow on its own. Its "
                 "characteristic function averages a unit arrow whose angle "
                 "is t times u transpose z. But that angle is also z dotted "
                 "with t u. That is the whole cloud's characteristic "
                 "function, evaluated at the single point t u. <bookmark "
                 "mark='meaning'/>That means u picks out a ray from the "
                 "origin of frequency space, and t says how far out along "
                 "that ray we are. <bookmark mark='trace'/>So as t grows, "
                 "the shadow's curve reads off the cloud's characteristic "
                 "function along that one ray."
        ) as tracker:
            self.wait_until_bookmark("one")
            # Snap to the already-drawn upper-left shadow. Animating from the
            # accumulated multi-turn tracker value would visibly spin backward.
            angle.set_value(float(shadow_angles[active_shadow_index]))
            self.update_mobjects(0)
            one_budget = max(0.7, tracker.time_until_bookmark("meaning"))
            spoke_pulse_time = min(0.8, one_budget)
            self.play(
                cloud.dots.animate.set_opacity(0.0),
                inactive_shadow_plots.animate.set_opacity(0.0),
                Create(converse_axes),
                Create(converse_curve),
                FadeIn(converse_panel_label),
                FadeIn(converse_eq[0], shift=0.05 * UP),
                active_line.animate.set_stroke(opacity=0.85),
                Succession(
                    Indicate(
                        active_spoke, color=DIRECTION, scale_factor=1.015,
                        run_time=spoke_pulse_time,
                    ),
                    Wait(run_time=max(0.0, one_budget - spoke_pulse_time)),
                ),
                run_time=one_budget,
            )
            self.wait_until_bookmark("meaning")
            meaning_budget = max(2.4, tracker.time_until_bookmark("trace"))
            frame_budget = meaning_budget * 0.35
            ring_pulse_time = min(0.8, frame_budget)
            self.play(
                FadeOut(plane), FadeOut(active_line),
                FadeIn(frequency_frame), FadeIn(frequency_labels),
                FadeIn(freq_tag, shift=0.04 * UP),
                Create(frequency_guide),
                Succession(
                    Indicate(
                        wheel_ring, color=DIRECTION, scale_factor=1.01,
                        run_time=ring_pulse_time,
                    ),
                    Wait(run_time=max(0.0, frame_budget - ring_pulse_time)),
                ),
                run_time=frame_budget,
            )
            self.play(
                t_val.animate.set_value(CF_T_MAX),
                FadeIn(freq_tracer), FadeIn(graph_tracer),
                run_time=meaning_budget * 0.65,
                rate_func=linear,
            )
            self.wait_until_bookmark("trace")
            self.play(
                Indicate(
                    shadow_plots[active_shadow_index],
                    color=DIRECTION,
                    scale_factor=1.025,
                ),
                Indicate(converse_curve, color=MAGNITUDE, scale_factor=1.025),
                run_time=max(0.8, tracker.get_remaining_duration()),
            )

        # Retire the derivation furniture while preserving the curve itself.
        # Beat 4 starts from the exact radial slice it is about to encode.
        self.play(
            FadeOut(converse_eq), FadeOut(converse_panel_label),
            FadeOut(shadow_plots[active_shadow_index]),
            run_time=0.45,
        )

        # --- every direction: encode the slice on its ray and fill the plane
        # Brightness is the signed curve height clipped at zero: positive
        # values emit light, while negative values are deliberately dark.
        height_label = ty.caption("height").set_color(MUTED)
        first_equals = ty.maths("=", size=ty.LABEL, color=MUTED)
        height_value = ty.maths(
            R"\varphi_Z(tu)", size=ty.LABEL, color=MAGNITUDE,
        )
        second_equals = ty.maths("=", size=ty.LABEL, color=MUTED)
        brightness_label = ty.caption("brightness").set_color(MUTED)
        encoding_legend = VGroup(
            height_label, first_equals, height_value,
            second_equals, brightness_label,
        ).arrange(RIGHT, buff=0.14)
        encoding_legend.next_to(converse_axes, DOWN, buff=0.32)
        layout.fit_in_frame(encoding_legend)

        reveal = ValueTracker(0.0)
        ray = VGroup(*(
            Line(ORIGIN, ORIGIN) for _ in range(N_RAY_SEGMENTS)
        ))

        def update_ray(mob):
            u = direction()
            revealed_t = reveal.get_value() * CF_T_MAX
            for i, seg in enumerate(mob):
                seg.put_start_and_end_on(
                    t_samples[i] * t_scale_wheel * u,
                    t_samples[i + 1] * t_scale_wheel * u,
                )
                if t_samples[i + 1] <= revealed_t:
                    segment_reveal = 1.0
                elif t_samples[i] >= revealed_t:
                    segment_reveal = 0.0
                else:
                    segment_reveal = (
                        (revealed_t - t_samples[i])
                        / (t_samples[i + 1] - t_samples[i])
                    )
                seg.set_stroke(
                    MAGNITUDE, 4,
                    opacity=ray_opacities[i] * segment_reveal,
                )

        update_ray(ray)
        ray.add_updater(update_ray)
        self.add(ray)

        with self.voiceover(
            text="<bookmark mark='encode'/>So far that is one ray, and the "
                 "rest of the plane is still blank. The curve gives us each "
                 "value as a height, but we can just as well draw it as "
                 "brightness, right at the point t u. <bookmark "
                 "mark='lit'/>Then the whole curve becomes one line of light "
                 "along the ray, bright at the origin and fading as the "
                 "curve falls. <bookmark mark='sweep'/>Now, if we turn u, "
                 "the ray turns with it, <bookmark mark='fill'/>and since "
                 "every point of frequency space sits at some distance along "
                 "some direction, the sweep fills in the whole plane. This "
                 "is the cloud's characteristic function, drawn everywhere "
                 "at once."
        ) as tracker:
            self.wait_until_bookmark("encode")
            self.play(
                FadeIn(encoding_legend, shift=0.04 * UP),
                run_time=max(0.7, tracker.time_until_bookmark("lit")),
            )
            self.wait_until_bookmark("lit")
            self.play(
                reveal.animate.set_value(1.0),
                FadeOut(frequency_guide), FadeOut(freq_tracer),
                FadeOut(graph_tracer),
                run_time=max(1.2, tracker.time_until_bookmark("sweep")),
                rate_func=linear,
            )
            self.wait_until_bookmark("sweep")

            # Static rays reveal behind the live ray as u turns. Each receives
            # a brief width pop at the reveal edge, so the fan reads as a
            # directional accumulation rather than a flat radial wipe.
            sweep_start_angle = angle.get_value()
            ray_offsets = np.linspace(0, TAU, N_SWEEP_RAYS, endpoint=False)[1:]
            trail_rays = VGroup()
            for offset in ray_offsets:
                a = sweep_start_angle + offset
                u = np.array([np.cos(a), np.sin(a), 0.0])
                trail_ray = VGroup(*(
                    Line(
                        t_samples[i] * t_scale_wheel * u,
                        t_samples[i + 1] * t_scale_wheel * u,
                    ).set_stroke(MAGNITUDE, 3, opacity=0.0)
                    for i in range(N_RAY_SEGMENTS)
                ))
                trail_rays.add(trail_ray)

            def reveal_trail(mob):
                progress = angle.get_value() - sweep_start_angle
                for offset, trail_ray in zip(ray_offsets, mob):
                    edge = (progress - offset) / 0.12 + 1.0
                    trail_reveal = float(np.clip(edge, 0.0, 1.0))
                    pop = 1.0
                    if edge > 1.0:
                        pop = 1.0 + 1.1 * float(
                            np.exp(-10.0 * (edge - 1.0) ** 2)
                        )
                    for seg, base in zip(trail_ray, ray_opacities):
                        seg.set_stroke(
                            MAGNITUDE, 3 * pop,
                            opacity=base * trail_reveal,
                        )

            trail_rays.add_updater(reveal_trail)
            self.add(trail_rays)
            self.play(
                angle.animate.set_value(sweep_start_angle + TAU),
                FadeOut(encoding_legend),
                run_time=max(3.2, tracker.time_until_bookmark("fill")),
                rate_func=linear,
            )
            self.wait_until_bookmark("fill")
            self.freeze(
                ray, trail_rays, active_arrow, active_label,
                *shadow_dot_groups,
            )
            gaussian_field = _field_image(GAUSSIAN_PROFILE, MAGNITUDE)
            self.play(
                FadeOut(ray), FadeOut(trail_rays),
                FadeOut(active_arrow), FadeOut(active_label),
                FadeIn(gaussian_field),
                run_time=max(0.8, tracker.get_remaining_duration()),
            )

        # --- a second cloud: same first two moments, different slice -------
        # The original cloud's dot updater is anchored at the scene origin.
        # Freeze it, and every wheel shadow that reads it, before scaling and
        # moving the parent group into the left comparison panel.
        cloud.freeze()
        self.freeze(*shadow_dot_groups)

        comparison_mix = ValueTracker(1.0)
        ring_points_2d = data.ring_2d(
            n=len(gaussian_points), radius=np.sqrt(2.0), jitter=0.0, seed=31,
        )
        ring_points = np.column_stack([
            ring_points_2d, np.zeros(len(ring_points_2d)),
        ])
        gaussian_panel_points = (
            gaussian_points * SCALE * COMPARISON_SCALE + COMPARISON_RIGHT
        )
        ring_panel_points = (
            ring_points * SCALE * COMPARISON_SCALE + COMPARISON_RIGHT
        )

        transfer_times = np.linspace(
            0.0, 1.0 - MIX_WINDOW, len(gaussian_points),
        )
        transfer_times = np.random.default_rng(606).permutation(transfer_times)

        def point_gaussian_weights() -> np.ndarray:
            local = np.clip(
                (comparison_mix.get_value() - transfer_times) / MIX_WINDOW,
                0.0,
                1.0,
            )
            return local * local * (3.0 - 2.0 * local)

        rival_dots = VGroup(*(
            Dot(radius=DOT_RADIUS * COMPARISON_SCALE)
            .set_fill(RIVAL, 0.88)
            .set_stroke(width=0)
            .move_to(point)
            for point in gaussian_panel_points
        ))

        def move_rival_points(group):
            weights = point_gaussian_weights()[:, None]
            points = ring_panel_points + weights * (
                gaussian_panel_points - ring_panel_points
            )
            for dot, point in zip(group, points):
                dot.move_to(point)

        rival_dots.add_updater(move_rival_points)

        comparison_axes_shift = (
            COMPARISON_AXES_CENTRE - converse_axes.get_center()
        )
        comparison_panel_label = ty.maths(
            R"\varphi_{u^\top X}(t)", size=ty.EQ, color=MAGNITUDE,
        ).next_to(converse_axes, UP, buff=0.18).shift(comparison_axes_shift)

        x_caption = ty.caption("Gaussian cloud").set_color(MAGNITUDE)
        x_caption.move_to(np.array([COMPARISON_LEFT[0], 3.35, 0.0]))
        y_caption = ty.caption("ring cloud").set_color(RIVAL)
        y_caption.move_to(np.array([COMPARISON_RIGHT[0], 3.35, 0.0]))
        matched_y_caption = ty.caption("Gaussian cloud").set_color(RIVAL)
        matched_y_caption.move_to(y_caption)
        x_label = ty.maths("X", size=ty.EQ_DISPLAY, color=MAGNITUDE)
        x_label.move_to(COMPARISON_LEFT + 1.42 * LEFT)
        y_label = ty.maths("Y", size=ty.EQ_DISPLAY, color=RIVAL)
        y_label.move_to(COMPARISON_RIGHT + 1.42 * RIGHT)
        for label in (
            x_caption, y_caption, matched_y_caption, x_label, y_label,
        ):
            layout.fit_in_frame(label)

        comparison_axes_target = converse_axes.copy().shift(
            comparison_axes_shift,
        )
        ring_curve_values = np.interp(
            converse_curve_ts, FIELD_RADII, RING_PROFILE,
        )
        gaussian_curve_values = gaussian_cf(converse_curve_ts)
        rival_curve = VMobject().set_stroke(RIVAL, 3).set_fill(opacity=0.0)
        rival_curve.set_points_smoothly([
            comparison_axes_target.c2p(t, value)
            for t, value in zip(converse_curve_ts, ring_curve_values)
        ])
        rival_curve_label = ty.maths(
            R"\varphi_{u^\top Y}(t)", size=ty.TICK, color=RIVAL,
        )
        rival_curve_label.next_to(
            comparison_axes_target.c2p(2.65, -0.40), DOWN, buff=0.10,
        )

        gap_index = int(np.argmax(gaussian_curve_values - ring_curve_values))
        gap_t = float(converse_curve_ts[gap_index])
        gap_rule = Line(
            comparison_axes_target.c2p(
                gap_t, ring_curve_values[gap_index],
            ),
            comparison_axes_target.c2p(
                gap_t, gaussian_curve_values[gap_index],
            ),
        ).set_stroke(COLLAPSE, 3.0, opacity=0.95)

        moments_block = VGroup(
            ty.maths(
                R"\mathbb E[X]=\mathbb E[Y]=0",
                size=ty.BODY, color=MUTED,
            ),
            ty.maths(
                R"\operatorname{Cov}(X)=\operatorname{Cov}(Y)=I",
                size=ty.BODY, color=MUTED,
            ),
        ).arrange(DOWN, buff=0.14)
        comparison_content_bottom = min(
            comparison_axes_target.get_bottom()[1],
            rival_curve_label.get_bottom()[1],
        )
        moments_block.move_to(np.array([
            COMPARISON_AXES_CENTRE[0],
            comparison_content_bottom - 0.22 - moments_block.height / 2,
            0.0,
        ]))
        layout.fit_in_frame(moments_block)

        with self.voiceover(
            text="<bookmark mark='second'/>Now suppose we take a second "
                 "cloud. We start from the same points, and push them outward "
                 "until they sit on a ring instead of piling up in the "
                 "middle. <bookmark mark='moments'/>Its mean is still zero, "
                 "and its covariance is still the identity. So any test built "
                 "on those two numbers gives the same answer for both clouds, "
                 "<bookmark mark='differ'/>even though the ring and the "
                 "Gaussian are two different distributions."
        ) as tracker:
            self.wait_until_bookmark("second")
            second_budget = max(4.8, tracker.time_until_bookmark("moments"))
            self.play(
                FadeOut(frequency_frame),
                FadeOut(frequency_labels), FadeOut(freq_tag),
                wheel_ring.animate.set_stroke(opacity=0.0),
                spokes.animate.set_stroke(opacity=0.0),
                active_arrow.animate.set_opacity(0.0),
                active_label.animate.set_opacity(0.0),
                gaussian_field.animate.scale(
                    COMPARISON_FIELD_SCALE,
                ).move_to(np.array([
                    COMPARISON_LEFT[0], -2.25, 0.0,
                ])),
                cloud.dots.animate.scale(COMPARISON_SCALE).shift(
                    COMPARISON_LEFT,
                ).set_opacity(0.88),
                converse_axes.animate.shift(comparison_axes_shift),
                converse_curve.animate.shift(comparison_axes_shift),
                FadeIn(comparison_panel_label, shift=0.04 * UP),
                FadeIn(x_caption), FadeIn(x_label),
                run_time=second_budget * 0.25,
                rate_func=smooth,
            )
            self.play(
                LaggedStart(*(
                    TransformFromCopy(source, target)
                    for source, target in zip(cloud.dots, rival_dots)
                ), lag_ratio=0.004),
                FadeIn(y_caption), FadeIn(y_label),
                run_time=second_budget * 0.30,
                rate_func=smooth,
            )
            # TransformFromCopy registers the individual targets. Re-add the
            # same parent group because it owns the one mixture-wave updater.
            self.add(rival_dots)
            self.play(
                comparison_mix.animate.set_value(0.0),
                run_time=second_budget * 0.45,
                rate_func=linear,
            )
            self.wait_until_bookmark("moments")
            self.play(
                FadeIn(moments_block, shift=0.04 * UP),
                run_time=max(0.8, tracker.time_until_bookmark("differ")),
            )
            self.wait_until_bookmark("differ")
            self.play(
                Indicate(moments_block, color=INK, scale_factor=1.025),
                run_time=max(0.8, tracker.get_remaining_duration()),
            )

        # --- the two clouds cast different shadows along the same u --------
        comparison_angle = np.deg2rad(35.0)
        comparison_u = np.array([
            np.cos(comparison_angle), np.sin(comparison_angle), 0.0,
        ])
        # The wheel's eight rim plots (MINI_* above) are read as a family at a
        # glance, so they are deliberately tiny and tilted to their own
        # tangent. The comparison panels have the opposite job: the viewer has
        # to read ONE distribution's shape precisely enough to see that it
        # differs from its neighbour. Three things follow, and none of them
        # should be inherited from MINI_*.
        #
        # Horizontal, not tilted along u. A dot plot tilted 35 degrees is read
        # as a smear, and at these panel positions the tilted baseline also ran
        # under the captions and off the frame edge. The arrow through the
        # cloud already states the direction, and beat 5 flies the points from
        # the cloud into these bins, so the correspondence survives without the
        # tilt costing legibility.
        #
        # 80 samples, not the wheel's 36. The ring's projection is arcsine --
        # its whole signature is two piles at the edges of a bounded support --
        # and 36 samples cannot resolve two piles from one clump.
        #
        # A ceiling well above the tallest real column. MINI_STACK_MAX = 7 shaved
        # exactly the ring's two peaks (they reach 12) while never touching the
        # Gaussian (6), which flattened both to the same height and destroyed
        # the one contrast this beat exists to show. 16 is a guard against a
        # pathological input, not a shaping parameter.
        COMPARISON_SAMPLE_COUNT = 80
        COMPARISON_STACK_MAX = 16
        comparison_dot_radius = 0.023
        comparison_half_width = 1.40
        comparison_span_sd = 3.1
        comparison_stack_step = 2 * comparison_dot_radius * 1.12
        comparison_baseline_y = 2.32
        comparison_indices = np.linspace(
            0, len(cloud.dots) - 1, COMPARISON_SAMPLE_COUNT, dtype=int,
        )

        def comparison_shadow(point_group, centre):
            anchor = np.array([centre[0], comparison_baseline_y, 0.0])
            baseline = Line(
                anchor - comparison_half_width * RIGHT,
                anchor + comparison_half_width * RIGHT,
            ).set_stroke(AXIS, 1.4, opacity=0.60)
            dots = VGroup(*(
                Dot(radius=comparison_dot_radius)
                .set_fill(DIRECTION, 0.90)
                .set_stroke(width=0)
                for _ in comparison_indices
            ))

            def move_comparison_shadow(group):
                points = np.array([
                    point_group[index].get_center()
                    for index in comparison_indices
                ])
                # The plotted value is still u^T z; only the axis it is drawn
                # against is horizontal.
                values = (
                    (points - centre) / (SCALE * COMPARISON_SCALE)
                ) @ comparison_u
                positions = np.clip(
                    values / comparison_span_sd * comparison_half_width,
                    -comparison_half_width,
                    comparison_half_width,
                )
                levels = np.minimum(
                    np.asarray(
                        layout.stack_levels(
                            positions, comparison_stack_step,
                        ),
                        dtype=float,
                    ),
                    COMPARISON_STACK_MAX,
                )
                for dot, position, level in zip(group, positions, levels):
                    dot.move_to(
                        anchor
                        + float(position) * RIGHT
                        + (level + 0.75) * comparison_stack_step * UP
                    )

            move_comparison_shadow(dots)
            dots.add_updater(move_comparison_shadow)
            return VGroup(baseline, dots)

        x_shadow = comparison_shadow(cloud.dots, COMPARISON_LEFT)
        y_shadow = comparison_shadow(rival_dots, COMPARISON_RIGHT)
        x_projection = Arrow(
            COMPARISON_LEFT - 1.25 * comparison_u,
            COMPARISON_LEFT + 1.25 * comparison_u,
            buff=0.0, stroke_width=4.0, tip_length=0.14,
            color=DIRECTION,
        )
        y_projection = Arrow(
            COMPARISON_RIGHT - 1.25 * comparison_u,
            COMPARISON_RIGHT + 1.25 * comparison_u,
            buff=0.0, stroke_width=4.0, tip_length=0.14,
            color=DIRECTION,
        )

        rival_field = _field_image(RING_PROFILE, RIVAL)
        rival_field.scale(COMPARISON_FIELD_SCALE)
        rival_field.move_to(np.array([
            COMPARISON_RIGHT[0], -2.25, 0.0,
        ]))
        rival_field_mix = [None]

        def update_rival_field(mob):
            mix = comparison_mix.get_value()
            if rival_field_mix[0] == mix:
                return
            blend = (
                (1.0 - mix) * RING_PROFILE
                + mix * GAUSSIAN_PROFILE
            )
            mob.pixel_array[..., 3] = _field_alpha(blend)
            rival_field_mix[0] = mix

        rival_field.add_updater(update_rival_field)

        with self.voiceover(
            text="<bookmark mark='project'/>Project both clouds onto the same "
                 "direction. <bookmark mark='shadows'/>The Gaussian's shadow "
                 "is one hump. The ring's shadow is two piles, pushed out to "
                 "either side, and those two batches still share the same "
                 "mean and variance. <bookmark mark='curves'/>But their "
                 "characteristic functions do not agree. The ring's curve "
                 "dips below zero, where the Gaussian's is still falling "
                 "smoothly. <bookmark mark='gap'/>So one direction is "
                 "already enough to separate two clouds that the moments "
                 "could not. <bookmark mark='fields'/>And if we sweep u "
                 "around the ring as well, the difference shows up across "
                 "the whole plane: the Gaussian's field fades out smoothly, "
                 "while the ring's has a bright core and a dark band where "
                 "its curve goes negative."
        ) as tracker:
            self.wait_until_bookmark("project")
            self.play(
                GrowArrow(x_projection), GrowArrow(y_projection),
                run_time=max(0.7, tracker.time_until_bookmark("shadows")),
            )
            self.wait_until_bookmark("shadows")

            # Keep the live shadow groups in the scene from the start. The
            # previous TransformFromCopy version animated their child dots as
            # temporary LaggedStart-owned targets and then tried to re-parent
            # those same mobjects afterward; that scene-graph handoff left no
            # persistent shadow in the real voice-timed render. These separate
            # flight copies are explicit top-level mobjects, while the live
            # histogram waits invisibly at the exact landing positions.
            # Adding them through a (zero-length) play(), not a bare add(),
            # matters: every other long-lived mobject in this scene enters
            # via self.play(), and a mobject added outside that path was
            # observed to survive its own later FadeOut on screen -- correctly
            # dropped from self.mobjects, but never actually cleared from the
            # rendered frame for the rest of the video.
            x_shadow.set_opacity(0.0)
            y_shadow.set_opacity(0.0)
            self.play(
                FadeIn(x_shadow[0]), FadeIn(x_shadow[1]),
                FadeIn(y_shadow[0]), FadeIn(y_shadow[1]),
                run_time=max(
                    1 / config.frame_rate,
                    0.01 * tracker.time_until_bookmark("curves"),
                ),
            )

            x_flight_dots = [
                cloud.dots[index].copy()
                for index in comparison_indices
            ]
            y_flight_dots = [
                rival_dots[index].copy()
                for index in comparison_indices
            ]
            x_flight = VGroup(*x_flight_dots)
            y_flight = VGroup(*y_flight_dots)
            x_targets = [
                dot.copy()
                .set_fill(DIRECTION, 0.90)
                .set_stroke(width=0)
                for dot in x_shadow[1]
            ]
            y_targets = [
                dot.copy()
                .set_fill(DIRECTION, 0.90)
                .set_stroke(width=0)
                for dot in y_shadow[1]
            ]
            assert len(x_flight) == len(x_targets) == COMPARISON_SAMPLE_COUNT
            assert len(y_flight) == len(y_targets) == COMPARISON_SAMPLE_COUNT
            self.add(x_flight, y_flight)
            self.play(
                x_shadow[0].animate.set_stroke(AXIS, 1.1, opacity=0.60),
                y_shadow[0].animate.set_stroke(AXIS, 1.1, opacity=0.60),
                LaggedStart(*(
                    Transform(dot, target)
                    for dot, target in zip(x_flight, x_targets)
                ), lag_ratio=0.006),
                LaggedStart(*(
                    Transform(dot, target)
                    for dot, target in zip(y_flight, y_targets)
                ), lag_ratio=0.006),
                run_time=max(0.9, tracker.time_until_bookmark("curves")),
            )
            # Scene.play promotes each Transform-animated submobject out of
            # its parent VGroup and into scene.mobjects in its own right, so by
            # the time the play returns, x_flight/y_flight are empty shells:
            # removing just the groups leaves all 160 flown copies on screen for
            # the rest of the scene, stacked exactly on the bins they landed in
            # and invisible as a defect when the comparison clears at 'if'.
            # Name the dots themselves as well as their groups.
            self.remove(
                x_flight, y_flight, *x_flight_dots, *y_flight_dots,
            )
            x_shadow[1].set_fill(DIRECTION, 0.90).set_stroke(width=0)
            y_shadow[1].set_fill(DIRECTION, 0.90).set_stroke(width=0)
            self.update_mobjects(0)
            self.wait_until_bookmark("curves")
            self.play(
                Create(rival_curve), FadeIn(rival_curve_label),
                run_time=max(1.0, tracker.time_until_bookmark("gap")),
            )
            self.wait_until_bookmark("gap")
            self.play(
                Create(gap_rule),
                Indicate(rival_curve, color=RIVAL, scale_factor=1.015),
                run_time=max(0.8, tracker.time_until_bookmark("fields")),
            )
            self.wait_until_bookmark("fields")
            field_centre = rival_field.get_center()
            field_sweep = Line(
                field_centre,
                field_centre + 0.5 * COMPARISON_FIELD_DIAMETER * RIGHT,
            ).set_stroke(DIRECTION, 3.0, opacity=0.95)
            fields_budget = max(1.2, tracker.get_remaining_duration())
            fields_sweep_time = min(1.2, fields_budget)
            self.play(
                FadeIn(rival_field),
                Rotate(
                    field_sweep, angle=TAU, about_point=field_centre,
                ),
                run_time=fields_sweep_time,
                rate_func=linear,
            )
            remaining_fields_time = max(
                0.0, tracker.get_remaining_duration(),
            )
            self.play(
                FadeOut(field_sweep),
                run_time=max(
                    1 / config.frame_rate,
                    min(0.35, remaining_fields_time),
                ),
            )
            self.wait(tracker.get_remaining_duration())

        # --- one mixture tracker moves Y, its shadow, and its population CF
        def update_rival_curve(mob):
            mix = comparison_mix.get_value()
            values = (
                (1.0 - mix) * ring_curve_values
                + mix * gaussian_curve_values
            )
            mob.set_points_smoothly([
                converse_axes.c2p(t, value)
                for t, value in zip(converse_curve_ts, values)
            ])

        rival_curve.add_updater(update_rival_curve)

        with self.voiceover(
            text="<bookmark mark='push'/>Now, if we move the ring's points "
                 "back, a few at a time, into the positions the Gaussian's "
                 "points occupy, <bookmark mark='follow'/>then its shadow "
                 "closes into a single hump, its curve climbs toward the "
                 "Gaussian's, and the dark band in its field fills in. "
                 "<bookmark mark='meet'/>The two fields only agree once the "
                 "two clouds do."
        ) as tracker:
            self.wait_until_bookmark("push")
            push_budget = max(1.0, tracker.time_until_bookmark("follow"))
            total_mix_budget = max(
                push_budget + 1.0, tracker.time_until_bookmark("meet"),
            )
            first_mix = float(np.clip(
                push_budget / total_mix_budget, 0.25, 0.55,
            ))
            self.play(
                comparison_mix.animate.set_value(first_mix),
                FadeOut(gap_rule), FadeOut(y_caption),
                run_time=push_budget,
                rate_func=linear,
            )
            self.wait_until_bookmark("follow")
            self.play(
                comparison_mix.animate.set_value(1.0),
                FadeIn(matched_y_caption, shift=0.04 * UP),
                run_time=max(1.0, tracker.time_until_bookmark("meet")),
                rate_func=linear,
            )
            self.wait_until_bookmark("meet")
            self.play(
                Indicate(
                    VGroup(converse_curve, rival_curve),
                    color=INK,
                    scale_factor=1.012,
                ),
                Indicate(
                    gaussian_field,
                    color=MAGNITUDE,
                    scale_factor=1.025,
                ),
                Indicate(
                    rival_field,
                    color=RIVAL,
                    scale_factor=1.025,
                ),
                run_time=max(0.8, tracker.get_remaining_duration()),
            )

        uniqueness_recall = ty.maths(
            R"\varphi_X=\varphi_Y\ \Longrightarrow\ X\overset{d}{=}Y",
            size=ty.EQ, color=INK,
        ).to_edge(DOWN, buff=0.48)
        layout.fit_in_frame(uniqueness_recall)

        cw_statement = ty.maths(
            R"\varphi_{u^\top X}(t)=\varphi_{u^\top Y}(t)\ \ \forall u,t"
            R"\quad\Longrightarrow\quad X\overset{d}{=}Y",
            size=ty.EQ,
            color=INK,
            isolate=[R"\forall u,t"],
        ).to_edge(UP, buff=0.5)
        cw_statement.set_color_by_tex(R"\forall u,t", DIRECTION)
        layout.fit_in_frame(cw_statement)
        quantifier = cw_statement.get_part_by_tex(R"\forall u,t")
        quantifier_box = SurroundingRectangle(
            quantifier, color=DIRECTION, buff=0.08, corner_radius=0.05,
        ).set_stroke(width=1.5)
        cw_label = ty.maths(
            R"\text{Cram\'er--Wold}", size=ty.STATEMENT, color=INK,
        ).next_to(cw_statement, DOWN, buff=0.38)
        layout.fit_in_frame(cw_label)

        with self.voiceover(
            text="<bookmark mark='if'/>So if two clouds cast the same shadow "
                 "in every direction, then every ray carries the same "
                 "brightness for both, and their characteristic functions "
                 "agree at every point of the plane. <bookmark "
                 "mark='unique'/>And two distributions with the same "
                 "characteristic function everywhere are the same "
                 "distribution. <bookmark mark='statement'/>That means "
                 "matching every one-dimensional shadow, for every direction "
                 "u and every frequency t, forces the two clouds to have the "
                 "same joint distribution. <bookmark mark='name'/>This is "
                 "the Cramer Wold theorem."
        ) as tracker:
            self.wait_until_bookmark("if")
            self.freeze(
                cloud.dots, rival_dots, rival_curve,
                x_shadow[0], x_shadow[1], y_shadow[0], y_shadow[1],
            )
            if_budget = max(2 / config.frame_rate,
                            tracker.time_until_bookmark("unique"))
            self.play(
                FadeOut(cloud.dots), FadeOut(rival_dots),
                FadeOut(x_caption), FadeOut(matched_y_caption),
                FadeOut(x_label), FadeOut(y_label),
                FadeOut(moments_block),
                FadeOut(x_projection), FadeOut(y_projection),
                FadeOut(x_shadow[0]), FadeOut(x_shadow[1]),
                FadeOut(y_shadow[0]), FadeOut(y_shadow[1]),
                FadeOut(rival_curve), FadeOut(rival_curve_label),
                FadeOut(comparison_panel_label),
                FadeOut(converse_axes), FadeOut(converse_curve),
                run_time=if_budget * 0.45,
            )
            # Transform animations promote their dots out of their VGroups;
            # remove the saved child references as well as the empty shells.
            self.remove(
                x_flight, y_flight, *x_flight_dots, *y_flight_dots,
                y_caption, gap_rule,
            )
            self.freeze(rival_field)
            comparison_to_theorem_scale = (
                2 * SPOKE_RADIUS * 0.82 / COMPARISON_FIELD_DIAMETER
            )
            self.play(
                gaussian_field.animate.scale(
                    comparison_to_theorem_scale,
                ).move_to(ORIGIN),
                rival_field.animate.scale(
                    comparison_to_theorem_scale,
                ).move_to(ORIGIN).set_opacity(0.0),
                run_time=if_budget * 0.55,
                rate_func=smooth,
            )
            self.remove(rival_field)
            self.wait_until_bookmark("unique")
            self.play(
                FadeIn(uniqueness_recall, shift=0.04 * UP),
                run_time=max(0.8, tracker.time_until_bookmark("statement")),
            )
            self.wait_until_bookmark("statement")
            statement_budget = max(
                1.0, tracker.time_until_bookmark("name"),
            )
            self.play(
                FadeIn(cw_statement, shift=0.05 * UP),
                FadeIn(quantifier_box),
                run_time=statement_budget * 0.55,
            )
            self.play(
                Indicate(quantifier_box, color=DIRECTION, scale_factor=1.08),
                run_time=statement_budget * 0.45,
            )
            self.wait_until_bookmark("name")
            name_budget = max(0.55, tracker.get_remaining_duration())
            self.play(
                FadeOut(uniqueness_recall), FadeOut(quantifier_box),
                FadeIn(cw_label, shift=0.05 * UP),
                run_time=min(0.55, name_budget),
                rate_func=smooth,
            )
            self.wait(max(0.0, name_budget - min(0.55, name_budget)))

        specialize_eq = ty.maths(
            R"\varphi_{u^\top Z}(t)=e^{-t^2/2}",
            size=ty.EQ,
            color=MAGNITUDE,
        ).to_edge(UP, buff=0.70)
        layout.fit_in_frame(specialize_eq)
        field_label = ty.maths(
            R"\varphi_Z(\xi)=e^{-\|\xi\|^2/2}",
            size=ty.EQ,
            color=MAGNITUDE,
        ).next_to(specialize_eq, DOWN, buff=0.42)
        layout.fit_in_frame(field_label)
        conclusion = ty.maths(
            R"Z\sim\mathcal N(0,I_D)",
            size=ty.EQ_DISPLAY,
            color=INK,
            isolate=[R"\mathcal N(0,I_D)"],
        )
        conclusion.set_color_by_tex(R"\mathcal N(0,I_D)", TARGET)
        conclusion.to_corner(UL, buff=0.50)

        # Two steps, not one crossfade. The theorem and specialisation share
        # the top text band, so clear the named theorem before the next
        # voiceover starts and then reveal the target equation on clean space.
        self.play(
            FadeOut(cw_statement), FadeOut(cw_label),
            run_time=0.45,
        )

        with self.voiceover(
            text="<bookmark mark='specialize'/>For our target, every shadow "
                 "has the same characteristic function, e to the minus t "
                 "squared over two. <bookmark mark='field'/>Read along every "
                 "ray, that one curve fills the plane with e to the minus the "
                 "squared distance from the origin, over two. <bookmark "
                 "mark='resolve'/>And only one cloud has that characteristic "
                 "function: <bookmark mark='conclude'/>Z itself, standard "
                 "Gaussian in every dimension. <bookmark mark='payoff'/>That "
                 "is what the theorem buys us. We never have to look at the "
                 "cloud in D dimensions. If every one-dimensional shadow "
                 "matches the standard bell, then the whole cloud matches "
                 "the target."
        ) as tracker:
            self.wait_until_bookmark("specialize")
            self.play(
                FadeIn(specialize_eq, shift=0.06 * UP),
                run_time=max(0.7, tracker.time_until_bookmark("field")),
            )
            self.wait_until_bookmark("field")
            self.play(
                FadeIn(field_label, shift=0.06 * UP),
                Indicate(
                    gaussian_field, color=MAGNITUDE, scale_factor=1.02,
                ),
                run_time=max(0.8, tracker.time_until_bookmark("resolve")),
            )
            self.wait_until_bookmark("resolve")

            # Two steps, not one crossfade. The closing wheel rises through
            # the two field equations, so clear the frequency-space frame
            # first, then restore the frozen cloud and its shadows on clean
            # space. The conclusion is settled before the narration names Z.
            resolve_budget = max(
                2 / config.frame_rate,
                tracker.time_until_bookmark("conclude"),
            )
            self.play(
                FadeOut(gaussian_field), FadeOut(specialize_eq),
                FadeOut(field_label),
                run_time=resolve_budget * 0.35,
            )
            self.play(
                shadow_baselines.animate.set_stroke(opacity=0.52),
                VGroup(*shadow_dot_groups).animate.set_fill(opacity=0.66),
                target_curves.animate.set_stroke(opacity=0.78).set_fill(
                    opacity=0.0,
                ),
                wheel_ring.animate.set_stroke(opacity=0.35),
                spokes.animate.set_stroke(opacity=0.14),
                cloud.dots.animate.shift(-COMPARISON_LEFT).scale(
                    1.0 / COMPARISON_SCALE,
                ).set_opacity(0.58),
                FadeIn(conclusion, shift=0.08 * UP),
                run_time=resolve_budget * 0.65,
                rate_func=smooth,
            )
            self.wait_until_bookmark("conclude")
            self.play(
                Indicate(conclusion, color=TARGET, scale_factor=1.035),
                run_time=max(0.8, tracker.time_until_bookmark("payoff")),
            )
            self.wait_until_bookmark("payoff")
            self.wait(tracker.get_remaining_duration())

        self.freeze(
            gaussian_field, wheel_ring, spokes, cloud.dots, conclusion,
            *shadow_dot_groups,
        )
        cloud.freeze()
        self.settle_frame()
