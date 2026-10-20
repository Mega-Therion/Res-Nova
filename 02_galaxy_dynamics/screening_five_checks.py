#!/usr/bin/env python3
"""Five checks on tidal screening, 2026-10-16. Numbers only. Tiers are in the note."""

import json
import os
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

import sparc_reproduce as sr
import tidal_screening_sparc_cassini as TS
import tidal_screening_two_body as TB
from environment_screening import S as S_efe

XS = 703588428133.2817  # action-form x*_A
A0 = TS.A0
AU = 1.496e11
KAU = 1000 * AU


def sun_profile(n=400):
    r = np.geomspace(100 * AU, 1e5 * AU, n)
    gN = TS.GM / r**2
    y = np.maximum(gN / A0, 1e-30)
    nu = np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2)))
    v = TS.R_M / r
    x = np.sqrt((TS.X_M * v**3) ** 2 + TS.X_MW**2)
    s = 1 / (1 + (x / XS) ** 2)
    g_s = gN * (1 + s * (nu - 1))
    g_u = gN * nu
    return r, gN, g_s, g_u, s, x


def potential_shift(r, g, gN):
    """Extra potential Φ-Φ_N, zeroed at the inner edge. Inward g > 0."""
    extra = g - gN
    # integrate outward: d(δΦ)/dr = -(g - gN) if g is inward acceleration
    dphi = -0.5 * (extra[1:] + extra[:-1]) * np.diff(r)
    return np.concatenate([[0.0], np.cumsum(dphi)])


def one_over_a(dphi):
    """Keplerian 1/a shift (AU^-1) from an energy offset, measured where the field is Newtonian."""
    return -2 * dphi / TS.GM * AU


def comet_orbit(g_of_r, r0_kAU, years=2e6):
    """Radial orbit, specific angular momentum of a circular orbit at r0/5, so it reaches the outer cloud."""
    r0 = r0_kAU * KAU
    g0 = g_of_r(r0)
    # start at rest-ish from r0 (aphelion): vr=0, L small
    L = 0.15 * r0 * np.sqrt(max(g0 * r0, 0))

    def f(t, y):
        r, vr = y
        r = max(r, 50 * AU)
        return [vr, L**2 / r**3 - g_of_r(r)]

    sol = solve_ivp(
        f,
        (0, years * 365.25 * 86400),
        [r0, 0.0],
        rtol=1e-6,
        atol=1e-2,
        dense_output=False,
    )
    rr = sol.y[0]
    return dict(
        ok=bool(sol.success),
        rmin_kAU=float(rr.min() / KAU),
        rmax_kAU=float(rr.max() / KAU),
        n=int(rr.size),
    )


def ngc5055():
    g = sr.load_rotmod(Path(os.environ["SPARC_DATA_DIR"]) / "NGC5055_rotmod.dat")
    e_env = 0.04  # Chae et al. 2020 Table 2, in units of 1.2e-10
    gext = e_env * 1.2e-10
    a0 = sr.A0_HORIZON
    eta = gext / a0
    yd, fd = 0.55, 0.9
    vb = sr.v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], yd, 0.0)
    R, Vo, e = g["r"], g["v_obs"], g["v_err"]
    vb2 = fd * (vb * 1e3) ** 2
    r_m = R * 3.085677581e19 * fd
    gN = vb2 / np.maximum(r_m, 1e-6)
    nu = np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / np.maximum(gN / a0, 1e-30) ** 2)))
    geff = gN * (1 + S_efe(eta) * (nu - 1))
    vp = np.sqrt(geff * r_m) / 1e3
    vp0 = np.sqrt(gN * nu * r_m) / 1e3
    outer = R >= 10
    i14 = int(np.argmin(np.abs(R - 14)))
    i55 = int(np.argmax(R))

    def chi(mask, model):
        d = Vo[mask] - model[mask]
        return float(np.sum((d / e[mask]) ** 2)), float(np.median(d))

    c0, m0 = chi(outer, vp0)
    ce, me = chi(outer, vp)
    return {
        "e_env": e_env,
        "g_ext": gext,
        "eta": float(eta),
        "S": float(S_efe(eta)),
        "chi2_out_eta0": c0,
        "med_out_eta0": m0,
        "chi2_out_eenv": ce,
        "med_out_eenv": me,
        "V14_obs": float(Vo[i14]),
        "V14_eta0": float(vp0[i14]),
        "V14_eenv": float(vp[i14]),
        "V55_obs": float(Vo[i55]),
        "V55_eta0": float(vp0[i55]),
        "V55_eenv": float(vp[i55]),
        "data_drop": float(Vo[i14] - Vo[i55]),
        "model_drop_eta0": float(vp0[i14] - vp0[i55]),
        "model_drop_eenv": float(vp[i14] - vp[i55]),
        "R": [float(x) for x in R[outer]],
        "Vobs": [float(x) for x in Vo[outer]],
        "Veenv": [float(x) for x in vp[outer]],
    }


