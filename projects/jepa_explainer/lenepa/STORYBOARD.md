# LeNEPA storyboard

Target runtime: **4:30–4:55** with the ElevenLabs preview voice. The timing-only
draft assumes 168 spoken words per minute. Hard cuts are intentional because
this segment may be rearranged inside the larger JEPA-variants edit.

| Scene | Target | Focal event | Viewer state after |
| --- | ---: | --- | --- |
| 1. Tokens | 0:52–1:00 | quick mask/crop callbacks lead into one visible encoder dimension change | NEPA's objective and the input-to-token shape change are concrete |
| 2. Prediction | 0:33–0:35 | a braced causal prefix descends into an open chamber, mixes, and exits as the same objects one slot onto the next token | “next embedding prediction” is self-explanatory |
| 3. Loss | 0:45–0:52 | the comparison arrow moves into projected space and becomes a scalar | the equation transcribes a watched operation |
| 4. Temporal SIGReg | 1:05–1:10 | one batch, followed through vectors, a latent plane, a 1-D shadow, and network depth | the regularization axis is understood |
| 5. Objective | 0:25–0:30 | objective assembles, blade discards the head | training space and kept encoder are distinct |
| 6. Protocol | 0:28–0:34 | recipe cards copy to both datasets, weights retrain | recipe reuse is not checkpoint transfer |
| 7. Results | 0:45–0:55 | PTB-XL/Diag panels, speed band, qualified UCR check | result scope and limitations are retained |
| 8. Landing | 0:22–0:27 | the original signal traverses the complete pipeline | the method can be reconstructed from memory |

## Shot-level plan

### 1 — A time series becomes tokens

- Opening: one waveform draws on a quiet baseline. A coral masked-patch
  prediction and orange/green LeJEPA global/local crops briefly reuse that same
  signal as callbacks to the preceding chapters.
- View callback: an orange span marks the global crop while two separate green
  boxes mark local crops. Three compact embedding glyphs gather inside one
  alignment neighborhood. This is a reminder, not a second derivation of
  LeJEPA.
- Objective handoff: the callbacks clear; ordered patch embeddings and one
  green-to-amber next-step arrow establish the new objective. Only then does
  the `NEPA` title appear and transform into `LeNEPA`.
- Encoder close-up: the third patch is isolated immediately. Six representative
  input nodes stand for its `C×P` values, while nine output nodes make the map
  to a different latent dimension `D` unmistakable. Edges sit behind neurons,
  activations fill the layers, and a green passing flash crosses the learned
  connections. The output neurons become a signed, bracketed vector.
- Reference-code mapping: the layer/edge split and activation fill are ported
  from `_2017/nn/part1.py::NetworkMobject`; the compact two-layer layout follows
  `_2024/transformers/helpers.py::NeuralNetwork`; the one-example-then-parallel
  reveal follows `_2024/transformers/mlp.py::BasicMLPWalkThrough`.
- Expansion: the understood map repeats across the remaining windows. One
  full green `z_3` compresses into its abbreviated form and travels to the
  third slot; it is never cut away and replaced. The move is decisive rather
  than stretched across the full spoken clause, leaving roughly one second of
  stillness on the settled `z_3`. Only then do the other green vectors emerge
  with a restrained lag. One vector remains vertically
  aligned with each source patch, preserving temporal order without drawing
  six overlapping encoder blocks.
- Equation reveal: `[B,C,L] -> [B,T,D]` appears only after the full vector row
  exists.
- False inference prevented: each displayed output is a D-dimensional vector;
  the windows are ordered patches, not augmented views.

### 2 — Predict the next latent

- Board: the same vertical pipeline as before — token row on top, an open
  chamber beneath it, output row below that — is unchanged. Because the x
  coordinate is the time index in every tier, "the sequence keeps its shape
  through the backbone" stays legible without drawing a single wire, and the
  horizontal axis stays free for the one-slot shift.
- Opening: scene 01's exact abbreviated numeric embeddings return — signed
  coordinates, ellipsis, brackets, labels, colors, and deterministic values.
  They enter at scene 01's exit geometry and grow into the hero row, so the
  cut between scenes moves one object rather than replacing it.
- Focus and causality: a ring marks `z_4`; then it fades as `z_5` and `z_6`
  dim and physically drift off the row's baseline. That displacement *is* the
  "not seen yet" signal — there is no dashed cut line and no caption. A brace
  then names the visible prefix `z_{1:4}`, with its shape annotation sitting
  beside the brace's end rather than crowding the row underneath it.
- Chamber: an open-walled box — stroke only, no fill, interior visible from
  the moment it appears — replaces the old flat depth band. Scaled copies of
  `z_1` through `z_4` fall simultaneously into it, one persistent carrier per
  position; the source row dims while the chamber is active.
- Mixing: causal arcs bulge upward inside the chamber, each one running only
  from an earlier position toward a later one — never the reverse — so the
  causal restriction is spatially legible without narration. Every carrier's
  displayed coordinates change in the same beat, then position four's result
  is built from exactly its four carriers, with a brighter set of arcs
  converging on the fourth alone.
