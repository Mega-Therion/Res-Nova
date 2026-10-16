#!/usr/bin/env python3
"""Gravitational-wave speed and well-posedness for screening on a tidal coordinate.

The screening term is L_scr = -F S(x): F > 0 is the MOND scalar sector, S decreases
from 1, and x = c^2 |grad grad Phi| / a0^2 (Frobenius norm) is the tidal coordinate.
It can be built covariantly in two ways:
 (a) from curvature, E_ij = c^2 R_0i0j (electric part of Riemann in the aether frame);
 (b) from the scalar's own spatial Hessian, H_ij = q q grad grad Phi_s.
Two screening forms are carried throughout: S1 = 1/(1 + x/x*), S2 = 1/(1 + (x/x*)^2).

A. (a): x contains second time derivatives of h_ij, nondegenerately (Ostrogradsky).
   Size of its hddot^2 term against the Einstein-Hilbert kinetic term (c^2/32 pi G) hdot^2.
B. (b): x contains only first derivatives of h. The same ratio is a fractional change
   of the tensor kinetic term, i.e. of c_T^2.
C. Legendre-Hadamard on the highest-derivative part of J(Y) S(x(H)), J > 0:
   the AQUAL single-scalar form, and the QUMOND two-field form.
Writes TIDAL_SCREENING_CONSISTENCY.json. Exit 0 only if every assertion holds.
"""
import json
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
A0, C, G = 1.1607e-10, 2.998e8, 6.674e-11
H0 = 67.4e3 / 3.0857e22
RHO_C = 3 * H0**2 / (8 * np.pi * G)
XSTARS = (1e11, 1e12)
OMEGA = {"LIGO_100Hz": 2 * np.pi * 100.0, "PTA_10nHz": 2 * np.pi * 1e-8}
# f = 8 pi G F / a0^2 (scalar-sector energy density); x0 = background tidal coordinate
ENV = {
    "galaxy_disk": {"f": 1.0, "x0": 3.9e7, "g_s": A0, "phidot_s": 0.0},
    "intergalactic_phidot0": {"f": 8 * np.pi * G * 0.26 * RHO_C * C**2 / A0**2,
                              "x0": C**2 * 4 * np.pi * G * 0.31 * RHO_C / np.sqrt(3) / A0**2,
                              "g_s": 0.034 * A0, "phidot_s": 0.0},
    # the scalar's cosmic drift: Phi_s-dot = c^2 phi-dot with phi-dot ~ H0 (an upper-end guess)
    "intergalactic_phidotH0": {"f": 8 * np.pi * G * 0.26 * RHO_C * C**2 / A0**2,
                               "x0": C**2 * 4 * np.pi * G * 0.31 * RHO_C / np.sqrt(3) / A0**2,
                               "g_s": 0.034 * A0, "phidot_s": C**2 * H0},
}
out = {"forms": {"S1": "1/(1+x/x*)", "S2": "1/(1+(x/x*)^2)"}, "x_star": list(XSTARS)}

xs, xst = sp.symbols("x x_star", positive=True)
FORMS = {"S1": 1 / (1 + xs / xst), "S2": 1 / (1 + (xs / xst) ** 2)}


def derivs(form, x0, xstar):
    e = FORMS[form]
    d1 = sp.diff(e, xs).subs({xs: x0, xst: xstar})
    d2 = sp.diff(e, xs, 2).subs({xs: x0, xst: xstar})
    return float(d1), float(d2)


def fro(M):
    return sp.sqrt(sum(M[i, j] ** 2 for i in range(3) for j in range(3)))


eps = sp.symbols("epsilon", real=True)
B0 = sp.diag(-2, 1, 1) / sp.sqrt(6)            # unit-norm point-mass tidal shape
P = sp.diag(1, -1, 0)                          # + polarization, wave along z


def quad_coeffs(dM):
    """|B0 + eps dM| = 1 + n1 eps + n2 eps^2 + ...; returns (n1, n2)."""
    s = sp.series(fro(B0 + eps * dM), eps, 0, 3).removeO()
    return sp.nsimplify(s.coeff(eps, 1)), sp.nsimplify(s.coeff(eps, 2))


# ---- A. curvature-based x -----------------------------------------------------------
t, X, Y, Z = sp.symbols("t x y z", real=True)
cs = sp.symbols("c", positive=True)        # exact c in the symbolic parts
hp = sp.Function("hp")(t, Z)
coords = [cs * t, X, Y, Z]
h = sp.zeros(4, 4)
h[1, 1], h[2, 2] = hp, -hp


