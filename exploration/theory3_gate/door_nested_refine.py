#!/usr/bin/env python3
"""Refinement of door_nested_solution.py, 2026-11-18. [O]
The first pass assumed the Galaxy's scalar at R_sun is unscreened. Here the Milky Way is solved WITH the
Galileon (spherical enclosed-mass approximation; McMillan-2017-like baryons: Hernquist bulge 0.9e10 Msun,
a=0.6 kpc; exponential disc 5.0e10, R_d=2.6 kpc; gas 1.2e10, R_g=5 kpc), giving s(R) and s'(R) at R_sun.
Around that background the Galileon adds cof(T):d2 to the Sun's kinetic tensor:
   along e (to the GC):  A_par  = A_e (1 + L_e) + 3K s^2/R^2
   transverse:           A_perp = A_e + 3K s s'/R
A_perp <= 0 means the Sun's static problem is not elliptic. Otherwise sigma^2 = A_par/A_perp and the
stretched solution of door_nested_solution.py applies (c depends on K and sigma only). Also reported:
the model's own g(R_sun), to compare with the observed 1.9-2.4e-10 m/s^2."""
import json, math, os
import numpy as np
import door_nested_solution as D
HERE = os.path.dirname(os.path.abspath(__file__))
G = 6.674e-11; MSUN = 1.989e30; KPC = D.KPC
def M_enc(R):                                   # R in m
    r = R / KPC
    bulge = 0.9e10 * (r / (r + 0.6)) ** 2
    disc = 5.0e10 * (1 - (1 + r / 2.6) * np.exp(-r / 2.6))
    gas = 1.2e10 * (1 - (1 + r / 5.0) * np.exp(-r / 5.0))
    return (bulge + disc + gas) * MSUN
def s_screened(lam, K, R):
    eta, x, s, J1, f, L = D.tables(lam); a0m = eta * D.A0FIT
    q = G * M_enc(R) / R**2 / a0m
    lo, hi = np.zeros_like(q), np.interp(q, f, s)
    for _ in range(90):
        m = 0.5 * (lo + hi); F = np.interp(m, s, f) + K * m**3 / R**2 - q
        lo = np.where(F < 0, m, lo); hi = np.where(F >= 0, m, hi)
    return 0.5 * (lo + hi), q * a0m, a0m, (x, s, J1, L)
def diagnostics(c, sigma):
    def acc(pts):
        z = pts @ D.E_GC; rp_ = np.sqrt(np.sum(pts**2, 1) - z**2 + z**2 / sigma**2)
        return -c * (pts - (1 - 1 / sigma**2) * z[:, None] * D.E_GC[None, :]) / rp_[:, None]
    t = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    pm = np.stack([0.387 * D.AU * np.cos(t), 0.387 * D.AU * np.sin(t), 0 * t], 1)
    dg = -np.mean(np.sum(acc(pm) * pm, 1) / np.linalg.norm(pm, axis=1))
    prec = 2 * math.pi * dg * (0.387 * D.AU) ** 2 / D.GM * (100 / 0.2408) * 206264.8
    ps = pm * (9.537 / 0.387); a_s = acc(ps); bq = ps @ D.E_GC
    Qb = bq[:, None] * D.E_GC[None, :] - ps / 3; Rb = ps / np.linalg.norm(ps, axis=1)[:, None]
    coef, *_ = np.linalg.lstsq(np.stack([Qb.ravel(), Rb.ravel()], 1), a_s.ravel(), rcond=None)
    return prec, float(coef[0])
import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "DOOR_NESTED_SOLUTION.json"
DST = SRC.replace("SOLUTION", "REFINE")
res = json.load(open(os.path.join(HERE, SRC)))
out = []
for row in res["runs"]:
    lam, K = row["lambda_s"], row["K_m2"]
    if lam > 3.5:
        continue
    R = D.R_SUN * np.array([0.99, 1.0, 1.01])
    sv, gh, a0m, (x, s, J1, L) = s_screened(lam, K, R)
    se, sp_ = sv[1], (sv[2] - sv[0]) / (R[2] - R[0])
    g_model = gh[1] + a0m * se
    xe = np.interp(se, s, x); Ae = np.interp(xe, x, J1); Le = np.interp(xe, x, L)
    A_par = Ae * (1 + Le) + 3 * K * se**2 / R[1] ** 2
    A_perp = Ae + 3 * K * se * sp_ / R[1]
    rec = {"lambda_s": lam, "K_m2": K, "first_pass": row["all_pass"], "sparc_dchi2": row["sparc"]["dchi2_total"],
           "g_model_Rsun": g_model, "g_in_observed_band": 1.9e-10 <= g_model <= 2.4e-10,
           "s_e": se, "dlns_dlnR": sp_ * R[1] / se, "A_par": A_par, "A_perp": A_perp}
    if A_perp <= 0:
        rec["verdict"] = "non-elliptic at R_sun"
    else:
        sigma = math.sqrt(A_par / A_perp); c = (D.GM * sigma * a0m**2 / K) ** (1 / 3)
        prec, q2 = diagnostics(c, sigma)
        rec.update({"sigma": sigma, "c": c, "mercury_prec": prec, "mercury_ok": prec <= D.PREC_MAX,
                    "saturn_Q2_eff": q2, "saturn_ok": D.Q2_LO <= q2 <= D.Q2_HI})
    rec["pass_all"] = bool(rec.get("mercury_ok") and rec.get("saturn_ok") and rec["sparc_dchi2"] <= 0 and rec["g_in_observed_band"])
    out.append(rec)
    print(f"lam={lam:4.1f} K={K:.1e} g(Rsun)={g_model:.2e} dlns/dlnR={rec['dlns_dlnR']:+.2f} A_par={A_par:.2f} A_perp={A_perp:+.2f} "
          + (f"sigma={rec['sigma']:.2f} c={rec['c']:.1e} prec={rec['mercury_prec']:.1e} Q2={rec['saturn_Q2_eff']:.1e}" if 'sigma' in rec else rec.get('verdict', ''))
          + f" sparc={rec['sparc_dchi2']:.0f} PASS={rec['pass_all']}", flush=True)
json.dump(out, open(os.path.join(HERE, DST), "w"), indent=1, default=float)
print("any pass:", any(r["pass_all"] for r in out))
