#!/usr/bin/env python3
"""Clean-cut wide-binary chi2 at the Oort C window edges.

Bar, written before the catalog numbers: same as the working-C test in
working_c_wide_binary_rs.py. On the clean cut a model fails when
chi2_calibrated > 18.5 and raw chi2 exceeds that model's injection maximum.
chi2_calibrated = raw / kappa, kappa = median(injection chi2) / 3.357.
Seed family SEED0 = 2026101601. Decision field g_e = 1.9e-10. x* fixed.
The centre C already has WORKING_C_WIDE_BINARY_RS.json. This script scores
the two edges. It does not rewrite that centre file.
"""

import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np

import tidal_screening_two_body as T
import wide_binary_final as W
import wide_binary_fish as F
import working_c_wide_binary_rs as RS

HERE = Path(__file__).resolve().parent
XS = 703588428133.2817
GE = 1.9e-10
RADII = json.loads((HERE / "TIDAL_TWO_BODY_SUMMARY.json").read_text())["forms"][
    "action"
]["r_kau"]
EDGES = (0.208899, 0.696200)
BAR = 18.5
NPZ = "/tmp/claude-1000/-home-mega/6bf0494c-fd57-43a6-9af0-a0b1dc42070c/scratchpad/wbdata/eb21_cols.npz"


def cell(args):
    c_zero, M, rk, q1, mu = args
    s = T.solve_binary(M, rk * 1e3 * T.AU, q1, mu, GE, "action", xs=XS, c_zero=c_zero)
    return M, rk, q1, mu, s["Gamma_r"], s["Gamma_t"]


def gamma_table(c_zero):
    jobs = [
        (c_zero, M, float(rk), q1, float(mu))
        for M in T.TAB_M
        for rk in RADII
        for q1 in T.TAB_Q1
        for mu in T.TAB_MU
    ]
    raw = {}
    with mp.get_context("fork").Pool(4) as pool:
        for i, (M, rk, q1, mu, gr, gt) in enumerate(
            pool.imap_unordered(cell, jobs, chunksize=4)
        ):
            raw[(M, rk, q1, mu)] = (gr, gt)
            if i % 200 == 0:
                print(f"grid C={c_zero} {i}/{len(jobs)}", flush=True)
    Gr = np.empty((len(T.TAB_M), len(RADII), len(T.TAB_Q1), len(T.TAB_MU)))
    Gt = np.empty_like(Gr)
    for a, M in enumerate(T.TAB_M):
        for b, rk in enumerate(RADII):
            for c, q1 in enumerate(T.TAB_Q1):
                for d, mu in enumerate(T.TAB_MU):
                    Gr[a, b, c, d], Gt[a, b, c, d] = raw[(M, float(rk), q1, float(mu))]
    return {
        "C": c_zero,
        "g_e": GE,
        "x_star": XS,
        "a0": T.A0,
        "M_sun": T.TAB_M,
        "r_kau": list(map(float, RADII)),
        "q1": T.TAB_Q1,
        "mu_e": list(map(float, T.TAB_MU)),
        "mu_e_weights": list(map(float, T.TAB_MU_W)),
        "Gamma_r": np.round(Gr, 7).tolist(),
        "Gamma_t": np.round(Gt, 7).tolist(),
    }


