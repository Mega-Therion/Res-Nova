#!/usr/bin/env python3
"""D7 Stage 2, gate B2 on the C1 solver: the linear wind response must reproduce TARGET_D7 supplement section 7. Identical
physics, comparison and criterion to gate_wind_linear_fe.py (whose first run was on the locked Q1 discretization and is
withdrawn); only the discretization changes. Criterion (unchanged, fixed before the first B2 run): PASS iff at every radius
(0.1, 0.15, 0.2, 0.3 kpc) and both speeds (100, 300 km/s) the smooth ratio d_r(delta F)/d_r(pred) is within 0.10 of 1, the
100/300 km/s relative difference of the inner gradient field (0.05 < r < 0.3 kpc) is < 0.10, and max |delta u| / stealth
tilt < 0.05. Prediction (section 7, K_B = 1/2): delta phi = -[1/(4+lambda)] (4 Psi - 3 inv_lap d_z^2 Phihat), lambda = 2 J'.
delta F here is the change of phi = s - Q0 gam Lambda in the first Newton step H(v) dx = -grad(x_static; v).
Usage: gate_wind_linear_c1.py <g_e/a0> <box> <nR> <nz> [<nR2> <nz2>]. Output: GATE_B2_WIND_LINEAR_C1_ge<g_e>_box<box>.json.
"""

import json, math, sys, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_c1 as C

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
Q0 = 0.1
SHELLS = (0.1e-3, 0.15e-3, 0.2e-3, 0.3e-3)


def scalar_poisson(g, dm, D, dzf):
    """lap X = d_z f with X = 0 on the outer boundary, in the C1 space of the S slot (value-Dirichlet), from d_z f at the
    Gauss points: K X = G_z^T W (d_z f). Returns (value, d_R, d_z) of X at the Gauss points.
    """
    fi = C.FIX["S"]
    m = dm.index[fi]
    cols = np.unique(m[m >= 0])
    base = np.arange(g.ng) * C.NQ + 3 * fi
    Gv, Gr, Gz = D[base, :][:, cols], D[base + 1, :][:, cols], D[base + 2, :][:, cols]
    W = sps.diags(g.w)
    X = spla.spsolve((Gr.T @ W @ Gr + Gz.T @ W @ Gz).tocsc(), Gz.T @ (g.w * dzf))
    return Gv @ X, Gr @ X, Gz @ X


