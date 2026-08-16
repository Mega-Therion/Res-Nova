#!/usr/bin/env python3
"""NFW with the cosmological concentration prior actually applied.

The parameter ledger let c roam freely in [1,100]. 97 of 171 galaxies railed at
the c<=1 floor - the fitter trying to erase the central cusp. That makes the
unconstrained NFW chi2 a fit to a halo population that LCDM simulations do not
produce, so it is not a fair row in the ledger.

Simulations give c ~ 5-20 with ~0.11 dex scatter at fixed mass (Dutton &
Maccio 2014). Applying that as a prior is what LCDM is actually committed to.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from parameter_ledger import (YD_MEAN, YD_STD, YB_MEAN, YB_STD,
                              FD_STD, load, v_nfw, chi2)
from sparc_paths import resolve_sparc_dir

LOGC_MEAN, LOGC_STD = math.log10(10.0), 0.11   # Dutton & Maccio 2014


def fit(g, prior):
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd = t[0]; yb = t[1] if g["has_bulge"] else 0.0
        fd, c, v200 = t[-3], t[-2], t[-1]
        pr = ((yd-YD_MEAN)/YD_STD)**2 + ((fd-1)/FD_STD)**2
        if g["has_bulge"]: pr += ((yb-YB_MEAN)/YB_STD)**2
        if prior: pr += ((math.log10(max(c,1e-3))-LOGC_MEAN)/LOGC_STD)**2
        return chi2(g, v_nfw(g, yd, yb, fd, c, v200), pr)
    best = None
    for c0, v0 in ((10.,100.),(5.,200.),(15.,50.),(8.,300.)):
        x0 = [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0, c0, v0]
        b = [(0.01,5)]*nb + [(0.5,2.0),(1.0,100.0),(10.0,500.0)]
        r = minimize(f, x0, bounds=b, method="L-BFGS-B")
        if best is None or r.fun < best: best, bx = float(r.fun), r.x
    return best, bx, nb+3


def main() -> None:
    ap = argparse.ArgumentParser(description="Fit NFW halos with/without cosmological concentration prior.")
    ap.add_argument("--data-dir", default=None, help="Path to SPARC rotmod directory")
    ap.add_argument("--out", default="NFW_CONSTRAINED.json", help="Output JSON filename")
    args = ap.parse_args()

    sparc_dir = resolve_sparc_dir(args.data_dir)
    gals = load(sparc_dir)
    out = {}
    for label, prior in (("NFW_free_c", False), ("NFW_cosmological_c_prior", True)):
        per, cs, tot, pts, free = [], [], 0.0, 0, 0
        for g in gals:
            c2, bx, nf = fit(g, prior)
            npts = len(g["r"]); per.append(c2/max(npts-nf,1))
            cs.append(bx[-2]); tot += c2; pts += npts; free += nf
        per = np.array(per); cs = np.array(cs)
        out[label] = {"median_reduced_chi2": float(np.median(per)),
                      "frac_under_1": int((per<1).sum()),
                      "total_free_params": int(free),
                      "median_c": float(np.median(cs)),
                      "n_railed_c_low": int((cs<=1.01).sum())}
        print(f"{label:26s} median={np.median(per):6.2f}  free={free}  "
              f"median_c={np.median(cs):6.2f}  railed_low={int((cs<=1.01).sum()):3d}")
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
