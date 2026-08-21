"""Chapter C.04 — one shadow can be innocent.

C03 established that one direction produces one score. This turns the
direction through a half turn over a cloud that has something to hide, and
lets the same cloud produce both an alarming shadow and an innocent one.

Three Manim traps carried over from C03's review (each renders without an
error, so none of them shows up as a failure):

  1. A frame-coordinate mobject added inside a `ThreeDScene` without
     `add_fixed_in_frame_mobjects` is projected through the 3-D camera. Every
     panel, label and readout below is registered.
  2. `FadeIn`/`FadeOut` on an `always_redraw` mobject is a no-op -- the rebuild
     resets the opacity being animated. Nothing here uses `always_redraw`;
     `TurningProjection`'s updaters move points and never touch opacity, and
     every reveal happens while the angle tracker is held still.
  3. `FadeOut` on a `Group` sets one opacity across the whole family, so a
     member already at zero opacity is forced back to visible. Hidden mobjects
     are removed from the scene here rather than parked at zero.

Render:
    ./render.sh projects/sigreg_explainer/chapterC/c04_one_shadow_is_not_enough.py C04 -qh
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import data
from common.beat import ActScene
from common.cloud import CloudRig
from common.palette import AXIS, CLOUD, COLLAPSE, DIRECTION, MUTED, TARGET
from common.project import CloudProjectionRig, TurningProjection
from common.score import EP_GRID, EP_LAMBDA
from common import type as ty

# The turn's two settled directions. Zero is the axis the clumps separate
# along; a quarter turn later the direction is the y axis, which the narration
# calls "a quarter of the way round" because that is literally what it is.
ALARMING = 0.0
INNOCENT = np.pi / 2
HALF_TURN = np.pi

# C03's third and last direction, so its shadow, its arrow and its score are
# the ones standing in this scene's first frame.
INHERITED_U = np.array([0.0, 1.0, 0.0])

# Where the fixed-frame panels live, and how far the 3-D world is pushed left
# to clear them.
WORLD_OFFSET = 1.75
METER_POSITION = np.array([4.35, 2.55, 0.0])
TRACE_CENTRE = np.array([4.35, -1.15, 0.0])
# The silent Gaussian reference sits top-left, clear of both panels and of the
# cloud at every angle of the turn. Not in the panel column: the free space
# there is directly above "score along each direction", and a caption that
# close reads as labelling the curve above it rather than the axes below it.
BELL_CENTRE = np.array([-5.05, 2.30, 0.0])

# The shaded stretch of the trace in beat 5 is every direction scoring below
# this. Not a pass/fail threshold -- the chapter has not defined one, and this
# is never printed. It is the cutoff that makes "sits down near zero" a
# definite set of directions instead of a gesture, and `facts.py` checks the
# fraction the narration claims against it.
BAND_LEVEL = 0.5


class C04(ActScene, ThreeDScene):
    """Turn one direction over a structured cloud and score every angle."""

    def construct(self):
        angle = ValueTracker(ALARMING)
        cloud = CloudRig(data.gaussian_3d(), dot_colour=CLOUD)

        # --- the seam with C03 ---------------------------------------------
        # `build.sh` concatenates approved scene masters with a raw stream
        # copy, so a cut is a cut (VISUAL_SYSTEM.md section 7) and the only way
        # the join reads as continuous is for this first frame to be C03's last
        # one: the same cloud at the same camera, its third direction still
        # standing on its shadow, and the score it had just computed. All of it
        # leaves during beat 1, because the question C04 asks needs a cloud
        # with something to hide.
        self.set_camera_orientation(phi=76 * DEGREES, theta=12 * DEGREES)
        cloud.mount(self, ellipsoid=False)
        # `ThreeDAxes` draws a big white arrow tip on each axis. They belong to
        # C03's frame and are kept for it, then go with the camera: once it is
        # looking nearly straight down at the turning plane, three white
        # arrowheads sitting on the data read as stray arrows -- the exact
        # defect C03's review caught. Nothing in this scene points with an axis.
        axis_tips = [
            (axis, axis.tip)
            for axis in cloud.axes
            if getattr(axis, "tip", None) is not None
            and axis.tip in axis.submobjects
        ]
        # A `ThreeDAxes` does not put its zero at the world origin. `Axes`
        # centres each `NumberLine` on its own bounding box, which includes
        # ticks and a tip, so each axis's zero lands a sixth of a tick off:
        # x at (-0.175, 0, 0), y at (0, -0.175, 0), z at (0, 0, -0.175), and
        # `c2p(0, 0, 0)` -- which combines all three -- at (0.175, -0.175,
        # -0.175). `CloudRig` places its dots at raw world coordinates and the
        # projection line runs through the true origin, so the ticks and
        # anything drawn with `c2p` sit beside the data rather than on it. At
        # C03's oblique angle that reads as depth; looking almost straight down
        # at the turning plane it reads as the direction arrow floating off its
        # own line. Move each axis onto its own zero, which fixes `c2p` with it.
        for axis in cloud.axes.axes:
            axis.shift(-axis.number_to_point(0))
        inherited = CloudProjectionRig(
            cloud, INHERITED_U, lam=EP_LAMBDA, grid=EP_GRID,
        )
        inherited_arrow = inherited.direction_arrow()
        inherited_line = inherited.projection_line()
        inherited_line.set_stroke(opacity=0.38)
        inherited_shadow = inherited.shadow_dots(radius=0.028)
        inherited_shadow.set_opacity(0.88)
        inherited_label = ty.maths(R"u_3", size=ty.EQ, color=DIRECTION)
        inherited_label.move_to(inherited.direction_tip() + 0.28 * UP)
        inherited_score = ty.maths(
            Rf"\operatorname{{score}}(u_3)={inherited.score():.3f}",
            size=ty.EQ_DISPLAY,
            color=DIRECTION,
        ).move_to(METER_POSITION)
        self.add(inherited_line, inherited_arrow)
        self.add_fixed_orientation_mobjects(*inherited_shadow, inherited_label)
        self.add(inherited_shadow)
        self.add_fixed_in_frame_mobjects(inherited_score)
        self.inspect(0.6)

        # --- beat 1: the clumps arrive -------------------------------------
        # One purposeful camera move (VISUAL_SYSTEM.md section 8) that both
        # flattens the view onto the plane the direction will turn in and
        # slides the world left to clear the panels. It runs with the morph, so
        # the beat has one focal event: the cloud gaining structure.
        with self.voiceover(
            text="Now suppose the cloud has structure. "
                 "<bookmark mark='clumps'/>Two clumps, pulled well apart, in a "
                 "plane we can look straight down at."
        ) as tracker:
            # C03's apparatus leaves before the cloud changes, so the beat has
            # one focal event rather than two. Every piece of it is static --
            # `CloudProjectionRig` is a snapshot with no updaters -- so a plain
            # fade is honest here, and each piece is then removed from the scene
            # instead of being left sitting at zero opacity.
            handover = [
                inherited_arrow, inherited_line, inherited_shadow,
                inherited_label, inherited_score,
            ]
            self.play(
                *(FadeOut(mob) for mob in handover),
                run_time=max(0.5, min(1.0, tracker.time_until_bookmark("clumps"))),
            )
            self.remove(*handover, *inherited_shadow)
            self.remove_fixed_in_frame_mobjects(inherited_score)
            self.wait_until_bookmark("clumps")
            self.move_camera(
                phi=20 * DEGREES,
                theta=-90 * DEGREES,
                frame_center=np.array([WORLD_OFFSET, 0.0, 0.0]),
                run_time=max(2.2, tracker.get_remaining_duration() - 0.2),
                added_anims=[
                    cloud.animate_base_points(data.clumped_3d()),
                    # The direction never leaves the x-y plane, so the z axis
                    # goes with the camera rather than foreshortening into a
                    # stub through the middle of the shadow.
                    cloud.axes.z_axis.animate.set_opacity(0.0),
                    *(tip.animate.set_opacity(0.0) for _, tip in axis_tips),
                ],
            )
        # Out of the scene rather than parked at zero opacity: a hidden member
        # of a family is forced back to visible by any later group-wide opacity
        # animation, which is how C03's discrepancy formula reappeared on top of
        # its score.
        cloud.axes.remove(cloud.axes.z_axis)
        for axis, tip in axis_tips:
            axis.remove(tip)

        # The score table is read off the cloud's geometry, so it is built now
        # that the morph has landed -- `TurningProjection` does not recompute.
        projection = TurningProjection(
            cloud,
            angle,
            lam=EP_LAMBDA,
            grid=EP_GRID,
        )
        alarming_score = projection.score_at(ALARMING)
        innocent_score = projection.score_at(INNOCENT)

        # --- the fixed-frame panels ----------------------------------------
        trace_axes = Axes(
            x_range=(0, 180, 45),
            y_range=(0, 18, 6),
            x_length=4.05,
            y_length=2.85,
            tips=False,
            axis_config={
                "stroke_color": AXIS,
                "stroke_width": 1.6,
                "include_ticks": True,
                "tick_size": 0.05,
            },
        ).move_to(TRACE_CENTRE)
        trace_caption = ty.words(
            "score along each direction", size=ty.CAPTION, color=MUTED,
        ).next_to(trace_axes, UP, buff=0.22)
        quarter_turn = ty.maths(R"90^\circ", size=ty.TICK, color=MUTED)
        quarter_turn.next_to(trace_axes.c2p(90, 0), DOWN, buff=0.14)
        half_turn = ty.maths(R"180^\circ", size=ty.TICK, color=MUTED)
        half_turn.next_to(trace_axes.c2p(180, 0), DOWN, buff=0.14)

        # `ty.readout` rather than a hand-built pair: it aligns the Computer
        # Modern label and the DecimalNumber on a measured baseline, and a
        # DecimalNumber rebuilds its glyphs on every `set_value`, so anything
        # scaled or arranged around it afterwards drifts out of place as the
        # digit count changes between 17.095 and 0.046.
        meter = ty.readout(
            R"\operatorname{score}(u)", angle, places=3, color=DIRECTION,
        )
        meter.move_to(METER_POSITION)
        # The one number this scene speaks about, driven by the one angle
        # tracker through the one score table. Nothing else evaluates a score.
        #
        # The re-registration is load-bearing, and it is trap 1 wearing a
        # different hat. `add_fixed_in_frame_mobjects` registers mobject
        # INSTANCES with the camera, and `DecimalNumber.set_value` throws its
        # glyph submobjects away and builds new ones. Those new glyphs are not
        # in the registry, so the 3-D camera projects them: the digits render
        # left of and below the label they were arranged beside, which looks
        # like a layout bug and is not one. Register the family again on every
        # value change. `self.camera.add_fixed_in_frame_mobjects` rather than
        # the scene method, which would also re-`add` the mobject every frame
        # and restructure the scene graph out from under the group.
        def track_score(mob):
            mob.set_value(projection.score_now())
            self.camera.add_fixed_in_frame_mobjects(mob)

        meter[1].add_updater(track_score)

        # A standard normal, drawn in the free space between the two panels and
        # never spoken about. The scene makes two claims about shape -- two
        # piles with a hole, then a single hump -- and this is the thing both
        # are claims against, in TARGET, the palette's role for the Gaussian
        # reference. Nothing labels it and no line of narration points at it: it
        # is there to be compared against by eye, which is the only way a
        # "close enough to a bell" judgement can honestly be made on screen.
        bell = FunctionGraph(
            lambda x: np.exp(-0.5 * x * x), x_range=(-3.2, 3.2, 0.05),
        )
        bell.set_stroke(TARGET, 2.2).set_fill(TARGET, 0.0)
        bell.stretch_to_fit_width(2.25).stretch_to_fit_height(0.62)
        bell.move_to(BELL_CENTRE)
        bell_base = Line(bell.get_corner(DL), bell.get_corner(DR))
        bell_base.set_stroke(TARGET, 1.2)

        # Beat 5's band, marked by its two edges rather than filled. A shaded
        # rectangle behind the curve reads as an area under it -- an integral,
        # which is not the claim -- and it dulls the trace it sits behind.
        # Two dashed boundaries say the same thing about an interval of
        # directions and leave the curve alone. MUTED, not DIRECTION: green
        # verticals crossing a green curve separate badly, and dashed MUTED is
        # already this project's annotation-guide convention
        # (`CloudProjectionRig.guide_lines`).
        #
        # Registered HERE, before the panels and long before the trace, because
        # registration order is draw order and the curve belongs on top.
        band_degrees = np.degrees(
            projection.angles[projection.scores < BAND_LEVEL]
        )
        band = VGroup(*(
            DashedLine(
                trace_axes.c2p(edge, 0.0),
                trace_axes.c2p(edge, 18.0),
                dash_length=0.075,
            ).set_stroke(MUTED, 1.6)
            for edge in (float(band_degrees.min()), float(band_degrees.max()))
        ))
        self.add_fixed_in_frame_mobjects(*band)
        band.set_stroke(opacity=0.0)

        panels = VGroup(
            trace_axes, trace_caption, quarter_turn, half_turn, meter,
        )
        self.add_fixed_in_frame_mobjects(*panels)
        # Stroke and fill named separately, always. `set_opacity` on the bell
        # would raise the fill it is about to be revealed with, and the two are
        # animated to different values.
        self.add_fixed_in_frame_mobjects(bell, bell_base)
        bell.set_stroke(opacity=0.0)
        bell_base.set_stroke(opacity=0.0)
        for mob in panels:
            mob.set_opacity(0.0)

        # --- beat 2: the alarming direction --------------------------------
        arrow = projection.direction_arrow()
        line = projection.projection_line()
        shadow = projection.shadow_dots()
        trace = projection.trace(trace_axes)
        head = projection.head_dot(trace_axes)
        self.add_fixed_in_frame_mobjects(trace, head)
        # Stroke only. `set_opacity` on the trace would raise its fill with it
        # and flood the area under the curve solid white.
        trace.set_stroke(opacity=0.0)
        head.set_opacity(0.0)

        self.add(line)
        # Registering the billboards restructures the scene's top-level
        # mobjects and drops their parent VGroup, which is where the one
        # position updater lives -- so re-add the SAME group afterwards, the
        # way CloudRig.mount does.
        self.add_fixed_orientation_mobjects(*shadow)
        self.add(shadow)
        # After the shadow, so the direction glyph stays legible on top of the
        # 220 feet it is responsible for.
        self.add(arrow)
        arrow.set_opacity(0.0)
        line.set_opacity(0.0)
        shadow.set_opacity(0.0)

        with self.voiceover(
            text="<bookmark mark='along'/>Take the direction the clumps "
                 "separate along. <bookmark mark='piles'/>Then the shadow comes "
                 "out as two piles with a hole between them, "
                 "<bookmark mark='gaussian'/>and a Gaussian has no hole in the "
                 "middle. <bookmark mark='high'/>So the score climbs."
        ) as tracker:
            self.wait_until_bookmark("along")
            self.play(
                arrow.animate.set_opacity(1.0),
                line.animate.set_opacity(0.36),
                run_time=max(0.6, min(1.1, tracker.time_until_bookmark("piles"))),
            )
            self.wait_until_bookmark("piles")
            # The cloud recedes so the shadow reads on top of it: the active
            # object is brighter, the structure behind it dims (handoff
            # section 12), and nothing has to move to make room.
            self.play(
                shadow.animate.set_opacity(0.96),
                AnimationGroup(
                    *(dot.animate.set_opacity(0.3) for dot in cloud.dots),
                    lag_ratio=0.0,
                ),
                run_time=max(
                    0.8, min(1.6, tracker.time_until_bookmark("gaussian")),
                ),
            )
            # The reference arrives on the word it is a reference for, and is
            # then left alone for the rest of the scene.
            self.wait_until_bookmark("gaussian")
            self.play(
                AnimationGroup(
                    bell.animate.set_stroke(opacity=0.85)
                        .set_fill(TARGET, 0.14),
                    bell_base.animate.set_stroke(opacity=0.5),
                    lag_ratio=0.0,
                ),
                run_time=max(0.6, min(1.2, tracker.time_until_bookmark("high"))),
            )
            self.wait_until_bookmark("high")
            self.across(
                tracker,
                AnimationGroup(
                    meter.animate.set_opacity(1.0),
                    trace_axes.animate.set_opacity(1.0),
                    trace_caption.animate.set_opacity(1.0),
                    quarter_turn.animate.set_opacity(1.0),
                    half_turn.animate.set_opacity(1.0),
                    head.animate.set_opacity(1.0),
                    trace.animate.set_stroke(opacity=1.0),
                    lag_ratio=0.0,
                ),
                floor=0.8,
            )
        self.inspect(0.7)

        # --- beat 3: the innocent direction --------------------------------
        with self.voiceover(
            text="<bookmark mark='turn'/>Now turn that direction a quarter of "
                 "the way round. <bookmark mark='merge'/>The two piles slide "
                 "straight through each other, <bookmark mark='bell'/>and what "
                 "is left is a single hump. The score drops to almost nothing."
        ) as tracker:
            self.wait_until_bookmark("turn")
            self.play(
                angle.animate.set_value(INNOCENT),
                run_time=max(
                    3.0,
                    min(6.5, tracker.time_until_bookmark("bell")),
                ),
                rate_func=smooth,
            )
            self.wait_until_bookmark("bell")
            self.across(
                tracker,
                Indicate(meter, color=DIRECTION, scale_factor=1.08),
                floor=0.9,
            )
        # The reference has now done both of its jobs -- the shadow with a hole
        # and the shadow without one have each been seen against it -- so it
        # goes, in the silence after the beat that used it. Leaving it up would
        # make it furniture, and nothing in beats 4 or 5 is a shape judgement.
        # Faded rather than removed outright: it is registered fixed-in-frame
        # and nothing later animates opacity across a group containing it, so
        # trap 3 does not apply.
        self.inspect(
            0.8,
            AnimationGroup(
                bell.animate.set_stroke(opacity=0.0).set_fill(TARGET, 0.0),
                bell_base.animate.set_stroke(opacity=0.0),
                lag_ratio=0.0,
            ),
        )
        self.remove(bell, bell_base)
        self.remove_fixed_in_frame_mobjects(bell, bell_base)

        # --- beat 4: finish the half turn ----------------------------------
        with self.voiceover(
            text="<bookmark mark='keep'/>Keep turning and the hole opens "
                 "again. <bookmark mark='trace'/>Every direction in the plane "
                 "has its own score, and half a turn covers all of them."
        ) as tracker:
            self.wait_until_bookmark("keep")
            self.play(
                angle.animate.set_value(HALF_TURN),
                run_time=max(
                    2.6,
                    min(5.5, tracker.time_until_bookmark("trace")),
                ),
                rate_func=smooth,
            )
            self.wait_until_bookmark("trace")
            # The completed curve is the scene's product, so it thickens and
            # stays thick. An `Indicate` would flash it its own colour, which
            # on a green curve is no change at all.
            self.across(
                tracker,
                trace.animate.set_stroke(width=5.0),
                floor=0.8,
            )

        # --- beat 5: the conclusion ----------------------------------------
        # The turn is over, so the live objects are frozen at their exact
        # endpoint values before anything is marked on top of them. Freezing
        # first is what stops an updater rewriting geometry an animation is
        # transforming (ActScene.freeze).
        self.freeze(trace, head, shadow, arrow, line, meter[1])
        self.remove(head)
        self.remove_fixed_in_frame_mobjects(head)

        alarming_mark = Dot(
            trace_axes.c2p(0.0, alarming_score), radius=0.055,
        ).set_fill(COLLAPSE, 1.0)
        alarming_label = ty.maths(
            f"{alarming_score:.3f}", size=ty.TICK, color=COLLAPSE,
        ).next_to(alarming_mark, RIGHT, buff=0.2).shift(0.12 * DOWN)
        innocent_mark = Dot(
            trace_axes.c2p(90.0, innocent_score), radius=0.055,
        ).set_fill(DIRECTION, 1.0)
        innocent_label = ty.maths(
            f"{innocent_score:.3f}", size=ty.TICK, color=DIRECTION,
        ).next_to(innocent_mark, UP, buff=0.14)
        marks = VGroup(
            alarming_mark, alarming_label, innocent_mark, innocent_label,
        )
        self.add_fixed_in_frame_mobjects(*marks)
        marks.set_opacity(0.0)

        with self.voiceover(
            text="Seventeen here, and almost zero here. "
                 "<bookmark mark='band'/>And half of every direction in this "
                 "plane sits down in that band. <bookmark mark='verdict'/>So "
                 "pick one of them, and this cloud passes. A low score tells "
                 "you about the direction you picked. It tells you nothing "
                 "about the cloud behind it."
        ) as tracker:
            # "here, and here" is deictic, so the two marks are the sentence.
            self.play(
                marks.animate.set_opacity(1.0),
                run_time=max(0.7, min(1.6, tracker.time_until_bookmark("band"))),
            )
            self.wait_until_bookmark("band")
            # The band is the scene's actual verdict: not that one direction
            # happened to be innocent, but that half of them are.
            self.play(
                band.animate.set_stroke(MUTED, opacity=0.8),
                run_time=max(
                    0.6,
                    min(1.3, tracker.time_until_bookmark("verdict")),
                ),
            )
            self.wait_until_bookmark("verdict")
            # The cloud comes back up on "the cloud behind it" -- the same 220
            # dot instances that were there before the turn started, and the
            # thing the closing line is about. No Indicate on top: it would
            # drive the same dots' opacity as the restore and the two fight.
            self.across(
                tracker,
                AnimationGroup(
                    *(dot.animate.set_opacity(0.9) for dot in cloud.dots),
                    lag_ratio=0.0,
                ),
                floor=1.2,
            )
        self.inspect(0.9)

        cloud.freeze()
        self.settle_frame()
