import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { createReadStream } from "node:fs";
import { extname, join, normalize, relative, resolve } from "node:path";

const root = resolve(process.env.DOCS_SITE_ROOT || "/workspace/mintlify");
const port = Number(process.env.DOCS_SITE_PORT || "3000");
const host = process.env.DOCS_SITE_HOST || "0.0.0.0";

const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
  ".mdx": "text/markdown; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
};

function safePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?")[0] || "/");
  const normalized = normalize(decoded).replace(/^(\.\.(\/|\\|$))+/, "");
  const target = resolve(join(root, normalized));
  return relative(root, target).startsWith("..") ? root : target;
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[char]);
}

async function renderIndex() {
  const manifest = await readFile(join(root, "site-manifest.json"), "utf8").catch(() => "{}");
  const mint = await readFile(join(root, "mint.json"), "utf8").catch(() => "{}");
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Docs Preview</title>
  <style>
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #101418; color: #f5f1e8; }
    main { max-width: 960px; margin: 0 auto; padding: 40px 20px; }
    a { color: #d8b56d; }
    pre { overflow: auto; padding: 16px; background: #171d22; border: 1px solid #333c44; border-radius: 8px; }
    .grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin: 24px 0; }
    .card { border: 1px solid #333c44; border-radius: 8px; padding: 16px; background: #151a1f; }
  </style>
</head>
<body>
  <main>
    <h1>Docs Preview</h1>
    <p>Mintlify source is mounted and reachable. Use the links below to inspect generated docs and release pages.</p>
    <div class="grid">
      <section class="card"><h2>Docs</h2><p><a href="/docs/">/docs/</a></p></section>
      <section class="card"><h2>Releases</h2><p><a href="/releases/">/releases/</a></p></section>
      <section class="card"><h2>Assets</h2><p><a href="/assets/">/assets/</a></p></section>
    </div>
    <h2>site-manifest.json</h2>
    <pre>${escapeHtml(manifest)}</pre>
    <h2>mint.json</h2>
    <pre>${escapeHtml(mint)}</pre>
  </main>
</body>
</html>`;
}

async function renderDirectory(path, urlPath) {
  const { readdir } = await import("node:fs/promises");
  const entries = (await readdir(path, { withFileTypes: true }))
    .filter((entry) => !entry.name.startsWith("."))
    .sort((a, b) => Number(b.isDirectory()) - Number(a.isDirectory()) || a.name.localeCompare(b.name));
  const links = entries.map((entry) => {
    const href = `${urlPath.replace(/\/$/, "")}/${encodeURIComponent(entry.name)}${entry.isDirectory() ? "/" : ""}`;
    return `<li><a href="${href}">${escapeHtml(entry.name)}${entry.isDirectory() ? "/" : ""}</a></li>`;
  }).join("\n");
  return `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(urlPath)}</title><body><main><h1>${escapeHtml(urlPath)}</h1><ul>${links}</ul><p><a href="/">Back home</a></p></main></body></html>`;
}

createServer(async (request, response) => {
  try {
    const urlPath = new URL(request.url || "/", `http://${request.headers.host}`).pathname;
    if (urlPath === "/") {
      response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      response.end(await renderIndex());
      return;
    }

    const target = safePath(urlPath);
    const info = await stat(target);
    if (info.isDirectory()) {
      response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      response.end(await renderDirectory(target, urlPath));
      return;
    }

    response.writeHead(200, { "content-type": contentTypes[extname(target)] || "application/octet-stream" });
    createReadStream(target).pipe(response);
  } catch (error) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end(`Not found\n${error.message}\n`);
  }
}).listen(port, host, () => {
  console.log(`Docs preview listening on http://${host}:${port}`);
  console.log(`Serving ${root}`);
});
