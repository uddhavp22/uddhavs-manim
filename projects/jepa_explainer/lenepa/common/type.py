"""LeNEPA typography, delegated to the repository's canonical type system."""

import sys as _sys
from pathlib import Path as _Path

# ``tools/preflight.py`` imports star modules with its own folder at sys.path[0],
# while Manim receives the repo root through render.sh's PYTHONPATH.  Make this
# wrapper resolve identically in both paths.
_sys.path.insert(0, str(_Path(__file__).resolve().parents[4]))

from projects.sigreg_explainer.common.type import (  # noqa: E402
    BODY,
    CAPTION,
    EQ,
    EQ_DISPLAY,
    EQ_HERO,
    LABEL,
    MIN_SIZE,
    READOUT,
    STATEMENT,
    TICK,
    TITLE,
    Text,
    below,
    caption,
    curve_label,
    label,
    line,
    maths,
    readout,
    statement,
    title,
    words,
)

__all__ = [
    "BODY", "CAPTION", "EQ", "EQ_DISPLAY", "EQ_HERO", "LABEL",
    "MIN_SIZE", "READOUT", "STATEMENT", "TICK", "TITLE", "Text",
    "below", "caption", "curve_label", "label", "line", "maths",
    "readout", "statement", "title", "words",
]
