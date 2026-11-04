// Create a new studio page: npm run new -- <slug> [language]
//   -> studio/YYYY-MM-DD-<slug>/page.mdx
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const TOOL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [slug, language = "en"] = process.argv.slice(2);

if (!slug || !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) {
  console.error("Usage: npm run new -- <kebab-case-slug> [language]");
  process.exit(1);
}
const date = new Date().toISOString().slice(0, 10);
const id = `${date}-${slug}`;
const dir = path.join(TOOL_ROOT, "studio", id);
if (fs.existsSync(dir)) {
  console.error(`Already exists: ${dir}`);
  process.exit(1);
}
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(
  path.join(dir, "page.mdx"),
  `---
title: Title
description: One sentence on what this page explains
date: ${date}
language: ${language}
tags: []
sources: []
# memo: tools/memo/<topic>/<file>.md
---

## Section

Text with inline math $e^{i\\pi} + 1 = 0$.
`,
);
console.log(`CREATED ${dir}`);
console.log(`URL http://localhost:4321/${id}`);
