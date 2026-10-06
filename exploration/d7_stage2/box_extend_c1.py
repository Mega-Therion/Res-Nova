#!/usr/bin/env python3
"""Exploratory: extend the fixed-resolution box sweep (box_sweep_c1.py 16 32 fixed) to larger boxes, under the
pre-registration PREREG_BOX_EXTEND_2026-10-06.md (committed before the first run). Same physics and solver path as
box_sweep_c1.py; it writes NEW files only (never BOX_SWEEP_C1_*.json or cache_branch/boxsweep_*), so deflation gate D1's
cache is untouched.
Usage:
  box_extend_c1.py anchor          re-evaluate the committed 1000 kpc row from its cached solution (no re-solve)
  box_extend_c1.py <B> [<B> ...]   solve at box asinh(B) (edge ~0.1 B kpc), fixed resolution near the dwarf
Output: BOX_EXTEND_C1_16x32_fixed.json (rows appended per B), cache_branch/boxextend_B<B>_<nR>x<nz>_v100.npy."""
import json, math, os, sys, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; Q0 = 0.1
nR0 = 16
OUT = "BOX_EXTEND_C1_16x32_fixed.json"

def grid_for(B):
    nRb = max(nR0, math.ceil(nR0 * math.asinh(B) / math.asinh(100.0)))
    return nRb, 2 * nRb

def static_ref(g):
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, 0.0)
    x1, ok1, r1 = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=25, verbose=False, freeze=P0.lambda_dofs())
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    return P0, xs, (bool(ok1), r1, bool(ok2), r2)

def row_from(P, x, ref, B, nRb, nzb):
    k = "0.3kpc"; ob = observables(P, x)
    return {"box_B": B, "edge_kpc": 0.1*B, "grid": [nRb, nzb],
            "g_ratio_static": ob[k]["g"]/ref[k]["g"], "g_ratio_phihat_flux": ob[k]["g"]/ob[k]["flux"],
            "excess_over_GR": ob[k]["g"]/ob[k]["flux"] - 0.75,
            "Y_ratio": ob[k]["Y"]/ref[k]["Y"], "static_g_over_flux": ref[k]["g"]/ref[k]["flux"],
            "u_over_tilt": ob["max_u"]/((vf**2/b)/Q0)}

def save(row):
    out = json.load(open(OUT)) if os.path.exists(OUT) else {"grid0": [16, 32], "mode": "fixed", "v_kms": 100.0, "g_e_over_a0": 0.0, "rows": []}
    out["rows"].append(row); json.dump(out, open(OUT, "w"), indent=1)

if sys.argv[1] == "anchor":
    B = 10000.0; nRb, nzb = grid_for(B); t = time.time()
    g = C.GridC1(nRb, nzb, 1e-4, math.asinh(B), math.asinh(B))
    P0, xs, st = static_ref(g); ref = observables(P0, xs)
    P = C.ProblemC1(g, 100/299792.458, C.plummer_fn(M, b), 0.0)
    x = np.load(f"cache_branch/boxsweep_B{B:g}_{nRb}x{nzb}_v100.npy")
    gn = float(np.linalg.norm(P.grad_hess(x, want_hess=False)[0]))
    row = row_from(P, x, ref, B, nRb, nzb); row.update({"kind": "anchor_from_cache", "grad_norm": gn, "static": st, "seconds": round(time.time()-t, 1)})
    save(row); print(json.dumps(row, indent=1)); sys.exit(0)

for B in map(float, sys.argv[1:]):
    t = time.time(); nRb, nzb = grid_for(B)
    g = C.GridC1(nRb, nzb, 1e-4, math.asinh(B), math.asinh(B))
    P0, xs, st = static_ref(g); ref = observables(P0, xs)
    P = C.ProblemC1(g, 100/299792.458, C.plummer_fn(M, b), 0.0)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=40, verbose=True)
    row = {"box_B": B, "edge_kpc": 0.1*B, "grid": [nRb, nzb], "kind": "solve", "static": st, "converged": bool(ok), "residual": gn}
    if ok:
        row.update(row_from(P, x, ref, B, nRb, nzb)); row["converged"] = True; row["residual"] = gn
        np.save(f"cache_branch/boxextend_B{B:g}_{nRb}x{nzb}_v100.npy", x)
    row["seconds"] = round(time.time()-t, 1); save(row)
    print(f"box edge {0.1*B:g} kpc ({nRb}x{nzb}): converged {ok} ({gn:.1e})" + (f": excess {row['excess_over_GR']:.4f}, Y/Y_static {row['Y_ratio']:.3e}, g/g_static {row['g_ratio_static']:.4f}" if ok else "") + f" [{row['seconds']:.0f}s]", flush=True)
