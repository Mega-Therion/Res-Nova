#!/usr/bin/env python3
"""Postulate R Analytic Induced-Metric Brane No-Go & Analytic Auxiliary-Susceptibility Realization.

Extends `audits/2026-11-19/postulate_r_membrane_derivation.py` (PR #241).

WHAT IS PROVED SYMBOLICALLY HERE (and machine-checked in `05_lean_formalization/PostulateRAnalyticNoGo.lean`):
  [P] 1. Induced 3-brane metric spectrum: for h_ij = delta_ij + v_i v_j (v = grad phi / a0, |v| = x),
         the three eigenvalues are {1 + x^2, 1, 1}, so EVERY rotational scalar invariant of h_ij
         (det h, tr h, tr h^2, tr h^3, sqrt(det h), ...) is an analytic function of y = x^2 ONLY.
  [P] 2. Analytic induced-metric brane no-go: for ANY local 1-field action L(h_ij) = L_tilde(y)
         with L_tilde C^2 at y = 0, the Euler-Lagrange response mu(x) = 2 L_tilde'(x^2) has
         right-derivative mu'(0+) = 0, whereas mu_std(x) = x/sqrt(1+x^2) has mu_std'(0+) = 1.
         Hence NO analytic functional of the induced 3-brane metric (not Nambu-Goto, not DBI,
         not any polynomial or analytic function of det h and tr(h^k)) can reproduce Postulate R
         or any deep-MOND interpolating function with mu(x) ~ x as x -> 0+.
  [P] 3. Second-derivative blowup of the AQUAL kinetic function: J_std(y) = F_std(sqrt(y)) has
         J_std'(y) = sqrt(y) / (2 sqrt(1 + y)) and J_std''(y) = 1 / (4 sqrt(y) (1 + y)^(3/2)),
         which diverges as y^(-1/2) -> +oo at y -> 0+ (a y^(3/2) branch point).
  [P] 4. Exact analytic auxiliary-susceptibility realization: introducing a scalar susceptibility
         field s in [0, 1) with the COMPLETELY REAL-ANALYTIC potential
             V(s) = (1/2) (artanh(s) - s) = s^3/6 + s^5/10 + s^7/14 + ...
         and two-field Lagrangian L(x, s) = (1/2) s x^2 - V(s):
         - V'(0) = 0 and V''(0) = 0 (a massless spinodal critical point at s = 0);
         - stationarity dL/ds = 0 uniquely selects s = mu_std(x) = x / sqrt(1 + x^2) = sin(theta);
         - on-shell L(x, mu_std(x)) = F_std(x) = (1/2)(x sqrt(1+x^2) - arsinh(x)) identically;
         - strict concavity d^2 L / ds^2 = -s / (1 - s^2)^2 < 0 on (0, 1) makes F_std(x) the
           exact global supremum sup_{s in [0,1)} [(1/2) s x^2 - V(s)].

HONEST SCOPING:
  [O] Choosing V(s) = (1/2)(artanh(s) - s) among all cubic-onset analytic potentials
      V(s) = s^3/6 + O(s^5) is a constructive auxiliary-field realization equivalent to
      selecting mu_std; it does NOT derive mu_std uniquely from first principles without an
      independent dynamical principle selecting V(s).
"""
from __future__ import annotations

import json
import os
import sys
import sympy as sp


