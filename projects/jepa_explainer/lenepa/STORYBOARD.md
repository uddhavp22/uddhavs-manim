# LeNEPA storyboard

Target runtime: **4:30–4:55** with the ElevenLabs preview voice. The timing-only
draft assumes 168 spoken words per minute. Hard cuts are intentional because
this segment may be rearranged inside the larger JEPA-variants edit.

| Scene | Target | Focal event | Viewer state after |
| --- | ---: | --- | --- |
| 1. Tokens | 0:52–1:00 | quick mask/crop callbacks lead into one visible encoder dimension change | NEPA's objective and the input-to-token shape change are concrete |
| 2. Prediction | 0:33–0:35 | a braced causal prefix descends into an open chamber, mixes, and exits as the same objects one slot onto the next token | “next embedding prediction” is self-explanatory |
| 3. Loss | 0:45–0:52 | the comparison arrow moves into projected space and becomes a scalar | the equation transcribes a watched operation |
| 4. Temporal SIGReg | 0:40–0:48 | a globally spread batch hides one collapsed sequence | the regularization axis is understood |
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

Built as four clean compositions. Each is fully cleared (a hard `FadeOut` of
everything on screen) before the next begins -- no object survives a
composition boundary unless it is deliberately rebuilt there. This replaced
an earlier version that let objects accumulate across the whole scene; see
`RENDER_REVIEW.md`'s two 2026-08-24 entries for what that looked like and why
it was rejected.

- No title card, anywhere in this scene -- a chapter-wide rule now, not a
  one-off fix.
- **A.** A brief silent recap of scene 3's exit frame, fully cleared, then a
  large `(B, T)` grid of real layer-0 token glyphs: row `b=1` is scene 1's
  own token sequence; rows `b=2`, `b=3` are drawn the same way from a new
  seed. Row `b=1`'s entries then genuinely converge in place
  (`ChangeDecimalToValue`, never a color change mid-morph) onto one shared
  value; only once every value has actually landed does a coral outline mark
  the row as collapsed.
- **B.** All eighteen tokens in the batch -- not three separate per-sample
  clouds -- pool onto one large shared latent plane, built fresh (dots
  arriving via `GrowFromCenter`, never a `Transform` from a complex vector
  glyph into a dot, which produces mangled interpolation garbage). Row
  `b=1`'s six points land on one coincident spot; rows `b=2`/`b=3` keep real
  spread. Only then does the SIGReg chapter's own projection grammar (one
  `PlaneProjectionRig`, one direction, one line, one reference curve, no
  dashed guide-line clutter) run across each row in turn: `b=1`'s identical
  points spike and score high, `b=2`/`b=3` spread and score low.
- **C.** Layer 0 and layer 8 are pulled out of an actual, large transformer
  chamber -- `u^(0)` is scene 1's token row, `u^(8)` reuses scene 2's
  post-mixing carriers -- as real spatial extraction points (glyphs emerging
  from the chamber's top/bottom edge with their `ell=0`/`ell=8` tap attached
  at the same moment, not added later). `depth_plates()` gives the chamber
  visible interior structure. `L_T={0,8}` forms from the two taps.
- **D.** The temporal equation and legend land on an empty frame; only after
  a hold does the prediction loss fade back in above it, freshly built (not
  restored from a dimmed parked copy), so the scene ends on both training
  terms side by side.
- False inference prevented: temporal SIGReg does not pool all batch tokens
  into one plane for scoring -- it scores each sequence separately, along its
  own time axis; the shared-plane beat is only there to falsify the
  "batch-level check would have caught this" intuition.
- No comparative ablation claim closes the scene; ends on the two loss terms,
  not the weighted objective (that belongs to scene 5).

### 5 — The complete training step

- Prediction loss and temporal SIGReg become the weighted objective.
- The architecture replaces the equation.
- A vertical blade falls after the causal Transformer; projector and losses
  desaturate and leave while patch embedding plus encoder center themselves.

### 6 — What experiment is this?

- LeNEPA and JEPA recipe cards each copy into PTB-XL and Diag columns.
- Every destination receives the caption “retrain weights.”
- The distinction “recipe reuse — no checkpoint transfer” holds alone.
- 20,000 updates, five seeds, and frozen probes enter as quiet protocol facts.

### 7 — What happened?

- PTB-XL and Diag result panels reveal sequentially.
- The panels clear into two time bands for reaching 80% of final gain.
- A red qualification card appears before the UCR value.
- UCR 77.65% is held beside Mantis/MOMENT/NuTime and the explicit “single seed,
  best checkpoint” note.

### 8 — LeNEPA in one pass

- The original signal rapidly becomes three tokens, passes through the causal
  Transformer, then branches to prediction and temporal SIGReg.
- The pipeline clears to three method facts, followed by the smaller temporal
  spread statement.
