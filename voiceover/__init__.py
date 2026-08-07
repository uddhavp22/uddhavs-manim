"""Voiceover support for Manim Community.

A port of manim-voiceover (ManimCommunity/manim-voiceover, MIT) with two
additions this project needed: a macOS `say` backend for drafting timings for
free, and ducked background music beds. Write narration alongside the animation
and let the audio drive the timing:

    from manim import *
    from voiceover import VoiceoverScene
    from voiceover.services.say import SayService

    class Demo(VoiceoverScene):
        def construct(self):
            self.set_speech_service(SayService(voice="Samantha"))

            circle = Circle()
            with self.voiceover(text="Here is a circle.") as tracker:
                self.play(Create(circle), run_time=tracker.duration)

Services live in `voiceover.services` and are imported directly so that an
unused backend never has to have its dependencies installed.

Names here are resolved lazily so that a command-line tool can import this
package without paying for manim's import.
"""
import importlib

_LAZY = {
    "VoiceoverScene": "voiceover.scene",
    "SpeechService": "voiceover.services.base",
    "VoiceoverTracker": "voiceover.tracker",
}

__all__ = list(_LAZY)


def __getattr__(name: str):
    if name in _LAZY:
        return getattr(importlib.import_module(_LAZY[name]), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
