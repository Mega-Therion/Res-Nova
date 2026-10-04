#!/usr/bin/env python3
"""Refit the wide-binary models with Amendment B contaminants frozen.

f_c and beta are fit on the 500–2000 AU control bin only. They are not
adjusted to the test bins. Measured R(s) is the already published fit.
Model curves are Newtonian or modified draws with the frozen contaminant
applied, then scaled by the control bin of that same contaminated model.
"""

import json

import numpy as np

import wide_binary_contaminant as C
import wide_binary_fish as F

MODELS = ("N", "F", "E", "S", "P")
PUBLISHED = "WIDE_BINARY_FISH.json"


def load_measured(cut):
    data = json.load(open(PUBLISHED))
    rows = data[cut]["data"]["rows"]
    return [
        {"bin": r["bin"], "R": r["R"], "sigma": r["sigma"], "n": r["n"]} for r in rows
    ]


def contaminated_alpha(sub, model, kind, param, pdf, cdf):
    vt, idx = F.simulate(sub, model, nmc=10)
    s = sub["s"][idx]
    if kind == "T":
        vt = C.add_tertiaries(vt, s, param, C_RNG)
    else:
        vt = vt * C.mass_factor(s, param)
    return F.fit_alpha(vt, pdf, cdf, fix_c=0)["alpha"]


C_RNG = np.random.default_rng(20261005)


def one_cut(catalog, cut_name):
    b = F.prepare(catalog, F.CUTS[cut_name])
    ctrl = (b["s"] >= 500) & (b["s"] < 2000)
    f_c = C.fit_fc(b["s"][ctrl], b["vt"][ctrl], C_RNG)
    beta = C.fit_beta(b["s"][ctrl], b["vt"][ctrl], C_RNG)
    measured = load_measured(cut_name)
    out = {"f_c": f_c, "beta": beta, "variants": {}}
    for kind, param in (("T", f_c), ("M", beta)):
        rows = []
        alphas = {}
        for lo, hi in F.BINS:
            m = (b["s"] >= lo) & (b["s"] < hi)
            sub = {k: v[m] for k, v in b.items()}
            tN, _ = F.simulate(sub, "N", nmc=10)
            pdf, cdf = F.template(tN)
            alphas = {
                mod: contaminated_alpha(sub, mod, kind, param, pdf, cdf)
                for mod in MODELS
            }
            rows.append({"bin": [lo, hi], "n": int(m.sum()), "alpha": alphas})
        ctrl_a = rows[0]["alpha"]
        chi = {mod: 0.0 for mod in MODELS}
        reported = []
        for row, meas in zip(rows[1:], measured):
            pred = {mod: row["alpha"][mod] / ctrl_a[mod] for mod in MODELS}
            for mod in MODELS:
                chi[mod] += ((meas["R"] - pred[mod]) / meas["sigma"]) ** 2
            reported.append(
                {
                    "bin": row["bin"],
                    "measured_R": meas["R"],
                    "sigma": meas["sigma"],
                    "predicted_R": pred,
                }
            )
        out["variants"][kind] = {
            "rows": reported,
            "chi2": {k: float(v) for k, v in chi.items()},
            "excluded": {k: bool(v > 18.5) for k, v in chi.items()},
        }
    return out


def main():
    catalog = dict(
        np.load(
            "/tmp/claude-1000/-home-mega/e34b278d-ef0d-47d9-a7a6-04591e7f2ba0/scratchpad/wb/eb21_cols.npz"
        )
    )
    result = {}
    for cut in ("clean", "loose"):
        print("cut", cut, flush=True)
        result[cut] = one_cut(catalog, cut)
        print(
            cut,
            "f_c",
            result[cut]["f_c"],
            "beta",
            result[cut]["beta"],
            {k: result[cut]["variants"][k]["chi2"] for k in ("T", "M")},
            flush=True,
        )
    verdict = {}
    for mod in MODELS:
        verdict[mod] = all(
            result[cut]["variants"][kind]["excluded"][mod]
            for cut in result
            for kind in ("T", "M")
        )
    # 2–5 kAU is the first test bin
    offset_remains = {}
    for cut in result:
        for kind in ("T", "M"):
            row = result[cut]["variants"][kind]["rows"][0]
            gap = row["measured_R"] - row["predicted_R"]["N"]
            offset_remains[f"{cut}/{kind}"] = {
                "measured": row["measured_R"],
                "newton_plus_contaminant": row["predicted_R"]["N"],
                "gap": gap,
            }
    result["verdict_excluded_under_both_cuts_and_both_contaminants"] = verdict
    result["offset_2_5_kau"] = offset_remains
    result["rule"] = (
        "Excluded only if chi2>18.5 for both cuts and both frozen contaminants. "
        "If the 2-5 kAU gap remains, it stays a sample systematic."
    )
    json.dump(result, open("WIDE_BINARY_CONTAMINANT_REFIT.json", "w"), indent=1)
    print("wrote WIDE_BINARY_CONTAMINANT_REFIT.json")


if __name__ == "__main__":
    main()
