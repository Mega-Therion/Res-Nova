#!/usr/bin/env python3
"""C3 chi2 of the working-C action-form shell against the El-Badry sample.

Newton and the published unscreened two-body curve are scored beside it.
The clean-cut reproduction of WIDE_BINARY_FINAL.json is the control.
Decision field only: g_e = 1.9e-10. x* is not moved.
"""

import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator

import wide_binary_final as W
import wide_binary_fish as F

HERE = Path(__file__).resolve().parent
NEW = "action_C|1.9e-10"
OLD = "unscreened|1.9e-10"
SEED0 = 2026101601
KEYS = (NEW, OLD)


def load_interp(table, form_gamma, r_kau, key_label):
    mu = np.array(table["mu_e"])
    wmu = np.array(table["mu_e_weights"])
    lmax = len(mu)
    pl = np.array([np.polynomial.legendre.Legendre.basis(l)(mu) for l in range(lmax)])
    axes = (np.log(table["M_sun"]), np.log(r_kau), np.array(table["q1"]))
    gr = np.array(form_gamma)
    cl = np.einsum("...k,lk,k->...l", gr, pl, wmu) * (2 * np.arange(lmax) + 1) / 2
    inter = [RegularGridInterpolator(axes, cl[..., l]) for l in range(lmax)]
    return key_label, axes, inter, lmax


def boost(pack, M, r_au, q1, mu):
    _key, axes, inter, lmax = pack
    pts = np.stack(
        [
            np.clip(np.log(M), axes[0][0], axes[0][-1]),
            np.clip(np.log(r_au / 1e3), axes[1][0], axes[1][-1]),
            np.clip(q1, axes[2][0], axes[2][-1]),
        ],
        -1,
    )
    p = np.polynomial.legendre.legvander(mu, lmax - 1)
    return sum(inter[l](pts) * p[:, l] for l in range(lmax))


PACKS = {}


def simulate(b, key, nmc, noise=True):
    n = len(b["s"])
    idx = np.repeat(np.arange(n), nmc)
    s, M, q1, sig = b["s"][idx], b["M"][idx], b["q1"][idx], b["sig"][idx]
    rsky, r3, vsky, _ = F.kepler_mc(len(idx), F.gamma_of_s(s))
    vt = vsky * np.sqrt(rsky)[:, None]
    r_au = (s / rsky) * r3
    mu = F.RNG.uniform(-1, 1, len(idx))
    g = boost(PACKS[key], M, r_au, q1, mu)
    vt = vt * np.sqrt(np.maximum(g, 0))[:, None]
    if noise:
        vt = vt + F.RNG.normal(size=vt.shape) * sig[:, None]
    return np.hypot(vt[:, 0], vt[:, 1])


def inject(b, key):
    vt = simulate(b, key, nmc=1)
    ncont = int(0.05 * len(vt))
    j = F.RNG.choice(len(vt), ncont, replace=False)
    vt[j] = F.VMAX * np.sqrt(F.RNG.random(ncont))
    return vt


S = {}


def one(args):
    cut, key, i = args
    F.RNG = np.random.default_rng(
        SEED0 + 1000 * (KEYS.index(key) + 1) + i + (0 if cut == "clean" else 500000)
    )
    _rows, chi2 = W.measure(inject(S[cut]["b"], key), S[cut]["st"])
    return cut, key, chi2[key]


def main(npz):
    new = json.loads((HERE / "WORKING_C_GAMMA_TABLE.json").read_text())
    old = json.loads((HERE / "TIDAL_TWO_BODY_TABLE.json").read_text())
    PACKS[NEW] = load_interp(new, new["Gamma_r"], new["r_kau"], NEW)
    PACKS[OLD] = load_interp(
        {
            "M_sun": old["M_sun"],
            "q1": old["q1"],
            "mu_e": old["mu_e"],
            "mu_e_weights": old["mu_e_weights"],
        },
        old["forms"]["unscreened"]["1.9e-10"]["Gamma_r"],
        old["r_kau"],
        OLD,
    )
    frozen = json.loads((HERE / "WIDE_BINARY_FINAL.json").read_text())
    c = dict(np.load(npz))
    F.RNG = np.random.default_rng(20261004)
    out = {
        "reproduction": {},
        "C": new["C"],
        "g_e": new["g_e"],
        "x_star": new["x_star"],
        "seed0": SEED0,
    }
    for cut in ("clean", "loose"):
        b = F.prepare(c, F.CUTS[cut])
        S[cut] = dict(b=b, st=W.setup(b))
        rows, chi2 = W.measure(b["vt"], S[cut]["st"])
        fr = frozen[cut]
        dchi = max(abs(chi2[m] - fr["chi2"][m]) for m in W.MODELS)
        out["reproduction"][cut] = {
            "n": len(b["s"]),
            "n_frozen": fr["n"],
            "max_dchi2": dchi,
            "chi2_N": chi2["N"],
        }
        print(cut, out["reproduction"][cut], flush=True)
        if len(b["s"]) != fr["n"] or dchi > 1e-6:
            raise SystemExit("extract does not reproduce WIDE_BINARY_FINAL.json")
    for i, key in enumerate(KEYS):
        F.RNG = np.random.default_rng(SEED0 + i)
        for cut in ("clean", "loose"):
            b = S[cut]["b"]
            for _name, bins in S[cut]["st"]:
                for bj in bins:
                    if bj is None:
                        continue
                    sub = {k: v[bj["mask"]] for k, v in b.items()}
                    bj["models"][key] = W.fit_alpha(
                        simulate(sub, key, nmc=W.NM), bj["pdf"], bj["cdf"], fix_c=True
                    )[0]
    base = list(W.MODELS)
    W.MODELS = base + list(KEYS)
    for cut in ("clean", "loose"):
        rows, chi2 = W.measure(S[cut]["b"]["vt"], S[cut]["st"])
        out[cut] = {
            "n": len(S[cut]["b"]["s"]),
            "chi2": chi2,
            "rows": rows,
            "null": {k: [] for k in KEYS},
        }
        print(cut, "DATA", {k: round(chi2[k], 3) for k in ("N", NEW, OLD)}, flush=True)
    jobs = [
        (cut, key, i)
        for cut in ("clean", "loose")
        for key in KEYS
        for i in range(W.NINJ)
    ]
    with mp.get_context("fork").Pool(4) as pool:
        for n, (cut, key, raw) in enumerate(
            pool.imap_unordered(one, jobs, chunksize=2)
        ):
            out[cut]["null"][key].append(raw)
            if n % 10 == 0:
                print("inject", n, cut, key, round(raw, 3), flush=True)
    for cut in ("clean", "loose"):
        r = out[cut]
        r["kappa"] = {k: float(np.median(r["null"][k]) / W.CHI2_4_MEDIAN) for k in KEYS}
        r["null_max"] = {k: float(np.max(r["null"][k])) for k in KEYS}
        r["chi2_calibrated"] = {k: r["chi2"][k] / r["kappa"][k] for k in KEYS}
        r["fails"] = {
            k: bool(r["chi2_calibrated"][k] > 18.5 and r["chi2"][k] > r["null_max"][k])
            for k in KEYS
        }
    out["excluded_C3"] = {
        k: all(out[cut]["fails"][k] for cut in ("clean", "loose")) for k in KEYS
    }
    print("excluded", out["excluded_C3"], flush=True)
    path = HERE / "WORKING_C_WIDE_BINARY_RS.json"
    path.write_text(json.dumps(out, indent=1, default=float) + "\n")
    print("wrote", path, flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
