#!/usr/bin/env python3
"""Cassini as an a0 discriminator: sweep a0 per shape, find the Cassini edge in a0,
and score SPARC at every a0.

Pre-registration: CASSINI_A0_BOUNDARY_PREREG_2026-10-27.md (committed before any number).
Reuses the joint-scan families, admissibility test, Cassini scorer settings and SPARC fitter.
Writes CASSINI_A0_BOUNDARY.json (rows streamed to CASSINI_A0_BOUNDARY.partial.jsonl).
Run: python3 02_galaxy_dynamics/cassini_a0_boundary.py  (~40 min, 5 workers)
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

from cassini_sparc_joint_scan import BASE, GES, GRID_RES, HI, LO, admissible, make  # noqa: E402
from qumond_axisym_efe import A0_DERIVED, A0_FIT, Q2_richardson  # noqa: E402

NAMED = {"derived": A0_DERIVED, "fitted": A0_FIT}
A0_GRID = sorted([round(0.90e-10 + 0.025e-10 * k, 14) for k in range(17)] + list(NAMED.values()))
SHAPES = ([("a", (n,)) for n in (2.0, 3.0, 4.0, 5.0, 6.0)]
          + [("b", p) for p in ((5.0, 0.25), (6.0, 0.0), (6.0, 0.25), (6.0, 0.5), (8.0, 0.25))]
          + [("c", (2.0, 10.0)), ("c", (2.0, 3.1623))])
COMPS = ("tier0_median", "tier0_agg", "tier1_median", "tier1_agg")
_SP = {}


def sparc(nu, a0):
    if not _SP:
        import cassini_sparc_joint as c
        _SP["c"] = c
    c = _SP["c"]
    out = {}
    for t in (0, 1):
        chi, k = zip(*[c.fit(g, nu, a0, t) for g in c.gals])
        assert np.all(np.isfinite(chi)), "NaN/inf chi2"
        s = c.summ(chi, k, c.n)
        out[f"tier{t}_median"], out[f"tier{t}_agg"] = s["median"], s["agg"]
    return out


def cassini(nu, a0):
    q = {}
    for ge in GES:
        qx, _, err = Q2_richardson(nu, a0, ge, **GRID_RES)
        q[str(ge)] = {"Q2": float(qx), "err": float(err)}
    st = []
    for v in q.values():
        x, e = v["Q2"], v["err"]
        st.append("in" if LO + 3 * e < x < HI - 3 * e else ("out" if (x > HI + 3 * e or x < LO - 3 * e) else "edge"))
    verdict = "FAIL" if "out" in st else ("PASS" if all(s == "in" for s in st) else "INCONCLUSIVE")
    return q, verdict


def task(args):
    fam, p, a0 = args
    try:
        nu = make(fam, p)
        ok, _ = admissible(nu)
        row = {"family": fam, "params": list(p), "a0": a0, "admissible": ok}
        if not ok:
            return row
        q, cv = cassini(nu, a0)
        row.update({"sparc": sparc(nu, a0), "Q2": q, "Q2_max": max(v["Q2"] for v in q.values()), "cassini": cv})
        return row
    except Exception as exc:  # recorded on the row, not swallowed
        return {"family": fam, "params": list(p), "a0": a0, "error": repr(exc)}


def qmax_minus_hi(fam, p, a0):
    nu = make(fam, p)
    return max(Q2_richardson(nu, a0, ge, **GRID_RES)[0] for ge in GES) - HI


def edges_for(args):
    fam, p, pts = args
    pts = sorted(pts)
    roots = []
    for (a1, f1), (a2, f2) in zip(pts, pts[1:]):
        if f1 == 0:
            roots.append(a1)
        elif f1 * f2 < 0:
            roots.append(brentq(lambda a: qmax_minus_hi(fam, p, a), a1, a2, xtol=1e-14))
    return {"family": fam, "params": list(p), "cassini_edges_a0": roots}


def main():
    t0 = time.time()
    jobs = [(f, p, a) for f, p in SHAPES for a in A0_GRID]
    part = HERE / "CASSINI_A0_BOUNDARY.partial.jsonl"
    rows = []
    with Pool(5) as pool, open(part, "w") as fh:
        for row in pool.imap_unordered(task, jobs, chunksize=1):
            rows.append(row)
            fh.write(json.dumps(row, default=float) + "\n")
            fh.flush()
    print(f"grid done {time.time() - t0:.0f}s", flush=True)
    good = [r for r in rows if r.get("admissible") and "error" not in r]

    def key(r):
        return (r["family"], tuple(r["params"]))

    by = {}
    for r in good:
        by.setdefault(key(r), []).append(r)
    for k in by:
        by[k].sort(key=lambda r: r["a0"])

    # 1. Cassini edges in a0
    with Pool(5) as pool:
        edges = pool.map(edges_for, [(k[0], k[1], [(r["a0"], r["Q2_max"] - HI) for r in v]) for k, v in by.items()])
    print(f"edges done {time.time() - t0:.0f}s", flush=True)

    # 2. SPARC reference: nu_2 at its own best a0 (tier-1 aggregate)
    nu2 = by[("a", (2.0,))]
    ref_row = min(nu2, key=lambda r: r["sparc"]["tier1_agg"])
    R = ref_row["sparc"]

    # 3./4. acceptance and preferred a0
    for r in good:
        d = {c: r["sparc"][c] - R[c] for c in COMPS}
        r["delta_bestref"] = d
        r["sparc_gate_bestref"] = all(abs(v) < 1 for v in d.values())
        r["joint_bestref"] = bool(r["sparc_gate_bestref"] and r["cassini"] == "PASS")
        for nm, a in NAMED.items():
            if r["a0"] == a:
                r["frozen_delta_" + nm] = {c: r["sparc"][c] - BASE[nm][c.split("_")[0]][c.split("_")[1]] for c in COMPS}

    per_shape = []
    for k, v in by.items():
        e = next(x for x in edges if (x["family"], tuple(x["params"])) == k)["cassini_edges_a0"]
        pref = min(v, key=lambda r: r["sparc"]["tier1_agg"])
        jt = [r["a0"] for r in v if r["joint_bestref"]]
        where = []
        for a in e:
            where.append("below_derived" if a < A0_DERIVED else ("between" if a < A0_FIT else "above_fitted"))
        per_shape.append({
            "family": k[0], "params": list(k[1]), "cassini_edges_a0": e, "edge_position": where,
            "cassini_pass_a0": [r["a0"] for r in v if r["cassini"] == "PASS"],
            "sparc_bestref_pass_a0": [r["a0"] for r in v if r["sparc_gate_bestref"]],
            "joint_a0": jt,
            "joint_contains": {nm: (a in jt) for nm, a in NAMED.items()},
            "sparc_preferred_a0": pref["a0"], "tier1_agg_at_preferred": pref["sparc"]["tier1_agg"],
            "min_max_abs_delta_over_cassini_pass": (min(max(abs(x) for x in r["delta_bestref"].values())
                                                        for r in v if r["cassini"] == "PASS")
                                                    if any(r["cassini"] == "PASS" for r in v) else None),
        })

    joint_shapes = [s for s in per_shape if s["joint_a0"]]
    if not joint_shapes:
        verdict = "NO_JOINT_REGION"
    else:
        picks = set()
        clean = True
        for s in joint_shapes:
            inn = [nm for nm, b in s["joint_contains"].items() if b]
            if len(inn) != 1:
                clean = False
            picks.update(inn)
        verdict = "A0_DISCRIMINATES" if clean and len(picks) == 1 else "JOINT_REGION"

    out = {"prereg": "CASSINI_A0_BOUNDARY_PREREG_2026-10-27.md", "band": [LO, HI], "named_a0": NAMED,
           "a0_grid": A0_GRID, "grid_resolution": GRID_RES,
           "sparc_reference": {"shape": "nu_2", "a0": ref_row["a0"], "summaries": R},
           "per_shape": per_shape, "rows": rows, "verdict": verdict,
           "n_errors": sum(1 for r in rows if "error" in r), "runtime_s": time.time() - t0}
    (HERE / "CASSINI_A0_BOUNDARY.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps({k: out[k] for k in ("sparc_reference", "per_shape", "verdict", "n_errors")}, indent=1, default=float))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
