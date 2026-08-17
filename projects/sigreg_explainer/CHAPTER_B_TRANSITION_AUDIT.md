# Chapter B transition and breathing audit

Review scope: the final spoken thought, final visual state, first spoken thought,
and first visual action at every scene boundary. This is an approval list, not a
blanket rewrite plan.

## Fixed in the current pass

- **B01:** simplified the argument to `histogram preserves shape -> hard bins
  break differentiability`; removed the detour through alternate bin widths.
- **B01 sample crossing:** replaced the stop-start nudges with one continuous
  pass. The bar-count jump is timed to the word “crosses.”
- **B01 -> B02:** retained the unresolved `x_i -> ?` frame and answered it
  directly with “What we can do is let each sample represent a direction.”
- **B02:** split the complex-plane introduction into shorter, synchronized
  beats with an inspection breath between the point and the arrow.
- **B02 -> B03:** shortened the outgoing fade and incoming build. B03 now opens,
  “So if we want to wrap these samples around a circle...”

## Recommended next changes

### 1. B03 -> B04 — highest-priority visual seam

B03 clears the entire three-panel rig, and B04 immediately rebuilds the same
rig to name it. The narration is a continuation, but the picture behaves like a
new topic. Preserve the rig across the cut and let the characteristic-function
name arrive on the existing construction. Add a short silent hold after the
name lands, before revealing the formula.

### 2. B06 -> B07 — strengthen the spoken handoff

B06 establishes that `t = 0` cannot distinguish batches. B07 then asks about a
carefully chosen `t`, but its opening currently sounds like an unrelated new
question. Carry the logic forward explicitly: zero fails, so try a nonzero
value. The full fade is acceptable here because the visual experiment changes.

### 3. B07 -> B08 — remove the repeated conclusion

B07 ends by saying that the average must be followed as `t` varies. B08 opens by
saying that one frequency can be fooled and that the entire function must be
kept. Those are the same conclusion twice. Let B07 land on the failed single
measurement; let B08 perform the sweep and state what the whole curve buys us.
The shared frequency axes already support a clean match cut.

### 4. B03 needs one more internal breath

B03 is the densest conceptual scene: wrapping, averaging, tracing, two
components, and symmetry all arrive in one run. Its current pauses occur after
the early wrap and near the middle. Add one inspection beat after the full
two-coordinate curve is established, before switching to the symmetry test.

### 5. B07 and B08 need result holds

Neither scene currently has a real inspection pause. Give the aligned-arrow
counterexample in B07 a short hold before nudging `t`, and give the uniqueness
statement in B08 a short hold before introducing finite-batch estimation.

## Boundaries that already read cleanly

- **B04 -> B05:** “what does the function keep?” naturally leads into the
  worked stress tests; the new batch justifies the visual reset.
- **B08 -> B09:** finite-batch uncertainty directly motivates testing which
  frequencies are useful, and the axes are preserved.
- **B09 -> B10:** the selected window asks for a Gaussian target; B10 supplies
  it on the same graph.
- **B10 -> B11:** the marked gap at `t = 1.6` becomes the first contribution to
  the loss with an exact visual handoff.

