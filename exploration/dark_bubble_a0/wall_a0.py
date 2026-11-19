#!/usr/bin/env python3
"""Dark Bubble wall acceleration -> a0 (pre-registered in PREREG.md). [D] geometry + [E] SPARC.
Exact normal acceleration of a wall R(tau) in AdS5 with f = 1 + k^2 R^2:
    a5 = (R'' + k^2 R) / sqrt(1 + k^2 R^2 + R'^2)
Expanded for H, 1/R << k:  a5^2 - k^2 = 2 R''/R - (H^2 + 1/R^2) = (8 pi G/3)(rho_L - 2 rho_m) for LCDM (flat).
So a_w^2 = c^2 H0^2 [Om_L - 2 Om_m (1+z)^3]: k-independent; real only after rho_L > 2 rho_m."""
import glob, json, math, re
import numpy as np
c = 2.99792458e8; Mpc = 3.0857e22; KPC = 3.0857e19
H0 = 67.4e3 / Mpc; Om = 0.315; OL = 1 - Om
# 1) check the expansion against the exact formula, k >> H (units 1/s, R in light-seconds -> use c=1 units)
def exact_minus_k2(k, z, Om_=Om):
    a = 1 / (1 + z); H = H0 * math.sqrt(Om_ / a**3 + (1 - Om_))
    q = H0**2 * ((1 - Om_) - 0.5 * Om_ / a**3)           # R''/R
    R = 1e40                                               # flat limit: 1/R^2 -> 0
    Rd = H * R; Rdd = q * R
    a5 = (Rdd + k**2 * R) / math.sqrt(1 + k**2 * R**2 + Rd**2)
    return a5**2 - k**2, 2 * q - H**2
chk = [exact_minus_k2(k, 0.0) for k in (1e-12, 1e-11)]
aw2 = lambda z, Om_=Om: (c * H0) ** 2 * ((1 - Om_) - 2 * Om_ * (1 + z) ** 3)
aw = lambda z, Om_=Om: math.sqrt(aw2(z, Om_)) if aw2(z, Om_) > 0 else 0.0
z_on = ((1 - Om) / (2 * Om)) ** (1 / 3) - 1
Om_need = {r: None for r in ("R1", "R2")}
for rule, target_fac in (("R1", 1.0), ("R2", 2.0)):      # a0 = a_w / fac  ->  a_w = fac * 1.1607e-10
    tgt = target_fac * 1.1607e-10; Om_need[rule] = (1 - (tgt / (c * H0)) ** 2) / 3
out = {"expansion_check_exact_vs_formula_z0": chk,
       "a_w_z0": aw(0.0), "a0_R1_z0": aw(0.0), "a0_R2_z0": aw(0.0) / 2,
       "a_dS_pure_Lambda": c * H0 * math.sqrt(OL), "z_onset_a_w_real": z_on,
       "Om_needed_for_a0=1.1607": Om_need,
       "dlog_aw_dOm_at_0.315": None}
eps = 1e-4; out["dlog_aw_dOm_at_0.315"] = (math.log(aw(0, Om + eps)) - math.log(aw(0, Om - eps))) / (2 * eps)
# 2) K2: SPARC RAR with a0 = a_w(z(D)) (rule R1, mu_std -> nu) vs constant a0
nu = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-30)))   # nu for mu_std: y = gN/a0 ... exact for mu_std
def nu_std(gN, a0):
    y = gN / a0; return np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-300) ** 2)))
rows = []
for p in sorted(glob.glob("../../02_galaxy_dynamics/sparc_data/*_rotmod.dat")):
    D = float(re.search(r"Distance = ([\d.]+)", open(p).read()).group(1))
    d = np.loadtxt(p)
    if d.ndim < 2 or len(d) < 3: continue
    R, V, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    gbar = (Vg * np.abs(Vg) + 0.5 * Vd**2 + 0.7 * Vb**2) * 1e6 / (R * KPC)
    gobs = V**2 * 1e6 / (R * KPC); egob = 2 * eV / np.maximum(V, 1e-3) * gobs
    m = (gbar > 0) & (eV > 0)
    rows.append((D, gbar[m], gobs[m], egob[m]))
def chi2(a0_of_D):
    s = 0.0
    for D, gb, go, eg in rows:
        a0 = a0_of_D(D)
        if a0 <= 0: pred = gb
        else: pred = gb * nu_std(gb, a0)
        s += np.sum(((go - pred) / np.sqrt(eg**2 + (0.1 * go) ** 2)) ** 2)
    return s
grid = np.linspace(0.8e-10, 1.6e-10, 81)
c_const = [chi2(lambda D, a=a: a) for a in grid]; best = grid[int(np.argmin(c_const))]
zD = lambda D: H0 * D * Mpc / c
c_wall = chi2(lambda D: aw(zD(D)))
Om_grid = np.linspace(0.300, 0.330, 61)
c_wall_Om = [chi2(lambda D, o=o: aw(zD(D), o)) for o in Om_grid]
ob = float(Om_grid[int(np.argmin(c_wall_Om))])
Ds = np.array([r[0] for r in rows])
out["K2"] = {"N_gal": len(rows), "D_range_Mpc": [float(Ds.min()), float(Ds.max())],
             "z_max": zD(Ds.max()),
             "chi2_const_best": float(min(c_const)), "a0_const_best": float(best),
             "chi2_wall_Om0.315": float(c_wall), "delta_chi2_wall_vs_const": float(c_wall - min(c_const)),
             "chi2_wall_bestOm": float(min(c_wall_Om)), "Om_best": ob,
             "delta_chi2_wall_bestOm_vs_const": float(min(c_wall_Om) - min(c_const)),
             "frac_gal_with_a_w_zero_at_Om0.315": float(np.mean([aw(zD(D)) == 0 for D in Ds]))}
print(json.dumps(out, indent=1, default=float)); json.dump(out, open("WALL_A0.json", "w"), indent=1, default=float)
