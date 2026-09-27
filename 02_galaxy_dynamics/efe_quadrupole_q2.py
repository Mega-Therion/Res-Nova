#!/usr/bin/env python3
"""Solar-system external-field-effect quadrupole Q2 (Cassini test) for candidate interpolating
functions, at the DERIVED a0 = cH0/2pi.

Exact QUMOND expression (Milgrom 2009, MNRAS 399, 474; as used by Hees et al. 2016, MNRAS 455, 449, eq. 12):
    q(eta) = 3/2 Int_0^inf dv Int_-1^1 dxi (nu - nu_e) [etaN (3 xi - 5 xi^3) + v^2 (1 - 3 xi^2)]
    nu = nu( sqrt(etaN^2 + v^4 + 2 etaN v^2 xi) ),  etaN nu(etaN) = eta = g_e/a0
(the -1 of nu-1 replaced by -nu_e, allowed because the xi-integrals of both brackets vanish;
 this removes the non-decaying far tail)
    Q2 = -3 q a0^(3/2) / (2 (GM_sun)^(1/2))          (Hees eq. 10)
Cassini: Q2 = (3 +/- 3) x 10^-27 s^-2 (Hees et al. 2014), i.e. 0..6e-27 at 1 sigma.

Validation target (Hees 2016 Table 2, g_e = 1.9e-10): nu_2 (= mu_std), a0 = 1.60e-10 -> -q = 0.10, Q2 = 26e-27;
nu-bar_0.5 (= McGaugh RAR), a0 = 1.48e-10 -> -q = 0.131, Q2 = 31e-27.
Also reports the monopole residual at Mercury (the test that killed mu_dual in TARGET_D7 section 4.3).
"""
import json
import numpy as np
from math import pi, sqrt
from scipy.optimize import brentq

GM = 1.32712e20
A0_DERIVED = 2.998e8 * (67.4e3 / 3.0857e22) / (2 * pi)
R_MERC = 5.7909e10

NU = {
    "mu_std (nu_2)":         lambda y: np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2))),
    "RAR (nu-bar_0.5)":      lambda y: 1 / (-np.expm1(-np.sqrt(y))),
    "mu_dual/simple (nu_1)": lambda y: 0.5 * (1 + np.sqrt(1 + 4 / y)),
}


def q_of_eta(nu, eta, nv=3000, nxi=400):
    etaN = brentq(lambda x: x * nu(x) - eta, 1e-8, eta)
    nue = nu(etaN)
    # v from 0 to large; use u = v^2 on a log grid plus the origin region
    v = np.concatenate([np.linspace(0, 1e-3, 50)[:-1], np.logspace(-3, 3, nv)])
    xi, w = np.polynomial.legendre.leggauss(nxi)
    V, XI = np.meshgrid(v, xi, indexing="ij")
    y = np.sqrt(np.maximum(etaN**2 + V**4 + 2 * etaN * V**2 * XI, 1e-300))
    f = (nu(y) - nue) * (etaN * (3 * XI - 5 * XI**3) + V**2 * (1 - 3 * XI**2))
    inner = f @ w
    return 1.5 * np.trapezoid(inner, v), etaN


def Q2(nu, a0, ge):
    q, _ = q_of_eta(nu, ge / a0)
    return -3 * q * a0**1.5 / (2 * sqrt(GM)), q


def mercury_residual(nu, a0):
    """Monopole anomalous acceleration at Mercury: g - gN = (nu(gN/a0) - 1) gN."""
    gN = GM / R_MERC**2
    return float((nu(np.array([gN / a0]))[0] - 1) * gN)


def main():
    out = {"validation": {}, "derived_a0": A0_DERIVED, "results": {}}
    print("VALIDATION vs Hees et al. 2016 Table 2 (g_e = 1.9e-10):")
    for name, a0, want_q, want_Q2 in (("mu_std (nu_2)", 1.60e-10, 0.10, 26e-27), ("RAR (nu-bar_0.5)", 1.48e-10, 0.131, 31e-27),
                                      ("mu_std (nu_2)", 1.60e-10 * 1.9 / 1.9, 0.10, 26e-27)):
        Q, q = Q2(NU[name], a0, 1.9e-10)
        out["validation"][name] = {"a0": a0, "minus_q": -q, "Q2": Q, "hees_minus_q": want_q, "hees_Q2": want_Q2}
        print(f"  {name:22s} a0={a0:.2e}  -q={-q:.4f} (Hees {want_q})  Q2={Q:.2e} (Hees {want_Q2:.0e})")

    print(f"\nDERIVED a0 = {A0_DERIVED:.4e} m/s^2;  Cassini: Q2 = (3 +/- 3)e-27 s^-2")
    for name, nu in NU.items():
        row = {"mercury_monopole_residual": mercury_residual(nu, A0_DERIVED)}
        for ge in (1.9e-10, 2.4e-10):
            Q, q = Q2(nu, A0_DERIVED, ge)
            row[f"ge={ge:.1e}"] = {"eta": ge / A0_DERIVED, "minus_q": -q, "Q2": Q, "sigma_from_cassini": (Q - 3e-27) / 3e-27}
        out["results"][name] = row
        print(f"  {name:22s} Mercury monopole residual {row['mercury_monopole_residual']:.2e} m/s^2 (bound ~2e-16)")
        for ge in (1.9e-10, 2.4e-10):
            r = row[f"ge={ge:.1e}"]
            print(f"      g_e={ge:.1e}: eta={r['eta']:.2f}  -q={r['minus_q']:.4f}  Q2={r['Q2']:.2e}  -> {r['sigma_from_cassini']:+.1f} sigma")
    print("\nQ2 vs a0 (g_e = 1.9e-10), to see where each function would pass:")
    for name, nu in NU.items():
        s = []
        for a0 in (0.6e-10, 0.8e-10, 1.0e-10, A0_DERIVED, 1.2e-10, 1.6e-10):
            s.append(f"{a0*1e10:.2f}:{Q2(nu, a0, 1.9e-10)[0]*1e27:.1f}")
        print(f"  {name:22s} " + "  ".join(s) + "   (a0 in 1e-10 : Q2 in 1e-27)")
    json.dump(out, open("EFE_QUADRUPOLE_Q2.json", "w"), indent=1)


if __name__ == "__main__":
    main()
