# Narration review — Scene 02

## Objective and channel split

The viewer should understand one causal training pair before reading the same
one-step rule across the sequence. The animation supplies scene 01's ordered
numeric vectors, a distinct coordinate-changing Transformer output row, the
unavailable future, focus on the numerical fourth prediction, and the
one-position shift that aligns every `\hat z_t` with `z_{t+1}`. Narration
supplies the causal restriction, identifies prediction versus target, and
states which additional branches the task does not use.

Necessary claims:

- the output at position four may depend on `z_1` through `z_4`;
- `z_5` and `z_6` are unavailable to that output;
- `\hat z_4` is predicted from the available history;
- the training target for `\hat z_4` is the observed next token `z_5`;
- the same shift defines every usable pair;
- the task has no masked augmentation, second view, or teacher network.

Narration density: **medium**. The causal qualification and target identity are
spoken precisely; the repeated-pair expansion is allowed to carry itself
visually.

## Narration draft

These tokens are ordered in time. Suppose we take position four. The model
only gets the prefix up to there.

Inside the Transformer, each position mixes in the ones before it.

After going through the transformer, the goal is for the output at t to
equal the token at t plus one.

So for position four, that means the output is trained toward z five.

The same holds at every position. That's next-latent prediction.

## Revision — 2026-08-23

The board changed enough (a chamber the carriers actually enter and exit,
causal arcs standing in for the prefix restriction, the exclusions register
gone entirely) that the draft above replaces the previous version rather than
patching it. Four changes worth naming: the "five and six haven't happened
yet" phrasing is gone, since that claim is now made spatially by the tokens
dimming and drifting off the row rather than by a sentence; the "so what
should it equal?" rhetorical question before the target reveal is replaced
with a direct claim ("trained toward z five...") since the visual already
poses the question by leaving `\hat z_4` unpaired; the shift beat is worded
as a training claim ("trained toward the token at t plus one") rather than a
stage direction, so no line narrates the animation itself; and "next-latent
prediction" now lands as a quiet demoted caption under the closing identity
instead of as a spoken tagline. The full manual function/cadence/proof-
language audit below predates this revision and has not been re-run against
the new five-line draft — that re-audit is still pending as follow-up.

## Revision — 2026-08-23 (v2)

The owner watched the rendered `-qh` pass and asked for one more cut: the
mechanical description of what a transformer does ("each output is a new
vector") was explaining machinery instead of stating the training goal, so
it is gone. Three changes:

- Beats 6-7 no longer describe position four's output as "built from exactly
  those four" that "leaves as a new vector" — that was narrating the
  mechanism. It now states the goal directly: the output at t is trained to
  equal the token at t plus one. This claim used to arrive two beats later
  (beats 10-11); saying it here, at the first output the viewer sees, means
  the generalization line no longer has to introduce it from scratch.
- The position-four target line now opens with "So for position four, that
  means..." — a connective that treats the sentence as an instance of the
  claim just made, rather than a second independent assertion of the same
  training rule.
- The generalization line ("The same holds at every position") no longer
  repeats the "output at t / token at t plus one" wording, since beats 6-7
  already established it. It closes on "That's next-latent prediction"
  without re-deriving the rule it is naming.

Net: 86 words to 75 words. Runtime held in the 33-35s band by widening
existing silent beats (chamber-open, reflow, closing hold) rather than by
padding narration back out.

## Manual audit

### Transition and contrast

- Transition-list hits: none. The word “next” names the mathematical target;
  it does not announce lesson structure.
- Contrast patterns: one necessary exclusion sentence. It distinguishes the
  architecture from the masked, multiview, and teacher-based variants already
  established earlier in the larger video.
- Imperatives: one hypothetical, “Suppose we read…”. It fixes the position
  under inspection rather than issuing an empty attention command.
- Importance language, manufactured surprise, and rhetorical questions: none.

### Function audit

1. “The ordered tokens…” — `TRANSITION`, `VISUAL_TO_SYMBOL`.
2. “Suppose we read…” — `ATTENTION`.
3. “It can depend…” — `CLAIM`, `QUALIFICATION`.
4. “Those four available tokens…” — `CLAIM`, `VISUAL_TO_SYMBOL`.
5. “The target…” — `CLAIM`, `VISUAL_TO_SYMBOL`.
6. “The same one-step shift…” — `CLAIM`, `COMPRESSION`.
7. “The prediction task…” — `QUALIFICATION`.

Every sentence changes the viewer's model of the computation. There are no
lesson-plan announcements or redundant recaps.

### Cadence, grounding, and proof language

- Seven complete sentences range from a short setup to connected explanatory
  clauses; no syntax pattern repeats three times.
- “Position four,” “z one through z four,” “z five and z six,” and “z-hat
  four” each refer to objects still visible at the moment they are spoken.
- “Can depend” states permitted causal context without claiming that every
  input contributes equal attention.
- “Still out of reach” is literal architectural language, not a metaphor: the
  future tokens are excluded from the causal computation.
- No theorem, proof, or empirical-strength verbs occur.
- Metaphors and slogan-like conclusions: none.

## Highest-priority findings and revisions

The original passage moved too quickly from a generic instruction (“Focus on
position four”) to a fully formed prediction. It also described the future as
hidden while a dense settled fan made the relevant causal subset hard to read.
The revision names the exact output being inspected, separates allowed history
from unavailable future tokens, and gives `\hat z_4` its own causal sentence.

The original expansion sentence announced an animation command (“Shift that
same comparison across the row”). The revision states the reusable rule—“The
same one-step shift applies at every usable position”—while the animation
keeps the existing focused prediction and observed target in the expanded
construction.

Before:

> Focus on position four. Its output may use tokens one through four, but the
> future remains hidden.

After:

> Suppose we read the output at position four. It can depend on z one through
> z four; z five and z six are still out of reach.

Before:

> Shift that same comparison across the row.

After:

> The same one-step shift applies at every usable position.

## Final score

| Category | Score |
|---|---:|
| Spoken naturalness | 9/10 |
| Reasoning continuity | 10/10 |
| Cadence and variation | 9/10 |
| Economy | 10/10 |
| Visual coordination | 10/10 |
| **Total** | **48/50** |

The revised 100-word narration is the source used by both `scenes.py` and the
temporary ElevenLabs preview.
