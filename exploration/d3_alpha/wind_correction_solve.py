#!/usr/bin/env python3
"""D7 decisive step 2 (an INDICATION, local WKB): does the O(v) residual of the boosted-held configuration
force a large change of the dwarf's MOND field, or is it absorbed harmlessly?
  M(k, w=0; v) dX = -R,  M from aest_wind_bg.py (validated by wind_bg_validate.py),
  R = full residual vector in the builder basis from boosted_held_residuals.py (aether, scalar AND metric rows),
      with the v = 0 residual subtracted, mapped to a Fourier source at k = 1/r.
Point-to-mode mapping is ambiguous: gradient-type terms (no Hessian) enter with phase 1, Hessian-type terms with
phase 1, +i or -i (three variants). A result that changes by orders of magnitude between variants is not a result.
Diagnostics (gauge invariant): |dY|/(2Y0) = fractional change of the MOND field strength |S| (Y = |S|^2);
|rot| = rotation of the MOND field direction, (dS_perp - g h_xz)/|S|; and the aether tilt
|du^z| against the stealth-branch tilt g/Q0.
Usage: wind_correction_solve.py [par|perp] [75|750000].  Importable: setup(DIR, K2v) returns everything the
decomposition and sensitivity scripts need."""

from types import SimpleNamespace
import sympy as sp, mpmath as mp
from wind_cli import pick_dir, pick_k2
from sym_json import load_matrix, load_residuals

mp.mp.dps = 80


def setup(DIR, K2v):
    DIR = pick_dir([None, DIR])
    K2v = pick_k2([None, None, str(K2v)])
    M, names, (qb, Jp, Jl, g, k, w, vw), (KB, K2, Q0) = load_matrix(f"wind_bg_matrix_{DIR}_K2{K2v}.json")
    fM = sp.lambdify((qb, Jp, Jl, g, k, w, vw), M, "mpmath")
    RR = load_residuals(f"boosted_residuals_{DIR}.json")
    sKB, sK2, sQ0, sv, sgv, sHs, sghs, sHhs, sfY1, sF2 = RR["symbols"]

    # ---- first-order Y and Q of the builder (same conventions as aest_wind_bg.py) for the diagnostics ----
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
    Fh = {nm: sp.Function(nm)(t, z) for nm in mn.values()}
    UX, UZ, P = (
        sp.Function("ux")(t, z),
        sp.Function("uz")(t, z),
        sp.Function("phi")(t, z),
    )
    h = sp.zeros(4, 4)
    for (a, b), nm in mn.items():
        h[a, b] = Fh[nm]
        h[b, a] = Fh[nm]
    trunc = lambda ex, nn=2: (
        lambda E: sum(E.coeff(e, i) * e**i for i in range(nn + 1))
    )(sp.expand(ex))
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
    uv = [
        trunc(u.subs(a1, sa1).subs(a2, sa2)) if not isinstance(u, int) else u
        for u in uv
    ]
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
    dphi1 = [
        sp.expand(dp).coeff(e, 1) if isinstance(dp, sp.Basic) else 0 for dp in dphi
    ]
    dS = [
        dphi1[m] + Qq.coeff(e, 1) * A_lo[m].coeff(e, 0) + Qbg * A_lo[m].coeff(e, 1)
        for m in range(4)
    ]
    # gauge-invariant rotation of the MOND field: under x -> x + xi(z), dS_mu -> dS_mu + S_nu d_mu xi^nu,
    # h_xz -> h_xz + d_z xi_x.  par (S along z): rot = dS_x - g h_xz ; perp (S along x): rot = dS_z - g h_xz
    rot = (dS[1] if DIR == "par" else dS[3]) - g * Fh["hxz"]
    rotA = sp.expand(
        sp.expand(rot.subs({f: amp[f] * ph for f in fields}).doit()) / ph
    ).subs({t: 0, z: 0})
    args = [amp[f] for f in fields] + [qb, g, k, w, vw]
    frot = sp.lambdify(args, rotA, "mpmath")
    fY1d = sp.lambdify(args, Y1, "mpmath")
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
        """variant: 'real', '+i', '-i' (phase of Hessian-type terms) or a number (scale factor for them)."""
        yp = gval**2 / (1 - vv**2) if DIR == "par" else gval**2
        sub = {sKB: sp.Rational(1, 2), sK2: K2v, sQ0: Q0n}
        ph_h = (
            {"real": 1, "+i": 1j, "-i": -1j}[variant]
            if isinstance(variant, str)
            else variant
        )
        out = []
        for nm in names:
            ex = sp.expand(RR["builder"][nm].subs(sub))
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
            fg = sp.lambdify((sv,) + tuple(vals.keys()), grad, "mpmath")
            fh = sp.lambdify((sv,) + tuple(vals.keys()), hess, "mpmath")
            R_v = fg(vv, *vals.values()) + ph_h * fh(vv, *vals.values())
            R_0 = fg(0, *vals.values()) + ph_h * fh(0, *vals.values())
            out.append(R_v - R_0)
        return mp.matrix(out)

    def diag(dX, qq, kk, vv):
        """par: fractional change of |S| (dY/2Y0); perp: gauge-invariant rotation of S."""
        amps = [dX[i] for i in range(len(names))]
        if DIR == "par":
            return abs(fY1d(*amps, qq, gval, kk, 0, vv)) / (2 * fY0(gval, vv))
        return abs(frot(*amps, qq, gval, kk, 0, vv)) / mp.sqrt(fY0(gval, vv))

    return SimpleNamespace(
        DIR=DIR,
        K2v=K2v,
        names=names,
        fM=fM,
        fY1d=fY1d,
        fY0=fY0,
        frot=frot,
        residual_vector=residual_vector,
        diag=diag,
        qv=qv,
        Jpv=Jpv,
        Jlv=Jlv,
        gval=gval,
        kv=kv,
        c_kms=c_kms,
        Q0f=Q0f,
        mp=mp,
    )


