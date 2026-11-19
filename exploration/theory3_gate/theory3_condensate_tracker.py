#!/usr/bin/env python3
"""Correction to theory3_gate.py part (A), 2026-11-18. [O], order of magnitude.
If the w=1/3 tracker lives in AeST's own condensate (a K ~ (Q-Q0)^4 early regime), the shift-symmetry
first integral K_Q = I0/a^3 (TARGET_D5 §1.2) ties its amplitude to Omega_c: NOT a free initial
condition (theory3_gate.py (A) was wrong in this realisation). Continuity at the transition a_t gives
rho_phi/rho_r = a_t/a_eq before a_t. The BBN window then fixes a_t, and the condensate (= all the
dark matter in AeST) is radiation-like (c_ad^2 = 1/3, no clustering) until a_t."""
import json, math
r = math.sqrt(27 / 32)
x_lo, x_hi = 0.95 / r - 1, 1.05 / r - 1           # H^2/H^2_std = r(1+x) in [0.95, 1.05]
a_eq = 1 / 3400.0                                 # matter-radiation equality (CDM+baryons)
h = 0.70; Orh2 = 4.15e-5
H0sqrtOr = (h / 2997.92458) * math.sqrt(Orh2) / h  # Mpc^-1
out = {"x_window": [x_lo, x_hi], "x_exact_compensation": 1 / r - 1}
for tag, x in (("x_min", x_lo), ("x_exact", 1 / r - 1)):
    a_t = x * a_eq
    eta = a_t / H0sqrtOr                          # comoving horizon in RD, Mpc
    out[tag] = {"z_t": 1 / a_t - 1, "eta_t_Mpc": eta, "k_erased_above_per_Mpc": 1 / eta}
# what Lyman-alpha-cold dark matter allows (cold to k ~ 10/Mpc => horizon entry before a_t)
k_cold = 10.0
a_t_max = H0sqrtOr / k_cold
out["if_cold_to_k=10/Mpc"] = {"a_t_max": a_t_max, "z_t_min": 1 / a_t_max - 1, "x_max": a_t_max / a_eq,
                              "shortfall_vs_x_min": x_lo / (a_t_max / a_eq)}
out["verdict"] = ("[O] UNSAT: compensating BBN needs the condensate radiation-like until z~%.0e, "
                  "erasing dark-matter structure above k~%.1f/Mpc; cold-to-10/Mpc allows x<=%.1e, "
                  "%.0fx short of the BBN minimum." % (out["x_min"]["z_t"], out["x_min"]["k_erased_above_per_Mpc"],
                  out["if_cold_to_k=10/Mpc"]["x_max"], out["if_cold_to_k=10/Mpc"]["shortfall_vs_x_min"]))
print(json.dumps(out, indent=1)); json.dump(out, open("THEORY3_CONDENSATE_TRACKER.json", "w"), indent=1)
