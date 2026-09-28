#!/usr/bin/env python3
"""D7 decisive check, step 1 redone: every Euler-Lagrange residual of the boosted-held configuration at a point P
near a deep-MOND dwarf, INCLUDING the metric rows, mapped into the field basis of the linear builder
(aest_wind_bg.py: h00,h0x,h0z,hxx,hyy,hzz,hxz covariant metric perturbations; contravariant aether u^x,u^z with u^0
fixed by normalization; scalar).

Differences from boosted_held_check.py (which froze the metric and dropped fY'' terms):
  * metric rows computed: R[h_ab] = dS/dg_ab |_(A_mu fixed) + E_A . dA/dh_ab |_(u fixed)   (A_mu = g_mu nu u^nu)
  * MOND free function handled with the right weak-field counting: Y ~ eps^2, fY' = O(1), fY'' = F2/eps^2
  * each row computed by first variation along a single test function (fast)
Configuration (dwarf frame, stationary): metric diag(-(1+2Phi),(1-2Phi)I), Phi = Phihat + vphi,
  vphi = g n.x + (H/2) x.(I-2nn).x (deep-MOND point mass), Phihat = ghat n.x + (Hhat/2) x.(I-3nn).x (Newtonian),
  phi = Q0 gam (t + v z) + vphi, A^mu = N(1,0,0,-v) normalized, lambda at P solved from E_A0 = 0.
Output: series in eps (O(eps)) and v (to v^2) for each builder row; pickle for the solver.
"""

import sys, pickle, time, sympy as sp
from wind_cli import pick_dir

case = pick_dir()   # allowlisted: par | perp
t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
KB, K2, Q0, v, eps, lam = sp.symbols("K_B K_2 Q_0 v epsilon lam", real=True)
gv, Hs, ghs, Hhs, fY1, F2 = sp.symbols("g_vphi H_vphi g_hat H_hat fY1 F2", real=True)
s = sp.Symbol("s")
eta = sp.Function("eta")(t, x, y, z)
esym = sp.symbols("e_t e_x e_y e_z")
e0 = sp.Symbol("e_0")
n = (1, 0, 0) if case == "perp" else (0, 0, 1)
xs = (x, y, z)
quad = lambda gr, H, c: gr * sum(n[i] * xs[i] for i in range(3)) + sp.Rational(
    1, 2
) * H * sum(
    ((1 if i == j else 0) - c * n[i] * n[j]) * xs[i] * xs[j]
    for i in range(3)
    for j in range(3)
)
vphi = eps * quad(gv, Hs, 2)
Phi = eps * quad(ghs, Hhs, 3) + vphi
# gamma as a polynomial in v (to v^4): keeps every cancellation exact under expand; the symbolic
# 1/sqrt(1-v^2) left zeros-in-disguise (gam^2(1-v^2)-1) that the fY''=F2/eps^2 terms amplified into spurious 1/eps pieces
gam = 1 + v**2 / 2 + 3 * v**4 / 8
# configuration, consistently to O(eps)
Gm = sp.diag(-(1 + 2 * Phi), 1 - 2 * Phi, 1 - 2 * Phi, 1 - 2 * Phi)
Gi = sp.diag(-(1 - 2 * Phi), 1 + 2 * Phi, 1 + 2 * Phi, 1 + 2 * Phi)
sqG = 1 - 2 * Phi
Nn = gam * (1 - gam**2 * (1 + v**2) * Phi)
Acfg = [-(1 + 2 * Phi) * Nn, 0, 0, -(1 - 2 * Phi) * v * Nn]
phicfg = Q0 * gam * (t + v * z) + vphi
d = lambda f, a: sp.diff(f, X[a])


