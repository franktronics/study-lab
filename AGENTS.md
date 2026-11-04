# Study Lab

A study environment for **one subject**. The student puts their course material in `assets/` and works with you through conversation. You use the tools in `tools/` and the skills in `.agents/skills/` to help them understand, revise, and prepare for exams.

## Layout

| Path | Purpose |
|------|---------|
| `assets/` | Course material (PDFs, slides, notes, exercises…), organized freely by the student. **Source of truth.** Explore it to learn its structure. |
| `tools/memo/` | Your working memory: pointers and context to rebuild explanations. See the `memo` skill. |
| `tools/manim-video/` | Explanation videos with Manim Community. See the `manim-video` skill. |
| `tools/html-viewer/` | Interactive explanation pages (Astro + MDX). See the `html-viewer` skill. |
| `.agents/skills/` | One skill per tool, defining how to use it. |

## General rules

### Sources
- The course assets are the source of truth. Base explanations on them and cite them (file + page/slide/timestamp) when relevant.
- If something is not covered by the assets, say so rather than presenting it as course content.
- Explanations can be based on your own knowledge or even on information found on the internet, but assets remain the foundation and source of truth.

### Language
- **Responses to the user** (chat, generated pages, videos): the language of the user's question, unless they explicitly ask for another language.
- **Memo content**: the language of the knowledge itself (its source asset), regardless of the language the user is speaking. See the `memo` skill.

## Skills

Each tool has a skill defining how to use it. **Before using a tool, read its skill file.**

- [memo](.agents/skills/memo/SKILL.md) — save, update, remove, and recall knowledge in `tools/memo/`; build deliverables from it.
- [manim-video](.agents/skills/manim-video/SKILL.md) — create or modify explanation videos in `tools/manim-video/` (setup, studio folder, preview, final render, memo registration).
- [html-viewer](.agents/skills/html-viewer/SKILL.md) — create or modify interactive explanation pages and deliverables (Formelsammlung, cheat sheets) in `tools/html-viewer/` (setup, studio page, server, visual check, memo registration).

## Tools

### memo
Long-term memory of knowledge the student asked to keep. Write to it **only on request** (or when registering a generated video/page). Checking it before re-explaining a topic is recommended. Deliverables built from it (Formelsammlung, cheat sheets…) are never stored in it. Full rules: `.agents/skills/memo/SKILL.md`.

### manim-video
Short animated explanation videos (one concept, 30 s – 3 min, no audio, on-screen text in the user's language). Installs its own requirements on first use after asking the user. Every generated video is registered in the memo. Full rules: `.agents/skills/manim-video/SKILL.md`.

### html-viewer
Interactive pages (math, diagrams, interactive plots, quizzes, embedded videos) in the user's language, served locally at `http://localhost:4321`. Links to course files and videos, never copies them. Start the server to show a page; stop it when the user is done. Every generated page is registered in the memo. Full rules: `.agents/skills/html-viewer/SKILL.md`.
