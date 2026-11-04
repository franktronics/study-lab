// Screenshots for visual self-check (fallback when the agent has no browser tool of its own):
//   npm run shoot -- <page-id> [--width 1280]
// Uses the running dev server, or starts one in the background and stops it afterwards.
// Captures the page in light and dark mode (viewport-sized slices) and prints browser errors.
// Output: .cache/shots/<id>-<theme>-<n>.png
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const TOOL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ASTRO = path.join(TOOL_ROOT, "node_modules", "astro", "bin", "astro.mjs");
const args = process.argv.slice(2);
const id = args.find((a) => !a.startsWith("--"));
const width = Number(args[args.indexOf("--width") + 1]) || 1280;
const HEIGHT = 900;

if (!id) {
  console.error("Usage: npm run shoot -- <page-id> [--width 1280]");
  process.exit(1);
}

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  console.error("Playwright missing: run `npm install`.");
  process.exit(1);
}

const astro = (...a) => execFileSync(process.execPath, [ASTRO, "dev", ...a], { cwd: TOOL_ROOT, encoding: "utf8" });
const serverUrl = () => {
  try {
    const out = astro("status");
    return /running/i.test(out) ? out.match(/http:\/\/[\w.]+:\d+/)?.[0] : undefined;
  } catch {
    return undefined;
  }
};

let base = serverUrl();
const startedHere = !base;
if (startedHere) {
  astro("--background");
  base = serverUrl();
}

try {
  if (!base) throw new Error("Dev server did not start. See `npm run server:status` / `npx astro dev logs`.");
  const outDir = path.join(TOOL_ROOT, ".cache", "shots");
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(outDir, { recursive: true });

  let browser;
  try {
    browser = await chromium.launch();
  } catch {
    throw new Error("Chromium missing: run `npx playwright install chromium`.");
  }
  for (const theme of ["light", "dark"]) {
    const page = await browser.newPage({ viewport: { width, height: HEIGHT }, colorScheme: theme });
    page.on("console", (m) => m.type() === "error" && console.log(`CONSOLE_ERROR [${theme}] ${m.text()}`));
    page.on("pageerror", (e) => console.log(`PAGE_ERROR [${theme}] ${e.message}`));
    const res = await page.goto(`${base}/${id}`, { waitUntil: "networkidle" });
    if (!res?.ok()) throw new Error(`HTTP ${res?.status()} for /${id}`);
    // Scroll through so client:visible islands hydrate, then wait for lazy libraries (Plotly, Mermaid).
    const total = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < total; y += HEIGHT / 2) {
      await page.evaluate((v) => scrollTo(0, v), y);
      await page.waitForTimeout(150);
    }
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(2500);
    await page.evaluate(() => scrollTo(0, 0));
    const fullHeight = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let i = 0, y = 0; y < fullHeight; i++, y += HEIGHT) {
      const file = path.join(outDir, `${id}-${theme}-${String(i + 1).padStart(2, "0")}.png`);
      await page.screenshot({ path: file, fullPage: true, clip: { x: 0, y, width, height: Math.min(HEIGHT, fullHeight - y) } });
      console.log(`SHOT ${file}`);
    }
    await page.close();
  }
  await browser.close();
} catch (err) {
  console.error(String(err.message ?? err));
  process.exitCode = 1;
} finally {
  if (startedHere) astro("stop");
}
