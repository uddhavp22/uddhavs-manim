#!/usr/bin/env python3
"""Print where manim will write a scene's mp4, before it is rendered.

build.sh needs the output path *ahead* of the render, not after: the freshness
guard compares the file's mtime from before the attempt against the mtime after,
which is the only reliable way to tell "this render produced this file" from
"a previous render left this file here and today's crashed" (manim exits 0 after
an exception inside construct()).

Under manimgl the path was ours to construct. Manim Community owns it, and
composes it from config:

    {media_dir}/videos/{module_name}/{quality}/{SceneName}.mp4

where {quality} is a resolution-and-framerate stamp like `480p15` derived from
whichever -q flag was passed. Rather than hardcode that map -- which would drift
the moment the engine is upgraded or manim.cfg changes the frame rate -- this
asks the installed engine to resolve the path with its own config machinery.
Importing manim also picks up manim.cfg from the working directory, exactly as a
real render does, so an override there is honoured here too.

    python3 tools/output_path.py projects/.../b02_arrows.py B02 -ql

Prints one absolute path. Exits 2 on an unrecognised quality flag rather than
guessing, because a wrong path here silently disables the freshness guard.

This module also OWNS the project's chapter-grouping rule (see
`video_dir_template`), and it owns it because of that same freshness guard.
Manim's default flattens every scene file in the repo into one folder next to
unrelated projects, so a chapter's renders are grouped by the rule below
instead. The rule has to be applied in exactly two places -- here, and by
`render.sh` when it invokes the engine -- and if the two ever disagree,
build.sh compares the mtime of a file the render never wrote, which reports
every scene as freshly built. So `render.sh` asks THIS file for the template
rather than restating it:

    python3 tools/output_path.py --video-dir-template projects/.../c05.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import config
from manim.constants import QUALITIES

# Derive -ql/-qm/-qh/-qp/-qk from the engine's own table instead of restating
# it. QUALITIES holds the flag letter for every quality that has one;
# example_quality has flag None and is not reachable from the command line.
FLAG_TO_QUALITY = {
    f"-q{q['flag']}": name for name, q in QUALITIES.items() if q["flag"]
}


def video_dir_template(src: Path) -> str | None:
    """Where a scene file's renders belong, as a manim `video_dir` template.

    Scene files live at `projects/<project>/<chapter>/<module>.py`, and their
    renders belong together at `<media_dir>/videos/<project>/<chapter>/`.
    Manim's default is `{media_dir}/videos/{module_name}/{quality}`, which puts
    `c05_gaussian_marginals` beside `ionic_bonds` and loses the chapter
    entirely -- and `get_dir` only knows the placeholders `{media_dir}`,
    `{module_name}`, `{quality}` and `{scene_name}`, so the chapter cannot be
    recovered from inside manim.cfg. It has to be resolved from the source
    path, which is what this does.

    Returns None for anything not two levels below a `projects/` directory --
    a loose probe, a scratch file, another repo's scene -- and those keep the
    engine's default. Silently relocating a file we cannot place confidently is
    worse than leaving it where manim would have put it.
    """
    parts = Path(src).resolve().parts
    if "projects" not in parts:
        return None
    # Rightmost `projects/`, so a checkout that happens to sit inside a
    # directory of that name resolves against the repo's own.
    root = len(parts) - 1 - parts[::-1].index("projects")
    below = parts[root + 1:]
    if len(below) != 3:
        # Exactly <project>/<chapter>/<module>.py. `projects/<project>/x.py`
        # has no chapter level, and anything deeper is not a shape this rule
        # was written for; both keep the engine's default.
        return None
    project, chapter, _ = below
    return (f"{{media_dir}}/videos/{project}/{chapter}"
            "/{module_name}/{quality}")


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "--video-dir-template":
        # For render.sh. Prints nothing (and exits 0) when the default applies,
        # so the caller can test for an empty string.
        template = video_dir_template(Path(argv[2]))
        if template:
            print(template)
        return 0

    if len(argv) < 3:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        print("usage: output_path.py <src.py> <SceneName> [-ql|-qm|-qh|-qp|-qk]",
              file=sys.stderr)
        return 2

    src, scene = Path(argv[1]), argv[2]
    flags = argv[3:]

    for flag in flags:
        if flag in FLAG_TO_QUALITY:
            config.quality = FLAG_TO_QUALITY[flag]
        elif flag.startswith("-q"):
            print(f"error: unrecognised quality flag {flag!r}; "
                  f"expected one of {', '.join(sorted(FLAG_TO_QUALITY))}",
                  file=sys.stderr)
            return 2
        # Any other flag is not ours to interpret; manim gets it, and none of
        # the ones build.sh passes affect the directory.

    # The chapter-grouping rule, applied to the same config object the engine
    # would use. render.sh feeds the identical template to the real render
    # through a generated config file, so the two cannot drift.
    template = video_dir_template(src)
    if template:
        config.video_dir = template

    # module_name is the source file's stem -- manim derives it the same way
    # when it loads the scene file by path.
    video_dir = config.get_dir("video_dir", module_name=src.stem)
    print((Path(video_dir) / f"{scene}.mp4").resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
