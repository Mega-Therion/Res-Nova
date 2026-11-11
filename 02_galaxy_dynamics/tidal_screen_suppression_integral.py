#!/usr/bin/env python3
"""Named hypothesis: tidal-screen factor S_p(T0) for the Cassini Q2.

This is the integral written in the 2026-11-06 screening note, not a fit.
T0 is not adjusted. The file does not import SPARC and does not change
screen_mass_cassini.py. lambda and M there stay unfixed.

    K_0(u) = (5/u_e) (u/u_e)^4 / [1 + (u/u_e)^2]^(7/2),    ∫_0^∞ K_0 = 1

    W_p(u; T0) = u^(3p) / (u^(3p) + u_T^(3p)),
    u_T = (T_M / T0)^(1/3),    T(u) = T_M u^(-3)

    S_p(T0) = 5 ∫_0^∞ v^4 / (1+v^2)^(7/2) * v^(3p) / (v^(3p) + v_T^(3p)) dv
    v_T = η^(1/2) (T_M / T0)^(1/3)

Asymptotic, only for T0 ≪ T_M:

    S_p ≈ (C_p / η) (T0 / T_M)^(2/3),
    C_p = 5π / (3 p sin(2π / (3p)))

The note's printed table used that asymptotic with a rounded residual
9.68 * S_2. screen_mass_cassini.py records the unscreened residuals as
+9.72σ and +10.28σ on the 2026 window (1.6 ± 1.8)e-27 s^-2. This script
multiplies those two stored Q2 values by the full integral.
"""

import math
import numpy as np
from scipy.integrate import quad

# Reproduction block: the note's own constants (SPARC headline a0, its GM).
A0_NOTE = 1.1607e-10
GM_NOTE = 1.3271244e20
ETA_NOTE = 1.60

# Stored Cassini inputs. screen_mass_cassini.py lines 28-48.
A0_ANCHOR = 1.163e-10
GM_SUN = 1.32712e20
Q2_ROWS = (
    {"g_e": 1.9e-10, "Q2": 1.91e-26},
    {"g_e": 2.4e-10, "Q2": 2.01e-26},
)
Q2_2014 = (3.0e-27, 3.0e-27)  # center, sigma
Q2_2026 = (1.6e-27, 1.8e-27)
AU = 1.495978707e11
KPC = 3.0856775814913673e19
T0_GRID = (1e-25, 1e-26, 1e-27, 1e-28, 1e-29, 1e-30)


def r_M(a0, GM):
    return math.sqrt(GM / a0)


def T_M(a0, GM):
    return a0 / r_M(a0, GM)


def C_p(p):
    return 5.0 * math.pi / (3.0 * p * math.sin(2.0 * math.pi / (3.0 * p)))


def K0(u, u_e):
    x = u / u_e
    return (5.0 / u_e) * (x**4) / (1.0 + x * x) ** 3.5


def S_full(T0, p, TM, eta):
    """Full suppression integral. Returns (value, quad absolute error)."""
    vT = math.sqrt(eta) * (TM / T0) ** (1.0 / 3.0)

    def f(v):
        vp = v ** (3.0 * p)
        return 5.0 * (v**4) / (1.0 + v * v) ** 3.5 * vp / (vp + vT ** (3.0 * p))

    # The mass sits near v ~ 1 and near v ~ vT. Split so quad sees both.
    I1, e1 = quad(f, 0.0, 1.0, limit=400, epsabs=1e-12)
    I2, e2 = quad(f, 1.0, max(vT * 4.0, 8.0), limit=800, epsabs=1e-12)
    I3, e3 = quad(f, max(vT * 4.0, 8.0), np.inf, limit=400, epsabs=1e-14)
    return I1 + I2 + I3, e1 + e2 + e3


def S_asym(T0, p, TM, eta):
    vT = math.sqrt(eta) * (TM / T0) ** (1.0 / 3.0)
    return C_p(p) / (vT**2)


def sigma_of(q2, center, sigma):
    return (q2 - center) / sigma


