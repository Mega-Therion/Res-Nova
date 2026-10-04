#!/usr/bin/env python3
"""Where the 2–5 kAU step sits, after the close-bin baseline is matched.

The close pairs agree with Newton once the eccentricity offset is frozen.
This script asks whether the step that starts at 2 kAU is carried by a
change in mass, distance, or chance-alignment, or whether it remains in
the velocities after those are matched.
"""

import json

import numpy as np

import wide_binary_fish as F


def select(c, cut):
    b = F.prepare(c, cut)
    p1, p2 = c["parallax1"], c["parallax2"]
    e1, e2 = c["parallax_error1"], c["parallax_error2"]
    w1, w2 = 1 / e1**2, 1 / e2**2
    plx = (p1 * w1 + p2 * w2) / (w1 + w2)
    d_pc = 1000 / plx
    # Rebuild the same acceptance mask prepare uses, by recomputing s and vt
    # and matching the surviving rows in order. prepare filters with ok &=.
    # Recompute s the same way and keep rows that survive a second pass of the
    # returned arrays' identity via a parallel mask built inside prepare's cuts.
    return b, d_pc, c["R_chance_align"], np.maximum(c["ruwe1"], c["ruwe2"])


def surviving_mask(c, cut, b):
    """Boolean mask into the catalog for the rows prepare kept, same order."""
    p1, p2 = c["parallax1"], c["parallax2"]
    e1, e2 = c["parallax_error1"], c["parallax_error2"]
    w1, w2 = 1 / e1**2, 1 / e2**2
    plx = (p1 * w1 + p2 * w2) / (w1 + w2)
    d_kpc = 1 / plx
    MG1 = c["phot_g_mean_mag1"] + 5 * np.log10(plx / 100)
    MG2 = c["phot_g_mean_mag2"] + 5 * np.log10(plx / 100)
    ok = (
        (c["R_chance_align"] <= cut["rca"])
        & (c["ruwe1"] < cut["ruwe"])
        & (c["ruwe2"] < cut["ruwe"])
        & (p1 / e1 > 50)
        & (p2 / e2 > 50)
        & (np.abs(p1 - p2) < 3 * np.hypot(e1, e2))
        & (d_kpc < 0.2)
        & (MG1 > 4)
        & (MG1 < 12)
        & (MG2 > 4)
        & (MG2 < 12)
        & np.isfinite(c["bp_rp1"])
        & np.isfinite(c["bp_rp2"])
    )
    br = np.concatenate([c["bp_rp1"][ok], c["bp_rp2"][ok]])
    mg = np.concatenate([MG1[ok], MG2[ok]])
    edges = np.arange(0.4, 3.6, 0.1)
    idx = np.digitize(br, edges)
    med = np.array(
        [
            np.median(mg[idx == i]) if np.sum(idx == i) > 20 else np.nan
            for i in range(1, len(edges))
        ]
    )
    cen = 0.5 * (edges[1:] + edges[:-1])
    good = np.isfinite(med)
    loc = lambda x: np.interp(x, cen[good], med[good], left=np.nan, right=np.nan)
    ok &= (np.abs(MG1 - loc(c["bp_rp1"])) < 0.8) & (
        np.abs(MG2 - loc(c["bp_rp2"])) < 0.8
    )
    r1, ea1, ed1 = F.unit_vectors(c["ra1"], c["dec1"])
    r2, ea2, ed2 = F.unit_vectors(c["ra2"], c["dec2"])
    theta = np.arccos(np.clip(np.sum(r1 * r2, -1), -1, 1))
    s_au = theta * 206264.806 * (d_kpc * 1000)
    v1 = F.K * d_kpc[:, None] * (c["pmra1"][:, None] * ea1 + c["pmdec1"][:, None] * ed1)
    v2 = F.K * d_kpc[:, None] * (c["pmra2"][:, None] * ea2 + c["pmdec2"][:, None] * ed2)
    rv1, rv2 = c["dr2_radial_velocity1"], c["dr2_radial_velocity2"]
    rve1, rve2 = c["dr2_radial_velocity_error1"], c["dr2_radial_velocity_error2"]
    have1, have2 = np.isfinite(rv1), np.isfinite(rv2)
    rv = np.where(have1, rv1, np.where(have2, rv2, 0.0))
    rv_sig = np.where(have1, rve1, np.where(have2, rve2, F.SIG_VR))
    rv_sig = np.where(np.isfinite(rv_sig), rv_sig, F.SIG_VR)
    V = v1 + rv[:, None] * r1
    P2V = V - np.sum(V * r2, -1)[:, None] * r2
    dv = v2 - P2V
    vt = np.hypot(np.sum(dv * ea2, -1), np.sum(dv * ed2, -1)) / (
        F.VC1
        * np.sqrt(
            (np.interp(MG1, F.MG_TAB, F.M_TAB) + np.interp(MG2, F.MG_TAB, F.M_TAB))
            / s_au
        )
    )
    sig_pm2 = (
        (F.K * d_kpc) ** 2
        * (
            c["pmra_error1"] ** 2
            + c["pmra_error2"] ** 2
            + c["pmdec_error1"] ** 2
            + c["pmdec_error2"] ** 2
        )
        / 2
    )
    sig_t = np.sqrt(sig_pm2 + (rv_sig * theta) ** 2 / 2) / (
        F.VC1
        * np.sqrt(
            (np.interp(MG1, F.MG_TAB, F.M_TAB) + np.interp(MG2, F.MG_TAB, F.M_TAB))
            / s_au
        )
    )
    ok &= np.isfinite(vt) & (sig_t < cut["sig"]) & (s_au > 500) & (s_au < 30000)
    extra = dict(
        d_pc=d_pc_from(plx)[ok],
        rca=c["R_chance_align"][ok],
        ruwe=np.maximum(c["ruwe1"], c["ruwe2"])[ok],
    )
    return ok, extra