def ngc2419():
    """Plummer with Baumgardt et al. 2009 mass and half-mass radius. [C] inputs, [D] tide."""
    M = 9.0e5 * TS.MSUN
    rh = (
        26.0 * TS.PC
    )  # 3D half-mass, Baumgardt catalogue scale; paper half-light 19 pc projected
    a = rh / 1.305
    rho0 = 3 * M / (4 * np.pi * a**3)
    r = np.geomspace(0.5 * TS.PC, 200 * TS.PC, 200)
    # enclosed mass, Plummer
    Menc = M * r**3 / (r**2 + a**2) ** 1.5
    rho = (3 * M / (4 * np.pi * a**3)) * (1 + r**2 / a**2) ** -2.5
    gN = TS.G * Menc / r**2
    # Frobenius tide of a spherical field: eigenvalues (-2g/r * factor). Use |d g_r / dr| and g/r.
    # H_rr = d(gN)/dr with gN inward so Phi'' = d(gN)/dr? g_inward = GM/r^2, d(g)/dr = -2GM/r^3, H_rr=-2GM/r^3, H_tang=GM/r^3
    Ht = TS.G * Menc / r**3
    Hrr = np.gradient(gN, r)  # this is d(g_inward)/dr = -2 GM/r^3 outside
    HF = np.sqrt(Hrr**2 + 2 * Ht**2)
    x = TS.C**2 * HF / A0**2
    s = 1 / (1 + (x / XS) ** 2)
    y = gN / A0
    nu = np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-30) ** 2)))
    # isotropic Plummer σ_3d^2(r) = GM / (6 sqrt(r^2+a^2)); MOND: replace g by g*ν_eff in the Jeans estimate σ^2 ~ g r
    sig_n = np.sqrt(TS.G * M / (6 * np.sqrt(r**2 + a**2)))
    sig_s = sig_n * np.sqrt(1 + s * (nu - 1))
    return {
        "rho0_Msun_pc3": float(rho0 / TS.MSUN * TS.PC**3),
        "rho_half_Msun_pc3": float(np.interp(rh, r, rho) / TS.MSUN * TS.PC**3),
        "S_min": float(s.min()),
        "S_at_half": float(np.interp(rh, r, s)),
        "S_at_5pc": float(np.interp(5 * TS.PC, r, s)),
        "x_over_xs_max": float((x / XS).max()),
        "nu_at_half": float(np.interp(rh, r, nu)),
        "sig_newt_half_kms": float(np.interp(rh, r, sig_n) / 1e3),
        "sig_screen_half_kms": float(np.interp(rh, r, sig_s) / 1e3),
        "obs_sigma_kms": 4.14,
        "obs_sigma_err": 0.48,
    }


def main():
    r, gN, gs, gu, s, x = sun_profile()
    dphi_s = potential_shift(r, gs, gN)
    dphi_u = potential_shift(r, gu, gN)
    rk = r / KAU

    def at(target):
        i = int(np.argmin(np.abs(rk - target)))
        return dict(
            r_kAU=float(rk[i]),
            S=float(s[i]),
            g_over_gN_screen=float(gs[i] / gN[i]),
            g_over_gN_unscreened=float(gu[i] / gN[i]),
            d_inv_a_screen=float(one_over_a(dphi_s[i])),
            d_inv_a_unscreened=float(one_over_a(dphi_u[i])),
        )

    # interpolants for a few orbits
    from numpy import interp

    def gfun(arr):
        return lambda rr: float(interp(rr, r, arr))

    orbits = {}
    for name, arr in (("screen", gs), ("newton", gN), ("unscreened", gu)):
        orbits[name] = comet_orbit(gfun(arr), 20.0, years=5e5)

    # action-form binary, Sun-like total mass, q1=0.8, two angles. This is a binary, not a comet.
    gam = []
    for rkau in (5, 8, 10, 15, 20, 25, 40):
        row = {"r_kAU": rkau}
        for mu in (0.0, 0.86):
            out = TB.solve_binary(
                1.0, rkau * KAU, 0.8, mu, 1.9e-10, "action", xs=XS, res=1
            )
            row[f"mu{mu:.2f}"] = {
                "Gamma_r": float(out["Gamma_r"]),
                "Gamma_t": float(out["Gamma_t"]),
            }
        gam.append(row)
        print("binary", rkau, row, flush=True)

    H = XS * A0**2 / TS.C**2
    rho = H / (4 * np.pi * TS.G)
    # candidate identification: S=1/2 at the MOND radius would set x* = X_M
    result = {
        "x_star_action": XS,
        "H_F_at_xstar_s-2": float(H),
        "rho_if_HF_eq_4piGrho_Msun_pc3": float(rho * TS.PC**3 / TS.MSUN),
        "X_M_over_xstar": float(TS.X_M / XS),
        "r_screen_kAU": float(TB.r_screen(TS.GM, XS) / KAU),
        "r_mond_kAU": float(TS.R_M / KAU),
        "S_galactic_only": float(1 / (1 + (TS.X_MW / XS) ** 2)),
        "sun": [at(z) for z in (1, 5, 9.7, 15, 20, 25, 50, 100)],
        "orbits_0.5Myr_from_20kAU": orbits,
        "binary_Gamma": gam,
        "ngc5055": ngc5055(),
        "ngc2419": ngc2419(),
    }
    Path("/tmp/screening_five_checks.json").write_text(json.dumps(result, indent=1))
    print(
        json.dumps(
            {
                k: result[k]
                for k in result
                if k not in ("binary_Gamma", "sun", "ngc5055")
            },
            indent=1,
        )
    )
    print("SUN", json.dumps(result["sun"], indent=1))
    print("5055", json.dumps(result["ngc5055"], indent=1))
    print("2419", json.dumps(result["ngc2419"], indent=1))


if __name__ == "__main__":
    main()
