# Chapter B Part 1 — script revision record

Covers the pre-renumbering Part 1 revision that became `b00`–`b07`.
Part 2 (`b08`–`b11`) is out of scope.

Written against [`NARRATION_SPEC.md`](../../NARRATION_SPEC.md) §§1–30, audited under
§31 A–J, revised in §33 order. The external review's six-step process is followed;
its mandatory corrections 1–4 all land in this part and are treated as blockers.

**Baseline:** 1,511 spoken words, 7:55, seven scenes.

---

## Step 1 — Scene audit

### Summary

| Scene | Unique transition it creates | Verdict |
|---|---|---|
| `b00` | none → *simple statistics do not determine shape* | **REBUILD** |
| `b02` | complex arithmetic → *arrows, and their average measures agreement* | keep, compress |
| `b03` | angles are arbitrary → *a sample becomes an angle via `t·x`; sweeping `t` gives a curve* | keep, fix maths |
| `b03` real/imag beats | the curve is one number → *the average arrow has two coordinates, and both matter* | keep, compress |
| `b05` | the rig is abstract → *three batches whose curves can be predicted* | **SPLIT** |
| `b06` | curves start anywhere → *every curve starts at 1, so heights are comparable* | compress |
| `b07` | one frequency might do → *any single frequency has a counterexample* | keep, fix maths |

### Per scene

#### `b00_the_problem` — REBUILD

- **Teaching goal (stated):** a score must be one differentiable number.
- **Teaching goal (actual, wrong):** detect whether every sample is identical.
- **Learner before:** knows mean and variance.
- **Learner after (intended):** wants a description of the whole distribution.
- **Claim:** two batches can agree on mean and variance and differ in shape. `facts.py`
  verifies the batches agree to 5e-3.
- **Proof status:** empirical demonstration on two specific batches. Correct as stated.
- **Mathematical issue — the reason for the rebuild.** The scene opens on a collapsed
  batch against a spread one, and asks for a score separating them. **Variance already
  separates those two.** The chapter's actual problem — comparing whole distributional
  shape — only appears 40 seconds in, as a second beat. The opening therefore motivates
  a problem the chapter does not solve, and the real problem arrives as an afterthought.
- **Redundant narration:** *"Separating those by eye takes no effort."* — restates the
  animation. *"Mean and variance are the two summaries anyone reaches for first."* —
  true and inert.
