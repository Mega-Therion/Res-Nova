#!/usr/bin/env python3
"""D7 Stage 2, stage C: the non-linear steady state of the dwarf in the aether wind, by continuation in the wind speed v
from the static held solution (gate B1). Plummer dwarf, v_f = 10 km/s, b = 0.3 kpc, external field g_e along z, wind
along z. Usage: stage_c_continuation.py [g_e/a0 = 0.003] [box = 300] [nR = 32] [nz = 64].
At each speed: Newton (tol 1e-9) from a secant predictor, falling back to the last solution; on failure the step in v is
bisected. Fixed before the first run:
  - a failure is only called a failure, with its final residual logged; a fold needs an eigenvalue of the equilibrated
    Hessian going to zero as v approaches the stopping speed (the 6 eigenvalues nearest zero are logged per speed);
  - a jump: if u/tilt, Y/Y_static or g/g_static at r_h changes by more than 0.1 in one accepted step, the interval is
    bisected (down to 1/64 of the step or 0.05 km/s) to see whether the change is steep but continuous or a real jump;
    rows are flagged "steep" when the change stays above 0.1 at the finest bisection.
Per converged speed:
  - g_ratio_static: <d_r Psi_int> at r (Psi = -h00/2, the potential matter feels) over its static value (the observable);
  - g_ratio_phihat_flux: the same over M(<r)/(12 pi r^2), the Phihat-channel flux (a reference only: the dragged
    branch's own acceleration is not established);
  - Y_ratio: <Y> over its static value (held keeps Y; the dragged branch drives Y -> 0);
  - max_u_over_stealth_tilt (held ~0; dragged ~1);
  all with the smooth radial weight of gate B1.
Output: STAGE_C_CONTINUATION_ge<g_e>_box<box>_<nR>x<nz>.json, rewritten after every accepted speed.
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
RADII = (0.15e-3, 0.3e-3, 0.6e-3)
SPEEDS = (0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300)
JUMP = 0.1


def flux(r):
    return M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)


def observables(P, x):
    g = P.g
    q = (P.D @ x).reshape(g.ng, FE.NQ)
    qt = q + P.qbg
    c = lambda qq, n, k: qq[:, 3 * FE.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    Psi_r = -0.5 * (g.Rg * c(q, "S", 1) + g.zg * c(q, "S", 2)) / r
    Y = FE.y_accurate([qt[:, k] for k in range(FE.NQ)], g.Rg, P.v)
    out = {}
    for r0 in RADII:
        wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
        out[f"{r0 * 1e3:g}kpc"] = {
            "g": float(np.sum(Psi_r * wb) / np.sum(wb)),
            "flux": float(np.sum(flux(r) * wb) / np.sum(wb)),
            "Y": float(np.sum(Y * wb) / np.sum(wb)),
        }
    out["max_u"] = float(np.max(np.hypot(c(q, "U_R", 0), c(q, "U_z", 0))))
    return out


def near_zero_modes(P, x, k=6):
    grad, H, _ = P.grad_hess(x)
    Sd = sps.diags(1 / np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()))
    A = (Sd @ H @ Sd).tocsc()
    A = (0.5 * (A + A.T)).tocsc()
    try:
        ev, V = spla.eigsh(A, k=k, sigma=0, which="LM")
    except Exception as e:  # shift-invert fails if A is singular at the shift
        return {"error": str(e)[:120]}
    off = P.dm.offsets
    rows = []
    for i in np.argsort(np.abs(ev)):
        fw = [
            float(np.linalg.norm(V[off[f] : off[f + 1], i]) ** 2) for f in range(FE.NF)
        ]
        rows.append(
            {
                "eig": float(ev[i]),
                "field": FE.NAMES[int(np.argmax(fw))],
                "weight": round(max(fw), 3),
            }
        )
    return {"modes": rows}


def main(ge_a0=0.003, box=300.0, nR=32, nz=64):
    g_e = ge_a0 * FE.A0T
    g, P0, xs, res0 = FE.static_solution(nR, nz, M, b, g_e, box)
    rho = FE.plummer_fn(M, b)
    ref = observables(P0, xs)
    tilt = (vf**2 / b) / Q0
    path = f"STAGE_C_CONTINUATION_ge{ge_a0:g}_box{box:g}_{nR}x{nz}.json"
    log = {
        "grid": [nR, nz],
        "g_e_over_a0": ge_a0,
        "box": box,
        "static_residual": res0,
        "static": ref,
        "static_modes": near_zero_modes(P0, xs),
        "speeds": [],
    }

    def row_for(P, x, v, gn, secs):
        ob = observables(P, x)
        row = {
            "v_kms": v,
            "residual": gn,
            "seconds": secs,
            "max_u_over_stealth_tilt": ob["max_u"] / tilt,
        }
        for key in ob:
            if key.endswith("kpc"):
                row[key] = {
                    "g_ratio_static": ob[key]["g"] / ref[key]["g"],
                    "g_ratio_phihat_flux": ob[key]["g"] / ob[key]["flux"],
                    "Y_ratio": ob[key]["Y"] / ref[key]["Y"],
                }
        return row

    def jump(a, bb):
        if a is None:
            return 0.0
        return max(
            abs(a["max_u_over_stealth_tilt"] - bb["max_u_over_stealth_tilt"]),
            abs(a["0.3kpc"]["Y_ratio"] - bb["0.3kpc"]["Y_ratio"]),
            abs(a["0.3kpc"]["g_ratio_static"] - bb["0.3kpc"]["g_ratio_static"]),
        )

    x_prev, x_pp, v_prev, v_pp, last = xs, None, 0.0, None, None
    for v_target in SPEEDS:
        v_try, step0 = v_target, v_target - v_prev
        while True:
            t0 = time.time()
            P = FE.ProblemFE(g, v_try / C_KMS, rho, g_e)
            guess = (
                x_prev
                if x_pp is None
                else x_prev + (v_try - v_prev) / (v_prev - v_pp) * (x_prev - x_pp)
            )
            x, ok, gn = P.newton(guess, tol=1e-9, maxit=25, verbose=False)
            if not ok and x_pp is not None:
                x, ok, gn = P.newton(x_prev, tol=1e-9, maxit=25, verbose=False)
            dv_min = max(0.05, step0 / 64)
            if not ok:
                print(
                    f"v = {v_try:g} km/s: Newton failed (residual {gn:.1e}); bisecting",
                    flush=True,
                )
                log.setdefault("failures", []).append(
                    {"v_kms": v_try, "residual": gn, "from_kms": v_prev}
                )
                if v_try - v_prev <= dv_min:
                    log["stopped"] = {
                        "last_converged_kms": v_prev,
                        "failed_at_kms": v_try,
                        "residual": gn,
                    }
                    json.dump(log, open(path, "w"), indent=1)
                    print(
                        f"STOP: no convergence between {v_prev:g} and {v_try:g} km/s",
                        flush=True,
                    )
                    return
                v_try = 0.5 * (v_prev + v_try)
                continue
            row = row_for(P, x, v_try, gn, round(time.time() - t0, 1))
            jmp = jump(last, row)
            if jmp > JUMP and v_try - v_prev > dv_min:
                print(
                    f"v = {v_try:g} km/s: change {jmp:.2f} in one step from {v_prev:g}; refining",
                    flush=True,
                )
                v_try = 0.5 * (v_prev + v_try)
                continue
            row["steep"] = bool(jmp > JUMP)
            row["near_zero_modes"] = near_zero_modes(P, x)
            log["speeds"].append(row)
            json.dump(log, open(path, "w"), indent=1)
            m0 = row["near_zero_modes"].get("modes", [{}])[0]
            print(
                f"v = {v_try:g} km/s: residual {gn:.1e}, g/g_static(r_h) {row['0.3kpc']['g_ratio_static']:.4f}, "
                f"Y/Y_static {row['0.3kpc']['Y_ratio']:.4f}, u/tilt {row['max_u_over_stealth_tilt']:.2e}, "
                f"eig nearest 0 {m0.get('eig')} ({m0.get('field')}){' STEEP' if row['steep'] else ''}",
                flush=True,
            )
            x_pp, v_pp, x_prev, v_prev, last = x_prev, v_prev, x, v_try, row
            if v_try == v_target:
                break
            v_try = v_target


if __name__ == "__main__":
    a = sys.argv[1:]
    main(
        float(a[0]) if len(a) > 0 else 0.003,
        float(a[1]) if len(a) > 1 else 300.0,
        int(a[2]) if len(a) > 2 else 32,
        int(a[3]) if len(a) > 3 else 64,
    )
