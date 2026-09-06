#!/usr/bin/env python3
"""Required vs allowed disformal ratio B/A. Both derive from the symbolic result:
   f(phi) = sqrt((A-B)/A)  multiplies F^2   [traceless -> w=+1/3 regardless of f]
   B/(2 sqrt(A) sqrt(A-B)) multiplies E^2   [the only conformal-symmetry-breaking piece]
so every departure from pure Maxwell is O(B/A).
"""
import math

# --- REQUIRED: EM interaction must reach dark-energy density today ---------
h        = 0.6827          # Res-Nova derived H0 = 68.27
Om_g_h2  = 2.47e-5         # Planck 2018 photon density
Om_gamma = Om_g_h2/h**2
Om_Lambda= math.log(2)     # Res-Nova: Omega_Lambda = ln 2
required = Om_Lambda/Om_gamma

# --- ALLOWED: GW170817 luminality -----------------------------------------
# c_gamma^2 = (A-B)/A = 1 - B/A ;  c_T = 1  =>  c_T/c_gamma - 1 ~ (B/A)/2
gw_bound = 1e-15
allowed  = 2*gw_bound

print(f"Omega_gamma        = {Om_gamma:.3e}")
print(f"Omega_Lambda       = {Om_Lambda:.4f}")
print(f"REQUIRED |B/A|    >= {required:.3e}   (to source dark energy from the EM sector)")
print(f"ALLOWED  |B/A|    <= {allowed:.1e}   (GW170817, |c_T/c_gamma - 1| <= 1e-15)")
print(f"GAP                = {required/allowed:.2e}  = {math.log10(required/allowed):.1f} orders of magnitude")

# --- alpha_fs: is it the binding constraint? ------------------------------
# e_eff^2 ~ 1/f  =>  d(alpha)/alpha ~ -(1/2) d(f)/f ~ +(1/4)(B/A)
dalpha = 0.25*allowed
print(f"\nalpha_fs drift at the GW bound: |d(alpha)/alpha| <= {dalpha:.1e}")
print(f"  observational bound ~1e-6 (quasar/Oklo) -> slack of {1e-6/dalpha:.1e}x")
print("  => alpha_fs is NOT the binding constraint. GW170817 is, by ~9 orders.")
