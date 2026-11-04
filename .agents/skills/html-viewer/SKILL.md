---
name: html-viewer
description: Create or modify interactive explanation pages (Astro + MDX) in tools/html-viewer/ — concept explainers, chapter overviews, exercise trainers, and deliverables built from the memo (Formelsammlung, cheat sheets, revision summaries). Use when the user asks for a page, a visual or interactive explanation, a summary/cheat sheet to view or print, or when formulas, diagrams, interactive plots, quizzes or embedded videos would explain better than chat text. Handles installation, the studio folder per page, the local server, visual self-check, and memo registration.
---

# HTML viewer

Tool root: `tools/html-viewer/` (all commands below run from there). The base (layout, design tokens, study components, KaTeX, Mermaid, file serving) is fixed. For each page you write **one `page.mdx`** (markdown + components) and, only when needed, page-specific React components next to it.

## Talking to the user

The student is not necessarily technical. Never expose commands, stack traces, package names or logs. Talk about the page, not the tooling. Fix technical problems silently; only if truly blocked, explain in one plain sentence.

## 1. Setup (first use, or when something is missing)

```sh
node --version          # Node.js LTS (>= 20) available?
npm install             # dependencies (once, or after updates)
```

If Node.js is missing or `npm install` fails, ask **once**, simply: *"To create interactive pages I first need to install a few tools (a few minutes). Shall I do it?"* If yes, install **everything** yourself on whatever OS this is:

| | macOS | Linux (Debian/Ubuntu; adapt for others) | Windows (PowerShell) |
|---|---|---|---|
| Node.js LTS | `brew install node` (or the official installer from nodejs.org) | NodeSource LTS: `curl -fsSL https://deb.nodesource.com/setup_lts.x \| sudo -E bash - && sudo apt install -y nodejs` | `winget install OpenJS.NodeJS.LTS` |

Then `npm install`. Playwright's Chromium is only needed for screenshots (see 2.5): `npx playwright install chromium` (on Linux add `--with-deps`). If `sudo` needs a password, give the user that one command ready to paste.

## 2. Create a page

### 2.1 Scope and content
- A page can be: a concept explainer, a chapter overview, an exercise trainer, or a deliverable built from the memo (Formelsammlung, cheat sheet, revision summary).
- Content comes from the course assets (source of truth); check the memo (`tools/memo/INDEX.md`) for references and explanation approaches to reuse. For deliverables, follow the memo skill ("Build a deliverable").
- The page is written in the **user's language** (language of their request); set `language` accordingly.
- Prefer interaction where it teaches something (sliders that change a parameter, step-by-step reveals, self-tests), not decoration.

### 2.2 Scaffold
```sh
npm run new -- <slug> <language>     # -> studio/YYYY-MM-DD-<slug>/page.mdx
```
`<slug>`: kebab-case English (e.g. `laplace-roc`). URL: `http://localhost:4321/<id>`.

Frontmatter (validated at build, a missing field is an error):
```yaml
---
title: Region of convergence
description: Why the ROC decides causality and stability   # one sentence
date: 2026-11-04
language: fr
tags: [laplace, stability]
sources: ["assets/vl-05.pdf, p. 12–14"]     # memo-style references; project files become links
memo: tools/memo/laplace-transform/region-of-convergence.md   # optional
---
```
Do not repeat the title as `#` in the body; start with `##` sections.

### 2.3 Write `page.mdx`
Markdown, plus:
- **Math**: `$...$` inline, `$$...$$` display (KaTeX). In component props: a plain attribute keeps single backslashes (`front="$\\omega$"` is wrong, `front="$\omega$"` is right), but strings inside `{...}` are JavaScript and need doubled ones (`{ label: "$\\omega$" }`).
- **Diagrams**: a ```` ```mermaid ```` code block (flowchart, sequence, state, class, gantt...).
- **Code**: fenced code blocks with a language (highlighted, light/dark).
- **Study components**: available everywhere **without import**:

| Component | Use |
|---|---|
| `<Callout type="definition\|theorem\|note\|warning\|exam\|tip\|example" title="...">…</Callout>` | Highlighted block. `exam` for exam-relevant points. |
| `<Steps><Step title="...">…</Step>…</Steps>` | Step-by-step reveal (derivations, procedures). |
| `<Solution title="...">…</Solution>` | Hidden solution, click to open. |
| `<Tabs><Tab label="...">…</Tab>…</Tabs>` | Alternatives (methods, representations). |
| `<Quiz question="..." options={[{ text, correct?, explain? }]} explanation="..." />` | Self-test (several `correct` → multi-select). `$...$` math in strings. |
| `<Flashcards><Flashcard front="...">answer</Flashcard>…</Flashcards>` | Flip cards. |
| `<FunctionPlot functions={[{ expr, color?, label?, dashed? }]} params={{ a: { min, max, value, step?, label? } }} xRange yRange points height zoom />` | Interactive plot (Mafs). `expr` uses x and the params, mathjs syntax (`"a*sin(b*x)"`, `"x^2"`, `"exp(-x)"`, `"sign(x)"`, `pi`). |
| `<Plotly data={[...]} layout={{...}} height />` | Data charts, 3D surfaces, heatmaps (Plotly.js traces). Leave colors unset to use the theme. |
| `<Video src="tools/manim-video/studio/<id>/<id>.mp4" chapters={[{ t: "0:42", label }]} caption />` | Manim video, linked (never copied), clickable chapters. |
| `<Source file="assets/vl-05.pdf" page={12} />` | Link opening the course file at that page. |

`examples/demo/page.mdx` (`/demo`) is a complete working reference.

**Files of the project** (assets, videos of other tools) are linked, never copied: use project-root paths in `Video`/`Source`/`sources`; they are served under `/files/<path>`. For a raw link or image: `/files/assets/...`. Only files under `assets/` and `tools/` are served.

**Page-specific components** (only when no study component fits): put `MyWidget.tsx` in the page folder, then in the MDX:
```mdx
import MyWidget from "./MyWidget.tsx";

