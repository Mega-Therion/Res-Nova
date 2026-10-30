# Res Nova Research Atlas (web app)

Source for the Res Nova Research Atlas: an interactive hub covering the program's theory, evidence,
figures and publications. It was merged into Res-Nova on 2026-10-03 from the former
`Mega-Therion/res-nova-research-hub` repository (snapshot of `master` at `b364790`). That repository
is archived with its history intact.

The Atlas presents the corpus; it is not a source of physics claims. Where it and
[`../CURRENT_STATE_READ_THIS_FIRST.md`](../CURRENT_STATE_READ_THIS_FIRST.md) disagree, the
current-state file wins.

The  only  Res Nova  web  project on  Vercel  is  `res-nova-atlas` (https://res-nova-atlas.vercel.app).  The observatory is the static `visualizer/` tree, copied into this build at `/observatory/` by `scripts/mount-observatory.mjs`. Do not deploy `visualizer/` as its own Vercel project.

## Run locally

Node 20+ and pnpm:

```bash
cd research-hub
pnpm install
pnpm dev        # development server
pnpm test       # vitest
pnpm check      # TypeScript type check
pnpm build && pnpm start   # production build
```

The server reads its configuration (database URL and similar) from environment variables; see
`server/_core/`. No secrets are committed.
