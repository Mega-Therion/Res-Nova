#!/usr/bin/env python3
"""Exploratory: look for a second (held) steady state at satellite speed by deflation.

Deflation (Farrell, Birkisson & Funke 2015, SIAM J. Sci. Comput. 37, A2026) multiplies the residual F by
M(x) = prod_i [(|x - x_i*| / D0)^-p + shift] over the known solutions x_i*, so Newton cannot return to any of them.
The deflated Newton step is the ordinary Newton step scaled by tau = 1 / (1 - (grad M . dx) / M), where
(grad M . dx) / M = sum_i [-p m_i (d_i . dx) / |d_i|^2] / (m_i + shift), m_i = (|d_i| / D0)^-p, d_i = x - x_i*.
Convergence is judged on the undeflated residual, which is the steady-state equation itself.

Protocol: PREREG_DEFLATION_C1.md, committed before the first run.
Usage: deflation_c1.py selftest | run
"""

import json, math, sys, time
import numpy as np
import scipy.sparse as sps

P_EXP, SHIFT = 2.0, 1.0


def deflation_ratio(x, dx, roots, D0, p=P_EXP, shift=SHIFT):
    """(grad M . dx) / M for M = prod_i [(|x - r_i| / D0)^-p + shift]."""
    s = 0.0
    for r in roots:
        d = x - r
        dd = float(d @ d)
        m = (math.sqrt(dd) / D0) ** (-p)
        s += (-p * m * float(d @ dx) / dd) / (m + shift)
    return s


def deflation_M(x, roots, D0, p=P_EXP, shift=SHIFT):
    M = 1.0
    for r in roots:
        M *= (np.linalg.norm(x - r) / D0) ** (-p) + shift
    return M


# ------------------------------------------------------------------ self-test (gate D0)


def _dense_deflated_newton(F, J, x0, roots, D0, tol=1e-12, maxit=100):
    x = x0.astype(float).copy()
    for it in range(maxit):
        f = F(x)
        if np.linalg.norm(f) < tol:
            return x, True, it
        dx = np.linalg.solve(J(x), -f)
        tau = 1.0 / (1.0 - deflation_ratio(x, dx, roots, D0)) if roots else 1.0
        x = x + tau * dx
    return x, False, maxit


def selftest():
    ok = True
    # (a) the scaled step equals the Newton step of the explicitly deflated system G = M F
    rng = np.random.default_rng(7)
    n = 6
    A = rng.normal(size=(n, n)) + n * np.eye(n)
    F = lambda x: A @ x + 0.1 * x**3 - 1.0
    J = lambda x: A + np.diag(0.3 * x**2)
    roots = [rng.normal(size=n), rng.normal(size=n)]
    D0 = 1.7
    worst = 0.0
    for _ in range(20):
        x = rng.normal(size=n)
        dx = np.linalg.solve(J(x), -F(x))
        step = dx / (1.0 - deflation_ratio(x, dx, roots, D0))
        M = deflation_M(x, roots, D0)
        gM = np.zeros(n)  # grad M by central differences
        for k in range(n):
            e = np.zeros(n)
            e[k] = 1e-6
            gM[k] = (
                deflation_M(x + e, roots, D0) - deflation_M(x - e, roots, D0)
            ) / 2e-6
        JG = M * J(x) + np.outer(F(x), gM)
        explicit = np.linalg.solve(JG, -M * F(x))
        worst = max(worst, np.linalg.norm(step - explicit) / np.linalg.norm(explicit))
    a_pass = worst < 1e-6
    print(
        f"D0(a) scaled step vs explicit deflated Newton, 20 points: worst rel. diff {worst:.2e} -> {'PASS' if a_pass else 'FAIL'}"
    )
    ok &= a_pass
    # (b) two-root system: undeflated Newton finds (1, 1); deflating it, Newton from the same start finds (-1, -1)
    F2 = lambda x: np.array([x[0] ** 2 - 1.0, x[1] - x[0]])
    J2 = lambda x: np.array([[2 * x[0], 0.0], [-1.0, 1.0]])
    x0 = np.array([0.5, 0.5])
    r1, c1, _ = _dense_deflated_newton(F2, J2, x0, [], 1.0)
    r2, c2, _ = _dense_deflated_newton(F2, J2, x0, [r1], 1.0)
    b_pass = c1 and c2 and np.allclose(r1, [1, 1]) and np.allclose(r2, [-1, -1])
    print(
        f"D0(b) two-root system: undeflated -> {np.round(r1, 6)}, deflated -> {np.round(r2, 6)} -> {'PASS' if b_pass else 'FAIL'}"
    )
    ok &= b_pass
    return ok


# ------------------------------------------------------------------ production run


def deflated_newton(P, x0, roots, D0, tol=1e-10, maxit=60):
    """ProblemC1.newton (row-norm equilibration, backtracking) with the step scaled by tau and the line search on the
    deflated residual M(x) |F(x)|. Returns (x, converged, undeflated residual, iterations).
    """
    x = x0.copy()
    grad, H, _ = P.grad_hess(x)
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    Sd = sps.diags(1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30)))
    norm0 = np.linalg.norm(Sd @ P.src)
    res = lambda gr: np.linalg.norm(Sd @ gr) / norm0
    for it in range(maxit):
        gn = res(grad)
        if gn < tol:
            return x, True, gn, it
        A = (Sd @ H @ Sd).tocsr()
        step = Sd @ P.solve_linear(A, -(Sd @ grad))
        tau = 1.0 / (1.0 - deflation_ratio(x, step, roots, D0))
        step = tau * step
        fd = deflation_M(x, roots, D0) * gn
        lam = 1.0
        while True:
            xt = x + lam * step
            gt, _, _ = P.grad_hess(xt, want_hess=False)
            if deflation_M(xt, roots, D0) * res(gt) < fd * (1 - 1e-4 * lam):
                break
            lam *= 0.5
            if lam < 1e-4:
                return x, False, gn, it
        x = xt
        grad, H, _ = P.grad_hess(x)
    return x, False, res(grad), maxit


