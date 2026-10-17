#!/usr/bin/env python3
"""Closed form for the Oort window in C. Checks SCREENED_C_SOLUTIONS.json."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LO, HI = 1.0e4, 1.0e5


def c_of(p, inv0, target):
    return p * (1.0 - target / inv0)


def main():
    doc = json.loads((HERE / "SCREENED_C_SOLUTIONS.json").read_text())
    for row in doc["fields"]:
        p = row["P_ye"]
        inv0 = row["C_zero"]["inv_a_au"]
        centre = 1.0 / (LO * HI) ** 0.5
        c_lo = c_of(p, inv0, 1.0 / LO)
        c_hi = c_of(p, inv0, 1.0 / HI)
        c_mid = c_of(p, inv0, centre)
        stored = row["C_oort_peak"]["C"]
        err = abs(c_mid - stored)
        if err > 1e-12:
            raise SystemExit(f"centre mismatch {err}")
        if not (c_lo < c_mid < c_hi):
            raise SystemExit("window is not ordered")
        print(
            f"g_e={row['g_e_m_s2']:.3e} C_window=[{c_lo:.6f}, {c_hi:.6f}] "
            f"C_centre={c_mid:.6f} stored_err={err:.3e}"
        )
    print("MATCH")


if __name__ == "__main__":
    main()
