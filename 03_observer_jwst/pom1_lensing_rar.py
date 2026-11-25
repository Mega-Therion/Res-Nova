#!/usr/bin/env python3
"""P-OM-1: the weak-lensing RAR (KiDS-1000, Brouwer et al. 2021) against the optical map's phantom-lensing prediction.

Pre-registered: 03_observer_jwst/PREREG_POM1_LENSING_RAR_2026-11-25.md (rule frozen before the data comparison).

Forward model (no free parameter). Each lens is a baryonic point mass M (valid at the measured radii, R > 30 kpc;
B21 Sect. 2.4). The single-metric potential is the galaxy-tier law, mu_std with the observed a0:
    g(r) = nu(gN/a0) gN,  gN = GM/r^2,  nu(y) = sqrt((1 + sqrt(1 + 4/y^2))/2)   (inverse of mu = x/sqrt(1+x^2)).
The total enclosed mass is M3(<r) = r^2 g/G = M N(x), with x = r/r_M, r_M = sqrt(GM/a0) and N(x) = nu(1/x^2).
That mass (point mass plus the phantom density) is projected exactly into the excess surface density DeltaSigma(R),
and then converted with B21's own Eq. 7, g_lens = 4 G DeltaSigma. The prediction is therefore the same estimator
that was applied to the data, so B21's SIS-conversion bias does not enter the comparison.
In units of a0, with X = R/r_M and y = g_bar/a0 = 1/X^2:
    4 G DeltaSigma / a0 = (4/pi) [ y (N(X) + I1(X)) - I2(X)/2 ],
    I1 = int_X^inf N'(x) (1 - sqrt(1 - X^2/x^2)) dx,   I2 = int_X^inf N'(x) dx / (x sqrt(x^2 - X^2)).
Limits: deep MOND gives sqrt(y) exactly (the SIS conversion is exact there); the Newtonian point mass gives (4/pi) y.

Usage: python3 pom1_lensing_rar.py [--validate-model-only]
Output: POM1_LENSING_RAR.json (full run)
"""
import hashlib, io, json, math, sys, tarfile, urllib.request
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "04_cosmology" / "external_data" / "brouwer2021_rar"   # gitignored external-data cache
TAR_URL = "https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar"
TAR_SHA256 = "73adc2d4e848fa0a6a43187f7b5447e749b92eaec4a795b9902b0beaf8a78733"

A0_OBS = 1.1607e-10      # [E] SPARC-175 mu_std fit, canonical observed a0 (CURRENT_STATE, 2026-11-19)
A0_DER = 1.0422e-10      # [D] cH0/(2 pi) at H0 = 67.4, the theoretical anchor
G_PC = 4.52e-30          # pc^3 / (Msun s^2), B21 README value
PC_M = 3.086e16          # m per pc, B21 README value
ESD_TO_G = 4.0 * G_PC * PC_M      # (Msun/pc^2) -> m/s^2, B21 Eq. 7
GBAR_RELIABLE = 7.56e-14          # B21 Sect. 4.1: R < 0.3 Mpc/h70 at mean log Mgal = 10.69 (isolation reliable)
MSTAR_SYS_DEX = 0.2               # B21 Sect. 3.2: systematic stellar-mass band


# ----------------------------------------------------------------------------------------------------- model
def N(x):
    """M3(<r)/M = nu(1/x^2) for mu_std."""
    return math.sqrt((1.0 + math.sqrt(1.0 + 4.0 * x**4)) / 2.0)


def dN(x):
    return 2.0 * x**3 / (N(x) * math.sqrt(1.0 + 4.0 * x**4))


def lens_F(y):
    """4 G DeltaSigma / a0 for a point mass under mu_std, at g_bar/a0 = y (projected radius X = y^-1/2)."""
    X = 1.0 / math.sqrt(y)
    # x = X cosh t removes the endpoint singularity; both integrands decay like exp(-t).
    # (1 - tanh t) sinh t is written as tanh(t) exp(-t) to avoid cancellation at large t.
    i1 = quad(lambda t: dN(X * math.cosh(t)) * math.tanh(t) * math.exp(-t) * X, 0.0, 60.0,
              limit=400, epsabs=0.0, epsrel=1e-11)[0]
    i2 = quad(lambda t: dN(X * math.cosh(t)) / (X * math.cosh(t)), 0.0, 60.0,
              limit=400, epsabs=0.0, epsrel=1e-11)[0]
    return (4.0 / math.pi) * (y * (N(X) + i1) - 0.5 * i2)