def run():
    import solve_c1 as C
    from stage_c_c1 import observables

    vf = 10 / 299792.458
    b = 3e-4
    M = 12 * math.pi * vf**4 / C.A0T
    B, nR, nz, vk = 100.0, 16, 32, 100.0
    out = {
        "protocol": "PREREG_DEFLATION_C1.md",
        "box_B": B,
        "edge_kpc": 0.1 * B,
        "grid": [nR, nz],
        "v_kms": vk,
        "g_e_over_a0": 0.0,
        "p": P_EXP,
        "shift": SHIFT,
        "tol": 1e-10,
        "maxit": 60,
    }
    t0 = time.time()
    g = C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    ref = observables(P0, xs)
    P = C.ProblemC1(g, vk / 299792.458, rho, 0.0)
    xstar, oks, rs = P.newton(xs, tol=1e-10, maxit=40, verbose=False)
    k = "0.3kpc"

    def describe(x):
        ob = observables(P, x)
        return {
            "Y_ratio": ob[k]["Y"] / ref[k]["Y"],
            "g_ratio_static": ob[k]["g"] / ref[k]["g"],
        }

    D0 = float(np.linalg.norm(xs - xstar))
    star = describe(xstar)
    # gate D1: the stripped root reproduces the committed box-sweep row (16x32, 10 kpc) and its cached solution
    cached = np.load("cache_branch/boxsweep_B100_16x32_v100.npy")
    d1 = {
        "static": [bool(ok1), r1, bool(ok2), r2],
        "stripped_converged": bool(oks),
        "stripped_residual": rs,
        "Y_ratio": star["Y_ratio"],
        "g_ratio_static": star["g_ratio_static"],
        "rel_dist_to_cached": float(
            np.linalg.norm(xstar - cached) / np.linalg.norm(cached)
        ),
    }
    d1["pass"] = bool(
        oks
        and abs(star["Y_ratio"] / 0.0372 - 1) < 0.01
        and abs(star["g_ratio_static"] / 0.1732 - 1) < 0.01
        and d1["rel_dist_to_cached"] < 1e-6
    )
    out["gate_D1"] = d1
    out["D0_static_to_stripped"] = D0
    print(
        f"gate D1: stripped root converged {oks} ({rs:.1e}); Y/Y_static {star['Y_ratio']:.4f}, g/g_static "
        f"{star['g_ratio_static']:.4f}; |x*-cached|/|cached| {d1['rel_dist_to_cached']:.1e} -> {'PASS' if d1['pass'] else 'FAIL'}",
        flush=True,
    )
    if not d1["pass"]:
        json.dump(out, open("DEFLATION_C1_10kpc_16x32.json", "w"), indent=1)
        sys.exit(1)

    guesses = [("G1 static held", xs), ("G2 static, Lambda frozen", x1)] + [
        (f"G{3 + i} x* + {a:g}(xs - x*)", xstar + a * (xs - xstar))
        for i, a in enumerate((0.5, 0.75, 0.9, 1.25))
    ]
    roots, found = [xstar], []
    out["runs"] = []
    for name, x0 in guesses:
        t = time.time()
        x, ok, gn, its = deflated_newton(P, x0, roots, D0)
        row = {
            "guess": name,
            "converged": bool(ok),
            "residual": gn,
            "iterations": its,
            "dist_to_stripped_over_D0": float(np.linalg.norm(x - xstar) / D0),
            "seconds": round(time.time() - t, 1),
        }
        if ok:
            row.update(describe(x))
            dists = [float(np.linalg.norm(x - r) / D0) for r in roots]
            row["distinct"] = bool(min(dists) > 0.05)
            if row["distinct"]:
                yr = row["Y_ratio"]
                row["class"] = (
                    "held"
                    if yr >= 0.25
                    else (
                        "intermediate" if yr >= 3 * star["Y_ratio"] else "stripped-like"
                    )
                )
                roots.append(x)
                found.append(row)
                np.save(
                    f"cache_branch/deflation_B{B:g}_{nR}x{nz}_v{vk:g}_{len(found)}.npy",
                    x,
                )
        out["runs"].append(row)
        print(
            f"{name}: converged {ok} ({gn:.1e}, {its} it), |x-x*|/D0 {row['dist_to_stripped_over_D0']:.3f}"
            + (
                f", Y/Y_static {row['Y_ratio']:.4f}, g/g_static {row['g_ratio_static']:.4f}, distinct {row['distinct']}"
                + (f", {row['class']}" if row.get("distinct") else "")
                if ok
                else ""
            )
            + f" [{row['seconds']:.0f}s]",
            flush=True,
        )
        json.dump(out, open("DEFLATION_C1_10kpc_16x32.json", "w"), indent=1)
    out["second_states_found"] = len(found)
    out["held_found"] = any(r.get("class") == "held" for r in found)
    out["seconds_total"] = round(time.time() - t0, 1)
    json.dump(out, open("DEFLATION_C1_10kpc_16x32.json", "w"), indent=1)
    print(
        f"second steady states found: {len(found)}; held among them: {out['held_found']}  [{out['seconds_total']:.0f}s]"
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run()
    else:
        sys.exit(0 if selftest() else 1)
