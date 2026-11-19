#!/usr/bin/env python3
"""D10 with measured ACCEPT gas profiles (PREREG_ACCEPT.md). mu_std, Phi(r_v)=0, static and supply-capped."""
import json, math, importlib.util, os
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import brentq
D = "../../02_galaxy_dynamics/clusters/"; cwd = os.getcwd(); os.chdir(D)
spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py"); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
CL = cm.load(); M200 = {}
for l in open("corasaniti2021_table1_lensing.dat"):
    if len(l) >= 50: M200[cm.norm(l[0:20])] = float(l[27:32])
prof = {}
for l in open("accept_d10_subset.dat"):
    if l.startswith("#"): continue
    p = l.split(); prof.setdefault(p[0], []).append((float(p[1]), float(p[2]), float(p[3])))
os.chdir(cwd)
MAP = {"ABELL-209": "ABELL_0209", "ABELL-383": "ABELL_0383", "ABELL-773": "ABELL_0773", "ABELL-1689": "ABELL_1689",
       "ABELL-1763": "ABELL_1763", "ABELL-2034": "ABELL_2034", "ABELL-2142": "ABELL_2142", "CL-J1226.9+3332": "CL_J1226.9+3332",
       "MACS-J0717.5+3745": "MACS_J0717.5+3745", "RXC-J0232.2-4420": "RX_J0232.2-4420", "RX-J1347.5-1145": "RX_J1347.5-1145"}
MPC, G, MS = cm.MPC_M, cm.G_SI, cm.MSUN; MU0 = 1.0 / (0.9895 * MPC); MP = 1.67262e-27; MUE = 1.17
law = lambda u: cm.g_mond(max(u, 0.0))
def gas_model(rows, rv_m):
    a = np.array(sorted(set(rows))); rm = 0.5 * (a[:, 0] + a[:, 1]); ne = a[:, 2]
    ok = ne > 0; rm, ne = rm[ok], ne[ok]
    rmax = a[:, 1].max(); sel = rm > 0.5 * rmax
    beta = -np.polyfit(np.log(rm[sel]), np.log(ne[sel]), 1)[0]
    rg = np.geomspace(1e-4, rv_m / MPC * 1.01, 6000)            # Mpc
    lne = np.interp(np.log(rg), np.log(rm), np.log(ne), left=np.log(ne[0]), right=np.nan)
    out = rg > rm[-1]; lne[out] = np.log(ne[-1]) - beta * np.log(rg[out] / rm[-1])
    rho = MUE * MP * np.exp(lne) * 1e6                         # kg/m^3
    r_m = rg * MPC; Mg = cumulative_trapezoid(4 * math.pi * r_m**2 * rho, r_m, initial=0)
    return r_m, rho, Mg, float(beta), float(rmax)
def solve(r_m, rho_b, Mb_arr, r500, rv, M500, mu):
    Mb = lambda r: np.interp(r, r_m, Mb_arr); rho = lambda r: np.interp(r, r_m, rho_b)
    rmin = r_m[1]
    rhs = lambda r, y: [G * 4 * math.pi * r**2 * rho(r) - mu**2 * r**2 * y[1], law(y[0] / r**2)]
    def shoot(P0, full=False):
        s = solve_ivp(rhs, (rmin, rv), [G * Mb(rmin), P0], method="DOP853", rtol=1e-7, atol=[1e22, 10.0], dense_output=full)
        return s if full else s.y[1, -1]
    g0 = -law(G * Mb(r500) / r500**2) * rv * 3
    grid = np.linspace(-6 * abs(g0), 2 * abs(g0), 33); F = [shoot(p) for p in grid]
    i = next(i for i in range(32) if F[i] * F[i + 1] < 0)
    s = shoot(brentq(shoot, grid[i], grid[i + 1], xtol=1e-5 * abs(g0)), True)
    R = M500 / (law(s.sol(r500)[0] / r500**2) * r500**2 / G)
    return R, ((s.sol(rv)[0] - G * Mb(rv)) / G) / (5.36 * Mb(rv))
rows = []
for key, c in CL.items():
    if c["name"] not in MAP: continue
    M500 = c["M500"] * 1e14 * MS; r500 = cm.r_delta(M500, c["z"])
    r200 = cm.r_delta(M200[key] * 1e14 * MS, c["z"], 200.0); rv = r200 * (200 / 177.8) ** (1 / 3)
    r_m, rho_g, Mg, beta, rmax = gas_model(prof[MAP[c["name"]]], rv)
    Mg500 = float(np.interp(r500, r_m, Mg)); fstar = 0.015 * M500 / Mg500
    rho_b = rho_g * (1 + fstar); Mb = Mg * (1 + fstar)
    R0, dust0 = solve(r_m, rho_b, Mb, r500, rv, M500, MU0)
    if dust0 > 1:
        s_cap = brentq(lambda s: solve(r_m, rho_b, Mb, r500, rv, M500, MU0 * s)[1] - 1.0, 1e-3, 1.0, xtol=1e-3)
        Rc = solve(r_m, rho_b, Mb, r500, rv, M500, MU0 * s_cap)[0]
    else: Rc = R0
    print(c['name'], round(R0, 3), round(Rc, 3), flush=True)
    rows.append(dict(name=c["name"], fgas_measured=Mg500 / M500, fgas_catalog=c["fgas"], beta_outer=beta,
                     rmax_measured_over_r500=rmax * MPC / r500, R_static=R0, dust_ratio=dust0, R_capped=Rc,
                     R_pureMOND=M500 / (law(G * float(np.interp(r500, r_m, Mb)) / r500**2) * r500**2 / G)))
md = lambda k: float(np.median([r[k] for r in rows]))
inband = lambda k: int(sum(0.7 <= r[k] <= 1.4 for r in rows))
out = {"N": len(rows), "median_R_pureMOND": md("R_pureMOND"), "median_R_static": md("R_static"), "n_static_in": inband("R_static"),
       "median_R_capped": md("R_capped"), "n_capped_in": inband("R_capped"),
       "median_fgas_measured_over_catalog": float(np.median([r["fgas_measured"] / r["fgas_catalog"] for r in rows])),
       "median_rmax_over_r500": md("rmax_measured_over_r500"), "rows": rows}
for k, nk in (("static", "n_static_in"), ("capped", "n_capped_in")):
    R = out[f"median_R_{k}"]; out[f"verdict_{k}"] = "CLOSES" if 0.8 <= R <= 1.25 and out[nk] >= 9 else "FAILS"
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
for r in rows: print(f"  {r['name']:<20} fgas meas/cat={r['fgas_measured']:.3f}/{r['fgas_catalog']:.3f} beta={r['beta_outer']:.2f} rmax/r500={r['rmax_measured_over_r500']:.2f} R_MOND={r['R_pureMOND']:.2f} R_static={r['R_static']:.2f} R_cap={r['R_capped']:.2f}")
json.dump(out, open("ACCEPT_RERUN.json", "w"), indent=1)
