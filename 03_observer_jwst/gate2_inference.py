#!/usr/bin/env python3
"""
Gate 2 -- inference and design-realism framework for fixed-hypothesis
comparison of a0(z) models.

SCOPE AND EPISTEMIC STATUS
--------------------------
This module implements *inference machinery only*. It contains no dataset,
reaches no network, and produces no empirical result. It is deliberately
independent of Gate 1 (provenance): it can be reviewed and exercised against
synthetic self-tests or a provenance-documented dataset without either
blocking the other.

Nothing in this module promotes any claim. Every quantity it returns is tagged
"conditional" unless the caller supplies a dataset that has passed Gate 1, and
even then the tag is "observational_candidate" -- never "observational".

WHY A BESPOKE STATISTIC IS NEEDED
---------------------------------
The two hypotheses under comparison,

    H_const   : a0(z) = a0(0)
    H_horizon : a0(z) = xi * c * H(z)   with xi frozen from the z=0 anchor

are *fully specified before the comparison*. Both share the same two inputs
(the a0 scale, and the functional choice mu(x)); they differ only in the
redshift dependence. Crucially, ZERO parameters are re-fitted at the test
stage.

Consequences:

  1. Wilks's theorem does not apply. delta_chi2 is not a likelihood-ratio
     statistic here and has no chi2_1 null distribution. In particular
     sqrt(|delta_chi2|) is NOT a significance. (It can coincidentally land
     near the correct value when the data sit close to one hypothesis, but it
     does not generalise.)

  2. Because both models are fixed, delta_chi2 is LINEAR in the data and
     therefore EXACTLY Gaussian for Gaussian errors -- no asymptotics needed.
     With  S = sum_i ((g_h,i - g_c,i)/sigma_i)^2 :

         under H_const   : E[delta_chi2] = -S,  sd = 2*sqrt(S)
         under H_horizon : E[delta_chi2] = +S,  sd = 2*sqrt(S)

     so the significance against a hypothesis is (delta_chi2 - E)/(2 sqrt(S)).

  3. sqrt(S) is the maximum attainable separation between the hypotheses. It
     is a *design* quantity: it should be computed BEFORE collecting data, to
     confirm a planned sample can discriminate at all.

Usage:
  python3 03_observer_jwst/gate2_inference.py --self-test
"""

import sys
import math
import json
import argparse

C_LIGHT = 2.99792458e8
MPC_IN_KM = 3.085677581e19


# --------------------------------------------------------------------------
# Cosmology
# --------------------------------------------------------------------------


def hubble_parameter(z, H0_si, Om, Ol):
    """H(z) in s^-1 for flat LCDM."""
    return H0_si * math.sqrt(Om * (1.0 + z) ** 3 + Ol)


def dual_channel_g_pred(g_bar, a0):
    """g for mu(x) = x/(1+x):  g = g_bar * [1/2 + sqrt(1/4 + a0/g_bar)]."""
    if g_bar <= 0:
        return 0.0
    return g_bar * (0.5 + math.sqrt(0.25 + a0 / g_bar))


# --------------------------------------------------------------------------
# G2.1 -- analytic fixed-hypothesis comparison
# --------------------------------------------------------------------------


