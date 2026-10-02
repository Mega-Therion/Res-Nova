# Base44 Dev Environment

## What this app is
Res-Nova is a scientific manuscript/reproducibility repository. The only web-servable component is `visualizer/` — a single self-contained `index.html` static page using CDN-loaded Three.js, Chart.js, and KaTeX. No backend, no API, no build step.

## Running it
```
docker compose -f docker-compose.base44.yml up -d
```
Serves `visualizer/` via nginx:alpine on host port 3000.

## Editing
Edits to `visualizer/index.html` are immediately live (bind-mounted, no rebuild). Call `reload_preview` after changes so the preview iframe refreshes.

## No secrets required
The visualizer is fully client-side with CDN dependencies. No external credentials needed.
