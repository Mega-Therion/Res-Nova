#!/usr/bin/env python3
"""Cassini Q2 at the working Lagrangian zero, x* held at the action value.

C = 0 is the published calibration. The working centre is C_oort_peak at
g_e = 1.9e-10 in SCREENED_C_SOLUTIONS.json. nu_eff is unchanged; only W sees C.
"""

import json
from pathlib import Path

import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
XS = 703588428133.2817
SOL = json.loads((HERE / "SCREENED_C_SOLUTIONS.json").read_text())
C_WORK = next(r for r in SOL["fields"] if abs(r["g_e_m_s2"] - 1.9e-10) < 1e-14)[
    "C_oort_peak"
]["C"]


def one(ge, c_zero):
    tot, qf, qw = T.cassini_Q2(ge, "action", XS, parts=True, c_zero=c_zero)
    return {
        "Q2": tot,
        "divergence_part": qf,
        "W_part": qw,
        "inside_2sig": bool(T.Q2_WINDOW[0] <= tot <= T.Q2_WINDOW[1]),
    }


def main():
    out = {
        "x_star": XS,
        "C_working": C_WORK,
        "window": T.Q2_WINDOW,
        "rows": [],
    }
    for ge in T.GES:
        z = one(ge, 0.0)
        w = one(ge, C_WORK)
        out["rows"].append({"g_e": ge, "C0": z, "C_working": w})
        print(
            f"g_e={ge:.2e} C0 Q2={z['Q2']:.6e} W={z['W_part']:.6e} "
            f"C_work Q2={w['Q2']:.6e} W={w['W_part']:.6e} inside={w['inside_2sig']}",
            flush=True,
        )
    both = all(r["C_working"]["inside_2sig"] for r in out["rows"])
    out["passes_both_fields"] = both
    path = HERE / "CASSINI_AT_WORKING_C.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path, "passes", both, flush=True)


if __name__ == "__main__":
    main()