def d(f, mu):
    return sp.diff(f, t) / cs if mu == 0 else sp.diff(f, coords[mu])


def riem(m, n, r, s):                          # linearized R_{mnrs}
    return sp.Rational(1, 2) * (d(d(h[m, s], r), n) + d(d(h[n, r], s), m) - d(d(h[n, s], r), m) - d(d(h[m, r], s), n))


E11 = sp.simplify(cs**2 * riem(0, 1, 0, 1))
assert sp.simplify(E11 + sp.diff(hp, t, 2) / 2) == 0     # c^2 R_0101 = -hddot_+/2: second time derivative
n1, n2 = quad_coeffs(-P / 2)                   # dE = -(1/2) hddot_+ P, background |E0| = e0
# x = (c^2/a0^2) e0 |B0 + (hddot/e0) dM| -> quadratic in hddot: (c^2/a0^2) n2 hddot^2 / e0
# L_scr^(2) = -F [ S' (c^2/a0^2) n2 / e0 + (1/2) S'' (c^2/a0^2)^2 n1^2 ] hddot^2
A_rows = {}
for env, p in ENV.items():
    F = p["f"] * A0**2 / (8 * np.pi * G)
    e0 = p["x0"] * A0**2 / C**2
    for form in FORMS:
        for xstar in XSTARS:
            s1, s2 = derivs(form, p["x0"], xstar)
            coef = F * abs(s1 * (C**2 / A0**2) * float(n2) / e0 + 0.5 * s2 * (C**2 / A0**2) ** 2 * float(n1) ** 2)
            for wn, w in OMEGA.items():
                ratio = coef * w**2 / (C**2 / (32 * np.pi * G))
                A_rows[f"{env}|{form}|x*={xstar:.0e}|{wn}"] = ratio
            # amplitude above which the wave itself dominates x (linear theory fails)
            A_rows[f"{env}|{form}|x*={xstar:.0e}|h_linear_max_LIGO"] = 2 * e0 / OMEGA["LIGO_100Hz"] ** 2
assert min(v for k, v in A_rows.items() if k.endswith("LIGO_100Hz")) > 1e6
out["A_curvature"] = {"E_TT": "c^2 R_0i0j = -hddot_ij / 2 (second time derivative of h)",
                      "ratio_hddot2_to_EH": A_rows}

# ---- B. scalar-Hessian x ---------------------------------------------------------------
gx, gz, phid = sp.symbols("g_x g_z phidot", real=True)
Phi_s = gx * X + gz * Z + phid * t             # background scalar potential: gradient + drift
Gam = {}
for lam in range(4):
    for i in range(1, 4):
        for j in range(1, 4):
            sgn = -1 if lam == 0 else 1
            Gam[lam, i, j] = sgn * sp.Rational(1, 2) * (d(h[lam, j], i) + d(h[lam, i], j) - d(h[i, j], lam))
dH = sp.zeros(3, 3)
for i in range(1, 4):
    for j in range(1, 4):
        dH[i - 1, j - 1] = -sum(Gam[lam, i, j] * d(Phi_s, lam) for lam in range(4))
assert all(not dH[i, j].has(sp.Derivative(hp, (t, 2))) and not dH[i, j].has(sp.Derivative(hp, (Z, 2)))
           and not dH[i, j].has(sp.Derivative(hp, t, Z)) for i in range(3) for j in range(3))
# plane wave h(t - z/c): d_z h = -hdot/c. dH is then proportional to hdot.
hd = sp.symbols("hdot", real=True)
dHw = dH.subs(sp.Derivative(hp, Z), -sp.Derivative(hp, t) / cs).subs(sp.Derivative(hp, t), hd).subs(cs, C)
B_rows = {}
for env, p in ENV.items():
    F = p["f"] * A0**2 / (8 * np.pi * G)
    e0 = p["x0"] * A0**2 / C**2
    al = 0.7                                   # grad Phi_s at ~40 degrees to the propagation axis
    dHn = dHw.subs({gx: p["g_s"] * np.sin(al), gz: p["g_s"] * np.cos(al), phid: p["phidot_s"]})
    dM = sp.Matrix(dHn / hd / e0)              # dH / (e0 hdot), dimensionless shape
    m1, m2 = quad_coeffs(sp.Matrix(3, 3, lambda i, j: sp.Float(dM[i, j])))
    for form in FORMS:
        for xstar in XSTARS:
            s1, s2 = derivs(form, p["x0"], xstar)
            xs0 = p["x0"]
            coef = F * abs(s1 * xs0 * float(m2) + 0.5 * s2 * xs0**2 * float(m1) ** 2)
            B_rows[f"{env}|{form}|x*={xstar:.0e}|dcT2"] = coef / (C**2 / (32 * np.pi * G))
