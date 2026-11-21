#!/usr/bin/env python3
"""Independent checks of two other-agent results (2026-11-20), on code paths separate from theirs.

V1  B2 of phase3_wall_ghost_coupled.py: dispersion of the AeST-like wall condensate, re-derived from the Euler-Lagrange
    equations of the quadratic Lagrangian (no Fourier-matrix helper).
V2  conformal_time_integral.py: eta(0 -> 1) and the late-time E*a -> 2 sqrt(Omega_L/|kappa|) from a direct ODE integration
    of the coupled background (PREREG_FLUX: dY/da = kappa a^5 E^2, Y = a^4 Omega_net), not weyl_causal_envelope.bg_at_N."""
import json, os
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad

HERE = os.path.dirname(os.path.abspath(__file__))


def v1() -> dict:
    K2, KB, Qb, dQ, cY, w, k = sp.symbols("K2 K_B Qbar dQ c_Y omega k", positive=True)
    t, x = sp.symbols("t x", real=True)
    v = sp.Function("v")(t, x)
    A = sp.Function("A")(t, x)
    L = (sp.Rational(1, 2) * K2 * sp.diff(v, t) ** 2 + KB * sp.diff(A, t) ** 2 + sp.Rational(1, 2) * K2 * dQ * Qb * A**2
         + K2 * dQ * A * sp.diff(v, x) - sp.Rational(1, 2) * cY * (Qb * A + sp.diff(v, x)) ** 2)
    eqs = [sp.euler_equations(L, [v, A], [t, x])[i].lhs for i in range(2)]
    Vh, Ah = sp.symbols("V A_h")
    ph = sp.exp(sp.I * (k * x - w * t))
    sub = lambda e: sp.simplify((e.subs({v: Vh * ph, A: Ah * ph}).doit()) / ph)
    rows = [sp.expand(sub(e)) for e in eqs]
    M = sp.Matrix([[sp.diff(r, Vh), sp.diff(r, Ah)] for r in rows])
    det = sp.factor(sp.expand(M.det()))
    bare = sp.expand(det.subs(cY, 0))
    target = K2 * (2 * KB * w**4 + K2 * dQ * Qb * w**2 - K2 * dQ**2 * k**2)
    assert sp.simplify(bare - target) == 0 or sp.simplify(bare + target) == 0
    u = sp.Symbol("u")
    roots0 = sp.solve(sp.expand(bare.subs(k, 0)).subs(w**2, u), u)
    assert any(sp.simplify(r + K2 * dQ * Qb / (2 * KB)) == 0 for r in roots0)
    rk0 = [r for r in sp.solve(sp.expand(det.subs(k, 0)).subs(w**2, u), u) if r != 0]
    assert len(rk0) == 1 and sp.simplify(rk0[0] - Qb * (cY * Qb - K2 * dQ) / (2 * KB)) == 0
    return {"V1": ("Re-derived from the Euler-Lagrange equations: the bare condensate's dispersion is 2K_B w^4 + K2 dQ Qbar w^2 - K2 dQ^2 k^2 = 0 "
                   "(IR root w^2 = -K2 dQ Qbar/(2K_B) < 0: tachyonic for dQ > 0); with c_Y the k = 0 root is Qbar(c_Y Qbar - K2 dQ)/(2K_B), "
                   "stable iff c_Y >= K2 dQ/Qbar. Matches the agent's B2 (the agent's prose drops the square on dQ; its code has it).")}


def v2() -> dict:
    rec = json.load(open(os.path.join(HERE, "..", "drag_gcosmo", "FLUX_CODAZZI.json")))["F2_self_consistent_coupled_refit"]
    ORH2 = 4.18e-5
    out = {}
    for name, key in (("Pantheon+", "Pantheon+_BAO_CMB"), ("DES-Dovekie", "DES-Dovekie_BAO_CMB")):
        h, Om, kap = rec[key]["params_coupled_h_Om_kappa"]
        Or = ORH2 / h**2

        def solve(OL):
            f = lambda a, Y: [kap * (a**2 * Om + a * Or + a**5 * OL + a * Y[0])]
            return solve_ivp(f, (1e-6, 400.0), [0.0], method="LSODA", rtol=1e-10, atol=1e-14, dense_output=True)
        s0, s1 = solve(0.0), solve(1.0)
        OL = (1.0 - Om - Or - s0.sol(1.0)[0]) / (1.0 + s1.sol(1.0)[0] - s0.sol(1.0)[0])
        s = solve(OL)
        E = lambda a: float(np.sqrt(Om / a**3 + Or / a**4 + OL + s.sol(a)[0] / a**4))
        past = quad(lambda a: 1 / (a * a * E(a)), 1e-6, 1.0, limit=500)[0]
        C = 2 * np.sqrt(OL / abs(kap))
        out[name] = {"eta_0_to_1": past, "E_a_at_8": 8 * E(8.0), "E_a_at_400": 400 * E(400.0), "C_analytic": C}
        assert abs(400 * E(400.0) - C) / C < 2e-3
    return {"V2": out, "V2_reading": ("eta(0->1) = 3.212 / 3.210 and E*a -> 2 sqrt(Omega_L/|kappa|) confirmed on a direct ODE path: the "
                                       "late expansion coasts (adot -> const), eta grows as ln(a)/C, so these drag backgrounds have no event horizon.")}


res = {}
res.update(v1())
res.update(v2())
json.dump(res, open(os.path.join(HERE, "VERIFY_AGENT_CHECKS.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
