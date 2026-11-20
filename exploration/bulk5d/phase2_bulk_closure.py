#!/usr/bin/env python3
"""Phase 2 (PREREG_PHASE2.md): low-energy bulk closure for the flux-fed dark-bubble wall.

J1  pi_eff from the bulk state: thermal (horizon) / horizonless gapped / radion / free-streaming, tied to the flux channel.
J2  u_F drops out of the envelope's Law A equations at c_vis^2 = 0 (structural SymPy check on equations transcribed
    from weyl_causal_envelope.py).
J3  drag partner of the covariant sigma(X): a medium at rest in the static frame; sign of its energy exchange.
K1  consistency identity: uniform delta-mu and a uniform boost leave the projected Weyl tensor a perfect radiation fluid.
Verdict: reads PHASE2_CVIS_THRESHOLD.json (every integer ell in [2, 30]) and VERIFY_WEYL_KNIFE.json.
"""
from __future__ import annotations

import json
import math
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def j2_uF_drops_out() -> dict:
    s = sp.symbols
    dm, um, Dr, Fr, Psi, Qp, FW, SW = s("dm um Dr Fr Psi Qp FW SW", real=True)
    a, E2, Ep, OmW, q4, q4W, x0, K2, Or, Om, shear, cvis2, uF = s("a E2 Ep OmW q4 q4W x0 K2 Or Om shear cvis2 uF", real=True)
    # transcribed from weyl_causal_envelope.py, Law A (A_freefall), hu98 closure
    Phi = Psi - shear * a**2 * SW
    Psi_p = Qp - Phi
    DW = -sp.Rational(2, 3) * E2 * (K2 * Psi + 3 * (1 + x0 * a**2) * Qp) - Om / a**3 * dm - Dr
    Qp_p = sp.Rational(1, 2) / E2 * (Dr + DW) - sp.Rational(3, 2) / E2 * SW - (3 + Ep) * Psi_p - (3 + 2 * Ep) * Phi
    FW_p = -(5 + Ep) * FW + K2 * (DW / 3 + sp.Rational(4, 3) * OmW * Phi - SW) + q4 * uF
    dm_p = -um + 3 * Psi_p
    um_p = -(2 + Ep) * um + K2 * Phi
    Dr_p = -4 * Dr + 4 * Or / a**4 * Psi_p - Fr
    Fr_p = -(5 + Ep) * Fr + K2 * (Dr / 3 + sp.Rational(4, 3) * Or / a**4 * Phi)
    SW_p = (-7 + q4W) * SW + 2 * cvis2 * FW
    # at c_vis^2 = 0, SW' is proportional to SW and SW(N_i) = 0 in the code, so SW = 0 identically
    assert sp.simplify(SW_p.subs(cvis2, 0) - (-7 + q4W) * SW) == 0
    metric_rhs = [e.subs(SW, 0) for e in (dm_p, um_p, Dr_p, Fr_p, Psi_p, Qp_p)]
    observables = [(Phi + Psi).subs(SW, 0) / 2]
    free = set().union(*[e.free_symbols for e in metric_rhs + observables])
    assert FW not in free and uF not in free
    # and at c_vis^2 > 0 the flux frame does enter (through FW -> SW -> Phi)
    assert uF in FW_p.free_symbols and FW in SW_p.free_symbols
    return {"J2": "At c_vis^2 = 0: SW stays 0, D_W comes from the 00 constraint, and F_W (hence u_F) never enters the metric "
                  "subsystem or Phi_W: the observables are exactly independent of the flux frame, within the envelope's equations. "
                  "At c_vis^2 > 0, u_F enters through F_W -> S_W -> Phi."}