def lagrangian(gm, gi, sq, A, ph, YP):
    Aup = [sum(gi[m, k_] * A[k_] for k_ in range(4)) for m in range(4)]
    F = [[d(A[b], a) - d(A[a], b) for b in range(4)] for a in range(4)]
    F2t = sum(
        F[a][b] * F[c][dd] * gi[a, c] * gi[b, dd]
        for a in range(4)
        for b in range(4)
        for c in range(4)
        for dd in range(4)
        if F[a][b] != 0 and F[c][dd] != 0
    )
    Gam = [
        [
            [
                sum(
                    gi[m, k_] * (d(gm[k_, a], b) + d(gm[k_, b], a) - d(gm[a, b], k_))
                    for k_ in range(4)
                )
                / 2
                for b in range(4)
            ]
            for a in range(4)
        ]
        for m in range(4)
    ]
    J = [
        sum(
            Aup[a] * (d(Aup[m], a) + sum(Gam[m][a][b] * Aup[b] for b in range(4)))
            for a in range(4)
        )
        for m in range(4)
    ]
    dph = [d(ph, a) for a in range(4)]
    Jd = sum(J[m] * dph[m] for m in range(4))
    Q = sum(Aup[m] * dph[m] for m in range(4))
    Y = sum(gi[m, k_] * dph[m] * dph[k_] for m in range(4) for k_ in range(4)) + Q**2
    A2 = sum(Aup[m] * A[m] for m in range(4))
    fYexpr = fY1 * (Y - YP) + F2 / (2 * eps**2) * (Y - YP) ** 2
    return sq * (
        -(KB / 2) * F2t
        + 2 * (2 - KB) * Jd
        - (2 - KB) * Y
        - fYexpr
        + 2 * K2 * (Q - Q0) ** 2
        - lam * (A2 + 1)
    )


# Y at P for the configuration (defines the expansion point of the free function)
_Aup = [sum(Gi[m, k_] * Acfg[k_] for k_ in range(4)) for m in range(4)]
_dph = [d(phicfg, a) for a in range(4)]
_Q = sum(_Aup[m] * _dph[m] for m in range(4))
YPexpr = sp.expand(
    (
        sum(Gi[m, k_] * _dph[m] * _dph[k_] for m in range(4) for k_ in range(4)) + _Q**2
    ).subs({x: 0, y: 0, z: 0})
)
YP = sp.Symbol("Y_P")


def at_P_EL(Lpert):
    L1 = sp.diff(Lpert, s).subs(s, 0).doit()
    L1 = L1.subs({sp.Derivative(eta, X[m]): esym[m] for m in range(4)}).subs(eta, e0)
    a = sp.diff(L1, e0)
    E = a - sum(sp.diff(sp.diff(L1, esym[m]), X[m]) for m in range(4))
    return E.subs({x: 0, y: 0, z: 0})


rows = {}
t0 = time.time()
# aether rows (covariant A_mu varied, metric and phi fixed)
for i, nm in [(0, "A0"), (1, "Ax"), (3, "Az")]:
    A = list(Acfg)
    A[i] = A[i] + s * eta
    rows[nm] = at_P_EL(lagrangian(Gm, Gi, sqG, A, phicfg, YP))
    print(nm, f"{time.time()-t0:.0f}s", flush=True)
rows["phi"] = at_P_EL(lagrangian(Gm, Gi, sqG, Acfg, phicfg + s * eta, YP))
print("phi", f"{time.time()-t0:.0f}s", flush=True)
# metric rows at fixed covariant A_mu
mnames = {
    (0, 0): "h00",
    (0, 1): "h0x",
    (0, 3): "h0z",
    (1, 1): "hxx",
    (2, 2): "hyy",
    (3, 3): "hzz",
    (1, 3): "hxz",
}
for (a_, b_), nm in mnames.items():
    Em = sp.zeros(4, 4)
    Em[a_, b_] = 1
    Em[b_, a_] = 1
    gm = Gm + s * eta * Em
    gi = Gi - s * eta * (Gi * Em * Gi)
    sq = sqG * (1 + s * eta * sum((Gi * Em)[i, i] for i in range(4)) / 2)
    rows[nm] = at_P_EL(lagrangian(gm, gi, sq, Acfg, phicfg, YP))
    print(nm, f"{time.time()-t0:.0f}s", flush=True)


