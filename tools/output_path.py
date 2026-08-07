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

    python3 tools/output_path.py projects/.../b01_arrows.py B01 -ql

Prints one absolute path. Exits 2 on an unrecognised quality flag rather than
guessing, because a wrong path here silently disables the freshness guard.
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


def main(argv: list[str]) -> int:
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

    # module_name is the source file's stem -- manim derives it the same way
    # when it loads the scene file by path.
    video_dir = config.get_dir("video_dir", module_name=src.stem)
    print((Path(video_dir) / f"{scene}.mp4").resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
