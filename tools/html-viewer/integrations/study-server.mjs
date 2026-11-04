import path from "node:path";
import { fileURLToPath } from "node:url";
import sirv from "sirv";

const TOOL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const PROJECT_ROOT = path.resolve(TOOL_ROOT, "../..");

// Project folders that pages may link to through /files/<path>.
const ALLOWED = ["assets/", "tools/"];

/**
 * Dev-server additions:
 * - /files/<project-relative path> serves course assets and other tools' outputs (no copy, range requests for video).
 * - Shuts the server down after STUDYLAB_IDLE_MINUTES (default 30) without any request.
 */
export function studyServer() {
  return {
    name: "study-server",
    hooks: {
      "astro:server:setup": ({ server }) => {
        const files = sirv(PROJECT_ROOT, { dev: true, dotfiles: false });
        let lastRequest = Date.now();

        server.middlewares.use((req, res, next) => {
          lastRequest = Date.now();
          if (!req.url?.startsWith("/files/")) return next();
          const rel = decodeURIComponent(req.url.slice("/files/".length).split(/[?#]/)[0]);
          if (!ALLOWED.some((p) => rel.startsWith(p)) || rel.includes("..")) {
            res.statusCode = 403;
            return res.end("Forbidden");
          }
          req.url = "/" + req.url.slice("/files/".length);
          files(req, res, () => {
            res.statusCode = 404;
            res.end("Not found");
          });
        });

        const idleMinutes = Number(process.env.STUDYLAB_IDLE_MINUTES ?? 30);
        if (idleMinutes > 0) {
          const timer = setInterval(() => {
            if (Date.now() - lastRequest > idleMinutes * 60_000) {
              console.log(`[study-server] idle for ${idleMinutes} min, shutting down.`);
              clearInterval(timer);
              process.exit(0);
            }
          }, 60_000);
          timer.unref();
        }
      },
    },
  };
}
