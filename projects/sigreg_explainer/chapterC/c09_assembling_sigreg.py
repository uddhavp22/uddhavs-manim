"""Chapter C.09 -- the whole loss in one line, and its name.

The point, in three sentences: everything the loss does has now been watched
one piece at a time. Written in order, the pieces are one line: project onto
a drawn direction, score the numbers with the K-knot sum, average over the M
draws. LeJEPA calls that line SIGReg, and on the batch on screen it comes out
at the number the purple line was already showing.

What the viewer is shown, in order:

  * C08's last frame, continued (shared builder, exact seam); the knot panel
    and its numbers clear, the discretised score formula parks at the top;
  * a compact cloud with one drawn direction and its rim shadow; the label
    u^T Z rises into the line as its argument;
  * the parked score formula folds into T( . ; lambda) around it;
  * the score-versus-angle panel with its thirty-two readings, the purple
    average line and M = 32; its readout and M rise into (1/M) sum;
  * the name SIGReg(Z) is written -- the first time it is spoken in the
    explainer -- then the line is evaluated on the batch on screen, 0.090,
    and the purple readout pulses to say it is the same number;
  * everything but the line leaves, and the line parks where C10 finds it.

Pictures indicate, labels transform: every symbol arrives from a small text
proxy that moves into its slot and cross-fades, never from a cloud or a fan of
marks. The line is laid out once and never moves until it parks.

Render:
    SIGREG_VOICE=eleven ./render.sh \
        projects/sigreg_explainer/chapterC/c09_assembling_sigreg.py C09 -qh
"""

import os
import sys

import numpy as np
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from common import data, formula as fm, layout
from common.beat import ActScene
from common.palette import (
    ACCENT, AVERAGE, AXIS, CLOUD, DIRECTION, GRID, INK, MUTED, TARGET,
)
from common.score import EP_GRID, EP_LAMBDA, epps_pulley
from common import type as ty
from common.wheel import (
    ACTIVE_ARROW_LENGTH, DOT_RADIUS, MINI_SAMPLE_COUNT, SCALE, WHEEL_RADIUS,
    rim_plot,
)
from c08_frequency_knots import final_frame, scene_numbers, second_direction_batch

LINE_Y = 0.35
C08_PARK = np.array([0.0, 2.85, 0.0])
PICTURE_Y = -2.45
WHEEL_X = -4.1
PANEL_X = 3.3
WHEEL_SCALE = 0.46
RIM_PLOT_SCALE = 0.85
PANEL_WIDTH = 3.9
PANEL_HEIGHT = 2.2
SCORE_MAX = 0.2
CURVE_STEP_DEG = 1.0
M_TOTAL = data.DIRECTION_COUNT
K_KNOTS = 16


def unit3(u2: np.ndarray) -> np.ndarray:
    return np.array([u2[0], u2[1], 0.0])


def angle_deg(u2: np.ndarray) -> float:
    return float(np.degrees(np.arctan2(u2[1], u2[0])) % 180.0)


def knot_score(batch: np.ndarray, k: int = K_KNOTS) -> float:
    """The score C08 settled on: K knots across the window, doubled for t<0."""
    lo, hi = layout.FREQUENCY_WINDOW
    t = np.linspace(lo, hi, k)
    from common.wrap import ecf, gaussian_cf
    v = len(batch) * np.exp(-t ** 2 / (2 * EP_LAMBDA ** 2)) * np.abs(
        ecf(batch, t) - gaussian_cf(t),
    ) ** 2
    return float(2.0 * np.trapezoid(v, t))


def fly_into(proxy, part, scene_scale: float = 1.0):
    """A label rises into its slot in the line and cross-fades into the part.

    Two animations to play together: the proxy shrinks and moves onto the
    part while fading, and the part fades in underneath it.
    """
    target_height = part.get_height()
    factor = target_height / max(proxy.get_height(), 1e-6)
    return [
        proxy.animate.scale(factor * scene_scale).move_to(part.get_center())
        .set_opacity(0.0),
        FadeIn(part),
    ]


