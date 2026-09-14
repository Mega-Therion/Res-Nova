from __future__ import annotations

import sympy as sp

x, psi = sp.symbols("x psi", real=True)

mu_std = x / sp.sqrt(1 + x**2)
F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))

# Exact AQUAL constitutive identity.
constitutive_residual = sp.simplify(sp.diff(F_std, x) - x * mu_std)
assert constitutive_residual == 0, constitutive_residual

# Exact rapidity conjugacy on the real line.
rapidity_residual = sp.simplify(mu_std.subs(x, sp.sinh(psi)) - sp.tanh(psi))
assert rapidity_residual == 0, rapidity_residual

# Local and asymptotic expansions.
deep_series = sp.series(mu_std, x, 0, 6).removeO()
high_series = sp.series(mu_std.subs(x, 1/x), x, 0, 6).removeO().subs(x, 1/x)
expected_deep = x - sp.Rational(1, 2) * x**3 + sp.Rational(3, 8) * x**5
expected_high = 1 - sp.Rational(1, 2) / x**2 + sp.Rational(3, 8) / x**4
assert sp.expand(deep_series - expected_deep) == 0, (deep_series, expected_deep)
assert sp.expand(high_series - expected_high) == 0, (high_series, expected_high)

# Strict monotonicity: derivative is positive for x>0.
mu_prime = sp.simplify(sp.diff(mu_std, x))
assert sp.simplify(mu_prime - (1 + x**2) ** sp.Rational(-3, 2)) == 0, mu_prime

# Convexity of F_std follows from F'' = mu + x mu'.
F_second = sp.simplify(sp.diff(F_std, x, 2))
expected_F_second = x / sp.sqrt(1 + x**2) + x / (1 + x**2) ** sp.Rational(3, 2)
assert sp.simplify(F_second - expected_F_second) == 0, F_second

print("PASS: dF_std/dx = x*mu_std exactly")
print("PASS: mu_std(sinh(psi)) = tanh(psi) exactly")
print(f"PASS: deep series  = {deep_series}")
print(f"PASS: high series  = {high_series}")
print(f"PASS: mu_std'(x)   = {mu_prime}")
print(f"PASS: F_std''(x)   = {F_second}")
print("STATUS: constitutive mathematics verified; physical action-level derivation remains open")
