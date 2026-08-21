# LeNEPA segment plan

## Audience contract

- **Assume:** vectors, embeddings, MSE, batches, and the role of a Transformer.
- **Refresh:** causal context and next-token prediction through one visible
  position.
- **Teach:** LeNEPA's next-latent path, shared projected loss space, and the
  temporal axis of SIGReg.
- **Defer:** attention equations, the internal SIGReg statistic, optimizer
  details, and a full benchmark survey.

This is a chapter inside a larger JEPA-variants explainer. It opens directly on
a time series and does not restart the broader JEPA story.

## Learner journey

Before the segment, the viewer may understand JEPA-style latent prediction but
not see why time series permit a particularly lean autoregressive variant. By
the end, they should be able to reconstruct this chain:

`signal -> convolutional patches -> causal next-latent prediction -> shared
projector MSE + per-sample temporal SIGReg -> frozen encoder`.

The misconception to prevent is that any globally non-collapsed batch also has
healthy temporal variation inside each sample. Scene 4 constructs a direct
counterexample.

## Explanation path

1. Preserve a signal's identity while it becomes a token sequence.
2. Focus on one causal prediction, then apply the one-step shift everywhere.
3. Follow one prediction/target pair through a shared projector into one scalar.
4. Show why the aggregate batch can hide within-sequence collapse.
5. Assemble the objective and discard its training-only head.
6. Define the fixed-recipe experiment without implying checkpoint transfer.
7. Report the results with the regression and single-seed qualifications.
8. Run the original signal through the complete method once.

## Visual invariant

The data object persists. A waveform patch becomes `z_t`; `z_t` remains a
column in the Transformer; `z_hat_t` and `z_(t+1)` remain columns through the
shared projector; the projected discrepancy becomes the scalar loss. Color is
semantic but never the only cue: every role also has a label, position, or
shape.

## Deliverables

- `scenes.py`: eight independently renderable Manim scenes with narration.
- `common/`: semantic palette, typography bridge, voice service, and reusable
  token/network primitives.
- `STORYBOARD.md`: timed shot plan.
- `SCRIPT_ELEVENLABS.md`: exact temporary-voice script and recording handoff.
- `facts.py`: executable numeric-claim checks.
- `build.sh`: scene render and master concatenation.

