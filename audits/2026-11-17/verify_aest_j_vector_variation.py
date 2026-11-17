#!/usr/bin/env python3
"""Exact component check of the AeST J^mu nabla_mu phi vector variation.

This is deliberately a narrow regression check. It isolates the J-term on a
unit-timelike Minkowski configuration; it is not a full tensor variation of
the AeST action.
"""
import sympy as sp


def main() -> None:
    t, b = sp.symbols("t b", real=True)
    a = sp.Function("a")(t)

    # Minkowski signature (-+++), A^mu=(a(t),0,0,0), and phi=t^2/2.
    # At the background a=1, the unit constraint A^mu A_mu=-1 is satisfied.
    phi = t**2 / 2
    p0 = sp.diff(phi, t)

    # J^0 = A^0 d_t A^0; the action term is 2 b J^mu partial_mu phi.
    lagrangian_j = 2 * b * a * sp.diff(a, t) * p0

    # Euler-Lagrange derivative with respect to the contravariant component A^0.
    euler_a_contrav = sp.simplify(
        sp.diff(lagrangian_j, a)
        - sp.diff(sp.diff(lagrangian_j, sp.diff(a, t)), t)
    )

    # A_0=-A^0 in this signature, so delta/delta A_0 is minus delta/delta A^0.
    euler_a_cov = sp.simplify(-euler_a_contrav).subs(a, 1)

    # B^0 = p_mu partial^0 A^mu - partial_mu(A^mu p^0) = 1 at this background.
    b0 = sp.simplify(-sp.diff(-t, t))

    action_full_coefficient = sp.simplify(euler_a_cov / b0)
    action_normalized_coefficient = sp.simplify(action_full_coefficient / 2)
    printed_normalized_coefficient = 2 * b
    discrepancy = sp.simplify(
        printed_normalized_coefficient - action_normalized_coefficient
    )

    assert sp.simplify(euler_a_cov - 2 * b) == 0
    assert sp.simplify(b0 - 1) == 0
    assert sp.simplify(action_normalized_coefficient - b) == 0
    assert sp.simplify(discrepancy - b) == 0

    print("J-term full Euler coefficient (covector A_0):", euler_a_cov)
    print("B^0:", b0)
    print("Action normalized coefficient:", action_normalized_coefficient)
    print("Printed Eq. (4) normalized coefficient:", printed_normalized_coefficient)
    print("Difference (printed minus action):", discrepancy)
    print("PASS: exact component check; this isolates the J-term only.")


if __name__ == "__main__":
    main()
