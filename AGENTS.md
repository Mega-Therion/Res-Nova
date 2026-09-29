# AGENTS.md — Base44 Dev Environment

## What this is

Res-Nova is a scientific research repository (physics manuscript, Lean formalization,
Python reproducibility scripts). The only web-servable component is `visualizer/` — a
single static `index.html` (~2300 lines) with embedded CSS/JS that loads Three.js,
Chart.js, and KaTeX from CDNs. No build step, no backend, no database.

## Running the preview

```
docker compose -f docker-compose.base44.yml up -d
```

nginx:alpine serves `visualizer/` on host port 3000. The source is bind-mounted
read-only, so edits to `visualizer/index.html` appear after a browser refresh
(call `reload_preview` since there is no live-reload dev server).

## Key details

- `visualizer/vercel.json` sets `X-Frame-Options: DENY` for production on Vercel;
  the Base44 nginx config overrides this to `ALLOWALL` so the page can render in the
  preview iframe.
- `visualizer/package.json` only has Vercel analytics deps — not needed locally.
- No secrets or external credentials are required; all libraries load from CDNs
  client-side.
