# Chapter B — render review

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

*fingerprint* appeared 24 times across 8 scenes, first asserted flat in `b02`
("That curve is the fingerprint of this batch") five scenes before the
uniqueness theorem that licenses it. [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md)
§17 requires it be reserved for the theorem and qualified there. Now **5 uses
across 3 scenes**, introduced in `b09` at the moment the theorem is stated:

> *Because the curve determines the distribution completely, calling it a
> fingerprint is accurate rather than decorative, and that is the sense the
> word carries for the rest of the video.*

Before `b09` the object is called what it is: the characteristic function, or
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
| Scope | 12 captions across 6 scenes: `b00` *"Two numbers cannot see a shape"*; `b06` *"where the distribution sits lives in the phase / how spread out it is lives in the magnitude"*; `b09` *"we do not conclude the distributions are similar / We conclude they are equal"*; `b10` *"we did not choose the arrows because they were elegant / we chose them because gradients flow through them"*; `b11` *"this single fact does all the work"*; `b12` *"Representations are not numbers / They are vectors, in hundreds of dimensions"*. |
| Fix applied | Each replaced by the compressed statement §7.2 assigns to the screen — notation or result, not rhetoric. `b10`'s two lines became `histogram: d(count)/dx = 0 almost everywhere` / `wrapped sample: d/dx = i t · e^{itx}, never zero`, which is the actual argument rather than a claim about it. |

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

`b01`'s cancellation demonstration drew six unit arrows as bare `Line`s. Six
evenly spaced lines through a circle's centre read as three diameters, so
*"they cancel"* — the sentence the whole chapter turns on — had no visible
referent. Now `Arrow` with a tip. VISUAL_SYSTEM.md §5.

### F14 — `t` axis label inside the safe margin · **LOW** · closed

Placed `DR` of the last tick, which put it 0.1 units from the frame edge and
read as clipped at 480p. `layout.fit_in_frame` existed and was never applied to
it. Now `UR`, with `fit_in_frame` as a backstop since `t_max` is a caller
argument.

### F15 — `b02` had its own copy of the rig's axis labels · **MEDIUM** · closed

Found only because the fix for F14 landed in `ThreePanelRig.axis_labels()` and
`b02` still rendered a clipped `t` afterwards. `b02` duplicated that method
line for line — including `font_size=20`, below the readability floor — so the
shared fix reached `b05`, `b06`, and `b07` and left `b02` on the old geometry.

This is the drift `rig.py`'s own docstring warns about, in the one scene where
the rig is introduced. The readout was duplicated too, in `TARGET` — the colour
that means *the Gaussian reference* everywhere else in the chapter. Both now
call the shared helpers.

**Lesson recorded because it will recur:** a fix to shared geometry is not
verified by looking at one scene. After changing `common/`, check a frame from
*every* scene that uses it.

### F16 — Both outer rig panels overhung the safe margin · **MEDIUM** · closed

