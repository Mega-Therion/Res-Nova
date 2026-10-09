#!/usr/bin/env python3
"""Regression tests for signed numeric parsing in SPARC Rotmod files."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np

from sparc_reproduce import load_rotmod


def main() -> None:
    rows = [
        "0.5 10.0 2.0 -3.5 4.0 0.0",
        "1.0 11.0 2.0 +2.25 5.0 0.0",
        "1.5 12.0 2.0 -4.0e+0 6.0 0.0",
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "TEST_rotmod.dat"
        path.write_text("\\n".join(rows) + "\\n")
        result = load_rotmod(path)

    assert result is not None, "valid fixture rows should be parsed"
    np.testing.assert_allclose(result["v_gas"], [-3.5, 2.25, -4.0])
    np.testing.assert_allclose(result["r"], [0.5, 1.0, 1.5])
    assert result["n_points"] == 3
    print("PASS — signed decimals, explicit plus sign, and scientific notation preserved")


if __name__ == "__main__":
    main()