_LOGY = np.linspace(-9.0, 5.0, 1401)
_LOGF = None


def lens_F_interp(y):
    """Cubic interpolation of log F on a 0.01-dex grid (validated against lens_F in --validate-model-only)."""
    global _LOGF
    if _LOGF is None:
        _LOGF = np.log10([lens_F(10.0**ly) for ly in _LOGY])
    from scipy.interpolate import CubicSpline
    spl = CubicSpline(_LOGY, _LOGF)
    return 10.0 ** spl(np.log10(y))


def brute_force_deltasigma(X):
    """Independent check: project the phantom density directly, without the I1/I2 identities.
    Units M = r_M = 1, so a0 = G M / r_M^2 = 1 in units with G = 1 and 4 G DeltaSigma / a0 = 4 DeltaSigma."""
    rho = lambda r: dN(r) / (4.0 * math.pi * r * r)                     # phantom density (point mass excluded)
    sig = lambda R: 2.0 * quad(lambda z: rho(math.hypot(R, z)), 0.0, np.inf, limit=400, epsrel=1e-10)[0]
    inner = quad(lambda R: 2.0 * math.pi * R * sig(R), 0.0, X, limit=200, epsrel=1e-9)[0]
    sigbar = (1.0 + inner) / (math.pi * X * X)                            # + the baryonic point mass
    return 4.0 * (sigbar - sig(X))


def validate_model():
    out = {}
    out["deep_mond_limit"] = {f"y={y:g}": lens_F(y) / math.sqrt(y) for y in (1e-8, 1e-6, 1e-4)}
    out["newton_limit"] = {f"y={y:g}": lens_F(y) / (4.0 / math.pi * y) for y in (1e3, 1e4)}
    bf = {}
    for X in (0.5, 1.0, 3.0, 10.0):
        y = 1.0 / X**2
        bf[f"X={X:g}"] = {"I1I2_formula": lens_F(y), "brute_force": brute_force_deltasigma(X)}
        bf[f"X={X:g}"]["rel_diff"] = bf[f"X={X:g}"]["brute_force"] / bf[f"X={X:g}"]["I1I2_formula"] - 1.0
    out["brute_force_projection"] = bf
    ys = 10.0 ** (np.linspace(-6.5, -1.0, 23) + 0.005)          # midway between grid nodes
    out["interp_max_rel_err"] = float(max(abs(lens_F_interp(y) / lens_F(y) - 1.0) for y in ys))
    # the SIS-conversion factor the forward model carries relative to the plain RAR nu(y) y
    out["F_over_nu_y"] = {f"y={y:g}": lens_F(y) / (N(1.0 / math.sqrt(y)) * y) for y in (1e-5, 1e-3, 1e-2, 1e-1, 1.0)}
    ok = (all(abs(v - 1) < 1e-4 for v in out["deep_mond_limit"].values())
          and all(abs(v - 1) < 1e-3 for v in out["newton_limit"].values())
          and all(abs(v["rel_diff"]) < 1e-5 for v in bf.values())
          and out["interp_max_rel_err"] < 1e-6)
    out["model_checks_pass"] = bool(ok)
    return out


# ----------------------------------------------------------------------------------------------------- data
def ensure_data():
    need = ["Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"]
    if all((DATA / f).exists() for f in need):
        return
    DATA.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(TAR_URL, headers={"User-Agent": "research-script"})
    blob = urllib.request.urlopen(req, timeout=180).read()
    got = hashlib.sha256(blob).hexdigest()
    if got != TAR_SHA256:
        sys.exit(f"brouwer2021_rar.tar sha256 mismatch: {got}")
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
        members = [m for m in tf.getmembers() if m.isfile() and not Path(m.name).name.startswith("._")]
        tf.extractall(DATA, members=members, filter="data")


def load_esd(name):
    a = np.loadtxt(DATA / name, comments="#")
    gbar, esd, err, bias = a[:, 0], a[:, 1], a[:, 3], a[:, 4]
    return gbar, ESD_TO_G * esd / bias, ESD_TO_G * err / bias


