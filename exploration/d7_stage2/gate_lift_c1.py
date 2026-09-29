#!/usr/bin/env python3
"""D7 Stage 2, gate L: the C1 solver must carry exactly TARGET_D3 section 23's lift of the aether-tilt zero mode (the gate
the Q1 solver failed by ~1e8 through locking; diag_lift.py, DIAG_LIFT.txt).
Zero mode with the metric frozen (as in section 23): d Lambda = -chi/Q0, all other DOFs fixed. Since phi = s - Q0 gam Lambda
and u = grad Lambda + curl(psi theta_hat), this is d phi = chi, d u = -grad chi/Q0, which leaves S = grad phi + Q0 u unchanged;
in C1 elements it is represented exactly (zero discrete curl at every quadrature point).
Section 23: E_lift = [-2 K2 Q0^2 Psi + K_B lap Psi + (2-K_B) lap phi] |grad Lambda|^2, evaluated here with the static solution's
own Psi = -S/2, lap Psi and lap phi (second derivatives straight from the Hermite elements; the static background is the
stage-1 held solution, Lambda = 0). Bumps chi = exp(-((r - r0)/w)^2) at r0 = 0.15, 0.3, 0.6, 1.2 kpc, w = r0/3.
Criterion, fixed and committed before the first run: with R(r0) = dx^T H dx / (-2 int E_lift dV), PASS iff at each grid
(16x32, 24x48) every |R(r0)/mean_r0(R) - 1| < 0.10, and |mean_16x32 / mean_24x48 - 1| < 0.10. The common value of R is a
convention constant (expected +1 if the solver's quadratic Lagrangian is -E_lift); it is reported, not required.
Setup: g_e = 0.003 a0, box asinh(300)."""

import json, math
import numpy as np
import solve_c1 as C

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
g_e = 0.003 * C.A0T
Q0, KB, K2 = 0.1, 0.5, 75.0
RADII = (0.15e-3, 0.3e-3, 0.6e-3, 1.2e-3)


def stage1_static(nR, nz):
    g = C.GridC1(nR, nz, 1e-4, math.asinh(300.0), math.asinh(300.0))
    P = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), g_e)
    x, ok, gn = P.newton(
        C.initial_guess_c1(g, P.dm, M, b),
        tol=1e-11,
        maxit=20,
        verbose=False,
        freeze=P.lambda_dofs(),
    )
    if gn > 1e-10:  # implementation tolerance (24x48 stops at ~1.1e-11), not the gate criterion
        raise RuntimeError(f"stage-1 static solve did not converge ({gn:.1e})")
    return g, P, x, gn


def second_derivs(g, dm, x, field):
    """(f, f_R, f_z, f_RR, f_zz) of one C1 field at the Gauss points."""
    nodes = dm.to_nodes(x)[C.FIX[field]]
    out = {k: np.zeros(g.ng) for k in ("v", "R", "z", "RR", "zz")}
    for a, bb, d, bf in C.basis_at_gauss(g):
        coef = nodes[(g.ei + a) * (g.nz + 1) + (g.ej + bb), d]
        for k in out:
            out[k] += coef * bf[k]
    return out


def bump_nodes(g, dm, r0, w):
    """Hermite nodal data (f, f_xi, f_eta, f_xi_eta) of chi = exp(-((r - r0)/w)^2), as a full DOF vector in the Lambda slot
    scaled by -1/Q0."""
    RR, ZZ = np.meshgrid(g.Rn, g.zn, indexing="ij")
    R, Z = RR.ravel(), ZZ.ravel()
    r = np.hypot(R, Z)
    chi = np.exp(-(((r - r0) / w) ** 2))
    d1 = -2 * (r - r0) / w**2 * chi
    d2 = (4 * (r - r0) ** 2 / w**4 - 2 / w**2) * chi
    with np.errstate(invalid="ignore", divide="ignore"):
        nR_, nZ_ = np.where(r > 0, R / r, 0.0), np.where(r > 0, Z / r, 0.0)
        cross = np.where(r > 0, (d2 - d1 / np.where(r > 0, r, 1)) * nR_ * nZ_, 0.0)
    hR = g.a * np.cosh(np.arcsinh(R / g.a))
    hz = g.a * np.cosh(np.arcsinh(Z / g.a))
    arr = np.zeros((C.NF, g.nnode, 4))
    fi = C.FIX["U_R"]
    arr[fi, :, 0] = chi
    arr[fi, :, 1] = hR * d1 * nR_
    arr[fi, :, 2] = hz * d1 * nZ_
    arr[fi, :, 3] = hR * hz * cross
    return -dm.from_nodes(arr) / Q0


def run(nR, nz):
    g, P, x, gn = stage1_static(nR, nz)
    grad, H, Y = P.grad_hess(x)
    Sd = second_derivs(g, P.dm, x, "S")
    Fd = second_derivs(g, P.dm, x, "F")  # s = phi at Lambda = 0
    iR = 1 / g.Rg
    lap = lambda d: d["RR"] + d["R"] * iR + d["zz"]
    Psi = -0.5 * Sd["v"]
    lapPsi, lapphi = -0.5 * lap(Sd), lap(Fd)
    rows = []
    for r0 in RADII:
        dx = bump_nodes(g, P.dm, r0, r0 / 3)
        quad = float(dx @ (H @ dx))
        q = (P.D @ dx).reshape(g.ng, C.NQ)
        gL2 = (
            q[:, 3 * C.FIX["U_R"]] ** 2 + q[:, 3 * C.FIX["U_z"]] ** 2
        )  # |d u|^2 = |grad Lambda|^2
        terms = {
            "Q-sector": -2 * K2 * Q0**2 * Psi,
            "K_B lap Psi": KB * lapPsi,
            "(2-K_B) lap phi": (2 - KB) * lapphi,
        }
        E = {k: float(np.sum(g.w * v * gL2)) for k, v in terms.items()}
        Et = sum(E.values())
        rows.append(
            {
                "r0_kpc": r0 * 1e3,
                "quad_form": quad,
                "minus2_E_lift": -2 * Et,
                "R": quad / (-2 * Et),
                "E_terms": E,
            }
        )
    Rs = np.array([rr["R"] for rr in rows])
    return {
        "grid": [nR, nz],
        "stage1_residual": gn,
        "rows": rows,
        "R_mean": float(Rs.mean()),
        "max_rel_spread": float(np.max(np.abs(Rs / Rs.mean() - 1))),
    }


if __name__ == "__main__":
    res = [run(16, 32), run(24, 48)]
    fails = [
        f"{r['grid']}: spread {r['max_rel_spread']:.3f}"
        for r in res
        if r["max_rel_spread"] >= 0.10
    ]
    ratio = res[0]["R_mean"] / res[1]["R_mean"]
    if abs(ratio - 1) >= 0.10:
        fails.append(
            f"grid means differ: {res[0]['R_mean']:.4f} vs {res[1]['R_mean']:.4f}"
        )
    out = {"runs": res, "verdict": "PASS" if not fails else "FAIL: " + "; ".join(fails)}
    for r in res:
        print(
            f"{r['grid']}: R(r0) = "
            + ", ".join(f"{rr['R']:+.4f}" for rr in r["rows"])
            + f"; mean {r['R_mean']:+.4f}, spread {r['max_rel_spread']:.3f}"
        )
    print("GATE L " + out["verdict"])
    json.dump(out, open("GATE_L_LIFT_C1.json", "w"), indent=2)
