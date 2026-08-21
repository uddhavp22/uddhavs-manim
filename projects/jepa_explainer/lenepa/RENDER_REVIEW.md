# LeNEPA segment — render review

## Scene 01 workshop revision — 2026-08-20

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA01_review_eleven_qh.mp4` |
| Delivery | 34.47 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Scope | `LeNEPA01Tokens` only; scenes 02–08 were not revised in this pass |
| Mechanical checks | `preflight`, `facts.py`, and narration audit clean; audio/video durations matched; no silence interval over 3 s |
| Visual review | 1080p contact sheet plus targeted scans of the encoder propagation, coordinate assembly, and parallel reveal |
| Verdict | **READY FOR OWNER WORKSHOP** |

The revision removes the title card and the direct waveform-to-box morph. One
window first crosses the trace, the third patch then feeds an explicit shared
encoder, and its output neurons travel into coordinate slots before the numbers
appear. Only after this close-up does the operation repeat across the sequence.
Edges remain behind neurons, the propagation highlight follows the learned
connections, and incompatible shapes crossfade rather than tangling through a
path morph. No settled overlap or collision was observed.

`NARRATION_REVIEW_01.md` contains the required manual function, cadence,
metaphor, proof-language, and visual-grounding audit. The 89-word scene text is
the reviewed source for both ElevenLabs and the future human recording.

> The full-segment master reviewed below predates this scene-01 revision. It is
> retained as render history, but it is no longer the current editorial master.

## ElevenLabs preview master — 2026-08-20

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA_segment_eleven_qh.mp4` |
| Delivery | 297.75 s (4:57.75); 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Structure | 8 independently renderable scenes; 19 spoken passages; 691 words |
| Mechanical checks | `preflight` clean; `facts.py` clean; `py_compile` clean; narration audit within every budget; audio and video durations match exactly; no silence interval longer than 3 s |
| Visual review | 1080p frames checked across every scene plus targeted result-table, learning-curve, and UCR frames |
| Voice status | ElevenLabs preview voice with pronunciation substitutions; the source script retains conventional technical spellings for the planned human recording |
| Verdict | **PASS — preview master approved** |

The segment reconstructs the requested argument as one continuous visual object:
the signal becomes patch tokens, those same tokens enter a causal predictor, the
next token becomes the projected prediction target, and the token rows are then
reused to show temporal collapse and SIGReg. The equation appears only after its
two operational terms have been established. The protocol and results scenes
keep the fixed-recipe caveat visible, and the landing scene removes the training
heads before identifying the retained encoder.

The final duration is 2.25 seconds inside the five-minute ceiling. ElevenLabs
receives phonetic forms for invented names and acronyms while subtitles and the
human-recording script keep `LeNEPA`, `JEPA`, `SIGReg`, `PTB-XL`, and the metric
names in their standard written forms. Stable-Whisper transcription was used as
a pronunciation cross-check, not as the source of subtitles.

## Timecoded review

| Time | Observation | Result |
|---|---|---|
| 00:00–00:23 | Signal-to-patch continuity, dimensional annotation, and token readability | Pass |
| 00:23–00:57 | Causal focus and future-token exclusion | Pass |
| 00:57–01:42 | Shared projector, cosine loss, and two-sided gradient statement | Pass |
| 01:42–02:29 | Per-sample temporal collapse and taps at layers 0 and 8 | Pass |
| 02:29–02:57 | Prediction and temporal-SIGReg objective assembled from prior objects | Pass |
| 02:57–03:34 | Separate dataset training, fixed recipes, 20k updates, five seeds, frozen probes | Pass |
| 03:34–04:39 | PTB-XL/Diag tables, training-speed ranges, mixed regression caveat, and UCR result | Pass |
| 04:39–04:58 | One-pass recap and encoder-only landing | Pass |

No blocker, clipping, collision, unexplained object teleport, unreadable settled
text, or audio dead-air interval was observed. Some sampled contact-sheet frames
contain intentional mid-transition states; settled frames on both sides were
checked separately.

## Scorecard

| Category | Verdict | Note |
|---|---|---|
| Claim fidelity | Pass | Values and caveats match `facts.py` and `SOURCE_MAP.md`. |
| Story structure | Pass | Mechanism precedes notation; protocol precedes results. |
| Object continuity | Pass | Signal, patches, tokens, predictor, and retained encoder remain visually traceable. |
| Motion and transformations | Pass | Causal flow, shared projection, collapse, and layer taps are conveyed through transformations rather than labels alone. |
| Composition and hierarchy | Pass | One dominant idea per beat; secondary annotations remain subordinate. |
| Typography and color semantics | Pass | Project type scale and semantic palette are consistent at 1080p. |
| Narration synchronization | Pass | Visual beats resolve within their spoken passages; no silence over 3 s. |
| Technical delivery | Pass | 1080p60 H.264/AAC master, exact A/V duration match, 4:57.75 runtime. |

## Remaining production note

The ElevenLabs track is deliberately a temporary editorial voice. When the
author records the final narration, replace only the voice track first and use
the scene-level sources to retime individual beats if the human read differs
materially; do not time-stretch the recording to force this preview cadence.
