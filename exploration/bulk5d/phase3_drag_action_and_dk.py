#!/usr/bin/env python3
"""Phase 3 symbolic audit for the flux-fed dark-bubble wall (PREREG_PHASE3.md):
  P3-A  5D covariant drag action scan (tangential Killing invariant Y, normalized
        Killing velocity U^A, and bulk-Killing AeST dust condensate).
  P3-B  Delta k = k_- - k_+ cancellation vs amplification and bulk backreaction squeeze.
  P3-C  Kramers-Kronig causal dispersion identity and bulk-gap viscosity threshold.
"""
from __future__ import annotations

import json
import math
import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def check_p3a_covariant_drag_action() -> dict:
    tau = sp.Symbol("tau", real=True)
    k, mu, rho_b, sig0 = sp.symbols("k mu rho_b sigma0", positive=True)
    a = sp.Function("a", positive=True)(tau)
    ad = sp.diff(a, tau)
    f = k**2 * a**2 - mu / a**2

    # 1. Killing decomposition Y - X = f(a)
    Td = sp.sqrt(f + ad**2) / f
    # xi^A = (1, 0, 0, 0, 0), xi_A = (-f, 0, 0, 0, 0), e_tau^A = (Td, ad, 0, 0, 0), n_A = (-ad, Td, 0, 0, 0)
    xi_tau = -f * Td  # tangential pullback xi_0 = e_tau^A xi_A
    X = (-ad) ** 2  # (xi.n)^2
    # h = diag(h00, h11, h22, h33)
    h00, h11, h22, h33 = sp.symbols("h00 h11 h22 h33", real=True)
    hinv = sp.diag(1 / h00, 1 / h11, 1 / h22, 1 / h33)
    Y_gen = -hinv[0, 0] * xi_tau**2
    Y_frw = Y_gen.subs({h00: -1, h11: a**2, h22: a**2, h33: a**2})
    assert sp.simplify(Y_frw - (f + ad**2)) == 0
    assert sp.simplify((Y_frw - X) - f) == 0

    # 2. Exact metric stress variation S_{mu nu} = -(2/sqrt(-h)) d(sqrt(-h) L)/d(h^{mu nu})
    # Note h^{00} = 1/h00, sqrt(-h) = sqrt(-h00 * h11 * h22 * h33)
    hup00, hup11, hup22, hup33 = sp.symbols("hup00 hup11 hup22 hup33", real=True)
    sqrt_mh = 1 / sp.sqrt(-hup00 * hup11 * hup22 * hup33)
    Y_up = -hup00 * xi_tau**2
    L_naive = -sig0 + sp.Rational(1, 2) * rho_b * (Y_up - f)
    action_density = sqrt_mh * L_naive
    frw_up = {hup00: -1, hup11: 1 / a**2, hup22: 1 / a**2, hup33: 1 / a**2}
    S_00 = sp.simplify((-2 / sqrt_mh * sp.diff(action_density, hup00)).subs(frw_up))
    S_11 = sp.simplify((-2 / sqrt_mh * sp.diff(action_density, hup11)).subs(frw_up))
    # Mixed: rho_d = -S^0_0 = +S_00 (since h_00 = -1), p_d = S^1_1 = S_11 / a^2
    rho_naive = sp.simplify(S_00)
    p_naive = sp.simplify(S_11 / a**2)
    assert sp.simplify(rho_naive - (sig0 + rho_b * f + sp.Rational(1, 2) * rho_b * ad**2)) == 0
    assert sp.simplify(p_naive - (-sig0 + sp.Rational(1, 2) * rho_b * ad**2)) == 0

    # 3. Unit-normalized bulk Killing velocity U^A = xi^A / sqrt(f): Z = -h^{00} U_0^2 = 1 + adot^2 / f
    U_tau = -sp.sqrt(f) * Td
    Z_frw = sp.simplify(U_tau**2)
    assert sp.simplify(Z_frw - (1 + ad**2 / f)) == 0

    # 4. AeST-like wall dust condensate L_cond = -sig0 + (1/2) K2 (Q - Q0)^2 coupled to unit vector A_mu
    # with constraint -(1/2) lam (h^{ab} A_a A_b + 1), where Q = h^{ab} A_a d_b phi
    K2_ae, Q0, lam_ae = sp.symbols("K2 Q0 lam_ae", real=True)
    A0, dphi0 = sp.symbols("A0 dphi0", real=True)
    Q_gen = hup00 * A0 * dphi0
    L_cond = -sig0 + sp.Rational(1, 2) * K2_ae * (Q_gen - Q0) ** 2 - sp.Rational(1, 2) * lam_ae * (hup00 * A0**2 + 1)
    # Variation wrt A0 gives lam_ae: dL/dA0 = 0
    dL_dA0 = sp.diff(L_cond, A0)
    lam_sol = sp.solve(dL_dA0, lam_ae)[0]
    # On FRW (hup00 = -1, A0 = -1 => Q = dphi0), stress tensor is:
    S_cond_00 = sp.simplify((-2 / sqrt_mh * sp.diff(sqrt_mh * L_cond, hup00)).subs(lam_ae, lam_sol).subs({hup00: -1, hup11: 1 / a**2, hup22: 1 / a**2, hup33: 1 / a**2, A0: -1}))
    S_cond_11 = sp.simplify((-2 / sqrt_mh * sp.diff(sqrt_mh * L_cond, hup11)).subs(lam_ae, lam_sol).subs({hup00: -1, hup11: 1 / a**2, hup22: 1 / a**2, hup33: 1 / a**2, A0: -1}))
    rho_cond = sp.simplify(S_cond_00)
    p_cond = sp.simplify(S_cond_11 / a**2)
    Q_val = dphi0
    assert sp.simplify(rho_cond - (sig0 + sp.Rational(1, 2) * K2_ae * (Q_val - Q0) ** 2 + K2_ae * Q0 * (Q_val - Q0))) == 0
    assert sp.simplify(p_cond - (-sig0 + sp.Rational(1, 2) * K2_ae * (Q_val - Q0) ** 2)) == 0
    # Subtract vacuum tension sig0: dQ = Q - Q0 -> rho_dust = K2 Q0 dQ + (1/2) K2 dQ^2, p_dust = (1/2) K2 dQ^2 => w_d -> 0!
    dQ = sp.Symbol("dQ", real=True)
    w_d_series = sp.series((p_cond + sig0).subs(dphi0, Q0 + dQ) / (rho_cond - sig0).subs(dphi0, Q0 + dQ), dQ, 0, 2).removeO()
    assert sp.simplify(w_d_series - dQ / (2 * Q0)) == 0

    return {
        "killing_norm_identity": "Y - X = f(a), with X = adot^2 and Y = f(a) + adot^2",
        "naive_L_of_Y_rho_d": str(rho_naive),
        "naive_L_of_Y_obstruction": "Tangential Y = f(a) + adot^2 injects rho_b * k^2 * a^2 ~ (k/H)^2 ~ 1e62 times larger than drag",
        "unit_killing_Z": "Z = 1 + adot^2 / f(a) = 1 + O(H^2/k^2): no a^2 growth without a UV-growing bulk field",
        "aest_condensate_dust_limit": "rho_d = K2*Q0*dQ + (1/2)*K2*dQ^2, p_d = (1/2)*K2*dQ^2 => w_d = dQ/(2*Q0) -> 0 as dQ/Q0 -> 0",
        "law_c_link_and_risk": "Pinning A_mu to u_xi_mu gives F_d = 0 (Law C) on delta T|wall = 0 slices, but inherits -8*pi*G4 anti-gravitating wall sign requiring an explicit scalar-ghost check [O].",
    }


