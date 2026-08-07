"""Base scene for the explainer's acts.

Each act is structured as one method per beat of the script, so a note like
"redo the derivation" touches exactly one method and `-n <k>` skips straight to it.
"""

from __future__ import annotations

import os

from manim import FadeOut, Group, Write

from voiceover import VoiceoverScene
from voiceover.services.elevenlabs import ElevenLabsService
from voiceover.services.say import SayService

from . import type as ty
from .layout import act_title

# Voice is a build setting, not a source edit: `build.sh --voice eleven` selects
# Archer for the final narration pass.  Audio is cached by passage text plus its
# service settings, so unchanged passages do not call ElevenLabs again. This
# Creator account has 127,467 characters per month; a Chapter B pass is about
# 20,510 characters, not the obsolete 10k free-tier budget once documented here.
ARCHER = "Fahco4VZzobUeiPqni1S"  # Archer - Conversational
VOICE = os.environ.get("SIGREG_VOICE", "draft")
# The default settings produced audible breaks and choppiness across the Archer
# pass. Make the delivery settings explicit and steadier; including them in the
# service configuration deliberately creates a fresh cache key for this cut.
ARCHER_SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}


class ActScene(VoiceoverScene):
    """Common beat plumbing.

    Narration lives beside the animation and `tracker.duration` makes the audio
    drive the timing, so a beat can never run ahead of its own speech. That is
    what fixes the dead-air problem the flat per-beat clips had.
    """

    # Retained so scenes that set it still import; the chain bar it drove was
    # deleted (VISUAL_SYSTEM.md section 3). Unused.
    chain_link: str | None = None

    def setup(self):
        super().setup()
        if VOICE == "draft":
            service = SayService(voice="Evan (Enhanced)", rate=170,
                                 transcription_model="base")
        elif VOICE == "eleven":
            service = ElevenLabsService(voice_id=ARCHER,
                                        voice_settings=ARCHER_SETTINGS,
                                        transcription_model="base")
        else:
            raise ValueError(
                f"unknown SIGREG_VOICE={VOICE!r}; expected 'draft' or 'eleven'"
            )
        self.set_speech_service(service)

    # --- pacing ------------------------------------------------------------
    #
    # `voiceover()` ends every block by waiting out whatever audio is left
    # (voiceover/scene.py wait_for_voiceover). If the body of the block finishes
    # in 2 s against a 12 s clip, the remaining 10 s is a frozen frame with a
    # voice over it. Most of Chapter B's runtime was exactly that, which is what
    # made it feel simultaneously rushed and dead: dense narration, static
    # picture.
    #
    # Two helpers fix the two halves of the problem. `across()` gives the
    # animation the whole clip instead of a literal run_time, so the picture
    # moves for as long as the voice is talking. `inspect()` buys deliberate
    # silence *between* blocks, so the viewer gets time to look at something
    # with nothing being said over it.

    # Silence longer than this is indistinguishable from a missing audio stream
    # in build.sh's -45 dB check, and that check is load-bearing -- a scene with
    # no audio reports as no silence at all. Keeping deliberate pauses under the
    # threshold means the detector keeps working as a fault alarm.
    MAX_INSPECT = 2.2

    def across(self, tracker, *anims, floor: float = 1.0,
               reserve: float = 0.0, **kwargs) -> None:
        """Play `anims` across the rest of this beat's narration.

        `floor` keeps a short or fast draft voice from producing a jerky sweep;
        `reserve` holds time back for a follow-on play inside the same block.
        """
        run_time = max(floor, tracker.get_remaining_duration() - reserve)
        self.play(*anims, run_time=run_time, **kwargs)

    def inspect(self, seconds: float = 1.2, *anims, **kwargs) -> None:
        """A silent beat with something worth looking at.

        RENDER_REVIEW_SPEC.md section 10.2: a pause is dead air when nothing new
        can be inspected. So this either animates something or holds a frame the
        caller has just changed -- it is not a way to pad a scene to length.
        """
        seconds = min(seconds, self.MAX_INSPECT)
        if anims:
            self.play(*anims, run_time=seconds, **kwargs)
        else:
            self.wait(seconds)

    def clear_beat(self, run_time: float = 0.7) -> None:
        """Fade everything currently on screen.

        Updaters MUST be cleared first: an `always_redraw` mobject rebuilds itself
        every frame, which resets the opacity FadeOut is animating and leaves the
        thing stubbornly visible.
        """
        mobs = list(self.mobjects)
        if not mobs:
            return
        for m in mobs:
            m.clear_updaters(recursive=True)
        self.play(FadeOut(Group(*mobs)), run_time=run_time)

    def open_act(self, title: str, hold: float = 1.2) -> None:
        card = ty.title(title)
        self.play(Write(card), run_time=1.2)
        self.wait(hold)
        self.play(FadeOut(card), run_time=0.6)

    def banner(self, text: str):
        """Act title, added (not animated)."""
        group = Group(act_title(text))
        self.add(group)
        return group
