"""Glyph-integrity check for the project's typefaces.

Run this whenever the typeface changes. It exists because a broken glyph is a
*silent* failure in this pipeline, and the failure is not cosmetic:

    manimpango returned the digit '2' in Latin Modern Roman Demi with a path
    about four times its correct bounding box. Nothing raised. The frame
    rendered with a stray diagonal stroke across it, and -- worse -- the
    inflated bounding box propagated through VGroup.arrange() and set_height(),
    which crushed every other row in the frame to a tenth of its intended size.

That is two failure modes from one bad glyph, neither of which produces a
traceback, and neither of which any other gate in this repo can see. preflight
checks names, facts.py checks numbers, narration_audit checks language. Nothing
checked whether the letters draw.

Method: build one Text per character per face and compare its bounding box
against the median for that face. A glyph carrying a spurious control point is
an extreme outlier -- the real ones sat at 4-6x while everything else was
within a factor of two.

    ./render.sh tools/font_check.py FontCheck -s -ql

Exits by printing; read the output. CLEAN on every face in use is the pass
condition.
"""

from __future__ import annotations

import string

import numpy as np
from manim import Scene, Text

# The character set the scenes actually contain, not a full Unicode sweep.
CHARS = string.ascii_letters + string.digits + " .,;:=+-()[]{}'\"/?!%"

# Faces to check. Keep the rejected ones listed: the point of this file is to
# record *why* they are rejected, so nobody re-adopts one from its name alone.
FACES = [
    ("Latin Modern Roman", "in use"),
    ("Latin Modern Roman Demi", "REJECTED: '2' corrupt"),
    ("Helvetica Neue", "previous face, kept as a control"),
]

OUTLIER_FACTOR = 3.0


class FontCheck(Scene):
    def construct(self):
        for face, note in FACES:
            boxes = {}
            for ch in CHARS:
                m = Text(ch, font=face, font_size=48)
                boxes[ch] = (m.width, m.height)

            med_w = float(np.median([w for w, _ in boxes.values()]))
            med_h = float(np.median([h for _, h in boxes.values()]))

            bad = [
                (ch, w, h)
                for ch, (w, h) in boxes.items()
                if w > OUTLIER_FACTOR * med_w or h > OUTLIER_FACTOR * med_h
            ]

            status = "CLEAN" if not bad else f"{len(bad)} CORRUPT"
            print(f"\n--- {face}  [{note}]")
            print(f"    {status}   median w={med_w:.3f} h={med_h:.3f}")
            for ch, w, h in bad:
                print(f"      {ch!r}: w={w:.3f} ({w / med_w:.1f}x)  "
                      f"h={h:.3f} ({h / med_h:.1f}x)")
