"""Separation-dependent contaminants for the wide-binary test.

Pre-registered in PREREG_WIDE_BINARY_FISH.md, Amendment B.
This module does not read the Gaia catalog and does not refit R(s).

Two variants, never free at the same time.

T, hidden tertiary. A fraction
    f_t(s) = clip( f_c * log10(s / 1000 AU) / log10(30), 0, 0.50 )
grows from 0 at 1 kAU to f_c at 30 kAU. f_c is fit on the control bin
only (500–2000 AU), where every gravity model is Newtonian. A tagged
system keeps its outer Newtonian draw and adds an inner speed of 1.5
in quadrature. 1.5 is the middle of the ṽ excess Banik et al. 2024
place near 1–2. It is not fit. f_c is capped at 0.50 because direct
counts of close companions in local wide binaries lie below 50%
(Moe & Di Stefano 2017, as cited by Hernandez et al. 2024).

M, mass slope. The mass used in ṽ is wrong by (s / 1000 AU)^β.
ṽ scales as (s / 1000 AU)^(−β/2). β is fit on the control bin only,
and |β| ≤ 0.3.

A gravity verdict in the next run counts only if the same exclusion
holds with T and with M, parameters frozen from the control bin.
"""

import numpy as np

S_REF = 1000.0
S_MAX = 30000.0
V_INNER = 1.5
F_CAP = 0.50
BETA_CAP = 0.30


def f_triple(s, f_c):
    """Hidden-tertiary fraction at separation s (AU)."""
    slope = np.log10(np.maximum(s, 1.0) / S_REF) / np.log10(S_MAX / S_REF)
    return np.clip(f_c * slope, 0.0, F_CAP)


def add_tertiaries(vt, s, f_c, rng):
    """Quadrature-add a fixed inner speed to a fraction f_t(s) of draws."""
    take = rng.random(len(vt)) < f_triple(s, f_c)
    out = np.array(vt, copy=True)
    out[take] = np.sqrt(out[take] ** 2 + V_INNER**2)
    return out


def mass_factor(s, beta):
    """Multiplier on ṽ from a separation-dependent mass error."""
    beta = float(np.clip(beta, -BETA_CAP, BETA_CAP))
    return (np.maximum(s, 1.0) / S_REF) ** (-beta / 2)


def _newton_draws(s, rng, nmc=20):
    """Sky-projected Newtonian ṽ for random orbits, GM = a = 1."""
    import wide_binary_fish as wb

    wb.RNG = rng
    s_rep = np.repeat(s, nmc)
    gamma = np.clip(0.4 + 0.45 * np.log10(s_rep / 100), 0.4, 1.3)
    _rsky, _r3, vsky, _P = wb.kepler_mc(len(s_rep), gamma)
    return np.hypot(vsky[:, 0], vsky[:, 1]), s_rep


def fit_fc(s_control, vt_control, rng, grid=21):
    """Maximum likelihood f_c on the control bin. Gravity is Newtonian there."""
    base, s_rep = _newton_draws(s_control, rng)
    best, best_l = 0.0, -np.inf
    for f_c in np.linspace(0, 1, grid):
        pred = add_tertiaries(base, s_rep, f_c, rng)
        pred = pred[pred < 5]
        obs = vt_control[vt_control < 5]
        if len(pred) < 50 or len(obs) < 20:
            continue
        hist, edges = np.histogram(pred, bins=40, range=(0, 5), density=True)
        hist = hist + 1e-6
        centers = 0.5 * (edges[1:] + edges[:-1])
        like = np.interp(obs, centers, hist, left=hist[0], right=hist[-1])
        score = float(np.sum(np.log(like)))
        if score > best_l:
            best, best_l = float(f_c), score
    return best


def fit_beta(s_control, vt_control, rng):
    """Maximum likelihood mass slope on the control bin."""
    base, s_rep = _newton_draws(s_control, rng)
    best, best_l = 0.0, -np.inf
    obs = vt_control[vt_control < 5]
    for beta in np.linspace(-BETA_CAP, BETA_CAP, 25):
        pred = base * mass_factor(s_rep, beta)
        pred = pred[pred < 5]
        hist, edges = np.histogram(pred, bins=40, range=(0, 5), density=True)
        hist = hist + 1e-6
        centers = 0.5 * (edges[1:] + edges[:-1])
        like = np.interp(obs, centers, hist, left=hist[0], right=hist[-1])
        score = float(np.sum(np.log(like)))
        if score > best_l:
            best, best_l = float(beta), score
    return best


def smoke(seed=20261004):
    """Inject a known tertiary fraction. Recover it from the control bin only."""
    rng = np.random.default_rng(seed)
    s = np.concatenate(
        [
            rng.uniform(500, 2000, 2000),
            rng.uniform(2000, 5000, 800),
            rng.uniform(20000, 30000, 400),
        ]
    )
    truth = 0.40
    base, s_rep = _newton_draws(s, rng, nmc=8)
    injected = add_tertiaries(base, s_rep, truth, rng)
    control = (s_rep > 500) & (s_rep < 2000)
    outer = s_rep > 20000
    recovered = fit_fc(s_rep[control], injected[control], rng)
    pred_outer = add_tertiaries(base[outer], s_rep[outer], recovered, rng)
    ratio_true = np.median(injected[outer]) / np.median(injected[control])
    ratio_pred = np.median(pred_outer) / np.median(injected[control])
    return {
        "injected_f_c": truth,
        "recovered_f_c": recovered,
        "outer_median_ratio_injected": float(ratio_true),
        "outer_median_ratio_from_control_fit": float(ratio_pred),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(smoke(), indent=1))