def compare_fixed_hypotheses(points, a0_zero, xi, H0_si, Om, Ol):
    """
    Closed-form comparison of two fully specified hypotheses.

    `points`: list of dicts with keys g_bar, g_obs, sigma_g, z.
              Optional: sigma_gbar (G2.3).

    Returns delta_chi2, the separation S, the maximum attainable separation,
    and the conditional z-scores against each hypothesis.

    This function propagates NO systematic uncertainty. It is the statistical
    core only; callers must layer G2.2/G2.3/G2.4 on top.
    """
    chi2_c = chi2_h = S = 0.0

    for p in points:
        g_bar, g_obs, z = p["g_bar"], p["g_obs"], p["z"]
        var = p["sigma_g"] ** 2

        # G2.3 interface: g_bar uncertainty enters through the local slope
        # dg_pred/dg_bar, propagated into the effective variance.
        if p.get("sigma_gbar"):
            eps = g_bar * 1e-6
            for a0_ in (a0_zero,):
                slope = (
                    dual_channel_g_pred(g_bar + eps, a0_)
                    - dual_channel_g_pred(g_bar - eps, a0_)
                ) / (2 * eps)
            var += (slope * p["sigma_gbar"]) ** 2

        sig = math.sqrt(var)

        g_c = dual_channel_g_pred(g_bar, a0_zero)
        g_h = dual_channel_g_pred(
            g_bar, xi * C_LIGHT * hubble_parameter(z, H0_si, Om, Ol)
        )

        chi2_c += ((g_obs - g_c) / sig) ** 2
        chi2_h += ((g_obs - g_h) / sig) ** 2
        S += ((g_h - g_c) / sig) ** 2

    delta = chi2_c - chi2_h

    if S > 0:
        sd = 2.0 * math.sqrt(S)
        z_const = (delta - (-S)) / sd
        z_horizon = (delta - S) / sd
        max_sep = math.sqrt(S)
    else:
        z_const = z_horizon = max_sep = 0.0

    return {
        "chi2_H_const": chi2_c,
        "chi2_H_horizon": chi2_h,
        "delta_chi2": delta,
        "separation_S": S,
        "max_attainable_separation_sigma": max_sep,
        "z_vs_H_const": z_const,
        "z_vs_H_horizon": z_horizon,
        "statistic": "closed-form Gaussian (both hypotheses fully specified; "
        "zero parameters re-fitted; Wilks does not apply)",
    }


# --------------------------------------------------------------------------
# G2.2 -- frozen-a0 uncertainty propagation
# --------------------------------------------------------------------------


def propagate_a0_uncertainty(points, a0_zero, sigma_a0, H0_si, Om, Ol, n_draws=201):
    """
    Propagate the frozen a0(0) uncertainty through BOTH hypotheses coherently.

    This is deliberately not a naive independent error. a0(0) enters H_const
    directly and H_horizon through xi = a0(0)/(c H0), so a shift in a0(0) moves
    both predictions together and PARTIALLY CANCELS. Treating it as independent
    would overstate its effect; ignoring it understates the uncertainty on the
    separation. We therefore vary a0(0) as a single common parameter and
    recompute the whole comparison at each draw.

    Deterministic quadrature over a symmetric grid -- no RNG, so results are
    reproducible.
    """
    if sigma_a0 <= 0:
        raise ValueError("sigma_a0 must be positive; pass the measured value")

    lo, hi, results, weights = -3.0, 3.0, [], []
    for i in range(n_draws):
        t = lo + (hi - lo) * i / (n_draws - 1)
        w = math.exp(-0.5 * t * t)
        a0 = a0_zero + t * sigma_a0
        if a0 <= 0:
            continue
        xi = a0 / (C_LIGHT * H0_si)
        r = compare_fixed_hypotheses(points, a0, xi, H0_si, Om, Ol)
        results.append(r)
        weights.append(w)

    tot = sum(weights)

    def wmean(key):
        return sum(w * r[key] for w, r in zip(weights, results)) / tot

    def wsd(key):
        m = wmean(key)
        return math.sqrt(
            sum(w * (r[key] - m) ** 2 for w, r in zip(weights, results)) / tot
        )

    return {
        "a0_zero": a0_zero,
        "sigma_a0": sigma_a0,
        "relative_sigma_a0": sigma_a0 / a0_zero,
        "delta_chi2_mean": wmean("delta_chi2"),
        "delta_chi2_sd_from_a0": wsd("delta_chi2"),
        "separation_S_mean": wmean("separation_S"),
        "separation_S_sd_from_a0": wsd("separation_S"),
        "z_vs_H_horizon_mean": wmean("z_vs_H_horizon"),
        "z_vs_H_horizon_sd_from_a0": wsd("z_vs_H_horizon"),
        "note": (
            "a0(0) is varied as a SINGLE COMMON parameter entering both "
            "hypotheses; the partial cancellation is therefore retained "
            "rather than assumed away."
        ),
    }


# --------------------------------------------------------------------------
# G2.3 / G2.4 / G2.5 -- declared interfaces
# --------------------------------------------------------------------------


