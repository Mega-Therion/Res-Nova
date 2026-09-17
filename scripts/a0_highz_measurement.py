#!/usr/bin/env python3
"""
a0(z) measurement from high-z rotation-curve data (branch measure/a0-highz, 2026-09-16).

Sample: RC100 (Nestor Shachar+2023 Table 3) is the ONLY per-galaxy input to the likelihood.
RC41 (Genzel+2020) and G17 (Genzel+2017) are strict subsets (re-analyses of the same galaxies);
they are de-duplicated by RC100_idx, keeping the RC100 row.  RC41's photometric-input M_bar
(derived_logMbar_input) is used only for the prior-trend (w) test.  Ubler+2017 feeds only the
BTFR cross-check.  Ciocan+2026 (MUSE-DARK III) is an external comparison row, never merged.

Estimator: 02_galaxy_dynamics/highz_a0_method.py JointA0Likelihood (forward errors-in-variables,
intrinsic scatter profiled, population prior profiled), mu_std.  Model comparison sums the
per-bin profile Delta-chi2 curves; the T3 anchor enters once as a shared Gaussian nuisance in
ln a0(0).  Readings (Planck 2018 flat LCDM, as HORIZON_SELECTION_AUDIT): Hubble H(z)/H0,
Lambda-constant 1, Kodama [(1-q)H]/[(1-q0)H0], free power law (1+z)^n.

Tag of every a0(z) number here: [C] conditional on the Genzel-team GR+NFW dynamical fit
(fDM and tabulated M_bar are both outputs of that fit; the two routes are not independent).

Exit 0 iff all checks pass.  Sabotage hooks: the constants in the SABOTAGE block.
"""

import csv
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy import integrate, stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "02_galaxy_dynamics"))
import highz_a0_method as M  # noqa: E402

HZ = ROOT / "02_galaxy_dynamics" / "highz_data"

# ---------------------------------------------------------------- SABOTAGE block (all neutral)
DEDUPE_KEY = "RC100_idx"  # sabotage: "rc41_row" -> duplicates survive
SIM_TRUTH_SCALE = 1.0  # sabotage: 1.5 -> injected a0 != labelled truth
FIT_ERR_INFLATE = 1.0  # sabotage: 3.0 -> sensitivity collapses
SHUFFLE_ENABLED = True  # sabotage: False -> shuffle test becomes a no-op
# ----------------------------------------------------------------------------------------

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


# ---------------------------------------------------------------- cosmology / readings
PL_H0, PL_OM = 67.36, 0.3153


def E(z, Om=PL_OM):
    return math.sqrt(Om * (1 + z) ** 3 + 1 - Om)


def q_of_z(z, Om=PL_OM):
    Omz = Om * (1 + z) ** 3 / E(z, Om) ** 2
    return 1.5 * Omz - 1.0


def R_hubble(z):
    return E(z)


def R_lambda(z):
    return 1.0


def R_kodama(z):
    return (1 - q_of_z(z)) * E(z) / (1 - q_of_z(0.0))


READINGS = {"Hubble": R_hubble, "Lambda": R_lambda, "Kodama": R_kodama}


# ---------------------------------------------------------------- data
def read_csv(path):
    lines = [l for l in open(path) if not l.startswith("#")]
    return list(csv.DictReader(lines))


def dedupe():
    rc100 = read_csv(HZ / "RC100_NestorShachar2023_table3_transcribed.csv")
    rc41 = read_csv(HZ / "RC41_Genzel2020.csv")
    g17 = read_csv(HZ / "G17_Genzel2017.csv")
    by = {}
    for r in rc100:
        by[str(int(r["idx"]))] = ("RC100", r)
    added = {"RC41": 0, "G17": 0}
    bad_z = []
    for lab, rows in (("RC41", rc41), ("G17", g17)):
        for r in rows:
            key = r.get(DEDUPE_KEY, "NA")
            if key in ("NA", ""):
                key = f"{lab}-{r.get('rc41_row', r.get('galaxy'))}"
            if key in by:
                z100 = float(by[key][1]["z"])
                if abs(float(r["z"]) - z100) > 0.02:
                    bad_z.append((lab, key, r["z"], z100))
                continue
            by[key] = (lab, r)
            added[lab] += 1
    return by, added, bad_z, rc41


