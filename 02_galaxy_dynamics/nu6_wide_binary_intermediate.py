#!/usr/bin/env python3
"""One intermediate wide-binary cut for nu6.

Protocol: PREREG_NU6_WIDE_BINARY_INTERMEDIATE_2026-10-16.md.
Does not rewrite NU6_WIDE_BINARY.json.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import nu6_wide_binary as N
import wide_binary_final as W
import wide_binary_fish as F

HERE = Path(__file__).resolve().parent
SEED = 20261016
OFFSET = 450000
RCA = (0.01 * 0.1) ** 0.5
RUWE = (1.2 + 1.4) / 2
SIG = (0.10 * 0.20) ** 0.5
MID = dict(rca=RCA, ruwe=RUWE, sig=SIG)


def bag(b):
    return Counter(
        zip(b["s"].tolist(), b["M"].tolist(), b["q1"].tolist(), b["vt"].tolist())
    )


def nested(clean, mid, loose):
    bc, bm, bl = bag(clean), bag(mid), bag(loose)
    return (
        len(clean["s"]) < len(mid["s"]) < len(loose["s"])
        and all(bm[k] >= v for k, v in bc.items())
        and all(bl[k] >= v for k, v in bm.items())
    )


def injections(b, st, key):
    raws = []
    ge = N.GE_EXTRA if key.endswith("2.32") else N.GE_DECISION
    kind = "N" if key == "N" else "nu6"
    for i in range(40):
        F.RNG = np.random.default_rng(
            SEED + 10007 * i + OFFSET + (0 if key == "N" else 50)
        )
        vt = N.samples(b, kind, 1, ge)
        ncont = int(0.05 * len(vt))
        j = F.RNG.choice(len(vt), ncont, replace=False)
        vt[j] = F.VMAX * np.sqrt(F.RNG.random(ncont))
        _, chi2 = N.measure(vt, st, (key,))
        raws.append(chi2[key])
        print(f"inject intermediate {key} {i} {raws[-1]:.3f}", flush=True)
    return raws


def fails(raw, rec):
    return rec["chi2_calibrated"] > 18.5 and raw > rec["null_max"]


def main(npz):
    N.newton_self_check()
    tab = np.loadtxt(HERE / "mamajek_mg_mass.csv", delimiter=",", comments="#")
    F.MG_TAB, F.M_TAB = tab[:, 0], tab[:, 1]
    c = dict(np.load(npz))
    prepared = {}
    for name, cut in (
        ("clean", F.CUTS["clean"]),
        ("intermediate", MID),
        ("loose", F.CUTS["loose"]),
    ):
        F.RNG = np.random.default_rng(
            SEED + {"clean": 0, "intermediate": 2, "loose": 1}[name]
        )
        prepared[name] = F.prepare(c, cut)
        print(name, "n", len(prepared[name]["s"]), flush=True)
    ok = nested(prepared["clean"], prepared["intermediate"], prepared["loose"])
    print("nested", ok, flush=True)
    out = {
        "prereg": "PREREG_NU6_WIDE_BINARY_INTERMEDIATE_2026-10-16.md",
        "a0": N.A0,
        "seed": SEED,
        "offset": OFFSET,
        "cut": {"rca": RCA, "ruwe": RUWE, "sig": SIG},
        "n": {k: len(v["s"]) for k, v in prepared.items()},
        "nested": ok,
    }
    path = HERE / "NU6_WIDE_BINARY_INTERMEDIATE.json"
    if not ok:
        out["verdict"] = "cut not intermediate"
        out["nu6_excluded"] = False
        path.write_text(json.dumps(out, indent=1) + "\n")
        print("wrote", path, flush=True)
        return
    b = prepared["intermediate"]
    keys, st = N.build(b)
    rows, chi2 = N.measure(b["vt"], st, keys)
    out["chi2"] = chi2
    out["rows"] = rows
    print("intermediate", {k: round(v, 3) for k, v in chi2.items()}, flush=True)
    for key in ("N", "nu6", "nu6_2.32"):
        raws = injections(b, st, key)
        med = float(np.median(raws))
        kappa = med / W.CHI2_4_MEDIAN
        raw = chi2[key]
        out[key] = {
            "injected": raws,
            "median": med,
            "null_max": float(np.max(raws)),
            "kappa": kappa,
            "chi2_raw": raw,
            "chi2_calibrated": float(raw / kappa),
        }
        out[key]["fails"] = bool(fails(raw, out[key]))
    newton_passes = not out["N"]["fails"]
    nu_fails = out["nu6"]["fails"]
    out["newton_passes"] = newton_passes
    out["nu6_excluded"] = bool(nu_fails and newton_passes)
    if not newton_passes:
        out["verdict"] = "cut does not discriminate"
    elif out["nu6_excluded"]:
        out["verdict"] = "excluded"
    else:
        out["verdict"] = "not excluded"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path, flush=True)
    print("verdict", out["verdict"], "nu6_excluded", out["nu6_excluded"], flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
