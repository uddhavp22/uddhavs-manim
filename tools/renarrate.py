#!/usr/bin/env python3
"""Rewrite narration in place, matching on spoken text rather than source layout.

Narration lives inside `self.voiceover(text=...)` as implicitly concatenated
string literals wrapped to 79 columns, so the source form of a passage bears no
relation to the sentence anyone reads. Hand-editing it means matching whitespace
and continuation quotes, which is where narration edits historically went wrong:
a passage silently kept its old audio because one character of the replacement
did not match.

This locates each passage by its *normalised spoken text* -- bookmarks stripped,
whitespace collapsed -- and replaces the literal by AST span, then re-wraps.

    python3 tools/renarrate.py <edits.py>

where edits.py defines EDITS: {scene_stem: [(old_normalised, new_text), ...]}.
Every entry must match exactly one passage, or nothing is written.
"""

from __future__ import annotations

import ast
import pathlib
import re
import runpy
import sys
import textwrap

BOOKMARK = re.compile(r"<bookmark\s+mark=['\"][^'\"]*['\"]\s*/>")


def normalise(s: str) -> str:
    return " ".join(BOOKMARK.sub("", s).split())


def _const_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _const_str(node.left), _const_str(node.right)
        return None if a is None or b is None else a + b
    return None


def passages(tree: ast.AST):
    """-> [(node, text)] for every voiceover(text=...) with a literal string."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if not (isinstance(fn, ast.Attribute) and fn.attr == "voiceover"):
            continue
        for kw in node.keywords:
            if kw.arg != "text":
                continue
            s = _const_str(kw.value)
            if s is not None:
                out.append((kw.value, s))
    return out


def render_literal(text: str, indent: int) -> str:
    """Format a passage as wrapped implicitly-concatenated literals.

    Bookmarks are kept glued to the sentence that follows them, so a re-wrap can
    never move a bookmark across a sentence boundary and desynchronise the
    animation from the speech.
    """
    pad = " " * indent
    chunks = [c for c in re.split(r"(<bookmark\s+mark=['\"][^'\"]*['\"]\s*/>)", text) if c]
    lines: list[str] = []
    for chunk in chunks:
        if chunk.startswith("<bookmark"):
            lines.append(chunk)
            continue
        # break_on_hyphens=False: the default splits "well-chosen" after the
        # hyphen, and the join below then inserts a space, so the literal
        # concatenates to "well- chosen" and the voice says it that way.
        wrapped = textwrap.wrap(chunk.strip(), width=72 - indent,
                                break_on_hyphens=False) or [""]
        if lines and lines[-1].startswith("<bookmark"):
            lines[-1] = lines[-1] + wrapped[0]
            lines.extend(wrapped[1:])
        else:
            lines.extend(wrapped)
    parts = []
    for i, ln in enumerate(lines):
        trailing = " " if i < len(lines) - 1 and not ln.endswith(("/>", " ")) else ""
        parts.append('"' + ln.replace('"', r"\"") + trailing + '"')
    return ("\n" + pad).join(parts)


def apply(path: pathlib.Path, edits: list[tuple[str, str]]) -> int:
    src = path.read_text()
    lines = src.splitlines(keepends=True)
    offsets = [0]
    for ln in lines:
        offsets.append(offsets[-1] + len(ln))

    def span(node):
        return (offsets[node.lineno - 1] + node.col_offset,
                offsets[node.end_lineno - 1] + node.end_col_offset)

    found = []
    for old, new in edits:
        target = normalise(old)
        matches = [(n, t) for n, t in passages(ast.parse(src)) if normalise(t) == target]
        if len(matches) != 1:
            print(f"  {path.name}: {len(matches)} matches for {target[:64]!r}",
                  file=sys.stderr)
            return -1
        found.append((span(matches[0][0]), new, matches[0][0].col_offset))

    # Apply back to front so earlier spans stay valid.
    for (start, end), new, col in sorted(found, key=lambda f: -f[0][0]):
        src = src[:start] + render_literal(new, col) + src[end:]

    ast.parse(src)                       # never write a file that will not parse
    path.write_text(src)
    return len(found)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    mod = runpy.run_path(sys.argv[1])
    base = pathlib.Path(mod["CHAPTER"])
    total = 0
    for stem, edits in mod["EDITS"].items():
        # "{stem}_*" not "{stem}*": b06 must not match b06a_one_speed_fails.py.
        path = next(base.glob(f"{stem}_*.py"))
        n = apply(path, edits)
        if n < 0:
            print("aborted; nothing written for", path.name, file=sys.stderr)
            return 1
        print(f"{path.name}: {n} passages rewritten")
        total += n
    print(f"total {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
