#!/usr/bin/env python3
"""SymPy check of the screening split in MuStdSelection.lean.

mu_dual(x) = x/(1+x) is not inverse-square screened: x^2 * (1 - mu_dual(x))
is unbounded. mu_std(x) = x/sqrt(1+x^2) is: x^2 * (1 - mu_std(x)) <= 1 for x >= 1.
Exit 0 only if both identities hold. This is not a Lean, Coq, or Isabelle proof.
"""

import sys

import sympy as sp


def main() -> int:
    x = sp.symbols("x", real=True, positive=True)
    mu_dual = x / (1 + x)
    mu_std = x / sp.sqrt(1 + x**2)
    tail_dual = sp.simplify(1 - mu_dual)
    tail_std = sp.simplify(1 - mu_std)
    if tail_dual != 1 / (1 + x):
        print("FAIL dual tail", tail_dual)
        return 1
    s = sp.sqrt(1 + x**2)
    rationalised = sp.simplify(tail_std * s * (s + x))
    if rationalised != 1:
        print("FAIL std rationalisation", rationalised)
        return 1
    # For x >= 1, s >= x, so s(s+x) >= x^2 and the tail is <= 1/x^2.
    # x^2 <= S(S+x) iff S(S+x) - x^2 = 1 + x*S > 0, so the tail is <= 1/x^2.
    gap = sp.simplify(s * (s + x) - x**2)
    if gap != 1 + x * s:
        print("FAIL std gap", gap)
        return 1
    # Unbounded dual tail: lim x->oo of x^2 * (1-mu_dual) = oo
    lim = sp.limit(x**2 * tail_dual, x, sp.oo)
    if lim != sp.oo:
        print("FAIL dual limit", lim)
        return 1
    print("sympy", sp.__version__)
    print("PASS 1-mu_dual = 1/(1+x)")
    print("PASS 1-mu_std = 1/(S(S+x)) and x^2(1-mu_std) <= 1")
    print("PASS lim x^2(1-mu_dual) = oo, so no inverse-square C exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
