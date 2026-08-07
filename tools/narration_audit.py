#!/usr/bin/env python3
"""Narration diagnostics for the Explanation Compiler (EXPLAINER_PROCESS.md).

The process document's narration audit is quantitative -- "report repetition per
1,000 words", "flag clusters, not isolated uses". Left to prose judgement that
audit degrades into asking whether a script "sounds AI-generated", which is
exactly what the process forbids. So it runs here instead.

The narration lives inside `self.voiceover(text=...)` calls in the scene files.
This walks the AST rather than the rendered .srt, because the .srt only exists
after a render and is segmented by Whisper into subtitle fragments -- the
process explicitly wants the audit run on spoken passages, not on subtitles.

Usage:
    python3 tools/narration_audit.py projects/sigreg_explainer/chapterB
    python3 tools/narration_audit.py projects/sigreg_explainer/chapterB --quotes
    python3 tools/narration_audit.py .../b00_*.py .../b01_*.py    # one part only

Exit status is 1 if any check exceeds its budget, so this can gate a build.
"""

from __future__ import annotations

import argparse
import ast
import pathlib
import re
import statistics
import sys
from collections import Counter

# --- what counts as a finding -----------------------------------------------
#
# Budgets are per 1,000 words and deliberately non-zero. The process says these
# constructions are "not absolutely forbidden, but repeated use is a major
# failure", so a zero budget would be a misreading -- it would push the script
# toward stilted avoidance rather than natural speech.

TEACHING_PROCESS = [
    r"\blet'?s\b", r"\bwe'll (?:start|begin|look at|see)\b",
    r"\bhere'?s the (?:key|trick|idea)\b", r"\bthe key (?:idea|insight)\b",
    r"\bthis is where\b.{0,24}\b(?:interesting|fun)\b",
    r"\bstep back\b", r"\bat its core\b", r"\bfundamentally\b",
    r"\bin other words\b", r"\bthe important thing\b",
    r"\bwhat (?:we'?re|I'?m) going to do\b", r"\bfirst,? (?:let|we)\b",
]

CONTRAST = [
    r"\bnot\b[^.;]{1,48}\bbut\b", r"\brather than\b", r"\binstead of\b",
    r"\bis not\b[^.;]{1,40}\bit is\b", r"\bwe do(?:n'?t| not)\b[^.;]{1,40}\bwe\b",
    r"\bnot merely\b", r"\bthe point is not\b",
]

ATTENTION = [
    r"\bwatch\b", r"\bnotice\b", r"\blook (?:at|closely|here)\b",
    r"\bsee (?:what|how)\b", r"\bobserve\b",
]

IMPORTANCE = [
    r"\bcrucial", r"\bprofound", r"\bbeautiful", r"\bmagical", r"\bremarkable",
    r"\bsurprisingly\b", r"\bpowerful", r"\belegant", r"\bkey insight\b",
    r"\bfascinating", r"\bincredibl",
]

FALSE_SURPRISE = [
    r"\byou might be surprised\b", r"\bamazingly\b", r"\bbelieve it or not\b",
    r"\bthe shocking\b", r"\bhere'?s the (?:amazing|wild) part\b",
]

TRANSITIONS = ["now", "here", "instead", "rather", "key", "important",
               "simply", "essentially", "just", "actually"]

# --- the four tells that passed every budget above ---------------------------
#
# Chapter B rev 1 scored "all budgeted checks within limits" and still read as
# machine-written, because the loudest patterns in it were not shapes any of the
# lists above describe. Each of these is a named section of NARRATION_SPEC.md.

# NARRATION_SPEC.md section 13: one appositive shape used as the default
# sentence generator. "One last thing, and it is the thing the whole video runs
# on." The clause adds no content -- it only postpones the noun.
APPOSITIVE = [
    r",\s+and (?:it|this|that|these|one|they)\s+(?:is|are|was|were|has|have|does|do)\b",
    r",\s+and (?:it|this|that)'s\b",
    r"\band (?:it|this) (?:is|has) (?:the|a|an)\b",
]

