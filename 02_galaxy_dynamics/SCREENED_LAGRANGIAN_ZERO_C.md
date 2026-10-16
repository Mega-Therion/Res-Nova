# Screened field equation with the Lagrangian zero C

**Tier:** the equation is the variation of the action already used for the tidal screen. `C = 0` is the pre-registered model and stays `[X]` on the Oort cloud. Any `C ≠ 0` that moves the binding edge is a different model and stays `[O]`. This note does not adopt it and does not retune `a₀`, `μ_std`, or `x*`.

## Equation

Quasistatic QUMOND with the tidal screen on the Newtonian Hessian, and a constant zero `C` of the screened MOND Lagrangian:

```
L = -(1/(8πG)) [ 2 ∇Φ · ∇Φ_N - a₀² Qs ] - ρ Φ
Qs = z + S(x) (Q(z) - z - C)
z = y²,   y = |∇Φ_N| / a₀
P(y) = Q(z) - z = ∫₀ʸ 2t (ν(t) - 1) dt
x = c² ‖∇∇Φ_N‖ / a₀²
S(x) = 1 / (1 + (x/x*)²)
```

`C = 0` is the sentence in `OORT_TORQUE_2026-10-16.md`: no MOND energy where there is no field. Because `C` does not depend on `z`, `ν_eff = 1 + S(ν - 1)` is unchanged. The Hessian stress is not:

```
W_ij = -(c²/2) S'(x) (P(y) - C) H_ij / √(|H|² + h_g²)
```

For a lone Sun, `|H|_F = √6 GM / r³`. The radial operator from `PREREG_MASS_STRATIFIED_DIP_2026-10-16.md` is

```
g_W = (2/√6) r⁻³ d/dr (r³ w̃)
w̃ = -(c²/2) S'(x) (P(y_e) - C) |H| / Hn
```

Outward is positive. A comet that falls from rest at infinity has osculating

```
1/a = 2 Φ_W(0) / GM,    Φ_W(0) = ∫₀^∞ g_W(r) dr.
```

`g_W` is linear in `(P(y_e) - C)` when the external field is uniform, so one run at `C = 0` fixes the `C` that places `1/a` at a chosen edge.

## What the script solves

`screened_c_solutions.py` evaluates that radial operator on a logarithmic grid and writes `SCREENED_C_SOLUTIONS.json`. It reports, at the Cassini action value of `x*` and at both Galactic fields used in the Oort note:

- `C = 0`: whether net radial gravity changes sign (outward), and the numeric `1/a`.
- `C` such that `1/a` equals `1/√(10⁴ × 10⁵)` au⁻¹, the geometric centre of the observed Oort window. That `C` stays `[O]`.
- `C = P(y_e)`, which cancels the W push. Recorded so the zero of the offset is not confused with the value that sits inside the window.

The numbers in the ledger are whatever that JSON contains after a clean run. They are not typed in here.
