#!/usr/bin/env python3
"""D7 Stage 2: pseudo-arclength continuation in wind speed p [km/s] of (A) the held branch from the static state and
(B) the stripped branch downward from 20 km/s. Protocol: PREREG_ARCLENGTH_FOLD_2026-11-25.md (ab5a00ef), frozen first.
Same setup as branch_down_c1_v2.py: 16x32, g_e = 0.003 a0, box asinh(300), Plummer v_f = 10 km/s, b = 0.3 kpc.
Output: ARCLENGTH_C1_ge0.003_16x32.json (rewritten after every accepted point) and stdout -> ARCLENGTH_C1.txt."""
import gc, json, math, sys, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_c1 as C
from stage_c_c1 import observables, near_zero_modes

C_KMS = 299792.458
vf = 10 / C_KMS; b = 3e-4; M = 12 * math.pi * vf**4 / C.A0T; g_e = 0.003 * C.A0T
G = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
RHO = C.plummer_fn(M, b)
DP = 0.01            # km/s, central difference for dF/dp
TOL = 1e-10
OUT = "ARCLENGTH_C1_ge0.003_16x32.json"
LOG = {"prereg": "ab5a00ef", "gates": {}, "runs": {}}
_cache = {}


def prob(p):
    key = round(p, 9)
    if key not in _cache:
        while len(_cache) >= 3:
            _cache.pop(next(iter(_cache)))
        gc.collect()
        _cache[key] = C.ProblemC1(G, p / C_KMS, RHO, g_e)
    return _cache[key]


def F(x, p):
    return prob(p).grad_hess(x, want_hess=False)[0]


def Fp(x, p):
    return (F(x, p + DP) - F(x, p - DP)) / (2 * DP)


def equil(H):
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    return sps.diags(1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30)))


def save():
    json.dump(LOG, open(OUT, "w"), indent=1, default=float)


def obs_row(p, x, ref):
    P = prob(p); ob = observables(P, x); k = "0.3kpc"
    return {"g_ratio_static": ob[k]["g"] / ref[k]["g"], "Y_ratio": ob[k]["Y"] / ref[k]["Y"],
            "u_over_tilt": ob["max_u"] / ((vf**2 / b) / 0.1)}


def bordered_solve(A, fp, ty, tp, theta, rhs_top, rhs_bot):
    """Block elimination with one sparse LU of A (memory-lean; amended 2026-11-25 after an OOM kill of the
    monolithic bordered LU): A a = rhs_top, A c = fp, dp = (rhs_bot - theta ty.a)/(tp - theta ty.c), dy = a - c dp."""
    lu = spla.splu(A.tocsc())
    a = lu.solve(rhs_top); c = lu.solve(fp)
    for _ in range(2):  # iterative refinement
        a = a + lu.solve(rhs_top - A @ a); c = c + lu.solve(fp - A @ c)
    dp = (rhs_bot - theta * ty @ a) / (tp - theta * ty @ c)
    del lu; gc.collect()
    return a - c * dp, dp


def corrector(x0, p0, Sd, norm0, ty, tp, theta, yp_pred, p_pred, maxit=8):
    """Newton on [Sd F(x,p); theta*ty.(y-y_pred) + tp*(p-p_pred)] = 0 in y = Sd^-1 x."""
    x, p = x0.copy(), p0
    sdv = Sd.diagonal()
    for it in range(maxit + 1):
        Fx = F(x, p)
        res = np.linalg.norm(Sd @ Fx) / norm0
        y = x / sdv
        Ncond = theta * ty @ (y - yp_pred) + tp * (p - p_pred)
        if res < TOL and abs(Ncond) < 1e-9:
            return x, p, True, it, res
        if it == maxit or not np.isfinite(res) or res > 1e6:
            return x, p, False, it, res
        _, H, _ = prob(p).grad_hess(x)
        A = (Sd @ H @ Sd).tocsc()
        fp = Sd @ Fp(x, p)
        dy, dp = bordered_solve(A, fp, ty, tp, theta, -(Sd @ Fx), -Ncond)
        x = x + Sd @ dy; p = p + dp
    return x, p, False, maxit, res


def tangent(x, p, Sd, ty_old, tp_old, theta):
    _, H, _ = prob(p).grad_hess(x)
    A = (Sd @ H @ Sd).tocsc(); fp = Sd @ Fp(x, p)
    ty, tp = bordered_solve(A, fp, ty_old, tp_old, theta, np.zeros(A.shape[0]), 1.0)
    nrm = math.sqrt(theta * ty @ ty + tp * tp); ty, tp = ty / nrm, tp / nrm
    if theta * ty @ ty_old + tp * tp_old < 0:
        ty, tp = -ty, -tp
    return ty, tp


