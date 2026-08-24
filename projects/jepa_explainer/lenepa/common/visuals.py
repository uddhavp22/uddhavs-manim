"""Reusable LeNEPA visual objects.

The grammar is adapted to Manim CE from the reference code in
``3blue1brown_videos/_2017/nn/part1.py`` and
``3blue1brown_videos/_2024/transformers/{helpers,mlp,network_flow}.py``:
explicit vector columns, edges behind nodes, one highlighted vector before a
parallel reveal, and transformations that preserve an object's identity.
"""

from __future__ import annotations

import itertools as it

import numpy as np
from manim import (
    Arrow,
    Circle,
    DecimalNumber,
    DashedLine,
    Dot,
    Line,
    MathTex,
    Rectangle,
    RoundedRectangle,
    VGroup,
    DOWN,
    LEFT,
    RIGHT,
    UP,
)

from . import type as ty
from .palette import AXIS, GRID, INK, MUTED


class LayerMap(VGroup):
    """A visible two-layer node/edge map, ported from 3b1b's network primitives.

    ``NetworkMobject`` (2017) keeps neuron layers separate from edge groups,
    stores incoming/outgoing edges on every neuron, and draws the edges behind
    the neurons.  ``NeuralNetwork`` (2024) uses the same layer/product layout
    for compact transformer-era diagrams.  This CE version preserves those
    mechanics while representing any single learned map between two node
    counts: every shown input node connects to every shown output node.  It
    was first written for one strided-convolution window (patch encoder,
    scene 1) and is reused as-is for the projector (scene 3) -- the input and
    output node counts *are* the dimensions being mapped, whatever the map.
    """

    def __init__(
        self,
        *,
        input_size: int = 8,
        output_size: int = 7,
        color: str,
        neuron_radius: float = 0.075,
        layer_buff: float = 2.15,
    ) -> None:
        self.neuron_radius = neuron_radius
        self.encoder_color = color

        layers = VGroup()
        for size in (input_size, output_size):
            neurons = VGroup(*(
                Circle(radius=neuron_radius)
                .set_stroke(color, 1.7, opacity=0.9)
                .set_fill(color, opacity=0.08)
                for _ in range(size)
            ))
            neurons.arrange(DOWN, buff=0.105)
            for neuron in neurons:
                neuron.edges_in = VGroup()
                neuron.edges_out = VGroup()
            layers.add(neurons)
        layers.arrange(RIGHT, buff=layer_buff)

        edges = VGroup()
        for source, target in it.product(layers[0], layers[1]):
            edge = Line(
                source.get_center(),
                target.get_center(),
                buff=neuron_radius,
            ).set_stroke(color, 0.75, opacity=0.20)
            source.edges_out.add(edge)
            target.edges_in.add(edge)
            edges.add(edge)

        super().__init__(edges, layers)
        self.edges = edges
        self.layers = layers
        self.input_layer = layers[0]
        self.output_layer = layers[1]

    def set_layer_values(self, layer_index: int, values) -> "LayerMap":
        """Fill neurons by activation magnitude, as in ``NetworkMobject``."""
        values = np.asarray(values, dtype=float)
        scale = max(float(np.max(np.abs(values))), 1e-8)
        for value, neuron in zip(values, self.layers[layer_index]):
            opacity = 0.12 + 0.76 * abs(float(value)) / scale
            neuron.set_fill(self.encoder_color, opacity=opacity)
        return self

    def propagation_copy(self, *, color: str) -> VGroup:
        """Return the bright edge group used for a passing activation flash."""
        return self.edges.copy().set_stroke(color, 2.8, opacity=0.95)


