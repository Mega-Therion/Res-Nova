#!/usr/bin/env python3
"""BBN ceiling from the AeST non-folding condition, for any interpolating function (2026-11-18). [D]

Total law x = y nu(y) (QUMOND form). In the AeST total-scalar correspondence the scalar channel is s = x - eta y(x).
It is single-valued iff s'(x) = 1 - eta y'(x) > 0 for all x, i.e. eta < min_y d(y nu)/dy.
G_cosmo/G_N = eta (2 - K_B)/2 (repo formula with eta = lambda/(1+lambda)), so without solar-system screening
  sup G_cosmo/G_N = min_y d(y nu)/dy   (K_B -> 0).
For mu_std this is sqrt(27/32) = 0.91856 (reproduces Wave3BBNAndSpinCCP2Bounds). BBN at 5% needs >= 0.95.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../02_galaxy_dynamics"))
from cassini_sparc_joint import FUN
from cassini_sparc_joint_scan import make
y = np.logspace(-8, 8, 400001)
def ceiling(nu):
    x = y * nu(y); return float(np.gradient(x, y).min())
out = {"families": {}, "near_miss_shapes": {}}
for name, nu in FUN.items():
    out["families"][name] = ceiling(nu)
for tag, (f, p) in {"nu_5": ("a", (5.0,)), "nu_6": ("a", (6.0,)), "nu_6,0": ("b", (6.0, 0.0)),
                    "nu_6,0.25": ("b", (6.0, 0.25)), "nu_8,0.25": ("b", (8.0, 0.25))}.items():
    out["near_miss_shapes"][tag] = ceiling(make(f, p))
assert abs(out["families"]["nu_2"] - (27 / 32) ** 0.5) < 1e-4
cas = json.load(open(os.path.join(HERE, "../../02_galaxy_dynamics/CASSINI_SPARC_JOINT.json")))
out["frontier"] = {k: {"bbn_ceiling": out["families"][k], "Q2_max": max(cas[k]["Q2_ge1.9"], cas[k]["Q2_ge2.4"])}
                   for k in ("nu_1", "nubar_0.5", "nu_2", "nu_3") if k in cas}
out["verdict"] = ("Only nu_1 and nubar_0.5 clear BBN 5% (ceilings 1.000, 0.968), and both fail Cassini "
                  "(Q2 2.7-3.5e-26). Every shape steep enough to help Cassini has ceiling <= 0.84. BBN and Cassini "
                  "pull the interpolating function in opposite directions.")
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "BBN_FOLDING_GATE.json"), "w"), indent=1)
