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
# Desaturated steel blue-gray: the projector module's own colour.  Every
# saturated slot in this palette is already spoken for (green=prediction,
# amber=target, red=error, violet=SIGReg, blue=data/backbone), and the
# projected vectors passing through this module must keep their own
# green/amber identity rather than being recoloured by it -- see scene 3's
# beat table.  ~30% saturation at hue ~220: cooler than MUTED, dimmer and
# bluer than SIGREG.
PROJECTOR = "#7C8EB8"
# The old PROJECTOR hex.  Scene 1's LeJEPA global-crop callback inherited this
# colour from the previous chapter and has nothing to do with the projector
# module scene 3 draws; split the role under its own name instead of letting
# two unrelated concepts share one colour.
VIEW_GLOBAL = "#E58A3A"
KEEP = DIRECTION
DISCARD = MUTED

