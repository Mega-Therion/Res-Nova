#!/usr/bin/env python3
"""Driver for the independent axisymmetric QUMOND EFE solver (qumond_axisym_efe.py).

Writes NONSPHERICAL_EFE_SOLVER.json:
  - convergence table (n_r, n_theta, r_max, r_min) at the pinned nu_std point
  - external anchor: Hees et al. 2016 Table 2
  - every frozen Batch-1A row (nu_n, n = 1..8 step 0.5; fitted and derived a0;
    g_e = 1.9e-10 and 2.4e-10), compared with FROZEN_BATCH1A.json as numbers
  - verdicts by the pre-registered rule (NONSPHERICAL_EFE_SOLVER_PREREG_2026-10-27.md)
The repo's Milgrom-integral code is not imported; its outputs are read from JSON.
Run: python3 02_galaxy_dynamics/nonspherical_efe_run.py   (about 15 min, numpy/scipy)
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from qumond_axisym_efe import A0_DERIVED, A0_FIT, Q2, Q2_richardson, nu_n  # noqa: E402

GES = (1.9e-10, 2.4e-10)
BAND = (-2.0e-27, 5.2e-27)
PINNED = 1.9017920212899443e-26
NR, NTH = 4000, 200  # production pair: (4000, 200) and (7999, 400), Richardson


def nubar(a):
    def f(y):
        y = np.maximum(np.asarray(y, dtype=float), 1e-300)
        return (-np.expm1(-y**a)) ** (-1 / (2 * a)) + (1 - 1 / (2 * a)) * np.exp(-y**a)
    f.minus_1 = lambda y: f(y) - 1.0  # used only for the Hees anchor
    return f


def verdict(rows):
    lo, hi = BAND
    status = []
    for q, e in rows:
        if lo + 3 * e < q < hi - 3 * e:
            status.append("in")
        elif q > hi + 3 * e or q < lo - 3 * e:
            status.append("out")
        else:
            status.append("edge")
    if "out" in status:
        return "FAIL"
    if all(s == "in" for s in status):
        return "PASS"
    return "INCONCLUSIVE"


def main():
    t0 = time.time()
    out = {"prereg": "NONSPHERICAL_EFE_SOLVER_PREREG_2026-10-27.md", "band": BAND,
           "model": "QUMOND, axisymmetric, uniform external field; not AQUAL, not AeST"}
    nu2 = nu_n(2)
    # --- convergence at the pinned point
    conv = []
    for nr in (1000, 2000, 4000, 8000, 16000):
        conv.append({"n_r": nr, "n_theta": 200, "r_min": 1e-3, "r_max": 1e3,
                     "Q2": Q2(nu2, A0_FIT, 1.9e-10, n_r=nr, n_th=200)[0]})
    for nth in (50, 100, 400):
        conv.append({"n_r": 4000, "n_theta": nth, "r_min": 1e-3, "r_max": 1e3,
                     "Q2": Q2(nu2, A0_FIT, 1.9e-10, n_r=4000, n_th=nth)[0]})
    h = np.log(1e6) / 3999
    for rmin, rmax in ((1e-3, 30.0), (1e-3, 1e2), (1e-3, 1e4), (3e-3, 1e3), (1e-4, 1e3)):
        n = int(round(np.log(rmax / rmin) / h)) + 1
        conv.append({"n_r": n, "n_theta": 200, "r_min": rmin, "r_max": rmax,
                     "Q2": Q2(nu2, A0_FIT, 1.9e-10, n_r=n, n_th=200, r_min=rmin, r_max=rmax)[0]})
    seq = [c["Q2"] for c in conv[:5]]
    diffs = np.diff(seq)
    limit = seq[-1] + diffs[-1] / 3.0
    out["convergence"] = {"rows": conv, "successive_differences": diffs.tolist(),
                          "ratios": (diffs[:-1] / diffs[1:]).tolist(),
                          "richardson_limit_from_16000": limit}
    qx, qf, err = Q2_richardson(nu2, A0_FIT, 1.9e-10, n_r=NR, n_th=NTH)
    out["pinned_check"] = {"pinned": PINNED, "solver": qx, "solver_err": err,
                           "rel_diff": (qx - PINNED) / PINNED,
                           "sigma_2026": (qx - 1.6e-27) / 1.8e-27}
    print("pinned", out["pinned_check"], flush=True)
    # --- Hees 2016 Table 2 anchor
    anc = {}
    for name, nu, a0, hq, hQ in (("nu_2", nu2, 1.60e-10, 0.10, 26e-27),
                                 ("nubar_0.5 (RAR)", nubar(0.5), 1.48e-10, 0.131, 31e-27)):
        q2, q, _ = Q2(nu, a0, 1.9e-10, n_r=NR, n_th=NTH)
        anc[name] = {"a0": a0, "Q2": q2, "minus_q": -q, "hees_Q2": hQ, "hees_minus_q": hq}
        print("anchor", name, anc[name], flush=True)
    out["hees2016_anchor"] = anc
    # --- frozen Batch 1A family
    frozen = json.loads((HERE / "FROZEN_BATCH1A.json").read_text())["rows"]
    fz = {(r["n"], r["a0"]): r for r in frozen}
    rows = []
    for n in np.arange(1.0, 8.01, 0.5):
        for aname, a0 in (("fitted", A0_FIT), ("derived", A0_DERIVED)):
            nu = nu_n(float(n))
            per = {}
            for ge in GES:
                qx, qf, err = Q2_richardson(nu, a0, ge, n_r=NR, n_th=NTH)
                ref = fz[(float(n), aname)]["Q2"][str(ge)]["Q2"]
                per[str(ge)] = {"Q2": qx, "err": err, "frozen_Q2": ref, "rel_diff_vs_frozen": (qx - ref) / ref}
            v = verdict([(per[str(g)]["Q2"], per[str(g)]["err"]) for g in GES])
            frozen_gate = fz[(float(n), aname)]["cassini_gate"]
            row = {"n": float(n), "a0": aname, "a0_value": a0, "Q2": per, "verdict": v,
                   "frozen_cassini_gate": frozen_gate,
                   "agrees_with_frozen_gate": (v == "PASS") == bool(frozen_gate)}
            rows.append(row)
            print(f"n={n:.1f} {aname:7s} " + " ".join(
                f"{per[str(g)]['Q2']:.6e}({per[str(g)]['rel_diff_vs_frozen']:+.1e})" for g in GES)
                + f" {v} frozen={frozen_gate}", flush=True)
    out["batch1a"] = rows
    out["max_abs_rel_diff_vs_frozen"] = max(abs(r["Q2"][str(g)]["rel_diff_vs_frozen"]) for r in rows for g in GES)
    out["nu6"] = [r for r in rows if r["n"] == 6.0]
    out["runtime_s"] = time.time() - t0
    (HERE / "NONSPHERICAL_EFE_SOLVER.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
