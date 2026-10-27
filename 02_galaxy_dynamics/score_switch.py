#!/usr/bin/env python3
"""Score an existing QUMOND switch. Defines no new interpolating function.

A candidate is either a key of cassini_sparc_joint.FUN or a callable ν(y)
the caller already has. The gates are the frozen Batch 1A gates:

  algebra residual  — Newtonian and deep-MOND ends, plus the μ_std identity
                      when the candidate is ν_2
  Cassini Q2        — both external fields, band [-2e-27, 5.2e-27] s^-2
  SPARC             — tier 0 and tier 1 reduced χ², delta against the frozen
                      ν_2 baseline, pass if every |delta| < 1
  joint             — SPARC gate and Cassini gate both true at that a0

The frozen baseline file is read and not rewritten.
"""

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault(
    "SPARC_DATA_DIR",
    "/home/mega/Chyren/3_research/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data",
)

import numpy as np

from cassini_sparc_joint import FUN, fit, gals, n as NPTS, nubar, nu_n, summ
from efe_quadrupole_q2 import A0_DERIVED, Q2

A0_FIT = 1.1607e-10
A0S = (("fitted", A0_FIT), ("derived", A0_DERIVED))
GES = (1.9e-10, 2.4e-10)
Q2_LO, Q2_HI = -2.0e-27, 5.2e-27
HERE = Path(__file__).resolve().parent
FROZEN = HERE / "FROZEN_BATCH1A.json"


def mu_std(x):
    x = np.asarray(x, dtype=float)
    return x / np.sqrt(1.0 + x * x)


def algebra_residual(nu, check_identity):
    """Max absolute miss of the ends already required by Batch 1A's family."""
    newton = abs(float(np.asarray(nu(1e8))) - 1.0)
    deep = abs(float(np.sqrt(1e-10) * np.asarray(nu(1e-10))) - 1.0)
    parts = {"newton": newton, "deep_mond": deep, "mu_std_identity": None}
    residual = max(newton, deep)
    if check_identity:
        xs = np.array([1e-3, 0.1, 1.0, 10.0, 1e3, 1e5])
        mu = mu_std(xs)
        y = xs * mu
        ident = float(np.max(np.abs(np.asarray(nu(y), dtype=float) - 1.0 / mu)))
        parts["mu_std_identity"] = ident
        residual = max(residual, ident)
    return residual, parts


def resolve(which):
    """Return (nu, label, from_fun). Unknown names are refused."""
    if which in FUN:
        return FUN[which], which, True
    if which.startswith("nu_") and which[3:].replace(".", "", 1).isdigit():
        nval = float(which[3:])
        return nu_n(nval), which, False
    if which.startswith("nubar_"):
        aval = float(which[6:])
        return nubar(aval), which, False
    raise SystemExit(
        f"unknown switch {which!r}. CLI names are FUN keys or nu_<n> / nubar_<a> "
        "from cassini_sparc_joint. This file adds no formula."
    )


def _plain(obj):
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    return obj


def score(nu, label, check_identity=None):
    if check_identity is None:
        check_identity = label in ("nu_2", "mu_std", "mu_std (nu_2)")
    baseline = json.loads(FROZEN.read_text())["baseline_nu2"]
    residual, parts = algebra_residual(nu, check_identity)
    rows = []
    for aname, a0 in A0S:
        sparc = {}
        for tier in (0, 1):
            chi, k = zip(*[fit(g, nu, a0, tier) for g in gals])
            sparc[f"tier{tier}"] = summ(chi, k, NPTS)
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
                d = float(sparc[tier][stat] - baseline[aname][tier][stat])
                deltas[f"{tier}_{stat}"] = d
                ok_sparc = ok_sparc and abs(d) < 1.0
        q2_values = [q[str(ge)]["Q2"] for ge in GES]
        rows.append(
            {
                "a0": aname,
                "a0_value": a0,
                "algebra_residual": residual,
                "Q2_max": float(max(q2_values)),
                "sparc_reduced_chi2_tier1_median": sparc["tier1"]["median"],
                "sparc_reduced_chi2_tier0_median": sparc["tier0"]["median"],
                "joint": bool(ok_sparc and cass),
                "sparc_gate": ok_sparc,
                "cassini_gate": cass,
                "Q2": q,
                "sparc": sparc,
                "delta_vs_frozen_nu2": deltas,
            }
        )
    return _plain(
        {
            "candidate": label,
            "new_formula": False,
            "control": "FROZEN_BATCH1A.json baseline_nu2",
            "algebra_residual": residual,
            "algebra_parts": parts,
            "Q2_window": [Q2_LO, Q2_HI],
            "n_galaxies": len(gals),
            "rows": rows,
            "joint_any": any(r["joint"] for r in rows),
        }
    )


def main(argv):
    p = argparse.ArgumentParser(description="Score an existing switch. No new formula.")
    p.add_argument("--which", default="nu_2", help="FUN key, nu_<n>, or nubar_<a>")
    args = p.parse_args(argv)
    nu, label, _ = resolve(args.which)
    report = score(nu, label)
    json.dump(report, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
