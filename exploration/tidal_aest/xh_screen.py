#!/usr/bin/env python3
"""Item 2 resolution test: a nonlinearity screen on x_H = |grad grad Phi_N| / H^2, with H = theta/3 from the aether
expansion (covariant in AeST). Linear modes: x_H = 1.5 Om(a) Delta(a) <~ 1 at every z. Galaxies (collapsed): x_H >> 100.
S_lin = 1/(1 + (xH_low/x_H)^2). Gates: growth D/D_LCDM within 1% (k = 0.005-0.1 h/Mpc), and SPARC points with
S_lin < 0.99 at z ~ 0 (H = H0)."""
import glob, json, math
import numpy as np
from scipy.integrate import solve_ivp
c = 2.99792458e8; a0 = 1.1607e-10; KPC = 3.0857e19; Mpc = 3.0857e22; H0 = 67.4e3 / Mpc; Om = 0.315; OL = 1 - Om
nu = lambda y: math.sqrt(0.5 * (1 + math.sqrt(1 + 4 / y**2)))
lin = json.load(open("LINEAR_COSMOLOGY.json"))["linear_modes_z0"]
E2 = lambda a: Om / a**3 + OL
def growth(m, xh_low, screen=True):
    Delta0 = m["x"] * a0**2 / c**2 / (1.5 * Om * H0**2)          # recover Delta from x0
    def rhs(la, y):
        a = math.exp(la); z = 1 / a - 1; Oma = Om / a**3 / E2(a)
        g = m["g"] * (1 + z); Delta = Delta0 * a                     # matter-era linear growth (adequate to 1%)
        xh = 1.5 * Oma * Delta
        b = (nu(g / a0) - 1) * (1 / (1 + (xh_low / xh) ** 2) if screen else 0.0)
        return [y[1], -(2 - 1.5 * Oma) * y[1] + 1.5 * Oma * (1 + b) * y[0]]
    s = solve_ivp(rhs, (math.log(1e-3), 0.0), [1e-3, 1e-3], rtol=1e-9); return s.y[0, -1]
xH = []
for p in sorted(glob.glob("../../02_galaxy_dynamics/sparc_data/*_rotmod.dat")):
    d = np.loadtxt(p); R = d[:, 0] * KPC; V = d[:, 1] * 1e3
    if len(R) < 3: continue
    g = V**2 / R; gp = np.gradient(g, R); xH.extend(list(np.sqrt(gp**2 + 2 * (g / R) ** 2) / H0**2))
xH = np.array(xH)
out = {"sparc_xH": {"min": float(xH.min()), "p1": float(np.percentile(xH, 1)), "median": float(np.median(xH))}, "scan": {}}
for xl in (10.0, 40.0, 100.0, 300.0):
    gr = {n: growth(m, xl) / growth(m, xl, screen=False) for n, m in lin.items()}
    S = 1 / (1 + (xl / xH) ** 2)
    out["scan"][str(xl)] = {"max_growth_dev": max(abs(v - 1) for v in gr.values()), "sparc_frac_S_lt_0.99": float((S < 0.99).mean())}
    print(f"xH_low={xl}: max |D/D_LCDM - 1| = {max(abs(v-1) for v in gr.values()):.2e}; SPARC points S<0.99: {100*(S<0.99).mean():.2f}%")
print("SPARC x_H min/p1/median:", out["sparc_xH"])
json.dump(out, open("XH_SCREEN.json", "w"), indent=1)
