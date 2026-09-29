# Base44 development notes

- The browser app is `visualizer/index.html`; the rest of the repository is primarily a research corpus and reproducibility scripts, not an API. Preview uses the `visualizer` Vite dev server on port 3000 via `docker-compose.base44.yml`.
- The page loads Three.js, Chart.js, KaTeX, and Google Fonts from public CDNs; it needs browser access to those hosts to render fully. It does not require external API credentials or a local database.
- `/_vercel/insights/script.js` and `/_vercel/speed-insights/script.js` are Vercel-only analytics endpoints; they are absent in the local preview but do not block the visualizer.
- Verify with `docker compose -f docker-compose.base44.yml ps` and `curl -f http://localhost:3000/`; the served HTML should include `/@vite/client` and `RES-NOVA OBSERVATORY`.
