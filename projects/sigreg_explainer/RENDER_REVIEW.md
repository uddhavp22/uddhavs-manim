# SigReg explainer — render review

## Chapter C C02 final ElevenLabs and target revision — 2026-08-14

| | |
|---|---|
| Artifact | `media/videos/sigreg_explainer/chapterC/c02_the_shape_is_the_goal/1080p60/C02.mp4` |
| Delivery | 56.87 s; 1920×1080 at 60 fps; H.264 video; AAC 48 kHz stereo; ElevenLabs narration |
| Script | 158 spoken narration words by `narration_audit.py` |
| Mechanical checks | complete ffmpeg decode; `py_compile`; `preflight` with no undefined names; no dead air; claims ledger 24/24 |
| Visual review | real 1080p frames checked across C01 continuity, every shape rung, both partner draws, the average pull, the equation, and the restored cloud |
| Verdict | **PASS** |

C02 now begins on the exact fifteen points at the end of C01. The rest of the
cloud arrives under the opening sentence, so continuity is visible without a
separate setup beat. The sheet, line, and point captions crossfade rather than
morphing through tangled intermediate glyphs. The pointwise-matching section
emphasizes 32 representative pairs and dims the remaining dots, which keeps the
arbitrariness legible without filling the frame with 220 competing arrows.

The first high-resolution pass exposed a fixed-frame caption jump during the
second partner draw. The ornamental `Indicate` that triggered it was removed;
the rerender keeps “which Gaussian point?” centred. The axes also recede while
the expected-distance identity is present, then return as the scene resolves
to the round cloud. Frozen-frame analysis reports settled explanatory holds,
but no narration-free dead air.

The delivery revision introduces the desired distribution at the moment its
geometry returns: “The round cloud is our target: a standard Gaussian in D
dimensions.” The following sentence proposes pointwise enforcement as a
tempting shortcut, keeping the target and the failed method conceptually
separate. The Gaussian guide's stroke and fill were reduced, while its caption
was changed to amber, so the target is immediately identifiable without
overpowering the blue sample cloud. Stable-Whisper timing recovered the full
intended transcript before the final render was promoted.

## Chapter C C01 final ElevenLabs revision — 2026-08-13

| | |
|---|---|
| Artifact | `media/videos/sigreg_explainer/chapterC/c01_vectors/1080p60/C01.mp4` |
| Delivery | 46.22 s; 1920×1080 at 60 fps; H.264 video; AAC 48 kHz stereo; ElevenLabs narration |
| Script | 140 spoken narration words by `narration_audit.py`; generated into `SCRIPT_chapterC.md` from the scene source |
| Mechanical checks | complete ffmpeg decode; `py_compile`; `preflight` with no undefined names; frozen-frame/dead-air analysis passed; claims ledger 24/24 |
| Visual review | real 1080p frames checked across the equation build, both score examples, seven-input loop, whole-network propagation, line/plane/cloud transitions, `D=1/2/3/4/6/8` head growth, late `Z` reveal, and final cloud |
| Verdict | **PASS** |

C01 now begins with the actual Epps–Pulley equation rather than reconstructing
Chapter B's three-panel rig. The Gaussian and two-mode scores are evaluated by
the project implementation, not decorative values. The neural-network sequence ports
the relevant grammar from `3blue1brown_videos/_2017/nn`: large individual 5×7
digits run through the network before the compact batch appears; seven
representative passes receive about 1.1 seconds each; every image
has 35 literal pixels mapped to the 35-neuron input layer; neuron fills carry
activations; and a restrained blue wave crosses complete edge groups while the
voice continues. The output head is centred at `D=1`, expands through `D=2`
and `D=3`, and then grows continuously to `D=4,6,8`; each dimension label sits
below its actual head. The visible geometry remains marked `D=3`, so no abrupt
return cut is needed. The same sample dots retain identity through the line,
plane, and final centred 3-D cloud. `Z` is withheld until the cloud exists, and
the scene lands on the adopted standard-Gaussian target rather than a question.
The last narration revision replaces “encoder” with “a neural network” because
the selected ElevenLabs voice repeatedly pronounced the former incorrectly;
the delivered audio was regenerated from that final wording.

The final high-resolution review caught and closed one regression before
delivery: applying opacity to an entire image card overwrote the distinction
between lit and unlit pixels, making the digits look like solid grids. The
cards now retain their native pixel opacities and use only the selection frame
for focus. Stable frames are clean; brief blended states occur only during
intentional transforms.

## Chapter C prerequisite-aware script revision — C01–C03 — 2026-08-12

This revision supersedes the narration reviewed in the 1080p section below.
The older section remains as render-history evidence, but its high-resolution
files do **not** contain the current script. The current pass is draft-voice and
draft-resolution timing validation only.

| | |
|---|---|
| Source check | Re-read the linked *SIGReg from First Principles* tutorial, especially §4 (the one-dimensional statistic and quadrature) and §5 (`Z ∈ ℝ^{N×D}`, unit projections `uᵀZ`, and the later all-directions reduction) |
| Current artifacts | `c01_vectors/480p15/C01.mp4`; `c02_the_shape_is_the_goal/480p15/C02.mp4`; `c03_one_shadow/480p15/C03.mp4` |
| Geometry / voice | 854×480 @ 15 fps, H.264 + AAC; local macOS draft voice, not ElevenLabs |
| Durations | C01 22.27 s; C02 67.46 s; C03 42.80 s |
| Script size | 328 spoken narration words, down from 380; C01 is 66 words, down from 101 |
| Draft verdict | **PASS** — every scene renders, bookmarks resolve, subtitles match the rewritten source, and the shortened shape ladder retains settled endpoints |

The audience contract now controls the opening. C01 does not define vectors or
explain coordinates one at a time. It starts from Chapter B's number-line score,
states that the encoder returns `N` embeddings in `D` dimensions, and uses three
coordinates only as a drawing convention. The original dots still move into the
cloud, preserving the visual continuity without repeating prerequisite material.

C02 now uses the shortest complete collapse argument: directions disappear,
the constant encoder can achieve zero prediction loss, and independent Gaussian
target matching has the exact pointwise minimum `z = 0`. C03 writes the
projection as `uᵀz_i` immediately and reuses Chapter B's statistic. The tutorial's
quadrature and all-directions material remains reserved for C06–C08 rather than
being pulled forward into these scenes.

---

## Chapter C narration and timing review — C01–C03 — 2026-08-12

This pass incorporates the owner's narration review, closes the four dead-air
candidates inherited from `sigreg-chapterC-handoff-3.md`, and checks the final
draft-voice renders. It is not a delivery-voice approval of all of Chapter C.

| | |
|---|---|
| Artifacts | `c01_vectors/1080p60/C01.mp4`; `c02_the_shape_is_the_goal/1080p60/C02.mp4`; `c03_one_shadow/1080p60/C03.mp4` |
| Delivery geometry | all 1920×1080 @ constant 60 fps, H.264 + AAC |
| Durations | C01 29.32 s; C02 66.33 s; C03 42.33 s |
| Review method | narration/subtitle comparison, full-resolution real-frame extraction, contact sheets, targeted transition sequences, frame-count/cadence checks, and matching 480p15 replays |
| Focused verdict | **PASS** — the requested narration revisions and all inherited timing findings are closed; no dropped-frame cadence or choppy object motion found |

| Scene/time | Inherited finding | Revision and observed result |
|---|---|---|
| C01 0.00–29.32 | The narration described vector coordinates abstractly and the dimensional expansion needed a more conversational, visible progression. | The voice now moves from one number, to a plane, to space, then explicitly says that three dimensions are only what the screen can show. The original dots retain identity through the lift and fan; camera drift and the question-mark pulse keep the final reasoning beat alive. |
| C02 30.20–44.77 | The random-pairing objection was implied instead of asked, and the old caption change could turn into an unreadable glyph morph. | “But which Gaussian point should each embedding match?” now lands before the redraw. The caption changes by a short fade-out/fade-in succession; frame-by-frame checks confirm no overlapping or tangled text. The second settled partner draw then makes the arbitrariness visible. |
| C02 44.87–59.30 | The expected-distance identity held nearly unchanged while a dense sentence continued. | The explanation is split into observation, equation, and landing: random directions cancel; the surviving arrows point to zero; then the equation appears. The point-length and `D` terms receive modest sequential emphasis at their narration bookmarks. |
| C02 59.40–66.33 | The final cloud held static through the conclusion. | The conclusion now distinguishes pointwise matching from a property of the collection. A subtle camera move exposes the cloud's 3-D structure, then returns to the exact C02→C03 seam angle. |
| C03 09.05–14.31 | The complete Chapter B rig appeared early and then held. | The scalar shadow stays isolated until “the rig”; the number line, wrapping panel, and characteristic-function panel then assemble progressively around those same dots. Object identity is preserved and the build tracks the sentence. |
| C03 27.20–38.25 | Saying the target “is the same standard Gaussian it always was” pre-empted C06's all-directions result, and the score appeared too early. | C03 now says that a target must be chosen and chooses Chapter B's standard Gaussian only for this shadow. The target, gap, and score arrive on their matching words; the naming beat follows. The claim that every direction shares `N(0,1)` remains reserved for C06. |

The C03 displayed score was independently recomputed from the exact rendered
cloud and direction as `0.055476983…`, so the storyboard's stale `0.031` was
corrected to the rendered `0.055`. The final spoken form is TTS-safe — “Call
the score T of u” — while the screen keeps the mathematical `𝒯(u)` notation.

---

## Chapter B review

The written review required by [`RENDER_REVIEW_SPEC.md`](../../RENDER_REVIEW_SPEC.md).
One section per scene, in that document's §19 output order. **A scene with no
entry here has not been reviewed**, whatever its render status.

| | |
|---|---|
| Artifact under review | `videos/sigreg_explainer/chapterB_master.mp4` |
| Review rev | **2** (rev 1 reviewed 2026-08-06, findings below, all addressed) |
| Delivery target | 1920×1080 @ 60 fps |
| Reviewed at | **854×480 draft** — see the standing caveat |
| Voice | macOS `say` (Samantha) draft, **not** the delivery voice |
| Duration | **1156.3 s (19:16)**, up from 1081.8 s (18:02) — see O7 |
| Mechanical checks | 12/12 scenes carry an audio stream, each within 0.8 s of its video duration; 0 silence gaps > 2.5 s; 69,376 frames at 60 fps |
| Gates passing | `preflight` clean · `facts.py` 19/19 · `narration_audit` all budgets |
| Script | [`SCRIPT_chapterB.md`](SCRIPT_chapterB.md) — generated from the scenes, 3,608 spoken words |

