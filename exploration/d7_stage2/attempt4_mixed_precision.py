#!/usr/bin/env python3
"""Exploratory: attempt 4 of the box extension = option 2 (mixed-precision Newton), under Amendment 2 of
PREREG_BOX_EXTEND_2026-10-06.md (committed before this script first ran).

Identical to solve_c1.ProblemC1.newton in: the equations; every problem-defining datum (jet operator D, quadrature
weights w, density rho, constants, all as their float64 values); the equilibration Sd = 1/sqrt(row sums of |H|),
computed at x0 and then fixed; the residual measure |Sd g|/|Sd src|; the Armijo backtracking (factor 1e-4, halve,
stop when lambda < 1e-4); tol 1e-10; maxit 40.
Changed (arithmetic only):
  (i)   gradient and Hessian are assembled in x87 long double (eps 1.08e-19); the original rounds every local term
        to float64 before assembly (grad_hess: gq.astype(float), vals.astype(float));
  (ii)  the Newton step solves A y = -Sd g with right-preconditioned restarted GMRES in long double on the matrix-free
        long-double operator A v = Sd D^T W (D (Sd v)), preconditioned by the float64 LU of the float64-rounded A
        (restart 80, at most 3 restarts, relative tolerance 1e-12; the attained value is logged);
  (iii) residuals (acceptance, line search) are evaluated in long double. The float64 residual of the original code
        path, with the same Sd, is logged every iteration as well.
Modes:
  check      correctness of the extended path (thresholds fixed in PREREG Amendment 2) + descriptive precision data
  validate   committed 100 kpc fixed-sweep row from static (criterion fixed in Amendment 2)
  ladder     rungs n = 31..34 from the 1000 kpc cache, stop rule; refuses to run unless validate passed
  verdict    applies the Amendment 1 rule at n = 34 (needs the ladder row and BOX_LADDER_STATIC_n34.json)
Outputs: ATTEMPT4_CHECK.json, ATTEMPT4_VALIDATE.json, ATTEMPT4_LADDER.json, ATTEMPT4_VERDICT.json,
cache_branch/attempt4_<tag>_it<k>.npy, cache_branch/attempt4_ladder_n<n>_v100.npy."""

import json, math, os, sys, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_c1 as C
import local_derivs as LD
from solve_fe import y_accurate
from solve_steady import kfun
from stage_c_c1 import observables

LDT = np.longdouble
vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
V_W = 100 / 299792.458
DXI = math.asinh(1e4) / 30
TOL = 1e-10
MAXIT = 40
RHO = C.plummer_fn(M, b)


def nrm(v):
    return np.sqrt(np.dot(v, v))


