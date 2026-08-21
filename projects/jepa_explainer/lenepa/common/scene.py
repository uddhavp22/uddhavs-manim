"""Voiceover-aware base scene for the LeNEPA segment.

ElevenLabs is the current preview voice only.  The text in ``scenes.py`` is the
source of truth and is intentionally written to be replaced by the author's
recording later without retiming the animation by hand.
"""

from __future__ import annotations

import os
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from manim import FadeOut, Group, config
from pydub import AudioSegment

from voiceover import VoiceoverScene
from voiceover.helper import remove_bookmarks
from voiceover.services.base import PathLike, SpeechService
from voiceover.services.elevenlabs import ElevenLabsService
from voiceover.services.say import SayService


VOICE = os.environ.get("LENEPA_VOICE", "draft")
DRAFT_VOICE = os.environ.get("LENEPA_DRAFT_VOICE", "Evan (Enhanced)")
ARCHER = "Fahco4VZzobUeiPqni1S"
ARCHER_SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}

ELEVEN_PRONUNCIATIONS = (
    (r"\bLeNEPA\b", "leh NEP uh"),
    (r"\bNEPA\b", "NEP uh"),
    (r"\bSIGReg\b", "sig reg"),
    (r"\bJEPA\b", "JEP uh"),
    (r"\bPTB-XL\b", "P T B X L"),
    (r"\bDiag\b", "die ag"),
    (r"\bAUROC\b", "A U rock"),
    (r"\bAUPRC\b", "A U P R C"),
    (r"\bUCR\b", "U C R"),
    (r"\bEMA\b", "E M A"),
    (r"\bz-hat\b", "zee hat"),
)


class TimingService(SpeechService):
    """Silent audio with speech-length timing for sandboxed draft renders."""

    def __init__(self, words_per_minute: int = 168, **kwargs) -> None:
        self.words_per_minute = words_per_minute
        super().__init__(**kwargs)

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs,
    ) -> dict:
        cache_dir = Path(cache_dir or self.cache_dir)
        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "lenepa-timing",
            "config": {"words_per_minute": self.words_per_minute},
        }
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached
        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"
        word_count = max(1, len(re.findall(r"[A-Za-z0-9']+", input_text)))
        duration_ms = int(60_000 * word_count / self.words_per_minute + 350)
        AudioSegment.silent(duration=duration_ms).export(cache_dir / audio_path, format="mp3")
        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }


class LenepaScene(VoiceoverScene):
    """Audio drives every beat; scene code supplies only visual choreography."""

    MAX_INSPECT = 2.2

    def setup(self):
        super().setup()
        if VOICE == "draft":
            service = SayService(voice=DRAFT_VOICE, rate=168)
        elif VOICE == "timing":
            service = TimingService(words_per_minute=168)
        elif VOICE == "eleven":
            service = ElevenLabsService(
                voice_id=ARCHER,
                voice_settings=ARCHER_SETTINGS,
                transcription_model="base",
            )
        else:
            raise ValueError(
                f"unknown LENEPA_VOICE={VOICE!r}; expected 'draft', "
                "'timing', or 'eleven'"
            )
        self.set_speech_service(service)

    def across(self, tracker, *animations, floor: float = 1.0,
               reserve: float = 0.0, **kwargs) -> None:
        run_time = max(floor, tracker.get_remaining_duration() - reserve)
        self.play(*animations, run_time=run_time, **kwargs)

    @contextmanager
    def voiceover(self, text: str | None = None, **kwargs) -> Generator:
        """Give ElevenLabs phonetics without leaking them into subtitles."""
        if text is None:
            raise ValueError("Please specify voiceover text.")
        spoken = text
        if VOICE == "eleven":
            kwargs.setdefault("subcaption", text)
            for pattern, replacement in ELEVEN_PRONUNCIATIONS:
                spoken = re.sub(pattern, replacement, spoken)
        with super().voiceover(text=spoken, **kwargs) as tracker:
            yield tracker

    def inspect(self, seconds: float = 1.0) -> None:
        self.wait(min(seconds, self.MAX_INSPECT))

    def clear_beat(self, run_time: float = 0.6) -> None:
        mobs = list(self.mobjects)
        if not mobs:
            return
        for mob in mobs:
            mob.clear_updaters(recursive=True)
        self.play(FadeOut(Group(*mobs)), run_time=run_time)
        self.wait(1 / config.frame_rate)
