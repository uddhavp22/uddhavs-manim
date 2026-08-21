"""Chapter C.03 — one projection gives a scalar batch.

The finished choreography is timed to the approved narration with bookmarks.

Render:
    ./render.sh projects/sigreg_explainer/chapterC/c03_one_shadow.py C03 -qh
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data, layout
from common.beat import ActScene
from common.cloud import CloudRig
from common.palette import CLOUD, COLLAPSE, DIRECTION, TARGET
from common.project import CloudProjectionRig
from common.rig import ThreePanelRig
from common import type as ty
from common.wrap import gaussian_cf


SCORE_GRID = np.linspace(-8.0, 8.0, 4000)
SCORE_LAMBDA = 1.0
DIRECTION_U = np.array([0.70191946, 0.57980690, 0.41368228])


class C03(ActScene, ThreeDScene):
    """Project one isotropic cloud and hand its existing shadow to the rig."""

    def construct(self):
        cloud = CloudRig(
            data.gaussian_3d(),
            scale=CloudRig.SCALE,
            dot_colour=CLOUD,
        )
        projection = CloudProjectionRig(
            cloud,
            DIRECTION_U,
            lam=SCORE_LAMBDA,
            grid=SCORE_GRID,
        )
        projection_x = CloudProjectionRig(
            cloud,
            np.array([1.0, 0.0, 0.0]),
            lam=SCORE_LAMBDA,
            grid=SCORE_GRID,
        )
        projection_y = CloudProjectionRig(
            cloud,
            np.array([0.0, 1.0, 0.0]),
            lam=SCORE_LAMBDA,
            grid=SCORE_GRID,
        )
        projected_values = projection.projected_values

        # The scalar array driving the 3-D feet is handed unchanged to the
        # Chapter B rig and to the score readout. There is no second evaluator.
        rig = ThreePanelRig(
            projected_values,
            t_max=6.5,
            line_range=(-3, 3, 1),
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-32 * DEGREES)
        cloud.mount(self, ellipsoid=False)
        self.inspect(0.55)

        # Phase 1 — motivate projection before introducing its notation.
        direction_arrow = projection.direction_arrow()
        projection_line = projection.projection_line()
        direction_label = ty.maths("u", size=ty.EQ, color=DIRECTION)
        direction_label.move_to(projection.direction_tip() + 0.28 * UP)
        unit_badge = ty.maths(
            R"\|u\|=1",
            size=ty.EQ,
            color=DIRECTION,
        ).to_corner(UR, buff=0.56)
        direction_label.set_opacity(0.0)
        unit_badge.set_opacity(0.0)
        self.add_fixed_orientation_mobjects(direction_label)

        scalar_need = ty.line(
            "Epps--Pulley needs", R"$\{x_i\}_{i=1}^{N}\subset\mathbb R$",
            size=ty.LABEL,
        ).to_corner(UL, buff=0.52)
        model_gives = ty.line(
            "the model gives", R"$\{z_i\}_{i=1}^{N}\subset\mathbb R^D$",
            size=ty.LABEL,
        ).to_corner(UR, buff=0.52)
        scalar_bridge = ty.maths(
            R"\mathbb R^D\longrightarrow\mathbb R",
            size=ty.EQ_DISPLAY,
            color=DIRECTION,
        ).move_to(np.array([4.65, 3.22, 0.0]))
        layout.fit_in_frame(scalar_bridge)
        self.add_fixed_in_frame_mobjects(
            scalar_need, model_gives, scalar_bridge, unit_badge,
        )
        scalar_need.set_opacity(0.0)
        model_gives.set_opacity(0.0)
        scalar_bridge.set_opacity(0.0)
        with self.voiceover(
            text="<bookmark mark='need'/>In the last chapter, the Epps-Pulley "
                 "score started with a batch of scalars, "
                 "<bookmark mark='gives'/>but our model gives us a cloud of "
                 "vectors. <bookmark mark='bridge'/>So before we can use that "
                 "score, we need a way to turn vectors into scalars. "
                 "<bookmark mark='direction'/>Suppose we choose one direction, "
                 "u, through the cloud. <bookmark mark='unit'/>We keep u at "
                 "unit length, because "
                 "otherwise changing its length would rescale every number "
                 "we are about to measure."
        ) as tracker:
            self.wait_until_bookmark("need")
            self.play(
                scalar_need.animate.set_opacity(1.0),
                run_time=max(0.65, tracker.time_until_bookmark("gives")),
            )
            self.wait_until_bookmark("gives")
            self.move_camera(
                phi=76 * DEGREES,
                theta=-52 * DEGREES,
                run_time=max(0.8, tracker.time_until_bookmark("bridge")),
                added_anims=[
                    model_gives.animate.set_opacity(1.0),
                    Indicate(cloud.dots, color=CLOUD, scale_factor=1.025),
                ],
            )
            self.wait_until_bookmark("bridge")
            self.play(
                FadeOut(scalar_need, shift=0.08 * UP),
                FadeOut(model_gives, shift=0.08 * UP),
                scalar_bridge.animate.set_opacity(1.0),
                run_time=max(0.75, tracker.time_until_bookmark("direction")),
            )
            self.wait_until_bookmark("direction")
            self.move_camera(
                phi=66 * DEGREES,
                theta=-24 * DEGREES,
                run_time=max(1.15, tracker.time_until_bookmark("unit")),
                added_anims=[
                    scalar_bridge.animate.set_opacity(0.0),
                    GrowArrow(direction_arrow),
                    Create(projection_line),
                    direction_label.animate.set_opacity(1.0),
                ],
            )
            self.wait_until_bookmark("unit")
            self.across(
                tracker,
                unit_badge.animate.set_opacity(1.0),
                Indicate(direction_arrow, color=DIRECTION, scale_factor=1.08),
                floor=1.0,
            )
        self.remove(scalar_need, model_gives, scalar_bridge)

        # Phase 2 — explain one signed coordinate before projecting the batch.
        focus_index = 60
        negative_index = 83
        focus_dot = cloud.dots[focus_index]
        negative_dot = cloud.dots[negative_index]
        focus_point = cloud.current_points()[focus_index]
        negative_point = cloud.current_points()[negative_index]
        shadow_points = projection.shadow_points()
        shadow_radius = 0.035
        shadow_dot_list = [
            Dot(point, radius=shadow_radius).set_fill(DIRECTION, 0.96)
            for point in shadow_points
        ]
        shadow_dots = VGroup(*shadow_dot_list)
        focus_shadow = shadow_dot_list[focus_index]
        negative_shadow = shadow_dot_list[negative_index]
        other_cloud_dots = VGroup(*(
            dot for index, dot in enumerate(cloud.dots)
            if index not in (focus_index, negative_index)
        ))
        other_shadow_dots = VGroup(*(
            dot for index, dot in enumerate(shadow_dot_list)
            if index not in (focus_index, negative_index)
        ))
        all_guides = projection.guide_lines()
        focus_guide = all_guides[focus_index]
        negative_guide = all_guides[negative_index]
        guide_indices = [
            int(index) for index in np.linspace(
                0, len(cloud.dots) - 1, 44, dtype=int,
            )
            if int(index) not in (focus_index, negative_index)
        ]
        batch_guides = VGroup(*(all_guides[index] for index in guide_indices))
        z_label = ty.maths(R"z_i", size=ty.EQ, color=CLOUD)
        z_label.move_to(focus_point + 0.16 * UP)
        negative_label = ty.maths(R"z_j", size=ty.EQ, color=CLOUD)
        negative_label.move_to(negative_point + 0.16 * UP)
        negative_label.set_opacity(0.0)
        self.add_fixed_orientation_mobjects(z_label, negative_label)
        coordinate_formula = ty.maths(
            Rf"s_i=u^\top z_i=+{projected_values[focus_index]:.2f}",
            size=ty.EQ,
            color=DIRECTION,
        ).to_corner(UL, buff=0.52)
        negative_formula = ty.maths(
            Rf"s_j=u^\top z_j={projected_values[negative_index]:.2f}",
            size=ty.EQ,
            color=DIRECTION,
        ).move_to(coordinate_formula)
        self.add_fixed_in_frame_mobjects(coordinate_formula)
        coordinate_formula.set_opacity(0.0)
        with self.voiceover(
            text="Now suppose we take one embedding, z sub i. "
                 "<bookmark mark='drop'/>If we drop it perpendicularly onto "
                 "the line, <bookmark mark='read'/>then its signed position is "
                 "u transpose z sub i. <bookmark mark='positive'/>This foot "
                 "lands on the side u points toward, so the coordinate is "
                 "positive. <bookmark mark='other'/>Pick a point on the other "
                 "side instead. <bookmark mark='negative'/>Its foot "
                 "lands behind the origin, so the coordinate becomes negative."
        ) as tracker:
            self.play(
                focus_dot.animate.scale(1.45),
                FadeIn(z_label),
                run_time=max(0.75, tracker.time_until_bookmark("drop")),
            )
            self.wait_until_bookmark("drop")
            self.move_camera(
                phi=58 * DEGREES,
                theta=-8 * DEGREES,
                run_time=max(0.9, tracker.time_until_bookmark("read")),
                added_anims=[
                    Create(focus_guide),
                    TransformFromCopy(focus_dot, focus_shadow),
                ],
            )
            self.add_fixed_orientation_mobjects(focus_shadow)
            self.wait_until_bookmark("read")
            self.play(
                coordinate_formula.animate.set_opacity(1.0),
                Indicate(focus_shadow, color=DIRECTION, scale_factor=1.35),
                run_time=max(0.8, tracker.time_until_bookmark("positive")),
            )
            self.wait_until_bookmark("positive")
            self.play(
                Indicate(focus_shadow, color=DIRECTION, scale_factor=1.35),
                Indicate(coordinate_formula, color=DIRECTION, scale_factor=1.05),
                run_time=max(0.8, tracker.time_until_bookmark("other")),
            )
            self.wait_until_bookmark("other")
            self.play(
                focus_dot.animate.scale(1 / 1.45),
                FadeOut(z_label),
                negative_dot.animate.scale(1.45),
                negative_label.animate.set_opacity(1.0),
                Create(negative_guide),
                TransformFromCopy(negative_dot, negative_shadow),
                run_time=max(1.0, tracker.time_until_bookmark("negative")),
                rate_func=smooth,
            )
            self.add_fixed_orientation_mobjects(negative_shadow)
            self.wait_until_bookmark("negative")
            self.across(
                tracker,
                Transform(coordinate_formula, negative_formula),
                Indicate(negative_shadow, color=DIRECTION, scale_factor=1.35),
                floor=1.0,
            )

        # Phase 3 — repeat the same visible operation across the collection.
        batch_formula = ty.maths(
            R"\{u^\top z_i\}_{i=1}^{N}\subset\mathbb R",
            size=ty.EQ,
            color=DIRECTION,
        ).move_to(coordinate_formula)
        with self.voiceover(
            text="So now <bookmark mark='all'/>we do the same thing for every "
                 "embedding. <bookmark mark='shadow'/>Then the vectors become N "
                 "signed coordinates, which form a one-dimensional shadow of "
                 "the cloud. <bookmark mark='batch'/>The vector cloud "
                 "has become a scalar batch."
        ) as tracker:
            self.wait_until_bookmark("all")
            guide_time = max(
                1.1,
                0.42 * tracker.time_until_bookmark("shadow"),
            )
            self.move_camera(
                phi=70 * DEGREES,
                theta=-32 * DEGREES,
                run_time=guide_time,
                added_anims=[
                    LaggedStart(
                        *(Create(guide) for guide in batch_guides),
                        lag_ratio=0.018,
                    ),
                ],
            )
            self.play(
                TransformFromCopy(other_cloud_dots, other_shadow_dots),
                run_time=max(1.25, tracker.time_until_bookmark("shadow")),
                rate_func=smooth,
            )
            self.add_fixed_orientation_mobjects(*other_shadow_dots)
            self.wait_until_bookmark("shadow")
            self.play(
                Transform(coordinate_formula, batch_formula),
                FadeOut(VGroup(focus_guide, negative_guide, batch_guides)),
                FadeOut(negative_label),
                FadeOut(unit_badge),
                negative_dot.animate.scale(1 / 1.45),
                run_time=max(0.9, tracker.time_until_bookmark("batch")),
            )
            self.wait_until_bookmark("batch")

            # Phase 4 — freeze the rendered shadow into the screen plane, then
            # move those same instances to their exact scalar positions on the rig.
            projection_line.apply_function(self.camera.project_point)
            for dot in shadow_dots:
                dot.move_to(self.camera.project_point(dot.get_center()))
            self.remove_fixed_orientation_mobjects(*shadow_dots)
            self.add_fixed_in_frame_mobjects(projection_line, shadow_dots)

            target_dots = VGroup(*(
                Dot(
                    rig.line.number_to_point(value),
                    radius=shadow_radius,
                ).set_fill(DIRECTION, 0.96)
                for dot, value in zip(shadow_dots, projected_values)
            ))
            number_line_target = Line(
                rig.line.get_start(),
                rig.line.get_end(),
            ).set_stroke(DIRECTION, 2.5, opacity=0.78)
            self.across(
                tracker,
                FadeOut(cloud.dots),
                FadeOut(cloud.axes),
                FadeOut(direction_arrow),
                FadeOut(direction_label),
                Transform(projection_line, number_line_target),
                Transform(shadow_dots, target_dots),
                floor=1.9,
                rate_func=smooth,
            )
        self.remove(unit_badge)
        self.remove_fixed_in_frame_mobjects(unit_badge)
        self.inspect(0.45)

        # ``CloudRig.mount`` registers every billboard dot with the camera as
        # well as keeping their parent VGroup in the scene.  Fading only the
        # parent leaves those camera-owned instances drawable in Cairo.  Take
        # both registrations out before the flat three-panel composition.
        for dot in cloud.dots:
            dot.set_opacity(0.0)
        cloud.axes.set_opacity(0.0)
        direction_arrow.set_opacity(0.0)
        direction_label.set_opacity(0.0)
        self.remove_fixed_orientation_mobjects(*cloud.dots, direction_label)
        self.remove(cloud.dots, cloud.axes, direction_arrow, direction_label)

        # Phase 5 — adopt the already-placed dots. Mounting briefly creates the
        # live wrappers; remove them before the next rendered frame so this beat
        # reveals only the rig furniture around the one owned shadow group.
        before_mount = {id(mob) for mob in self.mobjects}
        rig.mount(
            self,
            dots=shadow_dots,
            dot_colour=DIRECTION,
            dot_radius=0.035,
            arrows=False,
        )
        mounted = [
            mob for mob in self.mobjects
            if id(mob) not in before_mount
        ]
        self.add_fixed_in_frame_mobjects(*mounted)
        live_rig = [mob for mob in mounted if mob.get_updaters()]
        furniture = [mob for mob in mounted if not mob.get_updaters()]

        # All 220 projected values remain present. Their arrows are thinner and
        # quieter than the earlier 40-arrow default so the circle remains a
        # readable average rather than becoming an opaque blue disk.
        live_arrows = always_redraw(
            lambda: rig.arrows(width=0.9, opacity=0.12)
        )
        self.add_fixed_in_frame_mobjects(live_arrows)
        self.remove(live_arrows)
        live_rig.insert(0, live_arrows)

        self.remove(*live_rig)
        for mob in furniture:
            mob.save_state()
            mob.set_opacity(0.0)
        with self.voiceover(
            text="We can now <bookmark mark='rig'/>run the "
                 "Epps-Pulley test on this shadow and compare it with a "
                 "standard Gaussian."
        ) as tracker:
            self.wait_until_bookmark("rig")
            self.across(
                tracker,
                projection_line.animate.set_opacity(0.0),
                coordinate_formula.animate.set_opacity(0.0),
                *(Restore(mob) for mob in furniture),
                floor=1.4,
                rate_func=smooth,
            )
        self.remove(projection_line)
        self.remove_fixed_in_frame_mobjects(projection_line)
        self.remove(coordinate_formula)

        # Phase 6 — run the familiar mechanism while the narration names the
        # mathematical role of each changing part.  The visible t readout,
        # arrows, empirical trace, target, discrepancy, and score are all one
        # continuous left-to-right computation.
        #
        # b03_the_rig.py::average_beat is this project's pattern for the moment
        # the rig's live parts first appear: animate static seed copies, then
        # hand off to the always_redraw versions. Two rules it encodes, both of
        # which an earlier attempt here broke. FadeIn on an always_redraw
        # mobject does nothing -- the updater rebuilds it every frame and resets
        # the opacity being animated, the same trap clear_beat's docstring
        # records -- so those parts simply popped. And inside a ThreeDScene a
        # seed built in frame coordinates must be registered with
        # add_fixed_in_frame_mobjects, or the camera projects it through the
        # 3-D view; an unregistered seed arrow is what drew a stray skewed
        # arrow across the circle.
        #
        # At t = 0 every wrapped arrow points the same way, so the bundle reads
        # as one line beneath the purple average and needs no reveal of its
        # own -- the sweep is what fans them apart. Only the average, its rider
        # and the t readout are given one.
        seed_centroid = rig.centroid()
        seeds = [seed_centroid, *seed_centroid, rig.rider(), rig.readout()]
        self.add_fixed_in_frame_mobjects(*seeds)
        self.remove(*seeds)
        self.play(
            GrowArrow(seed_centroid[0]),
            *(FadeIn(mob) for mob in seeds[1:] if mob is not seed_centroid[0]),
            run_time=0.6,
        )
        self.remove(*seeds)
        self.add(*live_rig)
        target_curve = VMobject().set_stroke(TARGET, 3.5).set_fill(opacity=0.0)
        target_curve.set_points_as_corners([
            rig.axes.c2p(t, value)
            for t, value in zip(rig.grid, gaussian_cf(rig.grid))
        ])
        empirical = rig.table
        target = gaussian_cf(rig.grid)
        gap_progress = ValueTracker(0.0)
        gap_visibility = ValueTracker(0.0)

        def current_gap_fill():
            limit = float(np.clip(
                gap_progress.get_value(), 0.0, rig.t_max,
            ))
            stop = max(2, int(np.searchsorted(rig.grid, limit, side="right")))
            stop = min(stop, len(rig.grid))
            ts = rig.grid[:stop]
            empirical_part = empirical[:stop]
            target_part = target[:stop]
            points = [
                rig.axes.c2p(t, value)
                for t, value in zip(ts, empirical_part)
            ]
            points.extend(
                rig.axes.c2p(t, value)
                for t, value in zip(ts[::-1], target_part[::-1])
            )
            region = VMobject()
            region.set_points_as_corners(points + [points[0]])
            visibility = gap_visibility.get_value()
            region.set_fill(COLLAPSE, opacity=0.42 * visibility)
            region.set_stroke(
                COLLAPSE, width=1.5, opacity=0.65 * visibility,
            )
            return region

        gap_fill = always_redraw(current_gap_fill)

        def current_gap_marker():
            """Keep the instantaneous curve separation legible as t moves."""
            t_value = float(np.clip(
                gap_progress.get_value(), 0.0, rig.t_max,
            ))
            empirical_value = float(np.interp(t_value, rig.grid, empirical))
            target_value = float(np.interp(t_value, rig.grid, target))
            empirical_point = rig.axes.c2p(t_value, empirical_value)
            target_point = rig.axes.c2p(t_value, target_value)
            opacity = gap_visibility.get_value()
            return VGroup(
                Line(
                    empirical_point,
                    target_point,
                    color=COLLAPSE,
                    stroke_width=7,
                ).set_opacity(opacity),
                Dot(
                    empirical_point,
                    radius=0.052,
                    color=COLLAPSE,
                ).set_opacity(opacity),
                Dot(
                    target_point,
                    radius=0.052,
                    color=COLLAPSE,
                ).set_opacity(opacity),
            )

        gap_marker = always_redraw(current_gap_marker)
        gap_formula = ty.maths(
            R"w_\lambda(t)\,|\widehat\varphi(t)-\varphi_0(t)|^2",
            size=ty.EQ,
            color=COLLAPSE,
        )
        gap_formula.move_to(np.array([4.55, -2.65, 0.0]))
        layout.fit_in_frame(gap_formula)
        self.add_fixed_in_frame_mobjects(
            gap_fill,
            target_curve,
            gap_marker,
            gap_formula,
        )
        target_curve.set_stroke(opacity=0.0)
        gap_formula.set_opacity(0.0)
        panel_score = ty.maths(
            Rf"{projection.score():.3f}",
            size=ty.EQ_DISPLAY,
            color=DIRECTION,
        )
        panel_score.move_to(np.array([layout.RIG_CF_CENTRE[0], -2.65, 0.0]))
        layout.fit_in_frame(panel_score)
        self.add_fixed_in_frame_mobjects(panel_score)
        panel_score.set_opacity(0.0)
        with self.voiceover(
            text="As <bookmark mark='frequency'/>t changes, each scalar "
                 "wraps around the circle, and their average traces the blue "
                 "empirical characteristic function. Once that blue curve is "
                 "drawn, we can compare it with <bookmark mark='target'/>the "
                 "standard-normal curve. <bookmark mark='gap'/>Wherever the "
                 "two curves separate, the red marker shows the gap at the "
                 "current value of t, while the weighted squared gap fills in "
                 "behind it. If the curves stay close, little accumulates. If "
                 "they pull apart, more accumulates. <bookmark mark='score'/>"
                 "At the end, all of those gaps combine into one score for "
                 "this shadow."
        ) as tracker:
            self.wait_until_bookmark("frequency")
            self.play(
                rig.t.animate.set_value(6.5),
                run_time=max(3.4, tracker.time_until_bookmark("target")),
                rate_func=linear,
            )
            self.wait_until_bookmark("target")
            target_window = max(0.05, tracker.time_until_bookmark("gap"))
            self.play(
                target_curve.animate.set_stroke(TARGET, 3.5, opacity=1.0),
                run_time=max(0.05, min(1.35, 0.55 * target_window)),
                rate_func=smooth,
            )
            self.wait_until_bookmark("gap")
            gap_intro = max(
                0.05,
                min(0.65, 0.18 * tracker.time_until_bookmark("score")),
            )
            self.play(
                gap_visibility.animate.set_value(1.0),
                gap_formula.animate.set_opacity(1.0),
                run_time=gap_intro,
                rate_func=smooth,
            )
            self.play(
                gap_progress.animate.set_value(6.5),
                run_time=max(1.8, tracker.time_until_bookmark("score")),
                rate_func=linear,
            )
            self.wait_until_bookmark("score")
            self.freeze(gap_fill)
            self.across(
                tracker,
                Succession(
                    AnimationGroup(
                        FadeOut(gap_fill),
                        FadeOut(gap_marker),
                        FadeOut(gap_formula),
                        lag_ratio=0.0,
                    ),
                    panel_score.animate.set_opacity(1.0),
                    lag_ratio=1.0,
                ),
                floor=1.1,
                rate_func=smooth,
            )
        self.remove(gap_fill)
        self.remove_fixed_in_frame_mobjects(gap_fill)
        self.remove(gap_marker)
        self.remove_fixed_in_frame_mobjects(gap_marker)
        # Take the faded discrepancy formula out of the scene rather than
        # leaving it at zero opacity. FadeOut on a Group sets one opacity
        # across the whole family, so an invisible member carried into the
        # rig's exit fade is forced back up to visible and fades from there --
        # which briefly redrew this formula on top of the score.
        self.remove(gap_formula)
        self.remove_fixed_in_frame_mobjects(gap_formula)
        with self.voiceover(
            text="That is a small score, so along this direction, the shadow "
                 "looks close to the target."
        ) as tracker:
            self.across(
                tracker,
                Indicate(panel_score, color=DIRECTION, scale_factor=1.12),
                Indicate(target_curve, color=TARGET, scale_factor=1.02),
                floor=1.1,
            )

        # Phase 8 — contract the rig, then turn the actual 3-D direction twice.
        # Each arrow, line, shadow, label, and displayed score comes from the
        # same CloudProjectionRig state for that example.
        meter_position = np.array([4.35, 2.55, 0.0])
        named_score = ty.maths(
            Rf"\operatorname{{score}}(u_1)={projection.score():.3f}",
            size=ty.EQ_DISPLAY,
            color=DIRECTION,
        ).move_to(meter_position)
        self.add_fixed_in_frame_mobjects(named_score)
        named_score.set_opacity(0.0)
        self.freeze(*live_rig)
        rig_mobjects = []
        for mob in [
            rig.line,
            *furniture,
            *live_rig,
            shadow_dots,
            target_curve,
        ]:
            if mob not in rig_mobjects:
                rig_mobjects.append(mob)
        rig_group = Group(*rig_mobjects)
        restored_line = projection.projection_line()
        restored_line.set_opacity(0.0)
        self.add(restored_line)
        restored_shadow = projection.shadow_dots(radius=0.028)
        restored_shadow.set_opacity(0.0)
        self.add_fixed_orientation_mobjects(*restored_shadow)

        first_label = ty.maths(R"u_1", size=ty.EQ, color=DIRECTION)
        first_label.move_to(projection.direction_tip() + 0.28 * UP)

        second_arrow = projection_x.direction_arrow()
        second_line = projection_x.projection_line()
        second_shadow = projection_x.shadow_dots(radius=0.028)
        second_label = ty.maths(R"u_2", size=ty.EQ, color=DIRECTION)
        second_label.move_to(projection_x.direction_tip() + 0.28 * UP)
        second_score = ty.maths(
            Rf"\operatorname{{score}}(u_2)={projection_x.score():.3f}",
            size=ty.EQ_DISPLAY,
            color=DIRECTION,
        ).move_to(meter_position)

        third_arrow = projection_y.direction_arrow()
        third_line = projection_y.projection_line()
        third_shadow = projection_y.shadow_dots(radius=0.028)
        third_label = ty.maths(R"u_3", size=ty.EQ, color=DIRECTION)
        third_label.move_to(projection_y.direction_tip() + 0.28 * UP)
        third_score = ty.maths(
            Rf"\operatorname{{score}}(u_3)={projection_y.score():.3f}",
            size=ty.EQ_DISPLAY,
            color=DIRECTION,
        ).move_to(meter_position)

        cloud.axes.set_opacity(0.0)
        direction_arrow.set_opacity(0.0)
        direction_label.set_opacity(0.0)
        for dot in cloud.dots:
            dot.set_opacity(0.0)
        self.add(cloud.axes, direction_arrow)
        self.add_fixed_orientation_mobjects(*cloud.dots, direction_label)
        self.add(cloud.dots)
        with self.voiceover(
            text="But this is still only one shadow. We chose u first, so the "
                 "score belongs to that direction. <bookmark mark='turn_one'/>"
                 "Now, if we turn u, every projected point moves, and the "
                 "score changes with the shadow. <bookmark mark='turn_two'/>"
                 "Turn u again, and both change again. "
                 "<bookmark mark='shadow_only'/>So one direction can tell us "
                 "whether one shadow looks Gaussian, <bookmark mark='whole'/>"
                 "but it cannot tell us whether the whole cloud does."
        ) as tracker:
            collapse_time = min(
                2.6,
                max(1.8, 0.55 * tracker.time_until_bookmark("turn_one")),
            )
            # Two beats, and a plain fade rather than a shrink into the corner.
            # Scaling the whole rig to 0.08 and sliding it to the meter dragged
            # a tray of illegible miniature panels across the frame, and doing
            # it while the 3-D direction faded in put a long diagonal across
            # the still-large 2-D panels -- two focal events at once, against
            # VISUAL_SYSTEM.md section 5's "one dominant focal event per beat".
            # Section 7 makes the fade the default way a rig leaves; the score
            # it computed crosses to its labelled position as it goes, so what
            # survives the cut is the result rather than a shrunken apparatus.
            fade_time = max(0.5, 0.45 * collapse_time)
            reveal_time = max(0.5, collapse_time - fade_time)
            self.play(
                FadeOut(rig_group),
                panel_score.animate.set_opacity(0.0),
                named_score.animate.set_opacity(1.0),
                run_time=fade_time,
                rate_func=smooth,
            )
            # Fixed-in-frame registrations can outlive a Group transform in
            # Cairo. Remove the rig explicitly before the held final frame so
            # its t readout cannot ghost behind score(u).
            self.remove(*rig_mobjects, panel_score)
            self.remove_fixed_in_frame_mobjects(*rig_mobjects, panel_score)
            self.play(
                cloud.axes.animate.set_opacity(1.0),
                direction_arrow.animate.set_opacity(1.0),
                Transform(direction_label, first_label),
                AnimationGroup(
                    *(dot.animate.set_opacity(0.9) for dot in cloud.dots),
                    lag_ratio=0.0,
                ),
                restored_line.animate.set_opacity(0.38),
                restored_shadow.animate.set_opacity(0.88),
                run_time=reveal_time,
                rate_func=smooth,
            )
            self.wait_until_bookmark("turn_one")
            turn_one_window = max(
                0.05,
                tracker.time_until_bookmark("turn_two"),
            )
            self.move_camera(
                phi=62 * DEGREES,
                theta=-65 * DEGREES,
                run_time=max(1.8, min(3.2, 0.72 * turn_one_window)),
                added_anims=[
                    Transform(direction_arrow, second_arrow),
                    Transform(restored_line, second_line),
                    Transform(restored_shadow, second_shadow),
                    Transform(direction_label, second_label),
                    Transform(named_score, second_score),
                ],
            )
            self.wait_until_bookmark("turn_two")
            turn_two_window = max(
                0.05,
                tracker.time_until_bookmark("shadow_only"),
            )
            self.move_camera(
                phi=76 * DEGREES,
                theta=12 * DEGREES,
                run_time=max(1.8, min(3.2, 0.78 * turn_two_window)),
                added_anims=[
                    Transform(direction_arrow, third_arrow),
                    Transform(restored_line, third_line),
                    Transform(restored_shadow, third_shadow),
                    Transform(direction_label, third_label),
                    Transform(named_score, third_score),
                ],
            )
            self.wait_until_bookmark("shadow_only")
            self.play(
                Indicate(
                    restored_shadow,
                    color=DIRECTION,
                    scale_factor=1.03,
                ),
                Indicate(named_score, color=DIRECTION, scale_factor=1.05),
                run_time=max(0.8, tracker.time_until_bookmark("whole")),
            )
            self.wait_until_bookmark("whole")
            self.across(
                tracker,
                Indicate(cloud.dots, color=CLOUD, scale_factor=1.02),
                floor=0.8,
            )
        self.inspect(0.75)

        cloud.freeze()
        self.settle_frame()
