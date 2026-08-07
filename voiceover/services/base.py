"""SpeechService: the abstract base every TTS/recording backend implements.

Port of manim_voiceover/services/base.py. The cache file format is unchanged,
so a `voiceovers/cache.json` produced here is readable by upstream and vice
versa.
"""
from __future__ import annotations

import hashlib
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

from manim import config, logger as log

from voiceover.audio import adjust_speed
from voiceover.helper import remove_bookmarks, slugify
from voiceover.tracker import AUDIO_OFFSET_RESOLUTION

PathLike = str | os.PathLike

DEFAULT_VOICEOVER_CACHE_DIR = "voiceovers"
DEFAULT_VOICEOVER_CACHE_JSON_FILENAME = "cache.json"


def timestamps_to_word_boundaries(segments) -> list[dict]:
    """Convert Whisper-style [{words: [{word, start}]}] into word boundaries."""
    word_boundaries: list[dict] = []
    current_text_offset = 0
    for segment in segments:
        for dict_ in segment["words"]:
            word = dict_["word"]
            word_boundaries.append({
                "audio_offset": int(dict_["start"] * AUDIO_OFFSET_RESOLUTION),
                "text_offset": current_text_offset,
                "word_length": len(word),
                "text": word,
                "boundary_type": "Word",
            })
            current_text_offset += len(word)
    return word_boundaries


def append_to_json_file(json_file: PathLike, data: dict) -> None:
    json_path = Path(json_file)
    if not json_path.exists():
        json_path.write_text(json.dumps([data], indent=2))
        return

    json_data = json.loads(json_path.read_text())
    if not isinstance(json_data, list):
        raise ValueError(f"{json_path} should contain a JSON list")
    json_data.append(data)
    json_path.write_text(json.dumps(json_data, indent=2))


