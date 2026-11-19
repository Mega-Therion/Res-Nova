#!/usr/bin/env python3
"""Steep-nu Cassini x SPARC joint test under the honest SPARC error model (PREREG_NU_FORWARD_MODEL_JOINT.md).
Cassini verdicts: CASSINI_A0_BOUNDARY.json (unchanged). SPARC: FM-A (committed tier-1, regression) and FM-B
(per-galaxy e_D/D distance prior + intrinsic scatter sigma_int, profiled once on nu_2, then fixed)."""
import json, os, sys
from multiprocessing import Pool
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]; GD = ROOT / "02_galaxy_dynamics"
os.environ["SPARC_DATA_DIR"] = str(GD / "sparc_data")
sys.path.insert(0, str(GD)); sys.path.insert(0, str(ROOT / "audits" / "2026-11-19"))
from scipy.optimize import minimize
import cassini_sparc_joint as CSJ
from cassini_sparc_joint_scan import make
from parameter_ledger import YD_MEAN, YD_STD, YB_MEAN, YB_STD
from sparc_forward_model_ablation import parse_master
A0_GRID = sorted([round(0.90e-10 + 0.025e-10 * k, 14) for k in range(17)] + [1.0422e-10, 1.1607e-10])
SHAPES = [("a", (2.0,)), ("a", (5.0,)), ("a", (6.0,)), ("b", (6.0, 0.0)), ("b", (6.0, 0.25)), ("b", (8.0, 0.25))]
MASTER = parse_master(GD / "sparc_data" / "SPARC_Lelli2016c.mrt")
GALS = CSJ.gals
REL = [MASTER.get(g["name"], {}).get("rel_eD", 0.10) for g in GALS]
NPTS = sum(len(g["r"]) for g in GALS)

def fit_B(g, nu, a0, sig, rel):
    var = g["verr"] ** 2 + sig ** 2; nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / rel) ** 2 + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        v = CSJ.v_nu(g, nu, a0, yd, yb, fd)
        return float(np.sum((g["vobs"] - v) ** 2 / var) + pr)
    lo, hi = max(0.3, 1 - 3.5 * rel), min(3.0, 1 + 3.5 * rel)
    r = minimize(f, [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0], bounds=[(0.01, 5)] * nb + [(lo, hi)], method="L-BFGS-B")
    return float(r.fun), nb + 1

def tier0_B(g, nu, a0, sig):
    var = g["verr"] ** 2 + sig ** 2
    v = CSJ.v_nu(g, nu, a0, YD_MEAN, YB_MEAN if g["has_bulge"] else 0.0, 1.0)
    return float(np.sum((g["vobs"] - v) ** 2 / var)), 0

def logdet(sig):
    return float(sum(np.sum(np.log(g["verr"] ** 2 + sig ** 2)) for g in GALS))

def task(args):
    fam, p, a0, sig = args
    nu = make(fam, p)
    c1, k1 = zip(*[fit_B(g, nu, a0, sig, rel) for g, rel in zip(GALS, REL)])
    c0, k0 = zip(*[tier0_B(g, nu, a0, sig) for g in GALS])
    n = [len(g["r"]) for g in GALS]
    s1, s0 = CSJ.summ(c1, k1, n), CSJ.summ(c0, k0, n)
    return {"family": fam, "params": list(p), "a0": a0, "sigma_int": sig, "m2lnL_fit": float(sum(c1)),
            "tier0_median": s0["median"], "tier0_agg": s0["agg"], "tier1_median": s1["median"], "tier1_agg": s1["agg"]}

