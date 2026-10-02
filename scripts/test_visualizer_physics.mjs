#!/usr/bin/env node
// Test the physics the public visualizer actually runs.
//
// Until 2026-09-30 visualizer/index.html computed every rotation curve with the
// inversion of the falsified mu_dual(x) = x/(1+x), with a hand-tuned a0 unit
// constant (3800 instead of 308.57 per 1e-11 m/s^2) and the superseded
// a0 = 9.433e-11. Nothing tested it, because the gate only read prose. This
// extracts the functions from the page itself -- not a copy -- and checks them.
//
//   node scripts/test_visualizer_physics.mjs
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(root, "visualizer/index.html"), "utf8");
let failed = 0;
const check = (ok, msg) => { console.log(`  ${ok ? "ok  " : "FAIL"}  ${msg}`); if (!ok) failed++; };

// 1. Every inline script must at least compile.
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
scripts.forEach((code, i) => {
  try { new vm.Script(code, { filename: `inline-script-${i}` }); check(true, `inline script ${i} compiles`); }
  catch (e) { check(false, `inline script ${i} compiles: ${e.message}`); }
});

// 1b. No attribute value may start with an escaped quote (onclick=\"...\" breaks the
//     element: this happened to all six ledger filter buttons during the 2026-09-30 rewrite).
const badAttr = html.match(/=\\"/g);
check(!badAttr, `no backslash-escaped attribute quotes (${badAttr ? badAttr.length : 0} found)`);

// 2. Pull the live physics out of the page.
const unitSrc = html.match(/const A0_UNIT = [^;]+;/);
const fnSrc = html.match(/function muStdInvert\(gBar, a0\) \{[\s\S]*?\n    \}/);
check(Boolean(unitSrc && fnSrc), "A0_UNIT and muStdInvert found in index.html");
if (!unitSrc || !fnSrc) process.exit(1);
const ctx = {};
vm.runInNewContext(`${unitSrc[0]}\n${fnSrc[0]}\nthis.A0_UNIT = A0_UNIT; this.muStdInvert = muStdInvert;`, ctx);
const { A0_UNIT, muStdInvert } = ctx;

// 3. Units: 1e-11 m/s^2 in (km/s)^2/kpc, parsec = 3.0856775814913673e16 m (IAU).
const expectUnit = 1e-11 * 3.0856775814913673e19 / 1e6;
check(Math.abs(A0_UNIT - expectUnit) / expectUnit < 1e-12, `A0_UNIT = ${A0_UNIT} (expected ${expectUnit})`);

// 4. It solves the live field equation mu_std(g/a0) * g = g_bar.
const muStd = x => x / Math.sqrt(1 + x * x);
let worst = 0;
for (let k = -6; k <= 6; k += 0.25) {
  const a0 = 1.0, gBar = Math.pow(10, k), g = muStdInvert(gBar, a0);
  worst = Math.max(worst, Math.abs(muStd(g / a0) * g - gBar) / gBar);
}
check(worst < 1e-9, `mu_std(g/a0) g = g_bar over 12 decades (worst rel. residual ${worst.toExponential(2)})`);

// 5. Against an independent 30-digit mpmath solve (y = g_bar/a0 -> g/a0).
const ref = [[1e-4, 0.010000250003124921873], [0.3, 0.59021710094028135139],
             [1, 1.2720196495140689643], [4.2, 4.3114905559069622139], [1e4, 10000.000049999999375]];
for (const [y, gy] of ref) {
  const got = muStdInvert(y, 1);
  check(Math.abs(got - gy) / gy < 1e-12, `y = ${y}: g/a0 = ${got} (mpmath ${gy})`);
}

// 6. Limits: Newtonian (g -> g_bar) and deep-MOND (g -> sqrt(g_bar a0)).
check(Math.abs(muStdInvert(1e8, 1) / 1e8 - 1) < 1e-12, "Newtonian limit g -> g_bar");
check(Math.abs(muStdInvert(1e-8, 1) / Math.sqrt(1e-8) - 1) < 1e-3, "deep-MOND limit g -> sqrt(g_bar a0)");

// 7. It is not mu_dual: at y = 1, mu_dual gives g/a0 = (1+sqrt 5)/2.
check(Math.abs(muStdInvert(1, 1) - (1 + Math.sqrt(5)) / 2) > 0.3, "differs from the retired mu_dual inversion");

// 8. Default a0 is the live mu_std extraction, not the superseded 9.433e-11.
check(/id="sparcA0Input"[^>]*value="11\.6"/.test(html) && /id="simA0Slider"[^>]*value="11\.6"/.test(html),
      "a0 sliders default to 11.6e-11 (live value 1.1607e-10)");
check(!/9\.433/.test(html), "superseded a0 = 9.433e-11 appears nowhere");

console.log(failed ? `visualizer physics: FAIL (${failed})` : "visualizer physics: PASS");
process.exit(failed ? 1 : 0);