def reproduce_note():
    TM = T_M(A0_NOTE, GM_NOTE)
    rM = r_M(A0_NOTE, GM_NOTE)
    u_e = ETA_NOTE ** (-0.5)
    K, eK = quad(lambda u: K0(u, u_e), 0.0, np.inf, limit=500)
    print("hypothesis check against the note's own constants")
    print(f"  a0 = {A0_NOTE:.4e}   GM = {GM_NOTE:.7e}")
    print(f"  r_M = {rM:.6e} m = {rM / AU:.1f} AU")
    print(f"  T_M = {TM:.6e} s^-2    T_M*sqrt(6) = {TM * math.sqrt(6):.6e}")
    print(f"  eta = {ETA_NOTE}   u_e = {u_e:.4f}   r_e = {u_e * rM / AU:.1f} AU")
    print(f"  ∫ K_0 du = {K:.12f}   quad err {eK:.2e}")
    if abs(K - 1.0) > 1e-9:
        raise SystemExit("K_0 integral drifted")
    for p in (1, 2):
        num, err = quad(
            lambda s, p=p: s ** (3 * p - 3) / (1.0 + s ** (3 * p)),
            0.0,
            np.inf,
            limit=500,
        )
        analytic = C_p(p)
        print(f"  C_{p} analytic {analytic:.6f}   5*∫ {5 * num:.6f}   err {err:.2e}")
        if abs(5 * num - analytic) > 1e-8:
            raise SystemExit("C_p drifted")
    print(
        f"\n  {'T0':>8} {'r_T AU':>10} {'S1 asym':>9} {'S1 full':>9} "
        f"{'S2 asym':>9} {'S2 full':>9} {'9.68*S2':>8}"
    )
    for T0 in T0_GRID:
        rT = (TM / T0) ** (1.0 / 3.0) * rM / AU
        s1a = S_asym(T0, 1, TM, ETA_NOTE)
        s2a = S_asym(T0, 2, TM, ETA_NOTE)
        s1, _ = S_full(T0, 1, TM, ETA_NOTE)
        s2, _ = S_full(T0, 2, TM, ETA_NOTE)
        print(
            f"  {T0:.0e} {rT:10.1f} {s1a:9.4f} {s1:9.4f} {s2a:9.4f} "
            f"{s2:9.4f} {9.68 * s2:8.3f}"
        )
    print(
        "  9.68*S2 is the note's residual column. It is not a line in "
        "screen_mass_cassini.py."
    )
    return TM


def apply_to_stored_q2():
    TM = T_M(A0_ANCHOR, GM_SUN)
    rM = r_M(A0_ANCHOR, GM_SUN)
    print("\nstored Q2 from screen_mass_cassini.py, times the full integral")
    print(f"  a0 anchor = {A0_ANCHOR:.4e}   GM = {GM_SUN:.5e}")
    print(f"  r_M = {rM / AU:.1f} AU    T_M = {TM:.6e} s^-2")
    print(f"  2014 window (3.0 ± 3.0)e-27    2026 window (1.6 ± 1.8)e-27")
    print(f"  S = 1 is the unscreened case already in that file.")
    for row in Q2_ROWS:
        eta = row["g_e"] / A0_ANCHOR
        s2014 = sigma_of(row["Q2"], *Q2_2014)
        s2026 = sigma_of(row["Q2"], *Q2_2026)
        print(
            f"\n  g_e = {row['g_e']:.1e}   eta = g_e/a0 = {eta:.4f}   "
            f"Q2 = {row['Q2']:.2e}"
        )
        print(f"  unscreened: 2014 {s2014:+.2f}σ    2026 {s2026:+.2f}σ")
        print(f"  {'T0':>8} {'S2 full':>9} {'Q2*S2':>10} " f"{'2014σ':>8} {'2026σ':>8}")
        for T0 in T0_GRID:
            s2, err = S_full(T0, 2, TM, eta)
            q = row["Q2"] * s2
            print(
                f"  {T0:.0e} {s2:9.4f} {q:10.3e} "
                f"{sigma_of(q, *Q2_2014):+8.2f} {sigma_of(q, *Q2_2026):+8.2f}"
                f"    quad {err:.1e}"
            )


# Radii named by manuscripts/2026-10-16-oort-c0/oort_kills_c0.tex:
# the C=0 push sits near 9 to 12 thousand AU; the observed peak of new
# comets is quoted as 10^4 to 10^5 AU. 3e4 AU is not one of those quotes.
OORT_RADII_AU = (
    ("C=0 shell, 9e3 AU", 9000.0),
    ("C=0 shell, 1.2e4 AU", 12000.0),
    ("quoted peak edge, 1e4 AU", 1.0e4),
    ("quoted peak edge, 1e5 AU", 1.0e5),
)


def oort_radii():
    """T0 = GM/r^3 at radii already written down. Not a fit to Q2."""
    TM = T_M(A0_ANCHOR, GM_SUN)
    print("\nT0 = GM_sun/r^3 at the Oort radii already in oort_kills_c0.tex")
    print(f"  {'radius':<28} {'T0':>10} {'g_e':>8} {'S2':>8} {'2026σ':>8}")
    for name, au in OORT_RADII_AU:
        T0 = GM_SUN / (au * AU) ** 3
        for row in Q2_ROWS:
            eta = row["g_e"] / A0_ANCHOR
            s2, err = S_full(T0, 2, TM, eta)
            q = row["Q2"] * s2
            print(
                f"  {name:<28} {T0:.3e} {row['g_e']:.1e} {s2:8.4f} "
                f"{sigma_of(q, *Q2_2026):+8.2f}    quad {err:.1e}"
            )


def galactic_floor(a0):
    print("\ngalactic tide a0/R at this same a0, for the lower edge of the window")
    for kpc in (2.0, 10.0):
        T = a0 / (kpc * KPC)
        print(f"  R = {kpc:.0f} kpc    a0/R = {T:.3e} s^-2")


def main():
    reproduce_note()
    apply_to_stored_q2()
    oort_radii()
    galactic_floor(A0_ANCHOR)
    print(
        "\nStatus: hypothesis. T0 is not a fitted parameter. "
        "The integral is not in the SPARC pipeline."
    )


if __name__ == "__main__":
    main()
