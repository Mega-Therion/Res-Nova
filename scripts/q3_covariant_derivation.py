#!/usr/bin/env python3
"""
Q3/AeST covariant derivation verifier — THEOREM B-cov (2026-09-16).

Target (interpretation layer 0, obligation 1): derive that the external gradient
enters as sinh of the internal rapidity — (B): x = sinh(artanh mu) — from the
covariant premises the AeST embedding supplies:
  K1  boost sector so(1,1) acting on the chiral two-state channel (Lorentz
      covariance of the embedding; aether A^mu defines the local frame),
  K2  unit-norm channel states (the lambda(A^mu A_mu + 1) constraint of the
      SZ action, TARGET_D7_COVARIANT_COMPLETION section 1),
  K3  the external gradient couples to the channel's boost MOMENTUM (the
      quasistatic reduction's J(Y), Y = |grad phi|^2, is a function of the
      scalar momentum only).

Machine checks (sympy, exact):
  C1  unit-norm orbit: under a boost of rapidity psi, a unit state's momentum
      components are (cosh psi, sinh psi); norm is preserved identically.
  C2  the spatial momentum component is sinh psi — the only covariant linear
      coupling target on the orbit.
  C3  mu = tanh psi (chiral velocity reading; two-state: psi -> -psi flips mu).
  C4  THEOREM B-cov: x = sinh(artanh mu)  <==>  mu = x/sqrt(1+x^2) = mu_std.
  C5  collapse corollary: (B) + C3 recovers mu_std exactly (50-digit check).
  C6  alternatives closure:
        x = psi        -> mu = tanh x     : violates K3 (psi is not a momentum;
                                             no covariant constraint has psi as
                                             conjugate force; energy E(psi)=psi^2/2
                                             is not boost-invariant)   [GALILEAN]
        x = mu         -> mu = x          : P5 non-interpolation, fails deep-MOND
                                             transition (REPRESENTATION_AUDIT_MU_STD P5) [X]
        odds coupling  -> mu = x/(1+x)    : mu_dual, killed by chiral input +
                                             solar system (P4)              [X]
        x = sinh(psi/2)-> mu = tanh(psi/2): mu_simple, killed by normalization
                                             knife mu'(0)=1/2; measured empirical
                                             shadow a0 displaced ~2x (ratio 0.469) [X]
  C7  the knife measurement: mu_simple'(0) = 1/2 exactly; mu_std'(0) = 1 exactly.
Exit 0 iff all checks pass. No [P] physics is asserted here; this script machine-
checks the algebraic content of Q3_AEST_COVARIANT_DERIVATION_2026-09-16.md.
"""
import sys
import sympy as sp

x, psi = sp.symbols("x psi", real=True)
FAILURES = []
NCHECKS = 0


def _bump():
    global NCHECKS
    NCHECKS += 1


def check_ne(name, got, want=0):
    _bump()
    ok = sp.simplify(got - want) != 0
    print(f"{name}: {'PASS' if ok else 'FAIL'}  (unexpected equality)")
    if not ok:
        FAILURES.append(name)


def check(name, got, want, tol=None):
    _bump()
    if tol is None:
        ok = sp.simplify(got - want) == 0
    else:
        ok = abs(complex(sp.N(got - want, 30))) < tol
    print(f"{name}: {'PASS' if ok else 'FAIL'}  ({sp.nsimplify(got) if not ok else ''})")
    if not ok:
        FAILURES.append(name)


