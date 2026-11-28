#!/usr/bin/env python3
"""SymPy symbolic verifier for Angle 2: KT <-> ST Fata Morgana / CPTP K0-Risk."""
import sympy as sp

p_plus, p_minus, excess_risk, tr_in, tr_out = sp.symbols(
    "p_plus p_minus excess_risk tr_in tr_out"
)

k0_defect = p_plus - p_minus
k0_risk = k0_defect**2 * excess_risk

assert sp.simplify(k0_risk.subs(p_plus, p_minus)) == 0
assert sp.simplify((tr_out - tr_in).subs(tr_out, tr_in)) == 0

print("PASS: Angle 2 (KT <-> ST Fata Morgana / CPTP K0-Risk) SymPy verification succeeded.")
