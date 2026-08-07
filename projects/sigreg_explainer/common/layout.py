"""Shared screen geometry (PLAN.md section 6).

The two-panel arrangement has to hold for minutes at a time across four
separately-rendered acts, so the positions live here and are never re-derived
inside a scene. The unit circle is ALWAYS left, the phi(t) plot ALWAYS right.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Axes, Circle, Line, Text, VGroup, config, DOWN, LEFT, RIGHT, UP,
)

from .palette import AXIS, GRID, INK, MUTED, TARGET

# --- two-panel geometry -----------------------------------------------------

CIRCLE_CENTRE = np.array([-3.75, -0.35, 0.0])
CIRCLE_RADIUS = 1.95

CF_CENTRE = np.array([3.05, -0.35, 0.0])
CF_WIDTH = 6.6
CF_HEIGHT = 3.9
CF_T_MAX = 5.0
CF_Y_RANGE = (-0.35, 1.1)

TITLE_Y = 3.25

# The frame edge nothing may cross. The `t` axis label in b02 clipped the right
# edge of the 480p master; fit_in_frame existed but was never applied to it.
SAFE_MARGIN = 0.45


def complex_panel() -> VGroup:
    """Unit circle plus real/imaginary axes, in the left panel."""
    r = CIRCLE_RADIUS
    circle = Circle(radius=r).set_stroke(AXIS, 2, opacity=0.75)
    re_axis = Line(r * 1.35 * LEFT, r * 1.35 * RIGHT).set_stroke(GRID, 1.5)
    im_axis = Line(r * 1.25 * DOWN, r * 1.25 * UP).set_stroke(GRID, 1.5)
    panel = VGroup(re_axis, im_axis, circle)
    panel.move_to(CIRCLE_CENTRE)
    return panel


def cf_axes() -> Axes:
    """Axes for the phi(t) plot, in the right panel."""
    axes = Axes(
        x_range=(0, CF_T_MAX, 1),
        y_range=(CF_Y_RANGE[0], CF_Y_RANGE[1], 0.5),
        x_length=CF_WIDTH,
        y_length=CF_HEIGHT,
        tips=False,
        axis_config={"include_tip": False, "stroke_width": 2},
    )
    axes.move_to(CF_CENTRE)
    return axes


def cf_target_curve(axes: Axes):
    """The Gaussian fingerprint e^{-t^2/2} drawn on the phi(t) axes."""
    curve = axes.plot(lambda t: np.exp(-t * t / 2), x_range=(0, CF_T_MAX))
    curve.set_stroke(TARGET, 3)
    return curve


# --- furniture --------------------------------------------------------------

def act_title(text: str) -> Text:
    from . import type as ty

    title = ty.statement(text)
    title.move_to(np.array([0.0, TITLE_Y, 0.0]))
    return fit_in_frame(title)


# chain_bar() is deleted, not shrunk.
#
# It was a seven-item dependency strip pinned above every scene at font_size 16
# -- 15 px at 1080p, below the 22 floor -- and then set_width-shrunk below even
# that. Permanently on screen, unreadable, and carrying nothing the scene
# needed: RENDER_REVIEW_SPEC.md section 7.3 (a persistent panel whose role has
# finished) and section 8.2 (an element whose main job is making the screen look
# full) at once. Scenes that referenced it via ActScene.chain_link now ignore it.


# --- the three-panel rig (PLAN.md section 2) --------------------------------
# numbers on a line  <->  arrows on the circle  <->  phi(t) vs t
# All three update together from one `t`. This is the central visual of the
# whole video, so its geometry is fixed once here and never re-derived.

# Both outer panels used to overhang the safe margin, which is why the phi(t)
# curve ran to the frame edge and the `t` axis label read as clipped in every
# rig scene. config.frame_width is 14.222, so the usable half-width is 7.111 - 0.45 =
# 6.661; the old geometry put the number line at -6.80 and the phi(t) axes at
# +6.85. Both now sit inside it, with the asymmetry (0.72 left gap vs 0.57
# right) spent on the phi(t) panel, which carries a curve rather than a rule.
#
#   line    -6.60 .. -2.70      circle  -2.03 .. 2.03      phi(t)  2.60 .. 6.60
RIG_Y = -0.35
RIG_LINE_CENTRE = np.array([-4.65, RIG_Y, 0.0])
RIG_LINE_WIDTH = 3.9
RIG_CIRCLE_CENTRE = np.array([0.0, RIG_Y, 0.0])
RIG_CIRCLE_RADIUS = 1.5
RIG_CF_CENTRE = np.array([4.60, RIG_Y, 0.0])
RIG_CF_WIDTH = 4.0
RIG_CF_HEIGHT = 3.0
RIG_TITLE_Y = 2.1


def rig_circle() -> VGroup:
    r = RIG_CIRCLE_RADIUS
    grp = VGroup(
        Line(1.35 * r * LEFT, 1.35 * r * RIGHT).set_stroke(GRID, 1.4),
        Line(1.25 * r * DOWN, 1.25 * r * UP).set_stroke(GRID, 1.4),
        Circle(radius=r).set_stroke(AXIS, 2, opacity=0.8),
    )
    grp.move_to(RIG_CIRCLE_CENTRE)
    return grp


def rig_cf_axes(t_max: float = 6.5, y_range=(-1.15, 1.15)) -> Axes:
    axes = Axes(
        x_range=(0, t_max, 1),
        y_range=(y_range[0], y_range[1], 0.5),
        x_length=RIG_CF_WIDTH,
        y_length=RIG_CF_HEIGHT,
        tips=False,
        axis_config={"include_tip": False, "stroke_width": 2, "color": AXIS},
    )
    axes.move_to(RIG_CF_CENTRE)
    return axes


def rig_titles(*labels: str) -> VGroup:
    """One caption per panel, pinned above each.

    Captions are furniture: MUTED, and at CAPTION size rather than the old 22,
    which was on the floor and read as an afterthought at 480p.
    """
    from . import type as ty

    centres = [RIG_LINE_CENTRE, RIG_CIRCLE_CENTRE, RIG_CF_CENTRE]
    out = VGroup()
    for text, c in zip(labels, centres):
        t = ty.caption(text)
        t.move_to(np.array([c[0], RIG_TITLE_Y, 0.0]))
        out.add(fit_in_frame(t))
    return out


def fit_in_frame(mob, margin: float = SAFE_MARGIN):
    """Shrink and nudge a mobject until it lies inside the frame horizontally.

    Safety net for annotations: `next_to(eq, RIGHT)` on a wide equation silently
    pushes text off the edge, which renders as a sentence running off screen
    rather than as an error. Call this on anything positioned relative to
    something whose width you do not control.
    """
    half = config.frame_width / 2 - margin
    if mob.width > 2 * half:
        mob.scale_to_fit_width(2 * half)
    right, left = mob.get_right()[0], mob.get_left()[0]
    if right > half:
        mob.shift(LEFT * (right - half))
    elif left < -half:
        mob.shift(RIGHT * (-half - left))
    return mob


def stack_levels(values, min_dx: float) -> list:
    """Vertical level for each value, so overlapping samples stack instead of hiding.

    A one-dimensional batch drawn as dots directly on the axis is unreadable
    wherever it is dense: forty samples from a bell curve pile into an
    indistinguishable bar, and the frame stops carrying the very thing the scene
    is claiming -- that the shapes differ. Stacking is what makes a hump look
    like a hump and two clumps look like two clumps.

    Greedy first-fit, the standard dot-plot rule: a sample sits at the lowest
    level where nothing within `min_dx` is already sitting.

    `min_dx` is in the same units as `values`; pass the dot diameter converted
    into data units, not screen units.

    Returns one integer level per value, in the caller's original order.
    """
    order = sorted(range(len(values)), key=lambda i: values[i])
    levels = [0] * len(values)
    occupied: list[list[float]] = []  # occupied[level] = xs already placed there
    for i in order:
        x = values[i]
        for lvl, xs in enumerate(occupied):
            if not xs or x - xs[-1] >= min_dx:
                xs.append(x)
                levels[i] = lvl
                break
        else:
            occupied.append([x])
            levels[i] = len(occupied) - 1
    return levels


def widest_gap(values) -> tuple:
    """The largest empty interval strictly inside a batch, as (lo, hi).

    Used to point at the space between two clumps. Deriving it from the data
    beats hard-coding a rectangle: the annotation cannot drift away from the
    thing it is annotating when the seed or the batch changes.
    """
    xs = sorted(values)
    lo, hi, best = xs[0], xs[0], 0.0
    for a, b in zip(xs, xs[1:]):
        if b - a > best:
            best, lo, hi = b - a, a, b
    return lo, hi


def freq_readout(value_tracker, label: str = "t") -> VGroup:
    """Live 't = 1.23' readout. Caller wraps this in always_redraw.

    INK rather than TARGET: the readout is orientation, not the Gaussian
    reference, and it was previously the brightest thing in frame while the
    curve it described was drawn in the same colour. One meaning per colour.
    """
    from . import type as ty

    group = ty.readout(label, value_tracker, places=2, color=INK)
    group.to_corner(np.array([1.0, 1.0, 0.0]), buff=SAFE_MARGIN)
    return group


# --- geometry guard ---------------------------------------------------------
# Panel positions are three numbers that have to stay inside a fourth. Nothing
# raises when they drift out: the render simply puts a curve on the frame edge,
# and it is only caught by looking at a frame. Assert at import instead.
def _assert_panels_inside_frame():
    half = config.frame_width / 2 - SAFE_MARGIN
    panels = {
        "number line": (RIG_LINE_CENTRE[0], RIG_LINE_WIDTH),
        "unit circle": (RIG_CIRCLE_CENTRE[0], 2 * 1.35 * RIG_CIRCLE_RADIUS),
        "phi(t) axes": (RIG_CF_CENTRE[0], RIG_CF_WIDTH),
        "complex panel": (CIRCLE_CENTRE[0], 2 * 1.35 * CIRCLE_RADIUS),
        "cf panel": (CF_CENTRE[0], CF_WIDTH),
    }
    for name, (centre, width) in panels.items():
        left, right = centre - width / 2, centre + width / 2
        if left < -half or right > half:
            raise AssertionError(
                f"{name} spans {left:.2f}..{right:.2f}, outside the safe "
                f"half-width {half:.2f}. See VISUAL_SYSTEM.md section 5.")


_assert_panels_inside_frame()