def run(nR, nz, ge_a0, box, speeds=(100.0, 300.0)):
    t0 = time.time()
    g_e = ge_a0 * C.A0T
    g = C.GridC1(nR, nz, 1e-4, math.asinh(box), math.asinh(box))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, g_e)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    q0 = (P0.D @ xs).reshape(g.ng, C.NQ)
    c = lambda q, n, k: q[:, 3 * C.FIX[n] + k]
    Psi = [-0.5 * c(q0, "S", k) for k in range(3)]
    X = scalar_poisson(g, P0.dm, P0.D, -0.5 * c(q0, "S", 2) - c(q0, "F", 2))
    qt = q0 + P0.qbg
    lam = 2 * C.mu_std(np.hypot(c(qt, "F", 1), c(qt, "F", 2)) / C.A0T)
    pred = [-(4 * Psi[k] - 3 * X[k]) / (4 + lam) for k in range(3)]
    r = np.hypot(g.Rg, g.zg)
    rad = lambda comp: (g.Rg * comp[1] + g.zg * comp[2]) / r
    phi_static = [c(q0, "F", k) for k in range(3)]
    inner = (r > 0.05e-3) & (r < 0.3e-3)
    out = {
        "nR": nR,
        "nz": nz,
        "g_e_over_a0": ge_a0,
        "box": box,
        "static": [bool(ok1), r1, bool(ok2), r2],
        "speeds": [],
    }
    dFs = {}
    for vk in speeds:
        Pv = C.ProblemC1(g, vk / C_KMS, rho, g_e)
        grad, H, _ = Pv.grad_hess(xs)
        Sd = sps.diags(1 / np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()))
        step = Sd @ Pv.solve_linear(Sd @ H @ Sd, -(Sd @ grad))
        qs = (Pv.D @ step).reshape(g.ng, C.NQ)
        dF = [c(qs, "F", k) for k in range(3)]
        dFs[vk] = dF
        rows = []
        for r0 in SHELLS:
            wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
            rows.append(
                {
                    "r_kpc": r0 * 1e3,
                    "dF_r_over_pred_r": float(
                        np.sum(rad(dF) * wb) / np.sum(rad(pred) * wb)
                    ),
                    "dF_r_over_static_phi_r": float(
                        np.sum(rad(dF) * wb) / np.sum(rad(phi_static) * wb)
                    ),
                    "pred_r_over_static_phi_r": float(
                        np.sum(rad(pred) * wb) / np.sum(rad(phi_static) * wb)
                    ),
                }
            )
        dv = np.stack([dF[1] - pred[1], dF[2] - pred[2]])[:, inner]
        pv = np.stack([pred[1], pred[2]])[:, inner]
        rel = math.sqrt(
            np.sum(g.w[inner] * (dv**2).sum(0)) / np.sum(g.w[inner] * (pv**2).sum(0))
        )
        Umax = float(np.max(np.hypot(c(qs, "U_R", 0), c(qs, "U_z", 0))))
        out["speeds"].append(
            {
                "v_kms": vk,
                "shells": rows,
                "grad_rel_L2_diff_inner": rel,
                "max_du_over_stealth_tilt": Umax / ((vf**2 / b) / Q0),
                "linear_solve_residual": Pv.solve_log[-1],
            }
        )
    a_, b_ = (dFs[v] for v in speeds)
    num = np.sum(g.w[inner] * ((a_[1] - b_[1]) ** 2 + (a_[2] - b_[2]) ** 2)[inner])
    den = np.sum(g.w[inner] * (a_[1] ** 2 + a_[2] ** 2)[inner])
    out["plateau_grad_rel_diff_inner"] = math.sqrt(num / den)
    fails = [
        f"v={s['v_kms']:g} r={sh['r_kpc']} ratio {sh['dF_r_over_pred_r']:.3f}"
        for s in out["speeds"]
        for sh in s["shells"]
        if abs(sh["dF_r_over_pred_r"] - 1) > 0.10
    ]
    fails += [
        f"v={s['v_kms']:g} tilt {s['max_du_over_stealth_tilt']:.3f}"
        for s in out["speeds"]
        if s["max_du_over_stealth_tilt"] >= 0.05
    ]
    if out["plateau_grad_rel_diff_inner"] >= 0.10:
        fails.append(f"plateau difference {out['plateau_grad_rel_diff_inner']:.3f}")
    out["verdict"] = "PASS" if not fails else "FAIL: " + "; ".join(fails)
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    ge_a0, box = float(a[0]), float(a[1])
    grids = [(int(a[2]), int(a[3]))] + ([(int(a[4]), int(a[5]))] if len(a) > 5 else [])
    res = []
    for n in grids:
        rr = run(*n, ge_a0, box)
        res.append(rr)
        print(
            json.dumps(
                {
                    k: rr[k]
                    for k in ("nR", "nz", "verdict", "plateau_grad_rel_diff_inner")
                }
            ),
            flush=True,
        )
        for s in rr["speeds"]:
            print(
                f"  v = {s['v_kms']:g}: tilt {s['max_du_over_stealth_tilt']:.3f}; "
                + ", ".join(
                    f"r {sh['r_kpc']}: dF/pred {sh['dF_r_over_pred_r']:+.3f} (dF/phi {sh['dF_r_over_static_phi_r']:+.3f}, pred/phi {sh['pred_r_over_static_phi_r']:+.3f})"
                    for sh in s["shells"]
                ),
                flush=True,
            )
    json.dump(
        res, open(f"GATE_B2_WIND_LINEAR_C1_ge{ge_a0:g}_box{box:g}.json", "w"), indent=2
    )