def main():
    out = {"prereg": "PREREG_NU_FORWARD_MODEL_JOINT.md", "n_gal": len(GALS), "n_pts": NPTS}
    # FM-A regression
    nu2 = make("a", (2.0,))
    c, k = zip(*[CSJ.fit(g, nu2, 1.225e-10, 1) for g in GALS])
    fmA = CSJ.summ(c, k, [len(g["r"]) for g in GALS])["agg"]
    out["FM_A_regression"] = {"tier1_agg_nu2_1.225": fmA, "committed": 6.034598428230875, "rel_diff": abs(fmA / 6.034598428230875 - 1)}
    print("FM-A regression", out["FM_A_regression"], flush=True)
    assert out["FM_A_regression"]["rel_diff"] < 1e-6, "FM-A regression failed"
    with Pool(5) as pool:
        # sigma_int: provisional 6 km/s -> nu_2 best a0 -> profile -> final
        r6 = pool.map(task, [("a", (2.0,), a0, 6.0) for a0 in A0_GRID])
        a_best = min(r6, key=lambda r: r["m2lnL_fit"])["a0"]
        prof = pool.map(task, [("a", (2.0,), a_best, s) for s in (0.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0)])
        for r in prof:
            r["m2lnL_full"] = r["m2lnL_fit"] + logdet(r["sigma_int"])
        sig = min(prof, key=lambda r: r["m2lnL_full"])["sigma_int"]
        out["sigma_int_profile"] = {"nu2_provisional_best_a0": a_best, "rows": [(r["sigma_int"], r["m2lnL_full"]) for r in prof], "sigma_int": sig}
        print("sigma_int profile ->", sig, "km/s at a0", a_best, flush=True)
        rows = pool.map(task, [(f, p, a0, sig) for f, p in SHAPES for a0 in A0_GRID])
    ref = min([r for r in rows if r["params"] == [2.0] and r["family"] == "a"], key=lambda r: r["m2lnL_fit"])
    cas = json.load(open(GD / "CASSINI_A0_BOUNDARY.json"))
    cmap = {(r["family"], tuple(r["params"]), r["a0"]): r.get("cassini") for r in cas["rows"] if "cassini" in r}
    for r in rows:
        r["delta_m2lnL"] = r["m2lnL_fit"] - ref["m2lnL_fit"]
        r["P1"] = r["delta_m2lnL"] <= 10
        r["cassini"] = cmap.get((r["family"], tuple(r["params"]), r["a0"]))
        r["joint"] = bool(r["P1"] and r["cassini"] == "PASS")
        r["secondary_gate"] = all(abs(r[c] - ref[c]) < 1 for c in ("tier0_median", "tier0_agg", "tier1_median", "tier1_agg"))
    per = []
    for f, p in SHAPES:
        v = sorted([r for r in rows if r["family"] == f and tuple(r["params"]) == p], key=lambda r: r["a0"])
        best = min(v, key=lambda r: r["m2lnL_fit"])
        cp = [r for r in v if r["cassini"] == "PASS"]
        per.append({"family": f, "params": list(p), "FMB_preferred_a0": best["a0"], "delta_at_preferred": best["delta_m2lnL"],
                    "best_delta_over_cassini_pass": (min(r["delta_m2lnL"] for r in cp) if cp else None),
                    "cassini_pass_a0": [r["a0"] for r in cp], "joint_a0": [r["a0"] for r in v if r["joint"]]})
        print(f"{f}{p}: FM-B pref a0={best['a0']:.4e} (d={best['delta_m2lnL']:+.1f}); best d over Cassini-pass = "
              f"{per[-1]['best_delta_over_cassini_pass']}; joint={per[-1]['joint_a0']}", flush=True)
    out.update({"sigma_int_kms": sig, "reference": {k: ref[k] for k in ("a0", "m2lnL_fit", "tier0_median", "tier0_agg", "tier1_median", "tier1_agg")},
                "per_shape": per, "rows": rows,
                "verdict": "JOINT_CANDIDATES" if any(s["joint_a0"] for s in per) else "NO_JOINT_UNDER_FM_B"})
    Path(__file__).with_name("NU_FORWARD_MODEL_JOINT.json").write_text(json.dumps(out, indent=1, default=float))
    print("verdict:", out["verdict"])

if __name__ == "__main__":
    main()
