#!/usr/bin/env python3
"""D7 Stage 2, gate B1 on the C1 solver (solve_c1.py): at v = 0 the full ten-field solution must obey AeST's static flux
laws. Same checks and criterion as gate_static_fe.py / gate_b1_verdict.py (smooth radial weight, the primary estimator
since the Q1 diagnosis): PASS iff Newton converged at both grids; the Newton channel <d_r Phihat> and the MOND channel
<J'(|grad phi_tot|) d_r phi_tot> are within 0.02 of M(<r)/(12 pi r^2) (averaged the same way) at every shell on both grids;
refinement does not drift away from 1 (|fine - 1| <= |coarse - 1| + 0.005); and max |u| / stealth tilt < 1e-3.
Why now: an exploratory wind run on this solver reported g/g_static = 0.098 together with g/(Phihat flux) = 3.3, which
implies a static g/(Phihat flux) of ~34 at r_h where deep MOND gives ~11; B1 had not been run on the C1 solver.
Usage: gate_static_c1.py <g_e/a0> <box> <nR> <nz> [<nR2> <nz2>]; static solution = stage 1 (Lambda frozen), then Lambda free
if that converges (both logged). Output: GATE_B1_STATIC_C1_ge<g_e>_box<box>.json."""

import json, math, sys, time
import numpy as np
import solve_c1 as C

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
Q0 = 0.1
SHELLS = (0.1e-3, 0.2e-3, 0.3e-3, 0.6e-3, 1.2e-3)


def flux(r):
    return M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)


def run(nR, nz, ge_a0, box):
    t0 = time.time()
    g_e = ge_a0 * C.A0T
    g = C.GridC1(nR, nz, 1e-4, math.asinh(box), math.asinh(box))
    P = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), g_e)
    x1, ok1, r1 = P.newton(
        C.initial_guess_c1(g, P.dm, M, b),
        tol=1e-11,
        maxit=20,
        verbose=False,
        freeze=P.lambda_dofs(),
    )
    x2, ok2, r2 = P.newton(x1, tol=1e-10, maxit=15, verbose=False)
    x, used = (x2, "Lambda free") if ok2 else (x1, "stage 1")
    q = (P.D @ x).reshape(g.ng, C.NQ)
    qt = q + P.qbg
    col = lambda qq, n, k: qq[:, 3 * C.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    dr = lambda qq, n: (g.Rg * col(qq, n, 1) + g.zg * col(qq, n, 2)) / r
    Psi_r = -0.5 * dr(q, "S")
    phihat_r = Psi_r - dr(q, "F")
    mond_r = C.mu_std(np.hypot(col(qt, "F", 1), col(qt, "F", 2)) / C.A0T) * dr(qt, "F")
    ref = flux(r)
    out = {
        "nR": nR,
        "nz": nz,
        "g_e_over_a0": ge_a0,
        "box": box,
        "stage1": [bool(ok1), float(r1)],
        "free": [bool(ok2), float(r2)],
        "used": used,
        "converged": bool(ok1),
        "final_residual": float(r2 if ok2 else r1),
        "seconds": round(time.time() - t0, 1),
        "shells": [],
    }
    for r0 in SHELLS:
        ws = g.w * (np.abs(r - r0) < 0.12 * r0)
        wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
        sh = {"r_kpc": r0 * 1e3}
        for tag, w in (("", ws), ("_smooth", wb)):
            den = np.sum(ref * w)
            sh["newton_channel_ratio" + tag] = float(np.sum(phihat_r * w) / den)
            sh["mond_channel_ratio" + tag] = float(np.sum(mond_r * w) / den)
            sh["psi_over_flux" + tag] = float(np.sum(Psi_r * w) / den)
        out["shells"].append(sh)
    out["max_u_over_stealth_tilt"] = float(
        np.max(np.hypot(col(q, "U_R", 0), col(q, "U_z", 0)))
    ) / ((vf**2 / b) / Q0)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    ge_a0, box = float(a[0]), float(a[1])
    grids = [(int(a[2]), int(a[3]))] + ([(int(a[4]), int(a[5]))] if len(a) > 5 else [])
    res = []
    for n in grids:
        rr = run(*n, ge_a0, box)
        print(
            f"{n}: stage1 {rr['stage1']}, free {rr['free']}, used {rr['used']}, u/tilt {rr['max_u_over_stealth_tilt']:.1e}",
            flush=True,
        )
        for sh in rr["shells"]:
            print(
                f"   r = {sh['r_kpc']:.1f} kpc: Newton channel {sh['newton_channel_ratio_smooth']:.4f}, MOND channel "
                f"{sh['mond_channel_ratio_smooth']:.4f}, Psi_r/flux {sh['psi_over_flux_smooth']:.3f}",
                flush=True,
            )
        res.append(rr)
    json.dump(
        res, open(f"GATE_B1_STATIC_C1_ge{ge_a0:g}_box{box:g}.json", "w"), indent=2
    )
