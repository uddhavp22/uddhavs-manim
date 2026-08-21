# ElevenLabs preview script

This is a **temporary synthetic-voice render** for editorial timing. The author
will record the final narration later. Keep `scenes.py` as the timing source of
truth when replacing the audio; its voiceover blocks drive the animations.

Preview voice: Archer (`eleven_multilingual_v2`), stability 0.65, similarity
0.75, style 0, speaker boost on. Approximate script length: **731 words**.
`common/scene.py` automatically sends the phonetic forms below to ElevenLabs
while retaining the conventional spellings in subtitles.

Pronunciation notes:

- LeNEPA: “leh-NEP-uh”
- SIGReg: “sig-reg”
- JEPA: “jepp-uh”
- PTB-XL: “P T B X L”
- Diag: “die-ag”
- AUROC: “A U rock”
- AUPRC: “A U P R C”
- UCR: “U C R”
- `z_hat`: “zee hat”

## 1 — A time series becomes tokens

This signal has L time steps. A strided convolution reads one short window at a
time, reusing the same filters as it slides along the trace. The windows keep
their left-to-right order.

Focus on the third window. Its samples feed the encoder together. Each output
channel applies a learned filter, and the D channel values form one latent
vector, z three.

The same map turns every other window into its own vector. So, across a batch,
B by C by L becomes B by T by D: T ordered tokens, each with D coordinates.

## 2 — Predict the next latent

The token row enters a causal Transformer. Focus on position four. Its output
may use tokens one through four, but the future remains hidden. The output,
z-hat four, predicts from the available history.

The target is the actual next token, z five. Shift that same comparison across
the row: z-hat one predicts z two, z-hat two predicts z three, and so on.
Defining the task needs no mask augmentation, second view, or teacher network.

## 3 — Where the prediction loss lives

LeNEPA does not compare the two D-dimensional vectors directly. Both pass
through the same small projector. The two paths share weights. In the main
experiments, this maps a 192-dimensional backbone vector into a 64-dimensional
loss space.

Line up the projected columns and subtract entry by entry. The difference is
one d-dimensional vector. Squaring and summing its entries contracts the column
to one scalar squared distance.

There is one such scalar for every sample and every usable time step; their
average is the prediction loss. Unlike vanilla NEPA, the target branch is not
stopped, so gradients flow through both sides. Stabilization must come
elsewhere.

## 4 — SIGReg acts across time

A batch-wide regularizer can see plenty of global spread. Different samples
occupy different regions, so the aggregate cloud looks healthy. But that view
hides a failure mode inside each sequence.

Inside a single time series, all seven tokens can still collapse toward one
point while other samples keep the batch spread out. A pooled check may miss
this. LeNEPA groups tokens by sample and applies SIGReg along that row's time
axis.

That temporal regularizer is tapped at the patch embeddings and after
Transformer layer eight. Averaging over samples and those layers gives the
temporal SIGReg term. Among the paper's single-component placements, this was
the one with sustained gains on both main datasets.

## 5 — The complete training step

Training combines the two scalars. The prediction term has weight one;
temporal SIGReg has weight twenty in the main configuration. One term teaches
what comes next; the other resists temporal collapse.

Once training ends, the cut falls after the causal Transformer. The projector
and both losses disappear. Only the patch embedding and encoder survive for
frozen-feature evaluation. The objective shaped a disposable space.

## 6 — What experiment is this?

The experiment holds each method's recipe fixed, then restarts training on each
dataset. LeNEPA is trained once on PTB-XL and separately on Diag; ECG-tuned JEPA
is too. What transfers is the configuration, not a checkpoint.

Both recipes were chosen using PTB-XL work; neither was retuned for Diag. The
comparison therefore asks how costly unchanged recipe reuse is under twenty
thousand updates, five seeds, and frozen probes—not for the best Diag-tuned
version of either method.

## 7 — What happened?

On PTB-XL, the ECG-tuned JEPA recipe is slightly stronger: its best readout
reaches point eight nine two AUROC and point two nine eight AUPRC. Under the
fixed-recipe rule on Diag, LeNEPA reaches point nine two zero and point six five
zero, clearly ahead on classification.

The learning curves also rise earlier. LeNEPA reaches eighty percent of its
final AUROC or AUPRC gain after roughly two to five thousand updates; JEPA takes
about five to ten thousand. These coarse, fixed-horizon observations are not a
universal speed guarantee.

The win is not universal. NEPA with a projector beats LeNEPA on several dense
Diag regression metrics, so the cleanest advantage is classification and
training dynamics. A frozen UCR check lands at 77.65 percent near the listed
baselines, but uses one seed and the best checkpoint.

## 8 — LeNEPA in one pass

Run the original signal through once more. Convolutional patches become latent
tokens. A causal Transformer predicts the next one, and temporal SIGReg keeps
each sample's token sequence from collapsing. After training, only the encoder
remains.

So LeNEPA's identity is compact: no augmentations, no EMA teacher, and a direct
prediction of the next latent. SIGReg supplies the temporal spread that
stabilizes training.
