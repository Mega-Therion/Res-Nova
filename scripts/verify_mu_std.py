from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

x, psi = sp.symbols("x psi", real=True)

mu_std = x / sp.sqrt(1 + x**2)
F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))

# Exact identities: these are symbolic certificates, not physical derivations.
constitutive_residual = sp.simplify(sp.diff(F_std, x) - x * mu_std)
assert constitutive_residual == 0, constitutive_residual

rapidity_residual = sp.simplify(mu_std.subs(x, sp.sinh(psi)) - sp.tanh(psi))
assert rapidity_residual == 0, rapidity_residual

deep_series = sp.series(mu_std, x, 0, 8).removeO()
high_series = sp.series(mu_std.subs(x, 1 / x), x, 0, 8).removeO().subs(x, 1 / x)
expected_deep = x - sp.Rational(1, 2) * x**3 + sp.Rational(3, 8) * x**5 - sp.Rational(5, 16) * x**7
expected_high = 1 - sp.Rational(1, 2) / x**2 + sp.Rational(3, 8) / x**4 - sp.Rational(5, 16) / x**6
assert sp.expand(deep_series - expected_deep) == 0, (deep_series, expected_deep)
assert sp.expand(high_series - expected_high) == 0, (high_series, expected_high)

mu_prime = sp.simplify(sp.diff(mu_std, x))
assert sp.simplify(mu_prime - (1 + x**2) ** sp.Rational(-3, 2)) == 0, mu_prime

F_second = sp.simplify(sp.diff(F_std, x, 2))
expected_F_second = x * (x**2 + 2) / (x**2 + 1) ** sp.Rational(3, 2)
assert sp.simplify(F_second - expected_F_second) == 0, F_second

certificate = {
    "definition": "mu_std(x) = x/sqrt(1+x^2)",
    "potential": "F_std(x) = (x*sqrt(1+x^2)-asinh(x))/2",
    "F_derivative": "dF_std/dx = x*mu_std(x)",
    "rapidity_identity": "mu_std(sinh(psi)) = tanh(psi)",
    "deep_series": str(deep_series),
    "newtonian_series": str(high_series),
    "mu_derivative": str(mu_prime),
    "F_second_derivative": str(F_second),
    "evidence_boundary": "P_math only; no covariant action-level or empirical claim",
}

# Certificate lives with the other recovered artifacts, not beside the script.
output_path = Path(__file__).resolve().parent.parent / "docs" / "recovered" / "mu_std_certificate.json"
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print("PASS: dF_std/dx = x*mu_std exactly")
print("PASS: mu_std(sinh(psi)) = tanh(psi) exactly")
print(f"PASS: deep series  = {deep_series}")
print(f"PASS: high series  = {high_series}")
print(f"PASS: mu_std'(x)   = {mu_prime}")
print(f"PASS: F_std''(x)   = {F_second}")
print(f"PASS: machine-readable certificate written to {output_path}")
print("STATUS: constitutive mathematics verified; physical action-level derivation remains open")
