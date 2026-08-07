"""Chapter B — one wrapping speed is not enough.

Ported from the rev-3 Act 4 (the aliasing beat), now narrated. Follows
b03_three_panels: the viewer has just watched a curve get traced, so the
natural question is "why sweep t at all — why not pick a good one?"

The answer is exact, not rhetorical. A batch whose values are all multiples of
2*pi/t sends every arrow to the same spot, so |phi(t)| = 1.0000 -- identical to
total collapse -- for a batch with standard deviation 4.19. Any other frequency
exposes it immediately.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b06a_one_speed_fails.py B06A -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import data, layout
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, EMPIRICAL, FAINT, MUTED, TARGET
from common import type as ty
from common.wrap import ecf, unit_arrow_tips



class B06A(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.aliasing_beat()

    def aliasing_beat(self):
        h = data.aliased_1d()
        t_bad = data.ALIAS_T
        t_tr = ValueTracker(t_bad)

        # The rhetorical-question header is deleted: the narration asks the
        # same question in the same breath, and a question pinned to the top of
        # the frame for the whole scene is a caption that answers nothing.
        # -7..7, not -6..6: the batch runs to +/-6.28 (three multiples of
        # 2*pi/3), so on a +/-6 axis the two outermost samples hang off the
        # ends of the line they are supposed to be sitting on.
        nl = NumberLine(x_range=(-7, 7, 2), length=10.0, include_numbers=True,
                        include_tip=False)
        nl.set_stroke(MUTED, 2)
        nl.move_to(np.array([0.0, 1.5, 0.0]))
        dots = VGroup(*(
            Dot(nl.number_to_point(v), radius=0.075).set_fill(CLOUD, 1)
            for v in h))

        with self.voiceover(
            text="Sweeping every frequency is expensive. If one well "
                 "chosen value of t did the job, the sweep would be "
                 "waste."
        ) as tracker:
            self.play(Create(nl), run_time=1.2)
            self.across(tracker, lagged_map(FadeIn, dots, lag_ratio=0.10),
                        floor=1.0)

        with self.voiceover(
            text="This batch is spread across nearly thirteen units. By "
                 "any reasonable reading it has not collapsed."
        ) as tracker:
            # "range", not "spread": the standard deviation of this batch is
            # 4.19, and a vague label beside a 12.6 would read as one of the
            # two numbers being wrong. facts.py carries both.
            span = ty.line("range", R"$= 12.6$", size=ty.LABEL, color=CLOUD)
            span.next_to(nl, UP, buff=0.35)
            # Draw the extent the number is measuring, rather than pulsing the
            # dots by 10% for five seconds -- which is what filled this block
            # before, and which reads as a still frame.
            lo, hi = float(h.min()), float(h.max())
            bar_y = nl.number_to_point(0)[1] + 0.22
            ends = [np.array([nl.number_to_point(v)[0], bar_y, 0.0])
                    for v in (lo, hi)]
            bracket = VGroup(
                Line(ends[0], ends[1]),
                Line(ends[0] + 0.09 * DOWN, ends[0] + 0.09 * UP),
                Line(ends[1] + 0.09 * DOWN, ends[1] + 0.09 * UP),
            ).set_stroke(CLOUD, 2.4)
            self.play(FadeIn(span), run_time=0.6)
            self.across(tracker, Create(bracket), floor=0.9)
            self.bracket = bracket
        self.span = span

        r = 1.3
        centre = np.array([-3.1, -1.75, 0.0])
        panel = VGroup(
            Circle(radius=r).set_stroke(MUTED, 1.8, opacity=0.55).move_to(centre),
            Line(centre + 1.75 * LEFT, centre + 1.75 * RIGHT).set_stroke(FAINT, 1.2),
            Line(centre + 1.65 * DOWN, centre + 1.65 * UP).set_stroke(FAINT, 1.2),
        )
        arrows = always_redraw(lambda: VGroup(*(
            Line(centre, p).set_stroke(CLOUD, 2.4, opacity=0.6)
            for p in unit_arrow_tips(h, t_tr.get_value(), r, centre))))

        def cpt():
            z = ecf(h, [t_tr.get_value()])[0]
            return centre + r * np.array([z.real, z.imag, 0.0])

        centroid = always_redraw(lambda: VGroup(
            Line(centre, cpt()).set_stroke(EMPIRICAL, 6),
            Dot(cpt(), radius=0.1).set_fill(EMPIRICAL, 1)))

        mag = always_redraw(lambda: VGroup(
            ty.line("average length", "$=$", size=ty.BODY),
            DecimalNumber(float(abs(ecf(h, [t_tr.get_value()])[0])),
                          num_decimal_places=3, font_size=ty.READOUT),
        ).arrange(RIGHT, buff=0.12)
            .set_color(COLLAPSE if abs(ecf(h, [t_tr.get_value()])[0]) > 0.9
                       else EMPIRICAL)
            .move_to(np.array([2.6, -1.1, 0.0])))

        readout = always_redraw(lambda: layout.freq_readout(t_tr))

        # Was one Text carrying an em dash and a pair of straight quotes. It is
        # two different things: an observation about the picture, and the
        # verdict a one-frequency test would return. Split, and the verdict set
        # as the reading it is rather than as a quoted word.
        verdict = VGroup(
            ty.words("every arrow lands on the same spot", size=ty.LABEL),
            ty.line("this test reports", R"$|\varphi| = 1$", size=ty.LABEL),
        ).arrange(DOWN, buff=0.18).set_color(COLLAPSE)
        verdict.move_to(np.array([2.6, -2.5, 0.0]))
        layout.fit_in_frame(verdict)

        with self.voiceover(
            text="Wrapped at this particular frequency, though, every "
                 "arrow lands on the same spot and the average has length "
                 "one. "
                 "<bookmark mark='verdict'/>Which is the reading a completely collapsed batch would "
                 "produce."
        ) as tracker:
            self.play(FadeIn(panel), Create(arrows), run_time=1.4)
            self.play(FadeIn(centroid), FadeIn(mag), run_time=1.0)
            self.add(readout)
            self.wait_until_bookmark("verdict")
            self.play(Write(verdict), run_time=1.4)
            self.across(tracker, Indicate(mag, scale_factor=1.10,
                                          color=COLLAPSE), floor=0.8)

        # The contradiction is the whole scene: a batch spread over twelve
        # units, and a test reporting total collapse, both on screen at once.
        # It needs a moment with nothing said over it.
        self.inspect(1.8)

        # "nudge the speed, and the illusion breaks" is deleted -- an aphorism
        # restating the sentence being spoken over it.
        with self.voiceover(
            text="The agreement survives almost no change in t. Nudge the "
                 "frequency and the arrows scatter, and the average falls "
                 "away to almost nothing."
        ) as tracker:
            self.play(FadeOut(verdict), run_time=0.5)
            self.across(tracker, t_tr.animate.set_value(1.7), floor=3.0)

        # Correction 3 (SCRIPT_REVISION_partA.md Step 3).
        #
        # The old close said the sweep "removes that option". It does not. It
        # removes THIS coincidence: a handful of other frequencies expose this
        # batch immediately, which is what the animation just showed. A finite
        # set of frequencies can still fail to separate some pair of
        # distributions, and only the full characteristic function carries the
        # uniqueness guarantee. That distinction has to survive into Part 2,
        # where the practical method samples finitely many knots -- so it is
        # flagged here rather than quietly assumed away.
        with self.voiceover(
            text="The samples happened to be spaced at multiples of the "
                 "wrapping period, and any single frequency has a batch "
                 "built the same way. Asking at several frequencies breaks "
                 "this particular coincidence, because no batch can be in "
                 "step with all of them at once. Whether finitely many "
                 "frequencies are enough to separate any two distributions "
                 "is a stronger question, and the answer to it belongs to "
                 "the whole curve rather than to any list of points on it."
        ) as tracker:
            probes = [2.4, 4.1, 5.2]
            for i, t in enumerate(probes):
                self.play(t_tr.animate.set_value(t),
                          run_time=max(0.9, (tracker.get_remaining_duration()
                                             - 1.0) / (len(probes) - i)))

        self.clear_beat()
