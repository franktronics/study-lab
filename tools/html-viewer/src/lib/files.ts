/**
 * URL for a file of the study project, given its path relative to the project root
 * (e.g. "assets/vl-05.pdf" or "tools/manim-video/studio/<id>/<id>.mp4").
 * Served by the dev server under /files/ without copying.
 */
export function fileUrl(projectPath: string, page?: number): string {
  const clean = projectPath.replace(/^\.?\//, "");
  const url = "/files/" + clean.split("/").map(encodeURIComponent).join("/");
  return page ? `${url}#page=${page}` : url;
}

/** Parse "1:42" / "01:02:03" / 102 into seconds. */
export function toSeconds(t: string | number): number {
  if (typeof t === "number") return t;
  return t.split(":").reduce((acc, part) => acc * 60 + Number(part), 0);
}
