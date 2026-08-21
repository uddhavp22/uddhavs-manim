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


class PatchEncoderNetwork(VGroup):
    """A visible local encoder, ported from 3b1b's network primitives.

    ``NetworkMobject`` (2017) keeps neuron layers separate from edge groups,
    stores incoming/outgoing edges on every neuron, and draws the edges behind
    the neurons.  ``NeuralNetwork`` (2024) uses the same layer/product layout
    for compact transformer-era diagrams.  This CE version preserves those
    mechanics while representing one strided-convolution window: every shown
    input sample connects to every shown output channel.
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

    def set_layer_values(self, layer_index: int, values) -> "PatchEncoderNetwork":
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
    height: float = 1.55,
    abbreviate: bool = True,
) -> VGroup:
    """A bracketed vector in the spirit of ``NumericEmbedding``.

    The compact form uses four values and an ellipsis for a D-dimensional
    embedding; the close-up form keeps every displayed coordinate.  Explicit
    signed coordinates make the encoder output read as a vector, not as a
    decorative stack of boxes.
    """
    values = np.asarray(values, dtype=float)
    shown = (
        (values[0], values[1], None, values[-2], values[-1])
        if abbreviate
        else tuple(values)
    )
    entries = VGroup()
    for value in shown:
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
    vector.set_height(height)

    group = VGroup(vector)
    group.entries = entries
    group.brackets = brackets
    group.vector = vector
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


def transformer_stack(*, width: float = 5.2, height: float = 2.15,
                      color: str, label: str = "causal Transformer") -> VGroup:
    """A restrained 2-D echo of the stacked prisms in network_flow.py."""
    layers = VGroup()
    for index in range(5):
        layer = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
        )
        layer.set_fill(color, opacity=0.045 + 0.018 * index)
        layer.set_stroke(color, 1.5, opacity=0.32 + 0.11 * index)
        layer.shift(index * (0.10 * UP + 0.10 * RIGHT))
        layers.add(layer)
    title = ty.words(label, size=ty.CAPTION, color=INK)
    title.move_to(layers[-1].get_top() + 0.30 * DOWN)
    return VGroup(layers, title)


def mlp_network(*, color: str, label: str = "projector") -> VGroup:
    """Small explicit MLP, following the layer/edge split of NetworkMobject."""
    sizes = (5, 7, 4)
    layers = VGroup()
    for size in sizes:
        dots = VGroup(*(
            Circle(radius=0.055).set_stroke(color, 1.4).set_fill(color, 0.28)
            for _ in range(size)
        ))
        dots.arrange(DOWN, buff=0.105)
        layers.add(dots)
    layers.arrange(RIGHT, buff=0.52)
    edges = VGroup()
    for first, second in zip(layers, layers[1:]):
        edges.add(VGroup(*(
            Line(a.get_center(), b.get_center()).set_stroke(color, 0.7, opacity=0.28)
            for a, b in it.product(first, second)
        )))
    box = RoundedRectangle(
        width=layers.width + 0.42,
        height=layers.height + 0.45,
        corner_radius=0.12,
    ).set_stroke(color, 1.7).set_fill(color, 0.045)
    title = ty.words(label, size=ty.LABEL, color=color)
    title.next_to(box, UP, buff=0.12)
    return VGroup(box, edges, layers, title)


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


def causal_fan(tokens: VGroup, target_index: int, *, color: str) -> VGroup:
    """Arcs are unnecessary here; converging arrows make the causal set explicit."""
    target = tokens[target_index]
    fan = VGroup()
    for source in tokens[:target_index + 1]:
        fan.add(Arrow(
            source.get_bottom(),
            target.get_bottom() + 0.55 * DOWN,
            buff=0.06,
            stroke_width=1.6,
            max_tip_length_to_length_ratio=0.13,
        ).set_color(color).set_opacity(0.62))
    return fan


def mini_axes(center: np.ndarray, *, width: float = 2.5,
              height: float = 1.35) -> VGroup:
    return VGroup(
        Line(center + width * 0.5 * LEFT, center + width * 0.5 * RIGHT),
        Line(center + height * 0.5 * DOWN, center + height * 0.5 * UP),
    ).set_stroke(AXIS, 1.4, opacity=0.65)


def scalar_dot(color: str, radius: float = 0.075) -> Dot:
    return Dot(radius=radius).set_fill(color, 1).set_stroke(color, 0)
