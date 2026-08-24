# ElevenLabs preview script

This is a **temporary synthetic-voice render** for editorial timing. The author
will record the final narration later. Keep `scenes.py` as the timing source of
truth when replacing the audio; its voiceover blocks drive the animations.

Preview voice: Archer (`eleven_multilingual_v2`) at 90% tempo, stability 0.65,
similarity 0.75, style 0, speaker boost on. Approximate script length:
**873 words**.
`common/scene.py` automatically sends the phonetic forms below to ElevenLabs
while retaining the conventional spellings in subtitles.

Pronunciation notes:

- LeNEPA: one word, “leh-NEP-uh”
- LeJEPA: one word, “leh-JEP-uh”
- SIGReg: “sig-reg”
- JEPA: “jepp-uh”
- PTB-XL: “P T B X L”
- Diag: “die-ag”
- AUROC: “A U rock”
- AUPRC: “A U P R C”
- UCR: “U C R”
- `z_hat`: “zee hat”

## 1 — A time series becomes tokens

Suppose we want to learn a representation of this time-series signal. We could
mask part of it and train the model to predict what is missing.

Or, as in LeJEPA, we could take global and local crops and align the
representations of those views.

Next-embedding predictive architectures use a different objective. They divide
the signal into patches, keep those patches in order, and predict the embedding
that comes next.

LeNEPA keeps the next-embedding task, but removes the masked or cropped views.

Suppose we focus on the third window. The encoder maps its C by P values into D
learned coordinates.

That D-dimensional output is z three. The same map turns every other window
into its own vector. So, across a batch, B by C by L becomes B by T by D: T
ordered tokens, each with D coordinates.

## 2 — Predict the next latent

The ordered tokens enter a causal Transformer. Suppose we read the output at
position four. It can depend on z one through z four; z five and z six are
still out of reach. Those four available tokens produce z-hat four, a
prediction made from the history so far.

The target for that prediction is the next token, z five. The same one-step
shift applies at every usable position: z-hat one predicts z two, z-hat two
predicts z three, and so on. The prediction task uses only this ordered token
sequence—there is no masked augmentation, second view, or teacher network.

## 3 — Where the prediction loss lives

To compute the loss, the transformer's output and the target embedding both
pass through the same projector.

We compute the MSE between the two projected vectors.

So when we do this for every prediction and time point in the batch, the
prediction loss becomes this:

## 4 — SIGReg acts across time

The prediction loss compares projected vectors, but temporal SIGReg works on
the raw tokens themselves, one sequence at a time. Now suppose a batch holds
several such sequences, each with its own tokens across time.

Nothing stops the tokens in one sequence from drifting together, until every
position ends up carrying the same embedding.

Now suppose we take every representation in the batch and put it into the
same projected plane. Across the whole batch, there's still plenty of spread.

Now follow the first sequence across time. All six of its representations
have landed in essentially the same place, so its score comes out large.

The second sequence hasn't collapsed, so it spreads out and scores low — and
the third looks the same way. So for each sequence, we run SIGReg across its
own tokens over time.

Tokens exist at every depth of the network, not just one. LeNEPA does this at
two places: the patch embeddings at layer zero, and again after layer eight.

Those two layers are the layer set L T.

Averaging those scores over the batch and over both layers gives the temporal
SIGReg term. Together with the prediction loss, that's what LeNEPA trains on.

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
