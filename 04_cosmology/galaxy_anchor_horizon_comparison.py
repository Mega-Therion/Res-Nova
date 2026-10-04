#!/usr/bin/env python3
"""Hold the galaxy scale fixed and compare the moving horizon scale to it.

The galaxy measurement is the anchor. c*H(z) is the scale that moves with
expansion. c*H(z)/(2*pi) is the same scale with the declared divisor, which
HorizonScale.lean does not derive.

Flat Lambda-CDM, Planck 2018: H0 = 67.36 km/s/Mpc, Omega_m = 0.3153.
The local galaxy anchor is SPARC T3 from A0_DISTANCE_CORRECTED_2026-09-16.json,
quoted in A0_HIGHZ_MEASUREMENT_2026-09-16.md: 1.16306e-10 m/s^2.
High-z galaxy anchors are that note's two-bin fDM ratios times T3.
"""

import json
import math

C = 299792458.0
MPC = 3.085677581e22
H0 = 67.36
OM = 0.3153
OL = 1.0 - OM
A0_GALAXY = 1.16306e-10

# (label, z, a0_galaxy / a0_T3) from the high-z audit. z=0 is the anchor itself.
BINS = (
    ("local SPARC T3", 0.0, 1.0),
    ("RC100 z<1.2", 0.867, 2.597),
    ("RC100 z>=1.2", 1.960, 2.286),
)


def h_over_h0(z):
    return math.sqrt(OM * (1.0 + z) ** 3 + OL)


def c_h(z):
    h_si = H0 * 1000.0 / MPC * h_over_h0(z)
    return C * h_si


rows = []
for label, z, ratio in BINS:
    galaxy = A0_GALAXY * ratio
    horizon = c_h(z)
    declared = horizon / (2.0 * math.pi)
    rows.append(
        {
            "label": label,
            "z": z,
            "a_galaxy_m_s2": galaxy,
            "cH_m_s2": horizon,
            "cH_over_2pi_m_s2": declared,
            "cH_over_galaxy": horizon / galaxy,
            "declared_over_galaxy": declared / galaxy,
            "fractional_gap_cH": (horizon - galaxy) / galaxy,
            "fractional_gap_declared": (declared - galaxy) / galaxy,
        }
    )

out = {
    "anchor": "galaxy measurement, SPARC T3 locally; high-z bins are the galaxies measured in that bin",
    "moving_scale": "c*H(z) in flat Planck 2018; the 2*pi form is reported beside it and is not derived",
    "H0_km_s_Mpc": H0,
    "Omega_m": OM,
    "a0_T3_m_s2": A0_GALAXY,
    "rows": rows,
}
json.dump(out, open("GALAXY_ANCHOR_HORIZON.json", "w"), indent=1)
for row in rows:
    print(
        f"{row['label']}: galaxy {row['a_galaxy_m_s2']:.4e}; "
        f"cH/galaxy {row['cH_over_galaxy']:.3f}; "
        f"(cH/2pi)/galaxy {row['declared_over_galaxy']:.3f}"
    )
