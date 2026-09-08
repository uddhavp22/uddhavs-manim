"""Chapter C.07 -- every direction is a sphere, so the loss samples M of them.

Opens on C06's last frame: the whitened Gaussian cloud in the wheel, eight rim
shadows with their bells, u at 45 degrees, ``Z ~ N(0, I_D)``.

What the viewer is shown, in order, and why:

  * the spokes densify to a solid disc: "every direction" is a cost, not a
    word, and in D dimensions it is a sphere with no single sweep;
  * one draw (a Gaussian vector scaled to length one) and then fifty of
    them pushed to the ring, landing evenly, so "round" is seen rather
    than asserted;
  * the same sample flown onto one sampled direction's rim plot and scored,
    then a second direction scoring lower;
  * the score revealed as a function of direction: u sweeps a half turn and
    a pen traces score(u) in a panel at the right, the two readings sit on
    the curve, and a dashed line marks the curve's mean, the average over
    every direction, which is what the loss wants;
  * thirty more draws read the curve where they land; the running average
    settles against the dashed line; M is named once that has been watched;
  * a different thirty-two land elsewhere and average almost the same; the
    curve itself belongs to the batch, and its mean is not zero.

Geometry shared with C06 and C09 is in ``common.wheel``; every number on
screen comes from ``common.data`` draws through ``common.score`` and is
checked in ``facts.py``.

Render:
    SIGREG_VOICE=eleven ./render.sh \
        projects/sigreg_explainer/chapterC/c07_sampling_directions.py C07 -qh
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.cloud import CloudRig
from common.palette import (
    ACCENT, AVERAGE, AXIS, CLOUD, DIRECTION, GRID, INK, MUTED, TARGET,
)
from common.score import EP_GRID, EP_LAMBDA, epps_pulley
from common import type as ty
from common.wheel import (
    ACTIVE_ARROW_LENGTH, COLLAPSED_DIRECTION, DOT_RADIUS, MINI_DOT_RADIUS,
    MINI_HALF_WIDTH, MINI_SAMPLE_COUNT, MINI_STACK_MAX, MINI_STACK_STEP,
    MINI_X_SCALE, N_SHADOWS, N_SPOKES, SCALE, SPOKE_RADIUS, WHEEL_RADIUS,
)

M_FIRST_WAVE = 8
M_TOTAL = data.DIRECTION_COUNT
DENSE_SPOKE_COUNTS = (32, 64, 256)

# The wheel slides left when the score panel needs the right third.
WHEEL_SHIFT = np.array([-1.9, 0.0, 0.0])
PANEL_CENTRE = np.array([4.25, 0.05, 0.0])
PANEL_WIDTH = 4.2
PANEL_HEIGHT = 3.3
SCORE_MAX = 0.2
CURVE_STEP_DEG = 0.5

RECIPE_CENTRE = np.array([-5.35, 0.35, 0.0])
CLOUD_OPACITY = 0.88
DIM_CLOUD_OPACITY = 0.32
SPRAY_RADIUS = 0.038
LANDING_RADIUS = 0.05


def _standardized_isotropic_points(n: int) -> np.ndarray:
    points = data.whiten(data.gaussian_2d(n=n))
    return np.column_stack([points, np.zeros(n)])


def score_of(points_2d: np.ndarray, u: np.ndarray) -> float:
    return epps_pulley(points_2d @ u, EP_LAMBDA, EP_GRID)


def unit3(u2: np.ndarray) -> np.ndarray:
    return np.array([u2[0], u2[1], 0.0])


def angle_deg(u2: np.ndarray) -> float:
    """Direction as an angle in [0, 180): u and -u give the same shadow."""
    return float(np.degrees(np.arctan2(u2[1], u2[0])) % 180.0)


class C07(ActScene, ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=0.0, theta=-90 * DEGREES, frame_center=ORIGIN,
        )

        # --- C06's last frame, rebuilt from the same seeds -----------------
        n_points = len(data.diagonal_2d())
        gaussian_points = _standardized_isotropic_points(n_points)
        points_2d = gaussian_points[:, :2]
        cloud = CloudRig(
            gaussian_points, scale=SCALE, dot_colour=CLOUD,
            dot_radius=DOT_RADIUS,
        )
        cloud.mount(self, axes=False, ellipsoid=False)
        cloud.dots.set_opacity(CLOUD_OPACITY)
        cloud.freeze()

        wheel_ring = Circle(radius=WHEEL_RADIUS).set_stroke(
            GRID, 1.5, opacity=0.35,
        )

        def diameters(count: int, opacity: float, skip_every: int = 0):
            """`count` diameters through the origin; with `skip_every`, only
            the ones a coarser set of that stride does not already draw."""
            angles = COLLAPSED_DIRECTION + np.linspace(
                0.0, np.pi, count, endpoint=False,
            )
            keep = [
                i for i in range(count)
                if not skip_every or i % skip_every
            ]
            return VGroup(*(
                Line(
                    -SPOKE_RADIUS * np.array([np.cos(angles[i]), np.sin(angles[i]), 0.0]),
                    SPOKE_RADIUS * np.array([np.cos(angles[i]), np.sin(angles[i]), 0.0]),
                ).set_stroke(DIRECTION, 1.1, opacity=opacity)
                for i in keep
            ))

        spokes = diameters(N_SPOKES, 0.10)
        self.add(wheel_ring, spokes)

        shadow_indices = np.linspace(
            0, n_points - 1, MINI_SAMPLE_COUNT, dtype=int,
        )
        sample_2d = points_2d[shadow_indices]

        def rim_plot(radial: np.ndarray, centre_of_wheel=ORIGIN) -> VGroup:
            """C06's rim plot for a unit direction: baseline tangent to the
            wheel, the sample's shadow stacked outward, the target bell."""
            tangent = np.array([-radial[1], radial[0], 0.0])
            centre = centre_of_wheel + WHEEL_RADIUS * radial
            baseline = Line(
                centre - MINI_HALF_WIDTH * tangent,
                centre + MINI_HALF_WIDTH * tangent,
            ).set_stroke(AXIS, 1.1, opacity=0.60)
            positions = (sample_2d @ radial[:2]) * MINI_X_SCALE
            levels = np.minimum(
                np.asarray(layout.stack_levels(positions, 0.046), dtype=float),
                MINI_STACK_MAX,
            )
            dots = VGroup(*(
                Dot(radius=MINI_DOT_RADIUS).set_fill(DIRECTION, 0.90)
                .set_stroke(width=0)
                .move_to(
                    centre
                    + float(position) * tangent
                    + (level + 0.75) * MINI_STACK_STEP * radial
                )
                for position, level in zip(positions, levels)
            ))
            bell = VMobject().set_stroke(TARGET, 2.0, opacity=0.85)
            bell.set_fill(opacity=0.0)
            xs = np.linspace(-3.2, 3.2, 121)
            edge = np.exp(-0.5 * 3.2 ** 2)
            bell.set_points_smoothly([
                centre
                + x * MINI_X_SCALE * tangent
                + 0.33 * (np.exp(-0.5 * x * x) - edge) / (1.0 - edge) * radial
                for x in xs
            ])
            return VGroup(baseline, dots, bell)

        shadow_angles = np.deg2rad(45 * np.arange(N_SHADOWS))
        family = VGroup(*(
            rim_plot(np.array([np.cos(a), np.sin(a), 0.0]))
            for a in shadow_angles
        ))
        self.add(family)

        inherited_u = unit3(np.array([np.cos(np.deg2rad(45.0)), np.sin(np.deg2rad(45.0))]))
        active_arrow = Arrow(
            ORIGIN, ACTIVE_ARROW_LENGTH * inherited_u, buff=0.0,
            stroke_width=5.0, max_tip_length_to_length_ratio=0.18,
        ).set_color(DIRECTION).set_opacity(0.95)
        active_label = ty.maths("u", size=ty.EQ, color=DIRECTION)
        active_label.move_to(
            ACTIVE_ARROW_LENGTH * inherited_u
            + 0.20 * np.array([-inherited_u[1], inherited_u[0], 0.0]),
        )
        active_line = Line(
            -2.56 * inherited_u, 2.56 * inherited_u,
        ).set_stroke(DIRECTION, 2.0, opacity=0.55)
        self.add(active_line, active_arrow, active_label)

        conclusion = ty.maths(
            R"Z\sim\mathcal N(0,I_D)", size=ty.EQ_DISPLAY, color=INK,
            isolate=[R"\mathcal N(0,I_D)"],
        )
        conclusion.set_color_by_tex(R"\mathcal N(0,I_D)", TARGET)
        conclusion.to_corner(UL, buff=0.50)
        self.add(conclusion)

        # --- the numbers this scene shows, computed once -------------------
        theta_deg = np.arange(0.0, 180.0 + CURVE_STEP_DEG / 2, CURVE_STEP_DEG)
        curve = np.array([
            score_of(points_2d, np.array([np.cos(np.deg2rad(d)), np.sin(np.deg2rad(d))]))
            for d in theta_deg
        ])
        curve_mean = float(curve[:-1].mean())

        def curve_at(deg: float) -> float:
            return float(np.interp(deg % 180.0, theta_deg, curve))

        g_vectors, u_vectors = data.sampled_directions(M_TOTAL)
        scores = np.array([score_of(points_2d, u) for u in u_vectors])
        degrees_of = np.array([angle_deg(u) for u in u_vectors])
        running_mean = np.cumsum(scores) / np.arange(1, M_TOTAL + 1)
        _g2, u_redraw = data.sampled_directions(M_TOTAL, seed=data.REDRAW_SEED)
        scores_redraw = np.array([score_of(points_2d, u) for u in u_redraw])
        degrees_redraw = np.array([angle_deg(u) for u in u_redraw])
        running_redraw = np.cumsum(scores_redraw) / np.arange(1, M_TOTAL + 1)
        assert scores[1] < scores[0] - 0.04, scores[:2]
        assert curve.max() < SCORE_MAX, curve.max()

        # ---------------------------------------------------------------
        # P1: every direction is another shadow, and there is no end of them.
        # ---------------------------------------------------------------
        dense_sets = [
            diameters(32, 0.10, skip_every=2),
            diameters(64, 0.12, skip_every=2),
            diameters(256, 0.14, skip_every=4),
        ]

        with self.voiceover(
            text="So the test has to pass in every direction. The trouble "
                 "is that <bookmark mark='dense'/>every direction is another "
                 "shadow we would have to score, <bookmark mark='more'/>and "
                 "there is no end of them. <bookmark mark='sphere'/>In D "
                 "dimensions, the directions make a whole sphere."
        ) as tracker:
            self.play(
                FadeOut(conclusion, shift=0.08 * UP),
                FadeOut(active_line), FadeOut(active_arrow), FadeOut(active_label),
                run_time=min(0.8, max(0.4, tracker.time_until_bookmark("dense"))),
            )
            self.wait_until_bookmark("dense")
            dense_budget = max(2.0, tracker.time_until_bookmark("more"))
            self.play(
                LaggedStart(*(FadeIn(line) for line in dense_sets[0]), lag_ratio=0.05),
                run_time=dense_budget * 0.45,
            )
            self.play(
                LaggedStart(*(FadeIn(line) for line in dense_sets[1]), lag_ratio=0.03),
                run_time=dense_budget * 0.45,
            )
            self.wait_until_bookmark("more")
            more_budget = max(2.4, tracker.time_until_bookmark("sphere"))
            self.play(
                LaggedStart(*(FadeIn(line) for line in dense_sets[2]), lag_ratio=0.004),
                FadeOut(family),
                run_time=more_budget * 0.9,
            )
            self.remove(family)
            self.wait_until_bookmark("sphere")
            self.play(
                FadeOut(spokes), *(FadeOut(group) for group in dense_sets),
                wheel_ring.animate.set_stroke(GRID, 2.6, opacity=1.0),
                run_time=min(1.2, max(0.6, tracker.get_remaining_duration() * 0.5)),
            )
            self.remove(spokes, *dense_sets)
        self.inspect(0.8)

        # ---------------------------------------------------------------
        # P2: one draw, then fifty; round lands evenly.
        # ---------------------------------------------------------------
        def gaussian_arrow(g: np.ndarray) -> Arrow:
            return Arrow(
                ORIGIN, SCALE * unit3(g), buff=0.0, stroke_width=4.5,
                max_tip_length_to_length_ratio=0.22,
            ).set_color(DIRECTION).set_opacity(0.9)

        def unit_arrow(u: np.ndarray) -> Arrow:
            return Arrow(
                ORIGIN, WHEEL_RADIUS * unit3(u), buff=0.0, stroke_width=4.5,
                max_tip_length_to_length_ratio=0.12,
            ).set_color(DIRECTION).set_opacity(0.95)

        def landing(u: np.ndarray) -> Dot:
            return Dot(radius=0.07).set_fill(DIRECTION, 1.0).set_stroke(
                width=0,
            ).move_to(WHEEL_RADIUS * unit3(u))

        def tip_label(text: str, end: np.ndarray, u: np.ndarray):
            normal = np.array([-u[1], u[0], 0.0])
            side = normal if normal[1] >= 0 else -normal
            return ty.maths(text, size=ty.EQ, color=DIRECTION).move_to(
                end + 0.30 * side,
            )

        def spray(points: np.ndarray, colour: str) -> tuple[VGroup, VGroup]:
            """Dots at the draws and the same dots pushed out to the ring."""
            dots = VGroup(*(
                Dot(radius=SPRAY_RADIUS).set_fill(colour, 0.9).set_stroke(width=0)
                .move_to(SCALE * unit3(p))
                for p in points
            ))
            pushed = VGroup(*(
                Dot(radius=LANDING_RADIUS).set_fill(colour, 0.95).set_stroke(width=0)
                .move_to(WHEEL_RADIUS * unit3(p / np.linalg.norm(p)))
                for p in points
            ))
            return dots, pushed

        recipe_top = ty.maths(
            R"u=\frac{g}{\|g\|}", size=ty.EQ, color=INK, isolate=["u"],
        )
        recipe_top.set_color_by_tex("u", DIRECTION)
        recipe_bottom = ty.maths(
            R"g\sim\mathcal N(0,I_D)", size=ty.EQ, color=INK,
        )
        recipe = VGroup(recipe_top, recipe_bottom).arrange(DOWN, buff=0.32)
        recipe.move_to(RECIPE_CENTRE)
        layout.fit_in_frame(recipe, margin=0.45)

        g1_arrow = gaussian_arrow(g_vectors[0])
        g1_label = tip_label("g", SCALE * unit3(g_vectors[0]), u_vectors[0])
        u1_arrow = unit_arrow(u_vectors[0])
        u1_dot = landing(u_vectors[0])
        u1_label = tip_label("u_1", WHEEL_RADIUS * unit3(u_vectors[0]), u_vectors[0])
        round_dots, round_pushed = spray(data.direction_spray(), DIRECTION)

        with self.voiceover(
            text="So we sample instead. <bookmark mark='draw'/>To draw a "
                 "direction, we take a random vector with a Gauss-ian in "
                 "every coordinate, <bookmark mark='norm'/>and scale it to "
                 "length one, so it lands on the ring. <bookmark "
                 "mark='spray'/>If we do that fifty times, the landings "
                 "spread evenly all the way round. <bookmark mark='round'/>"
                 "That is because a Gauss-ian is round, so it has no "
                 "preferred direction."
        ) as tracker:
            self.wait_until_bookmark("draw")
            draw_budget = max(2.0, tracker.time_until_bookmark("norm"))
            self.play(
                cloud.dots.animate.set_opacity(DIM_CLOUD_OPACITY),
                run_time=min(0.5, draw_budget * 0.2),
            )
            self.play(
                GrowArrow(g1_arrow),
                FadeIn(g1_label, shift=0.05 * UP),
                run_time=min(1.0, draw_budget * 0.4),
            )
            self.wait_until_bookmark("norm")
            norm_budget = max(2.4, tracker.time_until_bookmark("spray"))
            self.play(
                FadeIn(recipe_top, shift=0.06 * UP),
                run_time=min(0.5, norm_budget * 0.2),
            )
            # Same direction, new length: the arrow rides out to the ring.
            self.play(
                Transform(g1_arrow, u1_arrow),
                FadeOut(g1_label),
                run_time=min(1.2, norm_budget * 0.45),
                rate_func=smooth,
            )
            self.play(
                GrowFromCenter(u1_dot), FadeIn(u1_label),
                run_time=min(0.5, norm_budget * 0.2),
            )
            self.wait_until_bookmark("spray")
            spray_budget = max(3.4, tracker.time_until_bookmark("round"))
            self.play(
                LaggedStart(*(GrowFromCenter(d) for d in round_dots), lag_ratio=0.02),
                run_time=spray_budget * 0.4,
            )
            self.play(
                LaggedStart(*(
                    Transform(d, target) for d, target in zip(round_dots, round_pushed)
                ), lag_ratio=0.01),
                run_time=spray_budget * 0.6,
            )
            self.wait_until_bookmark("round")
            self.play(
                FadeIn(recipe_bottom, shift=0.06 * UP),
                wheel_ring.animate(rate_func=there_and_back).set_stroke(
                    DIRECTION, 3.0, opacity=1.0,
                ),
                run_time=min(1.4, max(0.8, tracker.get_remaining_duration() * 0.5)),
            )
        self.inspect(0.8)
        self.play(FadeOut(round_dots), run_time=0.6)
        self.remove(u1_arrow, round_dots)
        u1_arrow = g1_arrow  # the transformed instance is the one on screen

        # ---------------------------------------------------------------
        # P3: one direction, one number; a second scores lower.
        # ---------------------------------------------------------------
        def project_onto(plot: VGroup, budget: float):
            """Fly the sample points onto the plot, then swap in its dots."""
            baseline, dots, _bell = plot
            flight = VGroup(*(cloud.dots[i].copy() for i in shadow_indices))
            flight.set_opacity(CLOUD_OPACITY)
            self.add(flight)
            self.play(
                FadeIn(baseline),
                LaggedStart(*(
                    Transform(dot, target.copy())
                    for dot, target in zip(flight, dots)
                ), lag_ratio=0.01),
                run_time=budget,
            )
            self.add(dots)
            self.remove(flight, *flight)

        def score_readout(index: int, u: np.ndarray) -> VGroup:
            """``score(u_k) = value`` beside the plot, on the side that keeps
            it away from the frame's top and bottom edges."""
            radial = unit3(u)
            tangent = np.array([-radial[1], radial[0], 0.0])
            label = ty.maths(
                Rf"\operatorname{{score}}(u_{index})=", size=ty.EQ,
                color=DIRECTION,
            )
            number = ty.maths(f"{scores[index - 1]:.3f}", size=ty.EQ, color=DIRECTION)
            group = VGroup(label, number).arrange(RIGHT, buff=0.12)
            base = WHEEL_RADIUS * radial + 0.45 * radial
            candidates = [base + 2.15 * tangent, base - 2.15 * tangent]
            group.move_to(min(candidates, key=lambda p: abs(p[1])))
            layout.fit_in_frame(group, margin=0.45)
            return group

        plot1 = rim_plot(unit3(u_vectors[0]))
        plot2 = rim_plot(unit3(u_vectors[1]))
        readout1 = score_readout(1, u_vectors[0])
        readout2 = score_readout(2, u_vectors[1])
        u2_arrow = unit_arrow(u_vectors[1])
        u2_dot = landing(u_vectors[1])
        u2_label = tip_label("u_2", WHEEL_RADIUS * unit3(u_vectors[1]), u_vectors[1])

        with self.voiceover(
            text="<bookmark mark='project'/>Now if we project the cloud "
                 "onto that direction, we get a shadow, and we can score it "
                 "against the bell the way we already do. <bookmark "
                 "mark='gap'/>The score measures the mismatch, <bookmark "
                 "mark='score1'/>so this direction gives us one number. "
                 "<bookmark mark='second'/>If we draw a second direction and "
                 "do the same, <bookmark mark='score2'/>we get a lower "
                 "score, because its shadow is different."
        ) as tracker:
            self.wait_until_bookmark("project")
            project_budget = max(2.6, tracker.time_until_bookmark("gap"))
            self.play(
                cloud.dots.animate.set_opacity(CLOUD_OPACITY),
                run_time=min(0.4, project_budget * 0.15),
            )
            project_onto(plot1, min(1.6, project_budget * 0.45))
            self.play(Create(plot1[2]), run_time=min(0.9, project_budget * 0.3))
            self.wait_until_bookmark("gap")
            self.play(
                Indicate(plot1[1], color=ACCENT, scale_factor=1.12),
                Indicate(plot1[2], color=ACCENT, scale_factor=1.06),
                run_time=min(1.2, max(0.6, tracker.time_until_bookmark("score1"))),
            )
            self.wait_until_bookmark("score1")
            self.play(
                FadeIn(readout1, shift=0.06 * UP),
                run_time=min(0.6, max(0.3, tracker.time_until_bookmark("second"))),
            )
            self.wait_until_bookmark("second")
            second_budget = max(1.6, tracker.time_until_bookmark("score2"))
            self.play(
                u1_arrow.animate.set_opacity(0.45),
                u1_label.animate.set_opacity(0.6),
                u1_dot.animate.set_fill(opacity=0.6),
                GrowArrow(u2_arrow),
                run_time=min(1.0, second_budget * 0.6),
            )
            self.play(
                GrowFromCenter(u2_dot), FadeIn(u2_label),
                run_time=min(0.4, second_budget * 0.25),
            )
            self.wait_until_bookmark("score2")
            score2_budget = max(2.4, tracker.get_remaining_duration())
            project_onto(plot2, min(1.0, score2_budget * 0.35))
            self.play(Create(plot2[2]), run_time=min(0.6, score2_budget * 0.25))
            self.play(
                FadeIn(readout2, shift=0.06 * UP),
                run_time=min(0.5, score2_budget * 0.2),
            )
        self.inspect(0.8)

        # ---------------------------------------------------------------
        # P4: the score is a function of direction.
        # ---------------------------------------------------------------
        wheel_group = VGroup(
            wheel_ring, plot1, plot2, u1_arrow, u1_dot, u1_label,
            u2_arrow, u2_dot, u2_label, readout1, readout2,
        )
        wheel_centre = WHEEL_SHIFT.copy()

        axes = Axes(
            x_range=[0, 180, 90], y_range=[0, SCORE_MAX, 0.1],
            x_length=PANEL_WIDTH, y_length=PANEL_HEIGHT,
            axis_config={
                "stroke_color": AXIS, "stroke_width": 1.8,
                "include_tip": False, "include_ticks": True,
                "tick_size": 0.06,
            },
        ).move_to(PANEL_CENTRE)
        x_labels = VGroup(*(
            ty.maths(Rf"{d}^\circ", size=ty.TICK, color=MUTED).next_to(
                axes.c2p(d, 0), DOWN, buff=0.16,
            )
            for d in (0, 90, 180)
        ))
        y_labels = VGroup(*(
            ty.maths(text, size=ty.TICK, color=MUTED).next_to(
                axes.c2p(0, value), LEFT, buff=0.14,
            )
            for value, text in ((0.0, "0"), (0.1, "0.1"), (0.2, "0.2"))
        ))
        x_title = ty.label("direction of u", MUTED).next_to(x_labels, DOWN, buff=0.18)
        x_title.align_to(axes.c2p(0, 0), LEFT)
        caption_y = axes.c2p(0, SCORE_MAX)[1] + 0.78

        def small_readout(name: str, value: float, colour: str) -> VGroup:
            """A labelled number at LABEL size, for the row above the panel."""
            group = VGroup(
                ty.maths(name + "=", size=ty.LABEL, color=colour),
                DecimalNumber(value, num_decimal_places=3, font_size=ty.LABEL)
                .set_color(colour),
            )
            return group.arrange(RIGHT, buff=0.10, aligned_edge=DOWN)

        y_title = ty.label("score", MUTED).next_to(axes.c2p(0, SCORE_MAX), UP, buff=0.18)
        y_title.align_to(y_labels, LEFT)
        panel = VGroup(axes, x_labels, y_labels, x_title, y_title)
        layout.fit_in_frame(panel, margin=0.45)

        curve_points = [axes.c2p(d, s) for d, s in zip(theta_deg, curve)]
        sweep = ValueTracker(0.0)

        def partial_curve():
            frac = float(np.clip(sweep.get_value() / 180.0, 0.0, 1.0))
            count = max(2, int(round(frac * (len(curve_points) - 1))) + 1)
            return VMobject().set_points_as_corners(curve_points[:count]).set_stroke(
                DIRECTION, 2.6, opacity=0.95,
            )

        live_curve = always_redraw(partial_curve)
        pen = Dot(radius=0.06).set_fill(DIRECTION, 1.0).set_stroke(width=0)
        pen.add_updater(lambda m: m.move_to(
            axes.c2p(sweep.get_value(), curve_at(sweep.get_value())),
        ))

        def sweep_direction() -> np.ndarray:
            a = np.deg2rad(sweep.get_value())
            return np.array([np.cos(a), np.sin(a), 0.0])

        sweep_arrow = Arrow(
            wheel_centre, wheel_centre + ACTIVE_ARROW_LENGTH * sweep_direction(),
            buff=0.0, stroke_width=5.0, max_tip_length_to_length_ratio=0.18,
        ).set_color(DIRECTION).set_opacity(0.95)
        sweep_arrow.add_updater(lambda m: m.put_start_and_end_on(
            wheel_centre, wheel_centre + ACTIVE_ARROW_LENGTH * sweep_direction(),
        ))
        sweep_label = ty.maths("u", size=ty.EQ, color=DIRECTION)

        def move_sweep_label(m):
            d = sweep_direction()
            m.move_to(
                wheel_centre + ACTIVE_ARROW_LENGTH * d
                + 0.22 * np.array([-d[1], d[0], 0.0]),
            )

        sweep_label.add_updater(move_sweep_label)
        sweep_readout = ty.readout(
            R"\operatorname{score}(u)", ValueTracker(curve_at(0.0)), places=3,
            color=DIRECTION,
        )
        sweep_readout.next_to(axes.c2p(180, SCORE_MAX), UP, buff=0.22)
        sweep_readout.align_to(axes.c2p(180, 0), RIGHT)
        layout.fit_in_frame(sweep_readout, margin=0.45)
        sweep_readout[1].add_updater(
            lambda m: m.set_value(curve_at(sweep.get_value())),
        )

        def curve_mark(deg: float, value: float) -> Dot:
            return Dot(radius=0.065).set_fill(DIRECTION, 1.0).set_stroke(
                width=0,
            ).move_to(axes.c2p(deg, value))

        mark1 = curve_mark(degrees_of[0], scores[0])
        mark2 = curve_mark(degrees_of[1], scores[1])

        mean_line = DashedLine(
            axes.c2p(0, curve_mean), axes.c2p(180, curve_mean),
            dash_length=0.12, dashed_ratio=0.6,
        ).set_stroke(AVERAGE, 3.0, opacity=0.95)
        mean_caption = ty.maths(
            Rf"\text{{every direction}}={curve_mean:.3f}", size=ty.LABEL,
            color=AVERAGE,
        )
        mean_caption.move_to([0, caption_y, 0]).align_to(
            axes.c2p(180, 0) + 0.12 * RIGHT, RIGHT,
        )
        layout.fit_in_frame(mean_caption, margin=0.45)

        with self.voiceover(
            text="<bookmark mark='room'/>In fact, every direction has its "
                 "own score. <bookmark mark='sweep'/>So if we turn u through "
                 "a half turn and keep reading the score as it goes, we get "
                 "a whole curve."
        ) as tracker:
            self.wait_until_bookmark("room")
            room_budget = max(2.0, tracker.time_until_bookmark("sweep"))
            self.play(
                wheel_group.animate.shift(WHEEL_SHIFT),
                cloud.dots.animate.shift(WHEEL_SHIFT),
                FadeOut(recipe),
                run_time=min(1.2, room_budget * 0.55),
            )
            self.play(
                Create(axes), FadeIn(x_labels), FadeIn(y_labels),
                FadeIn(x_title), FadeIn(y_title),
                run_time=min(0.9, room_budget * 0.4),
            )
            self.wait_until_bookmark("sweep")
            self.play(
                FadeIn(sweep_arrow), FadeIn(sweep_label), FadeIn(sweep_readout),
                u1_arrow.animate.set_opacity(0.35),
                u2_arrow.animate.set_opacity(0.35),
                u1_label.animate.set_opacity(0.5),
                u2_label.animate.set_opacity(0.5),
                run_time=0.5,
            )
            self.add(live_curve, pen)
            # The sweep is the measurement; it takes the time it takes, and
            # the passage ends in silence if the words run out first.
            self.play(
                sweep.animate.set_value(180.0),
                run_time=max(6.0, tracker.get_remaining_duration()),
                rate_func=linear,
            )
        self.inspect(0.6)

        with self.voiceover(
            text="<bookmark mark='marks'/>Our two draws were just two "
                 "readings off this curve. <bookmark mark='mean'/>What the "
                 "loss actually wants is the score averaged over every "
                 "direction, which on this picture is the average height of "
                 "the curve."
        ) as tracker:
            self.wait_until_bookmark("marks")
            marks_budget = max(2.4, tracker.time_until_bookmark("mean"))
            self.play(
                FadeOut(sweep_arrow), FadeOut(sweep_label), FadeOut(pen),
                FadeOut(sweep_readout),
                run_time=min(0.4, marks_budget * 0.15),
            )
            # Each number leaves its label and sits on the curve at its
            # direction's angle.
            moves = []
            for readout, mark in ((readout1, mark1), (readout2, mark2)):
                label, number = readout
                moves += [
                    FadeOut(label),
                    number.animate.scale(ty.LABEL / ty.EQ).next_to(
                        mark, UR if mark is mark1 else DR, buff=0.08,
                    ),
                    GrowFromCenter(mark),
                ]
            self.play(*moves, run_time=min(1.4, marks_budget * 0.6))
            self.wait_until_bookmark("mean")
            self.play(
                Create(mean_line), FadeIn(mean_caption, shift=0.05 * UP),
                run_time=min(1.2, max(0.6, tracker.get_remaining_duration() * 0.5)),
            )
        self.freeze(live_curve, pen, sweep_arrow, sweep_label, sweep_readout[1])
        self.remove(pen, sweep_arrow, sweep_label, sweep_readout)
        static_curve = partial_curve()
        self.remove(live_curve)
        self.add(static_curve)
        self.add(mark1, mark2, mean_line, mean_caption)
        self.inspect(0.8)

        # ---------------------------------------------------------------
        # P5: sampling reads the curve where the draws land; M.
        # ---------------------------------------------------------------
        def fan_line(u: np.ndarray) -> Line:
            return Line(
                wheel_centre, wheel_centre + WHEEL_RADIUS * unit3(u),
            ).set_stroke(DIRECTION, 1.6, opacity=0.55)

        fan_lines = [fan_line(u) for u in u_vectors]
        fan_marks = [
            Dot(radius=0.05).set_fill(DIRECTION, 0.95).set_stroke(width=0)
            .move_to(axes.c2p(d, s))
            for d, s in zip(degrees_of, scores)
        ]

        progress = ValueTracker(2.0)

        def mean_at(p: float, means: np.ndarray) -> float:
            p = float(np.clip(p, 1.0, M_TOTAL))
            k = int(np.floor(p))
            if k >= M_TOTAL:
                return float(means[M_TOTAL - 1])
            frac = p - k
            return float(means[k - 1] + (means[k] - means[k - 1]) * smooth(frac))

        def place_average(line: Line, means: np.ndarray, tracker_: ValueTracker):
            y = mean_at(tracker_.get_value(), means)
            line.put_start_and_end_on(axes.c2p(0, y), axes.c2p(180, y))

        average_line = Line(
            axes.c2p(0, running_mean[1]), axes.c2p(180, running_mean[1]),
        ).set_stroke(AVERAGE, 3.4, opacity=1.0)
        average_line.add_updater(lambda m: place_average(m, running_mean, progress))
        average_readout = small_readout(R"\text{average}", running_mean[1], AVERAGE)
        average_readout.move_to([0, caption_y, 0]).align_to(
            axes.c2p(0, 0) + 0.45 * LEFT, LEFT,
        )
        average_readout[1].add_updater(
            lambda m: m.set_value(mean_at(progress.get_value(), running_mean)),
        )

        def fan_wave(lines, marks, tracker_, first: int, last: int, budget: float):
            arrivals = [
                AnimationGroup(Create(lines[k - 1]), GrowFromCenter(marks[k - 1]))
                for k in range(first, last + 1)
            ]
            self.play(
                LaggedStart(*arrivals, lag_ratio=1.0),
                tracker_.animate(rate_func=linear).set_value(float(last)),
                run_time=budget,
            )

        m_readout = ty.maths(f"M={M_TOTAL}", size=ty.EQ, color=DIRECTION)
        m_readout.move_to(x_title).align_to(axes.c2p(180, 0), RIGHT)
        layout.fit_in_frame(m_readout, margin=0.45)

        with self.voiceover(
            text="<bookmark mark='why'/>In two dimensions we could just "
                 "sweep the whole ring and be done. But in D dimensions the "
                 "sphere has no single sweep, so the loss cannot trace this "
                 "curve. What it can do is read the curve at the directions "
                 "it happens to draw. <bookmark mark='one'/>So we draw a "
                 "third direction, <bookmark mark='onemark'/>read its score "
                 "off the curve, <bookmark mark='average'/>and average the "
                 "three. <bookmark mark='more'/>Then we keep drawing. "
                 "<bookmark mark='eight'/>After the first few draws the "
                 "average has mostly settled, <bookmark mark='many'/>and by "
                 "thirty-two it barely moves. <bookmark mark='M'/>That "
                 "number of draws is what we call M."
        ) as tracker:
            self.wait_until_bookmark("why")
            self.play(
                Indicate(mark1, color=ACCENT, scale_factor=1.6),
                Indicate(mark2, color=ACCENT, scale_factor=1.6),
                run_time=min(1.2, max(0.6, tracker.time_until_bookmark("one"))),
            )
            self.wait_until_bookmark("one")
            self.play(
                Create(fan_lines[2]),
                run_time=min(0.8, max(0.4, tracker.time_until_bookmark("onemark"))),
            )
            self.wait_until_bookmark("onemark")
            self.play(
                GrowFromCenter(fan_marks[2]),
                run_time=min(0.6, max(0.3, tracker.time_until_bookmark("average"))),
            )
            self.wait_until_bookmark("average")
            average_budget = max(1.4, tracker.time_until_bookmark("more"))
            self.play(
                FadeIn(average_line), FadeIn(average_readout),
                run_time=min(0.5, average_budget * 0.3),
            )
            self.play(
                progress.animate.set_value(3.0),
                run_time=min(1.0, average_budget * 0.6),
            )
            self.wait_until_bookmark("more")
            fan_wave(
                fan_lines, fan_marks, progress, 4, M_FIRST_WAVE,
                max(1.6, tracker.time_until_bookmark("eight")),
            )
            self.wait_until_bookmark("eight")
            self.play(
                *(fan_lines[k].animate.set_stroke(opacity=0.22)
                  for k in range(2, M_FIRST_WAVE)),
                run_time=0.4,
            )
            fan_wave(
                fan_lines, fan_marks, progress, M_FIRST_WAVE + 1, M_TOTAL,
                max(4.0, tracker.time_until_bookmark("M") - 0.2),
            )
            self.wait_until_bookmark("M")
            self.play(
                *(fan_lines[k].animate.set_stroke(opacity=0.22)
                  for k in range(M_FIRST_WAVE, M_TOTAL)),
                FadeIn(m_readout, shift=0.06 * UP),
                run_time=min(0.7, max(0.4, tracker.get_remaining_duration())),
            )
            self.across(
                tracker,
                Indicate(m_readout, color=ACCENT, scale_factor=1.08),
                floor=0.6,
            )
        self.inspect(0.6)

        # ---------------------------------------------------------------
        # P6: the directions are our luck; the curve is the batch's.
        # ---------------------------------------------------------------
        redraw_lines = [fan_line(u) for u in u_redraw]
        redraw_marks = [
            Dot(radius=0.05).set_fill(DIRECTION, 0.95).set_stroke(width=0)
            .move_to(axes.c2p(d, s))
            for d, s in zip(degrees_redraw, scores_redraw)
        ]
        progress_redraw = ValueTracker(1.0)
        redraw_line = Line(
            axes.c2p(0, scores_redraw[0]), axes.c2p(180, scores_redraw[0]),
        ).set_stroke(AVERAGE, 3.4, opacity=1.0)
        redraw_line.add_updater(
            lambda m: place_average(m, running_redraw, progress_redraw),
        )

        with self.voiceover(
            text="<bookmark mark='redraw'/>If we draw a different "
                 "thirty-two, the readings land in different places, "
                 "<bookmark mark='same'/>but the average comes out almost "
                 "the same. <bookmark mark='batch'/>What does not change is "
                 "the curve itself. It belongs to this batch of two hundred "
                 "points, so drawing more directions only reads it more "
                 "closely, and the only thing that would move it is a "
                 "different batch."
        ) as tracker:
            self.wait_until_bookmark("redraw")
            self.freeze(average_line, average_readout[1])
            redraw_budget = max(3.2, tracker.time_until_bookmark("same"))
            self.play(
                *(line.animate.set_stroke(opacity=0.08) for line in fan_lines),
                *(mark.animate.set_fill(opacity=0.25) for mark in fan_marks),
                average_line.animate.set_stroke(opacity=0.35),
                FadeOut(average_readout),
                run_time=min(0.6, redraw_budget * 0.2),
            )
            average_readout[1].clear_updaters()
            redraw_readout = small_readout(
                R"\text{average}", scores_redraw[0], AVERAGE,
            )
            redraw_readout.move_to(average_readout).align_to(average_readout, LEFT)
            redraw_readout[1].add_updater(
                lambda m: m.set_value(mean_at(progress_redraw.get_value(), running_redraw)),
            )
            self.play(
                FadeIn(redraw_line), FadeIn(redraw_readout),
                run_time=min(0.4, redraw_budget * 0.1),
            )
            fan_wave(
                redraw_lines, redraw_marks, progress_redraw, 2, M_TOTAL,
                max(2.6, redraw_budget * 0.7),
            )
            self.wait_until_bookmark("same")
            self.play(
                *(line.animate.set_stroke(opacity=0.22) for line in redraw_lines),
                Indicate(redraw_line, color=ACCENT, scale_factor=1.0),
                Indicate(redraw_readout, color=ACCENT, scale_factor=1.05),
                run_time=min(1.2, max(0.6, tracker.time_until_bookmark("batch"))),
            )
            self.wait_until_bookmark("batch")
            batch_budget = max(2.0, tracker.get_remaining_duration())
            self.play(
                Indicate(
                    cloud.dots,
                    color=interpolate_color(
                        ManimColor(CLOUD), ManimColor(WHITE), 0.45,
                    ),
                    scale_factor=1.03,
                ),
                run_time=min(1.4, batch_budget * 0.5),
            )
            self.across(
                tracker,
                Indicate(mean_line, color=ACCENT, scale_factor=1.0),
                Indicate(mean_caption, color=ACCENT, scale_factor=1.04),
                floor=0.8,
            )

        self.freeze(redraw_line, redraw_readout[1])
        self.settle_frame()
