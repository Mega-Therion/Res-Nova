#!/usr/bin/env python3
"""The chi_floor x chi_ceil = ln2 relation is impossible, not underived.

Section VII.1 of FIG_TREE_MONOGRAPH.md. Regenerates the table printed there.

The product of the two band endpoints is an ALGEBRAIC number; ln 2 is
TRANSCENDENTAL by Lindemann-Weierstrass. No derivation can bridge that, so the
prior status [O] "not yet derived" was wrong in the direction of optimism.

Tests both readings of theta that circulate in the corpus, because the obvious
attack on the argument is that the endpoints might not be algebraic.
"""
from sympy import Rational, sqrt, log, simplify, minimal_polynomial, symbols, degree, N

x = symbols("x")
READINGS = [
    ("7/10 (band ceiling)", Rational(7, 10)),
    ("1/sqrt(2) (chiFloor in Lean)", 1 / sqrt(2)),
]


def main():
    ln2 = log(2)
    print(f"ln 2 = {N(ln2, 15)}  (transcendental, Lindemann-Weierstrass)\n")
    ok = True
    for name, theta in READINGS:
        kappa = sqrt(theta * (2 - theta))
        product = simplify(kappa / sqrt(2))          # chi_floor = 1/sqrt(2)
        mp = minimal_polynomial(product, x)
        gap = float(100 * abs(product - ln2) / ln2)
        print(f"theta = {name}")
        print(f"  kappa   = {simplify(kappa)} = {N(kappa, 12)}")
        print(f"  product = {product} = {N(product, 12)}")
        print(f"  minimal polynomial {mp}, degree {degree(mp)} -> ALGEBRAIC")
        print(f"  gap to ln2: {gap:.3f}%\n")
        # An algebraic number has a minimal polynomial over Q; a transcendental
        # one has none. Existence here IS the impossibility proof.
        ok &= mp is not None and degree(mp) >= 1

    assert ok, "every reading must yield an algebraic product"
    print("Algebraic numbers form a field closed under radicals, so any theta that")
    print("is rational or a radical gives an algebraic product. Escaping the")
    print("argument needs a TRANSCENDENTAL theta; neither corpus value is one.")
    print("\nVERDICT: chi_floor x chi_ceil = ln2 is IMPOSSIBLE. Status [X], not [O].")


if __name__ == "__main__":
    main()
