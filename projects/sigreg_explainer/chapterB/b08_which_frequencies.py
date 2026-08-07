"""Chapter B.8 — which frequencies are worth looking at.

Two facts, pulling in opposite directions. Both measured, neither asserted:

    LOW t is blind to shape.   The Gaussian and bimodal batches from B00 --
        same mean, same variance -- have fingerprints that differ by 0.0021 at
        t = 0.3. By t = 3.0 they differ by 0.8989.

    HIGH t is mostly noise.    With N samples the empirical fingerprint has a
        floor: E|phi_N(t)|^2 -> 1/N. Measured over 4000 draws at t = 6,
        N = 40 gives 0.0251 against 1/N = 0.0250, while the true value is
        2.3e-16. A perfectly Gaussian batch looks non-Gaussian up there,
        purely because it is finite.

Squeeze from both ends and a window falls out. That is the honest reason the
weighting w_lambda(t) exists, and the reason the integration range is [0.2, 4]
rather than "as wide as possible" -- it is not a tuning knob someone chose.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b08_which_frequencies.py B08 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import data, layout
from common.beat import ActScene
from common.palette import BG, CLOUD, COLLAPSE, EMPIRICAL, FAINT, MUTED, TARGET
from common.type import BODY, CAPTION, LABEL, STATEMENT, TICK, TITLE, Text
from common import type as ty
from common.wrap import ecf, gaussian_cf


T_MAX = 6.5
GRID = np.linspace(0, T_MAX, 700)

N_SAMPLES = 40
GAUSS = data.gaussian_1d(N_SAMPLES)
BIMODAL = data.bimodal_1d(N_SAMPLES)

# The window from PLAN.md section 7: 99.78% of the Epps-Pulley integrand's mass.
WINDOW = (0.2, 4.0)


def big_axes():
    axes = Axes(
        x_range=(0, T_MAX, 1),
        y_range=(-0.85, 1.1, 0.5),
        width=11.0,
        height=4.3,
        axis_config={"include_tip": False, "stroke_width": 2},
    )
    axes.move_to(np.array([0.0, -0.45, 0.0]))
    return axes


def polyline(axes, xs, ys, colour, width=4, opacity=1.0):
    c = VMobject().set_stroke(colour, width, opacity=opacity)
    c.set_points_as_corners([axes.c2p(a, b) for a, b in zip(xs, ys)])
    return c


class B08(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.axes = big_axes()
        self.setup_axes()
        self.low_is_blind()
        self.high_sees_shape()
        self.high_is_noisy()
        self.window_beat()

    # ------------------------------------------------------------------
    def setup_axes(self):
        labs = VGroup()
        for v in (1, 2, 3, 4, 5, 6):
            lab = MathTex(str(v), font_size=22).set_color(MUTED)
            lab.next_to(self.axes.c2p(v, 0), DOWN, buff=0.15)
            labs.add(lab)
        one = MathTex("1", font_size=22).set_color(MUTED)
        one.next_to(self.axes.c2p(0, 1), LEFT, buff=0.15)
        t_lab = MathTex("t", font_size=28).set_color(MUTED)
        t_lab.next_to(self.axes.c2p(T_MAX, 0), DR, buff=0.15)
        self.furniture = VGroup(labs, one, t_lab)
        self.add(self.axes, self.furniture)

        self.g_table = ecf(GAUSS, GRID).real
        self.b_table = ecf(BIMODAL, GRID).real

    # ------------------------------------------------------------------ 1
    def low_is_blind(self):
        """The two batches from B00 again. At low t nothing distinguishes them."""
        head = Text("how the two curves separate",
                    font_size=BODY).to_edge(UP, buff=0.6)
        head.set_color(MUTED)

        legend = VGroup(
            Text("bell curve", font_size=LABEL).set_color(EMPIRICAL),
            Text("two clumps", font_size=LABEL).set_color(COLLAPSE),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        legend.move_to(self.axes.c2p(5.4, 0.82))

        with self.voiceover(
            text="The blue batch is bell-shaped. The red batch has two clumps. Sweep the same frequency through both batches and compare their average arrows."
        ):
            self.play(FadeIn(head), FadeIn(legend), run_time=0.9)

        t = ValueTracker(0.0)
        g_curve = always_redraw(lambda: polyline(
            self.axes, *self._upto(self.g_table, t), EMPIRICAL))
        b_curve = always_redraw(lambda: polyline(
            self.axes, *self._upto(self.b_table, t), COLLAPSE))

        gap_readout = always_redraw(lambda: self._gap_readout(t))

        self.add(g_curve, b_curve, gap_readout)

        with self.voiceover(
            text="Near zero, both curves behave almost the same. As the frequency grows, the red curve falls below zero while the blue curve stays close to it."
        ) as tracker:
            self.play(t.animate.set_value(3.2),
                      run_time=max(5.0, tracker.get_remaining_duration()),
                      rate_func=linear)

        band = Rectangle(
            width=self.axes.c2p(0.6, 0)[0] - self.axes.c2p(0, 0)[0],
            height=3.4).set_fill(TARGET, 0.10).set_stroke(width=0)
        band.move_to(np.array([
            (self.axes.c2p(0, 0)[0] + self.axes.c2p(0.6, 0)[0]) / 2,
            self.axes.c2p(0, 0.45)[1], 0.0]))

        blind = VGroup(
            Text("near zero: almost the same", font_size=BODY),
            ty.line("at", "$t = 0.3$,", "gap", "$= 0.0021$", size=BODY).set_color(TARGET),
        ).arrange(DOWN, buff=0.2)
        blind.to_edge(DOWN, buff=0.45)
        layout.fit_in_frame(blind)

        with self.voiceover(
            text="At t equals point three, the gap is only two thousandths. Low frequencies mainly see location and spread, so matching mean and variance makes these two batches hard to distinguish there."
        ):
            self.play(FadeIn(band), run_time=0.7)
            self.play(FadeIn(blind), run_time=1.0)

        self.t, self.band, self.blind = t, band, blind
        self.head, self.legend = head, legend

    def _upto(self, table, t):
        m = GRID <= max(t.get_value(), 1e-4)
        xs, ys = GRID[m], table[m]
        if len(xs) < 2:
            xs, ys = np.array([0.0, 1e-4]), np.array([1.0, 1.0])
        return xs, ys

    def _gap_readout(self, t):
        v = t.get_value()
        gap = abs(np.interp(v, GRID, self.g_table)
                  - np.interp(v, GRID, self.b_table))
        grp = VGroup(
            ty.line("gap", "$=$", size=BODY),
            DecimalNumber(gap, num_decimal_places=4, font_size=28),
        ).arrange(RIGHT, buff=0.1).set_color(TARGET)
        # y = 2.5, not 3.05: the header sits at roughly 3.2 and the two
        # overlapped. Nothing errors -- the frame just reads as one smeared line.
        grp.move_to(np.array([0.0, 2.5, 0.0]))
        return grp

    # ------------------------------------------------------------------ 2
    def high_sees_shape(self):
        """Keep going, and the clumps announce themselves."""
        with self.voiceover(
            text="At t equals three, the gap is almost point nine. The two-clump structure has become visible."
        ) as tracker:
            self.play(FadeOut(self.blind), run_time=0.35)
            self.play(self.t.animate.set_value(T_MAX),
                      run_time=max(3.0, tracker.get_remaining_duration()),
                      rate_func=linear)

        peak = Line(self.axes.c2p(3.0, self.b_table[np.argmin(np.abs(GRID - 3))]),
                    self.axes.c2p(3.0, self.g_table[np.argmin(np.abs(GRID - 3))]))
        peak.set_stroke(TARGET, 4)
        peak_lab = MathTex("0.8989", font_size=28).set_color(TARGET)
        peak_lab.next_to(peak, RIGHT, buff=0.15)

        with self.voiceover(
            text="The separation tempts us to keep increasing t. A finite batch puts a limit on that."
        ):
            self.play(Create(peak), FadeIn(peak_lab), run_time=1.0)
            self.wait(0.5)

        self.play(FadeOut(VGroup(peak, peak_lab, self.band, self.legend)),
                  run_time=0.6)

    # ------------------------------------------------------------------ 3
    def high_is_noisy(self):
        """The finite-sample floor. Every curve here is a real draw of 40."""
        with self.voiceover(
            text="Draw forty samples from one genuine Gaussian, twenty times. Each blue curve is the empirical average from one such batch."
        ):
            self.play(FadeOut(self.head), run_time=0.4)
            self.remove(*[m for m in self.mobjects
                          if m not in (self.axes, self.furniture)])

        rng = np.random.default_rng(20260806)
        draws = VGroup()
        for _ in range(20):
            x = rng.standard_normal(N_SAMPLES)
            draws.add(polyline(self.axes, GRID, ecf(x, GRID).real,
                               CLOUD, width=2, opacity=0.45))

        truth = polyline(self.axes, GRID, gaussian_cf(GRID), TARGET, width=5)
        truth_lab = MathTex(R"e^{-t^2/2}", font_size=30).set_color(TARGET)
        truth_lab.move_to(self.axes.c2p(2.0, 0.5))

        with self.voiceover(
            text="The amber curve is the population value. The scatter around it comes from sampling, not from a different distribution."
        ):
            self.play(Create(truth), FadeIn(truth_lab), run_time=1.4)
            self.play(lagged_map(Create, draws, lag_ratio=0.06),
                      run_time=2.6)

        # Shade the region where the spread of the draws swamps the signal.
        x0 = self.axes.c2p(3.2, 0)[0]
        x1 = self.axes.c2p(T_MAX, 0)[0]
        noisy = Rectangle(width=x1 - x0, height=2.0)
        noisy.set_fill(COLLAPSE, 0.14).set_stroke(width=0)
        noisy.move_to(np.array([(x0 + x1) / 2, self.axes.c2p(0, 0.05)[1], 0.0]))

        floor = VGroup(
            Text("out here the truth is zero —", font_size=BODY),
            Text("everything you see is sampling noise",
                 font_size=BODY).set_color(COLLAPSE),
        ).arrange(DOWN, buff=0.18)
        floor.to_edge(DOWN, buff=0.42)
        layout.fit_in_frame(floor)

        with self.voiceover(
            text="Far to the right, the amber curve is essentially zero while the empirical curves still wander. That wandering is sampling noise."
        ):
            self.play(FadeIn(noisy), run_time=0.7)
            self.play(FadeIn(floor), run_time=1.0)

        law = VGroup(
            MathTex(R"\mathbb{E}\,|\hat\varphi_N(t)|^2 \ \longrightarrow\ "
                R"\frac{1}{N}", font_size=36).set_color(TARGET),
            Text("measured at t = 6, N = 40:   0.0251   against   1/N = 0.0250",
                 font_size=TICK).set_color(MUTED),
            Text("the true value there is 2 × 10⁻¹⁶",
                 font_size=TICK).set_color(MUTED),
        ).arrange(DOWN, buff=0.22)
        law.move_to(np.array([0.0, -0.4, 0.0]))
        box = BackgroundRectangle(law, buff=0.35).set_fill(BG, 0.88)
        layout.fit_in_frame(law)

        with self.voiceover(
            text="Its squared size settles near one over N. With forty samples that is point zero two five, even when the batch is Gaussian."
        ):
            self.play(FadeOut(floor), run_time=0.4)
            self.play(FadeIn(box), Write(law[0]), run_time=1.4)
            self.play(FadeIn(law[1]), run_time=0.8)
            self.play(FadeIn(law[2]), run_time=0.8)
            self.wait(0.5)

        self.play(FadeOut(VGroup(box, law, noisy, draws, truth, truth_lab)),
                  run_time=0.8)

    # ------------------------------------------------------------------ 4
    def window_beat(self):
        """Squeezed from both ends: a window, not a knob."""
        # Both captions go ABOVE the plot. Sitting them at the far left and
        # right *inside* it put "too low" on top of the window rectangle and the
        # y-axis label, because the t < 0.2 sliver is only a few pixels wide.
        left = Text("too low:\nblind to shape", font_size=LABEL,
                    alignment="CENTER").set_color(MUTED)
        left.move_to(np.array([-4.4, 2.75, 0.0]))
        right = Text("too high:\nnothing but noise", font_size=LABEL,
                     alignment="CENTER").set_color(MUTED)
        right.move_to(np.array([4.4, 2.75, 0.0]))

        x0 = self.axes.c2p(WINDOW[0], 0)[0]
        x1 = self.axes.c2p(WINDOW[1], 0)[0]
        win = Rectangle(width=x1 - x0, height=2.4)
        win.set_fill(TARGET, 0.13).set_stroke(TARGET, 2, opacity=0.6)
        win.move_to(np.array([(x0 + x1) / 2, self.axes.c2p(0, 0.3)[1], 0.0]))
        win_lab = MathTex(R"[\,0.2,\ 4\,]", font_size=32).set_color(TARGET)
        win_lab.next_to(win, UP, buff=0.18)

        with self.voiceover(
            text="Low frequencies miss shape. Very high frequencies measure mostly noise."
        ):
            self.play(FadeIn(left), run_time=0.8)
            self.play(FadeIn(right), run_time=0.8)

        with self.voiceover(
            text="The useful range lies between them: roughly point two to four for this Gaussian target."
        ):
            self.play(FadeIn(win), FadeIn(win_lab), run_time=1.2)

        punch = VGroup(
            Text("Something has to suppress the high frequencies.",
                 font_size=BODY),
            Text("That much is forced by having finitely many samples.",
                 font_size=BODY).set_color(TARGET),
        ).arrange(DOWN, buff=0.2)
        punch.to_edge(DOWN, buff=0.45)
        layout.fit_in_frame(punch)

        # Careful here. The source calls lambda a *bandwidth parameter*, so the
        # weighting plainly IS tunable and an earlier draft of this line claimed
        # it was not. What finite N forces is that high frequencies must be
        # suppressed at all -- not the particular bandwidth. Overclaiming the
        # second from the first is the kind of thing a persuasive animation gets
        # away with, which is why EXPLAINER_PROCESS.md audits it separately.
        with self.voiceover(
            text="The statistic therefore downweights high frequencies. The bandwidth remains a choice, but the need to suppress noisy frequencies does not."
        ):
            self.play(Write(punch), run_time=1.8)
            self.wait(0.6)

        with self.voiceover(
            text="Within this band, a Gaussian has a specific target curve."
        ):
            self.play(FadeOut(VGroup(left, right, win, win_lab, punch)), run_time=0.7)
        self.clear_beat()
