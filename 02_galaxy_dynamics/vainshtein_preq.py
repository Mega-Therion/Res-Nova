#!/usr/bin/env python3
"""Recompute the Vainshtein exponent the solar system actually requires.

TARGET_D7 §11.3 left p_req = 2.34 flagged: that figure divided by the
retracted 5.7e5 quadrupole-scale ratio. This module uses the Mercury
precession factor and the live QUMOND Q2 instead.

The Q2 line is a scaling estimate, (r_MOND / r_V)^p times the unscreened
quadrupole. It is not a nested solution of the field equation, and a
value under the Cassini window is not a pass.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

A0 = 1.1607e-10
G = 6.67430e-11
MSUN = 1.98847e30
GM = 1.32712e20
R_MERC = 5.7909e10
PC = 3.085677581e16
AU = 1.495978707e11
P_MERC_YR = 0.240846
BOUND_ARCSEC_CY = 0.0016  # 1.6 mas/cy, the 2σ figure quoted in TARGET_D7 §4.3
P_CUBIC = 1.5


def requirements(
    q2_bare: float, q2_center: float = 1.6e-27, q2_sigma: float = 1.8e-27
) -> dict:
    d_rad = 2.0 * math.pi * A0 * R_MERC**2 / GM
    orbits_per_cy = 100.0 / P_MERC_YR
    arcsec = d_rad * orbits_per_cy * (180.0 / math.pi) * 3600.0
    factor = arcsec / BOUND_ARCSEC_CY
    g_n = GM / R_MERC**2
    m_gal = 1e11 * MSUN
    r_mond_gal = math.sqrt(G * m_gal / A0)
    r_v_sun = r_mond_gal * (MSUN / m_gal) ** (1.0 / 3.0)
    r_mond_sun = math.sqrt(GM / A0)
    # Constant-tail force must fall from g_N-scaled Vainshtein to a0/factor.
    ab = A0 / factor
    p_prec = math.log(ab / g_n) / math.log(R_MERC / r_v_sun)
    cubic_at_merc = (R_MERC / r_v_sun) ** P_CUBIC
    q2_ceiling = q2_center + q2_sigma
    need = q2_ceiling / q2_bare
    p_q2 = math.log(need) / math.log(r_mond_sun / r_v_sun)
    q2_scaled = q2_bare * (r_mond_sun / r_v_sun) ** P_CUBIC
    return {
        "a0": A0,
        "precession_arcsec_per_cy": arcsec,
        "precession_factor": factor,
        "g_N_mercury": g_n,
        "r_V_sun_pc": r_v_sun / PC,
        "r_MOND_sun_AU": r_mond_sun / AU,
        "p_req_precession": p_prec,
        "p_cubic": P_CUBIC,
        "cubic_ratio_at_mercury": cubic_at_merc,
        "precession_ratio_required": ab / g_n,
        "cubic_clears_precession": cubic_at_merc <= ab / g_n,
        "Q2_bare": q2_bare,
        "Q2_ceiling_2026": q2_ceiling,
        "p_req_Q2_scaling": p_q2,
        "Q2_scaled_cubic": q2_scaled,
        "scaling_under_ceiling": q2_scaled <= q2_ceiling,
        "scaling_is_not_a_cassini_pass": True,
    }


def main() -> None:
    gate = json.loads(Path(__file__).with_name("SECOND_FIELD_GATES.json").read_text())
    q2 = float(gate["ge"]["1.9e-10"]["Q2"])
    out = requirements(q2)
    dest = Path(__file__).with_name("VAINSHTEIN_PREQ.json")
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(
        json.dumps(
            {
                k: out[k]
                for k in (
                    "precession_factor",
                    "p_req_precession",
                    "cubic_clears_precession",
                    "p_req_Q2_scaling",
                    "Q2_scaled_cubic",
                    "scaling_under_ceiling",
                )
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
