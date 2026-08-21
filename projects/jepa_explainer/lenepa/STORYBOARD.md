# LeNEPA storyboard

Target runtime: **4:30–4:55** with the ElevenLabs preview voice. The timing-only
draft assumes 168 spoken words per minute. Hard cuts are intentional because
this segment may be rearranged inside the larger JEPA-variants edit.

| Scene | Target | Focal event | Viewer state after |
| --- | ---: | --- | --- |
| 1. Tokens | 0:35–0:40 | one patch visibly passes through the shared encoder before the parallel reveal | the input-to-token shape change is concrete |
| 2. Prediction | 0:30–0:35 | one causal position expands into all one-step pairs | “next embedding prediction” is self-explanatory |
| 3. Loss | 0:45–0:50 | two projected columns become a difference and a scalar | the equation transcribes a watched operation |
| 4. Temporal SIGReg | 0:40–0:48 | a globally spread batch hides one collapsed sequence | the regularization axis is understood |
| 5. Objective | 0:25–0:30 | objective assembles, blade discards the head | training space and kept encoder are distinct |
| 6. Protocol | 0:28–0:34 | recipe cards copy to both datasets, weights retrain | recipe reuse is not checkpoint transfer |
| 7. Results | 0:45–0:55 | PTB-XL/Diag panels, speed band, qualified UCR check | result scope and limitations are retained |
| 8. Landing | 0:22–0:27 | the original signal traverses the complete pipeline | the method can be reconstructed from memory |

## Shot-level plan

### 1 — A time series becomes tokens

- Opening: one waveform draws on a quiet baseline. There is no title card and
  no architecture diagram competing with it.
- Locality: one scanning window crosses the trace before the six patch regions
  settle. The moving window establishes that the convolutional filters are
  reused rather than implying six independent encoders.
- Encoder close-up: the third patch is isolated. Eight representative samples
  become the input layer of an explicit network; edges sit behind neurons,
  activations fill the layers, and a green passing flash crosses the learned
  connections. The output neurons become a signed, bracketed vector.
- Reference-code mapping: the layer/edge split and activation fill are ported
  from `_2017/nn/part1.py::NetworkMobject`; the compact two-layer layout follows
  `_2024/transformers/helpers.py::NeuralNetwork`; the one-example-then-parallel
  reveal follows `_2024/transformers/mlp.py::BasicMLPWalkThrough`.
- Expansion: the understood map repeats across the remaining windows. One
  vector remains vertically aligned with each source patch, preserving temporal
  order without drawing six overlapping encoder blocks.
- Equation reveal: `[B,C,L] -> [B,T,D]` appears only after the full vector row
  exists.
- False inference prevented: each displayed output is a D-dimensional vector;
  the windows are ordered patches, not augmented views.

### 2 — Predict the next latent

- Opening: the same token row enters a layered causal Transformer block.
- Focus: position four; arrows converge only from positions one through four;
  a shaded curtain labels the future.
- Expansion: `z_hat_t -> z_(t+1)` repeats across all usable positions.
- Context badges: no mask augmentation, no second view, no teacher network.
- False inference prevented: causality limits context; the target is still the
  observed next patch token.

### 3 — Where the prediction loss lives

- One green prediction and one amber target pass through two visibly identical
  MLP drawings joined by a “same weights” brace.
- `D=192 -> d=64` appears while the projected columns remain visible.
- Columns align; the prediction column becomes the discrepancy; the
  discrepancy contracts to a red scalar.
- Zoom out to `B(T-1)` scalar dots and reveal the averaged MSE equation.
- Backward arrows on both branches replace a stop-gradient symbol.

### 4 — SIGReg acts across time

- Three per-sample clouds are separated globally.
- All tokens in sample one collapse around one point while the aggregate frame
  still encloses a spread-out batch.
- The same sample's dots become the ordered row `u_1,...,u_T`; a purple brace
  applies SIGReg to that row.
- Layer 0 and layer 8 tap into the temporal equation.
- False inference prevented: temporal SIGReg does not pool all batch tokens.

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
