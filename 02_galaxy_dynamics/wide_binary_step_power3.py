"""Power of a joint step-model comparison (candidate replacement statistic).

Per slice: median v~ in 8 log bins over 1-30 kAU relative to the slice's
500-1000 AU median, SE from the median's asymptotic error. Model
R(s) = 1 + A * Phi((ln s - ln s0) / 0.4). H_AU: both slices share s0.
H_alt: slice 2 uses s0 * P. A and s0 are fit on a grid under each hypothesis.
Call the hypothesis with lower chi2 if the difference is >= 4, else
inconclusive. Synthetic v~ only (Newtonian MC per real binary); no Gaia
velocities read. Output: WIDE_BINARY_STEP_POWER3.json
"""
import json
import sys

import numpy as np
from scipy.stats import norm

import wide_binary_fish as F
import wide_binary_step as S

EDGES = np.geomspace(1000, 30000, 9)
REF = (500, 1000)
W = 0.4
A_GRID = np.linspace(0.0, 0.15, 31)
S0_GRID = np.geomspace(700, 20000, 60)
NTRIAL = 40
S0 = 2000.0


def slice_R(s, vt):
    good = (vt > 0) & (vt < 5)
    ref = vt[(s >= REF[0]) & (s < REF[1]) & good]
    mref = np.median(ref)
    se_ref = 1.2533 * np.std(ref) / np.sqrt(len(ref)) / mref
    x, R, se = [], [], []
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        v = vt[(s >= lo) & (s < hi) & good]
        if len(v) < 50:
            continue
        r = np.median(v) / mref
        x.append(np.sqrt(lo * hi)); R.append(r)
        se.append(r * np.hypot(1.2533 * np.std(v) / np.sqrt(len(v)) / np.median(v), se_ref))
    return np.array(x), np.array(R), np.array(se)


def chi2_best(d1, d2, P):
    best = np.inf
    for s0 in S0_GRID:
        m1 = norm.cdf((np.log(d1[0]) - np.log(s0)) / W)
        m2 = norm.cdf((np.log(d2[0]) - np.log(s0 * P)) / W)
        for A in A_GRID:
            c = np.sum(((d1[1] - 1 - A * m1) / d1[2]) ** 2) + np.sum(((d2[1] - 1 - A * m2) / d2[2]) ** 2)
            best = min(best, c)
    return best


def call(d1, d2, P):
    c_au, c_alt = chi2_best(d1, d2, 1.0), chi2_best(d1, d2, P)
    if c_alt - c_au >= 4:
        return "AU"
    if c_au - c_alt >= 4:
        return "alternative"
    return "inconclusive"


def synth(b, m, onset, amp):
    sub = {k: v[m] for k, v in b.items()}
    vt, _ = F.simulate(sub, "N", nmc=1)
    return sub["s"], vt * (1 + amp * norm.cdf((np.log(sub["s"]) - np.log(onset)) / W))


def main():
    c = dict(np.load(sys.argv[1]))
    out = {}
    for sname, (dmax, split) in {"d200_split100": (0.2, 100.0), "d500_split200": (0.5, 200.0)}.items():
        F.DMAX = S.DMAX = dmax
        b = F.prepare(c, F.CUTS["clean"])
        _ok, ex = S.surviving_mask(c, F.CUTS["clean"], b)
        d = ex["d_pc"]
        tests = {"test1": (d < split, d >= split, float(np.median(d[d >= split]) / np.median(d[d < split]))),
                 "test2": (b["M"] < 1.0, b["M"] >= 1.5, float(np.sqrt(np.median(b["M"][b["M"] >= 1.5]) / np.median(b["M"][b["M"] < 1.0]))))}
        out[sname] = {}
        for tname, (m1, m2, P) in tests.items():
            for amp in (0.05, 0.03):
                r = {}
                for truth, shift in (("AU", 1.0), ("alternative", P)):
                    calls = []
                    for _ in range(NTRIAL):
                        d1 = slice_R(*synth(b, m1, S0, amp))
                        d2 = slice_R(*synth(b, m2, S0 * shift, amp))
                        calls.append(call(d1, d2, P))
                    r[f"truth_{truth}"] = {k: calls.count(k) / NTRIAL for k in set(calls)}
                out[sname][f"{tname}_A{amp}"] = dict(P=P, n1=int(m1.sum()), n2=int(m2.sum()), **r)
                print(sname, tname, amp, round(P, 2), r, flush=True)
    json.dump(out, open("WIDE_BINARY_STEP_POWER3.json", "w"), indent=1)



if __name__ == "__main__":
    main()