> **Standing caveat — this review is not final.**
> `RENDER_REVIEW_SPEC.md` §5.7 forbids approving text from a zoomed crop, and
> §13 requires the export to be checked at the target resolution. Everything
> below is marked `[RES]` where the finding is resolution-dependent and must be
> re-checked on the 1080p render, and `[VOICE]` where it depends on the draft
> TTS. **No scene can carry a verdict above `REVISE` until both are redone**
> (§16: *the clip is the wrong version, resolution, or duration* is a blocker).

---

## Chapter-level verdict

**`REVISE`** — for the two reasons in the caveat, not for anything found in the
content. Every rev-1 blocker below is closed, and the rev-2 render is the first
one whose typography, palette, and script were designed rather than defaulted.

---

## Rev 1 → rev 2: the systemic findings

These were not per-scene defects. Each was a single decision, repeated across
all twelve scenes, which is why they are recorded once here rather than twelve
times below.

### F1 — No typeface was ever chosen · **BLOCKER** · closed

| | |
|---|---|
| Category | Technical integrity (§13), visual taste (§8.3) |
| Evidence | ManimGL ships `text.font: Consolas`; `manimpango.list_fonts()` does not contain it on this machine. Every `Text` in the chapter rendered in an unspecified Pango fallback. |
| Viewer consequence | The prose looked like an unstyled default because it *was* one. This is the whole of the "text looks ugly and out of place" report. |
| Fix applied | `custom_config.yml` sets `text.font` explicitly; `common/type.py` passes `font=` on every mobject so a missing config cannot silently change the look. [`VISUAL_SYSTEM.md`](../../VISUAL_SYSTEM.md) §1–2. |
| Since rev 2 | The face is now **Latin Modern Roman**, not Helvetica Neue — see the rev-3 note below. `common/type.py` also **raises at import** if the family is absent, which is the check whose absence caused this finding. |

### F2 — English typeset in Computer Modern · **HIGH** · closed

| | |
|---|---|
| Category | Visual taste (§8.3) |
| Evidence | 00:00:25 — `Tex(R"\text{mean} = +0.00")` set the word *mean* in CM roman directly above a Helvetica sentence. 18 such sites across the chapter. |
| Viewer consequence | Two typographic textures doing one job in one frame; reads as unstyled even though each element is individually fine. |
| Fix applied | `ty.line()` composes Helvetica words and CM mathematics on one baseline. All 18 sites converted; `grep '\\text{'` over `chapterB/` is now empty. |

### F3 — Pure yellow on pure black · **MEDIUM** · closed

| | |
|---|---|
| Category | Accessibility (§12), taste (§8.1) |
| Evidence | 00:05:00 — the `\|φ(t)\|` curve rendered muddy olive while its own label rendered bright yellow, both nominally `#FFFF00`. Thin yellow strokes smear under chroma subsampling. |
| Viewer consequence | The target curve, the most important reference object in the chapter, was the hardest thing on screen to see. |
| Fix applied | `TARGET` → `#F0B429`. Background `#000000` → `#0C0E12` so furniture reads. [`VISUAL_SYSTEM.md`](../../VISUAL_SYSTEM.md) §4. |

### F4 — Two blues, one step apart, two meanings · **MEDIUM** · closed

`CLOUD #58C4DD` and `EMPIRICAL #9CDCEB` were indistinguishable at delivery
size while carrying different meanings. Merged to one role — the empirical
fingerprint belongs to the batch, so it is one idea.

### F5 — Twelve type scales · **MEDIUM** · closed

Each scene declared its own `BODY`/`SMALL`/`NOTE` at 26/27/28 and 21/22/23.
Nothing aligned across a cut, and §8.3 had nothing to check consistency
against. Collapsed onto six steps in `common/type.py`, with a hard floor of 22
that raises `ValueError` rather than rendering unreadable text.

### F6 — Illegible permanent progress bar · **MEDIUM** · closed

`chain_bar` was seven words at `font_size=16` (15 px), then `set_width`-shrunk
further, pinned above every scene, carrying nothing any scene needed. §7.3 and
§8.2 at once. **Deleted, not enlarged.**

### F7 — Every scene closed on a slogan · **HIGH** · closed

