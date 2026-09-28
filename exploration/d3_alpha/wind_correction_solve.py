#!/usr/bin/env python3
"""D7 decisive step 2 (an INDICATION, local WKB at k r = 1): does the O(v) residual of the boosted-held configuration
force a large change of the dwarf's MOND field, or is it absorbed harmlessly?
  M(k, w=0; v) dX = -R,  M from aest_wind_bg.py (validated by wind_bg_validate.py),
  R = full residual vector in the builder basis from boosted_held_residuals.py (aether, scalar AND metric rows),
      with the v = 0 residual subtracted, mapped to a Fourier source at k = 1/r.
Point-to-mode mapping is ambiguous: gradient-type terms (no Hessian) enter with phase 1, Hessian-type terms with
phase 1, +i or -i (three variants). A result that changes by orders of magnitude between variants is not a result.
Diagnostics (gauge invariant): |dY|/(2Y0) = fractional change of the MOND field strength |S| (Y = |S|^2);
|rot| = rotation of the MOND field direction, (dS_perp - g h_xz)/|S|; and the aether tilt
|du^z| against the stealth-branch tilt g/Q0.
Usage: wind_correction_solve.py [par|perp] [K2]"""

import sys, pickle, sympy as sp, mpmath as mp

mp.mp.dps = 80
DIR = sys.argv[1] if len(sys.argv) > 1 else "par"
K2v = int(sys.argv[2]) if len(sys.argv) > 2 else 75
M, names, (qb, Jp, Jl, g, k, w, vw), (KB, K2, Q0) = pickle.load(
    open(f"wind_bg_matrix_{DIR}_K2{K2v}.pkl", "rb")
)
fM = sp.lambdify((qb, Jp, Jl, g, k, w, vw), M, "mpmath")
RR = pickle.load(open(f"boosted_residuals_{DIR}.pkl", "rb"))
sKB, sK2, sQ0, sv, sgv, sHs, sghs, sHhs, sfY1, sF2 = RR["symbols"]

# ---- first-order Y and Q of the builder (same conventions as aest_wind_bg.py) for the diagnostics ----
t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
e = sp.Symbol("e")
eta = sp.diag(-1, 1, 1, 1)
mn = {
    (0, 0): "h00",
    (0, 1): "h0x",
    (0, 3): "h0z",
    (1, 1): "hxx",
    (2, 2): "hyy",
    (3, 3): "hzz",
    (1, 3): "hxz",
}
Fh = {nm: sp.Function(nm)(t, z) for nm in mn.values()}
UX, UZ, P = sp.Function("ux")(t, z), sp.Function("uz")(t, z), sp.Function("phi")(t, z)
h = sp.zeros(4, 4)
for (a, b), nm in mn.items():
    h[a, b] = Fh[nm]
    h[b, a] = Fh[nm]
trunc = lambda ex, nn=2: (lambda E: sum(E.coeff(e, i) * e**i for i in range(nn + 1)))(
    sp.expand(ex)
)
gm = eta + e * h
hu = eta * h * eta
gi = (eta - e * hu + e**2 * (hu * eta * h * eta)).applyfunc(trunc)
a1, a2 = sp.symbols("a1 a2")
gw = 1 / sp.sqrt(1 - vw**2)
uv = [gw + e * a1 + e**2 * a2, e * UX, 0, -vw * gw + e * UZ]
norm = sp.expand(
    sp.series(
        sp.expand(
            sum(gm[m, n_] * uv[m] * uv[n_] for m in range(4) for n_ in range(4)) + 1
        ),
        e,
        0,
        3,
    ).removeO()
)
sa1 = sp.solve(norm.coeff(e, 1), a1)[0]
sa2 = sp.solve(sp.expand(norm.coeff(e, 2).subs(a1, sa1)), a2)[0]
uv = [trunc(u.subs(a1, sa1).subs(a2, sa2)) if not isinstance(u, int) else u for u in uv]
Q0n = sp.Rational(1, 10)
gx_, gz_ = (0, g) if DIR == "par" else (g, 0)
dphi = [
    (Q0n + qb) * gw + e * sp.diff(P, t),
    gx_,
    0,
    (Q0n + qb) * gw * vw + gz_ + e * sp.diff(P, z),
]
Yq = trunc(
    sum(
        (gi[m, n_] + uv[m] * uv[n_]) * dphi[m] * dphi[n_]
        for m in range(4)
        for n_ in range(4)
    )
)
fields = list(Fh.values()) + [UX, UZ, P]
amp = {f: sp.Symbol("A_" + str(f.func)) for f in fields}
ph = sp.exp(sp.I * (k * z - w * t))
Y1 = sp.expand(
    sp.expand(Yq.coeff(e, 1).subs({f: amp[f] * ph for f in fields}).doit()) / ph
)
Y1 = sp.expand(
    Y1.subs({t: 0, z: 0})
)  # phase factor is 1 at t = z = 0 (robust to unsplit exponentials)
Y0 = sp.simplify(
    Yq.coeff(e, 0)
)  # = g^2 gamma^2 (par) or g^2 (perp); qbar cancels only after simplify
Qq = trunc(sum(uv[m] * dphi[m] for m in range(4)))
A_lo = [trunc(sum(gm[m, n_] * uv[n_] for n_ in range(4))) for m in range(4)]
Qbg = sp.simplify(Qq.coeff(e, 0))
dphi1 = [sp.expand(dp).coeff(e, 1) if isinstance(dp, sp.Basic) else 0 for dp in dphi]
dS = [
    dphi1[m] + Qq.coeff(e, 1) * A_lo[m].coeff(e, 0) + Qbg * A_lo[m].coeff(e, 1)
    for m in range(4)
]
# gauge-invariant rotation of the MOND field: under x -> x + xi(z), dS_mu -> dS_mu + S_nu d_mu xi^nu, h_xz -> h_xz + d_z xi_x
# par (S along z): rot = dS_x - g h_xz ; perp (S along x): rot = dS_z - g h_xz
rot = (dS[1] if DIR == "par" else dS[3]) - g * Fh["hxz"]
rotA = sp.expand(
    sp.expand(rot.subs({f: amp[f] * ph for f in fields}).doit()) / ph
).subs({t: 0, z: 0})
frot = sp.lambdify([amp[f] for f in fields] + [qb, g, k, w, vw], rotA, "mpmath")
fY1d = sp.lambdify([amp[f] for f in fields] + [qb, g, k, w, vw], Y1, "mpmath")
fY0 = sp.lambdify((g, vw), Y0, "mpmath")

