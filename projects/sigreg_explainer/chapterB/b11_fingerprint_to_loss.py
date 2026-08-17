"""Chapter B.11 — turn the Gaussian fingerprint into one scalar score.

B10 ends with one Gaussian target point and an unresolved empirical value at
the same frequency. This scene resolves that value in the complex plane,
traces the pointwise squared gap across frequency, and applies the smooth taper
motivated in B09 to obtain the Epps–Pulley statistic.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.bridge import vector_bridge
from common.fingerprint import CharacteristicFunctionPlot
from common.palette import CLOUD, COLLAPSE, FAINT, INK, MUTED, TARGET
from common.score import epps_pulley
from common import type as ty
from common.wrap import ecf, gaussian_cf


PLOT_T_MAX = 5.0
T_LO, T_HI = 0.0, PLOT_T_MAX
GRID = np.linspace(T_LO, T_HI, 700)
PLOT_GRID = np.linspace(0.0, PLOT_T_MAX, 900)
EP_GRID = np.linspace(-8.0, 8.0, 4000)
EP_LAMBDA = 1.0

GAUSS = data.gaussian_1d(40)
BIMODAL = data.bimodal_1d(40)

EP_BIMODAL_SCORE = epps_pulley(BIMODAL, EP_LAMBDA, EP_GRID)
EP_GAUSSIAN_SCORE = epps_pulley(GAUSS, EP_LAMBDA, EP_GRID)

VALIDATION_BATCHES = tuple(
    data.gaussian_1d(40, seed=seed)
    for seed in (34094, 34095, 34096)
)
VALIDATION_SCORES = tuple(
    epps_pulley(batch, EP_LAMBDA, EP_GRID)
    for batch in VALIDATION_BATCHES
)

PLANE_CENTRE = np.array([-3.95, -0.55, 0.0])
PLANE_R = 1.72


class B11(ActScene):
    chain_link = "Epps-Pulley"

    def construct(self):
        self.batch = BIMODAL
        self.t = ValueTracker(1.6)
        self._build_panels()
        self._mount_b10_handoff()

        self.fixed_frequency_beat()
        self.accumulation_beat()
        self.formula_beat()

    # ------------------------------------------------------------------
    def _build_panels(self):
        self.plane = VGroup(
            Line(1.38 * PLANE_R * LEFT, 1.38 * PLANE_R * RIGHT)
            .set_stroke(FAINT, 1.4),
            Line(1.22 * PLANE_R * DOWN, 1.22 * PLANE_R * UP)
            .set_stroke(FAINT, 1.4),
            Circle(radius=PLANE_R).set_stroke(MUTED, 1.5, opacity=0.42),
        ).move_to(PLANE_CENTRE)

        self.gap_axes = Axes(
            x_range=(0, PLOT_T_MAX, 1),
            y_range=(0, 0.75, 0.25),
            x_length=6.15,
            y_length=3.35,
            axis_config={"include_tip": False, "stroke_width": 2},
        )
        self.gap_axes.move_to(np.array([3.18, -0.55, 0.0]))

    def _mount_b10_handoff(self):
        plot = CharacteristicFunctionPlot()
        self.handoff_axes = plot.axes
        self.handoff_furniture = plot.furniture
        self.handoff_curve = plot.gaussian_curve()
        self.handoff_probe = plot.gaussian_probe(1.6)
        self.handoff_probe_line, self.handoff_probe_dot = self.handoff_probe
        self.handoff_unknown = ty.maths(
            R"\hat\varphi_N(1.6)=\,?",
            size=ty.EQ_DISPLAY,
            color=CLOUD,
        )
        self.handoff_unknown.move_to(np.array([0.0, 2.58, 0.0]))
        self.add(
            self.handoff_axes,
            self.handoff_furniture,
            self.handoff_curve,
            self.handoff_probe_line,
            self.handoff_probe_dot,
            self.handoff_unknown,
        )

    def _pt(self, value):
        return PLANE_CENTRE + PLANE_R * np.array([
            value.real, value.imag, 0.0,
        ])

    def _hat(self):
        return ecf(self.batch, [self.t.get_value()])[0]

    def _target(self):
        return complex(gaussian_cf(self.t.get_value()), 0.0)

    def _make_plane_live(self):
        hat_arm = always_redraw(
            lambda: Line(PLANE_CENTRE, self._pt(self._hat()))
            .set_stroke(CLOUD, 2.4, opacity=0.6)
        )
        target_arm = always_redraw(
            lambda: Line(PLANE_CENTRE, self._pt(self._target()))
            .set_stroke(TARGET, 2.4, opacity=0.6)
        )
        hat_dot = always_redraw(
            lambda: Dot(self._pt(self._hat()), radius=0.065)
            .set_fill(CLOUD, 1)
        )
        target_dot = always_redraw(
            lambda: Dot(self._pt(self._target()), radius=0.065)
            .set_fill(TARGET, 1)
        )
        gap = always_redraw(
            lambda: Line(self._pt(self._hat()), self._pt(self._target()))
            .set_stroke(COLLAPSE, 3.5)
        )
        base = VGroup(hat_arm, target_arm, hat_dot, target_dot)
        return base, gap, hat_dot, target_dot

    def _t_readout(self):
        number = DecimalNumber(
            self.t.get_value(),
            num_decimal_places=2,
            font_size=ty.READOUT,
            color=INK,
        )
        number.add_updater(lambda mob: mob.set_value(self.t.get_value()))
        readout = VGroup(
            ty.maths("t=", size=ty.READOUT, color=INK),
            number,
        ).arrange(RIGHT, buff=0.08)
        readout.move_to(np.array([0.0, 2.72, 0.0]))
        return readout

    def _gap_table(self, batch):
        return np.abs(ecf(batch, GRID) - gaussian_cf(GRID)) ** 2

    def _batch_strip(self, batch, label, colour, width=2.5, max_dots=16):
        sample_line = Line(width / 2 * LEFT, width / 2 * RIGHT).set_stroke(
            MUTED, 1.5, opacity=0.75,
        )
        count = min(max_dots, len(batch))
        indices = np.linspace(0, len(batch) - 1, count, dtype=int)
        shown = np.sort(batch)[indices]
        levels = {}
        dots = VGroup()
        for value in shown:
            proportion = float(np.clip((value + 3.0) / 6.0, 0.02, 0.98))
            bucket = int(round(proportion * 24))
            level = levels.get(bucket, 0)
            levels[bucket] = level + 1
            dots.add(
                Dot(
                    sample_line.point_from_proportion(proportion)
                    + (0.08 + 0.075 * level) * UP,
                    radius=0.036,
                ).set_fill(colour, 1)
            )
        batch_label = ty.label(label, color=colour)
        batch_label.scale(0.76)
        batch_label.next_to(dots, UP, buff=0.10)
        return VGroup(sample_line, dots, batch_label)

    def _score_row(self, batch, label, colour, score):
        batch_strip = self._batch_strip(
            batch, label, colour, width=3.15, max_dots=20,
        )
        arrow = Arrow(
            ORIGIN, 0.85 * RIGHT, buff=0,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.16,
        ).set_color(MUTED)
        target = ty.maths(
            R"\varphi_0", size=ty.TICK, color=TARGET,
        )
        target.next_to(arrow, UP, buff=0.08)
        comparison = VGroup(arrow, target)
        value = ty.maths(
            Rf"\mathcal T={score:.3f}",
            size=ty.BODY,
            color=colour,
        )
        return VGroup(batch_strip, comparison, value).arrange(
            RIGHT, buff=0.32,
        )

    def _validation_row(self, batch, score, index):
        batch_strip = self._batch_strip(
            batch, f"draw {index}", CLOUD, width=2.5, max_dots=8,
        )
        arrow = Arrow(
            ORIGIN, 0.65 * RIGHT, buff=0,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.18,
        ).set_color(MUTED)
        value = ty.maths(
            Rf"\mathcal T={score:.3f}",
            size=ty.BODY,
            color=CLOUD,
        )
        return VGroup(batch_strip, arrow, value).arrange(
            RIGHT, buff=0.24,
        )

    # ------------------------------------------------------------------ 1
    def fixed_frequency_beat(self):
        plane_live, gap_line, hat_dot, target_dot = self._make_plane_live()
        plane_live.update(0)
        gap_line.update(0)

        hat_seed = Dot(self._pt(self._hat()), radius=0.065).set_fill(CLOUD, 1)
        target_seed = Dot(
            self._pt(self._target()), radius=0.065,
        ).set_fill(TARGET, 1)
        hat_arm_seed = Line(PLANE_CENTRE, self._pt(self._hat())).set_stroke(
            CLOUD, 2.4, opacity=0.6,
        )
        target_arm_seed = Line(
            PLANE_CENTRE, self._pt(self._target()),
        ).set_stroke(TARGET, 2.4, opacity=0.6)

        with self.voiceover(
            text="At t equals one point six, the batch and the Gaussian each "
                 "give one point in the complex plane."
        ) as tracker:
            self.play(
                FadeOut(VGroup(
                    self.handoff_axes,
                    self.handoff_furniture,
                    self.handoff_curve,
                    self.handoff_probe_line,
                )),
                ReplacementTransform(self.handoff_probe_dot, target_seed),
                ReplacementTransform(self.handoff_unknown, hat_seed),
                Create(self.plane),
                run_time=1.15,
            )
            self.play(
                Create(hat_arm_seed),
                Create(target_arm_seed),
                run_time=0.65,
            )
            self.add(*plane_live)
            self.remove(
                hat_seed,
                target_seed,
                hat_arm_seed,
                target_arm_seed,
            )

            hat_label = ty.maths(
                R"\hat\varphi_N(t)", size=ty.LABEL, color=CLOUD,
            )
            target_label = ty.maths(
                R"\varphi_0(t)", size=ty.LABEL, color=TARGET,
            )
            hat_label.next_to(hat_dot, UL, buff=0.13)
            target_label.next_to(target_dot, DR, buff=0.13)
            self.play(
                FadeIn(hat_label),
                FadeIn(target_label),
                run_time=0.65,
            )

        with self.voiceover(
            text="Their distance tells us how much the two fingerprints "
                 "disagree at this frequency."
        ):
            gap_seed = Line(
                self._pt(self._hat()), self._pt(self._target()),
            ).set_stroke(COLLAPSE, 3.5)
            self.play(Create(gap_seed), run_time=0.8)
            self.add(gap_line)
            self.remove(gap_seed)
            self.wait(1.25)
            self.play(
                Indicate(gap_line, color=COLLAPSE, scale_factor=1.04),
                run_time=0.65,
            )

        squared = ty.maths(
            R"\Delta(t)=\big|\hat\varphi_N(t)-\varphi_0(t)\big|^2",
            size=ty.EQ,
            color=COLLAPSE,
        )
        squared.move_to(np.array([-3.95, 2.50, 0.0]))
        layout.fit_in_frame(squared)

        components = ty.maths(
            R"=\big(\operatorname{Re}\hat\varphi_N-\varphi_0\big)^2"
            R"+\big(\operatorname{Im}\hat\varphi_N\big)^2",
            size=ty.LABEL,
            color=INK,
        )
        components.next_to(squared, DOWN, buff=0.12)
        layout.fit_in_frame(components)

        with self.voiceover(
            text="That distance uses both coordinates: the horizontal "
                 "mismatch from the target, and any vertical component in the "
                 "empirical batch. Squaring it gives a nonnegative quantity "
                 "that still changes smoothly as the points move."
        ) as tracker:
            self.play(Write(squared), Write(components), run_time=1.1)
            self.play(
                Indicate(VGroup(squared, components), color=COLLAPSE,
                         scale_factor=1.035),
                run_time=0.75,
            )
            self.wait(0.45)
            self.play(self.t.animate.set_value(1.82), run_time=0.75)
            self.play(self.t.animate.set_value(1.60), run_time=0.75)

        self.plane_live = plane_live
        self.gap_line = gap_line
        self.hat_label = hat_label
        self.target_label = target_label
        self.squared = squared
        self.components = components

    # ------------------------------------------------------------------ 2
    def accumulation_beat(self):
        labels = VGroup()
        for value in range(1, 6):
            label = ty.maths(str(value), size=ty.TICK, color=MUTED)
            label.next_to(self.gap_axes.c2p(value, 0), DOWN, buff=0.13)
            labels.add(label)
        t_label = ty.maths("t", size=ty.TICK, color=MUTED)
        t_label.next_to(self.gap_axes.c2p(PLOT_T_MAX, 0), DR, buff=0.13)
        head = ty.label("squared gap", color=MUTED)
        head.next_to(self.gap_axes, UP, buff=0.28)

        self.table = self._gap_table(self.batch)
        t_readout = self._t_readout()
        batch_label = ty.label("two-clump batch", color=CLOUD)
        batch_label.move_to(np.array([-3.95, -2.72, 0.0]))

        with self.voiceover(
            text="Each t now gives one nonnegative contribution. "
                 "<bookmark mark='range'/>Let t vary, and those contributions "
                 "line up as a curve of squared disagreement."
        ) as tracker:
            self.play(
                FadeOut(VGroup(self.hat_label, self.target_label)),
                FadeOut(self.components),
                run_time=0.65,
            )
            self.wait_until_bookmark("range")
            self.play(
                FadeIn(t_readout),
                FadeIn(batch_label),
                Create(self.gap_axes),
                FadeIn(labels),
                FadeIn(t_label),
                FadeIn(head),
                self.t.animate.set_value(T_LO),
                run_time=1.25,
                rate_func=smooth,
            )

        gap_trace = always_redraw(
            lambda: self._curve_of(self.table, COLLAPSE)
        )
        self.add(gap_trace)

        with self.voiceover(
            text="Now watch the gap. Wherever the fingerprints separate, the "
                 "curve rises; where they agree, it settles back toward zero."
        ) as tracker:
            self.across(
                tracker,
                self.t.animate.set_value(T_HI),
                floor=6.0,
                rate_func=linear,
            )

        with self.voiceover(
            text="To compress this curve into one number, we still need to "
                 "decide how strongly each frequency should count."
        ) as tracker:
            self.across(tracker,
                        Indicate(gap_trace, color=COLLAPSE,
                                 scale_factor=1.01),
                        floor=0.9)

        self.gap_trace = gap_trace
        self.t_readout = t_readout
        self.batch_label = batch_label
        self.graph_furniture = VGroup(labels, t_label, head)

    # ------------------------------------------------------------------ 3
    def formula_beat(self):
        weight_axes = Axes(
            x_range=(0, PLOT_T_MAX, 1),
            y_range=(0, 1.05, 0.5),
            x_length=4.7,
            y_length=1.45,
            axis_config={"include_tip": False, "stroke_width": 1.5},
        )
        weight_axes.move_to(np.array([-3.35, -0.75, 0.0]))
        lambda_tracker = ValueTracker(EP_LAMBDA)

        def weight_profile():
            curve = VMobject().set_stroke(TARGET, 3)
            lam = lambda_tracker.get_value()
            curve.set_points_as_corners([
                weight_axes.c2p(
                    t,
                    np.exp(-t * t / (2 * lam ** 2)),
                )
                for t in PLOT_GRID
            ])
            return curve

        live_weight_curve = always_redraw(weight_profile)
        weight_heading = ty.label("frequency influence", color=TARGET)
        weight_heading.next_to(weight_axes, UP, buff=0.22)
        abs_t_label = ty.maths(R"|t|", size=ty.TICK, color=MUTED)
        abs_t_label.next_to(
            weight_axes.c2p(PLOT_T_MAX, 0), DR, buff=0.10,
        )
        weight_eq = ty.maths(
            R"w_\lambda(t)=e^{-t^2/(2\lambda^2)}",
            size=ty.EQ,
            color=TARGET,
        )
        weight_eq.next_to(weight_axes, DOWN, buff=0.24)
        lambda_number = DecimalNumber(
            EP_LAMBDA,
            num_decimal_places=2,
            font_size=ty.READOUT,
            color=TARGET,
        )
        lambda_number.add_updater(
            lambda mob: mob.set_value(lambda_tracker.get_value())
        )
        lambda_readout = VGroup(
            ty.maths(R"\lambda=", size=ty.READOUT, color=TARGET),
            lambda_number,
        ).arrange(RIGHT, buff=0.06)
        lambda_readout.next_to(weight_heading, RIGHT, buff=0.26)
        lambda_readout.align_to(weight_heading, DOWN)
        layout.fit_in_frame(lambda_readout)

        full = MathTex(
            R"\mathcal T=",
            R"N",
            R"\int_{-\infty}^{\infty}",
            R"w_\lambda(t)",
            R"\big|\hat\varphi_N(t)-\varphi_0(t)\big|^2",
            R"\,dt",
            font_size=40,
        ).set_color(INK)
        full[3].set_color(TARGET)
        full[4].set_color(COLLAPSE)
        full.move_to(np.array([0.0, 2.35, 0.0]))
        layout.fit_in_frame(full)

        weighted_table = (
            np.exp(-GRID ** 2 / (2 * EP_LAMBDA ** 2)) * self.table
        )
        self.t.set_value(T_HI)
        weighted_area = self._area_of(weighted_table, COLLAPSE)
        weighted_area.set_fill(COLLAPSE, 0.28)
        weighted_area.set_stroke(COLLAPSE, 2.5, opacity=0.8)

        with self.voiceover(
            text="The taper from the previous scene becomes a Gaussian "
                 "weight. <bookmark mark='weight'/>Its value tells us how much "
                 "influence a frequency receives: strongest near zero, then "
                 "fading smoothly into the tail. "
                 "<bookmark mark='lambda'/>Lambda controls the width of that "
                 "taper."
        ) as tracker:
            self.freeze(
                self.gap_trace,
                self.plane_live,
                self.gap_line,
                self.t_readout,
            )
            self.play(
                FadeOut(VGroup(
                    self.plane,
                    self.plane_live,
                    self.gap_line,
                    self.t_readout,
                    self.batch_label,
                    self.squared,
                )),
                Create(weight_axes),
                FadeIn(weight_heading),
                FadeIn(abs_t_label),
                run_time=0.9,
            )
            self.wait_until_bookmark("weight")
            weight_seed = weight_profile()
            self.play(Create(weight_seed), Write(weight_eq), run_time=0.8)
            self.add(live_weight_curve)
            self.remove(weight_seed)
            self.wait_until_bookmark("lambda")
            self.play(
                FadeIn(lambda_readout, shift=0.08 * LEFT),
                lambda_tracker.animate.set_value(1.65),
                run_time=0.65,
                rate_func=smooth,
            )
            self.play(
                lambda_tracker.animate.set_value(0.70),
                run_time=0.65,
                rate_func=smooth,
            )
            self.play(
                lambda_tracker.animate.set_value(EP_LAMBDA),
                run_time=0.5,
                rate_func=smooth,
            )

        with self.voiceover(
            text="At any t, <bookmark mark='weight_part'/>the yellow curve sets "
                 "the influence, and <bookmark mark='gap_part'/>the red curve "
                 "supplies the squared disagreement. "
                 "<bookmark mark='product'/>Multiplying them gives the weighted "
                 "contribution from that frequency."
        ) as tracker:
            self.wait_until_bookmark("weight_part")
            self.play(
                Indicate(live_weight_curve, color=TARGET, scale_factor=1.015),
                run_time=0.55,
            )
            self.wait_until_bookmark("gap_part")
            self.play(
                Indicate(self.gap_trace, color=COLLAPSE, scale_factor=1.01),
                run_time=0.55,
            )
            self.wait_until_bookmark("product")
            self.play(FadeOut(self.gap_trace), FadeIn(weighted_area),
                      run_time=0.9)

        with self.voiceover(
            text="Now add those weighted contributions across every t. "
                 "<bookmark mark='integral'/>The integration sign performs "
                 "that continuous sum. <bookmark mark='pieces'/>Inside it are "
                 "the weight and the squared gap we just built. "
                 "<bookmark mark='scale'/>Multiplying by N adjusts the "
                 "statistic for the batch size."
        ) as tracker:
            self.play(Write(full[0]), run_time=0.45)
            self.wait_until_bookmark("integral")
            self.play(Write(full[2]), run_time=0.65)
            self.wait_until_bookmark("pieces")
            self.play(Write(VGroup(full[3], full[4])), run_time=0.85)
            self.wait_until_bookmark("scale")
            self.play(
                Write(full[1]),
                Write(full[5]),
                run_time=0.65,
            )
        self.inspect(0.9)

        name = ty.statement("Epps–Pulley statistic", color=TARGET)
        name.move_to(np.array([0.0, 1.15, 0.0]))
        with self.voiceover(
            text="Put those pieces together, and this weighted total is the "
                 "Epps–Pulley statistic."
        ):
            self.freeze(live_weight_curve)
            self.play(
                FadeOut(VGroup(
                    weight_axes,
                    live_weight_curve,
                    weight_heading,
                    abs_t_label,
                    weight_eq,
                    lambda_readout,
                    weighted_area,
                    self.gap_axes,
                    self.graph_furniture,
                )),
                FadeIn(name, shift=0.12 * UP),
                run_time=0.75,
            )

        zero_chain = MathTex(
            R"\mathcal T_{\mathrm{pop}}=0",
            R"\Longrightarrow",
            R"\varphi_X(t)=\varphi_0(t)\quad\forall t",
            R"\Longrightarrow",
            R"X\sim\mathcal N(0,1)",
            font_size=36,
        ).set_color(INK)
        zero_chain[1].set_color(TARGET)
        zero_chain[3].set_color(TARGET)
        zero_chain.move_to(np.array([0.0, -0.7, 0.0]))
        layout.fit_in_frame(zero_chain)

        score_rows = VGroup(
            self._score_row(
                BIMODAL, "two-clump batch", COLLAPSE, EP_BIMODAL_SCORE,
            ),
            self._score_row(
                GAUSS, "bell-shaped batch", CLOUD, EP_GAUSSIAN_SCORE,
            ),
        ).arrange(DOWN, buff=0.58, aligned_edge=LEFT)
        score_rows.move_to(np.array([0.0, -0.72, 0.0]))
        layout.fit_in_frame(score_rows)

        with self.voiceover(
            text="Now bring back the two original batches. "
                 "<bookmark mark='compare'/>If we compare each fingerprint "
                 "with the standard Gaussian, the two clumps give a large "
                 "value, while the bell-shaped batch lands close to zero."
        ) as tracker:
            self.play(
                FadeIn(
                    VGroup(*(row[0] for row in score_rows)),
                    shift=0.10 * UP,
                ),
                run_time=max(
                    0.65,
                    tracker.time_until_bookmark("compare"),
                ),
            )
            self.wait_until_bookmark("compare")
            self.play(
                LaggedStart(
                    *(
                        AnimationGroup(
                            GrowArrow(row[1][0]),
                            FadeIn(row[1][1], shift=0.05 * UP),
                            FadeIn(row[2], shift=0.10 * RIGHT),
                            lag_ratio=0.20,
                        )
                        for row in score_rows
                    ),
                    lag_ratio=0.28,
                ),
                run_time=1.2,
            )

        validation_rows = VGroup(*(
            self._validation_row(batch, score, index)
            for index, (batch, score) in enumerate(
                zip(VALIDATION_BATCHES, VALIDATION_SCORES),
                start=1,
            )
        )).arrange(DOWN, buff=0.24, aligned_edge=RIGHT)
        validation_rows.move_to(np.array([0.0, -0.65, 0.0]))
        layout.fit_in_frame(validation_rows)

        validation_title = ty.line(
            "fresh samples from", R"$\mathcal N(0,1)$",
            size=ty.LABEL,
            color=CLOUD,
        )
        validation_title.next_to(validation_rows, UP, buff=0.28)

        variation_brace = Brace(
            VGroup(*(row[-1] for row in validation_rows)),
            RIGHT,
            color=MUTED,
            buff=0.16,
        )
        variation_label = ty.label("sampling variation", color=MUTED)
        variation_label.scale(0.72)
        variation_label.next_to(variation_brace, RIGHT, buff=0.12)
        variation_group = VGroup(variation_brace, variation_label)

        with self.voiceover(
            text="<bookmark mark='draws'/>Fresh Gaussian batches land at "
                 "<bookmark mark='values'/>slightly different positive values. "
                 "<bookmark mark='near_zero'/>A result near zero means the "
                 "batch fingerprint follows the Gaussian target about as "
                 "closely as <bookmark mark='variation'/>ordinary sampling "
                 "variation allows."
        ) as tracker:
            self.play(FadeOut(score_rows), run_time=0.4)
            self.wait_until_bookmark("draws")
            self.play(
                FadeIn(validation_title, shift=0.08 * UP),
                LaggedStart(
                    *(
                        FadeIn(row, shift=0.12 * RIGHT)
                        for row in validation_rows
                    ),
                    lag_ratio=0.25,
                ),
                run_time=max(1.35, tracker.time_until_bookmark("values")),
            )
            self.wait_until_bookmark("values")
            self.play(
                LaggedStart(
                    *(
                        Indicate(
                            row[-1], color=CLOUD, scale_factor=1.035,
                        )
                        for row in validation_rows
                    ),
                    lag_ratio=0.18,
                ),
                run_time=1.35,
            )
            self.wait_until_bookmark("near_zero")
            self.play(
                Indicate(
                    validation_rows[0][-1],
                    color=TARGET,
                    scale_factor=1.055,
                ),
                run_time=0.85,
            )
            self.wait_until_bookmark("variation")
            self.play(
                FadeIn(variation_group, shift=0.08 * LEFT),
                run_time=0.65,
            )

        with self.voiceover(
            text="At the population level, zero has an exact meaning. "
                 "<bookmark mark='theorem'/>If the score is zero, then the "
                 "characteristic function matches the Gaussian at every t. "
                 "<bookmark mark='distribution'/>The uniqueness theorem then "
                 "forces the distribution itself to be standard Gaussian."
        ) as tracker:
            self.wait_until_bookmark("theorem")
            self.play(
                FadeOut(validation_rows),
                FadeOut(validation_title),
                FadeOut(variation_group),
                FadeOut(name),
                run_time=0.45,
            )
            self.play(Write(zero_chain[:3]), run_time=0.9)
            self.wait_until_bookmark("distribution")
            self.play(Write(zero_chain[3:]), run_time=0.8)

        with self.voiceover(
            text="At the start, these two batches made the missing shape "
                 "information obvious. <bookmark mark='reference'/>Fixing the "
                 "standard Gaussian as the reference turns that visual "
                 "difference into a repeatable score: every batch is judged "
                 "against the same target."
        ) as tracker:
            self.play(
                FadeOut(zero_chain),
                FadeOut(full),
                FadeIn(score_rows, shift=0.10 * UP),
                run_time=0.75,
            )
            self.wait_until_bookmark("reference")
            self.play(
                LaggedStart(
                    *(
                        Indicate(row[1], color=TARGET, scale_factor=1.04)
                        for row in score_rows
                    ),
                    lag_ratio=0.22,
                ),
                run_time=0.95,
            )
            self.across(
                tracker,
                LaggedStart(
                    Indicate(score_rows[0][2], color=COLLAPSE,
                             scale_factor=1.04),
                    Indicate(score_rows[1][2], color=CLOUD,
                             scale_factor=1.04),
                    lag_ratio=0.22,
                ),
                floor=0.8,
            )

        recap_map = MathTex(
            R"(x_1,\ldots,x_N)",
            R"\longmapsto",
            R"\hat\varphi_N(t)",
            R"\longmapsto",
            R"\big|\hat\varphi_N(t)-\varphi_0(t)\big|^2",
            R"\longmapsto",
            R"\mathcal T\in\mathbb R",
            font_size=34,
        )
        recap_map.set_color(INK)
        recap_map[0].set_color(CLOUD)
        recap_map[1].set_color(TARGET)
        recap_map[2].set_color(CLOUD)
        recap_map[3].set_color(TARGET)
        recap_map[4].set_color(COLLAPSE)
        recap_map[5].set_color(TARGET)
        recap_map.move_to(np.array([0.0, -0.25, 0.0]))
        layout.fit_in_frame(recap_map)

        with self.voiceover(
            text="The whole construction now fits in one line. Start with the "
                 "samples, "
                 "<bookmark mark='fingerprint'/>build their empirical "
                 "fingerprint, <bookmark mark='compare'/>compare it with the "
                 "Gaussian fingerprint at every frequency, and "
                 "<bookmark mark='score'/>combine the weighted discrepancies "
                 "into one smooth number."
        ) as tracker:
            self.play(
                FadeOut(score_rows),
                Write(recap_map[0]),
                run_time=max(
                    0.65,
                    tracker.time_until_bookmark("fingerprint"),
                ),
            )
            self.wait_until_bookmark("fingerprint")
            self.play(Write(VGroup(recap_map[1], recap_map[2])), run_time=0.65)
            self.wait_until_bookmark("compare")
            self.play(Write(VGroup(recap_map[3], recap_map[4])), run_time=0.75)
            self.wait_until_bookmark("score")
            self.across(
                tracker,
                Write(VGroup(recap_map[5], recap_map[6])),
                floor=0.65,
            )

        self.inspect(1.25)

        bridge = vector_bridge()
        vector_samples, question_link, vector_score = bridge
        question_arrow, question = question_link

        with self.voiceover(
            text="In the next chapter, we'll discuss how to do the same thing "
                 "with <bookmark mark='vectors'/>a whole batch of vectors."
        ) as tracker:
            self.wait_until_bookmark("vectors")
            self.play(
                FadeOut(recap_map[1:]),
                FadeTransform(recap_map[0], vector_samples),
                run_time=1.2,
                rate_func=smooth,
            )
            self.across(
                tracker,
                GrowArrow(question_arrow),
                FadeIn(question, shift=0.06 * UP),
                FadeIn(vector_score, shift=0.10 * RIGHT),
                floor=0.9,
            )

        self.inspect(1.35)
        self.settle_frame()

    def _curve_of(self, table, colour):
        t = self.t.get_value()
        mask = GRID <= max(t, T_LO + 1e-4)
        xs, ys = GRID[mask], table[mask]
        if len(xs) < 2:
            xs = np.array([T_LO, T_LO + 1e-4])
            ys = np.array([table[0], table[0]])
        curve = VMobject().set_stroke(colour, 3.5)
        curve.set_points_as_corners([
            self.gap_axes.c2p(x, y) for x, y in zip(xs, ys)
        ])
        return curve

    def _area_of(self, table, colour):
        t = self.t.get_value()
        mask = GRID <= max(t, T_LO + 1e-4)
        xs, ys = GRID[mask], table[mask]
        if len(xs) < 2:
            return VMobject()
        points = [self.gap_axes.c2p(xs[0], 0)]
        points.extend(
            self.gap_axes.c2p(x, y) for x, y in zip(xs, ys)
        )
        points.append(self.gap_axes.c2p(xs[-1], 0))
        area = VMobject().set_fill(colour, 0.38).set_stroke(colour, 3)
        area.set_points_as_corners(points + [points[0]])
        return area
