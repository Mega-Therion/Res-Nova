#!/usr/bin/env python3
"""D7 §7 discriminating test: the wind operator with the wavevector at an angle alpha to the wind (aest_wind_bg_angled.py).
k = |k| (sin alpha, 0, cos alpha), |k| = 1/r fixed, point residual R(P) held fixed (boosted_held_residuals.py).
  The correction is carried by the scalar gradient, dS ~ i k dP, so it points along k.
  Streamline-local balance (v k_z coupling): |dS| ~ 1/cos(alpha).  Elliptic (set by |k|): |dS| independent of alpha.
Diagnostics: |k dP|/g = size of the scalar-gradient correction (direct test), and the gauge-invariant
|dY|/(2Y0) = its projection on S (par: ~cos alpha if elliptic, constant if streamline-local; perp: ~sin alpha vs tan alpha).
Validation first: (1) at k_x = 0 the angled matrix equals the validated aest_wind_bg.py matrix, symbolically;
(2) at v = g = qbar = Jl = 0 det M depends on (k_x, k_z) only through |k| (exact rational arithmetic).
Usage: wind_correction_angle.py [par|perp] [75|750000]"""

import sympy as sp, mpmath as mp
from wind_cli import pick_dir, pick_k2
from sym_json import load_matrix

mp.mp.dps = 80
DIR, K2v = pick_dir(), pick_k2()
MA, names, (qb, Jp, Jl, g, kx, kz, w, vw), (KB, K2, Q0) = load_matrix(f"wind_bg_angled_{DIR}_K2{K2v}.json")
M1, names1, (qb1, Jp1, Jl1, g1, k1, w1, vw1), _ = load_matrix(f"wind_bg_matrix_{DIR}_K2{K2v}.json")
assert names == names1
# ---- validation 1: reduction to the validated operator at k_x = 0 ----
D = (
    MA.subs(kx, 0).subs(kz, k1)
    - M1.subs({qb1: qb, Jp1: Jp, Jl1: Jl, g1: g, w1: w, vw1: vw})
).applyfunc(sp.simplify)
nz = sum(1 for q in D if q != 0)
print(
    f"[1] angled operator at k_x = 0 vs validated operator: {nz} nonzero entries of 100"
)
# ---- validation 2: rotational invariance of the isotropic background ----
Mb = MA.subs({Jl: 0, qb: 0}).subs({g: 0, vw: 0})
dets = [
    sp.nsimplify(
        Mb.subs({Jp: sp.Rational(3, 10), kx: a, kz: b, w: 2}).det(method="bareiss")
    )
    for a, b in [(3, 4), (4, 3), (0, 5), (5, 0)]
]
print(
    f"[2] isotropic background, |k| = 5: det M at (kx,kz) = (3,4),(4,3),(0,5),(5,0) equal: {len(set(dets)) == 1}"
)
if nz != 0 or len(set(dets)) != 1:
    raise SystemExit("VALIDATION FAIL")

# ---- first-order Y of the builder for plane waves in (x, z) ----
t, x, y, z = sp.symbols("t x y z", real=True)
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
Fh = {nm: sp.Function(nm)(t, x, z) for nm in mn.values()}
UX, UZ, P = (
    sp.Function("ux")(t, x, z),
    sp.Function("uz")(t, x, z),
    sp.Function("phi")(t, x, z),
)
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
    gx_ + e * sp.diff(P, x),
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
ph = sp.exp(sp.I * (kx * x + kz * z - w * t))
Y1 = sp.expand(
    sp.expand(Yq.coeff(e, 1).subs({f: amp[f] * ph for f in fields}).doit()) / ph
).subs({t: 0, x: 0, z: 0})
Y0 = sp.simplify(Yq.coeff(e, 0))
fY1d = sp.lambdify([amp[f] for f in fields] + [qb, g, kx, kz, w, vw], Y1, "mpmath")
fY0 = sp.lambdify((g, vw), Y0, "mpmath")
fM = sp.lambdify((qb, Jp, Jl, g, kx, kz, w, vw), MA, "mpmath")

# ---- residual (point value, 'real' phase) from the validated solver setup ----
from wind_correction_solve import setup

S = setup(DIR, K2v)
alphas = [0, 15, 30, 45, 60, 75]
ixP = names.index("phi")
for label, which in [("|dY|/(2Y0)  (projection of dS on S)", "Y"), ("|k dP|/g  (size of the scalar-gradient correction)", "P")]:
    print(f"{DIR}, K2={K2v}: {label}; R(P) fixed, |k| = 1/r, k at angle alpha to the wind")
    print(f"{'v [km/s]':>9s} " + " ".join(f"{'a='+str(a):>9s}" for a in alphas) + "   | a=60/a=0")
    for vk in ["1", "10", "100", "300", "600"]:
        vv = mp.mpf(vk) / S.c_kms; R = S.residual_vector(vv, "real"); row = []
        for a in alphas:
            al = mp.radians(a); kxv, kzv = S.kv * mp.sin(al), S.kv * mp.cos(al)
            dX = mp.lu_solve(mp.matrix(fM(S.qv, S.Jpv, S.Jlv, S.gval, kxv, kzv, 0, vv)), -R)
            if which == "Y":
                row.append(abs(fY1d(*[dX[i] for i in range(len(names))], S.qv, S.gval, kxv, kzv, 0, vv)) / (2 * fY0(S.gval, vv)))
            else:
                row.append(S.kv * abs(dX[ixP]) / S.gval)
        ratio = float(row[4] / row[0]) if row[0] > mp.mpf("1e-6") else float("nan")
        print(f"{float(vk):9.0f} " + " ".join(f"{float(q):9.3e}" for q in row) + f"   | {ratio:.3f}", flush=True)