# ---- parameters: galaxy-consistent point, dSph background at r = 0.3 kpc ----
c_kms = mp.mpf(299792.458)
xv = mp.mpf("0.05")
Jpv = xv / mp.sqrt(1 + xv * xv)
Jlv = xv * (1 + xv * xv) ** mp.mpf(-1.5)
gval = xv * 2 * mp.mpf("3.577e-5")
r = mp.mpf("3e-4")
kv = 1 / r
vf = mp.mpf(10) / c_kms
qv = (vf / r) ** 2 / (mp.mpf(K2) * mp.mpf(Q0))
KBn, Q0f = mp.mpf(1) / 2, mp.mpf(1) / 10


def residual_vector(vv, variant):
    yp = gval**2 / (1 - vv**2) if DIR == "par" else gval**2
    sub = {sKB: sp.Rational(1, 2), sK2: K2v, sQ0: Q0n}
    out = []
    for nm in names:
        ex = RR["builder"][nm]
        ex = sp.expand(ex.subs(sub))
        hess = sum(
            term for term in sp.Add.make_args(ex) if term.has(sHs) or term.has(sHhs)
        )
        grad = sp.expand(ex - hess)
        vals = {
            sgv: gval,
            sghs: Jpv * gval,
            sHs: gval * kv,
            sHhs: Jpv * gval * kv,
            sfY1: (2 - KBn) * Jpv,
            sF2: (2 - KBn) * Jlv / (2 * yp),
        }
        ph_h = {"real": 1, "+i": 1j, "-i": -1j}[variant]
        fg = sp.lambdify((sv,) + tuple(vals.keys()), grad, "mpmath")
        fh = sp.lambdify((sv,) + tuple(vals.keys()), hess, "mpmath")
        R_v = fg(vv, *vals.values()) + ph_h * fh(vv, *vals.values())
        R_0 = fg(0, *vals.values()) + ph_h * fh(0, *vals.values())
        out.append(R_v - R_0)
    return mp.matrix(out)


ix = {nm: i for i, nm in enumerate(names)}
print(
    f"{DIR}, K2={K2v}: k={float(kv):.0f}/Mpc, g={float(gval):.3e}/Mpc, qbar={float(qv):.3e}/Mpc, stealth tilt g/Q0={float(gval/Q0f):.2e}"
)
for variant in ["real", "+i", "-i"]:
    print(f"  Hessian-term phase {variant}:")
    print(
        f"  {'v [km/s]':>9s} {'|dS_par|/|S|':>13s} {'|rot|':>10s} {'|du^z|/(g/Q0)':>15s} {'|R|max':>11s} {'s_min(M)':>11s}"
    )
    for vk in ["1", "3", "10", "30", "100", "300", "600"]:
        vv = mp.mpf(vk) / c_kms
        Mn = mp.matrix(fM(qv, Jpv, Jlv, gval, kv, 0, vv))
        R = residual_vector(vv, variant)
        dX = mp.lu_solve(Mn, -R)
        dY = fY1d(*[dX[i] for i in range(len(names))], qv, gval, kv, 0, vv)
        dS_rel = abs(dY) / (2 * fY0(gval, vv))
        rotv = abs(
            frot(*[dX[i] for i in range(len(names))], qv, gval, kv, 0, vv)
        ) / mp.sqrt(fY0(gval, vv))
        tilt = abs(dX[ix["uz"]]) / (gval / Q0f)
        smin = min(abs(sval) for sval in mp.svd_c(Mn, compute_uv=False))
        print(
            f"  {float(vk):9.0f} {float(dS_rel):13.4e} {float(rotv):10.3e} {float(tilt):15.4e} {float(max(abs(R[i]) for i in range(R.rows))):11.3e} {float(smin):11.3e}",
            flush=True,
        )
