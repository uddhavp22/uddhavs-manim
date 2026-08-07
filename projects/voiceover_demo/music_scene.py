"""Background music under narration, with a breathing pause.

    ./render.sh projects/voiceover_demo/music_scene.py MusicDemo -ql

Uses sounds/_testbed.mp3, a synthesized constant tone, so the ducking is
measurable. Point add_background_music at a real track to use it for real.
"""

from manim import *

from voiceover import VoiceoverScene
from voiceover.services.say import SayService


class MusicDemo(VoiceoverScene):
    def construct(self):
        # say, not ElevenLabs: this scene exists to test the mix, and there is
        # no reason to spend API credits re-rendering it.
        self.set_speech_service(SayService(voice="Samantha", rate=170))

        self.add_background_music("_testbed.mp3", gain=-22, duck=-8)

        square = Square(side_length=2).set_stroke(BLUE_C, 4)

        with self.voiceover(text="Music sits underneath while I am speaking."):
            self.play(Create(square))

        # No narration here, so the bed comes back to its resting level and
        # the viewer gets a moment to sit with the shape.
        with self.music_break(4.0):
            self.play(Rotate(square, TAU), run_time=4)

        with self.voiceover(text="And it drops away again when I come back."):
            self.play(square.animate.scale(1.5))

        self.wait(2)
