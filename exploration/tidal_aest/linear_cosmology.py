#!/usr/bin/env python3
"""Item 2: the QUMOND-type sector on linear cosmological perturbations (2026-11-19). [D] scaling, [O] numbers.
On FRW the sector vanishes (no spatial gradients). On a perturbation, u = |grad psi|^2/a0^2 with psi = -Phi_N(pert),
and the phantom source is div[(nu - 1) S grad Phi_N] with nu - 1 ~ (a0/g)^(1/2) as g -> 0. That is non-analytic and
SUB-linear in amplitude, so unlike AeST's AQUAL Y^(3/2) term (D5 3.1, second order) it does NOT vanish at linear order.
Its size is quantified per mode, and the tidal coordinate x of linear modes is compared with SPARC's lowest x."""
import glob, json, math, os
import numpy as np
c = 2.99792458e8; a0 = 1.1607e-10; Mpc = 3.0857e22; KPC = 3.0857e19; H0 = 67.4e3 / Mpc; Om = 0.315; h = 0.674
nu = lambda y: np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2)))
# linear rms amplitude per log k at z=0: Delta^2(k) ~ (k/k_nl)^(n_eff) crude: Delta(0.01 h/Mpc)=0.05, Delta(0.1)=0.6, Delta(0.2)~1
modes = {}
for kh, Delta in ((0.005, 0.02), (0.01, 0.05), (0.03, 0.2), (0.1, 0.6)):
    k = kh * h / Mpc
    tid = 1.5 * Om * H0**2 * Delta            # |grad grad Phi| ~ k^2 Phi
    g = tid / k                               # |grad Phi|
    modes[f"k={kh}h/Mpc"] = {"g": g, "nu_minus_1": float(nu(g / a0) - 1), "x": c**2 * tid / a0**2}
# SPARC: lowest tidal coordinate over all points, using |T| ~ sqrt(g'^2 + 2 (g/r)^2) from the observed curve
xs = []
for p in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../02_galaxy_dynamics/sparc_data/*_rotmod.dat"))):
    d = np.loadtxt(p); R = d[:, 0] * KPC; V = d[:, 1] * 1e3
    if len(R) < 3: continue
    g = V**2 / R; gp = np.gradient(g, R); T = np.sqrt(gp**2 + 2 * (g / R) ** 2)
    xs.append(float((c**2 * T / a0**2).min()))
xs = np.array(xs)
out = {"linear_modes_z0": modes,
       "sparc_min_x": {"min": float(xs.min()), "p5": float(np.percentile(xs, 5)), "median": float(np.median(xs))},
       "note": "x* = 7.04e11 screens the Solar System; linear modes and SPARC are both far below it (S = 1)."}
xmax_lin = max(m["x"] for m in modes.values())
out["band_gap_factor"] = float(xs.min() / xmax_lin)
out["verdict"] = ("Linear modes get an O(10) phantom boost (nu - 1 >> 1) unless screened. A low-x cut would need "
                  f"x_low between max linear-mode x ({xmax_lin:.1f}) and SPARC min x ({xs.min():.1f}); gap factor {xs.min()/xmax_lin:.1f}.")
print(json.dumps(out, indent=1)); json.dump(out, open("LINEAR_COSMOLOGY.json", "w"), indent=1)
