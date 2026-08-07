"""Smoke-test a speech service without rendering a scene.

    PYTHONPATH=. .venv/bin/python -m voiceover.check say --voice Samantha
    PYTHONPATH=. .venv/bin/python -m voiceover.check elevenlabs --voice-name Adam
    PYTHONPATH=. .venv/bin/python -m voiceover.check say --transcribe base

Generates one clip, reports its duration, resolves any bookmarks, and plays it
back. Useful for confirming an API key works before committing a render to it.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess as sp
import sys
from pathlib import Path

DEFAULT_TEXT = (
    "First we <bookmark mark='spin'/>rotate the square, "
    "and then we <bookmark mark='grow'/>scale it up."
)


def build_service(name: str, args: argparse.Namespace):
    common = {"cache_dir": args.cache_dir, "global_speed": args.speed}
    if args.transcribe:
        common["transcription_model"] = args.transcribe

    if name == "say":
        from voiceover.services.say import SayService
        return SayService(voice=args.voice, rate=args.rate, **common)
    if name == "gtts":
        from voiceover.services.gtts import GTTSService
        return GTTSService(**common)
    if name == "openai":
        from voiceover.services.openai import OpenAIService
        return OpenAIService(voice=args.voice or "alloy", **common)
    if name == "elevenlabs":
        from voiceover.services.elevenlabs import ElevenLabsService
        return ElevenLabsService(voice_name=args.voice_name, voice_id=args.voice_id, **common)
    if name == "recorder":
        from voiceover.services.recorder import RecorderService
        return RecorderService(**common)
    raise SystemExit(f"Unknown service: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", choices=["say", "gtts", "openai", "elevenlabs", "recorder"])
    parser.add_argument("--text", default=DEFAULT_TEXT)
    parser.add_argument("--voice", default=None, help="say/openai voice name")
    parser.add_argument("--voice-name", default=None, help="elevenlabs voice name")
    parser.add_argument("--voice-id", default=None, help="elevenlabs voice id")
    parser.add_argument("--rate", type=int, default=None, help="say words per minute")
    parser.add_argument("--speed", type=float, default=1.0, help="global_speed")
    parser.add_argument("--transcribe", default=None, help="whisper model, e.g. base")
    parser.add_argument("--cache-dir", default="media/voiceovers")
    parser.add_argument("--no-play", action="store_true")
    args = parser.parse_args()

    service = build_service(args.service, args)
    data = service._wrap_generate_from_text(args.text)

    audio = Path(service.cache_dir) / data["final_audio"]

    # Import here so the tracker's scene-clock dependency stays optional.
    from voiceover.tracker import VoiceoverTracker

    class StubScene:
        time = 0.0

    tracker = VoiceoverTracker(StubScene(), data, service.cache_dir)

    print(f"\n  service   {args.service}")
    print(f"  audio     {audio}")
    print(f"  duration  {tracker.duration:.3f}s")
    print(f"  timings   {'whisper' if 'word_boundaries' in data else 'linear (estimated)'}")

    if getattr(tracker, "bookmark_times", None):
        print("  bookmarks")
        for mark, t in sorted(tracker.bookmark_times.items(), key=lambda kv: kv[1]):
            print(f"    {mark:<10} {t:6.3f}s")

    if not args.no_play and shutil.which("afplay"):
        print("\n  playing...")
        sp.run(["afplay", str(audio)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
