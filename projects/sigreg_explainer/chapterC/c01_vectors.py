"""Chapter C.01 — from the Epps--Pulley statistic to an embedding cloud.

The encoder is a Manim-CE port of the structural ideas used in
``3blue1brown_videos/_2017/nn``:

* ``part1.py::NetworkMobject`` — explicit layers, edges behind neurons, and
  neuron fill opacity representing activation;
* ``part1.py::MoreHonestMNistNetworkPreview`` — image pixels become the input
  layer rather than entering through a decorative arrow;
* ``part1.py::NetworkScene.feed_forward`` and
  ``part2.py::PreviewLearning.activate_network`` — every layer changes and a
  propagation flash crosses each complete edge group.

The source uses ManimGL.  This file implements the same visual grammar with
Manim Community primitives, as required by ``MANIM_CE_VS_MANIMGL.md``.

Render:
    SIGREG_VOICE=eleven ./render.sh \
        projects/sigreg_explainer/chapterC/c01_vectors.py C01 -qh
"""

from __future__ import annotations

import itertools as it
import os
import sys
from typing import cast

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common import type as ty
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, DIRECTION, GRID, INK, MUTED, TARGET
from common.score import epps_pulley


SCORE_GRID = np.linspace(-8.0, 8.0, 4000)
SCORE_LAMBDA = 1.0

# Small deterministic 5x7 bitmap digits.  Because every card has exactly 35
# cells, the first network layer can be the literal flattened image rather than
# a generic five-neuron stand-in.
DIGITS = (
    ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    ("11111", "10000", "10000", "11110", "00001", "00001", "11110"),
    ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
)


