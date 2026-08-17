# Explanation Compiler — the process for building explainers in this repo

This is the working method for turning a technical source into a visual,
mathematically careful video explanation. It governs `projects/*/` — the current
SIGReg explainer and every future one.

It sits **above** the rendering guide and **below** two binding specifications
supplied by the project owner. It does not replace any of them:

| Document | Scope |
|---|---|
| [`NARRATION_SPEC.md`](NARRATION_SPEC.md) | **binding.** How the spoken script is written and audited. Governs deliverables 7 and 9. |
| [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) | **binding.** How a rendered MP4 is reviewed before it counts as finished. Governs deliverable 10. |
| **this file** | what to build, in what order, and how it is judged |
| [`MANIM_GUIDE.md`](MANIM_GUIDE.md) | how to render it — environment, Manim CE API, gotchas, voiceover |
| [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) | the typographic and colour rules every scene obeys |
| `projects/<name>/PLAN.md` | the per-project instance of the artifacts below |
| `projects/<name>/RENDER_REVIEW.md` | the written per-scene review required by `RENDER_REVIEW_SPEC.md` |

Precedence, highest first:

1. `NARRATION_SPEC.md` on anything to do with the script.
2. `RENDER_REVIEW_SPEC.md` on anything to do with judging a finished render.
3. `MANIM_GUIDE.md` on *rendering* mechanics.
4. This file on *pedagogy or process*.

§6 (narration rules) and §8 (verification) below are **summaries** of the two
binding specs, kept here so the process reads end-to-end. Where a summary and
its spec disagree, the spec wins and the summary is the bug. Read the spec
itself before drafting or reviewing — the summaries are for mid-task recall,
and Chapter B rev 1 is the demonstration that working from them alone is not
enough.

---

## 0. The one-line summary

**The explanation must behave like a visual argument.** The visual
construction, the mathematical reasoning, and the narration describe the same
structure. A formula arises from a visible operation; it is never stated
alongside an analogy that is then claimed to explain it.

The failure mode this exists to prevent:

1. give an analogy
2. state an unrelated formula
3. assert the analogy explains the formula

If complex numbers are drawn as arrows, then adding complex numbers must
literally be adding those arrows on screen. The picture carries the reasoning;
it does not decorate it.

---

## 1. Who does what

**The user is a learner.** They supply a source — paper, PDF, link, blog post,
chapter, notes, an equation, or an existing script to improve. They may not yet
understand it well enough to plan the explanation.

Discovering prerequisites, central concepts, hidden assumptions, proof
structure, and explanation order is **my** job, from the source.

### Never ask the user

- Which concepts should be assumed?
- Which theorem should be central?
- What prerequisite depth?
- What is the concept graph? Which lemmas are required?
- Which representation should be used?

### Do ask the user (plain English, one at a time)

- Who is this for?
- What should the viewer understand afterward?
- How long?
- The whole paper, or one idea from it?
- Intuition, derivation, practical use, or all three?
- Standalone, or part of a sequence?
- Full proofs, sketched, or deferred?
- Is there a specific result you want it to reach?

Prefer *"Has the viewer seen Fourier transforms before, even if they still feel
unintuitive?"* over *"Should Fourier transforms be ASSUME or REFRESH?"*

**Do not quiz the user on the technical material.** The video is what creates
their understanding — requiring them to understand it first inverts the whole
point. When a decision genuinely turns on the mathematics, explain the tradeoff
in ordinary language and **recommend one option** rather than presenting a menu.

---

## 2. The ten deliverables

Produced **in order**, with review gates. Do not generate them all at once
unless explicitly asked. Do not jump from a source to polished narration.

