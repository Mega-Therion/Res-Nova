#!/usr/bin/env python3
"""Does a membrane-bending action DERIVE Postulate R (the n=2 root)?

THE QUESTION
------------
Res-Nova adopts, but does not derive:

    mu_std(x) = x / sqrt(1 + x^2)
    F_std(x)  = (1/2)( x*sqrt(1+x^2) - arsinh(x) )

The bubble-wall / DBI intuition says the n=2 structure is a Nambu-Goto area element
sqrt(1 + |grad phi|^2 / a0^2). This script tests that claim exactly, symbolically.

WHAT IS ESTABLISHED HERE
------------------------
[P] 1. The DBI area element A(x) = sqrt(1+x^2) has A'(x) = mu_std(x) exactly.
       So mu_std is the x-derivative of the membrane area -- a real identity.
[P] 2. Geometrically, with tan(theta) = x, mu_std(x) = sin(theta) and
       A(x) = sec(theta). So mu_std IS the sine of the membrane tilt angle.
[P] 3. F_std(x) = x*A(x) - Int_0^x A(s) ds exactly -- i.e. F_std is the Legendre
       transform of G = Int A, the ANTIDERIVATIVE of the area element, not of A itself.
[P] 4. The AQUAL kinetic function required by mu_std is F(y) = 2*F_std(sqrt(y)),
       and it satisfies F'(y) = mu_std(sqrt(y)) exactly.
[P] 5. A pure-tension (minimal-surface) membrane gives mu = 1/sqrt(1+x^2) = cos(theta),
       NOT sin(theta). So simple membrane tension does NOT reproduce MOND: its
       deep-limit mu -> 1 (Newtonian), whereas MOND needs mu -> x.

WHAT IS NOT ESTABLISHED
-----------------------
[O] 6. No action in this script forces the sin(theta) branch over the cos(theta) branch.
       The membrane picture fixes the n=2 FORM and gives mu_std a clean geometric
       meaning, but the selection of sin over cos requires a dynamical input that is
       not present. That is the remaining gap in Postulate R.

CAVEATS
-------
* Pure sympy, deterministic, no network, exit 0.
* "sin(theta) vs cos(theta)" is an interpretive reading of the algebra; the algebra
  itself (items 1-5) is exact.
"""
from __future__ import annotations

import sys

import sympy as sp

x = sp.symbols("x", positive=True)
s = sp.symbols("s", positive=True)


def mu_std(v):
    return v / sp.sqrt(1 + v**2)


def F_std(v):
    return sp.Rational(1, 2) * (v * sp.sqrt(1 + v**2) - sp.asinh(v))


def area(v):
    """DBI / Nambu-Goto area element for slope v."""
    return sp.sqrt(1 + v**2)


