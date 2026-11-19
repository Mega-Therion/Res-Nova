#!/usr/bin/env python3
"""Nested field solution for the open door (AeST live scalar law + quartic Galileon), 2026-11-18.

Model (AEST_TOTAL_SCALAR_CORRESPONDENCE, live total law x mu_std(x) = y, lambda_s < 11.2788):
  matter feels g = g_hat + g_phi;  lap(Phi_hat) = 4 pi G_hat rho;
  div[J'(|grad phi|^2) grad phi] + kappa * 6 det(d^2 phi) = 4 pi G_hat rho     (static quartic Galileon)
  scalar law (parametric in x):  s = x(1 - eta mu),  J' = eta mu/(1 - eta mu),  flux f = J' s = eta x mu.
Door bookkeeping: the Galileon screens the solar-system scalar, so locally measured G = G_hat, the SPARC
scale is a0_fit = a0_model/eta, and G_cosmo/G_local = (2 - K_B)/2 (lambda_s drops out of BBN).

Key step [D here, exact]: around the Sun the screened scalar gradient c << Galactic scalar gradient, so the
AQUAL term linearises to J'_e[lap + L d_z^2]; the Galileon term is blind to the uniform external field.
Stretching z' = z/sqrt(1+L) makes the whole operator isotropic (Part A checks this), so the exact solution
is the spherical Vainshtein profile in stretched coordinates: phi = c r' inside r_V', c = (G M sigma a0m^2/K)^(1/3).
The external-field anisotropy therefore survives inside the Vainshtein region as a constant-magnitude,
direction-dependent force -c grad r'. That leak is tested against Cassini Q2; c against Mercury; K against SPARC.
"""
import glob, json, math, os
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
GM = 1.32712e20; AU = 1.495978707e11; PC = 3.0857e16; KPC = 3.0857e19
A0FIT = 1.1607e-10
GES = (1.9e-10, 2.4e-10); R_SUN = 8.2 * KPC
Q2_LO, Q2_HI = -2.0e-27, 5.2e-27
PREC_MAX = 1.6e-3                                   # arcsec/cy, Mercury (VAINSHTEIN_PREQ)
E_GC = np.array([math.cos(math.radians(-5.54)) * math.cos(math.radians(266.84)),
                 math.cos(math.radians(-5.54)) * math.sin(math.radians(266.84)),
                 math.sin(math.radians(-5.54))])    # Galactic centre, ecliptic frame

# ---------------- Part A: stretched-coordinate reduction (numeric identity check) ----------------
def part_a():
    X, Y, Z, Lsym = sp.symbols("x y z L", positive=True)
    sig = sp.sqrt(1 + Lsym); rp = sp.sqrt(X**2 + Y**2 + Z**2 / sig**2)
    Fexpr = lambda r: r**sp.Rational(23, 10) + sp.Rational(7, 10) * r**sp.Rational(-1, 2)
    rr = sp.Symbol("r", positive=True)
    F1 = sp.diff(Fexpr(rr), rr); F2 = sp.diff(F1, rr)
    phi = Fexpr(rp)
    Hent = [[sp.lambdify((X, Y, Z, Lsym), sp.diff(phi, [X, Y, Z][i], [X, Y, Z][j])) for j in range(3)] for i in range(3)]
    lhs_lin = sp.diff(phi, X, 2) + sp.diff(phi, Y, 2) + (1 + Lsym) * sp.diff(phi, Z, 2)
    rhs_lin = (F2 + 2 * F1 / rr).subs(rr, rp)
    rhs_det = (F2 * (F1 / rr) ** 2).subs(rr, rp) / sig**2
    f_lin = sp.lambdify((X, Y, Z, Lsym), lhs_lin - rhs_lin); g_det = sp.lambdify((X, Y, Z, Lsym), rhs_det)
    rng = np.random.default_rng(1); worst = 0.0
    for _ in range(40):
        p = rng.uniform(0.3, 2.0, 3); Lv = rng.uniform(0.05, 25.0)
        Hn = np.array([[Hent[i][j](*p, Lv) for j in range(3)] for i in range(3)])
        worst = max(worst, abs(f_lin(*p, Lv)), abs(np.linalg.det(Hn) - g_det(*p, Lv)) / max(1e-12, abs(g_det(*p, Lv))))
    assert worst < 1e-9, worst
    partA = {"stretched_reduction_max_residual": worst, "checks": 40,
             "statement": "J'[lap + L d_z^2] + kappa det(d^2 phi) on phi=F(r') equals J' lap'F + (kappa/sigma^2) det'F"}

    return partA