def d_pc_from(plx):
    return 1000 / plx


def matched_step(s, vt, M, d, rca):
    """Match each 2–5 kAU pair to a 1–2 kAU pair in mass, distance, and chance."""
    near = (s >= 1000) & (s < 2000)
    far = (s >= 2000) & (s < 5000)
    near_i = np.where(near)[0]
    far_i = np.where(far)[0]
    used = np.zeros(len(near_i), dtype=bool)
    ratios = []
    for j in far_i:
        score = (
            (np.abs(M[near_i] - M[j]) / 0.15) ** 2
            + (np.abs(d[near_i] - d[j]) / 20) ** 2
            + (np.abs(np.log10(rca[near_i] + 1e-6) - np.log10(rca[j] + 1e-6))) ** 2
        )
        score[used] = 1e9
        k = int(np.argmin(score))
        if score[k] > 6:
            continue
        used[k] = True
        if vt[near_i[k]] > 0 and vt[j] < 5 and vt[near_i[k]] < 5:
            ratios.append(vt[j] / vt[near_i[k]])
    ratios = np.array(ratios)
    return {
        "n_matched": int(len(ratios)),
        "median_far_over_near": float(np.median(ratios)) if len(ratios) else None,
        "mean_far_over_near": float(np.mean(ratios)) if len(ratios) else None,
    }


def main():
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    for name, cut in F.CUTS.items():
        b = F.prepare(catalog, cut)
        _ok, extra = surviving_mask(catalog, cut, b)
        if len(extra["d_pc"]) != len(b["s"]):
            raise SystemExit(
                f"mask length {len(extra['d_pc'])} != {len(b['s'])} for {name}"
            )
        step = matched_step(b["s"], b["vt"], b["M"], extra["d_pc"], extra["rca"])
        result[name] = step
        print(name, step, flush=True)
    json.dump(result, open("WIDE_BINARY_STEP.json", "w"), indent=1)
    print("wrote WIDE_BINARY_STEP.json")


if __name__ == "__main__":
    main()
