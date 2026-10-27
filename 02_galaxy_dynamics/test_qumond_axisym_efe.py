#!/usr/bin/env python3
"""Fast checks for qumond_axisym_efe.py (a few seconds). Exit 0 on success.

1. nu_6 is the exact inverse of mu_6 = x/(1+x^6)^(1/6); nu_2 of mu_std.
2. nu.minus_1 agrees with nu - 1 where both are accurate.
3. Mode solver on a manufactured problem with a known answer: V = grad psi,
   psi = r^2 P2(cos th) exp(-r^2) gives lap Phi = -lap psi, so Phi = -psi + 0 and
   u_2(r)/r^2 -> -1 at small r.
4. Coarse reproduction of the pinned nu_std Q2 = 1.9017920213e-26 to 1e-3.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qumond_axisym_efe as S  # noqa: E402


def check_inverse():
    x = np.logspace(-4, 4, 200)
    for n in (2, 6):
        mu = x / (1 + x**n) ** (1 / n)
        err = np.max(np.abs(S.nu_n(n)(x * mu) * mu - 1))
        assert err < 1e-12, (n, err)
        y = np.array([1e-3, 0.3, 1.0, 5.0, 50.0])
        nu = S.nu_n(n)
        assert np.max(np.abs(nu.minus_1(y) - (nu(y) - 1))) < 1e-13


def check_manufactured():
    # Replace the physical flux with grad psi and reuse the same BVP code path.
    def fake_AB(nu, nue, ye, r, th, w, l):
        st, ct = np.sin(th), np.cos(th)
        R = r[:, None]
        P2 = 0.5 * (3 * ct**2 - 1)
        dpsi_dr = (2 * R - 2 * R**3) * np.exp(-R**2) * P2
        dpsi_dth_over_r = R * np.exp(-R**2) * (-3 * ct * st)
        Vr, Vt = dpsi_dr * np.ones_like(st), dpsi_dth_over_r
        Pl = S.eval_legendre(l, ct)
        dPl = S._legendre_deriv(l, ct)
        wt = w * st
        return (2 * l + 1) / 2 * (Vr * Pl) @ wt, (2 * l + 1) / 2 * (Vt * st * dPl) @ wt

    real = S._AB
    S._AB = fake_AB
    try:
        c2, _ = S.c2_of(S.nu_n(2), 1.0, n_r=3000, n_th=64, r_min=1e-3, r_max=30.0)
    finally:
        S._AB = real
    assert abs(c2 + 1.0) < 1e-4, c2


def check_pinned():
    q2, q, ye = S.Q2(S.nu_n(2), S.A0_FIT, 1.9e-10, n_r=1500, n_th=64)
    rel = abs(q2 - 1.9017920212899443e-26) / 1.9017920212899443e-26
    assert rel < 1e-3, (q2, rel)
    assert q < 0 and q2 > 0


if __name__ == "__main__":
    check_inverse()
    check_manufactured()
    check_pinned()
    print("test_qumond_axisym_efe: 3 groups OK")
