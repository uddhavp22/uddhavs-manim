"""Chapter B.2 — complex numbers as arrows.

The one prerequisite the rest of Chapter B leans on, and nothing more:

    a complex number can be pictured as an arrow from the origin
    e^{i theta} is the unit arrow at angle theta
    adding arrows is tip-to-tail, so averaging them is a centroid
    arrows that agree give a long average; arrows that spread cancel

Deliberately no Taylor series and no "e to the i pi plus one". The only property
used downstream is that e^{i theta} is a unit arrow at angle theta, so that is
the only property introduced. Everything after this scene is arrows.

Render:
    ./render.sh projects/sigreg_explainer/chapterB/b02_arrows.py B02 -ql
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import layout
from common.beat import ActScene
from common.palette import AVERAGE, CLOUD, COLLAPSE, EMPIRICAL, FAINT, MUTED, TARGET
from common import type as ty


CENTRE = np.array([-3.1, -0.35, 0.0])
RADIUS = 2.05


def plane(centre=CENTRE, r=RADIUS):
    """Unit circle with real and imaginary axes. Local rather than
    layout.complex_panel() because this scene labels the axes, and the labels
    have to be positioned against the same radius."""
    return VGroup(
        Line(1.45 * r * LEFT, 1.45 * r * RIGHT).set_stroke(FAINT, 1.5),
        Line(1.3 * r * DOWN, 1.3 * r * UP).set_stroke(FAINT, 1.5),
        Circle(radius=r).set_stroke(MUTED, 2, opacity=0.55),
    ).move_to(centre)


def arrow_to_point(tip, centre=CENTRE, colour=CLOUD, width=5):
    """An arrow from `centre` to `tip`, drawn with a head.

    VISUAL_SYSTEM.md section 5: anything the narration calls an arrow is drawn
    with an arrowhead. As bare Lines, six evenly spaced arrows read as three
    diameters through the origin, which leaves "they cancel" with no visible
    referent -- the viewer cannot see six directions to cancel.
    """
    return Arrow(centre, tip, buff=0.0, stroke_width=width,
                 tip_length=0.24).set_color(colour)


def arrow_to(angle, r=RADIUS, centre=CENTRE, colour=CLOUD, width=5):
    """The unit arrow at `angle`."""
    tip = centre + r * np.array([np.cos(angle), np.sin(angle), 0.0])
    return arrow_to_point(tip, centre, colour, width)


class B02(ActScene):
    chain_link = "arrows"

    def construct(self):
        self.arrow_beat()
        self.unit_arrow_beat()
        self.components_beat()
        self.average_beat()

    # ------------------------------------------------------------------ 1
    def arrow_beat(self):
        """Answer B01's on-screen unknown, then make direction precise."""
        # Match B01's closing frame so the cut continues the same question.
        sample_track = NumberLine(
            x_range=(-3, 3, 0.5), length=9.4, include_numbers=False,
            include_tip=False,
        ).set_stroke(MUTED, 2).move_to([0.0, -0.9, 0.0])
        sample_dot = Dot(sample_track.n2p(1.45), radius=0.085).set_fill(TARGET, 1)
        sample_label = ty.maths(R"x_i", size=ty.EQ, color=TARGET)
        sample_label.next_to(sample_dot, DOWN, buff=0.13)
        unknown = ty.maths(R"x_i \longmapsto\ ?", size=ty.EQ_DISPLAY,
                           color=TARGET).move_to([0.0, 1.25, 0.0])
        answer = ty.maths(
            R"x_i \longmapsto \text{a direction}",
            size=ty.EQ_DISPLAY, color=TARGET,
        ).move_to(unknown)

        # B01 leaves this frame standing. Mount it immediately rather than
        # fading a duplicate in from black, then give the cut a short breath
        # before the answer arrives.
        self.add(sample_track, sample_dot, sample_label, unknown)
        self.settle_frame()
        self.wait(0.18)

        with self.voiceover(
            text="What we can do is let each sample represent a direction."
        ) as tracker:
            self.play(ReplacementTransform(unknown, answer),
                      run_time=0.75, rate_func=smooth)
            self.play(
                AnimationGroup(
                    Indicate(sample_dot, color=TARGET, scale_factor=1.08),
                    Indicate(answer, color=TARGET, scale_factor=1.025),
                    lag_ratio=0.25,
                ),
                run_time=0.75,
            )

        self.inspect(0.5)

        pan = plane()
        re_lab = ty.words("real", size=ty.TICK, color=MUTED)
        re_lab.next_to(pan, RIGHT, buff=0.12).shift(0.3 * DOWN)
        im_lab = ty.words("imaginary", size=ty.TICK, color=MUTED)
        im_lab.next_to(pan, UP, buff=0.12).shift(0.2 * RIGHT)
        labs = VGroup(re_lab, im_lab)

        # One complex number, with every dependent mark driven by one tracker.
        z = ValueTracker(0.0)
        path = [0.62 + 0.55j, -0.48 + 0.72j, 0.80 - 0.42j]

        def point_at(u):
            k = min(int(u), len(path) - 2)
            a, b = path[k], path[k + 1]
            # The original piecewise-linear path made an instantaneous turn at
            # its middle waypoint. Hermite interpolation keeps the waypoint
            # while matching the incoming and outgoing velocity there.
            s = u - k
            m_a = path[1] - path[0] if k == 0 else (path[2] - path[0]) / 2
            m_b = (path[2] - path[0]) / 2 if k == 0 else path[2] - path[1]
            w = ((2 * s**3 - 3 * s**2 + 1) * a
                 + (s**3 - 2 * s**2 + s) * m_a
                 + (-2 * s**3 + 3 * s**2) * b
                 + (s**3 - s**2) * m_b)
            return CENTRE + RADIUS * np.array([w.real, w.imag, 0.0])

        tip_of = lambda: point_at(z.get_value())
        vec = always_redraw(lambda: arrow_to_point(tip_of()))
        dot = always_redraw(lambda: Dot(
            tip_of(), radius=layout.ARROW_TIP_DOT_RADIUS)
                            .set_fill(CLOUD, 1))
        zlab = ty.maths("a + bi", size=ty.EQ, color=CLOUD)
        zlab.add_updater(lambda m: m.next_to(dot, UR, buff=0.15))

        # Dashed drop-lines: the whole scene depends on "sideways part" and
        # "upward part" being visible quantities rather than named ones.
        def drops():
            tip = tip_of()
            foot_x = np.array([tip[0], CENTRE[1], 0.0])
            foot_y = np.array([CENTRE[0], tip[1], 0.0])
            return VGroup(
                DashedLine(tip, foot_x, dash_length=0.07),
                DashedLine(tip, foot_y, dash_length=0.07),
            ).set_stroke(TARGET, 1.6, opacity=0.8)

        drop = always_redraw(drops)

        with self.voiceover(
            text="The natural home for those two answers is the "
                 "<bookmark mark='plane'/>complex plane. A "
                 "point here is written A, plus B I. A gives its horizontal "
                 "coordinate, and B gives its vertical coordinate."
        ) as tracker:
            self.wait_until_bookmark("plane")
            self.play(
                FadeOut(VGroup(sample_track, sample_dot, sample_label, answer)),
                Create(pan), FadeIn(labs, shift=0.12 * DOWN),
                run_time=0.62,
            )
            self.play(
                FadeIn(dot), Create(drop), Write(zlab),
                run_time=0.72, rate_func=smooth,
            )
            self.across(tracker, z.animate.set_value(0.45),
                        floor=0.8, rate_func=smooth)

        self.inspect(0.55, z.animate.set_value(0.35), rate_func=smooth)

        with self.voiceover(
            text="Now draw an arrow from the origin to that point. As the "
                 "point moves, the direction changes smoothly with it."
        ) as tracker:
            # Grow a throwaway copy, then hand over to the live one. GrowArrow
            # on an always_redraw mobject fights its own updater, and adding the
            # live arrow without removing the seed leaves two arrows on screen.
            seed = arrow_to_point(tip_of())
            self.play(GrowArrow(seed), run_time=0.75)
            self.remove(seed)
            self.add(vec)
            self.across(tracker, z.animate.set_value(2.0), floor=1.6,
                        rate_func=smooth)

        self.pan, self.labs = pan, labs
        self.freeze(vec, dot, drop, zlab)
        self.play(FadeOut(VGroup(dot, zlab, drop, vec)), run_time=0.6)
        self.remove(vec, dot, drop, zlab)

    # ------------------------------------------------------------------ 2
    def unit_arrow_beat(self):
        """e^{i theta}: the unit arrow at angle theta."""
        theta = ValueTracker(0.0)

        vec = always_redraw(lambda: arrow_to(theta.get_value()))
        tip_dot = always_redraw(lambda: Dot(
            CENTRE + RADIUS * np.array([np.cos(theta.get_value()),
                                        np.sin(theta.get_value()), 0.0]),
            radius=layout.ARROW_TIP_DOT_RADIUS).set_fill(CLOUD, 1))

        # Arc from the real axis round to the arrow, so theta is a thing you
        # watch open rather than a symbol.
        arc = always_redraw(lambda: Arc(
            start_angle=0.0, angle=max(theta.get_value(), 1e-4),
            radius=0.55, arc_center=CENTRE).set_stroke(TARGET, 3))
        arc_lab = always_redraw(lambda: ty.maths(R"\theta", size=ty.TICK,
                                                 color=TARGET)
                                .move_to(CENTRE + 0.85 * np.array(
                                    [np.cos(theta.get_value() / 2),
                                     np.sin(theta.get_value() / 2), 0.0])))

        rule = ty.maths(R"e^{i\theta}", size=ty.EQ_DISPLAY, color=TARGET)
        rule.move_to(np.array([3.1, 1.5, 0.0]))

        # Halved. This beat is prerequisite restoration -- concepts.yaml marks
        # complex numbers ASSUME -- and NARRATION_SPEC.md section 12 says an
        # assumed prerequisite is not re-taught. What was two blocks, a
        # two-line gloss card and a double revolution is now one block and one
        # revolution. The gloss card is gone outright: it restated "length one,
        # angle theta", which the sentence says and the picture shows.
        # No bookmark. The old wait_until_bookmark('name') held the frame with
        # the arrow parked at 0.9 rad until the voice reached the word; the name
        # arriving a beat early costs nothing, and the arrow never stops.
        with self.voiceover(
            text="Suppose only the direction matters. Then we can set the "
                 "arrow's length to one, so a single angle, theta, determines "
                 "it. We write this unit direction as e to the i theta."
        ) as tracker:
            self.add(vec, tip_dot, arc, arc_lab)
            self.across(
                tracker,
                theta.animate.set_value(2.4),
                Succession(Wait(0.8), Write(rule, run_time=1.0)),
                floor=2.8,
                rate_func=linear,
            )

        self.theta = theta
        self.rule = rule
        self.vec, self.tip_dot = vec, tip_dot
        self.arc, self.arc_lab = arc, arc_lab

    # ------------------------------------------------------------------ 3
    def components_beat(self):
        """cos and sin are the shadows, and they are what gets plotted later."""
        # The theta arc has to go before the shadows arrive. It is drawn from
        # the raw tracker value, so after a full turn it wraps past 2*pi and
        # renders as an almost-closed ring sitting on top of the components --
        # no error, just an unreadable frame.
        #
        # Updaters first: an always_redraw mobject rebuilds itself every frame,
        # which resets the opacity FadeOut is animating and leaves it visible.
        self.freeze(self.arc, self.arc_lab)
        self.play(FadeOut(self.arc), FadeOut(self.arc_lab), run_time=0.5)
        self.remove(self.arc, self.arc_lab)

        def shadows():
            a = self.theta.get_value()
            tip = CENTRE + RADIUS * np.array([np.cos(a), np.sin(a), 0.0])
            fx = np.array([tip[0], CENTRE[1], 0.0])
            fy = np.array([CENTRE[0], tip[1], 0.0])
            return VGroup(
                Line(CENTRE, fx).set_stroke(EMPIRICAL, 5),
                Line(CENTRE, fy).set_stroke(COLLAPSE, 5),
                DashedLine(tip, fx, dash_length=0.07).set_stroke(FAINT, 1.5),
                DashedLine(tip, fy, dash_length=0.07).set_stroke(FAINT, 1.5),
            )

        parts = always_redraw(shadows)

        eq = ty.maths(R"e^{i\theta} = \cos\theta + i\,\sin\theta",
                      size=ty.EQ_DISPLAY,
                      isolate=[R"\cos\theta", R"\sin\theta"])
        eq.set_color_by_tex(R"\cos\theta", EMPIRICAL)
        eq.set_color_by_tex(R"\sin\theta", COLLAPSE)
        eq.move_to(np.array([3.1, 0.1, 0.0]))
        layout.fit_in_frame(eq)

        # These two stay. They are not slogans restating the narration -- they
        # name which coloured segment is which, on the segments' own terms, and
        # RENDER_REVIEW_SPEC.md section 12 forbids colour alone carrying a
        # distinction.
        key = VGroup(
            ty.curve_label("how far right", EMPIRICAL),
            ty.curve_label("how far up", COLLAPSE),
        ).arrange(DOWN, buff=0.22)
        key.next_to(eq, DOWN, buff=0.55)

        # Row 6 -- "Every curve later in this chapter turns out to be one of
        # those two components" -- deleted. It promises later relevance instead
        # of saying anything now (NARRATION_SPEC.md section 1), and b05 makes
        # the same point where it is actually earned.
        # The bookmark wait here was four seconds of a stopped arrow with its
        # two shadows frozen under it -- the one frame in the beat where the
        # shadows changing IS the sentence. One forward sweep now drives the
        # entire beat; the old back-forward-back sequence made the arrow jerk
        # at every sentence boundary.
        seed_parts = shadows()
        with self.voiceover(
            text="The tip gives us two numbers: the cosine of theta "
                 "horizontally, and the sine of theta vertically. As theta "
                 "changes, both move smoothly."
        ) as tracker:
            self.play(
                GrowFromPoint(seed_parts[0], CENTRE),
                GrowFromPoint(seed_parts[1], CENTRE),
                FadeIn(VGroup(seed_parts[2], seed_parts[3])),
                run_time=0.8,
                rate_func=smooth,
            )
            self.remove(seed_parts, *seed_parts)
            self.add(parts)
            self.across(
                tracker,
                self.theta.animate.set_value(5.0),
                Succession(
                    Wait(0.12),
                    AnimationGroup(
                        Write(eq, run_time=0.42),
                        FadeIn(key, run_time=0.42),
                        lag_ratio=0.15,
                    ),
                    Wait(0.46),
                ),
                floor=2.8,
                rate_func=linear,
            )

        # Silence with the two shadows sliding under a moving arrow: the viewer
        # has just been given a correspondence to check, and checking it takes a
        # moment with nothing said over it.
        self.inspect(1.1, self.theta.animate.set_value(5.55),
                     rate_func=linear)

        self.freeze(parts, self.vec, self.tip_dot)
        self.play(FadeOut(VGroup(eq, key, parts, self.vec, self.tip_dot,
                                 self.rule)), run_time=0.7)
        self.remove(parts, self.vec, self.tip_dot)

    # ------------------------------------------------------------------ 4
    def average_beat(self):
        """Agreeing arrows add; spread arrows cancel. The whole video in one
        picture, before any characteristic function exists.

        One tracker drives the whole beat. The previous cut built this in three
        stages -- a static agreeing bundle, a 1.6 s Transform onto a static
        spread bundle, then a live sweep between the two -- and the two static
        stages measured ten and eleven seconds of unchanging frame on the rev-3
        master while the voice made a claim about arrows moving. The third stage
        already did the whole job dynamically, so the first two are now the same
        tracker at different values and nothing in the beat ever stops.

        `u` runs from coincident (0) through roughly-agreeing (0.10) to evenly
        spread (1). Both ends are exact rather than illustrative: identical
        angles average to length 1, and six equally spaced angles are the sixth
        roots of unity, which sum to exactly 0.
        """
        spread = np.linspace(0.0, TAU, 6, endpoint=False)
        coincident = np.full(len(spread), 0.55)
        AGREE = 0.10                      # |average| = 0.98 at this value

        u = ValueTracker(AGREE)

        def angles():
            return coincident + u.get_value() * (spread - coincident)

        def bundle():
            # Thin and half-lit, so the average drawn over them at full weight
            # is the thing the eye lands on. Six same-coloured arrows at equal
            # weight left the average indistinguishable at 480p.
            return VGroup(*(arrow_to(a, colour=CLOUD, width=3).set_stroke(
                opacity=0.45) for a in angles()))

        def mean_parts():
            z = np.mean(np.exp(1j * angles()))
            tip = CENTRE + RADIUS * np.array([z.real, z.imag, 0.0])
            dot = Dot(tip, radius=layout.ARROW_TIP_DOT_RADIUS)
            dot.set_fill(AVERAGE, 1)
            # Evenly spaced angles average to exactly zero, so the arrow can be
            # asked to run from a point to itself. Drawing an arrowhead on a
            # zero-length shaft is undefined; the dot alone is the honest
            # picture of an average that has vanished, and it is what the
            # sweep lands on at that end.
            if abs(z) < 0.02:
                return VGroup(dot), abs(z)
            return VGroup(arrow_to_point(tip, colour=AVERAGE, width=8),
                          dot), abs(z)

        live_arrows = always_redraw(bundle)
        live_mean = always_redraw(lambda: mean_parts()[0])

        # The measured length is the one channel saying something the picture
        # does not: 0.98 against 0.00 is the claim, in numbers, and the viewer
        # can check it against the arrow in front of them. A static word plus a
        # DecimalNumber, not a rebuilt ty.line -- Text goes through Pango on
        # every construction, and rebuilding one per frame at 60 fps is the kind
        # of thing that turns a 5 s beat into a slow render.
        len_label = ty.line("length", "$=$", size=ty.STATEMENT,
                            color=AVERAGE)
        len_label.move_to(np.array([3.1, 0.9, 0.0]))
        len_value = always_redraw(lambda: DecimalNumber(
            mean_parts()[1], num_decimal_places=2,
            font_size=ty.STATEMENT).set_color(AVERAGE)
            .next_to(len_label, RIGHT, buff=0.18).align_to(len_label, DOWN))
        layout.fit_in_frame(len_label)

        with self.voiceover(
            text="Suppose we take a few directions and average their endpoints. "
                 "<bookmark mark='avg'/>When they point roughly together, "
                 "their average stays long."
        ) as tracker:
            seeds = bundle()
            self.play(lagged_map(GrowArrow, seeds, lag_ratio=0.14),
                      run_time=1.4)
            # lagged_map animates the children directly, so remove both the
            # container and its individually registered arrows before the live
            # bundle takes ownership.
            self.remove(seeds, *seeds)
            self.add(live_arrows)
            self.wait_until_bookmark("avg")
            mean_seed = mean_parts()[0]
            self.play(GrowArrow(mean_seed[0]), FadeIn(mean_seed[1]),
                      run_time=1.0)
            self.remove(mean_seed, *mean_seed)
            self.add(live_mean, len_label, len_value)
            self.play(FadeIn(len_label), FadeIn(len_value), run_time=0.5)
            # Small live wobble around the agreeing state: the average visibly
            # answers to the arrows, which is the fact the next sentence leans
            # on, and it costs no runtime that was not already being waited out.
            self.across(tracker, u.animate.set_value(0.24), floor=0.8,
                        rate_func=there_and_back)

        with self.voiceover(
            text="Then, if we spread those arrows around the circle, their "
                 "components cancel against one another, pulling the average "
                 "inward. With equal spacing around the circle, the "
                 "cancellation is exact."
        ) as tracker:
            # The fanning-out IS the sentence, so it gets the whole sentence
            # rather than a fixed 1.6 s with the rest played over a still frame.
            # The readout counts 0.98 down to 0.00 as it happens, so the claim
            # and its evidence arrive together.
            self.across(tracker, u.animate.set_value(1.0), floor=2.6,
                        rate_func=smooth)

        self.inspect(1.2, u.animate.set_value(0.94), rate_func=there_and_back)

        angle_prompt = ty.maths(
            R"x_i \longmapsto \theta_i =\ ?",
            size=ty.EQ_DISPLAY, color=TARGET,
        ).move_to(np.array([3.1, 0.7, 0.0]))
        layout.fit_in_frame(angle_prompt)

        with self.voiceover(
            text="So the average gives us a smooth measure of how well the "
                 "directions line up. To connect this back to our samples, we "
                 "just need a rule for choosing each angle."
        ) as tracker:
            # Do not replay the full aligned-to-cancelled experiment. A small
            # partial return keeps the diagram alive while the conclusion
            # lands, then the mapping takes over as the new focal object.
            self.play(u.animate.set_value(0.78), run_time=1.15,
                      rate_func=smooth)
            self.freeze(len_value)
            self.play(
                FadeOut(VGroup(len_label, len_value)),
                Write(angle_prompt),
                run_time=0.85,
                rate_func=smooth,
            )
            self.across(tracker, u.animate.set_value(0.88),
                        floor=1.0, rate_func=there_and_back)

        self.inspect(0.45)

        self.freeze(live_arrows, live_mean, len_value)
        self.clear_beat(run_time=0.35)
