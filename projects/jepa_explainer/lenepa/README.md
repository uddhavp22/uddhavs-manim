# LeNEPA Manim segment

Eight Manim Community scenes for a sub-five-minute chapter inside the larger
JEPA-variants explainer.

## Render

From the `uddhavs-manim` repository root:

```bash
# Timing-only draft; no network and intentionally silent
LENEPA_VOICE=timing ./render.sh projects/jepa_explainer/lenepa/scenes.py -a -ql

# Local macOS synthetic draft (outside sandboxes where `say` can synthesize)
LENEPA_VOICE=draft ./render.sh projects/jepa_explainer/lenepa/scenes.py -a -ql

# Requested ElevenLabs preview render
LENEPA_VOICE=eleven ./render.sh projects/jepa_explainer/lenepa/scenes.py -a -qh
```

Or render and concatenate through `build.sh`:

```bash
projects/jepa_explainer/lenepa/build.sh --voice eleven --quality h
```

The final human recording should replace the temporary TTS, not the script.
Use `SCRIPT_ELEVENLABS.md` for pronunciation and recording handoff.

