#!/usr/bin/env python3
"""Item 2 cont.: growth of linear modes with the phantom boost b(z,k) = (nu - 1) * S_low(x) * S_high(x).
Matter era: x(z) = x0 (1+z)^2 and g(z) = g0 (1+z), where x0 and g0 come from LINEAR_COSMOLOGY.json.
S_low = 1/(1 + (x_low/x)^2) is a proposed low-x cut; S_high (x* = 7.04e11) is irrelevant here.
Solves D'' + (2 + dlnH/dlna) D' = 1.5 Om(a) (1 + b) D in ln a, from z = 1e3 to 0. Reports D/D_LCDM at z = 0."""
import json, math
import numpy as np
from scipy.integrate import solve_ivp
a0 = 1.1607e-10; Om = 0.315; OL = 1 - Om
nu = lambda y: math.sqrt(0.5 * (1 + math.sqrt(1 + 4 / y**2)))
lin = json.load(open("LINEAR_COSMOLOGY.json"))["linear_modes_z0"]
E2 = lambda a: Om / a**3 + OL
def D_final(x0, g0, xlow):
    def rhs(la, y):
        a = math.exp(la); z = 1 / a - 1
        x = x0 * (1 + z) ** 2; g = g0 * (1 + z)
        if xlow is None: b = 0.0
        elif xlow == "none": b = nu(g / a0) - 1
        else: b = (nu(g / a0) - 1) / (1 + (xlow / x) ** 2)
        Oma = Om / a**3 / E2(a); dlnH = -1.5 * Oma
        D, Dp = y
        return [Dp, -(2 + dlnH) * Dp + 1.5 * Oma * (1 + b) * D]
    a_i = 1e-3
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [a_i, a_i], rtol=1e-8)
    return s.y[0, -1]
out = {}
for name, m in lin.items():
    base = D_final(m["x"], m["g"], None)
    row = {}
    for xl in ("none", 5e2, 5e3):
        row[str(xl)] = D_final(m["x"], m["g"], xl) / base
    out[name] = row
    print(name, {k: round(v, 3) for k, v in row.items()})
json.dump(out, open("LINEAR_GROWTH.json", "w"), indent=1)
