"""Chapter B.8 — the complete characteristic function is unique.

B07 showed why one frequency can be fooled. Here those isolated readings grow
into the full curve, which earns the uniqueness question before the theorem is
stated. The last beat introduces the practical gap between a population curve
and a finite-batch estimate, handing the shared axes directly to B09.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import layout
from common.beat import ActScene
from common.fingerprint import CharacteristicFunctionPlot
from common.palette import EMPIRICAL, INK, MUTED, TARGET
from common import type as ty
from common.wrap import ecf


class B08(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        plot = CharacteristicFunctionPlot()
        plot.mount(self)

        grid = np.linspace(0.0, layout.FREQUENCY_T_MAX, 500)
        values = np.exp(-0.12 * grid**2) * np.cos(1.15 * grid)
        probe_ts = np.array([0.0, 1.2, 2.4, 3.6, 5.2, 6.3])
        probe_values = np.exp(-0.12 * probe_ts**2) * np.cos(1.15 * probe_ts)
        probes = VGroup(*(
            plot.probe(t, value)
            for t, value in zip(probe_ts, probe_values)
        ))
        first_probe = probes[2]
        remaining_probes = VGroup(*(
            probe for index, probe in enumerate(probes) if index != 2
        ))
        sweep = ValueTracker(0.0)
        curve = plot.partial_curve(grid, values, sweep)

        with self.voiceover(
            text="As t varies, <bookmark mark='curve'/>those answers fill out "
                 "the characteristic function."
        ) as tracker:
            self.play(FadeIn(first_probe, shift=0.12 * UP), run_time=0.55)
            self.play(
                Indicate(first_probe, color=EMPIRICAL, scale_factor=1.06),
                run_time=max(0.8, tracker.time_until_bookmark("curve")),
            )
            self.wait_until_bookmark("curve")
            self.add(curve)
            self.across(
                tracker,
                lagged_map(
                    FadeIn,
                    remaining_probes,
                    shift=0.12 * UP,
                    lag_ratio=0.16,
                ),
                sweep.animate.set_value(layout.FREQUENCY_T_MAX),
                floor=2.2,
                rate_func=linear,
            )
        self.freeze(curve)

        one_lhs = ty.maths(
            R"\varphi_X(t_0)=\varphi_Y(t_0)",
            size=ty.EQ_DISPLAY,
            color=INK,
        )
        not_implication = ty.maths(
            R"\not\Longrightarrow", size=ty.EQ_DISPLAY, color=TARGET,
        )
        rhs = ty.maths(
            R"X\overset{d}{=}Y", size=ty.EQ_DISPLAY, color=INK,
        )
        one_value = VGroup(one_lhs, not_implication, rhs)
        one_value.arrange(RIGHT, buff=0.34)
        one_value.move_to(0.85 * UP)
        layout.fit_in_frame(one_value)

        full_lhs = ty.maths(
            R"\varphi_X(t)=\varphi_Y(t)\quad\text{for every }t",
            size=ty.EQ_DISPLAY,
            color=INK,
        )
        implication = ty.maths(
            R"\Longrightarrow", size=ty.EQ_DISPLAY, color=TARGET,
        )
        rhs_target = rhs.copy()
        full_layout = VGroup(full_lhs, implication, rhs_target)
        full_layout.arrange(RIGHT, buff=0.34)
        full_layout.move_to(one_value)
        layout.fit_in_frame(full_layout)
        theorem = VGroup(full_lhs, implication, rhs)

        theorem_name = ty.words(
            "uniqueness theorem", size=ty.BODY, color=MUTED,
        )
        theorem_name.next_to(full_layout, DOWN, buff=0.38)

        with self.voiceover(
            text="The uniqueness theorem tells us how much stronger that full "
                 "curve is. "
                 "<bookmark mark='one'/>Two distributions may agree at one "
                 "value of t. <bookmark mark='full'/>But if their "
                 "characteristic functions agree for every t, then they are "
                 "the same distribution. We'll use that result without "
                 "proving it here."
        ) as tracker:
            self.play(
                FadeOut(probes),
                curve.animate.set_stroke(opacity=0.13),
                FadeIn(theorem_name, shift=0.08 * UP),
                run_time=0.7,
            )
            self.play(
                Indicate(curve, color=TARGET, scale_factor=1.005),
                run_time=max(0.8, tracker.time_until_bookmark("one")),
            )
            self.wait_until_bookmark("one")
            self.play(FadeIn(one_value, shift=0.12 * UP), run_time=0.65)
            self.play(
                Indicate(one_value, color=TARGET, scale_factor=1.015),
                run_time=max(0.8, tracker.time_until_bookmark("full")),
            )
            self.wait_until_bookmark("full")
            self.play(
                TransformMatchingTex(one_lhs, full_lhs),
                ReplacementTransform(not_implication, implication),
                rhs.animate.move_to(rhs_target),
                run_time=0.9,
            )
            self.across(
                tracker,
                Indicate(
                    theorem,
                    color=TARGET,
                    scale_factor=1.015,
                ),
                floor=1.8,
            )

        # A real finite batch from the same symmetric mixture. Its horizontal
        # characteristic-function coordinate visibly departs from the smooth
        # population curve, especially at higher frequencies.
        rng = np.random.default_rng(20260809)
        components = rng.choice((-1.15, 1.15), size=36)
        samples = components + np.sqrt(0.24) * rng.standard_normal(36)
        estimate_values = ecf(samples, grid).real
        estimate = plot.curve(grid, estimate_values, EMPIRICAL, width=3.5)

        with self.voiceover(
            text="<bookmark mark='estimate'/>With a finite batch, we only "
                 "estimate this curve. "
                 "<bookmark mark='where'/>Before we turn that estimate into a "
                 "score, we need to find out which frequencies are actually "
                 "useful."
        ) as tracker:
            self.play(
                FadeOut(VGroup(theorem, theorem_name)),
                curve.animate.set_stroke(opacity=0.9),
                run_time=max(0.7, tracker.time_until_bookmark("estimate")),
            )
            self.wait_until_bookmark("estimate")
            self.play(
                Create(estimate),
                run_time=max(1.6, tracker.time_until_bookmark("where")),
                rate_func=linear,
            )
            self.wait_until_bookmark("where")
            self.across(
                tracker,
                Indicate(estimate, color=EMPIRICAL, scale_factor=1.01),
                floor=1.0,
            )

        self.play(FadeOut(VGroup(curve, estimate)), run_time=0.55)
        self.settle_frame()
        # Exact last-frame handoff to B09: the shared frequency axes remain.
