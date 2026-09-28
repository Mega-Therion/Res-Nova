#!/usr/bin/env python3
"""D7 Stage 2, step A: AeST in the dwarf's rest frame, for static fields in a uniform aether wind v along -z, kept
exact in the MOND non-linearity. The Lagrangian is that of the validated linear builder d3_alpha/aest_wind_bg.py,
with these changes:
  - fields are static functions of (x, y, z): all ten h_{mu nu}, the aether perturbation (ux, uy, uz), and the scalar
    perturbation phi;
  - there is no background MOND gradient and no Q offset: the dwarf's own field lives in phi;
  - the scalar function K(Y) = (2 - K_B)(Y + J(Y)) is kept whole, with J'(Y) = mu_std(sqrt(Y)/a0t).
Bookkeeping: every perturbation, and a0t, counts as O(e), so the Lagrangian is homogeneous of degree 2. K(Y) is
homogeneous because J(Y) = a0t^2 j(Y/a0t^2). Dropped terms are smaller by h ~ 1e-8 or u ~ 1e-5.
Checked here: the zeroth- and first-order parts of Y vanish (the cosmic gradient lies along the boosted aether).
Output (safe JSON, sym_json): L2 = L_EH + L_aether + 2(2-K_B) J.dphi + 2 K2 (Q-Q0)^2 at O(e^2), and Y2 = Y at O(e^2).
Field equations: EL[L2] - EL[K(Y2)] = matter terms. Units 16 pi G = 1; K_B = 1/2, K2 = 75, Q0 = 1/10 per Mpc.
"""

import json, sys, time, sympy as sp

sys.path.insert(0, "../d3_alpha")
from sym_json import enc

KBv, K2v, Q0v = sp.Rational(1, 2), sp.Integer(75), sp.Rational(1, 10)
t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
vw = sp.Symbol("v_w", real=True)
e = sp.Symbol("e")
eta = sp.diag(-1, 1, 1, 1)
comps = [(a, b) for a in range(4) for b in range(a, 4)]
H = {ab: sp.Function(f"h{ab[0]}{ab[1]}")(x, y, z) for ab in comps}
U = [sp.Function(n)(x, y, z) for n in ("ux", "uy", "uz")]
P = sp.Function("phi")(x, y, z)
h = sp.zeros(4, 4)
for (a, b), f in H.items():
    h[a, b] = f
    h[b, a] = f


def trunc(expr, n=2):
    ex = sp.expand(expr)
    return sum(ex.coeff(e, i) * e**i for i in range(n + 1))


t0 = time.time()
gm = eta + e * h
hu = eta * h * eta
gi = (eta - e * hu + e**2 * (hu * eta * h * eta)).applyfunc(trunc)
a1, a2 = sp.symbols("a1 a2")
gw = 1 / sp.sqrt(1 - vw**2)
uv = [gw + e * a1 + e**2 * a2, e * U[0], e * U[1], -vw * gw + e * U[2]]
norm = sp.expand(
    sp.series(
        sp.expand(
            sum(gm[m, n] * uv[m] * uv[n] for m in range(4) for n in range(4)) + 1
        ),
        e,
        0,
        3,
    ).removeO()
)
sa1 = sp.solve(norm.coeff(e, 1), a1)[0]
sa2 = sp.solve(sp.expand(norm.coeff(e, 2).subs(a1, sa1)), a2)[0]
uv = [trunc(u.subs(a1, sa1).subs(a2, sa2)) for u in uv]
d = lambda f, a: sp.diff(f, X[a])
dphi = [Q0v * gw, e * d(P, 1), e * d(P, 2), Q0v * gw * vw + e * d(P, 3)]
print(f"setup {time.time()-t0:.1f}s", flush=True)

