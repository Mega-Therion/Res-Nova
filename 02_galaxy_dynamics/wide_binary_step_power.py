"""Power of the Amendment-A step-tracking tests at the real slice sizes.

Synthetic v~ only (Newtonian MC on each real binary's s, M, sigma), times a
step of amplitude A that turns on at s0 (AU-tracking) or at s0*P for the
shifted slice (alternative-tracking). No Gaia velocities are read.
Output: WIDE_BINARY_STEP_POWER.json
"""
import json
import sys

import numpy as np

import wide_binary_fish as F
import wide_binary_step as S
import wide_binary_step_track_amended as T

T.NBOOT = 200
A = 0.05          # step amplitude, the measured 2-5 kAU size
S0 = 2000.0       # onset in AU for the reference slice
NTRIAL = 40


def synth(b, m, onset, rng):
    sub = {k: v[m] for k, v in b.items()}
    vt, _ = F.simulate(sub, "N", nmc=1)
    return sub["s"], vt * np.where(sub["s"] > onset, 1 + A, 1.0)


def trial(b, m1, m2, P, track_alt, names, rng):
    x = []
    for m, shift in ((m1, 1.0), (m2, P if track_alt else 1.0)):
        s, vt = synth(b, m, S0 * shift, rng)
        _, xc, _ = T.rows_and_cross(s, vt, T.AU_BINS[1:], (s >= 500) & (s < 1000), rng,
                                    ref_mid=float(np.sqrt(500 * 1000)))
        x.append(xc)
    Q = x[1] / x[0] if None not in x else None
    return T.decide(Q, P, names)


c = dict(np.load(sys.argv[1]))
out = {}
b = F.prepare(c, F.CUTS["clean"])
_ok, ex = S.surviving_mask(c, F.CUTS["clean"], b)
d = ex["d_pc"]
rng = np.random.default_rng(11)
tests = {
    "test1": (d < 100, d >= 100, np.median(d[d >= 100]) / np.median(d[d < 100]), ("tracks_AU", "tracks_arcseconds")),
    "test2": (b["M"] < 1.0, b["M"] >= 1.5, np.sqrt(np.median(b["M"][b["M"] >= 1.5]) / np.median(b["M"][b["M"] < 1.0])),
              ("tracks_AU", "tracks_acceleration")),
}
for name, (m1, m2, P, names) in tests.items():
    res = {}
    for truth, alt in (("AU", False), ("alternative", True)):
        calls = [trial(b, m1, m2, P, alt, names, rng) for _ in range(NTRIAL)]
        res[f"truth_{truth}"] = {k: calls.count(k) / NTRIAL for k in set(calls)}
    out[name] = dict(P=float(P), n1=int(m1.sum()), n2=int(m2.sum()), amplitude=A, onset=S0, ntrial=NTRIAL, **res)
    print(name, out[name], flush=True)
json.dump(out, open("WIDE_BINARY_STEP_POWER.json", "w"), indent=1)
