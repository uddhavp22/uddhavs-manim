# LeNEPA source map

## Primary source

- Alexander Chemeris, Ming Jin, and Randall Balestriero, *LeNEPA:
  No-Augmentation Next-Latent Prediction for Time-Series Representation
  Learning*, arXiv:2607.00958 (2026).
- Paper: https://arxiv.org/abs/2607.00958
- Reproduction artifacts: https://github.com/langotime/lenepa-milets-2026

## What the segment teaches

LeNEPA turns a time series into patch tokens, uses a causal Transformer to
predict each next latent token, computes that regression loss through a shared
disposable projector, and stabilizes learning with SIGReg along the temporal
tokens inside each sample.

The strongest visual explanation is the axis choice for SIGReg. A batch can be
globally spread while the tokens within one individual sequence collapse. The
animation therefore moves from an aggregate cloud to one sample's temporal row.

## Claims used on screen

| Claim | Source location / status |
| --- | --- |
| `x: [B,C,L] -> z: [B,T,D]`, convolutional patch embedding, causal ViT | Paper §2 and Figure 1; explicit |
| Shared projector `h_psi`, next-latent MSE, no stop-gradient | Paper Eq. 1 and Figure 1; explicit |
| Main dimensions `D=192`, `d=64` | Paper Table 2 / implementation configuration; explicit |
| Temporal SIGReg within each sample, at layers `{0,8}` | Paper Eq. 2 and main configuration; explicit |
| `lambda_pred=1`, `lambda_T=20` | Paper Eq. 3 and main configuration; explicit |
| Projector discarded for frozen evaluation | Paper Figure 1 and projector ablation; explicit |
| 20k updates, five seeds, frozen probes | Paper §3 and Table 2; explicit |
| PTB-XL and Diag values | Paper Table 3; explicit |
| 80% gain at 2–5k vs. 5–10k updates | Paper §4; qualitative and coarsely sampled |
| Dense Diag regression is mixed | Paper §5; explicit qualification |
| UCR 77.65% | Paper Table 4; single seed, best checkpoint qualification retained |

## Visual-code references

The animation borrows structural ideas, not assets or exact code, from:

- `3blue1brown_videos/_2017/nn/part1.py::NetworkMobject`
- `3blue1brown_videos/_2024/transformers/helpers.py::{NumericEmbedding,EmbeddingArray}`
- `3blue1brown_videos/_2024/transformers/mlp.py::BasicMLPWalkThrough`
- `3blue1brown_videos/_2024/transformers/network_flow.py::HighLevelNetworkFlow`

The adapted grammar is: explicit vector columns; edges behind nodes; isolate one
token before showing parallel application; preserve object identity across
representations; let the equation transcribe an operation already seen.

## Claims deliberately not made

- This is not a claim that LeNEPA universally beats JEPA.
- The Diag experiment is recipe reuse after retraining, not checkpoint transfer.
- The learning-speed observation is not a general convergence guarantee.
- The UCR number is not presented as a leaderboard result.
- The segment does not re-teach attention or SIGReg internals; the larger video
  supplies those prerequisites.

