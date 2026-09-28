#!/usr/bin/env python3
"""D7 Stage 2, step A (v2): the steady-state AeST Lagrangian for a static source in a uniform aether wind, exact in the
aether perturbation and the scalar, first order in the metric for the couplings, second order in the metric in the
Einstein-Hilbert term.

Why exact in the aether (gate A2 of v1 failed on this): at dwarf scales the tilt u ~ g/Q0 ~ 4e-5 is small, but its
gradient u/r ~ 0.1/Mpc matches Q0. So each extra factor (u . d) costs nothing, and terms up to u^4 d^2 are leading
order. Counting potentials ~ delta^2, u ~ d(phi)/Q0 ~ delta, d ~ Q0/delta: the leading Lagrangian is O(delta^2).
That keeps
  (i)   every flat-space term exactly (F^2, J.dphi, K(Y), (Q - Q0)^2 as functions of u and d(phi));
  (ii)  terms linear in h (built here exactly in u; the counting would allow dropping the higher ones);
  (iii) (dh)^2 from the Fierz-Pauli + de Donder term.
Terms of order h x (leading Lagrangian), including the sqrt(-g) prefactor and (Q - Q0)^2 at O(h^2), are O(delta^4)
and are dropped.

Fields are jet symbols (value X, derivatives X_x, X_y, X_z) for h_{mu nu} (10), the spatial aether perturbation
(ux, uy, uz) and the scalar phi. The full spatial aether is w = (ux, uy, -v gamma + uz). u^0 = N0 + N1, with
N0 = sqrt(1 + |w|^2) and N1 the O(h) unit-norm correction. Derivatives of composites use the chain rule over the
field values. Everything is assembled as O(h^0) + O(h^1) pieces explicitly, without series or full expansion.
Output (sym_json): Lrest (everything except the scalar function) and Y (the argument of K), so that
L = Lrest - K(Y), K(Y) = (2 - K_B)(Y + J(Y)), J' = mu_std(sqrt(Y)/a0t). Units 16 pi G = 1; K_B = 1/2, K2 = 75,
Q0 = 1/10 per Mpc."""

import json, sys, time, sympy as sp

sys.path.insert(0, "../d3_alpha")
from sym_json import enc

KB, K2, Q0 = sp.Rational(1, 2), sp.Integer(75), sp.Rational(1, 10)
v = sp.Symbol("v_w", real=True)
gam = 1 / sp.sqrt(1 - v**2)
comps = [(a, b) for a in range(4) for b in range(a, 4)]
FIELDS = [f"h{a}{b}" for a, b in comps] + ["ux", "uy", "uz", "phi"]
S = {n: sp.Symbol(n, real=True) for n in FIELDS}
Dj = {
    (n, i): sp.Symbol(f"{n}_{c}", real=True)
    for n in FIELDS
    for i, c in ((1, "x"), (2, "y"), (3, "z"))
}
HN = [f"h{a}{b}" for a, b in comps]


def D(expr, i):
    """d/dx^i of an expression in field values (static: i = 0 gives 0)."""
    if i == 0 or expr == 0:
        return sp.Integer(0)
    expr = sp.sympify(expr)
    return sp.Add(*[sp.diff(expr, S[n]) * Dj[(n, i)] for n in FIELDS if expr.has(S[n])])


def h1part(expr):
    """Part of expr linear in the h symbols (expr assumed polynomial of degree <= 1 in h after construction)."""
    return sp.Add(
        *[
            S[n] * sp.diff(expr, S[n]).subs({S[m]: 0 for m in HN})
            for n in HN
            if expr.has(S[n])
        ]
    )


t0 = time.time()
eta = sp.diag(-1, 1, 1, 1)
h = sp.zeros(4, 4)
for a, b in comps:
    h[a, b] = S[f"h{a}{b}"]
    h[b, a] = S[f"h{a}{b}"]
