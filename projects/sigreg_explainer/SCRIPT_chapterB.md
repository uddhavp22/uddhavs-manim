# Master script — `chapterB`

**Generated — do not edit.** Regenerate with:

```bash
python3 tools/script_dump.py projects/sigreg_explainer/chapterB \
    -o projects/sigreg_explainer/SCRIPT_chapterB.md
```

Extracted from `self.voiceover(text=…)` in the scene files, which is what
the render actually speaks. On-screen text is included as a second
channel — [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) §7.2 treats it as
one, and a line cut from the voice and left on screen is not cut.

Ordering within a scene is source order, which tracks playback order but
is not guaranteed to equal it: on-screen text is often constructed a few
lines before the passage that reveals it.

**13 scenes · 3,712 spoken words · 19:48**

| Scene | Words | Duration | Words/min |
|---|---:|---:|---:|
| [`b00_the_problem`](#b00-the-problem) | 272 | 1:22 | 197 |
| [`b01_arrows`](#b01-arrows) | 255 | 1:15 | 202 |
| [`b02_the_rig`](#b02-the-rig) | 234 | 1:10 | 198 |
| [`b05_real_and_imaginary`](#b05-real-and-imaginary) | 242 | 1:17 | 187 |
| [`b06_worked_examples`](#b06-worked-examples) | 142 | 0:48 | 177 |
| [`b06a_one_speed_fails`](#b06a-one-speed-fails) | 169 | 0:53 | 189 |
| [`b06b_what_magnitude_ignores`](#b06b-what-magnitude-ignores) | 166 | 0:52 | 188 |
| [`b07_the_anchor`](#b07-the-anchor) | 135 | 0:50 | 162 |
| [`b08_which_frequencies`](#b08-which-frequencies) | 462 | 2:23 | 193 |
| [`b09_uniqueness`](#b09-uniqueness) | 292 | 1:38 | 177 |
| [`b10_why_not_histograms`](#b10-why-not-histograms) | 351 | 1:50 | 191 |
| [`b11_gaussian_fingerprint`](#b11-gaussian-fingerprint) | 510 | 2:49 | 181 |
| [`b12_fingerprint_to_loss`](#b12-fingerprint-to-loss) | 482 | 2:35 | 186 |

---

## b00_the_problem

*Chapter B, opening — why summary statistics are not enough.*

`1:22` · [`b00_the_problem.py`](chapterB/b00_the_problem.py)

> **ON SCREEN** — one bell-shaped hump

> **ON SCREEN** — two separated clumps

Forty numbers drawn from a bell curve, laid out on a number line. And forty
more that fall into two separate clumps.

<sub>cues: second</sub>

Both batches hold the same number of samples. Their means agree. Their
variances agree, to two decimal places.

<sub>cues: mean, var</sub>

Every summary either batch offers up so far is identical, and the two pictures
are not. A mean fixes where a batch sits. A variance fixes how far it spreads
from there. Neither one says anything about how the mass is arranged inside
that spread, and the arrangement is the entire difference between one hump and
two.

> **ON SCREEN** — How many would be enough?

The usual next move is to add more summaries. Skewness measures asymmetry,
kurtosis measures the weight in the tails, and past those there is an
unlimited supply of higher moments. Each one catches something the previous
ones missed, which leaves a question nothing on this list answers.

<sub>cues: ask</sub>

> **ON SCREEN** — one differentiable score

What would settle it is a description of the whole distribution, rather than a
longer list of numbers taken from it.

> **ON SCREEN** — Samples are all that arrives. There may be no density formula to compare against.

> **ON SCREEN** — The comparison becomes a training loss, so moving one sample must move the score smoothly.

Two things constrain what such a description can be. A batch of samples is all
that ever arrives, so there may be no density formula available to compare
against. And the comparison has to end up as a training loss, which means
moving any single sample has to change the score smoothly, by an amount
gradient descent can follow.

<sub>cues: one, two</sub>

> **ON SCREEN** — a complete description

> **ON SCREEN** — one differentiable score

Both constraints have to hold at once. What follows asks the same batch a
whole family of questions, one frequency at a time, and keeps every answer.

<sub>cues: pipe</sub>

---

## b01_arrows

*Chapter B.1 — complex numbers as arrows.*

`1:15` · [`b01_arrows.py`](chapterB/b01_arrows.py)

Sideways measures the real part of a complex number, upward the imaginary
part.

The number a plus b i is the point with coordinates a and b. The picture that
will matter is the arrow from the origin out to that point, because the
operation this chapter keeps needing is addition, and arrows add tip to tail.

<sub>cues: arrow</sub>

Restrict to arrows of length one and each is determined by a single number,
its angle. The unit arrow at angle theta is written e to the i theta, and
raising theta walks it round the circle at a steady rate.

<sub>cues: name</sub>

> **ON SCREEN** — how far right

> **ON SCREEN** — how far up

Its sideways and upward components are the cosine and the sine of theta.
Euler's identity, read off the picture: how far right the arrow reaches, and
how far up.

<sub>cues: eq</sub>

Arrows add tip to tail, so a set of them has an average: the sum, divided by
how many there are. Six arrows pointing roughly the same way average to
something almost as long as they are.

<sub>cues: avg</sub>

Spread the same six around the circle and their components start cancelling
against one another, which pulls the average in toward the centre. Evenly
spaced, the cancellation is exact and the average is zero.

So the length of that average measures how much a set of angles agree: one
when they coincide, zero when they are spread evenly, and something in between
otherwise. The angles have been arbitrary so far. The next step is to get them
from data.

---

## b02_the_rig

*Chapter B.2-4 — the three-panel rig.*

`1:10` · [`b02_the_rig.py`](chapterB/b02_the_rig.py)

Seven measurements on a line. To reuse the arrow picture, each measurement has
to become an angle, and multiplying by a frequency t is the least elaborate
way to turn a position into one. Wrapping the line around the circle is that
multiplication, drawn.

<sub>cues: wrap</sub>

A value x lands at the angle t x, so samples further from zero travel further
round.

Each landing point is a unit arrow, and their average is a single point inside
the circle.

<sub>cues: avg</sub>

That average is one complex number, and plotting its horizontal coordinate
against t, on the right, gives the first point of a curve.

Raising t moves two of the three panels. The samples on the left do not move
at all: the data is fixed, and only the question being asked of it changes. On
the circle, samples further from zero accumulate angle faster, so over this
early stretch the arrows separate and the average is pulled in toward the
centre. Keep going and the arrows carry on turning, fall part way back into
step, and the average grows again. The curve on the right records where that
average keeps landing, and it rises and falls as the arrows drift in and out
of step.

One frequency produced one point. Sweeping t produced the curve. What is not
yet clear is how much about the batch that curve still remembers.

---

## b05_real_and_imaginary

*Chapter B.5 — the two components of phi(t).*

`1:17` · [`b05_real_and_imaginary.py`](chapterB/b05_real_and_imaginary.py)

> **ON SCREEN** — how far right, on average

> **ON SCREEN** — how far up, on average

Every curve so far has plotted one number, the horizontal coordinate of the
average arrow. An arrow in the plane has two coordinates, and the second one
has been discarded at every frequency.

Split the average into its components. The blue piece is how far right the
arrows point on average, the red piece how far up. Those are the real and
imaginary parts of phi.

<sub>cues: split</sub>

Averaging the cosines gives the sideways component, averaging the sines gives
the upward one.

Blue tracks the sideways coordinate of the average arrow and red tracks the
upward one. Read them together and they describe one point moving in the
plane, which is why dropping either curve loses information the other cannot
supply.

This batch is symmetric about zero: every value has a partner the same
distance away on the other side.

Each pair wraps to a pair of arrows at opposite angles, so whatever one
contributes upward the other contributes downward by the same amount. The
vertical components cancel pair by pair, which leaves the average nowhere to
go except along the horizontal axis.

The sweep agrees: the red curve sits at exactly zero across the whole range.

So a symmetric distribution has a purely real characteristic function. The
Gaussian is symmetric, so the target this chapter is heading toward will be a
single real curve, and now that follows from the pairing argument instead of
being a convenience of the drawing.

---

## b06_worked_examples

*Chapter B.6 — two worked examples on the rig.*

`0:48` · [`b06_worked_examples.py`](chapterB/b06_worked_examples.py)

> **ON SCREEN** — every value the same

Take a batch in which every value is the same number.

Equal values wrap to equal angles, so the arrows stay stacked on top of one
another however fast the winding goes. With nothing pointing in a different
direction there is nothing to cancel, and the average keeps its full length at
every frequency.

A flat line at one is the signature of complete collapse.

The simplest non-degenerate case: two values, minus one and plus one, equally
likely.

The two arrows sit at angles t and minus t, mirror images across the real
axis. Their vertical components cancel by the same pairing as before, so only
the horizontal ones survive, and the average traces out the cosine.

Every arrow in this batch is at angle plus or minus t, so the average is the
cosine of t, exactly, at every frequency.

---

## b06a_one_speed_fails

*Chapter B — one wrapping speed is not enough.*

`0:53` · [`b06a_one_speed_fails.py`](chapterB/b06a_one_speed_fails.py)

Sweeping every frequency is expensive. If one well chosen value of t did the
job, the sweep would be waste.

This batch is spread across nearly thirteen units. By any reasonable reading
it has not collapsed.

> **ON SCREEN** — every arrow lands on the same spot

Wrapped at this particular frequency, though, every arrow lands on the same
spot and the average has length one. Which is the reading a completely
collapsed batch would produce.

<sub>cues: verdict</sub>

The agreement survives almost no change in t. Nudge the frequency and the
arrows scatter, and the average falls away to almost nothing.

The samples happened to be spaced at multiples of the wrapping period, and any
single frequency has a batch built the same way. Asking at several frequencies
breaks this particular coincidence, because no batch can be in step with all
of them at once. Whether finitely many frequencies are enough to separate any
two distributions is a stronger question, and the answer to it belongs to the
whole curve rather than to any list of points on it.

---

## b06b_what_magnitude_ignores

*Chapter B.6b — what the magnitude ignores.*

`0:52` · [`b06b_what_magnitude_ignores.py`](chapterB/b06b_what_magnitude_ignores.py)

Take any batch, and alongside its curve draw the length of the average arrow
in amber.

Sweep once, and the amber curve drops almost to zero before creeping back up.

Now slide every value along the line by the same amount, and sweep again.

The blue curve changes completely while the amber one lands back on its own
ghost. Sliding every sample by the same amount adds the same angle to every
arrow, so the average rotates as a rigid object, and a rotation leaves length
alone.

> **ON SCREEN** — the shift moved the phase, and only the phase

Moving a batch multiplies its characteristic function by a factor of magnitude
one. Everything the shift did is in the phase, and the magnitude did not see
it at all.

So location and magnitude can be asked about separately. What the magnitude
does keep is the shape of the batch and how far it spreads, together, and
untangling those two takes a family of distributions narrow enough that one
number settles it. The Gaussian is a family that narrow.

---

## b07_the_anchor

*Chapter B.7 — phi(0) = 1, for every distribution there has ever been.*

`0:50` · [`b07_the_anchor.py`](chapterB/b07_the_anchor.py)

Set the frequency to zero. The product t x is zero whatever x was, so every
value in the batch produces the same angle, every arrow is the unit arrow
pointing right, and they stack on top of one another.

<sub>cues: same</sub>

Averaging identical arrows returns the same arrow, so phi of zero is one. The
data never entered that argument, which is what makes the result hold for
every distribution rather than for this batch.

<sub>cues: note</sub>

Three batches with nothing in common.

Three different curves, all leaving from the same point. Every characteristic
function is already normalised at the origin, so no curve has to be rescaled
before it is read: a height near one means the arrows still agree, and a
height falling away means they have begun to cancel.

---

## b08_which_frequencies

*Chapter B.8 — which frequencies are worth looking at.*

`2:23` · [`b08_which_frequencies.py`](chapterB/b08_which_frequencies.py)

> **ON SCREEN** — same mean, same variance — different shapes

> **ON SCREEN** — bell curve

> **ON SCREEN** — two clumps

Back to the two batches from the start: same mean, same variance, different
shapes. These are their two characteristic functions.

Starting the frequency low and creeping up, only one curve appears to be on
screen. Both are drawn; they are sitting on top of each other.

> **ON SCREEN** — low t: coarse structure only

At a frequency of nought point three the two curves differ by two thousandths.
Slow wrapping turns a whole batch through only a small angle, so it can
register roughly where the batch sits and roughly how wide it is, and little
else. Those are the two facts that already failed to separate these batches.

Keep going.

Once the wrapping is fast enough that the two clumps land at genuinely
different angles, the curves separate: the red one dives negative while the
blue flattens out near zero. By a frequency of three the gap is nine tenths.
Fine structure shows up at high frequency, not low.

Which suggests pushing the frequency as high as it will go. That fails, for a
reason that has nothing to do with the mathematics of the transform.

<sub>cues: no</sub>

A distribution is never what arrives. A batch is. So: forty numbers drawn from
a genuine bell curve, twenty separate times, with all twenty curves plotted.

The amber curve is the population characteristic function they were all drawn
from. The blue ones are what forty samples actually produce.

<sub>cues: draws</sub>

> **ON SCREEN** — out here the truth is zero —

> **ON SCREEN** — everything you see is sampling noise

At the right-hand end the population curve has been flat at zero for some
time, while the twenty draws are still wandering. Nothing in that wandering is
a property of the bell curve. It is the accident of which forty numbers came
out.

> **ON SCREEN** — measured at t = 6, N = 40: 0.0251 against 1/N = 0.0250

> **ON SCREEN** — the true value there is 2 × 10⁻¹⁶

That wandering has a predictable size. Where the population curve is zero, the
expected squared length of the empirical average settles at one over N: with
forty samples, nought point nought two five. Measured over four thousand draws
it comes out at nought point nought two five one. So a perfectly Gaussian
batch reads as non-Gaussian at high frequency purely because it is finite.

> **ON SCREEN** — too low: blind to shape

> **ON SCREEN** — too high: nothing but noise

Both ends are therefore ruled out for different reasons. Too low and the curve
cannot resolve a shape. Too high and it is reading its own sampling noise.

<sub>cues: right</sub>

What survives is a band in the middle. For a standard normal target that band
runs from about nought point two to four, and it carries over ninety-nine per
cent of the separating power.

<sub>cues: win</sub>

> **ON SCREEN** — Something has to suppress the high frequencies.

> **ON SCREEN** — That much is forced by having finitely many samples.

This is why the published statistic suppresses high frequencies. The
suppression is not tuning for its own sake: past some frequency the
measurement is dominated by sampling noise, so a cut has to exist. Where
exactly it falls is a bandwidth parameter, and the source is explicit that
someone chooses it.

---

## b09_uniqueness

*Chapter B.9 — why knowing every frequency is knowing the distribution.*

`1:38` · [`b09_uniqueness.py`](chapterB/b09_uniqueness.py)

> **ON SCREEN** — a sound

A sound, drawn as a pressure wave. In that form there is not much to hold on
to: no obvious quantity to compare against another sound.

The same sound decomposes into pure tones, and each tone carries a single
number, its amplitude.

Adding the tones back reconstructs the original wave exactly, not an
approximation to it.

> **ON SCREEN** — same amplitudes

So the list of amplitudes loses nothing: it is the same object in a different
coordinate system. Two sounds with the same list are the same sound.

The characteristic function stands in the same relation to a distribution. The
two situations are connected literally: both objects are Fourier transforms.

> **ON SCREEN** — a sound

> **ON SCREEN** — its amplitude at each tone

> **ON SCREEN** — a distribution

> **ON SCREEN** — its average arrow at each frequency

A sound is determined by how much of each tone it contains. A distribution is
determined by where its average arrow lands at each wrapping frequency.

<sub>cues: dist</sub>

> **ON SCREEN** — the uniqueness theorem

Written out, that is the uniqueness theorem: if two distributions have the
same characteristic function at every frequency, they are the same
distribution. Because the curve determines the distribution completely,
calling it a fingerprint is accurate rather than decorative, and that is the
sense the word carries for the rest of the video.

No proof here. It runs through an inversion formula that recovers the density
from the curve, which is a video of its own. The theorem is being cited, not
established, and everything after this depends on it.

The precision matters. Without the theorem, matching fingerprints would be a
proxy for matching distributions: suggestive, and no more. With it, the two
are the same statement.

> **ON SCREEN** — loss on fingerprints = 0

> **ON SCREEN** — not: the distributions are similar

> **ON SCREEN** — but: the distributions are equal

So a loss built from fingerprints, driven to zero, licenses the statement that
the distributions are equal, not merely that they resemble each other. That
licence comes from the theorem, and it is what the whole detour through the
transform buys.

---

## b10_why_not_histograms

*Chapter B.10 — the obvious alternative, and why it cannot be used.*

`1:50` · [`b10_why_not_histograms.py`](chapterB/b10_why_not_histograms.py)

> **ON SCREEN** — the obvious alternative: just bin it

There is a much more direct way to compare a batch against a bell curve. Chop
the line into bins, count how many samples land in each, and compare the
counts against what the bell curve predicts. Three objections rule it out, and
the third is the one that matters.

> **ON SCREEN** — the data has not moved — only the bin edges

The first: nothing in the data determines where the bins should start. Sliding
the edges along, without moving a single sample, changes the counts.

<sub>cues: slide</sub>

Counts before, counts after. The same forty numbers, and a different answer,
so any score built on top inherits an arbitrary choice.

The second objection is sharper. Bin width is also a free choice. This is the
two-clump batch, the one the mean and variance could not separate.

At a narrow width the two clumps are unmistakable. Widening the bins erases
them: at a width of one and a half the counts read two, fourteen, twenty-four,
zero, which reads as one lopsided hump. The structure the score exists to
detect can be removed by a parameter the analyst sets.

<sub>cues: gone</sub>

Both of those are arguments about arbitrariness. The third one is not.

> **ON SCREEN** — position of one sample

> **ON SCREEN** — count in its bin

Slide one sample slowly across a bin edge. The count does not ease from seven
down to six. It holds at seven, and then it is six.

> **ON SCREEN** — almost everywhere,

> **ON SCREEN** — undefined at the steps

A thousandth of a step moves the answer by a whole unit. The derivative of a
bin count with respect to a sample is therefore zero almost everywhere and
undefined at the jumps, which leaves gradient descent nothing to descend.

<sub>cues: grad</sub>

> **ON SCREEN** — histogram bin count

> **ON SCREEN** — a staircase in the data

> **ON SCREEN** — defined at every point

> **ON SCREEN** — never zero

> **ON SCREEN** — and it grows with t — high frequencies push hardest

The wrapped sample behaves differently. Differentiating e to the i t x with
respect to x returns i t times the same quantity.

Defined everywhere, never zero, and growing with the frequency. Nudging a
sample moves every value of the characteristic function smoothly, which is the
property that lets this sit inside a training loop.

> **ON SCREEN** — histogram: d(count)/dx = 0 almost everywhere

> **ON SCREEN** — wrapped sample: d/dx = i t · e^{itx}, never zero

So the choice of the complex exponential is doing work here that a histogram
cannot do at all, and the next question is how to turn two of these curves
into one number.

---

## b11_gaussian_fingerprint

*Chapter B.11 — the full derivation of the Gaussian fingerprint e^{-t^2/2}.*

`2:49` · [`b11_gaussian_fingerprint.py`](chapterB/b11_gaussian_fingerprint.py)

Comparing a batch against a Gaussian needs the Gaussian's own characteristic
function, and so far it has only been asserted to be a bell curve. It can be
derived in about two minutes.

The standard normal density. Nothing beyond this formula gets assumed.

> **ON SCREEN** — differentiate once: p'(x) = −x p(x)

Differentiating once, the exponent brings down a factor of minus x and what
remains is the density itself. So p prime of x equals minus x times p of x.

<sub>cues: key</sub>

That identity carries the derivation. It says the Gaussian's derivative is the
Gaussian again, up to a factor of x, and that is the property no other common
density has in so usable a form.

> **ON SCREEN** — differentiate under the integral

The characteristic function of that density is the same average arrow as
before. A formula has replaced the samples, so the average is written as an
integral.

Differentiate both sides with respect to t. Only the wrapped term carries a t,
and differentiating it brings down a factor of i x.

The integral now contains x times the density, which the identity from a
moment ago says is minus p prime of x. Substituting removes the x.

<sub>cues: sub</sub>

With the x gone, the integral is no longer a harder object than the one it
came from. That was the reason for differentiating the density first.

> **ON SCREEN** — boundary terms vanish: the density dies at both ends

Integrating by parts moves the derivative from the density onto the wrapped
term. The boundary terms vanish because the bell curve decays at both ends,
leaving nothing at infinity.

<sub>cues: why</sub>

What comes out is phi again. Substituting back, minus i times minus i t leaves
minus t.

<sub>cues: tidy</sub>

> **ON SCREEN** — a differential equation — no complex analysis needed

Which is a differential equation: the rate of change of phi is minus t times
phi. An integral that could not be evaluated directly has become an equation
that separates.

> **ON SCREEN** — every characteristic function is 1 at the origin

Phi on one side, t on the other. Integrating gives a logarithm on the left and
minus t squared over two on the right, plus a constant.

<sub>cues: int</sub>

The constant is already determined: every characteristic function equals one
at the origin, which was established from the stacked arrows earlier. So C is
zero.

Exponentiating gives the result: the characteristic function of a standard
Gaussian is e to the minus t squared over two. The bell curve transforms into
a bell curve.

Drawn out, this is the curve every batch in the rest of the video gets
measured against.

> **ON SCREEN** — real, and symmetric in t

> **ON SCREEN** — equal to 1 at the origin

> **ON SCREEN** — decays smoothly to zero

All three of its features were predictable from earlier scenes. Purely real,
because the Gaussian is symmetric and symmetric distributions cancel their
vertical components. One at the origin, like every characteristic function.
Decaying, because faster wrapping spreads the arrows of a spread-out batch
further apart.

> **ON SCREEN** — φ(t) = e^{−t²/2} — the target

From here on, asking whether a batch is Gaussian means asking how far its
fingerprint sits from this curve.

> **ON SCREEN** — phase shifts it; decay spreads it

A Gaussian with some other mean and variance gives this, and both new pieces
have appeared before. The mean sits in the phase, as the shift example showed.
The variance sets the decay rate, because a wider distribution spreads its
arrows at a lower frequency.

---

## b12_fingerprint_to_loss

*Chapter B.12 — from a fingerprint to a number you can minimise.*

`2:35` · [`b12_fingerprint_to_loss.py`](chapterB/b12_fingerprint_to_loss.py)

Two curves now exist: the batch's fingerprint, and the one a Gaussian would
give. Turning the pair into a single number is what remains.

Fix one frequency. The batch gives one average arrow there; the Gaussian gives
another. Two arrows, which is to say two points in the complex plane.

<sub>cues: tgt</sub>

Their disagreement is the distance between them.

> **ON SCREEN** — squared, so it is positive

> **ON SCREEN** — and smooth at zero

Squaring that distance makes it positive without introducing a kink at zero,
which the absolute value would, and a kink is exactly what differentiation
cannot cross.

> **ON SCREEN** — squared gap, at every frequency

One number, at one frequency. The band worth reading was settled earlier:
nought point two to four. So repeat the measurement across it.

The red segment on the left is the gap at the current frequency, stretching
and shrinking as the two curves drift apart and back together. Its squared
length is what the right-hand plot records, and the area under that plot
accumulates as the sweep proceeds.

The total area is the score for this batch: one point nought four.

A single score has no scale attached to it, so the same measurement runs on a
batch actually drawn from a bell curve.

The two curves stay close across the whole band, and almost no area
accumulates.

Nought point nought one eight, against one point nought four: a factor of
fifty-six. Nothing in the construction was told what a clump is, or how many
to look for.

> **ON SCREEN** — 0.0184 = the finite-sample floor

> **ON SCREEN** — for N = 40, measured earlier

The residual nought point nought one eight is the sampling floor measured
earlier, appearing where it should. Forty samples cannot produce a smaller
score than that even when the batch is genuinely Gaussian.

Written down, the area that just filled in is this: the squared gap,
integrated over the band.

The published version carries two further pieces. A weight function fades the
high frequencies out smoothly rather than stopping dead at four, with lambda a
bandwidth parameter the analyst sets. A factor of N in front makes scores
comparable across batch sizes. Adding both moves the separation between these
two batches from fifty-six times to fifty-seven.

<sub>cues: full</sub>

Every symbol in it has been on screen already. The squared gap is the red
segment. The integral accumulates it across frequencies. The weight
concentrates on the middle of the range, for the two reasons the sweep
demonstrated: low frequencies cannot resolve shape, and high ones are
dominated by sampling noise.

> **ON SCREEN** — this is the Epps–Pulley statistic

The statistic has a name. It is Epps-Pulley, published as a test of normality
in nineteen eighty-three.

It is differentiable in the samples, which was the requirement the histogram
failed, so gradient descent can push it down.

> **ON SCREEN** — this scores a batch of numbers

> **ON SCREEN** — a representation is a vector

> **ON SCREEN** — in hundreds of dimensions

One problem is left. Everything built so far scores a batch of single numbers,
and a learned representation is a vector in hundreds of dimensions.

Chapter C has to get from a test for one number to a test for a cloud in high
dimension.

---
