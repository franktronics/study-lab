/** Read a design token (CSS variable) at runtime, e.g. token("primary"). For canvas/SVG libs. */
export function token(name: string): string {
  if (typeof window === "undefined") return "";
  return getComputedStyle(document.documentElement).getPropertyValue(`--${name}`).trim();
}

/** Calls fn now and whenever the light/dark theme changes. Returns an unsubscribe function. */
export function onThemeChange(fn: (dark: boolean) => void): () => void {
  const root = document.documentElement;
  fn(root.classList.contains("dark"));
  const observer = new MutationObserver(() => fn(root.classList.contains("dark")));
  observer.observe(root, { attributes: true, attributeFilter: ["class"] });
  return () => observer.disconnect();
}
