#!/usr/bin/env python3
"""Exact check of the zero-mode 'lift' in a static weak-field background.
Zero mode = re-slicing of aether + scalar: T = t - eps*Lambda(x), u_mu = -N d_mu T (unit, hypersurface
orthogonal), phi = Q0*T + g*vphi(x). Metric (static background, not re-sliced):
g00 = -(1+2g Psi), gij = (1-2g Phi) delta_ij. Full AeST Lagrangian (tracking J = lambda_s Y, Q-sector 2K2 dQ^2):
  L = sqrt(-g)[ -(K_B/2) F^2 + 2(2-K_B) J^mu d_mu phi - (2-K_B)(1+lambda_s) Y + 2 K2 (Q-Q0)^2 ]
Expand: O(eps^2 g^0) (kinetic, time-dependent Lambda) and O(eps^2 g^1) (static lift), then compare
Euler-Lagrange expressions in vacuum (Laplacians of Psi, Phi, vphi set to zero) with the predicted
    L_kin  = K_B |grad dLambda/dt|^2 + 2 K2 Q0^2 (dLambda/dt)^2
    L_lift = 2 K2 Q0^2 Psi |grad Lambda|^2 ."""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
eps, gb = sp.symbols('epsilon g')
KB, lam, K2, Q0 = sp.symbols('K_B lambda_s K_2 Q_0', positive=True)
Psi, Phi, vphi = [sp.Function(n)(x, y, z) for n in ('Psi', 'Phi', 'vphi')]

def build(Lam):
    gm = sp.diag(-(1 + 2 * gb * Psi), 1 - 2 * gb * Phi, 1 - 2 * gb * Phi, 1 - 2 * gb * Phi)
    gi = sp.diag(*[1 / gm[i, i] for i in range(4)])
    T = t - eps * Lam
    dT = [sp.diff(T, v) for v in X]
    N = 1 / sp.sqrt(-sum(gi[m, m] * dT[m] ** 2 for m in range(4)))
    ul = [-N * dT[m] for m in range(4)]
    uu = [gi[m, m] * ul[m] for m in range(4)]
    phi = Q0 * T + gb * vphi
    dphi = [sp.diff(phi, v) for v in X]
    Fm = [[sp.diff(ul[n], X[m]) - sp.diff(ul[m], X[n]) for n in range(4)] for m in range(4)]
    F2 = sum(gi[m, m] * gi[n, n] * Fm[m][n] ** 2 for m in range(4) for n in range(4))
    Gam = lambda l, a, b: gi[l, l] * (sp.diff(gm[l, a], X[b]) + sp.diff(gm[l, b], X[a]) - sp.diff(gm[a, b], X[l])) / 2
    Jl = [sum(uu[a] * (sp.diff(ul[n], X[a]) - sum(Gam(l, a, n) * ul[l] for l in range(4))) for a in range(4)) for n in range(4)]
    Jdphi = sum(gi[m, m] * Jl[m] * dphi[m] for m in range(4))
    Y = sum(gi[m, m] * dphi[m] ** 2 for m in range(4)) + sum(uu[m] * dphi[m] for m in range(4)) ** 2
    Q = sum(uu[m] * dphi[m] for m in range(4))
    sqg = sp.sqrt((1 + 2 * gb * Psi) * (1 - 2 * gb * Phi) ** 3)
    return sqg * (-(KB / 2) * F2 + 2 * (2 - KB) * Jdphi - (2 - KB) * (1 + lam) * Y + 2 * K2 * (Q - Q0) ** 2)

def coeff(L, ne, ng):
    d = sp.diff(L, eps, ne)
    if ng: d = sp.diff(d, gb, ng)
    return sp.simplify(d.subs({eps: 0, gb: 0}) / (sp.factorial(ne) * sp.factorial(ng)))

def vac(expr):
    """Impose vacuum: reduce any derivative with z-order >= 2 of Psi, Phi, vphi using the Laplacian = 0."""
    def red(e):
        if isinstance(e, sp.Derivative) and e.expr in (Psi, Phi, vphi):
            orders = {v: 0 for v in (x, y, z)}
            for v, n in e.variable_count: orders[v] += n
            if orders[z] >= 2:
                f = e.expr
                a, b, c = orders[x], orders[y], orders[z]
                mk = lambda a_, b_, c_: sp.Derivative(f, *([(x, a_)] if a_ else []), *([(y, b_)] if b_ else []), *([(z, c_)] if c_ else [])) if (a_ + b_ + c_) else f
                return -mk(a + 2, b, c - 2) - mk(a, b + 2, c - 2)
        return None
    for _ in range(6):
        new = expr.replace(lambda e: isinstance(e, sp.Derivative) and e.expr in (Psi, Phi, vphi) and dict(e.variable_count).get(z, 0) >= 2,
                           lambda e: red(e))
        new = sp.expand(new.doit())
        if new == expr: break
        expr = new
    return sp.expand(expr)

def EL(L, f):
    r = sp.calculus.euler.euler_equations(L, [f], X if f.args == (t, x, y, z) else [x, y, z])
    return sp.expand(r[0].lhs) if r else sp.Integer(0)

# kinetic check: time-dependent Lambda, flat background
LamT = sp.Function('Lam')(t, x, y, z)
L20 = coeff(build(LamT), 2, 0)
print("L20 (time-dependent, flat) =", sp.simplify(L20))
pred_kin = KB * sum(sp.diff(LamT, t, v) ** 2 for v in (x, y, z)) + 2 * K2 * Q0 ** 2 * sp.diff(LamT, t) ** 2
print("kinetic: EL(L20) - EL(pred) =", sp.simplify(EL(L20, LamT) - EL(pred_kin, LamT)))
# static lift check
LamS = sp.Function('Lam')(x, y, z)
L21 = coeff(build(LamS), 2, 1)
L20s = coeff(build(LamS), 2, 0)
print("static O(eps^2 g^0) (must be 0 up to total derivative): EL =", sp.simplify(EL(L20s, LamS)))
pred_lift = 2 * K2 * Q0 ** 2 * Psi * sum(sp.diff(LamS, v) ** 2 for v in (x, y, z))
d = vac(EL(L21, LamS) - EL(pred_lift, LamS))
print("static lift: vacuum EL(L21) - EL(2K2 Q0^2 Psi |grad Lam|^2) =", sp.simplify(d))
