"""Chapter B.11 — the standard Gaussian target curve.

The derivation of this characteristic function is deliberately omitted here:
the argument needs a target curve, not a detour through integration by parts.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import layout
from common.beat import ActScene
from common.palette import MUTED, TARGET
from common.type import BODY, LABEL, Text
from common import type as ty


class B11(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        with self.voiceover(
            text="A standard Gaussian produces a fixed characteristic-function curve. That curve is the reference for the batch."
        ):
            self.open_act("The Gaussian fingerprint")

        formula = MathTex(R"\varphi_0(t)=e^{-t^2/2}", font_size=62).set_color(TARGET)
        formula.to_edge(UP, buff=1.0)
        tag = Text("standard Gaussian", font_size=LABEL).set_color(MUTED)
        tag.next_to(formula, DOWN, buff=0.25)
        axes = layout.cf_axes()
        axes.move_to(np.array([0.0, -0.65, 0.0]))
        curve = axes.plot(lambda t: float(np.exp(-t * t / 2)),
                               x_range=(0, layout.CF_T_MAX))
        curve.set_stroke(TARGET, 4)
        zero = Dot(axes.c2p(0, 1), radius=0.075).set_fill(TARGET, 1)
        origin = ty.line("starts at", "$1$", size=LABEL).set_color(MUTED)
        origin.next_to(zero, UL, buff=0.12)
        caption = VGroup(
            ty.words("the target curve", size=BODY).set_color(TARGET),
            ty.line("same frequency in, expected average arrow out", size=LABEL).set_color(MUTED),
        ).arrange(DOWN, buff=0.16)
        caption.to_edge(DOWN, buff=0.45)

        with self.voiceover(
            text="For a standard Gaussian, the characteristic function is e to the minus t squared over two. It starts at one, is real and symmetric, and falls smoothly toward zero as wrapping becomes faster."
        ):
            self.play(Write(formula), FadeIn(tag), run_time=1.4)
            self.play(Create(axes), Create(curve), FadeIn(zero),
                      FadeIn(origin), run_time=2.0)

        with self.voiceover(
            text="The batch curve can be compared with this one at each frequency. For training, that comparison must move smoothly when a sample moves."
        ):
            self.play(FadeIn(caption, shift=0.15 * UP), run_time=1.0)
            self.wait(0.6)
        self.clear_beat()
