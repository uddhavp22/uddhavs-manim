"""Silent slide scene: covalent bonds.

Render:
    ./render.sh projects/AP-BIO/chemistry-concepts/covalent_bonds.py CovalentBonds

Revised 2026-08-10 after a first pass was critiqued as visually thin even
after adding shells and an orbit: the only real motion happened before the
bond formed, and the moment the caption actually names -- the shared pair --
was a static freeze-frame for most of the scene, with a "pulse" meant to
suggest ongoing sharing that measured out to a 2-frame flicker on the
rendered video. See the note above `covalent_bond()` in `common/chem.py` and
the "Visual vocabulary" revision in `AP_BIO.md` dated the same day.
"""

import os
import sys

from manim import (
    PI,
    TAU,
    Create,
    FadeIn,
    FadeOut,
    LEFT,
    RIGHT,
    Rotating,
    UP,
    ValueTracker,
    VGroup,
)
from manim_slides import Slide

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.chem import atom, covalent_bond, shell
from common.palette import ATOM_PARTNER, ATOM_PRIMARY
from common.type import caption, label, title


class CovalentBonds(Slide):
    def construct(self):
        heading = title("Covalent Bond").to_edge(UP, buff=0.6)
        self.play(FadeIn(heading, shift=0.2 * UP), run_time=0.6)
        self.wait(0.8)
        self.next_slide()

        first = atom("H", color=ATOM_PRIMARY).move_to(3.0 * LEFT + 0.4 * UP)
        second = atom("Cl", color=ATOM_PARTNER).move_to(3.0 * RIGHT + 0.4 * UP)
        # Chlorine really does carry seven valence electrons -- the same
        # count IonicBonds draws for it. Only one of them, the one facing
        # hydrogen, ends up in the bond; the other six stay put as three
        # lone pairs, which is also chemically real and worth being able to
        # see stay behind.
        first_shell = shell(first, filled=1, color=first.atom_color, start_angle=PI)
        second_shell = shell(
            second, filled=7, color=second.atom_color, start_angle=0.0
        )

        self.play(
            FadeIn(first, shift=0.35 * RIGHT), FadeIn(second, shift=0.35 * LEFT),
            run_time=0.6,
        )
        self.play(
            FadeIn(first_shell.ring), FadeIn(first_shell.electrons),
            FadeIn(second_shell.ring), FadeIn(second_shell.electrons),
            run_time=0.6,
        )
        # Each atom's own electrons circle its own nucleus -- separate
        # ownership, established before anything is shared.
        self.play(
            Rotating(
                first_shell.electrons, TAU, about_point=first.get_center(),
                run_time=1.8,
            ),
            Rotating(
                second_shell.electrons, TAU, about_point=second.get_center(),
                run_time=1.8,
            ),
        )
        self.wait(0.3)
        self.next_slide()

        # Bonding is an attraction, not a line appearing between two fixed
        # points -- the atoms actually move.
        first_group = VGroup(first, first_shell)
        second_group = VGroup(second, second_shell)
        self.play(
            first_group.animate.shift(1.5 * RIGHT),
            second_group.animate.shift(1.5 * LEFT),
            run_time=1.2,
        )
        self.wait(0.3)
        self.next_slide()

        bond = covalent_bond(
            first,
            second,
            first_electron=first_shell.electrons[0],
            second_electron=second_shell.electrons[0],
        )
        self.play(
            bond.electrons[0].animate.move_to(bond.shared_positions[0]),
            bond.electrons[1].animate.move_to(bond.shared_positions[1]),
            FadeOut(first_shell.ring),
            run_time=1.2,
        )
        self.play(Create(bond.line), FadeIn(bond.shared_orbit), run_time=1.0)
        self.wait(0.4)

        # The shared pair actually keeps moving, along the ellipse's own
        # boundary via point_from_proportion -- not a rigid rotation about
        # its center, which would swing the electrons outside the ellipse's
        # flat shape (that mismatch is what forced the pulse-only version
        # this replaces). This keeps running for as long as the caption is
        # on screen, since that is the moment it needs to be visible.
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.3))
        self.add(phase)

        def orbiter(offset: float):
            def updater(mob):
                alpha = (phase.get_value() + offset) % 1.0
                mob.move_to(bond.shared_orbit.point_from_proportion(alpha))

            return updater

        bond.electrons[0].add_updater(orbiter(0.0))
        bond.electrons[1].add_updater(orbiter(0.5))

        formula = label("hydrogen chloride, HCl").next_to(
            VGroup(first, second), -UP, buff=0.55
        )
        self.play(FadeIn(formula), run_time=0.5)
        self.wait(1.2)
        self.next_slide()

        explanation = caption(
            "Atoms share pairs of electrons to form strong links inside molecules."
        ).move_to(2.9 * -UP)
        self.play(FadeIn(explanation, shift=0.15 * UP), run_time=0.6)
        self.wait(3.0)
        self.next_slide()

        bond.electrons[0].clear_updaters()
        bond.electrons[1].clear_updaters()
        phase.clear_updaters()
        self.play(FadeOut(VGroup(heading, explanation, formula)), run_time=0.6)
        self.play(
            FadeOut(
                VGroup(
                    first, second, second_shell.ring, second_shell.electrons,
                    bond.line, bond.shared_orbit, bond.electrons,
                )
            ),
            run_time=0.6,
        )
        self.wait(0.6)
