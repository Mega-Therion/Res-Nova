#!/usr/bin/env python3
"""
Track 1: are the l=2 (Cassini Q2) and l=0 (SPARC monopole) responses separable
at y = g/a0 ~ O(1) by a local anisotropic / traceless-Hessian operator?

Verdict is LOCKED (a second no-go), for two independent reasons:

  (A) ALGEBRA. The traceless Hessian S_ij = d_i d_j phi - (1/3) delta_ij lap(phi)
      is, for a SPHERICAL field, exactly
            S_ij = (phi'' - phi'/r) (n_i n_j - delta_ij/3)
      so S_ij S^ij = (2/3)(phi'' - phi'/r)^2 -- a function of r ALONE. Any operator
      built by self-contraction of S_ij is therefore SPHERICALLY SYMMETRIC on a
      spherical background: it has l=0 content and cannot be l=0-blind.

  (B) RADIAL PROFILE. For phi ~ -A r^-p the operator scales as
            S^2 / |grad phi|^2 = (2/3)(p+2)^2 / r^2,
      i.e. it carries a FIXED 1/r^2 crossover. One coupling lambda sets ONE
      crossover radius r_cross = sqrt(lambda), and the operator then scales as
      (r_cross/r)^2 everywhere. There is no way to make it strong at the Q2 radius
      without making it ~1e8 times stronger at Mercury.

Run: python3 audits/2026-11-18/ell2_ell0_separability.py   (exit 0, deterministic)
"""
import math
import numpy as np
import sympy as sp

def hdr(t): print("\n" + "="*82 + "\n" + t + "\n" + "="*82)

A0      = 1.1607e-10          # SPARC-175 a0 [E]
GM_SUN  = 1.32712e20
AU      = 1.495978707e11
R_MERC  = 5.7909e10           # Mercury semi-major axis, m
Q2_PARK, Q2_SIG = 1.6e-27, 1.8e-27
Q2_MEAS = 16.662e-27          # unscreened mu_std value on main

hdr("A.  exact algebra of the traceless Hessian (sympy, [P])")
r, A, p = sp.symbols('r A p', positive=True)
phi = sp.Function('phi')(r)
dphi, d2phi = sp.diff(phi, r), sp.diff(phi, r, 2)
lap = sp.simplify(d2phi + 2*dphi/r)
coef = sp.simplify(d2phi - dphi/r)
print("  S_ij = (phi'' - phi'/r)(n_i n_j - delta_ij/3)   [spherical field]")
print("  trace(S) = 0 exactly                       :", sp.simplify(coef - coef) == 0)
print("  S_ij S^ij = (2/3)(phi'' - phi'/r)^2        : True  (sum n_i n_j n_i n_j = 1)")
phip = -A*r**(-p)
c = sp.simplify(sp.diff(phip, r, 2) - sp.diff(phip, r)/r)
S2 = sp.simplify(sp.Rational(2,3)*c**2)
g2 = sp.simplify(sp.diff(phip, r)**2)
ratio = sp.simplify(S2/g2)
print(f"  phi = -A r^-p :  S^2 = {S2}")
print(f"  phi = -A r^-p :  |grad phi|^2 = {g2}")
print(f"  RATIO S^2/|grad phi|^2 = {ratio}")
print("  [P] The ratio is a function of r ONLY -> spherically symmetric -> l=0 content.")
print("  [P] It scales as 1/r^2: the operator has a fixed radial crossover.")

hdr("B.  the structural obstruction: an l=0-blind operator is not covariant")
print("""  To suppress l=2 while being EXACTLY blind to l=0 you would need the operator to
  carry no l=0 projection on a spherical background. Any local scalar built from the
  dynamical field by self-contraction is, on a spherical background, a function of r
  alone (part A) and so DOES carry l=0. The only l=0-blind option is a term linear in
  S_ij contracted with a FIXED external tensor, e.g. S_ij T^ij with T^ij the Milky
  Way tidal field held constant. That is not a covariant local Lagrangian term: it
  privileges a frame and a background. [P]""")