# ---------------- scalar law tables ----------------
mu = lambda x: x / np.sqrt(1 + x * x); dmu = lambda x: (1 + x * x) ** -1.5
def tables(lam):
    eta = lam / (1 + lam); x = np.logspace(-6, 6, 120001); m = mu(x)
    s = x * (1 - eta * m); J1 = eta * m / (1 - eta * m); f = eta * x * m
    ds = 1 - eta * (m + x * dmu(x)); dJ = eta * dmu(x) / (1 - eta * m) ** 2
    assert np.all(np.diff(s) > 0) and np.all(ds > 0), "folding"
    L = dJ * s / (J1 * ds)
    return eta, x, s, J1, f, L

def sun_problem(lam, K, ge):
    eta, x, s, J1, f, L = tables(lam); a0m = eta * A0FIT
    xe = ge / a0m; se = np.interp(xe, x, s); Ae = np.interp(xe, x, J1); Le = np.interp(xe, x, L)
    sigma = math.sqrt(1 + Le)
    c = (GM * sigma * a0m**2 / K) ** (1 / 3)
    rVp = math.sqrt(K * c**2 / (Ae * a0m**2 * sigma**2))
    gal_ratio = K * se**3 / (R_SUN**2 * np.interp(xe, x, f))      # Galileon/AQUAL flux, Galaxy at R_sun
    def acc(pts):                                                  # -c grad r'
        z = pts @ E_GC; rp_ = np.sqrt(np.sum(pts**2, 1) - z**2 + z**2 / sigma**2)
        grad = (pts - (1 - 1 / sigma**2) * z[:, None] * E_GC[None, :]) / rp_[:, None]
        return -c * grad
    def circle(r, n=720):
        t = np.linspace(0, 2 * np.pi, n, endpoint=False)
        return np.stack([r * np.cos(t), r * np.sin(t), 0 * t], 1)
    # Mercury: orbit-averaged radial component -> apsidal precession of a constant radial force
    pm = circle(0.387 * AU); am = acc(pm); dg = -np.mean(np.sum(am * pm, 1) / np.linalg.norm(pm, axis=1))
    prec = 2 * math.pi * dg * (0.387 * AU) ** 2 / GM * (100 / 0.2408) * 206264.8
    # Saturn: least-squares effective Q2 (Park convention a = Q2 (e(e.x) - x/3)) plus a free radial constant
    ps = circle(9.537 * AU); a_s = acc(ps)
    bQ = ps @ E_GC; Qb = bQ[:, None] * E_GC[None, :] - ps / 3; Rb = ps / np.linalg.norm(ps, axis=1)[:, None]
    Amat = np.stack([Qb.ravel(), Rb.ravel()], 1); coef, *_ = np.linalg.lstsq(Amat, a_s.ravel(), rcond=None)
    return {"a0_model": a0m, "x_e": xe, "s_e": float(se), "A_e": float(Ae), "L_e": float(Le), "sigma": sigma,
            "c": c, "c_over_scalar_ext": c / (a0m * se), "rV_stretched_pc": rVp / PC, "galaxy_flux_ratio_at_Rsun": float(gal_ratio),
            "mercury_prec_arcsec_cy": prec, "mercury_ok": prec <= PREC_MAX,
            "saturn_Q2_eff": float(coef[0]), "saturn_ok": Q2_LO <= coef[0] <= Q2_HI}

