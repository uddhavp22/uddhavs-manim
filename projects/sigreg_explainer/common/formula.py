"""The SIGReg line, verbatim from SOURCE_MAP.md section 8.

C09 assembles it and C10 keeps it parked at the top of the frame, so both
scenes build it here: one string, two callers, and the seam between them is
enforced by shared code rather than by two copies agreeing (VISUAL_SYSTEM.md
section 7). Parts are isolated at construction so a scene can reveal them one
at a time without ever re-laying the group out.

    [0] SIGReg(Z)=   [1] 1/M   [2] sum_{m=1}^{M}
    [3] T(           [4] u^{(m)T} Z          [5] ; lambda )
"""

from __future__ import annotations

import numpy as np
from manim import MathTex

from . import layout
from .palette import AVERAGE, DIRECTION, INK

NAME, ONE_OVER_M, SUM, SCORE_OPEN, ARGUMENT, SCORE_CLOSE = range(6)

# Where C09 leaves the line and C10 finds it.
PARK = np.array([0.0, 3.05, 0.0])
PARK_SIZE = 34
LINE_SIZE = 48


def sigreg_formula(font_size: int = LINE_SIZE) -> MathTex:
    tex = MathTex(
        R"\text{SIGReg}(Z)=",
        R"\frac{1}{M}",
        R"\sum_{m=1}^{M}",
        R"\mathcal T\big(",
        R"u^{(m)\top} Z",
        R"\,;\lambda\big)",
        font_size=font_size,
    ).set_color(INK)
    tex[ONE_OVER_M].set_color(AVERAGE)
    tex[SUM].set_color(AVERAGE)
    tex[ARGUMENT].set_color(DIRECTION)
    return tex


def parked_sigreg_formula() -> MathTex:
    tex = sigreg_formula(PARK_SIZE).move_to(PARK)
    layout.fit_in_frame(tex)
    return tex
