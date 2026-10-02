#!/usr/bin/env python3
"""D7 Stage 2, gate B2: the linear wind response of the full solver must reproduce TARGET_D7 supplement section 7.
Section 7 (WKB, K_B = 1/2, plateau regime v cos(alpha) >> v_x ~ 10 km/s, isolated deep-MOND field) gives the real-space
correction the wind forces on the dwarf's own field:
    delta phi = -[1/(4+lambda)] inv_lap[ 8K_B lap(phi+Phihat) + (4-8K_B) d_z^2 phi - 6K_B d_z^2 Phihat ]
              = -[1/(4+lambda)] ( 4 Psi - 3 inv_lap d_z^2 Phihat )          at K_B = 1/2 (Psi = phi + Phihat),
with lambda ~ 2 J' (0.98 and 0.73 at x = 0.05), a response that does not depend on v in the plateau.
Here the same quantity is the first Newton step of the full ten-field solver from the static held solution at wind
speed v: H(v) dx = -grad(x_static; v). Both sides are linear in the forcing, so they must agree where WKB applies.
Compared: radial derivatives (the field correction; the large-scale zero point of the potentials sits in the lift
regime) with the smooth radial weight of gate B1, at r = 0.1-0.3 kpc. Also: plateau v-independence (100 against
300 km/s) and the aether tilt (section 7: 0.1-3% of the stealth tilt g/Q0).
Usage: gate_wind_linear_fe.py [g_e/a0 = 0.003] [box = 300]. The primary case has the dwarf's own field ~10 g_e, as
section 7 assumes; g_e = 0.03 a0 (external-field dominated) is outside section 7's stated validity.
Criterion, fixed before the first run: PASS iff at every radius and both speeds the smooth ratio d_r(delta F)/d_r(pred)
is within 0.10 of 1 (WKB at kr ~ 1, and the angle dependence of section 7's response is ~3%), the 100/300 km/s
relative difference of the inner gradient field is < 0.10, and max |delta u| / stealth tilt < 0.05.
"""

import json, math, sys, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_fe as FE

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
Q0 = 0.1
SHELLS = (0.1e-3, 0.15e-3, 0.2e-3, 0.3e-3)


def jets(P, x):
    return (P.D @ x).reshape(P.g.ng, FE.NQ)


def scalar_poisson(P, dzf_at_gauss):
    """Solve lap X = d_z f with Dirichlet X = 0 on the outer boundary, given d_z f at the Gauss points; FE weak form
    K X = G_z^T W (d_z f). Uses the F-field dofs (same boundary mask). Returns (value, d_R, d_z) at the Gauss points.
    """
    g, dm = P.g, P.dm
    fi = FE.FIX["F"]
    cols = np.arange(dm.offsets[fi], dm.offsets[fi + 1])
    base = np.arange(g.ng) * FE.NQ + 3 * fi
    Gr = P.D[base + 1, :][:, cols]
    Gz = P.D[base + 2, :][:, cols]
    W = sps.diags(g.w)
    X = spla.spsolve(
        (Gr.T @ W @ Gr + Gz.T @ W @ Gz).tocsc(), Gz.T @ (g.w * dzf_at_gauss)
    )
    full = np.zeros(dm.ndof)
    full[cols] = X
    return jets(P, full)[:, 3 * fi : 3 * fi + 3]


def run(nR, nz, ge_a0, box, speeds_kms=(100.0, 300.0)):
    t0 = time.time()
    g_e = ge_a0 * FE.A0T
    g, P0, xs, res0 = FE.static_solution(nR, nz, M, b, g_e, box)
    rho = FE.plummer_fn(M, b)
    q0 = jets(P0, xs)
    c = lambda q, n, k: q[:, 3 * FE.FIX[n] + k]
    Psi = [-0.5 * c(q0, "S", k) for k in range(3)]
    X = scalar_poisson(P0, -0.5 * c(q0, "S", 2) - c(q0, "F", 2))  # inv_lap d_z^2 Phihat
    qt = q0 + P0.qbg
    lam = 2 * FE.mu_std(np.hypot(c(qt, "F", 1), c(qt, "F", 2)) / FE.A0T)
    pred = [-(4 * Psi[k] - 3 * X[:, k]) / (4 + lam) for k in range(3)]
    r = np.hypot(g.Rg, g.zg)
    rad = lambda comp: (g.Rg * comp[1] + g.zg * comp[2]) / r
    phi_static = [c(q0, "F", k) for k in range(3)]
    inner = (r > 0.05e-3) & (r < 0.3e-3)
    out = {
        "nR": nR,
        "nz": nz,
        "g_e_over_a0": ge_a0,
        "box": box,
        "static_residual": float(res0),
        "speeds": [],
    }
    dFs = {}
    for vk in speeds_kms:
        Pv = FE.ProblemFE(g, vk / C_KMS, rho, g_e)
        grad, H, _ = Pv.grad_hess(xs)
        Sd = sps.diags(1 / np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()))
        step = Sd @ spla.spsolve((Sd @ H @ Sd).tocsc(), -(Sd @ grad))
        qs = jets(Pv, step)
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
            }
        )
    a_, b_ = (dFs[v] for v in speeds_kms)
    num = np.sum(g.w[inner] * ((a_[1] - b_[1]) ** 2 + (a_[2] - b_[2]) ** 2)[inner])
    den = np.sum(g.w[inner] * (a_[1] ** 2 + a_[2] ** 2)[inner])
    out["plateau_grad_rel_diff_inner"] = math.sqrt(num / den)
    fails = [
        f"v={s['v_kms']:g} r={sh['r_kpc']} kpc ratio {sh['dF_r_over_pred_r']:.3f}"
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
    ge_a0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.003
    box = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    res = [run(32, 64, ge_a0, box), run(48, 96, ge_a0, box)]
    print(json.dumps(res, indent=1), flush=True)
    json.dump(
        res, open(f"GATE_B2_WIND_LINEAR_FE_ge{ge_a0:g}_box{box:g}.json", "w"), indent=2
    )
