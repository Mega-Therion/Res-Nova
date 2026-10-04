#!/usr/bin/env python3
"""Run the step-tracking tests under Amendment A of PREREG_WIDE_BINARY_STEP.md.

Usage: python3 wide_binary_step_track_amended.py <eb21_cols.npz> [<eem_mg_m.npy>]
Output: WIDE_BINARY_STEP_TRACK_AMENDED.json
"""

import json
import sys

import numpy as np

import wide_binary_fish as F
import wide_binary_step as S

AU_BINS = [
    (500, 1000),
    (1000, 2000),
    (2000, 5000),
    (5000, 10000),
    (10000, 20000),
    (20000, 30000),
]
G_EDGES = [2.0**k for k in range(-3, 10)]  # units of a0
NMIN = 100
THRESH = 1.03
NBOOT = 1000


def boot_ratio_se(a, b, rng):
    ra = rng.choice(a, (NBOOT, len(a)))
    rb = rng.choice(b, (NBOOT, len(b)))
    return float(np.std(np.median(ra, 1) / np.median(rb, 1)))


def rows_and_cross(x, vt, bins, ref_mask, rng, decreasing=False, ref_mid=None):
    """Rows over bins of x, R relative to the reference set, and the 1.03 crossing."""
    good = (vt > 0) & (vt < 5)
    ref = vt[ref_mask & good]
    rows = []
    if len(ref) < NMIN:
        return rows, None, "reference_too_small"
    mref = np.median(ref)
    for lo, hi in bins:
        m = (x >= lo) & (x < hi) & good
        n = int(m.sum())
        row = {"bin": [lo, hi], "n": n, "mid": float(np.sqrt(lo * hi))}
        if n >= NMIN:
            v = vt[m]
            R = float(np.median(v) / mref)
            se = boot_ratio_se(v, ref, rng)
            row.update(R=R, se=se, step=bool(R >= THRESH and (R - 1) >= 2 * se))
        rows.append(row)
    seq = sorted(rows, key=lambda r: r["mid"], reverse=decreasing)
    prev_x, prev_R = ref_mid, 1.0
    for r in seq:
        if "R" not in r:
            continue
        if r["step"]:
            if prev_x is None:
                return rows, None, "first_measured_bin_is_step"
            # linear in log(x) between prev and this bin
            t = (THRESH - prev_R) / (r["R"] - prev_R) if r["R"] != prev_R else 0.0
            t = min(max(t, 0.0), 1.0)
            lx = np.log(prev_x) + t * (np.log(r["mid"]) - np.log(prev_x))
            return rows, float(np.exp(lx)), "ok"
        prev_x, prev_R = r["mid"], r["R"]
    return rows, None, "no_step"


def decide(Q, P, names):
    if Q is None:
        return "inconclusive"
    a, b = abs(np.log(Q)), abs(np.log(Q / P))
    if a < b and a <= np.log(1.2):
        return names[0]
    if b < a and b <= np.log(1.2):
        return names[1]
    return "inconclusive"


def slice_cross(b, m, rng):
    s, vt = b["s"][m], b["vt"][m]
    ref = (s >= 500) & (s < 1000)
    rows, x, status = rows_and_cross(s, vt, AU_BINS[1:], ref, rng, ref_mid=float(np.sqrt(500 * 1000)))
    return rows, x, status


def g_rows(b, m, rng):
    s, vt, M = b["s"][m], b["vt"][m], b["M"][m]
    g = F.GN_1AU * M / s**2 / F.A0
    ref = (s >= 500) & (s < 1000)
    bins = [(G_EDGES[i], G_EDGES[i + 1]) for i in range(len(G_EDGES) - 1)]
    return rows_and_cross(g, vt, bins, ref, rng, decreasing=True, ref_mid=float(np.median(g[ref])))


def run(catalog, mam=None):
    out = {}
    for name, cut in F.CUTS.items():
        rng = np.random.default_rng(20261004)
        b = F.prepare(catalog, cut)
        _ok, extra = S.surviving_mask(catalog, cut, b)
        assert len(extra["d_pc"]) == len(b["s"])
        d = extra["d_pc"]
        # Test 1
        near, far = d < 100, d >= 100
        t1 = {}
        for lab, m in (("under_100pc", near), ("100_to_200pc", far)):
            rows, x, st = slice_cross(b, m, rng)
            t1[lab] = dict(
                n=int(m.sum()),
                median_d=float(np.median(d[m])),
                rows=rows,
                s_cross=x,
                status=st,
            )
        P1 = t1["100_to_200pc"]["median_d"] / t1["under_100pc"]["median_d"]
        xs = [t1[k]["s_cross"] for k in ("under_100pc", "100_to_200pc")]
        Q1 = xs[1] / xs[0] if None not in xs else None
        t1["P1"], t1["Q"] = P1, Q1
        t1["decision"] = decide(Q1, P1, ("tracks_AU", "tracks_arcseconds"))
        # Test 2
        light, heavy = b["M"] < 1.0, b["M"] >= 1.5
        t2 = {}
        for lab, m in (("light", light), ("heavy", heavy)):
            rows, x, st = slice_cross(b, m, rng)
            grows, gx, gst = g_rows(b, m, rng)
            t2[lab] = dict(
                n=int(m.sum()),
                median_M=float(np.median(b["M"][m])),
                rows=rows,
                s_cross=x,
                status=st,
                g_rows=grows,
                g_cross_a0=gx,
                g_status=gst,
            )
        P2 = np.sqrt(t2["heavy"]["median_M"] / t2["light"]["median_M"])
        xs = [t2[k]["s_cross"] for k in ("light", "heavy")]
        Q2 = xs[1] / xs[0] if None not in xs else None
        t2["P2"], t2["Q"] = float(P2), Q2
        t2["decision"] = decide(Q2, P2, ("tracks_AU", "tracks_acceleration"))
        if mam is not None:
            keep = (F.MG_TAB, F.M_TAB)
            F.MG_TAB, F.M_TAB = mam
            bm = F.prepare(catalog, cut)
            F.MG_TAB, F.M_TAB = keep
            t2["P2_mamajek"] = float(
                np.sqrt(
                    np.median(bm["M"][bm["M"] >= 1.5])
                    / np.median(bm["M"][bm["M"] < 1.0])
                )
            )
        out[name] = dict(test1=t1, test2=t2)
        print(
            name,
            "T1",
            t1["decision"],
            "Q",
            Q1,
            "P1",
            round(P1, 3),
            [
                (k, t1[k]["status"], t1[k]["s_cross"])
                for k in ("under_100pc", "100_to_200pc")
            ],
        )
        print(
            name,
            "T2",
            t2["decision"],
            "Q",
            Q2,
            "P2",
            round(float(P2), 3),
            [
                (k, t2[k]["status"], t2[k]["s_cross"], t2[k]["g_cross_a0"])
                for k in ("light", "heavy")
            ],
            flush=True,
        )
    out["decision_strict"] = dict(
        test1=out["clean"]["test1"]["decision"], test2=out["clean"]["test2"]["decision"]
    )
    return out


if __name__ == "__main__":
    cat = dict(np.load(sys.argv[1]))
    mam = tuple(np.load(sys.argv[2])) if len(sys.argv) > 2 else None
    res = run(cat, mam)
    json.dump(
        res, open("WIDE_BINARY_STEP_TRACK_AMENDED.json", "w"), indent=1, default=float
    )
    print(json.dumps(res["decision_strict"]))
