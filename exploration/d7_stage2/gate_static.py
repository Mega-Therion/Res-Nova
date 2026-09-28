#!/usr/bin/env python3
"""D7 Stage 2, gate B1: at v = 0 the full solver (all ten fields) must reproduce AeST's static MOND dwarf.
Setup: a Plummer dwarf with deep-MOND flat speed v_f = 10 km/s (M = 12 pi v_f^4 / a0t in 16 pi G~ = 1 units), b = 0.3 kpc,
and a weak external field g_e = 0.03 a0t along z, which makes the far field decay (EFE radius ~0.5 kpc). Stretched grid
out to ~10 kpc. Checks:
  (1) Newton converges;
  (2) the Newtonian channel: the shell-averaged radial derivative of the internal Phihat = Psi - phi
      (Psi = -h00/2) equals M(<r) / (12 pi r^2), the del^2 Phihat = rho/3 flux law (linear, so exact up to
      discretization and the boundary);
  (3) the MOND channel well inside the EFE radius: shell-averaged J'(|grad phi|) d_r phi against the same flux (the
      external field makes it non-spherical, so this only holds for r << r_EFE);
  (4) the aether stays aligned: max |u| against the stealth tilt g/Q0 = the tilt the dragged branch would need.
Run at two resolutions."""

import json, math, sys, time
import numpy as np
import solve_steady as SS

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / SS.A0T
g_e = 0.03 * SS.A0T
Q0 = 0.1


def run(nR, nz, a=1e-4, xi_max=math.asinh(100.0), eta_max=math.asinh(100.0)):
    g = SS.Grid(nR, nz, a, xi_max, eta_max)
    rho = SS.plummer(g, M, b)
    P = SS.Problem(g, 0.0, rho, g_e)
    f0 = SS.initial_guess(g, M, b, g_e)
    t0 = time.time()
    f, ok, gn = P.newton(f0, tol=1e-8, maxit=25)
    q = (P.D @ f).reshape(g.ncell, SS.NQ)  # internal jets (no background)
    col = lambda n, k: q[:, 3 * SS.FIX[n] + k]
    r = np.sqrt(g.Rc**2 + g.zc**2)
    dr = lambda n: (g.Rc * col(n, 1) + g.zc * col(n, 2)) / r
    phihat_r = -0.5 * dr("S") - dr("F")
    qt = q + P.qbg  # total jets for J'
    Fr_t, Fz_t = qt[:, 3 * SS.FIX["F"] + 1], qt[:, 3 * SS.FIX["F"] + 2]
    gphi = np.sqrt(Fr_t**2 + Fz_t**2)
    Jp = SS.mu_std(gphi / SS.A0T)
    mond_r = Jp * dr("F")
    out = {
        "nR": nR,
        "nz": nz,
        "converged": bool(ok),
        "final_grad": float(gn),
        "seconds": time.time() - t0,
        "shells": [],
    }
    for r0 in (0.1e-3, 0.2e-3, 0.3e-3, 0.6e-3, 1.2e-3):
        sel = np.abs(r - r0) < 0.12 * r0
        wts = g.w[sel]
        Menc = M * r0**3 / (r0**2 + b**2) ** 1.5
        flux = Menc / (12 * math.pi * r0**2)
        out["shells"].append(
            {
                "r_kpc": r0 * 1e3,
                "n_cells": int(sel.sum()),
                "newton_channel_ratio": float(
                    np.sum(phihat_r[sel] * wts) / np.sum(wts) / flux
                ),
                "mond_channel_ratio": float(
                    np.sum(mond_r[sel] * wts) / np.sum(wts) / flux
                ),
            }
        )
    gb = vf**2 / b
    Umax = float(np.max(np.hypot(col("U_R", 0), col("U_z", 0))))
    out["max_u_over_stealth_tilt"] = Umax / (gb / Q0)
    return out


if __name__ == "__main__":
    res = [run(40, 80), run(56, 112)]
    for rr in res:
        print(json.dumps(rr, indent=1))
    json.dump(res, open("GATE_B1_STATIC.json", "w"), indent=2)
