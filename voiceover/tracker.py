"""Tracks where a voiceover sits on the scene clock.

Direct port of manim_voiceover/tracker.py. One substitution:
`scipy.interpolate.interp1d` -> `np.interp`, which is the same piecewise linear
map but clamps at both ends instead of raising.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np

from manim import logger as log

from voiceover.audio import get_duration
from voiceover.helper import (
    BOOKMARK_CAPTURE_PATTERN,
    BOOKMARK_PATTERN,
    BOOKMARK_SPLIT_PATTERN,
    remove_bookmarks,
)

# Upstream uses 100ns ticks (inherited from the Azure TTS API) as the unit for
# audio_offset. Kept identical so cache files interoperate.
AUDIO_OFFSET_RESOLUTION = 10_000_000


class TimeInterpolator:
    """Maps a character offset in the script to a timestamp in the audio."""

    def __init__(self, word_boundaries: list[dict]) -> None:
        self.x = np.array([wb["text_offset"] for wb in word_boundaries], dtype=float)
        self.y = np.array(
            [wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION for wb in word_boundaries],
            dtype=float,
        )
        order = np.argsort(self.x, kind="stable")
        self.x = self.x[order]
        self.y = self.y[order]

    def interpolate(self, distance: float) -> float:
        return float(np.interp(distance, self.x, self.y))


class VoiceoverTracker:
    """Tracks the progress of a voiceover in a scene."""

    def __init__(self, scene, data: dict, cache_dir: str | Path) -> None:
        self.scene = scene
        self.data = data
        self.cache_dir = Path(cache_dir)
        self.duration = get_duration(self.cache_dir / data["final_audio"])

        last_t = scene.time
        if last_t is None:
            last_t = 0.0
        self.start_t = last_t
        self.end_t = last_t + self.duration

        # Upstream only processes bookmarks when the service reported word
        # boundaries, so `wait_until_bookmark` raises unless Whisper is
        # installed. Bookmarks are far more useful than that: if the script
        # contains any, fall back to assuming speech advances linearly through
        # the text. That is approximate, but for a single sentence it lands
        # within a few tenths of a second, and installing torch is a steep
        # price for that accuracy.
        if "word_boundaries" in self.data or re.search(
            BOOKMARK_PATTERN, self.data["input_text"]
        ):
            self._process_bookmarks()

    def _get_fallback_word_boundaries(self) -> list[dict]:
        """Dummy boundaries assuming text advances linearly through the audio."""
        input_text = remove_bookmarks(self.data["input_text"])
        return [
            {
                "audio_offset": 0,
                "text_offset": 0,
                "word_length": len(input_text),
                "text": self.data["input_text"],
                "boundary_type": "Word",
            },
            {
                "audio_offset": int(self.duration * AUDIO_OFFSET_RESOLUTION),
                "text_offset": len(input_text),
                "word_length": 1,
                "text": ".",
                "boundary_type": "Word",
            },
        ]

    def _process_bookmarks(self) -> None:
        self.bookmark_times: dict[str, float] = {}
        self.bookmark_distances: dict[str, int] = {}

        word_boundaries = self.data.get("word_boundaries")
        if not word_boundaries or len(word_boundaries) < 2:
            log.info(
                "No word-level timings for this voiceover; bookmarks will be "
                "placed by linear interpolation. Pass transcription_model='base' "
                "to the service for exact timings."
            )
            word_boundaries = self._get_fallback_word_boundaries()

        self.time_interpolator = TimeInterpolator(word_boundaries)

        net_text_len = len(remove_bookmarks(self.data["input_text"]))
        if "transcribed_text" in self.data:
            transcribed_text_len = len(self.data["transcribed_text"].strip())
        else:
            transcribed_text_len = net_text_len

        self.input_text = self.data["input_text"]
        self.content = ""

        for part in re.split(BOOKMARK_SPLIT_PATTERN, self.input_text):
            matched = re.match(BOOKMARK_CAPTURE_PATTERN, part)
            if matched:
                self.bookmark_distances[matched.group(1)] = len(self.content)
            else:
                self.content += part

        for mark, dist in self.bookmark_distances.items():
            # Rescale the offset into the transcript's coordinate system, since
            # a transcript rarely has the same character count as the script.
            scaled = dist * transcribed_text_len / net_text_len if net_text_len else 0
            self.bookmark_times[mark] = self.start_t + self.time_interpolator.interpolate(scaled)

    def get_remaining_duration(self, buff: float = 0.0) -> float:
        """Seconds of voiceover left to play from the scene's current time."""
        return max(self.end_t - float(self.scene.time) + buff, 0.0)

    def _check_bookmarks(self) -> None:
        if not hasattr(self, "bookmark_times"):
            raise Exception(
                "Word boundaries are required for timing with bookmarks. "
                "Either use a service that reports them natively (ElevenLabsService), "
                "or pass transcription_model='base' to enable Whisper transcription."
            )

    def time_until_bookmark(
        self,
        mark: str,
        buff: float = 0.0,
        limit: float | None = None,
    ) -> float:
        """Seconds from now until `mark` is spoken."""
        self._check_bookmarks()
        if mark not in self.bookmark_times:
            raise Exception("There is no <bookmark mark='%s' />" % mark)
        result = max(self.bookmark_times[mark] - float(self.scene.time) + buff, 0.0)
        if limit is not None:
            result = min(limit, result)
        return result
