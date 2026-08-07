"""Play a sample line in every available voice, so you can pick one.

    # macOS voices — free, offline
    PYTHONPATH=. .venv/bin/python -m voiceover.audition say

    # ElevenLabs — costs credits on the first run, cached after
    PYTHONPATH=. .venv/bin/python -m voiceover.audition elevenlabs
    PYTHONPATH=. .venv/bin/python -m voiceover.audition elevenlabs --only Daniel George Alice
    PYTHONPATH=. .venv/bin/python -m voiceover.audition elevenlabs --pause

Each clip is cached, so re-running an audition you have already heard costs
nothing. Only voices you have not sampled before spend characters.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess as sp
import sys
from pathlib import Path

DEFAULT_LINE = "The derivative measures how fast a function changes."

# The stock macOS narration voices. The other ~35 installed voices are novelty
# ones (Bubbles, Zarvox, Bad News) that are no use for a video.
SAY_VOICES = [
    ("Samantha", "US, default"),
    ("Alex", "US, male"),
    ("Fred", "US, male"),
    ("Daniel", "UK, male"),
    ("Moira", "Irish"),
    ("Karen", "Australian"),
    ("Tessa", "South African"),
    ("Rishi", "Indian"),
]


def installed_say_voices() -> list[tuple[str, str]]:
    """Filter SAY_VOICES down to the ones actually present on this machine."""
    result = sp.run(["say", "-v", "?"], capture_output=True, text=True)
    present = {line.split()[0] for line in result.stdout.splitlines() if line.strip()}
    return [(n, d) for n, d in SAY_VOICES if n in present]


def elevenlabs_voices(api_key: str) -> list[tuple[str, str, str]]:
    """Return [(voice_id, short_name, description)] for the account."""
    from voiceover.services.elevenlabs import API_ROOT, _get_json

    voices = _get_json(f"{API_ROOT}/voices", api_key)["voices"]
    out = []
    for v in voices:
        full = v.get("name", "")
        short, _, description = full.partition(" - ")
        out.append((v["voice_id"], short.strip(), description.strip()))
    return out


def play(path: Path) -> None:
    if shutil.which("afplay"):
        sp.run(["afplay", str(path)])


AUDIO_SUFFIXES = {".mp3", ".wav", ".m4a", ".aiff", ".aif", ".flac", ".ogg"}


def audition_music(args: argparse.Namespace) -> int:
    """Preview each candidate track with narration ducking over it.

    A bed that sounds lovely on its own often fights the voice — anything with
    melodic movement in the vocal range does. The only useful audition is the
    one that plays the music the way it will actually be heard.
    """
    from pydub import AudioSegment

    from voiceover.music import MusicCue, build_bed
    from voiceover.services.say import SayService

    tracks = sorted(
        p for p in Path(args.dir).iterdir()
        if p.suffix.lower() in AUDIO_SUFFIXES and not p.name.startswith(".")
    )
    if args.only:
        wanted = {n.lower() for n in args.only}
        tracks = [t for t in tracks if t.stem.lower() in wanted]
    if not tracks:
        print(f"  No audio files in {args.dir}/")
        return 1

    # Narration is synthesized with `say` on purpose: this is a music test, and
    # there is no reason to spend API credits on the voice.
    speech = SayService(voice=args.voice or "Samantha", cache_dir=args.cache_dir)
    data = speech._wrap_generate_from_text(args.line)
    voice_clip = AudioSegment.from_file(Path(speech.cache_dir) / data["final_audio"])
    voice_seconds = voice_clip.duration_seconds

    lead_in = 2.5
    preview = lead_in + voice_seconds + 3.0
    print(f"\n  {len(tracks)} track(s), {preview:.0f}s each: "
          f"{lead_in:.1f}s bed, then narration ducks it, then it returns.\n")

    for index, track in enumerate(tracks, start=1):
        print(f"  [{index}/{len(tracks)}] {track.name}")
        cue = MusicCue(
            path=track, gain=args.gain, duck=args.duck,
            fade_in=1.0, fade_out=1.5,
        )
        bed = build_bed(cue, preview, [(lead_in, lead_in + voice_seconds)])
        mix = bed.overlay(AudioSegment.silent(int(lead_in * 1000)) + voice_clip)

        out = Path(args.cache_dir) / f"_preview_{track.stem}.mp3"
        mix.export(out, format="mp3")
        play(out)

        if args.pause and index < len(tracks):
            if input("        Enter for next, q to stop: ").strip().lower() == "q":
                break

    # add_background_music resolves names against config.assets_dir (this repo
    # points it at sounds/), so a track in a subfolder has to be named relative
    # to that, not by basename alone.
    from manim import config

    try:
        reference = str(tracks[0].resolve().relative_to(
            Path(config.assets_dir).resolve()))
    except ValueError:
        reference = str(tracks[0].resolve())

    print(f"\n  Use one with:\n"
          f'    self.add_background_music("{reference}", '
          f"gain={args.gain:g}, duck={args.duck:g})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", choices=["say", "elevenlabs", "music"], default="say", nargs="?")
    parser.add_argument("--line", default=DEFAULT_LINE, help="sample sentence")
    parser.add_argument("--only", nargs="+", metavar="NAME", help="limit to these voices/tracks")
    parser.add_argument("--pause", action="store_true", help="wait for Enter between items")
    parser.add_argument("--no-intro", action="store_true", help="skip the spoken name")
    parser.add_argument("--cache-dir", default="media/voiceovers/auditions")
    parser.add_argument("--yes", action="store_true", help="skip the cost confirmation")
    parser.add_argument("--voice", default=None, help="music mode: voice for the test narration")
    # sounds/ itself holds the old per-beat narration wavs, so music gets its
    # own folder rather than auditioning someone's voice as a backing track.
    parser.add_argument("--dir", default="sounds/music", help="music mode: folder of candidate tracks")
    parser.add_argument("--gain", type=float, default=-22.0, help="music mode: bed level in dB")
    parser.add_argument("--duck", type=float, default=-8.0, help="music mode: duck depth in dB")
    args = parser.parse_args()

    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)

    if args.service == "music":
        return audition_music(args)

    if args.service == "say":
        voices = [(name, name, desc) for name, desc in installed_say_voices()]
    else:
        from voiceover.services.env import require_api_key

        api_key = require_api_key("ELEVEN_API_KEY", "audition")
        voices = elevenlabs_voices(api_key)

    if args.only:
        wanted = {n.lower() for n in args.only}
        voices = [v for v in voices if v[1].lower() in wanted]
        if not voices:
            print(f"None of {args.only} matched. Run without --only to see the list.")
            return 1

    def sample_for(short: str) -> str:
        if args.no_intro:
            return args.line
        return f"Hi, I'm {short}. {args.line}"

    if args.service == "elevenlabs" and not args.yes:
        chars = sum(len(sample_for(short)) for _, short, _ in voices)
        print(f"\n  {len(voices)} voices, about {chars} characters.")
        print(f"  Free tier is 10,000/month. Already-sampled voices are cached and free.")
        if input("  Continue? [y/N] ").strip().lower() not in {"y", "yes"}:
            return 1

    print()
    for index, (ident, short, description) in enumerate(voices, start=1):
        label = f"{short} — {description}" if description else short
        print(f"  [{index}/{len(voices)}] {label}")

        if args.service == "say":
            from voiceover.services.say import SayService

            service = SayService(voice=ident, cache_dir=args.cache_dir)
        else:
            from voiceover.services.elevenlabs import ElevenLabsService

            service = ElevenLabsService(voice_id=ident, cache_dir=args.cache_dir)

        try:
            data = service._wrap_generate_from_text(sample_for(short))
        except Exception as e:
            print(f"        failed: {e}\n")
            continue

        play(Path(service.cache_dir) / data["final_audio"])

        if args.pause and index < len(voices):
            if input("        Enter for next, q to stop: ").strip().lower() == "q":
                break

    print("\n  Use one with:")
    if args.service == "say":
        print('    SayService(voice="Samantha", transcription_model="base")')
    else:
        print('    ElevenLabsService(voice_name="Alice", transcription_model="base")')
    return 0


if __name__ == "__main__":
    sys.exit(main())
