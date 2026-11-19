#!/usr/bin/env python3
"""X-COP with the tidal-AeST virial screen on the MOND sector (tidal_aest/PREREG_XH_BARYONIC.md, Test B).
x_H from the BARYONIC tidal field; x_H,low = 110 (Test-A-allowed value)."""
import json, math, importlib.util, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
D = "../../02_galaxy_dynamics/clusters/"; cwd = os.getcwd(); os.chdir(D)
spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py"); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
os.chdir(cwd)
MPC, G, MS = cm.MPC_M, cm.G_SI, cm.MSUN; MU0 = 1.0 / (0.9895 * MPC)
law = lambda u: cm.g_mond(max(u, 0.0))
XHLOW = 110.0; Om = 0.315; H0 = 67.4e3 / MPC
Hz = lambda z: H0 * math.sqrt(Om * (1 + z) ** 3 + 1 - Om)
rows_in = [l.split("\t") for l in open("xcop_data.tsv") if not l.startswith("#") and l.strip()]
def shape_mass(x, xc, beta):         # integral of r^2 [1+(r/rc)^2]^(-3beta/2) from 0 to x (units of R500)
    return quad(lambda r: r**2 * (1 + (r / xc) ** 2) ** (-1.5 * beta), 0, x, limit=200)[0]
out = []
for nm, z, R5, R2, MH5, MH2, f5, f2, Mt5, Mt2 in rows_in:
    z, R5, R2 = float(z), float(R5) * MPC, float(R2) * MPC
    Mg5 = float(f5) * float(MH5) * 1e14 * MS; Mg2 = float(f2) * float(MH2) * 1e14 * MS
    Mt5, Mt2 = float(Mt5) * 1e14 * MS, float(Mt2) * 1e14 * MS
    xc = 0.1; x2 = R2 / R5; target = Mg2 / Mg5
    beta = brentq(lambda b: shape_mass(x2, xc, b) / shape_mass(1.0, xc, b) - target, 0.3, 3.0)
    rv = R2 * (200 / 177.8) ** (1 / 3); rc = xc * R5
    A = 1.09 * Mg5 / (4 * math.pi * R5**3 * shape_mass(1.0, xc, beta))   # baryon density normalisation (gas + 9% stars)
    rho = lambda r: A * (1 + (r / rc) ** 2) ** (-1.5 * beta)
    rg = np.linspace(0, rv, 4001); Mb_g = np.concatenate([[0], np.cumsum(0.5 * (4 * math.pi * rg[1:] ** 2 * rho(rg[1:]) + 4 * math.pi * rg[:-1] ** 2 * rho(rg[:-1])) * np.diff(rg))])
    Mb = lambda r: np.interp(r, rg, Mb_g)
    def solve(mu):
        rmin = 1e-4 * R5
        def Sx(r):
            gb = G * Mb(r) / r**2; gp = 4 * math.pi * G * rho(r) - 2 * gb / r
            xh = math.sqrt(gp**2 + 2 * (gb / r) ** 2) / Hz(z) ** 2
            return 1 / (1 + (XHLOW / xh) ** 2)
        glaw = lambda u, r: u + Sx(r) * (law(u) - u)
        rhs = lambda r, y: [G * 4 * math.pi * r**2 * rho(r) - mu**2 * r**2 * y[1], glaw(y[0] / r**2, r)]
        def shoot(P0, full=False):
            s = solve_ivp(rhs, (rmin, rv), [G * Mb(rmin), P0], method="DOP853", rtol=1e-8, atol=[1e21, 1.0], dense_output=full)
            return s if full else s.y[1, -1]
        g0 = -law(G * Mb(R5) / R5**2) * rv * 3
        grid = np.linspace(-6 * abs(g0), 2 * abs(g0), 41); F = [shoot(p) for p in grid]
        i = next(i for i in range(40) if F[i] * F[i + 1] < 0)
        s = shoot(brentq(shoot, grid[i], grid[i + 1], xtol=1e-6 * abs(g0)), True)
        Md = lambda r: glaw(s.sol(r)[0] / r**2, r) * r**2 / G
        return Mt5 / Md(R5), Mt2 / Md(R2), ((s.sol(rv)[0] - G * Mb(rv)) / G) / (5.36 * Mb(rv))
    Rm5 = Mt5 / (law(G * Mb(R5) / R5**2) * R5**2 / G); Rm2 = Mt2 / (law(G * Mb(R2) / R2**2) * R2**2 / G)
    S5, S2, dust = solve(MU0)
    if dust > 1:
        sc = brentq(lambda s: solve(MU0 * s)[2] - 1.0, 1e-3, 1.0, xtol=1e-4); C5, C2, _ = solve(MU0 * sc)
    else: sc, C5, C2 = 1.0, S5, S2
    r = dict(name=nm, beta=beta, fbar500=1.09 * Mg5 / Mt5, R500_pureMOND=Rm5, R200_pureMOND=Rm2, R500_static=S5, R200_static=S2,
             dust_ratio=dust, mu_scale_cap=sc, R500_capped=C5, R200_capped=C2)
    out.append(r); print(f"{nm:<9} beta={beta:.2f} fbar={r['fbar500']:.3f} MOND={Rm5:.2f}/{Rm2:.2f} static={S5:.2f}/{S2:.2f} dust={dust:.2f} capped={C5:.2f}/{C2:.2f}", flush=True)
md = lambda k: float(np.median([r[k] for r in out])); n_in = lambda k: int(sum(0.7 <= r[k] <= 1.4 for r in out))
summ = {k: {"median": md(k), "n_in_0.7_1.4": n_in(k)} for k in
        ("R500_pureMOND", "R200_pureMOND", "R500_static", "R200_static", "R500_capped", "R200_capped")}
for k in ("R500_capped", "R200_capped", "R500_static", "R200_static"):
    summ[k]["verdict"] = "CLOSES" if 0.8 <= summ[k]["median"] <= 1.25 and summ[k]["n_in_0.7_1.4"] >= 9 else "FAILS"
summ["median_dust_ratio"] = md("dust_ratio"); summ["n_dust_exceeds"] = int(sum(r["dust_ratio"] > 1 for r in out))
print(json.dumps(summ, indent=1)); json.dump({"summary": summ, "rows": out, "xH_low": XHLOW}, open("XCOP_SCREENED.json", "w"), indent=1)
