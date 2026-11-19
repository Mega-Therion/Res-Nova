#!/usr/bin/env python3
"""Can x* and C be derived from the theory's own constants? (2026-11-19) [D] dimensional analysis + numbers.

The available constants are G, c, a0, H0 (and Lambda = 3 Om_L H0^2). A tidal field has units s^-2, and x = c^2 T/a0^2.
Without a mass scale, the only tidal scales are combinations of a0/c and H0. With G and no mass, none can be formed
(G alone has no s^-2 combination with a0, c, H0 that lacks a mass). So every derivable x is a pure number times
products of the dimensionless ratio cH0/a0 (= 2 pi in the horizon picture). Those are listed and compared with the
data window x* in [1.7e10, 7.04e11]."""
import json, math
c = 2.99792458e8; a0 = 1.1607e-10; Mpc = 3.0857e22; H0 = 67.4e3 / Mpc; OL = 0.685
r = c * H0 / a0                                # ~ 2 pi
cands = {"(a0/c)^2": 1.0, "a0 H0/c": r, "H0^2": r**2, "Lambda c^2/3 /c^2 -> OL H0^2": OL * r**2}
for n in range(1, 31):
    cands[f"(cH0/a0)^{n}"] = r**n
window = (1.7e10, 7.04e11)
hits = {k: v for k, v in cands.items() if window[0] <= v <= window[1]}
# the pure power that lands in the window, and whether it is natural
need_n = (math.log(window[0]) / math.log(r), math.log(window[1]) / math.log(r))
# the Sun-specific identity: Cassini's x* equals placing the screen onset near the Sun's MOND radius
GM = 1.32712e20; rM = math.sqrt(GM / a0)
x_at_rM = c**2 * math.sqrt(6) * GM / rM**3 / a0**2
out = {"cH0_over_a0": r, "dimensionless_candidates_in_window": hits, "power_needed_range": need_n,
       "sun_identity": {"r_M_sun_AU": rM / 1.495978707e11, "x_at_sun_MOND_radius": x_at_rM,
                        "x_star_over_x_at_rM": 7.04e11 / x_at_rM},
       "C": ("C is a constant zero of the screening Lagrangian. Within the action it is an integration-type constant "
             "with no fixed point: no symmetry selects a nonzero value, and C = 0 is [X] (Oort). It cannot be derived "
             "from the action; it is a boundary datum."),
       "verdict": None}
out["verdict"] = ("x* is NOT derivable from {G, c, a0, H0, Lambda}: without a mass scale every tidal scale is a power "
                  f"of cH0/a0 = {r:.3f}, and the window needs a power {need_n[0]:.1f}-{need_n[1]:.1f}, which is unnatural. "
                  "Cassini's x* equals the tidal field near the Sun's MOND radius "
                  f"(ratio {7.04e11/x_at_rM:.2f}). That explains the value but is Sun-specific. So x* and C are genuine new "
                  "constants (a tidal scale and a boundary datum), not derivable within this theory.")
print(json.dumps(out, indent=1)); json.dump(out, open("CONSTANTS_DERIVATION.json", "w"), indent=1)
