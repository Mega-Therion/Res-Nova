#!/usr/bin/env python3
"""Conformal time on the live dark-bubble H(a).

eta(a) = ∫ da / (a^2 E(a)), in units of c/H0.
E(a) is bg_at_N from weyl_causal_envelope.py (w_d = 0, kappa = -x0).
Future finiteness is the event-horizon question. Past finiteness is the
particle horizon. No edit to CURRENT_STATE.
"""

from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "drag_gcosmo"))
from weyl_causal_envelope import bg_at_N, compute_OL  # noqa: E402

POINTS = {
    "LCDM_control": {"kappa": 0.0, "h": 0.6810363151866539, "Om": 0.30360698573080336},
    "Pantheon+_best": {
        "kappa": -2.2444519783747996,
        "h": 0.6803247862228956,
        "Om": 0.30865546826192025,
    },
    "DES-Dovekie_best": {
        "kappa": -2.496571182856366,
        "h": 0.6801065733422411,
        "Om": 0.3093795670685889,
    },
}


def inv_a2E(a: float, h: float, Om: float, x0: float, OL: float) -> float:
    _a, E, *_ = bg_at_N(math.log(a), h, Om, x0, OL)
    return 1.0 / (a * a * E)


def integrate(
    a_lo: float, a_hi: float, h: float, Om: float, x0: float, OL: float, n: int = 20000
) -> float:
    """Log-spaced trapezoid. a_lo > 0."""
    log_lo, log_hi = math.log(a_lo), math.log(a_hi)
    step = (log_hi - log_lo) / n
    acc = 0.0
    prev_a = a_lo
    prev_f = inv_a2E(prev_a, h, Om, x0, OL)
    for i in range(1, n + 1):
        a = math.exp(log_lo + i * step)
        f = inv_a2E(a, h, Om, x0, OL)
        acc += 0.5 * (prev_f + f) * (a - prev_a)
        prev_a, prev_f = a, f
    return acc


def asymptote_C(h: float, Om: float, x0: float, OL: float) -> float | None:
    """If E ~ C/a at large a, return C. None when x0 = 0 (E -> const)."""
    if x0 <= 0.0:
        return None
    a = 1.0e6
    _a, E, *_ = bg_at_N(math.log(a), h, Om, x0, OL)
    return E * a


def main() -> dict:
    out = {
        "definition": "eta = ∫ da/(a^2 E(a)) in units c/H0, E from weyl_causal_envelope.bg_at_N",
        "backgrounds": {},
    }
    for name, p in POINTS.items():
        kappa, h, Om = p["kappa"], p["h"], p["Om"]
        x0 = -kappa
        OL = compute_OL(h, Om, kappa)
        past = integrate(1.0e-12, 1.0, h, Om, x0, OL)
        # radiation tail below 1e-12: integrand ~ const, width 1e-12, negligible
        if x0 <= 0.0:
            fut_1_8 = integrate(1.0, 8.0, h, Om, x0, OL)
            fut_8_1e6 = integrate(8.0, 1.0e6, h, Om, x0, OL)
            tail = 1.0 / (1.0e6 * math.sqrt(OL))
            future_total = fut_1_8 + fut_8_1e6 + tail
            out["backgrounds"][name] = {
                "kappa": kappa,
                "x0": x0,
                "h": h,
                "Om": Om,
                "OL": OL,
                "eta_past_0_to_1": past,
                "eta_future_1_to_8": fut_1_8,
                "eta_future_total": future_total,
                "late_E_times_a": None,
                "future_conformal_time": "finite",
                "event_horizon": True,
                "tail": "Λ term: E -> sqrt(OL), ∫_A^∞ da/(a^2 E) = 1/(A sqrt(OL))",
            }
        else:
            # Float erfi(exp) overflows past a ~ 20. Match to the stable asymptotic
            # E ~ C/a with C = 2 sqrt(OL/x0), from y5 ~ -a^4 - (4/kappa) a^2.
            C = 2.0 * math.sqrt(OL / x0)
            a_match = 8.0
            fut_1_match = integrate(1.0, a_match, h, Om, x0, OL)
            _a, E_m, *_ = bg_at_N(math.log(a_match), h, Om, x0, OL)
            out["backgrounds"][name] = {
                "kappa": kappa,
                "x0": x0,
                "h": h,
                "Om": Om,
                "OL": OL,
                "eta_past_0_to_1": past,
                "eta_future_1_to_8": fut_1_match,
                "E_times_a_at_8": E_m * a_match,
                "late_E_times_a_analytic": C,
                "future_tail": "∫_8^∞ da/(a^2 E) ~ (1/C) ln(a/8) -> ∞",
                "future_conformal_time": "diverges_logarithmically",
                "event_horizon": False,
            }
    path = os.path.join(HERE, "CONFORMAL_TIME_INTEGRAL.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
