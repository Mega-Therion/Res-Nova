#!/usr/bin/env python3
"""Conditional toy MCMC for the compressed Res Nova LLR + MICROSCOPE model.

This is not a full ephemeris or MICROSCOPE time-series fit. It samples two
summary parameters:
  eta_A : active Al/Fe-like composition parameter constrained by LLR summary
  dxi_P : non-universal passive metric coupling difference xi_Ti-xi_Pt
          with unit wall-response normalization F=1.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

RNG = np.random.default_rng(20261125)
N_WALKERS = 64
N_STEPS = 30000
BURN = 5000
THIN = 10

# Compressed data summaries used by the prior report.
Y_LLR = 0.0
SIGMA_LLR = 3.9e-14
Y_MIC = -1.5e-15
SIGMA_MIC = float(np.hypot(2.3e-15, 1.5e-15))
ETA_ACTIVE_SCAN_MIN = 9.02e-3

# Broad proper priors; the passive parameter is dimensionless for F=1.
ETA_A_MIN, ETA_A_MAX = -0.1, 0.1
DXI_MIN, DXI_MAX = -0.1, 0.1


def logpost(x: np.ndarray) -> float:
    eta_a, dxi = x
    if not (ETA_A_MIN <= eta_a <= ETA_A_MAX and DXI_MIN <= dxi <= DXI_MAX):
        return -np.inf
    # Summary model: eta_LLR = eta_a; eta_MIC = dxi * F, F=1.
    z_llr = (Y_LLR - eta_a) / SIGMA_LLR
    z_mic = (Y_MIC - dxi) / SIGMA_MIC
    return -0.5 * (z_llr * z_llr + z_mic * z_mic)


def summarize(samples: np.ndarray) -> dict:
    q = np.quantile(samples, [0.025, 0.16, 0.5, 0.84, 0.975], axis=0)
    eta = samples[:, 0]
    dxi = samples[:, 1]
    return {
        "quantiles": {
            "eta_A": {p: float(v) for p, v in zip(["2.5%", "16%", "50%", "84%", "97.5%"], q[:, 0])},
            "delta_xi_P_Ti_minus_Pt": {p: float(v) for p, v in zip(["2.5%", "16%", "50%", "84%", "97.5%"], q[:, 1])},
        },
        "posterior_probability_eta_A_ge_res_nova_scan_min": float(np.mean(eta >= ETA_ACTIVE_SCAN_MIN)),
        "posterior_probability_abs_delta_xi_ge_1e_minus_14": float(np.mean(np.abs(dxi) >= 1e-14)),
        "n_samples": int(samples.shape[0]),
        "sigma_llr": SIGMA_LLR,
        "sigma_mic": SIGMA_MIC,
        "wall_response_normalization_F": 1.0,
        "seed": 20261125,
    }


def main() -> None:
    # Initialize walkers close to the posterior scales but spread across both signs.
    x = np.column_stack([
        RNG.normal(0.0, 8.0 * SIGMA_LLR, N_WALKERS),
        RNG.normal(Y_MIC, 8.0 * SIGMA_MIC, N_WALKERS),
    ])
    lp = np.array([logpost(v) for v in x])
    chain = np.empty((N_STEPS, N_WALKERS, 2))
    accepted = 0
    total = 0
    # Proposal scales target the very different LLR and MICROSCOPE widths.
    step = np.array([2.0e-14, 1.0e-15])
    for t in range(N_STEPS):
        proposal = x + RNG.normal(size=x.shape) * step
        lp_new = np.array([logpost(v) for v in proposal])
        log_alpha = lp_new - lp
        take = np.log(RNG.random(N_WALKERS)) < log_alpha
        x[take] = proposal[take]
        lp[take] = lp_new[take]
        accepted += int(np.count_nonzero(take))
        total += N_WALKERS
        chain[t] = x
    post = chain[BURN::THIN].reshape(-1, 2)
    out = {
        "configuration": {
            "n_walkers": N_WALKERS,
            "n_steps": N_STEPS,
            "burn_in": BURN,
            "thin": THIN,
            "acceptance_fraction": accepted / total,
            "model": "eta_LLR=eta_A; eta_MIC=delta_xi_P with F=1",
            "warning": "Conditional summary-statistic posterior; not a full ephemeris or MICROSCOPE time-series fit.",
        },
        "summary": summarize(post),
    }
    path = Path(__file__).with_name("joint_toy_mcmc_results.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