class Extended:
    """Long-double gradient and matrix-free Hessian of a ProblemC1 (float64 problem data, extended arithmetic)."""

    def __init__(self, P):
        self.P = P
        g = P.g
        self.D = P.D.astype(LDT).tocsr()
        self.w = g.w.astype(LDT)
        rho_g = RHO(g.Rg, g.zg)
        Svalrows = np.arange(g.ng) * C.NQ + 3 * C.FIX["S"]
        self.src = P.D[Svalrows, :].T.astype(LDT) @ (
            LDT(0.5) * rho_g.astype(LDT) * self.w
        )
        self.qbg = P.qbg.astype(LDT)
        self.Rg = g.Rg.astype(LDT)
        self.v = LDT(P.v)

    def _local(self, x):
        g = self.P.g
        q = (self.D @ np.asarray(x, dtype=LDT)).reshape(g.ng, C.NQ) + self.qbg
        qa = [np.ascontiguousarray(q[:, k]) for k in range(C.NQ)]
        arr = lambda t: np.broadcast_to(np.asarray(t, dtype=LDT), (g.ng,))
        return qa, arr

    def grad(self, x):
        g = self.P.g
        qa, arr = self._local(x)
        gL = np.array([arr(t) for t in LD.grad_L(qa, self.Rg, self.v)])
        gY = np.array([arr(t) for t in LD.grad_Y(qa, self.Rg, self.v)])
        Y = arr(y_accurate(qa, self.Rg, self.v))
        K1, K2 = kfun(Y)
        gq = gL - K1 * gY
        assert gq.dtype == LDT and np.asarray(K1).dtype == LDT
        return self.D.T @ (gq * self.w).T.ravel() + self.src

    def grad_and_W(self, x):
        g = self.P.g
        qa, arr = self._local(x)
        gL = np.array([arr(t) for t in LD.grad_L(qa, self.Rg, self.v)])
        gY = np.array([arr(t) for t in LD.grad_Y(qa, self.Rg, self.v)])
        Y = arr(y_accurate(qa, self.Rg, self.v))
        K1, K2 = kfun(Y)
        gq = gL - K1 * gY
        grad = self.D.T @ (gq * self.w).T.ravel() + self.src
        HL = dict(
            zip(LD.HESS_L_KEYS, (arr(t) for t in LD.hess_L_vals(qa, self.Rg, self.v)))
        )
        HY = dict(
            zip(LD.HESS_Y_KEYS, (arr(t) for t in LD.hess_Y_vals(qa, self.Rg, self.v)))
        )
        z0 = np.zeros(g.ng, dtype=LDT)
        vals = []
        for i, j in self.P.hkeys:
            a, bb = (i, j) if i <= j else (j, i)
            vals.append(
                (HL.get((a, bb), z0) - K1 * HY.get((a, bb), z0) - K2 * gY[i] * gY[j])
                * self.w
            )
        W = sps.csr_matrix(
            (np.concatenate(vals), (self.P.Wrows, self.P.Wcols)),
            shape=(g.ng * C.NQ, g.ng * C.NQ),
        )
        assert grad.dtype == LDT and W.dtype == LDT
        return grad, W

    def hess_apply(self, W, v):
        return self.D.T @ (W @ (self.D @ v))


def gmres_ld(apply_A, apply_Minv, rhs, tol=1e-12, restart=80, max_restarts=3):
    """Right-preconditioned restarted GMRES in long double. Returns y, attained |rhs - A y|/|rhs|, iterations."""
    n = rhs.size
    y = np.zeros(n, dtype=LDT)
    bnorm = nrm(rhs)
    its = 0
    beta_prev = None
    for _ in range(max_restarts + 1):
        r = rhs - apply_A(y)
        beta = nrm(r)
        if beta <= tol * bnorm:
            break
        if beta_prev is not None and beta > 0.5 * beta_prev:
            break  # a restart cycle gained < 2x: at the long-double attainable floor (~eps_ld |A||y|), stop
        beta_prev = beta
        V = np.zeros((restart + 1, n), dtype=LDT)
        Z = np.zeros((restart, n), dtype=LDT)
        H = np.zeros((restart + 1, restart), dtype=LDT)
        cs = np.zeros(restart, dtype=LDT)
        sn = np.zeros(restart, dtype=LDT)
        gv = np.zeros(restart + 1, dtype=LDT)
        gv[0] = beta
        V[0] = r / beta
        k = 0
        for j in range(restart):
            Z[j] = apply_Minv(V[j])
            w = apply_A(Z[j])
            for _pass in range(
                2
            ):  # modified Gram-Schmidt with one re-orthogonalisation
                for i in range(j + 1):
                    h = np.dot(V[i], w)
                    H[i, j] += h
                    w = w - h * V[i]
            H[j + 1, j] = nrm(w)
            if H[j + 1, j] > 0:
                V[j + 1] = w / H[j + 1, j]
            for i in range(j):
                t = cs[i] * H[i, j] + sn[i] * H[i + 1, j]
                H[i + 1, j] = -sn[i] * H[i, j] + cs[i] * H[i + 1, j]
                H[i, j] = t
            den = np.sqrt(H[j, j] * H[j, j] + H[j + 1, j] * H[j + 1, j])
            cs[j], sn[j] = H[j, j] / den, H[j + 1, j] / den
            H[j, j], H[j + 1, j] = den, LDT(0)
            gv[j + 1] = -sn[j] * gv[j]
            gv[j] = cs[j] * gv[j]
            its += 1
            k = j + 1
            if abs(gv[j + 1]) <= tol * bnorm:
                break
        c = np.zeros(k, dtype=LDT)
        for i in range(k - 1, -1, -1):
            c[i] = (gv[i] - np.dot(H[i, i + 1 : k], c[i + 1 : k])) / H[i, i]
        y = y + c @ Z[:k]
    rel = nrm(rhs - apply_A(y)) / bnorm
    return y, float(rel), its


