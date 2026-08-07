#!/usr/bin/env python3
"""Find stretches where a rendered scene shows nothing.

Dead air is this project's recurring defect and no other gate can see it.
`narration_audit.py` reads the prose, which is fine; `preflight.py` resolves
names, which resolve; `facts.py` checks numbers, which are right. Meanwhile the
scene holds an empty frame for four and a half seconds with a voice talking over
it, and the only symptom is that the video "drags a bit".

That is what happened to b00 at rev 3: 52.5 s to 57.0 s, completely empty, past
every gate. It was found by measuring, not by watching, and this is the measurement.

How it works: a blank frame is UNIFORM. Its brightest pixel is the background,
so peak luminance equals mean luminance (measured: a solid #0C0E12 frame through
this project's h264 settings gives YMAX = YAVG = 28 exactly). Draw anything at
all and the two separate -- one thin grey axis puts YMAX at 143 against a mean
of 28.4, and text puts it at 180.

So the test is `YMAX - YAVG`, which needs no calibration: it is near zero for an
empty frame of any background colour, at any resolution, and large for any frame
with content. Two earlier attempts got this wrong and are worth recording, since
both looked reasonable:

  * Absolute mean, `YAVG <= floor + 0.2`. A whole number line plus seven dots
    plus a label lifts the mean of a 854x480 frame by 0.25 -- barely above
    encoder noise -- so sparse frames all read as empty. Three false positives.
  * Peak against a per-file minimum. A scene that is never empty has its floor
    set by an ordinary content frame, so the tolerance band then swallows half
    the scene. It reported 25 consecutive seconds of b06b as blank while the
    frames plainly had three panels and an equation on them.

Reports EMPTY frames only -- nothing drawn at all. Whether a frame that HAS
content earns its time is a different question (RENDER_REVIEW_SPEC.md section
10.2) and stays a human pass; see the note by frozen_runs().

Usage:
    python3 tools/dead_air.py videos/sigreg_explainer/chapterB/*/[A-Z]*.mp4
    python3 tools/dead_air.py --min 2.0 path/to/master.mp4

Exit status is 1 if any file has a dead stretch, so this can gate a build.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

# Sampling rate for the scan. 2 fps is enough: the shortest stretch worth
# reporting is about a second, and a finer grid costs decode time for nothing.
FPS = 2.0

# Peak-minus-mean below this is a frame with nothing on it. Zero in theory;
# 8 leaves room for encoder ringing and for a background that is not perfectly
# flat. It only has to separate 0 from 115.
FLAT = 8.0


TIME_RE = re.compile(r"pts_time:([0-9.]+)")
YMAX_RE = re.compile(r"YMAX=([0-9.]+)")
YAVG_RE = re.compile(r"YAVG=([0-9.]+)")


def luminance_series(path: pathlib.Path) -> list[tuple[float, float, float]]:
    """[(timestamp, peak luma, mean luma)] sampled at FPS."""
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path),
         "-vf", f"fps={FPS},signalstats,metadata=print:file=-",
         "-f", "null", "-"],
        capture_output=True, text=True)
    # metadata=print writes to stderr; ffmpeg's own errors land there too.
    out = proc.stdout + proc.stderr
    series, t, peak = [], None, None
    for line in out.splitlines():
        m = TIME_RE.search(line)
        if m:
            t = float(m.group(1))
            continue
        m = YMAX_RE.search(line)
        if m:
            peak = float(m.group(1))
            continue
        m = YAVG_RE.search(line)
        if m and t is not None and peak is not None:
            series.append((t, peak, float(m.group(1))))
            t = peak = None
    return series


def _runs(series, predicate, min_seconds: float):
    """Maximal runs of samples satisfying `predicate`, as (start, end).

    Each sample stands for the 1/FPS window that follows it, so a run of one
    sample lasts 1/FPS -- not zero. Measuring `last - start` instead understates
    every run by one interval and silently discards single-sample runs, which is
    how the first version of this file passed a clip that was blank end to end.
    """
    step = 1.0 / FPS
    runs, start, last = [], None, None
    for sample in series:
        if predicate(sample):
            if start is None:
                start = sample[0]
            last = sample[0]
        elif start is not None:
            if last + step - start >= min_seconds:
                runs.append((start, last + step))
            start = None
    if start is not None and last + step - start >= min_seconds:
        runs.append((start, last + step))
    return runs


def _is_empty(sample) -> bool:
    """A frame whose brightest pixel is the background: nothing is drawn."""
    _, peak, mean = sample
    return peak - mean <= FLAT


def dead_runs(series, min_seconds: float):
    """Runs where nothing at all is drawn."""
    return _runs(series, _is_empty, min_seconds)


# There was a third level here -- "sparse", meaning something is drawn but
# almost nothing, aimed at cases like b08's bare axes under narration. Every
# threshold tried flagged frames with three full panels on them, because "how
# much is on screen" does not reduce to mean luminance: a dense dark diagram and
# a nearly empty frame measure the same. It is deleted rather than shipped
# noisy. Judging whether a frame earns its time is RENDER_REVIEW_SPEC.md
# section 10.2, and that stays a human pass.


def frozen_runs(series, min_seconds: float):
    """Runs where mean luminance does not change at all.

    A crude proxy for a held frame: if nothing anywhere in the picture changed
    brightness across a second, very little moved. It has real false positives
    -- a slow pan of equal-brightness content reads as frozen -- so it is
    advisory and off by default.
    """
    runs, start, last, prev = [], None, None, None
    for t, _, y in series:
        if prev is not None and abs(y - prev) < 1e-6:
            if start is None:
                start = last
        elif start is not None:
            if last - start >= min_seconds:
                runs.append((start, last))
            start = None
        prev, last = y, t
    if start is not None and last - start >= min_seconds:
        runs.append((start, last))
    return runs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+", type=pathlib.Path)
    ap.add_argument("--min", type=float, default=1.0,
                    help="shortest dead stretch to report, seconds (default 1.0)")
    ap.add_argument("--frozen", action="store_true",
                    help="also report unchanging (not just empty) stretches")
    args = ap.parse_args()

    bad = False
    for path in args.videos:
        if not path.exists():
            print(f"missing: {path}", file=sys.stderr)
            bad = True
            continue
        series = luminance_series(path)
        if not series:
            print(f"{path.name}: could not read frames", file=sys.stderr)
            bad = True
            continue

        empty = dead_runs(series, args.min)
        frozen = frozen_runs(series, args.min) if args.frozen else []

        if not (empty or frozen):
            print(f"  ok     {path.name}")
            continue
        for a, b in empty:
            print(f"  EMPTY  {path.name}  {a:6.1f} .. {b:6.1f}  ({b - a:.1f}s)")
            bad = True
        for a, b in frozen:
            print(f"  still  {path.name}  {a:6.1f} .. {b:6.1f}  ({b - a:.1f}s)")

    if bad:
        print("\nRESULT: dead air found. A frame with nothing on it under "
              "narration is RENDER_REVIEW_SPEC.md section 10.2.")
        return 1
    print("\nRESULT: no dead air.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