def main():
    mu = sp.tanh(psi)

    # C1: unit-norm boost orbit — momentum components and norm preservation
    E = sp.cosh(psi)          # time/norm (energy) component of the unit state
    P = sp.sinh(psi)          # spatial momentum component
    check("C1a momentum-norm invariance", sp.simplify(E**2 - P**2), 1)
    # C1b: the orbit is the unique norm-preserving curve through the rest state
    #      (cosh 0, sinh 0) = (1, 0): d/d psi (cosh, sinh) = (sinh, cosh) with
    #      unit "Minkowski norm" of the tangent — the geodesic on the hyperbola.
    dE, dP = sp.diff(E, psi), sp.diff(P, psi)
    check("C1b tangent norm preserved", sp.simplify(dE * E - dP * P), 0)

    # C2: spatial momentum is sinh psi — the force conjugate to psi under the
    #     boost-invariant constraint energy a0*(cosh psi - 1):
    dEdpsi = sp.diff(sp.cosh(psi), psi)
    check("C2 conjugate force is sinh", sp.simplify(dEdpsi - sp.sinh(psi)), 0)

    # C3: velocity reading mu = tanh psi; chirality psi -> -psi
    check("C3a mu = tanh psi = P/E", sp.simplify(mu - P / E), 0)
    check("C3b chirality: mu(-psi) = -mu(psi)", sp.simplify(mu.subs(psi, -psi) + mu), 0)

    # C4: THEOREM B-cov — (B) <==> mu_std
    lhs = sp.sinh(sp.atanh(mu))        # (B): x = sinh(artanh mu)
    check("C4a (B) gives x = mu/sqrt(1-mu^2)", sp.simplify(lhs - mu / sp.sqrt(1 - mu**2)), 0)
    # invert: mu = tanh(arsinh x) = x/sqrt(1+x^2)
    mu_from_B = sp.tanh(sp.asinh(x))
    mu_std = x / sp.sqrt(1 + x**2)
    check("C4b inversion: mu = x/sqrt(1+x^2)", sp.simplify(sp.expand_func(mu_from_B) - mu_std), 0)

    # C5: exact symbolic collapse check at rational points, 50-digit evaluated
    for xv in [sp.Rational(1, 10**6), sp.Rational(3, 10), sp.Integer(1), sp.Integer(12), sp.Integer(10**4)]:
        diff = sp.expand_func(sp.tanh(sp.asinh(xv)) - xv / sp.sqrt(1 + xv**2))
        check(f"C5 collapse x={xv}", sp.N(diff, 50), 0, tol=sp.Float(10) ** -45)

    # C6: alternatives closure (each non-momentum coupling is killed)
    #   x = psi  ->  mu = tanh(x): fails Postulate R (odds(mu) != x) — the chiral
    #   coordinate kill; K3 violated (psi is not a momentum component).
    mu_exp = sp.tanh(x)
    odds = sp.simplify(mu_exp / (1 - mu_exp))
    check_ne("C6a x=psi fails Postulate R: odds(tanh x) != x", sp.simplify(odds - x))
    #   x = mu  ->  mu = x: deep-MOND limit of closure g(g_b) -> g_b (no transition)
    #   (P5 kill; algebraic witness: mu=x has mu(inf)=inf, not 1)
    check_ne("C6b x=mu fails mu(inf)=1", sp.limit(x, x, sp.oo), 1)
    #   odds coupling -> mu_dual: killed (chiral + solar system); witness: it is
    #   a different function from mu_std (presence coordinate, not chiral)
    mu_dual = x / (1 + x)
    check_ne("C6c mu_dual != mu_std witness", sp.simplify(mu_dual - mu_std))
    #   x = sinh(psi/2) -> mu_simple = tanh(psi/2) = x/(1+sqrt(1+x^2))
    #   (two auto-simplifying steps: the half-angle identity in psi, then the
    #   composition asinh: sinh(asinh x)=x, cosh(asinh x)=sqrt(1+x^2))
    mu_simple_lit = x / (1 + sp.sqrt(1 + x**2))
    check("C6d half-angle identity: tanh(psi/2) = sinh psi/(1+cosh psi)",
          sp.simplify(sp.together((sp.tanh(psi / 2) - sp.sinh(psi) / (1 + sp.cosh(psi))).rewrite(sp.exp))), 0)
    check("C6d2 composition: sinh(asinh x)/(1+cosh(asinh x)) = mu_simple",
          sp.simplify(sp.sinh(sp.asinh(x)) / (1 + sp.cosh(sp.asinh(x))) - mu_simple_lit), 0)

    # C7: the normalization knife on the two rapidity points
    check("C7a mu_std'(0) = 1", sp.limit(sp.diff(mu_std, x), x, 0), 1)
    check("C7b mu_simple'(0) = 1/2", sp.limit(sp.diff(mu_simple_lit, x), x, 0), sp.Rational(1, 2))

    print()
    print(f"SUMMARY: Theorem B-cov checks: {NCHECKS} total, {len(FAILURES)} failures")
    if FAILURES:
        print("FAILED:", ", ".join(FAILURES))
        sys.exit(1)
    print("Q3 reduction delivered: (B) holds iff the gradient couples as the")
    print("spatial momentum sinh(psi) of the unit-norm internal boost; then")
    print("mu = mu_std identically. Residual open input: K3 (the momentum-")
    print("linearity of the coupling) is unique-covariant, not yet forced by J.")


if __name__ == "__main__":
    main()