- Exit: the chamber closes and every carrier descends out of it into the
  output row. These are the same objects that entered — not a separately
  built row that fades in beside them — so a viewer can trace one column from
  token to prediction without a hand-off.
- Target: `\hat z_4` slides exactly one slot right and `z_5` returns to the
  row, now amber, with one short coral arrow connecting them. No caption
  names the pair; the narration does that work instead.
- Shift: the three unread outputs make exactly the move `\hat z_4` already
  made, in one motion rather than three grown arrows. `z_1` dims and is
  excluded from the amber span rather than deleted, so the proof that
  `\hat z_1`'s target is `z_2` stays visible.
- Shapes: quiet annotations carry the tensor story — `z_{1:T}\in\mathbb
  R^{T\times D}`, `z_{1:4}\in\mathbb R^{4\times D}`, `\hat z_4\in\mathbb R^D`,
  and the two span brackets `Z_{2:T}` and `\hat Z_{1:T-1}`, both
  `\mathbb R^{(T-1)\times D}`. None of them are narrated.
- Landing: nothing moves. One unboxed identity, `z_{1:t}\rightarrow\hat
  z_t\approx z_{t+1}`, fades in at a quiet equation size, with "next-latent
  prediction" underneath it at the faintest caption tier — no title card, no
  frame-clear.
- False inference prevented: causality limits context; the target is still
  the observed next patch token.

### 3 — The prediction loss

- No title card. Beat A silently reopens scene 2's exact surviving pair
  (target on top, prediction below) at its own exit geometry.
- Beat B: the pair slides out to two lanes and a *single* 9-to-3-node
  `LayerMap` fades in between them. That one projector runs twice --
  `pred_src`'s values flow through it (scene 1's propagation-flash idiom),
  producing a small `h_\psi(\hat z_4)` column, then the same object runs
  `targ_src`'s values, producing `h_\psi(z_5)`. One projector object on
  screen makes "same weights" true by construction, so it is never spoken
  and never shown as a ghost copy or a brace.
- Beat C: MSE between the two projected vectors, one clean reveal --
  `{\rm MSE}_4 = \|h_\psi(\hat z_4) - h_\psi(z_5)\|_2^2 = 0.42` -- no
  separately-staged `\Delta` object, no square/contract gesture.
- Beat D: six small, real (if tiny) projected-vector pairs fan out across
  the frame to suggest "every position, every sequence in the batch" --
  replacing the old abstract `(b, t)` dot grid. A brace under the fan, then
  the batch loss formula:
  `\mathcal L_{\rm pred} = \frac{1}{B(T-1)}\sum_{b,t}\|h_\psi(\hat z_{b,t}) - h_\psi(z_{b,t+1})\|_2^2`.
  The scene ends there -- no gradient-flow beat, no "both branches move"
  claim.

### 4 — SIGReg acts across time

**One continuous visual argument, not a sequence of compositions.** Eighteen
`TokenColumn` objects are built once in beat 1 and are still the objects on
screen in beat 9. They are drawn as vectors, then as points in a latent plane,
then as shadows on one direction, then as vectors again, then rewritten depth
by depth. Nothing is faded out and respawned as a look-alike, so
"this token became that point" is a fact about the scene graph rather than a
claim the narration has to make. The four-composition build this replaced --
clear, rebuild, clear, rebuild -- is recorded in `RENDER_REVIEW.md`'s
2026-08-24 entries along with why it was rejected at the storyboard level.

- No title card anywhere in this scene, and no header, caption, or floating
  sentence standing in for one -- a chapter-wide rule.
- **The vectors show their coordinates**, in the same bracketed
  signed-decimal form scenes 1 to 3 use. `TokenColumn` is `numeric_embedding`
  that can be rewritten every frame: `DecimalNumber.set_value` per shown
  coordinate, re-anchored so nothing shifts, with brightness as a second
  channel for magnitude on top of the digits. An earlier build drew each
  coordinate as a shaded cell with no number on it -- that is what the whole
  scene is *about*, so it is what the frame has to show.
- **Almost no pulsing.** An earlier build ran seven `LaggedStart(Indicate(...))`
  cascades: one per beat and two in beat 8. Each has been replaced by a state
  that persists or a quantity that is drawn -- the collapsed row turns coral
  and stays coral, the spread of each sequence gets a ruled extent, the check
  gets one span rule. One `Indicate` survives in the whole scene.
- **1. One sequence collapses.** Opens directly on six large `TokenColumn`
  vectors filling the frame -- no recap of scene 3, which was a flashback
  slide rather than continuity. A single `ValueTracker` alpha drives all six
  simultaneously from their own values onto one shared vector; there is no
  left-to-right lag, because there is no left-to-right propagation in
  temporal collapse and staging one would assert a mechanism that does not
  exist. The endpoint is six *pixel-identical* columns, which is what makes
  the claim -- six columns of identical digits, before any colour is applied.
  Colour then records it: the row turns coral and stays coral for the rest of
  the scene, so `b=1` reaches the latent plane already marked. No pulse, and
  no surrounding rectangle.