class C09(ActScene):
    def construct(self):
        # --- the numbers ---------------------------------------------------
        points_2d = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
        batch = second_direction_batch()
        _full, dense, sums, errors = scene_numbers(batch)
        _g, u_first = data.sampled_directions(M_TOTAL)
        _g2, u_redraw = data.sampled_directions(M_TOTAL, seed=data.REDRAW_SEED)
        direction = u_first[1]                      # the one C08 scored
        theta_deg = np.arange(0.0, 180.0 + CURVE_STEP_DEG / 2, CURVE_STEP_DEG)
        curve = np.array([
            epps_pulley(
                points_2d @ np.array([np.cos(np.deg2rad(d)), np.sin(np.deg2rad(d))]),
                EP_LAMBDA, EP_GRID,
            )
            for d in theta_deg
        ])
        shown_scores = np.array([
            epps_pulley(points_2d @ u, EP_LAMBDA, EP_GRID) for u in u_redraw
        ])
        shown_average = float(shown_scores.mean())    # C07's purple readout
        line_value = float(np.mean([knot_score(points_2d @ u) for u in u_redraw]))
        assert f"{shown_average:.3f}" == f"{line_value:.3f}", (shown_average, line_value)
        assert f"{dense:.3f}" == f"{knot_score(batch):.3f}", (dense, knot_score(batch))

        # --- C08's last frame, continued -----------------------------------
        f = final_frame(self, batch, sums, errors, dense)
        lines16, dots16, poly16 = f.marks[16]
        c08_formula = f.formula
        c08_rest = VGroup(
            f.axes.x_axis, f.axes.y_axis, f.x_labels, f.y_labels, f.t_label,
            f.score_readout, f.curve, f.area, f.window, poly16, lines16, dots16,
            f.k_now, f.sum_now, f.err_now,
        )

        # --- the line, laid out once ---------------------------------------
        line = fm.sigreg_formula()
        value = ty.maths(f"={line_value:.3f}", size=ty.EQ_DISPLAY, color=AVERAGE)
        whole = VGroup(line, value.copy()).arrange(RIGHT, buff=0.18)
        whole.move_to([0.0, LINE_Y, 0.0])
        layout.fit_in_frame(whole, margin=0.45)
        line.move_to(whole[0])
        value.next_to(line, RIGHT, buff=0.18)
        value.match_y(line[fm.NAME])
        conditions = VGroup(
            ty.maths(f"M={M_TOTAL},", size=ty.LABEL, color=MUTED),
            ty.maths(f"K={K_KNOTS}", size=ty.LABEL, color=MUTED),
        ).arrange(RIGHT, buff=0.14).next_to(value, UP, buff=0.24)
        parked = fm.parked_sigreg_formula()

        # --- the compact wheel: cloud, one drawn direction, its shadow ------
        wheel_centre = np.array([WHEEL_X, PICTURE_Y, 0.0])
        ring = Circle(radius=WHEEL_SCALE * WHEEL_RADIUS).set_stroke(
            GRID, 2.0, opacity=1.0,
        ).move_to(wheel_centre)
        cloud = VGroup(*(
            Dot(radius=WHEEL_SCALE * DOT_RADIUS * 1.6).set_fill(CLOUD, 0.88)
            .set_stroke(width=0)
            .move_to(wheel_centre + WHEEL_SCALE * SCALE * unit3(p))
            for p in points_2d
        ))
        u3 = unit3(direction)
        arrow = Arrow(
            wheel_centre, wheel_centre + WHEEL_SCALE * WHEEL_RADIUS * u3,
            buff=0.0, stroke_width=4.0, max_tip_length_to_length_ratio=0.16,
        ).set_color(DIRECTION).set_opacity(0.95)
        normal = np.array([-u3[1], u3[0], 0.0])
        side = normal if normal[1] >= 0 else -normal
        u_label = ty.maths("u", size=ty.EQ, color=DIRECTION).move_to(
            wheel_centre + WHEEL_SCALE * ACTIVE_ARROW_LENGTH * 1.25 * u3 + 0.26 * side,
        )
        axis_line = Line(
            wheel_centre - WHEEL_SCALE * 2.56 * u3,
            wheel_centre + WHEEL_SCALE * 2.56 * u3,
        ).set_stroke(DIRECTION, 1.6, opacity=0.5)
        shadow_indices = np.linspace(0, len(points_2d) - 1, MINI_SAMPLE_COUNT, dtype=int)
        # u and -u cast the same shadow; the plot goes on the far side of the
        # ring from the arrow so the two do not collide.
        shadow = rim_plot(
            points_2d[shadow_indices], -u3, wheel_centre, scale=WHEEL_SCALE,
            plot_scale=RIM_PLOT_SCALE,
        )
        projection_label = ty.maths(R"u^{\top}Z", size=ty.EQ, color=DIRECTION)
        projection_label.next_to(shadow, -u3 * 1.0, buff=0.22)
        layout.fit_in_frame(projection_label, margin=0.45)
        wheel_picture = VGroup(ring, cloud, arrow, u_label, axis_line, shadow)

        # --- the compact score-versus-angle panel --------------------------
        axes = Axes(
            x_range=[0, 180, 90], y_range=[0, SCORE_MAX, 0.1],
            x_length=PANEL_WIDTH, y_length=PANEL_HEIGHT,
            axis_config={
                "stroke_color": AXIS, "stroke_width": 1.6,
                "include_tip": False, "include_ticks": True, "tick_size": 0.05,
            },
        ).move_to([PANEL_X, PICTURE_Y, 0.0])
        x_labels = VGroup(*(
            ty.maths(Rf"{d}^\circ", size=ty.TICK, color=MUTED).next_to(
                axes.c2p(d, 0), DOWN, buff=0.12,
            )
            for d in (0, 90, 180)
        ))
        y_labels = VGroup(*(
            ty.maths(text, size=ty.TICK, color=MUTED).next_to(
                axes.c2p(0, v), LEFT, buff=0.12,
            )
            for v, text in ((0.1, "0.1"), (0.2, "0.2"))
        ))
        score_curve = VMobject().set_stroke(DIRECTION, 2.2, opacity=0.95)
        score_curve.set_points_as_corners([axes.c2p(d, s) for d, s in zip(theta_deg, curve)])
        marks = VGroup(*(
            Dot(radius=0.045).set_fill(DIRECTION, 0.95).set_stroke(width=0)
            .move_to(axes.c2p(angle_deg(u), s))
            for u, s in zip(u_redraw, shown_scores)
        ))
        average_line = Line(
            axes.c2p(0, shown_average), axes.c2p(180, shown_average),
        ).set_stroke(AVERAGE, 3.2, opacity=1.0)
        average_readout = VGroup(
            ty.maths(R"\text{average}=", size=ty.LABEL, color=AVERAGE),
            ty.maths(f"{shown_average:.3f}", size=ty.LABEL, color=AVERAGE),
        ).arrange(RIGHT, buff=0.10, aligned_edge=DOWN)
        average_readout.next_to(axes.c2p(0, SCORE_MAX), UP, buff=0.16)
        average_readout.align_to(y_labels, LEFT)
        m_readout = ty.maths(f"M={M_TOTAL}", size=ty.EQ, color=DIRECTION)
        m_readout.next_to(axes.c2p(180, SCORE_MAX), UP, buff=0.16)
        m_readout.align_to(axes.c2p(180, 0), RIGHT)
        m_readout.align_to(average_readout, DOWN)
        panel_picture = VGroup(
            axes, x_labels, y_labels, score_curve, marks, average_line,
            average_readout, m_readout,
        )
        layout.fit_in_frame(panel_picture, margin=0.45)

        # ---------------------------------------------------------------
        # P0: everything we need is built; clear the desk.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="So now we have everything we need, <bookmark mark='clear'/>"
                 "and we can write the whole loss down in one line. <bookmark "
                 "mark='park'/>Each piece of it is something we have already "
                 "watched, so let's put them together in order."
        ) as tracker:
            self.wait_until_bookmark("clear")
            self.play(
                FadeOut(c08_rest),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("park"))),
            )
            self.wait_until_bookmark("park")
            self.play(
                c08_formula.animate.scale(0.82).move_to(C08_PARK).set_opacity(0.8),
                run_time=min(1.0, max(0.5, tracker.get_remaining_duration() * 0.4)),
            )
        self.inspect(0.5)

        # ---------------------------------------------------------------
        # P1: the projection is the argument.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='cloud'/>We start with the batch Z and one "
                 "direction u that we drew at random. <bookmark "
                 "mark='project'/>If we project the cloud onto u, every point "
                 "turns into one number. <bookmark mark='symbol'/>Written "
                 "out, that is u transpose Z, <bookmark mark='m'/>and the "
                 "little m just counts which of our draws it was."
        ) as tracker:
            self.wait_until_bookmark("cloud")
            self.play(
                FadeIn(ring), FadeIn(cloud), GrowArrow(arrow), FadeIn(u_label),
                run_time=min(1.1, max(0.6, tracker.time_until_bookmark("project"))),
            )
            self.wait_until_bookmark("project")
            project_budget = max(1.6, tracker.time_until_bookmark("symbol"))
            self.play(Create(axis_line), run_time=min(0.5, project_budget * 0.3))
            self.play(
                FadeIn(shadow[0]), FadeIn(shadow[2]),
                LaggedStart(*(GrowFromCenter(d) for d in shadow[1]), lag_ratio=0.03),
                run_time=min(1.1, project_budget * 0.6),
            )
            self.wait_until_bookmark("symbol")
            symbol_budget = max(1.6, tracker.time_until_bookmark("m"))
            self.play(
                FadeIn(projection_label, shift=0.05 * UP),
                run_time=min(0.5, symbol_budget * 0.3),
            )
            proxy = projection_label.copy()
            self.add(proxy)
            self.play(
                *fly_into(proxy, line[fm.ARGUMENT]),
                run_time=min(1.0, symbol_budget * 0.6),
            )
            self.remove(proxy)
            self.wait_until_bookmark("m")
            self.across(
                tracker,
                Indicate(line[fm.ARGUMENT], color=ACCENT, scale_factor=1.08),
                floor=0.8,
            )
        self.inspect(0.5)

        # ---------------------------------------------------------------
        # P2: the score folds into one symbol.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='score'/>Then we score those numbers "
                 "against the standard Gauss-ian. <bookmark mark='sum'/>That "
                 "score is exactly the sum we just built, <bookmark "
                 "mark='knots'/>with K knots <bookmark mark='taper'/>inside "
                 "the taper of width lambda, <bookmark mark='fold'/>so we can "
                 "fold all of it into one symbol, T, <bookmark "
                 "mark='lambda'/>and keep lambda inside the brackets so we "
                 "don't forget it is part of the score."
        ) as tracker:
            self.wait_until_bookmark("score")
            self.play(
                Indicate(shadow[2], color=ACCENT, scale_factor=1.05),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("sum"))),
            )
            self.wait_until_bookmark("sum")
            self.play(
                Indicate(c08_formula, color=ACCENT, scale_factor=1.03),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("knots"))),
            )
            self.wait_until_bookmark("knots")
            self.play(
                Indicate(c08_formula[2], color=ACCENT, scale_factor=1.12),
                run_time=min(0.9, max(0.4, tracker.time_until_bookmark("taper"))),
            )
            self.wait_until_bookmark("taper")
            self.play(
                Indicate(c08_formula[3], color=ACCENT, scale_factor=1.12),
                run_time=min(0.9, max(0.4, tracker.time_until_bookmark("fold"))),
            )
            self.wait_until_bookmark("fold")
            fold_budget = max(2.4, tracker.time_until_bookmark("lambda"))
            slot = VGroup(line[fm.SCORE_OPEN], line[fm.SCORE_CLOSE]).get_center()
            self.play(
                c08_formula.animate.scale(0.45).move_to(slot).set_opacity(0.0),
                FadeIn(line[fm.SCORE_OPEN]), FadeIn(line[fm.SCORE_CLOSE]),
                run_time=min(1.4, fold_budget * 0.5),
            )
            self.remove(c08_formula)
            self.wait_until_bookmark("lambda")
            self.across(
                tracker,
                Indicate(line[fm.SCORE_CLOSE], color=ACCENT, scale_factor=1.1),
                floor=0.8,
            )
        self.inspect(0.5)

        # ---------------------------------------------------------------
        # P3: the average over M draws.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='panel'/>Then we do the same for every "
                 "direction we drew, all thirty-two of them, <bookmark "
                 "mark='average'/>and take the average. <bookmark "
                 "mark='wrap'/>The one over M and the sum are just that "
                 "average, written out."
        ) as tracker:
            self.wait_until_bookmark("panel")
            panel_budget = max(2.0, tracker.time_until_bookmark("average"))
            self.play(
                FadeIn(axes), FadeIn(x_labels), FadeIn(y_labels), FadeIn(score_curve),
                run_time=min(0.8, panel_budget * 0.4),
            )
            self.play(
                LaggedStart(*(GrowFromCenter(m) for m in marks), lag_ratio=0.04),
                FadeIn(m_readout, shift=0.05 * UP),
                run_time=min(1.2, panel_budget * 0.55),
            )
            self.wait_until_bookmark("average")
            self.play(
                FadeIn(average_line), FadeIn(average_readout, shift=0.05 * UP),
                run_time=min(0.8, max(0.4, tracker.time_until_bookmark("wrap"))),
            )
            self.wait_until_bookmark("wrap")
            wrap_budget = max(1.6, tracker.get_remaining_duration())
            proxy_avg = average_readout.copy()
            proxy_m = m_readout.copy()
            self.add(proxy_avg, proxy_m)
            self.play(
                *fly_into(proxy_avg, line[fm.ONE_OVER_M]),
                *fly_into(proxy_m, line[fm.SUM]),
                run_time=min(1.2, wrap_budget * 0.7),
            )
            self.remove(proxy_avg, proxy_m)
        self.inspect(0.6)

        # ---------------------------------------------------------------
        # P4: the name.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='whole'/>And that is the whole regularizer. "
                 "<bookmark mark='name'/>LeJEPA calls it SIGReg, for sketched "
                 "isotropic Gauss-ian regularization. <bookmark "
                 "mark='sketched'/>Sketched, because we only ever look at M "
                 "directions, <bookmark mark='gaussian'/>and isotropic "
                 "Gauss-ian, because that is the target every shadow gets "
                 "compared with."
        ) as tracker:
            self.wait_until_bookmark("whole")
            self.play(
                Indicate(VGroup(*line[1:]), color=ACCENT, scale_factor=1.03),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("name"))),
            )
            self.wait_until_bookmark("name")
            self.play(
                Write(line[fm.NAME]),
                run_time=min(1.2, max(0.6, tracker.time_until_bookmark("sketched") * 0.5)),
            )
            self.wait_until_bookmark("sketched")
            self.play(
                Indicate(line[fm.SUM], color=ACCENT, scale_factor=1.08),
                LaggedStart(*(
                    Indicate(m, color=ACCENT, scale_factor=1.6) for m in marks
                ), lag_ratio=0.02),
                run_time=min(1.4, max(0.6, tracker.time_until_bookmark("gaussian"))),
            )
            self.wait_until_bookmark("gaussian")
            self.across(
                tracker,
                Indicate(shadow[2], color=ACCENT, scale_factor=1.12),
                Indicate(line[fm.SCORE_OPEN], color=ACCENT, scale_factor=1.08),
                floor=0.8,
            )
        self.inspect(1.0)

        # ---------------------------------------------------------------
        # P5: the line on the batch on screen; then park it.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='batch'/>And for the batch we have been "
                 "watching, <bookmark mark='M'/>with thirty-two directions "
                 "<bookmark mark='K'/>and sixteen knots, <bookmark "
                 "mark='number'/>the whole line comes out at zero point zero "
                 "nine zero, <bookmark mark='same'/>which is the number the "
                 "purple line was already showing. <bookmark mark='park'/>So "
                 "now we know what it computes. <bookmark mark='tease'/>What "
                 "we have not seen yet is what it does to a cloud."
        ) as tracker:
            self.wait_until_bookmark("batch")
            self.play(
                Indicate(
                    cloud,
                    color=interpolate_color(ManimColor(CLOUD), ManimColor(WHITE), 0.45),
                    scale_factor=1.03,
                ),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("M"))),
            )
            self.wait_until_bookmark("M")
            self.play(
                FadeIn(conditions[0], shift=0.05 * UP),
                run_time=min(0.5, max(0.3, tracker.time_until_bookmark("K"))),
            )
            self.wait_until_bookmark("K")
            self.play(
                FadeIn(conditions[1], shift=0.05 * UP),
                run_time=min(0.5, max(0.3, tracker.time_until_bookmark("number"))),
            )
            self.wait_until_bookmark("number")
            self.play(
                FadeIn(value, shift=0.06 * UP),
                run_time=min(0.8, max(0.4, tracker.time_until_bookmark("same") * 0.4)),
            )
            self.wait_until_bookmark("same")
            self.play(
                Indicate(average_readout, color=ACCENT, scale_factor=1.06),
                Indicate(average_line, color=ACCENT, scale_factor=1.0),
                Indicate(value, color=ACCENT, scale_factor=1.06),
                run_time=min(1.3, max(0.6, tracker.time_until_bookmark("park"))),
            )
            self.wait_until_bookmark("park")
            self.play(
                FadeOut(wheel_picture), FadeOut(projection_label),
                FadeOut(panel_picture), FadeOut(value), FadeOut(conditions),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("tease"))),
            )
            self.wait_until_bookmark("tease")
            self.across(
                tracker,
                line.animate.scale(fm.PARK_SIZE / fm.LINE_SIZE).move_to(parked),
                floor=1.2,
            )
        self.remove(line)
        self.add(parked)
        self.inspect(0.8)
        self.settle_frame()
