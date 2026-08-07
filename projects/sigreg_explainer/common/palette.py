"""Colour roles for the SIGReg explainer.

The rules and the reasoning behind each value live in VISUAL_SYSTEM.md section 4.
This file is the only place these hex values exist -- import the role, never the
colour, so a restyle is one edit.

Roles, not names: a scene asks for TARGET because it is drawing the Gaussian
reference, not because it wants amber.
"""

# --- ground ----------------------------------------------------------------
# Not pure black. #000000 crushed the panel furniture out of existence at 480p;
# a near-black with a slight cool cast leaves room for GRID to sit below the
# data without vanishing. Must match camera.background_color in custom_config.yml.
BG = "#0C0E12"

# --- text ------------------------------------------------------------------
INK = "#EDF0F4"       # primary text. Off-white; #FFFFFF on near-black glares.
MUTED = "#8A93A0"     # panel captions, de-emphasised context
AXIS = "#5A6472"      # axis lines, ticks, tick labels
GRID = "#2A303A"      # grid lines, panel furniture

# --- semantic --------------------------------------------------------------
CLOUD = "#4FA8E8"     # the data: samples, its arrows, its fingerprint, real parts
TARGET = "#F0B429"    # the Gaussian reference and its fingerprint
COLLAPSE = "#E8615A"  # the gap, the error, imaginary parts, the failure case
DIRECTION = "#5FCF80" # directions u, projections, shadows
ACCENT = "#EDF0F4"    # the single "look here now" highlight

# EMPIRICAL was a second blue one step from CLOUD (BLUE_B vs BLUE_C). At
# delivery size they were indistinguishable, and they were never really two
# ideas -- the empirical fingerprint belongs to the batch. Kept as an alias so
# existing imports resolve, but new code should say CLOUD.
EMPIRICAL = CLOUD

# Retired names, mapped so nothing breaks mid-rewrite.
FAINT = GRID
