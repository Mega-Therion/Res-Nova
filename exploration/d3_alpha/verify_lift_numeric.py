#!/usr/bin/env python3
"""(1) Check the O(qbar) zero-branch formula against the exact roots of the full quartic (in omega^2),
at SZ values, qbar = Q0*1.7e-6, k from 0.3 k* to 1e4 k*.  (2) Density reading.  (3) mu-independent R_max bound."""
import sympy as sp
from math import sqrt
import numpy as np
KB, lam, K2, Q0, qb, k, w = sp.symbols('K_B lambda_s K_2 Q_0 qbar k omega', real=True)
Gs = sp.Symbol('G', positive=True)
det = sp.sympify(open('AEST_DISPERSION_OFFSET.txt').read(), locals={'K_B':KB,'lambda_s':lam,'K_2':K2,'Q_0':Q0,'qbar':qb,'k':k,'omega':w,'G':Gs})
num, den = sp.fraction(sp.together(det))
big = [f for f, m in sp.factor_list(num)[1] if f.has(w) and sp.degree(f, w) > 4][0]
W2 = sp.Symbol('W2')
Pbig = sp.expand(big.subs(w, sp.sqrt(W2)))
vals = {KB: 0.5, K2: 7.5e5, Q0: 0.1}
for lv in (1.0,):
    vv = dict(vals); vv[lam] = lv
    q = 0.1 * 1.7e-6; vv[qb] = q
    mu2 = 2 * 7.5e5 * 0.01 / 1.5; ks = sqrt((1 + lv) * mu2 / lv)
    print(f"lambda_s={lv}: k* = {ks:.2f} Mpc^-1")
    print(f"{'k/k*':>8s} {'formula w^2':>13s} {'exact root nearest 0':>21s} {'rel.diff':>9s}")
    for kk in [0.3, 0.8, 0.95, 1.05, 1.5, 3, 10, 100, 1e3, 1e4]:
        kv = kk * ks
        coeffs = sp.Poly(Pbig.subs(vv).subs(k, kv), W2).all_coeffs()
        roots = np.roots([complex(sp.N(c_)) for c_ in coeffs])
        form = 7.5e5 * 0.1 * q * 1.5 * lv * (kv**2 - ks**2) / ((2 + 0.5 * lv) * kv**2 + 1.5 * (1 + lv) * mu2)
        r0 = min(roots, key=lambda r: abs(r - form))
        print(f"{kk:8.2f} {form:13.4e} {r0.real:13.4e}{r0.imag:+.1e}j {abs(r0.real - form)/max(abs(form),1e-300):9.2e}")
# (2) density reading
K2Q02 = 7.5e5 * 0.01
psi_mw = 550**2 / (2 * 299792.458**2)
fourpiGrho_phi = K2Q02 * psi_mw
vc, r = 220 / 299792.458, 0.01
fourpiGrho_mw = vc**2 / r**2
print(f"\n4piG rho_phi = K2 Q0^2 |Psi| = {fourpiGrho_phi:.3e} Mpc^-2 ; MW own 4piG rho at 10 kpc = v_c^2/r^2 = {fourpiGrho_mw:.3e} Mpc^-2 ; ratio {fourpiGrho_phi/fourpiGrho_mw:.2f}")
print(f"Jeans e-fold 1/sqrt(4piG rho_phi) = {1/sqrt(fourpiGrho_phi):.2f} Mpc/c = {1/sqrt(fourpiGrho_phi)*3.0857e19/299792.458/3.156e13:.1f} Myr")
# (3) mu-independent maximum of R:  R^2 = (2-K_B)^2 lam |Psi| (y-a) / (2 v^2 (B y + c) y),  y = k^2/mu^2
for lv in (0.3, 1.0, 2.2):
    a = (1 + lv) / lv; B = 2 + 0.5 * lv; cc = 1.5 * (1 + lv)
    ys = np.logspace(np.log10(a * 1.0001), np.log10(a * 1e6), 200000)
    f = (ys - a) / ((B * ys + cc) * ys)
    i = int(np.argmax(f)); pref = sqrt((1.5**2) * lv / 2 * f[i])
    print(f"lambda_s={lv}: R_max = {pref:.3f} * sqrt|Psi| c / v , at k = {sqrt(ys[i]/a):.2f} k*")
