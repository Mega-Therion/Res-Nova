#!/usr/bin/env python3
"""Milky Way dwarfs: does environmental screening S = 1 - mu_std(g_ext/a0) survive?

Data: Local Volume Database (Pace 2025, CC0; dwarf_data/lvdb_dwarf_mw.csv), MW satellites with a
measured (not upper-limit) velocity dispersion. Stars only, M/L_V = 2 (also 1, 3).
Predictions (McGaugh & Milgrom 2013, ApJ 775, 139), derived a0:
  sigma_N^2   = G M / (3 r_h)                       Newtonian, stars only
  sigma_iso   = (4 G M a0 / 81)^(1/4)                isolated deep MOND
  sigma_efe^2 = G M / (3 r_h mu_std(eta))            external-field dominated, eta = g_ext/a0
  sigma_MOND  = min(sigma_iso, sigma_efe)            (the EFE can only lower the isolated value)
  screened:  sigma^2 = sigma_N^2 [1 + S(eta)(B - 1)],  B = sigma_MOND^2 / sigma_N^2
g_ext = V_MW^2 / D_gc, V_MW = 200 km/s (180 / 220 bracketed). r_h circularized.
Score: chi2 on log10(sigma) with the measurement error plus 0.1 dex intrinsic scatter.
"""
import csv, json
import numpy as np
from efe_quadrupole_q2 import A0_DERIVED

G = 6.674e-11; PC = 3.0857e16; MSUN = 1.989e30
mu = lambda x: x / np.sqrt(1 + x**2)
S = lambda eta: 1 - mu(eta)

def load():
    out = []
    for r in csv.DictReader(open("dwarf_data/lvdb_dwarf_mw.csv")):
        try:
            if r.get("confirmed_galaxy") not in ("1", "1.0", "True"): continue
            dm = float(r["distance_modulus"]); mv = float(r["apparent_magnitude_v"]); rh = float(r["rhalf"])
            sig = float(r["vlos_sigma"]); em = float(r["vlos_sigma_em"]); ep = float(r["vlos_sigma_ep"])
        except (ValueError, KeyError, TypeError):
            continue
        if not (sig > 0 and em > 0 and ep > 0): continue
        ell = float(r["ellipticity"]) if r.get("ellipticity") not in ("", None, "nan") else 0.0
        if not np.isfinite(ell): ell = 0.0
        d = 10 ** (dm / 5 + 1) * PC
        rh_m = np.radians(rh / 60) * d * np.sqrt(1 - ell)
        MV = mv - dm; L = 10 ** (-0.4 * (MV - 4.83))
        ra, dec = np.radians(float(r["ra"])), np.radians(float(r["dec"]))
        # galactocentric distance (Sun at 8.2 kpc toward l=0): convert equatorial -> galactic
        x = np.array([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)])
        Rg = np.array([[-0.0548755604, -0.8734370902, -0.4838350155], [0.4941094279, -0.4448296300, 0.7469822445], [-0.8676661490, -0.1980763734, 0.4559837762]])
        gxyz = Rg @ x * d
        dgc = np.linalg.norm(gxyz - np.array([8.2e3 * PC, 0, 0]))
        out.append({"name": r["name"], "D_gc_kpc": dgc / PC / 1e3, "L": L, "rh_pc": rh_m / PC, "sig": sig, "em": em, "ep": ep})
    return out

def predict(d, ml, vmw, a0):
    M = ml * d["L"] * MSUN; rh = d["rh_pc"] * PC
    ge = (vmw * 1e3) ** 2 / (d["D_gc_kpc"] * 1e3 * PC); eta = ge / a0
    sN2 = G * M / (3 * rh)
    siso = (4 * G * M * a0 / 81) ** 0.25
    sefe = np.sqrt(sN2 / mu(eta))
    sM = min(siso, sefe)
    B = sM**2 / sN2
    sS = np.sqrt(sN2 * (1 + S(eta) * (B - 1)))
    return {"eta": eta, "S": S(eta), "N": np.sqrt(sN2) / 1e3, "MOND": sM / 1e3, "SCR": sS / 1e3}

def score(ds, model, ml, vmw, a0, subset=None):
    c = 0.0; n = 0
    for d in ds:
        p = predict(d, ml, vmw, a0)
        if subset and not subset(p): continue
        lo = np.log10(d["sig"]); e = 0.5 * (np.log10(d["sig"] + d["ep"]) - np.log10(max(d["sig"] - d["em"], 1e-3)))
        c += (lo - np.log10(p[model])) ** 2 / (e**2 + 0.1**2); n += 1
    return c, n

if __name__ == "__main__":
    ds = load(); a0 = A0_DERIVED
    print(f"{len(ds)} MW dwarfs with measured dispersions")
    out = {"n": len(ds), "rows": [], "scores": {}}
    for d in sorted(ds, key=lambda d: d["D_gc_kpc"]):
        p = predict(d, 2.0, 200, a0); out["rows"].append({**d, **p})
    for ml in (1.0, 2.0, 3.0):
        for vmw in (180, 200, 220):
            for label, sub in (("all", None), ("eta>0.3", lambda p: p["eta"] > 0.3), ("eta<0.15", lambda p: p["eta"] < 0.15)):
                key = f"ML{ml}_V{vmw}_{label}"
                res = {m: score(ds, m, ml, vmw, a0, sub) for m in ("N", "MOND", "SCR")}
                out["scores"][key] = {m: {"chi2": v[0], "n": v[1]} for m, v in res.items()}
                if vmw == 200:
                    print(f"M/L={ml} V=200 {label:8s} n={res['N'][1]:2d}  chi2  Newton {res['N'][0]:7.1f}  MOND {res['MOND'][0]:7.1f}  MOND+screen {res['SCR'][0]:7.1f}")
    print("\nclosest dwarfs (M/L=2, V=200):  name  D_gc  eta  S  sigma_obs  Newton  MOND  screened")
    for r in out["rows"][:14]:
        print(f"  {r['name'][:22]:22s} {r['D_gc_kpc']:6.1f} {r['eta']:5.2f} {r['S']:4.2f}  {r['sig']:5.2f}(+{r['ep']:.2f}/-{r['em']:.2f})  {r['N']:5.2f} {r['MOND']:5.2f} {r['SCR']:5.2f}")
    json.dump(out, open("DWARF_SCREENING_TEST.json", "w"), indent=1, default=float)
