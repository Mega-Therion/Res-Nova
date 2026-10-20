#!/usr/bin/env python3
"""Where does the baryon-only potential peak in a Bullet-like pair?

Gas sits at x=0. A lighter galaxy blob sits at x=d. The source is baryonic
rest mass only. Newtonian g_N and the algebraic boost nu(g_N)*g_N are both
local functions of that mass. The script reports which blob the acceleration
peak follows. It does not ray-trace 1E 0657.
"""

from __future__ import annotations

import numpy as np

import disk_qumond_split as q

# Mass ratio: hot gas dominates the baryons. Galaxies are the offset clump.
M_GAS = 9.0
M_GAL = 1.0
SIGMA = 1.0
D = 4.0
A0 = 1.0


def mass_profile(x: np.ndarray) -> np.ndarray:
    gas = M_GAS * np.exp(-0.5 * (x / SIGMA) ** 2) / (SIGMA * np.sqrt(2 * np.pi))
    gal = M_GAL * np.exp(-0.5 * ((x - D) / SIGMA) ** 2) / (SIGMA * np.sqrt(2 * np.pi))
    return gas, gal


def g_newton(x: np.ndarray, rho: np.ndarray) -> np.ndarray:
    """1D slab: d g / dx = 4 pi G rho, G=1, g(0 boundary) fixed by total mass."""
    dx = float(x[1] - x[0])
    # cumulative mass from the left, minus half the total so g is odd for one blob
    m = np.cumsum(rho) * dx
    return 2.0 * np.pi * (2.0 * m - m[-1])


def peak_of(g: np.ndarray, x: np.ndarray) -> float:
    # acceleration toward the pair: the lensing convergence in this slab tracks rho_eff.
    return float(x[int(np.argmax(np.abs(np.gradient(g, x))))])


def main() -> None:
    x = np.linspace(-8.0, 12.0, 4001)
    gas, gal = mass_profile(x)
    rho = gas + gal
    g_n = g_newton(x, rho)
    g_alg = q.nu_simple(np.abs(g_n) / A0) * g_n
    x_gas = float(x[int(np.argmax(gas))])
    x_gal = float(x[int(np.argmax(gal))])
    x_n = peak_of(g_n, x)
    x_a = peak_of(g_alg, x)
    # mass-weighted baryon centroid
    dx = float(x[1] - x[0])
    centroid = float(np.sum(rho * x) * dx / np.sum(rho * dx))
    print(f"gas peak at {x_gas:.3f}")
    print(f"galaxy peak at {x_gal:.3f}")
    print(f"baryon centroid at {centroid:.3f}")
    print(f"Newtonian convergence peak at {x_n:.3f}")
    print(f"algebraic convergence peak at {x_a:.3f}")
    if abs(x_a - x_gas) < abs(x_a - x_gal):
        print("RESULT lensing_peak_follows_gas")
    else:
        print("RESULT lensing_peak_follows_galaxies")


if __name__ == "__main__":
    main()
