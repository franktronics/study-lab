import { visit } from "unist-util-visit";

const escape = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** Turns ```mermaid code blocks into <div class="mermaid-diagram">, rendered client-side. */
export function remarkMermaid() {
  return (tree) => {
    visit(tree, "code", (node, index, parent) => {
      if (node.lang !== "mermaid" || !parent || index === undefined) return;
      parent.children[index] = {
        type: "html",
        value: `<div class="mermaid-diagram not-prose" data-source="${escape(node.value).replace(/"/g, "&quot;")}"></div>`,
      };
    });
  };
}
