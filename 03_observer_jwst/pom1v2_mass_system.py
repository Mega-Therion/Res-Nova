#!/usr/bin/env python3
"""P-OM-1 v2: the lensing RAR with every input put on the system the observed a0 was measured on.

Pre-registered: 03_observer_jwst/PREREG_POM1V2_MASS_SYSTEM_2026-11-25.md (rule frozen before this script ran on data).

v1 (POM1_LENSING_RAR_RECORD_2026-11-25.md) compared the SPARC-calibrated a0 with lensing data whose baryonic masses
and distance scale were on a different system. v2 converts the lens side to the kinematic (SPARC) system, using the
conversions published by Mistele et al. 2024 (JCAP 04, 020, Sects. 3-4). None of them is fitted here:
  1. distance scale H0 = 73 (the SPARC/kinematic scale): g_obs,data x 73/70 (g_obs ~ DeltaSigma ~ h; g_bar is h-free);
  2. stellar masses on the kinematic SPS system (Schombert & McGaugh 2014): M* = Q M*_KiDS, Q_LTG = 1.0, Q_ETG = 1.4,
     with the colour split u - r = 2.5 (identical to B21's split);
  3. gas: late types keep B21's cold gas (Mistele: "practically indistinguishable"); early types carry hot gas from the
     X-ray scaling of Chae et al. 2021, M_hot = 10^-5.414 M*^1.47 (M* on the converted system), and no cold gas.
The gas terms depend on mass; they are evaluated at B21's isolated-sample mean log M*_KiDS = 10.61 (the colour
samples are mass-matched to 0.025 dex), with +-0.2 dex sensitivity reported. Each type's bins are relabelled
g_bar -> F_type g_bar, F = M_b(new) / M_b(B21), and the frozen v1 forward model (point mass, mu_std, a0 = 1.1607e-10,
B21's own DeltaSigma -> g estimator) is applied unchanged.

Output: POM1V2_MASS_SYSTEM.json
"""
import json, math

import numpy as np
from scipy.stats import chi2 as chi2_dist

import pom1_lensing_rar as P

H0_CONV = 73.0 / 70.0
LOGM_REP = 10.61
Q = {"LTG": 1.0, "ETG": 1.4}


def f_cold_b21(logm):
    return 10.0 ** (-0.69 * logm + 6.63)                       # B21 Eq. 23 (Boselli et al. 2014)


def F_type(kind, logm=LOGM_REP):
    ms = 10.0 ** logm
    old = ms * (1.0 + f_cold_b21(logm))                       # B21: stars + cold gas
    if kind == "LTG":
        return (Q["LTG"] * ms * (1.0 + f_cold_b21(logm))) / old
    mn = Q["ETG"] * ms
    return (mn + 10.0 ** -5.414 * mn ** 1.47) / old           # Mistele 2024 Eq. 4.1 (Chae et al. 2021)


def load_split(obs):
    b1 = P.load_esd(f"Fig-8_RAR-KiDS-isolated_{obs}bin_1.txt")      # lower u-r / lower n: late type
    b2 = P.load_esd(f"Fig-8_RAR-KiDS-isolated_{obs}bin_2.txt")      # higher u-r / higher n: early type
    C = P.load_cov(f"Fig-8_RAR-KiDS-isolated_{obs}bins_covmatrix.txt", [b1[0], b2[0]])
    return b1, b2, C


