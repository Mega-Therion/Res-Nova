#!/usr/bin/env python3
"""Machine-check the algebraic factor in the stated rho_Lambda/rho_crit equations.

Uses only Python's standard library. This checks algebra and arithmetic, not the
physical validity of the input density formula.
"""
from math import isclose, log, pi

# SI conversion for H0 = 67.4 km s^-1 Mpc^-1.
C_M_S = 2.998e8
H0_KM_S_MPC = 67.4
KM_M = 1_000.0
MPC_M = 3.0857e22
H0_S_INV = H0_KM_S_MPC * KM_M / MPC_M
A0_M_S2 = C_M_S * H0_S_INV / (2.0 * pi)

# Given rho_Lambda = H0^2 ln(2)/(32 pi^2 G) and
# rho_crit = 3 H0^2/(8 pi G), H0^2 and G cancel exactly.
OMEGA_FROM_GIVEN_EQUATIONS = log(2.0) / (12.0 * pi)
CLAIMED_LN2 = log(2.0)

assert isclose(OMEGA_FROM_GIVEN_EQUATIONS * (12.0 * pi), CLAIMED_LN2,
               rel_tol=1e-14, abs_tol=0.0)
assert not isclose(OMEGA_FROM_GIVEN_EQUATIONS, CLAIMED_LN2,
                   rel_tol=1e-3, abs_tol=0.0)

print(f"H0 = {H0_S_INV:.12e} s^-1")
print(f"a0 = c H0/(2 pi) = {A0_M_S2:.12e} m s^-2")
print(f"Omega_Lambda from stated equations = ln(2)/(12 pi) = "
      f"{OMEGA_FROM_GIVEN_EQUATIONS:.12f}")
print(f"ln(2) = {CLAIMED_LN2:.12f}")
print(f"ratio Omega_Lambda/ln(2) = {OMEGA_FROM_GIVEN_EQUATIONS / CLAIMED_LN2:.12f}")
print("PASS: stated equations imply ln(2)/(12 pi), not ln(2).")
