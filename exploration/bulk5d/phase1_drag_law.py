#!/usr/bin/env python3
"""Phase 1 of the 5D bulk perturbation solve (PREREG_PHASE1.md): which drag-momentum law
does a 5D-covariant drag give?

Candidate (a): velocity-dependent tension sigma(X), X = (xi.n)^2, xi = d/dt (bulk static Killing).
  A1  X = adot^2 for the expanding wall in flat-sliced AdS(-Schwarzschild).
  A2  dark-bubble junction + sigma(X) reproduces the drag background H^2 ~ [...]/(1 + x0 a^2).
  A3  tangential S_mn = -sigma(X) h_mn: w = -1, zero momentum, momentum balance -d_i delta sigma.
  A4  required flux Q4 = d(Delta Sigma)/dtau; NEC factor s_NEC = (3/2)(1 + w_d) - q at w_d = -1
      on the FLUX_CODAZZI Pantheon+ best-fit background (data depend only on kappa).
Candidate (b): absorbed bulk null dust T_AB = psi l_A l_B.
  B1  deposited momentum ~ e^A_mu l_A = -d_mu (V|wall) exactly (v = advanced EF coordinate).
  B2  so the flux frame u_F is the normal to wall-restricted V = const slices (Law A form).
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def candidate_a_symbolic() -> dict:
    tau = sp.Symbol("tau", real=True)
    k, mu, G5, rho_b, sig0 = sp.symbols("k mu G5 rho_b sigma0", positive=True)
    a = sp.Function("a", positive=True)(tau)
    ad = sp.diff(a, tau)
    f = k**2 * a**2 - mu / a**2

    # A1: static coords (t, r, x^i): g = diag(-f, 1/f, r^2, r^2, r^2). Wall at r = a(tau), t = T(tau),
    # with -f Tdot^2 + adot^2/f = -1  =>  Tdot = sqrt(f + adot^2)/f.
    Td = sp.sqrt(f + ad**2) / f
    assert sp.simplify(-f * Td**2 + ad**2 / f + 1) == 0
    n_t, n_r = -ad, Td  # covariant unit normal (outward)
    norm = sp.simplify(n_t**2 * (-1 / f) + n_r**2 * f)
    assert sp.simplify(norm - 1) == 0
    u_dot_n = sp.simplify(Td * n_t + ad * n_r)  # tangency: u^A n_A = 0
    assert u_dot_n == 0
    X = sp.simplify(n_t**2)  # xi^A n_A = n_t with xi = d/dt
    assert sp.simplify(X - ad**2) == 0

    # A2: dark-bubble junction (flat slicing): wall energy rho_wall = (3/8 pi G5)[sqrt(f_- + adot^2) - sqrt(f_+ + adot^2)]/a
    km, kp, mum, mup, H, eps = sp.symbols("k_m k_p mu_m mu_p H epsilon", positive=True)
    A = sp.Symbol("a0", positive=True)
    root = lambda kk, mm: sp.sqrt(kk**2 - mm / A**4 + H**2)
    rho_wall = 3 / (8 * sp.pi * G5) * (root(km, mum) - root(kp, mup))
    # leading order in (H^2, mu/a^4) << k^2: scale H -> eps H, mu -> eps^2 mu and expand to eps^2
    lead = sp.series(rho_wall.subs({H: eps * H, mum: eps**2 * mum, mup: eps**2 * mup}), eps, 0, 3).removeO().subs(eps, 1)
    sig_ext = 3 * (km - kp) / (8 * sp.pi * G5)
    G4 = 2 * kp * km * G5 / (km - kp)
    c_coef = 3 / (8 * sp.pi * G4)
    dark_rad = (mup / kp - mum / km) / A**4
    # claim: sigma_ext - rho_wall = c [H^2 - (3/(8 pi G4))^{-1} * (3/(16 pi G5)) dark_rad ]  i.e. linear in H^2
    resid = sp.simplify(sp.expand(sig_ext - lead - (c_coef * H**2 - 3 / (16 * sp.pi * G5) * dark_rad)))
    assert resid == 0
    # with rho_wall = sigma0 + (1/2) rho_b a^2 H^2 + (bulk-sourced 4D matter enters with the paper's sign, rho_eff):
    rho_eff = sp.Symbol("rho_eff", real=True)
    Hsq = sp.solve(sp.Eq(sig_ext - (sig0 + sp.Rational(1, 2) * rho_b * A**2 * H**2) + rho_eff, c_coef * H**2), H**2)[0]
    x0_expr = sp.simplify(sp.Rational(1, 2) * rho_b / c_coef)  # coefficient of a^2 in (1 + x0 a^2)
    drag_form = sp.simplify(Hsq - (8 * sp.pi * G4 / 3) * (sig_ext - sig0 + rho_eff) / (1 + x0_expr * A**2))
    assert drag_form == 0

    # A3: tangential stress of a sigma(X) wall is -sigma(X) h_mn (X carries no h-dependence at fixed embedding).
    # FRW wall: h = diag(-1, a^2, a^2, a^2).  rho_d = sigma, p_d = -sigma  => w = -1, T^0_i = 0 in every frame.
    hmat = sp.diag(-1, A**2, A**2, A**2)
    sgm = sp.Symbol("sigma_X", positive=True)
    S = -sgm * hmat
    S_up = hmat.inv() * S  # S^mu_nu
    rho_d, p_d = -S_up[0, 0], S_up[1, 1]
    assert sp.simplify(rho_d - sgm) == 0 and sp.simplify(p_d + sgm) == 0
    assert all(S[0, i] == 0 for i in range(1, 4))
    # boosted observer u = gamma(1, v, 0, 0)/...: momentum density -S_mn u^m e^n = sigma h_mn u^m e^n = 0 for e orthogonal to u
    v = sp.Symbol("v", real=True)
    gam = 1 / sp.sqrt(1 - v**2)
    u = sp.Matrix([gam, gam * v / A, 0, 0])
    e1 = sp.Matrix([gam * v, gam / A, 0, 0])  # unit spatial vector orthogonal to u
    assert sp.simplify((u.T * hmat * e1)[0]) == 0
    mom = sp.simplify(-(u.T * S * e1)[0])
    assert mom == 0
    # Codazzi D^mu S_mu nu = -d_nu sigma(X): energy part gives sigma_dot = Q4 (flux), momentum part -d_i delta sigma.
    return {
        "A1_X_equals_adot_sq": True,
        "A1_note": "X = (xi.n)^2 = adot^2 for a wall at r = a(tau) in flat-sliced AdS-Schwarzschild; xi = d/dt",
        "A2_junction_leading_order_linear_in_H2": True,
        "A2_G4": "G4 = 2 k_+ k_- G5 / (k_- - k_+)  (matches 1807.01570)",
        "A2_drag_background_reproduced": True,
        "A2_x0": "x0 = (4 pi G4 / 3) rho_b  (sigma = sigma0 + rho_b adot^2 / 2; a = 1 today)",
        "A3_wd": -1,
        "A3_momentum_density_all_frames": 0,
        "A3_momentum_balance": "Q_i = -d_i delta sigma = -sigma'(X) d_i delta X  (no Phi term: rho + p = 0)",
        "A3_vs_LawC": "Law C has w_d = 0 and Q_i = -K^2 Omega_d Phi; the covariant sigma(X) wall has w = -1 and Q_i = -d_i delta sigma: not Law C",
        "A4_flux_required": "Q4 = d(Delta Sigma)/dtau = 2 H Delta Sigma (-q)  (vacuum bulk would force sigma_dot = 0)",
    }


def candidate_a_numeric() -> dict:
    sys.path.insert(0, os.path.join(HERE, "..", "drag_gcosmo"))
    cwd = os.getcwd()
    os.chdir(os.path.join(HERE, "..", "drag_gcosmo"))
    try:
        import flux_codazzi_check as F
    finally:
        os.chdir(cwd)
    rec = json.load(open(os.path.join(HERE, "..", "drag_gcosmo", "FLUX_CODAZZI.json")))
    out = {}
    for label, key in (("Pantheon+_BAO_CMB", "Pantheon+_BAO_CMB"), ("DES-Dovekie_BAO_CMB", "DES-Dovekie_BAO_CMB")):
        h, Om, kap = rec["F2_self_consistent_coupled_refit"][key]["params_coupled_h_Om_kappa"]
        z = np.linspace(0.0, 10.0, 20001)
        E, _ = F.E_coupled(z, h, Om, kap)
        lnE = np.log(E)
        q = -1.0 + (1.0 + z) * np.gradient(lnE, z)
        s_nec = 1.5 * (1.0 + (-1.0)) - q  # w_d = -1
        sign_change = bool(np.any(s_nec > 0) and np.any(s_nec < 0))
        i0 = int(np.argmax(s_nec < 0)) if np.any(s_nec < 0) else None
        out[label] = {
            "kappa": kap, "x0_at_wd_minus1": abs(kap) / 4.0, "x0_at_wd_0": abs(kap),
            "s_NEC_at_z0": float(s_nec[0]), "s_NEC_at_z2": float(np.interp(2.0, z, s_nec)),
            "s_NEC_min": float(s_nec.min()), "s_NEC_max": float(s_nec.max()),
            "z_sign_flip": float(z[i0]) if i0 is not None else None,
            "sign_changes_on_0_10": sign_change,
            "verdict_a": "[X] (NEC channel rule: Q4 flips sign at the onset of acceleration)" if sign_change else "live",
        }
    return out


def candidate_b_symbolic() -> dict:
    # Ingoing Eddington-Finkelstein: ds^2 = -f dv^2 + 2 dv dr + r^2 dx^2 (eps = +1), coordinates (v, r, x, y, z)
    v, r, x, y, zc = sp.symbols("v r x y z", real=True)
    k, mu = sp.symbols("k mu", positive=True)
    f = k**2 * r**2 - mu / r**2
    g = sp.zeros(5, 5)
    g[0, 0] = -f
    g[0, 1] = g[1, 0] = 1
    for i in (2, 3, 4):
        g[i, i] = r**2
    ginv = sp.simplify(g.inv())
    l_low = sp.Matrix([-1, 0, 0, 0, 0])  # l_A = -d_A v
    assert sp.simplify((l_low.T * ginv * l_low)[0]) == 0  # null
    l_up = ginv * l_low
    # geodesic: l^B nabla_B l_A = l^B (d_B l_A - Gamma^C_BA l_C); d_B l_A = 0, so check -l^B Gamma^C_BA l_C
    coords = [v, r, x, y, zc]
    Gam = [[[sum(ginv[C, D] * (sp.diff(g[D, A], coords[B]) + sp.diff(g[D, B], coords[A]) - sp.diff(g[A, B], coords[D])) / 2
                 for D in range(5)) for B in range(5)] for A in range(5)] for C in range(5)]
    acc = [sp.simplify(-sum(l_up[B] * Gam[C][B][A] * l_low[C] for B in range(5) for C in range(5))) for A in range(5)]
    assert all(t == 0 for t in acc)
    # perturbed wall embedding X^A(tau, y^i) = (V(tau, y), R(tau, y), y^1, y^2, y^3)
    tau, y1, y2, y3 = sp.symbols("tau y1 y2 y3", real=True)
    V = sp.Function("V")(tau, y1, y2, y3)
    R = sp.Function("R")(tau, y1, y2, y3)
    Xemb = [V, R, y1, y2, y3]
    wall = [tau, y1, y2, y3]
    e = [[sp.diff(Xemb[A], wall[m]) for A in range(5)] for m in range(4)]
    proj = [sp.simplify(sum(l_low[A] * e[m][A] for A in range(5))) for m in range(4)]
    assert all(sp.simplify(proj[m] + sp.diff(V, wall[m])) == 0 for m in range(4))
    return {
        "B1_l_null_and_geodesic": True,
        "B1_projection_identity": "e^A_mu l_A = -d_mu (V|wall) exactly, for any wall embedding (V, R)(tau, y)",
        "B1_deposited_momentum": "Q_mu = -[psi (l.n)] e^A_mu l_A  proportional to  d_mu V|wall",
        "B2_flux_frame": "u_F,mu = -d_mu V / sqrt(-h^ab d_a V d_b V): the normal to wall-restricted V = const slices (hypersurface-orthogonal)",
        "B2_law": "Law A (Q_mu = q4 u_F,mu) whenever the absorbed energy is stored in a momentum-carrying wall component",
        "B2_two_channels": "with inflow from both sides (outside ingoing V, inside outgoing U) u_F is the q-weighted sum of -dV and -dU",
        "B3_remaining": "u_F - u_m needs delta V|wall = delta T + delta R / f in wall longitudinal gauge, i.e. the bending from the asymmetric junction plus the bulk solution (Phase 2). The envelope's 'bulk_rest' convention is the special case delta V|wall = 0 on CN slices.",
    }


def main() -> int:
    res = {"candidate_a": candidate_a_symbolic()}
    res["candidate_a"]["A4_numeric"] = candidate_a_numeric()
    res["candidate_b"] = candidate_b_symbolic()
    a_dead = all(v["sign_changes_on_0_10"] for v in res["candidate_a"]["A4_numeric"].values())
    res["preregistered_decision"] = (
        "(a) [X]: the covariant sigma(X) drag reproduces the drag background exactly but is w = -1 and needs a flux that "
        "flips sign at the onset of acceleration. (b) gives Law A with a computed flux frame. So the envelope's Law A numbers "
        "apply (survives only at c_vis^2 = 0, 0.4% inside the ISW gate); Phase 2 narrows to pi_E from the bulk and u_F from delta V."
        if a_dead else "(a) live: see A4_numeric"
    )
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(HERE, "PHASE1_DRAG_LAW.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
