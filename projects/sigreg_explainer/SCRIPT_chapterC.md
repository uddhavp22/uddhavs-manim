# Master script — `chapterC`

**Generated — do not edit.** Regenerate with:

```bash
python3 tools/script_dump.py projects/sigreg_explainer/chapterC \
    -o projects/sigreg_explainer/SCRIPT_chapterC.md
```

Extracted from `self.voiceover(text=…)` in the scene files, which is what
the render actually speaks. On-screen text is included as a second
channel — [`NARRATION_SPEC.md`](../../docs/NARRATION_SPEC.md) §7.2 treats it as
one, and a line cut from the voice and left on screen is not cut.

Scenes follow the chapter's playback order. Ordering within a scene is
source order, which tracks playback order but
is not guaranteed to equal it: on-screen text is often constructed a few
lines before the passage that reveals it.

**9 scenes · 3,496 spoken words · 0:00**

| Scene | Words | Duration | Words/min |
|---|---:|---:|---:|
| [`c01_vectors`](#c01-vectors) | 155 | — | — |
| [`c02_the_shape_is_the_goal`](#c02-the-shape-is-the-goal) | 552 | — | — |
| [`c03_one_shadow`](#c03-one-shadow) | 413 | — | — |
| [`c04_one_shadow_is_not_enough`](#c04-one-shadow-is-not-enough) | 192 | — | — |
| [`c05_gaussian_marginals`](#c05-gaussian-marginals) | 177 | — | — |
| [`c06_every_direction`](#c06-every-direction) | 910 | — | — |
| [`c07_sampling_directions`](#c07-sampling-directions) | 453 | — | — |
| [`c08_frequency_knots`](#c08-frequency-knots) | 302 | — | — |
| [`c09_assembling_sigreg`](#c09-assembling-sigreg) | 342 | — | — |

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

One direction wasn't enough. The coordinate axes give us two natural
directions to try next: horizontal and vertical. Start with the horizontal
one. Drop every point straight onto that axis. Those landing positions are the
horizontal coordinates. They line up closely with the standard bell, so the
score is low.

<sub>cues: x_drop, x_stack</sub>

Now, if we turn that same projection onto the vertical axis, then nothing
changes. Each vertical coordinate copies its horizontal partner, so we get the
same batch and the same low score.

<sub>cues: y_turn, y_settle</sub>

But this strategy checks each coordinate separately. It never asks whether
they move together. So turn the line forty-five degrees, toward the diagonal
that subtracts one coordinate from the other. Since the coordinates are equal,
every point lands at zero. Both axis scores were low even though the cloud
still lies on a line. The axes miss this dependence, so we have to test
directions that mix the coordinates.

<sub>cues: mix, zero, verdict</sub>

---

## c06_every_direction

*Chapter C.06 — every direction produces a batch, and all batches identify the cloud.*

Keep turning the direction u. Every new angle gives us another shadow of the
same cloud, and every shadow has its own characteristic function. So if we let
u go all the way around, we get one characteristic function for every
direction there is. One direction was enough to catch this cloud lying on a
line. Does the whole family pin the cloud down completely?

<sub>cues: turn, fill, ask, line, family</sub>

> **ON SCREEN** — u^\top Z\sim\mathcal N(0,\,u^\top I u)=\mathcal N(0,1)

> **ON SCREEN** — \mathrm{Var}[u^\top Z]\approx

Suppose the cloud itself is standard Gauss-ian. Then its co-variance is the
identity, so if we project onto any unit direction, the variance is exactly
one. We can turn u wherever we like, and that number does not move. So every
direction gives the same standard Gauss-ian shadow, and that one bell is the
target every shadow has to match.

<sub>cues: gaussian, spread, hold, turn</sub>

> **ON SCREEN** — \varphi_{u^\top Z}(t)

> **ON SCREEN** — \varphi_{u^\top Z}(t)=\mathbb E\!\left[e^{it(u^\top Z)}\right]

> **ON SCREEN** — =\mathbb E\!\left[e^{i(tu)^\top Z}\right]

> **ON SCREEN** — frequency space

Now take one shadow on its own. Its characteristic function wraps each shadow
value, u transpose z, at frequency t. But t and u only ever reach the cloud
together, so we can gather them into one vector, t u. That turns the average
into the cloud's own characteristic function, at that single vector. So u
chooses a ray out of the origin, and t is how far along it we are. Run t up,
and the shadow's curve is reading the cloud along that one ray.

<sub>cues: one, cf, regroup, point, meaning, trace</sub>

That curve gives us each value as a height. But we can lay the same value down
as brightness instead, right at the point t u. Then the whole curve becomes
one line of light along the ray, bright at the origin and fading as the curve
falls. So turn u. Every point of frequency space lies along some direction, at
some distance, so the sweep leaves nothing out. And that is the cloud's
characteristic function, everywhere at once.

<sub>cues: encode, at, lit, sweep, fill, plane</sub>

> **ON SCREEN** — \varphi_{u^\top Z}(t)

> **ON SCREEN** — Gaussian cloud

> **ON SCREEN** — ring cloud

> **ON SCREEN** — Gaussian cloud

> **ON SCREEN** — \varphi_{u^\top Y}(t)

> **ON SCREEN** — \mathbb E[Z]=\mathbb E[Y]=0

Now a second cloud. We take the same points and push them out onto a ring, so
the middle empties. Its mean is still zero, and its co-variance is still the
identity. So we are right back where the last chapter started, now with clouds
instead of numbers: the summary numbers agree, and the shapes plainly do not.

<sub>cues: second, moments, cov, differ</sub>

So project both clouds onto the same direction. The Gauss-ian's shadow is one
hump. The ring's is two piles pushed to the sides. But their characteristic
functions do tell them apart. The ring's curve dips below zero, where the
Gauss-ian's is still falling smoothly. That gap is exactly what the Epps-
Pulley score was built to measure, so one direction already separates two
clouds the moments could not. Sweep u on the ring too, and the difference
covers the whole plane: the Gauss-ian's field fades out smoothly, the ring's
has a bright core, and then a red band where its curve went below zero.

<sub>cues: project, shadows, curves, gap, fields, smooth, core, band</sub>

Now, if we move the ring's points back, a few at a time, into the positions
the Gauss-ian's points occupy, then its shadow closes into a single hump, its
curve climbs toward the Gauss-ian's, and the red band in its field fades away.
The two fields only agree once the two clouds do.

<sub>cues: push, follow, meet</sub>

> **ON SCREEN** — \varphi_{u^\top Z}(t)=\varphi_{u^\top Y}(t)\quad\forall u,t

> **ON SCREEN** — \Longrightarrow\ \varphi_Z(\xi)=\varphi_Y(\xi)\quad\forall\xi

> **ON SCREEN** — \Longrightarrow\ Z\overset{d}{=}Y

So suppose two clouds cast the same shadow in every direction. Then every ray
carries the same brightness for both, and their characteristic functions agree
at every point of the plane. And two distributions with the same
characteristic function everywhere are the same distribution. Every direction,
every frequency, and the two clouds have to be the same. That implication is
the Cramer Wold theorem.

<sub>cues: if, agree, unique, statement, name</sub>

> **ON SCREEN** — \varphi_{u^\top Z}(t)=e^{-t^2/2}

> **ON SCREEN** — \Longrightarrow\ \varphi_Z(\xi)=e^{-\|\xi\|^2/2}

> **ON SCREEN** — Z\sim\mathcal N(0,I_D)

For our target, every shadow has the same characteristic function, e to the
minus t squared over two. Read along every ray, and the plane fills with e to
the minus the squared distance from the origin, over two. And only one cloud
has that characteristic function: Z itself, standard Gauss-ian in every
dimension.

<sub>cues: specialize, field, resolve, conclude</sub>

That is a bit abstract, so let us bring it back to the problem we actually
have. We have a cloud of embeddings in D dimensions, and we want it to be a
standard Gauss-ian. We can never see the whole cloud. But we can pick a
direction, project every point onto it, and look at the batch of numbers we
get. That is a one-dimensional batch, and we already know how to score it
against the standard bell. Turn u, and we can score another. The theorem says
that if the score passes in every direction, the cloud is the standard Gauss-
ian, and we never had to look at it in D dimensions.

<sub>cues: ground, cloud, pick, project, batch, test, again, family</sub>

---

## c07_sampling_directions

*Chapter C.07 -- every direction is a sphere, so the loss samples M of them.*

> **ON SCREEN** — Z\sim\mathcal N(0,I_D)

So the test has to pass in every direction. The trouble is that every
direction is another shadow we would have to score, and there is no end of
them. In D dimensions, the directions make a whole sphere.

<sub>cues: dense, more, sphere</sub>

> **ON SCREEN** — g\sim\mathcal N(0,I_D)

So we sample instead. To draw a direction, we take a random vector with a
Gauss-ian in every coordinate, and scale it to length one, so it lands on the
ring. If we do that fifty times, the landings spread evenly all the way round.
That is because a Gauss-ian is round, so it has no preferred direction.

<sub>cues: draw, norm, spray, round</sub>

Now if we project the cloud onto that direction, we get a shadow, and we can
score it against the bell the way we already do. The score measures the
mismatch, so this direction gives us one number. If we draw a second direction
and do the same, we get a lower score, because its shadow is different.

<sub>cues: project, gap, score1, second, score2</sub>

> **ON SCREEN** — direction of u

In fact, every direction has its own score. So if we turn u through a half
turn and keep reading the score as it goes, we get a whole curve.

<sub>cues: room, sweep</sub>

Our two draws were just two readings off this curve. What the loss actually
wants is the score averaged over every direction, which on this picture is the
average height of the curve.

<sub>cues: marks, mean</sub>

In two dimensions we could just sweep the whole ring and be done. But in D
dimensions the sphere has no single sweep, so the loss cannot trace this
curve. What it can do is read the curve at the directions it happens to draw.
So we draw a third direction, read its score off the curve, and average the
three. Then we keep drawing. After the first few draws the average has mostly
settled, and by thirty-two it barely moves. That number of draws is what we
call M.

<sub>cues: why, one, onemark, average, more, eight, many, M</sub>

If we draw a different thirty-two, the readings land in different places, but
the average comes out almost the same. What does not change is the curve
itself. It belongs to this batch of two hundred points, so drawing more
directions only reads it more closely, and the only thing that would move it
is a different batch.

<sub>cues: redraw, same, batch</sub>

---

## c08_frequency_knots

*Chapter C.08 -- each score is an integral over every frequency; K knots.*

> **ON SCREEN** — \mathcal T=

> **ON SCREEN** — \mathcal T\approx

> **ON SCREEN** — [\,0.2,\ 4\,]

Now, each of those scores is still an integral, so we have the same problem
one level down. Take the second direction, the one that scored zero point zero
four nine. If we compare its shadow's fingerprint with the Gauss-ian's at
every frequency, square the gap, and weight it with the taper from before, we
get this curve, and the score is the area underneath it. But we can't actually
add up over every frequency, any more than we could visit every direction.

<sub>cues: formula, axes, compare, gap, weight, curve, area, cannot</sub>

So we do the same thing we did with directions. We pick a handful of
frequencies inside the window, read off the height of the curve at each one,
and add up the trapezoids in between. If we try that with just four knots, the
sum comes out at zero point zero seven one, which is a long way off.

<sub>cues: window, read, trap, four</sub>

But if we go up to eight knots, the sum is already zero point zero four nine,
within a twentieth of a percent of the true area. And if we double that to
sixteen, the trapezoids hug the curve so closely that the sum matches the area
to every digit we're showing. Past that there's really nothing left to gain,
so sixteen is what we use, and that number of knots is what we call K.

<sub>cues: eight, sixteen, enough, name</sub>

So back in the formula, the integral over every frequency turns into a sum
over our K knots, and now the score is something we can actually compute.

<sub>cues: sum, compute</sub>

---

## c09_assembling_sigreg

*Chapter C.09 -- the whole loss in one line, and its name.*

So now we have everything we need, and we can write the whole loss down in one
line. Each piece of it is something we have already watched, so let's put them
together in order.

<sub>cues: clear, park</sub>

We start with the batch Z and one direction u that we drew at random. If we
project the cloud onto u, every point turns into one number. Written out, that
is u transpose Z, and the little m just counts which of our draws it was.

<sub>cues: cloud, project, symbol, m</sub>

Then we score those numbers against the standard Gauss-ian. That score is
exactly the sum we just built, with K knots inside the taper of width lambda,
so we can fold all of it into one symbol, T, and keep lambda inside the
brackets so we don't forget it is part of the score.

<sub>cues: score, sum, knots, taper, fold, lambda</sub>

Then we do the same for every direction we drew, all thirty-two of them, and
take the average. The one over M and the sum are just that average, written
out.

<sub>cues: panel, average, wrap</sub>

And that is the whole regularizer. LeJEPA calls it SIGReg, for sketched
isotropic Gauss-ian regularization. Sketched, because we only ever look at M
directions, and isotropic Gauss-ian, because that is the target every shadow
gets compared with.

<sub>cues: whole, name, sketched, gaussian</sub>

And for the batch we have been watching, with thirty-two directions and
sixteen knots, the whole line comes out at zero point zero nine zero, which is
the number the purple line was already showing. So now we know what it
computes. What we have not seen yet is what it does to a cloud.

<sub>cues: batch, M, K, number, same, park, tease</sub>

---
