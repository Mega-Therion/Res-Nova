#!/usr/bin/env python3
"""Independent re-check of the D3 §8 lambda_s table.

D3 derives the residual left by mu_std beyond Newton,

    delta_g(r) = (1 + lambda_s)^3 a_0^2 r^2 / (2 G_N M)

which GROWS as r^2, so the binding solar-system datum is the outermost body,
not the innermost. This recomputes the published table from CODATA/IAU inputs
and checks each column, rather than trusting the transcription.

    python3 lambda_s_solar_system_check.py
"""
from __future__ import annotations

A0 = 1.116e-10          # m/s^2, SPARC-measured (D3 §8)
GM_SUN = 1.32712440018e20   # m^3/s^2, IAU nominal
AU = 1.495978707e11     # m, IAU definition
Q2_MAX = 3.4e-27        # s^-2, Cassini-type quadrupole ceiling used in D3 §8

# (body, r/AU, published g_N, delta_g, Q2, margin, lambda_s ceiling)
PUBLISHED = [
    ("Mercury", 0.387, 3.957e-2, 1.574e-19, 2.717e-30, 1251, 9.78),
    ("Earth",   1.000, 5.930e-3, 1.050e-18, 7.020e-30,  484, 6.85),
    ("Mars",    1.524, 2.554e-3, 2.438e-18, 1.070e-29,  318, 5.83),
    ("Jupiter", 5.204, 2.189e-4, 2.844e-17, 3.653e-29, 93.1, 3.53),
    ("Saturn",  9.583, 6.458e-5, 9.643e-17, 6.727e-29, 50.5, 2.70),
    ("Uranus",  19.22, 1.606e-5, 3.878e-16, 1.349e-28, 25.2, 1.93),
]


def row(r_au: float, lam: float = 0.0):
    r = r_au * AU
    g_n = GM_SUN / r**2
    delta_g = (1 + lam) ** 3 * A0**2 * r**2 / (2 * GM_SUN)
    q2 = delta_g / r
    margin = Q2_MAX / q2
    return g_n, delta_g, q2, margin, margin ** (1 / 3) - 1


def main() -> None:
    tol = 0.02
    print(f"{'body':<9}{'g_N':>11}{'delta_g':>12}{'Q2':>12}{'margin':>9}"
          f"{'lam<=':>8}   agrees with D3")
    all_ok = True
    for name, r_au, *pub in PUBLISHED:
        got = row(r_au)
        ok = all(abs(g - p) / p < tol for g, p in zip(got, pub))
        all_ok &= ok
        print(f"{name:<9}{got[0]:>11.3e}{got[1]:>12.3e}{got[2]:>12.3e}"
              f"{got[3]:>9.1f}{got[4]:>8.2f}   {'yes' if ok else 'NO'}")
    print()
    print(f"every published column reproduced within {tol:.0%}: {all_ok}")
    print()
    print("structure (the [D] content, independent of the empirical inputs):")
    a, b = row(1.0), row(2.0)
    print(f"  delta_g doubling r        x{b[1] / a[1]:.2f}   (r^2 -> 4.00)")
    print(f"  Q2 doubling r             x{b[2] / a[2]:.2f}   (r^1 -> 2.00)")
    print(f"  ceiling doubling r        x{b[4] / a[4]:.3f}  (tightens)")
    print("  => the outermost body with a datum binds; Mercury is the weakest test.")


if __name__ == "__main__":
    main()
