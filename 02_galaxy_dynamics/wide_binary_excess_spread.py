#!/usr/bin/env python3
"""Refit the 2–5 kAU excess with a spread of inner speeds.

The single-speed model pinned to 0.2 km/s. Here each hidden companion
draws an inner speed from a lognormal. The median speed and the log-spread
are free. Two fits:

- Control-frozen: median, spread, and fraction are fit on 500–2000 AU only,
  then the outer bins are a prediction.
- Free-scale: the same three parameters are fit to the median trend in
  every bin. That uses the outer bins, so it is a description, not a
  blinded test.
"""

import json

import numpy as np

import wide_binary_fish as F

VC1 = F.VC1
BINS = [
    (500, 1000),
    (1000, 2000),
    (2000, 5000),
    (5000, 10000),
    (10000, 20000),
    (20000, 30000),
]
F_GRID = np.linspace(0.0, 0.5, 6)
V_GRID = np.array([0.1, 0.2, 0.35, 0.5, 0.8, 1.2, 2.0])
SIG_GRID = np.array([0.3, 0.6, 1.0])


def apply_spread(vt, s, M, f_c, v_med, sigma, rng):
    take = rng.random(len(vt)) < np.clip(f_c, 0.0, 0.5)
    out = np.array(vt, dtype=float, copy=True)
    v_draw = v_med * np.exp(sigma * rng.normal(size=len(vt)))
    extra = v_draw / (VC1 * np.sqrt(M / np.maximum(s, 1.0)))
    out[take] = np.sqrt(out[take] ** 2 + extra[take] ** 2)
    return out


def newton_cloud(s, M, rng, nmc=6):
    F.RNG = rng
    s_rep = np.repeat(s, nmc)
    M_rep = np.repeat(M, nmc)
    gamma = np.clip(0.4 + 0.45 * np.log10(s_rep / 100.0), 0.4, 1.3)
    _r, _r3, vsky, _P = F.kepler_mc(len(s_rep), gamma)
    return np.hypot(vsky[:, 0], vsky[:, 1]), s_rep, M_rep


def loglike(obs, pred):
    obs = obs[(obs > 0) & (obs < 5)]
    pred = pred[(pred > 0) & (pred < 5)]
    if len(obs) < 20 or len(pred) < 50:
        return -np.inf
    hist, edges = np.histogram(pred, bins=30, range=(0, 5), density=True)
    hist = hist + 1e-6
    cen = 0.5 * (edges[1:] + edges[:-1])
    like = np.interp(obs, cen, hist, left=hist[0], right=hist[-1])
    return float(np.sum(np.log(like)))


def fit_control(s, M, vt, rng):
    cloud_v, cloud_s, cloud_M = newton_cloud(s, M, rng)
    obs = vt[(vt > 0) & (vt < 5)]
    best = None
    for f_c in F_GRID:
        for v_med in V_GRID:
            for sigma in SIG_GRID:
                pred = apply_spread(cloud_v, cloud_s, cloud_M, f_c, v_med, sigma, rng)
                score = loglike(obs, pred)
                if best is None or score > best["loglike"]:
                    best = {
                        "f_c": float(f_c),
                        "v_med_kms": float(v_med),
                        "sigma_log": float(sigma),
                        "loglike": score,
                    }
    return best


def ratios(s, M, vt, f_c, v_med, sigma, rng):
    rows = []
    for lo, hi in BINS:
        m = (s >= lo) & (s < hi)
        if int(m.sum()) < 20:
            continue
        cloud_v, cloud_s, cloud_M = newton_cloud(s[m], M[m], rng, nmc=8)
        pred = apply_spread(cloud_v, cloud_s, cloud_M, f_c, v_med, sigma, rng)
        obs = vt[m]
        obs = obs[(obs > 0) & (obs < 5)]
        rows.append(
            {
                "bin": [lo, hi],
                "n": int(m.sum()),
                "median_observed": float(np.median(obs)),
                "median_model": float(np.median(pred[(pred > 0) & (pred < 5)])),
            }
        )
    anchor_o = rows[0]["median_observed"]
    anchor_m = rows[0]["median_model"]
    for row in rows:
        row["R_observed"] = row["median_observed"] / anchor_o
        row["R_model"] = row["median_model"] / anchor_m
    return rows


def fit_free(s, M, vt, rng):
    """Pick the spread that best matches the median trend in every bin."""
    best = None
    for f_c in F_GRID:
        for v_med in V_GRID:
            for sigma in SIG_GRID:
                rows = ratios(s, M, vt, f_c, v_med, sigma, rng)
                resid = sum((r["R_observed"] - r["R_model"]) ** 2 for r in rows[1:])
                if best is None or resid < best["residual"]:
                    best = {
                        "f_c": float(f_c),
                        "v_med_kms": float(v_med),
                        "sigma_log": float(sigma),
                        "residual": float(resid),
                        "rows": rows,
                    }
    return best


def main():
    rng = np.random.default_rng(11)
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    for name, cut in F.CUTS.items():
        b = F.prepare(catalog, cut)
        m = (b["s"] >= 500) & (b["s"] < 2000)
        frozen = fit_control(b["s"][m], b["M"][m], b["vt"][m], rng)
        frozen_rows = ratios(
            b["s"],
            b["M"],
            b["vt"],
            frozen["f_c"],
            frozen["v_med_kms"],
            frozen["sigma_log"],
            rng,
        )
        free = fit_free(b["s"], b["M"], b["vt"], rng)
        result[name] = {
            "control_frozen": {**frozen, "rows": frozen_rows},
            "free_scale": free,
        }
        print(
            name,
            "frozen",
            {k: frozen[k] for k in ("f_c", "v_med_kms", "sigma_log")},
            flush=True,
        )
        for row in frozen_rows:
            print(
                f"  frozen {row['bin']}: obs {row['R_observed']:.3f} model {row['R_model']:.3f}",
                flush=True,
            )
        print(
            name,
            "free",
            {k: free[k] for k in ("f_c", "v_med_kms", "sigma_log", "residual")},
            flush=True,
        )
        for row in free["rows"]:
            print(
                f"  free {row['bin']}: obs {row['R_observed']:.3f} model {row['R_model']:.3f}",
                flush=True,
            )
    json.dump(result, open("WIDE_BINARY_EXCESS_SPREAD.json", "w"), indent=1)
    print("wrote WIDE_BINARY_EXCESS_SPREAD.json")


if __name__ == "__main__":
    main()
