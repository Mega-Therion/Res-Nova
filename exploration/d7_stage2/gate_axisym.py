#!/usr/bin/env python3
"""D7 Stage 2, gate A': the axisymmetric reduction (reduce_axisym.py) must reproduce the Cartesian Lagrangian.
Random smooth axisymmetric test fields (polynomials in R and z, with the correct axis parity) are built as Cartesian
components. The Cartesian Lrest and Y (steady_lagrangian_v2.json) are evaluated at a point OFF the reduction plane
(azimuth 0.7 rad, which also tests the Lagrangian's invariance about the wind axis) and compared with the reduced
density at the same (R, z)."""

import json, sys, random, sympy as sp

sys.path.insert(0, "../d3_alpha")
from sym_json import dec

random.seed(20260928)
x, y, z = sp.symbols("x y z", real=True)
Rs = sp.Symbol("R", positive=True)
vw = sp.Symbol("v_w", real=True)
cart = json.load(open("steady_lagrangian_v2.json"))
axi = json.load(open("steady_lagrangian_axisym.json"))
Lc, Yc, La, Ya = dec(cart["Lrest"]), dec(cart["Y"]), dec(axi["Lrest"]), dec(axi["Y"])
r = sp.sqrt(x**2 + y**2)


def poly(odd, scale):
    """Random smooth function of (R, z): even in R, or R x (even), times a Gaussian-free small scale."""
    c = [sp.Rational(random.randint(-9, 9), 10) for _ in range(6)]
    even = c[0] + c[1] * z + c[2] * r**2 + c[3] * z**2 + c[4] * r**2 * z + c[5] * z**3
    return scale * (r * even if odd else even)


sc = {
    "S": 1e-8,
    "W_R": 1e-8,
    "W_z": 1e-8,
    "A": 1e-8,
    "B": 1e-8,
    "C": 1e-8,
    "D": 1e-8,
    "U_R": 3e-5,
    "U_z": 3e-5,
    "F": 1e-8,
}
odd = {"W_R", "C", "U_R"}
f = {n: poly(n in odd, sp.Float(s_)) for n, s_ in sc.items()}
f["B"] = f["B"] * r**2  # B n n must vanish like R^2 on the axis
nx, ny = x / r, y / r
comp = {
    "h00": f["S"],
    "h01": f["W_R"] * nx,
    "h02": f["W_R"] * ny,
    "h03": f["W_z"],
    "h11": f["A"] + f["B"] * nx * nx,
    "h22": f["A"] + f["B"] * ny * ny,
    "h33": f["A"] + f["D"],
    "h12": f["B"] * nx * ny,
    "h13": f["C"] * nx,
    "h23": f["C"] * ny,
    "ux": f["U_R"] * nx,
    "uy": f["U_R"] * ny,
    "uz": f["U_z"],
    "phi": f["F"],
}
R0, th, z0 = sp.Rational(7, 10), sp.Rational(7, 10), sp.Rational(-3, 10)
pt = {x: R0 * sp.cos(th), y: R0 * sp.sin(th), z: z0}
csub = {}
for n, ex in comp.items():
    csub[sp.Symbol(n, real=True)] = ex.subs(pt).evalf(30)
    for c_ in "xyz":
        csub[sp.Symbol(f"{n}_{c_}", real=True)] = (
            sp.diff(ex, {"x": x, "y": y, "z": z}[c_]).subs(pt).evalf(30)
        )
asub = {Rs: R0}
for n, ex in f.items():
    exRz = ex.subs(
        {x: Rs, y: 0}
    )  # on the plane y = 0 the functions are functions of (R, z)
    asub[sp.Symbol(n)] = exRz.subs({Rs: R0, z: z0}).evalf(30)
    asub[sp.Symbol(n + "_R")] = sp.diff(exRz, Rs).subs({Rs: R0, z: z0}).evalf(30)
    asub[sp.Symbol(n + "_z")] = sp.diff(exRz, z).subs({Rs: R0, z: z0}).evalf(30)
worst = 0.0
for vv in (0, sp.Rational(1, 2000), sp.Rational(3, 10)):
    for name, ec, ea in (("Lrest", Lc, La), ("Y", Yc, Ya)):
        vc = sp.N(ec.xreplace(csub).subs(vw, vv), 30)
        va = sp.N(ea.xreplace(asub).subs(vw, vv), 30)
        rel = abs(vc - va) / max(abs(vc), 1e-300)
        worst = max(worst, float(rel))
        print(
            f"v = {float(vv):.4g}: {name} Cartesian {float(vc):.12e}  reduced {float(va):.12e}  rel diff {float(rel):.2e}"
        )
print(
    f"GATE A' {'PASS' if worst < 1e-12 else 'FAIL'}: worst relative difference {worst:.2e}"
)
