"""Small utilities shared across the voiceover package.

Ported from manim-voiceover (ManimCommunity/manim-voiceover, MIT). The
bookmark regex is character-for-character the upstream one so that scripts
written against either project tokenize identically.
"""
from __future__ import annotations

import re
import textwrap
import unicodedata
from typing import Iterator, Sequence, TypeVar

T = TypeVar("T")

# Upstream: manim_voiceover/helper.py::remove_bookmarks
BOOKMARK_PATTERN = r"<bookmark\s*mark\s*=['\"]\w*[\"']\s*/>"
# Upstream: manim_voiceover/tracker.py::_process_bookmarks
BOOKMARK_SPLIT_PATTERN = r"(<bookmark\s*mark\s*=[\'\"]\w*[\"\']\s*/>)"
BOOKMARK_CAPTURE_PATTERN = r"<bookmark\s*mark\s*=[\'\"](.*)[\"\']\s*/>"


def remove_bookmarks(input: str) -> str:
    return re.sub(BOOKMARK_PATTERN, "", input)


def chunks(lst: Sequence[T], n: int) -> Iterator[Sequence[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def slugify(text: str, max_length: int = 50) -> str:
    """Filename-safe slug, word-boundary truncated.

    Stands in for python-slugify (upstream dependency) using only stdlib
    (unicodedata, re), so this file adds no extra pip requirement.
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    words = text.split()

    out: list[str] = []
    length = 0
    for word in words:
        # +1 for the joining hyphen
        if out and length + 1 + len(word) > max_length:
            break
        length += len(word) + (1 if out else 0)
        out.append(word)

    if not out:
        return words[0][:max_length] if words else "voiceover"
    return "-".join(out)


def msg_box(msg: str, indent: int = 1, width: int | None = None, title: str | None = None) -> str:
    """Print message-box with optional title."""
    raw_lines = msg.splitlines() or [""]
    space = " " * indent
    if width is None:
        width = min(max(map(len, raw_lines)), 80)
    lines: list[str] = []
    for line in raw_lines:
        lines.extend(textwrap.wrap(line, width) or [""])

    box = f"╔{'═' * (width + indent * 2)}╗\n"
    if title:
        box += f"║{space}{title:<{width}}{space}║\n"
        box += f"║{space}{'-' * len(title):<{width}}{space}║\n"
    box += "".join([f"║{space}{line:<{width}}{space}║\n" for line in lines])
    box += f"╚{'═' * (width + indent * 2)}╝"
    return box
