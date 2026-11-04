---
name: manim-video
description: Create or modify short explanation videos (Manim Community) in tools/manim-video/. Use when the user asks for a video or animation explaining a concept, wants an existing video changed, or when a visual, step-by-step animated explanation (derivations, graphs, geometric intuition, processes) would clearly help. Handles first-time installation, the studio folder per video, preview with visual self-check, final render, and registration in the memo.
---

# Manim video

Tool root: `tools/manim-video/` (all commands below run from there). The shared base (`studylab_manim`) already defines the canvas, themes, layout zones, LaTeX template and helpers. For each video you only write the **animation-specific code** in a studio folder.

## Talking to the user

The student is not necessarily technical. Never expose commands, stack traces, package names or install logs. Talk about the video, not the tooling. If something technical blocks you, fix it silently; only if you truly cannot, explain the problem in one plain sentence.

## 1. Setup (first use, or when a render fails on missing tools)

```sh
uv --version                              # is uv available?
uv sync                                   # Python 3.12 + pinned Manim in .venv
uv run python -m studylab_manim.check     # prints OK / MISSING per requirement
```

If anything is missing, ask **once**, simply, e.g. *"To create videos I first need to install a few tools (a few minutes). Shall I do it?"* If yes, install **everything** yourself, on whatever OS this is, then re-run `check` until all is OK. If no, stop and offer another format (explanation, html page).

What to install when missing (adapt to the OS and what is already present):

| Requirement | macOS | Linux (Debian/Ubuntu; adapt for others) | Windows (PowerShell) |
|---|---|---|---|
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | same | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| LaTeX (if no `latex` at all) | TinyTeX: `curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" \| sh` | same | TinyTeX: download and run `https://yihui.org/tinytex/install-bin-windows.bat` |
| LaTeX packages | `tlmgr install standalone preview amsmath amsfonts mathtools tools xcolor dvisvgm` | same | same |
| Build deps (only if `uv sync` fails building pycairo / manimpango) | `brew install cairo pango pkg-config` | `sudo apt install -y build-essential python3-dev pkg-config libcairo2-dev libpango1.0-dev` | not needed (wheels) |

Notes:
- Prefer TinyTeX (small, no admin rights). If a full LaTeX already exists, only add the missing packages (an existing system TeX Live may need `sudo tlmgr ...`).
- TinyTeX's default bin folders are added to `PATH` automatically by `studylab_manim`, so no new shell is needed.
- `uv` installs Python 3.12 itself; no system Python is required.
- If `sudo` needs a password, ask the user to run that one command, giving it to them ready to paste.

## 2. Create a video

### 2.1 Scope
- One video = **one concept**, 30 s – 3 min. Longer → propose splitting into several videos.
- Base the content on the course assets (source of truth). Check the memo (`tools/memo/INDEX.md`) for an existing explanation approach to reuse.
- On-screen text is in the **user's language** (language of their request). No audio, the captions carry the explanation.

### 2.2 Scaffold
```sh
uv run python -m studylab_manim.new <slug>     # -> studio/YYYY-MM-DD-<slug>/{brief.md, scene.py}
```
`<slug>`: kebab-case English, describes the concept (e.g. `gibbs-phenomenon`).

Fill `brief.md`: goal, concept, language, theme, memo entry, **sources** (precise asset references), **storyboard** (5–10 lines, one line per scene/beat).
For a long or ambiguous request, show the storyboard to the user (in plain words) and wait for approval before coding. For a short, clear request, go straight on.

### 2.3 Write `scene.py`
```python
from manim import *
from studylab_manim import StudyScene

class Intro(StudyScene):
    def construct(self):
        self.title_card("Gibbs phenomenon", "Why the overshoot never disappears")

class Main(StudyScene):
    def construct(self):
        self.section("Partial sums")
        self.cite("VL-05, p. 12")
        self.caption("A square wave is a sum of odd harmonics.")
        ...

class Recap(StudyScene):
    def construct(self):
        self.end_card(["Point 1", "Point 2", "Point 3"], title="Key points")
```
- Every scene class inherits `StudyScene`. Scenes are rendered **in definition order** and concatenated into one video. Classes used only as a base or named `_Something` are skipped.
- Typical structure: `Intro` (title card) → one or more content scenes → `Recap` (end card).
- `examples/demo.py` is a complete working reference.

**StudyScene API** (use it instead of re-implementing):

