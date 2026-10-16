#!/usr/bin/env python3
"""Tidal screening on SPARC and Cassini. PRE-REGISTERED 2026-10-15 (CDT), before any run.

Model (the one form left by tidal_screening_consistency.py): QUMOND, quasistatic,
    nu_eff = 1 + S(x) (nu_std(y) - 1),   y = |grad Phi_N| / a0,
    x = c^2 |grad grad Phi_N|_F / a0^2   (Frobenius norm of the Newtonian tidal tensor),
    S(x) = 1 / (1 + (x / x*)^2)           (S2; S1 = 1/(1 + x/x*) fails GW170817 between galaxies),
at the live a0 = 1.1607e-10 m/s^2.

Pre-declared, and not changed after the first run:
 1. x* is calibrated on Cassini only: the largest x* (least screening) with
    Q2 <= 5.2e-27 s^-2 (2026 bound 1.6 +/- 1.8, at 2 sigma) at both g_e = 1.9e-10 and 2.4e-10.
    No x* passing -> FAIL.
 2. SPARC is the test, at that x* and fixed a0, with the fitter and priors of
    environment_screening.py. PASS if the total chi^2 does not rise (K1 of the 2026-10-14
    screening criteria: dchi2 <= 0); otherwise FAIL. A rise below 1 is also reported as
    smaller than one unit of chi^2.
 3. The disk's vertical tide, 4 pi G rho_mid with rho_mid = Sigma_disk / (2 h_z), is bracketed:
    h_z = inf (in-plane terms only, least x), 0.3 kpc, 0.1 kpc. The verdict uses 0.1 kpc
    (most screening). Bulges: 4 pi G rho <= 3 V_bul^2 / R^2 (local density <= mean interior
    density). Gas enters the in-plane terms through V_gas; its vertical term is not modelled.
 4. x* is a new constant fitted to the Solar System, so the model fails K2 of the
    2026-10-14 criteria whatever these numbers say. The run measures what admitting it buys.
Predictions stated, not tested: S along wide-binary separations, dSphs, globular clusters.
Writes TIDAL_SCREENING_SPARC_CASSINI.json.
"""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

import efe_quadrupole_q2 as Q
import environment_screening as E
from parameter_ledger import (FD_STD, KM_TO_M, KPC_TO_M, YB_MEAN, YB_STD, YD_MEAN, YD_STD, chi2, load, v_bary_sq)
from sparc_paths import resolve_sparc_dir

A0 = 1.1607e-10
C = 2.998e8
G = 6.674e-11
MSUN, PC = 1.989e30, 3.0857e16
UP2 = 1.6e-27 + 2 * 1.8e-27
GES = (1.9e-10, 2.4e-10)
HZ = {"in_plane": None, "h0.3kpc": 0.3, "h0.1kpc": 0.1}
S2 = lambda x, xs: 1.0 / (1.0 + (x / xs) ** 2)
nu = Q.NU["mu_std (nu_2)"]
GM = Q.GM
R_M = np.sqrt(GM / A0)
X_M = np.sqrt(6) * C**2 / (A0 * R_M)          # Sun's tidal coordinate at its MOND radius
X_MW = C**2 * 4 * np.pi * G * 0.1 * MSUN / PC**3 / A0**2   # Galactic vertical tide at R0


def q_screened(eta, S_of_v, nv=3000, nxi=400):
    """Milgrom's q(eta) with the boost screened by S(v), v = r_M / r (S depends on v only,
    so the xi-integrals of both brackets still vanish and nu - nu_e stays valid)."""
    etaN = Q.brentq(lambda z: z * nu(z) - eta, 1e-8, eta)
    nue = nu(etaN)
    v = np.concatenate([np.linspace(0, 1e-3, 50)[:-1], np.logspace(-3, 3, nv)])
    xi, w = np.polynomial.legendre.leggauss(nxi)
    V, XI = np.meshgrid(v, xi, indexing="ij")
    y = np.sqrt(np.maximum(etaN**2 + V**4 + 2 * etaN * V**2 * XI, 1e-300))
    f = S_of_v(V) * (nu(y) - nue) * (etaN * (3 * XI - 5 * XI**3) + V**2 * (1 - 3 * XI**2))
    return 1.5 * np.trapezoid(f @ w, v)


def Q2(a0, ge, S_of_v):
    return -3 * q_screened(ge / a0, S_of_v) * a0**1.5 / (2 * np.sqrt(GM))


def x_sun(v):
    return np.sqrt((X_M * v**3) ** 2 + X_MW**2)


def sb_columns(d, gals):
    """SBdisk, SBbul with load()'s row filter; asserts the radii match the ledger loader."""
    out = {}
    for g in gals:
        rows = []
        for line in (d / f"{g['name']}_rotmod.dat").read_text().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            q = line.split()
            if len(q) < 6:
                continue
            try:
                rows.append([float(z) for z in q[:8]] + [0.0] * (8 - len(q[:8])))
            except ValueError:
                continue
        a = np.asarray(rows, float)
        k = (a[:, 0] > 0) & (a[:, 2] > 0) & (a[:, 1] > 0)
        assert np.allclose(a[k, 0], g["r"]), g["name"]
        out[g["name"]] = (a[k, 6], a[k, 7])
    return out


def tidal_x(g, sb, yd, yb, fd, hz):
    vb2 = v_bary_sq(g, yd, yb, fd) * KM_TO_M**2
    R = g["r"] * fd * KPC_TO_M
    phiR_over_R = vb2 / R**2
    phiRR = np.gradient(vb2 / R, R)
    T2 = phiRR**2 + phiR_over_R**2
    if hz is not None:
        sig = yd * sb[0] * MSUN / PC**2                    # surface density, kg/m^2
        rho = sig / (2 * hz * KPC_TO_M)
        rho_bul = 3 * yb * g["vbul"] ** 2 * fd * KM_TO_M**2 / (4 * np.pi * G * R**2)
        zz = 4 * np.pi * G * (rho + rho_bul) - phiRR - phiR_over_R
        T2 = T2 + zz**2
    return C**2 * np.sqrt(T2) / A0**2


