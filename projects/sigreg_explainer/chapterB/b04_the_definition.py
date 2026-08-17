"""Chapter B.4 — naming and defining the characteristic function.

The worked examples in b05 build three properties of one machine without ever
naming it, on purpose: NARRATION_SPEC.md says not to overuse delayed naming,
but the pairing argument in b03 exists precisely so the term is earned before
it is spent. This scene is that payoff -- recap what has been on screen as one
mechanism, name it, and write down the formula it has been computing the
whole time. b06 and b07 then use the name rather than re-explain the rig.

This scene follows the construction immediately. The definition is not saved
as a recap after several examples: it gives a name to the object the viewer has
just built, then the examples stress-test that named object.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b04_the_definition.py B04 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import layout
from common.beat import ActScene
from common.palette import TARGET
from common import type as ty
from common.rig import ThreePanelRig

T_MAX = 6.5
# The same watchable batch used to build the probe in B03.
SAMPLES = np.array([-1.95, -1.20, -0.70, -0.20, 0.30, 0.80, 1.80])


class B04(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.rig = ThreePanelRig(SAMPLES, t_max=T_MAX, line_range=(-3, 3, 1))
        self.rig.mount(self, trace_imag=True, rider_imag=True)
        self.name_beat()
        self.formula_beat()
        self.bridge_beat()

    # ------------------------------------------------------------------ 1
    def name_beat(self):
        """Sweep the whole rig once, over a sentence that recaps it as one
        mechanism rather than three separate panels."""
        r = self.rig
        name = ty.statement("the empirical characteristic function")
        name.move_to(np.array([0.0, 2.6, 0.0]))
        layout.fit_in_frame(name)

        with self.voiceover(
            text="To recap, we started with a batch of samples. "
                 "<bookmark mark='directions'/>For each t, every sample became "
                 "a direction, and those directions were averaged. "
                 "<bookmark mark='function'/>Let t vary, and the average "
                 "traces this function. <bookmark mark='name'/>This is the "
                 "empirical characteristic function."
        ) as tracker:
            self.play(
                Indicate(r.mounted_dots, color=TARGET, scale_factor=1.035),
                run_time=0.55,
            )
            self.wait_until_bookmark("directions")
            self.play(
                r.t.animate.set_value(1.6),
                Indicate(r.titles[1], color=TARGET, scale_factor=1.035),
                run_time=max(1.0, tracker.time_until_bookmark("function")),
                rate_func=smooth,
            )
            self.wait_until_bookmark("function")
            self.play(
                r.t.animate.set_value(T_MAX),
                Indicate(r.titles[2], color=TARGET, scale_factor=1.035),
                run_time=max(1.2, tracker.time_until_bookmark("name")),
                rate_func=linear,
            )
            self.wait_until_bookmark("name")
            self.play(Write(name), run_time=0.75)
            self.play(Indicate(name, color=TARGET, scale_factor=1.025),
                      run_time=0.5)

        self.name = name

    # ------------------------------------------------------------------ 2
    def formula_beat(self):
        formula = ty.maths(
            R"\hat\varphi_N(t) = \frac{1}{N}\sum_{j=1}^{N} e^{itx_j}",
            size=ty.EQ, color=TARGET,
            isolate=[R"\frac{1}{N}", R"\sum_{j=1}^{N}", R"e^{itx_j}"])
        formula.move_to(np.array([0.0, -2.85, 0.0]))
        layout.fit_in_frame(formula)

        with self.voiceover(
            text="For the batch we actually have, each sample contributes "
                 "<bookmark mark='wrap'/>e to the i t x. "
                 "<bookmark mark='add'/>Adding those arrows and "
                 "<bookmark mark='divide'/>dividing by the batch size gives "
                 "their empirical average."
        ) as tracker:
            self.play(Write(formula), run_time=0.85)
            self.wait_until_bookmark("wrap")
            self.play(
                Indicate(formula.get_part_by_tex(R"e^{itx_j}"),
                         scale_factor=1.05, color=TARGET),
                run_time=0.5,
            )
            self.wait_until_bookmark("add")
            self.play(
                Indicate(formula.get_part_by_tex(R"\sum_{j=1}^{N}"),
                         scale_factor=1.05, color=TARGET),
                run_time=0.5,
            )
            self.wait_until_bookmark("divide")
            self.play(
                Indicate(formula.get_part_by_tex(R"\frac{1}{N}"),
                         scale_factor=1.05, color=TARGET),
                run_time=0.5,
            )

        # The formula just landed. A moment with nothing said over it, to
        # actually read it.
        self.inspect(1.4)
        self.formula = formula

    # ------------------------------------------------------------------ 3
    def bridge_beat(self):
        population = ty.maths(
            R"\varphi_X(t)=\mathbb E\!\left[e^{itX}\right]",
            size=ty.EQ, color=TARGET,
        )
        empirical_target = self.formula.copy().scale(0.84)
        empirical_target.move_to(np.array([-3.35, -3.05, 0.0]))
        population.scale(0.84)
        population.move_to(np.array([3.35, -3.05, 0.0]))
        layout.fit_in_frame(empirical_target)
        layout.fit_in_frame(population)

        with self.voiceover(
            text="If we knew the full distribution, the same operation would "
                 "be an expectation. <bookmark mark='samples'/>We only have "
                 "samples, so the finite average estimates that population "
                 "function; <bookmark mark='hat'/>the hat keeps the two "
                 "quantities distinct."
        ) as tracker:
            self.play(
                Transform(self.formula, empirical_target),
                FadeIn(population, shift=0.18 * RIGHT),
                run_time=0.75,
            )
            self.play(Indicate(population, scale_factor=1.04,
                               color=TARGET), run_time=0.55)
            self.wait_until_bookmark("samples")
            self.play(Indicate(self.formula, scale_factor=1.04,
                               color=TARGET), run_time=0.55)
            self.wait_until_bookmark("hat")
            self.play(Indicate(VGroup(self.formula, population),
                               scale_factor=1.025, color=TARGET),
                      run_time=0.55)
        self.clear_beat()
