#!/usr/bin/env python3
"""Exact check of D3 note 7 §34: on the 'dragged' configuration A_mu = -d_mu phi / Q0 with |grad phi| = Q0, the AeST
contributions to ALL field equations vanish, so the metric can be exactly GR.

Test case: Schwarzschild in Painleve-Gullstrand form, ds^2 = -dT^2 + (dr + v dT)^2 + r^2 dOmega^2, v = sqrt(2M/r).
Free-fall observers have u_mu = -d_mu T, so phi = Q0*T gives A_mu = (-1,0,0,0), N = Q0, and a NONZERO expansion
theta = -(3/2) sqrt(2M/r^3). That makes it a sharp test of the theta-term cancellation.
Method: spherically symmetric ansatz with free functions, g = [[-f,h,0,0],[h,k,0,0],[0,0,s,0],[0,0,0,s sin^2]],
A_mu = (At, Ar, 0, 0), phi(t,r), lam(t,r). Euler-Lagrange equations of sqrt(-g) L_AeST (symmetric criticality;
the Einstein-Hilbert part vanishes on Schwarzschild), evaluated on the PG configuration.
L_AeST = -(K_B/2) F^2 + 2(2-K_B) J.dphi - (2-K_B) Y - F(Y,Q) - lam (A^2+1),  F(Y,Q) = cY*Y - 2*K2*(Q - Q1)^2."""
import sympy as sp
t, r, th, ph_ = sp.symbols('t r theta varphi', real=True)
X = [t, r, th, ph_]
KB, cY, K2, Q0, Q1, M = sp.symbols('K_B c_Y K_2 Q_0 Q_1 M', positive=True)
f, h, k, s = [sp.Function(n)(t, r) for n in ('f', 'h', 'k', 's')]
At, Ar, phi, lam = [sp.Function(n)(t, r) for n in ('A_t', 'A_r', 'phi', 'lam')]
g = sp.Matrix([[-f, h, 0, 0], [h, k, 0, 0], [0, 0, s, 0], [0, 0, 0, s*sp.sin(th)**2]])
gi = g.inv(); sqrtg = sp.sqrt(f*k + h**2) * s * sp.sin(th)
A_lo = [At, Ar, 0, 0]
A_up = [sp.simplify(sum(gi[m, n]*A_lo[n] for n in range(4))) for m in range(4)]
dphi = [sp.diff(phi, x) for x in X]
def d(e, a): return sp.diff(e, X[a])
Gam = [[[sp.simplify(sum(gi[m, n]*(d(g[n, a], b) + d(g[n, b], a) - d(g[a, b], n)) for n in range(4))/2)
         for b in range(4)] for a in range(4)] for m in range(4)]
F_lo = sp.Matrix(4, 4, lambda a, b: d(A_lo[b], a) - d(A_lo[a], b))
F2 = sum(F_lo[a, b]*F_lo[c, e]*gi[a, c]*gi[b, e] for a in range(4) for b in range(4) for c in range(4) for e in range(4))
covA = lambda nu, mu: d(A_up[mu], nu) + sum(Gam[mu][nu][rho]*A_up[rho] for rho in range(4))   # nabla_nu A^mu
J_up = [sum(A_up[nu]*covA(nu, mu) for nu in range(4)) for mu in range(4)]
Jdphi = sum(J_up[mu]*dphi[mu] for mu in range(4))
Q = sum(A_up[mu]*dphi[mu] for mu in range(4))
Y = sum((gi[m, n] + A_up[m]*A_up[n])*dphi[m]*dphi[n] for m in range(4) for n in range(4))
A2 = sum(A_up[mu]*A_lo[mu] for mu in range(4))
Fcal = cY*Y - 2*K2*(Q - Q1)**2
L = sqrtg*(-(KB/2)*F2 + 2*(2 - KB)*Jdphi - (2 - KB)*Y - Fcal - lam*(A2 + 1))
L2 = sp.simplify(L / sp.sin(th))
assert not L2.has(th), "theta dependence did not factor"
fields = [f, h, k, s, At, Ar, phi, lam]
eqs = sp.calculus.euler.euler_equations(L2, fields, [t, r])
v = sp.sqrt(2*M/r); T = t
cfg = {f: 1 - v**2, h: v, k: sp.Integer(1), s: r**2, At: sp.Integer(-1), Ar: sp.Integer(0), phi: Q0*T}
def on_cfg(e, lamval):
    e = e.lhs.subs(lam, lamval).subs(cfg).doit()
    return sp.simplify(e)
# lam from the A_t equation on the configuration, then check every equation
names = ['E_f (g_tt)', 'E_h (g_tr)', 'E_k (g_rr)', 'E_s (areal)', 'E_At', 'E_Ar', 'E_phi', 'E_lam (constraint)']
lam_s = sp.Function('lam')(t, r)
eAt = eqs[4].lhs.subs(cfg).doit()
lam_sol = sp.solve(sp.simplify(eAt), lam_s)
print("lambda from the A_t equation:", [sp.simplify(x) for x in lam_sol])
lv = lam_sol[0] if lam_sol else lam_s
for Q1v, tag in ((Q0, "F_Q(Q0) = 0 (condensate at its minimum)"), (Q0*sp.Rational(11, 10), "F_Q(Q0) != 0 (Q1 = 1.1 Q0)")):
    print(f"\n--- {tag} ---")
    for nm, e in zip(names, eqs):
        res = sp.simplify(e.lhs.subs(lam_s, lv).subs(cfg).doit().subs(Q1, Q1v))
        print(f"  {nm:22s} residual = {res}")
