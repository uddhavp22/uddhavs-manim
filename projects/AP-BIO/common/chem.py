"""Reusable 2D chemistry primitives for the AP Biology scenes.

The returned groups expose their meaningful parts as attributes so scene files
can sequence the chemistry without rebuilding circles, electrons, badges, or
bond geometry inline.

Bonding is shown through valence electrons, not just a labelled line: a
`shell()` ring around an atom carries the electrons that actually move,
merge, or fill a gap, because that motion is the mechanism the caption names
-- "share", "transfer" -- not the line itself.
"""

from __future__ import annotations

import numpy as np
from manim import (
    PI,
    TAU,
    ArcBetweenPoints,
    Circle,
    DashedLine,
    Dot,
    Ellipse,
    Line,
    MathTex,
    ParametricFunction,
    VGroup,
)

from .palette import (
    ATOM_PARTNER,
    ATOM_PRIMARY,
    BACKBONE,
    BG,
    BOND_COVALENT,
    BOND_IONIC,
    BOND_WEAK,
    CHARGE_NEG,
    CHARGE_POS,
    DELTA_NEG,
    DELTA_POS,
    ELECTRON,
    INK,
    MUTED,
)

ATOM_RADIUS = 0.8


def _direction(start: np.ndarray, end: np.ndarray) -> np.ndarray:
    vector = end - start
    length = np.linalg.norm(vector)
    if length == 0:
        raise ValueError("Chemistry objects need distinct centers.")
    return vector / length


def _radius(atom_group: VGroup) -> float:
    return float(atom_group.atom_radius)


