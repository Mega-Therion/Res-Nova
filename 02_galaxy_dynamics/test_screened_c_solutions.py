#!/usr/bin/env python3
"""Drive screened_c_solutions on the real radial operator. No pasted Oort numbers."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

import screened_c_solutions as S

HERE = Path(__file__).resolve().parent


def test_two_runs_match_and_span_the_window():
    a = S.solve()
    b = S.solve()
    assert a["fields"] == b["fields"]
    assert a["equation"].startswith("Qs = z + S(x)")
    target = 1.0 / np.sqrt(1.0e4 * 1.0e5)
    for row in a["fields"]:
        z = row["C_zero"]
        p = row["C_oort_peak"]
        assert z["sign_change_outward"] is True
        assert z["inv_a_au"] > 1.0e-4
        assert abs(p["inv_a_au"] - target) / target < 1.0e-6
        assert 1.0e4 < p["a_edge_au"] < 1.0e5
        assert row["C_equals_P"]["sign_change_outward"] is False
        assert abs(row["C_equals_P"]["inv_a_au"]) < 1.0e-12
        # The peak C is not the pre-registered zero and not a retune of x*.
        assert p["C"] != 0.0
        assert 0.0 < p["C"] < row["P_ye"]


def test_script_entry_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(HERE / "screened_c_solutions.py")],
        cwd=HERE,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads((HERE / "SCREENED_C_SOLUTIONS.json").read_text())
    assert "sign_change_outward" in data["fields"][0]["C_zero"]
    assert np.isfinite(data["fields"][0]["C_zero"]["inv_a_au"])
    assert "C_oort_peak" in data["fields"][0]


if __name__ == "__main__":
    test_two_runs_match_and_span_the_window()
    test_script_entry_exits_zero()
    print("PASS")
