"""Background music beds with automatic ducking under narration.

Not part of upstream manim-voiceover. The scene already knows exactly when
every voiceover starts and ends, so the music can be attenuated over precisely
those windows — no sidechain compressor guessing at where the speech is, and
no gain automation to draw by hand.

The result: music sits quietly under narration and comes back up in the gaps,
which is what makes a pause feel deliberate rather than empty.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pydub import AudioSegment

# Music is attenuated to this much below its resting level while someone is
# talking. -8 dB is roughly "clearly still there, never competing".
DEFAULT_DUCK_DB = -8.0
# Resting level under narration. Music mastered for listening is far too loud
# as a bed; this is the usual starting point for spoken-word content.
DEFAULT_GAIN_DB = -22.0
# Ramp in/out of a duck. Shorter sounds like a pumping compressor, longer and
# the music is still fading down when the sentence has started.
DEFAULT_RAMP_MS = 400


@dataclass
class MusicCue:
    """One music bed scheduled onto the scene timeline."""
    path: Path
    gain: float = DEFAULT_GAIN_DB
    duck: float = DEFAULT_DUCK_DB
    ramp_ms: int = DEFAULT_RAMP_MS
    fade_in: float = 1.5
    fade_out: float = 3.0
    loop: bool = True
    start: float = 0.0
    end: float | None = None


def merge_intervals(intervals: list[tuple[float, float]], pad: float = 0.0) -> list[tuple[float, float]]:
    """Sort, pad and coalesce overlapping (start, end) pairs."""
    if not intervals:
        return []
    padded = sorted((max(0.0, s - pad), e + pad) for s, e in intervals)
    merged = [padded[0]]
    for start, end in padded[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def duck_segment(
    bed: AudioSegment,
    intervals: list[tuple[float, float]],
    duck_db: float,
    ramp_ms: int,
) -> AudioSegment:
    """Attenuate `bed` by `duck_db` over each interval, with ramped edges.

    Intervals are in seconds and must already be merged. The bed is rebuilt by
    concatenating slices rather than overlaying, so gain is exact rather than
    the result of summing correlated signals.
    """
    if not intervals or duck_db == 0:
        return bed

    total_ms = len(bed)
    pieces: list[AudioSegment] = []
    cursor = 0

    for start_s, end_s in intervals:
        start_ms = max(0, min(total_ms, int(start_s * 1000)))
        end_ms = max(0, min(total_ms, int(end_s * 1000)))
        if end_ms <= cursor:
            continue

        ramp_start = max(cursor, start_ms - ramp_ms)
        if ramp_start > cursor:
            pieces.append(bed[cursor:ramp_start])

        down = bed[ramp_start:start_ms]
        if len(down) > 0:
            pieces.append(down.fade(from_gain=0.0, to_gain=duck_db, start=0, duration=len(down)))

        held = bed[max(start_ms, ramp_start):end_ms]
        if len(held) > 0:
            pieces.append(held.apply_gain(duck_db))

        ramp_end = min(total_ms, end_ms + ramp_ms)
        up = bed[end_ms:ramp_end]
        if len(up) > 0:
            pieces.append(up.fade(from_gain=duck_db, to_gain=0.0, start=0, duration=len(up)))

        cursor = ramp_end

    if cursor < total_ms:
        pieces.append(bed[cursor:])

    if not pieces:
        return bed
    result = pieces[0]
    for piece in pieces[1:]:
        result += piece
    return result


def build_bed(cue: MusicCue, scene_duration: float, narration: list[tuple[float, float]]) -> AudioSegment:
    """Render one MusicCue into a full-length, ducked, faded AudioSegment."""
    track = AudioSegment.from_file(str(cue.path))

    end = scene_duration if cue.end is None else min(cue.end, scene_duration)
    span = max(0.0, end - cue.start)
    if span <= 0:
        return AudioSegment.silent(0)
    span_ms = int(span * 1000)

    if cue.loop and len(track) < span_ms:
        # +1 so integer division never leaves the tail short.
        track = track * (span_ms // len(track) + 1)
    bed = track[:span_ms]

    bed = bed.apply_gain(cue.gain)

    # Narration times are absolute; the bed starts at cue.start.
    relative = [(s - cue.start, e - cue.start) for s, e in narration if e > cue.start and s < end]
    bed = duck_segment(bed, merge_intervals(relative), cue.duck, cue.ramp_ms)

    if cue.fade_in > 0:
        bed = bed.fade_in(min(int(cue.fade_in * 1000), len(bed)))
    if cue.fade_out > 0:
        bed = bed.fade_out(min(int(cue.fade_out * 1000), len(bed)))

    return bed