# ---------------- SPARC: door model vs live baseline (mu_std RAR at a0_fit) ----------------
def main(lams=(0.5, 1.0, 3.0, 11.0), Ks=tuple(np.logspace(37, 43, 13)), out_name="DOOR_NESTED_SOLUTION.json"):
    global base, gals
    FG = np.logspace(-0.5, 0.5, 61)
    gals = []
    for fpath in sorted(glob.glob(os.path.join(HERE, "../../02_galaxy_dynamics/sparc_data/*_rotmod.dat"))):
        d = np.loadtxt(fpath); gals.append((os.path.basename(fpath)[:-11], d))
    def xmu_inv(y):
        return np.sqrt((y**2 + y * np.sqrt(y**2 + 4)) / 2)
    def ghat(d):                                                       # (nF, npts) in m/s^2
        R, Vg, Vd, Vb = d[:, 0], d[:, 3], d[:, 4], d[:, 5]
        V2 = np.abs(Vg) * Vg + FG[:, None] * (0.5 * np.abs(Vd) * Vd + 0.7 * np.abs(Vb) * Vb)
        return np.maximum(V2, 1e-3) * 1e6 / (R * KPC)
    def chi2(d, gtot):
        R, V, eV = d[:, 0], d[:, 1], np.maximum(d[:, 2], 1.0)
        Vp = np.sqrt(gtot * R * KPC) / 1e3
        c = np.sum(((V - Vp) / eV) ** 2, 1) + (np.log10(FG) / 0.1) ** 2
        return float(c.min())
    base = {n: chi2(d, A0FIT * xmu_inv(ghat(d) / A0FIT)) for n, d in gals}
    def door_chi2(lam, K):
        eta, x, s, J1, f, L = tables(lam); a0m = eta * A0FIT
        out = {}
        for n, d in gals:
            gh = ghat(d); q = gh / a0m; r2 = (d[:, 0] * KPC) ** 2
            s0 = np.interp(q, f, s)                                    # unscreened (f monotone)
            lo, hi = np.zeros_like(s0), s0.copy()
            for _ in range(55):
                mid = 0.5 * (lo + hi); F = np.interp(mid, s, f) + K * mid**3 / r2 - q
                lo = np.where(F < 0, mid, lo); hi = np.where(F >= 0, mid, hi)
            out[n] = chi2(d, gh + a0m * 0.5 * (lo + hi)) - base[n]
        v = np.array(list(out.values()))
        return {"dchi2_total": float(v.sum()), "galaxies_dchi2>25": int((v > 25).sum()),
                "galaxies_dchi2<-25": int((v < -25).sum()),
                "worst": [(k, round(val, 1)) for k, val in sorted(out.items(), key=lambda t: -t[1])[:4]]}

    results = {"partA": part_a(), "chi2_baseline_live_mu_std": sum(base.values()), "runs": []}
    for lam in lams:
        for K in Ks:
            row = {"lambda_s": lam, "K_m2": float(K)}
            for ge in GES:
                row[f"sun_ge={ge:.1e}"] = sun_problem(lam, K, ge)
            row["sparc"] = door_chi2(lam, K)
            sun = [row[f"sun_ge={ge:.1e}"] for ge in GES]
            row["all_pass"] = all(u["mercury_ok"] and u["saturn_ok"] for u in sun) and row["sparc"]["dchi2_total"] <= 0
            results["runs"].append(row)
            print(f"lam={lam:5.2f} K={K:.1e} c={sun[0]['c']:.2e} rV'={sun[0]['rV_stretched_pc']:.2f}pc "
                  f"L={sun[0]['L_e']:.2f} prec={sun[0]['mercury_prec_arcsec_cy']:.1e} "
                  f"Q2={sun[0]['saturn_Q2_eff']:.1e}/{sun[1]['saturn_Q2_eff']:.1e} "
                  f"dchi2={row['sparc']['dchi2_total']:.0f} n>25={row['sparc']['galaxies_dchi2>25']} pass={row['all_pass']}", flush=True)
    json.dump(results, open(os.path.join(HERE, out_name), "w"), indent=1, default=float)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--lam0.2":
        main(lams=(0.2,), Ks=tuple(np.logspace(39, 42, 7)), out_name="DOOR_NESTED_SOLUTION_lam0.2.json")
    else:
        main()
