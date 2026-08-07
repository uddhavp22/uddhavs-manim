"""ElevenLabs TTS. Port of manim_voiceover/services/elevenlabs.py.

Upstream imports `generate`/`save`/`voices` from the `elevenlabs` package,
which is the pre-1.0 SDK surface. This talks to the documented REST endpoints
instead, so it does not depend on which SDK generation is installed.

Needs ELEVEN_API_KEY in the environment or in a .env file at the repo root.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from manim import logger as log

from voiceover.helper import remove_bookmarks
from voiceover.services.base import PathLike, SpeechService
from voiceover.services.env import require_api_key

API_ROOT = "https://api.elevenlabs.io/v1"


def _get_json(url: str, api_key: str) -> dict:
    request = urllib.request.Request(url, headers={"xi-api-key": api_key})
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def _error_message(e: urllib.error.HTTPError) -> str:
    """Pull ElevenLabs' human-readable reason out of an error response.

    Their failures are specific and actionable — a missing key scope, a tier
    restriction — but all of it lives in a nested `detail` object that is
    invisible if you only look at the status code.
    """
    body = e.read().decode(errors="replace")
    try:
        detail = json.loads(body)["detail"]
        message = detail.get("message", body)
        status = detail.get("status", "")
    except Exception:
        return f"{e.code}: {body[:300]}"

    hint = ""
    if status == "missing_permissions":
        hint = (
            "\nGrant that scope to the key at elevenlabs.io > Profile > API Keys, "
            "or pass voice_id= directly to skip the voice lookup entirely."
        )
    elif e.code == 402:
        hint = "\nThis is a subscription limit, not a configuration problem."
    return f"{e.code}: {message}{hint}"


class ElevenLabsService(SpeechService):
    """Speech service for the ElevenLabs API."""

    def __init__(
        self,
        voice_name: str | None = None,
        voice_id: str | None = None,
        model: str = "eleven_multilingual_v2",
        voice_settings: dict | None = None,
        output_format: str = "mp3_44100_128",
        transcription_model: str | None = None,
        **kwargs,
    ) -> None:
        """
        Args:
            voice_name: Voice name as shown in the ElevenLabs dashboard. Looked
                up against /v1/voices at construction time.
            voice_id: Used instead of voice_name if given.
            model: e.g. "eleven_multilingual_v2", "eleven_turbo_v2_5".
            voice_settings: Dict with `stability` and `similarity_boost`
                (both required if given), plus optional `style` and
                `use_speaker_boost`.
            output_format: See the ElevenLabs API reference. Higher bitrates
                need a paid tier.
            transcription_model: Whisper model for bookmark timing.
        """
        self.api_key = require_api_key("ELEVEN_API_KEY", "ElevenLabsService")
        self.model = model
        self.output_format = output_format

        if voice_settings is not None:
            missing = {"stability", "similarity_boost"} - set(voice_settings)
            if missing:
                raise KeyError(f"voice_settings is missing required keys: {sorted(missing)}")
        self.voice_settings = voice_settings

        self.voice_id = self._resolve_voice_id(voice_name, voice_id)
        super().__init__(transcription_model=transcription_model, **kwargs)

    def _resolve_voice_id(self, voice_name: str | None, voice_id: str | None) -> str:
        if voice_id:
            return voice_id

        try:
            available = _get_json(f"{API_ROOT}/voices", self.api_key)["voices"]
        except urllib.error.HTTPError as e:
            raise Exception(f"Could not list ElevenLabs voices — {_error_message(e)}")
        if not available:
            raise Exception("The ElevenLabs account has no voices available.")

        if voice_name:
            # ElevenLabs names its stock voices "Alice - Clear, Engaging
            # Educator", so an exact match on "Alice" finds nothing. Match the
            # part before the dash, case-insensitively, and fall back to an
            # exact match for custom voices whose names contain a dash.
            wanted = voice_name.strip().lower()

            def short_name(voice: dict) -> str:
                return voice.get("name", "").split(" - ")[0].strip().lower()

            for match in (
                lambda v: v.get("name", "").lower() == wanted,
                lambda v: short_name(v) == wanted,
                lambda v: short_name(v).startswith(wanted),
            ):
                found = [v for v in available if match(v)]
                if found:
                    if len(found) > 1:
                        log.info(
                            f"{voice_name!r} matched {len(found)} voices; using "
                            f"{found[0].get('name')!r}."
                        )
                    return found[0]["voice_id"]

            log.warning(
                f"Voice {voice_name!r} not found. Available: "
                f"{[v.get('name', '').split(' - ')[0] for v in available]}. "
                f"Defaulting to {available[0].get('name')!r}."
            )
        else:
            log.warning(
                "Neither voice_name nor voice_id was given. Defaulting to "
                f"{available[0].get('name')!r}."
            )
        return available[0]["voice_id"]

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
            "service": "elevenlabs",
            "config": {
                "model": self.model,
                "voice_id": self.voice_id,
                "voice_settings": self.voice_settings,
                "output_format": self.output_format,
            },
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"

        body: dict = {"text": input_text, "model_id": self.model}
        if self.voice_settings is not None:
            body["voice_settings"] = self.voice_settings

        query = urllib.parse.urlencode({"output_format": self.output_format})
        request = urllib.request.Request(
            f"{API_ROOT}/text-to-speech/{self.voice_id}?{query}",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
        )
        try:
            with urllib.request.urlopen(request) as response:
                (cache_dir / audio_path).write_bytes(response.read())
        except urllib.error.HTTPError as e:
            raise Exception(f"ElevenLabs refused the request — {_error_message(e)}")

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
