"""Chapter B, opening — why summary statistics are not enough.

Rebuilt. The previous version opened on a collapsed batch against a spread one
and asked for a score separating them, which is a problem variance already
solves; the chapter's real question only arrived forty seconds in. This version
states the goal once, at the start, and does not weaken it later:

    compare whole distributions, from samples, differentiably

    1. two batches agreeing on count, mean and variance, and plainly different
    2. what neither summary reaches: the arrangement inside the spread
    3. full-size batch pairs feed one scalar score while the two implementation
       constraints replace the summary table

Both batches are standardised, so the agreement is exact rather than
illustrative -- facts.py checks they match to 5e-3.

These two batches are the chapter's running experiment. They are named here,
returned to on the rig in b03, and the curves that finally separate them are
drawn in b09 -- so this scene is a question the chapter actually answers rather
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
from common.wrap import ecf

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
SCORE_GRID = np.linspace(0.2, 4.0, 500)


def pair_score(first, second):
    """Concrete scalar examples, using the distance derived later in Chapter B."""
    gaps = np.abs(ecf(first, SCORE_GRID) - ecf(second, SCORE_GRID)) ** 2
    return float(np.trapezoid(gaps, SCORE_GRID))


def batch_dots_on_line(h, colour, number_line, up=True):
    """Stack samples on an existing number line without moving the line."""
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
    return VGroup(*(
        Dot(number_line.number_to_point(s)
            + np.array([0.0, (lvl + 0.9) * step, 0.0]),
            radius=DOT_R).set_fill(colour, 0.9)
        for s, lvl in zip(snapped, levels)))


def batch_on_a_line(h, colour, y, up=True):
    """A number line at height `y` with a readable stacked sample batch."""
    nl = NumberLine(x_range=(-3, 3, 1), length=LINE_W, include_numbers=True,
                    include_tip=False)
    nl.move_to(np.array([LINE_X, y, 0.0]))
    nl.set_stroke(MUTED, 2)
    nl.numbers.set_color(MUTED)
    dots = batch_dots_on_line(h, colour, nl, up=up)
    return nl, dots


class B00(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.two_batches()
        self.what_we_need()

    # ------------------------------------------------------------------ 1
    def two_batches(self):
        self.h_bell = data.gaussian_1d(40)
        self.h_clumps = data.bimodal_1d(40)

        # Both batches stack upward off their own line. A downward stack for
        # the second batch used to read as "facing away" in intent but as an
        # upside-down distribution on watch -- colour (CLOUD vs COLLAPSE) and
        # shape (hump vs two clumps) already distinguish the two without
        # needing orientation to carry a third signal.
        nl1, d1 = batch_on_a_line(self.h_bell, CLOUD, TOP_Y, up=True)
        nl2, d2 = batch_on_a_line(self.h_clumps, COLLAPSE, BOT_Y, up=True)

        lab1 = ty.label("one bell-shaped hump", color=CLOUD)
        lab1.next_to(d1, UP, buff=0.26)
        lab2 = ty.label("two separated clumps", color=COLLAPSE)
        lab2.next_to(d2, UP, buff=0.26)

        with self.voiceover(
            text="Imagine taking forty numbers drawn from a bell curve "
                 "and laying them out on a number line. <bookmark mark='second'/>"
                 "Then draw forty more numbers that fall into two separate clumps."
        ) as tracker:
            self.play(Create(nl1),
                      lagged_map(FadeIn, d1, lag_ratio=0.02),
                      FadeIn(lab1, shift=0.12 * DOWN),
                      run_time=1.05, rate_func=smooth)
            self.wait_until_bookmark("second")
            self.play(Create(nl2),
                      lagged_map(FadeIn, d2, lag_ratio=0.02),
                      FadeIn(lab2, shift=0.12 * UP),
                      run_time=1.05, rate_func=smooth)
            self.play(Indicate(VGroup(d1, d2), scale_factor=1.025,
                               color=TARGET), run_time=0.55)

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
            text="These two batches look completely different, yet their "
                 "<bookmark mark='count'/>sample counts, <bookmark mark='mean'/>"
                 "means, and <bookmark mark='var'/>variances agree."
        ) as tracker:
            self.play(Indicate(d1, scale_factor=1.04, color=CLOUD),
                      Indicate(d2, scale_factor=1.04, color=COLLAPSE),
                      run_time=0.55)
            for mark, row in (("count", 0), ("mean", 1), ("var", 2)):
                self.wait_until_bookmark(mark)
                self.play(FadeIn(top_blk[row], shift=0.12 * LEFT),
                          FadeIn(bot_blk[row], shift=0.12 * LEFT),
                          run_time=0.28)
            self.play(Indicate(VGroup(top_blk, bot_blk),
                               scale_factor=1.03, color=TARGET),
                      run_time=0.55)

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
    def what_we_need(self):
        """Keep the distributions large and make the scalar goal explicit."""
        # Open a quiet channel between the two number lines and centre the
        # experiment while its examples run. It only moves left when the
        # requirement panel needs the right side of the frame.
        centre_shift = -LINE_X * RIGHT
        top_shift = centre_shift + 0.35 * UP
        bot_shift = centre_shift + 1.10 * DOWN

        score_label = ty.words("one score", size=ty.BODY, color=TARGET)
        score_box = RoundedRectangle(
            width=1.85, height=0.90, corner_radius=0.14,
        ).set_fill(TARGET, 0.08).set_stroke(TARGET, 2)
        score_card = VGroup(score_box, score_label)
        score_card.move_to(0.20 * DOWN)

        # Equal-length, exactly vertical arrows floating in the gap. Anchoring
        # them to NumberLine.number_to_point(0) made sub-pixel layout offsets
        # read as a crooked pair, and the dots obscured their tails.
        arrow_length = 0.72
        arrow_clearance = 0.13
        top_end = score_box.get_top() + arrow_clearance * UP
        bot_end = score_box.get_bottom() + arrow_clearance * DOWN
        top_arrow = Arrow(
            top_end + arrow_length * UP, top_end,
            buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.16,
        ).set_color(CLOUD)
        bot_arrow = Arrow(
            bot_end + arrow_length * DOWN, bot_end,
            buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.16,
        ).set_color(COLLAPSE)

        with self.voiceover(
            text="So the question becomes: can we compress this difference "
                 "in shape into one smooth number?"
        ) as tracker:
            self.play(FadeOut(self.stats),
                      FadeOut(self.batch_labels),
                      self.plot_top[0].animate.shift(top_shift),
                      self.plot_top[1].animate.shift(top_shift),
                      self.plot_bot[0].animate.shift(bot_shift),
                      self.plot_bot[1].animate.shift(bot_shift),
                      run_time=0.85,
                      rate_func=smooth)
            self.play(GrowArrow(top_arrow), GrowArrow(bot_arrow),
                      FadeIn(score_box), FadeIn(score_label),
                      run_time=0.65)
            self.play(Indicate(score_card, scale_factor=1.04,
                               color=TARGET), run_time=0.55)

        self.inspect(1.2)

        score_prefix = ty.maths(R"s =", size=ty.EQ, color=TARGET)
        score_value = DecimalNumber(
            pair_score(self.h_bell, self.h_clumps),
            num_decimal_places=2, font_size=ty.EQ,
        ).set_color(TARGET)
        score_readout = VGroup(score_prefix, score_value).arrange(RIGHT, buff=0.10)
        score_readout.move_to(score_card)

        bell_again = data.gaussian_1d(40, seed=119)
        bell_pair = data.gaussian_1d(40, seed=812)
        collapsed = data.collapsed_1d(40)
        spread = np.linspace(-2.6, 2.6, 40)

        def dots_target(samples, colour, plot):
            return batch_dots_on_line(samples, colour, plot[0])

        with self.voiceover(
            text="Suppose this first pair gives us this number. Now feed the "
                 "same rule two bell-shaped batches, and the value falls."
        ) as tracker:
            self.play(ReplacementTransform(score_label, score_prefix),
                      FadeIn(score_value),
                      FadeOut(top_arrow), FadeOut(bot_arrow), run_time=0.9)
            self.across(
                tracker,
                Transform(self.plot_top[1], dots_target(
                    bell_again, CLOUD, self.plot_top)),
                Transform(self.plot_bot[1], dots_target(
                    bell_pair, COLLAPSE, self.plot_bot)),
                ChangeDecimalToValue(
                    score_value, pair_score(bell_again, bell_pair)),
                floor=1.5, rate_func=smooth,
            )

        self.inspect(1.2)

        with self.voiceover(
            text="Try a nearly collapsed batch against a spread-out one, and "
                 "the same rule responds again."
        ) as tracker:
            self.across(
                tracker,
                Transform(self.plot_top[1], dots_target(
                    collapsed, CLOUD, self.plot_top)),
                Transform(self.plot_bot[1], dots_target(
                    spread, COLLAPSE, self.plot_bot)),
                ChangeDecimalToValue(
                    score_value, pair_score(collapsed, spread)),
                floor=1.5, rate_func=smooth,
            )

        self.inspect(1.2)

        requirements = VGroup(
            ty.words("what must the score do?", size=ty.BODY, color=TARGET),
            ty.line("work from", R"$x_1,\ldots,x_N$", "alone",
                    size=ty.LABEL, color=CLOUD),
            ty.line("respond smoothly to every", "$x_i$",
                    size=ty.LABEL, color=COLLAPSE),
            ty.maths(R"\frac{\partial s}{\partial x_i}\ \text{exists}",
                     size=ty.EQ, color=COLLAPSE),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        requirements.move_to(np.array([4.35, 0.1, 0.0]))
        layout.fit_in_frame(requirements)

        # A short, deterministic stream of fresh inputs. Sorting each batch
        # keeps dot identities locally coherent from one example to the next,
        # so the changes read as rhythmic trials rather than forty crossing
        # trajectories.
        rng = np.random.default_rng(20260808)
        random_pairs = [
            (np.sort(rng.normal(-0.35, 0.55, 40)),
             np.sort(rng.normal(0.45, 0.45, 40))),
            (np.sort(np.r_[rng.normal(-1.15, 0.20, 20),
                           rng.normal(0.95, 0.24, 20)]),
             np.sort(rng.uniform(-2.35, 2.35, 40))),
            (np.sort(np.clip(rng.normal(0.0, 0.75, 40), -2.5, 2.5)),
             np.sort(np.clip(rng.normal(0.15, 1.05, 40), -2.5, 2.5))),
        ]

        return_left = LINE_X * RIGHT
        lower_clearance = 0.45 * DOWN

        with self.voiceover(
            text="Ideally, this score should come directly from the samples "
                 "themselves, without assuming we know a density formula."
        ) as tracker:
            self.play(
                self.plot_top[0].animate.shift(return_left),
                self.plot_top[1].animate.shift(return_left),
                self.plot_bot[0].animate.shift(return_left + lower_clearance),
                self.plot_bot[1].animate.shift(return_left + lower_clearance),
                score_box.animate.shift(return_left),
                score_prefix.animate.shift(return_left),
                score_value.animate.shift(return_left),
                FadeIn(requirements[0], shift=0.10 * DOWN),
                run_time=1.0, rate_func=smooth,
            )
            self.play(FadeIn(requirements[1], shift=0.12 * LEFT),
                      run_time=0.7)

            remaining = max(2.4, tracker.get_remaining_duration())
            step = remaining / len(random_pairs)
            for top_samples, bot_samples in random_pairs:
                transition = min(0.85, 0.78 * step)
                self.play(
                    Transform(self.plot_top[1], dots_target(
                        top_samples, CLOUD, self.plot_top)),
                    Transform(self.plot_bot[1], dots_target(
                        bot_samples, COLLAPSE, self.plot_bot)),
                    ChangeDecimalToValue(
                        score_value, pair_score(top_samples, bot_samples)),
                    run_time=transition, rate_func=smooth,
                )
                self.wait(max(0.0, step - transition))

        with self.voiceover(
            text="And if one sample nudges to the side, how should the number "
                 "respond? Smoothly enough that gradient descent can tell "
                 "which way to move it."
        ) as tracker:
            self.play(FadeIn(requirements[2], shift=0.12 * LEFT),
                      run_time=0.8)

            current_top, current_bot = random_pairs[-1]
            nudged_bot = current_bot.copy()
            nudge_index = int(np.argmin(np.abs(nudged_bot - 0.85)))
            nudged_bot[nudge_index] += 0.60
            old_x = round(current_bot[nudge_index] / BIN_DX) * BIN_DX
            new_x = round(nudged_bot[nudge_index] / BIN_DX) * BIN_DX
            nudge_vector = (
                self.plot_bot[0].number_to_point(new_x)
                - self.plot_bot[0].number_to_point(old_x)
            )

            sample_ring = Circle(radius=0.12).set_stroke(TARGET, 2)
            sample_ring.move_to(self.plot_bot[1][nudge_index])
            self.play(Create(sample_ring), run_time=0.35)
            self.across(
                tracker,
                self.plot_bot[1][nudge_index].animate.shift(nudge_vector),
                sample_ring.animate.shift(nudge_vector),
                ChangeDecimalToValue(
                    score_value, pair_score(current_top, nudged_bot)),
                FadeIn(requirements[3], shift=0.12 * LEFT),
                floor=1.2, reserve=0.35, rate_func=smooth,
            )
            self.play(FadeOut(sample_ring), run_time=0.35)

        final_question = ty.line(
            "samples", "$\\longrightarrow$", "$?$", "$\\longrightarrow$",
            "one smooth scalar",
            size=ty.BODY, color=TARGET,
        ).move_to(requirements)
        layout.fit_in_frame(final_question)
        self.play(FadeOut(requirements, shift=0.10 * UP), run_time=0.5)
        with self.voiceover(
            text="One smooth scalar is where we want to end. But we cannot "
                 "jump straight there. Before that, we need a description "
                 "that keeps the shape."
        ) as tracker:
            self.play(FadeIn(final_question, shift=0.10 * UP), run_time=0.45)
            self.play(Indicate(VGroup(score_box, score_readout),
                               scale_factor=1.06, color=TARGET),
                      run_time=0.65)

        self.inspect(0.8)

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
