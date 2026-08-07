"""Chapter B, opening — why summary statistics are not enough.

Rebuilt. The previous version opened on a collapsed batch against a spread one
and asked for a score separating them, which is a problem variance already
solves; the chapter's real question only arrived forty seconds in. This version
states the goal once, at the start, and does not weaken it later:

    compare whole distributions, from samples, differentiably

    1. two batches agreeing on count, mean and variance, and plainly different
    2. what neither summary reaches: the arrangement inside the spread
    3. those two batches become the input of a pipeline with a hole in it,
       and the two constraints are written under the arrows they constrain

Both batches are standardised, so the agreement is exact rather than
illustrative -- facts.py checks they match to 5e-3.

These two batches are the chapter's running experiment. They are named here,
returned to on the rig in b02, and the curves that finally separate them are
drawn in b07 -- so this scene is a question the chapter actually answers rather
than a motivating anecdote that is dropped.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b00_the_problem.py B00 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import data, layout
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, MUTED, TARGET
from common import type as ty

LINE_X = -2.55          # number lines sit left of centre; stats sit right
LINE_W = 7.4
STAT_X = 4.35
TOP_Y = 1.25          # stacks upward from here
BOT_Y = -1.25         # stacks downward, so the two batches face away
STAT_DY = 0.55        # stat blocks sit a little outboard of their line


DOT_R = 0.055
# Stack on a bin a little wider than a dot, not on the dot diameter itself.
# At the true diameter, forty samples over six units stack only three deep and
# the bell still reads as a smear. 0.25 gives 24 columns, which puts the peak
# around seven dots high -- tall enough that the hump and the two clumps are
# distinguishable at 480p, which is the entire claim this scene makes.
BIN_DX = 0.25


def batch_on_a_line(h, colour, y, up=True):
    """A number line at height `y` with the batch stacked above (or below) it.

    Stacked, not laid flat on the axis: forty samples from a bell curve overlap
    into a solid bar otherwise, and this scene's whole claim is that the two
    shapes are visibly different. Flat dots make that claim unverifiable from
    the frame.
    """
    nl = NumberLine(x_range=(-3, 3, 1), length=LINE_W, include_numbers=True,
                    include_tip=False)
    nl.move_to(np.array([LINE_X, y, 0.0]))
    nl.set_stroke(MUTED, 2)
    nl.numbers.set_color(MUTED)

    # Quantise once, and use the same snapped values for both jobs.
    #
    # stack_levels() is greedy first-fit over sorted values, so a run of nearby
    # samples climbs one level at a time. Drawn at their true x that run renders
    # as a diagonal streak rather than a column, and the frame stops looking
    # like a distribution at all. Snapping only the drawn x fixes the streaks
    # but leaves columns floating clear of the axis, because the levels were
    # still packed against true spacing -- measured on this batch, three of the
    # nine columns, one of them occupying levels 0,1,4,5,6,10,11. Binning first
    # makes every column pack from the axis outward, which is what a dot
    # histogram is.
    snapped = [round(v / BIN_DX) * BIN_DX for v in h]
    levels = layout.stack_levels(snapped, BIN_DX)

    step = (2 * DOT_R + 0.020) * (1 if up else -1)
    dots = VGroup(*(
        Dot(nl.number_to_point(s) + np.array([0.0, (lvl + 0.9) * step, 0.0]),
            radius=DOT_R).set_fill(colour, 0.9)
        for s, lvl in zip(snapped, levels)))
    return nl, dots


class B00(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.two_batches()
        self.what_the_summaries_miss()
        self.what_we_need()

    # ------------------------------------------------------------------ 1
    def two_batches(self):
        self.h_bell = data.gaussian_1d(40)
        self.h_clumps = data.bimodal_1d(40)

        nl1, d1 = batch_on_a_line(self.h_bell, CLOUD, TOP_Y, up=True)
        nl2, d2 = batch_on_a_line(self.h_clumps, COLLAPSE, BOT_Y, up=False)

        lab1 = ty.label("one bell-shaped hump", color=CLOUD)
        lab1.next_to(d1, UP, buff=0.26)
        lab2 = ty.label("two separated clumps", color=COLLAPSE)
        lab2.next_to(d2, DOWN, buff=0.26)

        with self.voiceover(
            text="Forty numbers drawn from a bell curve, laid out on a "
                 "number line. <bookmark mark='second'/>And forty more that "
                 "fall into two separate clumps."
        ):
            self.play(Create(nl1),
                      lagged_map(FadeIn, d1, lag_ratio=0.02),
                      run_time=1.3)
            self.play(FadeIn(lab1, shift=0.12 * DOWN), run_time=0.5)
            self.wait_until_bookmark("second")
            self.play(Create(nl2),
                      lagged_map(FadeIn, d2, lag_ratio=0.02),
                      run_time=1.3)
            self.play(FadeIn(lab2, shift=0.12 * UP), run_time=0.5)

        # The three agreeing summaries, revealed a row at a time and pulsed in
        # pairs. The pairing is the whole point of the beat, so it gets the
        # motion: two numbers lighting up together reads as "these are equal"
        # without a caption saying so.
        rows = [
            ("samples", "$= 40$", "$= 40$"),
            ("mean", "$= %+.2f$" % self._z(self.h_bell.mean()),
                     "$= %+.2f$" % self._z(self.h_clumps.mean())),
            ("variance", "$= %.2f$" % self.h_bell.var(),
                         "$= %.2f$" % self.h_clumps.var()),
        ]
        top_blk, bot_blk = VGroup(), VGroup()
        for name, v1, v2 in rows:
            top_blk.add(ty.line(name, v1, size=ty.LABEL, color=CLOUD))
            bot_blk.add(ty.line(name, v2, size=ty.LABEL, color=COLLAPSE))
        for blk, y in ((top_blk, TOP_Y + STAT_DY), (bot_blk, BOT_Y - STAT_DY)):
            blk.arrange(DOWN, buff=0.20, aligned_edge=LEFT)
            blk.move_to(np.array([STAT_X, y, 0.0]))
            layout.fit_in_frame(blk)

        # One bookmark per summary, so each pair arrives on the word that names
        # it. Revealing all three at one bookmark left seven measured seconds of
        # still frame while the voice listed them (tools/still_frames.py).
        with self.voiceover(
            text="Now for the awkward part. We chose these two toy batches so "
                 "the familiar checks agree: <bookmark mark='count'/>same "
                 "count, <bookmark mark='mean'/>same mean, "
                 "<bookmark mark='var'/>same variance. "
                 "<bookmark mark='yet'/>Yet one picture is one hump and the "
                 "other is plainly two clumps."
        ):
            for mark, row in (("count", 0), ("mean", 1), ("var", 2)):
                self.wait_until_bookmark(mark)
                self.play(FadeIn(top_blk[row], shift=0.12 * LEFT),
                          FadeIn(bot_blk[row], shift=0.12 * LEFT),
                          run_time=0.7)
            self.wait_until_bookmark("yet")
            self.play(Indicate(d1, scale_factor=1.06, color=CLOUD),
                      Indicate(d2, scale_factor=1.06, color=COLLAPSE),
                      run_time=1.2)

        # Silence, with both batches and all six numbers on screen. The viewer
        # is being asked to hold two things at once -- the numbers match, the
        # pictures do not -- and that comparison needs a moment with nothing
        # spoken over it.
        self.inspect(1.0)

        self.stats = VGroup(top_blk, bot_blk)
        self.lines = VGroup(nl1, d1, lab1, nl2, d2, lab2)
        # The plots without their captions, and each batch separately. Beat 3
        # shrinks them into the left end of a pipeline, one at a time; prose
        # scaled to half its size is unreadable furniture, so the captions are
        # dropped there, but the dot histograms are not -- their SHAPE is the
        # thing going in.
        self.plot_top = VGroup(nl1, d1)
        self.plot_bot = VGroup(nl2, d2)
        self.batch_labels = VGroup(lab1, lab2)
        self.clump_dots = d2

    # ------------------------------------------------------------------ 2
    def what_the_summaries_miss(self):
        """Name what the two summaries cannot reach, against the picture.

        The previous cut replaced this with a sentence over an amber question
        card held motionless for twelve seconds -- a third of the scene, and
        the caption said what the voice was saying at that instant. The gap
        between the clumps is the thing the sentence is about, so the sentence
        is spoken over the gap instead, and it is derived from the drawn batch
        rather than from a constant so it cannot drift off the stack.
        """
        lo, hi = layout.widest_gap(list(self.h_clumps))
        nl2, d2 = self.lines[3], self.lines[4]
        x_lo = nl2.number_to_point(round(lo / BIN_DX) * BIN_DX)[0]
        x_hi = nl2.number_to_point(round(hi / BIN_DX) * BIN_DX)[0]
        gap = Rectangle(width=x_hi - x_lo,
                        height=d2.height + 2 * DOT_R + 0.18)
        gap.set_stroke(TARGET, 2).set_fill(TARGET, 0.09)
        gap.move_to(np.array([(x_lo + x_hi) / 2, d2.get_center()[1], 0.0]))
        # The same span, marked on the bell batch, where nothing is missing.
        same = gap.copy().set_stroke(TARGET, 2, opacity=0.35).set_fill(
            TARGET, 0.0)
        same.move_to(np.array([(x_lo + x_hi) / 2,
                               self.lines[1].get_center()[1], 0.0]))
        same.stretch_to_fit_height(
            self.lines[1].height + 2 * DOT_R + 0.18)

        top_blk, bot_blk = self.stats
        with self.voiceover(
            text="A mean fixes where a batch sits, "
                 "<bookmark mark='var'/>and a variance fixes how far it "
                 "spreads, and both batches were built to agree on those. "
                 "<bookmark mark='gap'/>Neither of them reaches the "
                 "arrangement inside that spread, which is where all of the "
                 "difference is: an empty stretch in one batch, and the "
                 "fullest part of the other."
        ) as tracker:
            # Each summary lights up as it is named. Without this the sentence
            # ran for seven seconds over a still frame -- measured at
            # 00:18-00:26 on the first pass of this rebuild.
            self.play(Indicate(top_blk[1], scale_factor=1.18, color=CLOUD),
                      Indicate(bot_blk[1], scale_factor=1.18, color=COLLAPSE),
                      run_time=0.9)
            self.wait_until_bookmark("var")
            self.play(Indicate(top_blk[2], scale_factor=1.18, color=CLOUD),
                      Indicate(bot_blk[2], scale_factor=1.18, color=COLLAPSE),
                      run_time=0.9)
            self.wait_until_bookmark("gap")
            self.play(FadeIn(gap), run_time=0.7)
            self.play(TransformFromCopy(gap, same), run_time=1.1)
            # "the fullest part of the other" -- so the samples inside the
            # marked span on the bell batch light up one by one. An opacity
            # change from 0.09 to 0.22 spread over six seconds was the previous
            # filler here, and it measured as a still frame: a fill fade that
            # slow is below the threshold at which anything looks like motion.
            inside = VGroup(*(
                dot for dot, v in zip(self.lines[1], self.h_bell)
                if x_lo <= self.lines[0].number_to_point(
                    round(v / BIN_DX) * BIN_DX)[0] <= x_hi))
            self.across(tracker,
                        lagged_map(Indicate, inside, scale_factor=2.0,
                                       color=TARGET, lag_ratio=0.06),
                        floor=1.0)

        self.gap = VGroup(gap, same)

    # ------------------------------------------------------------------ 3
    def what_we_need(self):
        """The two batches become the left end of a pipeline with a hole in it.

        The unknown says something the voice does not: it names the two ends
        that are already fixed and marks the middle as the thing the rest of
        the video builds. Each constraint is written under the arrow it
        constrains rather than in a numbered list, so it annotates a step
        instead of floating (RENDER_REVIEW_SPEC.md section 7.3).
        """
        pipe = VGroup(
            ty.maths(R"\longrightarrow", size=ty.EQ),
            ty.maths("?", size=ty.EQ_DISPLAY, color=TARGET),
            ty.maths(R"\longrightarrow", size=ty.EQ),
            ty.words("one score", size=ty.BODY, color=TARGET),
        ).arrange(RIGHT, buff=0.40)
        pipe.move_to(np.array([2.15, 0.70, 0.0]))
        layout.fit_in_frame(pipe)

        # Where the shrunken batches land: stacked immediately left of the first
        # arrow, so they ARE the pipeline's input rather than a picture beside
        # it. One at a time, because both of them go in.
        top_nest = np.array([-4.55, 1.45, 0.0])
        bot_nest = np.array([-4.55, 0.05, 0.0])

        with self.voiceover(
            text="So those two batches are the test case: whatever we build "
                 "has to take a batch like these and return one number. "
                 "<bookmark mark='hole'/>The middle of that pipeline is the "
                 "part nobody has handed us yet."
        ) as tracker:
            self.play(FadeOut(self.stats), FadeOut(self.gap),
                      FadeOut(self.batch_labels), run_time=0.5)
            self.play(self.plot_top.animate.scale(0.48).move_to(top_nest),
                      run_time=1.3)
            self.play(self.plot_bot.animate.scale(0.48).move_to(bot_nest),
                      run_time=1.3)
            self.wait_until_bookmark("hole")
            self.play(FadeIn(pipe[0], shift=0.2 * RIGHT),
                      FadeIn(pipe[2], shift=0.2 * RIGHT),
                      FadeIn(pipe[3], shift=0.2 * RIGHT), run_time=0.9)
            self.across(tracker, Write(pipe[1]), floor=0.7)

        # Each constraint under the arrow it constrains, arriving as that arrow
        # is named. Two short lines rather than two sentences: the voice
        # carries the reasoning, the screen carries which step it lands on.
        # What the screen carries here is the FORM of each constraint, not a
        # paraphrase of the sentence being spoken over it: what actually
        # arrives, and what has to exist. Prose versions of these two lines were
        # a straight second copy of the narration (RENDER_REVIEW_SPEC.md section
        # 7.2) -- and, being two lines of prose hung under two arrows 1.7 units
        # apart, they also overlapped into an unreadable smear on the first
        # render of this rebuild.
        #
        # Different heights, each on a dashed lead down from the arrow it
        # constrains, so the attachment is drawn rather than inferred (5.4).
        c_in = ty.line("only", R"$x_1, \ldots, x_N$", size=ty.LABEL,
                       color=MUTED)
        c_in.move_to(np.array([pipe[0].get_center()[0], -0.85, 0.0]))
        c_out = ty.line(R"$\partial\,\mathrm{score}/\partial x_i$", "exists",
                        size=ty.LABEL, color=MUTED)
        c_out.move_to(np.array([pipe[2].get_center()[0] + 0.7, -2.15, 0.0]))
        for c in (c_in, c_out):
            layout.fit_in_frame(c)

        def lead(arrow, caption):
            return DashedLine(
                arrow.get_bottom() + 0.12 * DOWN,
                np.array([arrow.get_center()[0], caption.get_top()[1] + 0.12,
                          0.0]),
                dash_length=0.06).set_stroke(MUTED, 1.2, opacity=0.55)

        lead_in, lead_out = lead(pipe[0], c_in), lead(pipe[2], c_out)

        with self.voiceover(
            text="Two things pin down what can go in the hole. "
                 "<bookmark mark='in'/>A batch of samples is all that ever "
                 "arrives, so there may be no density formula on either side "
                 "to compare against. <bookmark mark='out'/>And the score "
                 "becomes a training loss, so nudging any single sample has "
                 "to change it by an amount gradient descent can follow."
        ) as tracker:
            self.wait_until_bookmark("in")
            self.play(Create(lead_in), FadeIn(c_in, shift=0.2 * UP),
                      Indicate(pipe[0], scale_factor=1.35, color=TARGET),
                      run_time=1.2)
            self.wait_until_bookmark("out")
            self.play(Create(lead_out), FadeIn(c_out, shift=0.2 * UP),
                      Indicate(pipe[2], scale_factor=1.35, color=TARGET),
                      run_time=1.2)
            # "nudging ANY single sample" -- so several of them get nudged, one
            # after another, each visibly. Three separate gestures, not one
            # slow one: a single dot drifting a third of a unit over eight
            # seconds is two pixels per frame at 0.48 scale, which measures and
            # reads as a still frame. Each also brightens, because a three-pixel
            # dot cannot carry a motion cue on position alone.
            order = np.argsort(self.h_clumps)
            picks = [self.clump_dots[int(order[k])]
                     for k in (len(order) - 1, len(order) // 2, 0)]
            span = max(1.2, tracker.get_remaining_duration())
            for dot in picks:
                self.play(dot.animate.shift(0.30 * RIGHT).scale(2.4)
                          .set_fill(TARGET, 1),
                          run_time=span / len(picks),
                          rate_func=there_and_back)

        # Resolve the hole rather than drawing a second pipeline underneath the
        # first, and let the closing sentence hand the next scene its job: the
        # batch is about to be asked a question, one sample at a time.
        #
        # The whole row re-lays-out in the SAME play as the substitution. Doing
        # the transform first and the re-arrange second left a long phrase
        # sitting on top of "one score" for 1.2 s, which rendered as two
        # overlapping strings.
        answer = ty.words("one question, asked of every sample",
                          size=ty.LABEL, color=TARGET)
        final = VGroup(pipe[0].copy(), answer, pipe[2].copy(),
                       pipe[3].copy()).arrange(RIGHT, buff=0.34)
        final.move_to(np.array([2.0, 0.70, 0.0]))
        layout.fit_in_frame(final)

        with self.voiceover(
            text="Nothing on the usual list of summaries survives both. "
                 "<bookmark mark='fill'/>What does is a single question put to "
                 "every sample at once, whose answers can either reinforce "
                 "each other or cancel."
        ) as tracker:
            self.wait_until_bookmark("fill")
            self.play(FadeOut(VGroup(lead_in, lead_out), shift=0.2 * DOWN),
                      FadeOut(c_in, shift=0.2 * DOWN),
                      FadeOut(c_out, shift=0.2 * DOWN),
                      ReplacementTransform(pipe[1], final[1]),
                      Transform(pipe[0], final[0]),
                      Transform(pipe[2], final[2]),
                      Transform(pipe[3], final[3]), run_time=1.3)
            # Every sample is asked, so every sample lights up in turn. This is
            # the visible form of "asked of every sample at once", and it hands
            # the next scene a batch that has just been questioned.
            self.across(tracker,
                        lagged_map(Indicate, self.clump_dots,
                                       scale_factor=2.4, color=TARGET,
                                       lag_ratio=0.035),
                        floor=1.2)

        self.clear_beat()

    # ------------------------------------------------------------------
    @staticmethod
    def _z(value):
        """Snap a near-zero mean to zero.

        -0.0005 prints as "-0.00", which reads as a difference between the two
        batches when there is none -- and this beat's whole claim is that there
        is none.
        """
        return 0.0 if abs(value) < 5e-3 else value
