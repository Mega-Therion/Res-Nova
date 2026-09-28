#!/usr/bin/env python3
"""SUPERSEDED by boosted_held_residuals.py (TARGET_D7_SUPPLEMENT sec.7). This first pass froze the metric (no gravity
rows) and, by counting fY'' as higher order, dropped the fY'' terms (Y ~ eps^2 makes fY'' ~ eps^-2). Its "static truncation
artefact" in E_phi was that missing term. Its aether residuals agree with the new script term for term. Kept as history.

Decisive check (D7 drag dilemma): does the HELD (MOND) configuration survive an ambient aether wind?
Local test at a point P near a deep-MOND dwarf. The metric is fixed to weak field, g = diag(-(1+2Phi), (1-2Phi) I),
with Phi = Phihat + vphi (AeST's dual channel). Fields in the dwarf frame (stationary):
  phi = Q0*gam*(t + v z) + vphi(x)          boosted clock plus static MOND scalar
  A^mu = boosted unit vector, streaming along -z at speed v (normalized in the metric)
  lam = Lagrange multiplier (solved from the time component)
Around P the potentials are expanded to 2nd order: vphi = vphi0 + g.x + x.H.x/2 (deep-MOND point mass: H = (vf^2/r^2)
(I - 2nn)), Phihat likewise (Newtonian: Hhat = (GM/r^3)(I - 3nn)). Euler-Lagrange residuals of the aether and scalar
equations are evaluated at P as series in v.
L = sqrt(-g)[ -(K_B/2)F^2 + 2(2-K_B) J.dphi - (2-K_B) Y - fY(Y) + 2 K2 (Q - Q0)^2 - lam (A^2 + 1) ]."""
import sympy as sp
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
KB, K2, Q0, v, lamS = sp.symbols('K_B K_2 Q_0 v lambda', real=True)
Phi = sp.Function('Phi')(x, y, z)
A = [sp.Function(f'A{i}')(t, x, y, z) for i in range(4)]            # covariant components A_mu
phi = sp.Function('phi')(t, x, y, z); lam = sp.Function('lam')(t, x, y, z)
fY = sp.Function('fY')
g = sp.diag(-(1 + 2*Phi), 1 - 2*Phi, 1 - 2*Phi, 1 - 2*Phi); gi = sp.diag(*[1/g[i, i] for i in range(4)])
sqrtg = sp.sqrt((1 + 2*Phi)*(1 - 2*Phi)**3)
d = lambda f, a: sp.diff(f, X[a])
Gam = [[[sum(gi[m, n]*(d(g[n, a], b) + d(g[n, b], a) - d(g[a, b], n)) for n in range(4))/2 for b in range(4)] for a in range(4)] for m in range(4)]
Aup = [gi[m, m]*A[m] for m in range(4)]
F = [[d(A[b], a) - d(A[a], b) for b in range(4)] for a in range(4)]
F2 = sum(F[a][b]*F[a][b]*gi[a, a]*gi[b, b] for a in range(4) for b in range(4))
covA = lambda nu, mu: d(Aup[mu], nu) + sum(Gam[mu][nu][r]*Aup[r] for r in range(4))
J = [sum(Aup[nu]*covA(nu, mu) for nu in range(4)) for mu in range(4)]
dphi = [d(phi, a) for a in range(4)]
Jdphi = sum(J[m]*dphi[m] for m in range(4))
Q = sum(Aup[m]*dphi[m] for m in range(4))
Y = sum(gi[m, m]*dphi[m]**2 for m in range(4)) + Q**2
A2 = sum(Aup[m]*A[m] for m in range(4))
L = sqrtg*(-(KB/2)*F2 + 2*(2 - KB)*Jdphi - (2 - KB)*Y - fY(Y) + 2*K2*(Q - Q0)**2 - lam*(A2 + 1))
fields = A + [phi]
print("building Euler-Lagrange equations ...", flush=True)
eqs = sp.calculus.euler.euler_equations(L, fields, X)
print("done; substituting the configuration", flush=True)
# ---- configuration ----
gv, Hs, ghs, Hhs = sp.symbols('g_vphi H_vphi g_hat H_hat', real=True)
# local point P on a ray at angle: choose n along x (wind perpendicular to the radial direction) or along z (parallel)
import sys
case = sys.argv[1] if len(sys.argv) > 1 else "perp"
n = (1, 0, 0) if case == "perp" else (0, 0, 1)
xs = (x, y, z)
Hm = lambda s, c: sp.Matrix(3, 3, lambda i, j: s*((1 if i == j else 0) - c*n[i]*n[j]))
vphi = sum(gv*n[i]*xs[i] for i in range(3)) + sum(Hm(Hs, 2)[i, j]*xs[i]*xs[j] for i in range(3) for j in range(3))/2
Phihat = sum(ghs*n[i]*xs[i] for i in range(3)) + sum(Hm(Hhs, 3)[i, j]*xs[i]*xs[j] for i in range(3) for j in range(3))/2
Phic = Phihat + vphi
gam = 1/sp.sqrt(1 - v**2)
phic = Q0*gam*(t + v*z) + vphi
# aether streaming along -z: A^mu = N*(1, 0, 0, -v) normalized with the metric; covariant A_mu = g_mu mu A^mu
Nn = 1/sp.sqrt((1 + 2*Phic) - (1 - 2*Phic)*v**2)
Acov = [-(1 + 2*Phic)*Nn, 0, 0, -(1 - 2*Phic)*v*Nn]
cfg = {Phi: Phic, phi: phic}
for i in range(4): cfg[A[i]] = Acov[i]
eps = sp.Symbol('epsilon')   # weak-field bookkeeping: potentials ~ eps
def at_P(expr):
    e = expr.subs(cfg).doit()
    e = e.subs({x: 0, y: 0, z: 0})
    return e
names = ["E_A0", "E_Ax", "E_Ay", "E_Az", "E_phi"]
res = {}
for nm, e in zip(names, eqs):
    res[nm] = at_P(e.lhs)
# lambda from the time component at P
lam0 = sp.Symbol('lam0')
lamPt = lam.subs({x: 0, y: 0, z: 0})
for kk in res: res[kk] = res[kk].subs(lamPt, lam0)
lamP = sp.solve(sp.Eq(res["E_A0"], 0), lam0)
lamP = lamP[0] if lamP else lam0
print("lambda at P:", sp.simplify(sp.series(lamP, v, 0, 2).removeO()) if lamP != lam0 else "unsolved", flush=True)
for nm in names[1:]:
    r_ = res[nm].subs(lam0, lamP)
    # weak field: potentials small -> keep leading order in the potential amplitudes (scale gv,Hs,ghs,Hhs by eps)
    r_ = r_.subs({gv: eps*gv, Hs: eps*Hs, ghs: eps*ghs, Hhs: eps*Hhs})
    r_ = sp.series(r_, eps, 0, 2).removeO()
    r_ = sp.series(r_, v, 0, 3).removeO()
    print(f"{nm}: {sp.simplify(sp.expand(r_))}", flush=True)
