"""Chapter B.2 — the three-panel rig, built and then read.

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
ask one question of one apparatus: b02 builds the curve, b05 notices the curve
was only half of the average arrow. They are now one continuous scene on one
rig, and the batch never changes until the symmetry argument needs it to.

Panel 3 starts by plotting Re phi(t) deliberately, not |phi(t)| — the real part
is literally "how far right do the arrows point on average", which is a thing
you can watch happen in panel 2. The second half of the scene is the payment of
that debt: Im phi(t) joins it on the same axes.

The geometry is ThreePanelRig's, not this scene's. It used to be duplicated
here in four blocks, and the copies drifted: the shared axis labels were fixed
(font 20 -> TICK, `t` pulled inside the safe margin) and this scene silently
kept the old geometry, so b02 rendered a clipped `t` while every other rig scene
did not. That is finding F15, and this is where it happened.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b02_the_rig.py B02 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import data, layout
from common.beat import ActScene
from common.palette import CLOUD, COLLAPSE, EMPIRICAL, TARGET
from common import type as ty
from common.rig import ThreePanelRig

T_MAX = 6.5

# A deliberately small slice of the same two-clump toy distribution from b00.
# Seven points keep each arrow individually visible while preserving the
# question the chapter opened with: what does the arrangement remember?
#
# It also does the second half of this scene's work without a swap: this slice
# is lopsided, so Im phi runs to 0.38 and the imaginary curve is visibly not
# zero. The folded-in b05 used its own SKEWED batch to get 0.41 out of a batch
# nobody had met, which meant changing the data at the exact moment the point
# was that the curve had been hiding something about THIS data all along.
SAMPLES = data.bimodal_1d(7)
# The same batch mirrored, value by value. Every arrow then has a partner at
# the opposite angle, so Im phi is identically zero -- exact, not illustrative.
MIRRORED = np.concatenate([SAMPLES, -SAMPLES])


class B02(ActScene):
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
        the end tick, and made the number line change width at the b02/b05 cut.
        """
        self.rig = ThreePanelRig(SAMPLES, t_max=T_MAX, wrapped_already=False,
                                 line_range=(-3, 3, 1))
        self.titles = layout.rig_titles(
            "the numbers", "wrapped onto the circle", "the average, against t")

    # ------------------------------------------------------------------ 1
    def wrap_beat(self):
        r = self.rig
        dots = always_redraw(r.dots)
        # The line the samples sit on, rolled by the same kappa. Rev-3 finding
        # R5: without it the first nine seconds are loose dots running past the
        # circle panel with nothing under them, so the beat's whole claim --
        # that a LINE is being wrapped -- is the part the frame omits.
        rolling = always_redraw(r.roll_curve)

        # Static copy on the number line: panel 1 keeps the numbers where they
        # are, so the viewer can compare against the wrapped version.
        line_dots = r.line_dots(radius=0.07)

        # The strip's length is t times the batch's range, because that is what
        # `wrapped()` computes -- so growing t stretches it, exactly. Starting
        # small and stretching to 1 turns "multiplying by a frequency" into
        # something the viewer watches. Without it this beat opened with
        # fourteen seconds of a motionless strip while the sentence describing
        # the multiplication played over it, which was the longest still frame
        # left in Part 1 after every other fix had landed.
        with self.voiceover(
            text="Back to the two clumps from the start, thinned to seven "
                 "values so every one of them stays watchable. "
                 "<bookmark mark='angle'/>Each value has to become an angle "
                 "before the arrow picture is any use, and multiplying it by a "
                 "frequency t is the least elaborate way to turn a position "
                 "into one: the bigger t is, the further round each value "
                 "travels. Wrapping that line around the circle is the "
                 "multiplication, drawn."
        ) as tracker:
            r.t.set_value(0.20)
            self.play(Create(r.line), FadeIn(line_dots), run_time=1.2)
            self.add(rolling)
            # The values are carried out onto the strip that is about to be
            # wrapped, rather than both appearing at once with no relation
            # drawn between them.
            snapshot = r.dots()
            self.play(FadeIn(rolling),
                      TransformFromCopy(line_dots, snapshot), run_time=1.5)
            self.remove(snapshot)
            self.add(dots)
            self.wait_until_bookmark("angle")
            # `across` with a reserve, not a fixed play followed by a second
            # bookmark. The clause between the two bookmarks runs about twelve
            # seconds and the stretch took 2.6 of them, so the first pass of
            # this fix still left ten seconds of stopped strip -- the fixed
            # play plus wait_until_bookmark pattern IS the dead-frame
            # generator, and reserving the tail for the wrap is the shape that
            # cannot produce one.
            # Overshoot and settle rather than a single monotone creep. Spread
            # over seven seconds a 0.2 -> 1.0 stretch moves the strip's end by
            # about a pixel per frame, which measures as still; going out past
            # the target and coming back covers half again the distance in the
            # same time, and "bigger t, further round" is what the overshoot is
            # showing.
            self.across(tracker, r.t.animate.set_value(1.28),
                        floor=1.4, reserve=7.4, rate_func=smooth)
            self.play(r.t.animate.set_value(1.0), run_time=1.6,
                      rate_func=smooth)
            self.play(r.kappa.animate.set_value(1.0), run_time=3.2,
                      rate_func=smooth)
            self.play(r.rigid.animate.set_value(1.0), run_time=1.3)

        # The rolled line has become the circle, which is already drawn. Leaving
        # it there doubles the stroke on the unit circle and nothing else.
        rolling.clear_updaters(recursive=True)
        self.play(FadeOut(rolling), run_time=0.4)
        self.remove(rolling)

        rule = ty.maths(R"x \quad\longmapsto\quad e^{itx}", size=ty.EQ_DISPLAY,
                        color=TARGET)
        rule.move_to(np.array([0.0, -2.75, 0.0]))

        with self.voiceover(
            text="A value x lands at the angle t x, so samples further "
                 "from zero travel further round."
        ) as tracker:
            self.play(FadeIn(r.circle), FadeIn(self.titles[0]),
                      FadeIn(self.titles[1]), run_time=1.0)
            self.play(Write(rule), run_time=1.2)
            self.across(tracker, Indicate(rule, scale_factor=1.06,
                                          color=TARGET), floor=0.8)

        # The translation rule is the one thing this chapter cannot be watched
        # without. Silence, with it on screen and the wrapped dots beside it.
        self.inspect(1.6)

        self.rule = rule
        self.line_dots, self.dots = line_dots, dots

        # This scene builds the rig by hand rather than through mount(), because
        # it is the one scene that starts unwrapped. mount() is also what
        # normally records the panel-1 dots for swap() to replace, so hand them
        # over now: the symmetry beat at the end of this scene calls swap(), and
        # without this it would remove(None) and take the whole render down.
        r.mounted_dots = line_dots
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
                           stroke_width=6.4, tip_length=0.24).set_color(COLLAPSE)
        mean_dot = Dot(mean_tip, radius=0.1).set_fill(COLLAPSE, 1)

        with self.voiceover(
            text="Each landing point is a unit arrow, and "
                 "<bookmark mark='avg'/>their average is a single point "
                 "inside the circle."
        ) as tracker:
            self.play(lagged_map(GrowArrow, starts, lag_ratio=0.10),
                      run_time=1.5)
            self.remove(starts)
            self.add(arrows)
            self.wait_until_bookmark("avg")
            self.play(GrowArrow(mean_arrow), FadeIn(mean_dot), run_time=1.0)
            self.remove(mean_arrow, mean_dot)
            self.add(centroid)
            self.across(tracker, Indicate(centroid, scale_factor=1.15,
                                          color=COLLAPSE), floor=0.8)

        self.arrows, self.centroid = arrows, centroid

    # ------------------------------------------------------------------ 3
    def sweep_beat(self):
        r = self.rig

        with self.voiceover(
            text="That average is one complex number, and plotting its "
                 "horizontal coordinate against t, on the right, gives the "
                 "first point of a curve."
        ) as tracker:
            self.play(Create(r.axes), FadeIn(r.axis_labels()),
                      FadeIn(self.titles[2]), run_time=1.3)
            self.add(always_redraw(r.trace), always_redraw(r.rider),
                     always_redraw(r.link), always_redraw(r.readout))
            # "gives the first point of a curve" -- so a first stub of curve is
            # traced. An Indicate on the panel caption filled this block on the
            # first pass, which measured five motionless seconds.
            self.across(tracker, r.t.animate.set_value(1.4), floor=0.9,
                        rate_func=there_and_back)

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
            text="Raising t moves two of the three panels. The samples on "
                 "the left do not move at all: the data is fixed, and only "
                 "the question being asked of it changes. On the circle, "
                 "samples further from zero accumulate angle faster, so "
                 "over this early stretch the arrows separate and the "
                 "average is pulled in toward the centre. Keep going and "
                 "the arrows carry on turning, fall part way back into "
                 "step, and the average grows again. The curve on the "
                 "right records where that average keeps landing, and it "
                 "rises and falls as the arrows drift in and out of step."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(T_MAX),
                        floor=6.0, rate_func=linear)

        # The standalone closing block that sat here is gone. It was one
        # sentence played over a completely motionless rig -- seven seconds at
        # 00:03:12 of the rev-3 master, with t parked at 6.50 -- and it said
        # what the next beat then re-said. Its one useful clause now opens the
        # next beat, over the sweep running back down.

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
            text="One frequency gave one answer, and sweeping gave the whole "
                 "curve. But that curve has been keeping only the horizontal "
                 "coordinate of the average arrow, and the arrow has been "
                 "moving up and down this whole time as well."
        ) as tracker:
            self.play(FadeOut(self.rule), run_time=0.4)
            # Run t back to where the average sits well off the horizontal, so
            # the sentence's last clause is a thing happening on screen.
            self.across(tracker, r.t.animate.set_value(1.35), floor=1.8,
                        rate_func=smooth)

        with self.voiceover(
            text="<bookmark mark='split'/>Split the average into its "
                 "components. The blue piece is how far right the arrows "
                 "point on average, the red piece how far up. Those are the "
                 "real and imaginary parts of phi."
        ) as tracker:
            self.wait_until_bookmark("split")
            # Fade in a throwaway snapshot, then hand over to the live one --
            # the same pattern as the arrow hand-over in b01, and for a related
            # reason. always_redraw rebuilds comps every frame, and the dashed
            # connector's submobject count changes with its length (a 0.3-unit
            # dash line has 3 dashes, a 2.4-unit one has 20). Manim Community
            # zips a mobject against the copy taken at begin() with strict=True,
            # so a family that changes size mid-animation raises
            # "zip() argument 2 is shorter than argument 1" from deep inside
            # interpolate_mobject, naming neither the mobject nor the scene.
            seed = r.centroid_components()
            self.play(FadeIn(seed), run_time=0.9)
            self.remove(seed)
            self.add(comps)
            self.play(FadeIn(legend), run_time=0.7)
            self.across(tracker, r.t.animate.set_value(1.9), floor=0.9,
                        rate_func=there_and_back)

        defn = ty.maths(
            R"\varphi(t) = \underbrace{\mathbb{E}[\cos tX]}_{\text{right}}"
            R" + i\, \underbrace{\mathbb{E}[\sin tX]}_{\text{up}}",
            size=ty.EQ)
        defn.move_to(np.array([0.0, -3.15, 0.0]))
        layout.fit_in_frame(defn)

        with self.voiceover(
            text="Averaging the cosines gives the sideways component, "
                 "averaging the sines gives the upward one."
        ) as tracker:
            self.play(FadeOut(legend), run_time=0.4)
            self.play(Write(defn), run_time=1.4)
            self.across(tracker, r.t.animate.set_value(1.05), floor=0.8,
                        rate_func=smooth)

        # The formula and the split arrow are on screen together, and the
        # correspondence between them is the thing to check. Near-silence for
        # it, with the split still answering to t so there is something to look
        # at while looking.
        self.inspect(1.5, r.t.animate.set_value(1.6), rate_func=there_and_back)

        self.comps, self.defn = comps, defn

    # ------------------------------------------------------------------ 5
    def two_curves_beat(self):
        """Both coordinates, plotted together, as t sweeps. (Formerly b05.2.)

        The real curve is the one already on the axes -- the same mobject the
        viewer watched get drawn -- so this beat adds a curve rather than
        replacing a panel. b05 used to mount its own pair, which is why the two
        scenes could not be watched as one.
        """
        r = self.rig
        im_curve = always_redraw(lambda: r.trace_imag())
        im_dot = always_redraw(lambda: r.rider_imag())

        re_lab = ty.maths(R"\mathrm{Re}\,\varphi", size=ty.TICK,
                          color=EMPIRICAL)
        re_lab.move_to(r.axes.c2p(5.4, 0.78))
        im_lab = ty.maths(R"\mathrm{Im}\,\varphi", size=ty.TICK,
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
            text="So the picture on the right is half finished. Give the "
                 "upward coordinate its own curve and sweep the frequency "
                 "again, and the two of them together track one point moving "
                 "in the plane -- which is why dropping either one loses "
                 "information the other cannot supply."
        ) as tracker:
            r.t.set_value(0.0)
            self.add(im_curve, im_dot)
            self.play(FadeIn(re_lab), FadeIn(im_lab),
                      FadeOut(self.titles[2], shift=0.15 * UP),
                      FadeIn(new_title, shift=0.15 * UP), run_time=0.9)
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=5.0,
                        rate_func=linear)

        self.im_curve, self.im_dot = im_curve, im_dot
        self.re_lab, self.im_lab = re_lab, im_lab

    # ------------------------------------------------------------------ 6
    def symmetry_beat(self):
        """Symmetric batch => Im phi identically zero, exactly. (b05.3.)"""
        r = self.rig

        with self.voiceover(
            text="Now mirror the batch: keep every value and add its opposite, "
                 "so each one has a partner the same distance away on the "
                 "other side of zero."
        ) as tracker:
            self.play(FadeOut(self.defn), run_time=0.4)
            r.swap(self, MIRRORED)
            self.across(tracker, r.t.animate.set_value(1.35), floor=1.2)

        # Was a bare self.wait(0.5) under eleven seconds of narration -- a
        # frozen frame with a voice over it, while the sentence describes a
        # pairing the picture could be showing. It shows it now: the arrows
        # walk far enough for the mirror pairs to be visibly opposite, and the
        # average stays pinned to the horizontal.
        with self.voiceover(
            text="Each pair wraps to a pair of arrows at opposite angles, "
                 "so whatever one contributes upward the other "
                 "contributes downward by the same amount. The vertical "
                 "components cancel pair by pair, which leaves the "
                 "average nowhere to go except along the horizontal axis."
        ) as tracker:
            self.across(tracker, r.t.animate.set_value(2.4), floor=2.0)

        with self.voiceover(
            text="The sweep agrees: the red curve sits at exactly zero "
                 "across the whole range."
        ) as tracker:
            r.t.set_value(0.0)
            self.across(tracker, r.t.animate.set_value(T_MAX), floor=5.0,
                        rate_func=linear)

        result = ty.line("$X$", "symmetric about", "$0$", R"$\Longrightarrow$",
                         R"$\mathrm{Im}\,\varphi(t) = 0$", size=ty.BODY,
                         color=TARGET)
        result.move_to(np.array([0.0, -3.15, 0.0]))
        layout.fit_in_frame(result)

        with self.voiceover(
            text="So a symmetric distribution has a purely real characteristic "
                 "function. The Gaussian is symmetric, so the target this "
                 "chapter is heading toward will be a single real curve, and "
                 "that now follows from the pairing argument instead of being "
                 "a convenience of the drawing."
        ) as tracker:
            self.play(Write(result), run_time=1.3)
            self.across(tracker, r.t.animate.set_value(3.4), floor=1.0,
                        rate_func=there_and_back)

        self.clear_beat()