- **2. The batch widens.** The same row is resized and moved, not cleared and
  rebuilt smaller. Rows `b=2`, `b=3` arrive in one gesture -- revealing them
  token by token over several seconds would be filling time.
- **3. Into a shared latent plane.** Every column already contains a carrier
  dot at its centre. The bodies fade where they stand and the carriers, which
  have been there all along, travel. Nothing is created at the destination,
  and no `Transform` is attempted between a bracketed column and a `Dot`.
  Arrival is sample by sample, never shuffled: a randomised order destroys
  the one thing the move exists to preserve.
- **4. The SIGReg grammar, reused.** Direction arrow, projection line, dashed
  guides and stacked shadow dots, through the shared `PlaneProjectionRig` --
  the same objects, stroke weights and rhythm the SIGReg chapter spent
  minutes teaching. No new metaphor for spread, and no score printed: the
  viewer was never given that scale.
- **5. The collapsed sequence alone.** Its six points are genuinely
  coincident, so they are drawn coincident -- no jitter is added to make them
  countable, because falsifying the geometry to make a count legible trades
  away the exact fact the beat proves. A `\times 6` states the multiplicity
  in the cloud; in the shadow it needs no stating, because `stack_levels`
  piles six equal projections into a visible column of six. One kept guide
  line runs from the knot to that spike, and a ruled extent under the stack
  measures the spread: for this row it has zero length and renders as a single
  tick. It is measured off the projected feet, not off the shadow dots, whose
  bounding box is one dot diameter wider than the quantity and would turn no
  spread into a small box.
- **6. The other two, trial by trial.** Chapter B's repeated-example rhythm
  with readable endpoint states, not one continuous morph through all three.
  Each trial ends on the same rule in the same place at a different length,
  labelled `b=`, so the comparison is one measurement repeated rather than
  three light shows.
- **7. Back to the rows.** The carriers return to the columns they came out
  of, so the plane reads as a detour taken and come back from. One span rule
  per row, each measuring that row's own six positions, then the notation
  `SIGReg({u_{b,t}}_{t=1}^T)` -- after the operation has been watched.
- **8. Layer 0 to layer 8.** Depth is an axis beside the row, not a stack of
  plates the row travels through: nine layers across five units are 0.65
  apart, a row of *readable* vectors is three times that tall, and a row
  "resting on layer 0" visibly covered layers 0, 1 and 2. So the row stays
  still and large and a marker slides down the axis, with a thin leader from
  the marker to the row -- and every coordinate on screen rewrites itself
  continuously underneath it. This is the beat the digits exist for. It is
  `b=2`, the healthy sequence, on purpose -- watching a sequence just
  supposed into collapse evolve with depth would contradict the supposition
  still standing. `L_T={0,8}` is read off the two lit markers
  with a digit-to-digit `TransformFromCopy`, the one transform here that is
  structurally safe.
- **9. The equation.** Built right to left: the operation the viewer has now
  seen twice appears first, and the two averages are prepended onto it.
- False inference prevented: temporal SIGReg does not pool all batch tokens
  into one plane for scoring -- it scores each sequence separately, along its
  own time axis; the shared-plane beat is only there to falsify the
  "batch-level check would have caught this" intuition.
- The scene ends on the temporal term alone. Scene 5 owns combining it with
  the prediction loss, and showing both here made that beat redundant.

### 5 — The complete training step

- No title card -- as everywhere in this segment.
- Prediction loss and temporal SIGReg become the weighted objective. The
  equation is the hero of the beat and is sized like one; it previously
  played `TransformFromCopy` *and* `FadeIn` on the same mobject in one call
  and so never appeared on screen at all.
- The architecture replaces the equation.
- A vertical blade falls after the causal Transformer; projector and losses
  desaturate and leave while patch embedding plus encoder center themselves.

### 6 — What experiment is this?

- No title card. The two dataset columns are symmetric about the frame
  centre; they used to sit at x=-1.55 and x=+2.65.
- LeNEPA and JEPA recipe cards each copy into PTB-XL and Diag columns.
- Every destination receives the caption “retrain weights.”
- The distinction “recipe reuse — no checkpoint transfer” holds alone.
- 20,000 updates, five seeds, and frozen probes enter as quiet protocol facts.

### 7 — What happened?

- No title card. Panels and the speed chart are sized to the frame rather
  than to the band left over beneath a header.
- PTB-XL and Diag result panels reveal sequentially.
- The panels clear into two time bands for reaching 80% of final gain.
- A red qualification card appears before the UCR value.
- UCR 77.65% is held beside Mantis/MOMENT/NuTime and the explicit “single seed,
  best checkpoint” note.

### 8 — LeNEPA in one pass

- The original signal rapidly becomes three tokens, passes through the causal
  Transformer, then branches to prediction and temporal SIGReg. The pipeline
  is chained with `next_to` rather than placed at hand-picked x coordinates,
  which is what previously drew the transformer pill straight through `z_3`.
- The closing statements clear the pipeline first and build on empty space;
  the two occupy the same screen band and crossfading them stacked layers.
- The pipeline clears to three method facts, followed by the smaller temporal
  spread statement.
