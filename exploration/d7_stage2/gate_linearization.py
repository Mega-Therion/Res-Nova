#!/usr/bin/env python3
"""D7 Stage 2, gate A2: the steady-state Lagrangian of derive_steady.py, linearized about a uniform MOND gradient g
(par: along the wind axis z; perp: along x) with static plane waves e^{ikz}, must reproduce the validated wind operator
d3_alpha/wind_bg_matrix_{dir}_K275.json at omega = 0 and qbar = 0.
The two bookkeepings differ only by terms smaller by h ~ 1e-8 or u ~ 1e-5, which the builder keeps because it counts
g as O(1). Entry-wise agreement is therefore expected to about 1e-5 relative.
The scalar function is expanded to second order about Y0: K' = (2-K_B)(1+Jp), K'' = (2-K_B) Jl / (2 Y0), which is the
builder's (1+Jp) Y2 + Jl Y1^2 / (4 Y0).
Usage: gate_linearization.py [par|perp]"""

import json, sys, sympy as sp, mpmath as mp

sys.path.insert(0, "../d3_alpha")
from sym_json import dec, load_matrix
from wind_cli import pick_dir

mp.mp.dps = 40
DIR = pick_dir()
d = json.load(open("steady_lagrangian.json"))
L2, Y2 = dec(d["L2"]), dec(d["Y2"])
x, y, z = sp.symbols("x y z", real=True)
vw = sp.Symbol("v_w", real=True)
g, Jp, Jl, k, s = sp.symbols("g Jp Jl k s", real=True)
KB = sp.Rational(1, 2)
keep = [
    "h00",
    "h01",
    "h03",
    "h11",
    "h22",
    "h33",
    "h13",
    "ux",
    "uz",
    "phi",
]  # builder order: h00 h0x h0z hxx hyy hzz hxz ux uz phi
dz = {n: sp.Function(n + "_z")(z) for n in keep}
sub = {}
for sym in L2.free_symbols | Y2.free_symbols:
    nm = sym.name
    if nm == "v_w":
        continue
    base, _, der = (
        nm.rpartition("_") if nm.rsplit("_", 1)[-1] in ("x", "y", "z") else (nm, "", "")
    )
    if base == "phi":  # scalar: background gradient + plane wave along z
        bg = {"par": {"z": g}, "perp": {"x": g}}[DIR]
        sub[sym] = (
            bg.get(der, 0) + (s * sp.diff(dz["phi"], z) if der == "z" else 0)
            if der
            else s * dz["phi"]
        )
    elif base in keep:
        sub[sym] = s * (
            dz[base] if der == "" else (sp.diff(dz[base], z) if der == "z" else 0)
        )
    else:
        sub[sym] = 0  # uy, h02, h12, h23: decouple by y -> -y reflection


def lin(expr):
    ex = sp.expand(expr.subs(sub).doit())
    return [sp.expand(ex.coeff(s, i)) for i in range(3)]


L2c, Y2c = lin(L2), lin(Y2)
Y0 = sp.simplify(Y2c[0])
Kp, Kpp = (2 - KB) * (1 + Jp), (2 - KB) * Jl / (2 * Y0)
Lq = sp.expand(L2c[2] - Kp * Y2c[2] - Kpp * Y2c[1] ** 2 / 2)
fields = [dz[n] for n in keep]
eqs = sp.calculus.euler.euler_equations(Lq, fields, [z])
ph = sp.exp(sp.I * k * z)
amp = {f: sp.Symbol("A_" + str(f.func)) for f in fields}
alg = [
    sp.expand(
        sp.powsimp(sp.expand(eq.lhs.subs({f: amp[f] * ph for f in fields}).doit() / ph))
    )
    for eq in eqs
]
Mmine = sp.Matrix([[sp.diff(a, amp[f]) for f in fields] for a in alg])
MB, names, pars, _ = load_matrix(f"../d3_alpha/wind_bg_matrix_{DIR}_K275.json")
qb, JpB, JlB, gB, kB, wB, vB = pars
c_kms = mp.mpf(299792.458)
xv = mp.mpf("0.05")
num = {
    "g": xv * 2 * mp.mpf("3.577e-5"),
    "Jp": xv / mp.sqrt(1 + xv**2),
    "Jl": xv * (1 + xv**2) ** mp.mpf(-1.5),
    "k": 1 / mp.mpf("3e-4"),
}
worst = 0
for vk in ("0", "10", "150"):
    vv = mp.mpf(vk) / c_kms
    fm = sp.lambdify((g, Jp, Jl, k, vw), Mmine, "mpmath")
    fb = sp.lambdify((qb, JpB, JlB, gB, kB, wB, vB), MB, "mpmath")
    A = mp.matrix(fm(num["g"], num["Jp"], num["Jl"], num["k"], vv))
    B = mp.matrix(fb(0, num["Jp"], num["Jl"], num["g"], num["k"], 0, vv))
    scale = max(abs(B[i, j]) for i in range(B.rows) for j in range(B.cols))
    rel = max(
        abs(A[i, j] - B[i, j]) / max(abs(B[i, j]), scale * mp.mpf("1e-12"))
        for i in range(B.rows)
        for j in range(B.cols)
        if abs(B[i, j]) > scale * 1e-12 or abs(A[i, j]) > scale * 1e-12
    )
    absd = (
        max(abs(A[i, j] - B[i, j]) for i in range(B.rows) for j in range(B.cols))
        / scale
    )
    worst = max(worst, float(absd))
    print(
        f"{DIR}, v = {vk} km/s: max |M_mine - M_builder| / max|M| = {float(absd):.3e}; max entry-wise relative = {float(rel):.3e}",
        flush=True,
    )
print(
    f"GATE A2 {'PASS' if worst < 1e-4 else 'FAIL'} ({DIR}): worst normalized difference {worst:.3e}"
)
