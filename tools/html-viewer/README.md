# html-viewer

Interactive explanation pages (Astro + React + MDX + Tailwind v4 + shadcn/ui). The base (layout, design tokens, study components, file serving) is fixed; each page lives in its own `studio/YYYY-MM-DD-<slug>/page.mdx`.

Used through the `html-viewer` skill (`.agents/skills/html-viewer/SKILL.md`).

```
html-viewer/
├── astro.config.mjs            # MDX + KaTeX + Mermaid + React + Tailwind
├── integrations/
│   ├── study-server.mjs        # /files/... (project files, no copy) + idle shutdown
│   └── remark-mermaid.mjs      # ```mermaid blocks -> client-side diagrams
├── src/
│   ├── content.config.ts       # page collection + frontmatter schema
│   ├── pages/                  # / (index of pages) and /<id>
│   ├── layouts/BaseLayout.astro
│   ├── styles/global.css       # design tokens (same palette as manim-video)
│   ├── components/ui/          # shadcn/ui
│   ├── components/study/       # study components available in every page
│   └── lib/                    # helpers (files, i18n, math, theme)
├── scripts/
│   ├── new.mjs                 # scaffold a studio page
│   └── shoot.mjs               # screenshots for visual checks (Playwright)
├── examples/demo/page.mdx      # reference page using every component (/demo)
└── studio/                     # generated pages (git-ignored)
```

Commands (from this folder):

```sh
npm install
npm run new -- <slug> [language]   # studio/YYYY-MM-DD-<slug>/page.mdx
npm run check                      # types + MDX
npm run build                      # full build (catches render errors)
npm run server:start               # background server on http://localhost:4321
npm run server:status
npm run server:stop
npm run shoot -- <id>              # screenshots in .cache/shots/
```

The server stops by itself after 30 minutes without requests (`STUDYLAB_IDLE_MINUTES`).
