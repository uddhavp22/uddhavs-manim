"""Chapter B.9 — why the entire characteristic-function curve is enough.

One value of the characteristic function is only one average arrow. The
uniqueness theorem is the precise statement that the collection of values, for
every frequency, determines the distribution. Its proof is intentionally not
part of this chapter; the theorem is used to motivate a loss on the curve.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import layout
from common.beat import ActScene
from common.palette import COLLAPSE, EMPIRICAL, FAINT, MUTED, TARGET
from common.type import BODY, LABEL, STATEMENT, Text
from common import type as ty


class B09(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        title = ty.words("at one t: one average arrow", size=STATEMENT)
        title.set_color(MUTED).to_edge(UP, buff=0.7)

        ts = [-2.4, -1.2, 0.0, 1.2, 2.4]
        samples = VGroup(*(
            VGroup(
                Dot(np.array([t, 0.55, 0.0]), radius=0.075).set_fill(EMPIRICAL, 1),
                ty.line("at", "$t=%+.1f$" % t, size=LABEL).set_color(MUTED),
            ).arrange(DOWN, buff=0.16)
            for t in ts
        ))
        line = Line(np.array([-3.3, 0.55, 0]), np.array([3.3, 0.55, 0]))
        line.set_stroke(FAINT, 2)
        samples.move_to(np.array([0.0, 0.15, 0.0]))

        curve = VGroup(
            ty.words("all t: one curve", size=STATEMENT).set_color(TARGET),
            ty.line("the characteristic function", size=BODY).set_color(MUTED),
        ).arrange(DOWN, buff=0.22)
        curve.move_to(np.array([0.0, -1.8, 0.0]))

        with self.voiceover(
            text="At one frequency, the average arrow is only one number. Changing the frequency gives a different number from the same distribution."
        ):
            self.play(FadeIn(title), Create(line), run_time=0.9)
            self.play(lagged_map(FadeIn, samples, shift=0.12 * UP,
                                     lag_ratio=0.18), run_time=1.7)

        with self.voiceover(
            text="Taken together, those answers make the characteristic-function curve. A theorem says the entire curve determines the distribution."
        ):
            self.play(samples.animate.shift(0.55 * UP), run_time=0.8)
            self.play(FadeIn(curve, shift=0.2 * UP), run_time=1.0)

        theorem = MathTex(R"\varphi_X(t)=\varphi_Y(t)\ \text{for every }t"
                      R"\quad\Longrightarrow\quad X\overset{d}{=}Y",
                      font_size=42).set_color(TARGET)
        theorem.move_to(np.array([0.0, -0.05, 0.0]))
        box = SurroundingRectangle(theorem, buff=0.28).set_stroke(TARGET, 2)
        name = Text("uniqueness theorem", font_size=LABEL).set_color(MUTED)
        name.next_to(box, DOWN, buff=0.26)
        layout.fit_in_frame(VGroup(theorem, name))

        with self.voiceover(
            text="If two characteristic functions agree for every frequency, then the distributions agree. The proof uses an inversion formula; we will use the result."
        ):
            self.play(FadeOut(VGroup(title, line, samples, curve)),
                      Write(theorem), run_time=1.7)
            self.play(Create(box), FadeIn(name), run_time=0.8)

        bridge = VGroup(
            ty.words("complete curve", size=BODY).set_color(TARGET),
            ty.words("finite-batch estimate", size=BODY).set_color(COLLAPSE),
        ).arrange(DOWN, buff=0.28)
        bridge.to_edge(DOWN, buff=0.65)
        with self.voiceover(
            text="A batch only estimates this curve, and the estimate is not equally reliable at every frequency."
        ):
            self.play(FadeIn(bridge, shift=0.16 * UP), run_time=1.0)
            self.wait(0.4)
        self.clear_beat()
