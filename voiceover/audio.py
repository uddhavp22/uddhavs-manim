"""Audio duration and tempo helpers.

Upstream manim-voiceover uses mutagen for durations and pysox for tempo
changes. Both are replaced here with pydub (declared directly in
pyproject.toml — CE's own file writer uses PyAV, not pydub) and ffmpeg.
"""
from __future__ import annotations

import os
import subprocess as sp
from pathlib import Path

from pydub import AudioSegment

PathLike = str | os.PathLike


def get_duration(path: PathLike) -> float:
    """Duration of an audio file in seconds.

    pydub reads the container metadata via ffmpeg, so this covers wav/mp3/m4a
    alike — upstream needed a separate mutagen branch per format.
    """
    return AudioSegment.from_file(str(path)).duration_seconds


def adjust_speed(input_path: PathLike, output_path: PathLike, tempo: float) -> None:
    """Re-time audio without changing pitch, via ffmpeg's atempo filter.

    atempo only accepts 0.5–2.0 per instance, so factors outside that range
    are decomposed into a chain.
    """
    if tempo <= 0:
        raise ValueError(f"tempo must be positive, got {tempo}")

    factors: list[float] = []
    remaining = tempo
    while remaining > 2.0:
        factors.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        factors.append(0.5)
        remaining /= 0.5
    factors.append(remaining)

    filter_arg = ",".join(f"atempo={f:.6f}" for f in factors)
    command = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(input_path),
        "-filter:a", filter_arg,
        str(output_path),
    ]
    sp.run(command, check=True)


def to_mp3(input_path: PathLike, output_path: PathLike | None = None, bitrate: str = "192k") -> Path:
    """Transcode any ffmpeg-readable audio file to mp3."""
    if output_path is None:
        output_path = Path(input_path).with_suffix(".mp3")
    AudioSegment.from_file(str(input_path)).export(
        str(output_path), format="mp3", bitrate=bitrate
    )
    return Path(output_path)
