#!/usr/bin/env python3
"""Regression tests for the SPARC reproduction pipeline. No SPARC data needed: synthetic fixtures only.

1. Signed numeric parsing: leading minus, explicit plus, scientific notation.
2. Signed baryonic velocity: V_bar^2 = V_gas|V_gas| + Yd V_disk^2 + Yb V_bul^2.
3. Model parity: sparc_reproduce (regex loader, its own V_bar and mu_std prediction) against
   parameter_ledger (line.split loader, v_bary_sq, v_mond_like). The comparison is made at
   Yd, Yb != 1 and fd != 1, on a galaxy with a negative V_gas and a bulge. At Y = 1 and fd = 1,
   Y^2 = Y and fd drops out, so the two defects found on 2026-10-09 (Y applied to V instead of
   V^2, and fd dividing R instead of scaling V_bar^2 and R) were invisible.

    python3 02_galaxy_dynamics/test_sparc_parser.py     # exit 0 on PASS
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parameter_ledger as pl  # noqa: E402
from sparc_reproduce import A0_HORIZON, load_rotmod, predict_velocity, v_baryon  # noqa: E402

ROWS = [
    "0.5 10.0 2.0 -3.5 4.0 0.0",
    "1.0 11.0 2.0 +2.25 5.0 0.0",
    "1.5 12.0 2.0 -4.0e+0 6.0 0.0",
]
# A galaxy with a bulge and a negative V_gas, enough points for both loaders (>= 5).
PARITY_ROWS = [
    "0.5 40.0 3.0 -5.0 30.0 20.0",
    "1.0 60.0 3.0 2.0 45.0 25.0",
    "2.0 80.0 3.0 8.0 55.0 22.0",
    "4.0 95.0 4.0 15.0 60.0 18.0",
    "8.0 100.0 5.0 25.0 52.0 12.0",
    "12.0 102.0 6.0 30.0 44.0 9.0",
]


def write(rows: list[str], tmp: str, name: str) -> Path:
    path = Path(tmp) / f"{name}_rotmod.dat"
    path.write_text("# R Vobs errV Vgas Vdisk Vbul\n" + "\n".join(rows) + "\n")
    return path


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        result = load_rotmod(write(ROWS, tmp, "TEST"))
        assert result is not None, "valid fixture rows should be parsed"
        np.testing.assert_allclose(result["v_gas"], [-3.5, 2.25, -4.0])
        np.testing.assert_allclose(result["r"], [0.5, 1.0, 1.5])
        assert result["n_points"] == 3

        # Row 0: vgas=-3.5, vdisk=4.0 -> V_bar^2 = -12.25 + 16.0 = 3.75 at unit M/L.
        vb = v_baryon(result["v_gas"], result["v_disk"], result["v_bulge"], 1.0, 1.0)
        np.testing.assert_allclose(vb[0], np.sqrt(-3.5 * 3.5 + 4.0**2))
        # Y multiplies V^2: at Yd = 0.5, V_bar^2 = -12.25 + 0.5 * 16.0 < 0 -> clamped, not (0.5 * 4)^2 = 4.
        vb_half = v_baryon(result["v_gas"], result["v_disk"], result["v_bulge"], 0.5, 1.0)
        assert vb_half[0] < 1e-5, f"Y must multiply V^2, got V_bar = {vb_half[0]}"

        sr = load_rotmod(write(PARITY_ROWS, tmp, "PARITY"))
        led = pl.load(Path(tmp))
        led = [g for g in led if g["name"] == "PARITY"]
        assert sr is not None and len(led) == 1, "both loaders must accept the parity fixture"
        L = led[0]
        for yd, yb, fd in ((1.3, 0.4, 1.12), (0.5, 0.7, 0.88), (1.0, 1.0, 1.0)):
            vbar_l = np.sqrt(pl.v_bary_sq(L, yd, yb, fd))
            vbar_r = np.sqrt(fd) * v_baryon(sr["v_gas"], sr["v_disk"], sr["v_bulge"], yd, yb)
            np.testing.assert_allclose(vbar_r, vbar_l, rtol=1e-12, atol=1e-9,
                                       err_msg=f"V_bar parity at Yd={yd}, Yb={yb}, fd={fd}")
            vp_l = pl.v_mond_like(L, pl.A0_HORIZON, yd, yb, fd)
            vp_r = predict_velocity(v_baryon(sr["v_gas"], sr["v_disk"], sr["v_bulge"], yd, yb), sr["r"], A0_HORIZON, fd)
            np.testing.assert_allclose(vp_r, vp_l, rtol=1e-9, atol=1e-6,
                                       err_msg=f"mu_std prediction parity at Yd={yd}, Yb={yb}, fd={fd}")

    print("PASS: signed parsing, signed V_bar with Y on V^2, and sparc_reproduce == parameter_ledger at Y != 1, fd != 1")


if __name__ == "__main__":
    main()