Found by checking `b06` and `b07` after F15, which is the only reason it was
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
| O2 | 00:02:50 `b02` | Clarity (§5.2) | LOW `[RES]` | Downgraded from MEDIUM. The perceived imbalance was mostly F16; what remains is ~1.5 units of empty band above the panel captions, which §8.2 says is not in itself a defect. | Leave. Re-judge at 1080p. |
| O3 | 00:00:38 `b00` | Pacing (§10.2) | ~~MEDIUM~~ **closed** | The scene's final 13 s hold one static frame while the closing sentence plays. §10.2: a pause is dead air when nothing new can be inspected. | **Closed at rev 3.** `b00` was rebuilt; the gap between the clumps is now shaded from the data (`layout.widest_gap()`) and the scene ends on the pipeline rather than a hold. |
| O4 | `b11` | Pacing (§7.5) | MEDIUM `[VOICE]` | 2:59 against a chapter mean of 1:30; `PLAN.md` §5 itself calls this derivation an appendix. | Judge on the ElevenLabs pass — draft TTS pacing is not evidence. Do not cut `b08` or `b12` first; both are load-bearing. |
| O7 | chapter | Pacing (§7.5) | MEDIUM | **Runtime grew: 18:02 → 19:16, +74 s (+6.8%).** `NARRATION_SPEC.md` §6 and §13 require that operations carry their reason and that fragments be joined into connected sentences; doing that raised mean sentence length from 11 to 15 words. Smaller than feared — `b11` and `b12` both got *shorter* — but Chapter B was already long against an ~8 min plan. | **User decision — flagged, not silently resolved.** Cutting the reasoning back out would undo the rewrite. The levers: (a) accept 19:16; (b) split B into two videos at `b09`, a natural seam — construction, then consequences — giving roughly 9:30 and 9:45; (c) demote `b11`'s derivation to an appendix, which `PLAN.md` §5 already contemplates. Recommendation: **(b)**. |
| O5 | `b08` | Proof status (§6.4) | MEDIUM | The 1/N sampling-floor claim is `empirical_observation` in `concepts.yaml`, verified in `facts.py`, and narrated with "settles at". Correct, but the animation shows one clean convergence. | Confirm on the HD render that no visual implies more than the label allows. |
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
| `b01_arrows` | 1:24 | 1:31 | +0:07 | F13 arrows without tips; F8 appositive ×3. Arrowheads make the cancellation demonstration legible for the first time. |
| `b02_the_rig` | 0:41 | 1:01 | +0:20 | F9 *fingerprint* asserted 5 scenes early; F15 duplicated axis labels; F16 clipped panel. Now closes on the open question rather than the label. |
| `b05_real_and_imaginary` | 1:16 | 1:24 | +0:08 | F3 target curve unreadable at 480p; slogan close. |
| `b06_worked_examples` | 1:26 | 1:32 | +0:06 | F7 *"That split is worth remembering."* → the phase/magnitude split now stated as the fact `b11` will use. |
| `b06a_one_speed_fails` | 0:33 | 0:42 | +0:09 | F7 *"One frequency can be fooled."* → the aliasing mechanism named. The counterexample itself was strong and was kept. |
| `b07_the_anchor` | 1:03 | 1:04 | +0:01 | F7 *"No scale to ask about."* → why a shared start makes two curves comparable. |
| `b08_which_frequencies` | 2:08 | 2:24 | +0:16 | F8 *"the most useful thing in this chapter"*; λ now named a bandwidth parameter, per the source. O5 open. |
| `b09_uniqueness` | 1:31 | 1:39 | +0:08 | F9 — the metaphor is now **introduced** here and qualified by the theorem. Proof debt stated plainly. |
| `b10_why_not_histograms` | 1:48 | 1:50 | +0:02 | F7 slogan close; the three objections are now numbered by the argument, and the third is flagged as the one that matters. |
| `b11_gaussian_fingerprint` | 2:59 | **2:49** | **−0:10** | O4 length. Got *shorter* — the derivation was carrying commentary about itself. |
| `b12_fingerprint_to_loss` | 2:43 | **2:35** | **−0:08** | F7 *"We did not invent it, we rebuilt it."* Also shorter. |

Growth is concentrated in the four scenes that had the least reasoning per
sentence to begin with; the two densest scenes contracted.

---

## Rev 3 — Part 1 (`chapterB1`)

| | |
|---|---|
| Artifact under review | `videos/sigreg_explainer/chapterB1_master.mp4` |
| Scope | **Part 1 only**: `b00 b01 b02 b05 b06 b06b b06a b07`. Part 2 (`b08`–`b12`) is unchanged and still at rev 2. |
| Reviewed at | 854×480 draft, macOS `say` (**Evan (Enhanced)**, changed from Samantha) |
| Duration | **8:31** (511.4 s) across 8 scenes |
| Typeface | Latin Modern Roman throughout, regular weight only |
| Mechanical checks | 8/8 scenes carry an audio stream, each within 0.72 s of its video duration (`B06` 2.0 s, a silent tail); **0 silence gaps > 2.5 s**; 30,696 frames at 60 fps; **0 empty-screen stretches ≥ 1 s** (`tools/dead_air.py`) |
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

- **Correction 1 is demonstrable.** `b02`'s curve visibly dips below zero near
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
| R3 | `b06a` | Clarity (§5.1) | LOW | The batch runs to ±6.28 on a ±6 axis, so the two outermost samples hung off the ends of the line they sit on. | **Fixed.** Axis widened to ±7. |
| R1b | `b00` | Redundancy (§7.2) | MEDIUM | The **first** fix for R1 put the words *"a description of the whole distribution"* on screen — which is what the narration says at that exact moment. Straight channel redundancy, and the newly-gating on-screen slogan scan caught it immediately. The gate was right and the fix was wrong. | **Fixed.** Replaced by `samples → ? → one differentiable score`, which names the two fixed ends and marks the middle as the unknown. It says something the voice does not, both constraints are then visibly constraints on that middle box, and the scene closes by resolving the `?` rather than drawing a second pipeline beneath the first (§7.3). |
| R5b | `b01` | Pacing (§10.2) | **HIGH** | **The last 14 seconds are a completely static frame** — six motionless arrows and a fixed `length = 0.00` — while the closing sentence makes a claim about a *range*: "one when they coincide, zero when they are spread evenly, and something in between otherwise". The in-between case was never shown anywhere in the chapter. `dead_air.py` cannot catch this: there is content on screen. This is precisely the class §10.2 reserves for a human pass, and it was found by watching. | **Fixed.** The six arrows now sweep continuously between coincident and evenly-spread with the length tracking live, so the sentence and the picture make the same claim. The readout is a static word plus a `DecimalNumber` rather than a rebuilt `ty.line` — `Text` goes through Pango on every construction, and rebuilding one per frame at 60 fps is a slow-render trap. |
| R4 | chapter | Taste (§8.3) | MEDIUM | **`ty.line()` misaligns mixed baselines when a word carries a descender.** It aligns every part to the bottom edge of part 0; a `Text` containing "y" or "p" extends below the baseline, so adjacent `Tex` digits sit visibly low. Clearest at `b05` 01:04 — the `0` in *"X symmetric about 0"* drops below the line. Affects ~30 call sites. | **Open.** Real but cosmetic. Fixing it means baseline alignment rather than bounding-box alignment, which manim does not expose directly, and it would require re-rendering and re-checking every scene. Deferred deliberately rather than churned immediately before a commit. |
| R5 | `b02` | Taste (§8.2) | LOW | For the first ~9 s the unrolled sample line extends well past the circle panel it belongs to, reading as loose dots with no line under them. Pre-existing, not introduced by the refactor; it resolves as the wrap animation runs. | **Open.** Re-judge at 1080p. |
| R6 | chapter | Pacing (§7.5) | NOTE | Runtime came in at **8:31** against the agreed 9–10 min. Under, not over. The redundancy audit cut more than the corrections added. | **User decision.** Not padded to hit a number. If more time is wanted, `b02` and `b06a` are where inspection silence would buy the most — both carry the chapter's load-bearing arguments. |

