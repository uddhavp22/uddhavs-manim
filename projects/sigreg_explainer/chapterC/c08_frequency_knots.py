"""Chapter C.08 -- each score is an integral over every frequency; K knots.

The point, in three sentences: each direction's score is an integral over
every frequency, and we cannot compute that either. So we read the integrand
at K frequencies and add up the trapezoids. A handful of knots already
reproduces the area, and that count is K.

What the viewer is shown, in order:

  * B11's formula returns; under it the second direction's shadow
    fingerprint is drawn, the Gaussian's on top of it, and a probe walks
    every frequency comparing the two; the gap is squared (and scaled by N,
    as the formula says) into a curve that grows where the fingerprint is
    just noise; the taper from B09 crushes that tail, and the panel zooms
    into what is left -- the curve whose area is the score the viewer saw in
    C07, 0.049;
  * four knots inside Chapter B's window, the trapezoids between them, and a
    sum that is well off (0.071); eight knots, and the sum is already 0.049;
  * sixteen knots match the area to every digit shown; K is named after that
    has been watched;
  * the integral in the formula becomes a sum over K knots.

Every number is computed from the same batch (the C07 cloud projected on
its second sampled direction) through ``common.score``'s integrand and is
checked in ``facts.py``.

Render:
    SIGREG_VOICE=eleven ./render.sh \
        projects/sigreg_explainer/chapterC/c08_frequency_knots.py C08 -qh
"""

import os
import sys
from types import SimpleNamespace

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.palette import (
    ACCENT, AXIS, CLOUD, COLLAPSE, DIRECTION, INK, MUTED, TARGET,
)
from common.score import EP_GRID, EP_LAMBDA, epps_pulley
from common import type as ty
from common.wrap import ecf, gaussian_cf

T_LO, T_HI = layout.FREQUENCY_WINDOW
PLOT_T_MAX = 5.0
Y_MAX = 0.03
KNOT_COUNTS = (4, 8, 16)
DENSE_KNOTS = 2000

AXES_CENTRE = np.array([-0.85, -0.55, 0.0])
AXES_WIDTH = 8.4
AXES_HEIGHT = 3.4
COLUMN_X = 5.35
FORMULA_Y = 2.55


def second_direction_batch() -> np.ndarray:
    """The C07 cloud projected on its second sampled direction."""
    points = data.whiten(data.gaussian_2d(n=len(data.diagonal_2d())))
    _g, u = data.sampled_directions()
    return points @ u[1]


def integrand(batch: np.ndarray, t) -> np.ndarray:
    """N w_lambda(t) |phi_hat(t) - phi_0(t)|^2, the curve whose area is the score."""
    t = np.atleast_1d(np.asarray(t, dtype=float))
    weight = np.exp(-t ** 2 / (2 * EP_LAMBDA ** 2))
    return len(batch) * weight * np.abs(ecf(batch, t) - gaussian_cf(t)) ** 2