# NARRATION_SPEC.md section 5: evaluative framing standing in for the
# observation. If it is worth remembering, that is the viewer's call.
EVALUATIVE = [
    r"\bworth (?:remembering|banking|noting|being|asking|reading|measuring|"
    r"the trouble|it\b)", r"\bthat'?s? worth\b", r"\bhold on to that\b",
    r"\bremember (?:that|those|this)\b", r"\bthe most (?:useful|important)\b",
    r"\bthe whole (?:point|reason|requirement|thing|derivation|video|chapter|"
    r"of it)\b", r"\bwhich is the whole\b", r"\bis what makes\b.{0,20}\bspecial\b",
]

# NARRATION_SPEC.md section 4: open on the object, not on a presentational
# gesture toward it.
HERE_IS = [r"(?:^|(?<=[.!?]\s))\s*(?:And |But |So )?Here (?:is|are|'s)\b"]

# NARRATION_SPEC.md section 18. A slogan is short, final, and evaluative rather
# than informative -- it restates rather than advances. One in a script is a
# good line; one per scene is a template, and the template is what gives the
# whole document away.
SLOGAN_SHAPE = re.compile(
    r"^(?:That(?:'s| is)|It(?:'s| is)|Which is|And that|This is|We did not|"
    r"Nothing here|No scale|They were chosen|One frequency)\b", re.I)
SLOGAN_EVALUATIVE = re.compile(
    r"\b(?:whole|worth|why|surprise|honest|difference|reason|precisely|"
    r"exactly what|is not|rather than|cannot|only ever|the point)\b", re.I)
SLOGAN_MAX_WORDS = 14

# Verbs that assert a proof status. Not errors -- they are cross-checked by hand
# against the claims ledger, so the audit's job is to surface every one.
PROOF_VERBS = [r"\btherefore\b", r"\bmust\b", r"\bproves?\b", r"\bshows? that\b",
               r"\bguarantees?\b", r"\bit follows\b", r"\bhence\b",
               r"\bimplies\b", r"\bcannot\b"]

# Per-project metaphor inventory. The process caps a video at roughly one
# central metaphor, so the point of this list is to make churn countable.
METAPHORS = ["fingerprint", "shadow", "arrow", "lens", "probe", "machine",
             "map", "language", "recipe", "knob", "spotlight", "staircase"]

BUDGETS = {              # findings per 1,000 words
    "teaching-process": 4.0,
    "contrast": 4.0,     # was 6.0; rev 1 sat at 1.4 and still read as a tic
    "importance": 2.0,
    "false-surprise": 0.0,
    "bare-attention": 2.0,
    "appositive": 2.0,
    "evaluative": 1.5,
    "here-is": 2.0,
}

# Not per-1k: a fraction of scenes. Measured over scenes, because the failure is
# that EVERY scene ends the same way, which no per-word rate can see.
SLOGAN_ENDING_BUDGET = 0.35

# A count, and zero, because the screen is a different channel from the voice.
# The rev-2 rewrite scored 0/12 slogans in the narration and still put thirteen
# slogan captions on screen -- the tic moved channels rather than going away,
# and this scan already detected every one of them without ever failing the
# build. Zero rather than a rate: a slogan-shaped caption is a decision someone
# made, not a statistical tendency, so each one is answerable individually.
SCREEN_SLOGAN_BUDGET = 0


# --- extraction --------------------------------------------------------------

BOOKMARK = re.compile(r"<bookmark\s+mark=['\"][^'\"]*['\"]\s*/>")