class SpeechService(ABC):
    """Abstract base class for a speech service."""

    def __init__(
        self,
        global_speed: float = 1.00,
        cache_dir: PathLike | None = None,
        transcription_model: str | None = None,
        transcription_kwargs: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Args:
            global_speed: Playback tempo multiplier applied to every clip.
            cache_dir: Where audio and cache.json live. Defaults to
                `<media_dir>/voiceovers`.
            transcription_model: Whisper model name for word-level timing.
                Requires `pip install stable-whisper`. None disables it, in
                which case bookmarks fall back to linear interpolation.
            transcription_kwargs: Extra kwargs forwarded to `transcribe()`.
        """
        self.global_speed = global_speed

        if cache_dir is not None:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(config.media_dir) / DEFAULT_VOICEOVER_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.transcription_model: str | None = None
        self._whisper_model = None
        self.set_transcription(
            model=transcription_model,
            kwargs=transcription_kwargs or {},
        )

        self.additional_kwargs = kwargs

    # -- caching ---------------------------------------------------------

    @property
    def cache_json_path(self) -> Path:
        return self.cache_dir / DEFAULT_VOICEOVER_CACHE_JSON_FILENAME

    def get_cached_result(self, input_data: dict, cache_dir: PathLike) -> dict | None:
        json_path = Path(cache_dir) / DEFAULT_VOICEOVER_CACHE_JSON_FILENAME
        if not json_path.exists():
            return None
        try:
            entries = json.loads(json_path.read_text())
        except json.JSONDecodeError:
            log.warning(f"Could not parse {json_path}, ignoring the voiceover cache.")
            return None

        for entry in entries:
            if entry.get("input_data") != input_data:
                continue
            # global_speed lives on the service rather than in input_data (which
            # is kept byte-compatible with upstream's cache format), so it has to
            # be matched separately. Without this, changing global_speed would
            # keep returning the previous speed's audio.
            if entry.get("global_speed", 1.0) != self.global_speed:
                continue
            # A cache hit whose audio has been deleted is not a hit.
            audio = entry.get("final_audio") or entry.get("original_audio")
            if audio and not (Path(cache_dir) / audio).exists():
                continue
            # Flag consumed by _wrap_generate_from_text, which must not redo
            # the speed adjustment already baked into this entry.
            return {**entry, "_cached": True}
        return None

    def get_audio_basename(self, data: dict) -> str:
        data_hash = hashlib.sha256(json.dumps(data).encode("utf-8")).hexdigest()
        slug = slugify(remove_bookmarks(data["input_text"]), max_length=50)
        return f"{slug}-{data_hash[:8]}"

    # -- transcription ---------------------------------------------------

    def set_transcription(self, model: str | None = None, kwargs: dict | None = None) -> None:
        """Set the Whisper model used to recover word-level timings."""
        if kwargs is None:
            kwargs = {}
        if model != self.transcription_model:
            if model is not None:
                try:
                    import stable_whisper
                except ImportError:
                    raise ImportError(
                        # The import name and the distribution name differ: the
                        # module is stable_whisper, the package on PyPI is
                        # stable-ts. Naming the wrong one here costs whoever
                        # hits this a resolver error instead of a fix.
                        "Word-level timing needs stable-ts. Install it with:\n"
                        "    uv pip install --python .venv/bin/python stable-ts\n"
                        "Or drop transcription_model= to use linear bookmark timing."
                    )
                self._whisper_model = stable_whisper.load_model(model)
            else:
                self._whisper_model = None

        self.transcription_model = model
        self.transcription_kwargs = kwargs

    # -- main entry point ------------------------------------------------

    def _wrap_generate_from_text(self, text: str, **kwargs) -> dict:
        # Collapse newlines and runs of spaces so that cache keys are stable
        # against reflowing the script in the source file.
        text = " ".join(text.split())
        path = kwargs.pop("path", None)

        dict_ = self.generate_from_text(text, cache_dir=None, path=path, **kwargs)
        original_audio = dict_["original_audio"]

        # The cache key is the bookmark-STRIPPED text, deliberately: moving a
        # bookmark does not change a syllable of the audio, so it must not
        # re-spend the TTS budget. But `VoiceoverTracker` reads bookmark
        # positions out of `input_text`, and a cache hit returns whatever
        # bookmarks that entry happened to be written with. Editing only the
        # bookmarks in a passage therefore either silently timed them at their
        # OLD positions or, if a name had changed, raised
        # "There is no <bookmark mark='...'/>" from inside the render -- twenty
        # minutes in, with no hint that a stale cache entry was responsible.
        #
        # Overwrite with what this scene actually asked for. Placed before the
        # `_cached` early return so it covers the hit and the miss alike.
        dict_["input_text"] = text

        if dict_.pop("_cached", False):
            # Everything below (transcription, tempo adjustment, boundary
            # rescaling) is already reflected in the stored entry. Redoing it
            # would divide the audio offsets by global_speed a second time.
            dict_.setdefault("final_audio", original_audio)
            return dict_

        if "word_boundaries" not in dict_ and self._whisper_model is not None:
            transcription_result = self._whisper_model.transcribe(
                str(self.cache_dir / original_audio), **self.transcription_kwargs
            )
            log.info("Transcription: " + transcription_result.text)
            dict_["word_boundaries"] = timestamps_to_word_boundaries(
                transcription_result.segments_to_dicts()
            )
            dict_["transcribed_text"] = transcription_result.text

        self.audio_callback(original_audio, dict_, **kwargs)

        if self.global_speed != 1:
            stem, ext = os.path.splitext(original_audio)
            # The speed goes in the filename too, or two different speeds of the
            # same line would write over each other on disk.
            speed_tag = f"{self.global_speed:g}".replace(".", "_")
            adjusted_path = f"{stem}_adjusted_{speed_tag}{ext}"
            adjust_speed(
                self.cache_dir / original_audio,
                self.cache_dir / adjusted_path,
                self.global_speed,
            )
            dict_["final_audio"] = adjusted_path
            for word_boundary in dict_.get("word_boundaries", []):
                word_boundary["audio_offset"] = int(
                    word_boundary["audio_offset"] / self.global_speed
                )
        else:
            dict_["final_audio"] = dict_["original_audio"]

        dict_["global_speed"] = self.global_speed
        append_to_json_file(self.cache_json_path, dict_)
        return dict_

    @abstractmethod
    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs,
    ) -> dict:
        """Synthesize `text` and return a dict with at least:

        input_text:     the original text, bookmarks included
        input_data:     the dict used as the cache key
        original_audio: audio filename, relative to cache_dir

        Optionally `word_boundaries` if the service reports timings natively.
        """
        raise NotImplementedError

    def audio_callback(self, audio_path: str, data: dict, **kwargs) -> None:
        """Hook called once audio exists on disk. Override for e.g. denoising."""
        pass
