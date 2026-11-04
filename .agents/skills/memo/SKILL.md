---
name: memo
description: Manage the study memo in tools/memo/ — the AI's long-term working memory of knowledge the student asked to keep (exam-relevant points, specific explanations, generated videos/pages). Use when the user asks to save, add, remember, update, or remove something in the memo; when manim-video or html-viewer produce an output that must be registered; and (recommended) before re-explaining a course topic, to check whether a saved explanation or reference already exists. Also use when building deliverables (e.g. a Formelsammlung, cheat sheet, revision summary) from previously saved knowledge.
---

# Memo

`tools/memo/` is the AI's working memory for this subject. It stores **pointers and context**, not course content: each entry holds just enough to rebuild an explanation later from the course assets. The student is not expected to ever read it.

## Core principles

1. **Assets are the source of truth.** The course material in `assets/` always wins. The memo is for reusing knowledge and reproducing an explanation the way it was given before. If a memo entry contradicts the assets, trust the assets, tell the user, and offer to fix the entry.
2. **Point, don't copy.** No transcribed lecture text, no full derivations, no long formula lists. If it is in the assets, reference it precisely. Keep only what the assets cannot give back: why it matters, what the student struggled with, how it was explained.
3. **Write only on request.** Never add to the memo on your own initiative. The only exception: when the manim-video or html-viewer tools generate an output, register it in the memo (see [Generated outputs](#generated-outputs)).
4. **Deliverables are not memo.** A Formelsammlung, cheat sheet, or summary the user asks for is *built from* the memo and the assets, but is never stored in `tools/memo/`.

## Structure

```
tools/memo/
├── README.md              # short description, do not edit
├── INDEX.md               # catalogue of every topic and file (create if missing)
└── <topic>/               # one folder per topic, kebab-case, English, stable name
    ├── <concept>.md       # one file per piece of knowledge / sub-concept
    └── <other-concept>.md
```

- **Folder = topic** (e.g. `laplace-transform/`). **File = one knowledge item or sub-concept** (e.g. `region-of-convergence.md`).
- Names are kebab-case English, describe the subject, and do not change when the content does. No dates or chapter numbers in names — those go in the frontmatter.
- The memo is flat: one subject per project, no subject level.

## INDEX.md

Always read `INDEX.md` first instead of opening every file. Update it on **every** create, rename, or delete. If it does not exist, create it.

Format:

```markdown
# Memo index

## laplace-transform
- `region-of-convergence.md` — ROC determines causality/stability; exam trap on two-sided signals — laplace, stability, exam
- `inverse-by-partial-fractions.md` — step order the student found clearest — laplace, method

## fourier-series
- `gibbs-phenomenon.md` — overshoot at discontinuities; linked manim video — fourier, video
```

One line per file: `` `file.md` — one-line summary — tags ``. Sections sorted alphabetically by topic.

## Knowledge file template

```markdown
---
title: Region of convergence
topic: laplace-transform
tags: [laplace, stability, exam]
language: de
created: 2026-11-04
updated: 2026-11-04
---

## Key points
- 2–6 short bullets: what matters and why it was saved (e.g. "explicitly marked as exam-relevant").

## Context
Where it came up, what the student was struggling with or found important.

## Explanation approach
Optional. Only when a specific way of explaining was used and should be reproduced:
the analogy, the order of steps, the example chosen, the linked video/page.

## References
- assets/lectures/vl-05.pdf, p. 12–14
- assets/exercises/ue-03.pdf, task 2b
- tools/manim-video/studio/<id>/... @ 01:42
```

Rules:
- `References` is **mandatory** and must be precise (file + page / slide / task / timestamp). Paths are relative to the project root.
- Reference formats:
  - Document: `assets/<path>, p. 12–14` · `, slide 7` · `, task 2b` · `, section 3.4`
  - Video or audio: `<path> @ mm:ss` (or a range `@ 01:42–02:30`)
  - Generated page: `tools/html-viewer/studio/<id>/<file>` (+ `#section` if relevant)
  - Other memo entry: relative link, e.g. `[ROC](../laplace-transform/region-of-convergence.md)`
  - No source in the assets: `conversation, YYYY-MM-DD` — say so explicitly, never invent a page number.
- `Explanation approach` and any extra section (e.g. `Pitfalls`, `Example`) are optional; drop them when empty.
- Dates are ISO `YYYY-MM-DD`; bump `updated` on every change.

## Language

- Write the entry in the **language of the knowledge**: the language of its main source asset (a German lecture → German entry), regardless of the language the user is speaking.
- If the knowledge has no source in the assets (born in conversation), use the language of the conversation where it was created.
- Record it in the frontmatter `language` field (ISO 639-1 code).
- Folder names, file names, frontmatter keys, and section headings stay in English.

## Workflows

### Add knowledge

1. Identify exactly what the user wants kept. If ambiguous, ask a short clarifying question.
2. Locate the precise sources (open the asset if needed to get page numbers / timestamps).
3. Read `INDEX.md` and decide placement:
   - **Same sub-concept** already has a file → merge into that file (edit sections, do not just append duplicates).
   - **Same topic**, different sub-concept → new file in that topic folder.
   - **No matching topic** → new topic folder + file.
4. Write the entry following the template. Keep it short.
5. Update `INDEX.md`.
6. Tell the user in one or two lines where it was saved (topic/file) and what was recorded.

### Update knowledge

1. Find the entry via `INDEX.md`.
2. Apply the change, bump `updated`, keep references accurate.
3. If the summary or tags change, update `INDEX.md`.
4. Briefly report what changed.

### Remove knowledge

- Asking for confirmation is recommended, especially for whole folders or several entries.
- A light removal with a clear reason (the user asked for that specific point to go, or it is obviously wrong/duplicated) can be done directly.
- Remove the line(s) from `INDEX.md`; delete the topic folder and its INDEX section when it becomes empty.
- Fix or remove links from other entries that pointed to the deleted file.

### Use the memo (recall)

Recommended, not mandatory, before explaining a course topic:
1. Scan `INDEX.md` for the topic.
2. If an entry exists, use its references to go back to the assets, and reproduce the `Explanation approach` if one was recorded.
3. Answer from the assets; the memo guides, it does not replace them.

### Build a deliverable from the memo

When the user asks for a Formelsammlung, cheat sheet, revision summary, etc.:
1. Select the relevant entries via `INDEX.md` (filter by topic / tags).
2. Pull the actual content from the assets through the references.
3. Produce the deliverable in the user's language (chat, html-viewer page, file they asked for) — **outside** `tools/memo/`.

### Generated outputs

When manim-video or html-viewer generate an output, register it automatically:
1. Find (or create) the knowledge file for the concept the output explains.
2. Add a reference to the output in `References` (path, plus key timestamps or sections) and, if useful, a line in `Explanation approach` describing what the output shows.
3. Never copy the output file into `tools/memo/` — link to it where it lives in `studio/`.
4. Update `INDEX.md` (add tag `video` or `page`).
