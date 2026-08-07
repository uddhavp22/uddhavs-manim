"""VoiceoverScene — a Manim Community Scene that syncs animations to narration.

Port of manim_voiceover/voiceover_scene.py. The public API (`set_speech_service`,
`voiceover`, `wait_until_bookmark`, `safe_wait`, `add_voiceover_text`) matches
upstream, so scenes written for the manim-voiceover plugin port over unchanged.

Two things this adds on top of upstream: ducked background music beds
(`add_background_music`, `music_break`) and the `narration_spans` bookkeeping
they are built from.
"""
from __future__ import annotations

from contextlib import contextmanager
from math import ceil
from pathlib import Path
from typing import Generator

from pydub import AudioSegment

from manim import Scene, config, logger
from manim.utils.sounds import get_full_sound_file_path

from voiceover.helper import chunks, remove_bookmarks
from voiceover.music import MusicCue, build_bed
from voiceover.services.base import SpeechService
from voiceover.tracker import VoiceoverTracker


class VoiceoverScene(Scene):
    """A Scene that can add voiceovers and time animations against them."""

    speech_service: SpeechService
    current_tracker: VoiceoverTracker | None = None
    create_subcaption: bool = True

    def set_speech_service(
        self,
        speech_service: SpeechService,
        create_subcaption: bool = True,
    ) -> None:
        """Set the speech service. Call this before any voiceover.

        Args:
            speech_service: The service used to produce audio.
            create_subcaption: Whether to emit an .srt alongside the movie.
        """
        self.speech_service = speech_service
        self.current_tracker = None
        self.create_subcaption = create_subcaption
        self.narration_spans: list[tuple[float, float]] = []
        self.music_cues: list[MusicCue] = []

    # -- adding voiceovers ------------------------------------------------

    def add_voiceover_text(
        self,
        text: str,
        subcaption: str | None = None,
        max_subcaption_len: int = 70,
        subcaption_buff: float = 0.1,
        **kwargs,
    ) -> VoiceoverTracker:
        """Add a voiceover to the scene and return its tracker.

        Args:
            text: The text to be spoken. May contain `<bookmark mark='x'/>`.
            subcaption: Alternative subtitle text. Defaults to `text` with the
                bookmarks stripped out.
            max_subcaption_len: Longer subtitles are split into chunks.
            subcaption_buff: Gap in seconds between split subtitle chunks.
        """
        return self._add_voiceover_text(
            text,
            service_kwargs=kwargs,
            subcaption=subcaption,
            max_subcaption_len=max_subcaption_len,
            subcaption_buff=subcaption_buff,
        )

    def _add_voiceover_text(
        self,
        text: str,
        service_kwargs: dict,
        subcaption: str | None = None,
        max_subcaption_len: int = 70,
        subcaption_buff: float = 0.1,
    ) -> VoiceoverTracker:
        if not hasattr(self, "speech_service"):
            raise Exception(
                "You need to call set_speech_service() before adding a voiceover."
            )

        dict_ = self.speech_service._wrap_generate_from_text(text, **service_kwargs)
        cache_dir = Path(self.speech_service.cache_dir)
        tracker = VoiceoverTracker(self, dict_, cache_dir)

        # Scene.add_sound takes its own early return while animations are being
        # skipped (--from_animation_number), which is the behaviour we want:
        # audio recorded over a stretch with no frames has no video to sit
        # against.
        self.add_sound(str(cache_dir / dict_["final_audio"]))
        self.current_tracker = tracker

        # Recorded against the movie's clock, so background music can duck over
        # exactly these windows later.
        if not self.renderer.skip_animations:
            self.narration_spans.append((tracker.start_t, tracker.end_t))

        if self.create_subcaption:
            if subcaption is None:
                subcaption = remove_bookmarks(text)
            self.add_wrapped_subcaption(
                subcaption,
                tracker.duration,
                subcaption_buff=subcaption_buff,
                max_subcaption_len=max_subcaption_len,
            )

        return tracker

    def add_wrapped_subcaption(
        self,
        subcaption: str,
        duration: float,
        subcaption_buff: float = 0.1,
        max_subcaption_len: int = 70,
    ) -> None:
        """Split a subtitle into chunks and lay them across `duration`.

        Chunks go through `Scene.add_subcaption`, so the .srt is written by
        manim's own file writer rather than assembled here.
        """
        subcaption = " ".join(subcaption.split())
        if not subcaption:
            return

        n_chunk = ceil(len(subcaption) / max_subcaption_len)
        tokens = subcaption.split()
        chunk_len = ceil(len(tokens) / n_chunk)
        subcaptions = [" ".join(chunk) for chunk in chunks(tokens, chunk_len)]
        total_len = len("".join(subcaptions))
        weights = [len(sub) / total_len for sub in subcaptions]

        # `add_subcaption` stamps `self.time + offset`, so offsets accumulate
        # from zero rather than from an absolute timestamp.
        offset = 0.0
        for sub, weight in zip(subcaptions, weights):
            chunk_duration = duration * weight
            self.add_subcaption(
                sub,
                duration=max(chunk_duration - subcaption_buff, 0),
                offset=offset,
            )
            offset += chunk_duration

    # -- waiting ----------------------------------------------------------

    def wait_for_voiceover(self) -> None:
        """Wait out whatever is left of the current voiceover."""
        if self.current_tracker is None:
            return
        self.safe_wait(self.current_tracker.get_remaining_duration())

    def safe_wait(self, duration: float) -> None:
        """Wait, unless the duration is shorter than a single frame."""
        if duration > 1 / config.frame_rate:
            self.wait(duration)

    def wait_until_bookmark(self, mark: str) -> None:
        """Wait until `<bookmark mark='...'/>` is reached in the narration."""
        if self.current_tracker is None:
            raise RuntimeError("No active voiceover tracker is available.")
        self.safe_wait(self.current_tracker.time_until_bookmark(mark))

    @contextmanager
    def voiceover(
        self,
        text: str | None = None,
        **kwargs,
    ) -> Generator[VoiceoverTracker, None, None]:
        """Speak `text` while the body of the `with` block animates.

        On exit the scene waits for any remaining narration, so the block
        never runs ahead of the audio.

            with self.voiceover(text="Watch the curve bend") as tracker:
                self.play(Create(graph), run_time=tracker.duration)
        """
        if text is None:
            raise ValueError("Please specify a voiceover text string.")

        service_kwargs = dict(kwargs)
        subcaption = service_kwargs.pop("subcaption", None)
        max_subcaption_len = service_kwargs.pop("max_subcaption_len", 70)
        subcaption_buff = service_kwargs.pop("subcaption_buff", 0.1)

        try:
            yield self._add_voiceover_text(
                text,
                service_kwargs=service_kwargs,
                subcaption=subcaption,
                max_subcaption_len=max_subcaption_len,
                subcaption_buff=subcaption_buff,
            )
        finally:
            self.wait_for_voiceover()

    # -- background music -------------------------------------------------

    def add_background_music(
        self,
        sound_file: str,
        gain: float = -22.0,
        duck: float = -8.0,
        fade_in: float = 1.5,
        fade_out: float = 3.0,
        loop: bool = True,
        start: float = 0.0,
        end: float | None = None,
        ramp_ms: int = 400,
    ) -> None:
        """Lay a music bed under the whole scene, ducked beneath narration.

        Args:
            sound_file: Path to the track, or a name resolved out of
                `config.assets_dir` (this repo points that at `sounds/`).
            gain: Resting level in dB. Music mastered for listening needs a lot
                of attenuation to sit under speech; -22 is a sane start.
            duck: Extra attenuation in dB applied while anyone is talking.
            fade_in / fade_out: Seconds, at the start and end of the bed.
            loop: Repeat the track if it is shorter than the scene.
            start / end: Restrict the bed to part of the scene, in seconds.
            ramp_ms: Duration of the glide in and out of each duck.

        The mix is built at tear down, once the scene's true length and every
        narration span are known — so this can be called anywhere in construct.
        """
        if not hasattr(self, "music_cues"):
            # Music without narration is legitimate; set_speech_service may
            # never have been called.
            self.narration_spans = []
            self.music_cues = []

        self.music_cues.append(MusicCue(
            path=Path(get_full_sound_file_path(sound_file)),
            gain=gain,
            duck=duck,
            ramp_ms=ramp_ms,
            fade_in=fade_in,
            fade_out=fade_out,
            loop=loop,
            start=start,
            end=end,
        ))

    @contextmanager
    def music_break(self, duration: float) -> Generator[None, None, None]:
        """Hold for `duration` with no narration, so the music comes back up.

            with self.music_break(4.0):
                self.play(Rotate(shape, TAU), run_time=4)

        Nothing is playing over it, so the bed is automatically un-ducked for
        the whole block — this is just a readable way to say "let it breathe".
        Any animations inside should add up to about `duration`; whatever is
        left over is waited out.
        """
        start = self.time
        try:
            yield
        finally:
            self.safe_wait(duration - (self.time - start))

    def _mix_background_music(self) -> None:
        """Fold every music cue under the narration track."""
        cues = getattr(self, "music_cues", None)
        if not cues:
            return

        writer = self.renderer.file_writer
        narration: AudioSegment | None = getattr(writer, "audio_segment", None)

        scene_duration = max(self.time, 0.0)
        if narration is not None:
            scene_duration = max(scene_duration, narration.duration_seconds)
        if scene_duration <= 0:
            return

        mixed: AudioSegment | None = None
        for cue in cues:
            bed = build_bed(cue, scene_duration, self.narration_spans)
            if len(bed) == 0:
                continue
            offset_ms = int(cue.start * 1000)
            placed = AudioSegment.silent(offset_ms) + bed if offset_ms else bed
            mixed = placed if mixed is None else mixed.overlay(placed)

        if mixed is None:
            return

        # Ensure the writer will actually mux audio even in a music-only scene.
        if not writer.includes_sound:
            writer.includes_sound = True
            writer.create_audio_segment()
            narration = writer.audio_segment

        writer.audio_segment = mixed.overlay(narration) if narration is not None else mixed
        logger.info(
            f"Mixed {len(cues)} music bed(s) under "
            f"{len(self.narration_spans)} narration span(s)"
        )

    # -- lifecycle --------------------------------------------------------

    def tear_down(self) -> None:
        # Scene.render() calls tear_down() before renderer.scene_finished(),
        # which is where the file writer muxes audio into the movie — so this
        # is the last point at which the mix can still be changed.
        self._mix_background_music()
        super().tear_down()
