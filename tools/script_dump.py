#!/usr/bin/env python3
"""Generate a readable master script from the scene files.

A script kept as a separate hand-maintained document rots the moment a line is
edited in a scene, and then two versions disagree with no way to tell which is
real. This derives the script from the same AST the audit reads, so the file is
always what the render actually says.

    python3 tools/script_dump.py projects/sigreg_explainer/chapterB \\
        -o projects/sigreg_explainer/SCRIPT_chapterB.md

Durations come from the rendered MP4s when they exist, so the word counts and
the runtime in the output belong to the same version of the chapter.
"""

from __future__ import annotations

import argparse
import ast
import pathlib
import re
import subprocess
import sys
import textwrap

BOOKMARK = re.compile(r"<bookmark\s+mark=['\"]([^'\"]*)['\"]\s*/>")

# Calls whose first string argument lands on screen. Kept in step with
# narration_audit.onscreen_text -- both need to know what counts as the second
# channel (NARRATION_SPEC.md 7.2).
ONSCREEN_CALLS = (
    "Text", "MathTex", "maths", "words", "statement", "label", "caption",
    "curve_label",
)

# `build.sh` deliberately plays Chapter B as an argument rather than filename
# order. Keep the generated master script in that same order, so a reader is
# reviewing what will actually be rendered and concatenated.
PLAYBACK_ORDER = {
    "chapterB": (
        "b00", "b01", "b02", "b03", "b04", "b05", "b06", "b07",
        "b08", "b09", "b10", "b11",
    ),
}


def _const_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _const_str(node.left), _const_str(node.right)
        return None if a is None or b is None else a + b
    return None


def scene_content(path: pathlib.Path):
    """-> (docstring_first_line, [(lineno, kind, text)]) in source order.

    kind is "spoken" or "screen". Source order is close enough to playback
    order to read as a script, and is the only ordering available without
    executing the scene.
    """
    tree = ast.parse(path.read_text(), filename=str(path))
    doc = (ast.get_docstring(tree) or "").strip().split("\n")[0]

    items = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "attr", getattr(node.func, "id", ""))

        if name == "voiceover":
            for kw in node.keywords:
                if kw.arg != "text":
                    continue
                values = (kw.value.elts
                          if isinstance(kw.value, (ast.List, ast.Tuple))
                          else [kw.value])
                for v in values:
                    s = _const_str(v)
                    if s:
                        items.append((node.lineno, "spoken", s))

        elif name in ONSCREEN_CALLS:
            if node.args and isinstance(node.args[0], ast.Constant) \
               and isinstance(node.args[0].value, str):
                s = node.args[0].value
                if len(s.split()) >= 2:
                    items.append((node.lineno, "screen", s))

    items.sort(key=lambda i: i[0])
    return doc, items


def duration(scene_stem: str, chapter_dir: pathlib.Path) -> float | None:
    repo = chapter_dir.parents[2]
    scene = scene_stem.split("_")[0].upper()
    mp4 = (repo / "videos" / chapter_dir.parent.name / chapter_dir.name
           / scene_stem / f"{scene}.mp4")
    if not mp4.exists():
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(mp4)],
            capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return None


def playback_files(chapter: pathlib.Path) -> list[pathlib.Path]:
    """Return scene sources in the build order when the chapter defines one."""
    files = sorted(chapter.glob("[abc][0-9][0-9]*_*.py"))
    order = PLAYBACK_ORDER.get(chapter.name)
    if not order:
        return files
    by_prefix = {f.stem.split("_")[0]: f for f in files}
    missing = [prefix for prefix in order if prefix not in by_prefix]
    if missing:
        raise ValueError(
            f"{chapter.name} playback order names missing scenes: {', '.join(missing)}"
        )
    extras = sorted(set(by_prefix) - set(order))
    if extras:
        raise ValueError(
            f"{chapter.name} playback order omits scenes: {', '.join(extras)}"
        )
    return [by_prefix[prefix] for prefix in order]


def mmss(seconds: float) -> str:
    return f"{int(seconds) // 60}:{int(seconds) % 60:02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", help="a chapter directory of scene files")
    ap.add_argument("-o", "--out", help="write here instead of stdout")
    args = ap.parse_args()

    chapter = pathlib.Path(args.chapter)
    try:
        files = playback_files(chapter)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    if not files:
        print(f"no scene files under {chapter}", file=sys.stderr)
        return 2

    lines: list[str] = []
    w = lines.append

    total_words = total_secs = 0.0
    rows = []
    for f in files:
        _, items = scene_content(f)
        n = sum(len(re.findall(r"[A-Za-z']+", t))
                for _, kind, t in items if kind == "spoken")
        d = duration(f.stem, chapter)
        rows.append((f.stem, n, d))
        total_words += n
        total_secs += d or 0.0

    w(f"# Master script — `{chapter.name}`")
    w("")
    w("**Generated — do not edit.** Regenerate with:")
    w("")
    w("```bash")
    w(f"python3 tools/script_dump.py {chapter} \\")
    w(f"    -o {chapter.parent}/SCRIPT_{chapter.name}.md")
    w("```")
    w("")
    w("Extracted from `self.voiceover(text=…)` in the scene files, which is what")
    w("the render actually speaks. On-screen text is included as a second")
    w("channel — [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) §7.2 treats it as")
    w("one, and a line cut from the voice and left on screen is not cut.")
    w("")
    w("Scenes follow the chapter's playback order. Ordering within a scene is")
    w("source order, which tracks playback order but")
    w("is not guaranteed to equal it: on-screen text is often constructed a few")
    w("lines before the passage that reveals it.")
    w("")
    w(f"**{len(files)} scenes · {int(total_words):,} spoken words · "
      f"{mmss(total_secs)}**")
    w("")
    w("| Scene | Words | Duration | Words/min |")
    w("|---|---:|---:|---:|")
    for stem, n, d in rows:
        wpm = f"{n / (d / 60):.0f}" if d else "—"
        w(f"| [`{stem}`](#{stem.replace('_', '-')}) | {n} | "
          f"{mmss(d) if d else '—'} | {wpm} |")
    w("")
    w("---")
    w("")

    for f in files:
        doc, items = scene_content(f)
        d = duration(f.stem, chapter)
        w(f"## {f.stem}")
        w("")
        if doc:
            w(f"*{doc}*")
            w("")
        if d:
            w(f"`{mmss(d)}` · [`{f.name}`]({chapter.name}/{f.name})")
            w("")

        for _, kind, text in items:
            if kind == "spoken":
                marks = BOOKMARK.findall(text)
                clean = " ".join(BOOKMARK.sub("", text).split())
                body = textwrap.fill(clean, 78)
                w(body)
                if marks:
                    w("")
                    w(f"<sub>cues: {', '.join(marks)}</sub>")
                w("")
            else:
                flat = " ".join(text.split())
                w(f"> **ON SCREEN** — {flat}")
                w("")
        w("---")
        w("")

    out = "\n".join(lines)
    if args.out:
        pathlib.Path(args.out).write_text(out)
        print(f"wrote {args.out}  ({len(files)} scenes, "
              f"{int(total_words):,} words, {mmss(total_secs)})")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