hup = eta * h * eta  # h^{mn} (indices raised with eta)
w = [S["ux"], S["uy"], -v * gam + S["uz"]]
N0 = sp.sqrt(1 + sum(wi**2 for wi in w))
# O(h) unit-norm correction: g_mn u^m u^n = -1 at O(h): -2 N0 N1 + h00 N0^2 + 2 N0 h0i w_i + h_ij w_i w_j = 0
N1 = (
    h[0, 0] * N0**2
    + 2 * N0 * sum(h[0, i + 1] * w[i] for i in range(3))
    + sum(h[i + 1, j + 1] * w[i] * w[j] for i in range(3) for j in range(3))
) / (2 * N0)
u0 = [N0] + w  # O(h^0) aether (upper)
u1 = [N1, 0, 0, 0]  # O(h^1) correction (upper)
dphi = [Q0 * gam, Dj[("phi", 1)], Dj[("phi", 2)], Q0 * gam * v + Dj[("phi", 3)]]
print(f"setup {time.time()-t0:.1f}s", flush=True)

# lowered aether A_m = g_mn u^n: O(1) and O(h) parts
A0 = [sum(eta[m, n] * u0[n] for n in range(4)) for m in range(4)]
A1 = [sum(eta[m, n] * u1[n] + h[m, n] * u0[n] for n in range(4)) for m in range(4)]
F0 = [[D(A0[b], a) - D(A0[a], b) for b in range(4)] for a in range(4)]
F1 = [[D(A1[b], a) - D(A1[a], b) for b in range(4)] for a in range(4)]
# F^2 = F_ab F_cd g^ac g^bd, g^ac = eta^ac - h^ac: O(1) and O(h)
F2_0 = sp.Add(
    *[eta[a, a] * eta[b, b] * F0[a][b] ** 2 for a in range(4) for b in range(4)]
)
F2_1 = sp.Add(
    *[
        2 * eta[a, a] * eta[b, b] * F0[a][b] * F1[a][b]
        for a in range(4)
        for b in range(4)
    ]
) - sp.Add(
    *[
        2 * hup[a, c] * eta[b, b] * F0[a][b] * F0[c][b]
        for a in range(4)
        for c in range(4)
        for b in range(4)
        if hup[a, c] != 0
    ]
)
print(f"F2 {time.time()-t0:.1f}s", flush=True)
# Christoffels at O(h): Gamma^m_ab = (1/2) eta^mm (d_a h_mb + d_b h_ma - d_m h_ab)
Gam = [
    [
        [
            eta[m, m] * (D(h[m, b], a) + D(h[m, a], b) - D(h[a, b], m)) / 2
            for b in range(4)
        ]
        for a in range(4)
    ]
    for m in range(4)
]
# J^m = u^a d_a u^m + Gamma^m_ab u^a u^b: O(1) and O(h)
J0 = [sp.Add(*[u0[a] * D(u0[m], a) for a in range(4)]) for m in range(4)]
J1 = [
    sp.Add(*[u1[a] * D(u0[m], a) + u0[a] * D(u1[m], a) for a in range(4)])
    + sp.Add(*[Gam[m][a][b] * u0[a] * u0[b] for a in range(4) for b in range(4)])
    for m in range(4)
]
Jphi0 = sp.Add(*[J0[m] * dphi[m] for m in range(4)])
Jphi1 = sp.Add(*[J1[m] * dphi[m] for m in range(4)])
# O(h^2) Christoffel piece, Gamma^m_ab = (1/2)(-h^mn)(d_a h_nb + d_b h_na - d_n h_ab), on the background aether. By the
# counting it is O(delta^3) (Q0 h dh); kept so the linearization matches the builder exactly (e.g. -(3/2) Q0 h0z d_z h00).
Gam2nd = [
    [
        [
            sp.Add(
                *[
                    -hup[m, n] * (D(h[n, b], a) + D(h[n, a], b) - D(h[a, b], n)) / 2
                    for n in range(4)
                    if hup[m, n] != 0
                ]
            )
            for b in range(4)
        ]
        for a in range(4)
    ]
    for m in range(4)
]
Jphi2 = sp.Add(
    *[
        Gam2nd[m][a][b] * u0[a] * u0[b] * dphi[m]
        for m in range(4)
        for a in range(4)
        for b in range(4)
    ]
)
Jphi1 = Jphi1 + Jphi2
# Y = (g^mn + u^m u^n) dphi_m dphi_n and Q = u^m dphi_m
ud0 = sp.Add(*[u0[m] * dphi[m] for m in range(4)])
ud1 = sp.Add(*[u1[m] * dphi[m] for m in range(4)])
Y0 = sp.Add(*[eta[m, m] * dphi[m] ** 2 for m in range(4)]) + ud0**2
Y1 = (
    -sp.Add(
        *[
            hup[m, n] * dphi[m] * dphi[n]
            for m in range(4)
            for n in range(4)
            if hup[m, n] != 0
        ]
    )
    + 2 * ud0 * ud1
)
Qm0 = ud0 - Q0
print(f"J, Y, Q {time.time()-t0:.1f}s", flush=True)
# Fierz-Pauli + de Donder (as the validated builder), static
trh = sum(eta[a, a] * h[a, a] for a in range(4))
L_EH = (
    sp.Add(
        *[
            -D(h[m, n], l) * eta[l, l] * D(hup[m, n], l)
            for l in range(1, 4)
            for m in range(4)
            for n in range(4)
        ]
    )
    + sp.Add(
        *[sp.Rational(1, 2) * D(trh, l) * eta[l, l] * D(trh, l) for l in range(1, 4)]
    )
) / 4
# O(h^2) aether term: F1.F1 with the flat inverse metric. It is (dh)^2, the same order as Einstein-Hilbert: A_0 carries
# h00/2 through the unit norm, and at K_B = 1/2 its (dh00)^2 cancels EH's exactly, as in the validated builder.
# The other O(h^2) pieces (F0.F2, h h F0 F0, h^{ac} F0 F1) carry powers of u and are O(delta^4).
F2_2 = sp.Add(
    *[eta[a, a] * eta[b, b] * F1[a][b] ** 2 for a in range(4) for b in range(4)]
)
Lrest = (
    -(KB / 2) * (F2_0 + F2_1 + F2_2)
    + 2 * (2 - KB) * (Jphi0 + Jphi1)
    + 2 * K2 * (Qm0**2 + 2 * Qm0 * ud1)
    + L_EH
)
Y = Y0 + Y1
# sanity at the pure background (all perturbations zero): Y, (Q - Q0), J.dphi and F^2 vanish
bg = {s_: 0 for s_ in list(S.values()) + list(Dj.values())}
# sympy cannot cancel sqrt(1/(1-v^2)) sqrt(1-v^2) without |v| < 1, so check numerically at several wind speeds
chk = [
    max(abs(float(x_.subs(bg).subs(v, vv))) for vv in (0, 5e-4, 0.3, 0.9))
    for x_ in (Y0, Qm0, Jphi0, F2_0)
]
print(
    f"background check, max over v in (0, 5e-4, 0.3, 0.9) of |Y0|, |Q-Q0|, |J.dphi|, |F^2| = {chk}  [{time.time()-t0:.1f}s]",
    flush=True,
)
assert all(c_ < 1e-15 for c_ in chk)
json.dump(
    {
        "fields": FIELDS,
        "jets": "X = value, X_x/X_y/X_z = first derivatives",
        "wind_symbol": "v_w",
        "constants": {"K_B": "1/2", "K2": "75", "Q0": "1/10"},
        "Lrest": enc(Lrest),
        "Y": enc(Y),
    },
    open("steady_lagrangian_v2.json", "w"),
)
print(f"saved steady_lagrangian_v2.json  [{time.time()-t0:.1f}s]", flush=True)