| # | Deliverable | Artifact in the repo |
|---|---|---|
| 1 | Source map | `projects/<name>/SOURCE_MAP.md` |
| 2 | Interview + audience contract | `PLAN.md` § audience contract |
| 3 | Learner-journey model | `PLAN.md` § learner journey |
| 4 | Concept graph | `projects/<name>/concepts.yaml` |
| 5 | Explanation path | `PLAN.md` § explanation path |
| 6 | Scene graph | `PLAN.md` § scene graph |
| 7 | Draft narration — **written to [`NARRATION_SPEC.md`](NARRATION_SPEC.md) §§1–30** | prose first, in the scene files |
| 8 | Diagnostic report + scorecard — **[`NARRATION_SPEC.md`](NARRATION_SPEC.md) §31 audit A–J, §32 scoring** | `tools/narration_audit.py` + written audit |
| 9 | Revised narration — **[`NARRATION_SPEC.md`](NARRATION_SPEC.md) §33 revision order** | targeted edits, diagnostics rerun |
| 10 | Production package — **reviewed under [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md)** | rendered scenes, master, subtitles, `projects/<name>/RENDER_REVIEW.md` |

### Deliverable 1 — Source map

Answer, concisely enough that the user does not need to understand the whole
subject to approve a direction:

1. What problem is being solved?
2. What is the central idea?
3. Why is it difficult?
4. What background is necessary?
5. Which part makes the strongest visual explanation?
6. Which claims need particular care?
7. What should be omitted?

Preserve section, theorem, equation, and page numbers where the source has them.

**Attribution discipline.** Always separate: what the source explicitly claims /
what follows mathematically / my interpretation / a pedagogical simplification /
what remains uncertain. Never invent a motivation or implication and attribute
it to the source.

### Deliverable 2 — Audience contract

Every prerequisite gets exactly one label:

- **ASSUME** — usable comfortably. Do not reteach. A contextual reminder is
  allowed only if the concept is being used unusually.
- **REFRESH** — encountered before; restore the mental picture briefly and
  operationally. This must not swell into a foundational lesson.
- **TEACH** — developed inside the video.
- **DEFER** — unnecessary here. Mention only to mark a limitation or a later video.

Show it back in ordinary language, e.g. *"I'll assume vectors, averages, and
basic probability; briefly restore the picture of a complex exponential as a
rotating unit arrow; teach characteristic functions themselves; and cite but not
prove Fourier uniqueness."* The contract describes what the **video** does, not
what the user must already know.

### Deliverable 3 — Learner-journey model

For each important idea, state:

1. what the viewer believes beforehand
2. what question or difficulty arises
3. what visual construction addresses it
4. what the viewer observes
5. what mathematical claim follows
6. why it follows
7. what they understand afterward
8. what misconception the scene must avoid
9. proof status (see §3)

### Deliverable 4 — Concept graph

**One** typed graph — not separate prerequisite, motivation, and visual graphs.
Those are filtered views of the same thing. Machine-readable so views can be
generated rather than hand-maintained (`concepts.yaml`; see §5).

Node kinds: concept, claim, equation, visual model, example, misconception,
application.

Edge types: `requires`, `motivates`, `visualizes`, `formalizes`, `justifies`,
`generalizes`, `approximates`, `contrasts_with`, `fails_when`, `used_by`,
`proved_using`.

Also mark: central nodes, optional branches, conceptual bottlenecks, **places
where an animation could create a false inference**, and nodes needed for source
fidelity but not central to the video.

### Deliverable 5 — Explanation path

The graph holds more than the video should use. Choose the **shortest coherent
path** to the learning goal. Each step carries: the question the learner is
ready to ask, the construction, the observation, the claim, why it follows, the
proof status, learner state before and after, the misconception in play, and any
deferred proof.

**No manufactured curiosity.** A question must arise from something the viewer
has actually seen and cannot yet explain. Banned unless genuinely earned:
*"But what if there were another way?"*

### Deliverable 6 — Scene graph

Per scene: pedagogical purpose, the reasoning step it serves, opening state,
sequence of visual changes, focal point at each moment, **what changes and what
stays invariant**, representations on screen, explicit translation rules between
them, equation reveal timing, likely false inferences, learner state before and
after, duration, narration intent and constraints.

When multiple representations share the screen, write the correspondence out:

