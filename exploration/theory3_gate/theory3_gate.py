#!/usr/bin/env python3
"""Theory-3 gate (2026-11-18): radiation-tracking w=1/3 compensator + Vainshtein screening.
Question: does "replace Q^3 with a w=1/3 tracker, screen Y with p>=3/2" give a SAT window on
BBN + Cassini + c_T=c without initial-condition tuning? Inputs are repo numbers only."""
import json, sympy as sp

lam = sp.symbols("lambda_s", positive=True)
lam_max = (27 + 12*sp.sqrt(6))/5                       # non-folding window (Wave3BBN, [D])
sup_ratio = sp.nsimplify(sp.simplify(lam_max/(1+lam_max)))  # K_B -> 0 edge
assert sp.simplify(sup_ratio**2 - sp.Rational(27, 32)) == 0
r = float(sup_ratio)                                    # 0.918559

# BBN: H^2/H^2_std = r/(1-Omega_phi) must lie in [0.95, 1.05]  (repo's 5% bound on G_cosmo/G_N)
Om_lo, Om_hi = 1 - r/0.95, 1 - r/1.05

# (A) Pure free w=1/3 field: rho_phi ~ a^-4 for ANY amplitude -> amplitude is an integration
#     constant. Delta N_eff is not predicted; it is the initial condition, renamed.
dNeff_needed = (1 - r) * (1 + 0.2271*3.044) / 0.2271 / r   # rho_phi/rho_r = (1-r)/r in N_eff units

# (B) Scaling attractor (exponential potential, slope k): Omega = 4/k^2 (RD), 3/k^2 (MD).
#     Amplitude now set by a Lagrangian constant, not ICs. RD window -> forced MD fraction:
k2_lo, k2_hi = 4/Om_hi, 4/Om_lo
Om_MD_min = 3/k2_hi
EDE_BOUND = 0.0036   # Planck 2015 XIV early-DE bound Omega_e (95%); verify before citing

# (C) Cassini: VAINSHTEIN_PREQ [D] needs p >= 1.890. Galileon order -> p, c_T status.
P_REQ = 1.890
vainshtein = {"cubic L3": (1.5, "c_T=c"), "quartic L4": (2.0, "c_T!=c (GW170817 excludes generic G4X)"),
              "quintic L5": (2.5, "c_T!=c (excluded)")}
cassini = {k: {"p": p, "clears_p_req": p >= P_REQ, "cT": c} for k, (p, c) in vainshtein.items()}

out = {
 "sup_G_cosmo_over_G_N": r, "BBN_Omega_phi_window_RD": [Om_lo, Om_hi],
 "A_free_dark_radiation": {"dNeff_for_exact_compensation": dNeff_needed,
     "verdict": "FAILS metric: amplitude is an initial condition"},
 "B_scaling_attractor": {"k2_window": [k2_lo, k2_hi], "Omega_MD_min": Om_MD_min,
     "EDE_bound": EDE_BOUND, "ratio": Om_MD_min/EDE_BOUND,
     "verdict": "UNSAT unless scaling exits before recombination (a new tuned scale)"},
 "C_cassini_vainshtein": cassini,
 "C_verdict": "cubic (the p>=3/2 proposal) fails p_req; quartic clears p_req but breaks c_T=c "
              "unless DHOST-tuned; no Horndeski Galileon is SAT on Cassini AND GW170817",
 "overall": "UNSAT as proposed (Theory 3). Panel's own rule then routes to Theory 1.",
}
print(json.dumps(out, indent=1))
json.dump(out, open("THEORY3_GATE.json", "w"), indent=1)