def equilibration(P, W):
    H64 = (P.D.T @ W.astype(np.float64) @ P.D).tocsc()
    rown = np.asarray(abs(H64).sum(axis=1)).ravel()
    return H64, 1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30))


def mp_newton(P, ext, x0, tag, tol=TOL, maxit=MAXIT):
    x = np.asarray(x0, dtype=LDT).copy()
    grad, W = ext.grad_and_W(x)
    H64, sd = equilibration(P, W)
    sd_ld = sd.astype(LDT)
    norm0 = nrm(sd_ld * ext.src)
    norm0_64 = np.linalg.norm(sd * P.src)
    res = lambda gr: float(nrm(sd_ld * gr) / norm0)
    res64 = lambda xx: float(
        np.linalg.norm(
            sd * P.grad_hess(np.asarray(xx, dtype=np.float64), want_hess=False)[0]
        )
        / norm0_64
    )
    log = []
    for it in range(maxit):
        gn = res(grad)
        r64 = res64(x)
        np.save(f"cache_branch/attempt4_{tag}_it{it}.npy", x)
        if gn < tol:
            print(
                f"    mpnewton {it}: residual(ld) {gn:.3e}  residual(f64) {r64:.3e}  CONVERGED",
                flush=True,
            )
            log.append({"it": it, "residual": gn, "residual_f64": r64})
            return x, True, gn, r64, log
        A64 = (sps.diags(sd) @ H64 @ sps.diags(sd)).tocsc()
        lu = spla.splu(A64)
        apply_A = lambda v: sd_ld * ext.hess_apply(W, sd_ld * v)
        apply_Minv = lambda v: lu.solve(np.asarray(v, dtype=np.float64)).astype(LDT)
        rhs = -(sd_ld * grad)
        y, lin_rel, lin_its = gmres_ld(apply_A, apply_Minv, rhs)
        del lu, A64
        step = sd_ld * y
        lam = 1.0
        while True:
            gt = ext.grad(x + LDT(lam) * step)
            if res(gt) < gn * (1 - 1e-4 * lam):
                break
            lam *= 0.5
            if lam < 1e-4:
                entry = {
                    "it": it,
                    "residual": gn,
                    "residual_f64": r64,
                    "gmres_rel": lin_rel,
                    "gmres_its": lin_its,
                    "line_search": "no descent (lambda < 1e-4)",
                }
                log.append(entry)
                print(
                    f"    mpnewton {it}: residual(ld) {gn:.3e}  residual(f64) {r64:.3e}  gmres {lin_its} its rel {lin_rel:.1e}: NO DESCENT",
                    flush=True,
                )
                return x, False, gn, r64, log
        entry = {
            "it": it,
            "residual": gn,
            "residual_f64": r64,
            "gmres_rel": lin_rel,
            "gmres_its": lin_its,
            "lambda": lam,
        }
        log.append(entry)
        print(
            f"    mpnewton {it}: residual(ld) {gn:.3e}  residual(f64) {r64:.3e}  gmres {lin_its} its rel {lin_rel:.1e}  lambda {lam:.3g}",
            flush=True,
        )
        x = x + LDT(lam) * step
        grad, W = ext.grad_and_W(x)
        H64 = (P.D.T @ W.astype(np.float64) @ P.D).tocsc()
    gn = res(grad)
    return x, gn < tol, gn, res64(x), log


def problem(g, v=V_W):
    return C.ProblemC1(g, v, RHO, 0.0)


def obs03(P, x):
    k = observables(P, np.asarray(x, dtype=np.float64))["0.3kpc"]
    return {"g": k["g"], "flux": k["flux"], "Y": k["Y"]}


