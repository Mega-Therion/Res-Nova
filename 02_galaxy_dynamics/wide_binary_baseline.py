#!/usr/bin/env python3
"""Remove the close-bin baseline mismatch from the Newton model.

In the 500–1000 AU bin the Newton median sits near 0.58 while the pairs
sit near 0.54. A single scale factor would cancel in the ratio. The
mismatch is removed here by one eccentricity offset, fit so the noisy
Newton median matches the close bin, then frozen at every separation.
"""

import json

import numpy as np

import wide_binary_fish as F

BINS = [
    (500, 1000),
    (1000, 2000),
    (2000, 5000),
    (5000, 10000),
    (10000, 20000),
    (20000, 30000),
]


def draw(s, sig, rng, dgamma, nmc=8):
    F.RNG = rng
    s_rep = np.repeat(s, nmc)
    sig_rep = np.repeat(sig, nmc)
    base = np.clip(0.4 + 0.45 * np.log10(np.maximum(s_rep, 1.0) / 100.0), 0.4, 1.3)
    gamma = np.clip(base + dgamma, 0.0, 2.0)
    _r, _r3, vsky, _P = F.kepler_mc(len(s_rep), gamma)
    vsky = vsky + rng.normal(size=vsky.shape) * sig_rep[:, None]
    vt = np.hypot(vsky[:, 0], vsky[:, 1])
    return vt[(vt > 0) & (vt < 5)]


def median_at(s, sig, vt, rng, dgamma, lo, hi):
    m = (s >= lo) & (s < hi)
    pred = draw(s[m], sig[m], rng, dgamma)
    obs = vt[m]
    obs = obs[(obs > 0) & (obs < 5)]
    return float(np.median(obs)), float(np.median(pred)), int(m.sum())


def fit_dgamma(s, sig, vt, rng):
    target, _, _ = median_at(s, sig, vt, rng, 0.0, 500, 2000)
    best, best_err = 0.0, 1e9
    for dgamma in np.linspace(-0.8, 0.8, 17):
        _o, pred, _n = median_at(s, sig, vt, rng, dgamma, 500, 2000)
        err = abs(pred - target)
        if err < best_err:
            best, best_err = float(dgamma), err
    return best, target


def main():
    rng = np.random.default_rng(23)
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    for name, cut in F.CUTS.items():
        b = F.prepare(catalog, cut)
        dgamma, target = fit_dgamma(b["s"], b["sig"], b["vt"], rng)
        rows = []
        for lo, hi in BINS:
            obs, pred, n = median_at(b["s"], b["sig"], b["vt"], rng, dgamma, lo, hi)
            rows.append(
                {"bin": [lo, hi], "n": n, "median_observed": obs, "median_newton": pred}
            )
        ao, an = rows[0]["median_observed"], rows[0]["median_newton"]
        for row in rows:
            row["R_observed"] = row["median_observed"] / ao
            row["R_newton"] = row["median_newton"] / an
            row["gap"] = row["R_observed"] - row["R_newton"]
        result[name] = {"dgamma": dgamma, "close_target": target, "rows": rows}
        print(name, "dgamma", round(dgamma, 3), "close", round(target, 3), flush=True)
        for row in rows:
            print(
                f"  {row['bin']}: obs {row['R_observed']:.3f} newton {row['R_newton']:.3f} gap {row['gap']:+.3f}",
                flush=True,
            )
    json.dump(result, open("WIDE_BINARY_BASELINE.json", "w"), indent=1)
    print("wrote WIDE_BINARY_BASELINE.json")


if __name__ == "__main__":
    main()
