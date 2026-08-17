"""Silent slide scene: ionic bonds.

Render:
    ./render.sh projects/AP-BIO/chemistry-concepts/ionic_bonds.py IonicBonds -ql
"""

import os
import sys

from manim import (
    FadeIn,
    FadeOut,
    LEFT,
    MoveAlongPath,
    RIGHT,
    UP,
    VGroup,
    smooth,
)
from manim_slides import Slide

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.chem import atom, ionic_bond
from common.palette import ATOM_PARTNER, ATOM_PRIMARY, BOND_IONIC, ELECTRON
from common.type import caption, label, title


class IonicBonds(Slide):
    def construct(self):
        heading = title("Ionic Bond").to_edge(UP, buff=0.6)
        self.play(FadeIn(heading, shift=0.2 * UP), run_time=0.6)
        self.wait(0.8)
        self.next_slide()

        donor = atom("Na", color=ATOM_PARTNER).move_to(3.1 * LEFT + 0.3 * UP)
        acceptor = atom("Cl", color=ATOM_PRIMARY).move_to(3.1 * RIGHT + 0.3 * UP)
        transfer = ionic_bond(donor, acceptor)

        self.play(
            FadeIn(donor, shift=0.35 * RIGHT),
            FadeIn(acceptor, shift=0.35 * LEFT),
            run_time=0.6,
        )
        self.play(
            FadeIn(transfer.donor_shell.ring),
            FadeIn(transfer.donor_shell.electrons),
            FadeIn(transfer.acceptor_shell.ring),
            FadeIn(transfer.acceptor_shell.electrons),
            FadeIn(transfer.acceptor_shell.gaps),
            run_time=0.6,
        )
        # Sodium has one electron it doesn't need to keep; chlorine's shell
        # is one electron short of a full outer shell -- the gap is drawn
        # in, not just implied, so filling it is a visible event.
        self.wait(1.6)
        self.next_slide()

        self.play(
            MoveAlongPath(transfer.transfer_electron, transfer.transfer_path),
            run_time=1.2,
            rate_func=smooth,
        )
        # The gap closes: the electron that just arrived IS the eighth
        # electron now, not a stand-in for it -- recolour it in place
        # rather than swap in a new dot, so the object every later group
        # and animation refers to is the one that actually made the trip.
        self.play(
            FadeOut(transfer.gap),
            transfer.transfer_electron.animate.set_color(ELECTRON),
            transfer.acceptor_shell.ring.animate.set_stroke(
                color=BOND_IONIC, opacity=0.85
            ),
            run_time=0.5,
        )
        # Sodium's outer shell is empty now -- it doesn't get to keep the
        # ring it just gave away, and a cation really is smaller than the
        # neutral atom it came from.
        self.play(
            FadeOut(transfer.donor_shell.ring),
            donor.animate.scale(0.82),
            run_time=0.6,
        )
        self.wait(0.6)
        self.next_slide()

        self.play(FadeIn(transfer.charges), run_time=0.5)
        self.wait(1.0)

        acceptor_electrons = VGroup(
            transfer.acceptor_shell.electrons, transfer.transfer_electron
        )
        donor_ion = VGroup(donor, transfer.positive_badge)
        acceptor_ion = VGroup(
            acceptor, transfer.negative_badge, acceptor_electrons,
            transfer.acceptor_shell.ring,
        )
        self.play(
            donor_ion.animate.shift(1.1 * RIGHT),
            acceptor_ion.animate.shift(1.1 * LEFT),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(1.4)
        self.next_slide()

        formula = label("sodium chloride, NaCl").next_to(
            VGroup(donor_ion, acceptor_ion), -UP, buff=0.6
        )
        self.play(FadeIn(formula), run_time=0.5)
        self.wait(1.0)

        explanation = caption(
            "Charged ions attract each other after an electron transfer."
        ).move_to(3.0 * -UP)
        self.play(FadeIn(explanation, shift=0.15 * UP), run_time=0.6)
        self.wait(2.5)
        self.next_slide()

        self.play(FadeOut(VGroup(heading, explanation, formula)), run_time=0.6)
        self.play(
            FadeOut(VGroup(donor_ion, acceptor_ion)),
            run_time=0.6,
        )
        self.wait(0.8)
