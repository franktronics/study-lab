# Study Lab

A study environment for **one subject**. The student puts their course material in `assets/` and works with you through conversation. You use the tools in `tools/` and the skills in `.agents/skills/` to help them understand, revise, and prepare for exams.

## Layout

| Path | Purpose |
|------|---------|
| `assets/` | Course material (PDFs, slides, notes, exercises…), organized freely by the student. **Source of truth.** Explore it to learn its structure. |
| `tools/memo/` | Your working memory: pointers and context to rebuild explanations. See the `memo` skill. |
| `tools/manim-video/` | Explanation videos with Manim Community. *(coming)* |
| `tools/html-viewer/` | Interactive explanation pages. *(coming)* |
| `.agents/skills/` | One skill per tool, defining how to use it. |

## General rules

### Sources
- The course assets are the source of truth. Base explanations on them and cite them (file + page/slide/timestamp) when relevant.
- If something is not covered by the assets, say so rather than presenting it as course content.

### Language
- **Responses to the user** (chat, generated pages, videos): the language of the user's question, unless they explicitly ask for another language.
- **Memo content**: the language of the knowledge itself (its source asset), regardless of the language the user is speaking. See the `memo` skill.

## Skills

Each tool has a skill defining how to use it. **Before using a tool, read its skill file.**

- [memo](.agents/skills/memo/SKILL.md) — save, update, remove, and recall knowledge in `tools/memo/`; build deliverables from it.

## Tools

### memo
Long-term memory of knowledge the student asked to keep. Write to it **only on request** (or when registering a generated video/page). Checking it before re-explaining a topic is recommended. Deliverables built from it (Formelsammlung, cheat sheets…) are never stored in it. Full rules: `.agents/skills/memo/SKILL.md`.
