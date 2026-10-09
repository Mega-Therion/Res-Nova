#!/usr/bin/env python3
"""Strong-coupling scale against the published inverse-square window.

This script does not use D7, screening, or a branch choice. It computes
Lambda_SC from a0, G, hbar, and c, and compares the range to the Eot-Wash
window quoted in TARGET_D6_SUPPLEMENT_LSC_EXPERIMENTAL_CHECK.md section 2:
gravitational-strength Yukawa violations are excluded for lambda >= 39 um
(arXiv:2406.13020, as cited there).

An unscreened coupling of gravitational strength at this range sits inside
that window. Whether screening removes it is a separate question and is not
answered here.
"""

import json

HBAR = 1.054571817e-34
C = 2.99792458e8
G = 6.67430e-11
J2EV = 1.602176634e-19
HBAR_C = HBAR * C
EOT_WASH_UM = 39.0

rows = []
for name, a0 in (
    ("literature", 1.2e-10),
    ("sparc_fit_mu_std", 1.1607e-10),           # live mu_std fit (A0_DISTANCE_CORRECTED_2026-09-16.json)
    # 5.461e-11 * sqrt(5): the "canonical constants block" value. Labelled "horizon_anchor" until 2026-10-09,
    # which it is not; the horizon anchor is cH0/2pi, added below.
    ("canonical_5.461e-11_sqrt5", 1.2211e-10),
    ("horizon_anchor_cH0_2pi", 1.0421152108506952e-10),
):
    lam = ((a0**2 / G) * HBAR_C**3) ** 0.25
    rang_um = HBAR_C / lam * 1e6
    rows.append(
        {
            "a0_m_s2": a0,
            "label": name,
            "lambda_sc_meV": lam / J2EV * 1000,
            "range_um": rang_um,
            "inside_eot_wash_window": rang_um >= EOT_WASH_UM,
        }
    )
out = {
    "eot_wash_excluded_um": EOT_WASH_UM,
    "citation": "arXiv:2406.13020 as quoted in TARGET_D6_SUPPLEMENT_LSC_EXPERIMENTAL_CHECK.md",
    "screening_used": False,
    "rows": rows,
}
json.dump(out, open("LAMBDA_SC_UNSCREENED.json", "w"), indent=1)
for row in rows:
    print(
        f"{row['label']}: {row['lambda_sc_meV']:.4f} meV, {row['range_um']:.1f} um, inside window {row['inside_unscreened_window'] if False else row['inside_eot_wash_window']}"
    )
