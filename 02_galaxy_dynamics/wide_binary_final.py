#!/usr/bin/env python3
"""Wide-binary test under Amendment C of PREREG_WIDE_BINARY_FISH.md.

C1 Mamajek masses; C2 mass-stratified ratio; C3 injection-calibrated threshold;
C4 templates 320 draws/binary, model curves 80.
Usage: python3 wide_binary_final.py <eb21_cols.npz>
Output: WIDE_BINARY_FINAL.json
"""

import json
import multiprocessing as mp
import sys

import numpy as np

import wide_binary_fish as F

MODELS = ["N", "F", "E", "S", "P"]
STRATA = [("M<1", 0.0, 1.0), ("1<=M<1.5", 1.0, 1.5), ("M>=1.5", 1.5, 99.0)]
NT, NM, NINJ, NMIN = 320, 80, 40, 30
CHI2_4_MEDIAN = 3.357
ALPHAS = np.linspace(0.6, 2.2, 321)
CS = np.linspace(0, 0.6, 61)

tab = np.loadtxt("mamajek_mg_mass.csv", delimiter=",", comments="#")
F.MG_TAB, F.M_TAB = tab[:, 0], tab[:, 1]


def fit_alpha(vt, pdf, cdf, fix_c=False):
    vt = vt[vt < F.VMAX]
    pc = F.p_cont(vt)
    cs = np.array([0.0]) if fix_c else CS
    L = np.empty((len(ALPHAS), len(cs)))
    for i, a in enumerate(ALPHAS):
        pn = pdf(vt / a) / a / cdf(F.VMAX / a)
        L[i] = np.log((1 - cs)[None, :] * pn[:, None] + cs[None, :] * pc[:, None]).sum(
            0
        )
    prof = L.max(1)
    i0 = int(np.argmax(prof))
    inside = ALPHAS[prof > prof[i0] - 0.5]
    return float(ALPHAS[i0]), float((inside.max() - inside.min()) / 2)


def setup(b):
    """Per stratum, per bin: template and model alphas. Independent of observed v~."""
    out = []
    for name, lo_m, hi_m in STRATA:
        ms = (b["M"] >= lo_m) & (b["M"] < hi_m)
        bins = []
        for lo, hi in F.BINS:
            m = ms & (b["s"] >= lo) & (b["s"] < hi)
            if m.sum() < NMIN:
                bins.append(None)
                continue
            sub = {k: v[m] for k, v in b.items()}
            pdf, cdf = F.template(F.simulate(sub, "N", nmc=NT)[0])
            mods = {
                M: fit_alpha(F.simulate(sub, M, nmc=NM)[0], pdf, cdf, fix_c=True)[0]
                for M in MODELS
            }
            bins.append(dict(mask=m, pdf=pdf, cdf=cdf, models=mods))
        out.append((name, bins))
    return out


def measure(vt, st):
    """Combined R(s), sigma, and combined model curves for one v~ catalogue."""
    rows = []
    per = []
    for name, bins in st:
        if bins[0] is None:
            continue
        a0, s0 = fit_alpha(vt[bins[0]["mask"]], bins[0]["pdf"], bins[0]["cdf"])
        r = []
        for j in range(1, len(F.BINS)):
            bj = bins[j]
            if bj is None:
                r.append(None)
                continue
            a, s = fit_alpha(vt[bj["mask"]], bj["pdf"], bj["cdf"])
            R = a / a0
            sig = max(R * np.hypot(s / a, s0 / a0), 1e-3)
            mods = {M: bj["models"][M] / bins[0]["models"][M] for M in MODELS}
            r.append(dict(R=R, sig=sig, models=mods, n=int(bj["mask"].sum())))
        per.append((name, r))
    for j in range(len(F.BINS) - 1):
        ent = [(nm, r[j]) for nm, r in per if r[j] is not None]
        w = np.array([1 / e["sig"] ** 2 for _, e in ent])
        R = float(np.sum(w * [e["R"] for _, e in ent]) / w.sum())
        mods = {
            M: float(np.sum(w * [e["models"][M] for _, e in ent]) / w.sum())
            for M in MODELS
        }
        rows.append(
            dict(
                bin=list(F.BINS[j + 1]),
                R=R,
                sigma=float(1 / np.sqrt(w.sum())),
                models=mods,
                strata={nm: dict(R=e["R"], sig=e["sig"], n=e["n"]) for nm, e in ent},
            )
        )
    chi2 = {
        M: float(sum(((r["R"] - r["models"][M]) / r["sigma"]) ** 2 for r in rows))
        for M in MODELS
    }
    return rows, chi2


G = {}


def one_injection(args):
    cut, T, i = args
    F.RNG = np.random.default_rng(
        1000 * MODELS.index(T) + i + (0 if cut == "clean" else 500000)
    )
    vt = F.inject(G[cut]["b"], T)
    _, chi2 = measure(vt, G[cut]["st"])
    return cut, T, chi2[T]


def main(npz):
    c = dict(np.load(npz))
    F.RNG = np.random.default_rng(20261004)
    for cut in ("clean", "loose"):
        b = F.prepare(c, F.CUTS[cut])
        G[cut] = dict(b=b, st=setup(b))
        print(cut, "setup done", len(b["s"]), flush=True)
    result = {}
    for cut in ("clean", "loose"):
        rows, chi2 = measure(G[cut]["b"]["vt"], G[cut]["st"])
        result[cut] = dict(
            n=int(len(G[cut]["b"]["s"])),
            rows=rows,
            chi2=chi2,
            null={M: [] for M in MODELS},
        )
        print(cut, "DATA", {k: round(v, 1) for k, v in chi2.items()}, flush=True)
    jobs = [
        (cut, T, i) for cut in ("clean", "loose") for T in MODELS for i in range(NINJ)
    ]
    with mp.get_context("fork").Pool(7) as pool:
        for cut, T, x in pool.imap_unordered(one_injection, jobs, chunksize=4):
            result[cut]["null"][T].append(x)
    for cut in ("clean", "loose"):
        r = result[cut]
        r["kappa"] = {M: float(np.median(r["null"][M]) / CHI2_4_MEDIAN) for M in MODELS}
        r["null_max"] = {M: float(np.max(r["null"][M])) for M in MODELS}
        r["chi2_calibrated"] = {M: r["chi2"][M] / r["kappa"][M] for M in MODELS}
        print(
            cut,
            "kappa",
            {k: round(v, 2) for k, v in r["kappa"].items()},
            "calibrated",
            {k: round(v, 1) for k, v in r["chi2_calibrated"].items()},
            "null_max",
            {k: round(v, 1) for k, v in r["null_max"].items()},
            flush=True,
        )
    result["excluded"] = {
        M: all(
            result[cut]["chi2_calibrated"][M] > 18.5
            and result[cut]["chi2"][M] > result[cut]["null_max"][M]
            for cut in ("clean", "loose")
        )
        for M in MODELS
    }
    print("excluded", result["excluded"])
    json.dump(result, open("WIDE_BINARY_FINAL.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
