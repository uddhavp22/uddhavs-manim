"""Typography for the SIGReg explainer.

The rules live in VISUAL_SYSTEM.md sections 2 and 3. The short version:

    MathTex -> mathematics    (Computer Modern, via LaTeX)
    Text    -> English        (Computer Modern Roman, installed as OpenType)

and nothing on screen is below MIN_SIZE.

One face, two renderers. `MathTex` sets Computer Modern because that is what the
default LaTeX template does; `Text` sets the original Computer Modern Roman in
an OpenType conversion. The two match exactly, so a caption and an equation in
the same frame read as one document rather than two design systems.

`MathTex`, not `Tex`: Manim Community splits the two, and its `Tex` compiles in
LaTeX *text* mode. Everything this module calls mathematics is set in math mode,
which is `MathTex` here. Mixed prose-and-symbol lines are assembled by `line()`
out of `Text` and `MathTex` parts rather than by dropping `\\text{...}` into a
formula.

Every helper here passes `font=` explicitly rather than relying on
config.font. Manim's default is the empty string, which lets Pango substitute
silently -- the original cause of the whole restyle. Setting it in manim.cfg
fixes it globally; setting it here as well means a render from a machine
without that config still looks right. The guard at the bottom of this module
turns a missing face into an import error instead, because that silent fallback
cost a whole chapter's re-render once already.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import DecimalNumber, MathTex, RIGHT, UP, VGroup
from manim import Text as _ManimText

from .palette import INK, MUTED

# --- the one typeface ------------------------------------------------------
# Converted from TinyTeX's original Type 1 cmr10.pfb into ~/Library/Fonts.
#
# Regular only, and not by preference. The prior Latin Modern Demi/Bold faces
# returned corrupt glyphs through manimpango; the converted original is
# deliberately the supplied regular cmr10 face only. Nothing raises for a bad
# weight: a stray path and inflated bounding box silently wreck arrange() and
# set_height(). Asking Pango for MEDIUM is not a substitute for an installed
# face, so hierarchy remains size and colour alone.
#
# Hierarchy therefore runs on size and colour alone. tools/font_check.py is the
# regression check; run it if the typeface ever changes.
FONT = "Computer Modern"

# CE renders Text 1.3623x larger than ManimGL at the same font_size -- measured
# directly: font_size 24/36/48 gave height ratios 1.3632/1.3616/1.3623, and the
# ratio held across strings too. ManimGL calibrates on
# font_size_for_unit_height = 144, CE on SCALE_FACTOR_PER_FONT_POINT = 1/960;
# the two were never meant to agree. MathTex and DecimalNumber are unaffected
# (1.031 and 1.018 -- imperceptible), so this is a Text-only correction, applied
# below so the tier numbers under it keep meaning what they meant when they
# were set by reading _fonttest.py under ManimGL.
_CE_TEXT_CALIBRATION = 1.3623

# --- the scale (VISUAL_SYSTEM.md section 3) --------------------------------
# px at 1080p = font_size * 0.9375
#
# These tiers were last judged with Latin Modern. Computer Modern's original
# x-height can differ, so re-check _fonttest.py at delivery size before any
# scale retuning; that is a design decision, not an import-time adjustment.
TITLE = 46      # transient scene title card
STATEMENT = 36  # the one sentence a beat is about
BODY = 31       # a full annotation sentence on screen
CAPTION = 28    # pinned above a panel
LABEL = 26      # legend, curve label, short annotation
TICK = 24       # axis tick label -- the hard floor
READOUT = 32    # live "t = 1.35"

# Display mathematics still runs on its own tier, but for a different reason
# than before. The old note here said Computer Modern at 32 does not read as
# the same size as Helvetica at 32 -- true, and now moot, since both channels
# are the same face. What survives is that a derivation the viewer must read is
# a different job from a caption, so EQ sits level with BODY and the two larger
# steps exist for emphasis rather than for compensation.
EQ = 31         # an equation in the flow of a scene, level with BODY
EQ_DISPLAY = 48 # the one equation a beat is about
EQ_HERO = 64    # a result held alone on screen

# Before this module, each of the twelve Chapter B scenes declared its own
# BODY/SMALL/NOTE at 26, 27, or 28 and 21, 22, or 23. Twelve near-identical
# scales is the same defect as no scale: nothing lines up across a cut, and
# RENDER_REVIEW_SPEC.md section 8.3 (consistent typeface and font sizes) has
# nothing to check against. Six steps, one place.

MIN_SIZE = 24

# Kept because ~30 call sites name them, and because the distinction they mark
# -- "this is the active line, that is context" -- is still real. It is now
# carried by size and colour rather than by stroke weight; see the FONT note.
NORMAL = "NORMAL"
MEDIUM = "MEDIUM"


def _checked(font_size: int) -> int:
    """Refuse to render text nobody can read.

    An unreadable label is a silent failure -- it renders without complaint and
    fails review later, after a full-resolution render has been spent on it.
    Fail here instead.
    """
    if font_size < MIN_SIZE:
        raise ValueError(
            f"font_size={font_size} is below the {MIN_SIZE} floor "
            f"(VISUAL_SYSTEM.md section 3). If the text does not fit at "
            f"{MIN_SIZE}, the layout is wrong, not the type size."
        )
    return font_size


class Text(_ManimText):
    """The project's Text: calibrated to ManimGL's scale, `font=` defaulted.

    Two defects, one fix. (1) CE's font_size is not ManimGL's -- see the
    `_CE_TEXT_CALIBRATION` note above; dividing by it here means TITLE/BODY/etc.
    still mean what they meant when they were set. (2) CE has no global font
    setting the way `custom_config.yml`'s `text.font` was, so a scene that
    constructs `Text(...)` without `font=` silently gets whatever Pango picks --
    the exact defect VISUAL_SYSTEM.md section 1 exists to prevent. Defaulting
    `font=FONT` here closes every call site at once, including the ones in scene
    files that import this class directly instead of going through `words()`.
    """

    def __init__(self, text: str, *, font_size: int = BODY, font: str = FONT, **kwargs):
        super().__init__(
            text, font=font, font_size=_checked(font_size) / _CE_TEXT_CALIBRATION, **kwargs
        )


def words(
    text: str,
    size: int = LABEL,
    color: str = INK,
    weight: str = NORMAL,
) -> Text:
    """English. Never mathematics.

    `weight` is accepted and deliberately not passed through: no heavier Latin
    Modern face survives this pipeline intact (see the FONT note). Callers keep
    saying MEDIUM to record which line is the active one; the emphasis itself
    comes from the size and colour they pick alongside it.
    """
    return Text(text, font_size=size).set_color(color)


def title(text: str) -> Text:
    return words(text, size=TITLE, weight=MEDIUM)


def statement(text: str, color: str = INK) -> Text:
    """The single sentence a beat is about."""
    return words(text, size=STATEMENT, color=color, weight=MEDIUM)


def caption(text: str) -> Text:
    """Pinned above a panel, in MUTED -- furniture, not argument."""
    return words(text, size=CAPTION, color=MUTED)


def label(text: str, color: str = INK) -> Text:
    return words(text, size=LABEL, color=color)


def maths(expression: str, size: int = LABEL, color: str = INK,
          isolate: list[str] | None = None) -> MathTex:
    """Mathematics. Never English.

    If a `\\text{...}` is needed inside, the label is prose and belongs in
    `words()` beside the expression, not inside it.

    `isolate` names sub-expressions to break out as their own submobjects, so
    they can be coloured or animated separately:

        eq = ty.maths(R"e^{i\\theta} = \\cos\\theta + i\\,\\sin\\theta",
                      isolate=[R"\\cos\\theta", R"\\sin\\theta"])
        eq.set_color_by_tex(R"\\cos\\theta", EMPIRICAL)

    Without it a MathTex is one single submobject, and `set_color_by_tex` then
    matches the whole formula rather than the part asked for -- which colours
    the entire equation and looks like the call silently did nothing.
    """
    tex = MathTex(
        expression,
        font_size=_checked(size),
        substrings_to_isolate=list(isolate) if isolate else None,
    )
    return tex.set_color(color)


@lru_cache(maxsize=None)
def _baseline_drop(kind: str, text: str, size: int) -> float:
    """Measure ink extending below a part's baseline proxy.

    Manim trims Text and MathTex to their ink and exposes no baseline.  In a
    same-kind probe, a leading capital H gives that baseline: the difference
    between its bottom and the remaining ink is the descender drop.  Cache the
    scalar, not the probe mobject, so repeated live readouts stay inexpensive.
    """
    # DecimalNumber contains only numerals here, whose ink bottoms sit on the
    # baseline; unlike Text/MathTex it cannot be prefixed with an H probe.
    if kind == "decimal":
        return 0.0
    make = words if kind == "words" else maths
    probe = make("H" + text, size=size)
    # Down to the drawn glyphs, because the two kinds nest differently: a Text
    # holds one submobject per character, while a MathTex holds a single
    # SingleStringMathTex whose own submobjects are the glyphs. Comparing
    # `probe.submobjects` directly would measure a one-item list for every
    # equation and silently return a zero drop.
    glyphs = probe.family_members_with_points()
    if len(glyphs) < 2:
        return 0.0
    rest = VGroup(*glyphs[1:])
    return float(glyphs[0].get_bottom()[1] - rest.get_bottom()[1])


def _align_baselines(group: VGroup, metadata: list[tuple[str, str, int]]) -> None:
    """Align mixed Text/Tex parts by a measured baseline, not ink bottoms."""
    if len(group) < 2:
        return
    drops = [_baseline_drop(kind, text, size) for kind, text, size in metadata]
    target = group[0].get_bottom()[1] + drops[0]
    for mob, drop in zip(group[1:], drops[1:]):
        mob.shift((target - (mob.get_bottom()[1] + drop)) * UP)


def line(*parts: str, size: int = LABEL, color: str = INK) -> VGroup:
    """One baseline mixing English and mathematics.

    Parts wrapped in $...$ are set as MathTex; everything else as Text.

        ty.line("mean ", "$= +0.00$")
        ty.line("$X$ symmetric about ", "$0$", " so ", R"$\\operatorname{Im}\\varphi = 0$")

    This exists because `MathTex(R"\\text{mean} = +0.00")` sets an English word in
    Computer Modern roman, which is what put a serif "mean" and "variance"
    directly above a Helvetica sentence in b00 and made the frame look
    unstyled. VISUAL_SYSTEM.md section 2: one face per job.
    """
    group = VGroup()
    metadata: list[tuple[str, str, int]] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("$") and part.endswith("$"):
            group.add(maths(part[1:-1], size=size, color=color))
            metadata.append(("maths", part[1:-1], size))
        else:
            # Pango collapses leading/trailing spaces, so carry them as buffs.
            text = part.strip()
            group.add(words(text, size=size, color=color))
            metadata.append(("words", text, size))
    group.arrange(RIGHT, buff=0.16)
    _align_baselines(group, metadata)
    return group


def readout(name: str, tracker, places: int = 2, color: str = INK) -> VGroup:
    """A labelled live number: the word in Helvetica, the value in Computer Modern.

    The one place the two faces legitimately meet. Caller wraps in always_redraw.
    """
    group = VGroup(
        maths(name + " =", size=READOUT, color=color),
        DecimalNumber(
            tracker.get_value(),
            num_decimal_places=places,
            font_size=READOUT,
        ).set_color(color),
    )
    group.arrange(RIGHT, buff=0.14)
    _align_baselines(
        group,
        [("maths", name + " =", READOUT), ("decimal", "", READOUT)],
    )
    return group


def curve_label(text: str, color: str, size: int = LABEL) -> Text:
    """Names a curve in its own colour.

    Colour alone must never carry the distinction (RENDER_REVIEW_SPEC.md
    section 12), so every coloured curve gets one of these placed on the curve
    rather than in a corner legend.
    """
    return words(text, size=size, color=color, weight=MEDIUM)


def below(mob, text_mob, buff: float = 0.28):
    """Place text under a mobject, kept inside the safe margin."""
    from .layout import fit_in_frame

    text_mob.next_to(mob, np.array([0.0, -1.0, 0.0]), buff=buff)
    return fit_in_frame(text_mob, margin=0.45)


def _assert_fonts_installed() -> None:
    """Fail at import if the typeface is missing.

    Pango does not raise on an absent family -- it substitutes silently, and the
    render completes looking wrong with no traceback. That is exactly how the
    project shipped a whole chapter in an unspecified fallback face
    (VISUAL_SYSTEM.md section 1, PLAN.md section 10). Same shape as
    layout._assert_panels_inside_frame(): make the silent failure loud, here,
    before a render is spent on it.
    """
    import manimpango

    # Dropping the converted .otf into ~/Library/Fonts is not sufficient on
    # its own: unlike Latin Modern (installed the same way, and picked up by
    # CoreText immediately), this fontforge-generated file was not picked up
    # by the OS font registry even after `fc-cache -f` and a font-cache reset
    # -- manimpango's macOS build talks to CoreText directly (see its linked
    # frameworks), not fontconfig, and CoreText's auto-scan of ~/Library/Fonts
    # did not validate this particular file. `register_font()` is manimpango's
    # own documented API for exactly this: it hands the file to the native OS
    # API directly, no cache/registry dependent on timing. Calling it here
    # every import is idempotent and cheap, and removes the dependency on
    # whatever silently made Latin Modern work and this face not.
    font_path = Path.home() / "Library" / "Fonts" / "cmr10.otf"
    if font_path.exists():
        manimpango.register_font(str(font_path))

    if FONT not in set(manimpango.list_fonts()):
        raise RuntimeError(
            f"typeface not installed: {FONT!r}.\n"
            f"Install FontForge and convert the supplied Type 1 face:\n"
            f"    brew install fontforge\n"
            f"    fontforge -lang=py -c \"import fontforge; "
            f"f = fontforge.open('$HOME/Library/TinyTeX/texmf-dist/fonts/"
            f"type1/public/amsfonts/cm/cmr10.pfb'); "
            f"f.generate('$HOME/Library/Fonts/cmr10.otf')\"\n"
            f"Then confirm the Pango family with:\n"
            f"    python3 -c \"import manimpango; print([f for f in "
            f"manimpango.list_fonts() if 'cm' in f.lower() or "
            f"'computer' in f.lower()])\"\n"
            f"then verify glyph integrity with:\n"
            f"    ./render.sh tools/font_check.py FontCheck -s -ql\n"
            f"See VISUAL_SYSTEM.md section 2."
        )


_assert_fonts_installed()
