"""Geometry of the wheel of shadows, shared by C06, C07 and C09.

C06 builds the wheel; C07 opens on its last frame and C09 restores C07's.
Nothing type-checks that the three scenes agree on a radius, so every number
that decides where a wheel object sits lives here and nowhere else.
"""

import numpy as np

SCALE = 0.78                 # world units per standard deviation of the cloud
DOT_RADIUS = 0.033
COLLAPSED_DIRECTION = 3 * np.pi / 4

WHEEL_RADIUS = 2.86
SPOKE_RADIUS = 2.58
ACTIVE_ARROW_LENGTH = 1.55
ACTIVE_LINE_HALF_LENGTH = 2.56
N_SPOKES = 16
N_SHADOWS = 8

# One rim plot: a baseline tangent to the wheel, dots stacked outward.
MINI_HALF_WIDTH = 0.72
MINI_X_SCALE = 0.18
MINI_STACK_STEP = 0.035
MINI_STACK_MAX = 7
MINI_DOT_RADIUS = 0.018
MINI_SAMPLE_COUNT = 36


def rim_plot(sample_2d, radial, centre_of_wheel, scale: float = 1.0,
             plot_scale: float | None = None):
    """C06's rim plot for a unit direction: baseline tangent to the wheel, the
    sample's shadow stacked outward, the target bell. `scale` shrinks the
    wheel the plot sits on; `plot_scale` (default `scale`) sizes the plot
    itself, so a compact wheel can still carry a legible shadow (C09).

    C06 and C07 still carry their own copies of this inside `construct`;
    they were rendered before it was lifted here and are left untouched.
    """
    import numpy as np
    from manim import Dot, Line, VGroup, VMobject

    from . import layout
    from .palette import AXIS, DIRECTION, TARGET

    radial = np.asarray(radial, dtype=float)
    tangent = np.array([-radial[1], radial[0], 0.0])
    centre = np.asarray(centre_of_wheel, dtype=float) + scale * WHEEL_RADIUS * radial
    scale = plot_scale if plot_scale is not None else scale
    baseline = Line(
        centre - scale * MINI_HALF_WIDTH * tangent,
        centre + scale * MINI_HALF_WIDTH * tangent,
    ).set_stroke(AXIS, 1.1, opacity=0.60)
    positions = (np.asarray(sample_2d) @ radial[:2]) * MINI_X_SCALE
    levels = np.minimum(
        np.asarray(layout.stack_levels(positions, 0.046), dtype=float),
        MINI_STACK_MAX,
    )
    dots = VGroup(*(
        Dot(radius=scale * MINI_DOT_RADIUS).set_fill(DIRECTION, 0.90)
        .set_stroke(width=0)
        .move_to(
            centre
            + scale * float(position) * tangent
            + scale * (level + 0.75) * MINI_STACK_STEP * radial
        )
        for position, level in zip(positions, levels)
    ))
    bell = VMobject().set_stroke(TARGET, 2.0, opacity=0.85)
    bell.set_fill(opacity=0.0)
    xs = np.linspace(-3.2, 3.2, 121)
    edge = np.exp(-0.5 * 3.2 ** 2)
    bell.set_points_smoothly([
        centre
        + scale * x * MINI_X_SCALE * tangent
        + scale * 0.33 * (np.exp(-0.5 * x * x) - edge) / (1.0 - edge) * radial
        for x in xs
    ])
    return VGroup(baseline, dots, bell)