- **Redundant on-screen text:** `"Same mean. Same variance. Different shapes."` (rule of
  three, and the narration says the same thing in the same breath — F10 channel
  redundancy at the chapter's first frame, closed in rev 2 and reopened by this caption).
  `"mean, variance fixed ⇒ shape still free"` restates it a third time.
- **Pacing:** the final 13 s hold one static frame (open finding O3). The scene's whole
  second half is a frozen tableau.

#### `b02_arrows` — keep, compress

- **Teaching goal:** `e^{iθ}` is a unit arrow at angle θ; averaging arrows measures
  angular agreement.
- **Learner before:** complex numbers assumed (`concepts.yaml` marks this ASSUME).
- **Learner after:** can predict that spread arrows average short.
- **Claim:** six evenly spaced unit arrows average to zero. `facts.py` verifies |z| < 1e-15.
- **Proof status:** exact, and verified.
- **Redundant narration:** *"The complex plane, for one minute, because everything after
  this is built on it."* — lesson-plan narration, `NARRATION_SPEC.md` §2. *"Nothing in
  this chapter needs the power series or any identity beyond that"* — tells the viewer
  what they will not need, which is not information. *"Every curve later in this chapter
  turns out to be one of those two components, averaged over a batch of samples."* —
  promises later relevance, §1.
- **Redundant on-screen text:** `"arrows that agree → a long average"` / `"arrows that
  spread → they cancel"` — a matched slogan pair, and both restate what the animation
  shows *and* what the narration says: three channels, one fact.
  `"The length of the average arrow / measures how much the angles agree."` — the
  narration's next sentence, verbatim.
- **Repeated idea:** the cancellation argument is made here, then re-derived in `b05` for
  the ±1 case. `b05` should back-reference.
- **Pacing:** 1:30, the longest scene in Part 1, and §12 of the spec says assumed
  prerequisites should not be re-taught. The Euler's-identity beat is prerequisite
  restoration and can be halved.

#### `b03_the_rig` — keep, **mathematical correction 1**

- **Teaching goal:** the translation rule — sample → angle `t·x` → arrow → average →
  the average's horizontal position *is* the curve's height.
- **Learner after:** can predict what panel 3 does before it does it.
- **Claim:** the roll lands exactly on `e^{itx}`. `facts.py` verifies to 1e-12.
- **Proof status:** exact.
- **Mathematical issue — BLOCKER (correction 1).** *"On the circle, samples further from
  zero accumulate angle faster, so the arrows separate, and the average pulls in toward
  the centre."* stated over a sweep, with no locality. Characteristic functions oscillate
  and arrows realign; `|φ|` is not monotone in `t`. As phrased, the sentence generalises a
  local observation into a false global one, and the animation — one clean sweep — is
  exactly the "universal-looking parameter sweep" `RENDER_REVIEW_SPEC.md` §6.4 names as
  falsely implying a theorem.
- **Redundant on-screen text:** `"one point of this curve, per frequency"` — the narration
  says "One frequency produced one point" four seconds earlier.
- **Structural:** the scene hand-duplicates `ThreePanelRig` (four blocks). This is how F15
  happened: a shared fix reached three scenes and left this one behind.
- **Pacing:** 1:01 for the chapter's single most important translation rule. Under-timed.
  This is the scene that most needs inspection silence.

#### `b05_real_and_imaginary` — keep, compress

- **Teaching goal:** the average arrow has two coordinates; discarding one loses
  information. Symmetric batch ⟹ `Im φ = 0`.
- **Claim:** symmetric batch has `max|Im φ| < 1e-14`, and the skewed batch does not.
  `facts.py` verifies both directions.
- **Proof status:** the pairing argument is a genuine proof, and is delivered as one.
- **Redundant narration:** *"Two components need two curves, so both get one, and the
  frequency sweeps again."* — narrates the animation. *"Which is all the formula says"* —
  filler.
- **Redundant on-screen text:** `"symmetric batch ⟹ Im φ = 0 everywhere"` immediately
  after `ty.line` has already set `X symmetric about 0 ⟹ Im φ(t) = 0`. The same statement
  twice, in two registers, one of them setting `⟹` and `φ` as Helvetica prose.
- **Pacing:** two of its beats are a bare `self.wait()` under narration — a frozen frame
  with voice over it.

#### `b05_worked_examples` — **SPLIT**

- **Teaching goal (three separate ones):** constant batch → `|φ|=1`; two-point → `φ = cos t`
  exactly; shift → phase only.
- **Claims:** all three verified in `facts.py` to 1e-12.
- **Proof status:** exact for all three.
- **Mathematical issue — BLOCKER (correction 2).** On-screen `location → phase` /
  `spread → magnitude` is too broad. Translation changes phase and leaves magnitude fixed
  — that is exact. But magnitude records **shape and scale**, not "spread". Within the
  Gaussian family variance controls the decay rate, and that narrower claim is what `b10`
  actually needs.
- **Redundant narration:** *"One more case, and it separates two things that have been
  travelling together."* — announces structure (§2). *"The cosine arrived without an
  integral being evaluated."* — evaluative framing. The ±1 mirror-cancellation is
  re-derived here having been proved in `b05`; back-reference instead.
- **Redundant on-screen text:** em dash in `"every value the same — plotting |φ(t)|"`; `φ`
  set as Helvetica; the `location →` / `spread →` slogan pair.
- **Pacing:** 1:32 carrying three independent examples, zero bookmarks, and twelve
  voiceover blocks. Highest density in Part 1. **Split: the degenerate + two-point cases
  are one scene (predicting curves), the shift is another (what magnitude ignores).**

#### `b07_one_speed_fails` — keep, **mathematical correction 3**

- **Teaching goal:** any single frequency admits a batch that fakes total agreement.
- **Claim:** `aliased_1d(3.0, k=3)` has `|φ(3)| = 1` with sd > 4. Verified.
- **Proof status:** an explicit counterexample — the strongest proof status in Part 1.
- **Mathematical issue — BLOCKER (correction 3).** *"so a score built on one frequency can
  be defeated by construction, and the sweep is what removes that option"* implies the
  sweep removes the problem. It removes *this* coincidence. A finite set of frequencies
  can still fail to separate some pairs of distributions; only the full characteristic
  function carries the uniqueness guarantee. This distinction has to survive into Part 2,
  where the practical method samples finitely many knots.
- **Redundant on-screen text:** `"Why sweep t at all? Why not just pick a good one?"` — a
  rhetorical question pair the narration then asks again. Em dash and straight quotes in
  `"every arrow lands on the same spot — at this one speed, the test says \"collapsed\""`.
  `"nudge the speed, and the illusion breaks"` — aphorism.
- **Keep the counterexample itself intact.** It is the best beat in Part 1.

#### `b06_the_anchor` — compress

- **Teaching goal:** `φ(0) = 1` for every distribution, so curves share a reference point.
- **Claim:** verified for gaussian, bimodal and constant batches to 1e-15.
- **Proof status:** exact, and the argument is delivered (the data never enters it).
- **Mathematical issue — BLOCKER (correction 4).** *"No normalisation has to be established
  first, which is what lets two curves from different batches be compared at all."*
  overclaims. A shared anchor is useful; it is not what makes comparison possible.
- **Redundant on-screen text:** `"Three different distributions."` + `"φ(0) = 1, for every
  distribution"` — a slogan pair, the second setting `φ` as Helvetica prose, and both
  restating the narration.
- **Pacing:** 1:03 for `φ(0) = E[1] = 1`. Three of its beats are bare waits. The idea is
  short; the universality point is the part worth keeping. **Target 40–45 s.**

---

## Step 2 — Redundancy audit

Sentences that exist because narration was expected at that moment. Classified per the
review's scheme. **Aggressive by instruction.**

| # | Scene | Passage | Class | Note |
|---|---|---|---|---|
| 1 | b00 | "Separating those by eye takes no effort." | **delete** | The animation is the argument. |
| 2 | b00 | "Mean and variance are the two summaries anyone reaches for first." | **merge** | Fold into the moment-ladder sentence. |
| 3 | b00 | "These two batches agree on both, to three decimal places." | **keep** | Load-bearing: it is the whole discrepancy. |
| 4 | b02 | "The complex plane, for one minute, because everything after this is built on it." | **delete** | Lesson-plan narration, §2. |
| 5 | b02 | "Nothing in this chapter needs the power series or any identity beyond that…" | **delete** | Negative information. |
| 6 | b02 | "Every curve later in this chapter turns out to be one of those two components…" | **delete** | Promises later relevance, §1. |
| 7 | b02 | "Arrows add tip to tail, so a set of them has an average: the sum, divided by how many there are." | **keep** | Defines the operation the chapter runs on. |
| 8 | b02 | "The angles have been arbitrary so far. The next step is to get them from data." | **keep** | Creates the need for `b03`. §19. |
| 9 | b03 | "Wrapping the line around the circle is that multiplication, drawn." | **keep** | The translation rule itself. |
| 10 | b03 | "That average is one complex number, for this one frequency." | **merge** | Combine with the plotting sentence. |
| 11 | b03 | "What is not yet clear is how much about the batch that curve still remembers." | **keep** | Sets up `b08`. |
| 12 | b05 | "Two components need two curves, so both get one, and the frequency sweeps again." | **leave to animation** | Pure description. |
| 13 | b05 | "Which is all the formula says: average the cosines…" | **replace** | State the correspondence, not its adequacy. |
| 14 | b05 | "The sweep agrees: the red curve sits at zero across the whole range, not merely close to it." | **keep** | Observation *and* qualification. |
| 15 | b05 | "The degenerate case first: every value in the batch is the same number." | **replace** | Fragment opener; state the batch. |
| 16 | b05 | "One more case, and it separates two things that have been travelling together." | **delete** | Announces structure. |
| 17 | b05 | "Their vertical components cancel exactly, by the pairing argument from a moment ago" | **merge** | Back-reference `b05`; do not re-derive. |
| 18 | b05 | "Two arrows turning, and their average. The cosine arrived without an integral being evaluated." | **delete** | Evaluative framing, §5. |
| 19 | b05 | "A faint copy of that amber curve stays on screen as a reference." | **leave to animation** | Narrates a visual affordance. |
| 20 | b07 | "Sweeping every frequency is expensive. If one well-chosen value of t did the job, the sweep would be waste." | **keep** | Genuine motivation. |
| 21 | b07 | "By any reasonable reading it has not collapsed." | **keep** | The contradiction the scene runs on. |
| 22 | b06 | "Every graph from here on starts at exactly the same height." | **replace** | Promise; state `φ(0)=1` and show it. |
| 23 | b06 | "The data never entered that argument, which is what makes the result hold for every distribution rather than for this batch." | **keep** | The universality point — the best sentence in the scene. |
| 24 | b06 | "Three batches with nothing in common: a spread-out one, two separate clumps, and one constant value repeated." | **compress** | Rule of three; the visual names them. |

**On-screen text — delete or convert (13 captions):**

| Scene:line | Caption | Action |
|---|---|---|
| b00:136 | `Same mean. Same variance. Different shapes.` | delete — narration says it |
| b00:137 | `mean, variance fixed ⇒ shape still free` | convert to the stat block itself |
| b02:265 | `arrows that agree → a long average` | delete |
| b02:285 | `arrows that spread → they cancel` | delete — keep the live length readout instead |
| b02:305–306 | `The length of the average arrow / measures how much the angles agree.` | delete |
| b03:248 | `one point of this curve, per frequency` | delete |
| b05:198 | `symmetric batch ⟹ Im φ = 0 everywhere` | delete — `ty.line` already sets it correctly |
| b05:82 | `every value the same — plotting \|φ(t)\|` | **em dash** — rebuild as a label + `ty.maths` |
| b05:200 | `location → phase` | replace with the exact identity (correction 2) |
| b05:202 | `spread → magnitude` | replace (correction 2) |
| b07:44 | `Why sweep t at all? Why not just pick a good one?` | delete |
| b07:99 | `every arrow lands on the same spot — at this one speed…"collapsed"` | **em dash** — split into a label and a readout |
| b07:118 | `nudge the speed, and the illusion breaks` | delete |
| b06:171–172 | `Three different distributions.` / `φ(0) = 1, for every distribution` | replace with `ty.maths(R"\varphi(0) = 1")` |

**Unicode maths set as prose (6 sites):** `→` at b02:265, b02:285, b05:200, b05:202;
`⟹` at b05:198; `θ` at b02:145; `φ` at b05:198, b05:82, b06:172. All are deleted or moved
into `ty.maths` / `ty.line` by the above.

---

## Step 3 — Mathematical corrections

All four are blockers under `RENDER_REVIEW_SPEC.md` §6.4. Applied in Step 5.

| # | Scene | Before | After |
|---|---|---|---|
| 1 | b03 | "samples further from zero accumulate angle faster, so the arrows separate, and the average pulls in toward the centre" | Scoped to the visible sweep: *over this range* the arrows separate and the average moves inward. No implication that `\|φ\|` decreases in `t` generally. |
| 2 | b05 | `location → phase`, `spread → magnitude` | Translation changes the phase and leaves the magnitude unchanged; the magnitude therefore records shape and scale independently of location. Variance-controls-decay is deferred to `b10`, inside the Gaussian family where it is true. |
| 3 | b07 | "a score built on one frequency can be defeated by construction, and the sweep is what removes that option" | Several frequencies break *this* coincidence. The uniqueness guarantee belongs to the full characteristic function across all frequencies — flagged now because Part 2's method samples finitely many. |
| 4 | b06 | "No normalisation has to be established first, which is what lets two curves from different batches be compared at all." | Every characteristic function is pre-normalised at the origin, which gives all curves a common reference point. Useful; not the sole reason comparison is possible. |

**Nothing here is invented.** Each correction weakens a claim to what the source and
`facts.py` support. No claim in Part 1 is unverifiable from the existing ledger — the
19 claims in `facts.py` cover every number spoken in these seven scenes.

---

## Step 4 — Structure

| Scene | Was | Becomes | Runtime |
|---|---|---|---|
| `b00_the_problem` | 0:45 | **rebuilt** — same-mean/same-variance opening, moment ladder, two constraints | ~1:15 |
| `b02_arrows` | 1:30 | compressed; prerequisite restoration halved | ~1:10 |
| `b03_the_rig` | 1:01 | correction 1; onto `ThreePanelRig`; inspection silence added | ~1:25 |
| `b05_real_and_imaginary` | 1:23 | compressed | ~1:15 |
| `b05_worked_examples` | 1:32 | **split** → `b05` (constant + two-point) | ~1:05 |
| `b06b_what_magnitude_ignores` | — | **new** — the shift example, correction 2 | ~0:55 |
| `b07_one_speed_fails` | 0:41 | correction 3 | ~0:50 |
| `b06_the_anchor` | 1:03 | compressed hard; universality kept | ~0:45 |

Eight scenes, estimated **~8:40**, inside the agreed 9–10 min with room for the pauses to
land longer than estimated.

**Playback order is not filename order.** The two worked-example scenes belong together,
so Part 1 plays `b05` → `b06b` → `b07`, and a glob sorts `b07` before `b06b`. The part
map in `build.sh` therefore names the eight scenes explicitly, and errors if a named
scene does not resolve to exactly one file — a silently dropped scene would still produce
a master, just one missing a minute of the argument.

---

## Step 5 — What the rewrite actually did

The narration itself lives in the scene files; this records the shape of the change.

### Measured

| | Before | After |
|---|---|---|
| Spoken words, Part 1 | 1,511 (7 scenes) | 1,557 (8 scenes) |
| On-screen multi-word captions | 21 across Part 1 | **8** |
| Slogan-shaped captions | 13 | **0** |
| Em dashes on screen | 2 | **0** |
| Unicode maths set as prose | 6 sites | **0** |
| `facts.py` claims | 19 | **22** |
| Scenes closing on a slogan | — | 0/8 |

Word count went **up**, by 46. That is the trade `RENDER_REVIEW_SPEC.md` §6.4 requires:
corrections 1–4 all replace a confident wrong claim with a qualified right one, and
qualification costs words. The redundancy audit's deletions paid for most of it.

### Corrections 1–4, as applied

1. **`b03`** — the old line said the arrows separate and "the average pulls in toward
   the centre", over a whole sweep. On this scene's own batch `|φ|` falls to 0.027 near
   t=4 and is back at 0.311 by t=6.5, so the sentence was contradicted by the animation
   running underneath it. Now scoped to the early stretch, with the recovery named:
   *"Keep going and the arrows carry on turning, fall part way back into step, and the
   average grows again."* The viewer can check this against the curve.
2. **`b06b`** — `location → phase` / `spread → magnitude` is gone. The identity stays
   because it is exact. What replaces the second half: the magnitude keeps shape *and*
   scale together, and separating them needs a family narrow enough that one number
   settles it. `b10` is where that is earned.
3. **`b07`** — no longer says the sweep "removes that option". Several frequencies
   break *this* coincidence, because no batch can be in step with all of them at once.
   Whether finitely many suffice for any two distributions is named as the stronger
   question it is, and left with the whole curve. This is the distinction Part 2's
   finitely-many-knots method depends on.
4. **`b06`** — a shared anchor is no longer "what lets two curves be compared at all".
   Every characteristic function is already normalised at the origin, so no curve has to
   be rescaled before it is read. Useful; not the reason comparison is possible.

### Beyond the audit

Six defects surfaced during the rewrite that the Step 1–2 audit had not caught:

- `b02` said "six arrows" over five, and the two bundles held different counts, so
  there was no "same six" to transform between.
- `b02` drew arrows as headless `Line`s in two places the narration calls them arrows
  (VISUAL_SYSTEM.md §5).
- `rig.readout()` set type by hand at `font_size=30` — below the floor, and it never
  moved when the scale was re-anchored for Latin Modern.
- `b00`'s dot stack needed binning *before* `stack_levels()`, not just at draw time;
  snapping only the drawn x left 3 of 9 columns floating clear of the axis.
- Playback order is not filename order — see §Step 4.
- Three spoken numbers had no ledger entry (`b07`'s range, its off-resonance
  magnitudes, `b06b`'s dip). Added to `facts.py`; the `b05` shift claim was retagged to
  `b06b` and the `b05` claim's spoken quote refreshed to match the revised line.

## Step 6 — Self-audit

`narration_audit.py` over the eight Part 1 scenes: **every budgeted check within
limits**. Teaching-process 0.0/1k, importance 0.0, false-surprise 0.0, bare-attention
0.0, appositive 0.0, evaluative 0.0, "here is" 0.0, contrast 3.2 against a budget of
4.0. Longest choppy run is 3 sentences (`b00`); no scene closes on a slogan.

**One metaphor**, as the process requires: *arrow*, 28 uses across 7 scenes. Nothing
else on the inventory registers.

### Humaniser

Run last, over the prose only, all 25 rules. Four changes, and one flagged conflict:

- **Rule 9** (negative parallelism) fired twice, and both were load-bearing.
  `b03`'s *"The curve on the right is not a decay"* became *"records where that average
  keeps landing, and it rises and falls as the arrows drift in and out of step"* — the
  denial was the correction, and stating the mechanism directly is both cleaner and more
  informative. `b05`'s *"at zero, not merely close to it"* became *"at exactly zero"*,
  which keeps the exactness that made the qualification load-bearing.
  **Neither is a genuine conflict once rewritten** — but the audit's row 14 marks the
  `b05` line KEEP for its qualification, so the qualification survives in the word
  *exactly* rather than in the construction.
- **Rule 25** (hyphenated pairs): `well-chosen` → `well chosen`, `part-way` → `part way`.
  `non-degenerate` kept — rule 25 exempts technical compound modifiers, and it is one.
- **Rule 22** (filler): `b06b`'s *"Sweep the frequency once to fix both curves in mind"*
  told the viewer what to do with their memory and said nothing about the picture. It
  now states what the picture does, and that statement is in the ledger.

Rules 1–8, 10–21, 23, 24 found nothing. Zero em dashes and zero curly quotes in the
narration, checked mechanically rather than by eye.

### What the render then found that no gate could

Full findings in [`RENDER_REVIEW.md`](RENDER_REVIEW.md) §"Rev 3". The one worth
repeating here, because it bears on how this document should be used:

**`b00` held 4.5 seconds of completely empty screen with narration playing over it**,
at the seam between the moment ladder and the two constraints. Every gate passed. The
narration audit cannot see it — the prose is fine. `preflight` cannot see it —
the names resolve. `facts.py` cannot see it — no number is wrong.

It was found by computing mean frame luminance at 2 fps and looking for runs at the
background value, not by watching. That check took one command and caught something
seven passes of human attention might have registered only as "this drags a bit":

```bash
ffmpeg -v error -i SCENE.mp4 -vf "fps=2,signalstats,metadata=print:file=-" -f null - 2>&1
```

The empty-frame value on this project's background is `YAVG = 28.0`. Anything sitting
there for more than a second is dead air, and dead air was the whole reason for this
rebuild. Worth adding to the gate suite as a real check rather than leaving it as a
thing someone remembered to run once.

The fix also closed a second defect nobody had noticed: the next sentence opens *"Two
things constrain what such a description can be"*, and "such a description" had no
visible referent (`NARRATION_SPEC.md` §26). The object that replaces the ladder now
stays on screen and becomes the heading the constraints sit under.

**And the first attempt at that fix was itself caught by a gate.** It put the words
*"a description of the whole distribution"* on screen — which is precisely what the
narration says at that moment. The on-screen slogan scan, made to gate at the top of
this session, failed the build. It was right. The object now reads

    samples ⟶ ? ⟶ one differentiable score

which names the two ends already fixed and marks the middle as the unknown, so it
carries something the voice does not. Both constraints are then visibly constraints
on that middle box, and the scene closes by resolving the `?` rather than fading in a
second pipeline underneath the first.

That sequence is the argument for gating rather than reporting: a check that only
prints is a check you read past, and this one caught a regression introduced in the
course of fixing something else, four hours after it was made to gate.

### And what measurement could not find

`b02` closed on **fourteen seconds of a completely static frame** — six motionless
arrows and a fixed `length = 0.00` — while the narration made a claim about a whole
range: *"one when they coincide, zero when they are spread evenly, and something in
between otherwise."* The in-between case was never shown anywhere in the chapter.

No gate can see this. There is content on screen, so `dead_air.py` passes it; the
prose is good, so the narration audit passes it; the numbers are right, so `facts.py`
passes it. It was found by watching, which is what `RENDER_REVIEW_SPEC.md` §20–21
exist to require.

The six arrows now sweep continuously between coincident and evenly spread with the
length tracking live: 1.00, then 0.52, then 0.00. The sentence and the picture make
the same claim, and the middle of the range is finally visible.

**The two halves of the review are not substitutes.** Measurement found a blank frame
that no one would have described precisely; watching found a frozen frame that no
measurement in this repo can detect. Running only one of them would have shipped the
other defect.
