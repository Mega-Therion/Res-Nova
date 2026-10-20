#!/usr/bin/env python3
"""Galaxy-gas lag from a speed and a time, compared with the lensing lags.

The independent test needs both inputs free of the lensing map.
Markevitch / Clowe shock speed ~4700 km/s is an X-ray jump. It is not the
speed of the gas bullet relative to the galaxies.
Lage & Farrar 2014 (arXiv:1312.0959): closest approach of the mass centroids
at 0.73 Gyr, best description of the data at 0.85 Gyr, so 120 Myr later.
That clock was fit with the lensing map in the chi-squared. It is not
an independent time.
Springel & Farrar 2007: shock ~4500 km/s, mass centroid ~2600 km/s in the
parent frame. Their difference is not a measured galaxy-gas speed.

1 km/s * 1 Gyr = 1.0227 kpc.
"""

from __future__ import annotations

KPC_PER_KMS_GYR = 1.0227
T_LAGE_GYR = 0.12
DV_SHOCK_MINUS_HALO = 4500.0 - 2600.0
LENSING_LAGS = (("bullet", 270.0), ("main", 110.0))


def main() -> None:
    product = DV_SHOCK_MINUS_HALO * T_LAGE_GYR * KPC_PER_KMS_GYR
    print(
        f"shock minus halo speed {DV_SHOCK_MINUS_HALO:.0f} km/s"
        f" times {T_LAGE_GYR:.2f} Gyr = {product:.1f} kpc"
    )
    for name, lag in LENSING_LAGS:
        print(f"{name} lensing-gas lag {lag:.0f} kpc | product/lag {product / lag:.2f}")
    print("RESULT clock_uses_lensing_map")
    print("RESULT speed_difference_is_not_galaxy_minus_gas")


if __name__ == "__main__":
    main()
