#!/usr/bin/env python3
"""D7 Stage 2: the static (v = 0) content of the axisymmetric Lagrangian, restricted to the Newtonian-gauge ansatz
h00 = -2 Psi, h_ij = -2 Psi delta_ij (Psi = Phi, which satisfies de Donder), h0i = 0 and u = 0. This reads off the
Poisson and scalar equations the full solver must reproduce at v = 0, and the u-equation's source at u = 0 (the AeST
alignment constraint)."""
import json, sys, sympy as sp
sys.path.insert(0, "../d3_alpha")
from sym_json import dec
d = json.load(open("steady_lagrangian_axisym.json"))
L, Y = dec(d["Lrest"]), dec(d["Y"])
vw = sp.Symbol("v_w", real=True); R = sp.Symbol("R", positive=True)
Ps, PsR, Psz, F_, FR, Fz = sp.symbols("Psi Psi_R Psi_z F F_R F_z", real=True)
UR, URR, URz, Uz, UzR, Uzz = sp.symbols("U_R U_R_R U_R_z U_z U_z_R U_z_z", real=True)
def s(n): return sp.Symbol(n)
rep = {s("S"): -2 * Ps, s("S_R"): -2 * PsR, s("S_z"): -2 * Psz, s("A"): -2 * Ps, s("A_R"): -2 * PsR, s("A_z"): -2 * Psz}
for n in ("W_R", "W_z", "B", "C", "D"):
    for suf in ("", "_R", "_z"): rep[s(n + suf)] = 0
for n in ("U_R", "U_z"):
    for suf in ("", "_R", "_z"): rep[s(n + suf)] = sp.Symbol(n + suf, real=True)
rep[s("F")] = F_; rep[s("F_R")] = FR; rep[s("F_z")] = Fz
Ls = sp.expand(L.xreplace(rep).subs(vw, 0)); Ys = sp.expand(Y.xreplace(rep).subs(vw, 0))
U0 = {sp.Symbol(n + suf, real=True): 0 for n in ("U_R", "U_z") for suf in ("", "_R", "_z")}
L0 = sp.expand(Ls.subs(U0)); Y0 = sp.expand(Ys.subs(U0))
print("static Lrest at u = 0:", sp.factor(L0))
print("static Y at u = 0:   ", sp.factor(Y0))
# u-equation sources at u = 0: dL/dU (value) - (1/R) d_R(R dL/dU_R) - d_z(dL/dU_z), to first order in u, at u = 0
for n in ("U_R", "U_z"):
    dLdU = sp.diff(Ls, sp.Symbol(n, real=True)).subs(U0)
    dYdU = sp.diff(Ys, sp.Symbol(n, real=True)).subs(U0)
    dLdUR = sp.diff(Ls, sp.Symbol(n + "_R", real=True)).subs(U0); dLdUz = sp.diff(Ls, sp.Symbol(n + "_z", real=True)).subs(U0)
    print(f"{n}: dLrest/d{n} = {sp.factor(dLdU)};  dY/d{n} = {sp.factor(dYdU)};  dLrest/d{n}_R = {sp.factor(dLdUR)};  dLrest/d{n}_z = {sp.factor(dLdUz)}")
