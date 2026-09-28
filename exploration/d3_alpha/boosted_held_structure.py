#!/usr/bin/env python3
"""Structure of the O(v) along-wind aether residual for a GENERAL local field (not the point-mass form):
vphi = gx x + gz z + (1/2)(Hxx x^2 + Hyy y^2 + Hzz z^2 + 2 Hxz x z), Phihat likewise (hatted). Wind along -z.
Question: is R[uz] an exact along-wind derivative v d_z(X) (only d_z g_z-type components), or does it also carry the
trace (the phantom density lap(vphi)) and transverse Hessians?  Aether rows only (fY'' does not enter E_A)."""
import sys, sympy as sp
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
KB, K2, Q0, v, eps, lam, fY1 = sp.symbols('K_B K_2 Q_0 v epsilon lam fY1', real=True)
gx, gz, Hxx, Hyy, Hzz, Hxz = sp.symbols('g_x g_z H_xx H_yy H_zz H_xz', real=True)
hx, hz, Kxx, Kyy, Kzz, Kxz = sp.symbols('ghat_x ghat_z Hhat_xx Hhat_yy Hhat_zz Hhat_xz', real=True)
s = sp.Symbol('s'); eta = sp.Function('eta')(t, x, y, z); esym = sp.symbols('e_t e_x e_y e_z'); e0 = sp.Symbol('e_0')
vphi = eps * (gx * x + gz * z + (Hxx * x**2 + Hyy * y**2 + Hzz * z**2 + 2 * Hxz * x * z) / 2)
Phi = eps * (hx * x + hz * z + (Kxx * x**2 + Kyy * y**2 + Kzz * z**2 + 2 * Kxz * x * z) / 2) + vphi
gam = 1 + v**2 / 2 + 3 * v**4 / 8
Gm = sp.diag(-(1 + 2 * Phi), 1 - 2 * Phi, 1 - 2 * Phi, 1 - 2 * Phi); Gi = sp.diag(-(1 - 2 * Phi), 1 + 2 * Phi, 1 + 2 * Phi, 1 + 2 * Phi)
sqG = 1 - 2 * Phi; Nn = gam * (1 - gam**2 * (1 + v**2) * Phi)
Acfg = [-(1 + 2 * Phi) * Nn, 0, 0, -(1 - 2 * Phi) * v * Nn]; phicfg = Q0 * gam * (t + v * z) + vphi
d = lambda f, a: sp.diff(f, X[a])
def L_of(A):
    Aup = [sum(Gi[m, k_] * A[k_] for k_ in range(4)) for m in range(4)]
    F = [[d(A[b], a) - d(A[a], b) for b in range(4)] for a in range(4)]
    F2t = sum(F[a][b] * F[c][dd] * Gi[a, c] * Gi[b, dd] for a in range(4) for b in range(4) for c in range(4) for dd in range(4) if F[a][b] != 0 and F[c][dd] != 0)
    Gam = [[[sum(Gi[m, k_] * (d(Gm[k_, a], b) + d(Gm[k_, b], a) - d(Gm[a, b], k_)) for k_ in range(4)) / 2 for b in range(4)] for a in range(4)] for m in range(4)]
    J = [sum(Aup[a] * (d(Aup[m], a) + sum(Gam[m][a][b] * Aup[b] for b in range(4))) for a in range(4)) for m in range(4)]
    dph = [d(phicfg, a) for a in range(4)]
    Q = sum(Aup[m] * dph[m] for m in range(4)); Y = sum(Gi[m, k_] * dph[m] * dph[k_] for m in range(4) for k_ in range(4)) + Q**2
    A2 = sum(Aup[m] * A[m] for m in range(4))
    return sqG * (-(KB / 2) * F2t + 2 * (2 - KB) * sum(J[m] * dph[m] for m in range(4)) - (2 - KB) * Y - fY1 * Y + 2 * K2 * (Q - Q0)**2 - lam * (A2 + 1))
def EL(i):
    A = list(Acfg); A[i] = A[i] + s * eta
    L1 = sp.diff(L_of(A), s).subs(s, 0).doit()
    L1 = L1.subs({sp.Derivative(eta, X[m]): esym[m] for m in range(4)}).subs(eta, e0)
    E = sp.diff(L1, e0) - sum(sp.diff(sp.diff(L1, esym[m]), X[m]) for m in range(4))
    return sp.expand(E.subs({x: 0, y: 0, z: 0}))
def coeffs(E):   # O(eps) and v-polynomial to v^1
    E = sp.expand(E); c1 = E.coeff(eps, 1)
    return [sp.expand(c1).coeff(v, i) for i in range(2)], E.coeff(eps, 0)
NUM = {Q0: sp.Rational(1, 10)}
EA0 = EL(0).subs(NUM); EAz = EL(3).subs(NUM)
# lambda = L0 + eps*L1 from E_A0 (linear in lambda), to O(v)
c0, c1 = sp.expand(EA0).coeff(eps, 0), sp.expand(EA0).coeff(eps, 1)
L0 = sp.solve(c0, lam)[0]; L1 = sp.solve(sp.expand(c1.subs(lam, L0) + sp.diff(c0, lam) * sp.Symbol('LL')), sp.Symbol('LL'))[0]
Ez = sp.expand(EAz.subs(lam, L0 + eps * L1))
Ez1 = sp.expand(sp.series(sp.expand(Ez).coeff(eps, 1), v, 0, 2).removeO())
print("O(eps^0) of E_Az:", sp.simplify(sp.expand(Ez).coeff(eps, 0)))
print("E_Az, O(eps v^0):", sp.factor(Ez1.coeff(v, 0)))
Ov = sp.collect(sp.expand(Ez1.coeff(v, 1)), [Hxx, Hyy, Hzz, Hxz, Kxx, Kyy, Kzz, Kxz])
print("E_Az, O(eps v^1):", Ov)
for sym in [Hxx, Hyy, Hzz, Hxz, Kxx, Kyy, Kzz, Kxz]:
    print(f"   coefficient of {sym}: {sp.factor(sp.expand(Ez1.coeff(v, 1)).coeff(sym))}")
