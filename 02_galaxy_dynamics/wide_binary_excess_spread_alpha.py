"""Control-only spread fit WITH a free velocity scale alpha.

wide_binary_excess_spread.py fits the control bin on absolute v~ histograms with
no scale freedom; the Newtonian baseline already runs ~9% fast there, so its
control-frozen parameters land on grid edges. Here alpha multiplies the model
speeds during the control fit only, so the companion parameters are not steered
by the baseline offset. Ratios R are anchored to 500-1000 AU, so alpha cancels in
the test-bin prediction. Fit sees 500-2000 AU only (blinded to test bins).
Output: WIDE_BINARY_EXCESS_SPREAD_ALPHA.json
"""
import json
import sys

import numpy as np

import wide_binary_excess_spread as X
import wide_binary_fish as F

A_GRID = np.linspace(0.50, 1.10, 61)


def fit_control_alpha(s, M, vt, rng):
    cv, cs, cM = X.newton_cloud(s, M, rng)
    obs = vt[(vt > 0) & (vt < 5)]
    best = None
    for f_c in X.F_GRID:
        for v in X.V_GRID:
            for sg in X.SIG_GRID:
                pred0 = X.apply_spread(cv, cs, cM, f_c, v, sg, rng)
                for a in A_GRID:
                    sc = X.loglike(obs, pred0 * a)
                    if best is None or sc > best["loglike"]:
                        best = dict(f_c=float(f_c), v_med_kms=float(v), sigma_log=float(sg),
                                    alpha=float(a), loglike=sc)
    return best


def main(npz):
    c = dict(np.load(npz))
    out = {}
    for name, cut in F.CUTS.items():
        b = F.prepare(c, cut)
        rng = np.random.default_rng(20261006)
        ctrl = (b["s"] >= 500) & (b["s"] < 2000)
        fit = fit_control_alpha(b["s"][ctrl], b["M"][ctrl], b["vt"][ctrl], rng)
        rows = X.ratios(b["s"], b["M"], b["vt"], fit["f_c"], fit["v_med_kms"], fit["sigma_log"], rng)
        null = X.ratios(b["s"], b["M"], b["vt"], 0.0, 0.1, 0.3, rng)
        out[name] = dict(fit=fit, rows=rows, newton_rows=null)
        print(name, fit)
        for r, n in zip(rows, null):
            print("  ", r["bin"], round(r["R_observed"], 3), "model", round(r["R_model"], 3),
                  "newton", round(n["R_model"], 3))
    json.dump(out, open("WIDE_BINARY_EXCESS_SPREAD_ALPHA.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