def check_p3b_delta_k_window() -> dict:
    kp, km,dk, rho_p, rho_m, pi_p, pi_m, c_p, alpha = sp.symbols(
        "k_p k_m Delta_k rho_p rho_m pi_p pi_m c_p alpha", positive=True
    )
    pi_eff = (km * pi_p - kp * pi_m) / (km - kp)
    rho_eff = (km * rho_p - kp * rho_m) / (km - kp)
    ratio = sp.simplify(pi_eff / rho_eff)

    # 1. Single-sided linear flux (rho_m = 0, pi_m = 0): Delta k cancels identically
    ratio_single = sp.simplify(ratio.subs({rho_m: 0, pi_m: 0}))
    assert sp.simplify(ratio_single - pi_p / rho_p) == 0

    # 2. Two-sided background cancellation: rho_m / km = alpha * (rho_p / kp), pi_m = 0, pi_p = c_p * rho_p
    ratio_cancel = sp.simplify(ratio.subs({pi_m: 0, pi_p: c_p * rho_p, rho_m: alpha * km / kp * rho_p}))
    assert sp.simplify(ratio_cancel - c_p / (1 - alpha)) == 0

    # 3. Metric-induced differential perturbation: pi_p = d_pi_p, pi_m = d_pi_m with fixed denominator Omega_W
    # Rewriting pi_eff = pi_p + (kp / (km - kp)) * (pi_p - pi_m)
    assert sp.simplify(pi_eff - (pi_p + kp / (km - kp) * (pi_p - pi_m))) == 0

    # 4. Bulk energy density scaling for Q_4 = (d(Delta Sigma)/dtau + 3 H Delta Sigma)
    # Wait: in FLUX_CODAZZI (w_d = 0), Delta Sigma = x0 * a^2 * (3 H^2 / (8 pi G4))
    # Let's compute Q4 = d(Delta Sigma)/dtau + 3 H Delta Sigma using dH/dtau = H^2 * Ep_H (where Ep_H = E'/E)
    # Delta Sigma = x0 * a^2 * 3 H^2 / (8 pi G4); d/dtau (a^2 H^2) = 2 a^2 H^3 (1 + Ep_H)
    # => Q4 = (5 + 2 Ep_H) * x0 * a^2 * 3 H^3 / (8 pi G4)
    # Using G4 = 2 kp km G5 / (km - kp) => 1/(8 pi G4) = (km - kp)/(2 kp km * kappa5)
    # And |rho_Lambda5| = 6 k^2 / kappa5 (with k ~ kp ~ km or k_eff = kp*km/k)
    H, x0, Ep_H, kap5, k_sym = sp.symbols("H x0 Ep_H kappa5 k", real=True)
    a_sym = sp.Symbol("a", positive=True)
    G4 = 2 * kp * km * (kap5 / (8 * sp.pi)) / (km - kp)
    DelSig = x0 * a_sym**2 * 3 * H**2 / (8 * sp.pi * G4)
    # d/dtau(a^2 H^2) = 2 a H (a H) + a^2 (2 H dH/dtau) with dH/dtau = H^2 * Ep_H
    dDelSig_dtau = x0 * 3 / (8 * sp.pi * G4) * (2 * a_sym**2 * H**3 * (1 + Ep_H))
    Q4_expr = sp.simplify(dDelSig_dtau + 3 * H * DelSig)
    rho_L5_abs = 6 * k_sym**2 / kap5
    q_over_L5 = sp.simplify(Q4_expr / rho_L5_abs)
    # At kp = k, km = k + dk -> (km - kp)/(kp km) = dk / (k*(k+dk)) ~ dk/k^2; let k_eff = kp*km/k
    # Exact check: q_over_L5 == (5 + 2*Ep_H)/4 * x0 * a^2 * (km - kp)*k/(kp*km) * (H/k)^3
    target_q = (5 + 2 * Ep_H) / 4 * x0 * a_sym**2 * ((km - kp) * k_sym / (kp * km)) * (H / k_sym) ** 3
    assert sp.simplify(q_over_L5 - target_q) == 0

    # Numerical benchmark (a = 1 today, Pantheon+ x0 = 2.2445, Ep_H = E'/E today ~ -0.45, L = 5e-5 m)
    c_light = 299792458.0
    Mpc = 3.0856775814913673e22
    H0 = 67.4e3 / Mpc
    L_ads = 5e-5
    H_over_k = H0 * L_ads / c_light
    # At E(z=0)=1, Omega_m=0.3087, x0=2.2445, OmW(0)~1.75 => Ep(0) = -1.5*Om - 2*OmW + 1.5*x0
    Om0 = 0.308655
    x0_val = 2.244452
    OmW0 = 1.75
    Ep0 = -1.5 * Om0 - 2.0 * OmW0 + 1.5 * x0_val
    pref_null = ((5.0 + 2.0 * Ep0) / 4.0) * x0_val * (H_over_k**3)
    # Inelastic kinetic dissipation: Q4 = (1/2) rho_med (H/k)^3 => rho_med/|rho_L5| = ((5 + 2*Ep0)/2) * x0 * (dk/k)
    pref_med = ((5.0 + 2.0 * Ep0) / 2.0) * x0_val

    return {
        "single_sided_pi_over_rho": str(ratio_single),
        "single_sided_delta_k_cancels": True,
        "two_sided_cancellation_amplification": str(ratio_cancel),
        "Q4_over_abs_rho_Lambda5_exact": "(5 + 2*E'/E)/4 * x0 * a^2 * ((k_- - k_+)*k/(k_+*k_-)) * (H/k)^3",
        "H0_over_k_micron": H_over_k,
        "Ep_today_approx": Ep0,
        "null_dust_ratio_at_dk_over_k_1": pref_null,
        "static_medium_v3_ratio_prefactor_times_dk_over_k": pref_med,
        "backreaction_bound_dk_over_k_for_10pct": 0.1 / pref_med,
    }


