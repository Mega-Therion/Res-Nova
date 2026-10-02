#!/usr/bin/env python3
"""Exploratory: the structure of a saved steady state (stripped_highv_c1.py / branch_down_c1_v2.py) against the static held
solution. Radial shells (smooth weight) at r = 0.1-2.4 kpc: g = <d_r Psi> (Psi = -h00/2, what matter feels), <d_r phi>,
<d_r Phihat> = g - <d_r phi>, the MOND-channel field <(grad phi + Q0 u)_r> and <Y>, and the tilt <u_r>; each as a ratio to
the static value. At r_h, upstream (cos theta > 0.5, the wind comes from +z), side (|cos theta| < 0.5) and downstream
(cos theta < -0.5) sectors separately.
Usage: analyse_stripped_c1.py <state.npy> <g_e/a0> <box> <nR> <nz> <v_kms>."""

import json, math, sys
import numpy as np
import solve_c1 as C

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
Q0 = 0.1
path, ge_a0, box, nR, nz, vk = (
    sys.argv[1],
    float(sys.argv[2]),
    float(sys.argv[3]),
    int(sys.argv[4]),
    int(sys.argv[5]),
    float(sys.argv[6]),
)
g_e = ge_a0 * C.A0T
g = C.GridC1(nR, nz, 1e-4, math.asinh(box), math.asinh(box))
rho = C.plummer_fn(M, b)
P0 = C.ProblemC1(g, 0.0, rho, g_e)
x1, ok1, _ = P0.newton(
    C.initial_guess_c1(g, P0.dm, M, b),
    tol=1e-11,
    maxit=20,
    verbose=False,
    freeze=P0.lambda_dofs(),
)
x2, ok2, _ = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
xs = x2 if ok2 else x1
P = C.ProblemC1(g, vk / C_KMS, rho, g_e)
xv = np.load(path)
r = np.hypot(g.Rg, g.zg)
ct = g.zg / r


def fields(Pr, x):
    q = (Pr.D @ x).reshape(g.ng, C.NQ)
    qt = q + Pr.qbg
    c = lambda qq, n, k: qq[:, 3 * C.FIX[n] + k]
    rad = lambda qq, n: (g.Rg * c(qq, n, 1) + g.zg * c(qq, n, 2)) / r
    gpsi = -0.5 * rad(q, "S")
    gphi = rad(q, "F")
    ur = (g.Rg * c(q, "U_R", 0) + g.zg * c(q, "U_z", 0)) / r
    Y = np.asarray(
        C.y_accurate([qt[:, k] for k in range(C.NQ)], g.Rg, Pr.v), dtype=float
    )
    return {
        "g": gpsi,
        "phi_r": gphi,
        "phihat_r": gpsi - gphi,
        "S_r": gphi + Q0 * ur,
        "Y": Y,
        "u_r": ur,
    }


F0, F1 = fields(P0, xs), fields(P, xv)
out = {
    "state": path,
    "g_e_over_a0": ge_a0,
    "box": box,
    "grid": [nR, nz],
    "v_kms": vk,
    "shells": [],
    "sectors_rh": {},
}
print(
    f"{'r/kpc':>6} "
    + " ".join(f"{k + ' ratio':>14}" for k in ("g", "phi_r", "phihat_r", "S_r", "Y"))
    + f" {'u_r/tilt':>10}"
)
tilt = (vf**2 / b) / Q0
for r0 in (0.1e-3, 0.2e-3, 0.3e-3, 0.6e-3, 1.2e-3, 2.4e-3):
    wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
    avg = lambda f: float(np.sum(f * wb) / np.sum(wb))
    row = {"r_kpc": r0 * 1e3}
    for k in ("g", "phi_r", "phihat_r", "S_r", "Y"):
        row[k + "_ratio"] = avg(F1[k]) / avg(F0[k])
    row["u_r_over_tilt"] = avg(F1["u_r"]) / tilt
    out["shells"].append(row)
    print(
        f"{r0 * 1e3:6.2f} "
        + " ".join(
            f"{row[k + '_ratio']:14.4f}" for k in ("g", "phi_r", "phihat_r", "S_r", "Y")
        )
        + f" {row['u_r_over_tilt']:10.2e}"
    )
wb = g.w * np.exp(-(((r - 0.3e-3) / (0.15 * 0.3e-3)) ** 2))
for name, sel in (
    ("upstream", ct > 0.5),
    ("side", np.abs(ct) <= 0.5),
    ("downstream", ct < -0.5),
):
    w = wb * sel
    avg = lambda f: float(np.sum(f * w) / np.sum(w))
    out["sectors_rh"][name] = {
        k + "_ratio": avg(F1[k]) / avg(F0[k]) for k in ("g", "phi_r", "S_r", "Y")
    }
    print(
        f"r_h {name:10s}: "
        + ", ".join(f"{k} {v:.4f}" for k, v in out["sectors_rh"][name].items())
    )
json.dump(
    out,
    open(
        path.replace(".npy", "_analysis.json").replace("cache_branch/", "ANALYSIS_"),
        "w",
    ),
    indent=1,
)
