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
import random
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import type as ty
from common.data import (
    BATCH_B,
    BATCH_T,
    BATCH_TOKENS,
    COLLAPSED_TOKEN,
    LATENT_SCALE,
    LAYER8_ROW,
    MIXED_VALUES,
    PRD_ROW_Y,
    PRED_H,
    TGT_ROW_Y,
    TIME_DIR,
    TOKEN_H,
    TOKEN_VALUES,
    latent,
)
from common.project import PlaneProjectionRig
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
    VIEW_GLOBAL,
)
from common.scene import LenepaScene
from common.visuals import (
    caption_pill,
    decimal_entries,
    depth_plates,
    latent_column,
    latent_row,
    LayerMap,
    mini_axes,
    numeric_embedding,
    scalar_dot,
    span_bracket,
    transformer_block,
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

        # Brief callbacks to the objectives already established earlier in the
        # larger EPA-variants video.  They reuse the same signal and occupy the
        # frame sequentially; this is orientation, not a second explanation.
        mask_index = 3
        mask_box = patch_boxes[mask_index].copy()
        mask_box.set_stroke(ERROR, 2.8, opacity=1.0)
        mask_box.set_fill(ERROR, opacity=0.28)
        mask_mark = ty.maths(R"?", size=ty.EQ_HERO, color=INK)
        mask_mark.move_to(mask_box)
        masked_prediction = patches[mask_index].copy()
        masked_prediction.set_stroke(NEXT_TARGET, 3.8, opacity=1.0)

        # LeJEPA callback: a long span and two shorter crops are marked without
        # nesting three boxes on top of one another.  Their small embedding
        # glyphs then gather into one alignment neighborhood below the signal.
        global_y = signal_y + 1.08
        global_left = bounds[0] + 0.52
        global_right = bounds[-1] - 1.12
        global_span = VGroup(
            Line([global_left, global_y, 0], [global_right, global_y, 0]),
            Line([global_left, global_y, 0], [global_left, global_y - 0.20, 0]),
            Line([global_right, global_y, 0], [global_right, global_y - 0.20, 0]),
        ).set_stroke(VIEW_GLOBAL, 2.8)
        global_label = ty.words("global view", size=ty.LABEL, color=VIEW_GLOBAL)
        global_label.next_to(global_span, UP, buff=0.10)
        local_crops = VGroup(
            RoundedRectangle(width=2.20, height=1.45, corner_radius=0.08)
            .move_to(np.array([-2.65, signal_y, 0.0])),
            RoundedRectangle(width=2.20, height=1.45, corner_radius=0.08)
            .move_to(np.array([2.75, signal_y, 0.0])),
        )
        local_crops.set_stroke(KEEP, 2.5).set_fill(KEEP, opacity=0.035)
        local_labels = VGroup(*(
            ty.words("local view", size=ty.LABEL, color=KEEP)
            .next_to(crop, DOWN, buff=0.16)
            for crop in local_crops
        ))

        def view_embedding(color: str, x: float) -> VGroup:
            cells = VGroup(*(
                RoundedRectangle(width=0.18, height=0.11, corner_radius=0.025)
                .set_stroke(color, 1.1)
                .set_fill(color, opacity=0.62 - 0.10 * index)
                for index in range(4)
            ))
            cells.arrange(DOWN, buff=0.035)
            cells.move_to(np.array([x, -1.05, 0.0]))
            return cells

        view_embeddings = VGroup(
            view_embedding(VIEW_GLOBAL, -2.45),
            view_embedding(KEEP, 0.0),
            view_embedding(KEEP, 2.45),
        )
        aligned_positions = (
            np.array([-0.34, -1.10, 0.0]),
            np.array([0.0, -0.96, 0.0]),
            np.array([0.34, -1.10, 0.0]),
        )
        alignment_ring = Ellipse(width=1.42, height=0.92)
        alignment_ring.move_to(np.array([0.0, -1.06, 0.0]))
        alignment_ring.set_stroke(INK, 1.6, opacity=0.72)
        alignment_label = ty.words("align the views", size=ty.LABEL, color=INK)
        alignment_label.next_to(alignment_ring, DOWN, buff=0.14)

        preview_tokens = VGroup()
        for index, box in enumerate(patch_boxes):
            token = VGroup(*(
                Dot(radius=0.040).set_fill(INPUT, 1).set_stroke(INPUT, 0)
                for _ in range(5)
            ))
            token.arrange(DOWN, buff=0.055)
            label = ty.maths(rf"z_{index + 1}", size=ty.LABEL, color=INPUT)
            label.next_to(token, DOWN, buff=0.10)
            token_group = VGroup(token, label)
            token_group.move_to(np.array([box.get_x(), -0.42, 0.0]))
            preview_tokens.add(token_group)
        preview_down_arrows = VGroup(*(
            Arrow(
                box.get_bottom(), token.get_top(), buff=0.10,
                stroke_width=1.6, max_tip_length_to_length_ratio=0.22,
            ).set_color(INPUT).set_opacity(0.55)
            for box, token in zip(patch_boxes, preview_tokens)
        ))
        history = VGroup(*preview_tokens[:3])
        history_box = SurroundingRectangle(history, buff=0.18)
        history_box.set_stroke(PREDICTION, 2.2).set_fill(PREDICTION, 0.025)
        next_box = SurroundingRectangle(preview_tokens[3], buff=0.16)
        next_box.set_stroke(NEXT_TARGET, 2.4).set_fill(NEXT_TARGET, 0.04)
        next_arrow = Arrow(
            history_box.get_right(), next_box.get_left(), buff=0.10,
            stroke_width=2.6, max_tip_length_to_length_ratio=0.20,
        ).set_color(PREDICTION)
        next_label = ty.words("predict next", size=ty.TICK, color=PREDICTION)
        next_label.scale(0.82)
        next_label.next_to(next_arrow, UP, buff=0.18).shift(0.06 * UP)

        nepa_title = ty.title("NEPA").set_color(PREDICTION)
        nepa_title.move_to(2.55 * DOWN)
        nepa_expansion = ty.words(
            "Next-Embedding Predictive Autoregression",
            size=ty.STATEMENT,
            color=INK,
        )
        nepa_expansion.next_to(nepa_title, UP, buff=0.18)
        nepa_card = VGroup(nepa_expansion, nepa_title)
        lenepa_title = ty.title("LeNEPA").set_color(PREDICTION)
        lenepa_title.move_to(nepa_title)
        lenepa_subtitle = ty.words(
            "no masked or cropped views",
            size=ty.CAPTION,
            color=MUTED,
        )
        lenepa_subtitle.move_to(nepa_expansion)
        lenepa_card = VGroup(lenepa_subtitle, lenepa_title)

        with self.voiceover(
            text="Suppose we want to learn a representation of this time-series "
                 "signal. We could mask part of it and train the model to predict "
                 "what is missing."
        ) as tracker:
            self.play(Create(baseline), Create(patches, lag_ratio=0.025), run_time=1.9)
            self.play(
                LaggedStart(*[FadeIn(box) for box in patch_boxes], lag_ratio=0.08),
                run_time=0.9,
            )
            self.play(
                patches[mask_index].animate.set_stroke(opacity=0.05),
                FadeIn(mask_box),
                FadeIn(mask_mark),
                run_time=0.8,
            )
            self.play(
                FadeOut(mask_mark),
                Create(masked_prediction),
                mask_box.animate.set_fill(opacity=0.05),
                run_time=1.25,
            )
            self.wait(max(0.1, tracker.get_remaining_duration()))
        # Let the completed prediction register before changing objectives.
        self.wait(0.65)

        with self.voiceover(
            text="Or, as in LeJEPA, we could take global and local crops and "
                 "align the representations of those views."
        ) as tracker:
            self.play(
                FadeOut(VGroup(mask_box, masked_prediction, patch_boxes)),
                patches[mask_index].animate.set_stroke(opacity=1.0),
                run_time=0.65,
            )
            self.play(
                Create(global_span),
                FadeIn(global_label),
                LaggedStart(*[FadeIn(crop) for crop in local_crops], lag_ratio=0.15),
                LaggedStart(*[FadeIn(label) for label in local_labels], lag_ratio=0.15),
                run_time=1.15,
            )
            self.play(
                LaggedStart(*(
                    FadeIn(embedding, shift=0.15 * DOWN)
                    for embedding in view_embeddings
                ), lag_ratio=0.14),
                run_time=0.85,
            )
            self.play(
                *[
                    embedding.animate.move_to(target)
                    for embedding, target in zip(view_embeddings, aligned_positions)
                ],
                FadeIn(alignment_ring),
                FadeIn(alignment_label, shift=0.08 * UP),
                run_time=1.45,
                rate_func=smooth,
            )
            self.wait(max(0.1, tracker.get_remaining_duration()))
        # 3Blue1Brown-style punctuation: settle the aligned views, then cut.
        self.wait(0.75)

        with self.voiceover(
            text="Next-embedding predictive architectures use a different "
                 "objective. They divide the signal into patches, keep those patches "
                 "in order, and predict the embedding that comes next."
        ) as tracker:
            self.play(
                FadeOut(VGroup(
                    global_span, global_label, local_crops, local_labels,
                    view_embeddings, alignment_ring, alignment_label,
                )),
                run_time=0.80,
            )
            self.play(
                FadeIn(patch_boxes),
                LaggedStart(*[Create(line) for line in dividers], lag_ratio=0.10),
                run_time=0.9,
            )
            self.play(
                LaggedStart(*[GrowArrow(arrow) for arrow in preview_down_arrows], lag_ratio=0.08),
                LaggedStart(*[FadeIn(token, shift=0.12 * DOWN) for token in preview_tokens], lag_ratio=0.08),
                run_time=1.25,
            )
            self.play(
                Create(history_box),
                Create(next_box),
                GrowArrow(next_arrow),
                FadeIn(next_label),
                preview_tokens[3].animate.set_color(NEXT_TARGET),
                run_time=1.2,
            )
            self.play(FadeIn(nepa_card, shift=0.08 * UP), run_time=0.8)
            self.wait(max(0.1, tracker.get_remaining_duration()))
        self.wait(0.85)

        with self.voiceover(
            text="LeNEPA keeps the next-embedding task, but removes the masked "
                 "or cropped views."
        ) as tracker:
            # A cut through empty space is cleaner here than morphing two lines
            # with different widths, which produced doubled letterforms.
            self.play(FadeOut(nepa_card, shift=0.08 * DOWN), run_time=0.50)
            self.play(FadeIn(lenepa_card, shift=0.08 * UP), run_time=0.65)
            self.wait(max(0.1, tracker.get_remaining_duration()))
        self.wait(0.70)

        focus_index = 2
        focus_patch = patches[focus_index].copy()
        focus_patch.scale(1.12).move_to(4.55 * LEFT + 0.55 * DOWN)
        sample_dots = VGroup(*(
            Dot(focus_patch.point_from_proportion(alpha), radius=0.045)
            .set_fill(INPUT, 1)
            .set_stroke(INPUT, 0)
            for alpha in np.linspace(0.06, 0.94, 6)
        ))
        input_values = np.array([
            signal(x)
            for x in np.linspace(bounds[focus_index], bounds[focus_index + 1], 6)
        ])
        output_values = np.array([
            0.72, -0.34, 0.18, 0.91, -0.57, 0.43, -0.11, 0.61, -0.26,
        ])
        encoder = LayerMap(
            input_size=6,
            output_size=9,
            color=INPUT,
            layer_buff=2.25,
        )
        encoder.move_to(0.35 * LEFT + 0.55 * DOWN)
        encoder_label = ty.words("patch encoder", size=ty.CAPTION, color=INK)
        encoder_label.next_to(encoder, UP, buff=0.30)
        input_dim_label = ty.maths(R"C\times P", size=ty.LABEL, color=INPUT)
        input_dim_label.next_to(encoder.input_layer, DOWN, buff=0.18)
        output_dim_label = ty.maths(R"D", size=ty.LABEL, color=PREDICTION)
        output_dim_label.next_to(encoder.output_layer, DOWN, buff=0.18)
        focus_input_label = ty.maths(
            R"x_3\in\mathbb R^{C\times P}", size=ty.LABEL, color=INPUT,
        )
        focus_input_label.next_to(focus_patch, DOWN, buff=0.22)
        output_vector = numeric_embedding(
            output_values,
            color=PREDICTION,
            label=R"z_3\in\mathbb R^D",
            height=2.10,
            abbreviate=False,
        )
        output_vector.next_to(encoder, RIGHT, buff=0.72)

        with self.voiceover(
            text="Suppose we focus on the third window. The encoder maps its "
                 "C by P values into D learned coordinates."
        ) as tracker:
            self.play(
                FadeOut(VGroup(
                    preview_tokens, preview_down_arrows, history_box, next_box,
                    next_arrow, next_label, lenepa_card,
                )),
                run_time=0.75,
            )
            self.play(
                patches.animate.set_stroke(opacity=0.16),
                patch_boxes.animate.set_stroke(opacity=0.12).set_fill(opacity=0.01),
                dividers.animate.set_opacity(0.18),
                TransformFromCopy(patches[focus_index], focus_patch, path_arc=-0.18),
                run_time=1.25,
            )
            self.play(
                FadeIn(sample_dots),
                FadeIn(encoder),
                FadeIn(encoder_label),
                FadeIn(input_dim_label),
                FadeIn(output_dim_label),
                FadeIn(focus_input_label),
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
                neuron.set_stroke(PREDICTION, 1.8, opacity=0.95)
                neuron.set_fill(
                    PREDICTION,
                    opacity=0.12 + 0.76 * abs(value) / scale,
                )
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
        self.wait(0.75)

        rng = np.random.default_rng(21)
        vector_values = [rng.normal(size=9) for _ in range(6)]
        vector_values[focus_index] = output_values
        vectors = VGroup(*(
            numeric_embedding(
                values,
                color=PREDICTION,
                label=rf"z_{index + 1}",
                height=1.25,
            )
            for index, values in enumerate(vector_values)
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
            ).set_color(PREDICTION).set_opacity(0.68)
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
            text="That D-dimensional output is z three. "
                 "<bookmark mark='others'/>The same map turns every other "
                 "window into its own vector. <bookmark mark='shape'/>So, "
                 "across a batch, B by C by L becomes B by T by D: T ordered "
                 "tokens, each with D coordinates."
        ) as tracker:
            # Make the contraction decisive, then hold on the settled z_3.
            # The spoken clause owns the whole beat, but the motion does not
            # need to occupy every syllable.
            focus_time = max(
                1.45,
                tracker.time_until_bookmark("others") - 1.05,
            )
            self.play(
                FadeOut(VGroup(
                    focus_patch, sample_dots, encoder, encoder_label,
                    input_dim_label, output_dim_label, focus_input_label,
                )),
                patches.animate.set_stroke(opacity=1.0),
                patch_boxes.animate.set_stroke(opacity=0.35).set_fill(opacity=0.035),
                dividers.animate.set_opacity(0.35),
                Transform(
                    output_vector,
                    vectors[focus_index],
                    path_arc=-0.16,
                ),
                GrowArrow(arrows[focus_index]),
                run_time=focus_time,
                rate_func=smooth,
            )
            self.wait_until_bookmark("others")

            parallel_reveals = []
            for index, (arrow, vector) in enumerate(zip(arrows, vectors)):
                if index == focus_index:
                    continue
                parallel_reveals.append(AnimationGroup(
                    GrowArrow(arrow),
                    FadeIn(vector, shift=0.14 * DOWN),
                    lag_ratio=0.28,
                ))
            parallel_time = max(
                1.80,
                tracker.time_until_bookmark("shape") - 0.25,
            )
            self.play(
                LaggedStart(*parallel_reveals, lag_ratio=0.13),
                run_time=parallel_time,
            )
            self.wait_until_bookmark("shape")
            self.play(FadeIn(batch_shape, shift=0.08 * UP), run_time=1.15)
            self.wait(max(0.1, tracker.get_remaining_duration()))

        self.inspect(1.40)
        self.clear_beat()


class LeNEPA02Predict(LenepaScene):
    """A causal prefix enters the backbone; its output is the next token.

    The board is a vertical pipeline: the token row on top, an open chamber
    beneath it, and the output row below that.  Because x is the time index
    in all three tiers, "the sequence keeps its shape through the backbone"
    is legible without drawing a single wire, and the horizontal axis stays
    free for the one-slot shift that ends the scene.

    Causal exclusion is spatial, not narrated: the unseen future physically
    leaves the row's baseline in beat 3.  The four columns that descend into
    the chamber are the same objects that mix inside it and re-emerge as
    predictions below -- one persistent carrier per position, not a separate
    input row and output row.
    """

    def construct(self):
        # ------------------------------------------------------------------
        # Geometry.  Every x is derived from the row, never written down, so
        # the one-slot shift later is exact by construction.
        # ------------------------------------------------------------------
        # TOKEN_H, PRED_H, and the landing rows TGT_ROW_Y/PRD_ROW_Y are shared
        # with scene 3 via common/data.py -- scene 3 opens exactly where this
        # scene's beat 8 leaves off, at the same heights and y-positions.
        TOKEN_BUFF = 0.62
        TOKEN_ROW_Y = 2.24
        OUT_ROW_Y = -1.95
        focus = 3
        EXCLUDE_SHIFT = np.array([0.22, 0.22, 0.0])

        def pair_arrow(index: int) -> Arrow:
            x = (index + 1 - 2.5) * slot_dx
            return Arrow(
                np.array([x, PRD_ROW_Y + 0.5 * PRED_H, 0.0]),
                np.array([x, TGT_ROW_Y - 0.5 * TOKEN_H, 0.0]),
                buff=0.13,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.34,
            ).set_color(ERROR)

        # The values and the generator seed are scene 01's exit state -- see
        # common/data.py::TOKEN_VALUES.  This is a continuation, not a second
        # derivation of the same object.
        token_values = TOKEN_VALUES
        tokens = VGroup(*(
            numeric_embedding(
                values,
                color=PREDICTION,
                label=rf"z_{index + 1}",
                height=TOKEN_H,
            )
            for index, values in enumerate(token_values)
        ))
        # A uniform slot pitch, rather than ``arrange``, so that shifting a
        # prediction by exactly one slot lands it under the next token even
        # though the printed coordinates have slightly different widths.
        slot_dx = max(token.width for token in tokens) + TOKEN_BUFF
        for index, token in enumerate(tokens):
            token.move_to(np.array([(index - 2.5) * slot_dx, TOKEN_ROW_Y, 0.0]))
        assert tokens.width <= 11.2, tokens.width
        tokens.save_state()
        visible_prefix = VGroup(*tokens[:focus + 1])

        # Open on scene 01's exit geometry and grow into the hero row, so the
        # hard cut between scenes moves one object instead of replacing it.
        tokens.scale(1.25 / TOKEN_H).move_to(np.array([0.0, -1.05, 0.0]))

        time_arrow = Arrow(
            np.array([-2.5 * slot_dx - 0.55, 3.42, 0.0]),
            np.array([2.5 * slot_dx + 0.55, 3.42, 0.0]),
            buff=0,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.020,
        ).set_color(MUTED).set_opacity(0.85)
        time_word = ty.words("time", size=ty.LABEL, color=MUTED)
        time_word.next_to(time_arrow, UP, buff=0.06).align_to(time_arrow, LEFT)

        shape_sequence = ty.maths(
            R"z_{1:T}\in\mathbb R^{T\times D}",
            size=ty.LABEL,
            color=MUTED,
        )
        shape_sequence.move_to(np.array([5.15, TOKEN_ROW_Y, 0.0]))

        # ------------------------------------------------------------------
        # Causal setup: the future leaves the row's baseline -- dimmed and
        # physically displaced -- rather than being cut off with a dashed
        # line and a caption.  Only a braced prefix ever enters the chamber.
        # ------------------------------------------------------------------
        focus_ring = SurroundingRectangle(tokens.saved_state[focus], buff=0.10)
        focus_ring.set_stroke(PREDICTION, 2.4)

        prefix_group = VGroup(*tokens.saved_state[:focus + 1])
        prefix_brace = Brace(prefix_group, DOWN, buff=0.12)
        prefix_brace.set_stroke(INK, 2.2).set_fill(INK, 1.0)
        shape_prefix = ty.maths(
            R"z_{1:4}\in\mathbb R^{4\times D}",
            size=ty.LABEL,
            color=MUTED,
        )
        # Beside the brace's end rather than below it, reclaiming the
        # vertical space the old dashed cut and "not seen yet" caption used.
        shape_prefix.next_to(prefix_brace, RIGHT, buff=0.18)

        band_left = tokens.saved_state[0].get_left()[0]
        band_right = tokens.saved_state[focus].get_right()[0]
        chamber_width = (band_right - band_left) + 0.60
        chamber_height = 1.90
        shape_output = ty.maths(
            R"\hat z_4\in\mathbb R^{D}",
            size=ty.LABEL,
            color=MUTED,
        )
        shape_output.move_to(np.array([3.05, OUT_ROW_Y, 0.0]))

        self.play(
            FadeIn(tokens, shift=0.10 * UP),
            run_time=1.00,
        )

        # ------------------------------------------------------------------
        # Beats 1-3: the row settles, focus lands on position four, and the
        # future is excluded before anything enters the chamber.
        # ------------------------------------------------------------------
        with self.voiceover(
            text="These tokens are ordered in time. "
                 "<bookmark mark='focus'/>Suppose we take position four. "
                 "<bookmark mark='prefix'/>The model only gets the prefix "
                 "up to there."
        ) as tracker:
            self.play(
                Restore(tokens),
                FadeIn(time_word, shift=0.05 * DOWN),
                Create(time_arrow),
                FadeIn(shape_sequence, shift=0.08 * LEFT),
                run_time=max(0.85, tracker.time_until_bookmark("focus") - 0.10),
                rate_func=smooth,
            )

            self.wait_until_bookmark("focus")
            self.play(Create(focus_ring), run_time=0.55)

            self.wait_until_bookmark("prefix")
            self.play(
                FadeOut(focus_ring),
                GrowFromCenter(prefix_brace),
                FadeIn(shape_prefix, shift=0.06 * DOWN),
                VGroup(tokens[focus + 1], tokens[focus + 2]).animate
                .set_color(MUTED)
                .set_opacity(0.14)
                .shift(EXCLUDE_SHIFT),
                run_time=0.90,
            )
            self.wait(max(0.1, tracker.get_remaining_duration()))

        # ------------------------------------------------------------------
        # Beat 4 (silent, ~1.1s): the chamber opens and the braced prefix --
        # as persistent carrier objects, not a separate row -- descends in.
        # ------------------------------------------------------------------
        band = transformer_block(
            width=chamber_width,
            height=chamber_height,
            color=BACKBONE,
        )
        # ``band`` is a group whose external label sticks out to the right, so
        # a plain ``move_to`` would center the *label-inclusive* bounding box
        # -- not the shell -- and misplace the chamber.  Shift by the exact
        # delta that lands the shell's own center on the target point.
        band.shift(
            np.array([0.5 * (band_left + band_right), -0.18, 0.0])
            - band.shell.get_center()
        )

        carriers = VGroup(*(
            tokens[index].vector.copy() for index in range(focus + 1)
        ))
        carrier_scale = 0.70
        carrier_targets = [
            np.array([(index - 2.5) * slot_dx, band.shell.get_y(), 0.0])
            for index in range(focus + 1)
        ]
        self.add(carriers)
        self.play(FadeIn(band, shift=0.08 * UP), run_time=0.65)
        self.play(
            visible_prefix.animate.set_opacity(0.30),
            AnimationGroup(*(
                carrier.animate.scale(carrier_scale).move_to(target)
                for carrier, target in zip(carriers, carrier_targets)
            )),
            rate_func=rush_into,
            run_time=1.45,
        )

        # ------------------------------------------------------------------
        # Beat 5: causal mixing.  Arcs only ever originate at or left of
        # their own target, so causality is spatially legible without being
        # narrated.  Every carrier's numbers change in the same breath.
        # ------------------------------------------------------------------
        arc_rng = random.Random(83)
        w_max = 3.6
        mix_arcs = VGroup()
        for j in range(focus + 1):
            # Strictly i < j: i == j is causal self-attention, which is not
            # drawable as an arc between two coincident points.
            for i in range(j):
                arc = ArcBetweenPoints(
                    carriers[i].get_top(), carriers[j].get_top(), angle=-PI / 3,
                )
                stroke_width = w_max * arc_rng.random() ** 3
                arc.set_stroke(BACKBONE, stroke_width, opacity=0.55)
                mix_arcs.add(arc)

        # The displayed abbreviated form shows positions 0, 1, -2, -1 of each
        # 9-vector, in that order -- see common/data.py::MIXED_VALUES, shared
        # with scene 3's projector input.
        decimal_anims = []
        for carrier, values9 in zip(carriers, MIXED_VALUES):
            shown_positions = (values9[0], values9[1], values9[-2], values9[-1])
            for entry, target_value in zip(decimal_entries(carrier), shown_positions):
                decimal_anims.append(ChangeDecimalToValue(entry, float(target_value)))

        with self.voiceover(
            text="Inside the Transformer, each position mixes in the ones "
                 "before it."
        ) as tracker:
            self.across(
                tracker,
                LaggedStart(*(
                    ShowPassingFlash(arc, time_width=0.55) for arc in mix_arcs
                ), lag_ratio=0.12),
                *decimal_anims,
                floor=2.10,
            )

        # ------------------------------------------------------------------
        # Beats 6-7: position four's result is built from exactly those
        # four carriers, then the chamber closes and every carrier exits as
        # the output row -- the same objects, now predictions.
        # ------------------------------------------------------------------
        converge_arcs = VGroup(*(
            ArcBetweenPoints(
                carriers[k].get_top(), carriers[focus].get_top(), angle=-PI / 3,
            ).set_stroke(PREDICTION, 3.2, opacity=0.85)
            for k in range(focus)
        ))
        scale_back = PRED_H / (carrier_scale * TOKEN_H)
        out_targets = [
            np.array([(index - 2.5) * slot_dx, OUT_ROW_Y, 0.0])
            for index in range(focus + 1)
        ]

        with self.voiceover(
            text="After going through the transformer, the goal is for the output at t "
                 "<bookmark mark='exit'/>to equal the token at t plus one."
        ) as tracker:
            self.play(
                *(carriers[k].animate.set_opacity(0.40) for k in range(focus)),
                run_time=0.40,
            )
            self.play(
                LaggedStart(*(
                    ShowPassingFlash(arc, time_width=0.6) for arc in converge_arcs
                ), lag_ratio=0.15),
                Indicate(carriers[focus], color=PREDICTION, scale_factor=1.05),
                run_time=0.85,
            )

            self.wait_until_bookmark("exit")
            # Each carrier gets exactly one ``.animate`` chain here -- scale,
            # move, *and* recolor together.  Two separate ``.animate`` calls
            # on the same mobject inside one ``self.play`` silently fight
            # each other (the second resets it toward its pre-play snapshot),
            # which previously left carriers 0-2 stranded near the token row.
            carrier_moves = []
            for index, (carrier, target) in enumerate(zip(carriers, out_targets)):
                mover = carrier.animate.scale(scale_back).move_to(target)
                if index < focus:
                    mover = mover.set_color(MUTED)
                carrier_moves.append(mover)
            self.play(
                band.shell.animate.set_fill(opacity=0.10),
                AnimationGroup(*carrier_moves),
                visible_prefix.animate.set_opacity(1.0),
                run_time=1.05,
            )
            pred_labels = VGroup(*(
                ty.maths(
                    rf"\hat z_{index + 1}",
                    size=ty.LABEL,
                    color=PREDICTION if index == focus else MUTED,
                ).next_to(carriers[index], DOWN, buff=0.14)
                for index in range(focus + 1)
            ))
            self.across(
                tracker,
                FadeIn(pred_labels, shift=0.06 * DOWN),
                FadeIn(shape_output, shift=0.08 * LEFT),
                floor=1.05,
            )

        # ------------------------------------------------------------------
        # Beat 8 (silent, ~0.6s): the chamber and the beat-3 brace clear; the
        # token row and the output row rise to their landing positions.
        # ------------------------------------------------------------------
        reflow = VGroup(band, prefix_brace, shape_prefix, shape_sequence,
                        shape_output, time_arrow, time_word)
        self.play(
            FadeOut(reflow),
            tokens.animate.shift((TGT_ROW_Y - TOKEN_ROW_Y) * UP),
            VGroup(carriers, pred_labels).animate
            .shift((PRD_ROW_Y - OUT_ROW_Y) * UP),
            run_time=1.10,
            rate_func=smooth,
        )

        # ------------------------------------------------------------------
        # Beat 9: z_5 returns as the observed target; z-hat-4 slides one
        # slot right to meet it.
        # ------------------------------------------------------------------
        with self.voiceover(
            text="<bookmark mark='land'/>So for position four, that means the "
                 "output is trained toward z five."
        ) as tracker:
            self.wait_until_bookmark("land")
            self.play(
                VGroup(carriers[focus], pred_labels[focus]).animate
                .shift(slot_dx * RIGHT),
                tokens[focus + 1].animate
                .set_color(NEXT_TARGET)
                .set_opacity(1.0)
                .shift(-EXCLUDE_SHIFT),
                run_time=0.90,
                rate_func=smooth,
            )
            arrow_4 = pair_arrow(focus)
            self.across(tracker, GrowArrow(arrow_4), floor=1.05)

        # ------------------------------------------------------------------
        # Beats 10-11: the same shift, made for every usable position at
        # once; the identity lands quietly, without a title card.
        # ------------------------------------------------------------------
        with self.voiceover(
            text="The same holds at every position. "
                 "<bookmark mark='name'/>That's next-latent prediction."
        ) as tracker:
            self.play(
                AnimationGroup(*(
                    VGroup(carriers[index], pred_labels[index]).animate
                    .shift(slot_dx * RIGHT)
                    .set_color(PREDICTION)
                    for index in range(focus)
                ), lag_ratio=0.05),
                VGroup(*tokens[1:focus + 2]).animate
                .set_color(NEXT_TARGET)
                .set_opacity(1.0),
                tokens[0].animate.set_color(MUTED).set_opacity(0.24),
                run_time=1.20,
                rate_func=smooth,
            )

            new_arrows = VGroup(*(pair_arrow(index) for index in range(focus)))
            target_span = span_bracket(
                VGroup(*tokens[1:focus + 2]),
                color=NEXT_TARGET,
                label=("target  ", R"$Z_{2:T}\in\mathbb R^{(T-1)\times D}$"),
                side=UP,
                buff=0.20,
                align=LEFT,
            )
            prediction_span = span_bracket(
                VGroup(*carriers, *pred_labels),
                color=PREDICTION,
                label=("prediction  ", R"$\hat Z_{1:T-1}\in\mathbb R^{(T-1)\times D}$"),
                side=DOWN,
                buff=0.20,
                align=LEFT,
            )
            self.play(
                LaggedStart(*(GrowArrow(a) for a in new_arrows), lag_ratio=0.12),
                Create(target_span.rule),
                FadeIn(target_span.label),
                Create(prediction_span.rule),
                FadeIn(prediction_span.label),
                run_time=0.90,
            )

            self.wait_until_bookmark("name")
            identity = ty.maths(
                R"z_{1:t}\;\longrightarrow\;\hat z_t\;\approx\;z_{t+1}",
                size=ty.EQ,
                isolate=[R"z_{1:t}", R"\hat z_t", R"z_{t+1}"],
            )
            identity.set_color(INK)
            identity.set_color_by_tex(R"z_{1:t}", PREDICTION)
            identity.set_color_by_tex(R"z_{t+1}", NEXT_TARGET)
            identity.set_color_by_tex(R"\hat z_t", PREDICTION)
            identity.move_to(np.array([0.0, -3.05, 0.0]))
            landing_note = ty.words(
                "next-latent prediction", size=ty.LABEL, color=MUTED,
            )
            landing_note.next_to(identity, DOWN, buff=0.14)
            self.across(
                tracker,
                FadeIn(identity),
                FadeIn(landing_note, shift=0.06 * UP),
                floor=1.30,
            )

        self.inspect(2.20)
        self.clear_beat(1.15)


class LeNEPA03PredictionLoss(LenepaScene):
    """One projector, run twice, then the batch loss.

    Continuation of scene 2's exact vertical pair -- target lane on top,
    prediction lane below.  Beat A silently reopens that pair.  Beat B
    slides it into two lanes and runs a *single* ``LayerMap`` projector
    twice, once per lane -- because there is only one projector object on
    screen, "same weights" is true by construction and needs no ghost copy,
    no brace, no spoken claim.  Beat C computes MSE directly between the two
    projected vectors.  Beat D fans out several small (real, not dotted)
    projected-vector pairs to suggest "every position, every sequence in the
    batch," then lands on the batch loss formula.  The scene ends there --
    no gradient-flow beat.
    """

    def construct(self):
        # ------------------------------------------------------------------
        # Layout.  TOKEN_H/PRED_H/TGT_ROW_Y/PRD_ROW_Y come from common/data.py
        # -- scene 2's exact exit geometry.  Everything below is local to this
        # scene.  Named ``..._POS`` (not the bare role name) so nothing here
        # shadows an imported palette colour such as ``GRID``.
        # ------------------------------------------------------------------
        OPEN_X = 2.30  # scene 2's approximate post-shift focus-pair x; cosmetic
        TGT_LANE_Y = 1.62
        PRD_LANE_Y = -1.62
        SRC_X = -5.05
        NET_X = -3.15
        PROJ_X = -1.05
        PROJ_H = 0.85
        MSE_EQ_POS = np.array([3.10, 0.00, 0.0])

        def gap_arrow(x: float, bottom_y: float, top_y: float) -> Arrow:
            return Arrow(
                np.array([x, bottom_y + 0.5 * PRED_H, 0.0]),
                np.array([x, top_y - 0.5 * TOKEN_H, 0.0]),
                buff=0.13,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.34,
            ).set_color(ERROR)

        # ------------------------------------------------------------------
        # Beat A (silent, ~0.9s): scene 2's surviving pair reopens at its own
        # exit rows.  No title, no scene_title() call anywhere in this scene.
        # ------------------------------------------------------------------
        targ_src = numeric_embedding(
            TOKEN_VALUES[4], color=NEXT_TARGET, label=R"z_5", height=TOKEN_H,
        )
        targ_src.move_to(np.array([OPEN_X, TGT_ROW_Y, 0.0]))
        pred_src = numeric_embedding(
            MIXED_VALUES[3], color=PREDICTION, height=PRED_H,
        )
        pred_src.move_to(np.array([OPEN_X, PRD_ROW_Y, 0.0]))
        pred_label = ty.maths(R"\hat z_4", size=ty.LABEL, color=PREDICTION)
        pred_label.next_to(pred_src, DOWN, buff=0.14)
        pred_group = VGroup(pred_src, pred_label)
        pair_arrow = gap_arrow(OPEN_X, PRD_ROW_Y, TGT_ROW_Y)

        self.play(
            FadeIn(VGroup(targ_src, pred_group, pair_arrow), shift=0.10 * UP),
            run_time=0.90,
        )

        # ------------------------------------------------------------------
        # Beat B (VO1): the pair slides out to two lanes; a single LayerMap
        # fades in between them and runs *twice* -- pred_src's values, then
        # targ_src's values -- scene 1's exact propagation-flash idiom, once
        # per pass.  One projector object on screen makes "same weights" true
        # by construction, so it is never spoken.
        # ------------------------------------------------------------------
        proj_pred_vals3 = np.array([0.52, -0.24, 0.38])
        proj_targ_vals3 = np.array([0.44, -0.16, 0.29])

        def run_projector(values, out_vals, color, label, pos):
            net.set_layer_values(0, values)
            edge_flash = net.propagation_copy(color=color)
            self.play(
                LaggedStart(*(
                    ShowPassingFlash(edge, time_width=0.3) for edge in edge_flash
                ), lag_ratio=0.01),
                run_time=0.55,
            )

            proj = numeric_embedding(
                out_vals, color=color, label=label, shown=3, height=PROJ_H,
            )
            proj.move_to(pos)

            scale = max(float(np.max(np.abs(out_vals))), 1e-8)
            movers = net.output_layer.copy()
            for value, mover in zip(out_vals, movers):
                mover.set_stroke(color, 1.8, opacity=0.95)
                mover.set_fill(color, opacity=0.12 + 0.76 * abs(value) / scale)
            self.add(movers)
            self.play(
                LaggedStart(*(
                    mover.animate.move_to(entry).set_opacity(0)
                    for mover, entry in zip(movers, proj.entries)
                ), lag_ratio=0.06),
                FadeIn(proj.entries, lag_ratio=0.06),
                Create(proj.brackets),
                FadeIn(proj.label),
                run_time=0.55,
            )
            self.remove(movers)
            self.add(proj)
            return proj

        with self.voiceover(
            text="To compute the loss, the transformer's output and the "
                 "target embedding both pass through the same projector."
        ) as tracker:
            lane_arrow = gap_arrow(SRC_X, PRD_LANE_Y, TGT_LANE_Y)
            self.play(
                targ_src.animate.move_to(np.array([SRC_X, TGT_LANE_Y, 0.0])),
                pred_group.animate.move_to(np.array([SRC_X, PRD_LANE_Y, 0.0])),
                ReplacementTransform(pair_arrow, lane_arrow),
                run_time=0.70,
            )

            net = LayerMap(
                input_size=9, output_size=3, color=PROJECTOR,
                neuron_radius=0.055, layer_buff=1.35,
            )
            net.move_to(np.array([NET_X, 0.0, 0.0]))
            net_label = ty.line(
                "projector  ", R"$h_\psi$", size=ty.LABEL, color=PROJECTOR,
            )
            net_label.next_to(net, UP, buff=0.18)
            r_in_label = ty.maths(R"\mathbb R^{192}", size=ty.LABEL, color=MUTED)
            r_in_label.next_to(net.input_layer, DOWN, buff=0.18)
            r_out_label = ty.maths(R"\mathbb R^{64}", size=ty.LABEL, color=MUTED)
            r_out_label.next_to(net.output_layer, DOWN, buff=0.18)
            self.play(
                FadeIn(net), FadeIn(net_label),
                FadeIn(r_in_label), FadeIn(r_out_label),
                run_time=0.45,
            )

            proj_pred = run_projector(
                MIXED_VALUES[3], proj_pred_vals3, PREDICTION,
                R"h_\psi(\hat z_4)", np.array([PROJ_X, PRD_LANE_Y, 0.0]),
            )
            proj_targ = run_projector(
                TOKEN_VALUES[4], proj_targ_vals3, NEXT_TARGET,
                R"h_\psi(z_5)", np.array([PROJ_X, TGT_LANE_Y, 0.0]),
            )
            self.wait(max(0.1, tracker.get_remaining_duration()))

        # ------------------------------------------------------------------
        # Beat C (VO2): MSE between the two projected vectors, one clean
        # reveal collapsing straight to its value -- no separately-staged
        # Delta object.
        # ------------------------------------------------------------------
        with self.voiceover(
            text="We compute the MSE between the two projected vectors."
        ) as tracker:
            self.play(
                Indicate(proj_pred, color=ERROR, scale_factor=1.05),
                Indicate(proj_targ, color=ERROR, scale_factor=1.05),
                run_time=0.5,
            )

            mse_eq = ty.maths(
                R"{\rm MSE}_4=\|h_\psi(\hat z_4) - h_\psi(z_5)\|_2^2=0.42",
                size=ty.EQ,
                isolate=[R"{\rm MSE}_4", R"h_\psi(\hat z_4)", R"h_\psi(z_5)", "0.42"],
            )
            mse_eq.set_color(INK)
            mse_eq.set_color_by_tex(R"{\rm MSE}_4", ERROR)
            mse_eq.set_color_by_tex(R"h_\psi(\hat z_4)", PREDICTION)
            mse_eq.set_color_by_tex(R"h_\psi(z_5)", NEXT_TARGET)
            mse_eq.set_color_by_tex("0.42", ERROR)
            if mse_eq.width > 6.6:
                mse_eq.scale_to_fit_width(6.6)
            mse_eq.move_to(MSE_EQ_POS)

            self.play(FadeIn(mse_eq, shift=0.08 * UP), run_time=0.9)
            self.wait(max(0.1, tracker.get_remaining_duration()))

        # ------------------------------------------------------------------
        # Beat D (VO3): several real (if tiny) projected-vector pairs, fanned
        # out to suggest "every position, every sequence in the batch," then
        # the batch loss formula.  Replaces the old abstract (b, t) dot grid.
        # ------------------------------------------------------------------
        with self.voiceover(
            text="So when we do this for every prediction and time point "
                 "in the batch, the prediction loss becomes this:"
        ) as tracker:
            self.play(
                FadeOut(VGroup(
                    targ_src, pred_group, lane_arrow, net, net_label,
                    r_in_label, r_out_label, proj_pred, proj_targ, mse_eq,
                )),
                run_time=0.40,
            )

            fan_rng = np.random.default_rng(43)
            MINI_H = 0.50

            def mini_pair(x: float, y: float) -> VGroup:
                pred_mini = numeric_embedding(
                    fan_rng.normal(scale=0.5, size=9),
                    color=PREDICTION, shown=3, height=MINI_H,
                )
                targ_mini = numeric_embedding(
                    fan_rng.normal(scale=0.5, size=9),
                    color=NEXT_TARGET, shown=3, height=MINI_H,
                )
                pair = VGroup(pred_mini, targ_mini).arrange(DOWN, buff=0.10)
                pair.move_to(np.array([x, y, 0.0]))
                return pair

            fan_group = VGroup(*(
                mini_pair(x, 0.85) for x in np.linspace(-3.4, 3.4, 6)
            ))

            self.play(
                LaggedStart(*(FadeIn(p, shift=0.06 * UP) for p in fan_group),
                            lag_ratio=0.09),
                run_time=0.75,
            )

            fan_brace = Brace(fan_group, DOWN, color=ERROR)
            self.play(GrowFromCenter(fan_brace), run_time=0.45)

            loss_eq = ty.maths(
                R"\mathcal L_{\rm pred}=\frac{1}{B(T-1)}\sum_{b,t}"
                R"\|h_\psi(\hat z_{b,t}) - h_\psi(z_{b,t+1})\|_2^2",
                size=ty.EQ,
                color=INK,
            )
            if loss_eq.width > 11.5:
                loss_eq.scale_to_fit_width(11.5)
            loss_eq.next_to(fan_brace, DOWN, buff=0.28)

            self.play(FadeIn(loss_eq, shift=0.08 * UP), run_time=0.9)
            self.wait(max(0.1, tracker.get_remaining_duration()))

        self.inspect(1.8)
        self.clear_beat(1.0)


class LeNEPA04TemporalSIGReg(LenepaScene):
    """A shared latent plane proves temporal collapse survives a healthy batch.

    Four clean compositions, each fully cleared before the next begins -- no
    object survives a composition boundary unless it is deliberately rebuilt.
    No title card anywhere in this scene.

    A) A (B, T) grid of real token glyphs, large.  Sample b=1's row collapses
       as a genuine ``ChangeDecimalToValue`` convergence -- color never
       changes mid-morph; a coral outline marks the row only once every
       value has actually landed on the same number.
    B) Every token in the batch pools onto one large shared latent plane, so
       "the batch still looks fine" is watched, not asserted.  The SIGReg
       chapter's own projection grammar (one direction, one line, one score)
       is reused directly: b=1's identical points spike and score high;
       b=2/b=3 spread and score low.
    C) Layer 0 and layer 8 are pulled out of an actual, large transformer
       chamber -- real spatial extraction points, not floating pill labels.
    D) The temporal equation and the restored prediction loss land together,
       on an otherwise empty frame.
    """

    def construct(self):
        # ==================================================================
        # Composition A -- the temporal batch.
        # ==================================================================
        fan_rng = np.random.default_rng(43)

        def mini_pair(x: float, y: float) -> VGroup:
            pred_mini = numeric_embedding(
                fan_rng.normal(scale=0.5, size=9),
                color=PREDICTION, shown=3, height=0.50,
            )
            targ_mini = numeric_embedding(
                fan_rng.normal(scale=0.5, size=9),
                color=NEXT_TARGET, shown=3, height=0.50,
            )
            pair = VGroup(pred_mini, targ_mini).arrange(DOWN, buff=0.10)
            pair.move_to(np.array([x, y, 0.0]))
            return pair

        fan_group = VGroup(*(mini_pair(x, 0.85) for x in np.linspace(-3.4, 3.4, 6)))
        fan_brace = Brace(fan_group, DOWN, color=ERROR)
        recap_eq = ty.maths(
            R"\mathcal L_{\rm pred}=\frac{1}{B(T-1)}\sum_{b,t}"
            R"\|h_\psi(\hat z_{b,t}) - h_\psi(z_{b,t+1})\|_2^2",
            size=ty.EQ, color=INK,
        )
        if recap_eq.width > 11.5:
            recap_eq.scale_to_fit_width(11.5)
        recap_eq.next_to(fan_brace, DOWN, buff=0.28)

        self.play(
            LaggedStart(*(FadeIn(p, shift=0.06 * UP) for p in fan_group), lag_ratio=0.09),
            run_time=0.5,
        )
        self.play(GrowFromCenter(fan_brace), FadeIn(recap_eq, shift=0.08 * UP), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(VGroup(fan_group, fan_brace, recap_eq)), run_time=0.5)

        ROW_H = 1.15
        ROW_DY = 1.9
        row1 = VGroup(*(
            numeric_embedding(v, color=BACKBONE, shown=3, height=ROW_H)
            for v in BATCH_TOKENS[0]
        ))
        slot_dx = max(g.width for g in row1) + 0.55

        def place_row(row: VGroup, y: float) -> None:
            for i, g in enumerate(row):
                g.move_to(np.array([(i - 2.5) * slot_dx, y, 0.0]))

        place_row(row1, 0.0)
        if row1.width > 12.6:
            scale = 12.6 / row1.width
            row1.scale(scale)
            slot_dx *= scale
            place_row(row1, 0.0)

        row2 = VGroup(*(
            numeric_embedding(v, color=BACKBONE, shown=3, height=ROW_H)
            for v in BATCH_TOKENS[1]
        ))
        row3 = VGroup(*(
            numeric_embedding(v, color=BACKBONE, shown=3, height=ROW_H)
            for v in BATCH_TOKENS[2]
        ))
        place_row(row2, 0.0)
        place_row(row3, 0.0)

        b_labels = VGroup(*(
            ty.maths(rf"b={i + 1}", size=ty.LABEL, color=MUTED)
            for i in range(BATCH_B)
        ))
        b_labels[0].next_to(row1, LEFT, buff=0.32)

        time_arrow = Arrow(
            np.array([-2.5 * slot_dx - 0.6, ROW_DY + 1.05, 0.0]),
            np.array([2.5 * slot_dx + 0.6, ROW_DY + 1.05, 0.0]),
            buff=0, stroke_width=2.0, max_tip_length_to_length_ratio=0.020,
        ).set_color(MUTED).set_opacity(0.85)
        time_word = ty.words("time", size=ty.LABEL, color=MUTED)
        time_word.next_to(time_arrow, UP, buff=0.06).align_to(time_arrow, LEFT)

        with self.voiceover(
            text="The prediction loss compares projected vectors, but "
                 "temporal SIGReg works on the raw tokens themselves, one "
                 "sequence at a time. <bookmark mark='batch'/>Now suppose a "
                 "batch holds several such sequences, each with its own "
                 "tokens across time."
        ) as tracker:
            self.play(
                FadeIn(row1, shift=0.10 * UP),
                FadeIn(b_labels[0]),
                run_time=max(1.0, tracker.time_until_bookmark("batch") - 0.2),
            )
            self.wait_until_bookmark("batch")
            row2.move_to(row1).shift(ROW_DY * DOWN)
            row3.move_to(row1).shift(2 * ROW_DY * DOWN)
            b_labels[1].next_to(row2, LEFT, buff=0.32)
            b_labels[2].next_to(row3, LEFT, buff=0.32)
            self.across(
                tracker,
                row1.animate.shift(ROW_DY * UP),
                b_labels[0].animate.shift(ROW_DY * UP),
                FadeIn(row2, shift=0.08 * DOWN),
                FadeIn(row3, shift=0.08 * DOWN),
                FadeIn(b_labels[1]), FadeIn(b_labels[2]),
                FadeIn(time_arrow), FadeIn(time_word),
                floor=1.2,
            )

        # ------------------------------------------------------------------
        # The collapse: entries converge in place via ChangeDecimalToValue --
        # color never changes mid-morph, so there is no red/blue double
        # exposure.  Only once every value has actually landed does a coral
        # outline mark the row as collapsed.
        # ------------------------------------------------------------------
        collapse_anims = []
        for g in row1:
            entry_first, entry_last = decimal_entries(g)
            collapse_anims.append(ChangeDecimalToValue(entry_first, float(COLLAPSED_TOKEN[0])))
            collapse_anims.append(ChangeDecimalToValue(entry_last, float(COLLAPSED_TOKEN[-1])))
        collapse_outline = SurroundingRectangle(row1, buff=0.24, color=ERROR, stroke_width=2.6)

        with self.voiceover(
            text="Nothing stops the tokens in one sequence from drifting "
                 "together, until every position ends up carrying the same "
                 "embedding."
        ) as tracker:
            self.play(
                row2.animate.set_opacity(0.4), row3.animate.set_opacity(0.4),
                b_labels[1].animate.set_opacity(0.4), b_labels[2].animate.set_opacity(0.4),
                run_time=0.5,
            )
            self.across(
                tracker,
                LaggedStart(*collapse_anims, lag_ratio=0.05),
                floor=2.2,
            )
            self.play(Create(collapse_outline), run_time=0.55)
            self.wait(0.4)

        self.play(
            FadeOut(VGroup(
                row1, row2, row3, b_labels, time_arrow, time_word, collapse_outline,
            )),
            run_time=0.6,
        )

        # ==================================================================
        # Composition B -- the shared latent plane.
        # ==================================================================
        PLANE_SCALE = 1.30
        PLANE_CENTER = np.array([0.0, -0.15, 0.0])
        axes = mini_axes(PLANE_CENTER, width=9.6, height=6.0)

        def plane_point(u9) -> np.ndarray:
            xy = latent(np.asarray(u9)) * PLANE_SCALE
            return PLANE_CENTER + np.array([xy[0], xy[1], 0.0])

        collapsed_row = [COLLAPSED_TOKEN] * BATCH_T
        b1_dots = VGroup(*(
            scalar_dot(ERROR, radius=0.12).move_to(plane_point(COLLAPSED_TOKEN))
            for _ in range(BATCH_T)
        ))
        b2_dots = VGroup(*(
            scalar_dot(BACKBONE, radius=0.11).move_to(plane_point(v))
            for v in BATCH_TOKENS[1]
        ))
        b3_dots = VGroup(*(
            scalar_dot(BACKBONE, radius=0.11).move_to(plane_point(v))
            for v in BATCH_TOKENS[2]
        ))

        with self.voiceover(
            text="Now suppose we take every representation in the batch "
                 "and put it into the same projected plane. "
                 "<bookmark mark='spread'/>Across the whole batch, there's "
                 "still plenty of spread."
        ) as tracker:
            self.play(FadeIn(axes), run_time=0.4)
            self.play(
                LaggedStart(*(GrowFromCenter(d) for d in b1_dots), lag_ratio=0.20),
                run_time=max(1.3, tracker.time_until_bookmark("spread") - 0.3),
            )
            self.wait_until_bookmark("spread")
            self.across(
                tracker,
                LaggedStart(*(
                    GrowFromCenter(d) for d in list(b2_dots) + list(b3_dots)
                ), lag_ratio=0.05),
                floor=1.3,
            )
        self.wait(0.5)

        def row_rig(values9_list) -> PlaneProjectionRig:
            return PlaneProjectionRig(
                latent(np.array(values9_list)),
                origin=PLANE_CENTER, scale=PLANE_SCALE, direction=TIME_DIR,
            )

        rig_b1 = row_rig(collapsed_row)
        arrow = rig_b1.direction_arrow(length=1.8)
        proj_line = rig_b1.projection_line()
        bell = rig_b1.target_bell(height=0.7, gap=0.55)

        with self.voiceover(
            text="Now follow the first sequence across time. "
                 "<bookmark mark='spike'/>All six of its representations "
                 "have landed in essentially the same place, so its score "
                 "comes out large."
        ) as tracker:
            self.play(
                b2_dots.animate.set_opacity(0.30), b3_dots.animate.set_opacity(0.30),
                run_time=0.5,
            )
            self.play(GrowArrow(arrow), Create(proj_line), run_time=0.7)
            self.play(Create(bell), run_time=0.5)
            self.wait_until_bookmark("spike")
            shadow_pts_1 = rig_b1.shadow_points()
            self.play(
                *(d.animate.move_to(p) for d, p in zip(b1_dots, shadow_pts_1)),
                run_time=1.0,
            )
            score_label = ty.maths(rf"{rig_b1.score():.1f}", size=ty.EQ_DISPLAY, color=ERROR)
            score_label.next_to(proj_line, DOWN, buff=0.55)
            self.across(
                tracker,
                FadeIn(score_label, shift=0.08 * UP),
                Indicate(b1_dots, color=ERROR, scale_factor=1.2),
                floor=0.6,
            )

        def sweep_to_line(tracker, dots, values9_list, run_time: float):
            rig = row_rig(values9_list)
            shadow_pts = rig.shadow_points()
            new_score = ty.maths(f"{rig.score():.1f}", size=ty.EQ_DISPLAY, color=SIGREG)
            new_score.move_to(score_label)
            self.play(
                *(d.animate.move_to(p) for d, p in zip(dots, shadow_pts)),
                Transform(score_label, new_score),
                run_time=run_time,
            )

        with self.voiceover(
            text="The second sequence hasn't collapsed, so it spreads out "
                 "and scores low -- and the third looks the same way. "
                 "<bookmark mark='notation'/>So for each sequence, we run "
                 "SIGReg across its own tokens over time."
        ) as tracker:
            self.play(
                b2_dots.animate.set_opacity(1.0), b3_dots.animate.set_opacity(0.30),
                run_time=0.4,
            )
            sweep_to_line(tracker, b2_dots, list(BATCH_TOKENS[1]), 1.3)
            self.play(
                b3_dots.animate.set_opacity(1.0), b2_dots.animate.set_opacity(0.30),
                run_time=0.35,
            )
            sweep_to_line(tracker, b3_dots, list(BATCH_TOKENS[2]), 1.0)
            self.wait_until_bookmark("notation")
            notation = ty.maths(
                R"\operatorname{SIGReg}\big(\{z_{b,t}\}_{t=1}^{T}\big)",
                size=ty.EQ, color=SIGREG,
            )
            notation.next_to(axes, DOWN, buff=0.35)
            self.across(tracker, FadeIn(notation, shift=0.08 * UP), floor=0.9)

        self.play(
            FadeOut(VGroup(
                axes, b1_dots, b2_dots, b3_dots, arrow, proj_line, bell,
                score_label, notation,
            )),
            run_time=0.6,
        )

        # ==================================================================
        # Composition C -- layer 0 and layer 8, pulled from an actual chamber.
        # ==================================================================
        block = transformer_block(width=7.4, height=3.6, color=BACKBONE)
        block.shift(np.array([0.0, -0.15, 0.0]) - block.shell.get_center())
        plates = depth_plates(block, count=9, color=BACKBONE)

        u0_row = VGroup(*(
            numeric_embedding(v, color=BACKBONE, shown=3, height=0.62)
            for v in TOKEN_VALUES
        )).arrange(RIGHT, buff=0.30)
        u0_row.next_to(block.shell, UP, buff=0.40)
        u8_row = VGroup(*(
            numeric_embedding(v, color=BACKBONE, shown=3, height=0.62)
            for v in LAYER8_ROW
        )).arrange(RIGHT, buff=0.30)
        u8_row.next_to(block.shell, DOWN, buff=0.40)

        def sweep_bar(row: VGroup) -> Rectangle:
            bar = Rectangle(width=row.width + 0.28, height=row.height + 0.24)
            bar.set_stroke(opacity=0).set_fill(SIGREG, opacity=0.16)
            bar.move_to(row.get_left())
            return bar

        with self.voiceover(
            text="Tokens exist at every depth of the network, not just "
                 "one. <bookmark mark='l0'/>LeNEPA does this at two "
                 "places: the patch embeddings at layer zero, "
                 "<bookmark mark='l8'/>and again after layer eight."
        ) as tracker:
            self.play(
                FadeIn(block, shift=0.06 * UP),
                LaggedStart(*(Create(p) for p in plates), lag_ratio=0.08),
                run_time=1.1,
            )
            self.wait_until_bookmark("l0")
            tap0 = ty.maths(R"\ell=0", size=ty.LABEL, color=SIGREG)
            tap0.next_to(u0_row, UP, buff=0.18)
            self.play(FadeIn(u0_row, shift=0.35 * UP), FadeIn(tap0), run_time=0.8)
            sweep0 = sweep_bar(u0_row)
            self.play(sweep0.animate.move_to(u0_row.get_right()), run_time=0.7)
            self.wait_until_bookmark("l8")
            tap8 = ty.maths(R"\ell=8", size=ty.LABEL, color=SIGREG)
            tap8.next_to(u8_row, DOWN, buff=0.18)
            self.play(FadeIn(u8_row, shift=0.35 * DOWN), FadeIn(tap8), run_time=0.8)
            sweep8 = sweep_bar(u8_row)
            self.across(tracker, sweep8.animate.move_to(u8_row.get_right()), floor=0.7)

        with self.voiceover(
            text="Those two layers are the layer set L T."
        ) as tracker:
            layers_label = ty.maths(R"L_T=\{0,8\}", size=ty.EQ_DISPLAY, color=SIGREG)
            layers_label.next_to(block.shell, RIGHT, buff=0.55)
            self.across(
                tracker,
                TransformFromCopy(VGroup(tap0, tap8), layers_label),
                floor=1.0,
            )
        self.wait(0.4)

        self.play(
            FadeOut(VGroup(
                block, plates, u0_row, u8_row, tap0, tap8, sweep0, sweep8,
                layers_label,
            )),
            run_time=0.6,
        )

        # ==================================================================
        # Composition D -- the temporal term, then the restored prediction
        # loss, on an otherwise empty frame.
        # ==================================================================
        temporal_eq = ty.maths(
            R"\mathcal L_{\rm SIG}^{\rm time}="
            R"\frac{1}{B}\sum_b\frac{1}{|L_T|}\sum_{\ell\in L_T}"
            R"\operatorname{SIGReg}\big(\{u^{(\ell)}_{b,t}\}_{t=1}^{T}\big)",
            size=ty.EQ, color=INK,
        )
        lt_label = ty.maths(R"L_T=\{0,8\}", size=ty.EQ, color=SIGREG)
        top_row = VGroup(temporal_eq, lt_label).arrange(RIGHT, buff=0.6)
        top_row.move_to(0.6 * UP)

        with self.voiceover(
            text="Averaging those scores over the batch and over both "
                 "layers gives the temporal SIGReg term. "
                 "<bookmark mark='pair'/>Together with the prediction "
                 "loss, that's what LeNEPA trains on."
        ) as tracker:
            self.play(FadeIn(top_row, shift=0.08 * UP), run_time=1.1)
            self.wait_until_bookmark("pair")
            pred_eq = ty.maths(
                R"\mathcal L_{\rm pred}=\frac{1}{B(T-1)}\sum_{b,t}"
                R"\|h_\psi(\hat z_{b,t}) - h_\psi(z_{b,t+1})\|_2^2",
                size=ty.EQ, color=INK,
            )
            final = VGroup(pred_eq.copy(), top_row.copy()).arrange(DOWN, buff=0.6)
            final.move_to(ORIGIN)
            pred_eq.move_to(final[0])
            self.across(
                tracker,
                top_row.animate.move_to(final[1]),
                FadeIn(pred_eq, shift=0.08 * UP),
                floor=1.3,
            )

        self.inspect(1.8)
        self.clear_beat(1.0)


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
            ty.words("No EMA teacher", size=ty.STATEMENT, color=NEXT_TARGET),
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
