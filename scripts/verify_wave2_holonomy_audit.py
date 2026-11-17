#!/usr/bin/env python3
"""
Wave 2 Holonomy Audit (BLK-1405 / prediction-falsification-audit-2026-11-16.md §8 Closure 5).

Audits the phenomenological ansatz:
    a_0 = (c * H_0 / (2 * pi)) * f,   with target f = 1.1143 (divisor D_eff = 2 * pi / f ≈ 5.6385)
matching live SPARC a_0 = 1.1607e-10 m/s^2 at Planck 2018 H_0 = 67.36 km/s/Mpc against the
three pre-registered kills from prediction-falsification-audit-2026-11-16.md §8:
  - Kill 1: Wrong factor (canonical hemisphere f=1, full-sphere two-fold f=2, or pinned
            euclid_note / BandCircle invariants != 1.1143).
  - Kill 2: Fitting / numerical coincidence (PAPER_15 delta_e = 1.1143% is a 10x decimal
            shift yielding 1 + delta < 1.013; formation-epoch z_form requires tuning).
  - Kill 3: Missing dimensional coupling (KMS 2*pi cancellation yields xi = 1 in
            HorizonScale.lean; live D7 action has no dynamical coupling from Omega_fiber to c*H_0).

Writes machine-readable receipt to benchmarks/wave2_holonomy_audit_2026-11-17.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from scipy.optimize import brentq
import sympy as sp

C_SI = 299792458.0  # m/s (exact SI)
MPC_M = 3.0856775814913673e22  # m (IAU exact)
A0_SPARC_LIVE = 1.1607e-10  # m/s^2 (175 SPARC galaxies under mu_std)
A0_SPARC_CI68 = (1.059e-10, 1.232e-10)
A0_SPARC_CI95 = (0.972e-10, 1.295e-10)
H0_PLANCK18 = 67.36  # km/s/Mpc
H0_PLANCK_ALT = 67.40  # km/s/Mpc


def cH0_SI(h0_km_s_mpc: float) -> float:
    return C_SI * (h0_km_s_mpc * 1e3 / MPC_M)


def run_arithmetic_target_check() -> dict:
    cH0_6736 = cH0_SI(H0_PLANCK18)
    a_hor_6736 = cH0_6736 / (2.0 * math.pi)
    f_emp_6736 = A0_SPARC_LIVE / a_hor_6736
    d_eff_6736 = cH0_6736 / A0_SPARC_LIVE

    cH0_6740 = cH0_SI(H0_PLANCK_ALT)
    a_hor_6740 = cH0_6740 / (2.0 * math.pi)
    f_emp_6740 = A0_SPARC_LIVE / a_hor_6740
    d_eff_6740 = cH0_6740 / A0_SPARC_LIVE

    a_pred_11143 = a_hor_6736 * 1.1143
    assert abs(f_emp_6736 - 1.1143) < 1e-4, f"Expected f_emp ~ 1.1143-1.1144, got {f_emp_6736}"
    assert abs(d_eff_6736 - 5.6385) < 2e-4, f"Expected D_eff ~ 5.6384-5.6385, got {d_eff_6736}"
    assert abs(f_emp_6736 * d_eff_6736 - 2.0 * math.pi) < 1e-12

    print(
        f"[PASS] Arithmetic target (H0=67.36): a_hor = {a_hor_6736:.6e}, "
        f"f_emp = {f_emp_6736:.6f}, D_eff = {d_eff_6736:.6f}"
    )
    return {
        "canon_a0_sparc_m_s2": A0_SPARC_LIVE,
        "sparc_ci68_m_s2": list(A0_SPARC_CI68),
        "sparc_ci95_m_s2": list(A0_SPARC_CI95),
        "planck_67_36": {
            "H0_km_s_Mpc": H0_PLANCK18,
            "cH0_m_s2": cH0_6736,
            "cH0_over_2pi_m_s2": a_hor_6736,
            "f_emp": round(f_emp_6736, 8),
            "D_eff": round(d_eff_6736, 8),
            "a0_at_f_1_1143_m_s2": a_pred_11143,
            "rel_err_at_1_1143": abs(a_pred_11143 - A0_SPARC_LIVE) / A0_SPARC_LIVE,
        },
        "planck_67_40": {
            "H0_km_s_Mpc": H0_PLANCK_ALT,
            "cH0_m_s2": cH0_6740,
            "cH0_over_2pi_m_s2": a_hor_6740,
            "f_emp": round(f_emp_6740, 8),
            "D_eff": round(d_eff_6740, 8),
        },
    }


def run_kill1_fiber_invariants() -> dict:
    a_hor = cH0_SI(H0_PLANCK18) / (2.0 * math.pi)
    f_target = sp.Rational(11143, 10000)

    candidates = [
        ("hemisphere_holonomy_pi_2", sp.Integer(1) - sp.cos(sp.pi / 2), "UT(S^2) cone phi=pi/2"),
        ("full_sphere_two_fold_pi", sp.Integer(1) - sp.cos(sp.pi), "UT(S^2) two-fold / full sphere phi=pi"),
        ("sqrt_T3sq_over_T2sq", sp.sqrt(sp.Rational(5, 6) / sp.Rational(2, 3)), "sqrt(T_3^2 / T_2^2) = sqrt(5)/2"),
        ("sqrt_1_plus_Pc", sp.sqrt(1 + sp.Rational(1, 3)), "sqrt(1 + P_c(1/sqrt(2))) = 2/sqrt(3)"),
        ("T3sq_over_T2sq", sp.Rational(5, 6) / sp.Rational(2, 3), "T_3^2 / T_2^2 = 5/4"),
        ("one_plus_Pc", 1 + sp.Rational(1, 3), "1 + P_c(1/sqrt(2)) = 4/3"),
        ("inv_one_minus_Pc", 1 / (1 - sp.Rational(1, 3)), "1 / (1 - P_c(1/sqrt(2))) = 3/2"),
        ("inv_kappa_theta_0p7", 1 / sp.sqrt(sp.Rational(7, 10) * sp.Rational(13, 10)), "1 / kappa(0.7)"),
    ]

    results = []
    for name, expr, desc in candidates:
        expr_s = sp.simplify(expr)
        assert sp.simplify(expr_s - f_target) != 0, f"Unexpected exact match for {name}"
        val = float(expr_s.evalf())
        a_val = a_hor * val
        pct_vs_sparc = (a_val - A0_SPARC_LIVE) / A0_SPARC_LIVE * 100.0
        in_ci68 = A0_SPARC_CI68[0] <= a_val <= A0_SPARC_CI68[1]
        in_ci95 = A0_SPARC_CI95[0] <= a_val <= A0_SPARC_CI95[1]
        results.append(
            {
                "name": name,
                "symbolic": str(expr_s),
                "description": desc,
                "value": round(val, 8),
                "a0_m_s2": a_val,
                "pct_diff_vs_canon_a0": round(pct_vs_sparc, 4),
                "inside_sparc_68CI": in_ci68,
                "inside_sparc_95CI": in_ci95,
                "exact_equals_1_1143": False,
            }
        )

    # Specifically confirm naive two-fold f=2 is ~+79.5% high (excluded)
    two_fold = next(r for r in results if r["name"] == "full_sphere_two_fold_pi")
    assert abs(two_fold["pct_diff_vs_canon_a0"] - 79.48) < 0.2
    assert not two_fold["inside_sparc_95CI"]

    print(
        f"[PASS] Kill 1 verified: naive two-fold f=2 gives {two_fold['a0_m_s2']:.4e} m/s^2 "
        f"(+{two_fold['pct_diff_vs_canon_a0']:.2f}%, EXCLUDED); closest pinned ratio is "
        f"sqrt(5)/2 = {results[2]['value']:.6f} (+{results[2]['pct_diff_vs_canon_a0']:.2f}%)"
    )
    return {
        "candidates": results,
        "kill1_discharged": False,
        "verdict": "None of the pinned fiber/euclid invariants equals 1.1143; naive f=1 (-10.26%) and f=2 (+79.48%) fail. Closest un-fitted algebraic ratio from euclid_note is sqrt(T_3^2/T_2^2) = sqrt(5)/2 = 1.118034 (+0.33%, inside 68% CI), remaining [C]/[O] without dynamical derivation.",
    }


def run_kill2_no_fitting_expose() -> dict:
    # 1. PAPER_15 slip formula: delta = (1 - theta)^2 * theta / (4 + kappa + theta)
    def slip_eval(theta: float) -> tuple[float, float, float]:
        kappa = math.sqrt(theta * (2.0 - theta))
        delta = ((1.0 - theta) ** 2) * theta / (4.0 + kappa + theta)
        return kappa, delta, 1.0 + delta

    k_070, d_070, f_070 = slip_eval(0.70)
    k_ln2, d_ln2, f_ln2 = slip_eval(math.log(2.0))
    assert abs(d_070 - 0.011143) < 1e-5
    assert f_070 < 1.013 and f_ln2 < 1.013

    # 2. Flat LCDM formation-epoch fitting check (Planck 2018 Omega_m = 0.315, Omega_L = 0.685)
    omega_m, omega_l = 0.315, 0.685
    f_emp = A0_SPARC_LIVE / (cH0_SI(H0_PLANCK18) / (2.0 * math.pi))

    def E_z(z: float) -> float:
        return math.sqrt(omega_m * (1.0 + z) ** 3 + omega_l)

    z_form_linear = brentq(lambda z: E_z(z) - f_emp, 0.0, 2.0, xtol=1e-12)
    z_form_sqrt = brentq(lambda z: math.sqrt(E_z(z)) - f_emp, 0.0, 2.0, xtol=1e-12)

    print(
        f"[PASS] Kill 2 verified: PAPER_15 delta(0.70) = {d_070*100:.4f}% gives factor {f_070:.6f} "
        f"(10x shift from 1.1143); LCDM z_form requires continuous fit z = {z_form_linear:.4f} (H(z)/H0) or {z_form_sqrt:.4f} (sqrt)"
    )
    return {
        "paper15_slip_at_theta_0p70": {
            "theta": 0.70,
            "kappa": round(k_070, 8),
            "delta_fraction": round(d_070, 8),
            "delta_percent": round(d_070 * 100.0, 6),
            "one_plus_delta": round(f_070, 8),
            "tenfold_decimal_shift_confirmed": True,
        },
        "paper15_slip_at_theta_ln2": {
            "theta": round(math.log(2.0), 8),
            "kappa": round(k_ln2, 8),
            "delta_fraction": round(d_ln2, 8),
            "delta_percent": round(d_ln2 * 100.0, 6),
            "one_plus_delta": round(f_ln2, 8),
        },
        "lcdm_formation_redshift_fit": {
            "Omega_m": omega_m,
            "Omega_Lambda": omega_l,
            "f_target_67_36": round(f_emp, 8),
            "z_form_if_E_equals_f": round(z_form_linear, 6),
            "z_form_if_sqrtE_equals_f": round(z_form_sqrt, 6),
        },
        "kill2_discharged": False,
    }


def run_kill3_dimensional_coupling() -> dict:
    hbar, a, c, H, kB, pi_sym = sp.symbols("hbar a c H kB pi", positive=True)
    T_U = (hbar * a) / (2 * pi_sym * c * kB)
    T_GH = (hbar * H) / (2 * pi_sym * kB)
    sol_a = sp.solve(sp.Eq(T_U, T_GH), a)[0]
    assert sp.simplify(sol_a - c * H) == 0

    print("[PASS] Kill 3 verified: T_Unruh = T_GH reduces identically to a = c * H (2*pi cancels; xi = 1)")
    return {
        "kms_thermal_matching": "a = c * H (xi = 1, 2*pi cancels identically)",
        "live_d7_action_contains_H0": False,
        "dimensionless_holonomy_coupling_missing": True,
        "kill3_discharged": False,
    }


def main() -> None:
    print("=== Wave 2 Holonomy Audit (BLK-1405 / Closure 5) ===")
    r_target = run_arithmetic_target_check()
    r_k1 = run_kill1_fiber_invariants()
    r_k2 = run_kill2_no_fitting_expose()
    r_k3 = run_kill3_dimensional_coupling()

    here = Path(__file__).resolve().parent
    bench_dir = here.parent / "benchmarks"
    out_path = (bench_dir if bench_dir.is_dir() else here) / "wave2_holonomy_audit_2026-11-17.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "date": "2026-11-17",
        "scope": "Wave 2 Holonomy (BLK-1405) & Closure 5 Audit (prediction-falsification-audit-2026-11-16.md §8)",
        "overall_status": "TARGET_ARITHMETIC_[D]_CONFIRMED; HOLONOMY_DERIVATION_[O]_UNCLOSED (Kills 1-3 active)",
        "arithmetic_target": r_target,
        "kill_1_fiber_invariants": r_k1,
        "kill_2_no_fitting": r_k2,
        "kill_3_dimensional_coupling": r_k3,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"[SAVED] Receipt written to {out_path}")


if __name__ == "__main__":
    main()