trh = sum(eta[a, a] * h[a, a] for a in range(4))
L_EH = (
    sum(
        -d(h[m, n], l) * eta[l, l] * d(hu[m, n], l)
        for l in range(4)
        for m in range(4)
        for n in range(4)
    )
    + sum(sp.Rational(1, 2) * d(trh, l) * eta[l, l] * d(trh, l) for l in range(4))
) / 4
A_lo = [trunc(sum(gm[m, n] * uv[n] for n in range(4)), 1) for m in range(4)]
# The background A (uniform wind) is constant, so F starts at O(e): F^2 at O(e^2) needs only F^(1) and the flat
# inverse metric. (The first run contracted with gi to O(e^2); same result, 38 minutes instead of seconds.)
F1 = [
    [sp.expand(d(A_lo[b], a) - d(A_lo[a], b)).coeff(e, 1) for b in range(4)]
    for a in range(4)
]
L_ae = -(KBv / 2) * sp.expand(
    sum(eta[a, a] * eta[b, b] * F1[a][b] ** 2 for a in range(4) for b in range(4))
)
print(f"EH + aether {time.time()-t0:.1f}s", flush=True)

Gam2 = [
    [
        [
            trunc(
                sum(
                    gi[m, n] * (d(gm[n, a], b) + d(gm[n, b], a) - d(gm[a, b], n))
                    for n in range(4)
                )
                / 2
            )
            for b in range(4)
        ]
        for a in range(4)
    ]
    for m in range(4)
]
Jv = [
    trunc(
        sum(
            uv[a] * (d(uv[m], a) + sum(Gam2[m][a][b] * uv[b] for b in range(4)))
            for a in range(4)
        )
    )
    for m in range(4)
]
Yq = trunc(
    sum(
        (gi[m, n] + uv[m] * uv[n]) * dphi[m] * dphi[n]
        for m in range(4)
        for n in range(4)
    )
)
Qq = trunc(sum(uv[m] * dphi[m] for m in range(4)))
Jphi = trunc(sum(Jv[m] * dphi[m] for m in range(4)))
dQ2 = trunc((Qq - Q0v) ** 2)
Y0, Y1 = sp.simplify(Yq.coeff(e, 0)), sp.simplify(Yq.coeff(e, 1))
Qc0 = sp.simplify(Qq.coeff(e, 0) - Q0v)
print(
    f"scalar sector {time.time()-t0:.1f}s; Y0 = {Y0}, Y1 = {Y1}, Q0-part of (Q - Q0) = {Qc0}",
    flush=True,
)
assert Y0 == 0 and Y1 == 0 and Qc0 == 0

L2 = sp.expand(
    L_EH + L_ae + 2 * (2 - KBv) * Jphi.coeff(e, 2) + 2 * K2v * dQ2.coeff(e, 2)
)
Y2 = sp.expand(Yq.coeff(e, 2))
print(
    f"L2: {len(L2.args)} terms, Y2: {len(Y2.args)} terms, {time.time()-t0:.1f}s",
    flush=True,
)
fields = [H[ab] for ab in comps] + U + [P]


def to_jets(expr):
    """Replace f(x,y,z) -> Symbol('f') and d f / d v -> Symbol('f_v'), so sym_json can store the result."""
    dsub = {}
    for dv in expr.atoms(sp.Derivative):
        ((var, cnt),) = dv.variable_count
        assert cnt == 1, dv
        dsub[dv] = sp.Symbol(f"{dv.expr.func}_{var}", real=True)
    fsub = {
        f: sp.Symbol(str(f.func), real=True)
        for f in expr.atoms(sp.Function)
        if f.args == (x, y, z)
    }
    return sp.expand(expr.xreplace(dsub).xreplace(fsub))


L2j, Y2j = to_jets(L2), to_jets(Y2)
json.dump(
    {
        "fields": [str(f.func) for f in fields],
        "jets": "Symbol f = field value, f_x/f_y/f_z = first derivatives",
        "wind_symbol": "v_w",
        "constants": {"K_B": "1/2", "K2": "75", "Q0": "1/10"},
        "L2": enc(L2j),
        "Y2": enc(Y2j),
    },
    open("steady_lagrangian.json", "w"),
)
print("saved steady_lagrangian.json", flush=True)
