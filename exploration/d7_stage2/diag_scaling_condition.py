#!/usr/bin/env python3
"""Exploratory diagnostic for option 1 (field rescaling), no solve. Does a better diagonal scaling of the wind
Hessian lift the soft band, i.e. lower the condition number kappa = |eig|max / |eig|min of sym(D H D)?
Scalings compared at the cached converged 1000 kpc fixed-sweep state (30x60) and at attempt 2's initial guess
(1000 kpc solution zero-padded onto 31x62):
  rowsum : D = 1/sqrt(row sums of |H|)       (what ProblemC1.newton uses today)
  jacobi : D = 1/sqrt(|H_ii|), rowsum fallback where H_ii = 0
  ruiz   : symmetric Ruiz equilibration (20 sweeps of D <- D / sqrt(max_j |D_i H_ij D_j|))
A diagonal scaling does not change the exact Newton step, only the roundoff in solving for it. So a scaling that
lowers kappa by >= 100x would make option 1 viable; one that does not means the near-singularity is intrinsic.
Writes SCALING_CONDITION_C1.json only."""

import json, math, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_c1 as C

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
V_W = 100 / 299792.458
DXI = math.asinh(1e4) / 30


def problem(g):
    return C.ProblemC1(g, V_W, C.plummer_fn(M, b), 0.0)


def embed(x_old, g_old, dm_old, g_new, dm_new):
    oj = (g_new.nz - g_old.nz) // 2
    a_old = dm_old.to_nodes(x_old).reshape(C.NF, g_old.nR + 1, g_old.nz + 1, 4)
    a_new = np.zeros((C.NF, g_new.nR + 1, g_new.nz + 1, 4))
    a_new[:, : g_old.nR + 1, oj : oj + g_old.nz + 1, :] = a_old
    return dm_new.from_nodes(a_new.reshape(C.NF, g_new.nnode, 4))


def scalings(H):
    absH = abs(H).tocsr()
    rown = np.asarray(absH.sum(axis=1)).ravel()
    d_row = 1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30))
    diag = np.abs(H.diagonal())
    d_jac = np.where(
        diag > diag.max() * 1e-30, 1.0 / np.sqrt(np.maximum(diag, 1e-300)), d_row
    )
    d = np.ones(H.shape[0])
    for _ in range(20):
        S = sps.diags(d) @ absH @ sps.diags(d)
        rmax = np.asarray(S.max(axis=1).todense()).ravel()
        d = d / np.sqrt(np.maximum(rmax, 1e-300))
    return {"rowsum": d_row, "jacobi": d_jac, "ruiz": d}


def kappa(H, d):
    A = (sps.diags(d) @ H @ sps.diags(d)).tocsc()
    As = (0.5 * (A + A.T)).tocsc()
    lmax = float(
        np.max(
            np.abs(
                spla.eigsh(As, k=1, which="LM", return_eigenvectors=False, maxiter=5000)
            )
        )
    )
    lmin_all = spla.eigsh(As, k=4, sigma=0, which="LM", return_eigenvectors=False)
    lmin = float(np.min(np.abs(lmin_all)))
    return {"lam_max": lmax, "lam_min": lmin, "kappa": lmax / lmin}


out = {"rows": []}
t0 = time.time()
g_old = C.GridC1(30, 60, 1e-4, math.asinh(1e4), math.asinh(1e4))
P_old = problem(g_old)
x_old = np.load("cache_branch/boxsweep_B10000_30x60_v100.npy")
B31 = math.sinh(31 * DXI)
g31 = C.GridC1(31, 62, 1e-4, math.asinh(B31), math.asinh(B31))
P31 = problem(g31)
x31 = embed(x_old, g_old, P_old.dm, g31, P31.dm)
for label, P, x in (
    ("1000kpc_converged_30x60", P_old, x_old),
    ("1391kpc_attempt2_guess_31x62", P31, x31),
):
    _, H, _ = P.grad_hess(x)
    for name, d in scalings(H).items():
        t = time.time()
        k = kappa(H, d)
        row = {
            "point": label,
            "scaling": name,
            **k,
            "seconds": round(time.time() - t, 1),
        }
        out["rows"].append(row)
        json.dump(out, open("SCALING_CONDITION_C1.json", "w"), indent=1)
        print(
            f"{label:30s} {name:7s} lam_max {k['lam_max']:.3e} lam_min {k['lam_min']:.3e} kappa {k['kappa']:.3e}",
            flush=True,
        )
print(f"total {time.time()-t0:.0f}s", flush=True)
