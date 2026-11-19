#!/usr/bin/env python3
"""Supply-limited / time-dependent AeST dust in clusters (PREREG_ACCRETION.md). mu_std law."""
import json, math, importlib.util, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
D = "../../02_galaxy_dynamics/clusters/"; cwd = os.getcwd(); os.chdir(D)
spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py"); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
CL = cm.load(); M200 = {}
for l in open("corasaniti2021_table1_lensing.dat"):
    if len(l) >= 50: M200[cm.norm(l[0:20])] = float(l[27:32])
os.chdir(cwd)
MPC, G, MS = cm.MPC_M, cm.G_SI, cm.MSUN; MU0 = 1.0 / (0.9895 * MPC)
law = lambda u: cm.g_mond(max(u, 0.0))
H0 = 67.4e3 / MPC; Om = 0.315; GYR = 3.156e16
age = lambda z: quad(lambda zz: 1 / ((1 + zz) * H0 * math.sqrt(Om * (1 + zz) ** 3 + 1 - Om)), z, np.inf)[0] / GYR
def solve(c, key, mu):
    M500 = c["M500"] * 1e14 * MS; fbar = c["fgas"] + 0.015
    r500 = cm.r_delta(M500, c["z"]); rc = 0.1 * r500
    r200 = cm.r_delta(M200[key] * 1e14 * MS, c["z"], 200.0); rv = r200 * (200 / 177.8) ** (1 / 3)
    norm = fbar * M500 / ((r500 / rc) - math.atan(r500 / rc)); Mb = lambda r: norm * ((r / rc) - math.atan(r / rc))
    rmin = 1e-4 * r500
    rhs = lambda r, y: [G * norm * (r**2 / rc**3) / (1 + (r / rc) ** 2) - mu**2 * r**2 * y[1], law(y[0] / r**2)]
    def shoot(P0, full=False):
        s = solve_ivp(rhs, (rmin, rv), [G * Mb(rmin), P0], method="DOP853", rtol=1e-10, atol=[1e20, 1.0], dense_output=full)
        return s if full else s.y[1, -1]
    g0 = -law(G * Mb(r500) / r500**2) * rv * 3
    grid = np.linspace(-6 * abs(g0), 2 * abs(g0), 81); F = [shoot(p) for p in grid]
    i = next(i for i in range(80) if F[i] * F[i + 1] < 0)
    s = shoot(brentq(shoot, grid[i], grid[i + 1], xtol=1e-6 * abs(g0)), True)
    R = M500 / (law(s.sol(r500)[0] / r500**2) * r500**2 / G)
    extra = (s.sol(rv)[0] - G * Mb(rv)) / G
    return R, extra / (5.36 * Mb(rv)), M500, r500
rows = []
for key, c in CL.items():
    R0, ratio0, M500, r500 = solve(c, key, MU0)
    rho500 = M500 / (4 / 3 * math.pi * r500**3); cs = math.sqrt(4 * math.pi * G * rho500) / MU0
    t_eq = r500 / cs / GYR; t_age = age(c["z"]) - age(c["z"] + 0.4)
    if ratio0 > 1:
        f = lambda s: solve(c, key, MU0 * s)[1] - 1.0
        s_cap = brentq(f, 1e-3, 1.0, xtol=1e-4); Rc = solve(c, key, MU0 * s_cap)[0]
    else:
        s_cap, Rc = 1.0, R0
    rows.append(dict(name=c["name"], R_static=R0, dust_ratio_static=ratio0, mu_scale_cap=s_cap, R_capped=Rc,
                     cs_kms=cs / 1e3, t_eq_Gyr=t_eq, t_age_Gyr=t_age, t_eq_over_age=t_eq / t_age))
md = lambda k: float(np.median([r[k] for r in rows]))
Rc = [r["R_capped"] for r in rows]
out = {"median_R_static": md("R_static"), "median_R_capped": md("R_capped"),
       "n_capped_in_0.7_1.4": int(sum(0.7 <= x <= 1.4 for x in Rc)),
       "median_t_eq_over_age": md("t_eq_over_age"), "n_t_eq_lt_0.3_age": int(sum(r["t_eq_over_age"] < 0.3 for r in rows)),
       "rows": rows}
out["verdict_a"] = "STATIC VALID" if out["n_t_eq_lt_0.3_age"] >= 9 else "STATIC NOT VALID (time dependence matters)"
R = out["median_R_capped"]
out["verdict_b"] = "CLOSES" if 0.8 <= R <= 1.25 and out["n_capped_in_0.7_1.4"] >= 9 else "FAILS"
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
for r in rows: print(f"  {r['name']:<20} R_static={r['R_static']:.2f} dust={r['dust_ratio_static']:.2f} R_cap={r['R_capped']:.2f} t_eq/age={r['t_eq_over_age']:.2f}")
json.dump(out, open("ACCRETION.json", "w"), indent=1)
