#!/usr/bin/env python3
"""Phase 2 (PREREG_PHASE2.md): how small must the bulk's effective Weyl viscosity be?
Law A (Phase 1), bulk_rest frame (irrelevant at c_vis^2 = 0 by J2), every integer ell in [2, 30], 25 k-modes,
c_vis^2 in {0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 0.03, 0.1} on the Pantheon+ / DES-Dovekie best fits and the Pantheon+ 2-sigma floor."""
import json, os, sys
import numpy as np
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "drag_gcosmo"))
import weyl_causal_envelope as W
W.ELL_ISW = list(range(2, 31))
NK = len(W.K_GRID)
CV = [0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 0.03, 0.1]
BG = ("Pantheon+_best", "DES-Dovekie_best", "Pantheon+_2sigma_floor")
def main():
    pts = W.get_parameter_points()["points"]
    specs = {f"A|{bg}|{c:g}": dict(law="A_freefall", bg_name=bg, closure="hu98", c_vis2=c, v_flux="bulk_rest", ic_W="adiabatic", **pts[bg])
             for bg in BG for c in CV}
    with ProcessPoolExecutor(max_workers=6) as pool:
        L = pts["LCDM_control"]
        t = [("LCDM", i, float(k), L["h"], L["Om"], 0.0, "C_Fd0", "hu98", 0.0, "bulk_rest", "adiabatic", False) for i, k in enumerate(W.K_GRID)]
        r = {x[1]: x for x in pool.map(W._solve_single_mode, t)}
        lobs = W.compute_observables_for_run(L["h"], L["Om"], 0.0, np.vstack([r[i][3] for i in range(NK)]), np.vstack([r[i][4] for i in range(NK)]))
        summ = W.build_and_run_runs(specs, pool, lobs)
    out = {}
    for key, v in summ.items():
        isw = v.get("ISW_ratio_by_ell") or {}
        if not isw:
            out[key] = {"linear_stable": v.get("linear_stable", False), "pass": False}; continue
        lens = v["A_phiphi_by_L"]
        imax = max(isw.values()); imin = min(isw.values())
        lens_ok = all(abs(x - 1.0) <= 0.08 for x in lens.values())
        out[key] = {"A_phiphi_mean": v["A_phiphi_mean"], "A_phiphi_min_max": v["A_phiphi_min_max"], "ISW_min": imin, "ISW_max": imax,
                    "ell_at_max": max(isw, key=isw.get), "pass": bool(lens_ok and 0.4 <= imin and imax <= 1.6)}
        print(key, round(imax, 4), out[key]["pass"], flush=True)
    thr = {}
    for bg in BG:
        cs = [(c, out[f"A|{bg}|{c:g}"]) for c in CV]
        passing = [c for c, o in cs if o["pass"]]
        failing = [c for c, o in cs if not o["pass"]]
        thr[bg] = {"largest_passing_cvis2": max(passing) if passing else None,
                   "smallest_failing_cvis2": min(failing) if failing else None}
        # linear interpolation of ISW_max = 1.6 crossing between bracketing grid points
        xs = [c for c, o in cs if "ISW_max" in o]; ys = [o["ISW_max"] for c, o in cs if "ISW_max" in o]
        cross = None
        for i in range(len(xs) - 1):
            if (ys[i] - 1.6) * (ys[i + 1] - 1.6) < 0:
                cross = xs[i] + (1.6 - ys[i]) * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i]); break
        thr[bg]["cvis2_at_ISW_1p6_interp"] = cross
    res = {"grid": out, "threshold": thr, "ell": "every integer ell in [2, 30]", "k_modes": NK}
    json.dump(res, open(os.path.join(HERE, "PHASE2_CVIS_THRESHOLD.json"), "w"), indent=1)
    print(json.dumps(thr, indent=1))
if __name__ == "__main__":
    main()