def continue_branch(name, x, p, direction, ref, ds_dp0, pmax=110.0, pmin=0.05, maxsteps=400):
    run = LOG["runs"].setdefault(name, {"rows": [], "events": []}); rows = run["rows"]
    _, H, _ = prob(p).grad_hess(x); Sd = equil(H); norm0 = np.linalg.norm(Sd @ prob(p).src)
    A = (Sd @ H @ Sd).tocsc(); fp = Sd @ Fp(x, p)
    dydp = spla.splu(A).solve(-fp)
    theta = 1.0 / float(dydp @ dydp)
    ty, tp = direction * dydp / math.sqrt(2), direction * 1.0 / math.sqrt(2)
    ds = ds_dp0 / abs(tp); ds_min = 0.002 / abs(tp); ds_max = 5.0 / abs(tp)
    t0 = time.time()
    for step in range(maxsteps):
        sdv = Sd.diagonal(); y = x / sdv
        yp, pp = y + ds * ty, p + ds * tp
        xn, pn, ok, its, res = corrector(Sd @ yp, pp, Sd, norm0, ty, tp, theta, yp, pp)
        if not ok:
            ds *= 0.5
            run["events"].append({"step": step, "fail_at_p": float(pp), "res": float(res), "new_ds": float(ds)})
            if ds < ds_min:
                run["stop"] = f"corrector failed at minimum ds near p = {p:.4f} km/s (last res {res:.2e})"
                print(f"[{name}] STOP: {run['stop']}", flush=True); save(); return run
            continue
        # accept
        x_old_dot = Sd @ ty
        x, p = xn, pn
        _, H, _ = prob(p).grad_hess(x); Sd = equil(H); norm0 = np.linalg.norm(Sd @ prob(p).src)
        ty_old = x_old_dot / Sd.diagonal()
        ty, tp_new = tangent(x, p, Sd, ty_old, tp, theta)
        turned = (tp_new * tp < 0)
        tp = tp_new
        row = {"step": step, "p_kms": float(p), "pdot": float(tp), "iters": its, "res": float(res), "ds": float(ds)}
        row.update(obs_row(p, x, ref))
        if step % 6 == 0 or turned or abs(tp) < 0.2:
            nz = near_zero_modes(prob(p), x)
            row["eig_min"] = (nz.get("modes") or [{}])[0].get("eig")
            row["eig_field"] = (nz.get("modes") or [{}])[0].get("field")
        if turned:
            row["FOLD"] = True
            run["events"].append({"fold_near_p": float(p), "step": step})
        rows.append(row); save()
        print(f"[{name}] p = {p:8.4f}  pdot {tp:+.3f}  Y/Ys {row['Y_ratio']:.4f}  g/gs {row['g_ratio_static']:.4f}  "
              f"u/tilt {row['u_over_tilt']:.2e}  its {its}  eig {row.get('eig_min')}  {'FOLD' if turned else ''}  "
              f"[{time.time() - t0:.0f}s]", flush=True)
        if its <= 4:
            ds = min(ds * 1.5, ds_max)
        if p > pmax or p < pmin:
            run["stop"] = f"left range at p = {p:.3f}"; save(); return run
        if step > 0 and abs(p) < 1e-6:
            break
    run["stop"] = run.get("stop", "max steps"); save(); return run


def main():
    t0 = time.time()
    # G1: static held state (Lambda frozen), then Lambda free at v = 0
    P0 = prob(0.0)
    xs, ok, gn = P0.newton(C.initial_guess_c1(G, P0.dm, M, b), tol=TOL, maxit=25, verbose=False, freeze=P0.lambda_dofs())
    ref = observables(P0, xs)
    LOG["gates"]["G1_static"] = {"residual": gn, "converged": bool(ok and gn < TOL)}
    print("G1 static:", LOG["gates"]["G1_static"], flush=True); save()
    if not LOG["gates"]["G1_static"]["converged"]:
        return
    # G0: reproduce the cached stripped state at 20 km/s with the bordered corrector (tangent = d/dp)
    xc = np.load("cache_branch/stripped_ge0.003_16x32_v20.npy")
    _, H, _ = prob(20.0).grad_hess(xc); Sd = equil(H); norm0 = np.linalg.norm(Sd @ prob(20.0).src)
    n = H.shape[0]
    xg, pg, okg, itg, resg = corrector(xc, 20.0, Sd, norm0, np.zeros(n), 1.0, 1.0, xc / Sd.diagonal(), 20.0)
    yr = obs_row(pg, xg, ref)["Y_ratio"]
    LOG["gates"]["G0_reproduce_stripped_20"] = {"converged": bool(okg), "res": resg, "p": pg, "Y_ratio": yr,
                                               "pass": bool(okg and abs(yr - 0.0154) < 1e-4)}
    print("G0:", LOG["gates"]["G0_reproduce_stripped_20"], flush=True); save()
    if not LOG["gates"]["G0_reproduce_stripped_20"]["pass"]:
        return
    # G2: natural Newton at 0.25 km/s from static
    x1, ok1, gn1 = prob(0.25).newton(xs, tol=TOL, maxit=25, verbose=False)
    LOG["gates"]["G2_first_step"] = {"converged": bool(ok1), "residual": gn1}
    print("G2:", LOG["gates"]["G2_first_step"], flush=True); save()
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if ok1 and which in ("both", "held"):
        continue_branch("A_held_up", x1, 0.25, +1, ref, ds_dp0=0.25)
    if which in ("both", "stripped"):
        continue_branch("B_stripped_down", xg, pg, -1, ref, ds_dp0=0.5)
    LOG["runtime_s"] = time.time() - t0; save()


if __name__ == "__main__":
    main()
