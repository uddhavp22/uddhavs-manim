"""Chapter B.1 — why the obvious shape picture is a bad training loss.

Histograms arrive immediately after the opening problem because they are the
natural first attempt. Their decisive limitation is not appearance but their
hard, discontinuous response when a sample crosses a bin edge.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.distribution import HistogramDiagram
from common.palette import CLOUD, COLLAPSE, MUTED, TARGET
from common import type as ty


def stacked_samples(values, number_line):
    """The sample shape B00 established, before bins replace the points."""
    bin_dx = 0.25
    snapped = [round(value / bin_dx) * bin_dx for value in values]
    levels = layout.stack_levels(snapped, bin_dx)
    return VGroup(*(
        Dot(number_line.n2p(value) + (0.14 + 0.13 * level) * UP,
            radius=0.055).set_fill(CLOUD, 0.92)
        for value, level in zip(snapped, levels)
    ))


class B01(ActScene):
    chain_link = "histograms"

    def construct(self):
        batch = data.bimodal_1d(40)
        edges = np.linspace(-3, 3, 13)
        moving_index = int(np.argmin(np.abs(batch - 0.65)))
        histogram = HistogramDiagram(
            batch, edges, moving_index=moving_index, line_y=-1.95)
        number_line = histogram.number_line
        bars = histogram.bars
        guides = histogram.guides
        sample_dots = stacked_samples(batch, number_line)

        samples_title = ty.words("samples", size=ty.STATEMENT, color=CLOUD)
        samples_title.to_edge(UP, buff=0.55)

        with self.voiceover(
            text="Mean and variance weren't enough, <bookmark mark='samples'/>"
                 "so let's keep all the samples in view."
        ) as tracker:
            self.play(
                FadeIn(samples_title, shift=0.10 * DOWN),
                Create(number_line),
                LaggedStart(*[FadeIn(dot) for dot in sample_dots],
                            lag_ratio=0.018),
                run_time=0.85,
                rate_func=smooth,
            )
            self.wait_until_bookmark("samples")
            self.play(Indicate(sample_dots, color=CLOUD,
                               scale_factor=1.025), run_time=0.5)

        self.inspect(0.65)

        title = ty.words("Histogram", size=ty.STATEMENT, color=TARGET)
        title.move_to(samples_title)
        with self.voiceover(
            text="The first thing you might try is a histogram. "
                 "<bookmark mark='bins'/>Split the number line into bins, "
                 "<bookmark mark='counts'/>then count how many samples land "
                 "in each one. <bookmark mark='shape'/>This keeps the shape "
                 "that those "
                 "two summary numbers missed."
        ) as tracker:
            self.play(Succession(
                          FadeOut(samples_title, shift=0.08 * UP),
                          FadeIn(title, shift=0.08 * UP),
                      ),
                      run_time=0.65)
            self.wait_until_bookmark("bins")
            self.play(FadeIn(guides), run_time=0.32)
            self.wait_until_bookmark("counts")
            # Let the dots recede as their counts rise. Doing both in one
            # gesture preserves the causal link without drawing bars through
            # live points or making one encoding pop out before the other.
            self.play(
                AnimationGroup(
                    LaggedStart(*[
                        FadeOut(dot, shift=0.12 * DOWN)
                        for dot in sample_dots
                    ], lag_ratio=0.018),
                    LaggedStart(*[
                        GrowFromEdge(bar, DOWN) for bar in bars
                    ], lag_ratio=0.05),
                    lag_ratio=0.12,
                ),
                run_time=1.05,
                rate_func=smooth,
            )
            self.wait_until_bookmark("shape")
            self.play(Indicate(bars, color=TARGET, scale_factor=1.02),
                      run_time=0.5)

        self.inspect(0.75)

        # The chart moves up only when a separate sample track needs the lower
        # third. Keeping x_i off the histogram baseline prevents the sample,
        # bars, and axis labels from becoming one ambiguous pile of marks.
        chart_shift = 0.65 * UP
        sample_track = NumberLine(
            x_range=(-3, 3, 0.5), length=9.4, include_numbers=False,
            include_tip=False,
        ).set_stroke(MUTED, 2)
        sample_track.move_to([0.0, -2.75, 0.0])

        histogram.follow_moving_sample()
        # Begin far enough inside the bin that the viewer can see a genuine
        # interval of motion before the count changes.
        histogram.moving_x.set_value(0.68)

        moving_dot = always_redraw(lambda: Dot(
            sample_track.n2p(histogram.moving_x.get_value()), radius=0.085,
        ).set_fill(TARGET, 1))
        sample_label = ty.maths(R"x_i", size=ty.EQ, color=TARGET)
        sample_label.add_updater(
            lambda m: m.next_to(moving_dot, DOWN, buff=0.13))

        edge_value = 1.0
        edge_x = number_line.n2p(edge_value)[0]
        edge = Line(
            [edge_x, sample_track.n2p(edge_value)[1] + 0.10, 0.0],
            [edge_x, number_line.n2p(edge_value)[1] - 0.08, 0.0],
        ).set_stroke(TARGET, 2.5, opacity=0.9)
        edge_label = ty.words("bin edge", size=ty.LABEL, color=TARGET)
        edge_label.next_to(edge, RIGHT, buff=0.16)

        edge_index = int(np.flatnonzero(np.isclose(edges, edge_value))[0])
        left_bin, right_bin = edge_index - 1, edge_index

        def count_in(bin_index):
            return int(np.histogram(histogram.current_samples(), bins=edges)[0][bin_index])

        left_count = Integer(count_in(left_bin), font_size=ty.READOUT).set_color(TARGET)
        right_count = Integer(count_in(right_bin), font_size=ty.READOUT).set_color(TARGET)
        left_count.add_updater(
            lambda m: m.set_value(count_in(left_bin)).next_to(
                bars[left_bin], UP, buff=0.10))
        right_count.add_updater(
            lambda m: m.set_value(count_in(right_bin)).next_to(
                bars[right_bin], UP, buff=0.10))
        count_labels = VGroup(left_count, right_count)

        verdict = VGroup(
            ty.line("between edges:", R"$\frac{dc}{dx_i}=0$",
                    size=ty.LABEL, color=CLOUD),
            ty.line("at an edge:", "undefined",
                    size=ty.LABEL, color=COLLAPSE),
        ).arrange(DOWN, buff=0.18)
        verdict.move_to([-4.45, 2.25, 0])
        layout.fit_in_frame(verdict)

        with self.voiceover(
            text="But the score still has to be differentiable in every "
                 "sample. <bookmark mark='sample'/>Watch what happens to this "
                 "one."
        ) as tracker:
            dot_seed = Dot(
                sample_track.n2p(histogram.moving_x.get_value()),
                radius=0.085,
            ).set_fill(TARGET, 1)
            sample_label.update(0)
            self.play(
                FadeOut(title),
                number_line.animate.shift(chart_shift),
                bars.animate.shift(chart_shift),
                guides.animate.shift(chart_shift),
                run_time=0.65,
                rate_func=smooth,
            )
            self.wait_until_bookmark("sample")
            self.play(Create(sample_track), FadeIn(dot_seed),
                      Create(edge), FadeIn(edge_label),
                      FadeIn(count_labels), FadeIn(sample_label), run_time=0.48)
            self.remove(dot_seed)
            self.add(moving_dot)

        with self.voiceover(
            text="Inside the bin, both counts stay fixed. But the instant it "
                 "<bookmark mark='crosses'/>crosses the edge, one drops and "
                 "the other jumps."
        ) as tracker:
            # One linear pass, rather than separate approach/cross/depart
            # animations. Choose its endpoints from the actual bookmark time,
            # so the discrete bar jump lands on the word "crosses" without the
            # dot stopping at the boundary.
            run_time = max(3.0, tracker.get_remaining_duration())
            cross_fraction = np.clip(
                tracker.time_until_bookmark("crosses") / run_time,
                0.25, 0.75,
            )
            span = 0.62
            start = edge_value - cross_fraction * span
            end = start + span
            histogram.moving_x.set_value(start)
            moving_dot.update(0)
            self.play(
                histogram.moving_x.animate.set_value(end),
                ShowPassingFlash(
                    edge.copy().set_stroke(WHITE, 5),
                    time_width=0.22,
                    rate_func=squish_rate_func(
                        there_and_back,
                        max(0.0, cross_fraction - 0.08),
                        min(1.0, cross_fraction + 0.08),
                    ),
                ),
                run_time=run_time,
                rate_func=linear,
            )

        self.inspect(0.65)

        with self.voiceover(
            text="So the derivative is <bookmark mark='zero'/>zero between "
                 "edges and <bookmark mark='undefined'/>undefined at the "
                 "boundary. That breaks the differentiability we needed."
        ) as tracker:
            self.wait_until_bookmark("zero")
            self.play(FadeIn(verdict[0], shift=0.10 * RIGHT), run_time=0.3)
            self.wait_until_bookmark("undefined")
            self.play(FadeIn(verdict[1], shift=0.10 * RIGHT), run_time=0.3)
            self.play(Circumscribe(verdict, color=COLLAPSE,
                                   fade_out=True, buff=0.12),
                      run_time=0.7)

        with self.voiceover(
            text="We need a smooth question we can ask each sample, so that "
                 "<bookmark mark='small'/>a small move produces a small "
                 "change in its answer."
        ) as tracker:
            self.freeze(bars, count_labels)
            self.play(
                FadeOut(VGroup(number_line, guides, edge, edge_label,
                               verdict, count_labels, bars)),
                sample_track.animate.shift(1.85 * UP),
                histogram.moving_x.animate.set_value(1.45),
                run_time=0.65,
                rate_func=smooth,
            )
            prompt = ty.maths(R"x_i \longmapsto\ ?", size=ty.EQ_DISPLAY,
                              color=TARGET)
            prompt.move_to([0.0, 1.25, 0.0])
            self.play(FadeIn(prompt, shift=0.10 * UP), run_time=0.4)
            self.wait_until_bookmark("small")
            self.play(Circumscribe(prompt, color=TARGET,
                                   fade_out=True, buff=0.16),
                      run_time=0.7)
        self.inspect(0.55)
        # Keep this exact unresolved frame for B02's match cut. Clearing here
        # and fading the same objects back in there caused a black flash at the
        # boundary and made the opening word of B02 feel clipped.
        self.settle_frame()
