"""Power of the Amendment-A step-tracking tests on the RV-fixed, larger samples.

Synthetic v~ only (Newtonian MC per real binary: its s, M, sigma) times an
injected step; no Gaia velocities are read. Samples are defined by distance
limit and the test-1 distance split, both fixed here before any fit.
Usage: python3 wide_binary_step_power2.py <eb21_cols.npz>
Output: WIDE_BINARY_STEP_POWER2.json
"""
import json
import sys

import numpy as np

import wide_binary_fish as F
import wide_binary_step as S
import wide_binary_step_track_amended as T

T.NBOOT = 200
S0 = 2000.0
NTRIAL = 40
SAMPLES = {"d200_split100": (0.2, 100.0), "d500_split200": (0.5, 200.0)}
AMPS = (0.05, 0.03)


def load(c, dmax, cut):
    F.DMAX = S.DMAX = dmax
    b = F.prepare(c, cut)
    _ok, ex = S.surviving_mask(c, cut, b)
    assert len(ex["d_pc"]) == len(b["s"])
    return b, ex["d_pc"]


def cross(b, m, onset, amp, rng):
    sub = {k: v[m] for k, v in b.items()}
    vt, _ = F.simulate(sub, "N", nmc=1)
    vt = vt * np.where(sub["s"] > onset, 1 + amp, 1.0)
    s = sub["s"]
    return T.rows_and_cross(s, vt, T.AU_BINS[1:], (s >= 500) & (s < 1000), rng,
                            ref_mid=float(np.sqrt(500 * 1000)))[1]


def power(b, m1, m2, P, names, amp, rng):
    res = {}
    for truth, shift in (("AU", 1.0), ("alternative", P)):
        calls = []
        for _ in range(NTRIAL):
            x1, x2 = cross(b, m1, S0, amp, rng), cross(b, m2, S0 * shift, amp, rng)
            calls.append(T.decide(x2 / x1 if None not in (x1, x2) else None, P, names))
        want = names[0] if truth == "AU" else names[1]
        res[f"truth_{truth}"] = dict(correct=calls.count(want) / NTRIAL,
                                     calls={k: calls.count(k) / NTRIAL for k in set(calls)})
    return res


c = dict(np.load(sys.argv[1]))
rng = np.random.default_rng(12)
out = {}
for sname, (dmax, split) in SAMPLES.items():
    b, d = load(c, dmax, F.CUTS["clean"])
    near, far = d < split, d >= split
    light, heavy = b["M"] < 1.0, b["M"] >= 1.5
    P1 = float(np.median(d[far]) / np.median(d[near]))
    P2 = float(np.sqrt(np.median(b["M"][heavy]) / np.median(b["M"][light])))
    entry = dict(dmax_kpc=dmax, split_pc=split, n=int(len(b["s"])), n_near=int(near.sum()), n_far=int(far.sum()),
                 n_light=int(light.sum()), n_heavy=int(heavy.sum()), P1=P1, P2=P2)
    for amp in AMPS:
        entry[f"test1_A{amp}"] = power(b, near, far, P1, ("tracks_AU", "tracks_arcseconds"), amp, rng)
        entry[f"test2_A{amp}"] = power(b, light, heavy, P2, ("tracks_AU", "tracks_acceleration"), amp, rng)
        print(sname, amp, "T1", {k: entry[f"test1_A{amp}"][k]["correct"] for k in ("truth_AU", "truth_alternative")},
              "T2", {k: entry[f"test2_A{amp}"][k]["correct"] for k in ("truth_AU", "truth_alternative")}, flush=True)
    out[sname] = entry
    print(sname, {k: v for k, v in entry.items() if not k.startswith("test")}, flush=True)
json.dump(out, open("WIDE_BINARY_STEP_POWER2.json", "w"), indent=1)
