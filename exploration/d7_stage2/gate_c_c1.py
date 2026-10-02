#!/usr/bin/env python3
"""D7 Stage 2, gate C: the steady state of the isolated dwarf at satellite speeds is GR-Newtonian in the Newton channel,
with a MOND remnant that falls as the box grows. Criterion fixed and committed BEFORE the first run (2026-09-28), after
exploratory runs (STRIPPED_HIGHV_*, BOX_SWEEP_*, ANALYSIS_*) suggested it:
  (a) Newton from the static held state converges at v = 100 and 300 km/s in every run;
  (b) in every run, the Newton channel <d_r Phihat> (Phihat = Psi - phi) at r = 0.1, 0.2, 0.3, 0.6 kpc is within 0.02 of
      (1 - K_B/2) = 0.75 times its static value (D3 section 34: the dragged branch is GR with G~, the held branch has
      G~/(1 - K_B/2));
  (c) the scalar remnant <d_r phi>_moving/<d_r phi>_static at r_h = 0.3 kpc is smaller in the 1 Mpc box than in the 100 kpc
      box (same element size near the dwarf);
  (d) plateau: g/g_static at r_h differs by < 0.02 (relative) between 100 and 300 km/s in every run.
Runs (isolated dwarf, g_e = 0, fixed element size near the dwarf, d xi = asinh(100)/16 or asinh(100)/21):
  box edge 100 kpc on 23x46 and 30x60; box edge 1 Mpc on 30x60 (a second 1 Mpc grid does not fit in memory).
Output: GATE_C_C1.json and a PASS/FAIL line."""

import json, math, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import observables

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
KB = 0.5
RADII = (0.1e-3, 0.2e-3, 0.3e-3, 0.6e-3)


def radial_parts(P, x):
    g = P.g
    q = (P.D @ x).reshape(g.ng, C.NQ)
    c = lambda n, k: q[:, 3 * C.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    rad = lambda n: (g.Rg * c(n, 1) + g.zg * c(n, 2)) / r
    gpsi, gphi = -0.5 * rad("S"), rad("F")
    out = {}
    for r0 in RADII:
        wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
        avg = lambda f: float(np.sum(f * wb) / np.sum(wb))
        out[r0] = {"g": avg(gpsi), "phi_r": avg(gphi), "phihat_r": avg(gpsi - gphi)}
    return out


def run(B, nR, nz):
    t0 = time.time()
    g = C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    s0 = radial_parts(P0, xs)
    row = {
        "edge_kpc": 0.1 * B,
        "grid": [nR, nz],
        "static": [bool(ok1), r1, bool(ok2), r2],
        "speeds": {},
    }
    for vk in (100.0, 300.0):
        P = C.ProblemC1(g, vk / C_KMS, rho, 0.0)
        x, ok, gn = P.newton(xs, tol=1e-10, maxit=40, verbose=False)
        entry = {"converged": bool(ok), "residual": gn}
        if ok:
            s1 = radial_parts(P, x)
            entry["newton_channel_ratio"] = {
                f"{r0 * 1e3:g}": s1[r0]["phihat_r"] / s0[r0]["phihat_r"] for r0 in RADII
            }
            entry["scalar_remnant_rh"] = s1[0.3e-3]["phi_r"] / s0[0.3e-3]["phi_r"]
            entry["g_ratio_rh"] = s1[0.3e-3]["g"] / s0[0.3e-3]["g"]
            np.save(f"cache_branch/gateC_B{B:g}_{nR}x{nz}_v{vk:g}.npy", x)
        row["speeds"][f"{vk:g}"] = entry
        print(
            f"edge {0.1 * B:g} kpc {nR}x{nz} v = {vk:g}: converged {ok} ({gn:.1e})"
            + (
                f"; Newton channel {[round(v, 4) for v in entry['newton_channel_ratio'].values()]}, scalar remnant {entry['scalar_remnant_rh']:.4f}, g ratio {entry['g_ratio_rh']:.4f}"
                if ok
                else ""
            ),
            flush=True,
        )
    row["seconds"] = round(time.time() - t0, 1)
    return row


if __name__ == "__main__":
    runs = [run(1000.0, 23, 46), run(1000.0, 30, 60), run(10000.0, 30, 60)]
    fails = []
    for rr in runs:
        tag = f"{rr['edge_kpc']:g} kpc {rr['grid'][0]}x{rr['grid'][1]}"
        for vk, e in rr["speeds"].items():
            if not e["converged"]:
                fails.append(f"{tag} v={vk}: not converged")
                continue
            for rk, val in e["newton_channel_ratio"].items():
                if abs(val - (1 - KB / 2)) > 0.02:
                    fails.append(f"{tag} v={vk} r={rk}: Newton channel {val:.4f}")
        e1, e3 = rr["speeds"]["100"], rr["speeds"]["300"]
        if (
            e1["converged"]
            and e3["converged"]
            and abs(e1["g_ratio_rh"] / e3["g_ratio_rh"] - 1) >= 0.02
        ):
            fails.append(
                f"{tag}: plateau {e1['g_ratio_rh']:.4f} vs {e3['g_ratio_rh']:.4f}"
            )
    try:
        rem100 = runs[1]["speeds"]["100"]["scalar_remnant_rh"]
        rem1000 = runs[2]["speeds"]["100"]["scalar_remnant_rh"]
        if not rem1000 < rem100:
            fails.append(
                f"scalar remnant does not fall with box: {rem100:.4f} (100 kpc) vs {rem1000:.4f} (1 Mpc)"
            )
    except KeyError:
        fails.append("scalar remnant comparison unavailable (a run did not converge)")
    verdict = "PASS" if not fails else "FAIL: " + "; ".join(fails)
    json.dump({"runs": runs, "verdict": verdict}, open("GATE_C_C1.json", "w"), indent=1)
    print("GATE C " + verdict)
