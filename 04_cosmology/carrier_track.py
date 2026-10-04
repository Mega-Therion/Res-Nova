#!/usr/bin/env python3
"""Track the moving frame. See which relationship stands still.

Bob McGwier, Danny Jones interview, 22 May 2026, on the Vega balloon
signal: the gondola was a pendulum, the oscillator was hot and jittery,
and a linear receiver could not follow it. His nonlinear filter estimated
the state. After the carrier was tracked, the modulation stood still
because it had a fixed relationship to that carrier.

Here the candidate carriers are the expansion, H(z), and the galaxy scale.
The observations are the measured galaxy ratios in A0_HIGHZ_MEASUREMENT_2026-09-16.md.
No Cassini term enters.
"""

import json
import math

H0 = 67.36
OM = 0.3153
OL = 1.0 - OM
# label, z, measured a / local SPARC T3
OBS = (
    ("local", 0.0, 1.0),
    ("z<1.2", 0.867, 2.597),
    ("z>=1.2", 1.960, 2.286),
)


def h_ratio(z):
    return math.sqrt(OM * (1.0 + z) ** 3 + OL)


rows = []
for label, z, measured in OBS:
    hz = h_ratio(z)
    # Message if H is the carrier: measured scale divided by the expansion.
    sideband = measured / hz
    rows.append(
        {
            "label": label,
            "z": z,
            "measured_over_local": measured,
            "H_over_H0": hz,
            "sideband_if_H_is_carrier": sideband,
        }
    )

high = [r["measured_over_local"] for r in rows if r["z"] > 0]
high_h = [r["sideband_if_H_is_carrier"] for r in rows if r["z"] > 0]
mean_gal = sum(high) / len(high)
mean_h = sum(high_h) / len(high_h)
spread_gal = max(high) - min(high)
spread_h = max(high_h) - min(high_h)

out = {
    "quote": "the modulation stood still because it had a fixed relationship to the tracked carrier",
    "rows": rows,
    "high_z_galaxy_ratios": high,
    "high_z_spread_if_galaxy_is_carrier": spread_gal,
    "high_z_spread_if_H_is_carrier": spread_h,
    "which_stands": "galaxy" if spread_gal < spread_h else "expansion",
}
json.dump(out, open("CARRIER_TRACK.json", "w"), indent=1)
for r in rows:
    print(
        f"{r['label']}: measured {r['measured_over_local']:.3f}  "
        f"H/H0 {r['H_over_H0']:.3f}  "
        f"sideband {r['sideband_if_H_is_carrier']:.3f}"
    )
print(f"spread if galaxy is the carrier: {spread_gal:.3f}")
print(f"spread if expansion is the carrier: {spread_h:.3f}")
print("stands:", out["which_stands"])
