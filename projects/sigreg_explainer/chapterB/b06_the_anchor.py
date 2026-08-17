"""Chapter B.6 — the universal anchor of every characteristic function.

This scene owns one discovery: at zero frequency every sample produces the
same unit direction, so every characteristic-function curve passes through
one. The opening-distribution comparison belongs to B09, where it creates the
question of which frequencies are informative.
"""

import os
import sys

from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.palette import TARGET
from common import type as ty
from common.rig import ThreePanelRig


class B06(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        rig = ThreePanelRig(data.gaussian_1d(12), t_max=6.5,
                            line_range=(-3, 3, 1))
        rig.mount(self, dot_radius=0.06, stack_dots=True)
        rig.t.set_value(1.6)

        steps = VGroup(
            ty.maths(R"t = 0", size=ty.EQ),
            ty.line(R"$t x = 0$", "for every", "$x$", size=ty.EQ),
            ty.maths(R"e^{i\cdot0}=1", size=ty.EQ),
        ).arrange(DOWN, buff=0.26)
        steps.move_to([0.0, -3.05, 0.0])
        steps[2].set_color(TARGET)
        layout.fit_in_frame(steps)

        with self.voiceover(
            text="Before looking at any particular shape, there is one point we "
                 "can predict: when the frequency is zero, every sample lands at "
                 "angle zero."
        ) as tracker:
            self.play(FadeIn(steps[0]), rig.t.animate.set_value(0.0),
                      run_time=1.6)
            self.play(FadeIn(steps[1]), FadeIn(steps[2]), run_time=0.9)
            self.across(tracker, rig.t.animate.set_value(0.45), floor=0.9,
                        rate_func=there_and_back)

        result = ty.maths(R"\varphi(0)=1", size=ty.EQ_HERO, color=TARGET)
        result.move_to([0.0, -3.05, 0.0])
        with self.voiceover(
            text="The arrows stack at one, so phi of zero is one. "
                 "<bookmark mark='note'/>Every characteristic function "
                 "passes through this exact point, so zero can never tell "
                 "two batches apart."
        ) as tracker:
            self.play(FadeOut(steps), run_time=0.5)
            self.play(Write(result),
                      run_time=max(0.8, tracker.time_until_bookmark("note")))
            self.wait_until_bookmark("note")
            rig.swap(self, data.bimodal_1d(12))
            self.across(tracker, Indicate(result, scale_factor=1.06,
                                           color=TARGET), floor=1.0)

        self.inspect(1.0)
        self.clear_beat()
