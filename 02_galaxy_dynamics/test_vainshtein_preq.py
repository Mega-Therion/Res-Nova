"""The recomputed exponent is read from the live gate file, not a pasted number."""

import json
from pathlib import Path

from vainshtein_preq import P_CUBIC, requirements


def test_cubic_galileon_misses_the_constant_tail_and_the_q2_line_is_only_a_scaling():
    gate = json.loads(Path(__file__).with_name("SECOND_FIELD_GATES.json").read_text())
    q2 = float(gate["ge"]["1.9e-10"]["Q2"])
    got = requirements(q2)
    assert got["p_cubic"] == P_CUBIC
    assert got["p_req_precession"] > P_CUBIC
    assert got["cubic_clears_precession"] is False
    assert got["Q2_scaled_cubic"] < got["Q2_ceiling_2026"]
    assert got["scaling_is_not_a_cassini_pass"] is True
    assert got["p_req_Q2_scaling"] < P_CUBIC