KBSYM = len(sys.argv) > 2 and sys.argv[2] == "kbsym"   # keep K_B symbolic (slower; for the K_B-dependence)
NUM = {Q0: sp.Rational(1, 10)} if KBSYM else {KB: sp.Rational(1, 2), Q0: sp.Rational(1, 10)}   # K2 kept symbolic

VORD = 3   # keep v^0..v^3 (config is exact to v^4, so these are exact)

def trunc_v(ex, nmax=VORD):
    ex = sp.expand(ex)
    return sum(ex.coeff(v, i) * v**i for i in range(nmax + 1))

def eps_coeffs(expr):
    """O(eps^0) and O(eps^1) coefficients (polynomial in v, to v^3). fY'' = F2/eps^2 makes eps^2*E polynomial in eps;
    any surviving eps^0 or eps^1 term in eps^2*E would be a genuine inconsistency and is reported."""
    ex = sp.expand(sp.expand(expr.subs(YP, YPexpr).subs(NUM)) * eps**2)
    bad = trunc_v(ex.coeff(eps, 0) + ex.coeff(eps, 1))
    if bad != 0: print("   WARNING: negative powers of eps survive:", bad, flush=True)
    return trunc_v(ex.coeff(eps, 2)), trunc_v(ex.coeff(eps, 3))

# lambda at P from E_A0 = 0 (E_A0 is linear in lambda), exact in v
c0, c1 = eps_coeffs(rows["A0"])
al0, be0 = c0.subs(lam, 0), sp.diff(c0, lam); al1, be1 = c1.subs(lam, 0), sp.diff(c1, lam)
L0 = trunc_v(sp.series(sp.simplify(-al0 / be0), v, 0, VORD + 1).removeO())
L1 = trunc_v(sp.series(sp.simplify(-(al1 + be1 * L0) / be0), v, 0, VORD + 1).removeO())
print("lambda_P: O(1) =", L0, "; O(eps) =", sp.simplify(L1), flush=True)
res = {}
for nm, ex in rows.items():
    r0, r1 = eps_coeffs(ex)
    # lambda = L0 + eps*L1: O(1) gets L0; O(eps) gets L0 in r1 and L1 through d r0/d lambda
    R0 = sp.simplify(trunc_v(r0.subs(lam, L0))); R1 = trunc_v(r1.subs(lam, L0) + sp.diff(r0, lam) * L1)
    res[nm] = (R0, R1); print("  row", nm, f"{time.time()-t0:.0f}s", flush=True)
u0, uz = gam, -v * gam
chain = {'h00': 0, 'h0x': res["Ax"][1] * u0, 'h0z': res["Az"][1] * u0, 'hxx': 0, 'hyy': 0,
         'hzz': res["Az"][1] * uz, 'hxz': res["Ax"][1] * uz}
builder = {nm: trunc_v(res[nm][1] + chain[nm]) for nm in mnames.values()}
builder['ux'] = res["Ax"][1]; builder['uz'] = res["Az"][1]; builder['phi'] = res["phi"][1]
print(f"\n=== {case}: O(eps^0) parts (aether/scalar must vanish; metric rows = uniform condensate stress, dropped) ===")
for nm in res: print(f"  {nm}: {res[nm][0]}")
print(f"\n=== {case}: O(eps) residuals in the builder basis, K_B = 1/2, Q0 = 1/10, series to v^2 (exact-in-v forms pickled) ===")
for nm, ex in builder.items():
    sr = trunc_v(ex, 2)
    print(f"  R[{nm}] = {sp.collect(sr, v) if sr != 0 else 0}", flush=True)
pickle.dump({'case': case, 'builder': builder, 'raw': res, 'lamP': (L0, L1), 'num': NUM,
             'symbols': (KB, K2, Q0, v, gv, Hs, ghs, Hhs, fY1, F2)}, open(f"boosted_residuals_{case}{'_kbsym' if KBSYM else ''}.pkl", "wb"))
print(f"done {time.time()-t0:.0f}s")
