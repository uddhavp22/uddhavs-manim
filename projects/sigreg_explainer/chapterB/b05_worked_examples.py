"""Chapter B.5 — worked examples on one continuous rig.

Each teaches exactly one thing, and each is exact rather than illustrative
(verified in facts.py, PLAN.md section 7):

    constant  X = c    -> |phi(t)| = 1 for every t.   No uncertainty, no cancellation.
    two-point X = +/-1 -> phi(t) = cos t exactly.     Imaginary part identically zero.
    shift     Y = X + mu -> phase changes, magnitude does not.

The examples now remain in one scene. They all ask the same three-panel rig a
different question, so a cut between them made the chapter feel episodic rather
than like one developing experiment.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b05_worked_examples.py B05 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, EMPIRICAL, MAGNITUDE, MUTED, TARGET
from common import type as ty
from common.rig import ThreePanelRig


T_MAX = 6.5
CONSTANT = np.full(7, 0.9)
TWO_POINT = np.array([-1.0, 1.0])


class B05(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.rig = ThreePanelRig(CONSTANT, t_max=T_MAX, line_range=(-3, 3, 1))
        self.rig.mount(self, dot_colour=COLLAPSE)
        self.constant_beat()
        self.two_point_beat()
        self.shift_beat()

    # ------------------------------------------------------------------ 1
    def constant_beat(self):
        r = self.rig
        r.colour = COLLAPSE
        # Plot |phi|, not Re phi: the point here is that nothing cancels, so
        # the average keeps its LENGTH. Re phi would just oscillate as
        # cos(0.9 t) and contradict the line.
        r.show_abs = True

        # Was a single Text carrying an em dash and a Unicode phi set as
        # Helvetica prose. Split into what it actually is: a plain-English
        # label for the batch, and the quantity being plotted, as mathematics.
        label = ty.words("every value the same", size=ty.LABEL, color=COLLAPSE)
        plotted = ty.maths(R"|\varphi(t)|", size=ty.EQ, color=COLLAPSE)
        caption = VGroup(label, plotted).arrange(RIGHT, buff=0.45)
        caption.move_to(np.array([0.0, -3.3, 0.0]))

        # Row 15: the fragment opener "The degenerate case first:" announced
        # the running order rather than the batch. State the batch.
        with self.voiceover(
            text="So before trusting what it keeps, we should try the most "
                 "extreme case, where every sample is in the same place."
        ) as tracker:
            self.play(FadeIn(caption), run_time=1.0)
            self.across(tracker, r.t.animate.set_value(0.8),
                        Indicate(plotted, scale_factor=1.08,
                                 color=COLLAPSE), floor=0.8,
                        rate_func=smooth)

        with self.voiceover(
            text="Every value now wraps to the same angle, so nothing would "
                 "cancel, and the arrows stay stacked. If we model the "
                 "magnitude of the arrow, it stays at one."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=5.0,
                        rate_func=linear)

        result = ty.line(R"$|\varphi(t)| = 1$", "for every", "$t$",
                         size=ty.STATEMENT, color=COLLAPSE)
        result.move_to(np.array([0.0, -3.3, 0.0]))

        with self.voiceover(
            text="The flat curve we see is the magnitude of the function, "
                 "not the characteristic function itself. For a collapsed "
                 "batch, its magnitude stays one at every frequency."
        ) as tracker:
            self.play(FadeOut(caption), FadeIn(result), run_time=1.0)
            self.across(tracker, r.t.animate.set_value(0.0),
                        Indicate(result, scale_factor=1.06,
                                 color=COLLAPSE), floor=1.5,
                        rate_func=linear)

        # A flat line is the easiest thing in the chapter to miss, because
        # nothing moved. A moment to notice that nothing moved.
        self.inspect(1.4)

        self.constant_result = result

    # ------------------------------------------------------------------ 2
    def two_point_beat(self):
        r = self.rig

        with self.voiceover(
            text="If we try the smallest symmetric batch next, it's minus "
                 "one and plus one."
        ) as tracker:
            # Return to the common t=0 anchor while the magnitude trace is
            # still selected. Switching show_abs at t=6.5 made panel three
            # jump from a flat magnitude curve to an oscillating real curve on
            # the first frame of the batch transition.
            self.play(FadeOut(self.constant_result),
                      r.t.animate.set_value(0.0), run_time=0.8,
                      rate_func=smooth)
            r.show_abs = False
            r.swap(self, TWO_POINT, EMPIRICAL, CLOUD)
            self.across(tracker, Indicate(r.mounted_dots, scale_factor=1.2,
                                          color=CLOUD), floor=0.8)

        # Row 17: the mirror-cancellation argument was re-derived here having
        # been proved in b03. Back-reference instead -- NARRATION_SPEC.md
        # section 21, repetition is deliberate or it is padding.
        with self.voiceover(
            text="Their vertical pieces cancel, while the horizontal pieces "
                 "agree. Look at the average as the pair turns."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=5.5,
                        rate_func=linear)

        expanded = ty.maths(
            R"{{\varphi(t) =}} \tfrac{1}{2}e^{it} + \tfrac{1}{2}e^{-it}",
            size=ty.EQ_DISPLAY, color=EMPIRICAL)
        expanded.move_to(np.array([0.0, -3.3, 0.0]))
        layout.fit_in_frame(expanded)

        result = ty.maths(R"{{\varphi(t) =}} \cos t", size=ty.EQ_DISPLAY,
                          color=EMPIRICAL)
        result.move_to(np.array([0.0, -3.3, 0.0]))

        # Row 18 -- "Two arrows turning, and their average. The cosine arrived
        # without an integral being evaluated." -- deleted. The first sentence
        # narrates the picture; the second grades the derivation, which is
        # evaluative framing (NARRATION_SPEC.md section 5). What replaces it
        # says where the cosine came from, which is information.
        with self.voiceover(
            text="It produces one half of e to the i t, plus one half of e to "
                 "the minus i t, <bookmark mark='simplify'/>which simplifies "
                 "to the cosine of t."
        ) as tracker:
            self.play(Write(expanded),
                      run_time=max(1.3,
                                   tracker.time_until_bookmark("simplify")))
            self.wait_until_bookmark("simplify")
            self.play(TransformMatchingTex(
                expanded, result, transform_mismatches=True), run_time=0.8)
            # Measured on the rev-3 master: 00:38-00:47 of this scene was one
            # unchanging frame with t parked at 6.50, because the only thing
            # filling the block was an Indicate on a line of text. Running the
            # sweep back through the cosine while the sentence claims it is a
            # cosine is the same time spent on the claim's evidence.
            self.across(tracker, r.t.animate.set_value(1.0), floor=1.0,
                        rate_func=smooth)

        self.inspect(1.2, r.t.animate.set_value(T_MAX), rate_func=smooth)
        self.two_point_result = result

    # ------------------------------------------------------------------ 3
    def shift_beat(self):
        """Keep the rig on screen and ask the next, sharper question."""
        r = self.rig
        r.show_abs = False

        mag_lab = ty.maths(R"|\varphi(t)|", size=ty.TICK, color=MAGNITUDE)
        mag_lab.move_to(r.axes.c2p(5.2, 0.72))

        # The two blocks that used to open this beat are one. The first ended
        # in `across(Indicate(mounted_dots))` -- six dots pulsing 12% against a
        # rig parked at t = 0 -- which measured nine seconds of still frame at
        # 00:47-00:56 on the rev-3 master. The batch now moves into its new
        # positions and the sweep starts inside the same sentence, so the amber
        # curve is being drawn while it is being described.
        with self.voiceover(
            text="Put a spread batch back on the circle and track the "
                 "length of its arrow. "
                 "<bookmark mark='sweep'/>As the frequency climbs, that length "
                 "nearly vanishes, then rises again."
        ) as tracker:
            self.play(FadeOut(self.two_point_result), run_time=0.4)
            r.swap(self, data.SPREAD_6, EMPIRICAL, CLOUD)
            self.mag_curve = always_redraw(lambda: r.trace_abs(colour=MAGNITUDE))
            self.add(self.mag_curve)
            self.play(FadeIn(mag_lab), run_time=0.5)
            self.wait_until_bookmark("sweep")
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=3.2,
                        rate_func=linear)

        ghost = r.trace_abs().copy().set_stroke(MAGNITUDE, 11, opacity=0.32)

        with self.voiceover(
            text="Suppose all the points shift three units right. The shape "
                 "hasn't changed, and we run exactly the same sweep."
        ) as tracker:
            self.play(FadeIn(ghost), run_time=0.55)
            r.swap(self, data.SPREAD_6 + data.SHIFT_MU, EMPIRICAL, CLOUD)
            # "and run exactly the same sweep" -- so the sweep starts here
            # rather than after a pause with the dots pulsing at t = 0. The
            # next block carries it on from wherever this one leaves it.
            self.across(tracker, r.t.animate.set_value(1.2), floor=0.8,
                        rate_func=smooth)

        with self.voiceover(
            text="Every arrow turns together. The blue curve keeps changing, "
                 "while the magnitude returns to its old trace."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=4.5,
                        rate_func=linear)

        identity = ty.maths(R"\varphi_{X+\mu}(t) = e^{i\mu t}\,\varphi_X(t)",
                            size=ty.EQ_DISPLAY, color=TARGET)
        magnitude_fact = ty.maths(R"|e^{i\mu t}| = 1", size=ty.EQ,
                                  color=MAGNITUDE)
        full_value = ty.words("the full complex value still changes",
                              size=ty.LABEL, color=EMPIRICAL)
        block = VGroup(identity, magnitude_fact, full_value).arrange(
            DOWN, buff=0.08)
        block.move_to(np.array([0.0, -2.85, 0.0]))
        layout.fit_in_frame(block)
        with self.voiceover(
            text="The shift rotates the full complex value, while "
                 "<bookmark mark='why'/>its magnitude stays the same. When we "
                 "compare distributions, we will keep the full complex point."
        ) as tracker:
            self.play(Write(identity),
                      run_time=max(1.0, tracker.time_until_bookmark("why")))
            self.wait_until_bookmark("why")
            self.across(tracker, r.t.animate.set_value(2.2),
                        Write(magnitude_fact), FadeIn(full_value), floor=1.0,
                        rate_func=smooth)

        self.clear_beat()
