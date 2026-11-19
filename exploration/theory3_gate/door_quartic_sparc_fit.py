#!/usr/bin/env python3
"""Quartic-Vainshtein screening vs SPARC with per-galaxy mass-to-light refit (2026-11-18). [O]
Heuristic as in VAINSHTEIN_PREQ: spherical enclosed mass, the MOND part of the RAR acceleration
suppressed by u, u + (r_V(M)/r)^6 u^3 = 1, r_V(M)^3 = r_V_sun^3 * M/Msun. Not a field solution.
Each galaxy: Ups_disk=0.5f, Ups_bul=0.7f, prior log10 f ~ N(0, 0.1); chi2 minimised over f for
unscreened and screened predictions. Output: Delta chi2 per Sun Vainshtein radius."""
import glob, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
G = 4.30091e-6; a0 = 1.1607e-10 / 3.2408e-14
F = np.logspace(-0.5, 0.5, 201)
def u_of(s):
    u = np.minimum(1.0, np.where(s > 0, s, 1.0) ** (-1 / 3))
    for _ in range(80):
        u = u - (s * u**3 + u - 1) / (3 * s * u**2 + 1)
    return u
def vpred(R, Vg, Vd, Vb, f, rho_V):
    Vb2 = np.abs(Vg) * Vg + 0.5 * f * np.abs(Vd) * Vd + 0.7 * f * np.abs(Vb) * Vb
    Vb2 = np.maximum(Vb2, 1e-6)
    gN = Vb2 / R; gM = gN / (1 - np.exp(-np.sqrt(gN / a0)))
    if rho_V is None:
        return np.sqrt(gM * R)
    u = u_of(((Vb2 * R / G) / R**3 / rho_V) ** 2)
    return np.sqrt((gN + u * (gM - gN)) * R)
gals = []
for f in sorted(glob.glob(os.path.join(HERE, "../../02_galaxy_dynamics/sparc_data/*_rotmod.dat"))):
    d = np.loadtxt(f); gals.append((os.path.basename(f)[:-11], d))
def fit(d, rho_V):
    R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    eV = np.maximum(eV, 1.0)
    chi = [np.sum(((V - vpred(R, Vg, Vd, Vb, f, rho_V)) / eV) ** 2) + (np.log10(f) / 0.1) ** 2 for f in F]
    i = int(np.argmin(chi)); return chi[i], F[i]
base = {n: fit(d, None) for n, d in gals}
chi_base = sum(c for c, _ in base.values())
out = {"chi2_unscreened_total": chi_base, "N_points": int(sum(len(d) for _, d in gals)), "scan": {}}
for rV in (1.088, 1.2, 1.4, 1.7, 2.0, 2.361):
    rho_V = 1.0 / (rV * 1e-3) ** 3
    dchi = {}; fshift = []
    for n, d in gals:
        c, fbest = fit(d, rho_V); dchi[n] = c - base[n][0]; fshift.append(np.log10(fbest / base[n][1]))
    v = np.array(list(dchi.values()))
    worst = sorted(dchi.items(), key=lambda t: -t[1])[:5]
    out["scan"][f"rV_sun={rV}pc"] = {"delta_chi2_total": float(v.sum()), "galaxies_dchi2>9": int((v > 9).sum()),
        "galaxies_dchi2>25": int((v > 25).sum()), "median_dlog10_Ups": float(np.median(fshift)),
        "worst": [(n, round(float(x), 1)) for n, x in worst]}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "DOOR_QUARTIC_SPARC_FIT.json"), "w"), indent=1)
