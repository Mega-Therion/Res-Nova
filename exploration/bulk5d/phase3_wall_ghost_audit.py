#!/usr/bin/env python3
"""Quadratic sign audit for the P3-A AeST dust condensate and the dark-bubble wall.

Does not close spatial gradient stability. Does not edit CURRENT_STATE.
Signature (-+++). Action density is L, with a healthy canonical scalar reading
+1/2 (time derivative)^2. Einstein equation convention is the one already
checked in p0_asymmetric_wall.py C3: 4G = -8 pi G4 tau + Weyl terms.
"""

from __future__ import annotations

import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def audit() -> dict:
    K2, KB, Q0, eps = sp.symbols("K2 K_B Q0 epsilon", real=True)
    dQ = sp.Symbol("dQ", real=True)
    a = sp.Symbol("a", positive=True)
    gx, gy, gz = sp.symbols("dPhi_x dPhi_y dPhi_z", real=True)
    grad2 = gx**2 + gy**2 + gz**2

    # L_cond time piece, A_mu pinned, Q = Q0 + dQ. Vacuum tension dropped.
    L_time = sp.Rational(1, 2) * K2 * dQ**2
    coeff_time = sp.diff(L_time, dQ, 2)
    assert sp.simplify(coeff_time - K2) == 0

    # No spatial derivative of the condensate scalar appears in L_cond as written
    # in phase3_drag_action_and_dk.py (Q = h^{00} A_0 partial_0 phi only).
    spatial_gradient_coeff = 0

    # J2b: F_{mu nu} F^{mu nu} = -2 eps^2 |grad Phi|^2 / a^2
    # Action term - (K_B / 2) F^2.
    F2 = -2 * eps**2 * grad2 / a**2
    L_vec = sp.simplify(-sp.Rational(1, 2) * KB * F2)
    # L_vec = K_B * eps^2 |grad Phi|^2 / a^2
    assert sp.simplify(L_vec - KB * eps**2 * grad2 / a**2) == 0

    # Junction sign, copied from the C3 identity (units G5 = 1).
    kp, km = sp.symbols("k_p k_m", positive=True)
    G4 = sp.simplify(2 * kp * km / (km - kp))
    # tau = -(sigma - sigma_ext) h, h_00 = -1, so tau_00 = -(sigma - sigma_ext)(-1)
    # is not re-derived here. The H^2 identity already checked in p0 is recorded.
    H2_factor = sp.simplify(
        sp.Rational(8, 3) * sp.pi * G4
    )  # multiplies (sigma_ext - sigma)

    out = {
        "scalar_time_kinetic_second_derivative": str(coeff_time),
        "scalar_no_ghost_iff": "K2 > 0",
        "scalar_spatial_gradient_coefficient_in_L_cond": spatial_gradient_coeff,
        "scalar_gradient_stability": "[O] L_cond has no (spatial gradient of phi)^2 term. This audit does not decide gradient stability.",
        "vector_electric_lagrangian": "L = K_B * epsilon^2 |grad Phi|^2 / a^2",
        "vector_no_ghost_on_J2b_electric_mode_iff": "K_B > 0",
        "F2_used": "-2*epsilon^2*|grad Phi|^2/a^2 (JACOBIAN_SPLIT J2b)",
        "G4_over_G5": str(G4),
        "G4_positive_when": "k_m > k_p",
        "junction": "4G = -8 pi G4 tau + Weyl. The minus is the Israel convention already verified in p0 C3, not a negative Newton constant.",
        "H2_identity": "H^2 = (8 pi G4 / 3) (sigma_ext - sigma) when tension is the only source. Positive for sub-extremal tension.",
        "H2_prefactor_symbol": str(H2_factor)
        + "*(sigma_ext - sigma), with G4 = 2*k_p*k_m/(k_m - k_p)",
        "where_rho_d_sits": "[O] Whether rho_d from L_cond adds to wall tension (lowers H^2) or to brane matter (ordinary attraction) is not fixed by the quadratic kinetic signs.",
        "verdict": "Time-kinetic ghost-free iff K2 > 0. Electric vector energy positive iff K_B > 0. Gradient stability and the gravitational seat of rho_d stay open.",
    }
    path = os.path.join(HERE, "PHASE3_WALL_GHOST_AUDIT.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    return out


if __name__ == "__main__":
    print(json.dumps(audit(), indent=1))