def _edge_points(
    first: VGroup, second: VGroup, buff: float = 0.04
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    first_center = first.get_center()
    second_center = second.get_center()
    direction = _direction(first_center, second_center)
    start = first_center + direction * (_radius(first) + buff)
    end = second_center - direction * (_radius(second) + buff)
    return start, end, direction


def atom(
    symbol: str,
    *,
    color: str = ATOM_PRIMARY,
    radius: float = ATOM_RADIUS,
    label_size: int = 31,
) -> VGroup:
    """Return a filled, labelled atom circle."""
    shell_disc = Circle(
        radius=radius,
        stroke_color=INK,
        stroke_width=2.4,
        fill_color=color,
        fill_opacity=0.9,
    )
    label = MathTex(
        rf"\mathrm{{{symbol}}}",
        font_size=label_size,
        color=BG,
    ).move_to(shell_disc)
    result = VGroup(shell_disc, label)
    result.shell = shell_disc
    result.label = label
    result.atom_radius = radius
    result.atom_color = color
    result.set_z_index(2)
    return result


def shell(
    atom_group: VGroup,
    *,
    filled: int,
    empty: int = 0,
    radius_multiplier: float = 1.75,
    color: str | None = None,
    start_angle: float = PI / 2,
) -> VGroup:
    """A valence-electron ring around an atom.

    `empty` slots are drawn as faint open rings marking unfilled octet
    positions, so a shell can visibly go from "gapped" to "full" instead of
    an electron count only being asserted in a caption.
    """
    center = atom_group.get_center()
    orbit_radius = _radius(atom_group) * radius_multiplier
    ring = Circle(
        radius=orbit_radius,
        stroke_color=MUTED,
        stroke_width=1.2,
        stroke_opacity=0.4,
    ).move_to(center)

    total = filled + empty
    angles = start_angle + np.linspace(0, TAU, total, endpoint=False)
    positions = [
        center + orbit_radius * np.array([np.cos(a), np.sin(a), 0.0])
        for a in angles
    ]
    electrons = VGroup(
        *[Dot(p, radius=0.09, color=color or ELECTRON) for p in positions[:filled]]
    )
    gaps = VGroup(
        *[
            Circle(radius=0.13, stroke_color=MUTED, stroke_width=1.6, stroke_opacity=0.6)
            .move_to(p)
            for p in positions[filled:]
        ]
    )
    result = VGroup(ring, electrons, gaps).set_z_index(3)
    result.ring = ring
    result.electrons = electrons
    result.gaps = gaps
    result.positions = positions
    result.orbit_radius = orbit_radius
    return result


def covalent_bond(
    first: VGroup, second: VGroup, *, first_electron: Dot, second_electron: Dot
) -> VGroup:
    """Bond geometry -- the line and the shared electron cloud -- for two
    atoms already at their bonded distance, built around the two specific
    electrons (one from each atom's own `shell()`) that are being shared.

    Deliberately takes the electrons as arguments rather than building
    fresh ones: a scene needs those exact objects on screen *before* the
    bond forms (each orbiting its own atom, to show separate ownership),
    then moved rather than replaced once it does -- an electron built fresh
    here instead of reusing the one the viewer has been watching would
    repeat the bug that once left a transferred electron behind in
    `ionic_bond`'s ion-pair animation.
    """
    start, end, direction = _edge_points(first, second)
    line = Line(start, end, color=BOND_COVALENT, stroke_width=6.5).set_z_index(0)

    midpoint = (first.get_center() + second.get_center()) / 2
    span = float(np.linalg.norm(second.get_center() - first.get_center()))
    angle = float(np.arctan2(direction[1], direction[0]))
    # The cloud is the actual content of this scene -- it has to read as a
    # solid, colored region the viewer can see, not a near-transparent
    # outline that only asserts a cloud is there. No stroke: a visible
    # stroke here would run parallel to `line` and misread as a second
    # bond (wrong for a single covalent bond like HCl).
    shared_orbit = Ellipse(
        width=span * 0.62,
        height=0.5,
        stroke_width=0,
        fill_color=BOND_COVALENT,
        fill_opacity=0.3,
    ).move_to(midpoint)
    shared_orbit.rotate(angle)

    shared_positions = (
        midpoint + (span * 0.3) * direction,
        midpoint - (span * 0.3) * direction,
    )
    electrons = VGroup(first_electron, second_electron).set_z_index(4)

    result = VGroup(line, shared_orbit)
    result.line = line
    result.shared_orbit = shared_orbit
    result.electrons = electrons
    result.shared_positions = shared_positions
    result.midpoint = midpoint
    return result


def _charge_badge(atom_group: VGroup, sign: str, color: str, side: float) -> VGroup:
    radius = 0.21
    badge_center = atom_group.get_center() + np.array(
        [side * 0.72 * _radius(atom_group), 0.78 * _radius(atom_group), 0.0]
    )
    disk = Circle(
        radius=radius,
        stroke_color=color,
        stroke_width=2.2,
        fill_color=BG,
        fill_opacity=1.0,
    ).move_to(badge_center)
    mark = MathTex(sign, font_size=26, color=color).move_to(disk)
    return VGroup(disk, mark).set_z_index(5)


def ionic_bond(donor: VGroup, acceptor: VGroup) -> VGroup:
    """A full octet transfer: the donor's one valence electron travels to
    the one open gap in the acceptor's seven-electron shell.

    This is the actual mechanism -- an unstable shell becoming stable on
    both sides -- rather than an arrow standing in for "something moved".
    """
    donor_shell = shell(donor, filled=1, color=donor.atom_color, start_angle=PI)
    acceptor_shell = shell(
        acceptor, filled=7, empty=1, color=acceptor.atom_color, start_angle=0.0
    )

    transfer_electron = donor_shell.electrons[0]
    gap = acceptor_shell.gaps[0]
    transfer_path = ArcBetweenPoints(
        donor_shell.positions[0], gap.get_center(), angle=-PI / 3
    )

    positive_badge = _charge_badge(donor, "+", CHARGE_POS, side=-1.0)
    negative_badge = _charge_badge(acceptor, "-", CHARGE_NEG, side=1.0)

    result = VGroup(donor_shell, acceptor_shell)
    result.donor_shell = donor_shell
    result.acceptor_shell = acceptor_shell
    result.transfer_electron = transfer_electron
    result.transfer_path = transfer_path
    result.gap = gap
    result.positive_badge = positive_badge
    result.negative_badge = negative_badge
    result.charges = VGroup(positive_badge, negative_badge)
    return result


def water_molecule(
    center: np.ndarray,
    *,
    scale: float = 1.0,
    orientation: float = PI / 2,
) -> VGroup:
    """A bent H2O molecule at the real ~104.5-degree H-O-H bond angle, with
    partial-charge labels -- the concrete, recognizable case of a polar
    covalent molecule that hydrogen bonds actually form between.
    """
    bond_angle = np.radians(104.5)
    half = bond_angle / 2
    h1_dir = np.array(
        [np.cos(orientation + half), np.sin(orientation + half), 0.0]
    )
    h2_dir = np.array(
        [np.cos(orientation - half), np.sin(orientation - half), 0.0]
    )
    away_dir = -(h1_dir + h2_dir)
    away_dir = away_dir / np.linalg.norm(away_dir)

    bond_length = 0.8 * scale
    o = atom("O", color=ATOM_PARTNER, radius=0.34 * scale, label_size=24).move_to(
        center
    )
    h1 = atom("H", color=ATOM_PRIMARY, radius=0.23 * scale, label_size=18).move_to(
        center + bond_length * h1_dir
    )
    h2 = atom("H", color=ATOM_PRIMARY, radius=0.23 * scale, label_size=18).move_to(
        center + bond_length * h2_dir
    )
    bond1 = Line(
        *_edge_points(o, h1, buff=0.02)[:2], color=BOND_COVALENT, stroke_width=3.5
    )
    bond2 = Line(
        *_edge_points(o, h2, buff=0.02)[:2], color=BOND_COVALENT, stroke_width=3.5
    )

    delta_neg = MathTex(r"\delta^-", font_size=18, color=DELTA_NEG).move_to(
        center + 0.62 * scale * away_dir
    )
    delta_pos_1 = MathTex(r"\delta^+", font_size=16, color=DELTA_POS).move_to(
        center + (bond_length + 0.3 * scale) * h1_dir
    )
    delta_pos_2 = MathTex(r"\delta^+", font_size=16, color=DELTA_POS).move_to(
        center + (bond_length + 0.3 * scale) * h2_dir
    )

    result = VGroup(bond1, bond2, o, h1, h2, delta_neg, delta_pos_1, delta_pos_2)
    result.o = o
    result.h1 = h1
    result.h2 = h2
    result.deltas = VGroup(delta_neg, delta_pos_1, delta_pos_2)
    result.bonds = VGroup(bond1, bond2)
    return result


def helix_ribbon(
    *,
    loops: int = 3,
    amplitude: float = 0.7,
    loop_height: float = 1.15,
    center: np.ndarray | None = None,
    color: str | None = None,
) -> VGroup:
    """A stylized coiled polypeptide backbone (a 2D projection of an alpha
    helix) with dashed rungs marking the hydrogen bonds that hold its turns
    together -- the "3D shape of a large molecule" the caption names,
    made of the same weak-force vocabulary as the water beat.

    Drawn as two offset strands (one bold, one faint) rather than a single
    thin line -- a lone sine curve reads as a generic squiggle, not a
    ribbon with any sense of coiled depth. The faint strand is the same
    curve shifted slightly along its own width, which is enough separation
    at this scale to read as "one folded ribbon" without becoming a literal
    3D ball-and-stick render (AP_BIO.md rules that out).
    """
    if center is None:
        center = np.zeros(3)
    total_height = loops * loop_height

    def point(t: float, offset: float = 0.0) -> np.ndarray:
        y = center[1] + total_height / 2 - t * loop_height
        x = center[0] + offset + amplitude * np.sin(t * TAU)
        return np.array([x, y, 0.0])

    strand_color = color or BACKBONE
    curve = ParametricFunction(
        point,
        t_range=[0, loops, 0.01],
        color=strand_color,
        stroke_width=8.0,
    )
    shadow_strand = ParametricFunction(
        lambda t: point(t, offset=0.16),
        t_range=[0, loops, 0.01],
        color=strand_color,
        stroke_width=3.0,
        stroke_opacity=0.35,
    )

    # Rungs connect matching phase one loop apart -- the i, i+4 hydrogen-bond
    # spacing that actually holds a real alpha helix's turns together.
    phase = 0.25
    rungs = VGroup(
        *[
            DashedLine(
                point(i + phase),
                point(i + 1 + phase),
                dash_length=0.1,
                color=BOND_WEAK,
                stroke_width=2.4,
                stroke_opacity=0.7,
            )
            for i in range(loops - 1)
        ]
    )

    result = VGroup(shadow_strand, curve, rungs)
    result.curve = VGroup(shadow_strand, curve)
    result.rungs = rungs
    return result


def weak_force_line(
    first: VGroup, second: VGroup, *, opacity: float = 0.58
) -> DashedLine:
    """A subdued dashed contact between pre-existing fragments."""
    start, end, _ = _edge_points(first, second, buff=0.07)
    return DashedLine(
        start,
        end,
        dash_length=0.13,
        dashed_ratio=0.52,
        color=BOND_WEAK,
        stroke_width=2.0,
        stroke_opacity=opacity,
    ).set_z_index(1)