def check_p3c_kramers_kronig() -> dict:
    # Causal single-pole response G(w) = chi(w) - chi(inf) = G_inf / (1 - i w tau_R)
    # Analytic in upper half-plane (pole at w = -i / tau_R in lower half-plane).
    w, wp, tau_R, G_inf = sp.symbols("w wp tau_R G_inf", real=True, positive=True)
    # Allow w to be any real nonzero frequency (evaluate PV integral via explicit contour / indefinite + delta limit)
    w_real = sp.Symbol("w_real", real=True, positive=True)
    G_w = G_inf / (1 - sp.I * w_real * tau_R)
    Re_G = sp.simplify(sp.re(G_w))
    Im_G = sp.simplify(sp.im(G_w))
    assert sp.simplify(Re_G - G_inf / (1 + w_real**2 * tau_R**2)) == 0
    assert sp.simplify(Im_G - G_inf * w_real * tau_R / (1 + w_real**2 * tau_R**2)) == 0

    # Verify exact Kramers-Kronig identity:
    # Re G(w) = (2/pi) P.V. int_0^oo wp * Im G(wp) / (wp^2 - w^2) dwp
    # Partial fraction decomposition in wp:
    integrand_full = (2 / sp.pi) * (G_inf * tau_R * wp**2 / ((1 + tau_R**2 * wp**2) * (wp**2 - w_real**2)))
    term_pv = (2 / sp.pi) * (G_inf * tau_R * w_real**2 / (1 + tau_R**2 * w_real**2)) / (wp**2 - w_real**2)
    term_reg = (2 / sp.pi) * (G_inf * tau_R / (1 + tau_R**2 * w_real**2)) / (1 + tau_R**2 * wp**2)
    assert sp.simplify(integrand_full - (term_pv + term_reg)) == 0

    # 1. Exact symmetric Cauchy PV integral of 1 / (wp^2 - w_real^2) over [0, oo) vanishes:
    del_s, M_s = sp.symbols("del_s M_s", positive=True)
    # Antiderivative of 1/(wp^2 - w^2) is (1/(2w)) * ln(|wp - w| / (wp + w))
    pv_finite = (
        sp.log(del_s / (2 * w_real - del_s)) - sp.log(sp.Integer(1))
        + sp.log((M_s - w_real) / (M_s + w_real)) - sp.log(del_s / (2 * w_real + del_s))
    ) / (2 * w_real)
    # Check antiderivative derivative away from w_real
    assert sp.simplify(sp.diff(sp.log((w_real - wp) / (w_real + wp)) / (2 * w_real), wp) - 1 / (wp**2 - w_real**2)) == 0
    pv_del0 = sp.simplify(sp.limit(pv_finite, del_s, 0, "+"))
    pv_val = sp.simplify(sp.limit(pv_del0, M_s, sp.oo))
    assert pv_val == 0

    # 2. Regular part integrates directly over [0, oo) to Re G(w)
    reg_val = sp.simplify(sp.integrate(term_reg, (wp, 0, sp.oo)))
    diff_kk = sp.simplify(reg_val - Re_G)
    assert diff_kk == 0

    # Benchmark: H0 * tau_R for UV-gapped bulk (tau_R ~ 1/k, L = 5e-5 m) vs gapless bulk (tau_R ~ 1/H0)
    c_light = 299792458.0
    Mpc = 3.0856775814913673e22
    H0 = 67.4e3 / Mpc
    L_ads = 5e-5
    H0_over_k = H0 * L_ads / c_light
    return {
        "causal_pole": "w = -i / tau_R (strictly in lower half-plane)",
        "kramers_kronig_pv_integral_matches_ReG": True,
        "low_freq_cvis2_scaling": "c_vis^2 ~ (G_inf / rho_W) * (H0 * tau_R)",
        "uv_gapped_tauR_1_over_k": H0_over_k,
        "gapless_tauR_1_over_H0": 1.0,
        "pantheon_lawA_ceiling": "1.5e-4 to 5.5e-4 (phase2_threshold_frame.py)",
        "implication": "Under Law A, Pantheon+ forbids gapless O(1)-shear bulk states (tau_R ~ 1/H0 unless G_inf/rho_W <= 1e-4), while a UV-gapped state (tau_R ~ 1/k) naturally yields H0*tau_R ~ 3.6e-31 << 1e-4.",
    }


def main() -> int:
    res = {
        "P3A_covariant_drag_action": check_p3a_covariant_drag_action(),
        "P3B_delta_k_window": check_p3b_delta_k_window(),
        "P3C_kramers_kronig": check_p3c_kramers_kronig(),
    }
    out_path = os.path.join(HERE, "PHASE3_DRAG_ACTION_AND_DK.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
