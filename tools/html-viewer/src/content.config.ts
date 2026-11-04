import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

/** Every studio/<id>/page.mdx (and examples/<id>/page.mdx) becomes a page at /<id>. */
const pages = defineCollection({
  loader: glob({
    base: ".",
    pattern: ["studio/*/page.mdx", "examples/*/page.mdx"],
    generateId: ({ entry }) => entry.split("/")[1],
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    language: z.string().min(2),
    tags: z.array(z.string()).default([]),
    sources: z.array(z.string()).default([]),
    memo: z.string().optional(),
  }),
});

export const collections = { pages };