```
sample x on number line
  → angle t·x
    → arrow e^{itx}
      → average arrow
        → characteristic-function value at t
```

Never put three panels up and say only *"watch all three panels"*. Name the
relationship the viewer is meant to follow. Every animation needs a mathematical
or attentional purpose; no decorative motion.

### Deliverable 7 — Draft narration

**Governed by [`NARRATION_SPEC.md`](NARRATION_SPEC.md). Read it before writing a
line of script — not after, when only phrase-swapping is left.** Its §30 gives
the per-scene drafting procedure: objective → necessary claims → what the
animation already says → *only what narration must add* → the link to the next
scene → read aloud.

Write **full spoken passages**, not subtitle fragments
([`NARRATION_SPEC.md`](NARRATION_SPEC.md) §23). Segmentation happens later, from
the render.

### Deliverables 8–9 — Diagnose, then revise in priority order

Run `tools/narration_audit.py` (mechanises
[`NARRATION_SPEC.md`](NARRATION_SPEC.md) §31 A–E and H), write out §31 F, G, I,
J by hand, score against §32, and add the written mathematical and pedagogical
audits (§4 below). Then revise — **do not blanket-rewrite** — in this order:

1. mathematical errors
2. false proof implications
3. missing prerequisites or prerequisite overreach
4. broken visual-symbolic mappings
5. missing learner-state transitions
6. motivation and pacing
7. repetitive or artificial narration
8. stylistic preference

Rerun diagnostics, re-score, list unresolved limitations, and confirm no new
unsupported claim was introduced.

---

## 3. Proof-status discipline

Every central claim carries exactly one label, recorded in `concepts.yaml`:

`exact_derivation` · `full_proof` · `proof_sketch` · `theorem_statement` ·
`intuition_only` · `analogy` · `empirical_observation`

**A persuasive animation must never silently impersonate a proof.**

The words *therefore, must, proves, shows, guarantees, hence, implies, cannot*
assert a proof status. `narration_audit.py` lists every occurrence; each one is
checked by hand against the claim's label. A `theorem_statement` narrated with
"therefore" is a blocking defect, not a style note.

Intuition and proof are not separate modes — build the intuition out of the same
relationships that carry the argument.

---

## 4. Mathematical and pedagogical diagnostics

Run these **separately** from the language audit. They are judgement work; no
script substitutes for them.

- **Source fidelity** — every significant claim checked against the source or an
  established result. Hunt for: unsupported claims, overstatements, missing
  conditions, wrong generalizations, source claims presented as my deduction,
  my interpretation presented as the source's.
- **Representation completeness** — does the visual preserve everything later
  claims need? *If only `Re φ` is plotted, do not later claim the displayed
  curve determines the distribution.*
- **Parameter-sweep validity** — is the narrated behavior monotonic, oscillatory,
  asymptotic, conditional, or merely typical? Do not say "it shrinks toward
  zero" if realignment can occur.
- **Prerequisite discipline** — ASSUME not retaught, REFRESH stays short, TEACH
  actually developed, no undeclared prerequisite sneaking in.
- **Learner-state progression** — every scene must change something. Flag scenes
  that add terminology without understanding, restate an existing model, move
  without a new inference, introduce several central concepts at once, or recap
  without compressing.
- **Motivation** — unusual constructions must solve a problem the learner already
  feels. Do not manufacture motivation for routine steps, especially for expert
  audiences.
- **Visual-symbolic correspondence** — per equation: what each symbol refers to
  visually, which visible operation matches each algebraic one, when it appears,
  and **what part of it has no visual counterpart**.
- **Edge cases** — chosen for the actual topic, not applied mechanically. Zero,
  negative, symmetric, degenerate, parameter limits, repeated values, and any
  case where the visible trend reverses.

---

## 5. Repo artifacts this process requires

### `projects/<name>/concepts.yaml` — the typed graph

