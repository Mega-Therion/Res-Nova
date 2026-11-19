"""Robustness of the knife-edge Law A / c_vis^2=0 ISW pass (1.593 vs gate 1.6):
denser k grid and every integer ell in the pre-registered range [2, 30]."""
import sys, json, numpy as np
from concurrent.futures import ProcessPoolExecutor
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weyl_causal_envelope as W
NK = int(sys.argv[1]); W.K_GRID = np.geomspace(1e-4, 0.2, NK); W.ELL_ISW = list(range(2, 31))
pts = W.get_parameter_points()["points"]
mid = NK // 2
def specs():
    out = {}
    for law in ("C_Fd0", "A_freefall"):
        for bg in ("Pantheon+_best", "DES-Dovekie_best"):
            for c2 in (0.0, 0.1, 1/3):
                out[f"{law}|{bg}|cvis2={c2:.3f}"] = dict(law=law, bg_name=bg, closure="hu98", c_vis2=c2, v_flux="bulk_rest", ic_W="adiabatic", **pts[bg])
    return out
with ProcessPoolExecutor(max_workers=4) as pool:
    L = pts["LCDM_control"]
    t = [("LCDM", i, float(k), L["h"], L["Om"], 0.0, "C_Fd0", "hu98", 0.0, "bulk_rest", "adiabatic", False) for i, k in enumerate(W.K_GRID)]
    r = {x[1]: x for x in pool.map(W._solve_single_mode, t)}
    lobs = W.compute_observables_for_run(L["h"], L["Om"], 0.0, np.vstack([r[i][3] for i in range(NK)]), np.vstack([r[i][4] for i in range(NK)]))
    summ = W.build_and_run_runs(specs(), pool, lobs)
res = {}
for k, v in summ.items():
    isw = v.get("ISW_ratio_by_ell", {})
    lens = v.get("lens_ratio_by_L") or {kk: vv for kk, vv in v.items() if "lens" in kk.lower() and isinstance(vv, (int, float))}
    if isw:
        im = max(isw, key=isw.get)
        res[k] = dict(isw_max=isw[im], ell_at_max=im, isw_min=min(isw.values()), isw_ell2=isw["2"], A=v.get("A_phiphi_mean"))
    else:
        res[k] = dict(stable=v.get("linear_stable"))
    print(k, res[k], flush=True)
json.dump(res, open(f"{sys.argv[2]}", "w"), indent=1)
