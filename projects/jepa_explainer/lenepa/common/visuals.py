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
    ManimColor,
    MathTex,
    Rectangle,
    RoundedRectangle,
    VGroup,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    interpolate_color,
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


class TokenColumn(VGroup):
    """One representation vector, showing its coordinates, changeable in place.

    Same object as ``numeric_embedding`` draws -- signed decimals between
    brackets, abbreviated with a ``\\vdots`` -- and deliberately so: these are
    the same token vectors scenes 1 to 3 already put on screen, and a viewer
    who has been reading numbers off them for two minutes should not arrive at
    the temporal-collapse scene to find the vectors have quietly turned into
    unlabelled bars.  The whole argument here is that six *values* become one
    value, so the values are what is drawn.

    What this adds over ``numeric_embedding`` is that the vector can be
    rewritten every frame.  ``set_values`` calls ``DecimalNumber.set_value``
    on each shown coordinate and re-anchors it, so:

    * a single ``ValueTracker`` can drive a whole row continuously;
    * the entry count never changes, so nothing re-lays-out mid-animation.

    That last point is load-bearing and depends on the data: with
    ``include_sign=True`` and one decimal place, every value in ``(-10, 10)``
    renders as exactly four glyphs (sign, digit, point, digit).  Token
    coordinates are unit normals, so the glyph count is constant and CE's
    ``set_value`` zips old and new submobjects one-to-one.  Feeding this class
    values that can cross +-10 would reintroduce the desync
    ``numeric_embedding``'s docstring warns about.

    Magnitude is additionally carried by brightness, following
    ``_2024/transformers/helpers.py::value_to_color``: near-zero coordinates
    sit close to ``MUTED``, large ones at full colour.  It is a second channel
    on top of the digits, never a replacement for them -- at row-in-a-batch
    size the pattern stays legible from across the frame while the digits stay
    there to be read.

    ``carrier`` is a persistent anchor dot at the column's centre, invisible
    until a caller reveals it.  It is what travels into the latent plane when
    the column stops being drawn as a vector and starts being drawn as a
    point -- the *same* Mobject before and after, so token-to-point identity
    is structural rather than implied.  ``numeric_embedding``'s docstring
    records why the alternative (Transforming a bracketed glyph straight into
    a ``Dot``) cannot be used: the point counts do not correspond and the
    interpolation is visibly mangled.
    """

    #: Which coordinates of a D-dimensional vector are drawn:
    #: ``v0, v1, \vdots, v_{-2}, v_{-1}``.  Identical to
    #: ``numeric_embedding(shown=5)``, so a column here and a column in scene
    #: 2 are the same picture of the same vector.
    SHOWN = 5
    #: Coordinate magnitude that reaches full colour.  Unit-normal coordinates
    #: rarely exceed this, and clipping above it costs nothing: no beat reads
    #: a magnitude off the brightness, only off the digits.
    VREF = 1.45
    #: Brightness floor.  Zero would make small coordinates unreadable, which
    #: defeats the point of drawing digits at all.
    DIM = 0.38

    def __init__(
        self,
        values: np.ndarray | list[float],
        *,
        color: str,
        height: float = 1.60,
        font_size: float = ty.LABEL,
        carrier_radius: float = 0.075,
    ) -> None:
        values = np.asarray(values, dtype=float)
        entries = VGroup()
        numeric = []
        for index in self._shown_indices(len(values)):
            if index is None:
                entries.add(MathTex(r"\vdots", font_size=font_size, color=color))
            else:
                entry = DecimalNumber(
                    float(values[index]),
                    num_decimal_places=1,
                    include_sign=True,
                    font_size=font_size,
                    color=color,
                )
                entries.add(entry)
                numeric.append((index, entry))
        entries.arrange(DOWN, buff=0.075)

        pad, tick = 0.12, 0.12
        left_x = entries.get_left()[0] - pad
        right_x = entries.get_right()[0] + pad
        top_y = entries.get_top()[1] + 0.06
        bottom_y = entries.get_bottom()[1] - 0.06
        brackets = VGroup(
            VGroup(
                Line([left_x + tick, top_y, 0], [left_x, top_y, 0]),
                Line([left_x, top_y, 0], [left_x, bottom_y, 0]),
                Line([left_x, bottom_y, 0], [left_x + tick, bottom_y, 0]),
            ),
            VGroup(
                Line([right_x - tick, top_y, 0], [right_x, top_y, 0]),
                Line([right_x, top_y, 0], [right_x, bottom_y, 0]),
                Line([right_x, bottom_y, 0], [right_x - tick, bottom_y, 0]),
            ),
        ).set_stroke(color, 1.8)

        # Anchors are measured against the *brackets*, which nothing in
        # ``set_values`` ever touches.  Measuring them against ``entries``
        # instead -- the obvious choice, and the one this class shipped with
        # -- is a feedback loop: re-placing the entries moves the group whose
        # centre and height the placement is derived from, so every call
        # compounds the last one.  Over a two-second updater the digits crawl
        # out of their own brackets and the group's bounding box inflates by
        # more than double.  A reference frame must not be something the
        # thing being placed is part of.
        anchors = [entry.get_center() - brackets.get_center()
                   for _, entry in numeric]
        built_brackets_height = float(brackets.height)

        body = VGroup(entries, brackets)
        body.set_height(height)
        carrier = scalar_dot(color, radius=carrier_radius)
        carrier.move_to(entries.get_center()).set_opacity(0.0)

        # Carrier last, so it draws over the body it will replace.
        super().__init__(body, carrier)
        self.colour = color
        self.entries = entries
        self.numeric = numeric
        self._anchors = anchors
        self._built_brackets_height = built_brackets_height
        self.brackets = brackets
        self.body = body
        self.carrier = carrier
        self.token_values = values
        self.body_alpha = 1.0
        self._paint()

    @staticmethod
    def _shown_indices(dim: int) -> tuple[int | None, ...]:
        return (0, 1, None, dim - 2, dim - 1)

    def set_values(self, values: np.ndarray | list[float]) -> "TokenColumn":
        """Rewrite the coordinates in place, without moving the column."""
        self.token_values = np.asarray(values, dtype=float)
        # Both the origin and the scale come off the brackets: they are the
        # one part of the column that ``set_values`` never writes to, so they
        # stay a fixed frame no matter how many times this runs.  See the
        # note where ``anchors`` is built.
        centre = self.brackets.get_center()
        scale = self.brackets.height / self._built_brackets_height
        for (index, entry), anchor in zip(self.numeric, self._anchors):
            entry.set_value(float(self.token_values[index]))
            entry.move_to(centre + scale * anchor)
        return self._paint()

    def set_body_alpha(self, alpha: float) -> "TokenColumn":
        """Fade the vector drawing without discarding what it is drawing.

        Opacity is kept as a separate multiplier that ``_paint`` re-applies,
        rather than being written straight onto the entries: brightness here
        encodes magnitude, and a plain ``set_opacity`` round trip would flatten
        eighteen distinctly-shaded vectors into eighteen identical ones.
        """
        self.body_alpha = float(np.clip(alpha, 0.0, 1.0))
        return self._paint()

    def _paint(self) -> "TokenColumn":
        alpha = self.body_alpha
        for (index, entry), _ in zip(self.numeric, self._anchors):
            level = min(1.0, abs(float(self.token_values[index])) / self.VREF)
            entry.set_color(interpolate_color(
                ManimColor(MUTED), ManimColor(self.colour),
                self.DIM + (1.0 - self.DIM) * level,
            ))
            entry.set_opacity(alpha)
        for entry in self.entries:
            if not isinstance(entry, DecimalNumber):
                entry.set_color(MUTED).set_opacity(alpha)
        self.brackets.set_stroke(self.colour, 1.8, opacity=alpha)
        return self

    def set_carrier_radius(self, radius: float) -> "TokenColumn":
        """Give the carrier an absolute world radius again.

        Resizing the column scales everything inside it, carrier included --
        correct while the carrier is a hidden anchor riding along, and wrong
        the moment it becomes a point in a plane, where its size is the
        plane's business and not the column's.  A row shrunk from hero size
        to grid size drags its carriers down by the same factor, and they
        reach the plane as specks a third the size of their own shadows.
        """
        current = max(float(self.carrier.width), 1e-6)
        self.carrier.scale(2.0 * float(radius) / current)
        return self

    def recolor(self, color: str) -> "TokenColumn":
        """Restate which colour the digits, brackets and carrier are drawn in."""
        self.colour = color
        self.carrier.set_fill(color).set_stroke(color, width=0)
        return self._paint()

    def carrier_home(self) -> np.ndarray:
        """Where the carrier sits when the column is drawn as a vector.

        Taken off the brackets for the same reason ``set_values`` is: the
        entries' bounding box depends on which digits are currently shown.
        """
        return self.brackets.get_center()


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


def caption_pill(text: str, *, color: str, width: float | None = None,
                 size: float | None = None) -> VGroup:
    """A labelled pill.

    ``size`` picks the label's type tier.  It exists because the pill is the
    main object in several scenes rather than an annotation on one, and a
    ``LABEL``-sized word inside a box sized to the frame reads as a caption
    that has floated loose.  ``width`` still overrides the box, but the box
    now grows from the text by default, so asking for bigger text cannot
    silently clip it.
    """
    label = ty.words(text, size=size or ty.LABEL, color=color)
    box = RoundedRectangle(
        width=max(width or 0.0, label.width + 0.48),
        height=label.height + 0.34,
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