def score_clean(table, tag):
    W.MODELS = ["N", "F", "E", "S", "P"]
    key = f"action_C{tag}|1.9e-10"
    RS.PACKS.clear()
    RS.PACKS[key] = RS.load_interp(table, table["Gamma_r"], table["r_kau"], key)
    RS.KEYS = (key,)
    c = dict(np.load(NPZ))
    F.RNG = np.random.default_rng(20261004)
    frozen = json.loads((HERE / "WIDE_BINARY_FINAL.json").read_text())
    b = F.prepare(c, F.CUTS["clean"])
    st = W.setup(b)
    rows, chi2 = W.measure(b["vt"], st)
    fr = frozen["clean"]
    dchi = max(abs(chi2[m] - fr["chi2"][m]) for m in W.MODELS)
    if len(b["s"]) != fr["n"] or dchi > 1e-6:
        raise SystemExit(f"clean extract mismatch n={len(b['s'])} dchi={dchi}")
    F.RNG = np.random.default_rng(RS.SEED0)
    for _name, bins in st:
        for bj in bins:
            if bj is None:
                continue
            sub = {k: v[bj["mask"]] for k, v in b.items()}
            bj["models"][key] = W.fit_alpha(
                RS.simulate(sub, key, nmc=W.NM), bj["pdf"], bj["cdf"], fix_c=True
            )[0]
    base = [m for m in W.MODELS if not str(m).startswith("action_C")]
    W.MODELS = base + [key]
    rows, chi2 = W.measure(b["vt"], st)
    RS.S["clean"] = dict(b=b, st=st)
    null = []
    jobs = [("clean", key, i) for i in range(W.NINJ)]
    with mp.get_context("fork").Pool(4) as pool:
        for n, (_cut, _key, raw) in enumerate(
            pool.imap_unordered(RS.one, jobs, chunksize=2)
        ):
            null.append(raw)
            if n % 10 == 0:
                print("inject", tag, n, round(raw, 3), flush=True)
    kappa = float(np.median(null) / W.CHI2_4_MEDIAN)
    raw_chi = float(chi2[key])
    cal = raw_chi / kappa
    null_max = float(np.max(null))
    fails = bool(cal > BAR and raw_chi > null_max)
    print(
        f"CLEAN C={table['C']} raw={raw_chi:.4f} cal={cal:.4f} "
        f"kappa={kappa:.4f} null_max={null_max:.4f} fails={fails}",
        flush=True,
    )
    return {
        "C": table["C"],
        "cut": "clean",
        "n": len(b["s"]),
        "chi2_raw": raw_chi,
        "chi2_N": float(chi2["N"]),
        "kappa": kappa,
        "chi2_calibrated": cal,
        "null_max": null_max,
        "bar": BAR,
        "fails": fails,
        "reproduction_max_dchi2": dchi,
    }


def main():
    centre = json.loads((HERE / "WORKING_C_WIDE_BINARY_RS.json").read_text())
    out = {
        "bar": "clean cut fails if chi2_calibrated > 18.5 and raw chi2 > injection maximum",
        "centre_source": "WORKING_C_WIDE_BINARY_RS.json",
        "centre": {
            "C": centre["C"],
            "cut": "clean",
            "chi2_raw": centre["clean"]["chi2"]["action_C|1.9e-10"],
            "chi2_calibrated": centre["clean"]["chi2_calibrated"]["action_C|1.9e-10"],
            "kappa": centre["clean"]["kappa"]["action_C|1.9e-10"],
            "null_max": centre["clean"]["null_max"]["action_C|1.9e-10"],
            "fails": centre["clean"]["fails"]["action_C|1.9e-10"],
        },
        "edges": [],
    }
    prior = HERE / "C_WINDOW_WIDE_BINARY.json"
    if prior.exists():
        old = json.loads(prior.read_text())
        out["edges"] = old.get("edges", [])
    for i, c_zero in enumerate(EDGES):
        tpath = HERE / f"C_WINDOW_GAMMA_{i}.json"
        if tpath.exists() and any(abs(e["C"] - c_zero) < 1e-9 for e in out["edges"]):
            print("skip scored", c_zero, flush=True)
            continue
        if tpath.exists():
            table = json.loads(tpath.read_text())
            print("loaded", tpath, flush=True)
        else:
            table = gamma_table(c_zero)
            tpath.write_text(json.dumps(table))
            print("wrote", tpath, flush=True)
        row = score_clean(table, str(i))
        row["gamma_table"] = tpath.name
        out["edges"].append(row)
        (HERE / "C_WINDOW_WIDE_BINARY.json").write_text(
            json.dumps(out, indent=1) + "\n"
        )
    print("wrote", HERE / "C_WINDOW_WIDE_BINARY.json", flush=True)


if __name__ == "__main__":
    main()