### Runtime, per scene

| Scene | Rev 2 | Rev 3 | Δ |
|---|---|---|---|
| `b00_the_problem` | 0:46 | 1:23 | +0:37 — rebuilt |
| `b01_arrows` | 1:31 | 1:16 | −0:15 |
| `b02_the_rig` | 1:01 | 1:11 | +0:10 |
| `b05_real_and_imaginary` | 1:24 | 1:18 | −0:06 |
| `b06_worked_examples` | 1:32 | 0:48 | −0:44 — split |
| `b06b_what_magnitude_ignores` | — | 0:53 | new |
| `b06a_one_speed_fails` | 0:42 | 0:54 | +0:12 |
| `b07_the_anchor` | 1:04 | 0:50 | −0:14 |
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
- **`b06a`.** Constructing a batch that a single frequency reads as fully
  collapsed is a genuine counterexample, not an illustration — it earns the
  sweep instead of asserting it.
- **`b08`'s twenty draws from a true Gaussian.** Showing the sampling floor
  rather than claiming it is the strongest §6.4 moment in the chapter.
- **`b11`'s derivation** arriving at a differential equation from `p' = -x p`.
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
| Scope | **Part 1 only**, now **six scenes**: `b00 b01 b02 b06 b06a b07`. Part 2 is untouched and still at rev 2. |
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
2. **The rig was torn down and rebuilt at every seam.** `b02`, `b05`, `b06`,
   `b06b` and `b07` all use the same three-panel rig, each rendered as its own
   MP4 ending in `clear_beat()`. At 00:03:19 of the rev-3 master the viewer
   watches a live rig fade to background and an almost identical one appear one
   second later with different captions and a different batch. That is a cut
   between episodes, drawn in the middle of one investigation.
3. **Roughly a fifth of the runtime was a motionless picture with narration
   over it.** Not blank — full, and frozen, which is why every gate passed it.

### Structural changes

| Change | Why |
|---|---|
| **`b05_real_and_imaginary.py` folded into `b02`, source deleted** | One rig, one batch, no cut. `b02` builds the curve; the same rig then notices the curve was only one of the average arrow's two coordinates. The merged scene also drops `b05`'s private `SKEWED` batch — the seven-value clump slice `b02` already runs is lopsided enough (`max|Im φ| = 0.375`), so the data no longer changes at the exact moment the point is that the curve was hiding something about *this* data. |
| **`b06b_what_magnitude_ignores.py` folded into `b06`, source deleted** | Same rig, third question. |
| **`b07` rewritten as the payoff** | `φ(0) = 1` is proved as before, and then **`b00`'s two batches** — the same forty numbers, from the same fixed seeds — go through the rig one after the other. Their curves are nothing alike: the hump decays and never goes negative (min +0.009), the clumps swing to **−0.647**, and the widest gap is **0.764 at t = 2.94**. Both leave from 1, which is what `φ(0) = 1` is *for* and why the two curves can be read off one pair of axes without rescaling. Verified in `facts.py` as `toy_batches_have_different_curves`. |
| **`b00` rebuilt around the same thread** | The rev-3 cut ended on an amber question card held motionless for twelve seconds — a third of the scene, saying in text what the voice was saying at that instant. The two batches now shrink into the left end of a pipeline `→ ? → one score`, each constraint is written under the arrow it constrains, and the `?` resolves. |
| **Sources deleted rather than orphaned** | A stale duplicate of shared geometry is finding F15's failure mode. Git has the history. |

The toy experiment is now the spine: named in `b00`, returned to on the rig in
`b02` ("back to the two clumps from the start"), and **answered** in `b07`.

### The systemic finding

**S1 — `across(tracker, Indicate(...))` was the project's dominant source of
frozen frames.** · **HIGH** · fixed at ~20 sites

`ActScene.across()` exists to give an animation the whole narration clip instead
of a literal `run_time`. It was overwhelmingly being handed an `Indicate` — a
one-second gesture at `scale_factor` 1.02–1.15. Stretched over eight seconds of
speech that is not a gesture, it is a still frame. Measured examples on the
rev-3 master: `b01` 01:34–01:44 (six motionless arrows under a sentence about
arrows spreading), `b06` 00:47–00:56 (six dots pulsing 12% at `t = 0`), `b07`'s
entire closing tableau.

Second form of the same bug: **a fixed-length `self.play(...)` followed by
`wait_until_bookmark`.** Whatever is left of the clause between the two plays is
a held frame. `b02`'s opening ran fourteen seconds that way.

Both are now written as `across(..., reserve=<tail>)` with the animation sized
to the clause, and the filler animations are gone — every one replaced by
something the sentence is actually about:

- `b01`'s averaging beat is one `ValueTracker` from coincident (length exactly
  1) through roughly-agreeing (0.98) to evenly spread (exactly 0, the sixth
  roots of unity), with the readout counting down live. The three stages that
  used to be static-transform-static are the same tracker at different values.
- `b02` stretches the unrolled strip as `t` grows, because the strip's length
  *is* `t` times the batch's range — so "multiplying by a frequency" is watched.
- `b07`'s gap between the two curves is a live measurement that opens and closes
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
| `b01_arrows` | 1:24 | 4.8 s |
| `b02_the_rig` | **2:41** | **0.0 s** |
| `b06_worked_examples` | 1:20 | 6.2 s |
| `b06a_one_speed_fails` | 0:55 | 0.0 s |
| `b07_the_anchor` | 1:30 | 6.6 s |

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
changed (`b07`'s `inspect(1.8)` on the finished comparison, `b06`'s flat line at
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
| N4 | `b02` | `swap()` would have raised on `remove(None)` — this scene builds the rig by hand rather than through `mount()`, which is what normally records the panel-1 dots, and the folded-in symmetry beat calls `swap()`. | **Fixed** before the first render of the merge. |
| N5 | `b02` | The strip stretch was a monotone creep: about one pixel per frame, below the threshold at which anything looks like motion. | **Fixed.** Overshoots past the target and settles. |
| N6 | `voiceover/services/base.py` | **Editing only the bookmarks in a passage reused the previous entry's bookmarks.** The TTS cache keys on the bookmark-*stripped* text — correct, since moving a bookmark changes no audio and must not re-spend the budget — but `VoiceoverTracker` reads bookmark positions out of the cached entry's `input_text`. Re-marking a sentence whose words were unchanged therefore either timed the bookmarks at their old positions **silently**, or raised `There is no <bookmark mark='count'/>` from inside the render, twenty minutes in, with nothing pointing at the cache. Hit for real in this revision. | **Fixed.** `_wrap_generate_from_text` overwrites `input_text` with what the scene actually asked for, before the cache-hit early return so it covers hit and miss alike. The key is untouched, so bookmark edits are still free. |

### Also closed

- **R5** (rev 3, open) — the unrolled sample line had nothing under it for the
  first nine seconds. `ThreePanelRig.roll_curve()` now draws the line being
  rolled, from the same `wrapped()` call as the dots, so it cannot disagree with
  where they land. The samples are carried onto it by `TransformFromCopy` rather
  than both appearing at once.
- **`b02`'s number line** was `(-2, 2)` where every other rig scene uses
  `(-3, 3)`, which put this batch's largest sample on top of the end tick and
  changed the line's width at the old `b02`/`b05` cut. Now consistent.
- **Panel-1 stacking is in the rig**, not copied. `b07` shows two real
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
| O9 | chapter | Redundancy (§7.2) | LOW | `narration_audit`'s on-screen scan reports 2 slogan-shaped captions, both in **Part 2** (`b09` *"one frequency asks one question"*, `b12` *"this is the Epps–Pulley statistic"*). Pre-existing and outside this revision's scope; Part 1 scores 0. | Fix when Part 2 is re-cut. It is the only check over budget. |
| O10 | Part 1 | Pacing (§7.5) | NOTE | Runtime grew to 9:01 from 8:31. The growth is `b07`'s payoff and `b00`'s restored middle; the merges themselves were roughly runtime-neutral. | **User decision.** Nothing here is padding, but if Part 1 must come in under nine minutes, `b06a` is the least load-bearing minute. |
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
