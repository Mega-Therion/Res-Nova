#!/usr/bin/env python3
"""Is the exclusion GW170817-dependent? No. It is signature-dependent.

Safa's objection: translating the GW170817 speed bound into a bound on B/A is
model-dependent (screening, line-of-sight vs cosmic mean, epoch). Granted.
But the disformal photon cone gives an OBSERVATION-FREE bound.
"""
import math

h=0.6827; Om_g=2.47e-5/h**2; Om_L=math.log(2)
required = Om_L/Om_g

print("REQUIRED  |B/A| >= %.3e   (EM interaction reaching dark-energy density)\n"%required)

# Photon cone from g~ = A g + B u u, u comoving:
#   -(A-B) dt^2 + A dx^2 = 0   =>   c_gamma^2 = (A-B)/A = 1 - B/A
for name,r in [("B/A = +required", +required), ("B/A = -required", -required)]:
    c2 = 1 - r
    print(f"{name:18} c_gamma^2 = 1 - ({r:+.3e}) = {c2:+.4e}")
    if c2 < 0:
        print("                   -> g~_00 and g~_ij share a sign: signature is NOT Lorentzian.")
        print("                      The photon light cone does not exist. No propagation at all.")
    elif c2 > 1:
        print(f"                   -> c_gamma = {math.sqrt(c2):.1f} c  (superluminal photons)")
        print(f"                      GRB170817A would have preceded the GW by ~{40e6*3.086e22/3e8*(1-1/math.sqrt(c2))/(3600*24*365):.2e} yr,")
        print("                      not followed it by 1.7 s.")
    print()

print("LORENTZIAN SIGNATURE ALONE REQUIRES  B/A < 1.")
print("Required value exceeds that by %.2e -- with NO observational input."%(required/1.0))
print("\nGW170817 does not create the exclusion. It only tightens the ceiling")
print("from  B/A < 1  (geometry)  to  B/A <= 2e-15  (measurement).")
print("Margin available to any screening/environment loophole: %.2e -> still short by %.2e"
      %(1.0, required/1.0))
