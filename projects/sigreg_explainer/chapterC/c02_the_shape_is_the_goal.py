"""Chapter C.02 — Gaussianity belongs to the collection.

Render:
    ./render.sh projects/sigreg_explainer/chapterC/c02_the_shape_is_the_goal.py C02 -qh
"""

import os
import sys
from typing import cast

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common import type as ty
from common.beat import ActScene
from common.cloud import CloudRig
from common.palette import AVERAGE, BG, CLOUD, COLLAPSE, DIRECTION, MUTED, TARGET


class C02(ActScene, ThreeDScene):
    """Move from collapse to a failed pointwise Gaussian-matching idea."""

    def construct(self):
        # Reconstruct C01's endpoint, then complete the larger cloud while the
        # narration begins.  The same dot instances survive every later morph.
        c01_points = data.gaussian_3d(n=15, seed=76)
        full_draw = data.gaussian_3d(n=220, seed=5)
        cloud_points = np.vstack((c01_points, full_draw[15:]))
        cloud = CloudRig(cloud_points, scale=CloudRig.SCALE, dot_colour=CLOUD)
        cloud.ellipsoid.set_fill(TARGET, opacity=0.025)
        cloud.ellipsoid.set_stroke(TARGET, width=0.40, opacity=0.18)
        cloud.axes.set_opacity(0.72)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-32 * DEGREES)
        for dot in cloud.dots[15:]:
            dot.scale(0.55)
            dot.set_opacity(0.0)
        cloud.mount(self, ellipsoid=False)

        collapse_mark = Circle(radius=0.16, color=COLLAPSE, stroke_width=4)
        collapse_mark.set_fill(COLLAPSE, opacity=0.12)
        collapse_mark.set_opacity(0.0)
        self.add_fixed_orientation_mobjects(collapse_mark)

        rank_label = ty.maths(R"\operatorname{rank}(Z)=3", size=ty.EQ, color=MUTED)
        rank_label.to_corner(DL, buff=0.48)
        self.add_fixed_in_frame_mobjects(rank_label)
        rank_label.set_opacity(0.0)

        with self.voiceover(
            text="Suppose the cloud starts losing its spread. "
                 "<bookmark mark='pancake'/>If one direction disappears, it "
                 "flattens into a sheet, so the batch rank drops from three "
                 "to two. <bookmark mark='rod'/>If another disappears, the "
                 "rank drops to one. <bookmark mark='point'/>And if the last "
                 "spread disappears, every embedding meets at one point. The "
                 "rank is zero."
        ) as tracker:
            self.play(
                LaggedStart(
                    *(
                        cast(Animation, dot.animate.scale(1 / 0.55).set_opacity(0.9))
                        for dot in cloud.dots[15:]
                    ),
                    lag_ratio=0.006,
                ),
                rank_label.animate.set_opacity(1.0),
                run_time=max(1.2, tracker.time_until_bookmark("pancake")),
            )
            # Child animations promote dots into the scene; restore the parent
            # group so its single updater remains the source of truth.
            self.add(cloud.dots)
            cloud.dots.update(0)
            self.wait_until_bookmark("pancake")
            rank_two = ty.maths(
                R"\operatorname{rank}(Z)=2", size=ty.EQ, color=MUTED,
            ).move_to(rank_label)
            self.add_fixed_in_frame_mobjects(rank_two)
            self.play(
                cloud.animate_shape((1.0, 1.0, 0.0)),
                ReplacementTransform(rank_label, rank_two),
                run_time=1.35,
            )
            rank_label = rank_two
            self.wait_until_bookmark("rod")
            rank_one = ty.maths(
                R"\operatorname{rank}(Z)=1", size=ty.EQ, color=MUTED,
            ).move_to(rank_label)
            self.add_fixed_in_frame_mobjects(rank_one)
            self.play(
                cloud.animate_shape((1.0, 0.0, 0.0)),
                ReplacementTransform(rank_label, rank_one),
                run_time=1.35,
            )
            rank_label = rank_one
            self.wait_until_bookmark("point")
            rank_zero = ty.maths(
                R"\operatorname{rank}(Z)=0", size=ty.EQ, color=COLLAPSE,
            ).move_to(rank_label)
            self.add_fixed_in_frame_mobjects(rank_zero)
            self.play(
                cloud.animate_shape((0.0, 0.0, 0.0)),
                collapse_mark.animate.set_opacity(1.0),
                ReplacementTransform(rank_label, rank_zero),
                run_time=1.5,
            )
            rank_label = rank_zero

        # Give the conclusion its own clean vocal and visual beat. Keeping it
        # out of the long rank-ladder clip prevents the final words from being
        # swallowed by that clip's tail.
        with self.voiceover(
            text="The representation has collapsed."
        ) as tracker:
            self.play(
                Indicate(rank_label, color=COLLAPSE, scale_factor=1.08),
                Indicate(collapse_mark, color=COLLAPSE, scale_factor=1.18),
                run_time=tracker.duration,
            )

        target_name = ty.maths(
            R"z^\star\sim\mathcal N(0,I_D)", size=ty.EQ, color=TARGET,
        )
        target_mean = ty.maths(
            R"\mathbb E[z^\star]=0", size=ty.BODY, color=MUTED,
        )
        target_covariance = ty.maths(
            R"\operatorname{Cov}(z^\star)=I_D", size=ty.BODY, color=MUTED,
        )
        target_facts = VGroup(target_name, target_mean, target_covariance)
        target_facts.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        target_facts.to_corner(UL, buff=0.50)
        self.add_fixed_in_frame_mobjects(target_facts)
        target_facts.set_opacity(0.0)

        direction_arrow = Arrow(
            ORIGIN,
            0.92 * CloudRig.SCALE * RIGHT,
            buff=0.025,
            stroke_width=4.0,
            tip_length=0.13,
            color=DIRECTION,
        )
        target_origin = Dot(ORIGIN, radius=0.07, color=TARGET)
        target_origin.set_opacity(0.0)
        self.add_fixed_orientation_mobjects(target_origin)

        # Restore full rank and motivate the target. Keep the future-video
        # qualification attached directly to the LeJEPA claim it qualifies.
        with self.voiceover(
            text="So training needs a target that stays spread out in every "
                 "direction. LeJEPA chooses a standard normal distribution "
                 "in D dimensions because, in its downstream-task setting, that "
                 "distribution minimizes worst-case prediction error. "
                 "There is more to unpack about that claim, so we can come "
                 "back to it in a future video."
        ) as tracker:
            self.across(
                tracker,
                cloud.animate_shape((1.0, 1.0, 1.0)),
                FadeOut(collapse_mark),
                FadeOut(rank_label),
                FadeIn(cloud.ellipsoid),
                target_name.animate.set_opacity(1.0),
                cloud.axes.animate.set_opacity(0.72),
                floor=1.8,
                rate_func=smooth,
            )

        # Now unpack the geometry encoded by N(0, I_D). The compact green
        # direction remains inside the amber target as it sweeps through
        # genuine 3-D orientations.
        with self.voiceover(
            text="For now, what matters is that this standard normal has mean "
                 "zero and unit variance in every direction. "
                 "<bookmark mark='center'/>Mean zero centers the cloud at the "
                 "origin. <bookmark mark='spread'/>Unit variance gives it the "
                 "same spread in every direction. "
                 "<bookmark mark='turn'/>So if we turn the direction, the "
                 "round target stays unchanged; it does not favor one "
                 "direction over another."
        ) as tracker:
            self.wait_until_bookmark("center")
            self.play(
                target_mean.animate.set_opacity(1.0),
                target_origin.animate.set_opacity(1.0),
                run_time=0.85,
            )
            self.wait_until_bookmark("spread")
            self.play(
                target_covariance.animate.set_opacity(1.0),
                GrowArrow(direction_arrow),
                run_time=0.9,
            )
            # Leave the screen plane while "unit variance in every direction"
            # is spoken, so the claim reads as three-dimensional geometry.
            self.play(
                Succession(
                    Rotate(
                        direction_arrow,
                        angle=0.58 * PI,
                        axis=UP,
                        about_point=ORIGIN,
                        rate_func=smooth,
                    ),
                    Rotate(
                        direction_arrow,
                        angle=0.52 * PI,
                        axis=RIGHT,
                        about_point=ORIGIN,
                        rate_func=smooth,
                    ),
                ),
                run_time=max(1.2, tracker.time_until_bookmark("turn")),
            )
            self.wait_until_bookmark("turn")
            self.across(
                tracker,
                Succession(
                    Rotate(
                        direction_arrow,
                        angle=0.70 * PI,
                        axis=OUT,
                        about_point=ORIGIN,
                        rate_func=smooth,
                    ),
                    Rotate(
                        direction_arrow,
                        angle=0.62 * PI,
                        axis=UP,
                        about_point=ORIGIN,
                        rate_func=smooth,
                    ),
                    Rotate(
                        direction_arrow,
                        angle=0.56 * PI,
                        axis=RIGHT,
                        about_point=ORIGIN,
                        rate_func=smooth,
                    ),
                ),
                floor=1.7,
            )

        # Training can only enforce the target through a scalar objective.
        # Pulse the batch and target on their spoken phrases before trying the
        # tempting pointwise construction, so "loss" has a job before it is
        # used as a name.
        match_loss = ty.maths(
            R"\mathcal L_{\mathrm{match}}(Z)",
            size=ty.EQ_DISPLAY,
            color=MUTED,
        ).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(match_loss)
        match_loss.set_opacity(0.0)
        with self.voiceover(
            text="So how do we train <bookmark mark='cloud'/>this blue batch "
                 "to match <bookmark mark='target'/>the amber target "
                 "distribution? <bookmark mark='loss'/>We need a loss that "
                 "measures the mismatch."
        ) as tracker:
            self.wait_until_bookmark("cloud")
            self.play(
                Indicate(cloud.dots, color=CLOUD, scale_factor=1.025),
                run_time=0.62,
            )
            self.wait_until_bookmark("target")
            self.play(
                cloud.ellipsoid.animate(rate_func=there_and_back)
                .set_fill(TARGET, opacity=0.12)
                .set_stroke(TARGET, width=1.15, opacity=0.55),
                Indicate(target_name, color=TARGET, scale_factor=1.045),
                run_time=max(0.72, tracker.time_until_bookmark("loss")),
            )
            self.wait_until_bookmark("loss")
            self.across(
                tracker,
                match_loss.animate.set_opacity(1.0),
                floor=0.45,
            )

        # Use one embedding first.  Only after its local pair is legible do we
        # repeat the construction across a sparse subset of the batch.
        all_starts = cloud.current_points()
        pair_indices = np.linspace(0, len(all_starts) - 1, 14, dtype=int)
        starts = all_starts[pair_indices]
        focus_slot = 9
        focus_index = int(pair_indices[focus_slot])
        focus_start = starts[focus_slot]
        pair_index_set = set(pair_indices.tolist())
        background_dots = VGroup(*(
            dot for index, dot in enumerate(cloud.dots)
            if index not in pair_index_set
        ))
        other_pair_dots = VGroup(*(
            cloud.dots[index] for slot, index in enumerate(pair_indices)
            if slot != focus_slot
        ))
        focus_dot = cloud.dots[focus_index]

        partners_a = self._partner_points(len(starts), seed=2401)
        focus_partner = self._partner_dots(partners_a[[focus_slot]], radius=0.065)
        focus_arrow = self._pull_arrows(
            starts[[focus_slot]], partners_a[[focus_slot]], TARGET, 0.92,
            stroke_width=2.5, tip_length=0.13,
        )
        z_label = ty.maths(R"z_i", size=ty.EQ, color=CLOUD)
        z_star_label = ty.maths(R"z_i^\star", size=ty.EQ, color=TARGET)
        z_label.next_to(focus_start, LEFT, buff=0.10)
        z_star_label.next_to(partners_a[focus_slot], RIGHT, buff=0.10)
        pair_cost = ty.maths(
            R"\lVert z_i-z_i^\star\rVert^2",
            size=ty.EQ,
            color=MUTED,
        ).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(pair_cost)
        pair_cost.set_opacity(0.0)

        with self.voiceover(
            text="Suppose we build that loss as directly as possible. "
                 "<bookmark mark='sample'/>Take one blue embedding, z sub i. "
                 "<bookmark mark='partner'/>Draw one possible partner, z sub "
                 "i star, from the normal target. <bookmark mark='pair'/>Compare "
                 "the pair with their squared distance, and use that number "
                 "as the loss. <bookmark mark='all_pairs'/>Then repeat the "
                 "same construction for every embedding in the batch."
        ) as tracker:
            self.move_camera(
                phi=0 * DEGREES,
                theta=-90 * DEGREES,
                run_time=max(1.3, tracker.time_until_bookmark("sample")),
                added_anims=[
                    FadeOut(cloud.ellipsoid),
                    FadeOut(target_facts),
                    FadeOut(direction_arrow),
                    FadeOut(target_origin),
                    background_dots.animate.set_opacity(0.10),
                    other_pair_dots.animate.set_opacity(0.22),
                ],
            )
            self.remove(cloud.ellipsoid)
            cloud.ellipsoid.clear_updaters()
            self.wait_until_bookmark("sample")
            self.play(
                focus_dot.animate.scale(1.35),
                FadeIn(z_label),
                run_time=0.75,
            )
            self.wait_until_bookmark("partner")
            self.play(
                FadeIn(focus_partner, scale=0.65),
                FadeIn(z_star_label),
                run_time=0.85,
            )
            self.wait_until_bookmark("pair")
            pair_cost.set_opacity(1.0)
            self.play(
                GrowArrow(cast(Arrow, focus_arrow[0])),
                ReplacementTransform(match_loss, pair_cost),
                run_time=1.0,
            )
            self.wait_until_bookmark("all_pairs")
            other_slots = [i for i in range(len(starts)) if i != focus_slot]
            other_partners = self._partner_dots(partners_a[other_slots])
            other_arrows = self._pull_arrows(
                starts[other_slots], partners_a[other_slots], TARGET, 0.34,
            )
            self.across(
                tracker,
                LaggedStart(
                    *(FadeIn(dot, scale=0.65) for dot in other_partners),
                    lag_ratio=0.045,
                ),
                LaggedStart(
                    *(GrowArrow(cast(Arrow, arrow)) for arrow in other_arrows),
                    lag_ratio=0.035,
                ),
                floor=1.35,
            )

        partner_dots = VGroup(focus_partner, other_partners)
        pull_arrows = VGroup(focus_arrow, other_arrows)

        # A finite but visibly growing sample stands in for the continuum of
        # possible target draws. It accumulates while "infinitely many" is
        # spoken instead of reducing that claim to three isolated examples.
        many_ends = self._partner_points(30, seed=2403)
        many_dots = self._partner_dots(
            many_ends, radius=0.030, opacity=0.54,
        )
        many_lines = VGroup(*(
            DashedLine(focus_start, end, dash_length=0.085)
            .set_stroke(TARGET, width=1.0, opacity=0.18)
            for end in many_ends
        ))

        with self.voiceover(
            text="But the target distribution does not prescribe one partner "
                 "for z sub i. <bookmark mark='many'/>There are infinitely "
                 "many possible draws. We cannot show all of them, but a "
                 "rapid sample gives us the picture. "
                 "<bookmark mark='resample'/>If we sample the "
                 "amber points again, the blue batch stays fixed while every "
                 "pairing changes."
        ) as tracker:
            self.wait_until_bookmark("many")
            self.play(
                LaggedStart(
                    *(
                        AnimationGroup(
                            FadeIn(dot, scale=0.55),
                            Create(line),
                        )
                        for dot, line in zip(many_dots, many_lines)
                    ),
                    lag_ratio=0.035,
                ),
                run_time=max(1.5, tracker.time_until_bookmark("resample")),
            )
            self.wait_until_bookmark("resample")
            self.play(
                FadeOut(many_dots),
                FadeOut(many_lines),
                FadeOut(partner_dots),
                FadeOut(pull_arrows),
                FadeOut(z_star_label),
                run_time=0.5,
            )
            partners_b = self._partner_points(len(starts), seed=2402)
            partner_dots = self._partner_dots(partners_b)
            pull_arrows = self._pull_arrows(starts, partners_b, TARGET, 0.34)
            self.across(
                tracker,
                LaggedStart(
                    *(FadeIn(dot, scale=0.65) for dot in partner_dots),
                    lag_ratio=0.035,
                ),
                LaggedStart(
                    *(GrowArrow(cast(Arrow, arrow)) for arrow in pull_arrows),
                    lag_ratio=0.025,
                ),
                floor=1.4,
            )

        # Average partners for one fixed z.  This makes the cancellation local
        # and readable instead of drawing a starburst from every sample.
        average_partners = self._partner_points(48, seed=2500)
        repeated_focus = np.repeat(focus_start[None, :], len(average_partners), axis=0)
        average_partner_dots = self._partner_dots(
            average_partners, radius=0.036, opacity=0.46,
        )
        random_arrows = self._pull_arrows(
            repeated_focus, average_partners, TARGET, 0.16,
            stroke_width=1.0, tip_length=0.065,
        )
        mean_arrow = self._pull_arrows(
            focus_start[None, :], np.zeros((1, 3)), AVERAGE, 0.95,
            stroke_width=3.0, tip_length=0.15,
        )
        origin = Dot(ORIGIN, radius=0.075).set_fill(AVERAGE, opacity=1.0)

        with self.voiceover(
            text="So instead of listing every possible draw, we can use the "
                 "normal target to calculate an expectation. The number of "
                 "possible draws has nothing to do with the number of blue "
                 "embeddings. <bookmark mark='focus'/>We hold one embedding z "
                 "fixed. "
                 "As more possible partners fill the target around zero, "
                 "opposite directions balance. <bookmark mark='origin'/>Their "
                 "average pull points straight from z to the origin."
        ) as tracker:
            self.play(
                FadeOut(partner_dots),
                FadeOut(pull_arrows),
                FadeOut(z_label),
                FadeOut(pair_cost),
                other_pair_dots.animate.set_opacity(0.10),
                run_time=max(0.7, tracker.time_until_bookmark("focus")),
            )
            self.wait_until_bookmark("focus")
            self.play(
                LaggedStart(
                    *(FadeIn(dot, scale=0.65) for dot in average_partner_dots),
                    lag_ratio=0.018,
                ),
                LaggedStart(
                    *(Create(arrow) for arrow in random_arrows),
                    lag_ratio=0.014,
                ),
                run_time=max(
                    1.5,
                    tracker.time_until_bookmark("origin"),
                ),
            )
            self.wait_until_bookmark("origin")
            self.across(
                tracker,
                average_partner_dots.animate.set_opacity(0.14),
                FadeOut(random_arrows),
                GrowArrow(cast(Arrow, mean_arrow[0])),
                FadeIn(origin, scale=0.6),
                floor=1.1,
            )

        expected_distance = R"\mathbb E\lVert z-z^\star\rVert^2"
        point_length = R"\lVert z\rVert^2"
        mean_term = R"\mathbb E[z^\star]"
        partner_energy = R"\mathbb E\lVert z^\star\rVert^2"
        expanded = ty.maths(
            expected_distance
            + "=" + point_length
            + R"-2z^\top" + mean_term
            + "+" + partner_energy,
            size=34,
            color=MUTED,
            isolate=[expected_distance, point_length, mean_term, partner_energy],
        )
        mean_fact = ty.maths(
            mean_term + "=0", size=ty.BODY, color=MUTED,
            isolate=[mean_term, "0"],
        )
        energy_fact = ty.maths(
            partner_energy + "=D", size=ty.BODY, color=MUTED,
            isolate=[partner_energy, "D"],
        )
        facts = VGroup(mean_fact, energy_fact).arrange(RIGHT, buff=0.75)
        simplified = ty.maths(
            expected_distance + "=" + point_length + "+D",
            size=ty.EQ_DISPLAY,
            color=MUTED,
            isolate=[expected_distance, point_length, "+D"],
        )
        minimum = ty.maths(
            R"\operatorname*{arg\,min}_{z}\;(\lVert z\rVert^2+D)=0",
            size=ty.EQ,
            color=MUTED,
        )
        equation_group = VGroup(expanded, facts, simplified, minimum)
        equation_group.arrange(DOWN, buff=0.12)
        equation_group.to_edge(DOWN, buff=0.26)
        layout.fit_in_frame(equation_group)
        equation_plate = BackgroundRectangle(
            equation_group,
            color=BG,
            fill_opacity=0.94,
            stroke_opacity=0.0,
            buff=0.18,
        )
        equation_panel = VGroup(
            equation_plate, expanded, mean_fact, energy_fact, simplified, minimum,
        )
        self.add_fixed_in_frame_mobjects(equation_panel)
        equation_plate.set_opacity(0.0)
        expanded.set_opacity(0.0)
        mean_fact.set_opacity(0.0)
        energy_fact.set_opacity(0.0)
        simplified.set_opacity(0.0)
        minimum.set_opacity(0.0)
        point_length_part = expanded.get_part_by_tex(point_length)
        mean_part = expanded.get_part_by_tex(mean_term)
        energy_part = expanded.get_part_by_tex(partner_energy)
        constant_part = simplified.get_part_by_tex("+D")
        if any(part is None for part in (
            point_length_part, mean_part, energy_part, constant_part,
        )):
            raise RuntimeError("expected-distance terms were not isolated")

        # Keep the algebra attached to the picture.  The focus radius is the
        # visible ||z|| term; the faint Gaussian draw is the expectation; and
        # the final field of arrows shows that the same pointwise minimum is
        # requested independently for every embedding.
        focus_radius = Line(ORIGIN, focus_start)
        focus_radius.set_stroke(CLOUD, width=3.2, opacity=0.88)
        batch_origin_arrows = self._pull_arrows(
            starts,
            np.zeros_like(starts),
            COLLAPSE,
            0.52,
            stroke_width=1.55,
            tip_length=0.085,
        )

        with self.voiceover(
            text="Because the standard normal has a known mean and variance, "
                 "we can evaluate this expectation exactly. "
                 "<bookmark mark='equation'/>If we "
                 "expand the square, the first term is the squared length of "
                 "z. <bookmark mark='mean'/>The cross term contains the mean "
                 "of z star, which is zero. <bookmark mark='energy'/>And z "
                 "star has D coordinates with variance one, so its expected "
                 "squared length is D. <bookmark mark='simplify'/>The average "
                 "loss is therefore the squared length of z, plus D. "
                 "<bookmark mark='constant'/>Since D is constant, "
                 "<bookmark mark='minimum'/>the pointwise minimum is z equals "
                 "zero."
        ) as tracker:
            # The setup sentence explains why the infinite average is still
            # tractable. Keep the corresponding geometry active: the possible
            # targets, their zero centre, and their mean pull arrive in order.
            self.play(
                LaggedStart(
                    Indicate(
                        average_partner_dots,
                        color=TARGET,
                        scale_factor=1.04,
                    ),
                    Indicate(origin, color=TARGET, scale_factor=1.35),
                    Indicate(
                        mean_arrow,
                        color=AVERAGE,
                        scale_factor=1.08,
                    ),
                    lag_ratio=0.42,
                ),
                run_time=max(1.8, tracker.time_until_bookmark("equation")),
            )
            self.wait_until_bookmark("equation")
            self.play(
                equation_plate.animate.set_opacity(1.0),
                expanded.animate.set_opacity(1.0),
                cloud.axes.animate.set_opacity(0.18),
                Create(focus_radius),
                run_time=0.8,
            )
            self.play(
                Indicate(point_length_part, color=CLOUD, scale_factor=1.06),
                Indicate(focus_dot, color=CLOUD, scale_factor=1.35),
                run_time=0.7,
            )
            self.wait_until_bookmark("mean")
            self.play(
                Indicate(mean_part, color=TARGET, scale_factor=1.08),
                mean_fact.animate.set_opacity(1.0),
                Indicate(origin, color=TARGET, scale_factor=1.30),
                run_time=0.8,
            )
            self.wait_until_bookmark("energy")
            self.play(
                Indicate(energy_part, color=TARGET, scale_factor=1.06),
                energy_fact.animate.set_opacity(1.0),
                Indicate(
                    average_partner_dots,
                    color=TARGET,
                    scale_factor=1.025,
                ),
                run_time=0.8,
            )
            self.wait_until_bookmark("simplify")
            self.play(simplified.animate.set_opacity(1.0), run_time=0.7)
            self.wait_until_bookmark("constant")
            self.play(
                Indicate(constant_part, color=TARGET, scale_factor=1.12),
                run_time=0.7,
            )
            self.wait_until_bookmark("minimum")
            self.across(
                tracker,
                minimum.animate.set_opacity(1.0).set_color(COLLAPSE),
                Indicate(origin, color=COLLAPSE, scale_factor=1.35),
                FadeOut(mean_arrow),
                LaggedStart(
                    *(GrowArrow(cast(Arrow, arrow)) for arrow in batch_origin_arrows),
                    lag_ratio=0.025,
                ),
                floor=0.9,
            )

        with self.voiceover(
            text="But this gives us the wrong loss: now every embedding gets "
                 "pulled toward zero. So the pointwise minimum puts the whole "
                 "batch at the collapsed "
                 "point we started with. <bookmark mark='collection'/>If the "
                 "goal is the shape of the blue collection, then "
                 "<bookmark mark='measure'/>the loss has to compare "
                 "distributions rather than assign partners."
        ) as tracker:
            self.move_camera(
                phi=70 * DEGREES,
                theta=-32 * DEGREES,
                run_time=max(1.7, tracker.time_until_bookmark("collection")),
                added_anims=[
                    FadeOut(origin),
                    FadeOut(equation_panel),
                    FadeOut(average_partner_dots),
                    FadeOut(focus_radius),
                    FadeOut(batch_origin_arrows),
                    background_dots.animate.set_opacity(0.9),
                    other_pair_dots.animate.set_opacity(0.9),
                    focus_dot.animate.scale(1 / 1.35),
                    cloud.axes.animate.set_opacity(0.72),
                ],
            )
            self.wait_until_bookmark("collection")
            cloud.ellipsoid.set_fill(TARGET, opacity=0.025)
            cloud.ellipsoid.set_stroke(TARGET, width=0.40, opacity=0.18)
            cloud.ellipsoid.update(0)
            self.play(FadeIn(cloud.ellipsoid), run_time=0.9)
            self.wait_until_bookmark("measure")
            self.across(
                tracker,
                Indicate(cloud.dots, color=CLOUD, scale_factor=1.035),
                cloud.ellipsoid.animate(rate_func=there_and_back)
                .set_fill(TARGET, opacity=0.12)
                .set_stroke(TARGET, width=1.15, opacity=0.55),
                floor=1.0,
            )

        self.remove(
            collapse_mark, pair_cost, match_loss, mean_arrow, origin, equation_panel,
            average_partner_dots, random_arrows, target_facts, direction_arrow,
            target_origin, focus_radius, batch_origin_arrows,
        )
        cloud.freeze()
        self.settle_frame()

    @staticmethod
    def _partner_points(count: int, *, seed: int) -> np.ndarray:
        rng = np.random.default_rng(seed)
        points = np.zeros((count, 3))
        points[:, :2] = rng.standard_normal((count, 2)) * CloudRig.SCALE
        return points

    @staticmethod
    def _partner_dots(
        points,
        *,
        radius: float = 0.042,
        opacity: float = 0.82,
    ) -> VGroup:
        return VGroup(*(
            Dot(point, radius=radius).set_fill(TARGET, opacity=opacity)
            for point in points
        ))

    @staticmethod
    def _pull_arrows(
        starts,
        ends,
        colour,
        opacity: float,
        *,
        stroke_width: float = 1.35,
        tip_length: float = 0.085,
    ) -> VGroup:
        return VGroup(*(
            Arrow(
                start,
                end,
                buff=0.07,
                stroke_width=stroke_width,
                tip_length=tip_length,
            ).set_color(colour).set_opacity(opacity)
            for start, end in zip(starts, ends)
        ))
