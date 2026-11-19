#!/usr/bin/env python3
"""D10 cluster attack, ideas 1-4 (PREREG.md). #1 nonperturbative virial-boundary solve; #2 two-radius shape;
#3 cosmic dust budget; #4 fully screened (Newtonian) limit."""
import json, math, importlib.util, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
D = "../../02_galaxy_dynamics/clusters/"
cwd = os.getcwd(); os.chdir(D)
spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py"); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
CL = cm.load(); M200 = {}
for l in open("corasaniti2021_table1_lensing.dat"):
    if len(l) >= 50: M200[cm.norm(l[0:20])] = (float(l[27:32]), float(l[51:55]))
os.chdir(cwd)
MPC, G, MS, A0 = cm.MPC_M, cm.G_SI, cm.MSUN, cm.A0
MU = 1.0 / (0.9895 * MPC)
LAWS = {"simple": lambda u: u + math.sqrt(A0 * max(u, 0.0)), "mu_std": lambda u: cm.g_mond(max(u, 0.0))}
def nfw_ratio(c=4.0):           # M(r200)/M(r500) for NFW with c200 = c
    m = lambda x: math.log(1 + x) - x / (1 + x)
    f = lambda y: m(c * y) / m(c) - 500 / 200 * y**3   # M(<y r200)/M200 = (500/200) y^3 at y = r500/r200
    y = brentq(f, 0.3, 0.99); return m(c) / m(c * y)
out = {"nfw_c4_M200_over_M500": nfw_ratio(4.0), "clusters": []}
for key, c in CL.items():
    M500 = c["M500"] * 1e14 * MS; fbar = c["fgas"] + 0.015
    r500 = cm.r_delta(M500, c["z"]); rc = 0.1 * r500
    m200, ratio_cat = M200[key]; r200 = cm.r_delta(m200 * 1e14 * MS, c["z"], 200.0); rv = r200 * (200 / 177.8) ** (1 / 3)
    norm = fbar * M500 / ((r500 / rc) - math.atan(r500 / rc))
    Mb = lambda r: norm * ((r / rc) - math.atan(r / rc))
    rmin = 1e-4 * r500
    row = {"name": c["name"], "fbar": fbar, "M200_over_M500_catalog": m200 / c["M500"], "catalog_col7": ratio_cat,
           "R_newton_screened": 1 / fbar}
    for lname, law in LAWS.items():
        bad = {"flag": False}
        def rhs(r, y):
            W, Phi = y
            u = W / r**2
            if u <= 0: bad["flag"] = True
            return [G * norm * (r**2 / rc**3) / (1 + (r / rc) ** 2) - MU**2 * r**2 * Phi, law(u)]
        def shoot(P0, full=False):
            bad["flag"] = False
            s = solve_ivp(rhs, (rmin, rv), [G * Mb(rmin), P0], method="DOP853", rtol=1e-10, atol=[1e20, 1.0],
                          dense_output=full)
            return (s if full else s.y[1, -1])
        g0 = -LAWS[lname](G * Mb(r500) / r500**2) * rv * 3
        grid = np.linspace(-6 * abs(g0), 2 * abs(g0), 81)
        F = [shoot(p) for p in grid]
        roots = [brentq(shoot, grid[i], grid[i + 1], xtol=1e-6 * abs(g0)) for i in range(80) if F[i] * F[i + 1] < 0]
        if not roots:
            row[lname] = {"converged": False}; continue
        P0 = roots[0]; s = shoot(P0, True); ill = bad["flag"]
        def Mdyn(r):
            W = s.sol(r)[0]; return law(W / r**2) * r**2 / G
        W_v = s.sol(rv)[0]
        row[lname] = {"converged": True, "n_roots": len(roots), "uE_positive_throughout": not ill,
                      "R": M500 / Mdyn(r500), "R_pure_MOND": M500 / (law(G * Mb(r500) / r500**2) * r500**2 / G),
                      "M200_over_M500_model": Mdyn(r200) / Mdyn(r500),
                      "M200_over_M500_pureMOND": (law(G * Mb(r200) / r200**2) * r200**2) / (law(G * Mb(r500) / r500**2) * r500**2),
                      "extra_mass_over_cosmic_dust_budget": ((W_v - G * Mb(rv)) / G) / (5.36 * Mb(rv)),
                      "mu_rv_rad": MU * rv}
    out["clusters"].append(row)
def med(lname, k):
    v = [r[lname][k] for r in out["clusters"] if r[lname].get("converged")]
    return (float(np.median(v)), len(v)) if v else (None, 0)
summ = {}
for lname in LAWS:
    Rs = [r[lname]["R"] for r in out["clusters"] if r[lname].get("converged")]
    summ[lname] = {"median_R": med(lname, "R"), "n_in_0.7_1.4": int(sum(0.7 <= x <= 1.4 for x in Rs)),
                   "all_uE_positive": all(r[lname].get("uE_positive_throughout", False) for r in out["clusters"]),
                   "median_M200_M500_model": med(lname, "M200_over_M500_model"),
                   "median_M200_M500_pureMOND": med(lname, "M200_over_M500_pureMOND"),
                   "median_extra_over_dust_budget": med(lname, "extra_mass_over_cosmic_dust_budget"),
                   "max_extra_over_dust_budget": max(r[lname]["extra_mass_over_cosmic_dust_budget"] for r in out["clusters"] if r[lname].get("converged"))}
    R, n = summ[lname]["median_R"]
    summ[lname]["verdict_1"] = ("CLOSES" if R is not None and 0.8 <= R <= 1.25 and summ[lname]["n_in_0.7_1.4"] >= 9 else "FAILS")
summ["median_M200_M500_catalog"] = float(np.median([r["M200_over_M500_catalog"] for r in out["clusters"]]))
summ["catalog_col7_equals_ratio"] = all(abs(r["M200_over_M500_catalog"] - r["catalog_col7"]) < 0.02 for r in out["clusters"])
summ["median_R_newton_screened"] = float(np.median([r["R_newton_screened"] for r in out["clusters"]]))
out["summary"] = summ
print(json.dumps(summ, indent=1))
for r in out["clusters"]:
    print(f"  {r['name']:<20} " + "  ".join(f"{l}: R={r[l]['R']:.2f} ok={r[l]['uE_positive_throughout']}" if r[l].get('converged') else f"{l}: noconv" for l in LAWS))
json.dump(out, open("D10_ATTACK.json", "w"), indent=1, default=float)
