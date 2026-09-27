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
KB, lam, K2, Q0, C2 = sp.symbols('K_B lambda_s K_2 Q_0 c_2', real=True)
c1, c2, c3, c4 = sp.symbols('c_1 c_2a c_3 c_4', real=True)   # free aether couplings (AeST+c2: K_B, c2, -K_B, 0)

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
dphi = [Q0 + e * sp.diff(P, t), 0, 0, e * sp.diff(P, z)]
def dd(f, a): return sp.diff(f, X[a])
Gam2 = [[[sp.expand(sum(gi[m, n] * (dd(gm[n, a], b) + dd(gm[n, b], a) - dd(gm[a, b], n)) for n in range(4)) / 2)
          for b in range(4)] for a in range(4)] for m in range(4)]
Jv = [sp.expand(sum(uv[a] * (dd(uv[m], a) + sum(Gam2[m][a][b] * uv[b] for b in range(4))) for a in range(4))) for m in range(4)]
def trunc(f, n=2): return sp.expand(sp.series(sp.expand(f), e, 0, n + 1).removeO())
Yq = trunc(sum((gi[m, n] + uv[m] * uv[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
Qq = trunc(sum(uv[m] * dphi[m] for m in range(4)), 1)
Jphi = trunc(sum(Jv[m] * dphi[m] for m in range(4)))
if False: print("check O(e^0), O(e^1) of Y, J.dphi (must vanish):", sp.simplify(Yq.coeff(e, 0)), sp.simplify(Yq.coeff(e, 1)), sp.simplify(Jphi.coeff(e, 0)), sp.simplify(Jphi.coeff(e, 1)))

import sys, mpmath as mp
mp.mp.dps = 50
SCALAR = True
dQ = Qq - Q0
L_phi = (2 * (2 - KB) * Jphi.coeff(e, 2) - (2 - KB) * (1 + lam) * Yq.coeff(e, 2) + 2 * K2 * sp.expand(dQ**2).coeff(e, 2)) / (16 * sp.pi * G)
def build(scalar):
    L = sp.expand(L_EH() + L_ae() + L_src + (L_phi if scalar else 0))
    fields = list(F.values()) + [UX, UZ] + ([P] if scalar else [])
    eqs = sp.calculus.euler.euler_equations(L, fields, [t, z])
    ph = sp.exp(sp.I * (k * z - w * t))
    amp = {f: sp.Symbol('A_' + str(f.func)) for f in fields}
    sub = {f: amp[f] * ph for f in fields}; sub[rho] = R * ph
    alg = [sp.expand(q.lhs.subs(sub).doit().subs({t: 0, z: 0})) for q in eqs]
    Mx, bx = sp.linear_eq_to_matrix(alg, list(amp.values()))
    pars = (k, w, vx, vz, R, G, c1, c2, c3, c4, KB, lam, K2, Q0)
    return list(amp.keys()), sp.lambdify(pars, Mx, 'mpmath'), sp.lambdify(pars, bx, 'mpmath')
def coeffs(fM, fb, a, b, cs, sc, h=mp.mpf('1e-6'), npt=3):
    """Taylor coefficients (orders 0..2) of each amplitude in eps, with vx = a eps, vz = b eps, omega = vz (k = 1)."""
    pts = [j * h for j in range(-npt, npt + 1)]
    vals = []
    for ep in pts:
        args = (1, b * ep, a * ep, b * ep, 1, 1 / (16 * mp.pi)) + tuple(cs) + tuple(sc)
        vals.append(mp.lu_solve(mp.matrix(fM(*args)), mp.matrix(fb(*args))))
    n = len(vals[0]); out = []
    V = mp.matrix([[p ** m for m in range(len(pts))] for p in pts])
    for i in range(n):
        c = mp.lu_solve(V, mp.matrix([v[i] for v in vals]))
        out.append([c[0], c[1], c[2]])
    return out
def alphas(names, fM, fb, cs, sc):
    ix = {str(nm.func): i for i, nm in enumerate(names)}
    X = coeffs(fM, fb, 1, 0, cs, sc); Z = coeffs(fM, fb, 0, 1, cs, sc)
    u0 = X[ix['h00']][0] / 2
    cxx, czz = X[ix['h00']][2], Z[ix['h00']][2]
    xiz = (X[ix['hxx']][0] - X[ix['hzz']][0]) / (2j)
    q = (czz - cxx) / (2j)
    A = X[ix['h0x']][1]
    h0zg = Z[ix['h0z']][1] + 1j * (-xiz + q)
    B = h0zg - A
    aW = -B / (2 * u0); aV = A / u0 - aW
    a2 = -2 * aW - 1; a1 = -2 * aV - 7 + a2
    return a1, a2, u0
def fj(c1v, c2v, c3v, c4v):
    c123, c14 = c1v + c2v + c3v, c1v + c4v
    a1 = -8 * (c3v**2 + c1v * c4v) / (2 * c1v - c1v**2 + c3v**2)
    a2 = a1 / 2 - (c1v + 2 * c3v - c4v) * (2 * c1v + 3 * c2v + c3v + c4v) / (c123 * (2 - c14))   # FJ 2006, as validated in ea_ppn_pipeline.py
    return a1, a2
nm0, fM0, fb0 = build(False)
print("VALIDATION (scalar off):", flush=True)
for cs in [(mp.mpf('0.3'), mp.mpf('0.2'), mp.mpf('-0.1'), mp.mpf('0.05')), (mp.mpf('0.1'), mp.mpf('0.4'), mp.mpf('0.02'), mp.mpf('-0.03')), (mp.mpf('0.01'), mp.mpf('0.02'), mp.mpf('-0.005'), mp.mpf('0.003'))]:
    a1, a2, u0 = alphas(nm0, fM0, fb0, cs, (0, 0, 0, 0))
    ref = fj(*cs)
    print(f"  c={tuple(float(c) for c in cs)}: alpha1={mp.nstr(mp.re(a1),10)} (FJ {float(ref[0]):.10g})  alpha2={mp.nstr(mp.re(a2),10)} (FJ {float(ref[1]):.10g})  |Im|={mp.nstr(abs(mp.im(a1))+abs(mp.im(a2)),3)}", flush=True)
nm1, fM1, fb1 = build(True)
print("AeST + c2 at Q0=0 (solar limit): numeric vs Foster-Jacobson with c4_eff=(2-K_B)/(1+lambda_s):", flush=True)
for KBv, lamv in ((mp.mpf('0.5'), mp.mpf(1)), (mp.mpf('0.25'), mp.mpf(2)), (mp.mpf('1.0'), mp.mpf('0.5'))):
    c4eff = (2 - KBv) / (1 + lamv)
    for C2v in (mp.mpf('1'), mp.mpf('0.1'), mp.mpf('0.01')):
        for K2x in (mp.mpf(0), mp.mpf(10), mp.mpf(75)):
            a1, a2, u0 = alphas(nm1, fM1, fb1, (KBv, C2v, -KBv, 0), (KBv, lamv, K2x, 0))
            r1, r2 = fj(KBv, C2v, -KBv, c4eff)
            print(f"  K_B={float(KBv):4g} lam={float(lamv):3g} c2={float(C2v):5g} K2={float(K2x):3g}: alpha1={mp.nstr(mp.re(a1),10):>14s} (FJ {float(r1):.8g})  "
                  f"alpha2={mp.nstr(mp.re(a2),10):>14s} (FJ {float(r2):.8g}; diff {mp.nstr(mp.re(a2)-r2,8)})  |Im|={mp.nstr(abs(mp.im(a1))+abs(mp.im(a2)),3)}", flush=True)
