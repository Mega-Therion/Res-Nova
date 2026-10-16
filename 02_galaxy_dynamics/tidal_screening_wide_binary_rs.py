#!/usr/bin/env python3
"""Kill test for tidal screening: R(s) under Amendment C (wide_binary_final.py) with the two-body boost.
Pre-registered in PREREG_TIDAL_WIDE_BINARY_2026-10-15.md, section 4. The pinned pipeline files are imported, not edited.

1. Reproduce WIDE_BINARY_FINAL.json (n per cut, data R(s), chi2 of N F E S P) from the extract. Stop if it differs.
2. New models: v~ scaled by sqrt(Gamma_r(M, r_3D, q1, cos theta_e)) from TIDAL_TWO_BODY_TABLE.json, theta_e
   isotropic at random per draw (never the sky orientation), q1 clamped to the table, no q_two_body factor.
3. C3 per new model from 40 injected catalogues per cut; Gate 1 (power) for T = action form.
Usage: python3 tidal_screening_wide_binary_rs.py <eb21_cols.npz>     Output: TIDAL_WIDE_BINARY_RS.json
"""
import json
import multiprocessing as mp
import sys

import numpy as np
from scipy.interpolate import RegularGridInterpolator

import wide_binary_fish as F
import wide_binary_final as W

TAB = json.load(open("TIDAL_TWO_BODY_TABLE.json"))
GES = ("1.9e-10", "2.4e-10")
NEW = [f"{form}|{ge}" for form in ("action", "divergence", "unscreened") if form in TAB["forms"] for ge in GES]
SEED0 = 2026101500
MU = np.array(TAB["mu_e"])
WMU = np.array(TAB["mu_e_weights"])
LMAX = len(MU)
PL = np.array([np.polynomial.legendre.Legendre.basis(l)(MU) for l in range(LMAX)])
AXES, INTERP = {}, {}
for key in NEW:
    form, ge = key.split("|")
    AXES[key] = (np.log(TAB["M_sun"]), np.log(TAB["forms"][form].get("r_kau", TAB["r_kau"])), np.array(TAB["q1"]))
    Gr = np.array(TAB["forms"][form][ge]["Gamma_r"])            # (M, r, q1, mu)
    cl = np.einsum("...k,lk,k->...l", Gr, PL, WMU) * (2 * np.arange(LMAX) + 1) / 2
    INTERP[key] = [RegularGridInterpolator(AXES[key], cl[..., l]) for l in range(LMAX)]


def boost_new(key, M, r_au, q1, mu):
    ax = AXES[key]
    pts = np.stack([np.clip(np.log(M), ax[0][0], ax[0][-1]),
                    np.clip(np.log(r_au / 1e3), ax[1][0], ax[1][-1]),
                    np.clip(q1, ax[2][0], ax[2][-1])], -1)
    P = np.polynomial.legendre.legvander(mu, LMAX - 1)          # (n, L)
    return sum(INTERP[key][l](pts) * P[:, l] for l in range(LMAX))


CLIPPED = {}


def simulate_new(b, key, nmc, noise=True):
    """wide_binary_fish.simulate with the two-body boost in place of boost(model, gN, q1)."""
    n = len(b["s"])
    idx = np.repeat(np.arange(n), nmc)
    s, M, q1, sig = b["s"][idx], b["M"][idx], b["q1"][idx], b["sig"][idx]
    rsky, r3, vsky, _ = F.kepler_mc(len(idx), F.gamma_of_s(s))
    vt_vec = vsky * np.sqrt(rsky)[:, None]
    r_au = (s / rsky) * r3
    mu = F.RNG.uniform(-1, 1, len(idx))
    g = boost_new(key, M, r_au, q1, mu)
    CLIPPED[key] = CLIPPED.get(key, 0) + int((g < 0).sum())
    vt_vec = vt_vec * np.sqrt(np.maximum(g, 0))[:, None]
    if noise:
        vt_vec = vt_vec + F.RNG.normal(size=vt_vec.shape) * sig[:, None]
    return np.hypot(vt_vec[:, 0], vt_vec[:, 1]), idx


def inject_new(b, key):
    vt, _ = simulate_new(b, key, nmc=1)
    ncont = int(0.05 * len(vt))
    j = F.RNG.choice(len(vt), ncont, replace=False)
    vt[j] = F.VMAX * np.sqrt(F.RNG.random(ncont))
    return vt


S = {}


def one(args):
    cut, key, i = args
    F.RNG = np.random.default_rng(SEED0 + 1000 * (NEW.index(key) + 1) + i + (0 if cut == "clean" else 500000))
    _, chi2 = W.measure(inject_new(S[cut]["b"], key), S[cut]["st"])
    return cut, key, i, chi2