# ---------------------------------------------------------------- fitting helpers
GRID = math.log(M.load_anchor()["a0"]) + np.arange(
    math.log(0.25), math.log(7.0) + 1e-9, 0.02
)


def fit_view(v, route):
    return M.JointA0Likelihood(v, route).fit(GRID)


def info_weights(d, idx, a0):
    x = d["g_obs"][idx] / a0
    J = x / (1 + x * x) ** 1.5
    return J**2 / (d["e_fDM"][idx] ** 2 + J**2 * d["s_lng"][idx] ** 2)


def lnR_eff(fn, z, w):
    return float(np.sum(w * np.log([fn(zz) for zz in z])) / np.sum(w))


def compare(bins, lnA0, sig_anc, free_norm=False):
    """bins: list of dict(g, dchi, z, w). Returns per-reading chi2 (anchor nuisance profiled).
    free_norm=True drops the anchor: shape-only test (normalization A free, no z=0 pin)."""
    if free_norm:
        lnA = lnA0 + np.arange(-2.0, 2.5 + 1e-9, 0.005)
        pen = np.zeros_like(lnA)
    else:
        lnA = lnA0 + np.linspace(-4 * sig_anc, 4 * sig_anc, 161)
        pen = ((lnA - lnA0) / sig_anc) ** 2

    def chi_for(lnR_list):
        tot = pen.copy()
        for b, lr in zip(bins, lnR_list):
            tot += np.interp(lnA + lr, b["g"], b["dchi"], left=1e6, right=1e6)
        return float(tot.min())

    out = {}
    for name, fn in READINGS.items():
        out[name] = chi_for([lnR_eff(fn, b["z"], b["w"]) for b in bins])
    L1p = [float(np.sum(b["w"] * np.log1p(b["z"])) / np.sum(b["w"])) for b in bins]
    ns = np.arange(-3.0, 5.0 + 1e-9, 0.01)
    prof = np.array([chi_for([n * l for l in L1p]) for n in ns])
    i = int(np.argmin(prof))
    out["powerlaw"] = float(prof[i])
    d = prof - prof[i]
    inside68 = ns[d <= 1.0]
    inside95 = ns[d <= 3.841]
    out["n_hat"] = float(ns[i])
    out["n_ci68"] = [float(inside68.min()), float(inside68.max())]
    out["n_ci95"] = [float(inside95.min()), float(inside95.max())]
    out["n_edge"] = bool(
        i in (0, len(ns) - 1) or inside95.min() <= ns[0] or inside95.max() >= ns[-1]
    )
    return out


def run_pipeline(d, idx, zarr, edges, route, views=None):
    bins = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = idx[(zarr[idx] >= lo) & (zarr[idx] < hi)]
        if len(sel) < 5:
            continue
        v = views(sel) if views else M.data_view(d, sel, route)
        s = fit_view(v, route)
        w = info_weights(d, sel, M.load_anchor()["a0"])
        g, dchi = s["dchi2_fn"]
        bins.append(
            {
                "lo": lo,
                "hi": hi,
                "N": len(sel),
                "z": zarr[sel],
                "w": w,
                "g": g,
                "dchi": dchi,
                "fit": s,
            }
        )
    return bins


# Cross-method calibration nuisance (SPARC RAR extraction vs Genzel-team GR+NFW fDM), in ln a0.
# Size set by the helper's stated single-systematic shifts (fDM zero-point +-0.1, Vc +-5%: ~0.5 each).
SIG_CAL = 0.5
# Helper injection cov68 ~0.55 => effective half-width 0.755 sigma => dchi2 inflated by ~1/0.755^2 = 1.75.
COV_INFLATE = 1.75


def sigma_from_dchi2(dc, dof=1):
    p = stats.chi2.sf(max(dc, 0.0), dof)
    return p, float(stats.norm.isf(p / 2)) if p > 0 else float("inf")


def fmt_ci(ci, lnA0):
    return (
        "["
        + ", ".join("open" if c is None else f"{math.exp(c - lnA0):.3f}" for c in ci)
        + "]"
    )