def load_cov(name, gbar_by_bin):
    """Full covariance (bias-corrected, in (m/s^2)^2). gbar_by_bin: list of g_bar arrays, one per observable bin."""
    a = np.loadtxt(DATA / name, comments="#")
    mins = sorted(set(a[:, 0]))
    nb, nr = len(gbar_by_bin), len(gbar_by_bin[0])
    C = np.zeros((nb * nr, nb * nr))
    for m_, n_, gi, gj, cov, _corr, bias in a:
        m, n = mins.index(m_), mins.index(n_)
        i = int(np.argmin(abs(np.log(gbar_by_bin[m] / gi))))
        j = int(np.argmin(abs(np.log(gbar_by_bin[n] / gj))))
        C[m * nr + i, n * nr + j] = cov / bias * ESD_TO_G**2
    return C


# ----------------------------------------------------------------------------------------------------- stats
def chi2(d, p, C):
    r = d - p
    return float(r @ np.linalg.solve(C, r))


def pred(gbar, a0):
    return a0 * lens_F_interp(gbar / a0)


def a0_scan(gbar, gobs, C):
    grid = 10.0 ** np.linspace(np.log10(0.2e-10), np.log10(5e-10), 3001)
    c = np.array([chi2(gobs, pred(gbar, a), C) for a in grid])
    k = int(np.argmin(c))
    inside = grid[c <= c[k] + 1.0]
    return {"a0_best": float(grid[k]), "chi2_min": float(c[k]), "a0_1sigma": [float(inside.min()), float(inside.max())],
            "dof": len(gbar) - 1, "p_at_best": float(chi2_dist.sf(c[k], len(gbar) - 1))}


def verdict_block(gbar, gobs, C, label):
    n = len(gbar)
    res = {"label": label, "n_bins": n, "gbar_range": [float(gbar.min()), float(gbar.max())]}
    for name, a0 in (("a0_obs_1.1607", A0_OBS), ("a0_der_1.0422", A0_DER)):
        c = chi2(gobs, pred(gbar, a0), C)
        res[name] = {"chi2": c, "dof": n, "p": float(chi2_dist.sf(c, n)),
                     "median_obs_over_pred": float(np.median(gobs / pred(gbar, a0)))}
    cN = chi2(gobs, 4.0 / math.pi * gbar, C)
    res["newton_point_mass"] = {"chi2": cN, "dof": n, "p": float(chi2_dist.sf(cN, n)),
                                "median_obs_over_pred": float(np.median(gobs / (4.0 / math.pi * gbar)))}
    # mass-systematic profile: uniform log shift delta of g_bar within B21's band, a0 fixed at the observed value
    deltas = np.linspace(-MSTAR_SYS_DEX, MSTAR_SYS_DEX, 401)
    cs = np.array([chi2(gobs, pred(gbar * 10.0**dl, A0_OBS), C) for dl in deltas])
    k = int(np.argmin(cs))
    res["mass_shift_profile_a0_obs"] = {"delta_dex_best": float(deltas[k]), "chi2_min": float(cs[k]), "dof": n - 1,
                                        "p": float(chi2_dist.sf(cs[k], n - 1))}
    res["a0_fit"] = a0_scan(gbar, gobs, C)
    res["a0_fit_mass_minus_0.2dex"] = a0_scan(gbar * 10**-MSTAR_SYS_DEX, gobs, C)["a0_best"]
    res["a0_fit_mass_plus_0.2dex"] = a0_scan(gbar * 10**MSTAR_SYS_DEX, gobs, C)["a0_best"]
    return res