def numeric_embedding(
    values: np.ndarray | list[float],
    *,
    color: str,
    label: str | None = None,
    height: float | None = 1.55,
    abbreviate: bool = True,
    shown: int = 5,
) -> VGroup:
    """A bracketed vector in the spirit of ``NumericEmbedding``.

    The compact form uses an ellipsis for a D-dimensional embedding; the
    close-up form (``abbreviate=False``) keeps every displayed coordinate.
    Explicit signed coordinates make the encoder output read as a vector, not
    as a decorative stack of boxes.

    ``shown`` picks how many rows the abbreviated form draws: 5 is the
    default ``(v0, v1, ..., v-2, v-1)``; 3 gives ``(v0, ..., v-1)`` for a
    column whose true dimensionality is stylized down further (e.g. scene 3's
    projected vectors) but must still read as abbreviated, not as a literal
    low-dimensional vector -- dropping the ellipsis would misread as exactly
    that.  Only 3 and 5 are implemented; other values raise.

    ``height=None`` skips the final ``set_height`` call, so a caller can build
    a column at its natural glyph size and then match another column's glyph
    scale exactly, e.g.::

        proj.scale(src.entries[0].height / proj.entries[0].height)
    """
    values = np.asarray(values, dtype=float)
    if abbreviate:
        if shown == 5:
            entry_values = (values[0], values[1], None, values[-2], values[-1])
        elif shown == 3:
            entry_values = (values[0], None, values[-1])
        else:
            raise ValueError(f"numeric_embedding: unsupported shown={shown!r}")
    else:
        entry_values = tuple(values)
    entries = VGroup()
    for value in entry_values:
        if value is None:
            entry = MathTex(r"\vdots", font_size=ty.LABEL, color=color)
        else:
            entry = DecimalNumber(
                float(value),
                num_decimal_places=1,
                include_sign=True,
                font_size=ty.LABEL,
                color=color,
            )
        entries.add(entry)
    entries.arrange(DOWN, buff=0.075)

    pad = 0.12
    tick = 0.12
    left_x = entries.get_left()[0] - pad
    right_x = entries.get_right()[0] + pad
    top_y = entries.get_top()[1] + 0.06
    bottom_y = entries.get_bottom()[1] - 0.06
    left_bracket = VGroup(
        Line([left_x + tick, top_y, 0], [left_x, top_y, 0]),
        Line([left_x, top_y, 0], [left_x, bottom_y, 0]),
        Line([left_x, bottom_y, 0], [left_x + tick, bottom_y, 0]),
    ).set_stroke(color, 1.8)
    right_bracket = VGroup(
        Line([right_x - tick, top_y, 0], [right_x, top_y, 0]),
        Line([right_x, top_y, 0], [right_x, bottom_y, 0]),
        Line([right_x, bottom_y, 0], [right_x - tick, bottom_y, 0]),
    ).set_stroke(color, 1.8)
    brackets = VGroup(left_bracket, right_bracket)
    vector = VGroup(entries, brackets)
    if height is not None:
        vector.set_height(height)

    group = VGroup(vector)
    group.entries = entries
    group.brackets = brackets
    group.vector = vector
    # ``.vector`` and ``.label`` are separate submobjects (the label is not
    # inside the bracket group), so callers that only want the numeric column
    # -- e.g. a copy that travels through ``transformer_block`` -- must use
    # ``.vector`` explicitly.  Any value animated afterwards via
    # ``ChangeDecimalToValue`` must stay inside the open interval
    # ``(-0.95, 0.95)``: CE's ``DecimalNumber.set_value`` zips old/new
    # submobjects for ``match_style``, and a glyph-count change mid-animation
    # (crossing from one digit to two, or gaining/losing a sign) desyncs
    # styling and shifts layout.  Clip or generate animated target values to
    # that band.
    if label:
        label_mob = ty.maths(label, size=ty.LABEL, color=color)
        label_mob.next_to(vector, DOWN, buff=0.14)
        group.add(label_mob)
        group.label = label_mob
    return group