def verdict(cmp_):
    fixed = {k: cmp_[k] for k in READINGS}
    best = min(fixed, key=fixed.get)
    return best


def report_variant(label, bins, lnA0, sig_anc, lines):
    c = compare(bins, lnA0, sig_anc)
    cf = compare(bins, lnA0, sig_anc, free_norm=True)
    c["shape"] = cf
    best = verdict(c)
    lines.append(f"--- variant: {label}")
    for b in bins:
        f = b["fit"]
        zeff = float(np.sum(b["w"] * b["z"]) / np.sum(b["w"]))
        lines.append(
            f"  z[{b['lo']:.1f},{b['hi']:.1f}) N={b['N']:3d} z_eff={zeff:.3f}  a0/a0_T3={math.exp(f['lna0_hat'] - lnA0):.3f}"
            f"  68%{fmt_ci(f['ci68'], lnA0)} 95%{fmt_ci(f['ci95'], lnA0)}  sig_int={f['sig_best']:.2f}"
            f"  edge={f['at_edge']}  pred H/L/K={R_hubble(zeff):.3f}/1.000/{R_kodama(zeff):.3f}"
        )
    # Review fix (2026-09-16): the reference power law's own goodness of fit, a Birge-rescaled
    # and a coverage-corrected significance, and a cross-method calibration nuisance on the anchor.
    nb = len(bins)
    dof_pl = nb + 1 - 2  # nb bins + anchor constraint, minus (A, n)
    pgof = stats.chi2.sf(c["powerlaw"], dof_pl) if dof_pl > 0 else float("nan")
    birge = max(1.0, c["powerlaw"] / dof_pl) if dof_pl > 0 else 1.0
    cc = compare(bins, lnA0, math.sqrt(sig_anc**2 + SIG_CAL**2))
    lines.append(
        f"  power-law GOF: chi2_min={c['powerlaw']:.2f} on {dof_pl} dof (p={pgof:.2e}); Birge factor {birge:.2f}"
    )
    for k in READINGS:
        dc = c[k] - c["powerlaw"]
        p, s = sigma_from_dchi2(dc)
        _, sb = sigma_from_dchi2(dc / birge)
        _, sc = sigma_from_dchi2(dc / COV_INFLATE)
        dcc = cc[k] - cc["powerlaw"]
        _, scal = sigma_from_dchi2(dcc)
        lines.append(
            f"  {k:7s} chi2={c[k]:8.2f}  dchi2 vs free-n={dc:7.2f} (stat-only nominal 1-dof {s:.2f} sig; Birge {sb:.2f};"
            f" cov68-corrected {sc:.2f}) | with anchor calib nuisance {SIG_CAL} ln: dchi2={dcc:.2f} ({scal:.2f} sig)"
        )
    lines.append(
        f"  [calib-nuisance fit] n={cc['n_hat']:.2f} 95%[{cc['n_ci95'][0]:.2f},{cc['n_ci95'][1]:.2f}]; best fixed reading: {verdict(cc)}"
        "  (1-dof sigmas on non-nested readings are indicative only; not bootstrap-calibrated)"
    )
    lines.append(
        f"  power law n={c['n_hat']:.2f} 68%[{c['n_ci68'][0]:.2f},{c['n_ci68'][1]:.2f}] 95%[{c['n_ci95'][0]:.2f},{c['n_ci95'][1]:.2f}]"
        f" chi2={c['powerlaw']:.2f} edge={c['n_edge']}"
    )
    lr = c["Lambda"] - c["Hubble"]
    lines.append(
        f"  Hubble vs Lambda: chi2_L - chi2_H = {lr:+.2f} (LR = {math.exp(min(max(lr / 2, -700), 700)):.3g} for Hubble);"
        f" Kodama vs Lambda: {c['Lambda'] - c['Kodama']:+.2f};  favored fixed reading: {best}"
    )
    cf = c["shape"]
    lines.append(
        f"  SHAPE-ONLY (anchor dropped, normalization free): chi2 Hubble={cf['Hubble']:.2f} Lambda={cf['Lambda']:.2f}"
        f" Kodama={cf['Kodama']:.2f}; free n={cf['n_hat']:.2f} 95%[{cf['n_ci95'][0]:.2f},{cf['n_ci95'][1]:.2f}]"
        f"; chi2_L-chi2_H={cf['Lambda'] - cf['Hubble']:+.2f}; favored shape: {verdict(cf)}"
    )
    return c, best


