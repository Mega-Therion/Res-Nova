#!/usr/bin/env python3
"""O3 horizon-landing route: checks every computable step.
  1. Hubble/de Sitter horizon identity: T_H * S_H = E_c, the critical energy inside the horizon (exact, any epoch).
  2. Landing accounting: N = S/k_B horizon cells (one nat each), one balanced either/or landing per cell at the
     Landauer cost k_B T ln 2  ->  E_landing / E_c = ln 2  (Omega_Lambda), remainder 1 - ln 2 (Omega_m).
  3. Counting: the number of horizon cells A/(4 l_P^2) vs the vacuum-energy mismatch (E_Planck / E_Lambda)^4."""
import sympy as sp, mpmath as mp
H, G, hbar, c, kB = sp.symbols('H G hbar c k_B', positive=True)
R = c / H; A = 4 * sp.pi * R**2
S = kB * c**3 * A / (4 * G * hbar); T = hbar * H / (2 * sp.pi * kB)
E_c = 3 * H**2 / (8 * sp.pi * G) * c**2 * sp.Rational(4, 3) * sp.pi * R**3
print("1. T*S / E_c =", sp.simplify(T * S / E_c))
E_land = (S / kB) * kB * T * sp.log(2)
print("2. E_landing / E_c =", sp.simplify(E_land / E_c), "  (Omega_Lambda);  remainder =", sp.simplify(1 - E_land / E_c), "  (Omega_m)")
mp.mp.dps = 30
H0 = mp.mpf(70) * 1000 / mp.mpf("3.0857e22"); cl = mp.mpf(299792458); lP = mp.mpf("1.616255e-35")
RH = cl / H0
print(f"3. horizon cells A/(4 l_P^2) = {mp.nstr(4 * mp.pi * RH**2 / (4 * lP**2), 3)}   (H0 = 70)")
print(f"   vacuum mismatch (E_Planck/E_Lambda)^4 = {mp.nstr((mp.mpf('1.22089e28') / mp.mpf('2.3e-3'))**4, 3)}   (E_Lambda = rho_Lambda^(1/4) ~ 2.3 meV)")
print(f"   ln 2 = {mp.nstr(mp.log(2), 6)},  1 - ln 2 = {mp.nstr(1 - mp.log(2), 6)}")
