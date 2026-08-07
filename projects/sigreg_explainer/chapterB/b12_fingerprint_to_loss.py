"""Chapter B.12 — from a fingerprint to a number you can minimise.

The last step of Chapter B, and it is deliberately small, because all the work
was done already. At a fixed frequency the two fingerprints are two POINTS in
the plane. The disagreement between them is the distance between those points.
Square it so it is smooth and positive, add it up across the frequencies that
B08 said were worth looking at, and that total is the score.

Measured on the window [0.2, 4] (PLAN.md section 7):

    a genuine Gaussian batch of 40   ->   0.0184
    the two-clump batch of 40        ->   1.0369      56.4x larger

The residual 0.0184 is not an error. It is the finite-sample floor from B08,
showing up exactly where B08 said it would.

Ends on the question Chapter C opens with: this scores a batch of *scalars*, and
representations are vectors.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b12_fingerprint_to_loss.py B12 -ql
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
from common.wrap import ecf, gaussian_cf


T_LO, T_HI = 0.2, 4.0
GRID = np.linspace(T_LO, T_HI, 600)

GAUSS = data.gaussian_1d(40)
BIMODAL = data.bimodal_1d(40)

PLANE_CENTRE = np.array([-4.05, -0.55, 0.0])
PLANE_R = 1.75


class B12(ActScene):
    chain_link = "Epps-Pulley"

    def construct(self):
        self.batch = BIMODAL
        self.build_panels()
        self.two_points_beat()
        self.sweep_beat()
        self.compare_beat()
        self.formula_beat()

    # ------------------------------------------------------------------
    def build_panels(self):
        self.t = ValueTracker(T_LO)

        self.plane = VGroup(
            Line(1.4 * PLANE_R * LEFT, 1.4 * PLANE_R * RIGHT)
            .set_stroke(FAINT, 1.4),
            Line(1.25 * PLANE_R * DOWN, 1.25 * PLANE_R * UP)
            .set_stroke(FAINT, 1.4),
            Circle(radius=PLANE_R).set_stroke(MUTED, 1.6, opacity=0.35),
        ).move_to(PLANE_CENTRE)

        self.gap_axes = Axes(
            x_range=(0, T_HI, 1),
            y_range=(0, 0.75, 0.25),
            width=6.3, height=3.5,
            axis_config={"include_tip": False, "stroke_width": 2},
        )
        self.gap_axes.move_to(np.array([3.15, -0.55, 0.0]))

    def _pt(self, z):
        return PLANE_CENTRE + PLANE_R * np.array([z.real, z.imag, 0.0])

    def _hat(self):
        return ecf(self.batch, [self.t.get_value()])[0]

    def _tgt(self):
        return complex(gaussian_cf(self.t.get_value()), 0.0)

    def _gap_table(self, batch):
        return np.abs(ecf(batch, GRID) - gaussian_cf(GRID)) ** 2

    # ------------------------------------------------------------------ 1
    def two_points_beat(self):
        """At one frequency, both fingerprints are points. Nothing more."""
        with self.voiceover(
            text="At a fixed frequency, the batch and Gaussian produce two average arrows. Their separation gives one contribution to the loss."
        ):
            self.play(Create(self.plane), run_time=1.0)

        self.t.set_value(1.6)
        hat_dot = always_redraw(lambda: Dot(self._pt(self._hat()), radius=0.1)
                                .set_fill(EMPIRICAL, 1))
        tgt_dot = always_redraw(lambda: Dot(self._pt(self._tgt()), radius=0.1)
                                .set_fill(TARGET, 1))
        hat_arm = always_redraw(lambda: Line(PLANE_CENTRE,
                                             self._pt(self._hat()))
                                .set_stroke(EMPIRICAL, 3, opacity=0.55))
        tgt_arm = always_redraw(lambda: Line(PLANE_CENTRE,
                                             self._pt(self._tgt()))
                                .set_stroke(TARGET, 3, opacity=0.55))

        hat_lab = MathTex(R"\hat\varphi_N(t)", font_size=28).set_color(EMPIRICAL)
        tgt_lab = MathTex(R"\varphi_0(t)", font_size=28).set_color(TARGET)

        with self.voiceover(
            text="At this frequency, the batch gives one average arrow; "
                 "<bookmark mark='tgt'/>the Gaussian gives another. Their endpoints are two points in the complex plane."
        ):
            self.play(FadeIn(hat_arm), FadeIn(hat_dot), run_time=0.9)
            hat_lab.next_to(hat_dot, UL, buff=0.12)
            self.play(FadeIn(hat_lab), run_time=0.5)
            self.wait_until_bookmark("tgt")
            self.play(FadeIn(tgt_arm), FadeIn(tgt_dot), run_time=0.9)
            tgt_lab.next_to(tgt_dot, DR, buff=0.12)
            self.play(FadeIn(tgt_lab), run_time=0.5)

        gap_line = always_redraw(lambda: Line(
            self._pt(self._hat()), self._pt(self._tgt()))
            .set_stroke(COLLAPSE, 5))

        with self.voiceover(
            text="The red segment is their difference."
        ):
            self.play(Create(gap_line), run_time=1.0)

        sq = MathTex(R"\big|\hat\varphi_N(t) - \varphi_0(t)\big|^2", font_size=34)
        sq.set_color(COLLAPSE).move_to(np.array([-4.05, 2.5, 0.0]))
        layout.fit_in_frame(sq)
        why = VGroup(
            Text("squared, so it is positive", font_size=LABEL),
            Text("and smooth at zero", font_size=LABEL),
        ).arrange(DOWN, buff=0.16).set_color(MUTED)
        why.next_to(sq, DOWN, buff=0.28)

        with self.voiceover(
            text="Square the length: the contribution stays positive and remains smooth when the arrows meet."
        ):
            self.play(Write(sq), run_time=1.3)
            self.play(FadeIn(why), run_time=0.7)

        self.play(FadeOut(VGroup(hat_lab, tgt_lab, why)), run_time=0.5)
        self.sq = sq
        # Everything in the left panel that redraws itself every frame. It has
        # to be torn down explicitly when the panel goes: FadeOut cannot remove
        # an always_redraw mobject, so these would otherwise sit on the closing
        # frames as two stray dots with no panel around them.
        self.plane_live = VGroup(hat_arm, tgt_arm, hat_dot, tgt_dot, gap_line)

    # ------------------------------------------------------------------ 2
    def sweep_beat(self):
        """One t is one number. Every t is a curve, and its area is the score."""
        labs = VGroup()
        for v in (1, 2, 3, 4):
            lab = MathTex(str(v), font_size=22).set_color(MUTED)
            lab.next_to(self.gap_axes.c2p(v, 0), DOWN, buff=0.14)
            labs.add(lab)
        t_lab = MathTex("t", font_size=26).set_color(MUTED)
        t_lab.next_to(self.gap_axes.c2p(T_HI, 0), DR, buff=0.14)
        head = Text("squared gap, at every frequency", font_size=LABEL)
        head.set_color(MUTED).next_to(self.gap_axes, UP, buff=0.28)

        self.table = self._gap_table(self.batch)

        with self.voiceover(
            text="Repeat that squared distance across the frequency band from point two to four."
        ):
            self.play(Create(self.gap_axes), FadeIn(labs), FadeIn(t_lab),
                      FadeIn(head), run_time=1.2)

        self.t.set_value(T_LO)
        filled = always_redraw(lambda: self._area_of(self.table, COLLAPSE))
        self.add(filled)

        with self.voiceover(
            text="The red segment changes with t. The graph records its squared length, and the shaded area adds those contributions."
        ) as tracker:
            self.play(self.t.animate.set_value(T_HI),
                      run_time=max(6.5, tracker.get_remaining_duration()),
                      rate_func=linear)

        total = ty.line("total area", "$= 1.0369$", size=BODY)
        total.set_color(COLLAPSE).next_to(self.gap_axes, DOWN, buff=0.35)
        layout.fit_in_frame(total)

        with self.voiceover(
            text="For the two-clump batch, the accumulated area is one point zero four."
        ):
            self.play(Write(total), run_time=1.3)

        self.filled, self.total, self.head = filled, total, head
        self.axis_furniture = VGroup(labs, t_lab)

    # ------------------------------------------------------------------ 3
    def compare_beat(self):
        """A real Gaussian batch, for scale. The residual is B08's floor."""
        with self.voiceover(
            text="Run the same calculation on a batch drawn from a Gaussian."
        ):
            ghost = self.filled.copy().set_fill(COLLAPSE, 0.12)
            ghost.set_stroke(COLLAPSE, 2, opacity=0.4)
            self.remove(self.filled)
            self.add(ghost)
            self.play(FadeOut(self.total), run_time=0.4)
            self.batch = GAUSS
            self.table = self._gap_table(self.batch)
            self.t.set_value(T_LO)
            self.filled = always_redraw(
                lambda: self._area_of(self.table, EMPIRICAL))
            self.add(self.filled)
            self.ghost = ghost

        with self.voiceover(
            text="Its empirical curve stays close to the target, so little area accumulates."
        ) as tracker:
            self.play(self.t.animate.set_value(T_HI),
                      run_time=max(5.0, tracker.get_remaining_duration()),
                      rate_func=linear)

        scores = VGroup(
            ty.line("two clumps:", "$1.0369$", size=BODY)
            .set_color(COLLAPSE),
            ty.line("a real bell curve:", "$0.0184$", size=BODY)
            .set_color(EMPIRICAL),
            MathTex(R"56\times", font_size=38).set_color(TARGET),
        ).arrange(DOWN, buff=0.24)
        scores.move_to(np.array([-4.05, 0.6, 0.0]))
        layout.fit_in_frame(scores)

        with self.voiceover(
            text="Point zero one eight versus one point zero four: a factor of fifty-six. The score did not need a rule for how many clumps to search for."
        ):
            self.plane_live.clear_updaters(recursive=True)
            self.play(FadeOut(VGroup(self.plane, self.sq, self.plane_live)),
                      run_time=0.5)
            self.remove(self.plane_live)
            self.play(FadeIn(scores[0]), FadeIn(scores[1]), run_time=1.0)
            self.play(Write(scores[2]), run_time=0.8)

        honest = VGroup(
            Text("0.0184  =  the finite-sample floor", font_size=LABEL),
            Text("for N = 40, measured earlier",
                 font_size=LABEL).set_color(MUTED),
        ).arrange(DOWN, buff=0.16)
        honest.next_to(scores, DOWN, buff=0.45)
        layout.fit_in_frame(honest)

        with self.voiceover(
            text="The small residual is the finite-sample noise floor from the frequency sweep."
        ):
            self.play(FadeIn(honest), run_time=1.0)
            self.wait(0.6)

        self.play(FadeOut(VGroup(scores, honest, self.ghost, self.filled,
                                 self.gap_axes, self.axis_furniture,
                                 self.head)), run_time=0.8)

    def _area_of(self, table, colour):
        t = self.t.get_value()
        m = GRID <= max(t, T_LO + 1e-4)
        xs, ys = GRID[m], table[m]
        if len(xs) < 2:
            return VMobject()
        pts = [self.gap_axes.c2p(xs[0], 0)]
        pts += [self.gap_axes.c2p(x, y) for x, y in zip(xs, ys)]
        pts += [self.gap_axes.c2p(xs[-1], 0)]
        poly = VMobject().set_fill(colour, 0.4).set_stroke(colour, 3)
        poly.set_points_as_corners(pts + [pts[0]])
        return poly

    # ------------------------------------------------------------------ 4
    def formula_beat(self):
        """Write it down, and hand over to Chapter C."""
        # Two steps, deliberately. Step one is EXACTLY the quantity the sweep
        # animated; step two adds the weight and the N prefactor that make it
        # the named statistic. Showing the finished formula straight away puts
        # a w_lambda(t) on screen that the picture never constructed -- the
        # visual-symbolic correspondence check in EXPLAINER_PROCESS.md section 4
        # catches exactly that, and it was the original defect here.
        plain = MathTex(R"\int \big|\hat\varphi_N(t) - \varphi_0(t)\big|^2\, dt",
                    font_size=44)
        plain.move_to(np.array([0.0, 1.35, 0.0]))
        layout.fit_in_frame(plain)

        with self.voiceover(
            text="The picture writes as an integral of squared gaps."
        ):
            self.play(Write(plain), run_time=2.0)

        formula = MathTex(
            R"\mathcal{T} = N \int w_\lambda(t)\,"
            R"\big|\hat\varphi_N(t) - \varphi_0(t)\big|^2\, dt",
            font_size=44)
        formula.move_to(np.array([0.0, 1.35, 0.0]))
        layout.fit_in_frame(formula)

        with self.voiceover(
            text="The published statistic adds two normalizations. "
                 "<bookmark mark='full'/>A weight function fades the high frequencies out "
                 "smoothly rather than stopping at four. Lambda controls "
                 "that bandwidth. The factor N keeps the scale comparable "
                 "across batch sizes."
        ):
            self.wait_until_bookmark("full")
            self.play(TransformMatchingTex(plain, formula), run_time=1.8)

        # Symbol and gloss are separate mobjects: a Tex fragment inside a Text
        # string renders as literal characters, and the combining hat on phi
        # does not survive Text at all.
        rows = [
            (R"\big|\hat\varphi_N - \varphi_0\big|^2",
             "the squared gap between two points in the plane"),
            (R"\textstyle\int dt", "added up across frequencies"),
            (R"w_\lambda(t)", "high frequencies count for less"),
            (R"N", "so the score means the same at any batch size"),
        ]
        # Two columns with fixed x, rather than per-row arrange(RIGHT): the
        # symbols have very different widths, so arranging each row on its own
        # leaves the glosses ragged down the page.
        SYM_X, GLOSS_X = -3.9, -2.6
        parts = VGroup()
        for i, (tex, gloss) in enumerate(rows):
            y = -0.2 - 0.58 * i
            sym = MathTex(tex, font_size=30).set_color(COLLAPSE)
            sym.move_to(np.array([SYM_X, y, 0.0]), aligned_edge=RIGHT)
            txt = Text(gloss, font_size=LABEL).set_color(MUTED)
            txt.move_to(np.array([GLOSS_X, y, 0.0]), aligned_edge=LEFT)
            parts.add(VGroup(sym, txt))
        layout.fit_in_frame(parts)

        with self.voiceover(
            text="The square is the red segment. The integral adds it across frequencies. The weight suppresses the range where the empirical curve is noisy."
        ):
            self.play(lagged_map(FadeIn, parts, shift=0.15 * RIGHT,
                                     lag_ratio=0.4), run_time=2.4)

        name = Text("the Epps–Pulley statistic",
                    font_size=BODY).set_color(TARGET)
        name.move_to(np.array([0.0, -2.65, 0.0]))
        layout.fit_in_frame(name)

        with self.voiceover(
            text="This is the Epps–Pulley statistic."
        ):
            self.play(FadeIn(name), run_time=1.0)
            self.wait(0.5)

        with self.voiceover(
            text="Unlike the histogram count, this statistic is differentiable in the samples, so gradient descent can reduce it."
        ):
            self.play(FadeOut(VGroup(parts, name)), run_time=0.6)
            self.play(formula.animate.move_to(np.array([0.0, 2.15, 0.0])),
                      run_time=0.9)

        hand_over = VGroup(
            Text("this scores a batch of numbers", font_size=BODY),
            Text("a representation is a vector",
                 font_size=BODY).set_color(MUTED),
            Text("in hundreds of dimensions",
                 font_size=BODY).set_color(TARGET),
        ).arrange(DOWN, buff=0.3)
        hand_over.move_to(np.array([0.0, -0.55, 0.0]))
        layout.fit_in_frame(hand_over)

        with self.voiceover(
            text="This score accepts a batch of scalars. A learned representation supplies vectors."
        ):
            self.play(lagged_map(FadeIn, hand_over, shift=0.18 * UP,
                                     lag_ratio=0.45), run_time=2.4)

        with self.voiceover(
            text="Chapter C extends the construction from one coordinate to a cloud in high dimension."
        ):
            self.wait(0.8)

        self.clear_beat()
