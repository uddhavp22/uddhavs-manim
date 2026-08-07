"""Google Translate TTS. Port of manim_voiceover/services/gtts.py.

Free and needs no key, but it goes over the network and the voice is
noticeably robotic. Fine for drafts.

    .venv/bin/pip install gTTS
"""
from __future__ import annotations

from pathlib import Path

from voiceover.helper import remove_bookmarks
from voiceover.services.base import PathLike, SpeechService


class GTTSService(SpeechService):
    """SpeechService wrapping the gTTS library."""

    def __init__(self, lang: str = "en", tld: str = "com", **kwargs) -> None:
        """
        Args:
            lang: Language code, e.g. "en". See the Google Translate docs.
            tld: Top level domain of the Google Translate URL, which selects
                the accent — "com" is US, "co.uk" British, "com.au" Australian.
        """
        try:
            import gtts  # noqa: F401
        except ImportError:
            raise ImportError(
                "GTTSService needs gTTS. Install it with:\n"
                "    .venv/bin/pip install gTTS"
            )
        self.lang = lang
        self.tld = tld
        super().__init__(**kwargs)

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs,
    ) -> dict:
        from gtts import gTTS, gTTSError

        if cache_dir is None:
            cache_dir = self.cache_dir
        cache_dir = Path(cache_dir)

        input_text = remove_bookmarks(text)
        input_data = {"input_text": input_text, "service": "gtts"}

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"

        kwargs.setdefault("lang", self.lang)
        kwargs.setdefault("tld", self.tld)

        try:
            tts = gTTS(input_text, **kwargs)
            tts.save(str(cache_dir / audio_path))
        except gTTSError as e:
            raise Exception(
                f"gTTS gave an error: {e}\nEither you are not connected to the "
                f"internet, or lang={kwargs['lang']!r} / tld={kwargs['tld']!r} is invalid."
            )

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
