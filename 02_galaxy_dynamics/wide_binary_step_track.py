#!/usr/bin/env python3
"""Run the two pre-registered tests in PREREG_WIDE_BINARY_STEP.md.

Test 1 splits by distance. Test 2 splits by mass. The decision rule is
the one in that file.
"""

import json

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
ANG_BINS = [(5, 10), (10, 20), (20, 40), (40, 80), (80, 160)]


def rows_for(s, vt, bins):
    out = []
    for lo, hi in bins:
        m = (s >= lo) & (s < hi) & (vt > 0) & (vt < 5)
        if int(m.sum()) < 30:
            out.append({"bin": [lo, hi], "n": int(m.sum()), "median": None})
            continue
        out.append(
            {"bin": [lo, hi], "n": int(m.sum()), "median": float(np.median(vt[m]))}
        )
    return out


def step_of(rows):
    anchor = None
    for row in rows:
        if row["median"] is None:
            continue
        if anchor is None:
            anchor = row["median"]
            row["R"] = 1.0
            continue
        row["R"] = row["median"] / anchor
        if row["R"] >= 1.03:
            lo, hi = row["bin"]
            return (lo * hi) ** 0.5, row["bin"], row["R"], row["n"]
    return None


def decide_angle(near, far):
    if near is None or far is None:
        return "inconclusive"
    same_au = near["au_bin"] == far["au_bin"]
    same_ang = near["ang_bin"] == far["ang_bin"]
    if same_ang and not same_au:
        return "tracks_arcseconds"
    if same_au and not same_ang:
        return "tracks_AU"
    return "inconclusive"


def decide_mass(light, heavy, m_light, m_heavy):
    if light is None or heavy is None or m_light <= 0:
        return "inconclusive", None
    predicted = (m_heavy / m_light) ** 0.5
    got = heavy["au_mid"] / light["au_mid"]
    if abs(got / predicted - 1) <= 0.20:
        return "tracks_sqrtM", {"predicted_ratio": predicted, "measured_ratio": got}
    if light["au_bin"] == heavy["au_bin"]:
        return "same_AU_bin", {"predicted_ratio": predicted, "measured_ratio": got}
    return "inconclusive", {"predicted_ratio": predicted, "measured_ratio": got}


def pack(step):
    if step is None:
        return None
    mid, bin_, r, n = step
    return {"au_mid": mid, "au_bin": bin_, "R": r, "n": n}


def pack_ang(step):
    if step is None:
        return None
    mid, bin_, r, n = step
    return {"ang_mid": mid, "ang_bin": bin_, "R": r, "n": n}


def main():
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    for name, cut in F.CUTS.items():
        b = F.prepare(catalog, cut)
        _ok, extra = S.surviving_mask(catalog, cut, b)
        if len(extra["d_pc"]) != len(b["s"]):
            raise SystemExit(f"length mismatch {name}")
        s, vt, M, d = b["s"], b["vt"], b["M"], extra["d_pc"]
        ang = s / d
        slices = {
            "under_100pc": d < 100,
            "100_to_200pc": d >= 100,
        }
        test1 = {}
        for label, m in slices.items():
            au = rows_for(s[m], vt[m], AU_BINS)
            an = rows_for(ang[m], vt[m], ANG_BINS)
            test1[label] = {
                "au": au,
                "angle": an,
                "au_step": pack(step_of(au)),
                "angle_step": pack_ang(step_of(an)),
            }
        near, far = test1["under_100pc"]["au_step"], test1["100_to_200pc"]["au_step"]
        # Decision uses AU bin from the AU split and angle bin from the angle split.
        near_d = (
            None
            if near is None or test1["under_100pc"]["angle_step"] is None
            else {
                "au_bin": near["au_bin"],
                "ang_bin": test1["under_100pc"]["angle_step"]["ang_bin"],
            }
        )
        far_d = (
            None
            if far is None or test1["100_to_200pc"]["angle_step"] is None
            else {
                "au_bin": far["au_bin"],
                "ang_bin": test1["100_to_200pc"]["angle_step"]["ang_bin"],
            }
        )
        light = M < 1.0
        heavy = M >= 1.5
        light_step = pack(step_of(rows_for(s[light], vt[light], AU_BINS)))
        heavy_step = pack(step_of(rows_for(s[heavy], vt[heavy], AU_BINS)))
        m_light = float(np.median(M[light])) if light.any() else 0.0
        m_heavy = float(np.median(M[heavy])) if heavy.any() else 0.0
        mass_call, mass_ratio = decide_mass(light_step, heavy_step, m_light, m_heavy)
        result[name] = {
            "test1": test1,
            "test1_decision": decide_angle(near_d, far_d),
            "test2": {
                "light_step": light_step,
                "heavy_step": heavy_step,
                "median_mass_light": m_light,
                "median_mass_heavy": m_heavy,
                "n_light": int(light.sum()),
                "n_heavy": int(heavy.sum()),
                "decision": mass_call,
                "ratio": mass_ratio,
            },
        }
        print(
            name,
            "angle",
            result[name]["test1_decision"],
            "mass",
            mass_call,
            mass_ratio,
            flush=True,
        )
    # Pre-registered decisions use the strict cut.
    result["decision"] = {
        "test1_strict": result["clean"]["test1_decision"],
        "test2_strict": result["clean"]["test2"]["decision"],
    }
    json.dump(result, open("WIDE_BINARY_STEP_TRACK.json", "w"), indent=1)
    print("wrote WIDE_BINARY_STEP_TRACK.json")
    print(json.dumps(result["decision"]))


if __name__ == "__main__":
    main()
