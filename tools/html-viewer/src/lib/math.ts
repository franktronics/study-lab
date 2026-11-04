import katex from "katex";

/** Server-side: render a string with inline `$...$` math to HTML (for Astro component props). */
export function mathTextHtml(text: string): string {
  const escape = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return text
    .split(/(\$[^$]+\$)/g)
    .map((part) =>
      part.length > 2 && part.startsWith("$") && part.endsWith("$")
        ? katex.renderToString(part.slice(1, -1), { throwOnError: false })
        : escape(part),
    )
    .join("");
}
