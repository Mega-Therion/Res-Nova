#!/usr/bin/env python3
"""D7 Stage 2, stage C on the C1 solver (solve_c1.py): the non-linear steady state of the dwarf in the aether wind, by
continuation in the wind speed from the static held solution. Plummer dwarf, v_f = 10 km/s, b = 0.3 kpc, wind along z.
Usage: stage_c_c1.py [g_e/a0 = 0] [box = 100] [nR = 16] [nz = 32].
Why g_e = 0 is the primary case: with an external field the MOND curvature lap phi -> 0 beyond the EFE radius, the lift of
the aether-tilt zero mode vanishes there, and that region is dragged at ANY wind speed (an O(1) change that Newton cannot
reach from the static state). Without it (TARGET_D7 supplement section 7's own setting, an isolated deep-MOND dwarf) the
crossover v_x ~ C v_f ~ 2-3 km/s is the same at every radius, so continuation in small steps can follow the branch.
Static reference: the stage-1 held solution (Lambda frozen at 0; the aether's static source is divergence-free), then an
attempt with Lambda free; whichever converged is used (both residuals logged).
Per speed: Newton (tol 1e-9) from a secant predictor, then from the last solution; failure bisects the step (down to
1/64 of it or 0.02 km/s). Fixed before the first run: a fold needs an eigenvalue of the equilibrated Hessian going to zero
as the stopping speed is approached (6 nearest zero logged per speed); a change > 0.1 in u/tilt, Y/Y_static or g/g_static
at r_h in one step triggers interval refinement, and rows are flagged "steep" if it persists at the finest step.
Observables at r = 0.15, 0.3 (r_h), 0.6 kpc with the smooth radial weight: g/g_static (<d_r Psi>, Psi = -h00/2, the
potential matter feels), Y/Y_static, g over the Phihat-channel flux M(<r)/(12 pi r^2) (the static deep-MOND value is ~11
at r_h; D3 section 34 puts the dragged/GR branch at 1 - K_B/2 = 0.75 of it, a reference not verified in this solver), and
max |u| over the stealth tilt g_b/Q0. Output: STAGE_C_C1_ge<g_e>_box<box>_<nR>x<nz>.json, rewritten after every speed.
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
RADII = (0.15e-3, 0.3e-3, 0.6e-3)
SPEEDS = tuple(np.round(np.arange(0.25, 5.01, 0.25), 2)) + (
    6,
    7,
    8,
    10,
    12,
    15,
    20,
    30,
    50,
    75,
    100,
    150,
    200,
    300,
)
JUMP = 0.1
LABEL = {"W_R": "Omega", "W_z": "omega", "U_R": "Lambda", "U_z": "psi", "F": "s"}


def flux(r):
    return M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)


def observables(P, x):
    g = P.g
    q = (P.D @ x).reshape(g.ng, C.NQ)
    qt = q + P.qbg
    c = lambda qq, n, k: qq[:, 3 * C.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    Psi_r = -0.5 * (g.Rg * c(q, "S", 1) + g.zg * c(q, "S", 2)) / r
    Y = C.y_accurate([qt[:, k] for k in range(C.NQ)], g.Rg, P.v)
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
    _, H, _ = P.grad_hess(x)
    Sd = sps.diags(1 / np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()))
    A = (Sd @ H @ Sd).tocsc()
    A = (0.5 * (A + A.T)).tocsc()
    try:
        ev, V = spla.eigsh(A, k=k, sigma=0, which="LM")
    except Exception as e:
        return {"error": str(e)[:120]}
    idx = P.dm.index
    rows = []
    for i in np.argsort(np.abs(ev)):
        fw = {}
        for n in C.NAMES:
            m = idx[C.FIX[n]]
            fw[LABEL.get(n, n)] = float(np.linalg.norm(V[np.unique(m[m >= 0]), i]) ** 2)
        top = max(fw, key=fw.get)
        rows.append({"eig": float(ev[i]), "field": top, "weight": round(fw[top], 3)})
    return {"modes": rows}


def main(ge_a0=0.0, box=100.0, nR=16, nz=32):
    g_e = ge_a0 * C.A0T
    g = C.GridC1(nR, nz, 1e-4, math.asinh(box), math.asinh(box))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, g_e)
    lam = P0.lambda_dofs()
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=20,
        verbose=False,
        freeze=lam,
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs, which = (x2, "Lambda free") if ok2 else (x1, "stage 1 (Lambda frozen)")
    ref = observables(P0, xs)
    tilt = (vf**2 / b) / Q0
    path = f"STAGE_C_C1_ge{ge_a0:g}_box{box:g}_{nR}x{nz}.json"
    log = {
        "grid": [nR, nz],
        "g_e_over_a0": ge_a0,
        "box": box,
        "static": {
            "stage1_residual": r1,
            "stage1_converged": ok1,
            "free_residual": r2,
            "free_converged": ok2,
            "used": which,
            "observables": ref,
        },
        "speeds": [],
    }
    print(
        f"static: stage 1 {r1:.1e} ({ok1}), Lambda free {r2:.1e} ({ok2}); using {which}",
        flush=True,
    )

    def row_for(P, x, v, gn, secs):
        ob = observables(P, x)
        row = {
            "v_kms": float(v),
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
        v_try, step0 = float(v_target), float(v_target) - v_prev
        while True:
            t0 = time.time()
            P = C.ProblemC1(g, v_try / C_KMS, rho, g_e)
            guess = (
                x_prev
                if x_pp is None
                else x_prev + (v_try - v_prev) / (v_prev - v_pp) * (x_prev - x_pp)
            )
            x, ok, gn = P.newton(guess, tol=1e-9, maxit=30, verbose=False)
            if not ok and x_pp is not None:
                x, ok, gn = P.newton(x_prev, tol=1e-9, maxit=30, verbose=False)
            dv_min = max(0.02, step0 / 64)
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
            row["last_linear_solve_residual"] = P.solve_log[-1] if P.solve_log else None
            log["speeds"].append(row)
            json.dump(log, open(path, "w"), indent=1)
            m0 = row["near_zero_modes"].get("modes", [{}])[0]
            k = "0.3kpc"
            print(
                f"v = {v_try:g} km/s: residual {gn:.1e}, g/g_static(r_h) {row[k]['g_ratio_static']:.4f}, g/phihat-flux "
                f"{row[k]['g_ratio_phihat_flux']:.3f}, Y/Y_static {row[k]['Y_ratio']:.4f}, u/tilt {row['max_u_over_stealth_tilt']:.3e}, "
                f"eig nearest 0 {m0.get('eig')} ({m0.get('field')}){' STEEP' if row['steep'] else ''}",
                flush=True,
            )
            x_pp, v_pp, x_prev, v_prev, last = x_prev, v_prev, x, v_try, row
            if v_try == float(v_target):
                break
            v_try = float(v_target)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(
        float(a[0]) if len(a) > 0 else 0.0,
        float(a[1]) if len(a) > 1 else 100.0,
        int(a[2]) if len(a) > 2 else 16,
        int(a[3]) if len(a) > 3 else 32,
    )
