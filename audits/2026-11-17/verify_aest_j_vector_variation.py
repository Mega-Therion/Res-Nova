#!/usr/bin/env python3
"""Exact symbolic regression checks for the AeST vector-equation discrepancy.

Checks:
1. The J^mu nabla_mu phi contribution to the covector Euler derivative.
2. A constrained 1+1 Minkowski configuration where the candidate Noether
   residual caused by the printed 2024 vector equation is nonzero.

This is a component regression, not a complete 4D tensor proof.
"""
import sympy as sp


def check_j_term_variation() -> None:
    t, b = sp.symbols("t b", real=True)
    a = sp.Function("a")(t)
    phi = t**2 / 2
    p0 = sp.diff(phi, t)
    lagrangian_j = 2 * b * a * sp.diff(a, t) * p0

    euler_a_contrav = sp.simplify(
        sp.diff(lagrangian_j, a)
        - sp.diff(sp.diff(lagrangian_j, sp.diff(a, t)), t)
    )
    # A_0=-A^0 in signature (-,+,+,+).
    euler_a_cov = sp.simplify(-euler_a_contrav).subs(a, 1)
    b0 = sp.simplify(-sp.diff(-t, t))
    normalized_action = sp.simplify(euler_a_cov / (2 * b0))
    printed_normalized = 2 * b
    discrepancy = sp.simplify(printed_normalized - normalized_action)

    assert sp.simplify(euler_a_cov - 2 * b) == 0
    assert sp.simplify(b0 - 1) == 0
    assert sp.simplify(normalized_action - b) == 0
    assert sp.simplify(discrepancy - b) == 0
    print("J-term variation: PASS; full Euler=2b, B^0=1, normalized action=b, printed=2b")


def check_noether_residual() -> None:
    t, eps, b = sp.symbols("t eps b", real=True)
    chi = eps * t
    A_up = [sp.cosh(chi), sp.sinh(chi)]
    A_down = [-A_up[0], A_up[1]]
    p_down = [sp.Integer(1), sp.Integer(1)]  # phi=t+x
    p_up = [-sp.Integer(1), sp.Integer(1)]

    # B^nu = p_mu partial^nu A^mu - partial_mu(A^mu p^nu).
    B = []
    for nu in range(2):
        first = p_down[0] * (-sp.diff(A_up[0], t) if nu == 0 else 0)
        first += p_down[1] * (-sp.diff(A_up[1], t) if nu == 0 else 0)
        second = sp.diff(A_up[0] * p_up[nu], t)  # x derivatives vanish
        B.append(sp.simplify(first - second))

    F01 = sp.diff(A_down[1], t)
    F = [[sp.Integer(0), F01], [-F01, sp.Integer(0)]]
    div_B = sp.diff(B[0], t)  # plus d_x B^1=0
    residual = [
        sp.simplify(
            sum(B[mu] * F[nu][mu] for mu in range(2))
            - A_down[nu] * div_B
        )
        for nu in range(2)
    ]
    full_noether_shift = [sp.simplify(2 * b * value) for value in residual]

    assert sp.simplify(-A_up[0] ** 2 + A_up[1] ** 2 + 1) == 0
    assert sp.simplify(B[0] + eps * sp.cosh(chi)) == 0
    assert sp.simplify(B[1] + eps * sp.sinh(chi)) == 0
    assert sp.simplify(F01 - eps * sp.cosh(chi)) == 0
    assert sp.simplify(div_B + eps**2 * sp.sinh(chi)) == 0
    assert sp.simplify(residual[0] + eps**2 * sp.sinh(2 * chi)) == 0
    assert sp.simplify(residual[1] - eps**2 * sp.cosh(2 * chi)) == 0
    assert sp.simplify(full_noether_shift[0] + 2 * b * eps**2 * sp.sinh(2 * chi)) == 0
    assert sp.simplify(full_noether_shift[1] - 2 * b * eps**2 * sp.cosh(2 * chi)) == 0
    print("Noether residual: PASS; unit constraint holds and residual is generically nonzero")
    print("  R_0 =", residual[0], "; R_1 =", residual[1])
    print("  full identity shift =", full_noether_shift)


def main() -> None:
    check_j_term_variation()
    check_noether_residual()
    print("PASS: all exact symbolic AeST audit assertions passed.")


if __name__ == "__main__":
    main()
