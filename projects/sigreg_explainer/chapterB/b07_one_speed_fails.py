"""Chapter B.7 — one wrapping speed is not enough.

B06 established that t=0 cannot distinguish any two batches.  This scene tests
the tempting repair: choose one nonzero frequency and trust its one reading.
The counterexample is exact.  Seven samples spread across 4*pi units all wrap
to the same direction at t=3, so their average has length one—the same reading
as total collapse.  A small change in t exposes the spread immediately.

The scene ends on the shared frequency axes used by B08, where the question
changes from one reading to the complete curve.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b07_one_speed_fails.py B07 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import data, layout
from common.beat import ActScene
from common.fingerprint import CharacteristicFunctionPlot
from common.palette import AVERAGE, CLOUD, COLLAPSE, EMPIRICAL, MUTED, TARGET
from common import type as ty
from common.wrap import ecf, unit_arrow_tips


class B07(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.aliasing_beat()

    def aliasing_beat(self):
        samples = data.aliased_1d()
        t = ValueTracker(2.4)

        # Begin with the batch at a readable scale.  The same objects become
        # the left side of the experiment; they are never replaced by copies.
        line = NumberLine(
            x_range=(-7, 7, 2),
            length=10.2,
            include_numbers=True,
            include_tip=False,
        ).set_stroke(MUTED, 2)
        line.shift(np.array([0.0, 0.25, 0.0]) - line.number_to_point(0))
        dots = VGroup(*(
            Dot(line.number_to_point(value), radius=0.085).set_fill(CLOUD, 1)
            for value in samples
        ))

        with self.voiceover(
            text="Could one carefully chosen value of t identify an entire "
                 "batch of numbers?"
        ) as tracker:
            self.play(Create(line), run_time=0.7, rate_func=smooth)
            self.play(
                lagged_map(FadeIn, dots, lag_ratio=0.10),
                run_time=0.7,
                rate_func=smooth,
            )
            self.across(
                tracker,
                Indicate(dots, color=CLOUD, scale_factor=1.04),
                floor=0.7,
            )

        # The same objects settle into the chapter's established three-column
        # grammar: numbers, directions, measurement.
        target_line = NumberLine(
            x_range=(-7, 7, 2),
            length=layout.RIG_LINE_WIDTH,
            include_numbers=True,
            include_tip=False,
        ).set_stroke(MUTED, 2)
        target_line.shift(
            layout.RIG_LINE_CENTRE - target_line.number_to_point(0)
        )
        target_dots = VGroup(*(
            Dot(target_line.number_to_point(value), radius=0.065)
            .set_fill(CLOUD, 1)
            for value in samples
        ))

        circle = layout.rig_circle()
        titles = VGroup(
            ty.caption("sample values").move_to(
                [layout.RIG_LINE_CENTRE[0], layout.RIG_TITLE_Y, 0.0]
            ),
            ty.caption("wrapped directions").move_to(
                [layout.RIG_CIRCLE_CENTRE[0], layout.RIG_TITLE_Y, 0.0]
            ),
        )

        def wrapped_arrows():
            centre = layout.RIG_CIRCLE_CENTRE
            tips = unit_arrow_tips(
                samples, t.get_value(), layout.RIG_CIRCLE_RADIUS, centre
            )
            return VGroup(*(
                VGroup(
                    Arrow(
                        centre, tip, buff=0.0, stroke_width=2.4,
                        tip_length=0.14,
                    ).set_color(CLOUD).set_opacity(0.62),
                    Dot(tip, radius=0.045).set_fill(CLOUD, 1),
                )
                for tip in tips
            ))

        def average_point():
            z = ecf(samples, [t.get_value()])[0]
            return (
                layout.RIG_CIRCLE_CENTRE
                + layout.RIG_CIRCLE_RADIUS
                * np.array([z.real, z.imag, 0.0])
            )

        def average_arrow():
            point = average_point()
            return VGroup(
                Arrow(
                    layout.RIG_CIRCLE_CENTRE,
                    point,
                    buff=0.0,
                    stroke_width=6,
                    tip_length=layout.AVERAGE_ARROW_TIP_LENGTH,
                ).set_color(AVERAGE),
                Dot(point, radius=layout.ARROW_TIP_DOT_RADIUS)
                .set_fill(AVERAGE, 1),
            )

        arrows = always_redraw(wrapped_arrows)
        average = always_redraw(average_arrow)

        t_symbol = ty.maths(R"t =", size=ty.READOUT, color=TARGET)
        t_placeholder = DecimalNumber(
            t.get_value(), num_decimal_places=2, font_size=ty.READOUT
        ).set_color(TARGET)
        t_row = VGroup(t_symbol, t_placeholder).arrange(RIGHT, buff=0.12)
        t_row.move_to([layout.RIG_CF_CENTRE[0], 0.68, 0.0])

        def t_number():
            number = DecimalNumber(
                t.get_value(), num_decimal_places=2, font_size=ty.READOUT
            ).set_color(TARGET)
            number.move_to(t_placeholder)
            return number

        live_t = always_redraw(t_number)

        score_label = ty.words("average length", size=ty.BODY)
        score_label.move_to([layout.RIG_CF_CENTRE[0], -0.02, 0.0])
        score_placeholder = DecimalNumber(
            1.0, num_decimal_places=3, font_size=ty.EQ_HERO
        ).next_to(score_label, DOWN, buff=0.20)
        score_box = SurroundingRectangle(
            VGroup(t_row, score_label, score_placeholder), buff=0.3
        ).set_stroke(MUTED, 1.6)

        def score_number():
            value = float(abs(ecf(samples, [t.get_value()])[0]))
            colour = COLLAPSE if value > 0.9 else EMPIRICAL
            number = DecimalNumber(
                value, num_decimal_places=3, font_size=ty.EQ_HERO
            ).set_color(colour)
            number.move_to(score_placeholder)
            return number

        score = always_redraw(score_number)

        with self.voiceover(
            text="Suppose the chosen value is <bookmark mark='wrap'/>t "
                 "equals two point four. The directions partly cancel, "
                 "<bookmark mark='average'/>leaving an average length of "
                 "about point two three."
        ) as tracker:
            self.play(
                Transform(line, target_line),
                Transform(dots, target_dots),
                FadeIn(circle),
                FadeIn(titles),
                FadeIn(t_symbol),
                FadeIn(live_t),
                FadeIn(score_label),
                Create(score_box),
                run_time=max(0.9, tracker.time_until_bookmark("wrap")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("wrap")
            self.play(
                FadeIn(arrows),
                run_time=0.7,
                rate_func=smooth,
            )
            self.wait_until_bookmark("average")
            self.play(
                FadeIn(average),
                FadeIn(score),
                run_time=0.55,
                rate_func=smooth,
            )
            self.across(
                tracker,
                Indicate(VGroup(average, score), color=AVERAGE,
                         scale_factor=1.04),
                floor=0.65,
            )

        with self.voiceover(
            text="Now try <bookmark mark='three'/>t equals three. Each angle "
                 "becomes a whole number of turns, "
                 "<bookmark mark='align'/>so all seven directions land "
                 "together. <bookmark mark='score'/>The average length "
                 "becomes one, exactly what total collapse would produce."
        ) as tracker:
            self.wait_until_bookmark("three")
            self.play(
                t.animate.set_value(data.ALIAS_T),
                run_time=max(1.0, tracker.time_until_bookmark("align")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("align")
            self.play(
                ShowPassingFlash(
                    wrapped_arrows().copy().set_color(TARGET),
                    time_width=0.55,
                ),
                run_time=0.9,
            )
            self.wait_until_bookmark("score")
            self.play(
                Flash(score.get_center(), color=COLLAPSE,
                      flash_radius=0.55, line_length=0.16),
                run_time=0.7,
            )

        with self.voiceover(
            text="But if we <bookmark mark='nudge'/>nudge t back down to two "
                 "point six, <bookmark mark='settle'/>those same samples "
                 "produce directions that mostly cancel, "
                 "<bookmark mark='conclusion'/>which means a single t cannot "
                 "reliably identify a batch."
        ) as tracker:
            self.wait_until_bookmark("nudge")
            self.play(
                t.animate.set_value(2.6),
                run_time=max(1.2, tracker.time_until_bookmark("settle")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("settle")
            self.play(
                Indicate(VGroup(arrows, average), color=AVERAGE,
                         scale_factor=1.04),
                run_time=0.8,
            )
            self.wait_until_bookmark("conclusion")
            self.play(
                Indicate(VGroup(live_t, score), color=TARGET,
                         scale_factor=1.04),
                run_time=0.8,
            )

        with self.voiceover(
            text="One answer can be fooled. <bookmark mark='sweep'/>So keep "
                 "the batch's answers across the whole range of t."
        ) as tracker:
            self.wait_until_bookmark("sweep")

            handoff = CharacteristicFunctionPlot()
            outgoing = list(self.mobjects)
            self.freeze(*outgoing)
            self.play(
                FadeOut(Group(*outgoing)),
                FadeIn(handoff.axes),
                FadeIn(handoff.furniture),
                run_time=max(0.9, tracker.get_remaining_duration()),
                rate_func=smooth,
            )

        self.settle_frame()
        # Exact last-frame handoff to B08: the shared frequency axes remain.
