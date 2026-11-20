#!/usr/bin/env python3
"""Phase 2, open item 2 (matter sector): does bulk-carried 4D matter on the dark bubble respond like linearized 4D GR
for time-dependent (relativistic) sources? Verifies the algebra of arXiv:2001.07433 eqs. (fouriertransformT)-(onehalf),
which use the Lorentzian 4-momentum p^2 = -p0^2 + |p|^2 and include wall bending F."""
import json, os
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
kp, km, k5, p2 = sp.symbols("k_p k_m kappa5sq p2", positive=True)
T, Tab, eta = sp.symbols("T T_ab eta_ab", real=True)
alpha = (1 / kp - 1 / km) / (4 * k5)                       # alpha = (1/4 kappa5^2)(1/k+ - 1/k-)
F = k5 * T / (3 * (1 / kp - 1 / km) * p2)                  # from T~ = (3/kappa5^2)(1/k+ - 1/k-) p^2 F~
h = -(Tab - T * eta / 3) / (alpha * p2) + 2 * F * eta      # chi + 2F eta (q-term cancels the p_a p_b F piece)
h_GR = -(Tab - T * eta / 2) / (alpha * p2)
assert sp.simplify(h - h_GR) == 0
G4_over_G5 = 2 * kp * km / (km - kp)
kappa4sq = k5 * G4_over_G5                                  # kappa_4^2 = 8 pi G4 = kappa5^2 G4/G5
assert sp.simplify(1 / alpha - 2 * kappa4sq) == 0
res = {
    "algebra_verified": "h_ab = -(2 kappa4^2/p^2)(T_ab - T eta_ab/2) with kappa4^2 = 8 pi G4, G4 = 2 k+ k- G5/(k- - k+)",
    "scope": ("arXiv:2001.07433 sec. 3.1 uses the Lorentzian 4-momentum p^2 = -p0^2 + |p|^2 and includes the wall bending F, which converts "
              "the 5D tensor structure (T - T eta/3) into the 4D one (T - T eta/2). So at p << a k the full linear response to "
              "time-dependent sources is linearized 4D GR with G4, not only the static Newtonian limit of 1807.01570."),
    "sign": "The physical positive source is -Sigma (wall matter enters negative and is overcompensated by bulk string pull), as the paper states.",
    "matter_content": ("String endpoints act as point particles of mass tau/k on the wall (2001.07433 eq. near line 170): dust. "
                       "Worldvolume EM radiation gravitates as 4D radiation after backreaction (2310.15032 sec. 4.2)."),
    "remaining": ("Flat-background result: corrections O(p/(a k)) and, on an FRW wall, O(H/k). The endpoints' own equations of motion "
                  "are taken as point-particle (dust) dynamics; deriving them from the string action is not done here."),
    "status_change": "Phase 2 open item 2 (matter sector) moves from [O] to [D] at leading order in p/(a k) and H/k.",
}
json.dump(res, open(os.path.join(HERE, "PHASE2_MATTER_SECTOR.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
