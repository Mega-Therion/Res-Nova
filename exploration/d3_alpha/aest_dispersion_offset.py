#!/usr/bin/env python3
"""Linearized Einstein-aether PPN pipeline: alpha1, alpha2 from a point mass moving at v through
the aether rest frame. Validation targets: GR (a_V=-7/2, a_W=-1/2) and Foster-Jacobson 2006.

Conventions: signature (-+++); S = (1/16piG) Int sqrt(-g) [R - K^{ab}_{mn} D_a u^m D_b u^n
+ lambda(u^2+1)] + S_m, K = c1 g^{ab}g_{mn} + c2 d^a_m d^b_n + c3 d^a_n d^b_m - c4 u^a u^b g_{mn}.
Quadratic action about Minkowski, u = (1,0,0,0); de Donder gauge fixing; plane waves
exp(i(k z - w t)) with w = k.v; source T^{00}=rho, T^{0i}=rho v^i, T^{ij}=rho v^i v^j.
PPN extraction (gamma=1, xi=zeta=0): gauge-transform to (i) isotropic h_ij at O(2) and (ii) no
w^2/k^4 term in h00 at O(4); then h0i = a_V V_i + a_W W_i with
    a_V = -(7 + alpha1 - alpha2)/2,   a_W = -(1 + alpha2)/2.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
X = [t, x, y, z]
eta = sp.diag(-1, 1, 1, 1)
k, w, eps = sp.symbols('k omega epsilon', positive=True)
vx, vz = sp.symbols('v_x v_z', real=True)
G, R = sp.symbols('G R', real=True)
KB, lam, K2, Q0, qb = sp.symbols('K_B lambda_s K_2 Q_0 qbar', real=True)
c1, c2, c3, c4 = KB, 0, -KB, 0          # -(K_B/2)F^2 = -[K_B t1 - K_B t3]

names = {(0, 0): 'h00', (0, 1): 'h0x', (0, 3): 'h0z', (1, 1): 'hxx', (2, 2): 'hyy', (3, 3): 'hzz', (1, 3): 'hxz'}
F = {n: sp.Function(n)(t, z) for n in names.values()}
UX, UZ = sp.Function('ux')(t, z), sp.Function('uz')(t, z)
P = sp.Function('phi')(t, z)
h = sp.zeros(4, 4)
for (a, b), n in names.items():
    h[a, b] = F[n]; h[b, a] = F[n]
du = [h[0, 0] / 2, UX, 0, UZ]           # delta u^mu, du^0 from normalization
d = lambda f, a: sp.diff(f, X[a])
hup = eta * h * eta
trh = sum(eta[a, a] * h[a, a] for a in range(4))

def L_EH():
    L = 0
    for l in range(4):
        for m in range(4):
            for n in range(4):
                L += -d(h[m, n], l) * eta[l, l] * d(hup[m, n], l)
        L += sp.Rational(1, 2) * d(trh, l) * eta[l, l] * d(trh, l)
    return L / (64 * sp.pi * G)                 # FP + de Donder gauge fixing

# Christoffel Gamma^m_{a0} (linear), D_a u^m = d_a du^m + Gamma^m_{a0}
def Gam(m, a, b):
    return sum(eta[m, n] * (d(h[n, a], b) + d(h[n, b], a) - d(h[a, b], n)) for n in range(4)) / 2
Du = [[d(du[m], a) + Gam(m, a, 0) for m in range(4)] for a in range(4)]   # Du[a][m] = D_a u^m
Du_low = [[sum(eta[m, n] * Du[a][n] for n in range(4)) for m in range(4)] for a in range(4)]

def L_ae():
    t1 = sum(eta[a, a] * Du[a][m] * Du_low[a][m] for a in range(4) for m in range(4))
    t2 = sum(Du[a][a] for a in range(4)) ** 2
    t3 = sum(Du[a][m] * Du[m][a] for a in range(4) for m in range(4))
    t4 = -sum(Du[0][m] * Du_low[0][m] for m in range(4))         # -u^a u^b g_mn D_a u^m D_b u^n
    K = c1 * t1 + c2 * t2 + c3 * t3 - c4 * (-t4) * (-1)          # c4 enters K with a minus: -c4 J^2
    K = c1 * t1 + c2 * t2 + c3 * t3 + c4 * t4
    return -K / (16 * sp.pi * G)

rho = sp.Function('rho')(t, z)
T = sp.zeros(4, 4); vv = [1, vx, 0, vz]
for a in range(4):
    for b in range(4):
        T[a, b] = rho * vv[a] * vv[b]
L_src = sum(h[a, b] * T[a, b] for a in range(4) for b in range(4)) / 2


# ---- AeST scalar sector, built perturbatively to O(e^2) ----
e = sp.Symbol('e')
gm = eta + e * h
gi = eta - e * (eta * h * eta) + e**2 * (eta * h * eta * h * eta)
a1, a2 = sp.symbols('a1 a2')
uv = [1 + e * a1 + e**2 * a2, e * UX, 0, e * UZ]
norm = sp.expand(sum(gm[m, n] * uv[m] * uv[n] for m in range(4) for n in range(4)) + 1)
sa1 = sp.solve(norm.coeff(e, 1), a1)[0]
sa2 = sp.solve(norm.coeff(e, 2).subs(a1, sa1), a2)[0]
uv = [sp.expand(u.subs(a1, sa1).subs(a2, sa2)) if not isinstance(u, int) else u for u in uv]
dphi = [(Q0 + qb) + e * sp.diff(P, t), 0, 0, e * sp.diff(P, z)]   # background Qbar = Q0 + qbar (off the minimum)
def dd(f, a): return sp.diff(f, X[a])
Gam2 = [[[sp.expand(sum(gi[m, n] * (dd(gm[n, a], b) + dd(gm[n, b], a) - dd(gm[a, b], n)) for n in range(4)) / 2)
          for b in range(4)] for a in range(4)] for m in range(4)]
Jv = [sp.expand(sum(uv[a] * (dd(uv[m], a) + sum(Gam2[m][a][b] * uv[b] for b in range(4))) for a in range(4))) for m in range(4)]
def trunc(f, n=2): return sp.expand(sp.series(sp.expand(f), e, 0, n + 1).removeO())
Yq = trunc(sum((gi[m, n] + uv[m] * uv[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
Qq = trunc(sum(uv[m] * dphi[m] for m in range(4)), 2)
Jphi = trunc(sum(Jv[m] * dphi[m] for m in range(4)))
#print("check", sp.simplify(Yq.coeff(e, 0)), sp.simplify(Yq.coeff(e, 1)), sp.simplify(Jphi.coeff(e, 0)), sp.simplify(Jphi.coeff(e, 1)))
dQ = Qq - Q0
L_phi = (2 * (2 - KB) * Jphi.coeff(e, 2) - (2 - KB) * (1 + lam) * Yq.coeff(e, 2) + 2 * K2 * sp.expand(trunc(dQ**2)).coeff(e, 2)) / (16 * sp.pi * G)

L = sp.expand(L_EH() + L_ae() + L_src + L_phi)
fields = list(F.values()) + [UX, UZ, P]
eqs = sp.calculus.euler.euler_equations(L, fields, [t, z])

ph = sp.exp(sp.I * (k * z - w * t))
amp = {f: sp.Symbol('A_' + str(f.func)) for f in fields}
sub = {f: amp[f] * ph for f in fields}; sub[rho] = R * ph
alg = []
for e in eqs:
    ex = e.lhs.subs(sub).doit()
    alg.append(sp.simplify(sp.expand(ex / ph)))

unk=list(amp.values())
M=sp.Matrix([[sp.diff(a.subs(R,0),u) for u in unk] for a in alg])
det=sp.factor(sp.simplify(M.det(method='berkowitz')))
print("det (offset) =", det)
open("AEST_DISPERSION_OFFSET.txt","w").write(str(det))
