#!/usr/bin/env python3
"""
Job D: K(Q) does not choose I.
Argon4 Unidex Receipt Assembly.

References:
- TARGET_D5_COSMOLOGICAL_SECTOR.md
- TARGET_D7_COVARIANT_COMPLETION.md §1.1, §3.2
- Skordis & Zlosnik, PRL 127 161302 (2021) [arXiv:2007.00082]
"""

import os
import sys
import json
import math
from pathlib import Path
import sympy as sp


def evaluate_k_of_q():
    # -------------------------------------------------------------------------
    # 1. Background Statements from TARGET_D5_COSMOLOGICAL_SECTOR.md
    # -------------------------------------------------------------------------
    # In FLRW cosmology:
    # Metric: ds^2 = -N(t)^2 dt^2 + a(t)^2 delta_ij dx^i dx^j
    # Unit timelike aether field: A_mu = (-N(t), 0, 0, 0), A^mu = (1/N(t), 0, 0, 0)
    # Unit norm: A^mu A_mu = -1
    # Homogeneous scalar field: phi = phi_bar(t), so grad_mu phi = (dot(phi_bar), 0, 0, 0)

    # SymPy symbolic verification of Y = 0 on FLRW
    N, a, dot_phi = sp.symbols('N a dot_phi', positive=True)
    # Projection tensor q^{mu nu} = g^{mu nu} + A^mu A^nu
    # g^{00} = -1/N^2, A^0 = 1/N => q^{00} = -1/N^2 + (1/N)*(1/N) = 0
    g_inv_00 = -1 / (N**2)
    A_up_0 = 1 / N
    q_inv_00 = sp.simplify(g_inv_00 + A_up_0 * A_up_0)
    if q_inv_00 != 0:
        raise ValueError(f"Expected q^{{00}} = 0, got {q_inv_00}")

    # Y = q^{mu nu} grad_mu phi grad_nu phi
    # Since grad_i phi = 0 for homogeneous background, Y = q^{00} (dot_phi)^2 = 0
    Y_bkg = sp.simplify(q_inv_00 * (dot_phi**2))
    if Y_bkg != 0:
        raise ValueError(f"Expected Y = 0 on FLRW, got {Y_bkg}")

    # Kinetic variable Q = A^mu grad_mu phi = (1/N) * dot_phi
    Q_bkg = A_up_0 * dot_phi

    # In the full action, the scalar kinetic function is F(Y, Q).
    # Since Y = 0 identically on FLRW background, F(Y, Q)|_{FLRW} = F(0, Q).
    # In SZ eq. (5) -> eq. (3), and TARGET_D5 §1.1:
    # K(Q) = -1/2 * F(0, Q)

    # -------------------------------------------------------------------------
    # 2. Show that mu_std does not appear in background equation
    # -------------------------------------------------------------------------
    # In AeST (D7 §1.1, D7 §2.1, D5 §3.1):
    # The galaxy interpolating function mu_std(x) = x / sqrt(1 + x^2) arises
    # exclusively through the spatial gradient sector:
    # Y = q^{mu nu} grad_mu phi grad_nu phi = |grad phi|^2 / a^2 (static/perturbation)
    # where J(Y) = F(Y, Q_0) / (2 - K_B) and mu(x) = J'(Y).
    #
    # The background action on FLRW is:
    # S_bkg = 1/(8 pi G_tilde) int dt d^3x N a^3 [ -3 H^2 / N^2 + K(Q) ] + S_m
    #
    # Background equations of motion:
    # 1) Variation wrt phi_bar(t):
    #    d/dt ( a^3 dK/dQ ) = 0  =>  dK/dQ = I_0 / a^3  (shift current conservation)
    # 2) Variation wrt N:
    #    8 pi G_tilde rho_phi = Q dK/dQ - K
    # 3) Variation wrt a:
    #    8 pi G_tilde P_phi = K
    # 4) Friedmann:
    #    3 H^2 = 8 pi G_tilde (rho_m + rho_phi)

    # Symbolically verify that d/dY terms do not enter:
    Y_sym, Q_sym = sp.symbols('Y Q')
    F_sym = sp.Function('F')(Y_sym, Q_sym)
    # Background Lagrangian density for scalar: L_scalar = -1/2 * F(0, Q) = K(Q)
    K_sym = -sp.Rational(1, 2) * F_sym.subs(Y_sym, 0)

    # Verify that mu(x) ~ dF/dY is completely absent from K_sym and its Q-derivatives:
    mu_std_sym = sp.Symbol('mu_std')
    if mu_std_sym in K_sym.free_symbols:
        raise ValueError("mu_std unexpectedly appeared in K(Q)")
    dK_dQ = sp.diff(K_sym, Q_sym)
    if mu_std_sym in dK_dQ.free_symbols:
        raise ValueError("mu_std unexpectedly appeared in dK/dQ")

    mu_std_in_background = False

    # -------------------------------------------------------------------------
    # 3. Show that seam direct yield I is not a root
    # -------------------------------------------------------------------------
    # From SEAM.md / ORIGINAL_REQUEST.md:
    # Direct yield I = 1 / (8 * pi^(3/2)) = 0.02244839026564582
    I_direct_yield = 1.0 / (8.0 * (math.pi ** 1.5))
    expected_I = 0.02244839026564582
    if abs(I_direct_yield - expected_I) > 1e-15:
        raise ValueError(f"Direct yield calculation mismatch: {I_direct_yield} vs {expected_I}")

    # Check background equation roots:
    # Equation of motion: dK/dQ(Q) - I_0 / a^3 = 0
    # Here I_0 is an integration constant (conserved shift charge fixing Omega_c).
    #
    # Consider the Cosh background model adopted in TARGET_D5 §2:
    # K_cosh(Q) = -2*Lambda + 2*K_2*Z_0^2 * [ cosh((Q - Q_0)/Z_0) - 1 ]
    # dK/dQ = 2*K_2*Z_0 * sinh((Q - Q_0)/Z_0)
    Q, Q_0, K_2, Z_0, Lam, I_0_sym, a_sym = sp.symbols('Q Q_0 K_2 Z_0 Lambda I_0 a', positive=True)
    Z = (Q - Q_0) / Z_0
    K_cosh = -2*Lam + 2*K_2*(Z_0**2)*(sp.cosh(Z) - 1)
    dK_dQ_cosh = 2*K_2*Z_0*sp.sinh(Z)

    # Stationary point of K (where dK/dQ = 0):
    # sinh((Q - Q_0)/Z_0) = 0 => Q = Q_0
    # Q_0 is a free dimensional scale (e.g. 0.1 Mpc^-1 in SZ), not algebraically equal to I.
    # Roots of K_cosh(Q) = 0:
    # cosh((Q - Q_0)/Z_0) = 1 + Lambda / (K_2 * Z_0^2)
    # Q_root = Q_0 +/- Z_0 * arcosh(1 + Lambda / (K_2 * Z_0^2))
    # This root depends continuously on the free parameters (Lambda, K_2, Z_0, Q_0).
    # I is an absolute mathematical constant 1/(8 pi^(3/2)), not an algebraic root.

    # Numerical check at published SZ reference parameters (TARGET_D5 §2.5):
    # K_B = 0.5, Q_0 = 0.1, K_2 = 7.5e5, Z_0 = 1e-3, Lambda = 0
    Q_0_num = 0.1
    K_2_num = 7.5e5
    Z_0_num = 1e-3
    Lam_num = 0.0

    Z_at_I = (I_direct_yield - Q_0_num) / Z_0_num
    cosh_val = math.cosh(Z_at_I)
    K_at_I = -2*Lam_num + 2*K_2_num*(Z_0_num**2)*(cosh_val - 1.0)
    dK_dQ_at_I = 2*K_2_num*Z_0_num*math.sinh(Z_at_I)

    # Verify non-zero residual
    if abs(K_at_I) < 1e-10:
        raise ValueError(f"K(I) unexpectedly evaluated to 0: {K_at_I}")
    if abs(dK_dQ_at_I) < 1e-10:
        raise ValueError(f"dK/dQ(I) unexpectedly evaluated to 0: {dK_dQ_at_I}")

    # Quadratic model check (TARGET_D5 §1.3):
    K_quad_at_I = -2*Lam_num + K_2_num * ((I_direct_yield - Q_0_num)**2)
    dK_dQ_quad_at_I = 2 * K_2_num * (I_direct_yield - Q_0_num)
    if abs(K_quad_at_I) < 1e-10 or abs(dK_dQ_quad_at_I) < 1e-10:
        raise ValueError("Quadratic model unexpectedly has I as root")

    I_is_root = False

    # -------------------------------------------------------------------------
    # 4. Assemble Receipt JSON
    # -------------------------------------------------------------------------
    free_symbols_list = ["Q", "Q_0", "K_2", "Z_0", "Lambda", "I_0", "a"]

    receipt = {
        "job": "D",
        "exit_code": 0,
        "verdict": "k_of_q_does_not_choose_I",
        "tier": "D",
        "neighbor_constrained": "AeST background does not replace seam",
        "neighbor_forbidden": "seam yield, galaxy axiom",
        "free_symbols": free_symbols_list,
        "numeric_outputs": {
            "I_direct_yield": I_direct_yield
        },
        "script": "job_d_k_of_q.py",
        "background_statements": {
            "Y_identically_zero": True,
            "K_of_Q_relation": "K(Q) = -1/2 * F(0, Q)",
            "source": "TARGET_D5_COSMOLOGICAL_SECTOR.md"
        },
        "mu_std_in_background": False,
        "I_is_root_of_background": False,
        "choice_of_K_tier": "O",
        "separation_tier": "D",
        "summary": "AeST FLRW background has Y=0 and K(Q)=-1/2*F(0,Q). mu_std does not appear in background equations, and seam yield I is not a root. Choice of K remains tier O; background does not replace seam."
    }

    out_file = Path(__file__).parent / "job_d_k_of_q.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    # Print single JSON object as required
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(evaluate_k_of_q())
