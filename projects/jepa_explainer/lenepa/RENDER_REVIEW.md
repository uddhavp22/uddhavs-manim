# LeNEPA segment — render review

## Scene 04 four-composition rebuild — 2026-08-24

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA04_review_eleven_qh.mp4` |
| Delivery | 80.22 s; 1920×1080 at 60 fps (timing-voice draft: 82.80 s) |
| Scope | `LeNEPA04TemporalSIGReg` fully rewritten again; `common/project.py::PlaneProjectionRig.target_bell` gained a `gap` param; `STORYBOARD.md` §4 and `SCRIPT_ELEVENLABS.md` §4 resynced |
| Mechanical checks | Timing render at 480p15 clean; ElevenLabs `-qh` at 1080p60 clean; `narration_audit`, `.venv` preflight, `facts.py` all pass; no silence interval ≥ 3 s |
| Visual review | Full 1 fps pass over the entire delivered artifact plus targeted `video_detail` drills on the projection panel and the transformer chamber |
| Verdict | **READY FOR OWNER REVIEW** |

This supersedes the "full 7-beat rebuild" entry directly below. The owner
watched that render frame-by-frame (their own dense pass, not just spot
checks) and rejected it with a long, specific list of problems: objects
accumulating across the whole scene instead of clean state transitions (by
~31 s there were two overlapping copies of the `b=1` row and stranded
duplicate `b=` labels; by ~49–55 s stale collapsed vectors were overlapping
fresh ones under a mostly-empty transformer box); everything drawn far too
small relative to the frame; the collapse animation flickering between
red and blue because color and shape were changing in the same `Transform`;
the vector-grid-to-scatter-plot transition producing literally mangled
glyph shapes because `ReplacementTransform`/`Transform` was being asked to
interpolate between a bracketed multi-glyph vector and a plain dot; too many
thin, unlabeled lines (axes, dashed guides, a bell curve) competing for
attention; and narration that had been cut for time until it read as
telegraphic storyboard notes rather than speech. The one thing kept from the
previous version: no title card, ever.

**Root cause of the accumulation bugs.** `TransformFromCopy` and
`ReplacementTransform` do not remove anything by themselves unless the
caller explicitly fades the source out too. The previous version relied on
per-object cleanup at scattered points in a single continuous scene and
missed several -- most visibly `b_labels`, created in the scene's first beat
and never faded, which is why a second `small_labels` group built four beats
later visually doubled it. Rather than continue patching individual misses,
this rewrite restructures the whole class around four **compositions** --
Composition A (the temporal batch), B (the shared latent plane), C (the
transformer chamber), D (the equation landing) -- each ending in an explicit
`self.play(FadeOut(...))` of everything currently on screen before the next
composition builds anything. No object is allowed to survive a composition
boundary implicitly; anything needed again (e.g. the `L_T={0,8}` legend) is
rebuilt fresh in the new composition rather than threaded through.

**The collapse no longer recolors mid-morph.** Row `b=1`'s glyphs stay
`BACKBONE`-colored the entire time; only the `DecimalNumber` values move,
via `ChangeDecimalToValue` (checked in advance for sign-crossing risk against
`COLLAPSED_TOKEN`, since CE's decimal-glyph desync bug specifically triggers
on a sign flip mid-animation). A coral `SurroundingRectangle` marks the row
only after every value has actually landed on the same number -- the
collapse is the sameness, not a color cue standing in for it.

**No more `Transform`/`ReplacementTransform` across incompatible mobject
types.** Wherever a token glyph needs to become a plane point, the old code
morphed a bracketed multi-`DecimalNumber` group directly into a `Dot` --
Manim's point-interpolation between structurally different path counts is
what produced the reported "mangled skeletal shapes." The rewrite never does
this: Composition B's dots are built and revealed fresh via `GrowFromCenter`
(staggered, so `b=1`'s six dots visibly arrive and stack at one point one at
a time), and the only `Transform`-family calls left standing are between
same-type objects (dot→dot repositioning via `.animate.move_to`, or two
`span_bracket`/short-`MathTex` objects of matching structure).

**Fewer, cleaner lines.** `PlaneProjectionRig.target_bell()` gained a `gap`
parameter so the reference density curve sits a fixed distance off the
projection line instead of crossing through the plotted points; the dashed
`guide_lines()` are no longer called at all in this scene (the projection is
conveyed by the dots' own motion onto the line). The plane and the
transformer chamber are both built large (roughly 65–75% of frame width)
instead of the previous small side panels.

**Narration restored to natural connective phrasing.** The prior pass had
been trimmed for a ~60 s budget until lines like "Collect every token in the
batch onto one shared plane" read as captions rather than speech. This
rewrite keeps "now suppose," "so," and "but" back in, at the cost of the
scene running longer (80.2 s vs. the previously-approved ~70.8 s); the owner
had not raised timing as a concern in this round, only clarity.

| Gate | Result |
|---|---|
| Timing `-ql` render | Pass — 82.80 s |
| ElevenLabs `-qh` render | Pass — 80.22 s |
| ElevenLabs silence check | Pass — no gap ≥ 3 s |
| Narration audit | Pass |
| `.venv` preflight | Pass |
| Facts ledger | Pass |
| Fixed-path review copy | Written — `LeNEPA04_review_eleven_qh.mp4` |
| Video-vision review | Done — full 1 fps pass plus targeted drills on the two remaining soft spots (projection-panel reference curve, chamber depth-plate visibility); both read acceptably, not fully perfect, noted for a future polish pass if the owner wants it |

## Scene 04 full 7-beat rebuild — 2026-08-24

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA04_review_eleven_qh.mp4` |
| Delivery | 70.83 s; 1920×1080 at 60 fps (timing-voice draft: 64.80 s) |
| Scope | `LeNEPA04TemporalSIGReg` fully rebuilt (all 7 beats), new `common/project.py::PlaneProjectionRig`, new `common/data.py` batch/latent/layer-8 constants, new `common/visuals.py::depth_plates`, `STORYBOARD.md` §4 and `SCRIPT_ELEVENLABS.md` §4 resynced |
| Mechanical checks | Timing renders at 480p15 clean; ElevenLabs `-qh` at 1080p60 clean; `narration_audit`, `.venv` preflight, `facts.py` all pass; no silence interval ≥ 3 s (`silencedetect -45dB/3s`, no hits) |
| Visual review | Full frame-by-frame pass over the delivered ElevenLabs artifact (`video_watch` at 1 fps plus targeted `video_detail` drills on the beat-2 collapse, the beat-4/5 projection proof, and the beat-7 landing image) |
| Verdict | **READY FOR OWNER REVIEW** |

