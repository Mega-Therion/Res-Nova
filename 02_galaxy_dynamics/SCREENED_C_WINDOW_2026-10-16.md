# Working solution: C inside the Oort window

**Choice:** RY, 2026-10-16. Use the closed form below. `C = 0` stays the failed pre-registered case `[X]`. This note does not retune `a₀`, `μ_std`, or `x*`.

**Tier:** the algebra and the match to `SCREENED_C_SOLUTIONS.json` are `[D]`. `screened_c_window_check.py` exits 0 and prints `MATCH`. One-field `χ` is still impossible: `η` is one number at one point, and the Sun needs `1.637–2.068` while the Milky Way needs `3.0×10⁻³`.

## Equation

For a uniform external field the radial binding offset is linear in the Lagrangian zero,

```
(1/a)(C) = (1/a)(0) * (P(y_e) - C) / P(y_e)
C = P(y_e) * (1 - (1/a)_target / (1/a)(0))
```

`P` and `(1/a)(0)` are the JSON fields `P_ye` and `C_zero.inv_a_au`. A constant `C` does not change `ν_eff`.

## Solution

The Oort window is `10⁴–10⁵` au. The check script’s solution, which matches the stored centre with error 0, is:

| `g_e` (m s⁻²) | `C` for `10⁴` au | `C` centre | `C` for `10⁵` au |
|---|---|---|---|
| 1.90×10⁻¹⁰ | 0.208899 | 0.579125 | 0.696200 |
| 2.32×10⁻¹⁰ | 0.384925 | 0.755150 | 0.872226 |

The working value at the decision field `1.90×10⁻¹⁰` is the centre, `C = 0.579125`, which is `C_oort_peak` in the JSON. The window is the range around it.
