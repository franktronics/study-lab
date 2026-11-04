import katex from "katex";

/** Renders a string with inline `$...$` math (for props of React components). */
export function MathText({ text, className }: { text: string; className?: string }) {
  const parts = text.split(/(\$[^$]+\$)/g);
  return (
    <span className={className}>
      {parts.map((part, i) =>
        part.startsWith("$") && part.endsWith("$") && part.length > 2 ? (
          <span
            key={i}
            dangerouslySetInnerHTML={{ __html: katex.renderToString(part.slice(1, -1), { throwOnError: false }) }}
          />
        ) : (
          <span key={i}>{part}</span>
        ),
      )}
    </span>
  );
}
