"""Silent slide scene: hydrogen bonds and Van der Waals forces.

Render:
    ./render.sh projects/AP-BIO/chemistry-concepts/hydrogen_and_van_der_waals.py HydrogenAndVanDerWaals -ql

Revised 2026-08-17 after review found the water/helix pairing pinned to the
left edge with the whole right half of the frame black for seconds at a
time -- the exact imbalance VISUAL_SYSTEM.md #5 calls out by name -- and the
Van der Waals beat reduced to two small pale dots alone in an otherwise
empty frame. See the note above `helix_ribbon()` and `weak_force_line()` in
`common/chem.py` for the companion fixes.
"""

import os
import sys

import numpy as np
from manim import (
    Create,
    FadeIn,
    FadeOut,
    LEFT,
    RIGHT,
    UP,
    VGroup,
    smooth,
    there_and_back,
)
from manim_slides import Slide

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.chem import atom, helix_ribbon, water_molecule, weak_force_line
from common.palette import MUTED
from common.type import caption, label, title

VDW_RADIUS = 0.55


class HydrogenAndVanDerWaals(Slide):
    def construct(self):
        heading = title("Weak Intermolecular Forces").to_edge(UP, buff=0.6)
        self.play(FadeIn(heading, shift=0.2 * UP), run_time=0.6)
        self.wait(0.4)
        self.next_slide()

        # Two water molecules, close enough that one's hydrogen sits near
        # the other's oxygen -- the actual, recognizable case a "hydrogen
        # bond" refers to, not an abstract labelled dash. Drawn at a scale
        # that reads with confidence, and centered on the frame rather than
        # huddled in the left half with the right half black (the exact
        # imbalance VISUAL_SYSTEM.md #5 names as the one real empty-space
        # defect).
        water_a = water_molecule(
            np.array([-1.7, 0.85, 0.0]), scale=1.25, orientation=-0.15
        )
        water_b = water_molecule(
            np.array([1.75, -0.05, 0.0]), scale=1.25, orientation=np.pi - 0.35
        )

        self.play(
            FadeIn(water_a, shift=0.3 * RIGHT),
            FadeIn(water_b, shift=0.3 * LEFT),
            run_time=0.6,
        )
        self.play(FadeIn(water_a.deltas), FadeIn(water_b.deltas), run_time=0.4)

        hydrogen_contact = weak_force_line(water_a.h1, water_b.o, opacity=0.8)
        hydrogen_label = label("hydrogen bond").next_to(
            hydrogen_contact, -UP, buff=0.25
        )
        self.play(Create(hydrogen_contact), run_time=0.5)
        self.play(FadeIn(hydrogen_label), run_time=0.4)
        self.wait(1.1)
        self.next_slide()

        waters = VGroup(water_a, water_b, hydrogen_contact, hydrogen_label)
        # The same weak-force idea, at the scale that actually matters
        # biologically: hydrogen bonds between turns of a coiled backbone
        # are what hold a protein's folded shape together. Sized and
        # positioned to carry equal visual weight to the water pair rather
        # than shrinking into a corner beside a much larger empty half.
        self.play(
            waters.animate.scale(0.82).to_edge(LEFT, buff=0.75),
            run_time=0.8,
        )

        helix = helix_ribbon(
            loops=4, amplitude=0.85, loop_height=1.0,
            center=np.array([3.1, 0.15, 0.0]),
        )
        helix_caption = label(
            "protein backbone, held coiled by\nhydrogen bonds between its turns"
        ).next_to(helix, -UP, buff=0.4)
        self.play(Create(helix.curve), run_time=1.0)
        self.play(FadeIn(helix.rungs), run_time=0.5)
        self.play(FadeIn(helix_caption), run_time=0.4)
        self.wait(1.3)
        self.next_slide()

        # Van der Waals: even non-polar groups with no charge to speak of
        # still draw weakly together at close range -- fainter and less
        # specific than a hydrogen bond, which the lower line opacity here
        # is doing the work of showing rather than telling. Sized big
        # enough to hold the frame on its own rather than reading as two
        # stray dots in a mostly-empty scene.
        left_group = atom(
            "R", color=MUTED, radius=VDW_RADIUS, label_size=22
        ).move_to(1.5 * LEFT)
        right_group = atom(
            "R", color=MUTED, radius=VDW_RADIUS, label_size=22
        ).move_to(1.5 * RIGHT)
        self.play(
            FadeOut(VGroup(waters, helix, helix_caption)),
            FadeIn(left_group, shift=0.2 * RIGHT),
            FadeIn(right_group, shift=0.2 * LEFT),
            run_time=0.6,
        )
        self.play(
            left_group.animate.shift(0.45 * RIGHT),
            right_group.animate.shift(0.45 * LEFT),
            run_time=0.7,
            rate_func=smooth,
        )
        van_der_waals_contact = weak_force_line(left_group, right_group, opacity=0.4)
        van_der_waals_label = label("Van der Waals").next_to(
            VGroup(left_group, right_group), -UP, buff=0.3
        )
        self.play(Create(van_der_waals_contact), run_time=0.5)
        self.play(FadeIn(van_der_waals_label), run_time=0.4)
        # A faint attraction still has a moment, not just a held still
        # frame -- the two groups drift a hair closer and back, echoing
        # the covalent-bond settle pulse without promoting this force to
        # the same visual weight.
        vdw_pair = VGroup(left_group, right_group)
        self.play(
            vdw_pair.animate.scale(1.06),
            rate_func=there_and_back,
            run_time=0.6,
        )
        self.wait(0.7)
        self.next_slide()

        explanation = caption(
            "Weak forces maintain the 3D shapes of large molecules like proteins and DNA."
        ).move_to(3.0 * -UP)
        self.play(FadeIn(explanation, shift=0.15 * UP), run_time=0.6)
        self.wait(2.2)
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
        self.wait(0.4)