def latent_column(
    values: np.ndarray | list[float] | None = None,
    *,
    color: str,
    label: str | None = None,
    height: float = 1.85,
    width: float = 0.46,
) -> VGroup:
    """A compact embedding column with stable cells and mathematical label."""
    if values is None:
        values = np.array([0.25, 0.72, -0.35, 0.92, -0.58, 0.42, -0.12])
    values = np.asarray(values, dtype=float)
    cells = VGroup()
    cell_height = height / len(values)
    for value in values:
        cell = Rectangle(width=width, height=cell_height * 0.88)
        cell.set_stroke(color, 1.4, opacity=0.95)
        cell.set_fill(color, opacity=0.18 + 0.62 * min(1.0, abs(float(value))))
        cells.add(cell)
    cells.arrange(DOWN, buff=cell_height * 0.12)

    bracket_left = VGroup(
        Line(0.12 * RIGHT, 0.12 * LEFT),
        Line(0.12 * LEFT, height * 0.5 * DOWN + 0.12 * LEFT),
        Line(height * 0.5 * DOWN + 0.12 * LEFT,
             height * 0.5 * DOWN + 0.12 * RIGHT),
    ).set_stroke(color, 1.8)
    bracket_left.move_to(cells.get_left() + 0.07 * LEFT, aligned_edge=UP)
    bracket_left.set_height(cells.height)
    bracket_right = bracket_left.copy().flip(RIGHT)
    bracket_right.move_to(cells.get_right() + 0.07 * RIGHT)
    group = VGroup(cells, bracket_left, bracket_right)
    group.cells = cells
    if label:
        label_mob = ty.maths(label, size=ty.LABEL, color=color)
        label_mob.next_to(group, DOWN, buff=0.16)
        group.add(label_mob)
        group.label = label_mob
    return group


def latent_row(
    labels: list[str],
    *,
    color: str,
    height: float = 1.5,
    buff: float = 0.52,
    seed: int = 7,
) -> VGroup:
    rng = np.random.default_rng(seed)
    row = VGroup(*(
        latent_column(rng.normal(size=7), color=color, label=label, height=height)
        for label in labels
    ))
    row.arrange(RIGHT, buff=buff, aligned_edge=UP)
    return row


def transformer_block(*, width: float, height: float, color: str,
                      label: str = "causal Transformer",
                      label_side=RIGHT) -> VGroup:
    """A chamber that token embeddings visibly enter, mix, and exit.

    The earlier ``transformer_stack`` drew a low-contrast depth band that
    tokens vanished into and reappeared from -- a fine stand-in for "some
    computation happened," but not for causal mixing.  This chamber is built
    *open* (stroke only, fill opacity 0) from the start, so its interior stays
    legible for the whole beat: the calling scene animates ``.shell``'s fill
    opacity directly for open/close beats.  There is exactly one caller, so
    no ``open()``/``close()`` method pair is provided.
    """
    shell = RoundedRectangle(width=width, height=height, corner_radius=0.14)
    shell.set_stroke(color, 1.6, opacity=0.45)
    shell.set_fill(color, opacity=0.0)

    # Laminations sit near the top/bottom interior edges only.  The interior
    # center must stay completely clear -- that is where the token columns
    # descend and where the causal arcs arc between them.
    inset = 0.20
    half_span = 0.5 * width - 0.34
    top_y = 0.5 * height - inset
    bottom_y = -0.5 * height + inset
    laminations = VGroup(
        Line([-half_span, top_y, 0.0], [half_span, top_y, 0.0]),
        Line([-half_span, bottom_y, 0.0], [half_span, bottom_y, 0.0]),
    ).set_stroke(color, 1.2, opacity=0.12)

    depth_glyph = MathTex(r"\vdots", font_size=ty.LABEL, color=color)
    depth_glyph.set_opacity(0.5)
    depth_glyph.move_to(np.array([0.5 * width - 0.30, bottom_y + 0.30, 0.0]))

    title = ty.words(label, size=ty.LABEL, color=MUTED)

    group = VGroup(shell, laminations, depth_glyph, title)
    title.next_to(shell, label_side, buff=0.40)

    group.shell = shell
    group.laminations = laminations
    group.depth_glyph = depth_glyph
    group.label = title
    return group


