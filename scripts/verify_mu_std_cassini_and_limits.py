#!/usr/bin/env python3
"""
verify_mu_std_cassini_and_limits.py
===================================
Author: R.W. Yett (ORCID: 0009-0001-1303-7190)
Project: Res Nova Monograph / Chyren Autonomous Verification Pipeline

Comprehensive Symbolic & High-Precision Numerical Certification:
1. Exact Constitutive & Potential Calculus:
   - Potential: F_std(x) = 1/2 * (x * sqrt(1 + x^2) - arsinh(x))
   - Constitutive: mu_std(x) = x / sqrt(1 + x^2)
   - First derivative identity: dF_std/dx = x * mu_std(x) = x^2 / sqrt(1 + x^2)
   - Second derivative & strict convexity: F_std''(x) = x * (x^2 + 2) / (1 + x^2)^(3/2) > 0 for all x > 0.
2. Boundary Limits & Asymptotics:
   - Deep-MOND limit (x -> 0):
     lim_{x->0} F_std(x) / x^3 = 1/3 (Constraint C4)
     lim_{x->0} mu_std(x) / x = 1
     Taylor expansion: F_std(x) = x^3/3 - x^5/10 + 3*x^7/56 + O(x^9)
   - Newtonian limit (x -> oo):
     lim_{x->oo} F_std(x) / x^2 = 1/2 (Constraint C3)
     lim_{x->oo} mu_std(x) = 1
     Asymptotic expansion: F_std(x) ~ x^2/2 - 1/2*ln(2x) + 1/4 + O(1/x^2)
     Fractional deviation: delta(x) = 1 - mu_std(x) ~ 1/(2*x^2) - 3/(8*x^4) + O(x^-6)
3. Characteristic Speed Along the Gradient (corrected 2026-09-30):
   - Derived from the quadratic action of the relativistic P(X) completion
     L = f(X), X = g^{mn} d_m phi d_n phi, spacelike background gradient:
       f'(-w^2 + k_perp^2) + (f' + 2 X f'') k_par^2  ==>  c_par^2 = x F''(x) / F'(x)
   - For mu_std: c_par^2 = (x^2 + 2)/(x^2 + 1) in (1, 2]  -- SUPERLUMINAL (RAQUAL acausality)
   - The earlier "c_s^2 = (1+x^2)/(x^2+2) in [1/2, 1), strictly subluminal" was the
     reciprocal: a ratio of spatial stiffnesses with no time-derivative coefficient in it.
     It is asserted below to equal 1/c_par^2 so the inversion cannot silently return.
4. Solar-System MONOPOLE Deviation (scope corrected 2026-09-30):
   - Live a0 = 1.1607e-10 m/s^2 (mu_std SPARC extraction; 1.116e-10 is the superseded
     mu_dual-era value).
   - Evaluated (mpmath 50 digits) at Mercury ... Voyager 1:
   - Exact algebraic solve of spherical field equation: mu(g_phi/a0) * g_phi = g_N
     Exact root: y = sqrt((x^2 + x*sqrt(x^2 + 4)) / 2), g_phi = a0 * y
     Residual anomalous acceleration: Delta g = g_phi - g_N ~ a0^2 / (2 * g_N)
     Fractional deviation: Delta g / g_N ~ 1 / (2 * x^2)
   - NOT a Cassini clearance. 1 - mu is a fractional acceleration shift; the Cassini bound
     |gamma - 1| <= 2.3e-5 (Bertotti et al. 2003) constrains a light-propagation parameter
     and is not comparable. The binding Cassini test is the external-field quadrupole Q2,
     which bare mu_std FAILS at ~4.6 sigma
     (02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md).
   - Contrast against falsified dual branch mu_dual(x) = x / (1 + x):
     Produces unshielded Delta g ~ a0 across all orbits (falsification confirmed).
   - Generates machine-readable receipt at scripts/repro/cassini_clearance_receipt.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import mpmath as mp
import sympy as sp

# Configure 50 decimal digits of precision for high-precision validation
mp.mp.dps = 50

def run_symbolic_proofs():
    print("=" * 80)
    print(" [1/4] SYMPY SYMBOLIC CONSTITUTIVE & DERIVATIVE CERTIFICATION")
    print("=" * 80)

    x, psi = sp.symbols("x psi", positive=True, real=True)

    # 1. Definitions
    mu_std = x / sp.sqrt(1 + x**2)
    F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))
    mu_dual = x / (1 + x)

    # 2. First derivative identity: dF_std/dx = x * mu_std(x)
    dF_dx = sp.diff(F_std, x)
    res_dF = sp.simplify(dF_dx - x * mu_std)
    print(f"[+] dF_std/dx - x*mu_std(x) = {res_dF}")
    assert res_dF == 0, f"Constitutive relation violated! Residual: {res_dF}"

    # 3. Second derivative and strict convexity:
    # F_std''(x) = d/dx [ x^2 / sqrt(1+x^2) ] = x*(x^2 + 2)/(1 + x^2)^(3/2)
    d2F_dx2 = sp.diff(F_std, x, 2)
    expected_d2F = x * (x**2 + 2) / (1 + x**2) ** sp.Rational(3, 2)
    res_d2F = sp.simplify(d2F_dx2 - expected_d2F)
    print(f"[+] F_std''(x) exact formula match residual: {res_d2F}")
    assert res_d2F == 0, f"Second derivative mismatch: {res_d2F}"

    # Verify that F_std''(x) > 0 for all x > 0:
    # Since x > 0, x^2 + 2 > 0, and (1+x^2)^(3/2) > 0, F_std''(x) is strictly positive.
    test_points = [0.001, 0.1, 1.0, 10.0, 1000.0]
    for pt in test_points:
        val = float(expected_d2F.subs(x, pt))
        assert val > 0, f"Non-convex point at x={pt}: {val}"
    print(f"[+] Strict convexity F_std''(x) > 0 verified across test points {test_points}")

    # 4. Rapidity identity: mu_std(sinh(psi)) = tanh(psi)
    mu_sinh = mu_std.subs(x, sp.sinh(psi))
    # sp.sqrt(1 + sinh^2(psi)) = cosh(psi) for positive psi
    res_rapidity = sp.simplify(mu_sinh - sp.tanh(psi))
    print(f"[+] Rapidity identity mu_std(sinh(psi)) - tanh(psi) = {res_rapidity}")
    assert res_rapidity == 0, f"Rapidity identity failed: {res_rapidity}"

    # 5. Rapidity potential conjugacy: dF/dpsi = x^2 = sinh^2(psi)
    F_psi = sp.simplify(F_std.subs(x, sp.sinh(psi)))
    dF_dpsi = sp.simplify(sp.diff(F_psi, psi))
    res_conj = sp.simplify(dF_dpsi - sp.sinh(psi)**2)
    print(f"[+] Rapidity conjugacy dF/dpsi - sinh^2(psi) = {res_conj}")
    assert res_conj == 0, f"Rapidity conjugacy failed: {res_conj}"

    print("    -> PASS: All constitutive and differential calculus identities certified.")
    return {
        "dF_dx_status": "CERTIFIED_EXACT",
        "d2F_dx2_formula": str(expected_d2F),
        "rapidity_identity": "mu_std(sinh(psi)) = tanh(psi)",
        "rapidity_conjugacy": "dF_std/dpsi = sinh^2(psi) = x^2"
    }

def run_boundary_limits():
    print("\n" + "=" * 80)
    print(" [2/4] BOUNDARY LIMITS: C3 NEWTONIAN & C4 DEEP-MOND CERTIFICATION")
    print("=" * 80)

    x = sp.symbols("x", positive=True, real=True)
    mu_std = x / sp.sqrt(1 + x**2)
    F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))

    # C4: Deep-MOND limit as x -> 0
    # lim_{x->0} F_std(x) / x^3 = 1/3
    lim_F_deep = sp.limit(F_std / x**3, x, 0)
    print(f"[+] Deep-MOND limit lim_{{x->0}} F_std(x)/x^3 = {lim_F_deep} (Expected: 1/3)")
    assert lim_F_deep == sp.Rational(1, 3), f"Deep-MOND limit failed: {lim_F_deep}"

    lim_mu_deep = sp.limit(mu_std / x, x, 0)
    print(f"[+] Deep-MOND limit lim_{{x->0}} mu_std(x)/x = {lim_mu_deep} (Expected: 1)")
    assert lim_mu_deep == 1, f"Deep-MOND mu limit failed: {lim_mu_deep}"

    # Taylor series of F_std at x=0
    f_series = sp.series(F_std, x, 0, 8).removeO()
    expected_f_series = sp.Rational(1, 3) * x**3 - sp.Rational(1, 10) * x**5 + sp.Rational(3, 56) * x**7
    res_f_series = sp.simplify(f_series - expected_f_series)
    print(f"[+] F_std series expansion at 0: {f_series} (Residual: {res_f_series})")
    assert res_f_series == 0, f"F_std series expansion failed: {res_f_series}"

    # C3: Newtonian limit as x -> oo
    # lim_{x->oo} F_std(x) / x^2 = 1/2
    lim_F_newton = sp.limit(F_std / x**2, x, sp.oo)
    print(f"[+] Newtonian limit lim_{{x->oo}} F_std(x)/x^2 = {lim_F_newton} (Expected: 1/2)")
    assert lim_F_newton == sp.Rational(1, 2), f"Newtonian limit failed: {lim_F_newton}"

    lim_mu_newton = sp.limit(mu_std, x, sp.oo)
    print(f"[+] Newtonian limit lim_{{x->oo}} mu_std(x) = {lim_mu_newton} (Expected: 1)")
    assert lim_mu_newton == 1, f"Newtonian mu limit failed: {lim_mu_newton}"

    # Asymptotic expansion at large x: F_std(x) - [x^2/2 - 1/2*ln(2x)] -> 1/4
    lim_F_const = sp.limit(F_std - (x**2 / 2 - sp.log(2 * x) / 2), x, sp.oo)
    print(f"[+] High-x constant offset lim_{{x->oo}} [F_std - x^2/2 + ln(2x)/2] = {lim_F_const} (Expected: 1/4)")
    assert lim_F_const == sp.Rational(1, 4), f"High-x offset failed: {lim_F_const}"

    # Fractional deviation series: 1 - mu_std(x) ~ 1/(2*x^2) - 3/(8*x^4)
    # Using substitution u = 1/x -> 0
    u = sp.symbols("u", positive=True)
    mu_inv = mu_std.subs(x, 1 / u)
    delta_series = sp.series(1 - mu_inv, u, 0, 6).removeO().subs(u, 1 / x)
    expected_delta_series = sp.Rational(1, 2) / x**2 - sp.Rational(3, 8) / x**4
    res_delta = sp.simplify(delta_series - expected_delta_series)
    print(f"[+] Asymptotic deviation 1 - mu_std(x) = {delta_series} (Residual: {res_delta})")
    assert res_delta == 0, f"Delta series failed: {res_delta}"

    print("    -> PASS: Both C3 Newtonian and C4 Deep-MOND limits certified.")
    return {
        "deep_mond_F_limit": "1/3",
        "deep_mond_mu_limit": "1",
        "newtonian_F_limit": "1/2",
        "newtonian_mu_limit": "1",
        "high_x_constant_offset": "1/4",
        "asymptotic_deviation_series": str(delta_series)
    }

def run_sound_speed_analysis():
    print("\n" + "=" * 80)
    print(" [3/4] CHARACTERISTIC SPEED ALONG THE GRADIENT (P(X) COMPLETION)")
    print("=" * 80)

    x = sp.symbols("x", positive=True, real=True)
    X, w, kpar, kperp = sp.symbols("X omega k_par k_perp", positive=True)
    F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))
    mu_std = x / sp.sqrt(1 + x**2)

    # P(X) completion: f(X) = F_std(sqrt(X)), X = x^2 (units a0 = 1).
    f = F_std.subs(x, sp.sqrt(X))
    fp, fpp = sp.diff(f, X), sp.diff(f, X, 2)
    # Quadratic action f'(-w^2 + kperp^2) + (f' + 2 X f'') kpar^2 = 0 on shell.
    disp = -fp * w**2 + fp * kperp**2 + (fp + 2 * X * fpp) * kpar**2
    w2_par = sp.solve(disp.subs(kperp, 0), w**2)[0] / kpar**2
    w2_perp = sp.solve(disp.subs(kpar, 0), w**2)[0] / kperp**2
    c_par2 = sp.simplify(w2_par.subs(X, x**2))
    c_perp2 = sp.simplify(w2_perp.subs(X, x**2))

    # The same speed from F alone: c_par^2 = x F'' / F' (what MuStdFoundations.lean proves).
    c_par2_F = sp.simplify(x * sp.diff(F_std, x, 2) / sp.diff(F_std, x))
    expected = (x**2 + 2) / (x**2 + 1)
    assert sp.simplify(c_par2 - expected) == 0, c_par2
    assert sp.simplify(c_par2_F - expected) == 0, c_par2_F
    assert sp.simplify(c_perp2 - 1) == 0, c_perp2
    print(f"[+] c_par^2 (from dispersion relation) = {sp.factor(c_par2)}")
    print(f"[+] c_par^2 (x F''/F')                 = {sp.factor(c_par2_F)}")
    print(f"[+] c_perp^2                           = {c_perp2}")

    # Guard against the 2026-09-29 inversion: the old "c_s^2" was 1/c_par^2.
    old_cs2 = mu_std / (mu_std + x * sp.diff(mu_std, x))
    assert sp.simplify(old_cs2 * c_par2 - 1) == 0
    print("[+] Retired c_s^2 = mu/(mu + x mu') equals 1/c_par^2 (a stiffness ratio, not a speed)")

    lim0 = sp.limit(expected, x, 0)
    limoo = sp.limit(expected, x, sp.oo)
    assert lim0 == 2 and limoo == 1
    # 1 < c_par^2 <= 2: c_par^2 - 1 = 1/(x^2+1) > 0; 2 - c_par^2 = x^2/(x^2+1) >= 0
    assert sp.simplify(expected - 1 - 1 / (x**2 + 1)) == 0
    assert sp.simplify(2 - expected - x**2 / (x**2 + 1)) == 0
    print(f"[+] Deep-MOND c_par^2(0) = {lim0}; Newtonian c_par^2(oo) = {limoo}")
    print("    -> RESULT: 1 < c_par^2 <= 2 for x > 0. The P(X) completion is SUPERLUMINAL along")
    print("       the gradient (RAQUAL acausality). AeST's scalar speed is a separate result (D6).")
    return {
        "c_par_sq_formula": "c_par^2(x) = x F''/F' = (x^2 + 2)/(x^2 + 1)",
        "c_perp_sq": "1",
        "deep_mond_c_par_sq": "2",
        "newtonian_c_par_sq": "1",
        "verdict": "SUPERLUMINAL along the gradient in the P(X) completion (1 < c_par^2 <= 2)",
        "retired_claim": "c_s^2 = (1+x^2)/(x^2+2) in [1/2,1), 'strictly subluminal' -- was 1/c_par^2; retracted 2026-09-30",
    }

def run_cassini_and_solar_system():
    print("\n" + "=" * 80)
    print(" [4/4] SOLAR SYSTEM MONOPOLE DEVIATION (NOT A CASSINI CLEARANCE)")
    print("=" * 80)

    # Fundamental physical constants (SI units):
    # CODATA / IAU standard parameters
    G_M_sun = mp.mpf("1.32712440018e20")  # m^3 / s^2 (solar gravitational parameter GM_sun)
    AU_in_m = mp.mpf("1.495978707e11")    # m (1 Astronomical Unit)
    a0_sparc = mp.mpf("1.1607e-10")        # m / s^2 (live mu_std SPARC extraction)

    # Solar System Bodies / Orbital distances (semi-major axis in AU)
    orbit_data = [
        ("Mercury", mp.mpf("0.38709893")),
        ("Venus", mp.mpf("0.72333199")),
        ("Earth", mp.mpf("1.00000011")),
        ("Mars", mp.mpf("1.52366231")),
        ("Jupiter", mp.mpf("5.2044")),
        ("Saturn (Cassini)", mp.mpf("9.5826")),
        ("Uranus", mp.mpf("19.201")),
        ("Neptune", mp.mpf("30.047")),
        ("Kuiper Belt (Inner)", mp.mpf("40.0")),
        ("Voyager 1 / Heliopause", mp.mpf("100.0")),
    ]

    print(f"Physical Parameters:")
    print(f"  GM_sun:        {G_M_sun} m^3/s^2")
    print(f"  1 AU:          {AU_in_m} m")
    print(f"  a0 (SPARC):    {a0_sparc} m/s^2")
    print("-" * 105)
    print(f"{'Body':<23} | {'r (AU)':<7} | {'g_N (m/s^2)':<11} | {'x = g_N/a0':<11} | {'delta_std (1-mu)':<16} | {'Delta g (m/s^2)'}")
    print("-" * 105)

    results_table = []

    for name, r_au in orbit_data:
        r_meters = r_au * AU_in_m
        g_N = G_M_sun / (r_meters**2)
        x_val = g_N / a0_sparc

        # Exact algebraic solution to spherical AQUAL/AeST field equation:
        # mu_std(y) * y = x  where y = g_phi / a0
        # y^2 / sqrt(1 + y^2) = x  ==>  y^4 - x^2 * y^2 - x^2 = 0
        # Root: y^2 = (x^2 + x * sqrt(x^2 + 4)) / 2
        y_exact = mp.sqrt((x_val**2 + x_val * mp.sqrt(x_val**2 + 4)) / 2)
        g_phi_exact = a0_sparc * y_exact
        delta_g_exact = g_phi_exact - g_N

        # Constitutive values
        mu_std_val = x_val / mp.sqrt(1 + x_val**2)
        delta_std = 1 - mu_std_val

        # Dual branch (falsified): mu_dual(x) = x / (1 + x)
        mu_dual_val = x_val / (1 + x_val)
        delta_dual = 1 - mu_dual_val
        # Solve dual: y^2 / (1 + y) = x ==> y^2 - x*y - x = 0 ==> y = (x + sqrt(x^2 + 4*x))/2
        y_dual = (x_val + mp.sqrt(x_val**2 + 4 * x_val)) / 2
        g_phi_dual = a0_sparc * y_dual
        delta_g_dual = g_phi_dual - g_N

        print(f"{name:<23} | {float(r_au):<7.3f} | {float(g_N):<11.4e} | {float(x_val):<11.4e} | {float(delta_std):<16.6e} | {float(delta_g_exact):.4e}")

        results_table.append({
            "target": name,
            "radius_au": float(r_au),
            "radius_m": float(r_meters),
            "g_N_mps2": float(g_N),
            "x_ratio": float(x_val),
            "mu_std": float(mu_std_val),
            "delta_std": float(delta_std),
            "delta_g_exact_mps2": float(delta_g_exact),
            "mu_dual": float(mu_dual_val),
            "delta_dual": float(delta_dual),
            "delta_g_dual_mps2": float(delta_g_dual),
        })

    print("-" * 105)

    # Saturn monopole check, matching MuStdFoundations.saturn_monopole_deviation_le:
    saturn_entry = next(e for e in results_table if "Saturn" in e["target"])
    print(f"\n[+] Monopole deviation at Saturn (r = {saturn_entry['radius_au']} AU):")
    print(f"    Newtonian acceleration g_N:       {saturn_entry['g_N_mps2']:.6e} m/s^2")
    print(f"    Gradient parameter x:             {saturn_entry['x_ratio']:.6e}")
    print(f"    Standard mu deviation (1 - mu):   {saturn_entry['delta_std']:.6e}")
    assert saturn_entry["x_ratio"] >= 5e5, "Saturn x below the Lean theorem's hypothesis"
    assert saturn_entry["delta_std"] <= 2e-12, "Saturn monopole deviation exceeds the Lean bound"
    print("    SCOPE: isolated-Sun monopole only. Not comparable to the Cassini |gamma-1| bound.")
    print("    The binding Cassini test is the EFE quadrupole Q2, which bare mu_std FAILS (~4.6 sigma);")
    print("    see 02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md.")

    # Falsification contrast:
    print("\n[+] Contrast Against Falsified Dual Branch mu_dual(x) = x / (1 + x):")
    mercury_entry = next(e for e in results_table if "Mercury" in e["target"])
    print(f"    Mercury: Delta g (mu_std)  = {mercury_entry['delta_g_exact_mps2']:.6e} m/s^2 (Suppressed by 1/r^2 ~ 10^-19 m/s^2)")
    print(f"    Mercury: Delta g (mu_dual) = {mercury_entry['delta_g_dual_mps2']:.6e} m/s^2 (Unshielded, ~a0)")
    print(f"    Ratio [mu_dual / mu_std] residual at Mercury: {mercury_entry['delta_g_dual_mps2'] / mercury_entry['delta_g_exact_mps2']:.2e}x")
    print(f"    Conclusion: mu_dual produces unshielded ~10^-10 m/s^2 constant force, violating planetary perihelion shifts by > 10^3x.")
    print(f"    mu_std monopole: Delta g ~ a0^2/(2*g_N) is suppressed near the Sun (EFE quadrupole not covered).")

    return results_table

def main():
    print("=" * 80)
    print(" RES NOVA CANONICAL PHYSICS & THEOREM PROVING SUITE")
    print(" Verification of mu_std Constitutive Calculus, Gradient Characteristic Speed & Monopole Tail")
    print(" Author: R.W. Yett | ORCID: 0009-0001-1303-7190")
    print("=" * 80)

    res_1 = run_symbolic_proofs()
    res_2 = run_boundary_limits()
    res_3 = run_sound_speed_analysis()
    res_4 = run_cassini_and_solar_system()

    receipt = {
        "title": "Res Nova Monograph - mu_std Constitutive, Characteristic Speed & Monopole Receipt",
        "author": "R.W. Yett (ORCID: 0009-0001-1303-7190)",
        "timestamp_iso": "2026-09-30T00:00:00Z",
        "symbolic_calculus": res_1,
        "boundary_limits": res_2,
        "gradient_characteristic_speed": res_3,
        "saturn_monopole": {
            "r_au": 9.5826,
            "a0_mps2": 1.1607e-10,
            "delta_std": next(e["delta_std"] for e in res_4 if "Saturn" in e["target"]),
            "lean_bound": "1 - mu_std(x) <= 2e-12 for x >= 5e5 (saturn_monopole_deviation_le)",
            "scope": "Isolated-Sun monopole only. Not a Cassini clearance: the EFE quadrupole Q2 is the binding test and bare mu_std fails it at ~4.6 sigma (CASSINI_EFE_QUADRUPOLE_2026-09-27.md)."
        },
        "planetary_monopole_table": res_4,
        "overall_status": "CALCULUS_VERIFIED; P(X)_COMPLETION_SUPERLUMINAL; MONOPOLE_ONLY_NOT_CASSINI"
    }

    receipt_path = Path(__file__).resolve().parent / "repro" / "cassini_clearance_receipt.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"\n[✓] Machine-readable receipt written to: {receipt_path}")
    print("=" * 80)
    print(" STATUS: ALL ASSERTIONS PASSED (see scope notes above)")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())
