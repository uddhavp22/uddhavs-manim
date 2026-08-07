"""Chapter B.6 — worked examples on one continuous rig.

Each teaches exactly one thing, and each is exact rather than illustrative
(verified in facts.py, PLAN.md section 7):

    constant  X = c    -> |phi(t)| = 1 for every t.   No uncertainty, no cancellation.
    two-point X = +/-1 -> phi(t) = cos t exactly.     Imaginary part identically zero.
    shift     Y = X + mu -> phase changes, magnitude does not.

The examples now remain in one scene. They all ask the same three-panel rig a
different question, so a cut between them made the chapter feel episodic rather
than like one developing experiment.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b06_worked_examples.py B06 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import layout
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, EMPIRICAL, MUTED, TARGET
from common import type as ty
from common.rig import ThreePanelRig


T_MAX = 6.5
CONSTANT = np.full(7, 0.9)
TWO_POINT = np.array([-1.0, 1.0])
SPREAD = np.array([-1.4, -0.7, -0.2, 0.3, 0.9, 1.5])
SHIFT = 0.8


class B06(ActScene):
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
            text="Take a batch in which every value is the same number."
        ) as tracker:
            self.play(FadeIn(caption), run_time=1.0)
            self.across(tracker, Indicate(plotted, scale_factor=1.08,
                                          color=COLLAPSE), floor=0.8)

        with self.voiceover(
            text="Equal values wrap to equal angles, so the arrows stay "
                 "stacked on top of one another however fast the winding "
                 "goes. With nothing pointing in a different direction "
                 "there is nothing to cancel, and the average keeps its "
                 "full length at every frequency."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=5.0,
                        rate_func=linear)

        result = ty.line(R"$|\varphi(t)| = 1$", "for every", "$t$",
                         size=ty.STATEMENT, color=COLLAPSE)
        result.move_to(np.array([0.0, -3.3, 0.0]))

        with self.voiceover(
            text="A flat line at one is the signature of complete "
                 "collapse."
        ) as tracker:
            self.play(FadeOut(caption), FadeIn(result), run_time=1.0)
            self.across(tracker, Indicate(result, scale_factor=1.06,
                                          color=COLLAPSE), floor=0.8)

        # A flat line is the easiest thing in the chapter to miss, because
        # nothing moved. A moment to notice that nothing moved.
        self.inspect(1.4)

        self.constant_result = result

    # ------------------------------------------------------------------ 2
    def two_point_beat(self):
        r = self.rig

        with self.voiceover(
            text="The simplest non-degenerate case: two values, minus one "
                 "and plus one, equally likely."
        ) as tracker:
            self.play(FadeOut(self.constant_result), run_time=0.5)
            r.show_abs = False
            r.swap(self, TWO_POINT, EMPIRICAL, CLOUD)
            self.across(tracker, Indicate(r.mounted_dots, scale_factor=1.2,
                                          color=CLOUD), floor=0.8)

        # Row 17: the mirror-cancellation argument was re-derived here having
        # been proved in b05. Back-reference instead -- NARRATION_SPEC.md
        # section 21, repetition is deliberate or it is padding.
        with self.voiceover(
            text="The two arrows sit at angles t and minus t, mirror "
                 "images across the real axis. Their vertical components "
                 "cancel by the same pairing as before, so only the "
                 "horizontal ones survive, and the average traces out the "
                 "cosine."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=5.5,
                        rate_func=linear)

        result = ty.maths(R"\varphi(t) = \cos t", size=ty.EQ_DISPLAY,
                          color=EMPIRICAL)
        result.move_to(np.array([0.0, -3.3, 0.0]))

        # Row 18 -- "Two arrows turning, and their average. The cosine arrived
        # without an integral being evaluated." -- deleted. The first sentence
        # narrates the picture; the second grades the derivation, which is
        # evaluative framing (NARRATION_SPEC.md section 5). What replaces it
        # says where the cosine came from, which is information.
        with self.voiceover(
            text="Every arrow in this batch is at angle plus or minus t, "
                 "so the average is the cosine of t, exactly, at every "
                 "frequency."
        ) as tracker:
            self.play(Write(result), run_time=1.3)
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

        mag_lab = ty.maths(R"|\varphi(t)|", size=ty.TICK, color=TARGET)
        mag_lab.move_to(r.axes.c2p(5.2, 0.72))

        # The two blocks that used to open this beat are one. The first ended
        # in `across(Indicate(mounted_dots))` -- six dots pulsing 12% against a
        # rig parked at t = 0 -- which measured nine seconds of still frame at
        # 00:47-00:56 on the rev-3 master. The batch now arrives dot by dot and
        # the sweep starts inside the same sentence, so the amber curve is
        # being drawn while it is being described.
        with self.voiceover(
            text="Keep the same rig and change the question. Take a batch with "
                 "some spread to it, and alongside the usual curve draw the "
                 "length of the average arrow in amber. "
                 "<bookmark mark='sweep'/>As the frequency climbs that length "
                 "nearly vanishes, then rises again. Keep its shape in mind."
        ) as tracker:
            self.play(FadeOut(self.two_point_result), run_time=0.4)
            r.swap(self, SPREAD, EMPIRICAL, CLOUD)
            self.mag_curve = always_redraw(r.trace_abs)
            # swap() adds the new panel-1 dots immediately; take them back off
            # so lagged_map has something to bring in, or the "arrival" is
            # a fade-in of things already fully drawn.
            self.remove(r.mounted_dots)
            self.play(lagged_map(FadeIn, r.mounted_dots, lag_ratio=0.12),
                      run_time=1.0)
            self.add(self.mag_curve)
            self.play(FadeIn(mag_lab), run_time=0.5)
            self.wait_until_bookmark("sweep")
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=3.2,
                        rate_func=linear)

        ghost = r.trace_abs().copy().set_stroke(TARGET, 11, opacity=0.32)
        self.add(ghost)

        with self.voiceover(
            text="Now slide every value by the same amount and run exactly the "
                 "same sweep."
        ) as tracker:
            shifted = r.line_dots(radius=r._dot_radius, colour=CLOUD)
            shifted.shift(r.line.number_to_point(SHIFT)
                          - r.line.number_to_point(0.0))
            self.play(Transform(r.mounted_dots, shifted), run_time=1.2)
            r.swap(self, SPREAD + SHIFT, EMPIRICAL, CLOUD)
            # "and run exactly the same sweep" -- so the sweep starts here
            # rather than after a pause with the dots pulsing at t = 0. The
            # next block carries it on from wherever this one leaves it.
            self.across(tracker, r.t.animate.set_value(1.2), floor=0.8,
                        rate_func=smooth)

        with self.voiceover(
            text="The blue curve changes, but amber lands back on its ghost. "
                 "A common shift rotates every arrow together, and rotation "
                 "cannot change the average length."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=4.5,
                        rate_func=linear)

        identity = ty.maths(R"\varphi_{X+\mu}(t) = e^{i\mu t}\,\varphi_X(t)",
                            size=ty.EQ_DISPLAY, color=TARGET)
        reading = ty.words("the shift moved the phase, and only the phase",
                           size=ty.LABEL, color=MUTED)
        block = VGroup(identity, reading).arrange(DOWN, buff=0.22)
        block.move_to(np.array([0.0, -3.15, 0.0]))
        layout.fit_in_frame(block)
        with self.voiceover(
            text="The shift contributes only a unit-length factor. Its effect "
                 "lives in the phase; magnitude is blind to it."
        ) as tracker:
            self.play(Write(identity), FadeIn(reading), run_time=1.3)
            self.across(tracker, r.t.animate.set_value(2.2),
                        Indicate(identity, scale_factor=1.05, color=TARGET),
                        floor=1.0, rate_func=smooth)

        self.clear_beat()
