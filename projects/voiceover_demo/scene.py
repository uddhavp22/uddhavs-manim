"""Exercises every part of the voiceover port.

    ./render.sh projects/voiceover_demo/scene.py VoiceoverDemo -ql

Narration is synthesized with macOS `say`, so this renders on a fresh machine
with no API key and no network.
"""

from manim import *

from voiceover import VoiceoverScene
from voiceover.services.elevenlabs import ElevenLabsService
from voiceover.services.say import SayService  # noqa: F401  (offline fallback)


class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # transcription_model runs Whisper over the generated audio to find
        # where each word actually lands, so bookmarks hit the word rather
        # than an estimate of it. Costs a few seconds per line on first render,
        # then it is cached alongside the audio.
        self.set_speech_service(
            ElevenLabsService(voice_name="Chris", transcription_model="base")
        )

        # Swap this in to work offline without spending API credits. Timings
        # will shift, since it is a different voice at a different pace.
        #   SayService(voice="Samantha", rate=170, transcription_model="base")

        self.title_beat()
        self.bookmark_beat()
        self.graph_beat()

    def title_beat(self):
        title = Text("Voiceover in ManimGL", font_size=60)

        # tracker.duration is the length of the generated audio, so the
        # animation is stretched to exactly cover the sentence.
        with self.voiceover(
            text="This whole scene is timed against narration written next to the animation."
        ) as tracker:
            self.play(Write(title), run_time=tracker.duration)

        self.play(FadeOut(title))

    def bookmark_beat(self):
        square = Square(side_length=2).set_stroke(BLUE_C, 4)
        self.add(square)

        with self.voiceover(
            text="""First we <bookmark mark='spin'/>rotate the square,
                   and then we <bookmark mark='grow'/>scale it up."""
        ):
            self.wait_until_bookmark("spin")
            self.play(Rotate(square, PI / 2), run_time=1.0)
            self.wait_until_bookmark("grow")
            self.play(square.animate.scale(1.6), run_time=1.0)

        self.play(FadeOut(square))

    def graph_beat(self):
        axes = Axes(x_range=(-1, 4, 1), y_range=(-1, 5, 1), x_length=9, y_length=5.5)
        axes.add_coordinates(font_size=20)
        graph = axes.plot(lambda x: 0.4 * x**2, x_range=(-0.8, 3.4))
        graph.set_color(YELLOW)

        with self.voiceover(text="Here the parabola grows without bound.") as tracker:
            self.play(Create(axes), run_time=tracker.duration / 2)
            self.play(Create(graph), run_time=tracker.duration / 2)

        self.wait(0.5)
