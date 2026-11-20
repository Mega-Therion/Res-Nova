#!/usr/bin/env python3
"""Correction (2026-11-19): what the k-weighting of the two sides does to the closure seen on the wall.
The envelope's c_vis^2 is a ratio, pi_eff / rho_eff, not pi_eff alone."""
import json, os
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
kp, km = sp.symbols("k_p k_m", positive=True)
rp, rm, pp, pm, cbar, dc = sp.symbols("rho_p rho_m pi_p pi_m cbar dc", real=True)
w = lambda xp, xm: (km * xp - kp * xm) / (km - kp)           # P0: X_eff = (k- X+ - k+ X-)/(k- - k+)
R = sp.simplify(w(pp, pm) / w(rp, rm))
assert sp.simplify(R - (pp / kp - pm / km) / (rp / kp - rm / km)) == 0
single = sp.simplify(R.subs({rm: 0, pm: 0}))
assert sp.simplify(single - pp / rp) == 0                     # single-sided: k's drop out
c = sp.Symbol("c", real=True)
same = sp.simplify(R.subs({pp: c * rp, pm: c * rm}))
assert sp.simplify(same - c) == 0                             # same closure both sides: k's drop out
two = sp.simplify(R.subs({pp: (cbar + dc / 2) * rp, pm: (cbar - dc / 2) * rm}))
A = (km * rp + kp * rm) / (km * rp - kp * rm)
assert sp.simplify(two - (cbar + dc / 2 * A)) == 0            # general: R = cbar + (dc/2) A
assert sp.simplify(A.subs(rm, 0) - 1) == 0
res = {
    "identity": "pi_eff/rho_eff = (pi+/k+ - pi-/k-)/(rho+/k+ - rho-/k-)",
    "single_sided": "rho- = pi- = 0  =>  pi_eff/rho_eff = pi+/rho+ : k+, k- and Delta k drop out exactly",
    "same_closure": "pi+- = c rho+-  =>  pi_eff/rho_eff = c : k's drop out exactly",
    "general": "pi+- = (cbar +- dc/2) rho+-  =>  pi_eff/rho_eff = cbar + (dc/2) A,  A = (k- rho+ + k+ rho-)/(k- rho+ - k+ rho-)",
    "reading": ("Amplification needs BOTH dark radiation on both sides that nearly cancels in k- rho+ - k+ rho- AND different "
                "closures on the two sides (dc != 0). Delta k does not appear on its own. The earlier statements "
                "'near-symmetric bubble amplifies by k/(k- - k+)' (P0 O2, Phase 2 J1) were too strong and are corrected."),
    "status_change": ("Delta k leaves the open list: for single-sided feeding it is irrelevant to the closure; for two-sided "
                      "feeding what matters is the split k- rho+ vs k+ rho-, which is part of the flux-source specification."),
}
json.dump(res, open(os.path.join(HERE, "DK_RATIO_IDENTITY.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