GW = 1e-15                                     # GW170817, |v_GW - v_EM| / c
assert all(v < GW for k, v in B_rows.items() if k.startswith("galaxy_disk") or "|S2|" in k)
# S1's onset is linear in |H|, so it is not analytic in the Hessian, and between galaxies,
# where the background Hessian is tiny, it moves the tensor term past the GW170817 bound.
assert all(v > GW for k, v in B_rows.items() if k.startswith("intergalactic") and "|S1|" in k)
out["B_scalar_hessian"] = {"dH": "first derivatives of h only (Christoffels times grad Phi_s and Phi_s-dot)",
                           "fractional_change_of_tensor_kinetic_term": B_rows}

# ---- C. Legendre-Hadamard --------------------------------------------------------------
be = sp.symbols("beta", real=True)
xi = sp.Matrix([sp.sin(be), 0, sp.cos(be)])
H0m = sp.diag(-2, 1, 1)
k0 = sp.symbols("k0", positive=True)           # x = k0 |H|
LH = {}
for form, Sx in FORMS.items():
    for xstar in XSTARS:
        for x0 in (1e7, 1e10, 1e12, 1e13):
            k0v = x0 / float(fro(H0m))
            f_eps = Sx.subs({xs: k0v * fro(H0m + eps * xi * xi.T), xst: xstar})
            d2 = sp.diff(f_eps, eps, 2).subs(eps, 0)
            vals = [float(d2.subs(be, b)) for b in np.linspace(0, np.pi / 2, 91)]
            null = float(d2.subs(be, sp.atan(1 / sp.sqrt(2))))      # direction with xi.H.xi = 0
            LH[f"{form}|x*={xstar:.0e}|x0={x0:.0e}"] = {"min_over_directions": min(vals), "null_direction": null}
assert all(v["null_direction"] < 0 and v["min_over_directions"] < 0 for v in LH.values())

# QUMOND two-field form, 1D: L = -2 Phi' Phi_N' + Q(Phi_N'^2) S(Phi_N''^2) - 8 pi G rho Phi
u = sp.symbols("u", real=True)
Ph, PN = sp.Function("Phi")(u), sp.Function("PhiN")(u)
Qf, Sf, rho = sp.Function("Q"), sp.Function("Sf"), sp.Function("rho")(u)
Lq = -2 * Ph.diff(u) * PN.diff(u) + Qf(PN.diff(u) ** 2) * Sf(PN.diff(u, 2) ** 2) - 8 * sp.pi * G * rho * Ph
eqs = sp.euler_equations(Lq, [Ph, PN], u)
eq_phi = sp.simplify(eqs[0].lhs)
assert not eq_phi.has(Sf) and sp.simplify(eq_phi - (2 * PN.diff(u, 2) - 8 * sp.pi * G * rho)) == 0
eq_pn = sp.expand(eqs[1].lhs)
assert sp.simplify(sp.diff(eq_pn, Ph.diff(u, 2)) - 2) == 0 and not sp.diff(eq_pn, Ph.diff(u, 2)).has(Sf)
out["C_legendre_hadamard"] = {"aqual": LH,
                              "qumond": "Phi_N obeys Poisson (no S); Phi obeys a linear Poisson equation with a source from Phi_N"}

json.dump(out, open(HERE / "TIDAL_SCREENING_CONSISTENCY.json", "w"), indent=1)
g = {k: v for k, v in A_rows.items() if "LIGO" in k and "linear" not in k}
print(f"A  curvature x: hddot^2 term / EH kinetic at 100 Hz: {min(g.values()):.1e} .. {max(g.values()):.1e}")
p = {k: v for k, v in A_rows.items() if "PTA" in k}
print(f"   at 10 nHz: {min(p.values()):.1e} .. {max(p.values()):.1e}; linear theory needs h < "
      f"{min(v for k, v in A_rows.items() if 'linear' in k):.1e} at 100 Hz")
for env in ENV:
    for form in FORMS:
        r = [B_rows[f"{env}|{form}|x*={xs_:.0e}|dcT2"] for xs_ in XSTARS]
        print(f"B  scalar-Hessian x, {env}, {form}: change of tensor kinetic term {min(r):.1e} .. {max(r):.1e}")
print(f"C  AQUAL form, Legendre-Hadamard null direction: max {max(v['null_direction'] for v in LH.values()):.2e} (< 0: fails)")
print("   QUMOND form: Phi_N from Poisson, Phi linear: well-posed")
print("ALL CHECKS PASS")
