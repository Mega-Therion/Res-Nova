#!/usr/bin/env python3
"""Joint Cassini x SPARC scan over interpolating-function shape families.

Pre-registration: CASSINI_SPARC_JOINT_SCAN_PREREG_2026-10-27.md (commit 6be3885).
Record: CASSINI_SPARC_JOINT_SCAN_2026-10-27.md. Writes CASSINI_SPARC_JOINT_SCAN.json.

Gates are the frozen Batch-1A gates: Cassini via qumond_axisym_efe.py (PR #194, reused),
SPARC via cassini_sparc_joint.fit/summ against FROZEN_BATCH1A.json baseline_nu2 (read only).
numpy/scipy only. Run: python3 02_galaxy_dynamics/cassini_sparc_joint_scan.py  (~40 min, 6 workers)
"""
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

os.environ.setdefault(
    "SPARC_DATA_DIR",
    "/home/mega/Chyren/3_research/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data",
)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

from qumond_axisym_efe import A0_DERIVED, A0_FIT, Q2_richardson, nu_n  # noqa: E402

A0S = {"fitted": A0_FIT, "derived": A0_DERIVED}
GES = (1.9e-10, 2.4e-10)
LO, HI = -2.0e-27, 5.2e-27
BASE = json.loads((HERE / "FROZEN_BATCH1A.json").read_text())["baseline_nu2"]
COMPS = ("tier0_median", "tier0_agg", "tier1_median", "tier1_agg")
GRID_RES = dict(n_r=2000, n_th=100)
PROD_RES = dict(n_r=4000, n_th=200)


# ---------------------------------------------------------------- families
def nu_gb(g, b):
    """nu_{gamma,beta}(y) = (1 - e^{-y^{g/2}})^{-1/g} + b e^{-y^{g/2}}  (FM2012 sec. 6.2 union)."""
    def nu(y):
        y = np.maximum(np.asarray(y, dtype=float), 1e-300)
        E = np.exp(-y ** (g / 2.0))
        return (-np.expm1(-y ** (g / 2.0))) ** (-1.0 / g) + b * E

    def m1(y):
        y = np.maximum(np.asarray(y, dtype=float), 1e-300)
        z = y ** (g / 2.0)
        E = np.exp(-z)
        with np.errstate(divide="ignore", invalid="ignore"):
            first = np.where(z < 30, np.expm1(-np.log(-np.expm1(-z)) / g), np.expm1(-np.log1p(-E) / g))
        return first + b * E

    nu.minus_1 = m1
    return nu


def nu_tc(n, yc):
    """Tail-cut nu_n (diagnostic construction): 1 + (nu_n - 1) exp(-(y/yc)^2)."""
    base = nu_n(n)

    def m1(y):
        y = np.maximum(np.asarray(y, dtype=float), 1e-300)
        return base.minus_1(y) * np.exp(-(y / yc) ** 2)

    def nu(y):
        return 1.0 + m1(y)

    nu.minus_1 = m1
    return nu


def make(fam, p):
    if fam == "a":
        return nu_n(float(p[0]))
    if fam == "b":
        return nu_gb(float(p[0]), float(p[1]))
    return nu_tc(float(p[0]), float(p[1]))


def admissible(nu):
    y = np.logspace(-12, 8, 20001)
    v = np.asarray(nu(y), dtype=float)
    ok_f = bool(np.all(np.isfinite(v)))
    ok_1 = bool(np.all(v >= 1 - 1e-12))
    ok_m = bool(np.all(np.diff(y * v) > 0))
    return ok_f and ok_1 and ok_m, {"finite": ok_f, "nu_ge_1": ok_1, "y_nu_increasing": ok_m}


# ---------------------------------------------------------------- scorers
_SP = {}


def sparc_mod():
    if not _SP:
        import cassini_sparc_joint as c
        _SP["c"] = c
    return _SP["c"]


def sparc(nu, aname, tiers=(0, 1)):
    c = sparc_mod()
    a0 = A0S[aname]
    out = {}
    for t in tiers:
        chi, k = zip(*[c.fit(g, nu, a0, t) for g in c.gals])
        assert np.all(np.isfinite(chi)), "NaN/inf chi2"
        out[f"tier{t}"] = c.summ(chi, k, c.n)
    d = {}
    for t in tiers:
        for s in ("median", "agg"):
            d[f"tier{t}_{s}"] = float(out[f"tier{t}"][s] - BASE[aname][f"tier{t}"][s])
    return out, d


