#!/usr/bin/env python3
"""Muse frozen Batch 1A. mu_n family, n = 1.0 .. 8.0 step 0.5.

Both a0. Tier 0 and tier 1. Q2 at both g_e. Pass band [-2.0, +5.2]e-27 s^-2.
Delta is against nu_2 at the same a0. A point passes only if all four
|delta| values are < 1 and both Q2 values are inside the band.
"""

import json
import os
from pathlib import Path

os.environ.setdefault(
    "SPARC_DATA_DIR",
    "/home/mega/Chyren/3_research/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data",
)

import numpy as np

from cassini_sparc_joint import fit, gals, n as NPTS, nu_n, summ
from efe_quadrupole_q2 import A0_DERIVED, Q2

A0_FIT = 1.1607e-10
A0S = (("fitted", A0_FIT), ("derived", A0_DERIVED))
NS = [1.0 + 0.5 * i for i in range(15)]
GES = (1.9e-10, 2.4e-10)
Q2_LO, Q2_HI = -2.0e-27, 5.2e-27


def one(nu, a0):
    row = {}
    for tier in (0, 1):
        c, k = zip(*[fit(g, nu, a0, tier) for g in gals])
        row[f"tier{tier}"] = summ(c, k, NPTS)
    return row


def main():
    base = {}
    nu2 = nu_n(2)
    for name, a0 in A0S:
        base[name] = one(nu2, a0)
        print(f"baseline nu_2 {name} {base[name]}", flush=True)
    rows = []
    for nval in NS:
        nu = nu_n(nval)
        for aname, a0 in A0S:
            sparc = one(nu, a0)
            q = {}
            cass = True
            for ge in GES:
                q2, qq = Q2(nu, a0, ge)
                q[str(ge)] = {"Q2": float(q2), "q": float(qq)}
                cass = cass and Q2_LO <= q2 <= Q2_HI
            deltas = {}
            ok_sparc = True
            for tier in ("tier0", "tier1"):
                for stat in ("median", "agg"):
                    d = sparc[tier][stat] - base[aname][tier][stat]
                    deltas[f"{tier}_{stat}"] = float(d)
                    ok_sparc = ok_sparc and abs(d) < 1.0
            row = {
                "n": nval,
                "a0": aname,
                "a0_value": a0,
                "sparc": sparc,
                "delta_vs_nu2": deltas,
                "Q2": q,
                "sparc_gate": ok_sparc,
                "cassini_gate": cass,
                "joint": bool(ok_sparc and cass),
            }
            rows.append(row)
            print(
                f"n={nval:<4} {aname:8} sparc={ok_sparc} cassini={cass} joint={row['joint']}",
                flush=True,
            )
    passing = [r for r in rows if r["joint"]]
    out = {
        "spec": "Muse frozen Batch 1A, n=1..8 step 0.5",
        "Q2_window": [Q2_LO, Q2_HI],
        "baseline_nu2": base,
        "n_galaxies": len(gals),
        "rows": rows,
        "n_joint": len(passing),
        "verdict": "JOINT" if passing else "NO_JOINT_POINT",
    }

    def clean(obj):
        if isinstance(obj, dict):
            return {k: clean(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [clean(v) for v in obj]
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return obj

    dest = Path(__file__).resolve().parent / "FROZEN_BATCH1A.json"
    dest.write_text(json.dumps(clean(out), indent=1) + "\n")
    print(out["verdict"], len(passing), dest, flush=True)


if __name__ == "__main__":
    main()