| Helper | Purpose |
|---|---|
| `self.theme`, `self.c("primary")` | Theme palette. Keys: `text muted primary secondary accent highlight positive negative grid background`. Always use semantic keys, never hard-coded colors. |
| `self.text(s, size="body", color=None)` | Prose (any Unicode). Sizes: `title subtitle heading body caption small`. |
| `self.tex(*parts, size="math", color=None)` | Math via LaTeX (`MathTex`). Sizes: `display math small`. |
| `self.axes(x_range, y_range, x_label=, y_label=)` | Themed axes, already fitted into the content area. Labels are LaTeX. |
| `self.plot(ax, fn, color="primary")` | Themed curve on axes. |
| `self.title_card(title, subtitle)` | Animated opening card (clears itself). |
| `self.section(title)` | Persistent header top-left; replaces the previous one; `None` removes. |
| `self.caption(text)` | Explanation at the bottom; replaces the previous one; auto-wrapped; `None` removes. |
| `self.cite(source)` | Small source reference bottom-right (e.g. "VL-05, p. 12"). |
| `self.step_equation(steps, stacked=False)` | Derivation step by step (morphing, or stacked lines with `&=` alignment). |
| `self.highlight(mob, color="highlight", label=None)` | Box (+ label) around a part of the screen. |
| `self.fit(mob)` | Shrink to fit the content area and center it there. |
| `self.clear_content()` / `self.clear_all()` | Fade out content (keeping header/caption/citation) / everything. |
| `self.end_card(points, title)` | Recap screen with bullets. |

Layout rules:
- Keep content inside the **content area** (between header and caption). Pass large groups through `self.fit()`.
- Never place free text in the caption or citation zones; use `caption()` / `cite()`.
- Use `Text` (via `self.text`) for prose, `MathTex` (via `self.tex`) only for math.
- Pace for reading: after each new caption leave time (`self.wait(...)`, about 1 s per 10 words).
- Plain Manim (`Create`, `Transform`, `VGroup`, `always_redraw`, `ValueTracker`...) is fine for anything specific.

### 2.4 Preview and self-check (mandatory)
```sh
uv run python -m studylab_manim.render <id>          # 480p preview + frames
```
Prints `VIDEO <path>` and one `FRAME <path>` per extracted PNG (in `.cache/<id>/frames/`; `--frames N` for more per scene). **Open the frames and look at them.** Check:
- nothing cut off at the edges, nothing overlapping (text on curves, caption on content);
- text readable (size, contrast), correct language, no LaTeX artefacts;
- the animation actually shows what the storyboard says, mathematically correct.

Fix and re-render until clean. To iterate on one scene: `--scenes Main`.

### 2.5 Final render
```sh
uv run python -m studylab_manim.render <id> --quality final [--theme light]
```
Output: `studio/<id>/<id>.mp4` (1080p30). Theme defaults to `dark`; use `light` when asked or for print/light pages. Record the theme in `brief.md`.

### 2.6 Register in the memo, then answer
1. Follow the `memo` skill, "Generated outputs": find or create the knowledge entry for the concept, add `tools/manim-video/studio/<id>/<id>.mp4` (with key timestamps) to its references, update `INDEX.md`. Write `brief.md`'s "Memo entry" line.
2. Tell the user, in their language: what the video shows (1–2 sentences) and the path to the `.mp4` as a link.

## 3. Modify an existing video
- Edit the same studio folder in place (`brief.md`, `scene.py`), preview + self-check, final render; the `.mp4` is overwritten so memo references stay valid.
- A genuinely different video (another concept or angle) → new studio folder.

## 4. Extending the base
If a pattern appears repeatedly across videos (a diagram type, a recurring animation), add a helper to `studylab_manim/scene.py` (or a new module) rather than copy-pasting, keep it theme-aware, add it to the API table above, and render `examples/demo.py` to make sure nothing broke.

## Troubleshooting (internal, don't expose)
- `latex`/`dvisvgm` errors → run `check`, install missing LaTeX packages with `tlmgr install <pkg>`.
- LaTeX error in a formula → the bad string is in the Manim output; fix the TeX (escape `\`, balanced braces; text inside math with `\text{}`).
- Missing glyphs in `Text` → it's prose with special characters; `Text` handles Unicode, don't put it in `MathTex`.
- Render is slow → keep iterating with the preview quality and `--scenes`.