def embed(x_old, g_old, dm_old, g_new, dm_new):
    assert abs(g_old.dxi - g_new.dxi) < 1e-12 and abs(g_old.deta - g_new.deta) < 1e-12
    oj = (g_new.nz - g_old.nz) // 2
    a_old = dm_old.to_nodes(np.asarray(x_old, dtype=np.float64)).reshape(
        C.NF, g_old.nR + 1, g_old.nz + 1, 4
    )
    a_new = np.zeros((C.NF, g_new.nR + 1, g_new.nz + 1, 4))
    a_new[:, : g_old.nR + 1, oj : oj + g_old.nz + 1, :] = a_old
    return dm_new.from_nodes(a_new.reshape(C.NF, g_new.nnode, 4))


def box_grid(B, nR, nz):
    return C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))


mode = sys.argv[1]

if mode == "check":
    out = {
        "thresholds": {
            "src_rel": 1e-14,
            "grad_diff_equil": 1e-10,
            "hess_action_rel": 1e-12,
            "gmres_random_rel": 1e-10,
        }
    }
    rng = np.random.default_rng(7)
    t = time.time()
    # (1) correctness at the cached converged 100 kpc solution (23x46)
    g = box_grid(1000.0, 23, 46)
    P = problem(g)
    ext = Extended(P)
    x = np.load("cache_branch/boxsweep_B1000_23x46_v100.npy")
    g64, H, _ = P.grad_hess(x)
    gl, Wl = ext.grad_and_W(x)
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    sd = 1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30))
    sdl = sd.astype(LDT)
    n0 = nrm(sdl * ext.src)
    c = {
        "src_rel": float(nrm(ext.src - P.src.astype(LDT)) / nrm(P.src.astype(LDT))),
        "res_f64": float(np.linalg.norm(sd * g64) / np.linalg.norm(sd * P.src)),
        "res_ld": float(nrm(sdl * gl) / n0),
        "grad_diff_equil": float(nrm(sdl * (gl - g64.astype(LDT))) / n0),
    }
    v = rng.standard_normal(P.dm.ndof)
    Hv = H @ v
    Hv_ext = ext.hess_apply(Wl, v.astype(LDT))
    c["hess_action_rel"] = float(
        np.linalg.norm(Hv - Hv_ext.astype(np.float64)) / np.linalg.norm(Hv)
    )
    A64 = (sps.diags(sd) @ H @ sps.diags(sd)).tocsc()
    lu = spla.splu(A64)
    bvec = rng.standard_normal(P.dm.ndof).astype(LDT)
    _, rel, its = gmres_ld(
        lambda u: sdl * ext.hess_apply(Wl, sdl * u),
        lambda u: lu.solve(np.asarray(u, dtype=np.float64)).astype(LDT),
        bvec,
    )
    c["gmres_random_rel"], c["gmres_random_its"] = rel, its
    c["PASS"] = (
        c["src_rel"] <= 1e-14
        and c["grad_diff_equil"] <= 1e-10
        and c["hess_action_rel"] <= 1e-12
        and rel <= 1e-10
    )
    out["at_100kpc_converged"] = c
    print("check @100 kpc:", json.dumps(c), flush=True)
    del P, ext, H, Wl, A64, lu
    # (2) descriptive: is the committed float64 1000 kpc root also a long-double root?
    g = box_grid(1e4, 30, 60)
    P = problem(g)
    ext = Extended(P)
    x = np.load("cache_branch/boxsweep_B10000_30x60_v100.npy")
    g64, H, _ = P.grad_hess(x)
    gl = ext.grad(x)
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    sd = 1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30))
    sdl = sd.astype(LDT)
    d = {
        "res_f64": float(np.linalg.norm(sd * g64) / np.linalg.norm(sd * P.src)),
        "res_ld": float(nrm(sdl * gl) / nrm(sdl * ext.src)),
    }
    out["at_1000kpc_committed_root"] = d
    print("check @1000 kpc committed root:", json.dumps(d), flush=True)
    del P, ext, H
    # (3) descriptive: the first Newton step at attempt 2's initial guess (1391 kpc), float64 path vs extended path
    g_old = box_grid(1e4, 30, 60)
    P_old = problem(g_old)
    x_old = np.load("cache_branch/boxsweep_B10000_30x60_v100.npy")
    B31 = math.sinh(31 * DXI)
    g31 = box_grid(B31, 31, 62)
    P = problem(g31)
    ext = Extended(P)
    x0 = embed(x_old, g_old, P_old.dm, g31, P.dm)
    del P_old
    g64, H, _ = P.grad_hess(x0)
    gl, Wl = ext.grad_and_W(x0)
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    sd = 1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30))
    sdl = sd.astype(LDT)
    n0 = nrm(sdl * ext.src)
    A64 = (sps.diags(sd) @ H @ sps.diags(sd)).tocsc()
    y64 = P.solve_linear(A64, -(sd * g64))
    lu = spla.splu(A64)
    apply_A = lambda u: sdl * ext.hess_apply(Wl, sdl * u)
    rhs = -(sdl * gl)
    yld, rel_ld, its = gmres_ld(
        apply_A, lambda u: lu.solve(np.asarray(u, dtype=np.float64)).astype(LDT), rhs
    )
    e = {
        "res0_ld": float(nrm(sdl * gl) / n0),
        "f64_step_true_linear_rel": float(
            nrm(rhs - apply_A(y64.astype(LDT))) / nrm(rhs)
        ),
        "ld_step_true_linear_rel": rel_ld,
        "ld_gmres_its": its,
        "res_after_full_f64_step": float(
            nrm(sdl * ext.grad(x0 + sdl * y64.astype(LDT))) / n0
        ),
        "res_after_full_ld_step": float(nrm(sdl * ext.grad(x0 + sdl * yld)) / n0),
        "step_rel_diff": float(nrm(yld - y64.astype(LDT)) / nrm(yld)),
    }
    out["at_1391kpc_initial_guess"] = e
    print("check @1391 kpc initial guess:", json.dumps(e), flush=True)
    out["seconds"] = round(time.time() - t, 1)
    json.dump(out, open("ATTEMPT4_CHECK.json", "w"), indent=1)
    print("CHECK", "PASS" if c["PASS"] else "FAIL", flush=True)
    sys.exit(0 if c["PASS"] else 1)

