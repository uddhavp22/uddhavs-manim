"""LeNEPA — a sub-five-minute segment for the JEPA variants explainer.

Visual references (structural, not stylistic copies):

* ``3blue1brown_videos/_2017/nn/part1.py::NetworkMobject`` for explicit
  layers, edges behind nodes, and visible propagation through a small MLP;
* ``3blue1brown_videos/_2024/transformers/helpers.py::EmbeddingArray`` for
  persistent embedding columns;
* ``.../mlp.py::BasicMLPWalkThrough`` for focusing on one vector before
  revealing the same operation in parallel;
* ``.../network_flow.py::HighLevelNetworkFlow`` for keeping token objects
  visible as they move through a model block.

Render all draft scenes:
    LENEPA_VOICE=draft ./render.sh projects/jepa_explainer/lenepa/scenes.py -a -ql

Render all final-preview scenes with ElevenLabs:
    LENEPA_VOICE=eleven ./render.sh projects/jepa_explainer/lenepa/scenes.py -a -qh

ElevenLabs is a temporary preview voice.  The narration constants embedded in
the voiceover blocks are the handoff script for the author's future recording.
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import type as ty
from common.palette import (
    AXIS,
    BACKBONE,
    DISCARD,
    ERROR,
    GRID,
    INK,
    INPUT,
    KEEP,
    MUTED,
    NEXT_TARGET,
    PREDICTION,
    PROJECTOR,
    SIGREG,
)
from common.scene import LenepaScene
from common.visuals import (
    caption_pill,
    causal_fan,
    labelled_arrow,
    latent_column,
    latent_row,
    mini_axes,
    mlp_network,
    numeric_embedding,
    PatchEncoderNetwork,
    scalar_dot,
    transformer_stack,
)


def scene_title(text: str) -> Mobject:
    title = ty.title(text)
    title.to_edge(UP, buff=0.48)
    return title


def small_note(text: str, color: str = MUTED) -> Mobject:
    return ty.words(text, size=ty.LABEL, color=color)


class LeNEPA01Tokens(LenepaScene):
    """One signal passes through a visible shared encoder into ordered tokens."""

    def construct(self):
        def signal(x: float) -> float:
            return (
                0.52 * np.sin(1.45 * x)
                + 0.22 * np.sin(3.7 * x + 0.55)
                + 0.12 * np.cos(6.2 * x)
            )

        signal_y = 1.55
        bounds = np.linspace(-5.4, 5.4, 7)
        baseline = Line(5.65 * LEFT, 5.65 * RIGHT)
        baseline.shift(signal_y * UP)
        baseline.set_stroke(AXIS, 1.4, opacity=0.70)
        patches = VGroup(*(
            ParametricFunction(
                lambda t: np.array([t, signal(t) + signal_y, 0.0]),
                t_range=(left, right, 0.025),
            ).set_stroke(INPUT, 3.2)
            for left, right in zip(bounds[:-1], bounds[1:])
        ))
        dividers = VGroup(*(
            DashedLine(
                np.array([x, signal_y - 0.86, 0.0]),
                np.array([x, signal_y + 0.86, 0.0]),
                dash_length=0.08,
            ).set_stroke(GRID, 1.4)
            for x in bounds[1:-1]
        ))
        patch_boxes = VGroup(*(
            Rectangle(width=right - left - 0.05, height=1.72)
            .move_to(np.array([(left + right) / 2, signal_y, 0.0]))
            .set_stroke(INPUT, 1.2, opacity=0.35)
            .set_fill(INPUT, opacity=0.035)
            for left, right in zip(bounds[:-1], bounds[1:])
        ))
        signal_shape = ty.maths(R"x\in\mathbb R^{C\times L}", size=ty.LABEL, color=MUTED)
        signal_shape.next_to(baseline, DOWN, buff=0.16).to_edge(LEFT, buff=0.58)
        scan_window = patch_boxes[0].copy()
        scan_window.set_stroke(PREDICTION, 3.0, opacity=1.0)
        scan_window.set_fill(PREDICTION, opacity=0.06)

        with self.voiceover(
            text="This signal has L time steps. A strided convolution reads one "
                 "short window at a time, reusing the same filters as it slides "
                 "along the trace. The windows keep their left-to-right order."
        ) as tracker:
            self.play(Create(baseline), FadeIn(signal_shape), run_time=0.7)
            self.play(Create(patches, lag_ratio=0.025), run_time=1.45)
            self.play(FadeIn(scan_window), run_time=0.35)
            self.play(
                Succession(*(
                    scan_window.animate.move_to(box)
                    for box in patch_boxes[1:]
                )),
                run_time=3.8,
                rate_func=linear,
            )
            self.play(
                FadeOut(scan_window),
                LaggedStart(*[FadeIn(box) for box in patch_boxes], lag_ratio=0.08),
                LaggedStart(*[Create(line) for line in dividers], lag_ratio=0.10),
                run_time=1.1,
            )
            self.wait(max(0.1, tracker.get_remaining_duration()))

        focus_index = 2
        focus_patch = patches[focus_index].copy()
        focus_patch.scale(1.12).move_to(4.55 * LEFT + 0.55 * DOWN)
        sample_dots = VGroup(*(
            Dot(focus_patch.point_from_proportion(alpha), radius=0.045)
            .set_fill(INPUT, 1)
            .set_stroke(INPUT, 0)
            for alpha in np.linspace(0.05, 0.95, 8)
        ))
        input_values = np.array([
            signal(x)
            for x in np.linspace(bounds[focus_index], bounds[focus_index + 1], 8)
        ])
        output_values = np.array([0.72, -0.34, 0.18, 0.91, -0.57, 0.43, -0.11])
        encoder = PatchEncoderNetwork(color=INPUT)
        encoder.move_to(0.35 * LEFT + 0.55 * DOWN)
        encoder_label = ty.words("shared convolution", size=ty.CAPTION, color=INK)
        encoder_label.next_to(encoder, UP, buff=0.30)
        output_vector = numeric_embedding(
            output_values,
            color=INPUT,
            label=R"z_3\in\mathbb R^D",
            height=1.85,
            abbreviate=False,
        )
        output_vector.next_to(encoder, RIGHT, buff=0.72)

        with self.voiceover(
            text="Focus on the third window. Its samples feed the encoder "
                 "together. Each output channel applies a learned filter, and "
                 "the D channel values form one latent vector, z three."
        ) as tracker:
            self.play(
                patches.animate.set_stroke(opacity=0.16),
                patch_boxes.animate.set_stroke(opacity=0.12).set_fill(opacity=0.01),
                dividers.animate.set_opacity(0.18),
                signal_shape.animate.set_opacity(0.28),
                TransformFromCopy(patches[focus_index], focus_patch, path_arc=-0.18),
                run_time=1.25,
            )
            self.play(
                FadeIn(sample_dots),
                FadeIn(encoder),
                FadeIn(encoder_label),
                run_time=0.8,
            )
            self.play(
                LaggedStart(*(
                    TransformFromCopy(dot, neuron)
                    for dot, neuron in zip(sample_dots, encoder.input_layer)
                ), lag_ratio=0.06),
                run_time=1.15,
            )
            encoder.set_layer_values(0, input_values)
            output_targets = encoder.output_layer.copy()
            scale = np.max(np.abs(output_values))
            for value, neuron in zip(output_values, output_targets):
                neuron.set_fill(INPUT, opacity=0.12 + 0.76 * abs(value) / scale)
            edge_flash = LaggedStart(*(
                ShowPassingFlash(
                    edge.copy().set_stroke(PREDICTION, 2.8, opacity=0.95),
                    time_width=0.25,
                )
                for edge in encoder.edges
            ), lag_ratio=0.006)
            self.play(
                edge_flash,
                Transform(encoder.output_layer, output_targets),
                run_time=1.55,
            )
            coordinate_movers = encoder.output_layer.copy()
            self.add(coordinate_movers)
            self.play(
                LaggedStart(*(
                    mover.animate.move_to(entry)
                    for mover, entry in zip(
                        coordinate_movers,
                        output_vector.entries,
                    )
                ), lag_ratio=0.07),
                Create(output_vector.brackets),
                FadeIn(output_vector.label),
                run_time=1.15,
            )
            self.play(
                FadeOut(coordinate_movers),
                FadeIn(output_vector.entries),
                run_time=0.35,
            )
            self.wait(max(0.1, tracker.get_remaining_duration()))

        rng = np.random.default_rng(21)
        vectors = VGroup(*(
            numeric_embedding(
                rng.normal(size=7),
                color=INPUT,
                label=rf"z_{index + 1}",
                height=1.25,
            )
            for index in range(6)
        ))
        vectors.arrange(RIGHT, buff=0.82, aligned_edge=UP)
        vectors.move_to(1.05 * DOWN)
        arrows = VGroup(*(
            Arrow(
                box.get_bottom(),
                vector.get_top(),
                buff=0.10,
                stroke_width=1.7,
                max_tip_length_to_length_ratio=0.22,
            ).set_color(INPUT).set_opacity(0.68)
            for box, vector in zip(patch_boxes, vectors)
        ))
        batch_shape = ty.maths(
            R"x\in\mathbb R^{B\times C\times L}"
            R"\quad\longrightarrow\quad"
            R"\;z\in\mathbb R^{B\times T\times D}",
            size=ty.EQ_DISPLAY,
            color=INK,
        )
        batch_shape.to_edge(DOWN, buff=0.42)

        with self.voiceover(
            text="The same map turns every other window into its own vector. "
                 "So, across a batch, B by C by L becomes B by T by D: T "
                 "ordered tokens, each with D coordinates."
        ) as tracker:
            self.play(
                FadeOut(VGroup(focus_patch, sample_dots, encoder, encoder_label)),
                patches.animate.set_stroke(opacity=1.0),
                patch_boxes.animate.set_stroke(opacity=0.35).set_fill(opacity=0.035),
                dividers.animate.set_opacity(0.35),
                signal_shape.animate.set_opacity(0.75),
                run_time=0.70,
            )
            self.play(
                FadeOut(output_vector),
                FadeIn(vectors[focus_index]),
                run_time=0.40,
            )
            self.play(
                LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.10),
                run_time=1.15,
            )
            self.play(
                LaggedStart(*(
                    FadeIn(vector, shift=0.16 * DOWN)
                    for index, vector in enumerate(vectors)
                    if index != focus_index
                ), lag_ratio=0.12),
                run_time=1.10,
            )
            self.play(FadeIn(batch_shape, shift=0.08 * UP), run_time=1.0)
            self.wait(max(0.1, tracker.get_remaining_duration()))

        self.inspect(1.0)
        self.clear_beat()


class LeNEPA02Predict(LenepaScene):
    """Expose one causal prediction, then show the same shift everywhere."""

    def construct(self):
        title = scene_title("Predict the next latent")
        tokens = latent_row(
            [R"z_1", R"z_2", R"z_3", R"z_4", R"z_5", R"z_6"],
            color=INPUT,
            height=1.06,
            buff=0.64,
            seed=31,
        ).move_to(2.05 * UP)
        stack = transformer_stack(width=6.7, height=1.45, color=BACKBONE)
        stack.move_to(0.28 * UP)
        input_arrows = VGroup(*(
            Arrow(token.get_bottom(),
                  np.array([token.get_x(), stack.get_top()[1], 0.0]),
                  buff=0.06, stroke_width=1.5,
                  max_tip_length_to_length_ratio=0.20).set_color(INPUT)
            for token in tokens
        ))
        focus = 3
        focus_box = SurroundingRectangle(tokens[focus], buff=0.10)
        focus_box.set_stroke(PREDICTION, 2.4)
        fan = causal_fan(tokens, focus, color=PREDICTION)
        future_curtain = Rectangle(
            width=tokens[-1].get_right()[0] - tokens[focus + 1].get_left()[0] + 0.35,
            height=1.75,
        ).set_fill(GRID, 0.78).set_stroke(MUTED, 1.2, opacity=0.55)
        future_curtain.move_to(VGroup(*tokens[focus + 1:]).get_center())
        future_label = ty.words("future", size=ty.LABEL, color=MUTED)
        future_label.move_to(future_curtain)

        prediction = latent_column(
            np.array([0.55, -0.28, 0.82, -0.62, 0.18, 0.70, -0.42]),
            color=PREDICTION,
            label=R"\hat z_4",
            height=1.15,
        ).move_to(1.75 * DOWN)
        out_arrow = Arrow(stack.get_bottom(), prediction.get_top(), buff=0.10,
                          stroke_width=2.6).set_color(PREDICTION)

        with self.voiceover(
            text="The token row enters a causal Transformer. Focus on position "
                 "four. Its output may use tokens one through four, but the "
                 "future remains hidden. The output, z-hat four, predicts from "
                 "the available history."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(tokens, shift=0.10 * DOWN), run_time=0.75)
            self.play(FadeIn(stack), LaggedStart(*[GrowArrow(a) for a in input_arrows],
                                                lag_ratio=0.08), run_time=1.25)
            self.play(Create(focus_box), Create(fan),
                      FadeIn(future_curtain), FadeIn(future_label), run_time=1.2)
            self.across(tracker, GrowArrow(out_arrow), FadeIn(prediction), floor=1.35)

        target = tokens[focus + 1].copy()
        target.generate_target()
        target.target.move_to(prediction.get_center() + 2.2 * RIGHT)
        compare = labelled_arrow(
            prediction.get_right(), target.target.get_left(),
            "compare", color=ERROR, dashed=True,
        )
        next_label = ty.words("actual next token", size=ty.LABEL, color=NEXT_TARGET)
        next_label.next_to(target.target, DOWN, buff=0.18)

        with self.voiceover(
            text="The target is the actual next token, z five. Shift that same "
                 "comparison across the row: "
                 "z-hat one predicts z two, z-hat two predicts z three, and so "
                 "on. Defining the task needs no mask augmentation, second "
                 "view, or teacher network."
        ) as tracker:
            target.target.set_color(NEXT_TARGET)
            self.play(
                FadeOut(fan), FadeOut(future_curtain), FadeOut(future_label),
                MoveToTarget(target),
                FadeIn(next_label), Create(compare), run_time=1.1,
            )
            pairs = VGroup()
            for index in range(5):
                left = scalar_dot(PREDICTION, 0.08)
                right = scalar_dot(NEXT_TARGET, 0.08)
                arrow = Arrow(left.get_right(), right.get_left(), buff=0.08,
                              stroke_width=2.0).set_color(ERROR)
                pair = VGroup(left, arrow, right).arrange(RIGHT, buff=0.18)
                lab = ty.maths(
                    rf"\hat z_{index + 1}\to z_{index + 2}",
                    size=ty.LABEL,
                    color=INK,
                )
                lab.next_to(pair, DOWN, buff=0.10)
                pairs.add(VGroup(pair, lab))
            pairs.arrange(RIGHT, buff=0.36).to_edge(DOWN, buff=0.40)
            badges = VGroup(
                caption_pill("no mask augmentation", color=MUTED),
                caption_pill("no second view", color=MUTED),
                caption_pill("no teacher network", color=MUTED),
            ).arrange(RIGHT, buff=0.28).move_to(0.25 * DOWN)
            self.play(
                FadeOut(VGroup(stack, input_arrows, focus_box, out_arrow,
                               prediction, target, compare, next_label)),
                tokens.animate.scale(0.78).move_to(2.35 * UP),
                LaggedStart(*[FadeIn(pair, shift=0.06 * UP) for pair in pairs],
                            lag_ratio=0.12),
                run_time=1.45,
            )
            self.across(
                tracker,
                LaggedStart(*[FadeIn(badge) for badge in badges], lag_ratio=0.20),
                floor=1.25,
            )

        self.inspect(0.7)
        self.clear_beat()


class LeNEPA03PredictionLoss(LenepaScene):
    """The projected vectors literally become a difference and then a scalar."""

    def construct(self):
        title = scene_title("Where the prediction loss lives")
        pred = latent_column(color=PREDICTION, label=R"\hat z_t", height=1.45)
        target = latent_column(
            np.array([0.44, -0.18, 0.74, -0.50, 0.08, 0.64, -0.33]),
            color=NEXT_TARGET,
            label=R"z_{t+1}",
            height=1.45,
        )
        inputs = VGroup(pred, target).arrange(DOWN, buff=0.64).move_to(4.85 * LEFT)
        projectors = VGroup(
            mlp_network(color=PROJECTOR),
            mlp_network(color=PROJECTOR),
        ).arrange(DOWN, buff=0.50).move_to(1.65 * LEFT)
        for network, vector in zip(projectors, inputs):
            network.move_to(np.array([-1.65, vector.get_y() + 0.15, 0.0]))
        in_arrows = VGroup(*(
            Arrow(vector.get_right(), network.get_left(), buff=0.10,
                  stroke_width=2.2).set_color(PROJECTOR)
            for vector, network in zip(inputs, projectors)
        ))
        shared_brace = Brace(projectors, RIGHT, color=PROJECTOR)
        shared_label = ty.words("same weights", size=ty.LABEL, color=PROJECTOR)
        shared_label.next_to(shared_brace, RIGHT, buff=0.14)

        projected = VGroup(
            latent_column(color=PREDICTION, label=R"h_\psi(\hat z_t)", height=1.16),
            latent_column(
                np.array([0.40, -0.12, 0.67, -0.48, 0.02, 0.58, -0.28]),
                color=NEXT_TARGET,
                label=R"h_\psi(z_{t+1})",
                height=1.16,
            ),
        ).arrange(DOWN, buff=0.76).move_to(3.45 * RIGHT)
        out_arrows = VGroup(*(
            Arrow(network.get_right(), vector.get_left(), buff=0.10,
                  stroke_width=2.2).set_color(PROJECTOR)
            for network, vector in zip(projectors, projected)
        ))
        dims = ty.maths(R"D=192\quad\longrightarrow\quad d=64",
                        size=ty.EQ, color=PROJECTOR)
        dims.to_edge(DOWN, buff=0.40)

        with self.voiceover(
            text="LeNEPA does not compare the two D-dimensional vectors "
                 "directly. Both pass through the same small projector. The "
                 "two paths share weights. In the main experiments, this maps "
                 "a 192-dimensional backbone vector into a 64-dimensional "
                 "loss space."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(inputs), run_time=0.75)
            self.play(LaggedStart(*[FadeIn(net) for net in projectors], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(a) for a in in_arrows], lag_ratio=0.25),
                      run_time=1.25)
            self.play(Create(shared_brace), FadeIn(shared_label), run_time=0.75)
            self.across(
                tracker,
                LaggedStart(*[GrowArrow(a) for a in out_arrows], lag_ratio=0.22),
                LaggedStart(*[FadeIn(vector) for vector in projected], lag_ratio=0.22),
                FadeIn(dims, shift=0.06 * UP),
                floor=1.7,
            )

        diff = latent_column(
            np.array([0.08, -0.06, 0.15, -0.12, 0.09, 0.12, -0.10]),
            color=ERROR,
            label=R"\Delta_t",
            height=1.65,
        ).move_to(0.40 * UP)
        subtract = ty.maths(
            R"\Delta_t=h_\psi(\hat z_t)-h_\psi(z_{t+1})",
            size=ty.EQ_DISPLAY,
            color=INK,
        ).move_to(2.10 * DOWN)

        with self.voiceover(
            text="Line up the projected columns and subtract entry by entry. "
                 "The difference is one d-dimensional vector. Squaring and "
                 "summing its entries contracts the column to one scalar "
                 "squared distance."
        ) as tracker:
            self.play(
                FadeOut(VGroup(inputs, projectors, in_arrows, out_arrows,
                               shared_brace, shared_label, dims)),
                projected[0].animate.move_to(2.4 * LEFT + 0.35 * UP),
                projected[1].animate.move_to(2.4 * RIGHT + 0.35 * UP),
                run_time=0.85,
            )
            self.play(
                Transform(projected[0], diff),
                Indicate(projected[1], color=NEXT_TARGET, scale_factor=1.025),
                FadeIn(subtract, shift=0.08 * UP),
                run_time=1.35,
            )
            diff = projected[0]
            scalar = scalar_dot(ERROR, 0.16).move_to(diff.get_center())
            scalar_label = ty.maths(R"\|\Delta_t\|_2^2",
                                    size=ty.EQ_DISPLAY, color=ERROR)
            scalar_label.next_to(scalar, RIGHT, buff=0.35)
            self.across(
                tracker,
                FadeOut(diff, scale=0.15),
                FadeIn(scalar, scale=0.15),
                FadeIn(scalar_label),
                projected[1].animate.set_opacity(0.18),
                floor=1.35,
            )

        loss_grid = VGroup(*(
            VGroup(*(scalar_dot(ERROR, 0.07) for _ in range(6)))
            .arrange(RIGHT, buff=0.25)
            for _ in range(4)
        )).arrange(DOWN, buff=0.28).move_to(3.95 * LEFT + 0.20 * DOWN)
        grid_brace = Brace(loss_grid, RIGHT, color=ERROR)
        average_arrow = Arrow(grid_brace.get_right(), 0.35 * LEFT,
                              buff=0.15, stroke_width=2.5).set_color(ERROR)
        loss_eq = ty.maths(
            R"\mathcal L_{\rm pred}="
            R"\frac{1}{B(T-1)}\sum_{b,t}"
            R"\|h_\psi(\hat z_{b,t})-h_\psi(z_{b,t+1})\|_2^2",
            size=ty.EQ,
            color=INK,
        ).move_to(2.35 * RIGHT + 0.10 * DOWN)
        both_branches = ty.words("gradients through both branches",
                                 size=ty.LABEL, color=PREDICTION)
        both_branches.to_edge(DOWN, buff=0.38)
        backward_arrows = VGroup(
            Arrow(1.8 * RIGHT + 2.65 * DOWN, 4.2 * LEFT + 2.65 * DOWN,
                  stroke_width=2.2).set_color(PREDICTION),
            Arrow(1.8 * RIGHT + 2.90 * DOWN, 4.2 * LEFT + 2.90 * DOWN,
                  stroke_width=2.2).set_color(PREDICTION),
        )

        with self.voiceover(
            text="There is one such scalar for every sample and every usable "
                 "time step; their average is the prediction loss. Unlike "
                 "vanilla NEPA, the target branch is not stopped, so gradients "
                 "flow through both sides. Stabilization must come elsewhere."
        ) as tracker:
            self.play(
                FadeOut(VGroup(projected[1], subtract, scalar, scalar_label)),
                LaggedStart(*[FadeIn(row) for row in loss_grid], lag_ratio=0.16),
                run_time=1.0,
            )
            self.play(Create(grid_brace), GrowArrow(average_arrow),
                      FadeIn(loss_eq, shift=0.08 * RIGHT), run_time=1.4)
            self.across(
                tracker,
                LaggedStart(*[GrowArrow(a) for a in backward_arrows], lag_ratio=0.18),
                FadeIn(both_branches),
                floor=1.25,
            )

        self.inspect(0.8)
        self.clear_beat()


class LeNEPA04TemporalSIGReg(LenepaScene):
    """Make within-sample temporal collapse visible despite global spread."""

    def construct(self):
        title = scene_title("SIGReg acts across time")
        centres = [np.array([-3.6, 0.95, 0]), np.array([0.0, 0.10, 0]),
                   np.array([3.55, -0.75, 0])]
        axes = VGroup(*(mini_axes(center, width=2.7, height=1.65) for center in centres))
        rng = np.random.default_rng(44)
        clouds = VGroup()
        for sample, center in enumerate(centres):
            dots = VGroup(*(
                Dot(center + np.array([
                    rng.normal(scale=0.62), rng.normal(scale=0.34), 0,
                ]), radius=0.075).set_fill(INPUT, 0.95)
                for _ in range(7)
            ))
            label = ty.maths(rf"b={sample + 1}", size=ty.LABEL, color=MUTED)
            label.next_to(axes[sample], DOWN, buff=0.12)
            clouds.add(VGroup(dots, label))
        aggregate = SurroundingRectangle(VGroup(axes, clouds), buff=0.24)
        aggregate.set_stroke(INPUT, 1.6, opacity=0.55)
        aggregate_label = ty.words("aggregate batch is spread out",
                                   size=ty.CAPTION, color=INPUT)
        aggregate_label.next_to(aggregate, DOWN, buff=0.14)

        with self.voiceover(
            text="A batch-wide regularizer can see plenty of global spread. "
                 "Different samples occupy different regions, so the aggregate "
                 "cloud looks healthy. But that view hides a failure mode "
                 "inside each sequence."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(axes), run_time=0.65)
            self.play(LaggedStart(*[FadeIn(cloud[0]) for cloud in clouds],
                                  lag_ratio=0.20),
                      LaggedStart(*[FadeIn(cloud[1]) for cloud in clouds],
                                  lag_ratio=0.20), run_time=1.35)
            self.across(tracker, Create(aggregate), FadeIn(aggregate_label), floor=1.2)

        collapsed_targets = []
        for index, dot in enumerate(clouds[0][0]):
            angle = TAU * index / len(clouds[0][0])
            collapsed_targets.append(
                centres[0] + 0.10 * np.array([np.cos(angle), np.sin(angle), 0])
            )
        time_labels = VGroup(*(
            ty.maths(rf"u_{index + 1}", size=ty.LABEL, color=INPUT)
            for index in range(7)
        ))
        time_labels.arrange(RIGHT, buff=0.36).move_to(1.75 * DOWN)
        temporal_row = VGroup(*(dot.copy() for dot in clouds[0][0]))
        for dot, label in zip(temporal_row, time_labels):
            dot.next_to(label, UP, buff=0.13)
        temporal_brace = Brace(VGroup(temporal_row, time_labels), DOWN, color=SIGREG)
        temporal_sig = ty.maths(
            R"\operatorname{SIGReg}\big(\{u_{b,t}\}_{t=1}^{T}\big)",
            size=ty.EQ,
            color=SIGREG,
        ).next_to(temporal_brace, DOWN, buff=0.14)

        with self.voiceover(
            text="Inside a single time series, all seven tokens can still "
                 "collapse toward one point while other samples keep the batch "
                 "spread out. A pooled check may miss this. LeNEPA groups tokens "
                 "by sample and applies SIGReg along that row's time axis."
        ) as tracker:
            self.play(
                aggregate.animate.set_stroke(MUTED, opacity=0.22),
                aggregate_label.animate.set_color(MUTED),
                *(dot.animate.move_to(point)
                  for dot, point in zip(clouds[0][0], collapsed_targets)),
                run_time=1.45,
            )
            self.play(
                FadeOut(VGroup(axes, clouds, aggregate, aggregate_label)),
                FadeIn(time_labels),
                TransformFromCopy(clouds[0][0], temporal_row),
                run_time=1.1,
            )
            self.across(
                tracker,
                GrowFromCenter(temporal_brace),
                FadeIn(temporal_sig, shift=0.06 * UP),
                floor=1.35,
            )

        layer0 = caption_pill("patch layer 0", color=INPUT, width=2.55)
        layer8 = caption_pill("Transformer layer 8", color=BACKBONE, width=3.45)
        taps = VGroup(layer0, layer8).arrange(DOWN, buff=0.65).move_to(4.25 * LEFT)
        tap_arrows = VGroup(*(
            Arrow(tap.get_right(), 0.95 * LEFT + tap.get_y() * UP,
                  buff=0.10, stroke_width=2.2).set_color(SIGREG)
            for tap in taps
        ))
        equation = ty.maths(
            R"\mathcal L_{\rm SIG}^{\rm time}="
            R"\frac{1}{B|L_T|}\sum_{\ell\in L_T}\sum_b"
            R"\operatorname{SIGReg}\big(\{u^{(\ell)}_{b,t}\}_{t=1}^{T}\big)",
            size=ty.EQ,
            color=INK,
        ).move_to(2.30 * RIGHT + 0.40 * UP)
        layers_label = ty.maths(R"L_T=\{0,8\}", size=ty.EQ_DISPLAY, color=SIGREG)
        layers_label.next_to(equation, DOWN, buff=0.55)

        with self.voiceover(
            text="That temporal regularizer is tapped at the patch embeddings "
                 "and after Transformer layer eight. Averaging over samples "
                 "and those layers gives the temporal SIGReg term. "
                 "Among the paper's single-component placements, this was the "
                 "one with sustained gains on both main datasets."
        ) as tracker:
            self.play(FadeOut(VGroup(temporal_row, time_labels, temporal_brace,
                                     temporal_sig)), FadeIn(taps), run_time=0.85)
            self.play(LaggedStart(*[GrowArrow(a) for a in tap_arrows], lag_ratio=0.22),
                      FadeIn(equation, shift=0.08 * RIGHT), run_time=1.35)
            self.across(tracker, FadeIn(layers_label, shift=0.08 * UP), floor=1.2)

        self.inspect(0.8)
        self.clear_beat()


class LeNEPA05Objective(LenepaScene):
    """Assemble the objective, then discard the training-only head."""

    def construct(self):
        title = scene_title("The complete training step")
        pred_loss = caption_pill(R"prediction loss", color=ERROR, width=2.95)
        sig_loss = caption_pill(R"temporal SIGReg", color=SIGREG, width=3.25)
        terms = VGroup(pred_loss, sig_loss).arrange(RIGHT, buff=1.05).move_to(0.95 * UP)
        plus = ty.maths("+", size=ty.EQ_DISPLAY, color=INK).move_to(terms.get_center())
        equation = ty.maths(
            R"\mathcal L=\lambda_{\rm pred}\mathcal L_{\rm pred}"
            R"+\lambda_T\mathcal L_{\rm SIG}^{\rm time}",
            size=ty.EQ_DISPLAY,
            color=INK,
        ).move_to(0.55 * DOWN)
        weights = ty.maths(
            R"\lambda_{\rm pred}=1,\qquad\lambda_T=20",
            size=ty.EQ,
            color=MUTED,
        ).next_to(equation, DOWN, buff=0.48)

        with self.voiceover(
            text="Training combines the two scalars. The prediction term has "
                 "weight one; temporal SIGReg has weight twenty in the main "
                 "configuration. One term teaches what comes next; the other "
                 "resists temporal collapse."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(terms), FadeIn(plus), run_time=0.8)
            self.play(TransformFromCopy(terms, equation), FadeIn(equation), run_time=1.35)
            self.across(tracker, FadeIn(weights, shift=0.08 * UP), floor=1.15)

        patch = caption_pill("patch embedding", color=KEEP, width=2.9)
        backbone = caption_pill("causal Transformer", color=KEEP, width=3.35)
        projector = caption_pill("projector", color=PROJECTOR, width=2.25)
        losses = caption_pill("losses", color=ERROR, width=1.85)
        pipeline = VGroup(patch, backbone, projector, losses).arrange(RIGHT, buff=0.42)
        pipeline.move_to(0.15 * DOWN)
        pipe_arrows = VGroup(*(
            Arrow(a.get_right(), b.get_left(), buff=0.08,
                  stroke_width=2.1).set_color(MUTED)
            for a, b in zip(pipeline, pipeline[1:])
        ))
        keep_label = ty.words("KEEP FOR EVALUATION", size=ty.CAPTION, color=KEEP)
        keep_label.next_to(VGroup(patch, backbone), UP, buff=0.45)
        discard_label = ty.words("TRAINING ONLY", size=ty.CAPTION, color=DISCARD)
        discard_label.next_to(VGroup(projector, losses), UP, buff=0.45)
        blade = Line(0.82 * UP, 0.82 * DOWN).set_stroke(INK, 5)
        blade.move_to((backbone.get_right() + projector.get_left()) / 2 + 2.6 * UP)

        with self.voiceover(
            text="Once training ends, the cut falls after the causal "
                 "Transformer. The projector and both losses disappear. Only "
                 "the patch embedding and encoder survive for frozen-feature "
                 "evaluation. The objective shaped a disposable space."
        ) as tracker:
            self.play(FadeOut(VGroup(terms, plus, equation, weights)),
                      FadeIn(pipeline), FadeIn(pipe_arrows),
                      FadeIn(keep_label), FadeIn(discard_label), run_time=1.0)
            cut_y = pipeline.get_y()
            self.play(blade.animate.move_to(np.array([blade.get_x(), cut_y, 0.0])),
                      run_time=0.75, rate_func=linear)
            self.play(
                FadeOut(VGroup(projector, losses, pipe_arrows[1:], discard_label),
                        shift=0.55 * DOWN),
                VGroup(patch, backbone, pipe_arrows[0], keep_label)
                .animate.move_to(ORIGIN).scale(1.10),
                FadeOut(blade),
                run_time=1.15,
            )
            self.across(tracker,
                        Indicate(VGroup(patch, backbone), color=KEEP,
                                 scale_factor=1.025), floor=1.0)

        self.inspect(0.7)
        self.clear_beat()


class LeNEPA06Protocol(LenepaScene):
    """Explain recipe reuse without implying checkpoint transfer."""

    def construct(self):
        title = scene_title("What experiment is this?")
        column_titles = VGroup(
            ty.words("PTB-XL", size=ty.STATEMENT, color=INK),
            ty.words("Diag", size=ty.STATEMENT, color=INK),
        )
        column_titles[0].move_to(1.55 * LEFT + 2.15 * UP)
        column_titles[1].move_to(2.65 * RIGHT + 2.15 * UP)
        row_labels = VGroup(
            ty.words("LeNEPA", size=ty.CAPTION, color=PREDICTION),
            ty.words("ECG-tuned JEPA", size=ty.CAPTION, color=NEXT_TARGET),
        )
        row_labels[0].move_to(5.0 * LEFT + 0.70 * UP)
        row_labels[1].move_to(5.0 * LEFT + 0.85 * DOWN)

        lenepa_recipe = caption_pill("same LeNEPA recipe", color=PREDICTION, width=3.05)
        jepa_recipe = caption_pill("same JEPA recipe", color=NEXT_TARGET, width=3.05)
        recipe_cards = VGroup(lenepa_recipe, jepa_recipe).arrange(DOWN, buff=0.72)
        recipe_cards.move_to(0.35 * LEFT + 0.10 * DOWN)
        targets = []
        for row, recipe in enumerate(recipe_cards):
            for x in (-1.55, 2.65):
                target = recipe.copy().scale(0.82)
                target.move_to(np.array([x, 0.70 - 1.55 * row, 0.0]))
                targets.append(target)
        target_group = VGroup(*targets)
        train_labels = VGroup(*(
            ty.words("retrain weights", size=ty.LABEL, color=MUTED)
            .next_to(target, DOWN, buff=0.12)
            for target in target_group
        ))
        no_transfer = caption_pill("recipe reuse — no checkpoint transfer",
                                   color=INK, width=6.25)
        no_transfer.to_edge(DOWN, buff=0.43)

        with self.voiceover(
            text="The experiment holds each method's recipe fixed, then "
                 "restarts training on each dataset. LeNEPA is trained once on "
                 "PTB-XL and separately on Diag; ECG-tuned JEPA is too. What "
                 "transfers is the configuration, not a checkpoint."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(column_titles), FadeIn(row_labels),
                      FadeIn(recipe_cards), run_time=0.9)
            self.play(
                LaggedStart(*(
                    TransformFromCopy(recipe_cards[index // 2], target)
                    for index, target in enumerate(target_group)
                ), lag_ratio=0.17),
                run_time=1.8,
            )
            self.play(FadeOut(recipe_cards),
                      LaggedStart(*[FadeIn(label) for label in train_labels],
                                  lag_ratio=0.10), run_time=0.75)
            self.across(tracker, FadeIn(no_transfer, shift=0.08 * UP), floor=1.2)

        facts = VGroup(
            caption_pill("20,000 updates", color=MUTED),
            caption_pill("5 seeds", color=MUTED),
            caption_pill("frozen probes", color=MUTED),
        ).arrange(RIGHT, buff=0.42).move_to(2.55 * DOWN)

        with self.voiceover(
            text="Both recipes were chosen using PTB-XL work; neither was "
                 "retuned for Diag. The comparison therefore asks how costly "
                 "unchanged recipe reuse is under twenty thousand updates, "
                 "five seeds, and frozen probes—not for the best Diag-tuned "
                 "version of either method."
        ) as tracker:
            self.play(FadeOut(no_transfer), target_group.animate.shift(0.35 * UP),
                      train_labels.animate.shift(0.35 * UP), run_time=0.65)
            self.across(tracker,
                        LaggedStart(*[FadeIn(fact) for fact in facts], lag_ratio=0.22),
                        floor=1.3)

        self.inspect(0.8)
        self.clear_beat()


class LeNEPA07Results(LenepaScene):
    """Two honest result panels, then learning dynamics and qualifications."""

    def _result_panel(self, dataset: str, rows: list[tuple[str, str, str]],
                      *, accent: str) -> VGroup:
        box = RoundedRectangle(width=5.65, height=3.0, corner_radius=0.15)
        box.set_stroke(accent, 1.7, opacity=0.65).set_fill(GRID, 0.08)
        title = ty.words(dataset, size=ty.STATEMENT, color=INK)
        title.next_to(box.get_top(), DOWN, buff=0.25)
        headers = VGroup(
            ty.words("model", size=ty.LABEL, color=MUTED),
            ty.words("AUROC", size=ty.LABEL, color=MUTED),
            ty.words("AUPRC", size=ty.LABEL, color=MUTED),
        ).arrange(RIGHT, buff=0.70)
        headers.move_to(box.get_center() + 0.55 * UP)
        data_rows = VGroup()
        for name, auroc, auprc in rows:
            row_color = PREDICTION if name == "LeNEPA" else NEXT_TARGET
            row = VGroup(
                ty.words(name, size=ty.CAPTION, color=row_color),
                ty.maths(auroc, size=ty.EQ, color=row_color),
                ty.maths(auprc, size=ty.EQ, color=row_color),
            )
            row[0].set_width(1.55)
            row.arrange(RIGHT, buff=0.66)
            data_rows.add(row)
        data_rows.arrange(DOWN, buff=0.34)
        data_rows.next_to(headers, DOWN, buff=0.32)
        return VGroup(box, title, headers, data_rows)

    def construct(self):
        title = scene_title("What happened?")
        ptb = self._result_panel(
            "PTB-XL",
            [("JEPA best", ".892", ".298"), ("LeNEPA", ".880", ".285")],
            accent=NEXT_TARGET,
        ).move_to(3.0 * LEFT + 0.25 * UP)
        diag = self._result_panel(
            "Diag",
            [("JEPA CLS", ".880", ".597"), ("LeNEPA", ".920", ".650")],
            accent=PREDICTION,
        ).move_to(3.0 * RIGHT + 0.25 * UP)
        fixed_recipe = ty.words("same fixed-recipe rule",
                                size=ty.CAPTION, color=MUTED)
        fixed_recipe.to_edge(DOWN, buff=0.45)

        with self.voiceover(
            text="On PTB-XL, the ECG-tuned JEPA recipe is slightly stronger: "
                 "its best readout reaches point eight nine two AUROC and point "
                 "two nine eight AUPRC. Under the fixed-recipe rule on "
                 "Diag, LeNEPA reaches point nine two zero and point six five "
                 "zero, clearly ahead on classification."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(ptb[0]), FadeIn(ptb[1]), run_time=0.65)
            self.play(FadeIn(ptb[2]),
                      LaggedStart(*[FadeIn(row) for row in ptb[3]], lag_ratio=0.22),
                      run_time=1.25)
            self.play(FadeIn(diag[0]), FadeIn(diag[1]), FadeIn(diag[2]),
                      LaggedStart(*[FadeIn(row) for row in diag[3]], lag_ratio=0.22),
                      run_time=1.45)
            self.across(tracker, FadeIn(fixed_recipe), floor=1.1)

        speed_title = ty.words("80% of final gain", size=ty.STATEMENT, color=INK)
        speed_title.move_to(2.05 * UP)
        lenepa_line = NumberLine(x_range=(0, 10, 1), length=5.6,
                                 include_numbers=False, include_tip=False)
        jepa_line = lenepa_line.copy()
        lines = VGroup(lenepa_line, jepa_line).arrange(DOWN, buff=0.88).move_to(0.15 * DOWN)
        lines.set_stroke(AXIS, 2)
        labels = VGroup(
            ty.words("LeNEPA", size=ty.CAPTION, color=PREDICTION),
            ty.words("JEPA", size=ty.CAPTION, color=NEXT_TARGET),
        )
        for label, line in zip(labels, lines):
            label.next_to(line, LEFT, buff=0.32)
        lenepa_band = Line(lenepa_line.n2p(2), lenepa_line.n2p(5))
        lenepa_band.set_stroke(PREDICTION, 10)
        jepa_band = Line(jepa_line.n2p(5), jepa_line.n2p(10))
        jepa_band.set_stroke(NEXT_TARGET, 10)
        band_labels = VGroup(
            ty.words("2–5k updates", size=ty.LABEL, color=PREDICTION)
            .next_to(lenepa_band, UP, buff=0.15),
            ty.words("5–10k updates", size=ty.LABEL, color=NEXT_TARGET)
            .next_to(jepa_band, UP, buff=0.15),
        )

        with self.voiceover(
            text="The learning curves also rise earlier. LeNEPA reaches eighty "
                 "percent of its final AUROC or AUPRC gain after roughly two to "
                 "five thousand updates; JEPA takes about five to ten thousand. "
                 "These coarse, fixed-horizon observations are not a universal "
                 "speed guarantee."
        ) as tracker:
            self.play(FadeOut(VGroup(ptb, diag, fixed_recipe)), FadeIn(speed_title),
                      FadeIn(lines), FadeIn(labels), run_time=0.85)
            self.play(Create(lenepa_band), FadeIn(band_labels[0]), run_time=1.0)
            self.across(tracker, Create(jepa_band), FadeIn(band_labels[1]), floor=1.15)

        mixed = caption_pill("dense Diag regression: mixed", color=ERROR, width=5.0)
        ucr = ty.maths(R"77.65\%", size=ty.EQ_HERO, color=PREDICTION)
        ucr_label = ty.words("UCR-128 mean accuracy", size=ty.CAPTION, color=INK)
        ucr_note = ty.words("single seed • best checkpoint",
                            size=ty.LABEL, color=MUTED)
        ucr_group = VGroup(ucr, ucr_label, ucr_note).arrange(DOWN, buff=0.22)
        ucr_group.move_to(2.85 * RIGHT + 0.20 * DOWN)
        baselines = VGroup(
            ty.words("Mantis  78.81", size=ty.LABEL, color=MUTED),
            ty.words("MOMENT  77.89", size=ty.LABEL, color=MUTED),
            ty.words("NuTime  77.32", size=ty.LABEL, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        baselines.move_to(3.15 * LEFT + 0.15 * DOWN)

        with self.voiceover(
            text="The win is not universal. NEPA with a projector beats "
                 "LeNEPA on several dense Diag regression metrics, so the "
                 "cleanest advantage is classification and training dynamics. "
                 "A frozen UCR check lands at 77.65 percent near the listed "
                 "baselines, but uses one seed and the best checkpoint."
        ) as tracker:
            self.play(FadeOut(VGroup(speed_title, lines, labels, lenepa_band,
                                     jepa_band, band_labels)),
                      FadeIn(mixed), run_time=0.8)
            self.play(mixed.animate.move_to(2.35 * UP),
                      FadeIn(baselines, shift=0.08 * RIGHT), run_time=1.0)
            self.across(tracker, FadeIn(ucr_group, shift=0.08 * UP), floor=1.4)

        self.inspect(1.0)
        self.clear_beat()


class LeNEPA08Landing(LenepaScene):
    """Return to the signal and leave the method's conceptual identity."""

    def construct(self):
        title = scene_title("LeNEPA in one pass")
        signal = ParametricFunction(
            lambda t: np.array([
                -5.55 + 1.75 * t,
                0.36 * np.sin(4.2 * t) + 0.15 * np.sin(8.3 * t),
                0,
            ]),
            t_range=(0, 1, 0.02),
        ).set_stroke(INPUT, 3.0)
        signal_label = ty.words("signal", size=ty.LABEL, color=INPUT)
        signal_label.next_to(signal, DOWN, buff=0.20)

        tokens = latent_row([R"z_1", R"z_2", R"z_3"], color=INPUT,
                            height=0.90, buff=0.38, seed=82)
        tokens.scale(0.90).move_to(2.65 * LEFT)
        transformer = caption_pill("causal Transformer", color=BACKBONE, width=3.15)
        transformer.move_to(0.20 * RIGHT)
        prediction = caption_pill("next-latent prediction", color=PREDICTION, width=3.65)
        prediction.move_to(3.75 * RIGHT + 0.72 * UP)
        sigreg = caption_pill("temporal SIGReg", color=SIGREG, width=3.20)
        sigreg.move_to(3.75 * RIGHT + 0.78 * DOWN)
        flow_objects = [VGroup(signal, signal_label), tokens, transformer]
        arrows = VGroup(
            Arrow(signal.get_right(), tokens.get_left(), buff=0.10,
                  stroke_width=2.3).set_color(INPUT),
            Arrow(tokens.get_right(), transformer.get_left(), buff=0.10,
                  stroke_width=2.3).set_color(BACKBONE),
            Arrow(transformer.get_right(), prediction.get_left(), buff=0.10,
                  stroke_width=2.3).set_color(PREDICTION),
            Arrow(transformer.get_right(), sigreg.get_left(), buff=0.10,
                  stroke_width=2.3).set_color(SIGREG),
        )

        with self.voiceover(
            text="Run the original signal through once more. Convolutional "
                 "patches become latent tokens. A causal Transformer predicts "
                 "the next one, and temporal SIGReg keeps each sample's token "
                 "sequence from collapsing. After training, only the encoder "
                 "remains."
        ) as tracker:
            self.play(FadeIn(title), Create(signal), FadeIn(signal_label), run_time=0.75)
            self.play(GrowArrow(arrows[0]), TransformFromCopy(signal, tokens), run_time=1.0)
            self.play(GrowArrow(arrows[1]), FadeIn(transformer), run_time=0.8)
            self.across(
                tracker,
                LaggedStart(GrowArrow(arrows[2]), FadeIn(prediction),
                            GrowArrow(arrows[3]), FadeIn(sigreg), lag_ratio=0.20),
                floor=1.6,
            )

        phrases = VGroup(
            ty.words("No augmentations", size=ty.STATEMENT, color=INPUT),
            ty.words("No EMA teacher", size=ty.STATEMENT, color=PROJECTOR),
            ty.words("Predict the next latent", size=ty.STATEMENT, color=PREDICTION),
        ).arrange(DOWN, buff=0.42)
        subline = ty.words("SIGReg preserves temporal spread.",
                           size=ty.CAPTION, color=SIGREG)
        subline.next_to(phrases, DOWN, buff=0.62)

        with self.voiceover(
            text="So LeNEPA's identity is compact: no augmentations, no EMA "
                 "teacher, and a direct prediction of the next latent. SIGReg "
                 "supplies the temporal spread that stabilizes training."
        ) as tracker:
            self.play(FadeOut(VGroup(*flow_objects, arrows, prediction, sigreg)),
                      FadeIn(phrases.move_to(0.30 * UP)), run_time=0.9)
            self.across(tracker, FadeIn(subline, shift=0.08 * UP), floor=1.2)

        self.inspect(1.4)
        self.clear_beat()