def main():
    S = setup(pick_dir(), pick_k2())
    names, ix = S.names, {nm: i for i, nm in enumerate(S.names)}
    print(
        f"{S.DIR}, K2={S.K2v}: k={float(S.kv):.0f}/Mpc, g={float(S.gval):.3e}/Mpc, qbar={float(S.qv):.3e}/Mpc, "
        f"stealth tilt g/Q0={float(S.gval / S.Q0f):.2e}"
    )
    for variant in ["real", "+i", "-i"]:
        print(f"  Hessian-term phase {variant}:")
        print(
            f"  {'v [km/s]':>9s} {'|dS_par|/|S|':>13s} {'|rot|':>10s} {'|du^z|/(g/Q0)':>15s} {'|R|max':>11s} {'s_min(M)':>11s}"
        )
        for vk in ["1", "3", "10", "30", "100", "300", "600"]:
            vv = mp.mpf(vk) / S.c_kms
            Mn = mp.matrix(S.fM(S.qv, S.Jpv, S.Jlv, S.gval, S.kv, 0, vv))
            R = S.residual_vector(vv, variant)
            dX = mp.lu_solve(Mn, -R)
            amps = [dX[i] for i in range(len(names))]
            dS_rel = abs(S.fY1d(*amps, S.qv, S.gval, S.kv, 0, vv)) / (
                2 * S.fY0(S.gval, vv)
            )
            rotv = abs(S.frot(*amps, S.qv, S.gval, S.kv, 0, vv)) / mp.sqrt(
                S.fY0(S.gval, vv)
            )
            tilt = abs(dX[ix["uz"]]) / (S.gval / S.Q0f)
            smin = min(abs(sval) for sval in mp.svd_c(Mn, compute_uv=False))
            print(
                f"  {float(vk):9.0f} {float(dS_rel):13.4e} {float(rotv):10.3e} {float(tilt):15.4e} "
                f"{float(max(abs(R[i]) for i in range(R.rows))):11.3e} {float(smin):11.3e}",
                flush=True,
            )


if __name__ == "__main__":
    main()