def cassini(nu, aname, res=GRID_RES):
    q = {}
    for ge in GES:
        qx, qf, err = Q2_richardson(nu, A0S[aname], ge, **res)
        q[str(ge)] = {"Q2": float(qx), "err": float(err)}
    st = []
    for v in q.values():
        x, e = v["Q2"], v["err"]
        st.append("in" if LO + 3 * e < x < HI - 3 * e else ("out" if (x > HI + 3 * e or x < LO - 3 * e) else "edge"))
    verdict = "FAIL" if "out" in st else ("PASS" if all(s == "in" for s in st) else "INCONCLUSIVE")
    return q, verdict


def safe_task(args):
    try:
        return task(args)
    except Exception as exc:  # recorded, not swallowed: the row carries the error
        fam, p, aname = args
        return {"family": fam, "params": list(p), "a0": aname, "error": repr(exc)}


def task(args):
    fam, p, aname = args
    nu = make(fam, p)
    ok, parts = admissible(nu)
    row = {"family": fam, "params": list(p), "a0": aname, "admissible": ok, "admissibility": parts}
    if not ok:
        return row
    sp, d = sparc(nu, aname)
    q, cv = cassini(nu, aname)
    row.update({"sparc": sp, "delta": d, "max_abs_delta": max(abs(v) for v in d.values()),
                "binding_delta": max(d, key=lambda k: abs(d[k])),
                "sparc_gate": all(abs(v) < 1 for v in d.values()),
                "Q2": q, "Q2_max": max(v["Q2"] for v in q.values()), "cassini": cv})
    row["joint"] = bool(row["sparc_gate"] and cv == "PASS")
    return row


# ---------------------------------------------------------------- main
def grids():
    out = []
    for n in np.arange(1.0, 10.001, 0.25):
        out.append(("a", (round(float(n), 2),)))
    for g in (0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8):
        for b in (-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0):
            out.append(("b", (float(g), float(b))))
    for n in (1.5, 2.0, 2.5):
        for k in range(13):
            out.append(("c", (n, float(10 ** (0.25 * k)))))
    return out


def boundaries_a():
    """Root-find the gate edges in n for family (a), per a0."""
    res = {}
    for aname in A0S:
        def qmax(n):
            return cassini(nu_n(n), aname)[0]

        def qm(n):
            q = qmax(n)
            return max(v["Q2"] for v in q.values()) - HI

        nC = brentq(qm, 4.0, 6.0, xtol=1e-4)

        def t0(n, comp, sign):
            return sparc(nu_n(n), aname, tiers=(0,))[1][comp] - sign

        edges = {}
        for comp in ("tier0_agg", "tier0_median"):
            lo = hi = None
            try:
                lo = brentq(lambda n: t0(n, comp, -1.0 if t0(1.5, comp, 0) < 0 else 1.0), 1.5, 2.0, xtol=1e-5)
            except ValueError:
                pass
            try:
                hi = brentq(lambda n: t0(n, comp, 1.0 if t0(2.5, comp, 0) > 0 else -1.0), 2.0, 2.5, xtol=1e-5)
            except ValueError:
                pass
            edges[comp] = [lo, hi]
        win_lo = max(e[0] for e in edges.values() if e[0] is not None)
        win_hi = min(e[1] for e in edges.values() if e[1] is not None)
        at_edges = {}
        for n in (win_lo, win_hi):
            sp, d = sparc(nu_n(n), aname)
            at_edges[f"{n:.6f}"] = {"delta": d, "Q2": qmax(n)}
        res[aname] = {"n_C_cassini_edge": nC, "tier0_edges": edges, "sparc_window_tier0": [win_lo, win_hi],
                      "all_four_at_window_edges": at_edges, "separation_nC_minus_nhi": nC - win_hi}
    return res


