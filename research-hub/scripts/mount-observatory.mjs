#!/usr/bin/env node
// Copy the static observatory next to the atlas client so one Vercel build serves both.
import { cpSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const hub = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const visualizer = path.resolve(hub, "../visualizer");
const dest = path.join(hub, "client/public/observatory");
const files = [
  "index.html",
  "claims.json",
  "lean_modules.json",
  "evidence-atlas-lifecycle.svg",
];

rmSync(dest, { recursive: true, force: true });
mkdirSync(dest, { recursive: true });
for (const name of files) {
  cpSync(path.join(visualizer, name), path.join(dest, name));
}
console.log(`mount-observatory: wrote ${dest}`);
