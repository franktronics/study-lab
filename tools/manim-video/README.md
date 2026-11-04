# manim-video

Explanation videos with [Manim Community](https://www.manim.community/). The shared setup lives in `studylab_manim/`; each video lives in its own `studio/YYYY-MM-DD-<slug>/` folder and only contains the animation-specific code.

Used through the `manim-video` skill (`.agents/skills/manim-video/SKILL.md`).

```
manim-video/
├── pyproject.toml / uv.lock / .python-version   # uv project (Python 3.12, pinned Manim)
├── studylab_manim/
│   ├── config.py   # canvas, layout zones, qualities, LaTeX template, paths
│   ├── theme.py    # dark/light palettes, font sizes
│   ├── scene.py    # StudyScene base class + helpers
│   ├── new.py      # scaffold a studio folder
│   ├── render.py   # render + concat + frame extraction
│   └── check.py    # verify requirements
├── examples/demo.py  # smoke test / reference usage
├── studio/           # one folder per video (git-ignored)
└── .cache/           # Manim media, previews, frames (git-ignored)
```

Commands (from this folder):

```sh
uv sync                                            # install Python deps
uv run python -m studylab_manim.check              # verify requirements
uv run python -m studylab_manim.new <slug>         # new studio folder
uv run python -m studylab_manim.render <id>        # preview + frames
uv run python -m studylab_manim.render <id> --quality final
uv run python -m studylab_manim.render examples/demo.py
```
