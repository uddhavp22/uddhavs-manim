"""Semantic colour roles for the LeNEPA segment.

The base roles come from the repository-wide visual system.  The aliases below
name what each colour means in this particular architecture, so scene files do
not make colour decisions.
"""

from projects.sigreg_explainer.common.palette import (
    ACCENT,
    AXIS,
    BG,
    CLOUD,
    COLLAPSE,
    DIRECTION,
    GRID,
    INK,
    MUTED,
    TARGET,
)

INPUT = CLOUD
BACKBONE = CLOUD
PREDICTION = DIRECTION
NEXT_TARGET = TARGET
ERROR = COLLAPSE
SIGREG = "#9D6FE0"
PROJECTOR = "#E58A3A"
KEEP = DIRECTION
DISCARD = MUTED

