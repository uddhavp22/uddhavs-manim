"""Chapter B.10 — the obvious alternative, and why it cannot be used.

Everyone's first instinct for "is this batch Gaussian" is: bin it and compare
the bars. Three measured objections, in the order that they bite:

    ARBITRARY     Sliding the bin edges by 0.15 -- moving no data at all --
                  turns the counts [0 1 1 4 5 10 7 7 2 1 2 0]
                  into              [1 0 2 6 5 10 6 5 2 3 0 0].

    FRAGILE       At bin width 1.5 the bimodal batch reads [2 14 24 0].
                  The two clumps, which are the entire point, are gone.

    NOT USABLE    Moving one sample from 0.4990 to 0.5000 changes a count by a
                  whole unit. The loss is a staircase: derivative zero almost
                  everywhere, undefined at the steps. Gradient descent gets
                  nothing to descend.

The third is the one that actually rules it out, and it is what the smoothness
of e^{itx} buys: d/dx e^{itx} = it e^{itx}, defined everywhere, never zero.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b10_why_not_histograms.py B10 -ql
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
from common.type import BODY, CAPTION, LABEL, STATEMENT, TICK, TITLE, Text
from common import type as ty


GAUSS = data.gaussian_1d(40)
BIMODAL = data.bimodal_1d(40)

X_LO, X_HI = -3.0, 3.0
BASE_Y = -2.6
PLOT_W = 9.4

# Screen height per count. Two values, because the two beats have different
# worst cases: the offset sweep tops out at 12 in a bin, the width sweep at 24.
# A single unit either wastes half the frame in the first beat or sends the
# tallest bar clean off the top of the second -- and an off-frame bar is not an
# error, it just silently is not there.
UNIT_FIXED = 0.30        # offset beat, max count 12  -> top at  1.0
UNIT_WIDE = 0.165        # width beat,  max count 24  -> top at  1.4


def x_to_screen(x):
    return -PLOT_W / 2 + (x - X_LO) / (X_HI - X_LO) * PLOT_W


def histogram(h, width=0.5, offset=0.0, colour=CLOUD, unit=UNIT_FIXED):
    """Bars for `h` under the given binning, sitting on BASE_Y."""
    edges = np.arange(X_LO, X_HI + 1e-9, width) + offset
    counts, _ = np.histogram(h, bins=edges)
    bars = VGroup()
    for c, lo, hi in zip(counts, edges[:-1], edges[1:]):
        if c == 0:
            continue
        sl, sr = x_to_screen(lo), x_to_screen(hi)
        bar = Rectangle(width=sr - sl, height=c * unit)
        bar.set_fill(colour, 0.55).set_stroke(colour, 1.5)
        bar.move_to(np.array([(sl + sr) / 2, BASE_Y + c * unit / 2, 0.0]))
        bars.add(bar)
    return bars, counts


def baseline():
    return Line(np.array([-PLOT_W / 2, BASE_Y, 0.0]),
                np.array([PLOT_W / 2, BASE_Y, 0.0])).set_stroke(MUTED, 2)


def sample_dots(h, colour=EMPIRICAL, radius=0.055):
    return VGroup(*(
        Dot(np.array([x_to_screen(v), BASE_Y - 0.28, 0.0]), radius=radius)
        .set_fill(colour, 0.9) for v in h))


class B10(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.the_instinct()
        self.arbitrary_beat()
        self.fragile_beat()
        self.staircase_beat()
        self.contrast_beat()

    # ------------------------------------------------------------------ 1
    def the_instinct(self):
        head = Text("histogram counts",
                    font_size=BODY).set_color(MUTED)
        head.to_edge(UP, buff=0.6)

        base = baseline()
        dots = sample_dots(GAUSS)
        bars, _ = histogram(GAUSS)

        with self.voiceover(
            text="A histogram groups the samples into bins and compares the resulting counts with a bell curve. It can describe a batch, but it is a poor loss for training."
        ):
            self.play(FadeIn(head), Create(base), run_time=0.8)
            self.play(lagged_map(FadeIn, dots, lag_ratio=0.02),
                      run_time=1.0)
            self.play(lagged_map(FadeIn, bars, shift=0.2 * UP,
                                     lag_ratio=0.08), run_time=1.6)

        self.head, self.base, self.dots, self.bars = head, base, dots, bars

    # ------------------------------------------------------------------ 2
    def arbitrary_beat(self):
        """Slide the edges. No data moves; the picture does."""
        offset = ValueTracker(0.0)
        bars = always_redraw(
            lambda: histogram(GAUSS, offset=offset.get_value())[0])

        note = Text("the data has not moved — only the bin edges",
                    font_size=LABEL).set_color(TARGET)
        note.move_to(np.array([0.0, 2.85, 0.0]))

        with self.voiceover(
            text="Shift the bin edges without moving any sample. "
                 "<bookmark mark='slide'/>Sliding the edges along, without moving a single "
                 "sample, changes the counts."
        ):
            self.remove(self.bars)
            self.add(bars)
            self.wait_until_bookmark("slide")
            self.play(FadeIn(note), run_time=0.6)
            self.play(offset.animate.set_value(0.15), run_time=2.2)
            self.play(offset.animate.set_value(0.0), run_time=1.4)
            self.play(offset.animate.set_value(0.15), run_time=1.4)

        before = MathTex(R"[\,0\ 1\ 1\ 4\ 5\ 10\ 7\ 7\ 2\ 1\ 2\ 0\,]",
                     font_size=28).set_color(MUTED)
        after = MathTex(R"[\,1\ 0\ 2\ 6\ 5\ 10\ 6\ 5\ 2\ 3\ 0\ 0\,]",
                    font_size=28).set_color(COLLAPSE)
        pair = VGroup(before, after).arrange(DOWN, buff=0.24)
        # Above the bars, not across them: the tallest bar reaches y = 1.0.
        pair.move_to(np.array([0.0, 1.85, 0.0]))
        layout.fit_in_frame(pair)

        with self.voiceover(
            text="The counts change although the data does not. The score inherits the arbitrary choice of an origin for the bins."
        ):
            self.play(FadeIn(before), run_time=0.8)
            self.play(FadeIn(after), run_time=0.8)
            self.wait(0.6)

        self.play(FadeOut(VGroup(note, pair)), run_time=0.5)
        self.hist_bars, self.offset = bars, offset

    # ------------------------------------------------------------------ 3
    def fragile_beat(self):
        """Bin width can delete the only feature that mattered."""
        with self.voiceover(
            text="Width changes the picture as well. These red samples have two clumps."
        ):
            self.remove(self.hist_bars)
            self.play(FadeOut(self.dots), run_time=0.4)
            self.offset.set_value(0.0)
            dots = sample_dots(BIMODAL, COLLAPSE)
            self.add(dots)
            self.dots = dots

        width = ValueTracker(0.25)
        bars = always_redraw(
            lambda: histogram(BIMODAL, width=width.get_value(),
                              colour=COLLAPSE, unit=UNIT_WIDE)[0])
        w_read = always_redraw(lambda: VGroup(
            ty.line("bin width", "$=$", size=BODY),
            DecimalNumber(width.get_value(), num_decimal_places=2,
                          font_size=28),
        ).arrange(RIGHT, buff=0.1).set_color(TARGET)
            .move_to(np.array([0.0, 2.85, 0.0])))

        with self.voiceover(
            text="Narrow bins show both clumps. Widening them erases the gap: "
                 "<bookmark mark='gone'/>at a width of one and a half the counts read two, "
                 "fourteen, twenty-four, zero. The bin width has removed the structure we wanted to measure."
        ) as tracker:
            self.add(bars, w_read)
            self.wait(1.0)
            self.wait_until_bookmark("gone")
            self.play(width.animate.set_value(1.5),
                      run_time=max(3.0, tracker.get_remaining_duration() - 0.5),
                      rate_func=smooth)

        self.play(FadeOut(VGroup(bars, w_read, self.dots)), run_time=0.6)

    # ------------------------------------------------------------------ 4
    def staircase_beat(self):
        """The objection that actually rules it out: it is a step function."""
        with self.voiceover(
            text="There is a more serious problem when the score is used for learning."
        ):
            self.play(FadeOut(self.head), FadeOut(self.base), run_time=0.5)

        axes = Axes(
            x_range=(0.35, 0.65, 0.05),
            y_range=(4.5, 8.5, 1),
            width=7.6, height=3.6,
            axis_config={"include_tip": False, "stroke_width": 2},
        )
        axes.move_to(np.array([-1.7, -0.35, 0.0]))

        # The count in one bin, as a single sample slides across its edge.
        xs = np.linspace(0.35, 0.65, 601)
        step = VMobject().set_stroke(COLLAPSE, 4)
        step.set_points_as_corners(
            [axes.c2p(x, 7 if x < 0.5 else 6) for x in xs])

        x_lab = Text("position of one sample", font_size=LABEL).set_color(MUTED)
        x_lab.next_to(axes, DOWN, buff=0.3)
        y_lab = Text("count in its bin", font_size=LABEL).set_color(MUTED)
        y_lab.next_to(axes, LEFT, buff=0.2).rotate(PI / 2)
        edge = DashedLine(axes.c2p(0.5, 4.5), axes.c2p(0.5, 8.5),
                          dash_length=0.08).set_stroke(TARGET, 2, opacity=0.8)
        edge_lab = MathTex("0.5", font_size=24).set_color(TARGET)
        edge_lab.next_to(axes.c2p(0.5, 4.5), DOWN, buff=0.15)

        with self.voiceover(
            text="Move one sample across a bin edge. Its count stays at seven, then jumps to six."
        ):
            self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab),
                      run_time=1.0)
            self.play(Create(edge), FadeIn(edge_lab), run_time=0.6)
            self.play(Create(step), run_time=2.0)

        measured = VGroup(
            ty.line(R"$x_i = 0.4990 \longrightarrow$", "count", "$7$", size=BODY),
            ty.line(R"$x_i = 0.5000 \longrightarrow$", "count", "$6$", size=BODY).set_color(COLLAPSE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        measured.move_to(np.array([3.9, 0.9, 0.0]))
        layout.fit_in_frame(measured)

        verdict = VGroup(
            MathTex(R"\frac{\partial}{\partial x_i} = 0", font_size=34)
            .set_color(MUTED),
            Text("almost everywhere,", font_size=LABEL).set_color(MUTED),
            Text("undefined at the steps", font_size=LABEL).set_color(COLLAPSE),
        ).arrange(DOWN, buff=0.2)
        verdict.move_to(np.array([3.9, -1.5, 0.0]))
        layout.fit_in_frame(verdict)

        with self.voiceover(
            text="A movement of one thousandth changes the count by a whole unit. "
                 "<bookmark mark='grad'/>The derivative of a bin count with respect to a sample "
                 "is zero between jumps and undefined at the jumps. A gradient method gets no direction from it."
        ):
            self.play(FadeIn(measured), run_time=1.0)
            self.wait_until_bookmark("grad")
            self.play(FadeIn(verdict), run_time=1.0)
            self.wait(0.5)

        self.play(FadeOut(VGroup(axes, step, x_lab, y_lab, edge, edge_lab,
                                 measured, verdict)), run_time=0.7)

    # ------------------------------------------------------------------ 5
    def contrast_beat(self):
        """What the arrow construction gives instead."""
        top = ty.words("histogram bin count", size=STATEMENT).set_color(COLLAPSE)
        top.move_to(np.array([0.0, 2.2, 0.0]))
        top_note = Text("a staircase in the data", font_size=LABEL)
        top_note.set_color(MUTED).next_to(top, DOWN, buff=0.25)

        rule = MathTex(R"\frac{\partial}{\partial x}\, e^{itx} = it\, e^{itx}",
                   font_size=46).set_color(TARGET)
        rule.move_to(np.array([0.0, 0.1, 0.0]))
        box = SurroundingRectangle(rule, buff=0.28).set_stroke(TARGET, 2)

        props = VGroup(
            Text("defined at every point", font_size=LABEL),
            Text("never zero", font_size=LABEL),
            Text("and it grows with t — high frequencies push hardest",
                 font_size=LABEL),
        ).arrange(DOWN, buff=0.2).set_color(MUTED)
        props.next_to(box, DOWN, buff=0.5)
        layout.fit_in_frame(props)

        with self.voiceover(
            text="For the wrapped sample, differentiation returns i t times the same arrow."
        ):
            self.play(FadeIn(top), FadeIn(top_note), run_time=0.8)
            self.play(Write(rule), Create(box), run_time=1.6)

        with self.voiceover(
            text="This derivative exists at every sample value and is nonzero away from t equals zero. Moving a sample moves the characteristic function smoothly."
        ):
            self.play(lagged_map(FadeIn, props, shift=0.12 * UP,
                                     lag_ratio=0.35), run_time=1.8)
            self.wait(0.7)

        punch = Text("histogram:  d(count)/dx = 0  almost everywhere",
                     font_size=BODY).set_color(MUTED)
        punch2 = Text("wrapped sample:  d/dx = i t \u00b7 e^{itx},  never zero",
                      font_size=BODY).set_color(TARGET)
        pair = VGroup(punch, punch2).arrange(DOWN, buff=0.2)
        pair.to_edge(DOWN, buff=0.45)
        layout.fit_in_frame(pair)

        with self.voiceover(
            text="The complex exponential gives a smooth response to each sample. The remaining task is to add the disagreement across frequencies."
        ):
            self.play(FadeOut(props), run_time=0.4)
            self.play(Write(pair), run_time=1.8)
            self.wait(0.6)

        self.clear_beat()
