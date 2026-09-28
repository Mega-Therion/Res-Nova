#!/usr/bin/env python3
"""Fast builder: constrained AeST linear system with (i) Q-offset qbar, (ii) uniform background scalar gradient g
(local MOND field) along z (par: k || grad phi) or x (perp), (iii) local stiffness J'=Jp and 2Y J''=Jl.
Numbers for the parameter point go in early. All perturbative quantities are polynomials in the bookkeeping e,
so truncation is expand-and-collect (no series). Output: matrix per direction, saved as safe JSON (sym_json.py)."""
import sys, sympy as sp
from wind_cli import pick_dir, pick_k2
from sym_json import dump_matrix
direction = pick_dir()                        # 'par' or 'perp' (allowlisted)
KBv, K2v, Q0v = sp.Rational(1, 2), sp.Integer(pick_k2()), sp.Rational(1, 10)
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
k, w = sp.symbols('k omega', positive=True)
qb, Jp, Jl, g = sp.symbols('qbar Jp Jl g', real=True)
vw = sp.Symbol('v_w', real=True)   # background aether wind speed along -z (dwarf frame)
e = sp.Symbol('e')
eta = sp.diag(-1, 1, 1, 1)
names = {(0, 0): 'h00', (0, 1): 'h0x', (0, 3): 'h0z', (1, 1): 'hxx', (2, 2): 'hyy', (3, 3): 'hzz', (1, 3): 'hxz'}
F = {n: sp.Function(n)(t, z) for n in names.values()}
UX, UZ, P = sp.Function('ux')(t, z), sp.Function('uz')(t, z), sp.Function('phi')(t, z)
h = sp.zeros(4, 4)
for (a, b), n in names.items(): h[a, b] = F[n]; h[b, a] = F[n]
def trunc(expr, n=2):
    ex = sp.expand(expr); return sum(ex.coeff(e, i) * e**i for i in range(n + 1))
gm = eta + e * h
hu = eta * h * eta
gi = eta - e * hu + e**2 * (hu * eta * h * eta)
gi = gi.applyfunc(lambda q: trunc(q))
a1, a2 = sp.symbols('a1 a2')
gw = 1/sp.sqrt(1 - vw**2)
uv = [gw + e * a1 + e**2 * a2, e * UX, 0, -vw * gw + e * UZ]
norm = sp.expand(sum(gm[m, n] * uv[m] * uv[n] for m in range(4) for n in range(4)) + 1)
norm = sp.expand(sp.series(norm, e, 0, 3).removeO())
sa1 = sp.solve(norm.coeff(e, 1), a1)[0]; sa2 = sp.solve(sp.expand(norm.coeff(e, 2).subs(a1, sa1)), a2)[0]
uv = [trunc(u.subs(a1, sa1).subs(a2, sa2)) if not isinstance(u, int) else u for u in uv]
gx_, gz_ = (0, g) if direction == 'par' else (g, 0)
dphi = [(Q0v + qb) * gw + e * sp.diff(P, t), gx_, 0, (Q0v + qb) * gw * vw + gz_ + e * sp.diff(P, z)]
d = lambda f, a: sp.diff(f, X[a])
# ---- EH (FP + de Donder) and Maxwell aether (c1=K_B, c3=-K_B) quadratic pieces, as in the validated pipeline ----
trh = sum(eta[a, a] * h[a, a] for a in range(4))
L_EH = sum(-d(h[m, n], l) * eta[l, l] * d(hu[m, n], l) for l in range(4) for m in range(4) for n in range(4)) \
       + sum(sp.Rational(1, 2) * d(trh, l) * eta[l, l] * d(trh, l) for l in range(4))
L_EH = L_EH / 4                               # 16 pi G = 1 units: (1/64piG) -> 1/4
# Maxwell aether term, exact in the metric, truncated to O(e^2)
A_lo = [trunc(sum(gm[m, n] * uv[n] for n in range(4))) for m in range(4)]
Fm = [[d(A_lo[b], a) - d(A_lo[a], b) for b in range(4)] for a in range(4)]
F2 = trunc(sum(Fm[a][b] * Fm[c][dd_] * gi[a, c] * gi[b, dd_] for a in range(4) for b in range(4) for c in range(4) for dd_ in range(4)))
L_ae = -(KBv / 2) * F2.coeff(e, 2)
# ---- scalar sector, perturbative to O(e^2) ----
Gam2 = [[[trunc(sum(gi[m, n] * (d(gm[n, a], b) + d(gm[n, b], a) - d(gm[a, b], n)) for n in range(4)) / 2)
          for b in range(4)] for a in range(4)] for m in range(4)]
Jv = [trunc(sum(uv[a] * (d(uv[m], a) + sum(Gam2[m][a][b] * uv[b] for b in range(4))) for a in range(4))) for m in range(4)]
Yq = trunc(sum((gi[m, n] + uv[m] * uv[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
Qq = trunc(sum(uv[m] * dphi[m] for m in range(4)))
Jphi = trunc(sum(Jv[m] * dphi[m] for m in range(4)))
Y0 = g**2
dQ2 = trunc((Qq - Q0v)**2)
Y0 = sp.expand(Yq.coeff(e, 0))
L_phi = 2 * (2 - KBv) * Jphi.coeff(e, 2) - (2 - KBv) * ((1 + Jp) * Yq.coeff(e, 2) + Jl * Yq.coeff(e, 1)**2 / (4 * Y0)) \
        + 2 * K2v * dQ2.coeff(e, 2)
L = sp.expand(L_EH + L_ae + L_phi)
fields = list(F.values()) + [UX, UZ, P]
eqs = sp.calculus.euler.euler_equations(L, fields, [t, z])
ph = sp.exp(sp.I * (k * z - w * t))
amp = {f: sp.Symbol('A_' + str(f.func)) for f in fields}
sub = {f: amp[f] * ph for f in fields}
alg = [sp.expand(sp.powsimp(sp.expand(e_.lhs.subs(sub).doit() / ph))) for e_ in eqs]
unk = list(amp.values())
Msym = sp.Matrix([[sp.diff(a, u) for u in unk] for a in alg])
dump_matrix(f"wind_bg_matrix_{direction}_K2{K2v}.json", Msym, [str(f.func) for f in fields], (qb, Jp, Jl, g, k, w, vw), (KBv, K2v, Q0v))
print("built", direction, Msym.shape, "free symbols:", sorted(map(str, Msym.free_symbols)))
