#!/usr/bin/env python3
"""Regression tests for signed numeric parsing and signed baryon velocity in SPARC Rotmod files."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np

from sparc_reproduce import load_rotmod, v_baryon


def main() -> None:
    rows = [
        "0.5 10.0 2.0 -3.5 4.0 0.0",
        "1.0 11.0 2.0 +2.25 5.0 0.0",
        "1.5 12.0 2.0 -4.0e+0 6.0 0.0",
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "TEST_rotmod.dat"
        path.write_text("\n".join(rows) + "\n")
        result = load_rotmod(path)

    assert result is not None, "valid fixture rows should be parsed"
    np.testing.assert_allclose(result["v_gas"], [-3.5, 2.25, -4.0])
    np.testing.assert_allclose(result["r"], [0.5, 1.0, 1.5])
    assert result["n_points"] == 3

    # Test v_baryon preserves signed v_gas^2 contribution (v_gas * |v_gas|)
    # Row 0: vgas=-3.5, vdisk=4.0, vbul=0 -> v_bary^2 = -3.5*3.5 + 4.0^2 = -12.25 + 16.0 = 3.75 -> sqrt(3.75) ~ 1.93649
    vb = v_baryon(result["v_gas"], result["v_disk"], result["v_bulge"], 1.0, 1.0)
    expected_v0 = np.sqrt(-3.5 * 3.5 + 4.0**2)
    np.testing.assert_allclose(vb[0], expected_v0)

    print("PASS — signed decimals, explicit plus sign, scientific notation, and signed v_baryon preserved")


if __name__ == "__main__":
    main()
