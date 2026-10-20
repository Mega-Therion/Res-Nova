#!/usr/bin/env python3
"""One-scale rule connecting the plate pressure to a0. [O] identification, [D] arithmetic.

Rule: the acceleration imparted to a surface density Sigma by the Casimir
pressure of a cavity of size L is

    a(L) = pi**2 * hbar * c / (240 * L**4 * Sigma).

The ladder would require a(L_galaxy) = a0. This script prints that length
and the acceleration at galaxy sizes. It does not vary an action.
"""

from __future__ import annotations

import math

HBAR = 1.054571817e-34
C = 2.99792458e8
A0 = 1.1160351336495208e-10
MSUN = 1.98847e30
PC = 3.085677581e16
KPC = 1e3 * PC
PREF = math.pi**2 * HBAR * C / 240.0


def sigma_from_msun_per_pc2(surface: float) -> float:
    return surface * MSUN / PC**2


def a_of(length_m: float, sigma: float) -> float:
    return PREF / (length_m**4 * sigma)


def main() -> None:
    sigma = sigma_from_msun_per_pc2(100.0)
    length = (PREF / (A0 * sigma)) ** 0.25
    print(f"Sigma = {sigma:.6e} kg/m^2 for 100 Msun/pc^2")
    print(f"L where a(L) = a0: {length:.6e} m")
    for name, length_m in (("1 kpc", KPC), ("4.3 kpc", 4.3 * KPC)):
        acc = a_of(length_m, sigma)
        print(f"{name}: a = {acc:.3e} m/s^2   a/a0 = {acc / A0:.3e}")
    print("RESULT casimir_disk_ladder_fails")


if __name__ == "__main__":
    main()