def main(npz):
    frozen = json.load(open("WIDE_BINARY_FINAL.json"))
    c = dict(np.load(npz))
    F.RNG = np.random.default_rng(20261004)
    for cut in ("clean", "loose"):
        b = F.prepare(c, F.CUTS[cut])
        S[cut] = dict(b=b, st=W.setup(b))
        print(cut, "setup done", len(b["s"]), flush=True)
    out = {"reproduction": {}}
    for cut in ("clean", "loose"):
        rows, chi2 = W.measure(S[cut]["b"]["vt"], S[cut]["st"])
        fr = frozen[cut]
        dR = max(abs(r["R"] - q["R"]) for r, q in zip(rows, fr["rows"]))
        dchi = max(abs(chi2[m] - fr["chi2"][m]) for m in W.MODELS)
        out["reproduction"][cut] = {"n": len(S[cut]["b"]["s"]), "n_frozen": fr["n"], "max_dR": dR, "max_dchi2": dchi}
        print(cut, out["reproduction"][cut], flush=True)
        assert len(S[cut]["b"]["s"]) == fr["n"] and dR < 1e-6 and dchi < 1e-6, "extract does not reproduce WIDE_BINARY_FINAL.json"
    # model curves for the new models, from their own seeds
    for i, key in enumerate(NEW):
        F.RNG = np.random.default_rng(SEED0 + i)
        for cut in ("clean", "loose"):
            b = S[cut]["b"]
            for _, bins in S[cut]["st"]:
                for bj in bins:
                    if bj is None:
                        continue
                    sub = {k: v[bj["mask"]] for k, v in b.items()}
                    bj["models"][key] = W.fit_alpha(simulate_new(sub, key, nmc=W.NM)[0], bj["pdf"], bj["cdf"], fix_c=True)[0]
    W.MODELS = list(W.MODELS) + NEW
    for cut in ("clean", "loose"):
        rows, chi2 = W.measure(S[cut]["b"]["vt"], S[cut]["st"])
        out[cut] = {"n": len(S[cut]["b"]["s"]), "rows": rows, "chi2": chi2,
                    "null": {k: [] for k in NEW}, "inj_chi2": {k: [] for k in NEW}}
        print(cut, "DATA", {k: round(v, 2) for k, v in chi2.items()}, flush=True)
    jobs = [(cut, key, i) for cut in ("clean", "loose") for key in NEW for i in range(W.NINJ)]
    with mp.get_context("fork").Pool(4) as pool:
        for cut, key, i, chi2 in pool.imap_unordered(one, jobs, chunksize=2):
            out[cut]["null"][key].append(chi2[key])
            out[cut]["inj_chi2"][key].append(chi2)
    for cut in ("clean", "loose"):
        r = out[cut]
        r["kappa"] = {k: float(np.median(r["null"][k]) / W.CHI2_4_MEDIAN) for k in NEW}
        r["null_max"] = {k: float(np.max(r["null"][k])) for k in NEW}
        r["chi2_calibrated"] = {k: r["chi2"][k] / r["kappa"][k] for k in NEW}
        r["gate1"] = {}
        for ge in GES:
            T = f"action|{ge}"
            if T not in NEW:
                continue
            inj = r["inj_chi2"][T]
            r["gate1"][T] = {X: float(np.median([np.sqrt(max(0.0, d[X] - d[T])) for d in inj]))
                             for X in ("N", f"unscreened|{ge}")}
        print(cut, "kappa", {k: round(v, 2) for k, v in r["kappa"].items()}, "calibrated",
              {k: round(v, 1) for k, v in r["chi2_calibrated"].items()}, "null_max",
              {k: round(v, 1) for k, v in r["null_max"].items()}, "gate1", r["gate1"], flush=True)
    out["excluded_C3"] = {k: all(out[cut]["chi2_calibrated"][k] > 18.5 and out[cut]["chi2"][k] > out[cut]["null_max"][k]
                                 for cut in ("clean", "loose")) for k in NEW}
    tk = [f"action|{ge}" for ge in GES if f"action|{ge}" in NEW]
    if tk:
        dead = all(out["excluded_C3"][k] for k in tk)
        under = all(out[cut]["gate1"][k]["N"] < 4 for cut in ("clean", "loose") for k in tk)
        out["verdict"] = ("EXCLUDED: x* would have to move" if dead else
                          "NOT EXCLUDED; underpowered against Newton at current N" if under else "NOT EXCLUDED")
    out["clipped_negative_boost_draws"] = CLIPPED
    out["config"] = {"table": "TIDAL_TWO_BODY_TABLE.json", "x_star": TAB["x_star"], "a0": TAB["a0"], "seed0": SEED0}
    print("excluded", out["excluded_C3"], "verdict", out.get("verdict"), flush=True)
    for cut in ("clean", "loose"):
        out[cut].pop("inj_chi2")
    json.dump(out, open("TIDAL_WIDE_BINARY_RS.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main(sys.argv[1])
