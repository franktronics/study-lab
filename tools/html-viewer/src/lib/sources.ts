import { fileUrl } from "./files";

/** Parse a memo-style reference ("assets/vl-05.pdf, p. 12–14") into a label and a link (if it is a project file). */
export function parseSource(ref: string): { label: string; href?: string } {
  const match = ref.match(/^((?:assets|tools)\/[^,]+?)\s*(?:,\s*(.*))?$/);
  if (!match) return { label: ref };
  const [, path, rest] = match;
  const page = rest?.match(/(?:p\.|S\.|page|slide)\s*(\d+)/i)?.[1];
  return { label: ref, href: fileUrl(path, page ? Number(page) : undefined) };
}
