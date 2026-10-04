#!/usr/bin/env python3
"""Model the 2–5 kAU median shift as a hidden inner orbit.

Amendment B added 1.5 directly to the dimensionless ṽ and forced the
fraction to vanish at 1 kAU. The control bin then returned f_c = 0, and
the 4% shift at 2–5 kAU was untouched. That shift is in the peak, not
in a tail above ṽ = 2.

This model gives the inner orbit a fixed physical speed. The outer
circular speed falls as 1/sqrt(s), so the same companion moves the
dimensionless ṽ by more at larger separation. The fraction and the
inner speed are fit on the 500–2000 AU histogram only.

Written after the fish-rule result was known. It is a model of the
sample, not a blinded gravity verdict.
"""

import json

import numpy as np

import wide_binary_fish as F

VC1 = F.VC1  # km/s at 1 AU for 1 Msun
CTRL = (500.0, 2000.0)
BINS = [
    (500, 1000),
    (1000, 2000),
    (2000, 5000),
    (5000, 10000),
    (10000, 20000),
    (20000, 30000),
]


def f_of(s, f_c):
    return np.full(len(s), np.clip(f_c, 0.0, 0.5))


def apply_inner(vt, s, M, f_c, v_kms, rng):
    """Add a projected inner speed v_kms to a fraction f_c of draws."""
    take = rng.random(len(vt)) < f_of(s, f_c)
    out = np.array(vt, dtype=float, copy=True)
    v_outer = VC1 * np.sqrt(M / np.maximum(s, 1.0))
    extra = v_kms / v_outer
    out[take] = np.sqrt(out[take] ** 2 + extra[take] ** 2)
    return out


def newton_cloud(s, M, rng, nmc=6):
    import wide_binary_fish as wb

    wb.RNG = rng
    s_rep = np.repeat(s, nmc)
    M_rep = np.repeat(M, nmc)
    gamma = np.clip(0.4 + 0.45 * np.log10(s_rep / 100), 0.4, 1.3)
    _r, _r3, vsky, _P = wb.kepler_mc(len(s_rep), gamma)
    return np.hypot(vsky[:, 0], vsky[:, 1]), s_rep, M_rep


def fit_control(s, M, vt, rng):
    base_s, base_M = s, M
    cloud_v, cloud_s, cloud_M = newton_cloud(base_s, base_M, rng)
    obs = vt[(vt > 0) & (vt < 5)]
    best = (0.0, 0.3, -np.inf)
    for f_c in np.linspace(0, 0.5, 11):
        for v_kms in (0.2, 0.4, 0.8, 1.2):
            pred = apply_inner(cloud_v, cloud_s, cloud_M, f_c, v_kms, rng)
            pred = pred[pred < 5]
            hist, edges = np.histogram(pred, bins=30, range=(0, 5), density=True)
            hist = hist + 1e-6
            cen = 0.5 * (edges[1:] + edges[:-1])
            like = np.interp(obs, cen, hist, left=hist[0], right=hist[-1])
            score = float(np.sum(np.log(like)))
            if score > best[2]:
                best = (float(f_c), float(v_kms), score)
    return {"f_c": best[0], "v_kms": best[1], "loglike": best[2]}


def median_ratio(s, M, vt, f_c, v_kms, rng):
    rows = []
    for lo, hi in BINS:
        m = (s >= lo) & (s < hi)
        if m.sum() < 20:
            continue
        cloud_v, cloud_s, cloud_M = newton_cloud(s[m], M[m], rng, nmc=8)
        pred = apply_inner(cloud_v, cloud_s, cloud_M, f_c, v_kms, rng)
        obs = vt[m]
        obs = obs[obs < 5]
        rows.append(
            {
                "bin": [lo, hi],
                "n": int(m.sum()),
                "median_observed": float(np.median(obs)),
                "median_model": float(np.median(pred[pred < 5])),
            }
        )
    anchor = rows[0]["median_observed"]
    manchor = rows[0]["median_model"]
    for row in rows:
        row["R_observed"] = row["median_observed"] / anchor
        row["R_model"] = row["median_model"] / manchor
    return rows


def main():
    rng = np.random.default_rng(7)
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    for name, cut in F_CUTS:
        b = F.prepare(catalog, cut)
        m = (b["s"] >= CTRL[0]) & (b["s"] < CTRL[1])
        fit = fit_control(b["s"][m], b["M"][m], b["vt"][m], rng)
        rows = median_ratio(b["s"], b["M"], b["vt"], fit["f_c"], fit["v_kms"], rng)
        result[name] = {"fit": fit, "rows": rows}
        print(name, fit, flush=True)
        for row in rows:
            print(
                f"  {row['bin']}: obs {row['R_observed']:.3f} model {row['R_model']:.3f}",
                flush=True,
            )
    json.dump(result, open("WIDE_BINARY_EXCESS.json", "w"), indent=1)
    print("wrote WIDE_BINARY_EXCESS.json")


F = __import__("wide_binary_fish")
F_CUTS = list(F.CUTS.items())
CTRL = (500.0, 2000.0)

if __name__ == "__main__":
    main()
