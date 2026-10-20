#!/usr/bin/env python3
"""Bullet offset under the two mechanisms still on the table.

Cited lags, Clowe et al. 2006 as quoted by Mastropietro & Burkert 2008,
MNRAS 389, 967: lensing-gas offset about 270 kpc (bullet) and 110 kpc (main).
Lensing there sits near the galaxies.

Algebraic law: the two-blob run moved the convergence peak 0.135 toward a
galaxy blob 4.0 away, with gas nine times heavier. Fraction 0.135/4.

Holonomy rule [O]: the connection is carried by the collisionless galaxies,
so the lensing peak stays on the galaxies and the offset equals the
galaxy-gas lag. This script does not ray-trace 1E 0657.
"""

from __future__ import annotations

ALG_SHIFT = 0.135
ALG_SEP = 4.0
FRACTION = ALG_SHIFT / ALG_SEP
LAGS_KPC = (("bullet", 270.0), ("main", 110.0))


def main() -> None:
    print(f"algebraic peak shift / separation = {FRACTION:.4f}")
    for name, lag in LAGS_KPC:
        alg = FRACTION * lag
        print(
            f"{name}: galaxy-gas lag {lag:.0f} kpc | "
            f"holonomy offset {lag:.0f} kpc | "
            f"algebraic offset {alg:.1f} kpc"
        )
    print("RESULT holonomy_offset_equals_galaxy_lag")
    print("RESULT algebraic_offset_is_a_few_percent")


if __name__ == "__main__":
    main()
