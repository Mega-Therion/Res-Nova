#!/usr/bin/env python3
"""Item 2 decisive scan: low-x cut x_low vs (a) linear growth today, D/D_LCDM within 2% for k = 0.005-0.1 h/Mpc, and
(b) SPARC, the fraction of points with S_low < 0.9 (MOND part suppressed by more than 10%)."""
import glob, json, math, os
import numpy as np
from linear_growth import D_final, lin
c = 2.99792458e8; a0 = 1.1607e-10; KPC = 3.0857e19
xs = []
for p in sorted(glob.glob("../../02_galaxy_dynamics/sparc_data/*_rotmod.dat")):
    d = np.loadtxt(p); R = d[:, 0] * KPC; V = d[:, 1] * 1e3
    if len(R) < 3: continue
    g = V**2 / R; gp = np.gradient(g, R); xs.extend(list(c**2 * np.sqrt(gp**2 + 2 * (g / R) ** 2) / a0**2))
xs = np.array(xs)
out = {}
for xl in (5e3, 1e4, 3e4, 1e5, 3e5, 1e6):
    growth = {n: D_final(m["x"], m["g"], xl) / D_final(m["x"], m["g"], None) for n, m in lin.items()}
    S = 1 / (1 + (xl / xs) ** 2)
    out[f"{xl:.0e}"] = {"max_growth_ratio": max(growth.values()), "sparc_frac_S_lt_0.9": float((S < 0.9).mean()),
                        "sparc_frac_S_lt_0.5": float((S < 0.5).mean())}
    print(f"x_low={xl:.0e}: growth max {max(growth.values()):.3f}; SPARC points S<0.9: {100*(S<0.9).mean():.1f}%, S<0.5: {100*(S<0.5).mean():.1f}%", flush=True)
json.dump(out, open("XLOW_SCAN.json", "w"), indent=1)
