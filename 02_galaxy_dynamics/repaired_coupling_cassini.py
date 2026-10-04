#!/usr/bin/env python3
"""Index-repaired disformal coupling, then Cassini at the galaxy anchor.

The printed information-tension equation added a scalar to a tensor. The repair
is the standard disformal form, g_mu_nu + B * d_mu chi * d_nu chi. This script
checks that the added term is a tensor, then asks whether that repair screens
the solar system. It does not insert a free screen, and it does not use cH/2pi.

At the Sun, the Milky Way field is about 1.6 to 2.1 times the galaxy scale, so
mu_std is not in its high-acceleration limit. The Cassini quadrupole is then
the ordinary mu_std external-field effect.
"""

import json
import numpy as np
from efe_quadrupole_q2 import Q2, NU

# Index repair: a rank-2 term needs two free indices. A fully contracted
# product is a scalar and cannot be added to g_mu_nu.
gradient = np.array([0.2, 0.0, 0.0, 0.3])
tensor = np.outer(gradient, gradient)
scalar = float(gradient @ gradient)
assert tensor.shape == (4, 4)
assert abs(np.trace(tensor) - scalar) < 1e-12

A0 = 1.16306e-10
nu = NU["mu_std (nu_2)"]
rows = []
for ge in (1.9e-10, 2.4e-10):
    q2, _ = Q2(nu, A0, ge)
    eta = ge / A0
    rows.append(
        {
            "g_e": ge,
            "eta": eta,
            "Q2": q2,
            "sigma_2014": (q2 - 3e-27) / 3e-27,
            "sigma_2026": (q2 - 1.6e-27) / 1.8e-27,
            "high_g_fraction": 0.5 / eta**2,
            "passes_2014_1sigma": bool(q2 <= 6e-27),
            "passes_2026_2sigma": bool(q2 <= 5.2e-27),
        }
    )
out = {"a0_galaxy": A0, "coupling": "g_mu_nu + B d_mu chi d_nu chi", "rows": rows}
json.dump(out, open("REPAIRED_COUPLING_CASSINI.json", "w"), indent=1)
for row in rows:
    print(
        f"eta={row['eta']:.3f} Q2={row['Q2']:.3e} "
        f"2014 {row['sigma_2014']:+.2f}σ 2026 {row['sigma_2026']:+.2f}σ "
        f"pass2014={row['passes_2014_1sigma']} pass2026={row['passes_2026_2sigma']}"
    )
