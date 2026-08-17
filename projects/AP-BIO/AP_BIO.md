# AP-BIO — project requirements

## What this is

Brief, silent, caption-only Manim scenes explaining chemistry fundamentals an
AP Biology course assumes (bonding, intermolecular forces). No voiceover —
this is a different delivery format from `projects/sigreg_explainer/`, which
is narrated video. AP-BIO scenes are meant to be rendered individually, then
assembled into a click-through slide deck with `manim-slides` (see
`docs/PLUGINS.md`, "Adopted" — installed 2026-08-10, spike-tested against
this repo's manim engine).

Because there's no audio track, the on-screen animation carries the full
explanatory load that narration + visual would normally split between them
in `sigreg_explainer`. The caption names and anchors what the visual has
already shown; it is not a second channel doing independent explanatory work.
Keep captions to the single sentence already scripted per concept — do not
pad them into paragraphs to compensate for the missing voiceover. Let the
visual construction (atoms approaching, a bond forming, a dashed weak-force
line appearing) carry the "why," the same way the drafting process in
`docs/NARRATION_SPEC.md` §29 asks narration to preserve the reasoning path
without duplicating the visual — here that discipline runs in the other
direction: the *visual* must preserve the reasoning path without depending on
narration that doesn't exist.

## Content scope: Types of Bonds

Three scenes, one file per concept, under `projects/AP-BIO/chemistry-concepts/`:

| File | Scene class | Caption (verbatim) |
|---|---|---|
| `covalent_bonds.py` | `CovalentBonds` | "Atoms share pairs of electrons to form strong links inside molecules." |
| `ionic_bonds.py` | `IonicBonds` | "Charged ions attract each other after an electron transfer." |
| `hydrogen_and_van_der_waals.py` | `HydrogenAndVanDerWaals` | "Weak forces maintain the 3D shapes of large molecules like proteins and DNA." |

These three together are the "Types of Bonds" unit within the broader
AP-BIO chemistry-concepts track (intermolecular forces, basic bonding —
the prerequisite chemistry AP Bio assumes before macromolecules). Caption
text is fixed as scripted above; do not rephrase it when implementing.

Hydrogen bonds and Van der Waals forces share one scene because they're
scripted as one idea (weak forces vs. strong covalent/ionic bonds) — don't
split them into two files unless a future caption revision separates them.

## Why not chanim

`docs/PLUGINS.md` already documents this in detail: `chanim` is archived
upstream and, worse, its `manim.plugins` entry point crashes manim CE outright
just from being installed (`TexSymbol` doesn't exist in this repo's manim
version). It is **not a dependency** here, installed or otherwise.

"Follow chanim's example" means matching its *visual idiom* — clean 2D
structural diagrams (labeled circles for atoms, lines for bonds, not 3D
ball-and-stick renders) — reimplemented from plain Manim CE primitives
(`Circle`, `Dot`, `Line`, `DashedLine`, `VGroup`, `MathTex`/`Text`). chanim's
own README doesn't document its internal drawing primitives (single
high-level `ChemWithName(...)` example only, no primitive-level code), so
there's nothing to port — this is a from-scratch small drawing vocabulary,
not a reimplementation of chanim's API.

## Visual vocabulary

Revised 2026-08-10 after the first pass shipped visually thin (two circles
and a line, in most of an otherwise empty frame) and was rejected on sight.
"Brief" was being read as license to skip the mechanism entirely — a
labelled line doesn't show sharing, an arrow doesn't show a transfer. The
fix wasn't more time on screen, it was showing the actual electron
behavior the caption names, and giving every scene a title so it doesn't
open on bare geometry with no orientation:

- **Atom**: a filled `Circle` with an element-label `Text`/`MathTex` at its
  center. Color by element role (see `common/palette.py`), not by literal
  CPK convention.
- **Shell**: a faint valence-electron ring around an atom (`common/chem.py`'s
  `shell()`), holding the actual `Dot` electrons that later move. `empty`
  slots render as open outline circles, not just absent dots, so a gap in
  an octet is something the viewer sees close, not something the caption
  has to assert happened.
- **Covalent bond**: each atom's one contributed electron individually
  orbits its own nucleus first (`Rotating` about the atom's own center, on
  its own shell), establishing "these belong to separate atoms" before
  anything merges. Bonding moves both electrons into a shared, softly
  filled `Ellipse` spanning the bond axis, which pulses once — the electron
  pair now occupies the region between both nuclei instead of sitting at
  an inert midpoint.
- **Ionic bond**: the donor's shell shows its one electron; the acceptor's
  shell shows a full seven plus one visible open gap. The electron
  literally travels the gap along an `ArcBetweenPoints`, and the gap
  becomes that same electron (recolored in place, not a new mobject placed
  on top of it — see the note in `chemistry-concepts/ionic_bonds.py` about
  why: an object created separately from the one that actually moved will
  get left behind by a later group animation). The donor's now-empty shell
  ring fades and the atom itself shrinks slightly — a cation really is
  smaller than the neutral atom it came from, and the acceptor's ring
  recolors to signal a completed octet, not just a same-size relabeling
  with a badge stuck on.
- **Water molecule**: `common/chem.py`'s `water_molecule()` — a real bent
  H2O at the actual ~104.5° bond angle, with δ+/δ- partial-charge labels.
  This is the concrete, named case a "hydrogen bond" actually refers to;
  two abstract fragments with a dashed line between them was not.
