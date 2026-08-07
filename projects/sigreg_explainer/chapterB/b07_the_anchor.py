"""Chapter B.7 — the shared anchor, and the answer to the opening question.

Two things, in the order that makes the second one readable:

    1. phi(0) = 1, for every distribution there has ever been. At t = 0 the
       wrapping speed is zero, so t*x is zero whatever x was, so every arrow is
       the unit arrow pointing right. The batch never enters the argument --
       which is exactly why the result holds for every batch.

    2. **The toy experiment, finished.** The two batches from b00 -- the same
       forty numbers, the same mean, the same variance, and plainly different
       shapes -- go through the rig one after the other, and their curves are
       nothing alike. One decays and stays near zero; the other swings down to
       -0.65. Both leave from the height that 1 just established, so the
       comparison needs no rescaling.

Part 1 used to end without ever running the opening experiment through the
machine it had spent eight minutes building. b00 asked how two batches with
identical summaries could have different shapes; the old close here answered a
different, smaller question, with three batches nobody had met. The question the
chapter opens with is now the question its last scene answers, and phi(0) = 1 is
what licenses reading the two curves off one pair of axes.

What is deliberately NOT claimed: that different curves prove different
distributions. That is the uniqueness theorem, and it is b09's to state.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b07_the_anchor.py B07 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, TARGET
from common import type as ty
from common.rig import ThreePanelRig
from common.wrap import ecf


T_MAX = 6.5

# Literally b00's two batches. Not a fresh draw, not a smaller one: the whole
# point of this scene is that these are the numbers the viewer was shown eight
# minutes ago, so common/data.py's fixed seeds have to be the only source.
BELL = data.gaussian_1d(40)
CLUMPS = data.bimodal_1d(40)


class B07(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.rig = ThreePanelRig(BELL, t_max=T_MAX, line_range=(-3, 3, 1))
        # Stacked, because these are real forty-sample batches and the scene's
        # closing claim is about their SHAPES. Flat on the axis they are one
        # smear and panel 1 stops being evidence for anything.
        self.rig.mount(self, dot_radius=0.055, stack_dots=True)
        self.why_beat()
        self.toy_answer_beat()

    # ------------------------------------------------------------------ 1
    def why_beat(self):
        """t = 0: every arrow is the same arrow. The batch never appears."""
        r = self.rig
        # Start with the arrows spread, so "set the frequency to zero" is a
        # thing that happens on screen. The previous cut set t to zero before
        # the beat began and then talked over the resulting still frame for
        # twenty seconds -- the collapse onto one arrow IS the argument, and it
        # was the one part not shown.
        r.t.set_value(1.6)

        steps = VGroup(
            ty.maths(R"t = 0", size=ty.EQ),
            ty.line(R"$t\,x = 0$", "for every", "$x$", size=ty.EQ),
            ty.maths(R"e^{i \cdot 0} = 1", size=ty.EQ),
        ).arrange(DOWN, buff=0.26)
        steps.move_to(np.array([0.0, -3.05, 0.0]))
        layout.fit_in_frame(steps)
        steps[2].set_color(TARGET)

        with self.voiceover(
            text="Wind the frequency all the way back to zero. The product t x "
                 "is zero whatever x was, "
                 "<bookmark mark='same'/>so every value in the batch produces "
                 "the same angle, every arrow is the unit arrow pointing "
                 "right, and they stack on top of one another."
        ) as tracker:
            self.play(FadeIn(steps[0]), r.t.animate.set_value(0.0),
                      run_time=1.6)
            self.wait_until_bookmark("same")
            self.play(FadeIn(steps[1]), run_time=0.8)
            self.play(FadeIn(steps[2]), run_time=0.8)
            # Nudge off zero and back, so the stack visibly holds together only
            # at t = 0 rather than merely happening to be drawn that way.
            self.across(tracker, r.t.animate.set_value(0.45), floor=0.9,
                        rate_func=there_and_back)

        result = ty.maths(R"\varphi(0) = 1", size=ty.EQ_HERO, color=TARGET)
        result.move_to(np.array([0.0, -3.05, 0.0]))

        with self.voiceover(
            text="Averaging identical arrows returns the same arrow, so "
                 "phi of zero is one. "
                 "<bookmark mark='note'/>The data never entered that "
                 "argument, which is what makes the result hold for every "
                 "distribution rather than for this batch."
        ) as tracker:
            self.play(FadeOut(steps), run_time=0.4)
            self.play(Write(result), run_time=1.2)
            self.wait_until_bookmark("note")
            # The claim is about EVERY batch, so the batch changes while it is
            # made and the average arrow does not move: panel 1 reshuffles, the
            # curve's left-hand end stays pinned at 1.
            self.across(tracker, r.t.animate.set_value(0.3), floor=0.9,
                        rate_func=there_and_back)

        self.result = result

    # ------------------------------------------------------------------ 2
    def toy_answer_beat(self):
        """The two batches from b00, through the rig, side by side."""
        r = self.rig
        anchor = Dot(r.axes.c2p(0, 1), radius=0.09).set_fill(TARGET, 1)
        anchor_ring = Circle(radius=0.19).move_to(r.axes.c2p(0, 1))
        anchor_ring.set_stroke(TARGET, 2, opacity=0.7)

        label = ty.words("one bell-shaped hump", size=ty.TICK, color=CLOUD)
        label.move_to(np.array([-4.65, -2.55, 0.0]))
        layout.fit_in_frame(label)

        with self.voiceover(
            text="Which is what lets the two batches we opened with be read off "
                 "one pair of axes. The bell-shaped one first: all forty of "
                 "its numbers, wrapped and averaged at every frequency."
        ) as tracker:
            self.play(FadeOut(self.result), run_time=0.4)
            self.play(FadeIn(anchor), Create(anchor_ring),
                      FadeIn(label), run_time=0.9)
            r.t.set_value(0.0)
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=3.4,
                        rate_func=linear)

        bell_curve = r.trace().copy().set_stroke(CLOUD, 4, opacity=0.9)
        self.add(bell_curve)
        bell_lab = ty.maths(R"\varphi_{\mathrm{hump}}", size=ty.TICK,
                            color=CLOUD)
        bell_lab.move_to(r.axes.c2p(5.0, 0.55))

        clump_label = ty.words("two separated clumps", size=ty.TICK,
                               color=COLLAPSE)
        clump_label.move_to(label.get_center())
        layout.fit_in_frame(clump_label)

        with self.voiceover(
            text="Now the two clumps. Same forty numbers in the sense that "
                 "matters: same count, same mean, same variance, "
                 "<bookmark mark='swap'/>and every summary we started with "
                 "still cannot tell these two apart."
        ) as tracker:
            self.play(FadeIn(bell_lab), run_time=0.5)
            self.wait_until_bookmark("swap")
            r.swap(self, CLUMPS, COLLAPSE, COLLAPSE)
            self.play(FadeOut(label), FadeIn(clump_label), run_time=0.6)
            self.across(tracker, Indicate(r.mounted_dots, scale_factor=1.12,
                                          color=COLLAPSE), floor=0.7)

        clump_lab = ty.maths(R"\varphi_{\mathrm{clumps}}", size=ty.TICK,
                             color=COLLAPSE)
        clump_lab.move_to(r.axes.c2p(4.9, -0.72))

        # The gap between the two curves, measured off the same tables they are
        # drawn from rather than eyeballed, and LIVE: it opens and closes as t
        # moves. The first cut of this scene drew it once, at the end, and then
        # held the finished tableau for twenty-five seconds while three
        # sentences played over it -- the payoff frame, frozen, which is the
        # defect this whole revision is about. A gap that grows while the voice
        # says the curves are pulling apart is the same claim, animated.
        bell_re = ecf(BELL, r.grid).real
        gap_t = float(r.grid[np.argmax(np.abs(bell_re - r.table))])

        def gap_bar():
            t = r.t.get_value()
            hi = float(np.interp(t, r.grid, bell_re))
            lo = float(np.interp(t, r.grid, r.table))
            a, b = r.axes.c2p(t, hi), r.axes.c2p(t, lo)
            cap = 0.10
            return VGroup(
                Line(a, b),
                Line(a + cap * LEFT, a + cap * RIGHT),
                Line(b + cap * LEFT, b + cap * RIGHT),
            ).set_stroke(TARGET, 3)

        live_gap = always_redraw(gap_bar)

        with self.voiceover(
            text="Run the same sweep. The arrows start in step, exactly as "
                 "they did before, and then the two clumps pull apart into two "
                 "groups turning at different rates. Watch the distance "
                 "between the two curves as they go."
        ) as tracker:
            self.add(live_gap)
            self.play(FadeIn(clump_lab), run_time=0.5)
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=6.0,
                        rate_func=linear)

        with self.voiceover(
            text="They are nothing alike. <bookmark mark='gap'/>Both leave "
                 "from one, because every characteristic function does, but "
                 "the hump decays and stays down while the clumps swing the "
                 "average all the way over to the negative side -- those "
                 "arrows are genuinely pointing backwards. At its widest, that "
                 "distance is what the mean and the variance could not see."
        ) as tracker:
            # The bookmark is early and the rest of the sentence is spent
            # walking the measurement back across the whole range and then out
            # to the maximum. Putting the bookmark at the end instead left
            # eleven seconds of stopped rig while the contrast was described.
            self.wait_until_bookmark("gap")
            self.across(tracker, r.t.animate.set_value(0.9), floor=2.0,
                        reserve=3.0, rate_func=smooth)
            self.play(r.t.animate.set_value(gap_t), run_time=2.6,
                      rate_func=smooth)

        # Both curves, one anchor, one measured gap, and nothing said over it.
        # This is the frame Part 1 exists to produce.
        self.inspect(1.8)

        with self.voiceover(
            text="One object, built out of nothing but the samples, and it "
                 "separates a pair that three summaries agreed on. What is not "
                 "yet settled is how much of the batch that curve is really "
                 "holding, and how much of it we would have to measure to be "
                 "sure."
        ) as tracker:
            # "how much of it we would have to measure" -- so the measurement
            # moves, out along the axis and back to where it was widest.
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=2.0,
                        rate_func=there_and_back)

        live_gap.clear_updaters(recursive=True)
        self.clear_beat()