<MyWidget client:visible someProp={1} />
```
- `client:visible` is required for anything interactive.
- Build with shadcn/ui (`@/components/ui/*`: button, card, badge, tabs, accordion, slider, tooltip, separator; add others with `npx shadcn@latest add <name>`), `motion` for animation, `mafs`, `katex` / `MathText` from `@/lib/math-text`.
- **Design consistency**: colors only through the tokens (`bg-card`, `text-muted-foreground`, `border-border`, `text-primary`, `text-emphasis`, `bg-positive/10`...; in canvas/SVG code `var(--primary)` or `token("primary")` from `@/lib/theme`). Never hard-coded colors. Rounded `rounded-xl border bg-card` containers like the study components.

Token palette (same semantics as manim videos): `primary`, `violet`, `emphasis` (orange), `highlight` (yellow), `positive`, `negative`, plus shadcn's `background foreground card muted muted-foreground accent border`.

Print: interactive parts collapse to their static state and solutions open when printing; for print-oriented pages (Formelsammlung) keep content static and compact.

### 2.4 Check (mandatory)
```sh
npm run check     # types and MDX syntax
npm run build     # full render; catches errors in components, math, frontmatter
```
Fix every error. (`dist/` is a by-product, ignore it.)

### 2.5 Visual self-check (mandatory)
1. **If you have your own browser/page-viewing tool**, use it first: start the server (see 3), open the page, look at it in light and dark mode, scroll through it, try the interactive parts.
2. **Otherwise**: `npm run shoot -- <id>` (installs nothing; if Chromium is missing run `npx playwright install chromium` once). It prints `SHOT <png>` paths (light and dark, viewport slices) and any `CONSOLE_ERROR` / `PAGE_ERROR`. Open the PNGs and look at them.

Check: math rendered (no raw `$`, no red KaTeX errors), mermaid diagrams drawn, plots visible and readable, nothing overflowing or overlapping, both themes legible, correct language, content correct. Fix and re-check.

### 2.6 Register in the memo, then answer
1. Follow the `memo` skill, "Generated outputs": add `tools/html-viewer/studio/<id>/page.mdx` (+ relevant `#sections`) to the concept's entry, update `INDEX.md`, set `memo:` in the frontmatter. Deliverables built from the memo are registered the same way (they still live here, not in the memo).
2. Start the server (see 3) and give the user, in their language, a short description and the link `http://localhost:4321/<id>`. Mention they can print it to PDF from the browser when relevant.

## 3. Server

```sh
npm run server:status     # running?
npm run server:start      # background server, http://localhost:4321 (reuses a running one)
npm run server:stop
```
- One server serves every page (home `/` lists them all), with live reload while you edit.
- Stop it when the user says they are done, or at the end of the task/conversation when they no longer need it. It also stops itself after 30 minutes without any request.
- `npm run shoot` reuses a running server, or starts and stops its own.

## 4. Modify an existing page
Edit the same studio folder in place, re-run check + visual check. The URL stays the same, so memo references stay valid. A genuinely different page → new studio folder.

## 5. Extending the base
If a pattern repeats across pages (a widget type, a layout), turn it into a study component in `src/components/study/` (Astro for static parts; a React `*Island.tsx` + Astro wrapper with `client:visible` for interactive parts), register it in `src/components/study/index.ts`, add UI strings to `src/lib/i18n.ts` (en/fr/de; add the user's language if missing), add it to the table above and to `examples/demo/page.mdx`, then run check + build + shoot on `/demo`.

## Troubleshooting (internal, don't expose)
- MDX parse error `Could not parse expression`: a `{` or `<` in plain text is read as JSX. Put math inside `$...$`, escape literal braces (`\{`), or wrap code in backticks.
- Island not interactive: missing `client:visible` on a page-specific component.
- `/files/...` 403: the path must start with `assets/` or `tools/`; 404: wrong path.
- Port busy or stale server: `npm run server:stop`, then start again.
