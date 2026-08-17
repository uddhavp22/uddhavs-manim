"""Chapter B.3 — the three-panel rig, built and then read.

    numbers on a line  <->  arrows on the circle  <->  phi(t) vs t

All three panels move from one `t`. The link that makes it a single mechanism
rather than three charts: **the horizontal position of the average arrow IS the
height of the curve.** A guide line is drawn between them so the viewer sees
that, rather than being told it.

**b05_real_and_imaginary.py has been folded into this file.** It was a separate
scene, so the master cut faded the entire rig to background and rebuilt an
almost identical rig one second later with different panel captions and a
different batch -- the sharpest chop in Part 1, at 00:03:19 of the rev-3 master,
and the clearest case of "one investigation, cut into episodes". The two scenes
ask one question of one apparatus: this scene builds the curve, then notices it
was only half of the average arrow. They are now one continuous scene on one
rig, and the batch never changes until the symmetry argument needs it to.

Panel 3 starts by plotting Re phi(t) deliberately, not |phi(t)| — the real part
is literally "how far right do the arrows point on average", which is a thing
you can watch happen in panel 2. The second half of the scene is the payment of
that debt: Im phi(t) joins it on the same axes.

The geometry is ThreePanelRig's, not this scene's. It used to be duplicated
here in four blocks, and the copies drifted: the shared axis labels were fixed
(font 20 -> TICK, `t` pulled inside the safe margin) and this scene silently
kept the old geometry, so this scene rendered a clipped `t` while every other rig scene
did not. That is finding F15, and this is where it happened.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b03_the_rig.py B03 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import layout
from common.beat import ActScene
from common.palette import AVERAGE, CLOUD, COLLAPSE, EMPIRICAL, TARGET
from common import type as ty
from common.rig import ThreePanelRig

T_MAX = 6.5

# Seven deliberately separated values. At this scale, a viewer can follow each
# dot from the number line onto the circle without two samples merging into one
# marker. The batch is also mildly asymmetric, so both coordinates of its
# average remain visible at the end of the complete frequency sweep.
SAMPLES = np.array([-1.95, -1.20, -0.70, -0.20, 0.30, 0.80, 1.80])
# The same batch mirrored, value by value. Every arrow then has a partner at
# the opposite angle, so Im phi is identically zero -- exact, not illustrative.
MIRRORED = np.concatenate([SAMPLES, -SAMPLES])


class B03(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.build_rig()
        self.wrap_beat()
        self.average_beat()
        self.sweep_beat()
        # --- what used to be b05, on the same rig, with no cut ---------
        self.components_beat()
        self.two_curves_beat()
        self.symmetry_beat()

    # ------------------------------------------------------------------
    def build_rig(self):
        """Panels and trackers shared by every beat in this scene.

        `wrapped_already=False` starts kappa and rigid at zero, which is what
        lets the first beat straighten the circle back into a number line and
        wrap it -- the one thing this scene does that no other rig scene does.

        line_range is (-3, 3), matching every other rig scene. It was (-2, 2)
        here alone, which put the largest sample of this batch (1.95) on top of
        the end tick, and made the number line change width at the old scene cut.
        """
        self.rig = ThreePanelRig(SAMPLES, t_max=T_MAX, wrapped_already=False,
                                 line_range=(-3, 3, 1))
        self.titles = layout.rig_titles(
            "number line", "unit directions",
            "horizontal coordinate")

    # ------------------------------------------------------------------ 1
    def wrap_beat(self):
        r = self.rig
        # Match the numbered line's scale exactly while the wrapping strip is
        # straight: 3.9 screen units / 6 data units = radius * t.
        r.t.set_value(layout.RIG_LINE_WIDTH / (6 * layout.RIG_CIRCLE_RADIUS))
        # Position by the axis itself, not NumberLine's bounding-box centre.
        # The latter includes the labels, which puts dots visibly below the
        # stroke even when both objects have the same reported centre.
        opening_axis = np.array([0.0, -0.85, 0.0])
        carrier_axis_y = 0.75
        r.line.shift(opening_axis - r.line.number_to_point(0))

        # These are literally the dots on the numbered line. After they rise,
        # the wrapping updater takes ownership of this same group.
        dots = r.line_dots(radius=0.07)
        strip_offset = ValueTracker(
            carrier_axis_y - layout.RIG_CIRCLE_CENTRE[1]
        )

        def place_strip(mob, factory):
            mob.become(factory().shift(strip_offset.get_value() * UP))

        # Build the final left-panel dots from the current number line and the
        # exact displacement that will move that line into the shared rig.
        # FadeIn(..., shift=line_shift) makes them emerge with the moving line;
        # they do not fly back from the raised strip.
        line_shift = layout.RIG_LINE_CENTRE - r.line.get_center()
        home_dots = r.line_dots(radius=0.07).shift(line_shift)

        readout = always_redraw(r.readout)

        # Introduce the notation on one actual sample before the batch becomes
        # a strip.  The ring is a temporary attention cue, not a new datum.
        sample_index = 5
        sample_ring = Circle(radius=0.15).set_stroke(TARGET, 3)
        sample_ring.move_to(dots[sample_index])
        sample_label = ty.maths(R"x_i", size=ty.EQ, color=TARGET)
        sample_label.next_to(sample_ring, UP, buff=0.13)

        angle_rule = ty.maths(
            R"x_i \longmapsto \theta_i = {t}x_i",
            size=ty.EQ_DISPLAY,
            isolate=[R"{t}"],
        ).move_to(np.array([0.0, -2.75, 0.0]))
        angle_rule.set_color_by_tex(R"{t}", TARGET)
        layout.fit_in_frame(angle_rule)

        with self.voiceover(
            text="So if we want to wrap these samples around a circle, each one "
                 "<bookmark mark='each'/>needs an angle. "
                 "<bookmark mark='sample'/>Take this one. Its "
                 "position on the line is x sub i."
        ) as tracker:
            self.play(
                AnimationGroup(
                    Create(r.line),
                    FadeIn(dots),
                    lag_ratio=0.22,
                ),
                run_time=0.68,
                rate_func=smooth,
            )
            self.wait_until_bookmark("each")
            self.play(Indicate(dots, color=CLOUD, scale_factor=1.035),
                      run_time=0.45)
            self.wait_until_bookmark("sample")
            self.play(
                Create(sample_ring),
                FadeIn(sample_label, shift=0.08 * UP),
                run_time=0.5,
                rate_func=smooth,
            )

        with self.voiceover(
            text="<bookmark mark='rule'/>The parameter t controls how quickly "
                 "position turns into "
                 "angle. <bookmark mark='sample_angle'/>For this sample, the "
                 "angle is "
                 "t times x sub i."
        ) as tracker:
            self.play(
                FadeIn(readout),
                run_time=0.4,
                rate_func=smooth,
            )
            self.wait_until_bookmark("rule")
            self.play(
                Write(angle_rule),
                run_time=0.7,
                rate_func=smooth,
            )
            self.wait_until_bookmark("sample_angle")
            self.play(
                Indicate(VGroup(sample_ring, sample_label),
                         color=TARGET, scale_factor=1.04),
                Wiggle(angle_rule.get_part_by_tex(R"{t}"),
                       scale_value=1.18, n_wiggles=3),
                run_time=0.55,
            )

        with self.voiceover(
            text="With an angle attached to every sample, "
                 "<bookmark mark='wrap'/>the whole strip can wrap around the "
                 "circle."
        ) as tracker:
            lead = tracker.time_until_bookmark("wrap")
            self.play(
                dots.animate.shift((carrier_axis_y - opening_axis[1]) * UP),
                FadeOut(sample_ring),
                FadeOut(sample_label),
                run_time=max(0.42, 0.58 * lead),
                rate_func=smooth,
            )
            carrier = r.roll_curve().shift(strip_offset.get_value() * UP)
            self.play(
                Create(carrier),
                run_time=max(0.3, 0.32 * lead),
                rate_func=smooth,
            )
            # r.dots() at kappa=0 has the same horizontal scale as the number
            # line. Attaching the updater here produces no handoff or reset.
            dots.add_updater(lambda mob: place_strip(mob, r.dots))
            dots.update(0)
            carrier.add_updater(lambda mob: place_strip(mob, r.roll_curve))
            self.wait_until_bookmark("wrap")
            self.play(
                r.line.animate.shift(line_shift),
                strip_offset.animate.set_value(0.0),
                r.kappa.animate.set_value(1.0),
                r.rigid.animate.set_value(1.0),
                FadeIn(r.circle),
                FadeIn(home_dots, shift=line_shift),
                run_time=1.1,
                rate_func=smooth,
            )

        rule = ty.maths(
            R"x_i \longmapsto e^{i{t}x_i}",
            size=ty.EQ_DISPLAY,
            isolate=[R"{t}"],
        )
        rule.set_color_by_tex(R"{t}", TARGET)
        rule.move_to(np.array([0.0, -2.75, 0.0]))

        # The formula contains three i glyphs: the index on the input, the
        # imaginary unit, and the index on the exponent's x.  Use the isolated
        # t as a stable landmark so the spoken distinction can wiggle the two
        # relevant glyphs without changing the notation on screen.
        rule_glyphs = [
            mob for mob in rule.family_members_with_points()
            if not mob.submobjects
        ]
        t_glyph = rule.get_part_by_tex(R"{t}")
        imaginary_i = min(
            (mob for mob in rule_glyphs
             if mob.get_center()[0] < t_glyph.get_center()[0]),
            key=lambda mob: t_glyph.get_center()[0] - mob.get_center()[0],
        )
        index_i = max(rule_glyphs, key=lambda mob: mob.get_center()[0])

        with self.voiceover(
            text="We write the direction as e raised to i t x sub i, where "
                 "<bookmark mark='imaginary_i'/>this i is the imaginary unit, "
                 "and <bookmark mark='index_i'/>this i indexes x."
        ) as tracker:
            self.play(
                FadeIn(self.titles[0]), FadeIn(self.titles[1]),
                TransformMatchingTex(angle_rule, rule),
                run_time=0.75,
                rate_func=smooth,
            )
            self.wait_until_bookmark("imaginary_i")
            self.play(
                Wiggle(imaginary_i, scale_value=1.22,
                       rotation_angle=0.035 * TAU, n_wiggles=4),
                run_time=0.7,
            )
            self.wait_until_bookmark("index_i")
            self.play(
                Wiggle(index_i, scale_value=1.22,
                       rotation_angle=0.035 * TAU, n_wiggles=4),
                run_time=0.7,
            )

        with self.voiceover(
            text="When we change t, the samples do not move, but their angles "
                 "on the unit circle change, and the values farther from "
                 "zero turn faster. Each t asks the same batch a different "
                 "alignment question."
        ) as tracker:
            self.play(
                r.t.animate.set_value(1.6),
                run_time=max(2.2, tracker.duration),
                rate_func=linear,
            )

        self.freeze(carrier)
        self.play(FadeOut(carrier), run_time=0.4)
        self.remove(carrier)

        # The translation rule is the one thing this chapter cannot be watched
        # without. Silence, with it on screen and the wrapped dots beside it.
        self.inspect(0.8)

        self.rule = rule
        self.line_dots, self.dots = home_dots, dots
        self.readout = readout

        r.mounted_dots = home_dots
        r._dot_radius = 0.07

    # ------------------------------------------------------------------ 2
    def average_beat(self):
        r = self.rig
        arrows = always_redraw(r.arrows)
        centroid = always_redraw(r.centroid)

        # Do not let the arrows or their average simply appear. At this first
        # encounter, the viewer needs to see every arrow leave the origin and
        # then see the differently coloured average emerge from them.
        starts = VGroup(*(
            Arrow(r.circle.get_center(), tip, buff=0.0, stroke_width=2.6,
                  tip_length=0.20).set_color(CLOUD)
            for tip in r.tips()
        ))
        mean_tip = r.centroid_point()
        mean_arrow = Arrow(r.circle.get_center(), mean_tip, buff=0.0,
                           stroke_width=6.0,
                           tip_length=layout.AVERAGE_ARROW_TIP_LENGTH)
        mean_arrow.set_color(AVERAGE)
        mean_dot = Dot(mean_tip, radius=layout.ARROW_TIP_DOT_RADIUS)
        mean_dot.set_fill(AVERAGE, 1)

        with self.voiceover(
            text="Average the directions. <bookmark mark='mean'/>At this value "
                 "of t, the whole batch leaves one arrow."
        ) as tracker:
            self.play(lagged_map(GrowArrow, starts, lag_ratio=0.10),
                      run_time=max(0.8, tracker.time_until_bookmark("mean")))
            self.remove(starts, *starts)
            self.add(arrows)
            self.wait_until_bookmark("mean")
            self.play(
                Indicate(arrows, color=CLOUD, scale_factor=1.08),
                run_time=0.35,
            )
            self.play(GrowArrow(mean_arrow), FadeIn(mean_dot), run_time=0.55)
            self.remove(mean_arrow, mean_dot)
            self.add(centroid)

        self.arrows, self.centroid = arrows, centroid

    # ------------------------------------------------------------------ 3
    def sweep_beat(self):
        r = self.rig

        trace = always_redraw(r.trace)
        rider = always_redraw(r.rider)
        link = always_redraw(r.link)
        axis_labels = r.axis_labels()

        with self.voiceover(
            text="At one value of t, that arrow lands at one point. The blue "
                 "graph records only <bookmark mark='project'/>how far right "
                 "that point lies."
        ) as tracker:
            self.play(
                Create(r.axes),
                FadeIn(axis_labels), FadeIn(self.titles[2]),
                run_time=0.7,
                rate_func=smooth,
            )
            self.wait_until_bookmark("project")
            trace_seed = r.trace()
            rider_seed = r.rider()
            link_seed = r.link()
            self.play(
                Create(trace_seed),
                Create(link_seed),
                TransformFromCopy(self.centroid[1], rider_seed,
                                  path_arc=-0.25),
                run_time=0.85,
                rate_func=smooth,
            )
            self.remove(trace_seed, rider_seed, link_seed)
            self.add(trace, rider, link)

        # Correction 1 (SCRIPT_REVISION_partA.md Step 3).
        #
        # This block used to say the arrows separate and "the average pulls in
        # toward the centre", stated over a whole sweep with no locality. That
        # generalises a local observation into a false global one: |phi| is not
        # monotone in t. On this very batch it falls to 0.03 near t = 4 and is
        # back up at 0.31 by t = 6.5, so the old sentence was contradicted by
        # the animation playing underneath it -- the "universal-looking
        # parameter sweep" of RENDER_REVIEW_SPEC.md section 6.4.
        #
        # The replacement scopes the observation and names what actually
        # happens further out, which the viewer can check against the curve.
        with self.voiceover(
            text="If we vary t, we see how the horizontal average traces "
                 "the curve."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX),
                        floor=4.8, reserve=0.3, rate_func=linear)

        self.trace, self.rider, self.link = trace, rider, link

        # The standalone closing block that sat here is gone. It was one
        # sentence played over a completely motionless rig -- seven seconds at
        # 00:03:12 of the rev-3 master, with t parked at 6.50 -- and it said
        # what the next beat then re-said. Its one useful clause now opens the
        # next beat, where the same average is decomposed in place.

    # ------------------------------------------------------------------ 4
    def components_beat(self):
        """The curve was only half of the average arrow. (Formerly b05, beat 1.)

        No cut, no re-mount, no new batch: the rig the viewer has been watching
        for a minute simply gets asked a sharper question about the same
        picture, which is what makes the two halves one investigation.
        """
        r = self.rig
        comps = always_redraw(lambda: r.centroid_components())

        # Names the two coloured segments, on the segments' own terms. Not a
        # slogan: RENDER_REVIEW_SPEC.md section 12 forbids colour alone
        # carrying a distinction, so each piece is named where it is drawn.
        legend = VGroup(
            ty.curve_label("how far right, on average", EMPIRICAL),
            ty.curve_label("how far up, on average", COLLAPSE),
        ).arrange(DOWN, buff=0.2)
        legend.move_to(np.array([0.0, -3.15, 0.0]))
        layout.fit_in_frame(legend)

        with self.voiceover(
            text="But that curve only tracks where the arrow points sideways. "
                 "It <bookmark mark='imaginary'/>also has a vertical "
                 "coordinate."
        ) as tracker:
            # The long dotted guide has finished its one job: establishing the
            # real-coordinate graph point. Decompose the average locally from
            # here, so both coordinates get equal visual treatment without a
            # second guide crossing the frame.
            self.freeze(self.link)
            self.play(FadeOut(self.rule), FadeOut(self.link), run_time=0.4)
            self.remove(self.link)

            seed = r.centroid_components()
            self.play(
                GrowFromPoint(seed[0], layout.RIG_CIRCLE_CENTRE),
                run_time=0.55,
                rate_func=smooth,
            )
            self.wait_until_bookmark("imaginary")
            self.play(
                GrowFromPoint(seed[1], seed[0].get_end()),
                run_time=0.55,
                rate_func=smooth,
            )
            self.remove(seed, *seed)
            self.add(comps)

        with self.voiceover(
            text="<bookmark mark='horizontal'/>The horizontal and "
                 "<bookmark mark='vertical'/>vertical components locate the "
                 "same endpoint."
        ) as tracker:
            self.wait_until_bookmark("horizontal")
            self.play(FadeIn(legend[0]), run_time=0.35)
            self.wait_until_bookmark("vertical")
            self.play(FadeIn(legend[1]), run_time=0.35)
            self.play(ShowPassingFlash(r.centroid_components(),
                                       time_width=0.55),
                      run_time=0.65)

        defn = ty.maths(
            R"\overline{e^{itx_i}}"
            R" = \underbrace{\overline{\cos(tx_i)}}_{\text{right}}"
            R" + i\, \underbrace{\overline{\sin(tx_i)}}_{\text{up}}",
            size=ty.EQ,
            isolate=[R"\overline{e^{itx_i}}",
                     R"\overline{\cos(tx_i)}",
                     R"\overline{\sin(tx_i)}"])
        defn.move_to(np.array([0.0, -3.15, 0.0]))
        layout.fit_in_frame(defn)

        with self.voiceover(
            text="<bookmark mark='formula'/>Written out, they are the batch "
                 "averages of <bookmark mark='cosine'/>the cosine of t times "
                 "x sub i, and <bookmark mark='sine'/>the sine of t times x "
                 "sub i. <bookmark mark='bar'/>The bar means: evaluate every "
                 "sample in the batch, then average the results."
        ) as tracker:
            self.play(FadeOut(legend), run_time=0.4)
            self.wait_until_bookmark("formula")
            self.play(Write(defn), run_time=0.7)
            self.wait_until_bookmark("cosine")
            self.play(Indicate(defn.get_part_by_tex(
                               R"\overline{\cos(tx_i)}"),
                               color=EMPIRICAL, scale_factor=1.04),
                      run_time=0.45)
            self.wait_until_bookmark("sine")
            self.play(Indicate(defn.get_part_by_tex(
                               R"\overline{\sin(tx_i)}"),
                               color=COLLAPSE, scale_factor=1.04),
                      run_time=0.45)
            self.wait_until_bookmark("bar")
            self.play(Indicate(defn.get_part_by_tex(
                               R"\overline{e^{itx_i}}"),
                               color=TARGET, scale_factor=1.04),
                      run_time=0.45)

        # The formula and the split arrow are on screen together, and the
        # correspondence between them is the thing to check. Near-silence for
        # it. The frequency remains fixed until the imaginary curve exists;
        # otherwise the moving red component has no plotted counterpart yet.
        self.inspect(1.0)

        self.comps, self.defn = comps, defn

    # ------------------------------------------------------------------ 5
    def two_curves_beat(self):
        """Both coordinates, plotted together. (Formerly b05.2.)

        The real curve is the one already on the axes -- the same mobject the
        viewer watched get drawn -- so this beat adds a curve rather than
        replacing a panel. b05 used to mount its own pair, which is why the two
        scenes could not be watched as one.
        """
        r = self.rig
        im_curve = always_redraw(lambda: r.trace_imag())
        im_dot = always_redraw(lambda: r.rider_imag())

        re_lab = ty.maths(R"\overline{\cos(tx_i)}", size=ty.TICK,
                          color=EMPIRICAL)
        re_lab.move_to(r.axes.c2p(5.4, 0.78))
        im_lab = ty.maths(R"\overline{\sin(tx_i)}", size=ty.TICK,
                          color=COLLAPSE)
        im_lab.move_to(r.axes.c2p(5.4, -0.78))

        # The third caption changes, because what panel 3 holds has changed.
        # The other two do not: the numbers are still the numbers and the
        # circle still holds wrapped arrows, and renaming a panel that has not
        # changed is how "the same rig throughout" quietly stops being true.
        new_title = ty.caption("both coordinates, against t")
        new_title.move_to(self.titles[2].get_center())
        layout.fit_in_frame(new_title)

        with self.voiceover(
            text="One curve follows the horizontal average; "
                 "<bookmark mark='vertical'/>the other follows the vertical "
                 "average. <bookmark mark='full'/>Together they "
                 "preserve the average arrow for every t."
        ) as tracker:
            self.play(
                Indicate(self.trace, color=EMPIRICAL, scale_factor=1.08),
                FadeIn(re_lab),
                run_time=max(0.5, tracker.time_until_bookmark("vertical")),
            )
            self.wait_until_bookmark("vertical")

            # Draw the imaginary trace up to the frequency already on screen,
            # then hand it to the live updater. Resetting t to zero here made
            # the entire rig jump before this beat's first animation.
            im_seed = r.trace_imag()
            dot_seed = r.rider_imag()
            self.play(
                Create(im_seed), FadeIn(dot_seed),
                FadeIn(im_lab),
                run_time=max(0.8, tracker.time_until_bookmark("full")),
            )
            self.remove(im_seed, dot_seed)
            self.add(im_curve, im_dot)
            self.wait_until_bookmark("full")
            self.play(
                      FadeOut(self.titles[2], shift=0.15 * UP),
                      FadeIn(new_title, shift=0.15 * UP), run_time=0.55)

        self.im_curve, self.im_dot = im_curve, im_dot
        self.re_lab, self.im_lab = re_lab, im_lab

    # ------------------------------------------------------------------ 6
    def symmetry_beat(self):
        """Symmetric batch => vertical average identically zero. (b05.3.)"""
        r = self.rig

        with self.voiceover(
            text="At t equals zero, every direction equals one, so the "
                 "average is one."
        ) as tracker:
            self.play(FadeOut(self.defn), run_time=0.4)
            self.across(tracker, r.t.animate.set_value(0.0), floor=2.4,
                        rate_func=smooth)

        # The purple resultant stayed visible throughout the decomposition.
        # At t=0, retire only the component overlay.
        component_seed = r.centroid_components()
        self.remove(self.comps)
        self.add(component_seed)
        self.play(FadeOut(component_seed), run_time=0.55)

        partner_dots = r.line_dots(radius=r._dot_radius, samples=-SAMPLES)
        with self.voiceover(
            text="In a symmetric batch, each x sub i has a partner at negative "
                 "x sub i."
        ) as tracker:
            self.play(
                LaggedStart(*(
                    TransformFromCopy(source, target)
                    for source, target in zip(r.mounted_dots, partner_dots)
                ), lag_ratio=0.08, rate_func=smooth),
                Indicate(self.titles[0], color=TARGET, scale_factor=1.08),
                run_time=2.6,
            )

        original_dots = r.mounted_dots
        self.add(partner_dots)
        r.mounted_dots = VGroup(original_dots, partner_dots)
        r.set_batch(MIRRORED)

        with self.voiceover(
            text="Those partners have equal and opposite vertical components, "
                 "so they cancel for every t. The average stays horizontal, "
                 "and the vertical curve stays at zero."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=4.0,
                        rate_func=linear)

        result = ty.line("$X$", "symmetric about", "$0$", R"$\Longrightarrow$",
                         R"$\operatorname{Im}\varphi_X(t) = 0$", size=ty.BODY,
                         color=TARGET)
        result.move_to(np.array([0.0, -3.15, 0.0]))
        layout.fit_in_frame(result)

        with self.voiceover(
            text="Perfect symmetry pins the vertical curve at zero. "
                 "That is why the Gaussian target lies on the real axis. "
                 "But a finite batch rarely contains exact mirror pairs, so "
                 "its empirical point can still have a vertical component."
        ) as tracker:
            self.play(Write(result), run_time=1.15)
            self.across(
                tracker,
                r.t.animate.set_value(0.0),
                floor=2.8,
                rate_func=linear,
            )

        self.clear_beat()