```yaml
nodes:
  ecf:
    kind: concept
    label: empirical characteristic function
    status: TEACH
    central: true
  uniqueness:
    kind: claim
    label: "phi_X = phi_Y  =>  X and Y are equal in distribution"
    proof_status: theorem_statement     # cited, not proved
    scene: b08
edges:
  - [phase, visualizes, ecf]
  - [ecf, requires, complex_arrow]
  - [uniqueness, justifies, sigreg_proof]
false_inference_risks:
  - node: rig_panel3
    risk: "plots Re phi only; must not imply the curve determines the law"
```

Views (prerequisite chain, visual map, proof dependencies) are **generated** from
this, never maintained separately.

### `projects/<name>/facts.py` — the claims ledger, executable

PLAN.md §7 currently asserts verified numbers in a markdown table. Prose cannot
be rerun, so it silently rots as data or seeds change. Every numeric claim spoken
on screen becomes a function that recomputes it and asserts the value:

```python
def two_point_is_cosine():
    """phi(t) = cos t exactly for X = ±1.  Spoken in b05."""
    t = np.linspace(0, 6.5, 700)
    assert np.abs(ecf(np.array([-1.0, 1.0]), t) - np.cos(t)).max() < 1e-12
```

`python facts.py` re-verifies the whole video. This is the existing "verify
numerically before animating" norm, made durable.

### `tools/preflight.py` — undefined names, before a render is spent

Scene files use `from manimlib import *`, so pyflakes reports every mobject
class as possibly-undefined and the real findings drown. This resolves the star
import by importing the module and asking, so anything left unbound is genuine.

A `NameError` inside a beat method raises only when that beat executes. In
practice that meant twenty minutes into a chapter build, after four scenes'
text-to-speech had already been spent. `build.sh` runs this first and refuses
to render on a finding.

### `tools/dead_air.py` — empty frames, after the render

Every other tool here reads the source. This one reads the **output**, because
the defect it catches leaves no trace in the source: a scene can hold a
completely blank frame for four and a half seconds with narration playing over
it, and pass the claims ledger, preflight, and the language audit, because the
prose is fine, the names resolve, and no number is wrong. The only symptom is
that the video "drags".

It flags frames where peak luminance equals mean luminance. A blank frame is
uniform, so `YMAX − YAVG` is near zero; anything drawn separates the two, and
one thin grey axis is already a gap of 115. That criterion needs no per-project
calibration — no background colour, no resolution, no threshold to tune.

Two other criteria were tried first and both looked reasonable. Absolute mean
luminance fails because a whole number line plus samples plus a label moves the
mean of an 854×480 frame by 0.25, which is encoder noise. Peak against a
per-file minimum fails on any scene that never goes blank, because the floor is
then set by an ordinary frame. Both are recorded in the module so they are not
retried.