# ---------------------------------------------------------------- simulation-based checks
def simulate_bins(
    d, idx, zarr, edges, truth_fn, a0_anchor, err_scale, rng, route="fdm"
):
    gbar = d["gbar_a"][idx]
    a0_i = a0_anchor * np.array([truth_fn(z) for z in zarr[idx]]) * SIM_TRUTH_SCALE
    err = {
        "s_lnV": d["s_lnV"][idx] * err_scale,
        "s_lnR": d["s_lnR"][idx] * err_scale,
        "s_f": d["e_fDM"][idx] * err_scale,
        "s_lnM": d["s_lnM"][idx] * err_scale,
    }
    n = len(idx)
    lngt = np.log(M.g_pred(gbar, a0_i)) + 0.1 * rng.standard_normal(n)
    lng = (
        lngt
        + 2 * err["s_lnV"] * rng.standard_normal(n)
        - err["s_lnR"] * rng.standard_normal(n)
    )
    s_lng = np.sqrt((2 * err["s_lnV"]) ** 2 + err["s_lnR"] ** 2)
    f = 1 - gbar / np.exp(lngt) + err["s_f"] * rng.standard_normal(n)
    pos = {int(j): k for k, j in enumerate(idx)}

    def views(sel):
        kk = [pos[int(j)] for j in sel]
        return {"lng": lng[kk], "s_lng": s_lng[kk], "f": f[kk], "s_f": err["s_f"][kk]}

    return views


def _sim_job(args):
    seed, truth, err_scale, shuffle = args
    d = M.load_rc100()
    anc = M.load_anchor()
    idx = np.arange(100)
    rng = np.random.default_rng(seed)
    views = simulate_bins(
        d, idx, d["z"], [0.0, 1.2, 9.0], READINGS[truth], anc["a0"], err_scale, rng
    )
    zfit = d["z"].copy()
    if shuffle and SHUFFLE_ENABLED:
        zfit = rng.permutation(zfit)
    # bins are selected on zfit; views are keyed by galaxy index, so shuffling z breaks the association
    dd = dict(d)
    bins = run_pipeline(dd, idx, zfit, [0.0, 1.2, 9.0], "fdm", views=views)
    lnA0 = math.log(anc["a0"])
    sig = math.log(anc["ci68"][1] / anc["ci68"][0]) / 2
    c = compare(bins, lnA0, sig)
    c["shape"] = compare(bins, lnA0, sig, free_norm=True)
    lnR_true = [lnR_eff(READINGS[truth], b["z"], b["w"]) for b in bins]
    bias = [
        b["fit"]["lna0_hat"] - (lnA0 + lr)
        for b, lr in zip(bins, lnR_true)
    ]
    return {
        "c": c,
        "bias": bias,
        "cover95": [
            (b["fit"]["ci95"][0] or -9e9) <= lnA0 + lr <= (b["fit"]["ci95"][1] or 9e9)
            for b, lr in zip(bins, lnR_true)
        ],
    }