def knot_sum(batch: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Trapezoid sum on k knots across the window, doubled for t < 0."""
    knots = np.linspace(T_LO, T_HI, k)
    values = integrand(batch, knots)
    return knots, values, float(2.0 * np.trapezoid(values, knots))


def percent_text(fraction: float) -> str:
    percent = 100.0 * fraction
    if percent >= 1.0:
        return f"{percent:.0f}\\%"
    if percent >= 0.01:
        return f"{percent:.2f}\\%"
    return f"{percent:.3f}\\%"

def build_frame(batch: np.ndarray, sums: dict, errors: dict, dense: float) -> SimpleNamespace:
    """Every object C08 puts on screen, built the same way each time.

    C09 opens on C08's last frame, so both scenes build it from this one
    function (VISUAL_SYSTEM.md section 7: a seam is enforced by shared code,
    not by two copies agreeing).
    """
    # --- the formula, as B11 left it ---------------------------------
    formula = MathTex(
        R"\mathcal T=",
        R"N",
        R"\int_{-\infty}^{\infty}",
        R"w_\lambda(t)",
        R"\big|\hat\varphi_N(t)-\varphi_0(t)\big|^2",
        R"\,dt",
        font_size=40,
    ).set_color(INK)
    formula[3].set_color(TARGET)
    formula[4].set_color(COLLAPSE)
    formula.move_to([0.0, FORMULA_Y, 0.0])
    layout.fit_in_frame(formula)
    discrete = MathTex(
        R"\mathcal T\approx",
        R"N",
        R"\sum_{k=1}^{K}",
        R"w_\lambda(t_k)",
        R"\big|\hat\varphi_N(t_k)-\varphi_0(t_k)\big|^2",
        R"\,\Delta t",
        font_size=40,
    ).set_color(INK)
    discrete[3].set_color(TARGET)
    discrete[4].set_color(COLLAPSE)
    discrete.move_to(formula)
    layout.fit_in_frame(discrete)

    # --- the gap picture ---------------------------------------------
    axes = Axes(
        x_range=(0, PLOT_T_MAX, 1),
        y_range=(0, Y_MAX, 0.01),
        x_length=AXES_WIDTH,
        y_length=AXES_HEIGHT,
        axis_config={
            "include_tip": False, "stroke_width": 2, "color": AXIS,
            "include_ticks": True, "tick_size": 0.06,
        },
    ).move_to(AXES_CENTRE)
    x_labels = VGroup(*(
        ty.maths(str(v), size=ty.TICK, color=MUTED).next_to(
            axes.c2p(v, 0), DOWN, buff=0.14,
        )
        for v in range(0, int(PLOT_T_MAX) + 1)
    ))
    y_labels = VGroup(*(
        ty.maths(text, size=ty.TICK, color=MUTED).next_to(
            axes.c2p(0, v), LEFT, buff=0.14,
        )
        for v, text in ((0.01, "0.01"), (0.02, "0.02"), (0.03, "0.03"))
    ))
    t_label = ty.maths("t", size=ty.EQ, color=MUTED).next_to(
        axes.c2p(PLOT_T_MAX, 0), RIGHT, buff=0.18,
    )
    panel = VGroup(axes, x_labels, y_labels, t_label)

    # The same panel at fingerprint scale (0 to 1), for the derivation.
    axes_a = Axes(
        x_range=(0, PLOT_T_MAX, 1),
        y_range=(0, 1, 0.5),
        x_length=AXES_WIDTH,
        y_length=AXES_HEIGHT,
        axis_config={
            "include_tip": False, "stroke_width": 2, "color": AXIS,
            "include_ticks": True, "tick_size": 0.06,
        },
    ).move_to(AXES_CENTRE)
    y_labels_a = VGroup(*(
        ty.maths(text, size=ty.TICK, color=MUTED).next_to(
            axes_a.c2p(0, v), LEFT, buff=0.14,
        )
        for v, text in ((0.5, "0.5"), (1.0, "1"))
    ))

    grid = np.linspace(0.0, PLOT_T_MAX, 700)
    table = integrand(batch, grid)
    shadow_cf = ecf(batch, grid)
    target_cf = gaussian_cf(grid)
    gap_table = len(batch) * np.abs(shadow_cf - target_cf) ** 2
    taper_table = np.exp(-grid ** 2 / (2 * EP_LAMBDA ** 2))
    assert np.allclose(taper_table * gap_table, table)
    assert gap_table.max() < 1.0, gap_table.max()

    def trace(values, colour, width=3.5, on=axes_a) -> VMobject:
        mob = VMobject().set_stroke(colour, width)
        mob.set_points_as_corners([
            on.c2p(x, y) for x, y in zip(grid, values)
        ])
        return mob

    shadow_fp = trace(shadow_cf.real, CLOUD)
    target_fp = trace(target_cf, TARGET)
    gap_curve = trace(gap_table, COLLAPSE)
    taper = trace(taper_table, TARGET, width=3.0)
    product = trace(gap_table * taper_table, COLLAPSE)
    shadow_tag = ty.maths(R"\hat\varphi_N(t)", size=ty.LABEL, color=CLOUD)
    target_tag = ty.maths(R"\varphi_0(t)", size=ty.LABEL, color=TARGET)
    tags = VGroup(shadow_tag, target_tag).arrange(
        DOWN, buff=0.16, aligned_edge=LEFT,
    ).move_to(axes_a.c2p(3.55, 0.78))
    taper_tag = ty.maths(R"w_\lambda(t)", size=ty.LABEL, color=TARGET)
    taper_tag.next_to(axes_a.c2p(1.35, 0.42), RIGHT, buff=0.12)

    # A probe that walks the frequency axis comparing the two fingerprints.
    probe_t = ValueTracker(0.0)

    def probe_now() -> VGroup:
        t = probe_t.get_value()
        re = float(ecf(batch, [t])[0].real)
        phi = float(gaussian_cf(t))
        top = max(re, phi)
        return VGroup(
            DashedLine(
                axes_a.c2p(t, 0), axes_a.c2p(t, top), dash_length=0.07,
            ).set_stroke(MUTED, 1.5),
            Line(axes_a.c2p(t, phi), axes_a.c2p(t, re)).set_stroke(
                COLLAPSE, 4,
            ),
            Dot(axes_a.c2p(t, phi), radius=0.06).set_fill(TARGET, 1)
            .set_stroke(width=0),
            Dot(axes_a.c2p(t, re), radius=0.06).set_fill(CLOUD, 1)
            .set_stroke(width=0),
        )

    probe = always_redraw(probe_now)
    curve = VMobject().set_stroke(COLLAPSE, 3.5)
    curve.set_points_as_corners([axes.c2p(x, y) for x, y in zip(grid, table)])
    area = VMobject().set_fill(COLLAPSE, 0.38).set_stroke(COLLAPSE, 0)
    area_points = [axes.c2p(grid[0], 0)]
    area_points += [axes.c2p(x, y) for x, y in zip(grid, table)]
    area_points.append(axes.c2p(grid[-1], 0))
    area.set_points_as_corners(area_points + [area_points[0]])

    # Chapter B's window, drawn the way its bracket was.
    bracket_y = -0.0045
    start = axes.c2p(T_LO, bracket_y)
    end = axes.c2p(T_HI, bracket_y)
    window_rule = Line(start, end).set_stroke(TARGET, 3)
    window_caps = VGroup(
        Line(start + 0.10 * DOWN, start + 0.10 * UP),
        Line(end + 0.10 * DOWN, end + 0.10 * UP),
    ).set_stroke(TARGET, 3)
    window_label = ty.maths(R"[\,0.2,\ 4\,]", size=ty.EQ, color=TARGET)
    window_label.next_to(window_rule, DOWN, buff=0.13)
    window = VGroup(window_rule, window_caps, window_label)
    layout.fit_in_frame(window, margin=0.45)

    # --- the right-hand column of numbers ----------------------------
    score_readout = VGroup(
        ty.maths(R"\operatorname{score}(u_2)=", size=ty.EQ, color=DIRECTION),
        ty.maths(f"{dense:.3f}", size=ty.EQ, color=DIRECTION),
    ).arrange(RIGHT, buff=0.12).move_to([COLUMN_X, 1.05, 0.0])
    layout.fit_in_frame(score_readout, margin=0.45)

    def k_label(k: int):
        return ty.maths(f"K={k}", size=ty.EQ_DISPLAY, color=TARGET).move_to(
            [COLUMN_X, 0.1, 0.0],
        )

    def sum_label(k: int):
        return ty.maths(
            Rf"\text{{sum}}={sums[k][2]:.3f}", size=ty.EQ, color=TARGET,
        ).move_to([COLUMN_X, -0.7, 0.0])

    def error_label(k: int):
        return ty.maths(
            Rf"\text{{off by }}{percent_text(errors[k])}", size=ty.LABEL,
            color=MUTED,
        ).move_to([COLUMN_X, -1.32, 0.0])

    def knot_marks(k: int) -> tuple[VGroup, VGroup, VMobject]:
        knots, values, _total = sums[k]
        lines = VGroup(*(
            Line(axes.c2p(t, 0), axes.c2p(t, v)).set_stroke(
                TARGET, 1.8, opacity=0.85,
            )
            for t, v in zip(knots, values)
        ))
        dots = VGroup(*(
            Dot(radius=0.055).set_fill(TARGET, 1.0).set_stroke(width=0)
            .move_to(axes.c2p(t, v))
            for t, v in zip(knots, values)
        ))
        polygon = VMobject().set_fill(TARGET, 0.32).set_stroke(TARGET, 2.5)
        points = [axes.c2p(knots[0], 0)]
        points += [axes.c2p(t, v) for t, v in zip(knots, values)]
        points.append(axes.c2p(knots[-1], 0))
        polygon.set_points_as_corners(points + [points[0]])
        return lines, dots, polygon

    marks = {k: knot_marks(k) for k in KNOT_COUNTS}

    return SimpleNamespace(
        formula=formula, discrete=discrete, axes=axes, x_labels=x_labels,
        y_labels=y_labels, t_label=t_label, panel=panel, axes_a=axes_a,
        y_labels_a=y_labels_a, grid=grid, table=table, curve=curve,
        area=area, window=window, score_readout=score_readout,
        k_label=k_label, sum_label=sum_label, error_label=error_label,
        knot_marks=knot_marks, marks=marks, shadow_fp=shadow_fp,
        target_fp=target_fp, gap_curve=gap_curve, taper=taper,
        product=product, tags=tags, shadow_tag=shadow_tag,
        target_tag=target_tag, taper_tag=taper_tag, probe_t=probe_t,
        probe=probe,
    )


def final_frame(scene, batch: np.ndarray, sums: dict, errors: dict, dense: float) -> SimpleNamespace:
    """Add C08's last frame to `scene`, exactly as C08 leaves it."""
    f = build_frame(batch, sums, errors, dense)
    for i in range(len(f.formula)):
        f.formula[i].become(f.discrete[i])
    lines16, dots16, poly16 = f.marks[16]
    f.area.set_fill(opacity=0.18)
    f.k_now, f.sum_now, f.err_now = f.k_label(16), f.sum_label(16), f.error_label(16)
    scene.add(
        f.formula, f.axes.x_axis, f.axes.y_axis, f.x_labels, f.y_labels,
        f.t_label, f.score_readout, f.curve, f.area, f.window, poly16,
        lines16, dots16, f.k_now, f.sum_now, f.err_now,
    )
    return f


def scene_numbers(batch: np.ndarray) -> tuple[float, float, dict, dict]:
    full_score = epps_pulley(batch, EP_LAMBDA, EP_GRID)
    _k, _v, dense = knot_sum(batch, DENSE_KNOTS)
    sums = {k: knot_sum(batch, k) for k in KNOT_COUNTS}
    errors = {k: abs(sums[k][2] - dense) / dense for k in KNOT_COUNTS}
    assert f"{dense:.3f}" == f"{full_score:.3f}", (dense, full_score)
    assert errors[4] > 0.2 and errors[8] < 0.001 and errors[16] < 0.0001, errors
    return full_score, dense, sums, errors


class C08(ActScene):
    def construct(self):
        batch = second_direction_batch()
        _full_score, dense, sums, errors = scene_numbers(batch)

        f = build_frame(batch, sums, errors, dense)
        formula, discrete = f.formula, f.discrete
        axes, x_labels, y_labels, t_label = f.axes, f.x_labels, f.y_labels, f.t_label
        axes_a, y_labels_a = f.axes_a, f.y_labels_a
        curve, area, window, score_readout = f.curve, f.area, f.window, f.score_readout
        k_label, sum_label, error_label, marks = f.k_label, f.sum_label, f.error_label, f.marks
        shadow_fp, target_fp, gap_curve, taper, product = (
            f.shadow_fp, f.target_fp, f.gap_curve, f.taper, f.product,
        )
        tags, shadow_tag, target_tag, taper_tag = f.tags, f.shadow_tag, f.target_tag, f.taper_tag
        probe_t, probe = f.probe_t, f.probe

        # ---------------------------------------------------------------
        # P1: the score is an area over every frequency.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='formula'/>Now, each of those scores is "
                 "still an integral, so we have the same problem one level "
                 "down. <bookmark mark='axes'/>Take the second direction, the "
                 "one that scored zero point zero four nine. <bookmark "
                 "mark='compare'/>If we compare its shadow's fingerprint with "
                 "the Gauss-ian's at every frequency, <bookmark "
                 "mark='gap'/>square the gap, <bookmark mark='weight'/>and "
                 "weight it with the taper from before, <bookmark "
                 "mark='curve'/>we get this curve, <bookmark mark='area'/>and "
                 "the score is the area underneath it. <bookmark "
                 "mark='cannot'/>But we can't actually add up over every "
                 "frequency, any more than we could visit every direction."
        ) as tracker:
            self.wait_until_bookmark("formula")
            self.play(
                FadeIn(formula, shift=0.08 * DOWN),
                run_time=min(1.0, max(0.5, tracker.time_until_bookmark("axes"))),
            )

            # The shadow's fingerprint, on the panel at fingerprint scale.
            self.wait_until_bookmark("axes")
            axes_budget = max(3.0, tracker.time_until_bookmark("compare"))
            self.play(
                Create(axes_a), FadeIn(x_labels), FadeIn(y_labels_a),
                FadeIn(t_label),
                FadeIn(score_readout, shift=0.06 * UP),
                run_time=min(1.0, axes_budget * 0.3),
            )
            self.play(
                Create(shadow_fp), FadeIn(shadow_tag),
                run_time=min(2.2, max(1.2, axes_budget * 0.5)),
            )

            # The Gaussian's on top of it, then a probe compares the two at
            # every frequency.
            self.wait_until_bookmark("compare")
            compare_budget = max(3.4, tracker.time_until_bookmark("gap"))
            self.play(
                Create(target_fp), FadeIn(target_tag),
                run_time=min(1.1, compare_budget * 0.25),
            )
            probe_t.set_value(0.0)
            self.add(probe)
            self.play(
                probe_t.animate.set_value(PLOT_T_MAX),
                run_time=max(2.0, tracker.time_until_bookmark("gap") - 0.15),
                rate_func=linear,
            )

            # Square the gap (and scale by N, as the formula says): a curve
            # that grows where the fingerprint is only noise.
            self.wait_until_bookmark("gap")
            self.remove(probe)
            self.play(
                FadeOut(shadow_fp), FadeOut(target_fp), FadeOut(tags),
                Create(gap_curve),
                Indicate(formula[4], color=ACCENT, scale_factor=1.05),
                run_time=1.3,
            )

            # The taper from B09 crushes that tail.
            self.wait_until_bookmark("weight")
            weight_budget = max(2.0, tracker.time_until_bookmark("curve"))
            self.play(
                Create(taper), FadeIn(taper_tag),
                Indicate(formula[3], color=ACCENT, scale_factor=1.05),
                run_time=min(0.9, weight_budget * 0.45),
            )
            self.play(
                ReplacementTransform(gap_curve, product),
                run_time=min(1.0, weight_budget * 0.5),
            )

            # Zoom into what is left: the panel relabels to the score scale.
            self.wait_until_bookmark("curve")
            curve_budget = max(1.0, tracker.time_until_bookmark("area"))
            self.remove(axes_a)
            self.add(axes.x_axis, axes_a.y_axis)
            self.play(
                FadeOut(axes_a.y_axis), FadeIn(axes.y_axis),
                FadeOut(y_labels_a, shift=0.05 * UP),
                FadeIn(y_labels, shift=0.05 * UP),
                FadeOut(taper), FadeOut(taper_tag),
                ReplacementTransform(product, curve),
                run_time=min(1.1, curve_budget),
            )

            self.wait_until_bookmark("area")
            area_budget = max(1.6, tracker.time_until_bookmark("cannot"))
            self.play(FadeIn(area), run_time=min(0.9, area_budget * 0.45))
            self.play(
                Indicate(score_readout, color=ACCENT, scale_factor=1.06),
                run_time=min(0.8, area_budget * 0.4),
            )
            self.wait_until_bookmark("cannot")
            self.across(
                tracker,
                area.animate(rate_func=there_and_back).set_fill(opacity=0.6),
                floor=1.0,
            )
        self.inspect(0.6)

        # ---------------------------------------------------------------
        # P2: knots inside the window; four, then eight.
        # ---------------------------------------------------------------
        lines4, dots4, poly4 = marks[4]
        lines8, dots8, poly8 = marks[8]
        lines16, dots16, poly16 = marks[16]
        k_now = k_label(4)
        sum_now = sum_label(4)
        err_now = error_label(4)

        with self.voiceover(
            text="So we do the same thing we did with directions. <bookmark "
                 "mark='window'/>We pick a handful of frequencies inside the "
                 "window, <bookmark mark='read'/>read off the height of the "
                 "curve at each one, <bookmark mark='trap'/>and add up the "
                 "trapezoids in between. <bookmark mark='four'/>If we try "
                 "that with just four knots, the sum comes out at zero point "
                 "zero seven one, which is a long way off."
        ) as tracker:
            self.wait_until_bookmark("window")
            self.play(
                FadeIn(window, shift=0.05 * UP),
                run_time=min(0.8, max(0.4, tracker.time_until_bookmark("read"))),
            )
            self.wait_until_bookmark("read")
            read_budget = max(1.4, tracker.time_until_bookmark("trap"))
            self.play(
                LaggedStart(*(
                    AnimationGroup(Create(line), GrowFromCenter(dot))
                    for line, dot in zip(lines4, dots4)
                ), lag_ratio=0.35),
                run_time=min(1.4, read_budget * 0.8),
            )
            self.wait_until_bookmark("trap")
            trap_budget = max(1.6, tracker.time_until_bookmark("four"))
            self.play(
                FadeIn(poly4),
                area.animate.set_fill(opacity=0.18),
                FadeIn(k_now, shift=0.06 * UP),
                run_time=min(1.0, trap_budget * 0.5),
            )
            self.play(
                FadeIn(sum_now, shift=0.06 * UP),
                run_time=min(0.6, trap_budget * 0.3),
            )
            self.wait_until_bookmark("four")
            self.across(
                tracker,
                FadeIn(err_now, shift=0.06 * UP),
                floor=0.6,
            )
        self.inspect(0.8)

        # ---------------------------------------------------------------
        # P3: sixteen; name K.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='eight'/>But if we go up to eight knots, the "
                 "sum is already zero point zero four nine, within a "
                 "twentieth of a percent of the true area. <bookmark "
                 "mark='sixteen'/>And if we double that to sixteen, the "
                 "trapezoids hug the curve so closely that the sum matches "
                 "the area to every digit we're showing. <bookmark "
                 "mark='enough'/>Past that there's really nothing left to "
                 "gain, so sixteen is what we use, <bookmark mark='name'/>and "
                 "that number of knots is what we call K."
        ) as tracker:
            self.wait_until_bookmark("eight")
            eight_budget = max(2.4, tracker.time_until_bookmark("sixteen"))
            k_next, sum_next, err_next = k_label(8), sum_label(8), error_label(8)
            self.play(
                FadeOut(lines4), FadeOut(dots4),
                ReplacementTransform(poly4, poly8),
                LaggedStart(*(
                    AnimationGroup(Create(line), GrowFromCenter(dot))
                    for line, dot in zip(lines8, dots8)
                ), lag_ratio=0.15),
                FadeOut(k_now, shift=0.12 * UP), FadeIn(k_next, shift=0.12 * UP),
                FadeOut(sum_now, shift=0.12 * UP), FadeIn(sum_next, shift=0.12 * UP),
                FadeOut(err_now, shift=0.12 * UP), FadeIn(err_next, shift=0.12 * UP),
                run_time=min(1.6, eight_budget * 0.5),
            )
            k_now, sum_now, err_now = k_next, sum_next, err_next
            self.play(
                Indicate(sum_now, color=ACCENT, scale_factor=1.06),
                Indicate(score_readout[1], color=ACCENT, scale_factor=1.06),
                run_time=min(1.0, max(0.5, eight_budget * 0.3)),
            )
            self.wait_until_bookmark("sixteen")
            sixteen_budget = max(2.4, tracker.time_until_bookmark("enough"))
            k_next, sum_next, err_next = k_label(16), sum_label(16), error_label(16)
            self.play(
                FadeOut(lines8), FadeOut(dots8),
                ReplacementTransform(poly8, poly16),
                LaggedStart(*(
                    AnimationGroup(Create(line), GrowFromCenter(dot))
                    for line, dot in zip(lines16, dots16)
                ), lag_ratio=0.08),
                FadeOut(k_now, shift=0.12 * UP), FadeIn(k_next, shift=0.12 * UP),
                FadeOut(sum_now, shift=0.12 * UP), FadeIn(sum_next, shift=0.12 * UP),
                FadeOut(err_now, shift=0.12 * UP), FadeIn(err_next, shift=0.12 * UP),
                run_time=min(1.8, sixteen_budget * 0.55),
            )
            k_now, sum_now, err_now = k_next, sum_next, err_next
            self.play(
                Indicate(sum_now, color=ACCENT, scale_factor=1.06),
                Indicate(score_readout[1], color=ACCENT, scale_factor=1.06),
                run_time=min(1.2, max(0.6, sixteen_budget * 0.35)),
            )
            self.wait_until_bookmark("enough")
            self.wait_until_bookmark("name")
            self.across(
                tracker,
                Indicate(k_now, color=ACCENT, scale_factor=1.1),
                floor=0.8,
            )
        self.inspect(0.6)

        # ---------------------------------------------------------------
        # P4: the integral becomes a sum.
        # ---------------------------------------------------------------
        with self.voiceover(
            text="So back in the formula, <bookmark mark='sum'/>the integral "
                 "over every frequency turns into a sum over our K knots, "
                 "<bookmark mark='compute'/>and now the score is something we "
                 "can actually compute."
        ) as tracker:
            self.wait_until_bookmark("sum")
            sum_budget = max(1.8, tracker.time_until_bookmark("compute"))
            self.play(
                *(Transform(formula[i], discrete[i]) for i in range(len(formula))),
                run_time=min(1.4, sum_budget * 0.7),
            )
            self.wait_until_bookmark("compute")
            self.across(
                tracker,
                Indicate(formula[2], color=ACCENT, scale_factor=1.12),
                Indicate(k_now, color=ACCENT, scale_factor=1.08),
                floor=1.0,
            )
        self.inspect(0.8)
        self.settle_frame()