def k1_isotropy_identity() -> dict:
    m, v = sp.symbols("m v", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    Emix_rest = sp.diag(3 * m, -m, -m, -m)            # P0/C1: E^tau_tau = 3 mu/a^4, E^x_x = -mu/a^4
    E_low = eta * Emix_rest                           # E_{mu nu}
    gam = 1 / sp.sqrt(1 - v**2)
    L = sp.eye(4)
    L[0, 0] = L[1, 1] = gam
    L[0, 1] = L[1, 0] = -gam * v
    Eb = (L.T * E_low * L).applyfunc(lambda e: sp.series(e, v, 0, 2).removeO())
    spatial = Eb[1:, 1:]
    trace = sum(spatial[i, i] for i in range(3))
    aniso = (spatial - trace / 3 * sp.eye(3)).applyfunc(sp.simplify)
    assert aniso == sp.zeros(3, 3)
    assert sp.simplify(Eb[0, 1]) != 0  # momentum appears at O(v)
    return {"K1": "Consistency identity (not a test): the projected Weyl tensor of the planar black brane is isotropic in its rest frame "
                  "(P0/C1), so a uniform delta-mu or a uniform boost gives momentum at O(v) and no anisotropic stress at O(v). "
                  "Anisotropic stress needs gradients."}


def j1_bulk_states() -> dict:
    # thermal case, exact blackening at the wall: f(a) = k^2 a^2 (1 - (r_h/a)^4), T_bh = k^2 r_h / pi
    k, a, rh, Hh, HW, cw = sp.symbols("k a r_h H H_W c_w", positive=True)
    T_bh = k**2 * rh / sp.pi
    f_a = k**2 * a**2 * (1 - (rh / a) ** 4)
    T_loc = T_bh / sp.sqrt(f_a)
    # dark radiation weight: H_W^2 = c_w mu / a^4 with mu = k^2 r_h^4  ->  (r_h/a)^4 = H_W^2 / (c_w k^2)
    x = sp.Symbol("x", positive=True)  # x = (r_h/a)^4
    T_loc_x = (k / sp.pi) * x ** sp.Rational(1, 4) / sp.sqrt(1 - x)
    assert sp.simplify(T_loc.subs(rh, a * x ** sp.Rational(1, 4)) - T_loc_x) == 0
    # effective Hu viscosity of a Navier-Stokes fluid with eta/(rho + p) = 1/(4 pi T_loc): c_vis^2_eff ~ H/(2 pi T_loc) (order of magnitude)
    eps = sp.Symbol("eps", positive=True)  # H/k
    cv_eff = sp.simplify((Hh / (2 * sp.pi * T_loc_x)).subs(x, (HW / k) ** 2 / cw))
    cv_lead = sp.simplify(cv_eff.subs({Hh: eps * k, HW: eps * k}))
    # example: micron-scale AdS length L = 1/k = 5e-5 m (2311.14589), H0 for h = 0.674
    c = 299792458.0
    Mpc = 3.0856775814913673e22
    H0 = 67.4e3 / Mpc
    L = 5e-5
    H_over_k = H0 * L / c
    cv_micron = float(cv_lead.subs(eps, H_over_k).subs(cw, 1))
    return {
        "J1_flux_channel": ("FLUX_CODAZZI fits only the combination mu_+/k_+ - mu_-/k_-; the channel is unspecified. "
                            "Positive Omega_W growing in time needs ingoing dust from outside (mu_+ increasing) or outgoing dust "
                            "from inside (mu_- decreasing)."),
        "J1_i_thermal": ("A horizon (thermal state) makes the Weyl fluid hydrodynamic: cutoff fluid/gravity (Bredberg-Keeler-Lysov-Strominger "
                         "arXiv:1101.2451; Cai-Li-Zhang arXiv:1104.3281) with eta/s = 1/4pi. Exact local temperature at the wall: "
                         f"T_loc = (k/pi) x^(1/4)/sqrt(1 - x), x = (r_h/a)^4 = H_W^2/(c_w k^2). Effective Hu viscosity (order of magnitude) "
                         f"c_vis^2_eff ~ H/(2 pi T_loc) = {cv_lead} with eps = H/k at H_W = H. Micron example (L = 5e-5 m): "
                         f"H0/k = {H_over_k:.3e}, c_vis^2_eff ~ {cv_micron:.1e}."),
        "J1_i_conflict": ("But a horizon side cannot be the flux channel: an interior black hole contributes -mu_-/k_- (negative dark radiation) "
                          "and cannot emit outgoing dust classically; the exterior has no horizon (it would sit behind the wall). So the "
                          "thermal estimate covers only a static, non-feeding side."),
        "J1_ii_horizonless": ("The feeding side is horizonless: exterior AdS-Vaidya fed from the boundary region (mu_+ is itself a growing "
                              "normalizable mode, so it is not the normalizable-modes-vanish state of 2001.07433), or a horizonless interior "
                              "with an outgoing source. Planar radial null dust sits at fixed x, so each column deposits locally isotropic "
                              "dark radiation: pi = 0 at zeroth order in gradients. The first-order pi is set by the source's state, which the "
                              "flux-fed model does not specify."),
        "J1_iii_radion": "Koyama 2003's low-energy pi_E comes from the radion of a second brane. The dark bubble has one wall: no radion term.",
        "J1_iv_free_streaming": ("Free-streaming (c_vis^2 = 1/3) along the wall needs weakly coupled, non-hydrodynamic bulk content; classical "
                                 "5D Einstein gravity with radial null dust does not supply it at wavelengths >> 1/k. Metric perturbations "
                                 "tilt the dust at first order; the deposited momentum goes into u_F (J2: irrelevant at pi = 0)."),
        "J1_amplification": ("Corrected 2026-11-19 (dk_ratio_identity.py): the closure is pi_eff/rho_eff, which equals the feeding side's "
                             "closure for single-sided feeding; amplification needs two-sided, nearly cancelling dark radiation with different closures."),
        "J1_result": ("pi_eff is not fixed by the wall or by classical bulk gravity alone: it is set by the state of the flux source. "
                      "Zeroth order in gradients: pi_eff = 0. First order: source-dependent [O]."),
        "micron_H0_over_k": H_over_k,
        "thermal_cvis2_eff_micron": cv_micron,
    }


def j3_drag_partner() -> dict:
    rho_b, v, adot, addot = sp.symbols("rho_b v adot addot", real=True)
    gam2 = 1 / (1 - v**2)
    Q_abs = gam2 * rho_b * v                 # absorbed dust energy flux T^{0n} in the wall frame
    Q_refl = -2 * gam2 * rho_b * v**3        # elastic reflection: work done against ram pressure 2 gamma^2 rho_b v^2
    Q_req = rho_b * adot * addot             # sigma(X) needs d/dtau(rho_b adot^2 / 2)
    vpos = {v: sp.Rational(1, 3)}
    assert Q_abs.subs(vpos).subs(rho_b, 1) > 0 and Q_refl.subs(vpos).subs(rho_b, 1) < 0
    return {"J3": ("The covariant sigma(X), X = (xi.n)^2, singles out the bulk static frame: its partner is a medium at rest in that frame. "
                   "For an expanding wall (v = adot > 0) absorption gives Q > 0 and elastic reflection gives Q < 0 at every epoch, "
                   "while sigma(X) needs Q4 = rho_b adot addot, which changes sign at the onset of acceleration (z ~ 0.73). "
                   "No single interaction supplies it; switching channel exactly at z_acc would be post-hoc. So candidate (a) stays "
                   "excluded on physical grounds, not only by PREREG_FLUX's single-channel rule. The w_d = 0 flux-fed branch's partner "
                   "is the Vaidya null dust by construction (PREREG_FLUX); its drag still has no 5D action [O].")}


def verdict() -> dict:
    thr = json.load(open(os.path.join(HERE, "PHASE2_CVIS_THRESHOLD.json")))
    knife = json.load(open(os.path.join(HERE, "..", "drag_gcosmo", "VERIFY_WEYL_KNIFE.json")))
    g = thr["grid"]
    rows = {}
    for bg in ("Pantheon+_best", "DES-Dovekie_best", "Pantheon+_2sigma_floor"):
        o = g[f"A|{bg}|0"]
        rows[bg] = {"A_phiphi_mean": o.get("A_phiphi_mean"), "ISW_max_all_ell": o.get("ISW_max"), "pass_at_cvis2_0": o["pass"],
                    "cvis2_threshold": thr["threshold"][bg]}
    k50 = {key.split("|")[1]: v["isw_max"] for key, v in knife["k50"].items() if key.startswith("A_freefall") and "cvis2=0.000" in key}
    return {"at_pi_eff_0": rows, "knife_50_kmodes_ISW_max": k50,
            "rule": "PREREG_PHASE2: J1 could not pick a single state -> verdict conditional on the bulk state [O]"}


def main() -> int:
    res = {}
    res.update(j2_uF_drops_out())
    res.update(k1_isotropy_identity())
    res.update(j1_bulk_states())
    res.update(j3_drag_partner())
    res["K2_published_consistency"] = ("Cardoso-Hiramatsu-Koyama-Seahra (arXiv:0705.1685): modes with wavelength >> the AdS length are not "
                                       "amplified, i.e. 4D behaviour is recovered at low energy, consistent with the gradient expansion. "
                                       "A literature consistency check, not a reproduction.")
    res["verdict_inputs"] = verdict()
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(HERE, "PHASE2_BULK_CLOSURE.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
