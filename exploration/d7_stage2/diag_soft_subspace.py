#!/usr/bin/env python3
"""Exploratory diagnostic (no solve): at attempt 2's initial guess (the converged 1000 kpc solution zero-padded onto the
nested 31x62 grid, exactly as box_ladder_c1.py builds it), measure in Newton's own equilibrated coordinates
(y = Sd^-1 dx, A = Sd H Sd, Sd = 1/sqrt(row sums of |H|), as solve_c1.ProblemC1.newton and stage_c_c1.near_zero_modes):
  (a) fraction of the equilibrated residual r = Sd g lying in span(V), V = soft eigenvectors of sym(A) below the gap;
  (b) fraction of the Newton step y = -A^-1 r lying in span(V);
  (c) change of the observables (g/flux, Y at 0.3 kpc) and of the residual when x moves along the softest mode
      by the Newton step's own size.
Decides whether a projected-Newton attempt 3 is legitimate (residual has no soft component) or impossible (it does).
Writes SOFT_SUBSPACE_C1.json only."""

import json, math, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_c1 as C
from stage_c_c1 import observables, LABEL

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


def field_weights(P, vec):
    idx = P.dm.index
    w = {}
    for n in C.NAMES:
        m = idx[C.FIX[n]]
        w[LABEL.get(n, n)] = float(np.linalg.norm(vec[np.unique(m[m >= 0])]) ** 2)
    tot = sum(w.values()) or 1.0
    top = max(w, key=w.get)
    return top, round(w[top] / tot, 3)


t0 = time.time()
g_old = C.GridC1(30, 60, 1e-4, math.asinh(1e4), math.asinh(1e4))
P_old = problem(g_old)
x_old = np.load("cache_branch/boxsweep_B10000_30x60_v100.npy")
B31 = math.sinh(31 * DXI)
g31 = C.GridC1(31, 62, 1e-4, math.asinh(B31), math.asinh(B31))
assert abs(g31.dxi - DXI) < 1e-12
P = problem(g31)
x0 = embed(x_old, g_old, P_old.dm, g31, P.dm)

grad, H, _ = P.grad_hess(x0)
rown = np.asarray(abs(H).sum(axis=1)).ravel()
Sd = sps.diags(1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30)))
A = (Sd @ H @ Sd).tocsc()
As = (0.5 * (A + A.T)).tocsc()
asym = float(spla.norm(A - A.T) / spla.norm(A))
ev, Vall = spla.eigsh(As, k=12, sigma=0, which="LM")
order = np.argsort(np.abs(ev))
ev, Vall = ev[order], Vall[:, order]
absev = np.abs(ev)
ratios = absev[1:] / absev[:-1]
gap_at = int(np.argmax(ratios))  # cluster = modes 0..gap_at
Vc = Vall[:, : gap_at + 1]

r = Sd @ grad  # equilibrated residual (y-space)
frac_r = float(np.linalg.norm(Vc.T @ r) / np.linalg.norm(r))
y = P.solve_linear(A, -r)  # Newton step in y-space (same solve as ProblemC1.newton)
frac_y = float(np.linalg.norm(Vc.T @ y) / np.linalg.norm(y))
y_perp = y - Vc @ (Vc.T @ y)

dx_full = Sd @ y
dx_perp = Sd @ y_perp
v1 = Sd @ Vall[:, 0]
v1 *= np.linalg.norm(dx_full) / np.linalg.norm(
    v1
)  # move along the softest mode by the Newton step's own size
norm0 = np.linalg.norm(Sd @ P.src)
res = lambda gr: float(np.linalg.norm(Sd @ gr) / norm0)


def obs(x):
    k = observables(P, x)["0.3kpc"]
    return {"g_over_flux": k["g"] / k["flux"], "Y": k["Y"]}


o0, o1 = obs(x0), obs(x0 + v1)
res0 = res(grad)
res1 = res(P.grad_hess(x0 + v1, want_hess=False)[0])
res_perp_full = res(P.grad_hess(x0 + dx_perp, want_hess=False)[0])
res_full = res(P.grad_hess(x0 + dx_full, want_hess=False)[0])

out = {
    "point": "attempt-2 initial guess: 1000 kpc converged solution zero-padded onto 31x62 (1391 kpc)",
    "ndof": int(P.dm.ndof),
    "A_asymmetry_rel": asym,
    "eigs_sorted_by_abs": [float(e) for e in ev],
    "eig_fields": [field_weights(P, Vall[:, i]) for i in range(len(ev))],
    "gap_after_index": gap_at,
    "gap_ratio": float(ratios[gap_at]),
    "cluster_size": gap_at + 1,
    "a_frac_residual_in_soft": frac_r,
    "b_frac_step_in_soft": frac_y,
    "step_norm_dx": float(np.linalg.norm(dx_full)),
    "step_norm_dx_perp": float(np.linalg.norm(dx_perp)),
    "c_obs_at_x0": o0,
    "c_obs_after_soft_move": o1,
    "c_rel_change_g_over_flux": abs(o1["g_over_flux"] - o0["g_over_flux"])
    / abs(o0["g_over_flux"]),
    "c_rel_change_Y": abs(o1["Y"] - o0["Y"]) / abs(o0["Y"]),
    "residual_x0": res0,
    "residual_after_soft_move": res1,
    "residual_after_full_newton_step": res_full,
    "residual_after_projected_step": res_perp_full,
    "seconds": round(time.time() - t0, 1),
}
json.dump(out, open("SOFT_SUBSPACE_C1.json", "w"), indent=1)
print(json.dumps(out, indent=1), flush=True)
