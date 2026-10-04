#!/usr/bin/env python3
"""Newton model with measurement noise and an eccentricity error.

The excess scripts drew noiseless orbits from one gamma(s). The data carry
a per-binary velocity error, and Hwang+2022 gamma(s) is not known exactly.
Here gamma is gamma(s) plus a normal error of 0.3, the shift already used
as the sensitivity width, clipped to [0, 2]. Each sky component then gets
the binary's own sigma.

This does not refit a gravity law. It asks whether the 2-5 kAU median
rise is what noisy, uncertain-eccentricity Newton already produces.
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
GAMMA_ERR = 0.3


def gamma_draw(s, rng, err):
    base = np.clip(0.4 + 0.45 * np.log10(np.maximum(s, 1.0) / 100.0), 0.4, 1.3)
    if err == 0:
        return base
    return np.clip(base + rng.normal(0.0, err, size=len(s)), 0.0, 2.0)


def newton_vt(s, sig, rng, nmc=8, gamma_err=0.0, noise=False):
    F.RNG = rng
    s_rep = np.repeat(s, nmc)
    sig_rep = np.repeat(sig, nmc)
    gamma = gamma_draw(s_rep, rng, gamma_err)
    _r, _r3, vsky, _P = F.kepler_mc(len(s_rep), gamma)
    if noise:
        vsky = vsky + rng.normal(size=vsky.shape) * sig_rep[:, None]
    vt = np.hypot(vsky[:, 0], vsky[:, 1])
    return vt, s_rep


def ratios(s, sig, vt, rng, gamma_err, noise):
    rows = []
    for lo, hi in BINS:
        m = (s >= lo) & (s < hi)
        if int(m.sum()) < 20:
            continue
        pred, _ = newton_vt(s[m], sig[m], rng, gamma_err=gamma_err, noise=noise)
        obs = vt[m]
        obs = obs[(obs > 0) & (obs < 5)]
        pred = pred[(pred > 0) & (pred < 5)]
        rows.append(
            {
                "bin": [lo, hi],
                "n": int(m.sum()),
                "median_observed": float(np.median(obs)),
                "median_newton": float(np.median(pred)),
            }
        )
    ao, an = rows[0]["median_observed"], rows[0]["median_newton"]
    for row in rows:
        row["R_observed"] = row["median_observed"] / ao
        row["R_newton"] = row["median_newton"] / an
    return rows


def main():
    rng = np.random.default_rng(19)
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    variants = (
        ("bare", 0.0, False),
        ("noise", 0.0, True),
        ("eccentricity", GAMMA_ERR, False),
        ("noise_and_eccentricity", GAMMA_ERR, True),
    )
    for name, cut in F.CUTS.items():
        b = F.prepare(catalog, cut)
        result[name] = {}
        print("==", name, flush=True)
        for label, err, noise in variants:
            rows = ratios(b["s"], b["sig"], b["vt"], rng, err, noise)
            result[name][label] = rows
            for row in rows:
                if row["bin"][0] < 2000:
                    continue
                print(
                    f"  {label} {row['bin']}: obs {row['R_observed']:.3f} newton {row['R_newton']:.3f}",
                    flush=True,
                )
    json.dump(
        {"gamma_err": GAMMA_ERR, "cuts": result},
        open("WIDE_BINARY_NEWTON_ERRORS.json", "w"),
        indent=1,
    )
    print("wrote WIDE_BINARY_NEWTON_ERRORS.json")


if __name__ == "__main__":
    main()
