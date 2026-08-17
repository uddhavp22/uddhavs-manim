"""The three-panel rig, shared by every Chapter B scene.

    numbers on a line  <->  arrows on the circle  <->  phi(t) vs t

PLAN.md section 2 calls this the persistent visual language, which only works if
it is literally the same object every time. Duplicating the construction per
scene is how the panels quietly drift apart, so it lives here once.

The link that makes it one mechanism rather than three charts: the horizontal
position of the average arrow IS the height of the curve. `link()` draws that.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow, DashedLine, Dot, Line, NumberLine, ValueTracker,
    VGroup, VMobject, Transform, always_redraw, DOWN, LEFT, RIGHT, UR,
)

from . import layout
from .palette import AVERAGE, AXIS, CLOUD, COLLAPSE, EMPIRICAL, MUTED, TARGET
from .wrap import ecf, wrapped

# What the three panels are called, everywhere. A scene that renames a panel
# renames it for that scene only, which is how "the same rig throughout" stops
# being true without anything failing.
DEFAULT_TITLES = ("the numbers", "wrapped onto the circle",
                  "the average, against t")


class ThreePanelRig:
    """Holds the trackers and panel geometry; hands back mobject factories.

    Every factory is meant to be wrapped in `always_redraw`, so a scene can swap
    the batch mid-scene (see `set_batch`) and the existing mobjects follow --
    rather than a second set being added on top of the first, which renders as
    two overlapping curves.
    """

    def __init__(self, samples, t_max: float = 6.5, grid_n: int = 700,
                 wrapped_already: bool = True, line_range=(-2, 2, 1)):
        self.h = np.asarray(samples, dtype=float)
        self.t_max = t_max
        self.grid = np.linspace(0, t_max, grid_n)
        self.colour = EMPIRICAL
        # Which quantity panel 3 plots. Re phi is the default because it is
        # literally "how far right the arrows point", which the viewer can
        # watch in panel 2. Switch to abs for the constant case, where the
        # claim being made is about magnitude and Re phi merely oscillates.
        self.show_abs = False

        self.t = ValueTracker(0.0)
        # kappa 0 -> straight line, 1 -> wrapped; rigid 0 -> 1 rotates the
        # finished circle into standard complex-plane orientation.
        self.kappa = ValueTracker(1.0 if wrapped_already else 0.0)
        self.rigid = ValueTracker(1.0 if wrapped_already else 0.0)

        # x_range must land ticks on integers: (-2.5, 2.5, 1) puts them on
        # half-integers and the integer-rounded labels read "-2 -2 0 0 2 2".
        self.line = NumberLine(x_range=line_range, length=layout.RIG_LINE_WIDTH,
                               include_numbers=True, include_tip=False)
        self.line.set_stroke(MUTED, 2)

        # NumberLine's negative DecimalNumber labels are positioned by the
        # numeral while the minus sign extends left, leaving their actual
        # bounding-box centres about 0.11 units left of the ticks. Re-centre
        # every generated label from its measured bounds; positives already
        # land exactly and therefore do not move.
        for label in self.line.numbers:
            value = label.get_value()
            tick_x = self.line.number_to_point(value)[0]
            label.shift((tick_x - label.get_center()[0]) * RIGHT)

        self.line.move_to(layout.RIG_LINE_CENTRE)

        self.circle = layout.rig_circle()
        self.axes = layout.rig_cf_axes(t_max)

        # Set by mount(); named here so swap() before mount() fails loudly
        # rather than silently adding a second set of dots.
        self.mounted_dots = None
        self.titles = None
        self._dot_colour = CLOUD
        self._dot_radius = 0.075
        self._dot_stack = False

        self._refresh()

    # -- state ---------------------------------------------------------
    def _refresh(self):
        cf = ecf(self.h, self.grid)
        self.table = cf.real
        self.table_imag = cf.imag
        self.table_abs = np.abs(cf)

    def set_batch(self, samples, colour=None):
        self.h = np.asarray(samples, dtype=float)
        if colour is not None:
            self.colour = colour
        self._refresh()

    # -- mounting ------------------------------------------------------
    #
    # b05, b06 and b07 each grew their own setup_panels()/_swap() pair from the
    # same original, and the three then drifted: different dot radii, different
    # swap signatures, different sets of live mobjects. That is exactly the
    # drift this module's docstring warns about, so the mounting now lives here
    # beside the geometry it mounts.

    def mount(self, scene, *, titles=DEFAULT_TITLES, dots=None,
              dot_colour=CLOUD,
              dot_radius: float = 0.075, stack_dots: bool = False,
              arrows: bool = True, centroid: bool = True, trace: bool = True,
              rider: bool = True, readout: bool = True,
              link: bool = False, trace_imag: bool = False,
              rider_imag: bool = False) -> None:
        """Add the panels and every live mobject to `scene`.

        Each flag names a mobject some scene deliberately does without. b05
        passes `trace=False, rider=False` because its subject IS the two
        components, and it adds both curves itself a beat later -- mounting the
        default single trace first would leave a third curve on the axes.

        If `dots` is supplied, it is adopted as panel 1's batch without being
        copied or restyled. This preserves cloud-to-shadow object identity.
        """
        self._dot_colour = dot_colour
        self._dot_radius = dot_radius
        self._dot_stack = stack_dots
        self.titles = layout.rig_titles(*titles)
        # A projected batch may already own the exact dots that should enter
        # panel 1. Adopt those instances so mounting the rig cannot create a
        # second, visually identical batch on top of them.
        self.mounted_dots = (
            self.line_dots(radius=dot_radius, colour=dot_colour)
            if dots is None else dots
        )

        scene.add(self.line, self.circle, self.axes, self.axis_labels(),
                  self.titles, self.mounted_dots)
        # Added in drawing order: arrows behind their average, curve furniture
        # last, so nothing the viewer is asked to follow ends up underneath.
        for wanted, factory in ((arrows, self.arrows),
                                (centroid, self.centroid),
                                (trace, self.trace),
                                (trace_imag, self.trace_imag),
                                (rider, self.rider),
                                (rider_imag, self.rider_imag),
                                (link, self.link),
                                (readout, self.readout)):
            if wanted:
                scene.add(always_redraw(factory))

    def swap(self, scene, samples, colour=None, dot_colour=None) -> None:
        """Change the batch without drawing a second copy of everything.

        Everything `mount()` added is an `always_redraw` over `self.h`, so it
        follows a `set_batch()` by itself. The dots on the number line are the
        one exception, and deliberately so: they are a static group which is
        transformed into its new positions rather than rebuilt in a hard cut.

        The rig returns to its shared anchor at `t = 0` while the dots move.
        Only then does the backing batch change. At the anchor every batch has
        the same wrapped arrows and curve value, so the live panels cannot snap
        while the number-line dots are still in transit.
        """
        samples = np.asarray(samples, dtype=float)
        if dot_colour is not None:
            self._dot_colour = dot_colour
        target_dots = self.line_dots(radius=self._dot_radius,
                                     colour=self._dot_colour,
                                     samples=samples)
        anims = [Transform(self.mounted_dots, target_dots)]
        if abs(self.t.get_value()) > 1e-6:
            anims.insert(0, self.t.animate.set_value(0.0))
        scene.play(*anims, run_time=1.0)
        self.set_batch(samples, colour)

    # -- geometry ------------------------------------------------------
    def tips(self):
        return wrapped(self.h * max(self.t.get_value(), 1e-9),
                       self.kappa.get_value(), self.rigid.get_value(),
                       layout.RIG_CIRCLE_RADIUS, layout.RIG_CIRCLE_CENTRE)

    def centroid_point(self):
        z = ecf(self.h, [self.t.get_value()])[0]
        return (layout.RIG_CIRCLE_CENTRE
                + layout.RIG_CIRCLE_RADIUS * np.array([z.real, z.imag, 0.0]))

    # -- panel 1 -------------------------------------------------------
    # Stacking bin, in data units. Wide enough that a run of nearby samples
    # climbs as a column rather than a diagonal streak; see layout.stack_levels.
    STACK_BIN = 0.25

    def line_dots(self, radius: float = 0.075, colour=CLOUD,
                  stack: bool | None = None, samples=None) -> VGroup:
        """Panel 1's samples. `stack` draws them as a dot histogram.

        Flat on the axis is right for the handful-of-values scenes, where each
        dot is meant to be tracked individually. It is wrong for a real batch:
        forty samples over six units on a 3.9-unit-wide line merge into a bar,
        and a scene claiming that two batches have different SHAPES then has no
        evidence for it in panel 1. b00 hit this first and solved it there; the
        solution belongs here, next to the geometry, rather than in a second
        copy (which is finding F15's failure mode exactly).
        """
        values = self.h if samples is None else np.asarray(samples, dtype=float)
        if stack is None:
            stack = self._dot_stack
        if not stack:
            return VGroup(*(
                Dot(self.line.number_to_point(v),
                    radius=radius).set_fill(colour, 1)
                for v in values))

        # Quantise once and use the same snapped values for both jobs, so a
        # column packs from the axis outward instead of floating clear of it.
        snapped = [round(float(v) / self.STACK_BIN) * self.STACK_BIN
                   for v in values]
        levels = layout.stack_levels(snapped, self.STACK_BIN)
        step = 2 * radius + 0.018
        return VGroup(*(
            Dot(self.line.number_to_point(s)
                + np.array([0.0, (lvl + 0.9) * step, 0.0]),
                radius=radius).set_fill(colour, 1)
            for s, lvl in zip(snapped, levels)))

    # -- panel 2 -------------------------------------------------------
    def roll_curve(self, colour=MUTED, width: float = 2.0) -> VMobject:
        """The line the samples are sitting on, rolled by the same kappa.

        Without it the wrap is a set of loose dots that drift into a circle:
        rev-3 finding R5, where for the first nine seconds the unrolled samples
        ran well past the circle panel with nothing underneath them, so the one
        thing the beat claims -- that this is a LINE being wrapped -- was the
        thing the frame did not show. Drawn from the same `wrapped()` call as
        the dots, so it cannot disagree with where they land.
        """
        t = max(self.t.get_value(), 1e-9)
        lo, hi = float(self.h.min()), float(self.h.max())
        pad = 0.12 * max(hi - lo, 1e-3)
        a = np.linspace((lo - pad) * t, (hi + pad) * t, 240)
        pts = wrapped(a, self.kappa.get_value(), self.rigid.get_value(),
                      layout.RIG_CIRCLE_RADIUS, layout.RIG_CIRCLE_CENTRE)
        curve = VMobject().set_stroke(colour, width, opacity=0.55)
        curve.set_points_as_corners(list(pts))
        return curve

    def dots(self) -> VGroup:
        return VGroup(*(Dot(p, radius=layout.ARROW_TIP_DOT_RADIUS)
                        .set_fill(CLOUD, 1)
                        for p in self.tips()))

    def arrows(self, width: float = 2.0, opacity: float = 0.55) -> VGroup:
        c = layout.RIG_CIRCLE_CENTRE
        return VGroup(*(
            Arrow(c, p, buff=0.0, stroke_width=width, tip_length=0.14)
            .set_color(self.colour).set_opacity(opacity)
            for p in self.tips()
        ))

    def centroid(self) -> VGroup:
        p = self.centroid_point()
        return VGroup(
            Arrow(
                layout.RIG_CIRCLE_CENTRE, p,
                buff=0.0,
                stroke_width=6,
                tip_length=layout.AVERAGE_ARROW_TIP_LENGTH,
            ).set_color(AVERAGE),
            Dot(p, radius=layout.ARROW_TIP_DOT_RADIUS)
            .set_fill(AVERAGE, 1),
        )

    # -- panel 3 -------------------------------------------------------
    def axis_labels(self, xs=(2, 4, 6)) -> VGroup:
        from . import type as ty

        out = VGroup()
        for v in xs:
            lab = ty.maths(str(v), size=ty.TICK, color=AXIS)
            lab.next_to(self.axes.c2p(v, 0), DOWN, buff=0.15)
            out.add(lab)
        one = ty.maths("1", size=ty.TICK, color=AXIS)
        one.next_to(self.axes.c2p(0, 1), LEFT, buff=0.15)

        # The t label sat DR of the last tick, which put it 0.1 units from the
        # frame edge -- inside the frame, but well inside the 0.45 safe margin,
        # and it read as clipped at 480p. Above the axis end instead, then
        # fit_in_frame as a backstop, since t_max is a caller argument and this
        # geometry must hold for any value of it.
        t_lab = ty.maths("t", size=ty.TICK, color=AXIS)
        t_lab.next_to(self.axes.c2p(self.t_max, 0), UR, buff=0.12)
        layout.fit_in_frame(t_lab)
        return VGroup(out, one, t_lab)

    def _curve(self, table, colour, width=4):
        t = self.t.get_value()
        c = VMobject().set_stroke(colour, width).set_fill(opacity=0.0)
        m = self.grid <= max(t, 1e-4)
        pts = [self.axes.c2p(a, b) for a, b in zip(self.grid[m], table[m])]
        if len(pts) < 2:
            pts = [self.axes.c2p(0, 1)] * 2
        # as_corners, not smoothly: spline smoothing overshoots at the moving
        # endpoint and throws the curve outside the axes.
        c.set_points_as_corners(pts)
        return c

    def trace(self):
        table = self.table_abs if self.show_abs else self.table
        return self._curve(table, self.colour)

    def trace_abs(self, colour=TARGET):
        """|phi(t)| rather than Re phi(t) -- for the shift example, where the
        magnitude is unchanged and only the phase moves."""
        return self._curve(self.table_abs, colour, width=3)

    def trace_imag(self, colour=COLLAPSE, width=3):
        """Im phi(t): how far UP the arrows point on average. Drawn alongside
        the real part in B03, where the two components are the subject."""
        return self._curve(self.table_imag, colour, width)

    def rider_imag(self, colour=COLLAPSE) -> Dot:
        t = self.t.get_value()
        v = float(np.interp(t, self.grid, self.table_imag))
        return Dot(self.axes.c2p(t, v), radius=0.07).set_fill(colour, 1)

    def centroid_components(self, re_colour=EMPIRICAL, im_colour=COLLAPSE):
        """The average arrow split into its sideways and upward parts, drawn in
        the circle panel. This is the picture that makes Re phi and Im phi mean
        something before either is plotted."""
        c = layout.RIG_CIRCLE_CENTRE
        p = self.centroid_point()
        foot = np.array([p[0], c[1], 0.0])
        return VGroup(
            Line(c, foot).set_stroke(re_colour, 5),
            Line(foot, p).set_stroke(im_colour, 5),
        )

    def rider(self) -> Dot:
        t = self.t.get_value()
        table = self.table_abs if self.show_abs else self.table
        v = float(np.interp(t, self.grid, table))
        return Dot(self.axes.c2p(t, v), radius=0.08).set_fill(self.colour, 1)

    def link(self) -> DashedLine:
        """The centroid's horizontal position IS the curve's height."""
        t = self.t.get_value()
        table = self.table_abs if self.show_abs else self.table
        v = float(np.interp(t, self.grid, table))
        a = self.centroid_point()
        b = self.axes.c2p(t, v)
        return DashedLine(np.array([a[0], b[1], 0.0]), b,
                          dash_length=0.06).set_stroke(TARGET, 1.6, opacity=0.75)

    def readout(self) -> VGroup:
        """Live "t = 1.35", pinned above the panels.

        Through type.py, not a literal font_size: this was the last place in
        the rig setting type by hand, which meant it sat below the size floor
        and did not move when the scale was re-anchored for Latin Modern.
        """
        from . import type as ty

        group = ty.readout("t", self.t, places=2, color=TARGET)
        return group.move_to(np.array([0.0, 3.35, 0.0]))
