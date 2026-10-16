#!/usr/bin/env python3
"""Binding offset of nu6 on the frozen Oort map. Protocol: PREREG_NU6_OORT_2026-10-16.md.

No parameter is fitted. The decision rule in the pre-registration is applied to the number
this script computes.
"""

import json
import sys
from pathlib import Path

import numpy as np

import oort_torque_proxy as O

HERE = Path(__file__).resolve().parent
NU6 = lambda y: (0.5 * (1.0 + np.sqrt(1.0 + 4.0 * np.maximum(y, 1e-100) ** -6.0))) ** (
    1.0 / 6.0
)
GES = (1.9e-10, 2.32e-10)


def verdict(inv_a):
    if inv_a >= 1.0e-4:
        return "empties the peak"
    if abs(inv_a) <= 1.0e-5:
        return "preserves the peak in this proxy"
    return "shifts"


def one(ge):
    name = f"nu6|{ge:.2e}"
    O.CONFIGS[name] = (NU6, O.A0_LIVE, ge, "unscreened", None)
    m = O.dg_map(name)
    inv = float(O.binding_offset(m))
    r = np.array(m["r_kau"])
    mu = np.array(m["mu"])
    _, w = np.polynomial.legendre.leggauss(len(mu))
    fr = 0.5 * np.array(m["dgr_over_gN"]) @ w
    g_over = 1.0 + fr
    outward = [float(rk) for rk, g in zip(r, g_over) if g < 0]
    # dgr_over_gN is dg_r / g_N with g_N = GM/r^2 inward-positive in the proxy's radial
    # basis (n points outward, dg @ n). Net outward when dg_r > g_N, i.e. fr > 1?
    # Newtonian acceleration is separate. Net radial anomaly added to -GM/r^2 (outward
    # positive) is + (fr * GM/r^2) if fr = dg_out / g_N. Outward net when fr > 1.
    outward = [float(rk) for rk, f in zip(r, fr) if f > 1.0]
    return {
        "g_e": ge,
        "a0": O.A0_LIVE,
        "inv_a_au": inv,
        "a_edge_au": (1.0 / inv) if inv else None,
        "verdict": verdict(inv),
        "outward_r_kau": outward,
        "map_r_kau": m["r_kau"],
        "mean_dgr_over_gN": [float(v) for v in fr],
    }


def main():
    rows = [one(ge) for ge in GES]
    out = {"prereg": "PREREG_NU6_OORT_2026-10-16.md", "nu": "nu6", "fields": rows}
    path = HERE / "NU6_OORT_BINDING.json"
    # drop bulky per-radius list from the committed summary? keep it: it is the measurement.
    path.write_text(json.dumps(out, indent=2) + "\n")
    for row in rows:
        print(
            f"g_e={row['g_e']:.3e} inv_a={row['inv_a_au']:.6e} "
            f"edge_au={row['a_edge_au']} verdict={row['verdict']} "
            f"n_outward={len(row['outward_r_kau'])}"
        )
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
