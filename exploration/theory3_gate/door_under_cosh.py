#!/usr/bin/env python3
"""Open door re-run under the repo's ADOPTED Cosh K (TARGET_D5 §2), 2026-11-18.  Tier [O].

Supersedes small_q0_dust_check.py and sparc_mu_reach.py, which used the quadratic K that
TARGET_D5 §1.3 already excludes [D]. Under Cosh, mu (curvature at Q0) and early-time w
(width Z0, r = Z0/Q0) are carried by different parameters (D5 §2.2), and the background
depends on (mu, r, K_B) only — Q0 drops out.

Parts
  1. Cosmological floor on mu: exists r with a_* < 1, w(1e-4) <= 0.02, drift(1e-4 -> 1) <= 5.34%
     (SZ's own Planck-consistent run, D5 §2.5). Exact Cosh background, D5 §2.3.
  2. Galactic cap on mu: SZ's r_C ~ (r_M mu^-2)^(1/3) (D5 line 382) >= R_max for every SPARC
     galaxy (closes D5 §5 open item "r_C evaluated for real galaxies").
  3. Quartic-Vainshtein screening of SPARC: with Lambda fixed by the Sun window r_V in
     [1.09, 2.36] pc (OPEN_DOOR_GATE.json), how much is each galaxy's MOND boost suppressed?
"""
import glob, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SPARC = os.path.join(HERE, "../../02_galaxy_dynamics/sparc_data")

# ---------- 1. Cosh background (D5 §2.3) ----------
h, Om0, KB = 0.70, 0.26, 0.1
H0 = h / 2997.92458                                   # Mpc^-1

def w0_of(mu, kb=KB):                                 # D5 §1.3 box
    return 3 * H0**2 * Om0 / (2 * mu**2 * (2 - kb))

def bg(a, r, w0):
    A = 2 * w0 / r
    Z = np.arcsinh(A / a**3)
    y = r * a**3 * (np.cosh(Z) - 1) / A
    f = 1 + r * Z - y                                 # rho a^3 / (rho0 a^3 in quadratic limit)
    return y / f, f, A ** (1 / 3)                     # w, f, a_*

# regression: SZ's published Cosh run (K_B=0.5, Q0=0.1, K2=7.5e5, Z0=1e-3) -> D5 §2.5 numbers
mu_sz = math.sqrt(2 * 7.5e5 / 1.5) * 0.1
w0_sz = w0_of(mu_sz, 0.5)
w_sz, f4, ast_sz = bg(1e-4, 0.01, w0_sz)
_, f1, _ = bg(1.0, 0.01, w0_sz)
drift_sz = f4 / f1 - 1
assert abs(mu_sz - 100) < 1e-9 and abs(w0_sz / 1.42e-12 - 1) < 0.01
assert abs(w_sz / 9.46e-3 - 1) < 0.01 and abs(drift_sz / 0.0534 - 1) < 0.01 and abs(ast_sz / 6.6e-4 - 1) < 0.02

def feasible(mu, drift_max=drift_sz):
    w0 = w0_of(mu)
    for r in np.logspace(-9, math.log10(0.02), 400):
        if r <= 2 * w0:                               # a_* >= 1: not quadratic today
            continue
        w, f4, ast = bg(1e-4, r, w0)
        _, f1, _ = bg(1.0, r, w0)
        if w <= 0.02 and f4 / f1 - 1 <= drift_max:
            return r
    return None

mus = np.logspace(-5, 3, 801)
floor_w = next(m for m in mus if any(r > 2 * w0_of(m) for r in [0.02]))           # a_*<1 at r=0.02
floor = next(m for m in mus if feasible(m) is not None)

# ---------- SPARC loader (repo conventions: Ups_disk 0.5, Ups_bul 0.7, signed squares) ----------
G = 4.30091e-6                                        # kpc (km/s)^2 / Msun
a0 = 1.1607e-10 / 3.2408e-14                          # (km/s)^2 / kpc
def load(f):
    d = np.loadtxt(f)
    R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    Vbar2 = np.abs(Vg) * Vg + 0.5 * np.abs(Vd) * Vd + 0.7 * np.abs(Vb) * Vb
    return R, V, eV, Vbar2
gals = {os.path.basename(f)[:-11]: load(f) for f in sorted(glob.glob(SPARC + "/*_rotmod.dat"))}