def joint(obs, logm=LOGM_REP, h0=True, a0=P.A0_OBS, v1_masses=False):
    (g1, y1, _), (g2, y2, _), C = load_split(obs)
    nr = len(g1)
    s = H0_CONV if h0 else 1.0
    k1 = np.where(g1 > P.GBAR_RELIABLE)[0]            # reliability set by the original bins (R < 0.3 Mpc/h70)
    k2 = np.where(g2 > P.GBAR_RELIABLE)[0]
    fl, fe = (1.0, 1.0) if v1_masses else (F_type("LTG", logm), F_type("ETG", logm))
    gl, ge = g1[k1] * fl, g2[k2] * fe
    d = np.concatenate([y1[k1], y2[k2]]) * s
    idx = np.concatenate([k1, k2 + nr])
    Cs = C[np.ix_(idx, idx)] * s * s
    gb = np.concatenate([gl, ge])

    def chi(pred):
        r = d - pred
        return float(r @ np.linalg.solve(Cs, r))

    n = len(d)
    out = {"n_bins": n, "F_LTG": fl, "F_ETG": fe, "logM_rep": logm, "H0_73": h0}
    c0 = chi(P.pred(gb, a0))
    out["chi2"], out["p"] = c0, float(chi2_dist.sf(c0, n))
    cN = chi(4.0 / math.pi * gb)
    out["newton_chi2"], out["newton_p"] = cN, float(chi2_dist.sf(cN, n))
    deltas = np.linspace(-P.MSTAR_SYS_DEX, P.MSTAR_SYS_DEX, 401)
    cs = [chi(P.pred(gb * 10.0 ** dl, a0)) for dl in deltas]
    k = int(np.argmin(cs))
    out["mass_shift_best_dex"], out["mass_shift_chi2"] = float(deltas[k]), float(cs[k])
    out["mass_shift_p"] = float(chi2_dist.sf(cs[k], n - 1))
    # per type, and early-minus-late residual difference with the joint covariance
    pl, pe = P.pred(gl, a0), P.pred(ge, a0)
    nl = len(k1)
    for name, sl, pr in (("late", slice(0, nl), pl), ("early", slice(nl, n), pe)):
        r = d[sl] - pr
        c = float(r @ np.linalg.solve(Cs[sl, sl], r))
        out[f"{name}_chi2"], out[f"{name}_p"] = c, float(chi2_dist.sf(c, len(r)))
        out[f"{name}_median_obs_over_pred"] = float(np.median(d[sl] / pr))
    common = np.intersect1d(k1, k2)
    il = np.searchsorted(k1, common)
    ie = nl + np.searchsorted(k2, common)
    rl, re_ = d[il] / P.pred(gb[il], a0), d[ie] / P.pred(gb[ie], a0)      # residual ratios per type
    # difference of fractional residuals; covariance propagated to first order
    J = np.zeros((len(common), n))
    for t, (a, b) in enumerate(zip(ie, il)):
        J[t, a] = 1.0 / P.pred(gb[[a]], a0)[0]
        J[t, b] = -1.0 / P.pred(gb[[b]], a0)[0]
    dd = re_ - rl
    Cd = J @ Cs @ J.T
    cd = float(dd @ np.linalg.solve(Cd, dd))
    out["early_minus_late"] = {"chi2": cd, "dof": int(len(common)), "p": float(chi2_dist.sf(cd, len(common))),
                               "median_log10_ratio": float(np.median(np.log10(re_ / rl)))}
    return out


def main():
    P.ensure_data()
    res = {"prereg": "03_observer_jwst/PREREG_POM1V2_MASS_SYSTEM_2026-11-25.md",
           "conversions": {"H0": "73 (g_obs x 73/70)", "Q": Q, "ETG_hot_gas": "M_hot = 10^-5.414 M*^1.47 (Chae+2021)",
                           "LTG_gas": "B21 cold gas", "logM_rep_KiDS": LOGM_REP},
           "primary_colour": joint("Color")}
    p = res["primary_colour"]
    if p["newton_p"] >= 1e-6:
        verdict = "NO_POWER"
    elif p["p"] >= 0.01:
        verdict = "PASS"
    elif p["mass_shift_p"] >= 0.01:
        verdict = "PASS_WITHIN_MASS_SYSTEMATIC"
    else:
        verdict = "FAIL"
    res["verdict"] = verdict
    res["diagnostics"] = {
        "sersic_split_same_conversion": joint("Sersic"),
        "colour_logM_minus_0.2": joint("Color", logm=LOGM_REP - 0.2),
        "colour_logM_plus_0.2": joint("Color", logm=LOGM_REP + 0.2),
        "colour_without_H0_conversion": joint("Color", h0=False),
        "colour_v1_masses_for_reference": joint("Color", h0=False, v1_masses=True),   # v1 inputs, same statistic
    }
    json.dump(res, open(P.HERE / "POM1V2_MASS_SYSTEM.json", "w"), indent=1)
    print("VERDICT:", verdict)
    print(f"joint chi2 = {p['chi2']:.2f} / {p['n_bins']}  p = {p['p']:.3g}  | late {p['late_chi2']:.1f}  early {p['early_chi2']:.1f}"
          f"  | early-late {p['early_minus_late']['chi2']:.1f}/{p['early_minus_late']['dof']} (p {p['early_minus_late']['p']:.3g})")


if __name__ == "__main__":
    main()