def main():
    if "--validate-model-only" in sys.argv:
        print(json.dumps(validate_model(), indent=1))
        return
    out = {"prereg": "03_observer_jwst/PREREG_POM1_LENSING_RAR_2026-11-25.md",
           "data": {"source": "Brouwer et al. 2021, A&A 650, A113 (arXiv:2106.11677), KiDS-1000 data release",
                    "url": TAR_URL, "sha256": TAR_SHA256},
           "model_validation": validate_model()}
    if not out["model_validation"]["model_checks_pass"]:
        sys.exit("model validation failed; no data comparison run")
    ensure_data()

    # ---- primary + S1: KiDS-bright isolated lenses, stars + cold gas
    g, y, e = load_esd("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
    C = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", [g])
    out["diag_err_vs_cov"] = float(np.max(abs(np.sqrt(np.diag(C)) / e - 1.0)))
    rel = g > GBAR_RELIABLE
    idx = np.where(rel)[0]
    out["primary"] = verdict_block(g[rel], y[rel], C[np.ix_(idx, idx)], "KiDS isolated, g_bar > 7.56e-14 (R < 0.3 Mpc)")
    out["S1_all_bins"] = verdict_block(g, y, C, "KiDS isolated, all 15 bins (below 7.56e-14 satellites can add ~30%)")
    out["bins"] = [{"gbar": float(a), "gobs": float(b), "err": float(c), "pred_a0_obs": float(pred(np.array([a]), A0_OBS)[0]),
                    "reliable_isolation": bool(a > GBAR_RELIABLE)} for a, b, c in zip(g, y, e)]

    # ---- S2: hot-gas variant of g_bar (B21's rough estimate: isothermal hot gas, M_gas = M_star within 100 kpc)
    gh, yh, eh = load_esd("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
    Ch = load_cov("Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt", [gh])
    relh = gh > GBAR_RELIABLE
    ih = np.where(relh)[0]
    out["S2_hot_gas"] = verdict_block(gh[relh], yh[relh], Ch[np.ix_(ih, ih)], "KiDS isolated, g_bar incl. hot-gas estimate")

    # ---- S3: early/late split (diagnostic only; isolation criterion decides this, see prereg)
    for obs in ("Color", "Sersic"):
        b1 = load_esd(f"Fig-8_RAR-KiDS-isolated_{obs}bin_1.txt")
        b2 = load_esd(f"Fig-8_RAR-KiDS-isolated_{obs}bin_2.txt")
        Cj = load_cov(f"Fig-8_RAR-KiDS-isolated_{obs}bins_covmatrix.txt", [b1[0], b2[0]])
        nr = len(b1[0])
        blk = {}
        for k, (gg, yy, _ee) in enumerate((b1, b2)):
            r = gg > GBAR_RELIABLE
            ii = np.where(r)[0] + k * nr
            blk[f"bin_{k + 1}"] = verdict_block(gg[r], yy[r], Cj[np.ix_(ii, ii)], f"{obs} bin {k + 1}")
        # bin 1 minus bin 2 on the radial bins where both are in the reliable range (joint covariance)
        both = np.where((b1[0] > GBAR_RELIABLE) & (b2[0] > GBAR_RELIABLE))[0]
        i1, i2 = both, both + nr
        Cd = Cj[np.ix_(i1, i1)] + Cj[np.ix_(i2, i2)] - Cj[np.ix_(i1, i2)] - Cj[np.ix_(i2, i1)]
        d = b1[1][both] - b2[1][both]
        cd = float(d @ np.linalg.solve(Cd, d))
        blk["bin1_minus_bin2"] = {"chi2": cd, "dof": int(len(both)), "p": float(chi2_dist.sf(cd, len(both))),
                                  "median_log10_ratio_bin2_over_bin1": float(np.median(np.log10(b2[1][both] / b1[1][both])))}
        out[f"S3_{obs.lower()}_split"] = blk

    # ---- verdict, exactly as pre-registered (Sect. 4)
    p = out["primary"]
    if p["newton_point_mass"]["p"] >= 1e-6:
        verdict = "NO_POWER"
    elif p["a0_obs_1.1607"]["p"] >= 0.01:
        verdict = "PASS"
    elif p["mass_shift_profile_a0_obs"]["p"] >= 0.01:
        verdict = "PASS_WITHIN_MASS_SYSTEMATIC"
    else:
        verdict = "FAIL"
    out["verdict"] = verdict
    json.dump(out, open(HERE / "POM1_LENSING_RAR.json", "w"), indent=1)

    print(f"VERDICT: {verdict}")
    print(f"primary chi2 = {p['a0_obs_1.1607']['chi2']:.2f} / {p['n_bins']}  p = {p['a0_obs_1.1607']['p']:.3g}")
    print(f"newton  chi2 = {p['newton_point_mass']['chi2']:.1f}  p = {p['newton_point_mass']['p']:.3g}")
    print(f"a0 fit = {p['a0_fit']['a0_best']:.4g}  1sig {p['a0_fit']['a0_1sigma']}")


if __name__ == "__main__":
    main()