Reports empty frames only. Whether a frame that *has* content earns its time is
[`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §10.2 and stays a human pass —
an earlier "sparse frame" heuristic flagged frames carrying three full panels
and was deleted rather than shipped noisy.

`build.sh` runs it on the master and reports; it does not fail the build, since
a deliberate pause and dead air are the same measurement.

### `tools/script_dump.py` — the readable script, generated

A script kept as a separate hand-maintained document rots the moment a line is
edited in a scene, and then two versions disagree with no way to tell which is
real. This derives it from the same AST the audit reads, so the file always
says what the render says. Includes on-screen text as a second channel and
per-scene words-per-minute, and is the artifact to read when judging pacing or
redundancy across a whole chapter.

### `tools/renarrate.py` — narration edits by spoken text, not source layout

Narration is stored as implicitly-concatenated literals wrapped to 79 columns,
so the source form of a passage bears no relation to the sentence anyone hears.
Hand-editing means matching whitespace and continuation quotes, and a single
mismatched character silently leaves the old audio in place. This matches on
*normalised spoken text*, replaces by AST span, re-wraps, and keeps bookmarks
glued to the sentence that follows them so a re-wrap cannot desynchronise
speech from animation. It refuses to write anything unless every edit matches
exactly one passage.

### `tools/narration_audit.py` — the language audit, executable

Built and working. Extracts every `self.voiceover(text=...)` by walking the AST
(not the `.srt`, which only exists post-render and is Whisper-segmented into
subtitle fragments — the audit must run on spoken passages).

Checks: teaching-process phrases, contrast templates, unearned importance
language, manufactured surprise, bare attention commands, appositive filler,
evaluative framing, `"Here is"` openers, **slogan endings as a fraction of
scenes**, transition-word density, metaphor inventory, proof-verb inventory,
cadence runs, repeated sentence openers. Budgets are per 1,000 words and
deliberately non-zero — the spec says these constructions are *"not absolutely
forbidden, but repeated use is a major failure"*, so a zero budget would push
toward stilted avoidance.

Exit code 1 when over budget, so it can gate a build.

**A green audit is a floor, not a verdict.** Chapter B rev 1 passed every check
and still read as machine-written, because the four loudest patterns in it had
no budget describing their shape — nobody had thought to list them. The last
four checks above exist because a human read the script and found them. When
reading turns up a new tell, add a detector with a budget; the tool only ever
knows what has already been caught once.

---

## 6. Narration rules — summary of [`NARRATION_SPEC.md`](NARRATION_SPEC.md)

> **This section is a summary. [`NARRATION_SPEC.md`](NARRATION_SPEC.md) is the
> actual standard and wins on any conflict.** Read the spec itself before
> drafting; the reminders below are for mid-draft recall, not for planning.
>
> The four failures this summary historically let through, each now a named
> section in the spec:
>
> - **§18 — a polished slogan closing every scene.** One is a good line;
>   twelve is a template, and a template is the loudest tell in the document.
> - **§13 — one appositive shape reused as the default sentence.** *"One last
>   thing, and it is the thing the whole video runs on."* Say the thing.
> - **§5 — evaluative framing standing in for the observation.** *worth
>   remembering, worth banking, the most useful thing in this chapter.* If it
>   is worth remembering, the viewer decides that.
> - **§4 — `Here is/are…` as the default opener.** Open on the object.

Natural narration is an **engineering requirement**, not a final polish pass.
It should sound like a mathematically careful person thinking alongside the
viewer.

**Do not narrate the teaching process.** No *"let's begin by"*, *"now let's"*,
*"here's the key idea"*, *"the important thing to understand"*, *"at its core"*,
*"in other words"*. Open with the object, question, or situation instead.

> Weak: *We start with samples, not a formula.*
> Better: *Suppose these dots are measurements from an experiment.*

**Contrast templates.** *not X but Y*, *rather than X, do Y*, *this is not
merely X — it is Y*. Fine when the distinction genuinely matters; fatal as the
rhythm of a whole script.

**No procedural command chains.** "Take this. Move it here. Draw an arrow.
Average them. Plot the result." Commands may direct attention, but must be
embedded in reasoning — why the operation happens, and what to notice.

**Vary rhythm.** Not: short declarative, short declarative, imperative,
aphorism. Mix compact statements, connected explanatory sentences, occasional
questions, and a few deliberately longer sentences. **Do not end every paragraph
on a polished slogan.**

**No unearned importance.** *crucial, profound, beautiful, remarkable,
surprisingly, powerful, elegant, key insight.* Show why something matters.

**One central metaphor.** Do not call the same object a fingerprint, a lens, a
shadow, a probe, and a machine. Every metaphor's mapping must be explicit and
stable, and none may paper over a missing justification.

**No fake surprise.** *"You might be surprised"*, *"amazingly"*, *"believe it or
not"*. Let the mathematics do it.

**Transitions follow from reasoning**, not from the outline.

> Weak: *Now that we understand wrapping, let's move on to averaging.*
> Better: *Each sample has given us a direction. A single direction says little
> about the whole batch, so consider their average.*

**Delay names when it helps** — construct the object, explore it, establish its
use, then name it. But this is a tool, not a gimmick; expert audiences often
want the definition up front.

---

## 7. Scoring — 100 points

**Pedagogical and mathematical core — 80**

| | |
|---|---|
| Mathematical fidelity | 15 |
| Proof-status honesty | 10 |
| Audience and prerequisite fit | 10 |
| Mental-model progression | 15 |
| Visual-symbolic correspondence | 15 |
| Motivation and necessity | 10 |
| Transfer, comparison, edge cases | 5 |

**Narration — 20**

| | |
|---|---|
| Spoken naturalness | 10 |
| Economy and cadence | 10 |

Never report a bare number. Per category: score, strengths, failures,
**evidence**, recommended revision.

**Any high-severity mathematical or proof-status issue blocks finalization
regardless of total score.** A high total must never mask a severe error.

---

## 8. Verification — inherited, non-negotiable

> **A render is finished when it has passed
> [`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md), not when it renders without
> a traceback.** That spec requires seven viewing passes (uninterrupted, learner
> reconstruction, muted, audio-only, frame-by-frame, plan comparison, adjacent
> scenes), timecoded findings, an eight-category scorecard, and a verdict of
> `APPROVE` / `APPROVE WITH MINOR CHANGES` / `REVISE` / `REBUILD`. The result is
> written to `projects/<name>/RENDER_REVIEW.md`, per scene. **Its §16 blockers
> override any score.**
>
> The checks below are the mechanical floor underneath that review.