def depth_plates(block: VGroup, *, count: int = 9, color: str) -> VGroup:
    """Faint horizontal lines filling a ``transformer_block``'s interior.

    Unfolds ``block``'s single ``\\vdots`` ``depth_glyph`` into ``count``
    evenly spaced plates, index 0 topmost -- this scene's flow runs top to
    bottom (matching scene 2), so depth increases downward.  Pure geometry;
    does not touch or replace ``depth_glyph`` itself.
    """
    shell = block.shell
    inset = 0.20
    half_span = 0.5 * shell.width - 0.34
    top_y = shell.get_top()[1] - inset
    bottom_y = shell.get_bottom()[1] + inset
    center_x = shell.get_x()
    ys = np.linspace(top_y, bottom_y, count)
    return VGroup(*(
        Line(
            [center_x - half_span, y, 0.0], [center_x + half_span, y, 0.0],
        ).set_stroke(color, 1.2, opacity=0.16)
        for y in ys
    ))


def decimal_entries(mob) -> VGroup:
    """Every ``DecimalNumber`` in ``mob``'s family, in document order."""
    return VGroup(*(
        entry for entry in mob.get_family() if isinstance(entry, DecimalNumber)
    ))


def span_bracket(mob, *, color: str, label: str | tuple[str, ...] | None = None,
                 side=UP, buff: float = 0.14, tick: float = 0.20,
                 stroke: float = 2.4, align: np.ndarray | None = None) -> VGroup:
    """A ruled span with end ticks, naming which slice of a row holds a role.

    ``label`` is passed straight to ``ty.line``, so ``$...$`` parts are set as
    mathematics and the rest as English on one baseline.  By default the
    label is centered on the rule (unchanged from every existing caller); pass
    ``align`` (e.g. ``LEFT``/``RIGHT``) to additionally hug one end of the
    rule via ``align_to`` instead.
    """
    above = float(side[1]) >= 0
    edge = mob.get_top()[1] + buff if above else mob.get_bottom()[1] - buff
    inward = -tick if above else tick
    left_x = mob.get_left()[0]
    right_x = mob.get_right()[0]
    rule = VGroup(
        Line([left_x, edge + inward, 0], [left_x, edge, 0]),
        Line([left_x, edge, 0], [right_x, edge, 0]),
        Line([right_x, edge, 0], [right_x, edge + inward, 0]),
    ).set_stroke(color, stroke)
    group = VGroup(rule)
    group.rule = rule
    if label:
        parts = (label,) if isinstance(label, str) else tuple(label)
        words = ty.line(*parts, size=ty.LABEL, color=color)
        words.next_to(rule, side, buff=0.12)
        if align is not None:
            words.align_to(rule, align)
        group.add(words)
        group.label = words
    return group


def labelled_arrow(start, end, label: str | None = None, *, color: str,
                   dashed: bool = False) -> VGroup:
    line_type = DashedLine if dashed else Arrow
    if dashed:
        arrow = line_type(start, end, dash_length=0.12).set_stroke(color, 2.0)
    else:
        arrow = line_type(start, end, buff=0.08, stroke_width=2.5,
                          max_tip_length_to_length_ratio=0.18).set_color(color)
    group = VGroup(arrow)
    if label:
        text = ty.words(label, size=ty.LABEL, color=color)
        text.next_to(arrow, UP, buff=0.10)
        group.add(text)
    return group


def caption_pill(text: str, *, color: str, width: float | None = None) -> VGroup:
    label = ty.words(text, size=ty.LABEL, color=color)
    box = RoundedRectangle(
        width=width or label.width + 0.48,
        height=label.height + 0.30,
        corner_radius=0.14,
    ).set_stroke(color, 1.5).set_fill(color, 0.05)
    label.move_to(box)
    return VGroup(box, label)


def mini_axes(center: np.ndarray, *, width: float = 2.5,
              height: float = 1.35) -> VGroup:
    return VGroup(
        Line(center + width * 0.5 * LEFT, center + width * 0.5 * RIGHT),
        Line(center + height * 0.5 * DOWN, center + height * 0.5 * UP),
    ).set_stroke(AXIS, 1.4, opacity=0.65)


def scalar_dot(color: str, radius: float = 0.075) -> Dot:
    return Dot(radius=radius).set_fill(color, 1).set_stroke(color, 0)
