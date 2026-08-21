# Master script — `chapterC`

**Generated — do not edit.** Regenerate with:

```bash
python3 tools/script_dump.py projects/sigreg_explainer/chapterC \
    -o projects/sigreg_explainer/SCRIPT_chapterC.md
```

Extracted from `self.voiceover(text=…)` in the scene files, which is what
the render actually speaks. On-screen text is included as a second
channel — [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) §7.2 treats it as
one, and a line cut from the voice and left on screen is not cut.

Scenes follow the chapter's playback order. Ordering within a scene is
source order, which tracks playback order but
is not guaranteed to equal it: on-screen text is often constructed a few
lines before the passage that reveals it.

**5 scenes · 1,470 spoken words · 0:00**

| Scene | Words | Duration | Words/min |
|---|---:|---:|---:|
| [`c01_vectors`](#c01-vectors) | 155 | — | — |
| [`c02_the_shape_is_the_goal`](#c02-the-shape-is-the-goal) | 552 | — | — |
| [`c03_one_shadow`](#c03-one-shadow) | 413 | — | — |
| [`c04_one_shadow_is_not_enough`](#c04-one-shadow-is-not-enough) | 192 | — | — |
| [`c05_gaussian_marginals`](#c05-gaussian-marginals) | 158 | — | — |

---

## c01_vectors

*Chapter C.01 — from the Epps--Pulley statistic to an embedding cloud.*

> **ON SCREEN** — \mathcal T(

In the last chapter, we built the Epps-Pulley statistic, which compares a
scalar batch with the standard Gaussian. A Gaussian-shaped batch scores low,
while a batch with a different shape scores higher.

<sub>cues: examples</sub>

> **ON SCREEN** — \mathbb R

Suppose a neural network produces those numbers. With one output coordinate,
every input gives us one scalar, and the whole batch still lies on a line.

After the batch passes through, those outputs form the same one-dimensional
sample we scored before.

> **ON SCREEN** — \text{shown: }D=3

Now, if we widen the output layer, each input gets a second coordinate. The
line opens into a plane. Add a third, and the batch becomes a cloud.

<sub>cues: two, three</sub>

We'll use three dimensions because that's what we can see. In practice, D is
often much larger.

<sub>cues: more</sub>

> **ON SCREEN** — \text{target: }\mathcal N(0,I_D)

From here on, this cloud is Z. Suppose we want it to follow a standard
Gaussian in D dimensions.

<sub>cues: target</sub>

---

## c02_the_shape_is_the_goal

*Chapter C.02 — Gaussianity belongs to the collection.*

Suppose the cloud starts losing its spread. If one direction disappears, it
flattens into a sheet, so the batch rank drops from three to two. If another
disappears, the rank drops to one. And if the last spread disappears, every
embedding meets at one point. The rank is zero.

<sub>cues: pancake, rod, point</sub>

The representation has collapsed.

> **ON SCREEN** — z^\star\sim\mathcal N(0,I_D)

> **ON SCREEN** — \mathbb E[z^\star]=0

So training needs a target that stays spread out in every direction. LeJEPA
chooses a standard normal distribution in D dimensions because, in its
downstream-task setting, that distribution minimizes worst-case prediction
error. There is more to unpack about that claim, so we can come back to it in
a future video.

For now, what matters is that this standard normal has mean zero and unit
variance in every direction. Mean zero centers the cloud at the origin. Unit
variance gives it the same spread in every direction. So if we turn the
direction, the round target stays unchanged; it does not favor one direction
over another.

<sub>cues: center, spread, turn</sub>

> **ON SCREEN** — \mathcal L_{\mathrm{match}}(Z)

So how do we train this blue batch to match the amber target distribution? We
need a loss that measures the mismatch.

<sub>cues: cloud, target, loss</sub>

> **ON SCREEN** — \lVert z_i-z_i^\star\rVert^2

Suppose we build that loss as directly as possible. Take one blue embedding, z
sub i. Draw one possible partner, z sub i star, from the normal target.
Compare the pair with their squared distance, and use that number as the loss.
Then repeat the same construction for every embedding in the batch.

<sub>cues: sample, partner, pair, all_pairs</sub>

But the target distribution does not prescribe one partner for z sub i. There
are infinitely many possible draws. We cannot show all of them, but a rapid
sample gives us the picture. If we sample the amber points again, the blue
batch stays fixed while every pairing changes.

<sub>cues: many, resample</sub>

So instead of listing every possible draw, we can use the normal target to
calculate an expectation. The number of possible draws has nothing to do with
the number of blue embeddings. We hold one embedding z fixed. As more possible
partners fill the target around zero, opposite directions balance. Their
average pull points straight from z to the origin.

<sub>cues: focus, origin</sub>

> **ON SCREEN** — \operatorname*{arg\,min}_{z}\;(\lVert z\rVert^2+D)=0

Because the standard normal has a known mean and variance, we can evaluate
this expectation exactly. If we expand the square, the first term is the
squared length of z. The cross term contains the mean of z star, which is
zero. And z star has D coordinates with variance one, so its expected squared
length is D. The average loss is therefore the squared length of z, plus D.
Since D is constant, the pointwise minimum is z equals zero.

<sub>cues: equation, mean, energy, simplify, constant, minimum</sub>

But this gives us the wrong loss: now every embedding gets pulled toward zero.
So the pointwise minimum puts the whole batch at the collapsed point we
started with. If the goal is the shape of the blue collection, then the loss
has to compare distributions rather than assign partners.

<sub>cues: collection, measure</sub>

---

## c03_one_shadow

*Chapter C.03 — one projection gives a scalar batch.*

> **ON SCREEN** — \mathbb R^D\longrightarrow\mathbb R

In the last chapter, the Epps-Pulley score started with a batch of scalars,
but our model gives us a cloud of vectors. So before we can use that score, we
need a way to turn vectors into scalars. Suppose we choose one direction, u,
through the cloud. We keep u at unit length, because otherwise changing its
length would rescale every number we are about to measure.

<sub>cues: need, gives, bridge, direction, unit</sub>

Now suppose we take one embedding, z sub i. If we drop it perpendicularly onto
the line, then its signed position is u transpose z sub i. This foot lands on
the side u points toward, so the coordinate is positive. Pick a point on the
other side instead. Its foot lands behind the origin, so the coordinate
becomes negative.

<sub>cues: drop, read, positive, other, negative</sub>

> **ON SCREEN** — \{u^\top z_i\}_{i=1}^{N}\subset\mathbb R

So now we do the same thing for every embedding. Then the vectors become N
signed coordinates, which form a one-dimensional shadow of the cloud. The
vector cloud has become a scalar batch.

<sub>cues: all, shadow, batch</sub>

We can now run the Epps-Pulley test on this shadow and compare it with a
standard Gaussian.

<sub>cues: rig</sub>

As t changes, each scalar wraps around the circle, and their average traces
the blue empirical characteristic function. Once that blue curve is drawn, we
can compare it with the standard-normal curve. Wherever the two curves
separate, the red marker shows the gap at the current value of t, while the
weighted squared gap fills in behind it. If the curves stay close, little
accumulates. If they pull apart, more accumulates. At the end, all of those
gaps combine into one score for this shadow.

<sub>cues: frequency, target, gap, score</sub>

That is a small score, so along this direction, the shadow looks close to the
target.

But this is still only one shadow. We chose u first, so the score belongs to
that direction. Now, if we turn u, every projected point moves, and the score
changes with the shadow. Turn u again, and both change again. So one direction
can tell us whether one shadow looks Gaussian, but it cannot tell us whether
the whole cloud does.

<sub>cues: turn_one, turn_two, shadow_only, whole</sub>

---

## c04_one_shadow_is_not_enough

*Chapter C.04 — one shadow can be innocent.*

Now suppose the cloud has structure. Two clumps, pulled well apart, in a plane
we can look straight down at.

<sub>cues: clumps</sub>

> **ON SCREEN** — score along each direction

Take the direction the clumps separate along. Then the shadow comes out as two
piles with a hole between them, and a Gaussian has no hole in the middle. So
the score climbs.

<sub>cues: along, piles, gaussian, high</sub>

Now turn that direction a quarter of the way round. The two piles slide
straight through each other, and what is left is a single hump. The score
drops to almost nothing.

<sub>cues: turn, merge, bell</sub>

Keep turning and the hole opens again. Every direction in the plane has its
own score, and half a turn covers all of them.

<sub>cues: keep, trace</sub>

Seventeen here, and almost zero here. And half of every direction in this
plane sits down in that band. So pick one of them, and this cloud passes. A
low score tells you about the direction you picked. It tells you nothing about
the cloud behind it.

<sub>cues: band, verdict</sub>

---

## c05_gaussian_marginals

*Chapter C.05 — coordinate checks can miss a bad joint cloud.*

One direction wasn't enough, so a natural shortcut is to try the two
coordinate axes. Start with the horizontal coordinate: project every point
straight onto that axis. Those projected values line up closely with the
standard bell, so its score is low.

<sub>cues: x_drop, x_stack</sub>

Now turn the same projection onto the vertical axis. Nothing changes, because
each vertical coordinate copies its horizontal partner. It is the same batch,
with the same low score.

<sub>cues: y_turn, y_settle</sub>

But those two checks never compare the coordinates. So turn the line forty-
five degrees, toward the diagonal that subtracts one from the other. Since the
coordinates are equal, every projection lands at zero. Both coordinate scores
were low while the cloud still lay on a line. The axes miss this dependence,
so we have to test directions that mix the coordinates.

<sub>cues: mix, zero, verdict</sub>

---
