"""The single prose style needed by silent AP Biology scenes."""

from pathlib import Path

from manim import Text
from manim.mobject.text.text_mobject import register_font

from .palette import INK, MUTED

FONT = "Latin Modern Roman"
TITLE = 46
CAPTION = 28
LABEL = 24
_CE_TEXT_CALIBRATION = 1.3623
_FONT_FILE = (
    Path.home()
    / "Library/TinyTeX/texmf-dist/fonts/opentype/public/lm/lmroman10-regular.otf"
)


def _text(text: str, size: int, color: str) -> Text:
    # render.sh already binds this project to TinyTeX. Register its OpenType
    # face for the duration of Text construction so Pango cannot silently
    # substitute a system font on machines where it is not globally installed.
    with register_font(_FONT_FILE):
        return Text(text, font=FONT, font_size=size / _CE_TEXT_CALIBRATION, color=color)


def title(text: str) -> Text:
    """Set the concept name at the repository's calibrated TITLE tier."""
    return _text(text, TITLE, INK)


def caption(text: str) -> Text:
    """Set a caption at the repository's calibrated CAPTION tier."""
    return _text(text, CAPTION, MUTED)


def label(text: str) -> Text:
    """Set a short annotation (e.g. a bond-type name) at the LABEL tier."""
    return _text(text, LABEL, MUTED)