These come from `MANIM_GUIDE.md` and the project bug log. Every bug found in
this repo so far has been **silent** — no traceback.

- **Rendering without errors is not verification.** Extract frames and look at
  them: `ffmpeg -ss <t> -i <mp4> -frames:v 1 out.png`, then read the png.
- **Silence detection cannot see missing audio.** A scene with no audio *stream*
  reports as no silence at all. Cross-check `ffprobe -select_streams a` duration
  against video duration.
- **Verify claims numerically before animating them** — now via `facts.py`.
- **Draft at `-ql` (480p, 15 fps)**; full resolution only once a scene is
  settled. Do not judge colour *or motion smoothness* at draft — CE couples
  frame rate to the quality flag, so draft is half the frame rate final is.
  Crop and zoom before judging colour.
- **Always go through `render.sh`.** Running `manim` directly from another cwd
  silently loses `manim.cfg` — wrong background colour, wrong resolution, and
  output scattered into a stray `media/` folder relative to wherever it ran.
  (This was true of ManimGL and `custom_config.yml` too; the failure mode
  carried over unchanged when the project moved to Manim Community, only the
  config filename changed.)

---

## 8b. The visual system — see [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md)

Typography, colour, and layout are not per-scene decisions.
[`RENDER_REVIEW_SPEC.md`](RENDER_REVIEW_SPEC.md) §8.3 asks whether a scene
matches *the project's established visual language*; that language is written
down in [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) and implemented in
`projects/<name>/common/`.

The two rules that were broken here and cost a whole chapter's rerender:

- **Never let a font default.** ManimGL ships `text.font: Consolas`, which is
  absent from macOS, so every `Text` fell back to an unspecified Pango family.
  (Manim Community has no font default to ship at all — see
  [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §1 for how the same rule is now
  enforced.)
- **`MathTex` for mathematics, `Text` for English.** Not the other way round,
  and never both for the same job in the same frame. (Named `Tex` under
  ManimGL; Manim Community's own `Tex` is a different, text-mode renderer —
  see [`VISUAL_SYSTEM.md`](VISUAL_SYSTEM.md) §2.)

## 9. Interaction defaults

On receiving a source:

1. inspect it
2. say what I believe it contains
3. identify the missing production context
4. ask **the single most useful plain-language question**

Opening move, roughly:

> I'll study the source and separate its core idea from its supporting
> machinery. I won't assume you can identify the prerequisites or decide the
> mathematical path. I'll give you a concise map, recommend what the video
> should teach, and ask one question about audience or scope.

Then analyse. **Do not open by drafting narration. Do not open by teaching the
subject interactively.**

After the video exists: answer follow-ups, and treat confusion as evidence about
the script — locate the weak learner-state transition and fix that scene. A
follow-up question does not mean starting over.
