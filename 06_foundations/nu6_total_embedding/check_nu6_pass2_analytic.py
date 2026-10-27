#!/usr/bin/env python3
"""Independent check of the closed-form numbers in Muse's BLK-685 (nu6 pass 2).

Muse's scripts were not available to mirror (see README.md), so this does not
rerun them. It recomputes, from the definitions alone, the numbers that are
closed-form: the single-valuedness bound on lambda_s and the spherical anchor.

mu6(x) = x / (1 + x^6)^(1/6).  AQUAL total law: y = x * mu6(x) = x^2/(1+x^6)^(1/6),
x = g/a0, y = g_N/a0.  y'(x) = x (2 + x^6) / (1 + x^6)^(7/6).
"""
import json, math
from pathlib import Path
from scipy.optimize import brentq, minimize_scalar

def y(x): return x * x / (1 + x**6) ** (1 / 6)
def yp(x): return x * (2 + x**6) / (1 + x**6) ** (7 / 6)

r = minimize_scalar(lambda x: -yp(x), bounds=(0.1, 3.0), method="bounded",
                    options={"xatol": 1e-12})
xstar_num, M6 = r.x, yp(r.x)
xstar_closed = 0.4 ** (1 / 6)
bound = 1 / (yp(xstar_closed) - 1)
phi = (1 + 5 ** 0.5) / 2
x_anchor = brentq(lambda x: y(x) - 1.0, 0.5, 2.0, xtol=1e-15)
out = {
    "xstar_numeric": xstar_num, "xstar_closed_(2/5)^(1/6)": xstar_closed,
    "M6_max_yprime": yp(xstar_closed), "lambda_s_bound_1/(M6-1)": bound,
    "BLK685_M6": 1.3912500682, "BLK685_bound": 2.5559100974,
    "anchor_x_at_gN_eq_a0": x_anchor, "phi^(1/6)": phi ** (1 / 6),
    "anchor_rel_diff": abs(x_anchor / phi ** (1 / 6) - 1),
}
Path(__file__).with_name("check_nu6_pass2_analytic.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
