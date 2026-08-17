#!/usr/bin/env python3
"""Find stretches where the picture stops moving while narration continues.

    python3 tools/still_frames.py videos/.../chapterB1_master.mp4 --min 4

`tools/dead_air.py` detects a BLANK screen. It is structurally unable to detect
a screen that is full and motionless -- and that is the defect this repo keeps
shipping: `b02` once closed on fourteen seconds of six unmoving arrows while the
voice made a claim about a range of values, and `b06`'s payoff frame was held
for twenty-five seconds across three sentences. Both passed every gate.

ffmpeg's own `freezedetect` is not usable here. It thresholds the mean absolute
difference over the whole frame, and these scenes are thin bright strokes on a
near-black field: a curve sweeping across a panel moves a few thousand pixels
out of 400k, so the mean difference sits below any threshold that does not also
fire on genuine stillness. Measured on chapterB1 it reported 22.8 s frozen
across a passage in which a number line visibly unrolls into a circle.

So the metric is the COUNT of changed pixels, not the mean change: a frame is
"still" when fewer than `--pixels` of its pixels differ from the previous frame
by more than `--delta`. That is invariant to how much of the frame the moving
object covers, which is the property freezedetect lacks.

Reported, not fatal. A deliberate pause on something worth inspecting is a good
frame to hold; the judgement about which is which belongs to the review, and
`RENDER_REVIEW_SPEC.md` section 10.2 keeps it a human pass. This tool only makes
sure nobody has to find them by scrubbing.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

import numpy as np

# Sampling rate for the comparison. High enough that a slow tracker sweep still
# shows movement between consecutive samples, low enough to stay cheap.
FPS = 5
# 320x180, not 160x90. At the smaller size a legitimately moving small object --
# a sample dot travelling across a shrunken panel -- covers about one pixel per
# sample and falls under any threshold that also rejects h264 noise, so the tool
# reported stillness that was really "the tool cannot see this". It is worth
# knowing that a viewer would struggle too, but that is a separate finding from
# "nothing was animated here", and the measurement must not conflate them.
WIDTH, HEIGHT = 320, 180


def frames(path: str) -> np.ndarray:
    """Every sampled frame as a small greyscale image."""
    cmd = [
        "ffmpeg", "-v", "error", "-i", path,
        "-vf", f"fps={FPS},scale={WIDTH}:{HEIGHT},format=gray",
        "-f", "rawvideo", "-",
    ]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (WIDTH * HEIGHT)
    return np.frombuffer(raw, np.uint8, n * WIDTH * HEIGHT).reshape(
        n, HEIGHT, WIDTH).astype(np.int16)


def still_runs(imgs: np.ndarray, delta: int, pixels: int, min_len: float):
    """Runs of consecutive sample intervals in which almost nothing changed."""
    moved = (np.abs(np.diff(imgs, axis=0)) > delta).sum(axis=(1, 2))
    out, start = [], None
    for i, count in enumerate(moved):
        if count < pixels:
            start = i if start is None else start
        elif start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(moved)))
    return [(a / FPS, b / FPS) for a, b in out if (b - a) / FPS >= min_len]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("videos", nargs="+")
    p.add_argument("--min", type=float, default=4.0,
                   help="shortest still stretch to report, in seconds")
    p.add_argument("--delta", type=int, default=6,
                   help="per-pixel greyscale change that counts as movement")
    p.add_argument("--pixels", type=int, default=12,
                   help="how many changed pixels a moving frame needs")
    args = p.parse_args()

    worst = 0.0
    for path in args.videos:
        runs = still_runs(frames(path), args.delta, args.pixels, args.min)
        name = path.rsplit("/", 1)[-1]
        if not runs:
            print(f"  ok     {name}")
            continue
        total = sum(b - a for a, b in runs)
        print(f"  STILL  {name}: {len(runs)} stretch(es), {total:.1f}s total")
        for a, b in runs:
            worst = max(worst, b - a)
            print(f"           {int(a)//60:02d}:{a % 60:05.2f} - "
                  f"{int(b)//60:02d}:{b % 60:05.2f}   ({b - a:.1f}s)")
    print(f"\nlongest still stretch: {worst:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