def covariance_interface(points):
    """
    G2.3 -- report what covariance information a dataset carries.

    Diagonal-only chi2 is NOT acceptable once real data are attached: distance
    and inclination errors correlate g_bar and g_obs within a galaxy, and
    g_bar is in practice the noisier axis of the RAR. This function does not
    invent a covariance; it reports what is present so the gap is explicit.
    """
    n = len(points)
    return {
        "n_points": n,
        "has_sigma_gobs": all("sigma_g" in p for p in points),
        "has_sigma_gbar": all(p.get("sigma_gbar") for p in points),
        "has_galaxy_grouping": all("galaxy_id" in p for p in points),
        "has_distance_error": all(p.get("sigma_distance") for p in points),
        "within_galaxy_covariance_modelled": False,
        "status": "INTERFACE ONLY -- no covariance is modelled yet",
        "blocking_for_observational_claim": True,
    }


def selection_interface(selection_rule=None, rejection_log=None):
    """
    G2.4 -- selection effects. A dataset without a stated selection rule
    cannot support an observational conclusion, because the mapping from
    catalogue to sample is unknown and may correlate with redshift.
    """
    return {
        "selection_rule_stated": selection_rule is not None,
        "rejection_log_present": rejection_log is not None,
        "malmquist_type_bias_characterised": False,
        "selection_redshift_correlation_characterised": False,
        "status": "INTERFACE ONLY -- no selection effect is corrected yet",
        "blocking_for_observational_claim": True,
    }


SYSTEMATIC_TERMS = (
    "beam_smearing",
    "inclination",
    "asymmetric_drift_pressure_support",
    "stellar_mass_to_light",
    "imf",
    "gas_fraction",
    "distance_calibration",
)


def systematic_budget(supplied=None):
    """
    G2.5 -- systematic budget. At z ~ 1 every term below is first-order and in
    practice exceeds the ~0.1 dex statistical errors typically quoted. Each
    must be quantified or explicitly bounded.
    """
    supplied = supplied or {}
    return {
        "terms": {t: supplied.get(t, "UNQUANTIFIED") for t in SYSTEMATIC_TERMS},
        "all_quantified": all(t in supplied for t in SYSTEMATIC_TERMS),
        "status": "INTERFACE ONLY -- unquantified terms remain",
        "blocking_for_observational_claim": True,
    }


# --------------------------------------------------------------------------
# G2.6 -- Omega_m sensitivity  (H0 cancels exactly; Omega_m does not)
# --------------------------------------------------------------------------


def omega_m_sensitivity(points, a0_zero, H0_si, Om_central, Om_sigma, n_draws=41):
    """
    H0 cancels EXACTLY in this test:

        xi * c * H(z) = [a0(0)/(c H0)] * c * H0 * E(z) = a0(0) * E(z)

    so the H_horizon prediction is independent of H0. The test is therefore
    NOT circular with the distance ladder -- a genuine strength, and it should
    be stated as such.

    Omega_m does NOT cancel: it enters through E(z). It is currently never
    varied. This function measures that sensitivity.
    """
    out = []
    for i in range(n_draws):
        t = -3.0 + 6.0 * i / (n_draws - 1)
        Om = Om_central + t * Om_sigma
        if not (0.0 < Om < 1.0):
            continue
        xi = a0_zero / (C_LIGHT * H0_si)
        r = compare_fixed_hypotheses(points, a0_zero, xi, H0_si, Om, 1.0 - Om)
        out.append((Om, r["z_vs_H_horizon"], r["separation_S"]))

    zs = [z for _, z, _ in out]
    return {
        "omega_m_central": Om_central,
        "omega_m_sigma": Om_sigma,
        "z_vs_H_horizon_range": [min(zs), max(zs)] if zs else [0.0, 0.0],
        "z_vs_H_horizon_spread": (max(zs) - min(zs)) if zs else 0.0,
        "H0_cancels_exactly": True,
        "H0_cancellation_note": (
            "xi*c*H(z) = a0(0)*E(z); the H_horizon "
            "prediction does not depend on H0, so this "
            "test is not circular with the distance "
            "ladder."
        ),
    }


# --------------------------------------------------------------------------
# G2.8 -- mandatory conditional vs observational tagging
# --------------------------------------------------------------------------