def main():
    t0 = time.time()
    jobs = [(f, p, a) for f, p in grids() for a in A0S]
    # Rows are appended to a JSONL file as they finish, so a crash cannot discard
    # finished work; a failing job is recorded with its error instead of
    # aborting the pool.
    part = HERE / "CASSINI_SPARC_JOINT_SCAN.partial.jsonl"
    rows = []
    with Pool(6) as pool, open(part, "w") as fh:
        for row in pool.imap_unordered(safe_task, jobs, chunksize=1):
            rows.append(row)
            fh.write(json.dumps(row, default=float) + "\n")
            fh.flush()
    print(f"grid done {time.time() - t0:.0f}s", flush=True)
    # production-resolution spot checks (pre-registered)
    spots = [("a", (10.0,)), ("b", (8.0, -0.5)), ("b", (8.0, 1.0))] + [("c", (n, 1.0)) for n in (1.5, 2.0, 2.5)]
    spot = []
    for f, p in spots:
        nu = make(f, p)
        if not admissible(nu)[0]:
            spot.append({"family": f, "params": list(p), "admissible": False})
            continue
        qg, _ = cassini(nu, "fitted", GRID_RES)
        qp, _ = cassini(nu, "fitted", PROD_RES)
        rel = max(abs(qg[k]["Q2"] - qp[k]["Q2"]) / abs(qp[k]["Q2"]) for k in qg)
        spot.append({"family": f, "params": list(p), "grid": qg, "prod": qp, "max_rel_diff": rel})
    # near-edge cross-check with the frozen gate's integrator
    from efe_quadrupole_q2 import Q2 as Q2_milgrom
    cross = []
    for r in rows:
        if not r.get("admissible"):
            continue
        for ge, v in r["Q2"].items():
            for edge in (LO, HI):
                if abs(v["Q2"] - edge) <= 2e-3 * abs(edge):
                    qm, _ = Q2_milgrom(make(r["family"], r["params"]), A0S[r["a0"]], float(ge))
                    cross.append({"family": r["family"], "params": r["params"], "a0": r["a0"], "ge": ge,
                                  "solver": v["Q2"], "milgrom": float(qm),
                                  "same_side": (v["Q2"] <= edge) == (qm <= edge)})
    bnd = boundaries_a()
    print(f"boundaries done {time.time() - t0:.0f}s", flush=True)
    summary = {}
    for fam in "abc":
        R = [r for r in rows if r["family"] == fam and r.get("admissible")]
        sp = [r for r in R if r["sparc_gate"]]
        cp = [r for r in R if r["cassini"] == "PASS"]
        jt = [r for r in R if r["joint"]]
        pts = sorted(R, key=lambda r: r["Q2_max"])
        front, best = [], np.inf
        for r in pts:
            if r["max_abs_delta"] < best:
                best = r["max_abs_delta"]
                front.append({"params": r["params"], "a0": r["a0"], "Q2_max": r["Q2_max"],
                              "max_abs_delta": r["max_abs_delta"], "binding": r["binding_delta"]})
        both = {}
        for r in jt:
            both.setdefault(tuple(r["params"]), set()).add(r["a0"])
        summary[fam] = {
            "n_rows": len([r for r in rows if r["family"] == fam]), "n_admissible_rows": len(R),
            "n_sparc_pass": len(sp), "n_cassini_pass": len(cp), "n_joint": len(jt),
            "joint_points": [r["params"] + [r["a0"]] for r in jt],
            "joint_at_both_a0": [list(k) for k, v in both.items() if len(v) == 2],
            "min_Q2max_over_sparc_pass": (min(sp, key=lambda r: r["Q2_max"]) and
                                          {k: min(sp, key=lambda r: r["Q2_max"])[k] for k in ("params", "a0", "Q2_max", "max_abs_delta")}) if sp else None,
            "min_maxdelta_over_cassini_pass": ({k: min(cp, key=lambda r: r["max_abs_delta"])[k]
                                                for k in ("params", "a0", "Q2_max", "max_abs_delta", "binding_delta", "delta")} if cp else None),
            "pareto_front": front,
        }
    out = {"prereg": "CASSINI_SPARC_JOINT_SCAN_PREREG_2026-10-27.md", "prereg_commit": "6be3885",
           "band": [LO, HI], "a0": A0S, "grid_resolution": GRID_RES, "rows": rows, "spot_checks": spot,
           "near_edge_crosscheck": cross, "boundaries_family_a": bnd, "summary": summary,
           "verdict": "JOINT" if any(s["n_joint"] for s in summary.values()) else "NO_JOINT_POINT",
           "runtime_s": time.time() - t0}
    (HERE / "CASSINI_SPARC_JOINT_SCAN.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(summary, indent=1, default=float)[:6000])
    print(out["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
