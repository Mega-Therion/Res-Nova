#!/usr/bin/env python3
"""Item 5: remaining checkable statements. Uses only numbers printed in the two .md files
(no sample, no JSON)."""
import numpy as np
from scipy.stats import chi2
from scipy import constants as C

# --- 'two models survive the pre-registered chi2 rule' vs WIDE_BINARY_FINAL table (C3)
M = ["N", "F", "E", "S", "P"]
T = {"strict": dict(raw=[9.5, 246.8, 10.2, 7.1, 14.3], kap=[1.73, 1.57, 1.45, 1.50, 1.37],
                    cal=[5.5, 157.5, 7.0, 4.7, 10.5], nmax=[24.4, 16.9, 43.0, 21.8, 15.4]),
     "loose": dict(raw=[63.8, 531.8, 31.7, 16.1, 60.8], kap=[1.79, 1.19, 1.56, 1.50, 1.33],
                   cal=[35.6, 445.7, 20.3, 10.8, 45.6], nmax=[24.5, 15.7, 27.5, 21.7, 16.9])}
print(f"chi2(4) median = {chi2.median(4):.4f} (doc 3.36/3.357); chi2(4) p=0.001 critical = {chi2.isf(1e-3, 4):.3f} (18.5)")
fails = {}
for cut, d in T.items():
    for i, m in enumerate(M):
        c1 = d["cal"][i] > 18.5; c2 = d["raw"][i] > d["nmax"][i]
        fails[(cut, m)] = (c1, c2)
        print(f"  {cut:6s} {m}: raw/kappa={d['raw'][i]/d['kap'][i]:7.2f} (doc {d['cal'][i]})  cal>18.5:{c1!s:5}  raw>nullmax:{c2!s:5}")
excl = {m: all(all(fails[(c, m)]) for c in T) for m in M}
pass_both = {m: not any(any(fails[(c, m)]) for c in T) for m in M}
print("C3 excluded (both criteria, both cuts):", excl)
print("survive C3:", [m for m in M if not excl[m]], "| fail neither criterion in either cut:", [m for m in M if pass_both[m]])
print("loose E: fails calibrated?", fails[("loose", "E")][0], " fails raw>nullmax?", fails[("loose", "E")][1],
      "(doc prose: 'E fails only the calibrated one')")

# --- regime: is 5-30 kAU EFE-dominated?  q = g_N,int / g_N,ext at r = s, GE = 1.9e-10 (code)
GE = 1.9e-10; AU = C.au; G = C.G; Ms = 1.98847e30
r_e = lambda m: np.sqrt(G * m * Ms / GE) / AU
print(f"\nr where g_N,int = GE: 1.5 Msun {r_e(1.5):.0f} AU (A1 says ~6.8 kAU); 1.0 Msun {r_e(1.0):.0f} AU; 0.8 Msun {r_e(0.8):.0f} AU")
for s in (5e3, 7.07e3, 10e3, 14.1e3, 20e3, 24.5e3, 30e3):
    print(f"  s={s/1e3:5.1f} kAU  q(M=0.8,1.2,1.8) =", "  ".join(f"{(r_e(m)/s)**2:6.3f}" for m in (0.8, 1.2, 1.8)))

# --- angle averages: PDE form and existing mock E share nu_e(1+K0/3)
nu = lambda y: np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)
Kq = lambda y: -2 / (y**2 + y * np.sqrt(y**2 + 4) + 4)
ye = GE / 1.042e-10; u = np.linspace(-1, 1, 2000001)
pde = np.trapezoid(nu(ye) * (1 + Kq(ye) / 2 * (1 - u**2)), u) / 2
alg = np.trapezoid(nu(ye) * (1 + Kq(ye) * u**2), u) / 2
print(f"\nangle-avg boost: PDE {pde:.5f}, mock-E {alg:.5f}, nu_e(1+K0/3) {nu(ye)*(1+Kq(ye)/3):.5f}")
Q = (2/3) * (1 - 2 * 0.5**1.5) / 0.25
print(f"EFE-limit E plateau in R units: sqrt(1+Q(eta-1)) = {np.sqrt(1 + Q*(pde-1)):.4f} (doc E column 1.023/1.020/1.015)")

# --- brute-force overlap of A and B
zz = np.linspace(-6, 12, 1801); ee = np.linspace(0, 12, 1201)
Z, E = np.meshgrid(zz, ee)
for k in (1.0, 2.0, 2.5, 3.0):
    A = (Z >= 3) & (np.abs(Z - E) <= k)
    for sided in ("two", "one"):
        c0 = (np.abs(Z) <= k) if sided == "two" else (Z < 3)
        B = c0 & (E - Z >= 2)
        ov = A & B
        msg = f"z={Z[ov].min():.2f}..{Z[ov].max():.2f}, e={E[ov].min():.2f}..{E[ov].max():.2f}" if ov.any() else "none"
        print(f"  k={k} {sided}-sided: A&B overlap -> {msg}")
