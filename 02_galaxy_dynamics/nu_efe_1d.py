#!/usr/bin/env python3
"""1D collinear QUMOND external-field boost, scored against the frozen gates.

This is the aligned case of the vector formula in wide_binary_fish.boost model "E",
with the two-body factor Q set to 1. For a fixed external acceleration g_e and a
bare interpolating function nu,

    y_e * nu(y_e) = g_e / a0
    nu_E(y) = [nu(y + y_e) * (y + y_e) - nu(y_e) * y_e] / y

nu_E is the new function. The Cassini quadrupole is computed on the bare nu,
because Q2 already integrates the external field. Putting nu_E into Q2 would
count that field twice. SPARC is computed on nu_E. The frozen baseline file
is read and not rewritten.
"""

import json
import os
import sys

os.environ.setdefault(
    "SPARC_DATA_DIR",
    "/home/mega/Chyren/3_research/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data",
)

import numpy as np
from scipy.optimize import brentq

from cassini_sparc_joint import fit, gals, n as NPTS, nu_n, summ
from efe_quadrupole_q2 import Q2
from score_switch import A0S, FROZEN, GES, Q2_HI, Q2_LO, _plain

BARE = nu_n(2)


def y_external(nu, ge, a0):
    eta = ge / a0
    hi = max(eta, 1.0)
    return brentq(lambda x: x * float(nu(np.array(x))) - eta, 1e-14, hi * 4)


def nu_efe(nu, ge, a0):
    """Collinear external-field boost. Returns a callable of y = g_N / a0."""
    ye = y_external(nu, ge, a0)
    nue = float(nu(np.array(ye)))

    def out(y):
        y = np.asarray(y, dtype=float)
        s = y + ye
        return (nu(s) * s - nue * ye) / np.maximum(y, 1e-300)

    out.ye = ye
    return out


def limits(nu_e):
    newton = abs(float(np.asarray(nu_e(1e8))) - 1.0)
    deep = abs(float(np.sqrt(1e-10) * np.asarray(nu_e(1e-10))) - 1.0)
    return {"newton": newton, "deep_mond": deep, "algebra_residual": max(newton, deep)}


def main():
    baseline = json.loads(FROZEN.read_text())["baseline_nu2"]
    rows = []
    for aname, a0 in A0S:
        q = {}
        cass = True
        for ge in GES:
            q2, qq = Q2(BARE, a0, ge)
            q[str(ge)] = float(q2)
            cass = cass and Q2_LO <= q2 <= Q2_HI
        for ge in GES:
            nu = nu_efe(BARE, ge, a0)
            sparc = {}
            for tier in (0, 1):
                chi, k = zip(*[fit(g, nu, a0, tier) for g in gals])
                sparc[f"tier{tier}"] = summ(chi, k, NPTS)
            deltas = {}
            ok = True
            for tier in ("tier0", "tier1"):
                for stat in ("median", "agg"):
                    d = float(sparc[tier][stat] - baseline[aname][tier][stat])
                    deltas[f"{tier}_{stat}"] = d
                    ok = ok and abs(d) < 1.0
            rows.append(
                {
                    "a0": aname,
                    "a0_value": a0,
                    "g_e": ge,
                    "y_e": nu.ye,
                    "algebra": limits(nu),
                    "Q2_bare_nu2": q,
                    "Q2_max_bare": max(q.values()),
                    "cassini_gate_bare_nu2": bool(cass),
                    "sparc_reduced_chi2_tier1_median": sparc["tier1"]["median"],
                    "sparc_reduced_chi2_tier0_median": sparc["tier0"]["median"],
                    "sparc_gate": bool(ok),
                    "joint": bool(ok and cass),
                    "delta_vs_frozen_nu2": deltas,
                    "sparc": sparc,
                }
            )
            print(
                f"{aname} ge={ge:.2e} ye={nu.ye:.4e} "
                f"t0={sparc['tier0']['median']:.3f} t1={sparc['tier1']['median']:.3f} "
                f"sparc={bool(ok)} cassini_bare={bool(cass)} joint={bool(ok and cass)}",
                flush=True,
            )
    report = _plain(
        {
            "formula": "nu_E(y) = [nu(y+ye)*(y+ye) - nu(ye)*ye] / y",
            "bare": "nu_2",
            "n_galaxies": len(gals),
            "joint_any": any(r["joint"] for r in rows),
            "rows": rows,
        }
    )
    json.dump(report, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
