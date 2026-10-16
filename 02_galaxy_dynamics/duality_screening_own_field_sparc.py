#!/usr/bin/env python3
"""The horn the external-field reading avoids: grad chi follows each galaxy's own field.

A single field chi has one gradient at the Sun's position. Cassini needs it to be the
Galactic field there (eta ~ 2). Applied the same way inside every galaxy, chi follows the
galaxy's own field, eta(r) = g(r) / a0. This runs that case on SPARC with
    nu_eff = 1 + S(eta) (nu_std - 1),  S = 1 / (1 + eta^2),  eta = g_N(r) / a0.
g_N is used because the physical field is larger, so this is the least-screened version.
Same fitter, priors and normalisation as environment_screening.py. a0 is held fixed at two values,
then scanned over 1.0-1.6e-10 for both cases, since the own-field suppression could be partly
absorbed by a larger a0. Writes DUALITY_SCREENING_OWN_FIELD_SPARC.json.
"""
import json

import numpy as np
from scipy.optimize import minimize

import environment_screening as E
from parameter_ledger import (FD_STD, KM_TO_M, KPC_TO_M, YB_MEAN, YB_STD, YD_MEAN, YD_STD, chi2, load, v_bary_sq)
from sparc_paths import resolve_sparc_dir

S2 = lambda eta: 1 / (1 + eta**2)
A0_LIVE = 1.1607e-10


def v_own(g, a0, yd, yb, fd):
    vb2 = v_bary_sq(g, yd, yb, fd); r = g["r"] * fd
    y = np.maximum(vb2 * KM_TO_M**2 / (r * KPC_TO_M) / a0, 1e-12)
    return np.sqrt(vb2 * (1 + S2(y) * (E.nu_std(y) - 1)))


def fit_own(g, a0):
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2 + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        return chi2(g, v_own(g, a0, yd, yb, fd), pr)
    r = minimize(f, [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0], bounds=[(0.01, 5)] * nb + [(0.5, 2.0)], method="L-BFGS-B")
    return float(r.fun), nb + 1


def median_red(fits, gals):
    return float(np.median([x / max(len(g["r"]) - k, 1) for (x, k), g in zip(fits, gals)]))


if __name__ == "__main__":
    E.S = S2
    gals = load(resolve_sparc_dir(None))
    out = {"n": len(gals), "form": "S = 1/(1+eta^2), eta = g_N(r)/a0 (own field)"}
    for label, a0 in (("a0_cH0_over_2pi", E.A0_DERIVED), ("a0_live", A0_LIVE)):
        base = [E.fit1(g, a0, 0.0) for g in gals]
        own = [fit_own(g, a0) for g in gals]
        cb, co = sum(c for c, _ in base), sum(c for c, _ in own)
        worse = int(sum(o[0] > b[0] + 1e-9 for o, b in zip(own, base)))
        out[label] = {"a0": a0, "chi2_unscreened": cb, "chi2_own_field": co, "dchi2_over_s": (co - cb) / 6.09,
                      "t1_median_unscreened": median_red(base, gals), "t1_median_own_field": median_red(own, gals),
                      "galaxies_worse": worse}
        r = out[label]
        print(f"{label} a0={a0:.4e}: chi2 {cb:.1f} -> {co:.1f}  dchi2/s {r['dchi2_over_s']:+.1f}  "
              f"t1 median {r['t1_median_unscreened']:.3f} -> {r['t1_median_own_field']:.3f}  worse in {worse}/{len(gals)}")
    scan = {"a0": [], "chi2_unscreened": [], "chi2_own_field": []}
    for a0 in np.round(np.arange(1.0, 1.61, 0.1), 2) * 1e-10:
        scan["a0"].append(float(a0))
        scan["chi2_unscreened"].append(sum(E.fit1(g, a0, 0.0)[0] for g in gals))
        scan["chi2_own_field"].append(sum(fit_own(g, a0)[0] for g in gals))
        print(f"scan a0={a0:.2e}: unscreened {scan['chi2_unscreened'][-1]:.1f}  own field {scan['chi2_own_field'][-1]:.1f}")
    iu, io = int(np.argmin(scan["chi2_unscreened"])), int(np.argmin(scan["chi2_own_field"]))
    scan["best_unscreened"] = {"a0": scan["a0"][iu], "chi2": scan["chi2_unscreened"][iu]}
    scan["best_own_field"] = {"a0": scan["a0"][io], "chi2": scan["chi2_own_field"][io]}
    scan["dchi2_best_vs_best"] = scan["chi2_own_field"][io] - scan["chi2_unscreened"][iu]
    out["a0_scan"] = scan
    print(f"best unscreened {scan['chi2_unscreened'][iu]:.1f} at a0={scan['a0'][iu]:.2e}; best own field "
          f"{scan['chi2_own_field'][io]:.1f} at a0={scan['a0'][io]:.2e}; difference {scan['dchi2_best_vs_best']:+.1f}")
    json.dump(out, open("DUALITY_SCREENING_OWN_FIELD_SPARC.json", "w"), indent=1)
