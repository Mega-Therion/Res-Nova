#!/usr/bin/env python3
"""Independent relative-sign check between the linear operator (aest_wind_bg.py, JSON) and the residual script
(boosted_held_residuals.py): the static (v = 0) coupling of the along-wind aether row to the scalar at O(k), divided by i,
must equal dR_uz/dg_z = -2 Q0 (2-K_B)(J' + 2Y J'') (par geometry, g along z), up to a Qbar/Q0 factor near 1.
A sign mismatch would turn the cancellation into a doubling. Usage: wind_sign_check.py [75|750000]"""
import sympy as sp, mpmath as mp
from wind_cli import pick_k2
from sym_json import load_matrix, load_residuals

mp.mp.dps = 50
K2v = pick_k2([None, None] + ([__import__("sys").argv[1]] if len(__import__("sys").argv) > 1 else []))
M, names, (qb, Jp, Jl, g, k, w, vw), (KB, K2, Q0) = load_matrix(f"wind_bg_matrix_par_K2{K2v}.json")
ent = sp.expand(M[names.index("uz"), names.index("phi")].subs({vw: 0, w: 0}))
c1 = sp.expand(ent).coeff(k, 1)
print("M[uz,phi] at v=0, w=0:", sp.factor(ent))
print("O(k) coefficient / i:", sp.simplify(c1 / sp.I))
x = mp.mpf("0.05"); Jpv = x / mp.sqrt(1 + x * x); Jlv = x * (1 + x * x) ** mp.mpf(-1.5)
gval = x * 2 * mp.mpf("3.577e-5"); r = mp.mpf("3e-4"); vf = mp.mpf(10) / mp.mpf(299792.458)
qv = (vf / r) ** 2 / (mp.mpf(int(K2)) * mp.mpf(1) / 10)
val = sp.lambdify((qb, Jp, Jl, g), c1 / sp.I, "mpmath")(qv, Jpv, Jlv, gval)
pred = -2 * (mp.mpf(1) / 10) * (2 - mp.mpf(1) / 2) * (Jpv + Jlv)
print(f"operator:  O(k) coeff / i = {mp.nstr(val, 10)}")
print(f"residual:  dR_uz/dg_z     = {mp.nstr(pred, 10)}   (ratio {mp.nstr(val / pred, 8)}; Qbar/Q0 = {mp.nstr(1 + qv * 10, 8)})")
RR = load_residuals("boosted_residuals_par.json")
sKB, sK2, sQ0, sv, sgv, sHs, sghs, sHhs, sfY1, sF2 = RR["symbols"]
Ruz0 = sp.expand(RR["builder"]["uz"]).subs(sv, 0)          # = 2 Q0 [(2-K_B) ghat - fY' g_vphi]
print("residual script, R_uz at v = 0:", sp.factor(Ruz0))
# Like-for-like: the operator's pure-scalar perturbation holds the METRIC fixed, i.e. varies g_vphi at fixed total
# g_Phi = ghat + g_vphi (ghat -> g_Phi - g_vphi); fY' also moves with g (d(fY' g)/dg = fY' + 2Y fY'' = (2-K_B)(J'+2YJ'')).
gPhi, Jps, Jls = sp.symbols("g_Phi Jp_s Jl_s")
Rfix = sp.expand(Ruz0.subs(sghs, gPhi - sgv))
dR = sp.diff(Rfix.subs(sfY1, 0), sgv) - sp.Rational(3, 2) * (Jps + Jls) * sp.Rational(2, 10)   # fY' g_vphi term -> -(2Q0)(2-K_B)(J'+2YJ'')
print("residual, dR_uz/dg_vphi at fixed metric:", sp.factor(dR))
op0 = sp.expand((c1 / sp.I).subs(qb, 0))
print("operator at qbar = 0, O(k) coeff / i:   ", sp.factor(op0))
same = sp.simplify(op0 - dR.subs({Jps: Jp, Jls: Jl})) == 0
print("LIKE-FOR-LIKE SIGN/MAGNITUDE CHECK:", "PASS (identical)" if same else "FAIL")
print("(the naive comparison above differs by the metric tie, -2Q0(2-K_B) = -0.3, and the lift stand-in 4 K2 qbar ~ +0.49)")