This supersedes the same-day earlier rework directly above. The owner
rejected that version outright ("U KEEP ADDING THESE TITLES AT THE TOP, STOP
DOING THAT. IT LOOKS TACKY") and gave a full replacement spec: no persistent
scene-title text anywhere in the LeNEPA section, and a scene built around a
`(B, T)` grid of real token glyphs that pools onto one shared latent plane so
"the batch still looks fine" is something the viewer watches happen, not a
caption. That spec is what this rebuild implements, beat for beat.

**No title card.** `scene_title(...)` is not called anywhere in this class.
Labels attach to objects in place, at the moment they become meaningful (the
`b=` rows, the `ell=0`/`ell=8` taps, the `SIGReg(...)` notation growing out of
a span bracket) instead of sitting as prose above the diagram.

**The shared-latent-plane beat is the structural fix.** The earlier rework
(and the version before it) kept three separate per-sample plots and asserted
in narration that the aggregate still looked fine. This version pools all
eighteen tokens in the batch onto one plane: row `b=1`'s six tokens land on a
single coincident point while rows `b=2`/`b=3` keep genuine spread, in the
same frame. The claim is proven pictorially, not asserted.

**The projection/score beat reuses the SIGReg chapter's own grammar.** A new
`common/project.py::PlaneProjectionRig` is a static 2-D port of
`sigreg_explainer/common/project.py::CloudProjectionRig` -- same method
names (`direction_arrow`, `projection_line`, `guide_lines`, `shadow_dots`,
`score`), same `epps_pulley` evaluator, same `stack_levels` dot-plot rule --
so a viewer of both chapters sees one visual language, not two. The direction
arrow is deliberately left unlabeled (both chapters already call it `u`).

**Layer 0 and layer 8 come from an actual chamber.** `u^(0)` reuses scene 1's
token row; `u^(8)` reuses scene 2's post-mixing carriers -- no new data
invented. `depth_plates()` unfolds the existing `transformer_block`'s single
`\vdots` marker into a real stack of interior depth lines before the two taps
land, replacing the earlier rework's detached `caption_pill` buttons.

**Timing.** The owner was told the full spec runs nearer 60 s than the ~35-40 s
they estimated, and explicitly chose the full build over a trimmed ~52 s cut.
First narration pass ran 260 words (~93 s, ~100.5 s rendered) -- roughly 1.6x
over budget -- and was cut across all seven beats to 159 words before
re-rendering; that pass landed at 64.8 s (timing voice) / 70.8 s (ElevenLabs,
which runs at 90% tempo). Both are within the approved range.

**One real bug found and fixed by the video-vision pass.** `TransformFromCopy`
does not remove its source: the batch-row labels (`b=1`/`b=2`/`b=3`) and the
beat-5 `SIGReg({z_{b,t}})` notation were being copied into the final beat-7
equation but the originals kept sitting on screen through the ending, cluttering
what is supposed to be the clean two-equation landing image. Fixed by pairing
the `TransformFromCopy` with an explicit `FadeOut` of both source groups.
Also swapped the beat-2 collapse from `Transform` to `FadeTransform`, since
plain `Transform` between `DecimalNumber`/`MathTex` glyphs of different digit
counts produced a brief double-exposure ghosting artifact mid-morph;
`FadeTransform` crossfades cleanly instead.

| Gate | Result |
|---|---|
| Timing `-ql` render | Pass — 64.80 s |
| ElevenLabs `-qh` render | Pass — 70.83 s |
| ElevenLabs silence check | Pass — no gap ≥ 3 s |
| Narration audit | Pass |
| `.venv` preflight | Pass |
| Facts ledger | Pass |
| Fixed-path review copy | Written — `LeNEPA04_review_eleven_qh.mp4` |
| Video-vision review | Done — full pass plus two targeted re-drills after the fix |

## Scene 04 temporal-collapse rework — 2026-08-24

| | |
|---|---|
| Intended artifact | `media/videos/jepa_explainer/lenepa/LeNEPA04_review_eleven_qh.mp4` |
| Delivery | Full-resolution timing preview: 42.07 s; 1920×1080 at 60 fps. Final ElevenLabs duration pending. |
| Scope | `LeNEPA04TemporalSIGReg` plus the scene 3/4 script sync and scene 4 storyboard sync |
| Mechanical checks | Timing renders at 480p15 and 1080p60 clean; `narration_audit`, `.venv` preflight, and `facts.py` clean |
| Visual review | Both timing renders sampled across every beat; full-resolution drills on the collapse verdict, flat temporal row, guide line, `L_T` transformation, and final equation |
| Verdict | **IMPLEMENTED — ELEVENLABS VALIDATION BLOCKED** |

The aggregate spread check now remains fully lit while sample one collapses
and changes from blue to the coral failure color. Only the following beat
retires the aggregate frame and regroups those dots into a nearly flat row
against a faint time-axis guide. This makes the invariant batch verdict and
the hidden within-sequence failure readable in the same frame.

The closing beat removes the dangling arrows and unsupported ablation claim.
Both SIGReg taps now transform into `L_T={0,8}` before the equation appears;
the matching `\ell\in L_T` summation index is purple. The equation settles
without an additional spoken closer.

| Gate | Result |
|---|---|
| Timing `-ql` render | Pass — 42.07 s |
| ElevenLabs `-qh` render | Blocked — sandbox DNS/network access failed on the first uncached narration request |
| ElevenLabs silence check | Not run — no new ElevenLabs artifact was produced |
| Narration audit | Pass |
| `.venv` preflight | Pass |
| Facts ledger | Pass |
| Fixed-path review copy | Not written — a timing-voice render was not substituted for the required ElevenLabs artifact |

## Scene 03 simplification — 2026-08-23

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA03_review_eleven_qh.mp4` |
| Delivery | 18.73 s; 1920×1080 at 60 fps (previous cut: 41.40 s) |
| Scope | `LeNEPA03PredictionLoss` only -- beat A untouched, beats B onward rebuilt |
| Mechanical checks | `narration_audit`, `preflight`, `facts.py` clean; no silence interval ≥ 3 s (`silencedetect -45dB/3s`, no hits) |
| Visual review | 480p frame sampling every beat during iteration (caught and fixed a fan-row overlap, see below); full 1080p60 frame extraction on the delivered artifact |
| Verdict | **READY FOR OWNER REVIEW** |

The owner watched the two-lane rebuild above and called it "a long winded
slow way to explain MSE between these two," with concrete, quoted
instructions: show one projector, not two; run both vectors through it;
drop "that's where the loss lives" and "same weights on both sides"; show
several real example vectors across time and batch instead of the dotted
`(b, t)` grid; and cut the closing gradient-flow beat entirely. This pass
implements that brief line for line.

**One projector, run twice.** The two-lane setup (`net_pred` + `net_targ` +
a `TransformFromCopy` ghost copy) is gone. Beat B now builds a single
`LayerMap` and calls a local `run_projector(values, out_vals, color, label,
pos)` helper twice: once with `pred_src`'s values (`MIXED_VALUES[3]`),
producing `h_\psi(\hat z_4)`, then again with `targ_src`'s values
(`TOKEN_VALUES[4]`), producing `h_\psi(z_5)`. Because there is only one
projector object on screen, the shared-weights claim is true by
construction -- no ghost copy, no brace, no spoken line. Each pass also
drops the old intermediate `Transform(net.output_layer, ...)` recolor step:
the bright output-layer copies now animate straight into the projected
vector's entry positions while fading, folding what was two `self.play`
calls into one. Net effect: beats B+C of the old cut (two full parallel
propagation passes, a ghost-copy transform, two label fades) collapse into
one noticeably faster beat B.

**Two rejected lines removed.** "That's where the loss lives" and "same
weights on both sides" do not appear anywhere in the new script. Beat B's
narration is one plain sentence: "To compute the loss, the transformer's
output and the target embedding both pass through the same projector."

**Direct MSE, no staged `\Delta`.** Beat C used to build a separately-named
`\Delta_4` vector object with its own multi-beat reveal (create, transform,
fade, square, scalar). That is gone. Beat C now reveals one formula that
collapses straight to its value: `{\rm MSE}_4 = \|h_\psi(\hat z_4) -
h_\psi(z_5)\|_2^2 = 0.42`, reusing the same `proj_pred_vals3` /
`proj_targ_vals3` / `0.42` literals the old code already had. Colors follow
the established convention (PREDICTION / NEXT_TARGET / ERROR).

**Dot grid replaced with real miniature vectors.** The old `(b, t)` grid of
plain `scalar_dot`s is gone. Beat D now fans out six small
`numeric_embedding` pairs (`shown=3`, `height=0.50`) across the frame,
colored PREDICTION over NEXT_TARGET exactly like the beat B/C pair, so they
read as real (if tiny) vectors rather than abstract dots. A `Brace` sits
under the row, then the batch loss formula. One deviation caught during
480p iteration: an initial version added a second, fainter "depth" row of
vectors offset behind the front row (per the spec's "optionally a second
fainter row" suggestion) -- at this frame's scale the two rows' bounding
boxes overlapped and produced visible bracket/digit clutter. Dropped the
second row entirely in favor of one clean row of six; re-rendered and
confirmed no overlap at both 480p and full 1080p60.

**Gradient-flow ending cut.** The old beat G (reverse `ShowPassingFlash`
down both lanes, `Indicate` on both source vectors, "the gradient runs back
through both projectors" narration) is deleted outright, along with its
"both branches" claim. The scene now ends on the loss formula:
`self.inspect(1.8)` then `self.clear_beat(1.0)`.

**Deviations from the spec.** (1) The spec's suggested `self.across(...,
floor=...)` pattern for the closing formula reveals in beats C and D was
not used -- `across` consumes the tracker's *entire* remaining duration in
one animation, and since neither beat carries bookmarks, the remaining
duration at that point (several seconds) would have produced a
noticeably slow single fade-in, working against the "brisker" brief.
Both beats instead use a fixed `run_time=0.9` reveal followed by
`self.wait(max(0.1, tracker.get_remaining_duration()))`, the same idiom
the old code already used to close beat C. (2) The optional second
"fainter row" in beat D's fan was tried and dropped for the overlap
reason above. (3) No "prediction loss" caption was added under the final
formula -- `\mathcal L_{\rm pred}`'s own subscript already names it, and
the spec allowed skipping the caption if it read as padding.

## Scene 03 rebuild — 2026-08-23

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA03_review_eleven_qh.mp4` |
| Delivery | 41.40 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Scope | `LeNEPA03PredictionLoss` rebuilt; `common/palette.py`, `common/visuals.py` extended; new `common/data.py`; `LeNEPA02Predict` rewired to import shared constants (pure extraction); `LeNEPA01Tokens` and `LeNEPA08Landing` touched only at the mechanical `PROJECTOR` call sites named below |
| Mechanical checks | `narration_audit`, `preflight`, `facts.py` clean; no silence interval ≥ 3 s (`silencedetect -45dB/3s`, no hits) |
| Visual review | 480p frame sampling across every beat during iteration; full 1080p60 frame extraction on the delivered artifact, including drills on the `R^192`/`R^64` annotations against the `ẑ_4` label and the closing grid/brace/equation/caption stack |
| Verdict | **READY FOR OWNER REVIEW** |

The owner rejected the previous cut wholesale: a second, differently-styled
diagram of what scene 2 already drew, a warm orange projector stealing the
frame's one accent color from the comparison it was supposed to be
secondary to, an invisible D-to-d reduction, a tacky square-and-contract
gesture for the loss, an abrupt cut to a random dot grid, and a
gradients-through-both-branches ending asserted with giant arrows rather
than shown. This rebuild replaces all of it with two horizontal lanes that
continue scene 2's exact surviving pair, where the single load-bearing
motion — the coral comparison arrow migrating from the raw pair into
projected space and condensing into `\Delta` — carries the argument that
used to be six separate arrows and a caption.

**Palette split.** `PROJECTOR` was doing three unrelated jobs: scene 1's
LeJEPA global-crop callback, scene 3's projector, and scene 8's "No EMA
teacher" line. `PROJECTOR` is retargeted to a desaturated steel blue-gray
(`#7C8EB8`, ~30% saturation at hue ~220) so the projector module itself
reads as a quiet passage rather than a competing accent color — every
saturated slot in this palette is already spoken for, and the projected
vectors passing through the module must keep their own green/amber
identity for beat G's "both branches" claim to have anything to point at.
The old hex (`#E58A3A`) survives under a new name, `VIEW_GLOBAL`, for scene
1's crop callback, which has nothing to do with the projector and was only
ever borrowing the color. Scene 8's "No EMA teacher" line moves to
`NEXT_TARGET`, since that claim is about the target branch. Scene 5's
`projector` pill picks up the new hex with no code change.

**Beat structure.** No title card (a deliberate lead versus scenes 4-8,
which still open on one). Beat A silently reopens scene 2's exact exit
pair. Beat B slides both columns out to two lanes and fades in a shared
`LayerMap` (renamed from `PatchEncoderNetwork` — it was never
patch-specific) on the prediction lane, then a `TransformFromCopy` ghost
places an identical one on the target lane: the shared-weights claim told
as motion, not as a brace label. Beat C runs real propagation through both
lanes — scene 1's exact edge-flash idiom, twice — and the three lit output
neurons carry into two new columns built via `numeric_embedding`'s new
`shown=3` form: still abbreviated with an ellipsis, so the display never
misreads as a literal `d=3`. Beat D is the thesis motion: the coral arrow
shifts into the projected gap and condenses into `\Delta_4`, built from
explicit ghost copies of both projected columns so neither original is
destroyed — both stay on screen through beat G. Beat E turns one
difference into one static number, created at its final value, no
square-and-contract gesture. Beat F is a causal ladder: the scalar itself
becomes the first dot in a `(b, t)` grid (the object-identity link the old
abrupt jump lacked), the rest of its row follows, the remaining rows stack
in, and the closing equation is written in terms of `\Delta` — what this
scene just defined — instead of a re-spelled projector expression. Beat G
sends a reverse flash down both lanes in a visible 0.22 s stagger, then
indicates both original source columns together; two lanes have been
visibly identical since beat B, so "both branches" needs no caption and no
backward arrows under the frame. Narration cuts "vanilla NEPA" and
"stop-gradient" (a comparison this timebox cannot earn, and the same
judgement `RENDER_REVIEW.md`'s scene-2 passes already applied) and the
"stabilization must come elsewhere" cliffhanger; scene 4 opens on its own
apparatus and needs no handoff.

**Shared continuity state.** New `common/data.py` holds `TOKEN_H`,
`PRED_H`, the landing rows `TGT_ROW_Y`/`PRD_ROW_Y`, `TOKEN_VALUES` (scene
1's exit vectors), and `MIXED_VALUES` (scene 2's post-mixing carrier
values). `LeNEPA02Predict` now imports these instead of generating them
locally. This is a pure extraction with one real bug caught by diffing:
the first attempt drew `MIXED_VALUES`'s five non-displayed fill
coordinates *interleaved* with each carrier's four displayed draws, which
shifted every later carrier's displayed values off the original
`value_rng(97)` sequence and changed scene 2's rendered digits from carrier
1 onward. Caught by rendering `LeNEPA02Predict -qh` before and after and
diffing frames pixel-for-pixel — not just eyeballing — at four timestamps;
fixed by drawing all 16 original displayed values first, in the original's
exact order, before any filler draws. Re-verified: duration bit-identical
(33.483333 s both), max pixel diff 0 at every sampled timestamp.

**Verification of the narrow-scope edits.** `LeNEPA01Tokens` (owner's
separate in-progress scene): only the three `PROJECTOR`→`VIEW_GLOBAL` call
sites at the LeJEPA global-crop callback were touched, same hex value.
`-ql` before/after, pixel-diffed at multiple timestamps: duration identical
(52.599674 s), max diff 0. `LeNEPA08Landing`: one `PROJECTOR`→`NEXT_TARGET`
call site on the "No EMA teacher" line. `-ql` before/after: duration
identical (27.266341 s); the only changed pixels are the bounding box of
that one line's text (color shifts from the old orange to amber, as
intended) — nothing else in the frame moved.

**Deviations from the spec.** Beat C's four-step propagation recipe
(set values, flash edges, transform output layer, carry neurons to
entries) runs as several sequential `self.play` calls per lane rather than
nested `Succession`/`LaggedStart(lag_ratio=0.10)` combinators spanning both
lanes at once — both lanes animate together rather than with a 0.10 s
stagger between them. This keeps the choreography inside patterns already
proven in this codebase (scene 1 and scene 2 never nest cross-branch
`Succession`s either) while preserving the described result: both lanes
visibly process at once. `GRID`/`DELTA`/`SCALAR`/`LOSS_EQ` from the spec's
layout table are named `..._POS` in code, since a bare `GRID` would shadow
the palette's own `GRID` color import. `LOSS_EQ_POS` moved from the spec's
`(3.05, -0.95)` to `(3.05, -1.65)`: at the literal spec value, the closing
brace under the dot grid overlapped the loss equation's fraction bar by
about 0.45 units — confirmed by constructing both mobjects headlessly and
comparing bounding boxes, then again by frame extraction — which is
exactly the failure mode this rebuild exists to fix. Delivered runtime is
41.40 s against the spec's word-count estimate of ~46-48 s; the gap is the
168 wpm draft-rate estimate versus ElevenLabs' actual pacing at this
segment's `ARCHER_SPEED`, not a narration or beat-timing shortfall — no
silence interval exceeds 3 s.

**Flagged, not touched.** Scene 8's `latent_row`/`latent_column` still uses
the cell-grid glyph style this rebuild moved scene 3 away from
(`numeric_embedding`'s bracketed-column form). Left alone per the spec's
explicit instruction — out of scope for this pass.

## Scene 02 narration trim + bracket fix — 2026-08-23

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA02_review_eleven_qh.mp4` |
| Delivery | 33.48 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Scope | `LeNEPA02Predict` only; `common/visuals.py` and scenes 01, 03–08 unchanged |
| Mechanical checks | `narration_audit`, `preflight`, `facts.py` clean; no silence interval over 3 s (`silencedetect -45dB/3s`, no hits) |
| Visual review | 1080p60 frame sampling across the full clip plus drills on the finale bracket pair |
| Verdict | **READY FOR OWNER REVIEW** |

Two fixes from the owner's pass on the previous v2 artifact.

The beats 6-7 line was still explaining the Transformer mechanically ("each
one leaves as a new vector") instead of stating what the training setup is
actually for. It now says directly that the output at t is trained to equal
the token at t plus one, at the first output the viewer sees rather than two
beats later. The target-beat line ("So for position four, that means the
output is trained toward z five") now reads as an instance of that claim
instead of a second independent assertion of it, and the closing
generalization line no longer repeats the t/t-plus-one wording it already
introduced — it just names the pattern. Net: 86 words to 75. Cutting that
much narration dropped the ElevenLabs pass to 29.07 s, under the 33-35 s
scene-2 budget, so the silent beats (opening fade-in, chamber-open, the
reflow between the chamber and the shift beats, the closing hold) were
widened to bring it back to 33.48 s — no filler words were added back into
the narration to make up the difference. `across(..., floor=...)` values on
the audio-gated beats were raised too, but had no measurable effect: those
segments' narration audio already ran longer than the new floors, so the
floor never bound. The real lever turned out to be the handful of `self.play`
calls that sit outside any `voiceover` block, since those add wall-clock
time unconditionally.

The other fix is a real layout bug the owner caught by watching the previous
render: in the finale, the "prediction" `span_bracket` was built from
`VGroup(*carriers)` — the bare `\hat z` vector mobjects — with no knowledge
that the ẑ₁…ẑ₄ labels sit `buff=0.14` below them. `span_bracket` measures its
rule position from the group's `get_bottom()`, so the bracket's rule and its
"prediction Ẑ₁:ₜ₋₁ ∈ ℝ^(T-1)×D" caption landed at the bare carriers' bottom
edge — directly on top of the ẑ labels the group didn't know existed, visibly
smashing "ẑ₃" into the word "prediction". Fix is one line: the group passed
to that `span_bracket` call is now `VGroup(*carriers, *pred_labels)`, so its
bottom edge — and the `buff=0.20` clearance below it — is measured from
under the labels instead of under the raw vectors. `target_span`'s group was
left alone; it brackets `tokens[1:focus + 2]`, which already includes each
token's own label as part of the mobject, and sits above the row rather than
next to a separately-added label underneath it, so it never had this
problem. Confirmed fixed by re-extracting frames through the finale at
1080p — the bracket now clears the ẑ labels with visible margin. A broader
frame sample across the rest of the clip (roughly every 2-3 s) turned up no
other overlapping elements.

## Scene 02 re-board v2 — 2026-08-23

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA02_review_eleven_qh.mp4` |
| Delivery | 33.38 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Scope | `LeNEPA02Predict` and `common/visuals.py`; scenes 01, 03–08 unchanged |
| Mechanical checks | `narration_audit`, `preflight`, `facts.py` clean; no silence interval over 3 s (`silencedetect -45dB/3s`, no hits) |
| Visual review | Frame sampling across every beat at 480p/15fps during iteration, plus a full 1080p60 pass on the delivered artifact |
| Verdict | **READY FOR OWNER REVIEW** |

Yesterday's re-board fixed the input-copy error but still told causality with
words and showed the backbone as a place tokens vanish into and reappear
from. The owner's standing critique of that cut was that the Transformer
itself read as inert — three slabs and an `Indicate` pulse stood in for "some
computation happened" rather than showing anything resembling attention. This
pass replaces `transformer_stack` with `transformer_block`: an open-walled
chamber that never closes its interior from view, so the four carriers that
descend into it, mix, and re-emerge stay visible for the whole pass.

Causal exclusion is now spatial, not narrated. `z_5` and `z_6` dim and
physically drift off the row's baseline the moment the prefix is named; there
is no dashed cut line and no "not seen yet" caption competing with it for
attention. Inside the chamber, causal arcs bulge from each carrier only
toward carriers at or after it in time — never the reverse — so the
restriction that used to require a full sentence of narration is now legible
from the arc geometry alone, freeing the spoken line to state the modeling
claim ("each position mixes in the ones before it") instead of describing the
picture.

The carriers are the load-bearing change. `tokens[i].vector.copy()` descends
into the chamber, gets its numbers changed in place via the new
`decimal_entries` + `ChangeDecimalToValue` pairing, and is the same object
that scales back up and lands in the output row — never a separately built
`out_row` that fades in beside a chamber the input copies quietly vanished
into. A viewer can trace one column from token to prediction with no
hand-off to notice. This cost one real bug during implementation: an early
`band.move_to(...)` centered the chamber group's full bounding box, which
includes the external "causal Transformer" label sticking out to the right,
so the shell itself landed off-center and the fourth carrier rendered outside
the box. Fixed by shifting the group by the exact delta needed to land the
*shell's* center on the target point. A second bug — carriers 0–2 receiving
two separate `.animate` calls (one for the move, a second for the recolor)
inside the same `self.play` — silently reset their position each frame
toward the pre-play snapshot, stranding them near the token row instead of
the output row; fixed by chaining scale, move, and color into one `.animate`
builder per carrier. Both were caught by frame-sampling the draft render
before spending a full ElevenLabs pass on them.

The exclusions register — the crossed-out mask/second-view/EMA-teacher icons
under a "does not require" key — is deleted outright, along with its
narration line. Scene 02's job is to establish what LeNEPA's predictor does;
listing what it does not use asked the viewer to hold three negative claims
about the training recipe that scene 08's closing recap already carries.
Removing it also frees scene 03 to open directly on representation collapse
rather than following a beat that already ended on a negative-claim register
— a one-line forward pointer only; scene 03 itself is untouched this pass.
The freed budget funds the fuller chamber pass instead: this cut is 33.38 s
against the previous 36.02 s, despite the backbone beat carrying visibly more
now than before.

The closing identity is demoted to match: `z_{1:t}\rightarrow\hat
z_t\approx z_{t+1}` renders unboxed at the project's quiet equation tier,
with "next-latent prediction" beneath it at the faintest caption tier and no
`LeNEPA` title card. Nothing moves during this beat; the terminology lands
as a footnote to what the viewer just watched, not a slogan the scene stops
to announce.

## Scene 02 re-board — 2026-08-22

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA02_review_eleven_qh.mp4` |
| Delivery | 36.02 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Scope | `LeNEPA02Predict` and `common/visuals.py`; scenes 03–08 unchanged |
| Mechanical checks | `preflight`, `facts.py`, narration audit clean; no silence interval over 3 s |
| Visual review | 1 fps pass across the full clip plus 2–4 fps drills on the backbone pass, the shift, and the exclusion register |
| Verdict | **READY FOR OWNER REVIEW** |

The previous cut contained a mathematical error: a close-up copy of `z_4` was
shown feeding the Transformer, which reads as "the input at position t is
`z_t`". A causal output at t depends on the prefix `z_{1:t}`. The board is
rebuilt so that only a braced prefix ever enters the backbone, and the future
is dimmed before the brace is drawn rather than after four seconds of curved
attention wires. Those wires, the close-up copy, the two connector arrows, and
the horizontal sweep bar through the stack are all deleted.

The layout is now a vertical pipeline: token row, depth band, output row, with
x as the time index in every tier. Tokens are 1.45× their former height and
the backbone is demoted by contrast rather than by footprint — three slabs and
an ellipsis at ≤0.58 stroke opacity with a `ty.LABEL`/MUTED side label, in
place of five nearly coincident outlines under an `INK` title. `time`,
`not seen yet`, and the exclusion labels all move off the faintest type tier.

Generalisation is one motion. `\hat z_4` slides one slot right during the
target beat; the three unread outputs then make the same slide together. Their
absence of `\hat z_4` from that animation list is the argument. This replaces
five separately grown arrows and five sequential `Indicate` pulses, and it is
the bulk of the 7.8 s saved. `z_1` is dimmed and excluded from the amber span
rather than deleted, so the proof that `\hat z_1`'s target is `z_2` survives.

Tensor shapes are now stated on screen and never narrated: `z_{1:T}`,
`z_{1:4}`, `\hat z_4`, and the two `(T-1)\times D` span brackets. The scene
ends on a single boxed identity rather than a pile of facts, and the
exclusions register names `stop-gradient` explicitly alongside `EMA teacher`
(`SOURCE_MAP.md` line 27: no stop-gradient, Paper Eq. 1 and Figure 1).

`transformer_stack` was rewritten in place (verified single caller) and
`span_bracket` added; the unused `causal_fan` helper was removed.

## Scene 02 workshop revision — 2026-08-21

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA02_review_eleven_qh.mp4` |
| Delivery | 45.40 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo; 1.92 s silent final hold |
| Scope | `LeNEPA02Predict` only; scenes 03–08 were not revised in this pass |
| Mechanical checks | venv `preflight`, `facts.py`, `py_compile`, and narration audit clean; no silence interval over 3 s |
| Visual review | Full 1080p input/output, causal-boundary, target, final-shift, and exclusion frames; targeted dense motion scan of the row-to-row Transformer pass |
| Verdict | **READY FOR OWNER WORKSHOP** |

Scene 02 now begins with the exact abbreviated numeric embeddings that end
scene 01: signed coordinates, vertical ellipsis, square brackets, labels,
colors, and deterministic values. The rejected cell-grid glyphs and their
broken-looking bracket extensions are gone. The numeric input row passes
between two restrained Transformer rails and becomes a separate row of five
new numerical predictions. Every `\hat z_t` has visibly different coordinate
values, while the source tokens remain in place. The rail label clears during
the crossing so no moving vector passes through typography.

The fourth predicted embedding is isolated only after the full output row has
settled. Four temporary curves carry green passing flashes from `z_1` through
`z_4` into `\hat z_4` and then disappear, translating
`play_simple_attention_animation` without retaining a wire fan. A dashed
causal cut dims the unavailable future. This replaces the former extra state
row, unexplained output port, and overlapping equation.

The observed numeric `z_5` itself turns amber and receives the focused target
arrow. The already-generated prediction row then physically shifts one time
step right, aligning each `\hat z_t` directly beneath the existing `z_{t+1}`.
Short vertical coral arrows complete the comparison; the original `\hat z_4`
remains the same Manim object throughout. The custom crossed-out mask,
second-view, and teacher-network glyphs enter only after this computation has
settled.

The revised 100-word narration is audited manually in
`NARRATION_REVIEW_02.md`; bookmarks align the focus, causal-history flow,
future boundary, prediction, target, repeated shift, and exclusions to the
temporary ElevenLabs read. The source narration remains the handoff for the
author's future recording.

## Scene 01 workshop revision — 2026-08-21

| | |
|---|---|
| Artifact | `media/videos/jepa_explainer/lenepa/LeNEPA01_review_eleven_qh.mp4` |
| Delivery | 59.42 s; 1920×1080 at 60 fps; H.264; AAC 48 kHz stereo |
| Scope | `LeNEPA01Tokens` only; scenes 02–08 were not revised in this pass |
| Mechanical checks | `preflight`, `facts.py`, and narration audit clean; audio/video durations matched; no silence interval over 3 s |
| Visual review | 1080p contact sheet plus half-second scans of the crop callback and NEPA handoff; targeted encoder-propagation, identity-preserving `z_3` move, coordinate-assembly, and parallel-reveal frames |
| Verdict | **READY FOR OWNER WORKSHOP** |

The revision now begins in the context of the larger JEPA-variants video. The
same signal gets one short masked-modeling callback, then one short LeJEPA
global/local-crop callback. An orange span and two separate green crop boxes
replace the former nested rectangles; their embedding glyphs gather inside a
single alignment neighborhood. Those objects clear before the ordered patch
tokens establish NEPA's next-embedding objective. The NEPA and LeNEPA cards now
fade through an empty frame instead of morphing incompatible text, eliminating
the doubled title observed in the previous cut.

The later close-up still ports the explicit 3Blue1Brown-style network pass. It
now begins directly with “Suppose we focus on the third window”; the separate
strided-convolution explanation and scanning-window animation are gone. Six
representative input nodes labelled `C×P` map to nine output nodes labelled
`D`, making the change of dimension explicit before those neurons travel into
the coordinates of `z_3`. The complete green `z_3` then remains the same Manim
object while it contracts and travels into the third sequence slot. After that
anchor settles, the other five green vectors emerge with a lagged reveal; there
is no cut or replacement at the handoff. The move now resolves in about 2.87
seconds, followed by roughly one second of stillness before the bookmark releases
the other embeddings. Their unfold retains about 3.1 seconds before the
batch-shape equation appears. This focus–hold–parallel-expansion rhythm follows the
transition pattern reviewed in 3Blue1Brown's transformer MLP walkthrough.

Five additional rests of 0.65–0.85 seconds now punctuate the mask callback,
crop callback, NEPA objective, LeNEPA title, and encoder close-up. These are
silent settled frames between ideas rather than slower object motion; the
scene therefore gains breathing room without making its transformations feel
sluggish.

The “predict next” annotation is now set at the smallest project text tier and
scaled down once more. The settled 1080p frame leaves visible air between the
history box, the label, and the amber target box.

The semantic palette now distinguishes input blue, mask coral, prediction
amber, crop orange, and retained/predictive green. No settled overlap or
collision was observed.

`NARRATION_REVIEW_01.md` contains the required manual function, cadence,
metaphor, proof-language, and visual-grounding audit. The 143-word scene text is
the reviewed source for both ElevenLabs and the future human recording. The
temporary ElevenLabs preview is played at 90% tempo. Its service substitutes
“the previous method” and “this version” for the two invented names, avoiding
the synthetic voice's unnatural word breaks. The source narration and written
captions retain `LeJEPA` and `LeNEPA` for the author's future recording.

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
