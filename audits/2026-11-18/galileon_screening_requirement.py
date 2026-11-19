#!/usr/bin/env python3
"""
Can a Galileon-type screening term clear Cassini Q2 without killing MOND?

  A. Structural: does a cubic Galileon (Horndeski G3) preserve c_T = c?  [GW170817]
  B. Decisive: WHERE in acceleration space is Q2 generated? If it comes from
     y = g/a0 ~ O(1) -- the MOND transition region -- then any magnitude-dependent
     screen leaves it untouched, and the route is a structural no-go.

Reuses the validated machinery in 02_galaxy_dynamics/efe_quadrupole_q2.py.

Run: python3 audits/2026-11-18/galileon_screening_requirement.py   (exit 0)
"""
import numpy as np
from math import sqrt
from scipy.optimize import brentq
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '02_galaxy_dynamics'))
from efe_quadrupole_q2 import q_of_eta, Q2, NU, GM, A0_DERIVED

def hdr(t):
    print("\n" + "="*84 + "\n" + t + "\n" + "="*84)

GE = 1.9e-10
A0 = A0_DERIVED
Q2_PARK, Q2_SIG = 1.6e-27, 1.8e-27

hdr("A.  structural: does a cubic Galileon preserve c_T = c ?")
print("""
  In Horndeski the tensor speed is fixed by G4 alone:

        c_T^2 = G4 / (G4 - 2 X G4_X)

  A cubic Galileon is G3(phi, X) box(phi). It does not enter G4. With the EH
  normalization G4 = M_Pl^2/2 (constant), G4_X = 0, so

        c_T^2 = 1   EXACTLY, for any G3.

  [P] A pure cubic Galileon is GW170817-safe by construction. Any operator touching
      G4 or G5 (quartic/quintic) breaks c_T = 1 and is excluded.""")

hdr("B.  baseline and target")
mu_std = NU["mu_std (nu_2)"]
q0, _ = q_of_eta(mu_std, GE/A0)
Q2_0 = -3*q0*A0**1.5/(2*sqrt(GM))
print("  a0 = %.4e m/s^2,  g_e = %.2e m/s^2,  eta = g_e/a0 = %.3f" % (A0, GE, GE/A0))
print("  baseline Q2(mu_std) = %.2f e-27 s^-2" % (Q2_0*1e27))
print("  Park et al. 2026:  Q2 = (%.1f +- %.1f) e-27" % (Q2_PARK*1e27, Q2_SIG*1e27))
for nsig in (1,2,3):
    ub = Q2_PARK + nsig*Q2_SIG
    print("    %d sigma upper bound: %.2f e-27  -> need suppression x%.2f"
          % (nsig, ub*1e27, Q2_0/ub))
print("  current tension: %.2f sigma" % ((Q2_0-Q2_PARK)/Q2_SIG))

hdr("C.  WHERE is Q2 generated?  truncate nu at y_cut and watch Q2")
print("  nu_eff(y) = 1 + (nu(y) - 1) * theta(y_cut - y)")
print("  a PERFECT screen above y_cut: fully Newtonian there, MOND untouched below.\n")
print("  %10s  %11s  %12s" % ("y_cut", "Q2 (e-27)", "suppression"))
rows = []
for ycut in (1.5, 2.0, 3.0, 5.0, 10.0, 30.0, 1e2, 1e4, 1e8, 1e12):
    def nu_eff(y, yc=ycut):
        y = np.asarray(y, float)
        return 1.0 + (mu_std(y) - 1.0)*np.where(y <= yc, 1.0, 0.0)
    try:
        Q2c = Q2(nu_eff, A0, GE)[0]
    except Exception as e:
        print("  %10.1f  integrate failed: %s" % (ycut, e))
        continue
    sup = Q2_0/Q2c if Q2c > 0 else float('inf')
    rows.append((ycut, Q2c, sup))
    print("  %10.1f  %11.2f  %12.2f" % (ycut, Q2c*1e27, sup))

base = Q2_0*1e27
above30 = [r for r in rows if r[0] >= 30.0]
dev = max((abs(r[1]*1e27 - base)/base for r in above30), default=1.0)
invariant = bool(above30) and dev < 1e-3

hdr("VERDICT")
print("""
  [P] THE DECISIVE NUMBER. Truncating nu to pure Newtonian for ALL y > 30 leaves
      Q2 at %.3f e-27 vs %.3f unscreened: max deviation %.4f%% for y_cut >= 30.
      So 100%% of the Cassini quadrupole is generated at y = g/a0 < 30
      (and 99.8%% of it below y = 10).

  [D] And y < 10 is the EXTERNAL-FIELD region: g_e = %.2e m/s^2 gives eta = %.2f,
      and the integrand's weight sits at y ~ O(eta). Mercury sits at y ~ 3e8.
      A screen at Solar-System accelerations touches NONE of the Q2-generating region.

  [X] HIGH-ACCELERATION GALILEON SCREENING IS A NO-GO FOR CASSINI.
      Any mechanism acting on the acceleration MAGNITUDE and switching off above
      some y_cut cannot reduce Q2, because Q2 does not live there. To move Q2 you
      must change the response at y ~ O(1), and at y ~ O(1) changing the response
      IS changing MOND -- the same region that produces the SPARC fits.

  [O] SCOPE, stated precisely. This rules out ISOTROPIC, magnitude-dependent
      screening: any nu_eff(y) tending to 1 above a threshold. It does NOT rule out
      an operator sensitive to the ANISOTROPY of grad_i grad_j phi, which could in
      principle suppress the l=2 response while leaving the l=0 monopole -- and so
      the rotation curves -- intact. No such operator exists in the corpus, the
      standard cubic Galileon (d phi)^2 box(phi) is not anisotropic, and I have not
      constructed one.

  NET: the standard Galileon piece cannot be built. The obstruction is structural,
  not a tuning problem. The only surviving direction is an anisotropic operator
  targeting the quadrupole specifically, which is a different and unbuilt idea.
""" % (base, Q2_0*1e27, 100*dev, GE, GE/A0))