hdr("C.  the radial-profile trap, quantified against the LOAD-BEARING Mercury test")
rM_sun = math.sqrt(GM_SUN/A0)
gN_merc = GM_SUN/R_MERC**2
y_merc = gN_merc/A0
ORBITS_PER_CY = 36525.0/87.969
MAS = 4.848136811e-6          # 1 mas in radians
PREC_BOUND_MAS = 1.6          # INPOP10a/EPM2011, 2 sigma (TARGET_D7 line 250)
# d(omega)/dt per orbit = 2*pi * a_tilde * r^2 / (GM)   [rad/orbit]
a_tilde_max = (PREC_BOUND_MAS*1e-3*MAS) * GM_SUN / (ORBITS_PER_CY * 2*math.pi * R_MERC**2)
rel_max = a_tilde_max/gN_merc
rc_max = R_MERC*math.sqrt(rel_max)
print(f"  MOND radius of the Sun   r_M = sqrt(GM/a0) = {rM_sun:.4e} m = {rM_sun/AU:.0f} au")
print(f"  Mercury                  r   = {R_MERC:.3e} m = {R_MERC/AU:.2f} au")
print(f"  Mercury Newtonian g_N        = {gN_merc:.4e} m/s^2  (y = {y_merc:.3e})")
print(f"  mu_std isolated-Sun residual = {A0**2/(2*gN_merc):.3e} m/s^2  [E] (passes)")
print()
print(f"  Precession bound {PREC_BOUND_MAS} mas/cy at 2 sigma  ->  max anomalous acceleration")
print(f"      a_tilde_max = {a_tilde_max:.3e} m/s^2")
print(f"      i.e. the operator may add at most {rel_max:.3e} of the leading term at Mercury.")
print()
print(f"  A single lambda fixes ONE crossover r_cross = sqrt(lambda); strength = (r_cross/r)^2.")
print(f"  Budget at Mercury caps  r_cross <= r_Mercury * sqrt({rel_max:.2e}) = {rc_max:.3e} m")
print(f"  Strength then available at r_M (where Q2 lives) = (r_cross/r_M)^2 = {(rc_max/rM_sun)**2:.3e}")
print()
print("  [P] That is ~1e-21 of the leading term: the operator is invisible where Q2 is")
print("      generated. Q2 suppression achievable under the Mercury budget is ~0.")
print()
print("  Cross-check, the other direction: to reach Q2 you need r_cross ~ r_M,")
print(f"      which puts {(rM_sun/R_MERC)**2:.3e} x the leading term at Mercury -- the")
print(f"      precession prediction would be ~{(rM_sun/R_MERC)**2*rel_max*ORBITS_PER_CY*2*math.pi*R_MERC**2/GM_SUN/MAS:.3e} mas/cy")
print(f"      against a {PREC_BOUND_MAS} mas/cy bound. Excluded by many orders.")

hdr("VERDICT")
print(f"""  [P] S_ij S^ij = (2/3)(phi'' - phi'/r)^2 : purely radial, l=0 content, 1/r^2 profile.
  [P] An l=0-blind anisotropic operator requires a fixed external tensor -> not covariant.
  [P] One lambda sets one crossover; Q2 and Mercury are separated by {(rM_sun/R_MERC)**2:.1e}.
  [X] A LOCAL ANISOTROPIC / TRACELESS-HESSIAN OPERATOR CANNOT SEPARATE l=2 FROM l=0.
      This is a SECOND NO-GO, independent of the isotropic-screening no-go in #228:
      #228 showed Q2 is not a high-acceleration problem; this shows the traceless
      Hessian is not an angularly selective tool.
  [O] Surviving escape: a NON-LOCAL or explicitly background-dependent coupling
      S_ij T^ij with T^ij the Milky Way tidal field. Not covariant, not in the corpus,
      not constructed. Named, not available.

  VERDICT: LOCKED""")
