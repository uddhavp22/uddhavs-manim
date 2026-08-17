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

Scenes follow the chapter's playback order. Ordering within a scene is
source order, which tracks playback order but
is not guaranteed to equal it: on-screen text is often constructed a few
lines before the passage that reveals it.

**12 scenes · 2,445 spoken words · 0:00**

| Scene | Words | Duration | Words/min |
|---|---:|---:|---:|
| [`b00_the_problem`](#b00-the-problem) | 173 | — | — |
| [`b01_why_not_histograms`](#b01-why-not-histograms) | 151 | — | — |
| [`b02_arrows`](#b02-arrows) | 202 | — | — |
| [`b03_the_rig`](#b03-the-rig) | 406 | — | — |
| [`b04_the_definition`](#b04-the-definition) | 121 | — | — |
| [`b05_worked_examples`](#b05-worked-examples) | 230 | — | — |
| [`b06_the_anchor`](#b06-the-anchor) | 54 | — | — |
| [`b07_one_speed_fails`](#b07-one-speed-fails) | 138 | — | — |
| [`b08_uniqueness`](#b08-uniqueness) | 96 | — | — |
| [`b09_which_frequencies`](#b09-which-frequencies) | 218 | — | — |
| [`b10_gaussian_fingerprint`](#b10-gaussian-fingerprint) | 171 | — | — |
| [`b11_fingerprint_to_loss`](#b11-fingerprint-to-loss) | 485 | — | — |

---

## b00_the_problem

*Chapter B, opening — why summary statistics are not enough.*

> **ON SCREEN** — one bell-shaped hump

> **ON SCREEN** — two separated clumps

Imagine taking forty numbers drawn from a bell curve and laying them out on a
number line. Then draw forty more numbers that fall into two separate clumps.

<sub>cues: second</sub>

These two batches look completely different, yet their sample counts, means,
and variances agree.

<sub>cues: count, mean, var</sub>

> **ON SCREEN** — one score

So the question becomes: can we compress this difference in shape into one
smooth number?

> **ON SCREEN** — s =

Suppose this first pair gives us this number. Now feed the same rule two bell-
shaped batches, and the value falls.

Try a nearly collapsed batch against a spread-out one, and the same rule
responds again.

> **ON SCREEN** — what must the score do?

> **ON SCREEN** — \frac{\partial s}{\partial x_i}\ \text{exists}

Ideally, this score should come directly from the samples themselves, without
assuming we know a density formula.

And if one sample nudges to the side, how should the number respond? Smoothly
enough that gradient descent can tell which way to move it.

One smooth scalar is where we want to end. But we cannot jump straight there.
Before that, we need a description that keeps the shape.

---

## b01_why_not_histograms

*Chapter B.1 — why the obvious shape picture is a bad training loss.*

Mean and variance weren't enough, so let's keep all the samples in view.

<sub>cues: samples</sub>

The first thing you might try is a histogram. Split the number line into bins,
then count how many samples land in each one. This keeps the shape that those
two summary numbers missed.

<sub>cues: bins, counts, shape</sub>

> **ON SCREEN** — bin edge

But the score still has to be differentiable in every sample. Watch what
happens to this one.

<sub>cues: sample</sub>

Inside the bin, both counts stay fixed. But the instant it crosses the edge,
one drops and the other jumps.

<sub>cues: crosses</sub>

So the derivative is zero between edges and undefined at the boundary. That
breaks the differentiability we needed.

<sub>cues: zero, undefined</sub>

We need a smooth question we can ask each sample, so that a small move
produces a small change in its answer.

<sub>cues: small</sub>

> **ON SCREEN** — x_i \longmapsto\ ?

---

## b02_arrows

*Chapter B.2 — complex numbers as arrows.*

> **ON SCREEN** — x_i \longmapsto\ ?

> **ON SCREEN** — x_i \longmapsto \text{a direction}

What we can do is let each sample represent a direction.

> **ON SCREEN** — a + bi

The natural home for those two answers is the complex plane. A point here is
written A, plus B I. A gives its horizontal coordinate, and B gives its
vertical coordinate.

<sub>cues: plane</sub>

Now draw an arrow from the origin to that point. As the point moves, the
direction changes smoothly with it.

Suppose only the direction matters. Then we can set the arrow's length to one,
so a single angle, theta, determines it. We write this unit direction as e to
the i theta.

> **ON SCREEN** — e^{i\theta} = \cos\theta + i\,\sin\theta

> **ON SCREEN** — how far right

> **ON SCREEN** — how far up

The tip gives us two numbers: the cosine of theta horizontally, and the sine
of theta vertically. As theta changes, both move smoothly.

Suppose we take a few directions and average their endpoints. When they point
roughly together, their average stays long.

<sub>cues: avg</sub>

Then, if we spread those arrows around the circle, their components cancel
against one another, pulling the average inward. With equal spacing around the
circle, the cancellation is exact.

> **ON SCREEN** — x_i \longmapsto \theta_i =\ ?

So the average gives us a smooth measure of how well the directions line up.
To connect this back to our samples, we just need a rule for choosing each
angle.

---

## b03_the_rig

*Chapter B.3 — the three-panel rig, built and then read.*

> **ON SCREEN** — x_i \longmapsto \theta_i = {t}x_i

So if we want to wrap these samples around a circle, each one needs an angle.
Take this one. Its position on the line is x sub i.

<sub>cues: each, sample</sub>

The parameter t controls how quickly position turns into angle. For this
sample, the angle is t times x sub i.

<sub>cues: rule, sample_angle</sub>

With an angle attached to every sample, the whole strip can wrap around the
circle.

<sub>cues: wrap</sub>

> **ON SCREEN** — x_i \longmapsto e^{i{t}x_i}

We write the direction as e raised to i t x sub i, where this i is the
imaginary unit, and this i indexes x.

<sub>cues: imaginary_i, index_i</sub>

When we change t, the samples do not move, but their angles on the unit circle
change, and the values farther from zero turn faster. Each t asks the same
batch a different alignment question.

Average the directions. At this value of t, the whole batch leaves one arrow.

<sub>cues: mean</sub>

At one value of t, that arrow lands at one point. The blue graph records only
how far right that point lies.

<sub>cues: project</sub>

If we vary t, we see how the horizontal average traces the curve.

> **ON SCREEN** — how far right, on average

> **ON SCREEN** — how far up, on average

But that curve only tracks where the arrow points sideways. It also has a
vertical coordinate.

<sub>cues: imaginary</sub>

The horizontal and vertical components locate the same endpoint.

<sub>cues: horizontal, vertical</sub>

> **ON SCREEN** — \overline{e^{itx_i}} = \underbrace{\overline{\cos(tx_i)}}_{\text{right}} + i\, \underbrace{\overline{\sin(tx_i)}}_{\text{up}}

Written out, they are the batch averages of the cosine of t times x sub i, and
the sine of t times x sub i. The bar means: evaluate every sample in the
batch, then average the results.

<sub>cues: formula, cosine, sine, bar</sub>

> **ON SCREEN** — both coordinates, against t

One curve follows the horizontal average; the other follows the vertical
average. Together they preserve the average arrow for every t.

<sub>cues: vertical, full</sub>

At t equals zero, every direction equals one, so the average is one.

In a symmetric batch, each x sub i has a partner at negative x sub i.

Those partners have equal and opposite vertical components, so they cancel for
every t. The average stays horizontal, and the vertical curve stays at zero.

Perfect symmetry pins the vertical curve at zero. That is why the Gaussian
target lies on the real axis. But a finite batch rarely contains exact mirror
pairs, so its empirical point can still have a vertical component.

---

## b04_the_definition

*Chapter B.4 — naming and defining the characteristic function.*

> **ON SCREEN** — the empirical characteristic function

To recap, we started with a batch of samples. For each t, every sample became
a direction, and those directions were averaged. Let t vary, and the average
traces this function. This is the empirical characteristic function.

<sub>cues: directions, function, name</sub>

> **ON SCREEN** — \hat\varphi_N(t) = \frac{1}{N}\sum_{j=1}^{N} e^{itx_j}

For the batch we actually have, each sample contributes e to the i t x. Adding
those arrows and dividing by the batch size gives their empirical average.

<sub>cues: wrap, add, divide</sub>

> **ON SCREEN** — \varphi_X(t)=\mathbb E\!\left[e^{itX}\right]

If we knew the full distribution, the same operation would be an expectation.
We only have samples, so the finite average estimates that population
function; the hat keeps the two quantities distinct.

<sub>cues: samples, hat</sub>

---

## b05_worked_examples

*Chapter B.5 — worked examples on one continuous rig.*

> **ON SCREEN** — every value the same

So before trusting what it keeps, we should try the most extreme case, where
every sample is in the same place.

Every value now wraps to the same angle, so nothing would cancel, and the
arrows stay stacked. If we model the magnitude of the arrow, it stays at one.

The flat curve we see is the magnitude of the function, not the characteristic
function itself. For a collapsed batch, its magnitude stays one at every
frequency.

If we try the smallest symmetric batch next, it's minus one and plus one.

Their vertical pieces cancel, while the horizontal pieces agree. Look at the
average as the pair turns.

> **ON SCREEN** — {{\varphi(t) =}} \tfrac{1}{2}e^{it} + \tfrac{1}{2}e^{-it}

> **ON SCREEN** — {{\varphi(t) =}} \cos t

It produces one half of e to the i t, plus one half of e to the minus i t,
which simplifies to the cosine of t.

<sub>cues: simplify</sub>

Put a spread batch back on the circle and track the length of its arrow. As
the frequency climbs, that length nearly vanishes, then rises again.

<sub>cues: sweep</sub>

Suppose all the points shift three units right. The shape hasn't changed, and
we run exactly the same sweep.

Every arrow turns together. The blue curve keeps changing, while the magnitude
returns to its old trace.

> **ON SCREEN** — \varphi_{X+\mu}(t) = e^{i\mu t}\,\varphi_X(t)

> **ON SCREEN** — |e^{i\mu t}| = 1

> **ON SCREEN** — the full complex value still changes

The shift rotates the full complex value, while its magnitude stays the same.
When we compare distributions, we will keep the full complex point.

<sub>cues: why</sub>

---

## b06_the_anchor

*Chapter B.6 — the universal anchor of every characteristic function.*

> **ON SCREEN** — t = 0

Before looking at any particular shape, there is one point we can predict:
when the frequency is zero, every sample lands at angle zero.

The arrows stack at one, so phi of zero is one. Every characteristic function
passes through this exact point, so zero can never tell two batches apart.

<sub>cues: note</sub>

---

## b07_one_speed_fails

*Chapter B.7 — one wrapping speed is not enough.*

Could one carefully chosen value of t identify an entire batch of numbers?

> **ON SCREEN** — sample values

> **ON SCREEN** — wrapped directions

> **ON SCREEN** — t =

> **ON SCREEN** — average length

Suppose the chosen value is t equals two point four. The directions partly
cancel, leaving an average length of about point two three.

<sub>cues: wrap, average</sub>

Now try t equals three. Each angle becomes a whole number of turns, so all
seven directions land together. The average length becomes one, exactly what
total collapse would produce.

<sub>cues: three, align, score</sub>

But if we nudge t back down to two point six, those same samples produce
directions that mostly cancel, which means a single t cannot reliably identify
a batch.

<sub>cues: nudge, settle, conclusion</sub>

One answer can be fooled. So keep the batch's answers across the whole range
of t.

<sub>cues: sweep</sub>

---

## b08_uniqueness

*Chapter B.8 — the complete characteristic function is unique.*

As t varies, those answers fill out the characteristic function.

<sub>cues: curve</sub>

> **ON SCREEN** — \varphi_X(t)=\varphi_Y(t)\quad\text{for every }t

> **ON SCREEN** — uniqueness theorem

The uniqueness theorem tells us how much stronger that full curve is. Two
distributions may agree at one value of t. But if their characteristic
functions agree for every t, then they are the same distribution. We'll use
that result without proving it here.

<sub>cues: one, full</sub>

With a finite batch, we only estimate this curve. Before we turn that estimate
into a score, we need to find out which frequencies are actually useful.

<sub>cues: estimate, where</sub>

---

## b09_which_frequencies

*Chapter B.9 — which frequencies are useful for a finite batch.*

> **ON SCREEN** — bell-shaped batch

> **ON SCREEN** — two clumps

If we place the characteristic functions of our first two batches together,
their gap at t equals point three is close to zero.

<sub>cues: gap</sub>

At t equals three, the difference in their shapes leaves a much larger gap.

> **ON SCREEN** — vertical gap

But larger t is not automatically better. Suppose we take fresh samples from
the same Gaussian. Each batch gives a slightly different estimate of the same
curve.

Near the tail, those estimates spread apart even though the distribution has
not changed. That variation is sampling noise, so it need not represent real
structure.

> **ON SCREEN** — same-Gaussian variation

Condense those Gaussian resamples into this blue band. Its width records the
variation produced by one unchanged distribution. The red curve is the two-
clump batch.

<sub>cues: band, clumps</sub>

Near zero, every characteristic function is anchored at one, so the gap begins
small. Through the middle frequencies, the two-clump curve moves well beyond
ordinary resampling variation. Farther out, that variation becomes a larger
part of what we see.

<sub>cues: middle, tail</sub>

> **ON SCREEN** — frequency influence

So the score should keep every frequency, while letting their influence fade
smoothly into the noisy tail. This taper is the idea we will put into the
final formula.

<sub>cues: taper</sub>

The standard Gaussian now supplies the reference curve that each batch will be
compared with.

---

## b10_gaussian_fingerprint

*Chapter B.10 — reveal the standard Gaussian target curve.*

In a standard Gaussian, each value x is balanced by minus x. At any t, their
vertical arrow components cancel, so its fingerprint stays on the real axis.

<sub>cues: components, real</sub>

And when t equals zero, every arrow points to one, which fixes the curve's
starting point.

<sub>cues: start</sub>

For the standard Gaussian, we average e raised to the imaginary unit times t
times x over the bell curve. Written as an integration, this takes a separate
Gaussian calculation. Its result is e raised to minus t squared over two.
Because of that negative square, the curve falls smoothly from one toward
zero.

<sub>cues: average, integral, result, curve</sub>

So every frequency comes with a precise Gaussian target. At t equals one point
six, for example, that target is about point two eight.

<sub>cues: example, value</sub>

The batch gives us a second point at the same t. Their separation is what we
add up next.

<sub>cues: next</sub>

---

## b11_fingerprint_to_loss

*Chapter B.11 — turn the Gaussian fingerprint into one scalar score.*

> **ON SCREEN** — \mathcal T\in\mathbb R

At t equals one point six, the batch and the Gaussian each give one point in
the complex plane.

Their distance tells us how much the two fingerprints disagree at this
frequency.

That distance uses both coordinates: the horizontal mismatch from the target,
and any vertical component in the empirical batch. Squaring it gives a
nonnegative quantity that still changes smoothly as the points move.

> **ON SCREEN** — squared gap

> **ON SCREEN** — two-clump batch

Each t now gives one nonnegative contribution. Let t vary, and those
contributions line up as a curve of squared disagreement.

<sub>cues: range</sub>

Now watch the gap. Wherever the fingerprints separate, the curve rises; where
they agree, it settles back toward zero.

To compress this curve into one number, we still need to decide how strongly
each frequency should count.

> **ON SCREEN** — frequency influence

> **ON SCREEN** — \mathcal T=

The taper from the previous scene becomes a Gaussian weight. Its value tells
us how much influence a frequency receives: strongest near zero, then fading
smoothly into the tail. Lambda controls the width of that taper.

<sub>cues: weight, lambda</sub>

At any t, the yellow curve sets the influence, and the red curve supplies the
squared disagreement. Multiplying them gives the weighted contribution from
that frequency.

<sub>cues: weight_part, gap_part, product</sub>

Now add those weighted contributions across every t. The integration sign
performs that continuous sum. Inside it are the weight and the squared gap we
just built. Multiplying by N adjusts the statistic for the batch size.

<sub>cues: integral, pieces, scale</sub>

> **ON SCREEN** — Epps–Pulley statistic

Put those pieces together, and this weighted total is the Epps–Pulley
statistic.

> **ON SCREEN** — \mathcal T_{\mathrm{pop}}=0

Now bring back the two original batches. If we compare each fingerprint with
the standard Gaussian, the two clumps give a large value, while the bell-
shaped batch lands close to zero.

<sub>cues: compare</sub>

> **ON SCREEN** — sampling variation

Fresh Gaussian batches land at slightly different positive values. A result
near zero means the batch fingerprint follows the Gaussian target about as
closely as ordinary sampling variation allows.

<sub>cues: draws, values, near_zero, variation</sub>

At the population level, zero has an exact meaning. If the score is zero, then
the characteristic function matches the Gaussian at every t. The uniqueness
theorem then forces the distribution itself to be standard Gaussian.

<sub>cues: theorem, distribution</sub>

At the start, these two batches made the missing shape information obvious.
Fixing the standard Gaussian as the reference turns that visual difference
into a repeatable score: every batch is judged against the same target.

<sub>cues: reference</sub>

The whole construction now fits in one line. Start with the samples, build
their empirical fingerprint, compare it with the Gaussian fingerprint at every
frequency, and combine the weighted discrepancies into one smooth number.

<sub>cues: fingerprint, compare, score</sub>

In the next chapter, we'll discuss how to do the same thing with a whole batch
of vectors.

<sub>cues: vectors</sub>

---