# ---------- 2. Galactic cap from r_C ----------
cap = {}
for n, (R, V, eV, Vb2) in gals.items():
    Mb = max(Vb2[-1], 1e-9) * R[-1] / G
    rM = math.sqrt(G * Mb / a0)
    cap[n] = {"R_max": R[-1], "r_M": rM, "mu_max_per_Mpc": 1e3 * math.sqrt(rM / R[-1] ** 3),
              "mu_max_2R_per_Mpc": 1e3 * math.sqrt(rM / (2 * R[-1]) ** 3)}
binding = min(cap, key=lambda n: cap[n]["mu_max_per_Mpc"])
mu_cap = cap[binding]["mu_max_per_Mpc"]
mu_cap2 = min(c["mu_max_2R_per_Mpc"] for c in cap.values())
# SZ's own run, mu = 100/Mpc: galaxies whose last point lies beyond r_C
mu_k = mu_sz / 1e3
sz_fail = [n for n, c in cap.items() if c["R_max"] > (c["r_M"] / mu_k**2) ** (1 / 3)]

# ---------- 3. Quartic Vainshtein over SPARC ----------
def u_of(s):                                          # u + s u^3 = 1, u in (0, 1]
    u = np.minimum(1.0, np.where(s > 0, s, 1.0) ** (-1 / 3))
    for _ in range(80):
        u = u - (s * u**3 + u - 1) / (3 * s * u**2 + 1)
    return u
def rar(gN):
    return gN / (1 - np.exp(-np.sqrt(gN / a0)))
screen = {}
for tag, rV_pc in (("rV_sun_1.09pc", 1.0880745078887017), ("rV_sun_2.36pc", 2.3609412457165018)):
    rho_V = 1.0 / (rV_pc * 1e-3) ** 3                 # Msun / kpc^3, as M/r^3
    n_low = n_low_hit = n_all_hit = n_all = 0; worst = []
    for n, (R, V, eV, Vb2) in gals.items():
        ok = Vb2 > 0
        R_, eV_, Vb2_ = R[ok], eV[ok], Vb2[ok]
        gN = Vb2_ / R_; M = Vb2_ * R_ / G
        s = ((M / R_**3) / rho_V) ** 2
        u = u_of(s); gM = rar(gN)
        Vu = np.sqrt(gM * R_); Vs = np.sqrt((gN + u * (gM - gN)) * R_)
        hit = (Vu - Vs) > eV_
        low = gN < a0
        n_all += len(R_); n_all_hit += int(hit.sum())
        n_low += int(low.sum()); n_low_hit += int((hit & low).sum())
        if hit.any():
            worst.append((n, int(hit.sum()), float((Vu - Vs)[hit].max())))
    worst.sort(key=lambda t: -t[1])
    screen[tag] = {"points": n_all, "points_dV_gt_err": n_all_hit, "lowacc_points": n_low,
                   "lowacc_dV_gt_err": n_low_hit, "galaxies_hit": len(worst), "worst": worst[:8]}

Q0 = 2e-5
out = {
 "model": "Cosh K (TARGET_D5 §2), K_B=0.1, h=0.70, Om0=0.26",
 "regression_SZ_run": {"mu": mu_sz, "w0": w0_sz, "w_1e-4": float(w_sz), "drift": float(drift_sz), "a_star": float(ast_sz)},
 "mu_floor_a*<1_at_r=0.02_per_Mpc": float(floor_w),
 "mu_floor_with_drift<=SZ_per_Mpc": float(floor),
 "mu_cap_rC>=Rmax_per_Mpc": mu_cap, "binding_galaxy": binding, "binding": cap[binding],
 "mu_cap_rC>=2Rmax_per_Mpc": mu_cap2,
 "window_decades": math.log10(mu_cap / floor),
 "K2_at_Q0=2e-5_over_window": [floor**2 * (2 - KB) / (2 * Q0**2), mu_cap**2 * (2 - KB) / (2 * Q0**2)],
 "SZ_run_mu=100": {"galaxies_with_Rmax_beyond_rC": len(sz_fail), "of": len(gals), "examples": sz_fail[:8]},
 "quartic_vainshtein_SPARC": screen,
}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "DOOR_UNDER_COSH.json"), "w"), indent=1)
