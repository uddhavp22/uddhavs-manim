"""Type-scale smoke test. Not a chapter scene -- the leading underscore keeps it
out of build.sh's [abc][0-9][0-9]*_*.py glob.

Renders one frame carrying every tier in common/type.py so the scale can be
judged at delivery size before seven scenes are written against it. Latin Modern
has a smaller x-height and lighter strokes than the Helvetica it replaces, so
the tiers do not carry over unchanged.

    ./render.sh projects/sigreg_explainer/_fonttest.py FontTest -s -ql
    ./render.sh projects/sigreg_explainer/_fonttest.py FontTest -s -qh
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, Scene, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import type as ty
from common.palette import CLOUD, MUTED, TARGET


class FontTest(Scene):
    def construct(self):
        rows = VGroup(
            ty.title(f"Scene title card, TITLE {ty.TITLE}"),
            ty.statement(f"The one sentence a beat is about, STATEMENT {ty.STATEMENT}"),
            ty.words(f"A full annotation sentence on screen, BODY {ty.BODY}", size=ty.BODY),
            ty.caption(f"pinned above a panel, CAPTION {ty.CAPTION}"),
            ty.label(f"legend or curve label, LABEL {ty.LABEL}"),
            ty.words(f"axis tick label, TICK {ty.TICK}, the floor", size=ty.TICK),
            ty.maths(R"\varphi(t) = \mathbb{E}[e^{itX}]", size=ty.EQ),
            ty.maths(R"\varphi(t) = e^{-t^2/2}", size=ty.EQ_DISPLAY),
            ty.line("mean ", "$= +0.00$", "   variance ", "$= 1.00$", size=ty.BODY),
            ty.line("X", "symmetric about", "$0$", R"$\Longrightarrow$", size=ty.BODY),
            ty.label("coloured label on the data", color=CLOUD),
            ty.label("coloured label on the target", color=TARGET),
            ty.words("2   4   6      t = 1.35", size=ty.TICK, color=MUTED),
        )
        # Print the boxes as well as drawing them. A corrupt glyph shows up here
        # as an outlier row long before it is obvious in the frame -- and it was
        # this readout, not the picture, that located the bad '2'.
        for i, r in enumerate(rows):
            print(f"  row {i:2d} {type(r).__name__:10s} "
                  f"w={r.width:7.3f} h={r.height:7.3f}")

        rows.arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        print(f"  GROUP w={rows.width:.3f} h={rows.height:.3f}")
        rows.center()
        self.add(rows)
