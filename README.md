# Study Lab

A study environment for one subject, driven by an AI coding agent. Put your course material in it, open it in your AI tool, and study through conversation: the AI explains from your own courses, remembers what matters, makes explanation videos, and builds interactive pages.

## How it works

1. **One copy per subject.** Clone this project once for each subject (e.g. `study-signals`, `study-thermo`).
2. **Add your courses** to `assets/` — PDFs, slides, notes, exercises, in any folder structure you like.
3. **Open the folder in an AI agent** that can read and write files and run commands (Claude Code, Codex, Cursor, OpenCode...). It reads `AGENTS.md` and knows how to use everything here.
4. **Talk to it.** Ask questions, ask for explanations, videos, pages, summaries.

```sh
git clone <this-repo> study-<subject>
```

## What you can ask

- *"Explain the region of convergence from lecture 5."* — answers based on your course, with page references.
- *"Save this to the memo, it's important for the exam."* — the AI keeps it for later.
- *"Make a video showing how the Fourier partial sums converge."* — a short animated explanation.
- *"Make an interactive page on Bode plots with a quiz at the end."* — a page in your browser with formulas, diagrams, interactive plots, exercises.
- *"Build me a formula sheet from everything in the memo."* — a printable summary from what you saved.

The AI answers in the language you write in. Course content stays in its original language where it matters.

## Tools

| Tool | What it does |
|------|--------------|
| **memo** (`tools/memo/`) | The AI's long-term memory for this subject: what you asked to keep, with references to your courses. You never need to open it. |
| **manim-video** (`tools/manim-video/`) | Short explanation videos made with [Manim Community](https://www.manim.community/). |
| **html-viewer** (`tools/html-viewer/`) | Interactive pages (Astro + MDX): math, diagrams, interactive plots, quizzes, flashcards, embedded videos. Opened at `http://localhost:4321`. |

Each tool has a skill in `.agents/skills/` that tells the AI exactly how to use it.

## Requirements

Nothing to install by hand. The first time a tool needs something (Python via uv, LaTeX, Node.js...), the AI asks once and installs it for you on macOS, Linux or Windows.

What gets installed, for reference:
- **Videos**: [uv](https://docs.astral.sh/uv/) (Python 3.12 + Manim), LaTeX (TinyTeX if none is present).
- **Pages**: Node.js LTS + npm packages, and Chromium (Playwright) for the AI's visual checks if it has no browser of its own.

## Project structure

```
study-lab/
├── AGENTS.md            # instructions for the AI (rules, tools, skills)
├── assets/              # your course material (source of truth)
├── tools/
│   ├── memo/            # AI memory (knowledge entries + INDEX.md)
│   ├── manim-video/     # video toolkit + studio/ (one folder per video)
│   └── html-viewer/     # page toolkit + studio/ (one folder per page)
└── .agents/skills/      # one skill per tool
```

## Your data and git

Your courses (`assets/`), the memo, and the generated videos and pages (`studio/`) are git-ignored, so you never push your material by accident and you can still pull updates of the skeleton. Remove the matching lines in `.gitignore` if you want to version them in your own repository.

## Working on the skeleton

Everything in the skeleton (code, skills, docs) is written in English.

- `AGENTS.md`: global rules and the list of skills.
- `.agents/skills/<tool>/SKILL.md`: how the AI uses each tool.
- `tools/manim-video/README.md`, `tools/html-viewer/README.md`: toolkit details and commands.
- Smoke tests: `uv run python -m studylab_manim.render examples/demo.py` (in `tools/manim-video/`) and the `/demo` page with `npm run shoot -- demo` (in `tools/html-viewer/`).