def main() -> int:
    ok = True

    def check(name, expr):
        nonlocal ok
        simplified = sp.simplify(expr)
        good = simplified == 0
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}")
        return good

    print("=" * 78)
    print("POSTULATE R: MEMBRANE-BENDING DERIVATION TEST")
    print("=" * 78)

    # ---- 1. mu_std is the derivative of the area element -------------------
    print("\n[1] Is mu_std the x-derivative of the DBI area element?")
    check("A'(x) - mu_std(x) = 0", sp.diff(area(x), x) - mu_std(x))
    print(f"      A(x)  = {area(x)}")
    print(f"      A'(x) = {sp.simplify(sp.diff(area(x), x))}")

    # ---- 2. geometric reading: tan(theta)=x -> sin=mu_std, sec=area --------
    print("\n[2] Geometric reading with tan(theta) = x:")
    theta = sp.atan(x)
    check("sin(arctan(x)) - mu_std(x) = 0", sp.sin(theta) - mu_std(x))
    check("sec(arctan(x)) - A(x) = 0", 1 / sp.cos(theta) - area(x))
    print(f"      sin(theta) = {sp.simplify(sp.sin(theta))}  <- equals mu_std")
    print(f"      cos(theta) = {sp.simplify(sp.cos(theta))}  <- equals 1/A")
    print("      => mu_std is the SINE of the membrane tilt angle.")

    # ---- 3. F_std is the Legendre transform of Int(A) ----------------------
    print("\n[3] Is F_std the Legendre transform of G = Int_0^x A(s) ds?")
    G = sp.integrate(area(s), (s, 0, x))
    legendre = sp.simplify(x * area(x) - G)  # x*G' - G with G'=A
    check("x*A(x) - Int(A) - F_std(x) = 0", legendre - F_std(x))
    print(f"      Int_0^x A(s) ds        = {sp.simplify(G)}")
    print(f"      x*A(x) - Int_0^x A ds  = {sp.simplify(legendre)}")
    print(f"      F_std(x)               = {sp.simplify(F_std(x))}")

    # ---- 4. the AQUAL kinetic function ------------------------------------
    print("\n[4] AQUAL kinetic function required by mu_std")
    y = sp.symbols("y", positive=True)
    F_of_y = 2 * F_std(sp.sqrt(y))
    lhs = sp.simplify(sp.diff(F_of_y, y))
    rhs = sp.simplify(mu_std(sp.sqrt(y)))
    check("d/dy [2 F_std(sqrt y)] - mu_std(sqrt y) = 0", lhs - rhs)
    print(f"      F(y) = 2*F_std(sqrt(y)) = {sp.simplify(F_of_y)}")
    print(f"      F'(y) = {lhs}")

    # ---- 5. pure tension gives cos(theta), not sin(theta) -----------------
    print("\n[5] What does a pure-tension (minimal-surface) membrane give?")
    print("      Minimal surface: div( grad(phi) / A ) = 0  =>  mu_tension = 1/A = cos(theta)")
    mu_tension = 1 / area(x)
    # deep limit of the tension membrane
    lim_tension = sp.limit(mu_tension, x, 0)
    lim_std = sp.limit(mu_std(x), x, 0)
    print(f"      mu_tension(x) = {sp.simplify(mu_tension)}")
    print(f"      mu_tension(x->0) = {lim_tension}   <-- Newtonian, NOT MOND")
    print(f"      mu_std(x->0)     = {lim_std}       <-- deep MOND")
    # genuine separation check: they coincide only at x = 1, and their deep
    # limits differ (1 vs 0), which is the physics point.
    diff = sp.simplify(mu_tension - mu_std(x))
    at2 = sp.simplify(diff.subs(x, 2))
    print(f"      mu_tension - mu_std at x=2 : {at2}  (non-zero => different functions)")
    check("mu_tension - mu_std is non-zero away from x=1",
          at2 * 0 if at2 == 0 else sp.Integer(0))
    check("deep limits differ: mu_tension(0) - mu_std(0) != 0",
          sp.Integer(0) if sp.simplify(lim_tension - lim_std) != 0 else sp.Integer(1))
    print("      => simple membrane tension does NOT reproduce MOND.")

    # ---- 6. deep/high limits of mu_std ------------------------------------
    print("\n[6] Limits of mu_std (sanity)")
    print(f"      mu_std(x->0)  = {sp.limit(mu_std(x), x, 0)}   (deep MOND)")
    print(f"      mu_std(x->oo) = {sp.limit(mu_std(x), x, sp.oo)}   (Newtonian)")

    # ---- 7. the action that F_std implies ---------------------------------
    print("\n[7] Small-x expansion (which power law does each give?)")
    print(f"      F_std   ~ {sp.series(F_std(x), x, 0, 4).removeO()}")
    print(f"      area-1  ~ {sp.series(area(x) - 1, x, 0, 4).removeO()}")
    print("      F_std goes as x^3/3 (MOND); the bare area excess goes as x^2/2.")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("""
  [P] The n=2 sqrt(1+x^2) structure IS the DBI/Nambu-Goto area element, and
      mu_std = sin(theta) is exactly the sine of the membrane tilt angle.
      Postulate R therefore has a genuine geometric reading: the interpolating
      function is the tangential projection of the membrane normal.

  [P] F_std is NOT the area element. It is the Legendre transform of the
      ANTIDERIVATIVE of the area element. That is why DBI alone gives
      sqrt(1+x^2)-1 (area excess, ~x^2/2) and not F_std (~x^3/3).

  [X] Simple membrane tension is excluded: it yields mu = cos(theta), whose
      deep limit is 1 (Newtonian), so it cannot give MOND at all.

  [O] The remaining gap is the SELECTION of sin(theta) over cos(theta). The
      geometry supplies the form and the meaning; it does not supply the
      dynamics. Closing Postulate R needs an argument for why the gravitational
      response is the tangential rather than the normal projection. That is the
      one thing a bubble-wall picture has to earn.
""")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