class C01(ActScene, ThreeDScene):
    """Recall the scalar statistic, then expose its dimensional limitation."""

    def construct(self):
        embedding_values = data.gaussian_3d(n=15, seed=76)
        wide_rng = np.random.default_rng(7601)
        wide_values = np.column_stack((
            embedding_values,
            wide_rng.normal(0.0, 1.0, size=(len(embedding_values), 5)),
        ))
        scalar_values = wide_values[:, 0]

        # --- Chapter B, compressed into the equation it established. -------
        formula = MathTex(
            R"\mathcal T(",
            R"x_{1:N}",
            R")=",
            R"N\int_{-\infty}^{\infty}",
            R"w_\lambda(t)",
            R"\left|\widehat\varphi_N(t)-\varphi_0(t)\right|^2",
            R"\,dt",
            font_size=40,
        ).set_color(INK)
        formula[1].set_color(CLOUD)
        formula[4].set_color(TARGET)
        formula[5].set_color(COLLAPSE)
        formula.move_to(1.95 * UP)
        layout.fit_in_frame(formula)

        gaussian = data.gaussian_1d(40)
        bimodal = data.bimodal_1d(40)
        gaussian_row = self._recap_row(
            gaussian,
            epps_pulley(gaussian, SCORE_LAMBDA, SCORE_GRID),
            CLOUD,
        ).move_to(0.25 * UP)
        bimodal_row = self._recap_row(
            bimodal,
            epps_pulley(bimodal, SCORE_LAMBDA, SCORE_GRID),
            COLLAPSE,
        ).move_to(1.35 * DOWN)

        with self.voiceover(
            text="In the last chapter, we built the Epps-Pulley statistic, "
                 "which compares a scalar batch with the standard Gaussian. "
                 "<bookmark mark='examples'/>A Gaussian-shaped batch scores "
                 "low, while a batch with a different shape scores higher."
        ) as tracker:
            lead = tracker.time_until_bookmark("examples")
            self.play(FadeIn(formula, shift=0.08 * UP), run_time=0.75)
            self.play(
                LaggedStart(
                    Indicate(formula[1], color=CLOUD, scale_factor=1.03),
                    Indicate(formula[5], color=COLLAPSE, scale_factor=1.02),
                    lag_ratio=0.35,
                ),
                run_time=max(1.15, lead - 0.75),
            )
            self.across(
                tracker,
                LaggedStart(
                    FadeIn(gaussian_row, shift=0.10 * UP),
                    FadeIn(bimodal_row, shift=0.10 * UP),
                    lag_ratio=0.38,
                ),
                floor=1.2,
            )

        # --- The scalar batch is produced by a real feed-forward diagram. ---
        image_cards = self._image_batch(15)
        featured_card = self._pixel_card(0).scale(2.65)
        featured_card.move_to(np.array([-5.25, -0.48, 0.0]))
        layers, fixed_edges, output_edges = self._encoder_network()

        d_label = ty.maths("D=1", size=ty.EQ, color=DIRECTION)
        d_label.next_to(layers[-1][0], DOWN, buff=0.48)

        output_line = NumberLine(
            x_range=(-3, 3, 1),
            length=3.75,
            include_numbers=False,
            include_tip=False,
        ).set_stroke(MUTED, 2)
        output_line.move_to(np.array([4.55, -0.55, 0.0]))
        line_label = ty.maths(R"\mathbb R", size=ty.LABEL, color=MUTED)
        line_label.next_to(output_line, DOWN, buff=0.18)
        output_dots = VGroup(*(
            Dot(output_line.number_to_point(value), radius=0.058)
            .set_fill(DIRECTION, 0.22)
            for value in scalar_values
        ))

        active_dot = Dot(
            output_line.number_to_point(scalar_values[0]), radius=0.085,
        ).set_fill(DIRECTION, 1.0)
        active_value = DecimalNumber(
            scalar_values[0],
            num_decimal_places=1,
            include_sign=True,
            font_size=54,
            color=CLOUD,
        ).move_to(np.array([4.55, 0.38, 0.0]))

        network_furniture = Group(
            fixed_edges,
            layers[0],
            layers[1],
            layers[2],
            output_edges[0],
            layers[-1][0],
        )

        with self.voiceover(
            text="Suppose a neural network produces those numbers. With one output "
                 "coordinate, every input gives us one scalar, and the whole "
                 "batch still lies on a line."
        ) as tracker:
            self.play(
                FadeOut(gaussian_row),
                FadeOut(bimodal_row),
                formula.animate.scale(0.72).move_to(3.18 * UP),
                FadeIn(featured_card, shift=0.10 * RIGHT),
                FadeIn(network_furniture),
                FadeIn(d_label, shift=0.06 * UP),
                Create(output_line),
                FadeIn(line_label),
                run_time=0.85,
                rate_func=smooth,
            )
            shown_indices = (0, 1, 2, 3, 4, 5, 8)
            cycle_time = max(
                0.72,
                (tracker.get_remaining_duration() - 0.45) / len(shown_indices),
            )
            for position, index in enumerate(shown_indices):
                if position:
                    next_card = self._pixel_card(index).scale(2.65)
                    next_card.move_to(featured_card)
                    card_animation = Transform(featured_card, next_card)
                else:
                    card_animation = featured_card.animate.scale(1.015)
                self.play(
                    card_animation,
                    self._feed_forward(
                        layers,
                        fixed_edges,
                        output_edges,
                        self._digit_vector(index),
                        wide_values[index],
                        dimension=1,
                    ),
                    active_dot.animate.move_to(
                        output_line.number_to_point(scalar_values[index])
                    ),
                    active_value.animate.set_value(scalar_values[index]),
                    FadeIn(output_dots[index]),
                    run_time=cycle_time,
                    rate_func=smooth,
                )
            self.add(active_dot, active_value)

        with self.voiceover(
            text="After the batch passes through, those outputs form the same "
                 "one-dimensional sample we scored before."
        ) as tracker:
            self.across(
                tracker,
                LaggedStart(
                    AnimationGroup(
                        ReplacementTransform(featured_card, image_cards[0]),
                        FadeIn(VGroup(*image_cards[1:])),
                        FadeOut(active_value),
                        FadeOut(active_dot),
                    ),
                    AnimationGroup(
                        *(
                            dot.animate.set_fill(DIRECTION, 1.0)
                            if index in shown_indices
                            else FadeIn(dot)
                            for index, dot in enumerate(output_dots)
                        ),
                    ),
                    lag_ratio=0.28,
                ),
                floor=1.25,
            )

        # --- One centred output becomes a D-dimensional representation. -----
        plane = Axes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            x_length=3.55,
            y_length=2.35,
            tips=False,
            axis_config={"include_numbers": False, "stroke_width": 1.5},
        ).set_stroke(MUTED, opacity=0.70)
        plane.move_to(np.array([4.55, -0.48, 0.0]))
        plane_targets = [
            plane.c2p(x, y) for x, y in embedding_values[:, :2]
        ]

        preview_centre = np.array([4.55, -0.52, 0.0])
        preview_axes = VGroup(
            Line(preview_centre + 1.92 * LEFT,
                 preview_centre + 1.92 * RIGHT),
            Line(preview_centre + np.array([-1.18, -0.88, 0.0]),
                 preview_centre + np.array([1.18, 0.88, 0.0])),
            Line(preview_centre + 1.22 * DOWN,
                 preview_centre + 1.22 * UP),
        ).set_stroke(MUTED, 1.6, opacity=0.68)
        preview_targets = [
            preview_centre
            + (0.55 * x + 0.17 * z) * RIGHT
            + (0.37 * y + 0.15 * z) * UP
            for x, y, z in embedding_values
        ]

        head_edges = output_edges[0]
        head_nodes = VGroup(layers[-1][0])
        head_centre = layers[-1][0].get_center()
        edges_2, nodes_2 = self._output_head(layers[2], head_centre, 2)
        edges_3, nodes_3 = self._output_head(layers[2], head_centre, 3)
        d_two = ty.maths("D=2", size=ty.EQ, color=DIRECTION)
        d_two.next_to(nodes_2, DOWN, buff=0.34)
        d_three = ty.maths("D=3", size=ty.EQ, color=DIRECTION)
        d_three.next_to(nodes_3, DOWN, buff=0.34)
        geometry = VGroup(output_line, line_label)

        axes_3d = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
            x_length=5.2,
            y_length=5.2,
            z_length=5.2,
        )
        axes_3d.set_stroke(MUTED, 1.5, opacity=0.6)
        axes_3d.set_opacity(0.0)
        self.add(axes_3d)
        cloud_targets = [axes_3d.c2p(*point) for point in embedding_values]

        shown_label = ty.maths(
            R"\text{shown: }D=3", size=ty.LABEL, color=MUTED,
        ).next_to(preview_axes, UP, buff=0.18)

        with self.voiceover(
            text="Now, if we widen the output layer, "
                 "<bookmark mark='two'/>each input gets a second coordinate. "
                 "The line opens into a plane. <bookmark mark='three'/>Add a "
                 "third, and the batch becomes a cloud."
        ) as tracker:
            self.play(
                Indicate(head_nodes, color=DIRECTION, scale_factor=1.06),
                run_time=max(0.55, tracker.time_until_bookmark("two")),
            )
            second_time = max(1.0, tracker.time_until_bookmark("three"))
            self.play(
                Transform(head_edges, edges_2),
                Transform(head_nodes, nodes_2),
                Succession(FadeOut(d_label), FadeIn(d_two)),
                Succession(FadeOut(geometry), FadeIn(plane)),
                *(cast(Animation, dot.animate.move_to(point))
                  for dot, point in zip(output_dots, plane_targets)),
                run_time=second_time,
                rate_func=smooth,
            )
            d_label = d_two
            self.remove(geometry)
            geometry = plane
            self.across(
                tracker,
                Transform(head_edges, edges_3),
                Transform(head_nodes, nodes_3),
                Succession(FadeOut(d_label), FadeIn(d_three)),
                Succession(FadeOut(geometry), FadeIn(preview_axes)),
                *(cast(Animation, dot.animate.move_to(point))
                  for dot, point in zip(output_dots, preview_targets)),
                floor=1.35,
                rate_func=smooth,
            )
            d_label = d_three
            self.remove(geometry)
            geometry = preview_axes

        with self.voiceover(
            text="We'll use three dimensions because that's what we can see. "
                 "<bookmark mark='more'/>In practice, D is often much larger."
        ) as tracker:
            self.play(
                AnimationGroup(
                    Indicate(d_label, color=CLOUD, scale_factor=1.05),
                    Indicate(VGroup(geometry, output_dots),
                             color=CLOUD, scale_factor=1.01),
                    FadeIn(shown_label),
                    lag_ratio=0.28,
                ),
                run_time=max(0.75, tracker.time_until_bookmark("more")),
            )
            remaining = max(2.4, tracker.get_remaining_duration())
            dimensions = (4, 6, 8)
            settle = min(0.65, 0.18 * remaining)
            step_time = (remaining - settle) / len(dimensions)
            for dimension in dimensions:
                target_edges, target_nodes = self._output_head(
                    layers[2], head_centre, dimension,
                )
                target_label = ty.maths(
                    f"D={dimension}", size=ty.EQ, color=DIRECTION,
                )
                target_label.next_to(target_nodes, DOWN, buff=0.34)
                self.play(
                    Transform(head_edges, target_edges),
                    Transform(head_nodes, target_nodes),
                    Succession(FadeOut(d_label), FadeIn(target_label)),
                    run_time=step_time,
                    rate_func=smooth,
                )
                d_label = target_label
            self.wait(settle)

        z_label = ty.maths(
            R"Z=\{z_i\}_{i=1}^{N}",
            size=ty.EQ_DISPLAY,
            color=CLOUD,
        ).move_to(np.array([4.55, 1.45, 0.0]))
        target_label = ty.maths(
            R"\text{target: }\mathcal N(0,I_D)",
            size=ty.EQ,
            color=TARGET,
        ).move_to(np.array([3.85, 2.28, 0.0]))
        self.add_fixed_in_frame_mobjects(z_label, target_label)
        z_label.set_opacity(0.0)
        target_label.set_opacity(0.0)

        with self.voiceover(
            text="From here on, this cloud is Z. <bookmark mark='target'/>"
                 "Suppose we want it to follow a standard Gaussian in D "
                 "dimensions."
        ) as tracker:
            self.play(
                Succession(
                    FadeOut(shown_label),
                    z_label.animate.set_opacity(1.0),
                ),
                Indicate(output_dots, color=CLOUD, scale_factor=1.025),
                run_time=max(0.8, tracker.time_until_bookmark("target")),
            )
            diagram = Group(
                image_cards,
                layers[0],
                layers[1],
                layers[2],
                fixed_edges,
                head_nodes,
                head_edges,
                d_label,
            )
            self.play(
                FadeOut(diagram),
                FadeOut(formula),
                FadeOut(geometry),
                FadeOut(output_dots),
                z_label.animate.move_to(np.array([3.85, 2.72, 0.0])),
                run_time=0.65,
            )
            self.move_camera(
                phi=70 * DEGREES,
                theta=-32 * DEGREES,
                run_time=1.25,
                added_anims=[
                    cast(Animation, axes_3d.animate.set_opacity(0.6)),
                ],
            )
            cloud_dots = output_dots.copy()
            for dot, point in zip(cloud_dots, cloud_targets):
                dot.move_to(point).set_fill(CLOUD, 1.0)
            self.add_fixed_orientation_mobjects(*cloud_dots)
            cloud_dots.set_opacity(0.0)
            self.across(
                tracker,
                LaggedStart(*(
                    dot.animate.set_opacity(1.0)
                    for dot in cloud_dots
                ), lag_ratio=0.035),
                target_label.animate.set_opacity(1.0),
                floor=1.0,
            )

        self.inspect(1.0)
        self.settle_frame()

    @staticmethod
    def _recap_row(samples: np.ndarray, score: float, colour) -> VGroup:
        line = NumberLine(
            x_range=(-3, 3, 1),
            length=5.0,
            include_numbers=False,
            include_tip=False,
        ).set_stroke(MUTED, 2)
        dots = VGroup(*(
            Dot(line.number_to_point(value), radius=0.045)
            .set_fill(colour, 1.0)
            for value in samples
        ))
        result = ty.line(
            "score",
            Rf"$={score:.3f}$",
            size=ty.EQ_DISPLAY,
            color=colour,
        )
        result.next_to(line, RIGHT, buff=0.75)
        return VGroup(line, dots, result).move_to(ORIGIN)

    @classmethod
    def _image_batch(cls, count: int) -> VGroup:
        cards = VGroup(*(cls._pixel_card(index) for index in range(count)))
        cards.arrange_in_grid(rows=3, cols=5, buff=(0.09, 0.09))
        cards.move_to(np.array([-5.45, -0.18, 0.0]))
        return cards

    @staticmethod
    def _pixel_card(index: int) -> VGroup:
        bitmap = DIGITS[index % len(DIGITS)]
        frame = RoundedRectangle(
            width=0.48,
            height=0.62,
            corner_radius=0.045,
        ).set_fill(GRID, opacity=0.34).set_stroke(MUTED, 1.0, opacity=0.58)
        cells = VGroup()
        side = 0.050
        for row, bits in enumerate(bitmap):
            for column, bit in enumerate(bits):
                opacity = 0.96 if bit == "1" else 0.045
                cell = Square(side_length=side)
                cell.set_fill(CLOUD, opacity=opacity).set_stroke(width=0.0)
                cell.move_to(
                    frame.get_center()
                    + (column - 2) * side * 1.15 * RIGHT
                    + (3 - row) * side * 1.15 * UP
                )
                cells.add(cell)
        return VGroup(frame, cells)

    @staticmethod
    def _digit_vector(index: int) -> np.ndarray:
        return np.array(
            [float(bit) for row in DIGITS[index % len(DIGITS)] for bit in row],
            dtype=float,
        )

    @staticmethod
    def _encoder_network():
        """Port ``_2017/nn/part1.py::NetworkMobject`` to Manim CE.

        The layer sizes are ``35 -> 8 -> 6 -> D``.  Thirty-five is not a
        display abbreviation: it is the exact flattened size of each 5x7 input
        card.  Edges are built behind the neuron layers, matching the source.
        """
        sizes = (35, 8, 6, 8)
        radii = (0.028, 0.070, 0.070, 0.082)
        buffs = (0.060, 0.165, 0.190, 0.0)
        layers = VGroup()
        for layer_index, (size, radius, buff) in enumerate(
            zip(sizes, radii, buffs)
        ):
            colour = DIRECTION if layer_index == len(sizes) - 1 else CLOUD
            layer = VGroup(*(
                Circle(radius=radius)
                .set_stroke(colour, 1.15, opacity=0.92)
                .set_fill(colour, opacity=0.0)
                for _ in range(size)
            ))
            if size > 1:
                layer.arrange(DOWN, buff=buff)
            layers.add(layer)

        layers.arrange(RIGHT, buff=0.72)
        layers.move_to(np.array([-1.15, -0.20, 0.0]))

        output_centre = layers[-1].get_center()
        offsets = (0.0, 0.44, -0.44, 0.88, -0.88, 1.32, -1.32, 1.76)
        for node, offset in zip(layers[-1], offsets):
            node.move_to(output_centre + offset * UP)

        def connections(left, right, *, width, opacity):
            return VGroup(*(
                Line(
                    a.get_center(),
                    b.get_center(),
                    buff=(a.width + b.width) / 4,
                ).set_stroke(MUTED, width=width, opacity=opacity)
                for a, b in it.product(left, right)
            ))

        fixed_edges = VGroup(
            connections(layers[0], layers[1], width=0.55, opacity=0.13),
            connections(layers[1], layers[2], width=0.8, opacity=0.24),
        )
        output_edges = VGroup(*(
            connections(
                layers[2], VGroup(node), width=0.9, opacity=0.34,
            )
            for node in layers[-1]
        ))
        return layers, fixed_edges, output_edges

    @staticmethod
    def _output_head(source_layer: VGroup, centre: np.ndarray, dimension: int):
        """Build a centred output head whose geometry grows continuously.

        Each target is symmetric about ``centre``.  Transforming between these
        groups makes D=1 split into D=2, inserts the centred third coordinate,
        and then expands evenly for larger D without nodes popping in at one
        side of the layer.
        """
        spacing = 0.36 if dimension <= 3 else min(0.34, 2.5 / (dimension - 1))
        offsets = np.linspace(
            0.5 * (dimension - 1) * spacing,
            -0.5 * (dimension - 1) * spacing,
            dimension,
        )
        nodes = VGroup(*(
            Circle(radius=0.082)
            .set_stroke(DIRECTION, 1.15, opacity=0.92)
            .set_fill(DIRECTION, opacity=0.12)
            .move_to(centre + offset * UP)
            for offset in offsets
        ))
        edges = VGroup(*(
            Line(
                source.get_center(),
                target.get_center(),
                buff=(source.width + target.width) / 4,
            ).set_stroke(MUTED, width=0.9, opacity=0.34)
            for source, target in it.product(source_layer, nodes)
        ))
        return edges, nodes

    @staticmethod
    def _active_layers(
        layers: VGroup,
        pixel_vector: np.ndarray,
        output_vector: np.ndarray,
        *,
        dimension: int,
    ) -> list[VGroup]:
        """Return deterministic activation states for one feed-forward pass."""
        rng = np.random.default_rng(1701)
        w1 = rng.normal(0.0, 0.43, size=(8, 35))
        b1 = rng.normal(0.0, 0.22, size=8)
        w2 = rng.normal(0.0, 0.55, size=(6, 8))
        b2 = rng.normal(0.0, 0.20, size=6)

        sigmoid = lambda values: 1.0 / (1.0 + np.exp(-values))
        activations = [
            np.asarray(pixel_vector, dtype=float),
            sigmoid(w1 @ pixel_vector + b1),
        ]
        activations.append(sigmoid(w2 @ activations[-1] + b2))
        activations.append(sigmoid(np.asarray(output_vector[:dimension])))

        active_layers: list[VGroup] = []
        for layer_index, (layer, values) in enumerate(zip(layers, activations)):
            active = layer.copy()
            for node, value in zip(active, values):
                colour = DIRECTION if layer_index == 3 else CLOUD
                node.set_fill(colour, opacity=float(0.10 + 0.90 * value))
            active_layers.append(active)
        return active_layers

    @classmethod
    def _feed_forward(
        cls,
        layers: VGroup,
        fixed_edges: VGroup,
        output_edges: VGroup,
        pixel_vector: np.ndarray,
        output_vector: np.ndarray,
        *,
        dimension: int,
        include_input: bool = True,
    ) -> Succession:
        """Animate every active layer and complete edge group, left to right."""
        active = cls._active_layers(
            layers, pixel_vector, output_vector, dimension=dimension,
        )
        stages: list[Animation] = []
        if include_input:
            stages.append(Transform(layers[0], active[0]))
        stages.extend((
            AnimationGroup(
                cls._edge_wave(fixed_edges[0]),
                Transform(layers[1], active[1]),
            ),
            AnimationGroup(
                cls._edge_wave(fixed_edges[1]),
                Transform(layers[2], active[2]),
            ),
            AnimationGroup(
                *(
                    cls._edge_wave(output_edges[index])
                    for index in range(dimension)
                ),
                *(
                    Transform(layers[-1][index], active[-1][index])
                    for index in range(dimension)
                ),
            ),
        ))
        return Succession(*stages)

    @staticmethod
    def _edge_wave(edge_group: VGroup) -> ShowPassingFlash:
        """CE equivalent of 3b1b's full edge-propagation animation."""
        flash = edge_group.copy()
        flash.set_stroke(CLOUD, width=1.15, opacity=0.38)
        return ShowPassingFlash(flash, time_width=0.28)
