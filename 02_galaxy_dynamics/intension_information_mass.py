#!/usr/bin/env python3
"""Does the quantum information in the collisionless component outweigh the gas?

Information bound to a body travels with that body. Galaxy stars pass
through the collision. Gas is stopped. That is the transport half.

The weight half: each bit, held at a temperature T, carries an energy
k T ln 2. Compared with a proton rest energy that is a small mass.
Cluster gas is hotter than the stars, so a bit in the gas weighs more,
not less. The script uses the bullet-cluster regime T ~ 10 keV and
one bit per baryon. It does not vary an action.
"""

from __future__ import annotations

import math

K_B = 1.380649e-23
EV = 1.602176634e-19
M_P_C2_EV = 938.272e6
# 10 keV is the order of the bullet shock temperature.
T = (10e3 * EV) / K_B
BITS_PER_BARYON = 1.0
# Gas is the heavier baryon component. Galaxies are the smaller share.
GAS_FRACTION = 0.9


def main() -> None:
    e_bit = K_B * T * math.log(2.0)
    ratio = (BITS_PER_BARYON * e_bit / EV) / M_P_C2_EV
    # information mass on the galaxies over gas rest mass
    galaxy_share = 1.0 - GAS_FRACTION
    info_over_gas = galaxy_share * ratio / GAS_FRACTION
    print(f"T = {T:.3e} K")
    print(f"bit mass / proton mass = {ratio:.3e}")
    print(f"galaxy-information mass / gas rest mass = {info_over_gas:.3e}")
    if info_over_gas < 1.0:
        print("RESULT information_mass_does_not_outweigh_gas")
    else:
        print("RESULT information_mass_outweighs_gas")
    print("RESULT information_travels_with_its_body")


if __name__ == "__main__":
    main()