def tag_result(payload, gate1_passed, gate2_complete):
    """
    Every result MUST pass through this function. A result may never be
    labelled observational unless BOTH gates are satisfied -- and even then it
    is only an 'observational_candidate' pending a separate review decision.
    Claim-level promotion is never performed here.
    """
    if gate1_passed and gate2_complete:
        kind = "observational_candidate"
        note = (
            "Both gates satisfied. Promotion beyond D0 remains a separate "
            "reviewed decision and is NOT implied by this tag."
        )
    elif gate1_passed:
        kind = "conditional"
        note = "Gate 1 met; Gate 2 incomplete. Not an observational result."
    elif gate2_complete:
        kind = "conditional"
        note = (
            "Gate 2 met; data provenance NOT established. Not an "
            "observational result and must not be cited."
        )
    else:
        kind = "conditional"
        note = (
            "Neither gate satisfied. Harness behaviour only; not evidence "
            "about the universe."
        )

    return {
        "result_type": kind,
        "gate_1_provenance": "MET" if gate1_passed else "NOT MET",
        "gate_2_inference": "MET" if gate2_complete else "NOT MET",
        "claim_level": "D0_PROPOSED",
        "scope_note": note,
        "payload": payload,
    }


# --------------------------------------------------------------------------
# Self-test -- exercises the machinery on declared synthetic control input
# --------------------------------------------------------------------------


def _self_test():
    """
    Uses a DECLARED SYNTHETIC CONTROL, constructed here and labelled as such.
    It is not observational data, is not derived from any catalogue, and
    exists only to verify the machinery. No empirical claim follows from it.
    """
    H0_si = 67.4 / MPC_IN_KM
    Om, Ol = 0.315, 0.685
    a0 = 1.1162688655613144e-10
    sigma_a0 = 1.605926e-11
    xi = a0 / (C_LIGHT * H0_si)

    # Control points generated EXACTLY on H_const, so the machinery has a
    # known right answer: z_vs_H_const must be ~0 and S must be recovered.
    pts = []
    for i in range(20):
        z = 0.4 + 0.05 * i
        g_bar = 1.2e-11 * (1.0 + 0.35 * i)
        pts.append(
            {
                "galaxy_id": f"control_{i:02d}",
                "z": z,
                "g_bar": g_bar,
                "g_obs": dual_channel_g_pred(g_bar, a0),
                "sigma_g": 0.09 * math.log(10.0) * dual_channel_g_pred(g_bar, a0),
            }
        )

    base = compare_fixed_hypotheses(pts, a0, xi, H0_si, Om, Ol)
    assert abs(base["chi2_H_const"]) < 1e-12, "control must sit on H_const"
    assert abs(base["z_vs_H_const"]) < 1e-6, "z vs H_const must vanish"
    assert (
        abs(base["z_vs_H_horizon"] + base["max_attainable_separation_sigma"]) < 1e-6
    ), "on-H_const control must give z_horizon = -sqrt(S)"

    a0u = propagate_a0_uncertainty(pts, a0, sigma_a0, H0_si, Om, Ol)
    assert a0u["z_vs_H_horizon_sd_from_a0"] > 0, "a0 error must move the result"

    oms = omega_m_sensitivity(pts, a0, H0_si, 0.315, 0.007)
    tagged = tag_result({"comparison": base}, gate1_passed=False, gate2_complete=False)
    assert tagged["result_type"] == "conditional"
    assert tagged["claim_level"] == "D0_PROPOSED"

    print("Gate 2 self-test: PASS  (declared synthetic control; no empirical claim)")
    print(
        json.dumps(
            {
                "control_separation_S": round(base["separation_S"], 3),
                "control_max_attainable_sigma": round(
                    base["max_attainable_separation_sigma"], 3
                ),
                "a0_uncertainty_relative": round(a0u["relative_sigma_a0"], 4),
                "z_vs_H_horizon_sd_from_a0": round(a0u["z_vs_H_horizon_sd_from_a0"], 3),
                "omega_m_induced_z_spread": round(oms["z_vs_H_horizon_spread"], 3),
                "H0_cancels_exactly": oms["H0_cancels_exactly"],
                "result_type": tagged["result_type"],
                "claim_level": tagged["claim_level"],
            },
            indent=2,
        )
    )
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Gate 2 inference framework (no dataset, no network, "
        "no empirical result)"
    )
    ap.add_argument(
        "--self-test",
        action="store_true",
        help="exercise the machinery on a declared synthetic control",
    )
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    ap.print_help()
    print(
        "\nThis module produces no result on its own. It is inference "
        "machinery for a Gate-1-compliant dataset."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