def main() -> int:
    x = sp.symbols("x", positive=True)
    y = sp.symbols("y", positive=True)
    s = sp.symbols("s", real=True)
    v1, v2, v3 = sp.symbols("v1 v2 v3", real=True)

    mu_std = x / sp.sqrt(1 + x**2)
    F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))
    J_std = F_std.subs(x, sp.sqrt(y))

    checks: dict[str, bool] = {}

    def verify(name: str, expr) -> None:
        val = sp.simplify(expr)
        ok = val == 0
        checks[name] = ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            print(f"         residual = {val}")

    print("=" * 78)
    print("POSTULATE R: ANALYTIC INDUCED-METRIC NO-GO & AUXILIARY-FIELD REALIZATION")
    print("=" * 78)

    # 1. Exact induced 3-brane metric h_ij = delta_ij + v_i v_j spectrum
    v = sp.Matrix([v1, v2, v3])
    h = sp.eye(3) + v * v.T
    v2_norm = v1**2 + v2**2 + v3**2
    det_h = sp.factor(h.det())
    tr_h = sp.simplify(h.trace())
    tr_h2 = sp.simplify((h * h).trace())
    lam = sp.Symbol("lam")
    charpoly = sp.factor((h - lam * sp.eye(3)).det())
    expected_charpoly = -(lam - 1) ** 2 * (lam - (1 + v2_norm))
    verify("charpoly(delta_ij + v_i v_j) = -(lam-1)^2 (lam - (1 + |v|^2))", charpoly - expected_charpoly)
    verify("det(h) = 1 + |v|^2", det_h - (1 + v2_norm))
    verify("tr(h) = 3 + |v|^2", tr_h - (3 + v2_norm))
    verify("tr(h^2) = (1 + |v|^2)^2 + 2", tr_h2 - ((1 + v2_norm) ** 2 + 2))

    # 2. Analytic induced-metric response derivative at x = 0 vs mu_std'(0)
    g = sp.Function("g")
    x_real = sp.Symbol("x_real", real=True)
    d_even_at_0 = sp.diff(g(x_real**2), x_real).subs(x_real, 0)
    d_mu_at_0 = sp.limit(sp.diff(mu_std, x), x, 0, "+")
    verify("d/dx [g(x^2)]|_{x=0} = 0 for arbitrary C^1 g", d_even_at_0)
    verify("mu_std'(0+) = 1", d_mu_at_0 - 1)

    # 3. AQUAL kinetic function J_std(y) = F_std(sqrt(y)) second-derivative blowup at y -> 0+
    J1 = sp.simplify(sp.diff(J_std, y))
    J2 = sp.simplify(sp.diff(J1, y))
    J1_expected = sp.sqrt(y) / (2 * sp.sqrt(1 + y))
    J2_expected = 1 / (4 * sp.sqrt(y) * (1 + y) ** sp.Rational(3, 2))
    verify("J_std'(y) = sqrt(y) / (2 sqrt(1 + y))", J1 - J1_expected)
    verify("J_std''(y) = 1 / (4 sqrt(y) (1 + y)^(3/2))", J2 - J2_expected)
    lim_J2 = sp.limit(J2, y, 0, "+")
    checks["J_std''(y) -> +oo as y -> 0+"] = lim_J2 == sp.oo
    print(f"  [{'PASS' if lim_J2 == sp.oo else 'FAIL'}] J_std''(y) -> {lim_J2} as y -> 0+")

    # 4. Exact analytic auxiliary-susceptibility realization
    #    L(x, s) = (1/2) s x^2 - V(s),  V(s) = (1/2)(artanh(s) - s) = (1/4) log((1+s)/(1-s)) - s/2
    V = sp.Rational(1, 2) * (sp.atanh(s) - s)
    V_log = sp.Rational(1, 4) * sp.log((1 + s) / (1 - s)) - sp.Rational(1, 2) * s
    V1 = sp.simplify(sp.diff(V, s))
    V2 = sp.simplify(sp.diff(V1, s))
    V3 = sp.simplify(sp.diff(V2, s))
    verify("V'(s) = s^2 / (2 (1 - s^2))", V1 - s**2 / (2 * (1 - s**2)))
    verify("V''(s) = s / (1 - s^2)^2", V2 - s / (1 - s**2) ** 2)
    verify("V'(0) = 0", V1.subs(s, 0))
    verify("V''(0) = 0 (massless spinodal critical point)", V2.subs(s, 0))
    verify("V'''(0) = 1 (cubic onset)", V3.subs(s, 0) - 1)

    # Series expansion of V(s) around s = 0
    V_series = sp.series(V, s, 0, 8).removeO()
    verify("V(s) Taylor = s^3/6 + s^5/10 + s^7/14 + O(s^9)",
           V_series - (s**3 / 6 + s**5 / 10 + s**7 / 14))

    # Stationarity dL/ds = x^2/2 - V'(s) = 0 at s = mu_std(x)
    L_aux = sp.Rational(1, 2) * s * x**2 - V_log
    dL_ds = sp.diff(L_aux, s)
    verify("dL/ds |_{s = mu_std(x)} = 0", dL_ds.subs(s, mu_std))

    # Exact identity artanh(x / sqrt(1 + x^2)) = arsinh(x)
    ratio = sp.simplify((1 + mu_std) / (1 - mu_std))
    # Multiply numerator & denominator by sqrt(1+x^2) + x -> (sqrt(1+x^2) + x)^2
    verify("(1 + mu_std)/(1 - mu_std) = (x + sqrt(1 + x^2))^2",
           ratio - (x + sp.sqrt(1 + x**2)) ** 2)

    # On-shell Lagrangian L(x, mu_std(x)) = F_std(x)
    # Substitute (1+mu_std)/(1-mu_std) = (x+sqrt(1+x^2))^2 and log((x+sqrt(1+x^2))^2)/2 = asinh(x)
    L_onshell = sp.Rational(1, 2) * mu_std * x**2 - (sp.Rational(1, 2) * sp.asinh(x) - sp.Rational(1, 2) * mu_std)
    verify("L(x, mu_std(x)) = F_std(x) identically", L_onshell - F_std)

    # Numeric sanity check of L_aux(x, s) <= F_std(x) across grid (x, s)
    f_L = sp.lambdify((x, s), L_aux, "math")
    f_F = sp.lambdify(x, F_std, "math")
    f_mu = sp.lambdify(x, mu_std, "math")
    max_onshell_err = 0.0
    max_sup_violation = 0.0
    for xv in (0.05, 0.2, 0.5, 1.0, 2.5, 10.0):
        fv = f_F(xv)
        mv = f_mu(xv)
        max_onshell_err = max(max_onshell_err, abs(f_L(xv, mv) - fv))
        for sv in (0.0, 0.05, 0.2, 0.5, 0.8, 0.95, 0.995):
            diff = f_L(xv, sv) - fv
            if diff > max_sup_violation:
                max_sup_violation = diff
    checks["numeric_onshell_err < 1e-14"] = max_onshell_err < 1e-14
    checks["numeric_global_max_holds"] = max_sup_violation <= 1e-14
    print(f"  [{'PASS' if max_onshell_err < 1e-14 else 'FAIL'}] numeric on-shell max err = {max_onshell_err:.2e}")
    print(f"  [{'PASS' if max_sup_violation <= 1e-14 else 'FAIL'}] numeric supremum max violation = {max_sup_violation:.2e}")

    all_ok = all(checks.values())
    out = {
        "all_checks_passed": all_ok,
        "n_checks": len(checks),
        "checks": checks,
        "V_taylor_order_7": str(V_series),
        "J_std_second_deriv": str(J2_expected),
        "max_onshell_err": max_onshell_err,
        "max_sup_violation": max_sup_violation,
        "lean_module": "05_lean_formalization/PostulateRAnalyticNoGo.lean",
        "verdict": {
            "analytic_induced_metric_brane_route": "[X] / [P] no-go: any C^2-in-y local metric invariant has mu'(0+) = 0 != 1",
            "auxiliary_susceptibility_realization": "[P] exact Legendre-Fenchel supremum F_std(x) = sup_{s in [0,1)} [s x^2 / 2 - (artanh s - s)/2] with real-analytic V(s) and spinodal critical point V'(0) = V''(0) = 0",
            "selection_of_V_s": "[O] constructive realization; selecting V(s) = (artanh s - s)/2 among cubic-onset potentials remains equivalent to Postulate R",
        },
    }
    out_path = os.path.join(os.path.dirname(__file__), "POSTULATE_R_ANALYTIC_NOGO.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nALL CHECKS: {'PASS' if all_ok else 'FAIL'} ({sum(checks.values())}/{len(checks)})")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