| | |
|---|---|
| Category | Narration ([`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) §18) |
| Evidence | 12/12 scenes ended on a short quotable line: *"Two numbers cannot see a shape." · "One frequency can be fooled. That is why we use all of them." · "No scale to ask about." · "They were chosen because gradients flow through them." · "We did not invent it, we rebuilt it."* |
| Viewer consequence | One good closing line is a good line. Twelve is a template, and the template is the single loudest machine-written signal in the script — more than any individual phrase. |
| Fix applied | Full rewrite of all 92 passages. Scenes now close by stating the result precisely or by creating the next scene's question (§18). Detector added to `tools/narration_audit.py`; **42% → 0%**. |

### F8 — Three more narration tics · **HIGH** · closed

Each was invisible to the rev-1 audit because no budget described its shape.
All three now have one, and all three gate the build.

| Tic | Rev 1 | Rev 2 | Budget |
|---|---|---|---|
| `", and it is …"` appositive filler (§13) | 4.6 /1k | 0.9 | 2.0 |
| Evaluative framing — *worth banking*, *the whole point* (§5) | 5.1 /1k | 0.3 | 1.5 |
| `"Here is / Here are"` openers (§4) | 3.7 /1k | 0.0 | 2.0 |

Knock-on: repeated sentence openers fell from `"it is…"`×14 / `"that is…"`×12
to a maximum of ×3; mean sentence length rose from ~11 to ~15 words as
fragments were joined into reasoned sentences (§13); no scene has a choppy run.

### F9 — Metaphor used before it was earned · **MEDIUM** · closed

*fingerprint* appeared 24 times across 8 scenes, first asserted flat in `b03`
("That curve is the fingerprint of this batch") five scenes before the
uniqueness theorem that licenses it. [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md)
§17 requires it be reserved for the theorem and qualified there. Now **5 uses
across 3 scenes**, introduced in `b08` at the moment the theorem is stated:

> *Because the curve determines the distribution completely, calling it a
> fingerprint is accurate rather than decorative, and that is the sense the
> word carries for the rest of the video.*

Before `b08` the object is called what it is: the characteristic function, or
the average arrow against `t`.

### F10 — Channel redundancy at the chapter's first frame · **MEDIUM** · closed

00:00:08 — on-screen text read *"Telling them apart by eye is easy / We need
one number that does it / and gradient descent has to be able to differentiate
it"* while the voice said the same three things. §7.2 requires at least one
channel to carry a relationship. The screen now holds the *requirement* in the
form the chapter must satisfy; the voice explains why it is hard.

### F11 — The slogans survived on screen after being cut from the voice · **HIGH** · closed

| | |
|---|---|
| Category | Narration (§18), channel redundancy (§7.2) |
| How it was found | `video_watch` on the first rebuilt scene. Frame 00:00:25 still read **"Two numbers cannot see a shape."** in amber, inside a box, three hours after that exact sentence was deleted from the script. |
| Viewer consequence | The rewrite had not removed the slogans — it had moved them from the audio channel to the video channel, where they are *more* prominent and stay on screen for ten seconds instead of two. |
| Scope | 12 captions across 6 scenes: `b00` *"Two numbers cannot see a shape"*; `b05` *"where the distribution sits lives in the phase / how spread out it is lives in the magnitude"*; `b08` *"we do not conclude the distributions are similar / We conclude they are equal"*; `b01` *"we did not choose the arrows because they were elegant / we chose them because gradients flow through them"*; `b10` *"this single fact does all the work"*; `b11` *"Representations are not numbers / They are vectors, in hundreds of dimensions"*. |
| Fix applied | Each replaced by the compressed statement §7.2 assigns to the screen — notation or result, not rhetoric. `b01`'s two lines became `histogram: d(count)/dx = 0 almost everywhere` / `wrapped sample: d/dx = i t · e^{itx}, never zero`, which is the actual argument rather than a claim about it. |

**Method lesson.** The narration audit walks `self.voiceover(text=…)` only. It
is structurally blind to `Text(…)`, so a script can score clean while the
screen still says the thing. This is the second time a green tool has been
mistaken for a clean result; `tools/narration_audit.py` now has a companion
scan for on-screen strings, and neither substitutes for watching the render.

### F12 — `BackgroundRectangle(...).set_fill(BLACK)` · **MEDIUM** · closed

Three sites. Invisible against the old `#000000` camera background; against
`#0C0E12` a visibly darker slab with hard edges appears behind the caption. A
palette change that looks safe in the diff and wrong in the frame — exactly the
class of defect §3 exists to catch. Now filled with `BG`.

### F13 — Arrows drawn without arrowheads · **MEDIUM** · closed

`b02`'s cancellation demonstration drew six unit arrows as bare `Line`s. Six
evenly spaced lines through a circle's centre read as three diameters, so
*"they cancel"* — the sentence the whole chapter turns on — had no visible
referent. Now `Arrow` with a tip. VISUAL_SYSTEM.md §5.

### F14 — `t` axis label inside the safe margin · **LOW** · closed

Placed `DR` of the last tick, which put it 0.1 units from the frame edge and
read as clipped at 480p. `layout.fit_in_frame` existed and was never applied to
it. Now `UR`, with `fit_in_frame` as a backstop since `t_max` is a caller
argument.

### F15 — `b03` had its own copy of the rig's axis labels · **MEDIUM** · closed

Found only because the fix for F14 landed in `ThreePanelRig.axis_labels()` and
`b03` still rendered a clipped `t` afterwards. `b03` duplicated that method
line for line — including `font_size=20`, below the readability floor — so the
shared fix reached `b05`, `b05`, and `b06` and left `b03` on the old geometry.

This is the drift `rig.py`'s own docstring warns about, in the one scene where
the rig is introduced. The readout was duplicated too, in `TARGET` — the colour
that means *the Gaussian reference* everywhere else in the chapter. Both now
call the shared helpers.

**Lesson recorded because it will recur:** a fix to shared geometry is not
verified by looking at one scene. After changing `common/`, check a frame from
*every* scene that uses it.

### F16 — Both outer rig panels overhung the safe margin · **MEDIUM** · closed

Found by checking `b05` and `b06` after F15, which is the only reason it was
found at all: the φ(t) curve ran to the frame edge in every rig scene, and the
`t` label had nowhere legal to sit — `fit_in_frame` was pulling it back on top
of the last tick rather than clipping it, which looked like a missing label.

`FRAME_WIDTH` is 14.222, so the usable half-width is 6.661. The geometry put
the number line's left edge at **−6.80** and the φ(t) axes' right edge at
**+6.85**. Both outside, in the shared constants, since the rig was first
built.

Now −6.60 and +6.60.

**A guard was added rather than just the fix.** `layout._assert_panels_inside_frame()`
runs at import and raises with the offending span. Panel positions are a few
numbers that have to stay inside another number; nothing raises when they
drift, the render just puts a curve on the frame edge, and it is caught only by
someone looking at a frame — which is how this survived every previous review.

---

## Open findings, rev 2

| # | Time | Category | Severity | Finding | Recommended fix |
|---|---|---|---|---|---|
| O1 | all | Technical (§13) | **BLOCKER** | Render is 854×480 and the voice is macOS `say`. Wrong version for delivery under §16. | Re-render `--hd`; set the ElevenLabs voice. Blocked on the voice ID. |
| O2 | 00:02:50 `b03` | Clarity (§5.2) | LOW `[RES]` | Downgraded from MEDIUM. The perceived imbalance was mostly F16; what remains is ~1.5 units of empty band above the panel captions, which §8.2 says is not in itself a defect. | Leave. Re-judge at 1080p. |
| O3 | 00:00:38 `b00` | Pacing (§10.2) | ~~MEDIUM~~ **closed** | The scene's final 13 s hold one static frame while the closing sentence plays. §10.2: a pause is dead air when nothing new can be inspected. | **Closed at rev 3.** `b00` was rebuilt; the gap between the clumps is now shaded from the data (`layout.widest_gap()`) and the scene ends on the pipeline rather than a hold. |
| O4 | `b10` | Pacing (§7.5) | MEDIUM `[VOICE]` | 2:59 against a chapter mean of 1:30; `PLAN.md` §5 itself calls this derivation an appendix. | Judge on the ElevenLabs pass — draft TTS pacing is not evidence. Do not cut `b09` or `b11` first; both are load-bearing. |
| O7 | chapter | Pacing (§7.5) | MEDIUM | **Runtime grew: 18:02 → 19:16, +74 s (+6.8%).** `NARRATION_SPEC.md` §6 and §13 require that operations carry their reason and that fragments be joined into connected sentences; doing that raised mean sentence length from 11 to 15 words. Smaller than feared — `b10` and `b11` both got *shorter* — but Chapter B was already long against an ~8 min plan. | **User decision — flagged, not silently resolved.** Cutting the reasoning back out would undo the rewrite. The levers: (a) accept 19:16; (b) split B into two videos at `b08`, a natural seam — construction, then consequences — giving roughly 9:30 and 9:45; (c) demote `b10`'s derivation to an appendix, which `PLAN.md` §5 already contemplates. Recommendation: **(b)**. |
| O5 | `b09` | Proof status (§6.4) | MEDIUM | The 1/N sampling-floor claim is `empirical_observation` in `concepts.yaml`, verified in `facts.py`, and narrated with "settles at". Correct, but the animation shows one clean convergence. | Confirm on the HD render that no visual implies more than the label allows. |
| O6 | chapter | Context (§7) | LOW | Chapter A does not exist, so B opens cold on an audience contract A was meant to establish. | Resolve when A is built. |
| O8 | chapter | Taste (§8.3) | LOW — **half closed** | 28 `Tex` call sites still pass a literal `font_size` (34, 38, 44, 48, 52, 64). All are above the floor and all are equations, so nothing is unreadable — but they are ad hoc, and §8.3 checks font sizes for consistency. | **Closed for Part 1 at rev 3**: every string in the eight Part 1 scenes now goes through `common/type.py`, and `rig.readout()` — the last place in the rig setting type by hand — was migrated too. Part 2's sites remain. |

---

## Per-scene review

Each scene gets the `RENDER_REVIEW_SPEC.md` §19 output. Rev-2 entries are
**pending the HD + ElevenLabs render** — the spec forbids approving a scene
from code changes alone (§21, last box), and rev 2 changed code.

| Scene | rev 1 | rev 2 | Δ | Chief rev-1 finding, and what changed |
|---|---|---|---|---|
| `b00_the_problem` | 0:31 | 0:46 | +0:15 | F10 channel redundancy at the chapter's first frame; F7 *"Two numbers cannot see a shape."* in both channels. Longest single growth — the opening carried the least reasoning per sentence. |
| `b02_arrows` | 1:24 | 1:31 | +0:07 | F13 arrows without tips; F8 appositive ×3. Arrowheads make the cancellation demonstration legible for the first time. |
| `b03_the_rig` | 0:41 | 1:01 | +0:20 | F9 *fingerprint* asserted 5 scenes early; F15 duplicated axis labels; F16 clipped panel. Now closes on the open question rather than the label. |
| `b05_real_and_imaginary` | 1:16 | 1:24 | +0:08 | F3 target curve unreadable at 480p; slogan close. |
| `b05_worked_examples` | 1:26 | 1:32 | +0:06 | F7 *"That split is worth remembering."* → the phase/magnitude split now stated as the fact `b10` will use. |
| `b07_one_speed_fails` | 0:33 | 0:42 | +0:09 | F7 *"One frequency can be fooled."* → the aliasing mechanism named. The counterexample itself was strong and was kept. |
| `b06_the_anchor` | 1:03 | 1:04 | +0:01 | F7 *"No scale to ask about."* → why a shared start makes two curves comparable. |
| `b09_which_frequencies` | 2:08 | 2:24 | +0:16 | F8 *"the most useful thing in this chapter"*; λ now named a bandwidth parameter, per the source. O5 open. |
| `b08_uniqueness` | 1:31 | 1:39 | +0:08 | F9 — the metaphor is now **introduced** here and qualified by the theorem. Proof debt stated plainly. |
| `b01_why_not_histograms` | 1:48 | 1:50 | +0:02 | F7 slogan close; the three objections are now numbered by the argument, and the third is flagged as the one that matters. |
| `b10_gaussian_fingerprint` | 2:59 | **2:49** | **−0:10** | O4 length. Got *shorter* — the derivation was carrying commentary about itself. |
| `b11_fingerprint_to_loss` | 2:43 | **2:35** | **−0:08** | F7 *"We did not invent it, we rebuilt it."* Also shorter. |

Growth is concentrated in the four scenes that had the least reasoning per
sentence to begin with; the two densest scenes contracted.

---

## Rev 3 — Part 1 (`chapterB1`)

| | |
|---|---|
| Artifact under review | `videos/sigreg_explainer/chapterB1_master.mp4` |
| Scope | **Part 1 only**: `b00 b02 b03 b05 b05 b06b b07 b06`. Part 2 (`b09`–`b11`) is unchanged and still at rev 2. |
| Reviewed at | 854×480 draft, macOS `say` (**Evan (Enhanced)**, changed from Samantha) |
| Duration | **8:31** (511.4 s) across 8 scenes |
| Typeface | Latin Modern Roman throughout, regular weight only |
| Mechanical checks | 8/8 scenes carry an audio stream, each within 0.72 s of its video duration (`B05` 2.0 s, a silent tail); **0 silence gaps > 2.5 s**; 30,696 frames at 60 fps; **0 empty-screen stretches ≥ 1 s** (`tools/dead_air.py`) |
| Gates | `facts.py` **22/22** · `preflight` clean · `narration_audit` all budgets, including the newly-gating on-screen scan · `dead_air` clean · `script_dump` regenerated |

**New gate this rev: `tools/dead_air.py`.** R1 below is a four-and-a-half-second
blank screen that passed every existing check, so the check that would have caught
it now exists. It flags frames where peak luminance equals mean luminance — a blank
frame is uniform, so `YMAX − YAVG ≈ 0`, while one thin grey axis gives 115. That
criterion needs no per-project calibration; two earlier attempts (absolute mean, and
peak against a per-file floor) each produced false positives and are documented in
the module so they are not tried again. It is validated against a synthetic blank
clip, which the first version silently passed.

### Verdict — `REVISE`

For O1 alone: this is a 480p draft in a placeholder voice, which §16 makes an
automatic blocker regardless of content. **Nothing in the content is blocking.**
Corrections 1–4 are applied and each is now visible in the frame rather than
merely asserted in the script.

### How this review was run

`RENDER_REVIEW_SPEC.md` §20 forbids reviewing from a contact sheet and §21 forbids
approving from code changes alone, so **every scene was watched** — frames pulled at
0.1–0.6 fps through `claude-video-vision`, plus targeted windows wherever a beat's
claim needed checking against the picture.

Three of the six findings below were *only* findable that way, and two of those were
introduced by the rewrite itself. The measured checks and the watching found different
things and neither was redundant: `dead_air.py` caught a blank frame no human would
have described precisely, and watching caught a 14-second frozen frame `dead_air.py`
is structurally unable to see.

### What the render confirms

- **Correction 1 is demonstrable.** `b03`'s curve visibly dips below zero near
  t=2 and recovers by t=6.5. The old narration ("the average pulls in toward
  the centre") was being contradicted by the animation running underneath it.
- **The rig refactor is clean.** All four rig scenes render identical geometry
  and the `t` axis label sits inside the safe margin in every one — the F15
  check, which is the specific failure that motivated `ThreePanelRig.mount()`.
- **`b00`'s two carried-over defects are fixed.** Dot columns are vertical and
  packed from the axis; the gap rectangle covers the stack it annotates.
- **O3 is closed.** `b00` no longer ends on a static frame.

### Rev-3 findings

| # | Scene | Category | Severity | Finding | Status |
|---|---|---|---|---|---|
| R1 | `b00` | Pacing (§10.2) | **HIGH** | **4.5 s of completely empty screen** (52.5–57.0 s) with narration playing over it, at the seam between the moment ladder and the two constraints. Every gate passed it. Found by measuring mean frame luminance, not by watching. | **Fixed.** The ladder now becomes *"a description of the whole distribution"*, which stays on screen and lifts into a heading — so the next sentence's "such a description" also gains a visible referent (§26). Re-measured: no empty stretch remains. |
| R2 | `b06b` | Clarity (§5.3) | MEDIUM | The magnitude ghost was drawn at stroke 7 under a stroke-3 live curve, so the invariant the scene exists to demonstrate was almost invisible — asserted, not shown. | **Fixed.** Stroke 11 at opacity 0.32, so the live curve visibly sits inside a band. |
| R3 | `b07` | Clarity (§5.1) | LOW | The batch runs to ±6.28 on a ±6 axis, so the two outermost samples hung off the ends of the line they sit on. | **Fixed.** Axis widened to ±7. |
| R1b | `b00` | Redundancy (§7.2) | MEDIUM | The **first** fix for R1 put the words *"a description of the whole distribution"* on screen — which is what the narration says at that exact moment. Straight channel redundancy, and the newly-gating on-screen slogan scan caught it immediately. The gate was right and the fix was wrong. | **Fixed.** Replaced by `samples → ? → one differentiable score`, which names the two fixed ends and marks the middle as the unknown. It says something the voice does not, both constraints are then visibly constraints on that middle box, and the scene closes by resolving the `?` rather than drawing a second pipeline beneath the first (§7.3). |
| R5b | `b02` | Pacing (§10.2) | **HIGH** | **The last 14 seconds are a completely static frame** — six motionless arrows and a fixed `length = 0.00` — while the closing sentence makes a claim about a *range*: "one when they coincide, zero when they are spread evenly, and something in between otherwise". The in-between case was never shown anywhere in the chapter. `dead_air.py` cannot catch this: there is content on screen. This is precisely the class §10.2 reserves for a human pass, and it was found by watching. | **Fixed.** The six arrows now sweep continuously between coincident and evenly-spread with the length tracking live, so the sentence and the picture make the same claim. The readout is a static word plus a `DecimalNumber` rather than a rebuilt `ty.line` — `Text` goes through Pango on every construction, and rebuilding one per frame at 60 fps is a slow-render trap. |
| R4 | chapter | Taste (§8.3) | MEDIUM | **`ty.line()` misaligns mixed baselines when a word carries a descender.** It aligns every part to the bottom edge of part 0; a `Text` containing "y" or "p" extends below the baseline, so adjacent `Tex` digits sit visibly low. Clearest at `b05` 01:04 — the `0` in *"X symmetric about 0"* drops below the line. Affects ~30 call sites. | **Open.** Real but cosmetic. Fixing it means baseline alignment rather than bounding-box alignment, which manim does not expose directly, and it would require re-rendering and re-checking every scene. Deferred deliberately rather than churned immediately before a commit. |
| R5 | `b03` | Taste (§8.2) | LOW | For the first ~9 s the unrolled sample line extends well past the circle panel it belongs to, reading as loose dots with no line under them. Pre-existing, not introduced by the refactor; it resolves as the wrap animation runs. | **Open.** Re-judge at 1080p. |
| R6 | chapter | Pacing (§7.5) | NOTE | Runtime came in at **8:31** against the agreed 9–10 min. Under, not over. The redundancy audit cut more than the corrections added. | **User decision.** Not padded to hit a number. If more time is wanted, `b03` and `b07` are where inspection silence would buy the most — both carry the chapter's load-bearing arguments. |

### Runtime, per scene

| Scene | Rev 2 | Rev 3 | Δ |
|---|---|---|---|
| `b00_the_problem` | 0:46 | 1:23 | +0:37 — rebuilt |
| `b02_arrows` | 1:31 | 1:16 | −0:15 |
| `b03_the_rig` | 1:01 | 1:11 | +0:10 |
| `b05_real_and_imaginary` | 1:24 | 1:18 | −0:06 |
| `b05_worked_examples` | 1:32 | 0:48 | −0:44 — split |
| `b06b_what_magnitude_ignores` | — | 0:53 | new |
| `b07_one_speed_fails` | 0:42 | 0:54 | +0:12 |
| `b06_the_anchor` | 1:04 | 0:50 | −0:14 |
| **Total** | **7:55** | **8:31** | **+0:36** |

The three scenes that grew are the three carrying corrections or a rebuild. The
four that shrank are the four the redundancy audit marked hardest.

### Still not reviewable

`RENDER_REVIEW_SPEC.md` §3 Pass 4 (audio-only) ran against the per-scene Whisper
`.srt` rather than a separate transcription pass, which the plugin is not
configured for. Two mishearings in those transcripts (*"5 of 0 is 1"* for
*phi of zero is one*, *"before it is red"*) are Whisper artifacts on the draft
voice, not narration defects — worth re-checking on the ElevenLabs pass, since
if a speech model mishears "phi" a listener may too.

---

## Tasteful choices worth preserving

`RENDER_REVIEW_SPEC.md` §8 asks for these explicitly, and a review that only
removes things will hollow the chapter out.

- **The three-panel rig with one shared `t`.** Line, circle, curve, driven by a
  single tracker, with the samples visibly fixed while the phases move. This is
  the chapter's central visual argument and it does real work (§6.1).
- **`b07`.** Constructing a batch that a single frequency reads as fully
  collapsed is a genuine counterexample, not an illustration — it earns the
  sweep instead of asserting it.
- **`b09`'s twenty draws from a true Gaussian.** Showing the sampling floor
  rather than claiming it is the strongest §6.4 moment in the chapter.
- **`b10`'s derivation** arriving at a differential equation from `p' = -x p`.
  The equation compresses an operation the viewer has watched (§10).
- **Restraint throughout.** No glows, no particles, no bounce easing, no
  gratuitous camera motion. §8.1 has nothing to flag.

---

## How the chapter is assembled

Worth stating because it is easy to assume otherwise from the single
`chapterB_master.mp4`.

**Each scene is rendered independently.** `build.sh` runs `render.sh` once per
scene file, producing twelve separate MP4s under
`videos/sigreg_explainer/chapterB/<scene>/`. Each is a complete, publishable
clip with its own audio. The master is the last step: an `ffmpeg -f concat -c
copy` of the twelve, which is a **stream copy** — no re-encode, no generation
loss, and the joins are exact.

**The joins are hard cuts, deliberately.** `RENDER_REVIEW_SPEC.md` §7 asks
whether repeated title cards or recaps make a chapter feel *episodic rather
than continuous*; a wipe or crossfade at every seam is the strongest available
signal that a new episode has started. Every scene already ends on
`clear_beat()`, a fade of everything to background, and the next opens from
that background — so the fade **is** the transition, and it is inside the
scene where the pacing can be tuned against the narration. Adding a crossfade
on top would double it.

There is also a cost: `-c copy` requires identical stream parameters and does
no work. An `xfade` at eleven seams means re-encoding all eighteen minutes,
which costs quality and render time for an effect §8.1 would flag as
unjustified.

**If the chapter should ship as separate videos, nothing needs rebuilding** —
the twelve clips already exist and the master is a convenience artifact.

Rev 1 was reviewed from extracted frames plus the source and the audit tools —
`ffmpeg -ss <t> -i <mp4> -frames:v 1`, then read. That satisfies
`EXPLAINER_PROCESS.md` §8 but **not** `RENDER_REVIEW_SPEC.md` §3, which requires
seven passes including uninterrupted playback with audio, a muted pass, and an
audio-only pass, and which forbids reviewing from a contact sheet (§20).

Rev 2's full seven-pass review is owed on the HD + ElevenLabs render. The
`claude-video-vision` MCP tools cover the visual passes; transcription is not
configured for that plugin, so the audio-only pass runs against the Whisper
`.srt` that manim-voiceover already emits per scene.

---

## Rev 4 — Part 1 (`chapterB1`), re-cut for continuity

| | |
|---|---|
| Artifact under review | `videos/sigreg_explainer/chapterB1_master.mp4` |
| Scope | **Part 1 only**, now **six scenes**: `b00 b02 b03 b05 b07 b06`. Part 2 is untouched and still at rev 2. |
| Reviewed at | 854×480 draft, **ElevenLabs Archer** (`Fahco4VZzobUeiPqni1S`) — first Part 1 review on the delivery voice |
| Duration | **9:01 (541.3 s)** across 6 scenes, up from 8:31 across 8 |
| Brief | Make Part 1 feel like one curious argument rather than a run of separately-explained scenes |

### What this revision was for

Rev 3 closed every finding it raised and the chapter still watched as a
sequence. Three things were causing that, and none of them were per-scene
defects:

1. **The opening experiment was never finished.** `b00` puts up two batches
   with identical count, mean and variance and asks how they can have different
   shapes. Part 1 then built the entire characteristic-function apparatus and
   **never ran those two batches through it.** The question was scenery.
2. **The rig was torn down and rebuilt at every seam.** `b03`, `b05`, `b05`,
   `b06b` and `b06` all use the same three-panel rig, each rendered as its own
   MP4 ending in `clear_beat()`. At 00:03:19 of the rev-3 master the viewer
   watches a live rig fade to background and an almost identical one appear one
   second later with different captions and a different batch. That is a cut
   between episodes, drawn in the middle of one investigation.
3. **Roughly a fifth of the runtime was a motionless picture with narration
   over it.** Not blank — full, and frozen, which is why every gate passed it.

### Structural changes

| Change | Why |
|---|---|
| **`b05_real_and_imaginary.py` folded into `b03`, source deleted** | One rig, one batch, no cut. `b03` builds the curve; the same rig then notices the curve was only one of the average arrow's two coordinates. The merged scene also drops `b05`'s private `SKEWED` batch — the seven-value clump slice `b03` already runs is lopsided enough (`max|Im φ| = 0.375`), so the data no longer changes at the exact moment the point is that the curve was hiding something about *this* data. |
| **`b06b_what_magnitude_ignores.py` folded into `b05`, source deleted** | Same rig, third question. |
| **`b06` rewritten as the payoff** | `φ(0) = 1` is proved as before, and then **`b00`'s two batches** — the same forty numbers, from the same fixed seeds — go through the rig one after the other. Their curves are nothing alike: the hump decays and never goes negative (min +0.009), the clumps swing to **−0.647**, and the widest gap is **0.764 at t = 2.94**. Both leave from 1, which is what `φ(0) = 1` is *for* and why the two curves can be read off one pair of axes without rescaling. Verified in `facts.py` as `toy_batches_have_different_curves`. |
| **`b00` rebuilt around the same thread** | The rev-3 cut ended on an amber question card held motionless for twelve seconds — a third of the scene, saying in text what the voice was saying at that instant. The two batches now shrink into the left end of a pipeline `→ ? → one score`, each constraint is written under the arrow it constrains, and the `?` resolves. |
| **Sources deleted rather than orphaned** | A stale duplicate of shared geometry is finding F15's failure mode. Git has the history. |

The toy experiment is now the spine: named in `b00`, returned to on the rig in
`b03` ("back to the two clumps from the start"), and **answered** in `b06`.

### The systemic finding

**S1 — `across(tracker, Indicate(...))` was the project's dominant source of
frozen frames.** · **HIGH** · fixed at ~20 sites

`ActScene.across()` exists to give an animation the whole narration clip instead
of a literal `run_time`. It was overwhelmingly being handed an `Indicate` — a
one-second gesture at `scale_factor` 1.02–1.15. Stretched over eight seconds of
speech that is not a gesture, it is a still frame. Measured examples on the
rev-3 master: `b02` 01:34–01:44 (six motionless arrows under a sentence about
arrows spreading), `b05` 00:47–00:56 (six dots pulsing 12% at `t = 0`), `b06`'s
entire closing tableau.

Second form of the same bug: **a fixed-length `self.play(...)` followed by
`wait_until_bookmark`.** Whatever is left of the clause between the two plays is
a held frame. `b03`'s opening ran fourteen seconds that way.

Both are now written as `across(..., reserve=<tail>)` with the animation sized
to the clause, and the filler animations are gone — every one replaced by
something the sentence is actually about:

- `b02`'s averaging beat is one `ValueTracker` from coincident (length exactly
  1) through roughly-agreeing (0.98) to evenly spread (exactly 0, the sixth
  roots of unity), with the readout counting down live. The three stages that
  used to be static-transform-static are the same tracker at different values.
- `b03` stretches the unrolled strip as `t` grows, because the strip's length
  *is* `t` times the batch's range — so "multiplying by a frequency" is watched.
- `b06`'s gap between the two curves is a live measurement that opens and closes
  as `t` moves, instead of a bar drawn once at the end.
- `b00` nudges three different samples in turn under "nudging **any** single
  sample", and ripples every sample under "asked of every sample at once".

### New gate: `tools/still_frames.py`

R5b and S1 are both "the screen is full and nothing is moving", and nothing in
this repo could see it. `dead_air.py` detects a *blank* screen by construction.
ffmpeg's `freezedetect` is unusable on this material: it thresholds the **mean**
frame difference, and these scenes are thin bright strokes on near-black, so a
curve sweeping a whole panel moves a few thousand pixels out of 400k and reads
as frozen. Measured: it reported 22.8 s frozen across a passage in which a
number line visibly unrolls into a circle.

The new tool thresholds the **count** of changed pixels instead, which is
invariant to how much of the frame the moving object covers. It is reported, not
fatal — §10.2 keeps the judgement human — but nobody has to find these by
scrubbing any more.

**Measured on this cut:** 37.2 s of still frame in 9:01 — **6.9%** — in 7
stretches, the longest **6.8 s**. Per scene:

| Scene | Runtime | Still ≥ 4 s |
|---|---|---|
| `b00_the_problem` | 1:11 | 19.8 s |
| `b02_arrows` | 1:24 | 4.8 s |
| `b03_the_rig` | **2:41** | **0.0 s** |
| `b05_worked_examples` | 1:20 | 6.2 s |
| `b07_one_speed_fails` | 0:55 | 0.0 s |
| `b06_the_anchor` | 1:30 | 6.6 s |

The longest scene in Part 1 has no still stretch at all, which is the merge
working: a rig driven by one tracker has something moving in it whenever the
frequency is moving.

Two calibration notes, recorded because both were wrong on the first attempt and
would be got wrong again. The comparison runs at **320×180**: at 160×90 a
legitimately moving small object covers about one pixel per sample and falls
under any threshold that also rejects h264 noise, so the tool reported stillness
that was really *"the tool cannot see this"* — it scored this cut at 68.6 s when
the true figure was 37.2 s. And the sampling rate is **5 fps**, high enough that
a slow `ValueTracker` sweep still shows movement between consecutive samples.

What survives is 4–7 s holds, which §10.2 treats as a judgement call rather than
a defect — several are deliberate comprehension pauses on a frame that has just
changed (`b06`'s `inspect(1.8)` on the finished comparison, `b05`'s flat line at
one, where *nothing moving* is the entire observation). `b00`'s 19.8 s is the
weakest number in the table and is the place to look first if this scene is
revisited: its closing beat carries about 39 s of narration over a diagram, and
the honest fix there is a shorter script rather than invented motion.

### Defects introduced by this revision and fixed before it shipped

Each was found by pulling frames from the render, not from reading the diff.

| # | Where | Finding | Status |
|---|---|---|---|
| N1 | `b00` | The two constraint captions were two-line prose hung under two arrows 1.7 units apart. They **overlapped into an unreadable smear.** They were also a straight paraphrase of the narration (§7.2). | **Fixed.** Replaced by the *form* of each constraint — `only x₁,…,x_N` and `∂score/∂xᵢ exists` — on separate rows, each on a dashed lead down from the arrow it constrains, so the attachment is drawn rather than inferred (§5.4). |
| N2 | `b00` | Resolving the `?` transformed first and re-laid-out second, so a long phrase sat on top of "one score" for 1.2 s and rendered as two overlapping strings. | **Fixed.** The whole row re-lays-out in the same `play`. |
| N3 | `b00` | The "nudge a single sample" motion was invisible: a 3-pixel dot at 0.48 scale drifting a third of a unit over eight seconds. | **Fixed.** Three separate nudges, each brightening as it moves. |
| N4 | `b03` | `swap()` would have raised on `remove(None)` — this scene builds the rig by hand rather than through `mount()`, which is what normally records the panel-1 dots, and the folded-in symmetry beat calls `swap()`. | **Fixed** before the first render of the merge. |
| N5 | `b03` | The strip stretch was a monotone creep: about one pixel per frame, below the threshold at which anything looks like motion. | **Fixed.** Overshoots past the target and settles. |
| N6 | `voiceover/services/base.py` | **Editing only the bookmarks in a passage reused the previous entry's bookmarks.** The TTS cache keys on the bookmark-*stripped* text — correct, since moving a bookmark changes no audio and must not re-spend the budget — but `VoiceoverTracker` reads bookmark positions out of the cached entry's `input_text`. Re-marking a sentence whose words were unchanged therefore either timed the bookmarks at their old positions **silently**, or raised `There is no <bookmark mark='count'/>` from inside the render, twenty minutes in, with nothing pointing at the cache. Hit for real in this revision. | **Fixed.** `_wrap_generate_from_text` overwrites `input_text` with what the scene actually asked for, before the cache-hit early return so it covers hit and miss alike. The key is untouched, so bookmark edits are still free. |

### Also closed

- **R5** (rev 3, open) — the unrolled sample line had nothing under it for the
  first nine seconds. `ThreePanelRig.roll_curve()` now draws the line being
  rolled, from the same `wrapped()` call as the dots, so it cannot disagree with
  where they land. The samples are carried onto it by `TransformFromCopy` rather
  than both appearing at once.
- **`b03`'s number line** was `(-2, 2)` where every other rig scene uses
  `(-3, 3)`, which put this batch's largest sample on top of the end tick and
  changed the line's width at the old `b03`/`b05` cut. Now consistent.
- **Panel-1 stacking is in the rig**, not copied. `b06` shows two real
  forty-sample batches, and flat on a 3.9-unit line forty samples are one smear
  — a scene whose closing claim is about *shapes* then has no evidence in panel
  1. `b00` had solved this locally; `line_dots(stack=True)` reuses
  `layout.stack_levels` so there is one implementation (F15).

### Audio

Checked per scene with `astats`, not by ear alone: peaks **−2.4 to −4.5 dBFS**
(no clipping), RMS **−22.4 to −23.2 dB** (spread 0.8 dB across six scenes),
**flat factor 0** everywhere — no digital flat-lining, dropouts or clipped runs.
Every scene carries an audio stream within **0.71 s** of its video duration,
which is the trailing `clear_beat()` fade and is consistent across all six.

**No ElevenLabs setting was changed, deliberately.** `ARCHER_SETTINGS` in
`common/beat.py` is part of the service's cache key, so touching stability or
similarity_boost invalidates **every cached passage in the chapter** and re-spends
the full character budget on lines whose text has not changed. The measurements
above give no reason to: the earlier choppiness that motivated pinning those
settings is gone, and the delivery is level across the cut. If a future pass does
want different settings, that is a full-chapter re-narration and should be
planned as one.

### Open findings, rev 4

| # | Scene | Category | Severity | Finding | Recommended fix |
|---|---|---|---|---|---|
| O1 | all | Technical (§13) | **BLOCKER** | Still 854×480. §16 makes the wrong resolution an automatic blocker. The *voice* half of rev 3's O1 is now closed — this is the delivery voice. | Re-render `--hd`. |
| O9 | chapter | Redundancy (§7.2) | LOW | `narration_audit`'s on-screen scan reports 2 slogan-shaped captions, both in **Part 2** (`b08` *"one frequency asks one question"*, `b11` *"this is the Epps–Pulley statistic"*). Pre-existing and outside this revision's scope; Part 1 scores 0. | Fix when Part 2 is re-cut. It is the only check over budget. |
| O10 | Part 1 | Pacing (§7.5) | NOTE | Runtime grew to 9:01 from 8:31. The growth is `b06`'s payoff and `b00`'s restored middle; the merges themselves were roughly runtime-neutral. | **User decision.** Nothing here is padding, but if Part 1 must come in under nine minutes, `b07` is the least load-bearing minute. |
| O11 | `b00` | Pacing (§10.2) | LOW | 19.8 s of the scene's 71 s is still — the highest ratio in Part 1, concentrated in the closing pipeline beat, which carries ~39 s of narration over a diagram. | Shorten the script rather than invent motion. Deliberately not done in this pass: the beat's content is load-bearing for Part 2 and cutting it is a scope call. |
| R4 | chapter | Taste (§8.3) | LOW — **closed** | `ty.line()` misaligned mixed baselines when a word carried a descender. | **Closed.** `type.py` measures the descender drop against an `H` probe and aligns on that, cached per (kind, text, size). |

### Verdict — `REVISE`

For O1 alone: a 480p draft is a blocker under §16 regardless of content.
**Nothing in the content is blocking.** The three things this revision was
called for — the abandoned experiment, the chopped rig, and the frozen frames —
are addressed and each is now visible in the render rather than asserted in the
source.

### Method note

Everything above was found by watching the render at 0.2–0.5 fps with targeted
windows around every cut and reveal, and by measuring. The two methods found
different things and neither was redundant: **N1 and N2 are defects the diff
looks fine for** and only a frame shows, and **S1 is a defect no frame shows** —
it needs the still-frame measurement to separate "held deliberately" from
"nothing was animated here".

---

## Rev 5 — Part 1 (`chapterB1`), Manim CE port + first human watch-through

| | |
|---|---|
| Artifact under review | `media/masters/sigreg_explainer/chapterB1_master.mp4` |
| Scope | **Part 1**, six scenes: `b00 b02 b03 b05 b07 b06`, first watch since the ManimGL → Manim Community port. Rev 1–4 above are all pre-port. |
| Reviewed at | 854×480 draft, macOS `say` (Evan (Enhanced)) — **not** the delivery voice |
| Reviewer | User, full watch-through, not a frame sample |

Rev 4 closed the systemic issues in the ManimGL cut (the abandoned experiment,
the chopped rig, the frozen frames). None of what follows regresses that work —
these are defects the ManimGL-era review's checks were not built to catch:
colour *consistency* across a scene rather than colour choice, a hard-cut
`swap()` rather than a frozen frame, and register/register-drift in language
that the regex-based `narration_audit.py` budgets do not cover because each
individual line is under budget. All are **open**; none are fixed yet.

### New systemic findings

**F17 — The average arrow changes colour mid-introduction · `b03` · MEDIUM · open**

| | |
|---|---|
| Category | Visual consistency (VISUAL_SYSTEM.md — colour carries meaning) |
| Evidence | `b03_the_rig.py` `average_beat()` grows a one-off `mean_arrow` hardcoded to `COLLAPSE` (red), then immediately hands off to `always_redraw(r.centroid)`, and `ThreePanelRig.centroid()` (`common/rig.py`) is hardcoded to `EMPIRICAL` (blue). The average arrow the viewer is told to track changes colour the instant it starts being tracked. |
| Fix | Add a dedicated palette role (not `CLOUD`, not `COLLAPSE` — user specifically wants purple, distinct from either distribution's own colour-coding) and use it in both places so the arrow never changes colour once introduced. |

**F18 — `swap()`, `arrows()`, and `trace()` colour are inconsistent with each other · `common/rig.py` · MEDIUM · open**

| | |
|---|---|
| Category | Visual consistency + pacing (hard cuts) |
| Evidence | `ThreePanelRig.swap()` (`rig.py:132`) does `scene.remove(self.mounted_dots)` / `scene.add(self.mounted_dots)` on a freshly-built `VGroup` — an instant cut, not an animation. It is called at every batch change in Part 1: `b05`'s three worked examples, `b06`'s bell→clumps comparison. Separately, `arrows()` (`rig.py:225`) is hardcoded to `CLOUD` regardless of `self.colour`, so panel 2's arrows do not recolour when `trace()` correctly does (`trace()` already uses `self.colour`, which is why `b06`'s panel-3 curves are correctly blue/red per batch — panel 2 just never got the same treatment). |
| Fix | `swap()` should animate the old dots into the new positions (`Transform`, matching what `b05`'s `shift_beat` already does by hand for the shift case) rather than remove/add. `arrows()` should take `self.colour` the same way `trace()` does. |

**F19 — Downward-stacked histogram reads as inverted · `b00` · LOW · open**

| | |
|---|---|
| Category | Visual clarity |
| Evidence | `batch_on_a_line(..., up=False)` in `b00_the_problem.py` stacks the two-clumps (`COLLAPSE`, red) batch hanging *below* its number line, "so the two batches face away" per the code comment. Watched at full speed it reads as an upside-down distribution, not a mirrored layout. |
| Fix | Design call, not purely mechanical — options include keeping both batches stacked upward, or adding a visual cue (axis on top vs. bottom, or a brief settle animation) that reads as "facing away" rather than "inverted." Flagged for a pedagogy decision before Codex re-implements. |

**F20 — "characteristic function" is named before its payoff is shown · `b03` → `b05`/`b07` → `b06` · MEDIUM · open**

| | |
|---|---|
| Category | Pedagogical sequencing (EXPLAINER_PROCESS.md §16, "do not overuse delayed naming" — this is the inverse failure, naming too early) |
| Evidence | `b03_the_rig.py` `symmetry_beat()` says *"a symmetric distribution has a purely real characteristic function"* — the term's first spoken use — before the viewer has seen two different distributions actually produce two different curves. `b05`/`b07` then spend three scenes building worked examples on the same rig without the term being spoken again, and `b06` finally shows the payoff (two real batches, two different curves) but by then the name was already spent on a case (symmetry) that is not the chapter's central claim. |
| User's framing | "Once we show how for [different] samples the average line — or whatever we draw — is different, then we can say this is what a characteristic function is... All the properties we show, the collapse case, the magnitude case, the simple non-degenerate case, are perfect sections, but we need to be pedagogical and build up to something. Our goal is to differentiate distributions, and it feels like we lose this." |
| Fix | No rebuild needed, per the user — a reordering. Move the naming sentence to land at or after `b06`'s toy-batch comparison (the actual payoff), and rephrase `b03`'s closing so it establishes the *property* (purely real for symmetric batches) without spending the *name*. This is cross-cutting across four scene files and touches the chapter's narrative spine — worth a design pass before implementation, not a mechanical find-and-replace. |

**F21 — Language that survived the ManimGL-era `narration_audit.py` budgets but reads as AI-register on a human watch · Part 1 · LOW · open**

The existing audit is regex-budget-based (`tools/narration_audit.py`) and every
budget passed on this script — see the tool run below. All seven of these are
individually under-budget; the issue is register, not a countable pattern the
tool checks for. Rewrites via `/humaniser` + `NARRATION_SPEC.md` §3/§5:

| Scene | Was | Now | Why |
|---|---|---|---|
| `b00` line 154 | "Now for the awkward part. We chose these two toy batches so the familiar checks agree: ..." | "These two toy batches were built to make the familiar checks agree: ..." | Cuts the meta-commentary throat-clearing ("Now for the awkward part"); states the fact instead of narrating the act of choosing it. |
| `b02` line 274 | "...Euler's identity, read off the picture as how far right the arrow reaches, and how far up." | "...That's Euler's identity, and the picture is already showing it: how far right the arrow reaches, and how far up." | "Read off the picture as X" doesn't parse — read off *of* what, as *what*? Splits into two clean clauses. |
| `b02` line 140 | "Put one of those answers here. Its two coordinates fix a point, and the picture that will matter is the arrow..." | "One such answer lands as a point, fixed by its two coordinates. The picture that matters is the arrow..." | Drops the stilted imperative opener for a declarative that names what's on screen. |
| `b03` line 125 | "...Wrapping that line around the circle is the multiplication, drawn." | "...Wrapping that line around the circle is that multiplication, made visible." | Callback to "multiplying it by a frequency t," two clauses earlier in the same sentence, instead of a flat appositive. |
| `b03` lines 264–266 | "Raising t moves two of the three panels. The samples on the left do not move at all: the data is fixed, and only the question being asked of it changes." | *(cut entirely — the beat opens directly on what the circle does)* | States something the frame already shows; the viewer can see the left panel isn't moving without being told the data is fixed. |
| `b03` line 397 | "...which is why dropping either one loses information the other cannot supply." | "...Drop either curve and that point stops being pinned down: only its shadow on one axis survives, not its actual position." | "Loses information" was abstract — names what's actually lost (the point's position, vs. its shadow on one axis). |
| `b06` line 218 | "...those arrows are genuinely pointing backwards." | "...those arrows are pointing backwards." | `genuinely` is banned AI-register vocabulary (NARRATION_SPEC.md §5); the claim is stronger without the intensifier. |

`tools/narration_audit.py` output on all six Part 1 scenes: **all budgeted
checks within limits** — 1,669 words, every category at or under budget. This
confirms the tool's limits: it catches countable template patterns, not
register drift a human catches by ear. Nothing here suggests loosening the
budgets; it suggests the audit is a floor, not a substitute for a watch-through.

### Rev 5 findings — pacing and motivation

| # | Scene | Category | Severity | Finding | Recommended fix |
|---|---|---|---|---|---|
| P1 | `b03` | Motivation (§7) | MEDIUM | `average_beat()` opens directly on "each landing point is a unit arrow, and their average is..." with no framing question. The wrap beat that precedes it ends on the translation rule, not on a hook into "what if we averaged these." | Add a bridging clause — posing the average as a question before answering it — either at the close of `wrap_beat()` or the open of `average_beat()`. |
| P2 | `b02` | Technical | LOW | User reports the complex-plane animation reads as slightly jittery. Not yet root-caused — candidates are the `point_at()` piecewise-linear interpolation in `arrow_beat()` or per-frame rebuild cost in the `always_redraw` closures. | Needs investigation before a fix is written; flagged for Codex to profile rather than guess at. |
| P3 | `b03` | Pacing | LOW | Choppy cut around the "the picture on the right is half finished" line (`two_curves_beat()`, ~4:21 in the reviewed cut) — a title fade-out/fade-in coincides with the new imaginary curve appearing. | Stagger the title swap from the curve's first appearance rather than firing both in the same `play()`. |
| P4 | `b05`, `b06` | Pacing | MEDIUM | Sample-batch changes (constant→two-point→spread in `b05`; bell→clumps in `b06`) all go through `rig.swap()`'s hard remove/add — see F18. User: "keep the same number line, just move the samples on it." | Covered by F18's fix. |
| P5 | `b06` | Visual consistency | LOW | In the final bell-vs-clumps comparison, panel-2 arrows stay `CLOUD` (blue) after the swap to the red-coded clumps batch, so the two distributions aren't visually distinguished in the one panel where the viewer is watching them diverge. | Covered by F18's `arrows()` fix. |

### Tasteful, keep as-is

Per user: the worked-examples sequence in `b05` (constant/collapse case, the
two-point exact-cosine case, the shift/magnitude-invariance case) is "perfect,"
and the representation-collapse material specifically is "good." Nothing there
should change — the finding is sequencing and naming around it (F20), not the
content of the examples themselves.

### Verdict — `REVISE`

Not blocked on resolution/voice this time (O1 from rev 4 is unrelated to this
round). Blocked on F17–F21 and P1–P3: none are cosmetic-only, and F20 in
particular is the difference between "shows properties" and "builds to a
goal," which is the user's chief structural complaint about this cut.

### Fixes applied

Implemented by Codex against this section, then re-rendered and re-checked by
hand (Codex's own sandbox lacks the project's font environment, so its
`-ql` renders never got past scene construction — none of this was verified
by Codex itself).

| Finding | Status |
|---|---|
| F17 (average arrow recolours) | **Fixed.** New `AVERAGE` role colour (`common/palette.py`); `rig.py`'s `centroid()` and `b03`'s one-off seed arrow both use it. Flourish added: the individual arrows `Indicate` briefly at the `avg` bookmark before the average grows. |
| F18 (`swap()` hard cut, `arrows()`/`trace()` colour mismatch) | **Fixed.** `swap()` now `Transform`s the existing dots into their new positions/colour instead of remove+add. `arrows()` now follows `self.colour` like `trace()` already did. `b05`'s hand-rolled duplicate dot-animation code (a manual `Transform` for the shift case, a manual `lagged_map(FadeIn, ...)` for the others) was deleted as redundant now that `swap()` does it once, centrally. |
| F19 (upside-down clump histogram) | **Fixed.** User's call: both batches now stack upward off their own line (`up=True` for both in `two_batches()`); colour and shape alone distinguish them. Re-rendered and checked by frame — no collision between the two stacks or their labels. |
| F20 (term named before its payoff) | **Fixed.** `b03`'s `symmetry_beat` now says "a symmetric batch gives a purely real curve" (property, no name). `b06`'s `toy_answer_beat` now opens with "This curve is called the characteristic function..." at the actual payoff (the two-batch comparison). `b05`/`b07` content untouched, per the user. |
| F21 (language fixes) | **Fixed.** All 7 lines replaced as specified. `narration_audit.py` re-run post-edit: still all budgets within limits. |
| P1 (no motivation before averaging) | **Fixed.** Bridging question added to the top of `average_beat()`'s voiceover. |
| P2 (jittery complex-plane animation) | **Fixed, with a caveat.** Root cause found: `point_at()`'s piecewise-linear path had an instantaneous velocity change at its middle waypoint, which is what read as a jitter/snap. Replaced with C¹ Hermite interpolation so the path's velocity is continuous through the waypoint. Root-cause confidence is solid; whether it fully resolves what the user *saw* still wants a watch-through, since it was diagnosed from the math, not from the frame the user watched. |
| P3 (choppy cut at "half finished") | **Fixed.** The title-swap and the imaginary curve's first appearance no longer fire in the same `play()`; staggered into two sequential 0.55 s plays. |
| P4, P5 | Covered by F18. |

**Re-rendered and verified clean:** `B00`, `B02`, `B03`, `B05`, `B06` at
`-ql`, no tracebacks, fresh `.mp4`s written. `B07` untouched (no source
change) so not re-rendered. `narration_audit.py` and `preflight.py` both
clean on the full six-scene set post-edit.

**Not yet done:** a real watch-through of the new renders (the point of this
whole round was that automated gates don't catch everything), and the
ElevenLabs + `-qh` final pass, which was paused for this review.

---

## Rev 6 — Part 1, second human watch-through after Rev 5's fixes

| | |
|---|---|
| Artifact under review | `media/masters/sigreg_explainer/chapterB1_master.mp4` (the post-Rev-5 render) |
| Scope | `b02`, `b03` |
| Reviewed at | 1920x1080, ElevenLabs voice — the delivery cut |
| Reviewer | User, full watch-through, plus a second pass by Claude using `claude-video-vision` (frame extraction at 1.5–6 fps over the flagged windows) to root-cause each finding against the actual render rather than the source |

Three of the five items below are things Rev 5 claimed were fixed or in
scope and were not, in whole or in part. Recorded here plainly rather than
folded into the "Fixed" language Rev 5 used, since that language is what
produced the gap:

- **F17 was only ever fixed in `b03`.** `b02_arrows.py`'s own
  `average_beat()` — a separate arrow-averaging demo, unrelated to `b03`'s
  rig — has the identical bug (`EMPIRICAL`-coloured mean arrow/dot/readout)
  and was never touched, because F17's evidence only cited `b03_the_rig.py`.
- **The centre-then-left number-line choreography was never implemented.**
  The user described it in the critique that produced Rev 5 ("we start with
  the number line of points in the center then we wrap it around a circle
  ... then move the number line frame to the left panel"), but it never
  became a tracked finding — not F17–F21, not P1–P5. It fell out between the
  critique and the write-up.
- **F21's own fix line is the thing being flagged again.** The Rev 5 fix for
  the "read off the picture as X" complaint replaced it with "the picture is
  already showing it" — itself flagged this round as filler.

New findings, all fixed and re-rendered:

| # | Scene | Category | Finding | Fix |
|---|---|---|---|---|
| F22 | `b02` | Technical (root cause) | `unit_arrow_beat()` leaves `theta` at its raw value `1.6 + TAU` (≈7.88) when it ends. `components_beat()` immediately animates `theta.animate.set_value(0.9)` — Manim interpolates the *raw* tracker value, so the arrow spins backward almost a full extra revolution in 0.7s before landing. This is the "flourish where it goes clockwise is janky" report at ~1:43 in the reviewed cut; confirmed by frame extraction (`video_watch` at 3–6fps over 1:30–1:53), not just reasoned from the code. | One-line fix: `self.theta.set_value(self.theta.get_value() % TAU)` (instant, no animation — cos/sin are unaffected) immediately before the re-target, so the next animation takes the short way round. Re-extracted frames at the same timestamps confirm a direct, short rotation with no backward spin. |
| F17 (b02) | `b02` | Visual consistency | `average_beat()`'s mean arrow, dot, `length =` label, and live readout were all `EMPIRICAL` (blue, same as the data arrows) — the same bug F17 fixed in `b03`, missed here because it's a separate scene. | All four recoloured to `AVERAGE`. Confirmed by frame: the mean arrow and "length = " readout are now visibly purple against the blue data arrows. |
| F23 | `b03` | Pedagogical sequencing / motivation | `wrap_beat()` drew panel 1 (the number line, fully dotted) at its permanent left position from frame one, while a separate, disconnected strip wrapped into the circle in the centre panel. The two were never visually connected — the wrap had nothing to point back to, which is most of why the beat read as unmotivated. | Rebuilt: `r.line` now opens *at* `RIG_CIRCLE_CENTRE` (the centre panel), with its dots overlaid there. That same line and its dots are what stretches, rolls, and wraps into the circle — the wrap now visibly happens to the numbers the viewer is looking at. Once wrapped, the emptied line frame slides to its permanent home at `RIG_LINE_CENTRE` and the samples fade back in there. Confirmed by frame extraction over the full beat (0–30s of the isolated `B03` render): centred line → wrap → slide left → dots re-emerge → both panel captions land once both panels are populated. |
| — | `b02` | Motivation | No line connected "a number can be measured by where it sits" to "a number can also be measured by where it lands on a circle" before the complex plane is introduced — the user's specific ask ("we can think of a way of measuring points on the number line via the complex unit circle"). | Added as the opening clause of `arrow_beat()`'s first voiceover: "A number on a line can be measured a second way: not by where it sits, but by where it lands on a circle." Foreshadows `b03`'s wrap directly. |
| F21 (follow-up) | `b02` | Language register | "That's Euler's identity, and the picture is already showing it: how far right the arrow reaches, and how far up" — the replacement phrase from Rev 5's own F21 fix reads as filler on a second pass. | Cut to "That's Euler's identity: how far right the arrow reaches, and how far up." No meta-commentary about what the picture is doing. |

### Verification

- `B02` and `B03` re-rendered individually at `-ql`: both exit 0, no
  tracebacks (checked directly, not delegated).
- `tools/narration_audit.py` on both scenes: all budgeted checks within
  limits.
- `tools/preflight.py` on both scenes (inside `.venv`): no undefined names.
- Every fix above was confirmed against actual rendered frames via
  `claude-video-vision` `video_watch`/`video_info` — not inferred from the
  diff. F22 in particular required this: the bug is invisible in a code read
  and only shows as motion.
- **Not yet re-rendered:** the full `chapterB1` master (`build.sh`). These
  fixes are only live in the standalone `B02`/`B03` renders checked above.

### Verdict — `REVISE` → fixes landed, master rebuild pending

All five items above are closed. Nothing else in this round's critique
remains open. Next step is a full `chapterB1` rebuild
(`./build.sh chapterB1 -qh --voice eleven`) and a watch-through of the
assembled master before treating Part 1 as final.

---

## Rev 7 — narration recheck + the pedagogical restructure Rev 6 hadn't done

Two follow-ups from the same watch-through this session.

### Narration recheck (`/humaniser` + manual pass, all six Part 1 scenes)

`tools/narration_audit.py` was clean going in — as documented since Rev 5,
it catches countable template patterns, not register. A line-by-line reread
against `/humaniser`'s pattern list found the script largely clean already
(no classic AI vocabulary anywhere in Part 1: no "crucial," "delve,"
"showcase," "testament," etc.). Three small, real fixes:

| Scene | Was | Now | Why |
|---|---|---|---|
| `b05` | "...that length nearly vanishes, then rises again. Keep its shape in mind." | "...that length nearly vanishes, then rises again." | "Keep its shape in mind" promises future relevance without saying anything now — the exact pattern already deleted once in `b02` ("every curve later in this chapter turns out to be..."). Same violation, smaller instance. |
| `b06` | "One object, built out of nothing but the samples, and it separates a pair..." | "One object, built out of nothing but the samples, separates a pair..." | Dropped the appositive-filler "and it" — the one pattern `narration_audit.py`'s own regex flagged. |
| `b06` | "...swing the average all the way over to the negative side -- those arrows are pointing backwards." | "...swing the average all the way over to the negative side. Those arrows are pointing backwards." | One overloaded sentence with a double-hyphen aside, split into two clean ones. |

Verified: `narration_audit.py` and `preflight.py` clean on all six scenes;
`B05` and `B06` re-rendered individually, exit 0.

### The pedagogical restructure — F20 was a reorder, this is the real ask

F20 (Rev 5/6) moved *where a sentence naming the term sits* — it did not
change scene structure, and the user's Rev 7 question ("did you do any actual
reorganizing or add a new scene with the payoff") correctly identified that
this was never done. The user described a five-part structure: goal → a
couple of simple examples → **a new definition/recap scene** → the remaining
examples → a closing question for Part 2. Confirmed via `AskUserQuestion`:
keep `b05` intact (don't split the "perfect" scene) and insert the new scene
after it; treat `b07` as the "other properties" beat rather than building
new Gaussian-specific content.

**New scene added: `b04_the_definition.py` (class `B04`).** Reuses
`ThreePanelRig` and the same two-point batch `b05` just finished on (visual
continuity, not a new visual metaphor — "machine" is on the project's
approved metaphor list, used twice, well under the one-central-metaphor
cap). Three beats: (1) sweep the whole rig once, over narration recapping it
as one mechanism rather than three panels; (2) name it — "the characteristic
function" — and write $\varphi(t) = \mathbb{E}[e^{itX}]$; (3) bridge —
collapse, the exact cosine, and phase-blindness to a shift are named as
facts about this one function, tying `b05`'s three examples together under
the new name before `b07` and `b06` build on it.

**Chapter order changed:** `b00 b02 b03 b05 b07 b06` → `b00 b02 b03 b05 b04
b07 b06`, in `build.sh`'s `chapterB1`/`chapterB` part maps. Naming note:
`b06b` was deliberately *not* reused — it's a retired filename (the old
magnitude/shift beat, folded into `b05` and deleted per the F15-era comment
already in `build.sh`); reusing it for unrelated new content would collide
with that history, so the new scene is `b04`.

**`b06` trimmed:** the naming sentence in `toy_answer_beat` ("This curve is
called the characteristic function...") is now redundant — the term was
named an entire scene earlier — replaced with a callback ("That machine is
what lets the two batches we opened with be read off one pair of axes"),
echoing `b04`'s own "that whole machine has a name" framing rather than
re-explaining it.

**Closing question:** `b06` already ends on an open question pointed at
Part 2 ("What is not yet settled is how much of the batch that curve is
really holding, and how much of it we would have to measure to be sure") —
which is exactly what Part 2's `b09`/`b08` answer. Read this as already
satisfying that part of the ask; left as is rather than rewritten.

### Verification

- `B04` rendered individually at `-ql`: exit 0. Watched via
  `claude-video-vision` end to end — full rig sweep, name card and formula
  write in with no overlap against the panel titles or the live `t=`
  readout, held, fades clean.
- `B06` re-rendered after the trim: exit 0.
- `narration_audit.py` / `preflight.py` on the full seven-scene Part 1 set
  (including `b04`): clean.
- **Not yet done:** a full `chapterB1` draft rebuild through `build.sh` with
  the new scene in the chain (each scene has been validated individually,
  not yet as an assembled master), and the outstanding `-qh`/ElevenLabs
  final pass.

### Verdict — `REVISE` → structural change landed, full master rebuild still pending

---

## Rev 8 — the `chapterB1` master rebuild found a silent audio-dropping bug, not a scene problem

The pending `chapterB1` rebuild from Rev 7 was done, then watched end to end
via `claude-video-vision` `video_watch` (whisper-cpp transcription, installed
this session — it was not previously set up). The transcript disagreed with
`SCRIPT_chapterB.md` in nine places, scattered across `b00`, `b01`, `b02`
(×3), `b03` (×2), and `b07` (×2): whole sentences the script calls for were
simply not spoken. Confirmed as real digital silence, not a transcription
miss, with `ffmpeg silencedetect`/`volumedetect` on the raw track (e.g. a
16 s block at -30 dB across the `b03` gap) and by isolating each gap into
its own clip and re-transcribing alone. Every affected `.mp3` in
`media/voiceovers/` existed, at the right duration, so the TTS pass itself
was fine — the audio was generated and cached correctly and then never made
it into the rendered scene.

**Root cause, in `manim-ce`, not this project's scene code.** Every scene
here is a `VoiceoverScene`; narration is attached by `voiceover/scene.py`
calling `Scene.add_sound()` at the top of each `with self.voiceover(...)`
block. `add_sound()` (`manim/scene/scene.py`) is a hard no-op whenever
`renderer.skip_animations` is `True`. That flag is set by Manim's per-`play()`
caching (`manim/renderer/cairo_renderer.py`) whenever an animation's hash
matches a previous render, and it is **not reset until the next `self.play()`
call** — so it stays `True` across any plain code sitting between two
`self.play()`s, including the `add_sound()` call that opens the *next*
voiceover block. A voiceover block immediately following a cached, unchanged
animation (a static `inspect()` hold was the repeat offender across the
paired dropouts) had its narration silently discarded, while its own
on-screen animation rendered completely normally from that same cache. This
is why `tools/dead_air.py` never caught it: the picture keeps moving, so
nothing reads as dead air — it's narration-less motion, which is exactly
what the note about the "flow feeling offset" was describing. `disable_caching`
was off (the project default), so this could fire on any narrated scene, not
just these eight.

**Fix:** `manim.cfg` now sets `disable_caching = True`, project-wide, with
the mechanism above recorded in a comment next to it. `add_sound()`-driven
narration and Manim's animation cache are incompatible; correctness wins.
`chapterB1` was then rebuilt from a clean slate
(`./build.sh chapterB1 -ql --force`).

### Verification

- Re-transcribed the rebuilt `chapterB1_master.mp4` in full: all nine
  previously-missing sentences are present, in order, at normal pacing, with
  no gap anywhere exceeding an ordinary breath pause.
- `tools/dead_air.py --min 1.5`: clean, both before and after (expected —
  it was never able to see this class of bug).
- `tools/narration_audit.py`: clean, unchanged from Rev 7 (the script text
  itself was never the problem).
- Master duration dropped from 395.5 s to 381.8 s on rebuild. Silence
  removal alone would not explain that — `self.across()` sizes run_time from
  `tracker.get_remaining_duration()`, independent of whether `add_sound()`
  succeeded, so the stale caching was also drifting some animation timings,
  not only dropping audio. Not investigated further since the rebuilt master
  is a full re-render, not a patch.

### Scope note

This bug is in `manim-ce`, so it can affect **any** cached render across
this repo, not just `chapterB1`. `chapterB_master.mp4` (full chapter,
built 2026-08-08 10:20) and every `-qh`/ElevenLabs render under
`media/videos/**/1080p60/` predate this fix and have not been re-verified.
`chapterB1` was rebuilt because it's what was asked for; a full `chapterB`
rebuild (and the paid ElevenLabs `-qh` pass) is a follow-up, not yet done.

### Verdict — `REVISE` → root cause fixed and verified on `chapterB1` draft;
full-chapter and final-voice rebuilds still pending

---

## Chapter C C01–C03 — computation, motion, and redundancy pass (updated 2026-08-13)

### Result

- C01 opens on Chapter B's actual Epps–Pulley equation and two computed scalar
  examples. It then introduces fifteen 5×7 pixel digits and a
  `35 → 8 → 6 → D` network based specifically on 3Blue1Brown's 2017 neural
  network code. A selected image's literal pixels become the 35 input neurons;
  all layers activate and complete edge groups propagate. Seven representative
  images run slowly enough to read before the compact batch appears. The output
  grows from one centred neuron to two and then three, and the same dots move
  line → plane → centred cloud. No matrix competes with the geometry. Narration
  calls the result only **the score**, keeping it distinct from frequency `t`.
  `Z` appears only after the cloud exists; the scene ends by adopting
  `N(0,I_D)` as the target, not by asking an explicit transition question.
- C02 narration is now 158 words. It begins with C01's exact
  fifteen points, expands to the full cloud under narration, and limits the
  pairing field to 32 emphasized pairs. The shape ladder, resampling,
  cancellation, origin pull, and equation each carry the corresponding spoken
  claim; the reported holds contain narration and intentional inspection
  rather than dead air.
- C03 now preserves dot identity from cloud to shadow to scalar line, runs the
  same three-panel computation, introduces the target and weighted gap in
  order, returns the bare number `0.055`, and only then names it
  `score(u)=0.055` beside the restored direction.
  A Cairo fixed-orientation registration leak found in extracted frames was
  fixed before approval.

### Verification

- Current durations: C01 final 46.22 s; C02 final 56.87 s;
  C03 draft 34.13 s.
- `dead_air.py --min 1.5 --frozen`: no dead air. Short reported still windows
  all contain active narration and a settled mathematical state.
- `narration_audit.py`: all budgets pass (386 spoken words total; C01 140,
  C02 158, C03 88).
- `preflight.py`: no undefined names; `py_compile` passed.
- `facts.py`: 24/24 claims hold.
- C01 final render inspected from real 1920×1080 frames across the equation,
  both score examples, the pixel-to-input transform, whole-network propagation,
  seven-input loop, full-network propagation, the `D=1 → D=2 → D=3` geometry
  growth, the `D=4 → D=6 → D=8` width demonstration, the late `Z` reveal, and the
  final cloud. It has 60 fps H.264 video plus 48 kHz stereo AAC audio and runs
  46.22 s. The troublesome spoken “encoder” was replaced with “a neural
  network” and the ElevenLabs delivery was regenerated.

### Delivery scope

C01 and C02 received authorized final ElevenLabs passes. This delivery-scope
note was superseded by C03's authorized final pass recorded below.

---

## Chapter C C03 — owner-directed pedagogical and final-delivery pass (2026-08-16)

### Result

- Rebuilt the scene around the actual problem: Epps--Pulley accepts scalars
  while the model supplies vectors. The opening now says “in the last chapter”
  rather than naming a lettered chapter, and shows the required `R^D -> R`
  bridge before introducing projection notation.
- Camera movement is now tied to mathematical changes: one move establishes
  the scalar/vector contrast, another reveals the first perpendicular
  projection, and the final two moves accompany actual changes in `u`. This
  follows the local 3Blue1Brown pattern of concrete example, rhythmic batch,
  then aggregate result rather than using ornamental continuous rotation.
- The direction glyph is genuinely one data-unit long. A separate infinite
  line spans the cloud, so the picture no longer contradicts the claim that
  `u` is normalized. The final revision measures the arrow against the actual
  displayed axes (ratio `1.000000`) and shows `||u||=1`; the projection line is
  thinner and quieter so it cannot be mistaken for the arrow.
- One embedding is projected first, with a perpendicular guide, signed foot,
  and computed `u^T z_i = +1.93`. A second point then lands behind the origin
  and changes the readout to `u^T z_j = -1.53`. Only after both sign cases are
  visible do 44
  representative guides and all 220 projected dots form the scalar shadow.
- Those same dots become the number-line batch accepted by the established rig.
  The `t` sweep now completes the empirical characteristic function before the
  standard-normal target appears exactly on its spoken phrase. Only then does
  the weighted-gap sweep begin. A moving
  red segment explicitly marks the instantaneous curve separation while the
  weighted squared gap fills behind `t`.
- The red gap formula now clears before the green score appears. The final rig
  contraction restores the clean cloud, unit direction, and complete shadow.
  The scene then turns the same finite cloud through three directions and
  recomputes the exact scores `0.055`, `0.046`, and `0.872`, so the limitation
  of one shadow is demonstrated rather than merely stated. The alternate
  numerical values remain on screen but are no longer narrated; the ending is
  now a direct contrast between one shadow and the whole cloud.
- The rewritten narration restores conversational connective language—“so,”
  “suppose,” “if,” “then,” “now,” “wherever,” and “but”—through the complete
  causal chain.

### Verification and delivery

- Final file: `media/videos/c03_one_shadow/1080p60/C03.mp4`.
- H.264 1920×1080 at 60 fps; AAC 48 kHz stereo; 112.77 s; Archer ElevenLabs
  narration.
- Complete ffmpeg decode passed. The `-45 dB`/2.2 s silence scan reported no
  qualifying dead air.
- Fresh 1080p frames were inspected across the opening contrast, `R^D -> R`
  bridge, unit direction, single projection, representative batch guides,
  shadow-to-rig handoff, frequency sweep, moving target/gap marker, score
  reveal, contraction, and all three final direction examples. No projection
  ghosts, rig ghosts, clipped type, or persistent overlaps remain.
- `py_compile` passed; `preflight` reports no undefined names;
  `narration_audit` passes every budget (C03: 358 spoken words); `facts.py`
  passes 24/24.

### Verdict — `PASS`
