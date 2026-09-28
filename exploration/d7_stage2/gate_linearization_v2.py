#!/usr/bin/env python3
"""D7 Stage 2, gate A2 (v2): the v2 steady-state Lagrangian (exact in the aether and scalar), linearized about a uniform
MOND gradient g (par: along the wind axis z; perp: along x) with static plane waves e^{ikz}, must reproduce the
validated wind operator d3_alpha/wind_bg_matrix_{dir}_K275.json at omega = 0 and qbar = 0.
Quadratic part: L_q = (1/2) d^2/ds^2 Lrest |_(s=0) - [K'(Y0) Y2 + (1/2) K''(Y0) Y1^2], where Y1 = dY/ds, Y2 = (1/2)
d^2Y/ds^2 at s = 0, K' = (2-K_B)(1+Jp), K'' = (2-K_B) Jl/(2 Y0).
Comparison: each column is weighted by its field's typical size (h ~ 1e-8, u ~ g/Q0 = 3.6e-5, phi ~ 1e-9), and each
entry's difference is compared with its row's largest weighted entry. PASS if every entry agrees to 1e-6.
Usage: gate_linearization_v2.py [par|perp]"""

import json, sys, sympy as sp, mpmath as mp

sys.path.insert(0, "../d3_alpha")
from sym_json import dec, load_matrix
from wind_cli import pick_dir

mp.mp.dps = 40
DIR = pick_dir()
d = json.load(open("steady_lagrangian_v2.json"))
Lrest, Y = dec(d["Lrest"]), dec(d["Y"])
z = sp.Symbol("z", real=True)
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
]  # builder order
fz = {n: sp.Function(n + "_z")(z) for n in keep}
sub = {}
for sym in Lrest.free_symbols | Y.free_symbols:
    nm = sym.name
    if nm == "v_w":
        continue
    parts = nm.rsplit("_", 1)
    base, der = (
        (parts[0], parts[1])
        if len(parts) == 2 and parts[1] in ("x", "y", "z")
        else (nm, "")
    )
    if base == "phi":
        bg = {"par": {"z": g}, "perp": {"x": g}}[DIR].get(der, 0) if der else 0
        sub[sym] = (
            bg
            + (s * sp.diff(fz["phi"], z) if der == "z" else 0)
            + (s * fz["phi"] if der == "" else 0)
        )
    elif base in keep:
        sub[sym] = s * (
            fz[base] if der == "" else (sp.diff(fz[base], z) if der == "z" else 0)
        )
    else:
        sub[sym] = 0  # uy, h02, h12, h23 decouple by y -> -y reflection


def orders(expr):
    ex = expr.xreplace(sub)
    e0 = ex.subs(s, 0)
    e1 = sp.diff(ex, s).subs(s, 0)
    e2 = sp.diff(ex, s, 2).subs(s, 0) / 2
    return e0, e1, e2


L0, L1, L2q = orders(Lrest)
Y0, Y1, Y2q = orders(Y)
Y0 = sp.simplify(Y0)
Kp, Kpp = (2 - KB) * (1 + Jp), (2 - KB) * Jl / (2 * Y0)
Lq = L2q - Kp * Y2q - Kpp * Y1**2 / 2
fields = [fz[n] for n in keep]
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
SC = {
    n: (
        mp.mpf("3.6e-5")
        if n in ("ux", "uz")
        else mp.mpf("1e-9") if n == "phi" else mp.mpf("1e-8")
    )
    for n in keep
}
fm = sp.lambdify((g, Jp, Jl, k, vw), Mmine, "mpmath")
fb = sp.lambdify((qb, JpB, JlB, gB, kB, wB, vB), MB, "mpmath")
worst = mp.mpf(0)
for vk in ("0", "10", "150"):
    vv = mp.mpf(vk) / c_kms
    A = mp.matrix(fm(num["g"], num["Jp"], num["Jl"], num["k"], vv))
    B = mp.matrix(fb(0, num["Jp"], num["Jl"], num["g"], num["k"], 0, vv))
    bad = []
    for i in range(B.rows):
        rowscale = max(abs(B[i, j]) * SC[keep[j]] for j in range(B.cols))
        for j in range(B.cols):
            dd = abs(A[i, j] - B[i, j]) * SC[keep[j]] / rowscale
            worst = max(worst, dd)
            if dd > mp.mpf("1e-6"):
                bad.append(
                    f"row {keep[i]} col {keep[j]}: mine {mp.nstr(A[i, j], 8)} builder {mp.nstr(B[i, j], 8)} (weighted rel {mp.nstr(dd, 3)})"
                )
    print(
        f"{DIR}, v = {vk} km/s: {len(bad)} entries differ by > 1e-6 (weighted, row-relative)",
        flush=True,
    )
    for b_ in bad[:12]:
        print("   ", b_)
print(
    f"GATE A2 v2 {'PASS' if worst < 1e-6 else 'FAIL'} ({DIR}): worst weighted row-relative difference {mp.nstr(worst, 3)}"
)
