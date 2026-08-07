"""Record your own narration from the microphone, one block at a time.

Same idea as manim_voiceover/services/recorder, with a different engine:
upstream drives PyAudio (which needs a portaudio build) plus pynput. This
uses ffmpeg's avfoundation input and afplay for review, both of which are
already present on this machine.

Flow per voiceover block: print the line, record until you press Enter, play
it back, then [Enter] to keep, `r` to redo, `s` to skip the playback.
"""
from __future__ import annotations

import re
import shutil
import subprocess as sp
from pathlib import Path

from voiceover.audio import to_mp3
from voiceover.helper import msg_box, remove_bookmarks
from voiceover.services.base import PathLike, SpeechService


def list_input_devices() -> list[tuple[str, str]]:
    """Return [(index, name)] for avfoundation audio input devices."""
    # ffmpeg prints the device list to stderr and exits non-zero by design.
    result = sp.run(
        ["ffmpeg", "-hide_banner", "-f", "avfoundation", "-list_devices", "true", "-i", ""],
        capture_output=True,
        text=True,
    )
    output = result.stderr
    audio_section = output.split("AVFoundation audio devices:")
    if len(audio_section) < 2:
        return []
    return re.findall(r"\[(\d+)\]\s+(.+)", audio_section[1])


class RecorderService(SpeechService):
    """Speech service that records from a microphone during rendering."""

    def __init__(
        self,
        device_index: int | None = None,
        channels: int = 1,
        rate: int = 44100,
        transcription_model: str | None = None,
        **kwargs,
    ) -> None:
        """
        Args:
            device_index: avfoundation audio device index. Prompted for on the
                first recording if not given.
            channels: 1 for mono, 2 for stereo.
            rate: Sample rate in Hz.
            transcription_model: Whisper model for bookmark timing. Without it,
                bookmarks in recorded narration fall back to linear timing.
        """
        for tool in ("ffmpeg", "afplay"):
            if shutil.which(tool) is None:
                raise RuntimeError(f"RecorderService requires `{tool}` on PATH.")
        self.device_index = device_index
        self.channels = channels
        self.rate = rate
        super().__init__(transcription_model=transcription_model, **kwargs)

    def _ensure_device(self) -> int:
        if self.device_index is not None:
            return self.device_index

        devices = list_input_devices()
        if not devices:
            raise RuntimeError(
                "No avfoundation audio input devices found. Check that the "
                "terminal has microphone permission in System Settings > "
                "Privacy & Security > Microphone."
            )

        print("\nAvailable audio input devices:")
        for index, name in devices:
            print(f"  [{index}] {name}")

        while True:
            choice = input("Device index to record from: ").strip()
            if choice in {index for index, _ in devices}:
                self.device_index = int(choice)
                return self.device_index
            print("Not one of the listed indices.")

    def _record_once(self, output_path: Path) -> None:
        """Record until the user presses Enter."""
        command = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "avfoundation",
            "-ac", str(self.channels),
            "-ar", str(self.rate),
            "-i", f":{self.device_index}",
            str(output_path),
        ]
        process = sp.Popen(command, stdin=sp.PIPE)
        try:
            input("  ● Recording — press Enter to stop. ")
        finally:
            # 'q' asks ffmpeg to finalize the container rather than truncate it.
            try:
                process.communicate(input=b"q", timeout=10)
            except sp.TimeoutExpired:
                process.terminate()
                process.wait()

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
            # Bookmarks are stripped from the cache key so that moving a
            # bookmark does not force you to re-record the line.
            "input_text": input_text,
            "service": "recorder",
            "config": {"channels": self.channels, "rate": self.rate},
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"
        wav_path = cache_dir / (Path(audio_path).stem + ".wav")

        self._ensure_device()
        print("\n" + msg_box("Voiceover:\n\n" + input_text))

        while True:
            input("  Press Enter to start recording. ")
            self._record_once(wav_path)

            choice = input("  [Enter] keep · [r] redo · [s] skip playback: ").strip().lower()
            if choice == "r":
                continue
            if choice != "s":
                sp.run(["afplay", str(wav_path)])
                choice = input("  [Enter] keep · [r] redo: ").strip().lower()
                if choice == "r":
                    continue
            break

        to_mp3(wav_path, cache_dir / audio_path)
        wav_path.unlink(missing_ok=True)

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