if mode == "validate":
    t = time.time()
    B, nR, nz = 1000.0, 23, 46
    g = box_grid(B, nR, nz)
    P0 = problem(g, 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    ref = obs03(P0, xs)
    P = problem(g)
    ext = Extended(P)
    x, ok, gn, r64, log = mp_newton(P, ext, xs, "validate100")
    row = {
        "edge_kpc": 0.1 * B,
        "grid": [nR, nz],
        "static": [bool(ok1), r1, bool(ok2), r2],
        "converged": bool(ok),
        "residual_ld": gn,
        "residual_f64": r64,
        "log": log,
        "seconds": round(time.time() - t, 1),
    }
    if ok:
        o = obs03(P, x)
        mine = {
            "g_ratio_static": o["g"] / ref["g"],
            "g_ratio_phihat_flux": o["g"] / o["flux"],
            "Y_ratio": o["Y"] / ref["Y"],
        }
        committed = [
            r
            for r in json.load(open("BOX_SWEEP_C1_16x32_fixed.json"))["rows"]
            if r["edge_kpc"] == 100.0
        ][0]
        rel = {k: abs(mine[k] - committed[k]) / abs(committed[k]) for k in mine}
        tolr = {"g_ratio_static": 1e-6, "g_ratio_phihat_flux": 1e-6, "Y_ratio": 1e-5}
        row.update(
            {
                "mine": mine,
                "committed": {k: committed[k] for k in mine},
                "rel_diff": rel,
                "PASS": all(rel[k] <= tolr[k] for k in rel) and r64 <= 1e-10,
            }
        )
    else:
        row["PASS"] = False
    json.dump(row, open("ATTEMPT4_VALIDATE.json", "w"), indent=1)
    print(
        "VALIDATION",
        "PASS" if row["PASS"] else "FAIL",
        json.dumps(
            {
                k: row.get(k)
                for k in ("converged", "residual_ld", "residual_f64", "rel_diff")
            }
        ),
        flush=True,
    )
    sys.exit(0 if row["PASS"] else 1)

if mode == "ladder":
    assert (
        json.load(open("ATTEMPT4_VALIDATE.json")).get("PASS") is True
    ), "validation has not passed; the ladder may not run"
    g_prev = box_grid(1e4, 30, 60)
    P_prev = problem(g_prev)
    x_prev = np.load("cache_branch/boxsweep_B10000_30x60_v100.npy")
    out = {"prereg": "PREREG_BOX_EXTEND_2026-10-06.md Amendment 2", "rows": []}
    for n in (31, 32, 33, 34):
        t = time.time()
        Bn = math.sinh(n * DXI)
        g = box_grid(Bn, n, 2 * n)
        P = problem(g)
        ext = Extended(P)
        x0 = embed(x_prev, g_prev, P_prev.dm, g, P.dm)
        x, ok, gn, r64, log = mp_newton(P, ext, x0, f"ladder_n{n}")
        row = {
            "n": n,
            "B": Bn,
            "edge_kpc": 0.1 * Bn,
            "converged": bool(ok),
            "residual_ld": gn,
            "residual_f64": r64,
            "log": log,
            "seconds": round(time.time() - t, 1),
        }
        if ok:
            o = obs03(P, x)
            row.update(o)
            row.update(
                {
                    "g_over_flux": o["g"] / o["flux"],
                    "excess_over_GR": o["g"] / o["flux"] - 0.75,
                }
            )
            np.save(f"cache_branch/attempt4_ladder_n{n}_v100.npy", x)
        out["rows"].append(row)
        json.dump(out, open("ATTEMPT4_LADDER.json", "w"), indent=1)
        print(
            f"rung n={n} edge {0.1*Bn:.0f} kpc: converged {ok} (ld {gn:.1e}, f64 {r64:.1e})"
            + (f", e = {row['excess_over_GR']:.5f}" if ok else "")
            + f" [{row['seconds']:.0f}s]",
            flush=True,
        )
        if not ok:
            print("STOP RULE: rung did not converge; no verdict.", flush=True)
            sys.exit(2)
        del P_prev
        g_prev, P_prev, x_prev = g, P, x

if mode == "verdict":
    lad = {r["n"]: r for r in json.load(open("ATTEMPT4_LADDER.json"))["rows"]}
    r34 = lad.get(34)
    st = json.load(open("BOX_LADDER_STATIC_n34.json"))["rows"][-1]
    out = {
        "ladder_n34": (
            {
                k: r34.get(k)
                for k in (
                    "converged",
                    "residual_ld",
                    "residual_f64",
                    "g",
                    "flux",
                    "Y",
                    "excess_over_GR",
                )
            }
            if r34
            else None
        ),
        "static_n34": st,
    }
    if not r34 or not r34.get("converged"):
        out["verdict"] = "no verdict (n = 34 not converged)"
    else:
        e = r34["excess_over_GR"]
        # Amendment 1: the static reference counts if the stage actually used reached residual <= 1e-10
        # (box_ladder_c1 static: static = [ok1 (tol 1e-11), r1, ok2 (tol 1e-10), r2]; used = stage2 iff ok2)
        static_ok = (
            (st["static"][3] <= 1e-10)
            if st["used"] == "stage2"
            else (st["static"][1] <= 1e-10)
        )
        Yr = r34["Y"] / st["ref_Y"]
        out.update({"e": e, "Y_over_Y_static": Yr, "static_converged": bool(static_ok)})
        if e < -0.02:
            out["flag"] = "overshoot (e < -0.02)"
        persistent = e >= 0.156 or (static_ok and Yr >= 6.198e-5)
        converging = static_ok and e <= 0.1003 and Yr <= 2.929e-5
        out["verdict"] = (
            "persistent"
            if persistent
            else ("converging" if converging else "inconclusive")
        )
    json.dump(out, open("ATTEMPT4_VERDICT.json", "w"), indent=1)
    print(json.dumps(out, indent=1), flush=True)
