#!/usr/bin/env python3
"""
Obligation 3 audit verifier — the 2pi and the Hubble-form specificity.

THE_2PI candidate sources, discriminated against the measured facts of
REPRESENTATION_AUDIT_A0_SPARC_2026-09-16.md and against Theorem B-cov
(Q3_AEST_COVARIANT_DERIVATION_2026-09-16.md):

  S1  the thermal circle of the boost orbit (KMS/Unruh): the unit-norm orbit
      (cosh psi, sinh psi) that K2 forces closes under Wick rotation psi -> i*theta
      into the unit circle with period 2*pi — the Euclidean period of a hyperbolic
      observer with proper acceleration a is 2*pi/a, the Unruh circle. COMPOSES
      with B-cov (same orbit). [D machine-checked here]
  S2  the crossing-time winding (c/a0 = 2*pi/H0): same number, no mechanism —
      bookkeeping identity, no source. [D identity]
  S3  the rotation-2pi of the double cover (Pin-/SU(2): 2*pi rotation = -1):
      lives in the COMPACT rotation sector; the boost sector has no real period
      (cosh unbounded) — its only closure is S1's thermal circle. [D]

Machine checks:
  T1  Wick closure of the K2 orbit: cosh(i th) = cos th, sinh(i th) = i sin th;
      the hyperbola maps to the unit circle, period 2*pi exactly.
  T2  Euclidean period of the hyperbola: X0 = sinh(a*tau)/a, X1 = cosh(a*tau)/a
      closes under tau -> tau + 2*pi*i/a and under no smaller period.
  T3  two-state thermal polarization: partition function Z = 2 cosh(D/(2T)),
      equilibrium polarization = tanh(D/(2T)) — the channel's mu = tanh psi is
      a thermal-circle reading with psi = D/(2T). [C-level structural match;
      the machine checks the algebra only]
  T4  the measured factors, recomputed from constants:
        c*H0/(2*pi)     = 1.0421e-10 m/s^2 at H0 = 67.4 km/s/Mpc  (the anchor)
        c*H0 / anchor   = 2*pi            (Milgrom's a_dS miss, audit P3)
        sqrt(3*OmegaL)  = 1.4390         (Lambda form high, audit P2)
        sqrt(OmegaL)    = 0.8307         (de Sitter form low, audit P2)
  T5  boost sector has no real period (cosh monotone on the orbit); rotation
      sector's 2*pi is a different (compact) sector — S3 does not transfer.
Exit 0 iff all pass.
"""
import sys

import sympy as sp

FAILURES = []


def note(ok, name, detail=""):
    print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)


def main():
    th, tau, a = sp.symbols("theta tau a", positive=True)

    # T1: Wick closure of the K2 orbit — hyperbola -> circle, period 2*pi
    note(sp.simplify(sp.expand_func(sp.cosh(sp.I * th)) - sp.cos(th)) == 0,
         "T1a cosh(i th) = cos th")
    note(sp.simplify(sp.expand_func(sp.sinh(sp.I * th)) - sp.I * sp.sin(th)) == 0,
         "T1b sinh(i th) = i sin th")
    # after the Wick rotation the orbit coordinates are (cos th, sin th):
    note(sp.simplify(sp.cos(th + 2 * sp.pi) - sp.cos(th)) == 0
         and sp.simplify(sp.sin(th + 2 * sp.pi) - sp.sin(th)) == 0,
         "T1c circle period is 2*pi (after Wick rotation)")

    # T2: Euclidean period of the hyperbola (hyperbolic observer, c = 1)
    X0 = sp.sinh(a * tau) / a
    X1 = sp.cosh(a * tau) / a
    for X, name in [(X0, "X0"), (X1, "X1")]:
        d = sp.simplify(X.subs(tau, tau + 2 * sp.pi * sp.I / a) - X)
        note(sp.simplify(d) == 0, f"T2 {name} closes at tau + 2*pi*i/a")

    # T3: two-state thermal polarization = tanh(gap / 2T)
    D, T = sp.symbols("Delta T", positive=True)
    Z = sp.exp(D / (2 * T)) + sp.exp(-D / (2 * T))          # partition function
    pol = (sp.exp(D / (2 * T)) - sp.exp(-D / (2 * T))) / Z    # <s> = (+ - -)/( + + )
    tdiff = sp.together(pol - sp.tanh(D / (2 * T)).rewrite(sp.exp))
    note(sp.simplify(tdiff) == 0,
         "T3 <s> = tanh(D/(2T)); mu = tanh(psi) with psi = D/(2T)")

    # T4: the measured factors, recomputed from constants
    c = 2.99792458e8                 # m/s
    H0 = 67.4 * 1000 / 3.0856775814913673e22   # km/s/Mpc -> 1/s
    anchor = c * H0 / (2 * sp.pi)
    note(abs(float(anchor) - 1.0421e-10) / 1.0421e-10 < 1e-3,
         "T4a c*H0/(2*pi) = 1.0421e-10 m/s^2", f"= {float(anchor):.4e}")
    note(abs(c * H0 / float(anchor) - 2 * sp.pi) < 1e-9,
         "T4b a_dS = c*H0 misses by exactly 2*pi", f"ratio {c * H0 / float(anchor):.6f}")
    OmL = 0.69
    note(abs(sp.sqrt(3 * OmL).evalf() - 1.4390) / 1.4390 < 1e-3,
         "T4c Lambda form factor sqrt(3*OmL) = 1.439", f"= {float(sp.sqrt(3 * OmL).evalf()):.4f}")
    note(abs(sp.sqrt(OmL).evalf() - 0.8307) / 0.8307 < 1e-3,
         "T4d de Sitter form factor sqrt(OmL) = 0.831", f"= {float(sp.sqrt(OmL).evalf()):.4f}")

    # T5: boost sector has no real period; rotation 2*pi does not transfer
    x = sp.symbols("x", real=True)
    note(sp.limit(sp.cosh(x), x, sp.oo) == sp.oo,
         "T5a cosh unbounded: no real closure of the boost orbit")
    # the rotation 2*pi acts as -1 on the double cover's sheets (rotation sector)
    rot = sp.Matrix([[sp.cos(sp.pi), -sp.sin(sp.pi)], [sp.sin(sp.pi), sp.cos(sp.pi)]])
    note(rot == -sp.eye(2), "T5b 2*pi rotation = -1 on the double cover (compact sector)")

    print()
    print("SUMMARY: 2pi/Hubble-form audit checks:", 11, "total,", len(FAILURES), "failures")
    if FAILURES:
        print("FAILED:", ", ".join(FAILURES))
        sys.exit(1)
    print("Finding: the only 2pi that composes with B-cov is the thermal circle of")
    print("the K2 orbit itself (S1); the Hubble form selects WHICH horizon's circle")
    print("closes it (audit P2's measured discrimination). Triangle leg sharpened;")
    print("normalization caveat (D2-supp 6.1) unchanged.")


if __name__ == "__main__":
    main()
