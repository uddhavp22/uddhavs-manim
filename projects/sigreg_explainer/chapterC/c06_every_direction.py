"""Chapter C.06 — every direction produces a batch, and all batches identify the cloud.

The scene picks up directly from C05 -- no recap of C02's failed matching or
C03/C04's projection mechanics, both already spent -- and lets the wheel of
shadows build while `u` turns. The converse is derived, not cited: one
direction's characteristic function is shown, algebraically, to be a slice
through the cloud's own; a continuous sweep of `t` grounds how graph height
becomes frequency-space brightness before three example points confirm it;
sweeping `u` fills the plane. An analytic frequency field then compares a
Gaussian with a radius-sqrt(2) ring: the points and signed characteristic
field morph together before written Fourier uniqueness and Cramér--Wold close
the argument.

2026-08-24 revision: the frequency-space construction now resolves into one
reusable magenta ImageMobject, and the former decorative two-icon merge is
replaced by a same-moments Gaussian/ring comparison with a signed-field morph.
The Cramér--Wold implication is written and its all-directions quantifier is
emphasised. C06 now ends on that payoff; the former continuum-of-directions
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
    AXIS, CLOUD, DIRECTION, GRID, INK, MAGNITUDE, MUTED, RIVAL, TARGET,
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
# The three t-values confirmed explicitly once the continuous sweep has
# already drawn the whole ray (EXAMPLE_TS[1] deliberately not round, so it
# doesn't look cherry-picked).
EXAMPLE_TS = (0.5, 1.6, 3.0)
FIELD_GRID = 384
FIELD_PROFILE_SAMPLES = 4096
FIELD_EDGE = 0.06
FIELD_GAMMA = 0.7
PANEL_SCALE = 0.62
PANEL_OFFSET = 3.4
MINI_HALF_WIDTH = 0.72
MINI_X_SCALE = 0.18
MINI_STACK_STEP = 0.035
MINI_STACK_MAX = 7
MINI_DOT_RADIUS = 0.018
MINI_SAMPLE_COUNT = 36


def _standardized_isotropic_points(n: int) -> np.ndarray:
    points = data.gaussian_2d(n=n)
    points = (points - points.mean(axis=0)) / points.std(axis=0)
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
    values = np.abs(signed_profile[FIELD_INDICES])
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
                 "<bookmark mark='fill'/>Each new angle draws another "
                 "shadow of the same cloud, and by the time u has swept "
                 "all the way around, every direction has had its turn."
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
            self.across(
                tracker,
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
                floor=3.4,
                rate_func=linear,
            )

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
                 "standard Gaussian. <bookmark mark='spread'/>Its spread is "
                 "the identity in every direction, so projecting onto any "
                 "unit direction leaves the variance exactly one. <bookmark "
                 "mark='hold'/>The direction can swing anywhere it likes and "
                 "that number stays where it is — <bookmark mark='reason'/>"
                 "every unit direction produces the same standard Gaussian "
                 "shadow. <bookmark mark='turn'/>The finite batch still "
                 "wiggles a little around that shape; the target itself does "
                 "not."
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
            flick_budget = max(3.9, tracker.time_until_bookmark("reason"))
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
            self.wait_until_bookmark("reason")
            self.wait_until_bookmark("turn")
            variance_readout.clear_updaters()
            self.play(
                target_curves.animate.set_stroke(opacity=0.94),
                FadeOut(forward_eq, shift=0.04 * UP),
                FadeOut(variance_readout),
                run_time=0.65,
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

        # --- the converse: derive it on the wheel, re-read as frequency
        # space. Angle is u, radius is t = |xi|. No theorem card, no
        # continuous bend of a graph through the wheel's own plane (that
        # made the curve look like it lived in frequency space, which it
        # doesn't -- only the point xi = tu does). Instead: the identity is
        # shown algebraically, then a continuous sweep of t -- two tracers,
        # one on the graph and one on the live spoke, moving in lock-step --
        # actually shows graph height becoming frequency-space brightness
        # before three example points confirm it at a deliberate pace. The
        # uniqueness theorem is then made concrete by comparing two analytic
        # fields whose distributions share their first two moments. Fourier
        # uniqueness is the only thing still cited; SOURCE_MAP.md SS6e.
        converse_axes = layout.rig_cf_axes(t_max=CF_T_MAX, y_range=(-0.1, 1.15))
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
                R"\varphi_{u^\top Z}(t)=\mathbb E\!\left[e^{it(u^\top Z)}\right]",
                size=ty.EQ,
            ),
            ty.maths(R"=\mathbb E\!\left[e^{i(tu)^\top Z}\right]", size=ty.EQ),
            ty.maths(R"=\varphi_Z(tu)", size=ty.EQ, color=MAGNITUDE),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        converse_eq.to_corner(UL, buff=0.55)

        with self.voiceover(
            text="<bookmark mark='one'/>Take one of those shadows on its own, "
                 "and ask what its characteristic function is. <bookmark "
                 "mark='define'/>For a projection, that means averaging a "
                 "unit arrow whose angle is t times the projected value. "
                 "<bookmark mark='regroup'/>But the projection is already a "
                 "dot product, so the t can move inside it: the angle is the "
                 "point z, dotted with t u. <bookmark mark='identity'/>Which "
                 "makes it the whole cloud's characteristic function, read "
                 "off at the single point t u. <bookmark mark='trace'/>So as "
                 "t runs from zero outward, that point traces a ray across "
                 "frequency space, and the curve's height travels with it as "
                 "brightness. <bookmark mark='points'/>Pick a few heights off "
                 "the curve at random, and each one lands at exactly the "
                 "brightness it predicts. <bookmark mark='rotate'/>Turn u "
                 "through a full circle and the ray turns with it, one "
                 "direction at a time. <bookmark mark='together'/>Once every "
                 "direction has had its turn, the cloud's characteristic "
                 "function is filled in everywhere, because every point of "
                 "frequency space lies on somebody's ray."
        ) as tracker:
            self.wait_until_bookmark("one")
            self.play(
                cloud.dots.animate.set_opacity(0.0),
                # Fully hidden, not merely dimmed: even quiet mini bells cut
                # through the frequency-space labels and add a second curve
                # vocabulary over the continuous magenta field.
                shadow_plots.animate.set_opacity(0.0),
                angle.animate.set_value(angle.get_value() + np.deg2rad(38)),
                Create(converse_axes),
                Create(converse_curve),
                FadeIn(converse_panel_label),
                FadeIn(converse_eq[0], shift=0.05 * UP),
                active_line.animate.set_stroke(opacity=0.85),
                run_time=max(0.7, tracker.time_until_bookmark("define")),
            )
            self.wait_until_bookmark("define")
            self.play(
                FadeIn(converse_eq[1], shift=0.05 * UP),
                run_time=max(0.7, tracker.time_until_bookmark("regroup")),
            )
            self.wait_until_bookmark("regroup")
            self.play(
                FadeIn(converse_eq[2], shift=0.05 * UP),
                run_time=max(0.6, tracker.time_until_bookmark("identity")),
            )
            self.wait_until_bookmark("identity")
            self.play(
                Indicate(converse_eq[2], color=MAGNITUDE, scale_factor=1.04),
                run_time=max(0.7, tracker.time_until_bookmark("trace")),
            )
            self.wait_until_bookmark("trace")

            # --- Beat B: the continuous sweep that grounds the transfer.
            # Two tracers, driven by one ValueTracker, move in lock-step --
            # one along the graph (height), one along the live spoke
            # (brightness) -- while the ray itself is drawn progressively
            # behind the spoke tracer. This is what actually shows height
            # becoming brightness, rather than asserting it over a jump cut.
            t_scale_wheel = SPOKE_RADIUS / CF_T_MAX
            t_samples = np.linspace(0, CF_T_MAX, N_RAY_SEGMENTS + 1)
            h_samples = gaussian_cf(t_samples)
            ray_opacities = [
                float(np.clip(h, 0.0, 1.0)) for h in h_samples[:-1]
            ]

            t_val = ValueTracker(0.0)
            freq_tracer = Dot(radius=0.055).set_stroke(width=0)

            def update_freq_tracer(mob):
                t = t_val.get_value()
                mob.move_to(t * t_scale_wheel * direction())
                mob.set_fill(
                    MAGNITUDE, float(np.clip(gaussian_cf(t), 0.05, 1.0)),
                )

            freq_tracer.add_updater(update_freq_tracer)

            graph_tracer = Dot(radius=0.055).set_stroke(width=0)
            graph_tracer.set_fill(MAGNITUDE, 1.0)

            def update_graph_tracer(mob):
                t = t_val.get_value()
                mob.move_to(converse_axes.c2p(t, float(gaussian_cf(t))))

            graph_tracer.add_updater(update_graph_tracer)

            ray = VGroup(*(
                Line(ORIGIN, ORIGIN) for _ in range(N_RAY_SEGMENTS)
            ))

            def update_ray(mob):
                u = direction()
                tv = t_val.get_value()
                for i, seg in enumerate(mob):
                    seg.put_start_and_end_on(
                        t_samples[i] * t_scale_wheel * u,
                        t_samples[i + 1] * t_scale_wheel * u,
                    )
                    if t_samples[i + 1] <= tv:
                        reveal = 1.0
                    elif t_samples[i] >= tv:
                        reveal = 0.0
                    else:
                        reveal = (
                            (tv - t_samples[i])
                            / (t_samples[i + 1] - t_samples[i])
                        )
                    seg.set_stroke(
                        MAGNITUDE, 4, opacity=ray_opacities[i] * reveal,
                    )

            update_ray(ray)
            ray.add_updater(update_ray)
            self.add(ray, freq_tracer, graph_tracer)
            self.play(
                t_val.animate.set_value(CF_T_MAX),
                run_time=max(2.4, tracker.time_until_bookmark("points")),
                rate_func=linear,
            )
            self.wait_until_bookmark("points")
            self.play(FadeOut(freq_tracer), FadeOut(graph_tracer), run_time=0.3)

            # --- Beat C: three random points, confirmed at a deliberate,
            # one-at-a-time pace -- a beat of its own for each: highlight on
            # the curve, a breath, then the matching brightness on the
            # spoke. The ray already carries the right brightness from the
            # sweep above; this only makes the correspondence explicit.
            u_here = direction()
            example_graph_dots = [
                Dot(
                    converse_axes.c2p(t, float(gaussian_cf(t))), radius=0.065,
                ).set_fill(MAGNITUDE, 1.0).set_stroke(width=0)
                for t in EXAMPLE_TS
            ]
            example_ray_dots = [
                Dot(
                    t * t_scale_wheel * u_here, radius=0.065,
                ).set_fill(
                    MAGNITUDE, float(np.clip(gaussian_cf(t), 0.0, 1.0)),
                )
                .set_stroke(width=0)
                for t in EXAMPLE_TS
            ]
            # A gentle scale-in (not a hard pop) flowing straight into a
            # smoothly arced transfer -- no dead stop in between -- then one
            # clear settle before the next point. The abrupt full-stop
            # micro-pauses this replaced read as a stutter, not a rhythm.
            for gdot, rdot in zip(example_graph_dots, example_ray_dots):
                self.play(FadeIn(gdot, scale=1.2), run_time=0.35, rate_func=smooth)
                self.play(
                    TransformFromCopy(gdot, rdot, path_arc=-PI / 3),
                    run_time=0.55,
                    rate_func=smooth,
                )
                self.wait(0.25)

            example_graph_dots = VGroup(*example_graph_dots)
            example_ray_dots = VGroup(*example_ray_dots)
            self.play(
                FadeOut(converse_curve), FadeOut(converse_axes),
                FadeOut(converse_panel_label), FadeOut(converse_eq),
                FadeOut(example_graph_dots), FadeOut(example_ray_dots),
                active_line.animate.set_stroke(opacity=0.0),
                run_time=0.6,
            )
            self.wait_until_bookmark("rotate")

            # --- Beat D: rotate + sweep, mostly silent. A trail of static
            # rays reveals itself behind the live one as the angle sweeps a
            # full turn, so the fill is watched happening, not declared.
            # Each ray gets a brief brightness/width "pop" exactly as it
            # crosses into being revealed, so the fan reads as coming alive
            # one direction at a time rather than a flat linear wipe.
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
                    reveal = float(np.clip(edge, 0.0, 1.0))
                    pop = 1.0
                    if edge > 1.0:
                        pop = 1.0 + 1.1 * float(
                            np.exp(-10.0 * (edge - 1.0) ** 2)
                        )
                    for seg, base in zip(trail_ray, ray_opacities):
                        seg.set_stroke(
                            MAGNITUDE, 3 * pop, opacity=base * reveal,
                        )

            trail_rays.add_updater(reveal_trail)
            self.add(trail_rays)
            self.play(
                angle.animate.set_value(sweep_start_angle + TAU),
                run_time=max(3.2, tracker.time_until_bookmark("together")),
                rate_func=linear,
            )
            self.freeze(ray, trail_rays)
            self.wait_until_bookmark("together")
            gaussian_field = _field_image(GAUSSIAN_PROFILE, MAGNITUDE)

            # Freeze every origin-anchored updater before the wheel becomes a
            # movable panel. If even one survives, it resumes after the parent
            # transform and snaps its geometry straight back to ORIGIN.
            self.freeze(
                ray, trail_rays, active_line, active_arrow, active_label,
                *shadow_dot_groups,
            )
            cloud.freeze()
            self.play(
                FadeOut(ray), FadeOut(trail_rays), FadeOut(plane),
                FadeOut(active_line), FadeOut(active_arrow),
                FadeOut(active_label), FadeIn(gaussian_field),
                run_time=max(0.8, tracker.get_remaining_duration()),
            )

        # The comparison is field against field. Move the wheel furniture with
        # the left field so it can return to the exact centre later, but hide
        # it here: both panels contain only field, quiet raw points, caption.
        self.play(
            gaussian_field.animate.scale(PANEL_SCALE).shift(
                PANEL_OFFSET * LEFT,
            ),
            wheel_ring.animate.scale(PANEL_SCALE).shift(
                PANEL_OFFSET * LEFT,
            ).set_stroke(opacity=0.0),
            spokes.animate.scale(PANEL_SCALE).shift(
                PANEL_OFFSET * LEFT,
            ).set_stroke(opacity=0.0),
            cloud.dots.animate.scale(PANEL_SCALE).shift(
                PANEL_OFFSET * LEFT,
            ).set_opacity(0.30),
            run_time=1.0,
            rate_func=smooth,
        )

        left_caption = ty.caption("Gaussian cloud").set_color(MAGNITUDE)
        left_caption.next_to(gaussian_field, DOWN, buff=0.16)
        right_caption = ty.caption("ring cloud").set_color(RIVAL)

        ring_points = data.ring_2d(
            n=220, radius=np.sqrt(2.0), jitter=0.0, seed=31,
        )
        gaussian_rival_points = data.gaussian_2d(n=220, seed=76)
        gaussian_rival_points = (
            (gaussian_rival_points - gaussian_rival_points.mean(axis=0))
            / gaussian_rival_points.std(axis=0)
        )
        ring_scene_points = (
            ring_points * SCALE * PANEL_SCALE
            + PANEL_OFFSET * RIGHT[:2]
        )
        rival_gaussian_scene_points = (
            gaussian_rival_points * SCALE * PANEL_SCALE
            + PANEL_OFFSET * RIGHT[:2]
        )
        rival_dots = VGroup(*(
            Dot(
                np.array([point[0], point[1], 0.0]), radius=DOT_RADIUS * 0.8,
            # Bright while the ring is the only thing on this side -- the
            # narration describes its shape before its field exists, and the
            # left panel has a lit field to sit on while this one has nothing.
            # Dropped to match the left panel's 0.30 once the field arrives.
            ).set_fill(CLOUD, 0.75).set_stroke(width=0)
            for point in ring_scene_points
        ))
        rival_field = _field_image(RING_PROFILE, RIVAL)
        rival_field.scale(PANEL_SCALE).move_to(PANEL_OFFSET * RIGHT)
        right_caption.next_to(rival_field, DOWN, buff=0.16)
        same_distribution_caption = ty.caption("same distribution").set_color(
            MAGNITUDE,
        )
        same_distribution_caption.move_to(right_caption)

        uniqueness_recall = ty.maths(
            R"\varphi_X=\varphi_Y\ \Longrightarrow\ X\overset{d}{=}Y",
            size=ty.EQ, color=INK,
        ).to_edge(DOWN, buff=0.48)
        layout.fit_in_frame(uniqueness_recall)

        morph = ValueTracker(0.0)
        point_delays = np.linspace(0.0, 0.18, len(rival_dots))

        def move_rival_points(group):
            s = morph.get_value()
            for dot, start, end, delay in zip(
                group,
                ring_scene_points,
                rival_gaussian_scene_points,
                point_delays,
            ):
                local = float(np.clip((s - delay) / (1.0 - delay), 0.0, 1.0))
                local = smooth(local)
                point = (1.0 - local) * start + local * end
                dot.move_to(np.array([point[0], point[1], 0.0]))

        def morph_rival_field(image):
            s = morph.get_value()
            # Blend the signed characteristic fields first. Taking magnitudes
            # before this line would erase J_0's negative lobes and wash the
            # nulls out instead of letting them close during transport.
            signed = (1.0 - s) * RING_PROFILE + s * GAUSSIAN_PROFILE
            image.pixel_array[..., 3] = _field_alpha(signed)

        rival_dots.add_updater(move_rival_points)
        rival_field.add_updater(morph_rival_field)

        with self.voiceover(
            text="<bookmark mark='rival'/>Now a second cloud, shaped nothing "
                 "like the first — its points sit out around a ring instead "
                 "of piling up in the middle. It has the same mean and the "
                 "same covariance as the Gaussian, so no test built on those "
                 "two could tell them apart. <bookmark mark='rivalfield'/>"
                 "Run the same construction on it, every direction and every "
                 "distance, and its field fills in too — but it fills in with "
                 "bright rings and dark gaps, where the Gaussian has one "
                 "smooth peak. <bookmark mark='push'/>Push its points until "
                 "they sit the way the Gaussian's do, <bookmark mark='match'/>"
                 "and the field follows them the whole way: the gaps close, "
                 "the rings wash out, and the two only agree once the clouds "
                 "themselves agree. <bookmark mark='unique'/>That is the "
                 "uniqueness theorem — distributions that share a "
                 "characteristic function at every point are the same "
                 "distribution."
        ) as tracker:
            self.wait_until_bookmark("rival")
            self.play(
                FadeIn(left_caption, shift=0.04 * UP),
                FadeIn(rival_dots),
                FadeIn(right_caption, shift=0.04 * UP),
                run_time=max(0.8, tracker.time_until_bookmark("rivalfield")),
            )
            self.wait_until_bookmark("rivalfield")
            self.play(
                FadeIn(rival_field),
                rival_dots.animate.set_fill(CLOUD, 0.30),
                run_time=max(0.9, tracker.time_until_bookmark("push")),
            )
            self.wait_until_bookmark("push")
            push_budget = max(1.2, tracker.time_until_bookmark("match"))
            self.play(
                Indicate(rival_dots, color=RIVAL, scale_factor=1.025),
                run_time=min(0.65, push_budget * 0.35),
            )
            self.play(
                morph.animate.set_value(0.18),
                run_time=max(0.55, tracker.time_until_bookmark("match")),
                rate_func=linear,
            )
            self.wait_until_bookmark("match")
            morph_budget = max(1.8, tracker.time_until_bookmark("unique"))
            self.play(
                morph.animate.set_value(0.92),
                run_time=morph_budget - 0.8,
                rate_func=linear,
            )
            self.play(
                morph.animate.set_value(0.98),
                FadeOut(right_caption),
                run_time=0.4,
                rate_func=linear,
            )
            self.play(
                morph.animate.set_value(1.0),
                FadeIn(same_distribution_caption),
                run_time=0.4,
                rate_func=linear,
            )
            self.wait_until_bookmark("unique")
            self.freeze(rival_dots, rival_field)
            self.play(
                FadeIn(uniqueness_recall, shift=0.05 * UP),
                run_time=max(0.7, tracker.get_remaining_duration()),
            )

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
        ).next_to(cw_statement, DOWN, buff=0.38, aligned_edge=RIGHT)

        with self.voiceover(
            text="<bookmark mark='never'/>But that field was never measured "
                 "directly. Every value in it arrived from a shadow: one "
                 "direction, one distance along it. <bookmark mark='cw'/>So "
                 "if two clouds cast the same shadow in every single "
                 "direction, they fill in the same field — and uniqueness "
                 "finishes the argument for us. They are the same cloud. "
                 "<bookmark mark='name'/>That step, from every "
                 "one-dimensional projection up to the joint distribution, "
                 "is the Cramér–Wold theorem. <bookmark mark='specialize'/>"
                 "For the target we're matching, each shadow's fingerprint "
                 "is the standard Gaussian's own, e to the minus t squared "
                 "over two. <bookmark mark='pick'/>And any single point of "
                 "the field is fixed the same way: its distance from the "
                 "origin gives t, its direction gives u. <bookmark "
                 "mark='resolve'/>So that fingerprint belongs to exactly one "
                 "cloud — <bookmark mark='conclude'/>Z itself, standard "
                 "Gaussian in every dimension. <bookmark mark='payoff'/>"
                 "Which is what the theorem buys us: pinning down a "
                 "distribution in D dimensions never requires looking at it "
                 "in D dimensions — a family of one-dimensional shadows is "
                 "enough."
        ) as tracker:
            self.wait_until_bookmark("never")
            self.play(
                FadeIn(cw_statement, shift=0.05 * UP),
                FadeIn(quantifier_box),
                run_time=max(0.8, tracker.time_until_bookmark("cw")),
            )
            self.wait_until_bookmark("cw")
            self.play(
                Indicate(quantifier_box, color=DIRECTION, scale_factor=1.08),
                run_time=max(0.8, tracker.time_until_bookmark("name")),
            )
            self.wait_until_bookmark("name")
            self.play(
                gaussian_field.animate.scale(1.0 / PANEL_SCALE).shift(
                    PANEL_OFFSET * RIGHT,
                ),
                wheel_ring.animate.scale(1.0 / PANEL_SCALE).shift(
                    PANEL_OFFSET * RIGHT,
                ).set_stroke(opacity=0.35),
                spokes.animate.scale(1.0 / PANEL_SCALE).shift(
                    PANEL_OFFSET * RIGHT,
                ).set_stroke(opacity=0.14),
                cloud.dots.animate.scale(1.0 / PANEL_SCALE).shift(
                    PANEL_OFFSET * RIGHT,
                ),
                FadeOut(rival_field), FadeOut(rival_dots),
                FadeOut(left_caption), FadeOut(same_distribution_caption),
                FadeOut(uniqueness_recall), FadeOut(quantifier_box),
                FadeIn(cw_label, shift=0.05 * UP),
                run_time=max(1.0, tracker.time_until_bookmark("specialize")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("specialize")

            # The claim about every Gaussian shadow is visible before the
            # narration specialises the general theorem to this target.
            specialize_eq = ty.maths(
                R"\varphi_{u^\top Z}(t)=e^{-t^2/2}",
                size=ty.EQ,
                color=MAGNITUDE,
            ).to_edge(UP, buff=0.7)
            layout.fit_in_frame(specialize_eq)
            specialize_window = tracker.time_until_bookmark("pick")
            self.play(
                FadeOut(cw_statement), FadeOut(cw_label),
                FadeIn(specialize_eq, shift=0.06 * UP),
                # Settle before "any single point" begins. A minimum runtime
                # here can overrun the bookmark and steal the point's window.
                run_time=max(
                    1 / config.frame_rate, specialize_window - 0.5,
                ),
            )
            self.wait_until_bookmark("pick")

            example_angle = sweep_start_angle + np.deg2rad(128)
            example_t = 2.3
            example_u = np.array([
                np.cos(example_angle), np.sin(example_angle), 0.0,
            ])
            example_point = example_t * t_scale_wheel * example_u
            example_value = float(np.exp(-0.5 * example_t ** 2))
            example_line = DashedLine(ORIGIN, example_point, dash_length=0.06)
            example_line.set_stroke(INK, 1.8, opacity=0.85)
            example_dot = Dot(example_point, radius=0.05)
            example_dot.set_fill(MAGNITUDE, 1.0).set_stroke(width=0)
            example_label = ty.maths(R"\xi", size=ty.EQ, color=INK)
            example_label.next_to(example_dot, UR, buff=0.06)
            example_reading = ty.maths(
                R"t=\|\xi\|,\ \ u=\xi/\|\xi\|",
                size=ty.LABEL,
                color=INK,
            )
            example_value_label = ty.maths(
                Rf"\varphi_Z(\xi)=e^{{-t^2/2}}\approx {example_value:.2f}",
                size=ty.LABEL,
                color=MAGNITUDE,
            )
            example_readout = VGroup(
                example_reading, example_value_label,
            ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            example_readout.to_corner(DL, buff=0.50)
            layout.fit_in_frame(example_readout)

            # These are short reveals, not fractions of the full spoken
            # window. The value then owns the remaining time and settles for
            # several seconds before "So that fingerprint..." resolves it.
            self.play(
                Create(example_line),
                FadeIn(example_dot, scale=0.6),
                FadeIn(example_label),
                run_time=0.80,
            )
            self.play(
                FadeIn(example_reading, shift=0.04 * UP),
                run_time=0.75,
            )
            self.play(
                FadeIn(example_value_label, shift=0.04 * UP),
                run_time=0.75,
            )
            self.wait_until_bookmark("resolve")

            freq_tag = ty.caption("frequency space").to_corner(UL, buff=0.5)
            field_label = ty.maths(
                R"\varphi_Z(\xi)=e^{-\|\xi\|^2/2}",
                size=ty.EQ,
                color=MAGNITUDE,
            ).to_edge(UP, buff=1.15)

            # Two steps keep the point reading legible until it has done its
            # job, then let the already-resolved field take over cleanly.
            resolve_budget = max(1.2, tracker.time_until_bookmark("conclude"))
            self.play(
                FadeOut(example_line), FadeOut(example_dot),
                FadeOut(example_label), FadeOut(example_reading),
                FadeOut(example_value_label), FadeOut(specialize_eq),
                run_time=resolve_budget * 0.4,
            )
            self.play(
                FadeIn(freq_tag),
                FadeIn(field_label, shift=0.08 * UP),
                run_time=max(0.6, tracker.time_until_bookmark("conclude")),
            )
            self.wait_until_bookmark("conclude")

            conclusion = ty.maths(
                R"Z\sim\mathcal N(0,I_D)",
                size=ty.EQ_DISPLAY,
                color=INK,
                isolate=[R"\mathcal N(0,I_D)"],
            )
            conclusion.set_color_by_tex(R"\mathcal N(0,I_D)", TARGET)
            conclusion.to_corner(UL, buff=0.50)
            # Two steps, not one crossfade. `conclusion` lands in the same
            # top-left corner `freq_tag` occupies and the closing wheel rises
            # straight through `field_label`, so fading the old furniture out
            # while the new image faded in ghosted "frequency space" behind
            # "Z ~ N(0, I_D)" and smeared the field equation across the top of
            # the wheel. Clear the frequency-space frame first, then build the
            # closing image against a clean one -- the same fix, and the same
            # reason, as the ring-field transition further up.
            closing_budget = max(
                2 / config.frame_rate,
                tracker.time_until_bookmark("payoff"),
            )
            self.play(
                FadeOut(gaussian_field), FadeOut(freq_tag),
                FadeOut(field_label),
                run_time=closing_budget * 0.35,
            )
            self.play(
                shadow_baselines.animate.set_stroke(opacity=0.52),
                VGroup(*shadow_dot_groups).animate.set_fill(opacity=0.66),
                target_curves.animate.set_stroke(opacity=0.78).set_fill(
                    opacity=0.0,
                ),
                wheel_ring.animate.set_stroke(opacity=0.35),
                spokes.animate.set_stroke(opacity=0.14),
                cloud.dots.animate.set_opacity(0.58),
                FadeIn(conclusion, shift=0.08 * UP),
                run_time=closing_budget * 0.65,
                rate_func=smooth,
            )
            self.wait_until_bookmark("payoff")
            self.wait(tracker.get_remaining_duration())

        self.freeze(
            gaussian_field, wheel_ring, spokes, cloud.dots, conclusion,
            *shadow_dot_groups,
        )
        cloud.freeze()
        self.settle_frame()
