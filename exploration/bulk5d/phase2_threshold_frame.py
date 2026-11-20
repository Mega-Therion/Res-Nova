#!/usr/bin/env python3
"""Post-amendment characterization: is the Pantheon+ c_vis^2 threshold frame-dependent?
Law A, Pantheon+ best fit, every integer ell in [2, 30], c_vis^2 in {3e-4, 5.5e-4, 1e-3}, v_flux in {bulk_rest, matter_comoving}."""
import json, os, sys
import numpy as np
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "drag_gcosmo"))
import weyl_causal_envelope as W
W.ELL_ISW = list(range(2, 31))
NK = len(W.K_GRID)
def main():
    pts = W.get_parameter_points()["points"]
    bg = "Pantheon+_best"
    specs = {f"{vf}|{c:g}": dict(law="A_freefall", bg_name=bg, closure="hu98", c_vis2=c, v_flux=vf, ic_W="adiabatic", **pts[bg])
             for vf in ("bulk_rest", "matter_comoving") for c in (3e-4, 5.5e-4, 1e-3)}
    with ProcessPoolExecutor(max_workers=6) as pool:
        L = pts["LCDM_control"]
        t = [("LCDM", i, float(k), L["h"], L["Om"], 0.0, "C_Fd0", "hu98", 0.0, "bulk_rest", "adiabatic", False) for i, k in enumerate(W.K_GRID)]
        r = {x[1]: x for x in pool.map(W._solve_single_mode, t)}
        lobs = W.compute_observables_for_run(L["h"], L["Om"], 0.0, np.vstack([r[i][3] for i in range(NK)]), np.vstack([r[i][4] for i in range(NK)]))
        summ = W.build_and_run_runs(specs, pool, lobs)
    out = {k: {"ISW_max": max(v["ISW_ratio_by_ell"].values()), "A_phiphi_mean": v["A_phiphi_mean"]} for k, v in summ.items()}
    for k, v in out.items(): print(k, round(v["ISW_max"], 4), flush=True)
    json.dump(out, open(os.path.join(HERE, "PHASE2_THRESHOLD_FRAME.json"), "w"), indent=1)
if __name__ == "__main__":
    main()
