#!/usr/bin/env python3
"""O3 pre-registered test: Omega_Lambda = ln 2 vs the Pantheon+ likelihood.

Implements exactly the frozen protocol in PREREG_OMEGA_LN2_PANTHEONPLUS.md:
Pantheon+ SH0ES, full STAT+SYS covariance, official zHD>0.01 cosmology cut,
flat LCDM, absolute magnitude M marginalized analytically (flat prior).
Verdict emitted from the frozen rule.

The likelihood construction mirrors the official
Pantheon+_only_cosmosis_likelihood.py from the data release:
  - only SNe with zHD > 0.01 are used, covariance trimmed to that set
  - comoving distance evaluated at zHD, luminosity factor (1+zHEL)
  - no extra scatter is added: the released STAT+SYS matrix is complete

Run: python3 omega_ln2_pantheonplus.py --dat <Pantheon+SH0ES.dat> --cov <Pantheon+SH0ES_STAT+SYS.cov>
Data: github.com/PantheonPlusSH0ES/DataRelease (NOT vendored in this repo).
"""
import argparse
import json
import math
import numpy as np

C_KMS = 299792.458
LN2 = math.log(2.0)


def load_data(dat_path):
    """Load all rows; return zhel, zhd, mbcorr in file order (pre-mask)."""
    with open(dat_path) as f:
        header = f.readline().split()
        idx = {n: i for i, n in enumerate(header)}
        rows = []
        for line in f:
            parts = line.split()
            if len(parts) != len(header):
                continue
            rows.append((parts[idx["zHEL"]], parts[idx["zHD"]], parts[idx["m_b_corr"]]))
    arr = np.array(rows, dtype=float)
    return arr[:, 0], arr[:, 1], arr[:, 2]  # zhel, zhd, mbcorr


def official_mask(zhd):
    """The official Pantheon+ cosmology likelihood uses zHD > 0.01
    (Pantheon+_only_cosmosis_likelihood.py: self.ww = data['zHD']>0.01)."""
    return zhd > 0.01


def load_cov(cov_path):
    with open(cov_path) as f:
        n = int(f.readline())
        cov = np.empty((n, n))
        k = 0
        for line in f:
            for v in line.split():
                cov[k // n, k % n] = float(v)
                k += 1
    assert k == n * n, f"cov read mismatch: {k} vs {n*n}"
    return cov


def comoving_distance_mpc(z, omegam, zmax, h0=70.0):
    """Flat LCDM comoving distance at z (global cumulative integral + interp)."""
    omegal = 1.0 - omegam
    zs = np.linspace(0.0, zmax, 200001)
    ez = np.sqrt(omegam * (1.0 + zs) ** 3 + omegal)
    dc_cum = np.concatenate(
        ([0.0], np.cumsum((1.0 / ez)[1:] + (1.0 / ez)[:-1]) * 0.5 * np.diff(zs))
    )
    dc_cum *= C_KMS / h0  # Mpc
    return np.interp(z, zs, dc_cum)


def chi2_marginalized(mu_obs, mu_model, cinv):
    """chi^2 with M marginalized analytically over a flat prior:
    delta^T C^-1 delta - (sum C^-1 delta)^2 / (sum C^-1)."""
    delta = mu_obs - mu_model
    cid = cinv @ delta
    return float(delta @ cid - (cid.sum() ** 2) / cinv.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dat", required=True)
    ap.add_argument("--cov", required=True)
    ap.add_argument("--out", default="O3_PANTHEONPLUS_RESULT.json")
    args = ap.parse_args()

    zhel_all, zhd_all, mb_all = load_data(args.dat)
    ww = official_mask(zhd_all)
    zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]
    cov_all = load_cov(args.cov)
    n_all = len(zhel_all)
    assert cov_all.shape == (n_all, n_all)
    cov = cov_all[np.ix_(ww, ww)]
    n = int(ww.sum())
    cinv = np.linalg.inv(cov)

    grid = np.round(np.arange(0.01, 0.9901, 0.001), 4)
    chi2 = np.empty_like(grid)
    zmax = float(np.max(zhd)) * 1.0000001
    for i, om in enumerate(grid):
        dc = comoving_distance_mpc(zhd, om, zmax)
        mu_model = 5.0 * np.log10((1.0 + zhel) * dc) + 25.0
        chi2[i] = chi2_marginalized(mb, mu_model, cinv)

    imin = int(np.argmin(chi2))
    chi2_min = float(chi2[imin])
    om_best = float(grid[imin])
    ol_best = 1.0 - om_best

    # pre-declared test point
    om_ln2 = 1.0 - LN2
    j = int(np.argmin(np.abs(grid - om_ln2)))
    chi2_ln2 = float(chi2[j])
    om_used = float(grid[j])

    delta_chi2 = chi2_ln2 - chi2_min
    sigma = math.sqrt(max(delta_chi2, 0.0))

    def interval(tol):
        mask = chi2 - chi2_min <= tol
        ols = 1.0 - grid[mask]
        return [float(np.min(ols)), float(np.max(ols))]

    verdict = "CONSISTENT" if delta_chi2 <= 9.0 else "TENSION"

    result = {
        "protocol": "PREREG_OMEGA_LN2_PANTHEONPLUS.md",
        "date": "2026-09-09",
        "epistemic_classification": "[D] Computed Empirical Benchmark (the ln 2 conjecture itself remains [O])",
        "data": {
            "source": "Pantheon+ SH0ES (Scolnic et al. 2022, arXiv:2202.04077)",
            "release": "github.com/PantheonPlusSH0ES/DataRelease, Pantheon+_Data/4_DISTANCES_AND_COVAR",
            "n_sne_total": n_all,
            "n_sne_after_official_cut": n,
            "official_cut": "zHD > 0.01 (Pantheon+_only_cosmosis_likelihood.py)",
            "covariance": "Pantheon+SH0ES_STAT+SYS.cov (full statistical+systematic), trimmed to the official masked set",
            "distance_convention": "comoving distance at zHD, luminosity factor (1+zHEL)",
            "nuisance": "absolute magnitude M marginalized analytically (flat prior)",
        },
        "model": {
            "family": "flat LCDM",
            "grid_omegam": [float(grid[0]), float(grid[-1]), 0.001],
        },
        "best_fit": {
            "omega_m": om_best,
            "omega_lambda": ol_best,
            "chi2_min": chi2_min,
            "dof": n - 2,
            "chi2_per_dof": chi2_min / (n - 2),
        },
        "hypothesis_ln2": {
            "omega_m_tested": om_used,
            "omega_lambda_tested": float(1.0 - om_used),
            "omega_lambda_declared": LN2,
            "chi2": chi2_ln2,
            "delta_chi2_vs_best": delta_chi2,
            "sigma_from_best_fit": sigma,
        },
        "omega_lambda_intervals": {
            "1sigma": interval(1.0),
            "2sigma": interval(4.0),
            "3sigma": interval(9.0),
        },
        "verdict_rule": "delta_chi2 <= 9 -> CONSISTENT (inside 3sigma); > 9 -> TENSION",
        "verdict": verdict,
        "quarantine_standing": "The conjecture Omega_Lambda = ln 2 remains [O]: a conjectured horizon boundary condition, not a derived density. This test does not promote it. Closure of O3 still requires a covariant action whose on-shell Friedmann constraint produces ln 2 without inserting it.",
    }
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result["best_fit"], indent=1))
    print(json.dumps(result["hypothesis_ln2"], indent=1))
    print("VERDICT:", verdict)


if __name__ == "__main__":
    main()