- **Helix ribbon**: `helix_ribbon()` — a coiled backbone (2D alpha-helix
  projection) with dashed rungs connecting matching turns, the actual
  "3D shape of a large molecule" the caption names, at the scale where it
  matters biologically rather than a flat chain of unrelated atom letters.
- **Hydrogen bond / Van der Waals contact**: both still a `DashedLine`
  (`weak_force_line()`), but now deliberately different in weight — the
  hydrogen bond between water molecules renders at higher opacity than the
  Van der Waals contact between generic nonpolar groups, so "weaker, less
  specific" is something the two dashes visibly disagree about, not a fact
  only the two labels assert.

Every one of these belongs in the shared `projects/AP-BIO/common/chem.py`,
not copy-pasted into each scene file — see "Minimum redundancy" below.

## Pacing — 3blue1brown-style, adapted for brief silent scenes

Base timing on `docs/VISUAL_SYSTEM.md` §6, already binding repo-wide:

- Default transition **0.6s**; a transformation the viewer must actually
  follow (bond forming, electron transferring) gets **1.2s**.
- No bounce/elastic/overshoot easing.
- One dominant focal event per beat — don't animate the atoms approaching
  *and* the caption fading in *and* a label appearing all at once.
- Safe margins: nothing within 0.45 units of any frame edge (`VISUAL_SYSTEM.md` §5).

Beyond that, since there's no narration to pace against, hold each finished
state for **1.5–2.5s** so a viewer has time to read the caption before the
scene ends — this is the silent-scene equivalent of `beat.py`'s
`MAX_INSPECT = 2.2` constant. Target **15–25s total per scene**: brief means
brief. A three-beat shape works for all three concepts —

1. atoms/molecules enter, positioned apart (~2s);
2. the bond or force forms, with the one motion that is the actual content
   of the concept (~3–5s, per the 1.2s transformation rule, held slightly
   past the animation's end);
3. caption appears once the visual has already shown the thing it names,
   held ~2s, then out.

Do not narrate-via-caption *before* the visual has shown the relevant motion
— the caption should land on something the viewer has already watched
happen, the same "equations arrive from the scene" discipline
`NARRATION_SPEC.md` §10 applies to spoken narration.

## Caption voice

`NARRATION_SPEC.md` governs *spoken* narration and is written for
multi-paragraph reasoning, but its underlying rules about what to avoid
apply just as much to a single on-screen sentence: no manufactured
importance language ("crucial," "powerful," "amazing"), no address-the-viewer
filler ("notice that," "you can see"), no hedging softeners. State the
mechanism plainly, the way the three captions already scripted above do —
they're the model for any caption added later in this track.

## Minimum redundancy

```
projects/AP-BIO/
├── AP_BIO.md                  (this file)
├── common/
│   ├── __init__.py
│   ├── palette.py             (role-based colors: ATOM_*, BOND_COVALENT,
│   │                            BOND_IONIC, BOND_WEAK, CHARGE_POS/NEG,
│   │                            DELTA_POS/NEG, BACKBONE, following
│   │                            sigreg_explainer/common/palette.py's
│   │                            architecture — roles, not literal element
│   │                            names, so re-theming is a one-file edit)
│   ├── type.py                 (three tiers only — `title()`, `caption()`,
│   │                            `label()` at VISUAL_SYSTEM.md's TITLE/
│   │                            CAPTION/LABEL sizes, not the full six-tier
│   │                            scale sigreg's type.py carries for
│   │                            equations this project doesn't need)
│   └── chem.py                 (the visual vocabulary above: `atom()`,
│                                 `shell()`, `covalent_bond()`,
│                                 `ionic_bond()`, `water_molecule()`,
│                                 `helix_ribbon()`, `weak_force_line()` —
│                                 shared by all three scene files, each of
│                                 which should contain only its own beat
│                                 sequencing, not drawing logic)
└── chemistry-concepts/
    ├── covalent_bonds.py
    ├── ionic_bonds.py
    └── hydrogen_and_van_der_waals.py
```

`projects/AP-BIO/common/` is deliberately its own small module, not an import
from `sigreg_explainer/common/` — the two projects have different owners,
different subject matter, and no reason to couple their lifecycles. Only
`type.py`'s numeric scale (not the file itself) is carried over, since
`VISUAL_SYSTEM.md`'s type scale is a repo-wide rule, not a SIGReg-specific one.

Within `chemistry-concepts/`, if a second bonding-adjacent concept is added
later and needs the same atom/bond vocabulary, it imports `common/chem.py` —
it does not re-derive atom-drawing code inline.

## Validation

Each scene renders as a normal manim `Scene` subclass of `manim_slides.Slide`,
so both of these must work:

```
./render.sh projects/AP-BIO/chemistry-concepts/covalent_bonds.py CovalentBonds -ql
uv run manim-slides render -ql projects/AP-BIO/chemistry-concepts/covalent_bonds.py CovalentBonds
```

The first confirms the scene renders correctly as plain video; the second
confirms the `self.next_slide()` breaks are actually usable by the presenter
CLI once all three scenes exist and get assembled into one deck (a later
step, not part of this batch — no deck-assembly script exists yet).