def run_sims(truth, n, err_scale=1.0, shuffle=False, seed0=0, jobs=8):
    from multiprocessing import Pool

    with Pool(jobs) as p:
        return p.map(
            _sim_job, [(seed0 + i, truth, err_scale, shuffle) for i in range(n)]
        )


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    anc = M.load_anchor()
    A0 = anc["a0"]
    lnA0 = math.log(A0)
    sig_anc = math.log(anc["ci68"][1] / anc["ci68"][0]) / 2
    sig_anc95 = math.log(anc["ci95"][1] / anc["ci95"][0]) / (2 * 1.96)
    sig_anc = max(sig_anc, sig_anc95)
    out = []
    print("=" * 100)
    print(
        "a0_highz_measurement.py  (2026-09-16, branch measure/a0-highz)  all a0(z) numbers are [C]"
    )
    print("=" * 100)
    print(
        f"anchor T3: a0={A0:.5e}  68%={anc['ci68']}  95%={anc['ci95']}  sigma_ln(anchor)={sig_anc:.4f}"
    )

    print("\nCHECKS (data / provenance / readings)")
    check(
        "C0 anchor is T3 non-flow (1.16306e-10, 95% [0.96640,1.32393]e-10)",
        abs(A0 / 1.1630564344814754e-10 - 1) < 1e-12 and anc["n_galaxies"] == 78,
    )
    r = subprocess.run(
        ["bash", str(ROOT / "scripts" / "fetch_highz_data.sh")],
        capture_output=True,
        text=True,
    )
    check(
        "C1 source-hash provenance (file hash only, NOT cell values): sha256 of cached sources match CSV headers (fetch_highz_data.sh exit 0)",
        r.returncode == 0,
        f"exit={r.returncode}; "
        + "; ".join(
            l.split(":")[0]
            for l in r.stdout.splitlines()
            if l[:4] in ("PASS", "FAIL", "HAND", "MISS")
        ),
    )
    rh = [R_hubble(z) for z in (0.5, 1, 2)]
    rk = [R_kodama(z) for z in (0.5, 1, 2)]
    check(
        "C2 readings reproduce HORIZON_SELECTION values (H 1.323/1.791/3.034, K 0.942/0.962/1.214)",
        max(
            abs(a - b)
            for a, b in zip(rh + rk, [1.323, 1.791, 3.034, 0.942, 0.962, 1.214])
        )
        < 0.002,
        f"H={[round(x, 3) for x in rh]} K={[round(x, 3) for x in rk]}",
    )
    by, added, bad_z, rc41 = dedupe()
    n_unique = len(by)
    check(
        "C3 dedupe: RC41 (41) and G17 (6) all map onto RC100 rows (z agree <0.02); unique galaxies == 100",
        n_unique == 100 and added == {"RC41": 0, "G17": 0} and not bad_z,
        f"unique={n_unique} added={added} z-mismatch={len(bad_z)}",
    )

    d = M.load_rc100()
    check(
        "C4 RC100 transcription internal check (Sigma_DM recomputed) >= 93/100",
        int(d["sigmaDM_ok"].sum()) >= 93,
        f"{int(d['sigmaDM_ok'].sum())}/100",
    )
    idx = np.arange(100)
    z = d["z"]
    lines = []

    # regime
    x_all = d["g_obs"] / A0
    gbx = d["gbar_a"] / A0
    lines.append(
        f"REGIME: g_obs/a0_T3 median {np.median(x_all):.2f} [16-84% {np.percentile(x_all, 16):.2f},{np.percentile(x_all, 84):.2f}],"
        f" frac x<1: {np.mean(x_all < 1):.2f}; g_bar(fDM)/a0 median {np.median(gbx):.2f}, frac<1: {np.mean(gbx < 1):.2f}"
    )

    EDGES4 = [0.6, 1.0, 1.5, 2.0, 2.6]
    EDGES2 = [0.0, 1.2, 9.0]
    headline = {}
    for route in ("fdm", "mbar"):
        for lab, edges in (
            ("2bin z<1.2|>=1.2 [headline]", EDGES2),
            ("4bin 0.6-1.0-1.5-2.0-2.6", EDGES4),
        ):
            bins = run_pipeline(d, idx, z, edges, route)
            c, best = report_variant(
                f"route={route} {lab} nominal", bins, lnA0, sig_anc, lines
            )
            headline[(route, lab[:4])] = (c, best, bins)

    # systematics: M* and gas +-0.2 dex (prior-dominated limit w=1 for fDM route; direct for M_bar route)
    rc100rows = read_csv(HZ / "RC100_NestorShachar2023_table3_transcribed.csv")
    fstar = np.clip(
        10 ** (np.array([float(r["logMstar"]) for r in rc100rows]) - d["logMbar"]),
        0.0,
        1.0,
    )
    sysrows = []
    for comp in ("Mstar", "gas"):
        frac = fstar if comp == "Mstar" else 1 - fstar
        for dex in (+0.2, -0.2):
            dlnM = np.log(frac * 10**dex + (1 - frac))
            for route in ("fdm", "mbar"):

                def views(sel, route=route, dlnM=dlnM):
                    v = M.data_view(d, sel, route)
                    if route == "fdm":
                        v["f"] = 1 - (1 - v["f"]) * np.exp(dlnM[sel])
                    else:
                        v["lngb"] = v["lngb"] + dlnM[sel]
                    return v

                bins = run_pipeline(d, idx, z, EDGES2, route, views=views)
                c, best = report_variant(
                    f"route={route} 2bin {comp} {dex:+.1f} dex"
                    + (" (w=1 prior-dominated)" if route == "fdm" else ""),
                    bins,
                    lnA0,
                    sig_anc,
                    lines,
                )
                sysrows.append((route, comp, dex, best, c["n_hat"], c["n_ci95"], verdict(c["shape"]), c["shape"]["n_ci95"]))
    lines.append(
        "  (fDM route at w=0, data-dominated: mass shifts leave fDM unchanged -> identical to nominal, exactly)"
    )

    # prior-trend (w) test on the 41 RC41 galaxies with photometric-input M_bar
    rows41 = [
        (int(r["RC100_idx"]) - 1, float(r["derived_logMbar_input"]))
        for r in rc41
        if r["RC100_idx"] not in ("NA", "")
    ]
    ii = np.array([a for a, _ in rows41])
    lgb_prior = np.log(
        d["k_used"][ii]
        * M.GM_SUN
        * 10 ** np.array([b for _, b in rows41])
        / (d["Re_kpc"][ii] * M.KPC) ** 2
    )
    L1 = np.log1p(z)
    sl_prior = np.polyfit(L1[ii], lgb_prior - np.log(d["g_obs"][ii]), 1)[0]
    sl_fit = np.polyfit(L1, np.log(d["gbar_a"] / d["g_obs"]), 1)[0]
    lines.append(
        f"PRIOR-TREND TEST: d ln(g_bar/g_obs)/d ln(1+z): photometric-input prior (RC41 n={len(ii)}) {sl_prior:+.3f};"
        f" fitted (RC100 fDM) {sl_fit:+.3f}. A recovered a0(z) trend that tracks the prior's own trend is not separable from the prior [O]."
    )

    # BTFR cross-check
    ub = read_csv(HZ / "Ubler2017_KMOS3D_TFR.csv")
    uz = np.array([float(r["z"]) for r in ub])
    uV = np.array([float(r["Vcirc_max_kms"]) for r in ub])
    uM = np.array([float(r["logMbar"]) for r in ub])
    a_btfr_u = (uV * 1e3) ** 4 / (M.GM_SUN * 10**uM) / A0
    btfr_rc = (d["Vc_kms"] * 1e3) ** 4 / (M.GM_SUN * 10 ** d["logMbar"]) / A0
    zp = math.log(73.0 / 67.36)
    lines.append(
        "BTFR CROSS-CHECK (distance-dependent, a0_BTFR ∝ D_L^-2; H0-convention zp systematic 2 ln(73/67.36) = "
        f"{2 * zp:.3f} in ln a0, PR #67):"
    )
    for lo, hi in ((0.6, 1.1), (1.1, 1.8), (1.8, 2.7)):
        s = (uz >= lo) & (uz < hi)
        s2 = (z >= lo) & (z < hi)
        lines.append(
            f"  z[{lo},{hi}) Ubler N={s.sum():3d} median V^4/(G M_bar)/a0_T3 = {np.median(a_btfr_u[s]):.2f};"
            f" RC100 N={s2.sum():3d} median = {np.median(btfr_rc[s2]):.2f}"
        )
    lines.append(
        "  Deep-MOND conversion V^4 = G M a0 needs g/a0 << 1; RC100 (same KMOS3D/SINS parent population) has frac x<1 = "
        f"{np.mean(x_all < 1):.2f} -> NOT CONVERTIBLE. Numbers above are regime-biased (Newtonian-regime V^4/GM >> a0) and are not a0."
    )
    tf = read_csv(HZ / "HighZ_TF_published_fits.csv")
    for r in tf:
        if r["relation"] == "bTFR" and r["offset_vs_z0"]:
            lines.append(
                f"  Ubler bTFR {r['sample']} z~{r['z_typical']}: offset {r['offset_vs_z0']} dex vs Lelli+16 ->"
                f" formal deep-MOND ratio 10^(-offset) = {10 ** (-float(r['offset_vs_z0'])):.2f} [NOT CONVERTIBLE: regime]"
            )
    cio = {
        (r["quantity"], r["model"]): r
        for r in read_csv(HZ / "Ciocan2026_MUSEDARKIII_a0.csv")
    }
    cr = cio[("a0_z~1", "DC14 halo (fiducial)")]
    lines.append(
        f"EXTERNAL (not merged): Ciocan+2026 MUSE-DARK III a0(z~1) = {cr['value']} +{cr['err_plus']}/-{cr['err_minus']} e-10 (95% CI; LCDM"
        f" decomposition) -> /a0_T3 = {float(cr['value']) * 1e-10 / A0:.2f}; vs the paper's own local 1.2e-10 = {float(cr['value']) / 1.2:.2f}"
    )

    print("\nRESULTS")
    for l in lines:
        print(l)
    print(
        "\nSYSTEMATICS SUMMARY (2-bin): route, component, shift, favored fixed reading, n, n 95%"
    )
    for s in sysrows:
        print(
            f"  {s[0]:4s} {s[1]:5s} {s[2]:+.1f}  {s[3]:7s} n={s[4]:+.2f} 95%[{s[5][0]:+.2f},{s[5][1]:+.2f}]  | shape-only favored {s[6]:7s} n95%[{s[7][0]:+.2f},{s[7][1]:+.2f}]"
        )

    # ------------------------------------------------------------ simulation checks
    NS = 24
    print(
        f"\nSIMULATION CHECKS (RC100 error sizes, true g_bar = fDM-route values, sigma_int=0.1, {NS} realizations each, 2-bin)"
    )
    simL = run_sims("Lambda", NS, seed0=100)
    simH = run_sims("Hubble", NS, seed0=200)
    bias = np.array([b for s in simL + simH for b in s["bias"]])
    sep = math.log(M.HUBBLE_Z1_RATIO)
    check(
        "C5 injection-recovery: |median per-bin ln a0 bias| < sep/8 (sep = ln 1.791 = 0.583; threshold set a priori)",
        abs(np.median(bias)) < sep / 8,
        f"median bias {np.median(bias):+.4f}, sd {np.std(bias):.3f}, cov95 {np.mean([c for s in simL + simH for c in s['cover95']]):.2f}",
    )
    rejH = np.mean([s["c"]["Hubble"] - s["c"]["powerlaw"] > 3.841 for s in simL])
    rejL = np.mean([s["c"]["Lambda"] - s["c"]["powerlaw"] > 3.841 for s in simH])
    check(
        "C6 [unverified guard: errors x3 sabotage did not fire] sensitivity: Lambda-truth data reject Hubble form at 95% in >= 80% of realizations",
        rejH >= 0.8,
        f"rate {rejH:.2f}",
    )
    check(
        "C7 [unverified guard: errors x3 sabotage did not fire] sensitivity: Hubble-truth data reject Lambda-constant at 95% in >= 80% of realizations",
        rejL >= 0.8,
        f"rate {rejL:.2f}",
    )
    nL = np.array([s["c"]["n_hat"] for s in simL])
    check(
        "C8 Lambda-truth: median fitted n within 0.3 of 0",
        abs(np.median(nL)) < 0.3,
        f"median n {np.median(nL):+.2f}",
    )
    simS = run_sims("Hubble", NS, shuffle=True, seed0=300)
    covS = np.mean([s["c"]["shape"]["n_ci95"][0] <= 0 <= s["c"]["shape"]["n_ci95"][1] for s in simS])
    covU = np.mean([s["c"]["shape"]["n_ci95"][0] <= 0 <= s["c"]["shape"]["n_ci95"][1] for s in simH])
    check(
        "C9 z-label shuffle on Hubble-truth data: shape-only n 95% CI covers 0 in >= 80% (unshuffled covers 0 in <= 20%)",
        covS >= 0.8 and covU <= 0.2,
        f"shuffled {covS:.2f}, unshuffled {covU:.2f}",
    )

    npass = sum(ok for _, ok in RESULTS)
    print(f"\nCHECKS: {npass}/{len(RESULTS)} pass; runtime {time.time() - t0:.0f}s")
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
