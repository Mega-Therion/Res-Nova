#!/usr/bin/env python3
"""D7 Stage 2, gate B1 on the finite-element solver (solve_fe.py): at v = 0 the full solver (all ten fields) must
reproduce AeST's static MOND dwarf. Plummer dwarf with deep-MOND flat speed v_f = 10 km/s (M = 12 pi v_f^4 / a0t in
16 pi G~ = 1 units), b = 0.3 kpc, an external field g_e along z, grid out to asinh(box) in xi and eta.
Usage: gate_static_fe.py [g_e/a0 = 0.003] [box = 300]. Output GATE_B1_STATIC_FE_ge<g_e>_box<box>.json.
Checks, at the Gauss points, each against the reference flux M(<r)/(12 pi r^2) averaged the same way:
  (1) Newton converges;
  (2) the Newtonian channel: <d_r Phihat> (Phihat = Psi - phi, Psi = -h00/2), the flux law of del^2 Phihat = rho/3
      (the uniform external part of Phihat carries no net flux);
  (3) the MOND channel: <J'(|grad phi_tot|) d_r phi_tot>, the flux law of div(J' grad phi) = rho/3 for the total field
      phi_tot = phi + g_e z (exact for any g_e; with g_e = 0.03 a0 this dwarf's own field is only ~g_e at 0.1-0.6 kpc,
      so no region is "well inside the EFE radius");
  (4) the aether stays aligned: max |u| against the stealth tilt g_b / Q0 that the dragged branch would need.
Two averages: "sharp" (Gauss points with |r - r0| < 0.12 r0, the pre-registered estimator) and "smooth" (weight
exp(-((r - r0)/(0.15 r0))^2)). The sharp one splits the +/- Gauss-point pairs whose O(h) derivative errors cancel, so it
carries O(h/r) noise that does not shrink monotonically; it failed the no-drift criterion at r = 0.1 kpc in the first
corrected run (GATE_B1_VERDICT.txt) while the smooth one converges at second order (diag_b1_flux.py, DIAG_B1_FLUX.txt).
From then on the smooth estimator is the primary one; the sharp one is still reported.
"""

import json, math, sys, time
import numpy as np
import solve_fe as FE

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
Q0 = 0.1
SHELLS = (0.1e-3, 0.2e-3, 0.3e-3, 0.6e-3, 1.2e-3)


def flux(r):
    return M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)


def run(nR, nz, ge_a0, box):
    t0 = time.time()
    g_e = ge_a0 * FE.A0T
    g, P, x, gn = FE.static_solution(nR, nz, M, b, g_e, box)
    q = (P.D @ x).reshape(
        g.ng, FE.NQ
    )  # internal jets at the Gauss points (no background)
    qt = q + P.qbg
    col = lambda qq, n, k: qq[:, 3 * FE.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    dr = lambda qq, n: (g.Rg * col(qq, n, 1) + g.zg * col(qq, n, 2)) / r
    phihat_r = -0.5 * dr(q, "S") - dr(q, "F")
    mond_r = FE.mu_std(np.hypot(col(qt, "F", 1), col(qt, "F", 2)) / FE.A0T) * dr(
        qt, "F"
    )
    ref = flux(r)
    out = {
        "nR": nR,
        "nz": nz,
        "g_e_over_a0": ge_a0,
        "box": box,
        "ndof": int(P.dm.ndof),
        "converged": bool(gn < 1e-9),
        "final_residual": float(gn),
        "seconds": round(time.time() - t0, 1),
        "shells": [],
    }
    for r0 in SHELLS:
        sel = np.abs(r - r0) < 0.12 * r0
        ws = g.w * sel
        wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
        out["shells"].append(
            {
                "r_kpc": r0 * 1e3,
                "n_gauss_points_sharp": int(sel.sum()),
                "newton_channel_ratio": float(np.sum(phihat_r * ws) / np.sum(ref * ws)),
                "mond_channel_ratio": float(np.sum(mond_r * ws) / np.sum(ref * ws)),
                "newton_channel_ratio_smooth": float(
                    np.sum(phihat_r * wb) / np.sum(ref * wb)
                ),
                "mond_channel_ratio_smooth": float(
                    np.sum(mond_r * wb) / np.sum(ref * wb)
                ),
            }
        )
    Umax = float(np.max(np.hypot(col(q, "U_R", 0), col(q, "U_z", 0))))
    out["max_u_over_stealth_tilt"] = Umax / ((vf**2 / b) / Q0)
    return out


if __name__ == "__main__":
    ge_a0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.003
    box = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    res = []
    for n in ((32, 64), (48, 96)):
        rr = run(*n, ge_a0, box)
        print(json.dumps(rr, indent=1), flush=True)
        res.append(rr)
    json.dump(
        res, open(f"GATE_B1_STATIC_FE_ge{ge_a0:g}_box{box:g}.json", "w"), indent=2
    )
