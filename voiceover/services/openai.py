"""OpenAI TTS. Port of manim_voiceover/services/openai.py.

Upstream calls the `openai` SDK. This talks to the REST endpoint directly
through the standard library, so the service does not break when the SDK
changes its surface between major versions.

Needs OPENAI_API_KEY in the environment or in a .env file at the repo root.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from voiceover.helper import remove_bookmarks
from voiceover.services.base import PathLike, SpeechService
from voiceover.services.env import require_api_key

ENDPOINT = "https://api.openai.com/v1/audio/speech"


class OpenAIService(SpeechService):
    """Speech service for the OpenAI text-to-speech API."""

    def __init__(
        self,
        voice: str = "alloy",
        model: str = "tts-1-hd",
        transcription_model: str | None = None,
        **kwargs,
    ) -> None:
        """
        Args:
            voice: alloy, echo, fable, onyx, nova or shimmer.
            model: "tts-1-hd" (upstream's default), "tts-1" for lower latency,
                or "gpt-4o-mini-tts" for the newer, steerable model.
            transcription_model: Whisper model for bookmark timing. Upstream
                defaults this to "base"; here it is off unless you ask, since
                stable-whisper pulls in torch.
        """
        self.voice = voice
        self.model = model
        super().__init__(transcription_model=transcription_model, **kwargs)

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

        speed = kwargs.get("speed", 1.0)
        if not 0.25 <= speed <= 4.0:
            raise ValueError("The speed must be between 0.25 and 4.0.")

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "openai",
            "config": {"voice": self.voice, "model": self.model, "speed": speed},
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"

        api_key = require_api_key("OPENAI_API_KEY", "OpenAIService")
        payload = json.dumps({
            "model": self.model,
            "voice": self.voice,
            "input": input_text,
            "speed": speed,
            "response_format": "mp3",
        }).encode("utf-8")

        request = urllib.request.Request(
            ENDPOINT,
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request) as response:
                (cache_dir / audio_path).write_bytes(response.read())
        except urllib.error.HTTPError as e:
            raise Exception(
                f"OpenAI TTS returned {e.code}: {e.read().decode(errors='replace')}"
            )

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
