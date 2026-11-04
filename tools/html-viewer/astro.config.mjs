// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import react from "@astrojs/react";
import { unified } from "@astrojs/markdown-remark";
import tailwindcss from "@tailwindcss/vite";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { remarkMermaid } from "./integrations/remark-mermaid.mjs";
import { studyServer } from "./integrations/study-server.mjs";

export default defineConfig({
  server: { port: 4321, host: "localhost" },
  devToolbar: { enabled: false },
  integrations: [
    react(),
    mdx(),
    studyServer(),
  ],
  markdown: {
    // unified (remark/rehype) pipeline: math (KaTeX) and ```mermaid blocks.
    processor: unified({ remarkPlugins: [remarkMath, remarkMermaid], rehypePlugins: [rehypeKatex] }),
    shikiConfig: { themes: { light: "github-light", dark: "github-dark" } },
  },
  vite: {
    plugins: [tailwindcss()],
    server: { fs: { allow: ["../.."] } },
    // Plotly and Mermaid are large but loaded only on pages that use them.
    build: { chunkSizeWarningLimit: 5000 },
  },
});
