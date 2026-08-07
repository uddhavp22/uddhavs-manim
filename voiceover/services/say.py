"""macOS `say` speech service.

Not part of upstream manim-voiceover. It exists because it is the only
backend that needs no API key, no network, and no pip install on this
machine — which makes it the right default for drafting timings before
committing to a paid voice.

    say -v '?'      # list installed voices
"""
from __future__ import annotations

import shutil
import subprocess as sp
from pathlib import Path

from voiceover.audio import to_mp3
from voiceover.helper import remove_bookmarks
from voiceover.services.base import PathLike, SpeechService


class SayService(SpeechService):
    """Speech service backed by the macOS `say` command."""

    def __init__(
        self,
        voice: str | None = None,
        rate: int | None = None,
        **kwargs,
    ) -> None:
        """
        Args:
            voice: A voice name from `say -v '?'`, e.g. "Samantha". None uses
                the system default voice.
            rate: Words per minute. macOS defaults to about 175.
        """
        if shutil.which("say") is None:
            raise RuntimeError("SayService requires the macOS `say` command.")
        self.voice = voice
        self.rate = rate
        super().__init__(**kwargs)

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs,
    ) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir
        cache_dir = Path(cache_dir)

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "say",
            "config": {"voice": self.voice, "rate": self.rate},
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"

        # `say` writes AIFF; everything downstream assumes mp3.
        aiff_path = cache_dir / (Path(audio_path).stem + ".aiff")
        command = ["say"]
        if self.voice:
            command += ["-v", self.voice]
        if self.rate:
            command += ["-r", str(self.rate)]
        command += ["-o", str(aiff_path), input_text]

        try:
            sp.run(command, check=True, capture_output=True)
        except sp.CalledProcessError as e:
            raise Exception(
                f"`say` failed: {e.stderr.decode(errors='replace').strip()}\n"
                f"If the voice name is wrong, list valid ones with: say -v '?'"
            )

        to_mp3(aiff_path, cache_dir / audio_path)
        aiff_path.unlink(missing_ok=True)

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