def _const_str(node: ast.AST) -> str | None:
    """Recover a string from a literal or an implicit/explicit concatenation."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _const_str(node.left), _const_str(node.right)
        if left is not None and right is not None:
            return left + right
    if isinstance(node, ast.JoinedStr):        # f-string: not narration
        return None
    return None


def extract(path: pathlib.Path) -> list[str]:
    """Every `text=` passed to self.voiceover(...) in one scene file."""
    tree = ast.parse(path.read_text(), filename=str(path))
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if not (isinstance(fn, ast.Attribute) and fn.attr == "voiceover"):
            continue
        for kw in node.keywords:
            if kw.arg != "text":
                continue
            # A list of alternatives (b07 varies its line per batch) counts as
            # every branch, since each one is spoken in some render.
            if isinstance(kw.value, (ast.List, ast.Tuple)):
                for elt in kw.value.elts:
                    s = _const_str(elt)
                    if s:
                        out.append(s)
            else:
                s = _const_str(kw.value)
                if s:
                    out.append(s)
    return [BOOKMARK.sub("", s).strip() for s in out]


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", text)


# --- checks ------------------------------------------------------------------

def find_all(passages: list[tuple[str, str]], patterns: list[str]):
    """-> [(scene, sentence, matched_text)] over every sentence of every passage."""
    hits = []
    for scene, passage in passages:
        for sent in sentences(passage):
            for pat in patterns:
                for m in re.finditer(pat, sent, flags=re.I):
                    hits.append((scene, sent, m.group(0)))
    return hits


def bare_attention(passages: list[tuple[str, str]]):
    """Attention commands that never say what relationship to follow.

    "Watch the yellow curve against the ghost" is fine -- it names the
    comparison. "Watch what happens" is not. The heuristic: an attention verb
    whose sentence carries no comparative or relational cue.
    """
    RELATIONAL = re.compile(
        r"\b(?:against|compared|between|while|as |relative|versus|vs\b|"
        r"the same|differ|match|track|both|each other|line up|"
        r"stays?|never|still|apart|together)\b", re.I)
    hits = []
    for scene, passage in passages:
        for sent in sentences(passage):
            if not any(re.search(p, sent, re.I) for p in ATTENTION):
                continue
            # A concrete named object also counts as specifying the relation.
            named = re.search(r"\b(?:curve|arrow|dot|panel|bar|segment|axis|"
                              r"point|band|count|area|red|blue|yellow)\b",
                              sent, re.I)
            if not RELATIONAL.search(sent) and not named:
                hits.append((scene, sent, "bare attention command"))
    return hits


def cadence(passages: list[tuple[str, str]]):
    """Longest run of consecutive short sentences, per scene.

    The process flags "short fragment -> short fragment -> summary" as a
    signature LLM rhythm. A run of four or more is where it becomes audible.
    """
    # Aggregated per SCENE, not per passage. A run has to be measured across
    # the whole spoken track: consecutive passages are heard back to back, so
    # three short sentences ending one passage and three opening the next is a
    # run of six to the viewer, and per-passage stats would score it as 3+3.
    by_scene: dict[str, list[int]] = {}
    for scene, passage in passages:
        by_scene.setdefault(scene, []).extend(
            len(words(s)) for s in sentences(passage))

    report = []
    for scene, lens in by_scene.items():
        run = best = 0
        for n in lens:
            run = run + 1 if n <= 8 else 0
            best = max(best, run)
        report.append((scene, best, statistics.mean(lens),
                       statistics.pstdev(lens) if len(lens) > 1 else 0.0))
    return report


def slogan_endings(passages: list[tuple[str, str]]):
    """Scenes that close on a short evaluative aphorism.

    NARRATION_SPEC.md section 18. Detection is deliberately shape-based rather
    than a phrase list, because the whole problem is that the phrases are all
    different and the shape is always the same: short, final, and restating
    rather than advancing.

    Returns (hits, scene_count) so the caller can report a fraction.
    """
    last_by_scene: dict[str, str] = {}
    for scene, passage in passages:
        sents = sentences(passage)
        if sents:
            last_by_scene[scene] = sents[-1]      # later passages overwrite

    hits = []
    for scene, sent in last_by_scene.items():
        if len(words(sent)) > SLOGAN_MAX_WORDS:
            continue
        if SLOGAN_SHAPE.search(sent) or SLOGAN_EVALUATIVE.search(sent):
            hits.append((scene, sent, "slogan ending"))
    return hits, len(last_by_scene)


def repeated_openers(passages: list[tuple[str, str]], top=6):
    c = Counter()
    for _, passage in passages:
        for sent in sentences(passage):
            w = words(sent)
            if len(w) >= 2:
                c[" ".join(w[:2]).lower()] += 1
    return [(k, v) for k, v in c.most_common(top) if v > 2]


# --- reporting ---------------------------------------------------------------

def rate(n: int, total_words: int) -> float:
    return 0.0 if not total_words else n * 1000.0 / total_words


def section(title: str, hits, total_words: int, budget: float | None,
            show_quotes: bool, limit: int = 6) -> bool:
    r = rate(len(hits), total_words)
    over = budget is not None and r > budget
    flag = "OVER" if over else "ok"
    bud = f"  (budget {budget:.1f})" if budget is not None else ""
    print(f"\n{title}: {len(hits)} hits, {r:.1f} per 1k words{bud}   [{flag}]")
    if hits and (show_quotes or over):
        for scene, sent, matched in hits[:limit]:
            trimmed = sent if len(sent) <= 108 else sent[:105] + "..."
            print(f"    {scene:<26} \"{matched}\"  -- {trimmed}")
        if len(hits) > limit:
            print(f"    ... and {len(hits) - limit} more")
    return over


def onscreen_text(files) -> list[tuple[str, str]]:
    """Every multi-word string rendered on screen, as a second channel.

    The audit above walks `self.voiceover(text=...)` only, so it is structurally
    blind to `Text(...)`. Chapter B rev 2 scored a clean 0% slogan rate while
    twelve of the deleted slogans were still on screen as captions -- moved from
    the audio channel to the video channel, where they are more prominent and
    last longer. NARRATION_SPEC.md section 7.2 treats on-screen text as a
    channel; so must the audit.
    """
    out = []
    for f in files:
        tree = ast.parse(f.read_text(), filename=str(f))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "attr", getattr(node.func, "id", ""))
            if name not in ("Text", "words", "statement", "label", "caption",
                            "curve_label"):
                continue
            if node.args and isinstance(node.args[0], ast.Constant) \
               and isinstance(node.args[0].value, str):
                v = node.args[0].value
                if len(v.split()) >= 4:
                    out.append((f.stem, " ".join(v.split())))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="+",
                    help="scene .py files and/or chapter directories")
    ap.add_argument("--quotes", action="store_true",
                    help="quote passages even for checks within budget")
    args = ap.parse_args()

    # Several targets, because a chapter can be published as parts and a part
    # has to be auditable on its own. Auditing the whole directory to gate one
    # part means an unrevised scene elsewhere holds the gate red forever, which
    # trains everyone to read past it.
    files: list[pathlib.Path] = []
    for name in args.target:
        target = pathlib.Path(name)
        files += sorted(target.glob("[abc][0-9][0-9]*_*.py")) \
            if target.is_dir() else [target]
    files = sorted(set(files))
    label = " ".join(args.target)
    if not files:
        print(f"no scene files under {label}", file=sys.stderr)
        return 2

    passages: list[tuple[str, str]] = []
    per_scene: dict[str, int] = {}
    for f in files:
        texts = extract(f)
        scene = f.stem
        per_scene[scene] = sum(len(words(t)) for t in texts)
        passages += [(scene, t) for t in texts]

    total_words = sum(per_scene.values())
    print("=" * 74)
    print(f"NARRATION AUDIT  --  {label}")
    print("=" * 74)
    print(f"{len(files)} scenes, {len(passages)} spoken passages, "
          f"{total_words} words")
    for scene, n in per_scene.items():
        print(f"    {scene:<34} {n:>5} words")

    over = []
    over.append(section("Teaching-process narration",
                        find_all(passages, TEACHING_PROCESS), total_words,
                        BUDGETS["teaching-process"], args.quotes))
    over.append(section("Contrast templates",
                        find_all(passages, CONTRAST), total_words,
                        BUDGETS["contrast"], args.quotes))
    over.append(section("Unearned importance language",
                        find_all(passages, IMPORTANCE), total_words,
                        BUDGETS["importance"], args.quotes))
    over.append(section("Manufactured surprise",
                        find_all(passages, FALSE_SURPRISE), total_words,
                        BUDGETS["false-surprise"], args.quotes))
    over.append(section("Bare attention commands",
                        bare_attention(passages), total_words,
                        BUDGETS["bare-attention"], args.quotes))
    over.append(section("Appositive filler (\", and it is ...\")",
                        find_all(passages, APPOSITIVE), total_words,
                        BUDGETS["appositive"], args.quotes))
    over.append(section("Evaluative framing (\"worth remembering\", \"the whole point\")",
                        find_all(passages, EVALUATIVE), total_words,
                        BUDGETS["evaluative"], args.quotes))
    over.append(section("\"Here is / Here are\" openers",
                        find_all(passages, HERE_IS), total_words,
                        BUDGETS["here-is"], args.quotes))

    sl_hits, n_scenes = slogan_endings(passages)
    frac = len(sl_hits) / n_scenes if n_scenes else 0.0
    sl_over = frac > SLOGAN_ENDING_BUDGET
    print(f"\nScenes closing on a slogan: {len(sl_hits)}/{n_scenes} "
          f"= {frac:.0%}  (budget {SLOGAN_ENDING_BUDGET:.0%})   "
          f"[{'OVER' if sl_over else 'ok'}]")
    if sl_hits and (args.quotes or sl_over):
        for scene, sent, _ in sl_hits:
            print(f"    {scene:<26} \"{sent}\"")
    over.append(sl_over)

    print("\nTransition-word density (no budget; watch for one word dominating)")
    for w in TRANSITIONS:
        hits = find_all(passages, [rf"\b{w}\b"])
        if hits:
            print(f"    {w:<12} {len(hits):>3}   {rate(len(hits), total_words):>5.1f} /1k")

    print("\nMetaphor inventory (process caps a video near ONE central metaphor)")
    for m in METAPHORS:
        hits = find_all(passages, [rf"\b{m}s?\b"])
        if hits:
            scenes = len({s for s, _, _ in hits})
            print(f"    {m:<12} {len(hits):>3} uses across {scenes} scenes")

    print("\nProof-status verbs (cross-check each against the claims ledger)")
    pv = find_all(passages, PROOF_VERBS)
    print(f"    {len(pv)} occurrences, {rate(len(pv), total_words):.1f} /1k")
    if args.quotes:
        for scene, sent, matched in pv[:12]:
            trimmed = sent if len(sent) <= 96 else sent[:93] + "..."
            print(f"    {scene:<26} \"{matched}\"  -- {trimmed}")

    print("\nCadence (run = consecutive sentences of <= 8 words)")
    for scene, run, mean, sd in cadence(passages):
        mark = "  <-- choppy" if run >= 4 else ""
        print(f"    {scene:<34} longest run {run}, mean {mean:4.1f}, sd {sd:4.1f}{mark}")

    screen = onscreen_text(files)
    sl_screen = [(sc, t, "") for sc, t in screen
                 if len(words(t)) <= SLOGAN_MAX_WORDS
                 and (SLOGAN_SHAPE.search(t) or SLOGAN_EVALUATIVE.search(t))]
    screen_over = len(sl_screen) > SCREEN_SLOGAN_BUDGET
    print(f"\nOn-screen text: {len(screen)} multi-word captions, "
          f"{len(sl_screen)} slogan-shaped  (budget {SCREEN_SLOGAN_BUDGET})   "
          f"[{'OVER' if screen_over else 'ok'}]")
    if sl_screen:
        print("    (the voice is not the only channel -- check each by hand)")
        for sc, t, _ in sl_screen[:8]:
            print(f"    {sc:<26} \"{t}\"")
    over.append(screen_over)

    rep = repeated_openers(passages)
    if rep:
        print("\nRepeated sentence openers (>2 uses)")
        for opener, n in rep:
            print(f"    \"{opener}...\"  x{n}")

    print("\n" + "=" * 74)
    if any(over):
        print("RESULT: over budget on at least one check.")
        return 1
    print("RESULT: all budgeted checks within limits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