def v_tidal(g, sb, a0, yd, yb, fd, xs, hz):
    vb2 = v_bary_sq(g, yd, yb, fd)
    r = g["r"] * fd
    y = np.maximum(vb2 * KM_TO_M**2 / (r * KPC_TO_M) / a0, 1e-12)
    s = S2(tidal_x(g, sb, yd, yb, fd, hz), xs)
    return np.sqrt(vb2 * (1 + s * (E.nu_std(y) - 1))), s, y


def fit_tidal(g, sb, a0, xs, hz):
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2 + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        return chi2(g, v_tidal(g, sb, a0, yd, yb, fd, xs, hz)[0], pr)
    r = minimize(f, [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0], bounds=[(0.01, 5)] * nb + [(0.5, 2.0)], method="L-BFGS-B")
    t = r.x; yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
    _, s, y = v_tidal(g, sb, a0, yd, yb, fd, xs, hz)
    boost = E.nu_std(y) - 1
    dg = (1 - s) * boost / (1 + boost)                    # fractional change of g
    return float(r.fun), nb + 1, float(dg.max()), float(tidal_x(g, sb, yd, yb, fd, hz).max())


def main():
    out = {"a0": A0, "x_sun_mond_radius": X_M, "r_mond_au": R_M / 1.496e11, "x_galactic_R0": X_MW}
    # validation of the screened integrator
    for ge, want in ((1.9e-10, 16.66e-27), (2.4e-10, 17.17e-27)):
        q1 = Q2(Q.A0_DERIVED, ge, lambda v: np.ones_like(v))
        qh = Q2(Q.A0_DERIVED, ge, lambda v: 0.5 * np.ones_like(v))
        assert abs(q1 / want - 1) < 0.01 and abs(qh / q1 - 0.5) < 1e-12, (q1, qh)
    bare = {f"{ge:.1e}": Q2(A0, ge, lambda v: np.ones_like(v)) for ge in GES}
    out["cassini_bare_live_a0"] = bare
    # 1. calibrate x* on Cassini: largest x* with Q2 <= UP2 at both g_e
    passes = lambda lx: all(Q2(A0, ge, lambda v: S2(x_sun(v), 10**lx)) <= UP2 for ge in GES)
    lo, hi = 6.0, 16.0
    assert passes(lo) and not passes(hi)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if passes(mid) else (lo, mid)
    xs = 10**lo
    out["x_star"] = xs
    out["cassini_at_x_star"] = {f"{ge:.1e}": Q2(A0, ge, lambda v: S2(x_sun(v), xs)) for ge in GES}
    print(f"x* = {xs:.3e} (x at the Sun's MOND radius {X_M:.2e}); Q2 = "
          + ", ".join(f"{k}: {v * 1e27:.2f}e-27" for k, v in out["cassini_at_x_star"].items()) + f" (bound {UP2 * 1e27:.1f}e-27)")
    # 2. SPARC
    d = resolve_sparc_dir(None)
    gals = load(d)
    sb = sb_columns(d, gals)
    base = [E.fit1(g, A0, 0.0) for g in gals]
    cb = sum(c for c, _ in base)
    out["sparc"] = {"n": len(gals), "chi2_unscreened": cb}
    for label, hz in HZ.items():
        fits = [fit_tidal(g, sb[g["name"]], A0, xs, hz) for g in gals]
        ct = sum(f[0] for f in fits)
        worse = int(sum(f[0] > b[0] + 1e-6 for f, b in zip(fits, base)))
        out["sparc"][label] = {"chi2": ct, "dchi2": ct - cb, "galaxies_worse": worse,
                               "max_fractional_dg": max(f[2] for f in fits), "max_x": max(f[3] for f in fits)}
        r = out["sparc"][label]
        print(f"SPARC {label}: chi2 {cb:.1f} -> {ct:.1f} (d {r['dchi2']:+.2f}); worse in {worse}/{len(gals)}; "
              f"max dg/g {r['max_fractional_dg']:.2e}; max x {r['max_x']:.2e}")
    verdict = "PASS" if out["sparc"]["h0.1kpc"]["dchi2"] <= 0 else "FAIL"
    out["sparc"]["verdict_K1"] = verdict
    print(f"SPARC verdict (h_z = 0.1 kpc, K1 dchi2 <= 0): {verdict}. K2: fails by construction (x* fitted to the Solar System).")
    # predictions, not tests
    wb = {}
    for s_au in (2000, 5000, 1e4, 2e4, 3e4):
        x = C**2 * np.sqrt(6) * G * 1.5 * MSUN / (s_au * 1.496e11) ** 3 / A0**2
        wb[str(int(s_au))] = {"x": x, "S": S2(x, xs)}
    out["predictions"] = {"wide_binaries_1.5Msun": wb,
                          "dsph_rho_0.1Msun_pc3": S2(X_MW, xs),
                          "globular_core_1e3_1e4Msun_pc3": [S2(X_MW * 1e4, xs), S2(X_MW * 1e5, xs)]}
    print("wide binaries (1.5 Msun): " + ", ".join(f"{k} AU S={v['S']:.3f}" for k, v in wb.items()))
    json.dump(out, open(Path(__file__).resolve().parent / "TIDAL_SCREENING_SPARC_CASSINI.json", "w"), indent=1)


if __name__ == "__main__":
    main()
