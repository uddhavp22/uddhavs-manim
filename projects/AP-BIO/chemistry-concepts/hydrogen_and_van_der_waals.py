"""Silent slide scene: hydrogen bonds and Van der Waals forces.

Render:
    ./render.sh projects/AP-BIO/chemistry-concepts/hydrogen_and_van_der_waals.py HydrogenAndVanDerWaals -ql
"""

import os
import sys

import numpy as np
from manim import Create, FadeIn, FadeOut, LEFT, RIGHT, UP, VGroup, smooth
from manim_slides import Slide

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.chem import atom, helix_ribbon, water_molecule, weak_force_line
from common.palette import MUTED
from common.type import caption, label, title


class HydrogenAndVanDerWaals(Slide):
    def construct(self):
        heading = title("Weak Intermolecular Forces").to_edge(UP, buff=0.6)
        self.play(FadeIn(heading, shift=0.2 * UP), run_time=0.6)
        self.wait(0.6)
        self.next_slide()

        # Two water molecules, close enough that one's hydrogen sits near
        # the other's oxygen -- the actual, recognizable case a "hydrogen
        # bond" refers to, not an abstract labelled dash.
        water_a = water_molecule(np.array([-3.0, 0.75, 0.0]), orientation=-0.15)
        water_b = water_molecule(np.array([0.55, 0.15, 0.0]), orientation=np.pi - 0.35)

        self.play(
            FadeIn(water_a, shift=0.3 * RIGHT),
            FadeIn(water_b, shift=0.3 * LEFT),
            run_time=0.6,
        )
        self.play(FadeIn(water_a.deltas), FadeIn(water_b.deltas), run_time=0.5)
        self.wait(1.0)

        hydrogen_contact = weak_force_line(water_a.h1, water_b.o, opacity=0.75)
        hydrogen_label = label("hydrogen bond").next_to(
            hydrogen_contact, -UP, buff=0.25
        )
        self.play(Create(hydrogen_contact), run_time=0.6)
        self.play(FadeIn(hydrogen_label), run_time=0.5)
        self.wait(1.6)
        self.next_slide()

        waters = VGroup(water_a, water_b, hydrogen_contact, hydrogen_label)
        self.play(waters.animate.scale(0.62).to_edge(LEFT, buff=0.9), run_time=0.9)
        self.wait(0.4)

        # The same weak-force idea, at the scale that actually matters
        # biologically: hydrogen bonds between turns of a coiled backbone
        # are what hold a protein's folded shape together.
        helix = helix_ribbon(center=np.array([1.6, 0.2, 0.0]))
        helix_caption = label("protein backbone, held coiled by\nhydrogen bonds between its turns").next_to(
            helix, RIGHT, buff=0.7
        )
        self.play(Create(helix.curve), run_time=1.2)
        self.play(FadeIn(helix.rungs), run_time=0.6)
        self.play(FadeIn(helix_caption), run_time=0.5)
        self.wait(1.8)
        self.next_slide()

        self.play(
            FadeOut(VGroup(waters, helix, helix_caption)),
            run_time=0.6,
        )

        # Van der Waals: even non-polar groups with no charge to speak of
        # still draw weakly together at close range -- fainter and less
        # specific than a hydrogen bond, which the lower line opacity here
        # is doing the work of showing rather than telling.
        left_group = atom("R", color=MUTED, radius=0.34).move_to(1.2 * LEFT)
        right_group = atom("R", color=MUTED, radius=0.34).move_to(1.2 * RIGHT)
        self.play(FadeIn(left_group, shift=0.2 * RIGHT), FadeIn(right_group, shift=0.2 * LEFT), run_time=0.5)
        self.play(
            left_group.animate.shift(0.35 * RIGHT),
            right_group.animate.shift(0.35 * LEFT),
            run_time=0.8,
            rate_func=smooth,
        )
        van_der_waals_contact = weak_force_line(left_group, right_group, opacity=0.3)
        van_der_waals_label = label("Van der Waals").next_to(
            VGroup(left_group, right_group), -UP, buff=0.3
        )
        self.play(Create(van_der_waals_contact), run_time=0.5)
        self.play(FadeIn(van_der_waals_label), run_time=0.4)
        self.wait(1.4)
        self.next_slide()

        explanation = caption(
            "Weak forces maintain the 3D shapes of large molecules like proteins and DNA."
        ).move_to(3.0 * -UP)
        self.play(FadeIn(explanation, shift=0.15 * UP), run_time=0.6)
        self.wait(2.5)
        self.next_slide()

        self.play(
            FadeOut(
                VGroup(
                    heading,
                    explanation,
                    left_group,
                    right_group,
                    van_der_waals_contact,
                    van_der_waals_label,
                )
            ),
            run_time=0.6,
        )
        self.wait(0.8)
