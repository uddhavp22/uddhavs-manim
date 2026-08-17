"""Chapter B.10 — reveal the standard Gaussian target curve.

B09 motivated a smooth frequency taper. This scene makes the Gaussian
reference concrete, using symmetry and the universal value at zero as
predictions before revealing its closed form. It ends on one selected target
point so B11 can introduce the batch point beside it.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import layout
from common.beat import ActScene
from common.fingerprint import CharacteristicFunctionPlot
from common.palette import CLOUD, COLLAPSE, INK, MUTED, TARGET
from common import type as ty


PROBE_T = 1.6


class B10(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        plot = CharacteristicFunctionPlot()
        axes = plot.axes
        plot.mount(self)

        symmetry_picture, real_result = self._symmetry_picture()
        with self.voiceover(
            text="In a standard Gaussian, each value x is balanced by minus x. "
                 "<bookmark mark='components'/>At any t, their vertical arrow "
                 "components cancel, <bookmark mark='real'/>so its fingerprint "
                 "stays on the real axis."
        ) as tracker:
            self.play(
                Create(symmetry_picture[0]),
                Create(symmetry_picture[1]),
                run_time=0.6,
            )
            self.play(
                GrowArrow(symmetry_picture[2]),
                GrowArrow(symmetry_picture[3]),
                run_time=0.75,
            )
            self.wait_until_bookmark("components")
            self.play(
                GrowArrow(symmetry_picture[4][0]),
                GrowArrow(symmetry_picture[4][1]),
                run_time=0.7,
            )
            self.wait_until_bookmark("real")
            self.across(tracker, FadeIn(real_result, shift=0.1 * RIGHT),
                        floor=0.7)

        zero = Dot(axes.c2p(0, 1), radius=0.07).set_fill(TARGET, 1)
        zero_result = ty.maths(
            R"\varphi_0(0)=1", size=ty.EQ, color=INK,
        )
        zero_result.next_to(zero, RIGHT, buff=0.18)
        zero_result.shift(0.16 * UP)
        layout.fit_in_frame(zero_result)

        with self.voiceover(
            text="And when t equals zero, every arrow points to one, which "
                 "<bookmark mark='start'/>fixes the curve's starting point."
        ) as tracker:
            self.play(
                FadeIn(zero, scale=0.7),
                Indicate(zero, color=TARGET, scale_factor=1.18),
                run_time=0.8,
            )
            self.wait_until_bookmark("start")
            self.across(tracker, Write(zero_result), floor=0.7)
        self.inspect(0.55)

        definition = MathTex(
            R"\varphi_0(t)",
            "=",
            R"\mathbb E_{X\sim\mathcal N(0,1)}\!\left[e^{itX}\right]",
            font_size=38,
        ).set_color(INK)
        integral = MathTex(
            R"\varphi_0(t)",
            "=",
            R"\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty}"
            R"e^{itx}e^{-x^2/2}\,dx",
            font_size=38,
        ).set_color(INK)
        formula = MathTex(
            R"\varphi_0(t)",
            "=",
            R"e^{-t^2/2}",
            font_size=ty.EQ_DISPLAY,
        ).set_color(TARGET)
        for calculation in (definition, integral, formula):
            calculation.move_to(np.array([0.0, 2.68, 0.0]))
            layout.fit_in_frame(calculation)
        curve = plot.gaussian_curve()

        with self.voiceover(
            text="For the standard Gaussian, <bookmark mark='average'/>we "
                 "average e raised to the imaginary unit times t times x over "
                 "the bell curve. Written as an "
                 "<bookmark mark='integral'/>integration, this takes a separate "
                 "Gaussian calculation. <bookmark mark='result'/>Its result "
                 "is e raised to minus t squared over two. "
                 "<bookmark mark='curve'/>Because of that negative square, the "
                 "curve falls smoothly from one toward zero."
        ) as tracker:
            self.play(
                FadeOut(VGroup(symmetry_picture, real_result, zero_result)),
                run_time=0.55,
            )
            self.wait_until_bookmark("average")
            self.play(Write(definition), run_time=0.9)
            self.wait_until_bookmark("integral")
            self.play(
                TransformMatchingTex(definition, integral),
                run_time=0.9,
            )
            self.wait_until_bookmark("result")
            self.play(
                TransformMatchingTex(integral, formula),
                run_time=0.9,
            )
            self.wait_until_bookmark("curve")
            self.across(
                tracker,
                Create(curve),
                floor=2.6,
                rate_func=linear,
            )
        self.inspect(0.7)

        probe_t = ValueTracker(0.0)
        probe = always_redraw(
            lambda: plot.gaussian_probe(probe_t.get_value())
        )
        readout = self._target_readout(probe_t)

        with self.voiceover(
            text="So every frequency comes with a precise Gaussian target. "
                 "<bookmark mark='example'/>At t equals one point six, "
                 "<bookmark mark='value'/>for example, that target is about "
                 "point two eight."
        ) as tracker:
            self.add(probe)
            self.play(FadeIn(readout), run_time=0.45)
            self.wait_until_bookmark("example")
            self.play(
                probe_t.animate.set_value(PROBE_T),
                run_time=max(1.0, tracker.time_until_bookmark("value")),
                rate_func=linear,
            )
            self.wait_until_bookmark("value")
            self.play(
                Indicate(readout[1], color=TARGET, scale_factor=1.04),
                run_time=0.8,
            )
            self.across(tracker, Wait(0.1), floor=0.3)
        self.inspect(0.75)

        batch_unknown = ty.maths(
            R"\hat\varphi_N(1.6)=\,?",
            size=ty.EQ_DISPLAY,
            color=CLOUD,
        )
        batch_unknown.move_to(np.array([0.0, 2.58, 0.0]))

        with self.voiceover(
            text="The batch gives us a second point at the same t. "
                 "<bookmark mark='next'/>Their separation is what we add up "
                 "next."
        ) as tracker:
            self.freeze(probe, readout)
            self.play(
                FadeOut(VGroup(formula, readout, zero)),
                FadeIn(batch_unknown, shift=0.1 * UP),
                run_time=0.75,
            )
            self.wait_until_bookmark("next")
            self.play(
                Indicate(
                    VGroup(batch_unknown, probe[1]),
                    color=INK,
                    scale_factor=1.06,
                ),
                run_time=0.8,
            )
            self.across(tracker, Wait(0.1), floor=0.3)

        self.settle_frame()
        # Exact last-frame handoff to B11: bare axes, Gaussian curve, selected
        # Gaussian point, and the unresolved batch value at t = 1.6.

    def _symmetry_picture(self):
        centre = np.array([-3.9, 2.58, 0.0])
        radius = 0.58
        theta = 48 * DEGREES

        horizontal = Line(
            centre + 1.18 * radius * LEFT,
            centre + 1.18 * radius * RIGHT,
        ).set_stroke(MUTED, 1.2, opacity=0.6)
        circle = Circle(radius=radius).move_to(centre)
        circle.set_stroke(MUTED, 1.4, opacity=0.55)

        upper_end = centre + radius * np.array([np.cos(theta), np.sin(theta), 0])
        lower_end = centre + radius * np.array([np.cos(theta), -np.sin(theta), 0])
        upper = Arrow(
            centre,
            upper_end,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.16,
            color=CLOUD,
        )
        lower = Arrow(
            centre,
            lower_end,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.16,
            color=CLOUD,
        )

        projection_x = centre + radius * np.cos(theta) * RIGHT
        components = VGroup(
            Arrow(
                projection_x,
                upper_end,
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.18,
                color=COLLAPSE,
            ),
            Arrow(
                projection_x,
                lower_end,
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.18,
                color=COLLAPSE,
            ),
        )

        result = ty.maths(
            R"\operatorname{Im}\varphi_0(t)=0",
            size=ty.EQ,
            color=INK,
        )
        result.next_to(circle, RIGHT, buff=0.34)
        return VGroup(circle, horizontal, upper, lower, components), result

    def _target_readout(self, tracker):
        t_number = DecimalNumber(
            0.0,
            num_decimal_places=2,
            font_size=ty.READOUT,
            color=INK,
        )
        value_number = DecimalNumber(
            1.0,
            num_decimal_places=3,
            font_size=ty.READOUT,
            color=TARGET,
        )
        t_number.add_updater(
            lambda mob: mob.set_value(tracker.get_value())
        )
        value_number.add_updater(
            lambda mob: mob.set_value(np.exp(-tracker.get_value() ** 2 / 2))
        )

        t_row = VGroup(
            ty.maths("t=", size=ty.READOUT, color=INK),
            t_number,
        ).arrange(RIGHT, buff=0.08)
        target_row = VGroup(
            ty.maths(R"\varphi_0(t)=", size=ty.READOUT, color=TARGET),
            value_number,
        ).arrange(RIGHT, buff=0.08)
        readout = VGroup(t_row, target_row).arrange(RIGHT, buff=0.7)
        readout.move_to(np.array([0.0, 2.03, 0.0]))
        return readout
