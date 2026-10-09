#!/usr/bin/env python3
"""Cross-check sparc_reproduce.py against parameter_ledger.py, two separately written code paths.

The version of this file in PR #143's first commit compared sparc_reproduce with a copy of
its own baryon formula, evaluated only at unit mass-to-light (Y = 1) and fd = 1. There
Y^2 = Y and the distance factor drops out, so it could not see the two defects that remained:
Y applied to V instead of V^2, and fd dividing R instead of scaling V_bar^2 and R.

This version checks three things on every galaxy both loaders accept:
  1. loaders agree: sparc_reproduce.load_rotmod (regex) vs parameter_ledger.load (line.split);
  2. baryonic V_bar agrees at non-unit (Yd, Yb, fd);
  3. the mu_std prediction agrees at non-unit (Yd, Yb, fd).

    python3 independent_sparc_recompute.py --data-dir <sparc_data> [--out SPARC_RECOMPUTE_VERIFICATION.json]

Tolerances: 1e-6 km/s on V_bar and 1e-3 km/s on the prediction (SPARC velocity errors are >= 1 km/s).
At fd = 1 the two paths agree to 1e-13. At fd != 1 they differ by at most ~2e-4 km/s, only at points
whose V_bar^2 is negative (net outward gas force): parameter_ledger clamps fd*V_bar^2 at 1e-12, while
sparc_reproduce clamps V_bar^2 and then scales by fd. The count of such points is reported.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parameter_ledger as pl  # noqa: E402
import sparc_reproduce as sr  # noqa: E402

# (Yd, Yb, fd): unit, SPARC prior means, and off-centre points where Y^2 != Y and fd != 1.
POINTS = [(1.0, 1.0, 1.0), (0.5, 0.7, 1.0), (0.5, 0.7, 0.9), (1.3, 0.4, 1.12), (0.25, 1.75, 0.85)]
TOL_BAR = 1e-6
TOL_PRED = 1e-3


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=sr.DEFAULT_DATA)
    ap.add_argument("--out", type=Path, default=HERE / "SPARC_RECOMPUTE_VERIFICATION.json")
    args = ap.parse_args()

    ledger = {g["name"]: g for g in pl.load(args.data_dir)}
    repro = {}
    for p in sorted(args.data_dir.glob("*_rotmod.dat")):
        g = sr.load_rotmod(p)
        if g is not None:
            repro[g["id"]] = g
    common = sorted(set(ledger) & set(repro))

    loader_diff = 0.0
    n_points = 0
    worst = {"v_bar": 0.0, "v_pred": 0.0}
    per_point = []
    for yd, yb, fd in POINTS:
        dbar = dpred = 0.0
        for name in common:
            L, R = ledger[name], repro[name]
            if len(L["r"]) != len(R["r"]):
                print(f"FAIL loader length {name}: {len(L['r'])} vs {len(R['r'])}")
                return 1
            if (yd, yb, fd) == POINTS[0]:
                n_points += len(L["r"])
                for a, b in (("r", "r"), ("vobs", "v_obs"), ("vgas", "v_gas"), ("vdisk", "v_disk"), ("vbul", "v_bulge")):
                    loader_diff = max(loader_diff, float(np.max(np.abs(L[a] - R[b]))))
            vbar_l = np.sqrt(pl.v_bary_sq(L, yd, yb, fd))
            vbar_r = np.sqrt(fd) * sr.v_baryon(R["v_gas"], R["v_disk"], R["v_bulge"], yd, yb)
            vp_l = pl.v_mond_like(L, pl.A0_HORIZON, yd, yb, fd)
            vp_r = sr.predict_velocity(sr.v_baryon(R["v_gas"], R["v_disk"], R["v_bulge"], yd, yb), R["r"], sr.A0_HORIZON, fd)
            dbar = max(dbar, float(np.max(np.abs(vbar_l - vbar_r))))
            dpred = max(dpred, float(np.max(np.abs(vp_l - vp_r))))
        per_point.append({"Yd": yd, "Yb": yb, "fd": fd, "max_abs_diff_v_bar_km_s": dbar, "max_abs_diff_v_pred_km_s": dpred})
        worst["v_bar"] = max(worst["v_bar"], dbar)
        worst["v_pred"] = max(worst["v_pred"], dpred)

    n_floor = int(sum(int(np.sum(L["vgas"] * np.abs(L["vgas"]) + L["vdisk"] ** 2 + L["vbul"] ** 2 <= 0))
                      for L in (ledger[n] for n in common)))
    ok = loader_diff == 0.0 and worst["v_bar"] <= TOL_BAR and worst["v_pred"] <= TOL_PRED
    rec = {
        "method": "sparc_reproduce.py vs parameter_ledger.py (separately written loaders and models), mu_std, a0 = cH0/2pi",
        "n_galaxies_compared": len(common),
        "n_points_compared": n_points,
        "only_in_sparc_reproduce": sorted(set(repro) - set(ledger)),
        "only_in_parameter_ledger": sorted(set(ledger) - set(repro)),
        "max_abs_diff_loaded_columns": loader_diff,
        "points": per_point,
        "points_with_negative_v_bar_sq_at_unit_ML": n_floor,
        "tolerance_km_s": {"v_bar": TOL_BAR, "v_pred": TOL_PRED},
        "agreement": ok,
    }
    args.out.write_text(json.dumps(rec, indent=2) + "\n")
    print(json.dumps(rec, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
