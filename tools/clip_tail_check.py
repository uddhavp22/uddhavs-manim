#!/usr/bin/env python3
"""Flag voiceover clips that carry speech after their last transcribed word.

ElevenLabs occasionally appends a short spurious utterance after a sentence
(Whisper hears it as a stray word such as "Kasi"). It sits after a silent
gap, at full speech level, and would play in the video. This scans clips in
media/voiceovers whose cache entry matches a text fragment (or every clip
newer than --days) and reports any with a burst of energy after silence
following the last word.

    python3 tools/clip_tail_check.py --days 3
    python3 tools/clip_tail_check.py --grep "Gauss-ian"
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

import numpy as np

CACHE = "media/voiceovers/cache.json"
SR = 16000


def decode(path: str) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
         "-ar", str(SR), "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.float32)


def tail_burst(x: np.ndarray, last_word_s: float) -> tuple[bool, str]:
    """True if, after the last word, there is >=0.15 s of near-silence
    followed by a window at speech level."""
    dur = len(x) / SR
    body = x[int(0.5 * SR):max(int(0.5 * SR) + SR, int((last_word_s) * SR))]
    speech = float(np.sqrt(np.mean(body ** 2)) + 1e-9)
    step = 0.1
    seen_silence = False
    t = last_word_s + 0.3
    while t + step <= dur:
        seg = x[int(t * SR):int((t + step) * SR)]
        r = float(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        db = 20 * np.log10(r / speech)
        if db < -25:
            seen_silence = True
        elif seen_silence and db > -8:
            return True, f"burst at {t:.1f}s ({db:+.0f} dB) after silence; clip {dur:.1f}s"
        t += step
    return False, f"clean; clip {dur:.1f}s"


def normalise(text: str) -> list[str]:
    import re
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", text.lower()).split() if w]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=float, default=None)
    parser.add_argument("--grep", default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    cache = json.load(open(CACHE))
    items = cache if isinstance(cache, list) else list(cache.values())
    flagged = 0
    checked = 0
    cutoff = time.time() - 86400 * args.days if args.days else None
    for it in items:
        if not isinstance(it, dict):
            continue
        path = os.path.join("media/voiceovers", it.get("original_audio") or it.get("final_audio") or "")
        if not path.endswith(".mp3") or not os.path.exists(path):
            continue
        if cutoff and os.path.getmtime(path) < cutoff:
            continue
        if args.grep and args.grep not in it.get("input_text", ""):
            continue
        boundaries = it.get("word_boundaries") or []
        if not boundaries:
            continue
        checked += 1
        # 1. A trailing transcribed word that the passage never contained.
        heard = normalise(it.get("transcribed_text", ""))
        said = set(normalise(it.get("input_text", "")))
        stray = [w for w in heard[-3:] if w not in said and not w.isdigit()]
        # 2. Energy after a silence that follows the last word the passage
        # does contain (the burst itself is usually transcribed as the
        # stray word, so measure from the last genuine one).
        x = decode(path)
        dur = len(x) / SR
        offsets = [w["audio_offset"] for w in boundaries]
        # Offsets have been seen in seconds, milliseconds and 100 ns ticks;
        # pick the unit that keeps the last word inside the clip.
        scale = next(
            (u for u in (1e7, 1e4, 1e3, 1.0) if max(offsets) / u <= dur + 0.5),
            1e7,
        )
        genuine = [
            w for w in boundaries
            if any(tok in said for tok in normalise(w["text"]))
        ]
        last_start = (genuine[-1] if genuine else boundaries[-1])["audio_offset"] / scale
        burst, detail = tail_burst(x, last_start)
        if burst:
            flagged += 1
            print(f"  FLAG  {os.path.basename(path)}\n        {detail}; stray {stray}"
                  f"\n        heard: ...{it.get('transcribed_text','')[-90:]}")
        elif stray and args.verbose:
            print(f"  note  {os.path.basename(path)}: stray {stray} (no burst)")
    print(f"{checked} clips checked, {flagged} flagged")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
