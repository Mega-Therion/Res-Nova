#!/usr/bin/env python3
"""
Q3 Chiral Maurer-Cartan Projection & Gelfand-Yaglom Functional Determinant Audit
(/home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/q3_chiral_det.py).

Tests whether:
  (1) the unprojected path-ordered exponential H(x) = P exp(-int_0^x A(u) du)
      of A(x) = B(x)^(-1) dB/dx satisfies ln det H(x) = arsinh(x),
  (2) chiral projection I_{P+}(x) = int_0^x tr(P+ A(u)) du reproduces arsinh(x)
      solely via the algebraic Maurer-Cartan trace identity tr(P+ sigma_1) = 1,
  (3) the Gelfand-Yaglom determinant ratio for L = d/du + A(u) on [0, x]
      produces arsinh(x), and
  (4) any matching object also matches F_std(x) = (1/2) (x sqrt(1+x^2) - arsinh(x)).

Exit 0 means the script finished, not that F_std was derived.
"""

import json
import pathlib
import sys
import sympy as sp


def reduce_s2(expr: sp.Expr, x_sym: sp.Symbol, s_sym: sp.Symbol) -> sp.Expr:
    """Reduce powers of s modulo s^2 = 1 + x^2 in Q(x)[s]."""
    num, den = sp.fraction(sp.together(expr))
    mod_expr = s_sym**2 - (1 + x_sym**2)
    num_rem = sp.rem(sp.expand(num), mod_expr, s_sym)
    den_rem = sp.rem(sp.expand(den), mod_expr, s_sym)
    return sp.simplify(sp.cancel(num_rem / den_rem))


def simplify_hyp(expr: sp.Expr) -> sp.Expr:
    """Canonical simplification across hyperbolic / logarithmic forms on R."""
    e1 = sp.simplify(expr)
    if e1 == 0:
        return sp.Integer(0)
    e2 = sp.simplify(e1.rewrite(sp.log))
    if e2 == 0:
        return sp.Integer(0)
    return e1


def compare_candidate(
    name: str,
    expr_x: sp.Expr,
    x_sym: sp.Symbol,
    arsinh_expr: sp.Expr,
    f_std_expr: sp.Expr,
    extra_fields: dict | None = None,
) -> dict:
    """
    Compare expr_x symbolically and numerically (at x = 0.1, 1, 3) against
    arsinh(x) and F_std(x) = (1/2)*(x*sqrt(1+x^2) - arsinh(x)).
    """
    diff_arsinh = simplify_hyp(expr_x - arsinh_expr)
    diff_f_std = simplify_hyp(expr_x - f_std_expr)

    sym_zero_arsinh = bool(diff_arsinh == 0)
    sym_zero_f_std = bool(diff_f_std == 0)

    test_points = [
        ("0.1", sp.Rational(1, 10)),
        ("1", sp.Integer(1)),
        ("3", sp.Integer(3)),
    ]

    num_abs_diffs = {}
    all_num_arsinh_zero = True
    all_num_f_std_zero = True

    for label, pt in test_points:
        val_num = float(sp.N(expr_x.subs(x_sym, pt), 30))
        arsinh_num = float(sp.N(arsinh_expr.subs(x_sym, pt), 30))
        f_std_num = float(sp.N(f_std_expr.subs(x_sym, pt), 30))

        abs_d_arsinh = abs(val_num - arsinh_num)
        abs_d_f_std = abs(val_num - f_std_num)

        if abs_d_arsinh >= 1e-10:
            all_num_arsinh_zero = False
        if abs_d_f_std >= 1e-10:
            all_num_f_std_zero = False

        num_abs_diffs[label] = {
            "value": val_num,
            "abs_diff_from_arsinh": abs_d_arsinh,
            "abs_diff_from_F_std": abs_d_f_std,
            "within_1e-10_of_arsinh": bool(abs_d_arsinh < 1e-10),
            "within_1e-10_of_F_std": bool(abs_d_f_std < 1e-10),
        }

    out = {
        "name": name,
        "symbolic": str(expr_x),
        "difference_from_arsinh": str(diff_arsinh),
        "difference_from_F_std": str(diff_f_std),
        "numerical_absolute_differences": num_abs_diffs,
        "matches_arsinh": bool(sym_zero_arsinh and all_num_arsinh_zero),
        "matches_F_std": bool(sym_zero_f_std and all_num_f_std_zero),
    }
    if extra_fields:
        out.update(extra_fields)
    return out


def main() -> int:
    x = sp.Symbol("x", real=True)
    u = sp.Symbol("u", real=True)
    u1 = sp.Symbol("u1", real=True)
    u2 = sp.Symbol("u2", real=True)
    s = sp.Symbol("s", positive=True, real=True)

    # =========================================================================
    # INPUTS FIXED BY q3_det_ratio.py
    # =========================================================================
    B_xs = sp.Matrix([[s, x], [x, s]])
    # Derivative dB/dx under s^2 = 1 + x^2 => ds/dx = x/s:
    dB_dx_xs = sp.Matrix([[x / s, 1], [1, x / s]])

    det_B_xs = reduce_s2(B_xs.det(), x, s)
    B_adj_xs = B_xs.adjugate()
    B_inv_xs = sp.Matrix(
        2, 2, lambda i, j: reduce_s2(B_adj_xs[i, j] / det_B_xs, x, s)
    )
    A_raw_xs = B_inv_xs * dB_dx_xs
    A_xs = sp.Matrix(2, 2, lambda i, j: reduce_s2(A_raw_xs[i, j], x, s))

    # Independent direct SymPy differentiation check with s_real = sqrt(1 + x^2):
    s_real = sp.sqrt(1 + x**2)
    B_real = sp.Matrix([[s_real, x], [x, s_real]])
    A_real_direct = sp.simplify(B_real.inv() * B_real.diff(x))

    sigma_1 = sp.Matrix([[0, 1], [1, 0]])
    sigma_3 = sp.Matrix([[1, 0], [0, -1]])
    I2 = sp.eye(2)

    expected_A_xs = sigma_1 / s
    expected_A_real = sigma_1 / s_real

    if A_xs != expected_A_xs or A_real_direct != expected_A_real:
        sys.stderr.write(
            f"ERROR: A(x) simplified to {A_xs.tolist()} (direct: {A_real_direct.tolist()}), "
            "expected sigma_1 / s.\n"
        )
        return 1

    A_simplified_record = [[str(A_xs[i, j]) for j in range(2)] for i in range(2)]
    print(f"A_simplified (under s^2 = 1 + x^2): {A_simplified_record}")

    # =========================================================================
    # PRE-REGISTERED OPERATORS (BEFORE ANY COMPARISON; NO OTHERS)
    #   U:  2x2 path-ordered exponential of -int_0^x A(u) du (no projector)
    #   P+: (I + sigma_1) / 2
    #   P-: (I - sigma_1) / 2
    #   P3: (I + sigma_3) / 2
    # =========================================================================
    P_plus = (I2 + sigma_1) / sp.Integer(2)
    P_minus = (I2 - sigma_1) / sp.Integer(2)
    P_3 = (I2 + sigma_3) / sp.Integer(2)

    projectors = [
        ("P+", P_plus),
        ("P-", P_minus),
        ("P3", P_3),
    ]

    # =========================================================================
    # STEP 1: ALGEBRA (BEFORE ANY INTEGRAL)
    # =========================================================================
    step1_traces_xs = {}
    for p_name, p_mat in projectors:
        tr_val = reduce_s2((p_mat * A_xs).trace(), x, s)
        step1_traces_xs[p_name] = tr_val
        print(f"Step 1 | tr({p_name} * A(x)) = {tr_val}")

    tr_P_plus_sigma1 = sp.simplify((P_plus * sigma_1).trace())
    print(f"Step 1 | tr(P+ * sigma_1) = {tr_P_plus_sigma1}")
    if tr_P_plus_sigma1 != sp.Integer(1):
        sys.stderr.write(
            f"ERROR: tr(P+ * sigma_1) evaluated to {tr_P_plus_sigma1}, expected 1.\n"
        )
        return 1

    identity_not_derivation = True

    # =========================================================================
    # STEP 2: INTEGRALS & COMPARISONS
    # =========================================================================
    A_of_u = A_xs.subs({x: u, s: sp.sqrt(1 + u**2)})

    # Verify [A(u1), A(u2)] == 0 in SymPy so path-ordering collapses to exp:
    A_u1 = A_of_u.subs(u, u1)
    A_u2 = A_of_u.subs(u, u2)
    commutator_A = sp.simplify(A_u1 * A_u2 - A_u2 * A_u1)
    if commutator_A != sp.zeros(2, 2):
        sys.stderr.write("ERROR: [A(u1), A(u2)] is nonzero; path-ordering does not collapse.\n")
        return 1

    neg_int_A = sp.Matrix(
        2, 2, lambda i, j: -sp.integrate(A_of_u[i, j], (u, 0, x))
    )
    H_raw = neg_int_A.exp()
    H_mat = sp.Matrix(
        2,
        2,
        lambda i, j: sp.simplify(
            sp.radsimp(sp.simplify(H_raw[i, j].rewrite(sp.log)))
        ),
    )

    # Verify H(x) solves (d/dx) H(x) + A(x) H(x) = 0 with H(0) = I:
    ode_residual = sp.simplify(H_mat.diff(x) + A_real_direct * H_mat)
    assert ode_residual == sp.zeros(2, 2)
    assert H_mat.subs(x, 0) == I2

    # Compute det H(x) and ln det H(x) from H_mat without assuming its determinant:
    det_H = simplify_hyp(H_mat.det())
    ln_det_H = simplify_hyp(sp.log(det_H))
    print(f"Step 2 | H(x) = {H_mat.tolist()}")
    print(f"Step 2 | det H(x) = {det_H}, ln det H(x) = {ln_det_H}")

    # Compute I_P(x) = int_0^x tr(P A(u)) du for each pre-registered projector:
    projector_integrals = {}
    for p_name, p_mat in projectors:
        tr_integrand_u = sp.simplify((p_mat * A_of_u).trace())
        int_val = sp.simplify(sp.integrate(tr_integrand_u, (u, 0, x)))
        projector_integrals[p_name] = (tr_integrand_u, int_val)
        print(f"Step 2 | I_{p_name}(x) = int_0^x ({tr_integrand_u}) du = {int_val}")

    # Target functions for comparison (do not drop algebraic piece of F_std):
    arsinh_x = sp.asinh(x)
    F_std_x = sp.Rational(1, 2) * (x * s_real - sp.asinh(x))

    comp_ln_det_H = compare_candidate(
        "ln_det_H",
        ln_det_H,
        x,
        arsinh_x,
        F_std_x,
    )
    comp_I_P_plus = compare_candidate(
        "I_P+",
        projector_integrals["P+"][1],
        x,
        arsinh_x,
        F_std_x,
        {
            "step1_trace_s": str(step1_traces_xs["P+"]),
            "integrand_u": str(projector_integrals["P+"][0]),
        },
    )
    comp_I_P_minus = compare_candidate(
        "I_P-",
        projector_integrals["P-"][1],
        x,
        arsinh_x,
        F_std_x,
        {
            "step1_trace_s": str(step1_traces_xs["P-"]),
            "integrand_u": str(projector_integrals["P-"][0]),
        },
    )
    comp_I_P3 = compare_candidate(
        "I_P3",
        projector_integrals["P3"][1],
        x,
        arsinh_x,
        F_std_x,
        {
            "step1_trace_s": str(step1_traces_xs["P3"]),
            "integrand_u": str(projector_integrals["P3"][0]),
        },
    )

    integrals_list = [comp_ln_det_H, comp_I_P_plus, comp_I_P_minus, comp_I_P3]
    for item in integrals_list:
        print(
            f"Compare | {item['name']:8s} = {item['symbolic']:10s} | "
            f"diff_arsinh = {item['difference_from_arsinh']:28s} | "
            f"diff_F_std = {item['difference_from_F_std']}"
        )
        for pt_lbl, nd in item["numerical_absolute_differences"].items():
            print(
                f"  x = {pt_lbl:>3s}: val = {nd['value']:+.12f} | "
                f"|val - arsinh| = {nd['abs_diff_from_arsinh']:.12f} | "
                f"|val - F_std| = {nd['abs_diff_from_F_std']:.12f}"
            )

    # =========================================================================
    # STEP 3: PRE-REGISTERED GELFAND-YAGLOM RATIO FOR L = d/du + A(u) ON [0, x]
    # =========================================================================
    gy_convention = (
        "Under the initial-value Cauchy Gelfand-Yaglom convention where Y(u) solves "
        "(d/du + A(u)) Y(u) = 0 with Y(0) = I and Y_free(u) solves (d/du) Y_free(u) = 0 "
        "with Y_free(0) = I on [0, x], the functional determinant ratio "
        "det(d/du + A) / det(d/du) equals det(H_free(x))^(-1) * det(H(x))."
    )
    print(f"Step 3 convention: {gy_convention}")

    H_free_mat = sp.zeros(2, 2).exp()  # exp(-int_0^x 0 du) = I_2
    assert H_free_mat == I2
    det_H_free = simplify_hyp(H_free_mat.det())
    gy_ratio_expr = simplify_hyp((det_H_free ** (-1)) * det_H)
    ln_gy_ratio_expr = simplify_hyp(sp.log(gy_ratio_expr))

    gy_comparison = compare_candidate(
        "ln_gelfand_yaglom_ratio",
        ln_gy_ratio_expr,
        x,
        arsinh_x,
        F_std_x,
    )
    print(
        f"Step 3 | det H_free(x) = {det_H_free}, det H(x) = {det_H}, "
        f"GY ratio = {gy_ratio_expr}, ln(GY ratio) = {ln_gy_ratio_expr}"
    )

    gelfand_yaglom_record = {
        "operator": "L = d/du + A(u), u in [0, x], Y(0) = I",
        "convention": gy_convention,
        "H_free_matrix": [[str(H_free_mat[i, j]) for j in range(2)] for i in range(2)],
        "H_matrix": [[str(H_mat[i, j]) for j in range(2)] for i in range(2)],
        "det_H_free": str(det_H_free),
        "det_H": str(det_H),
        "ratio": str(gy_ratio_expr),
        "ln_ratio": str(ln_gy_ratio_expr),
        "ln_ratio_comparison": gy_comparison,
    }

    # =========================================================================
    # VERDICT & matches_F_std GATE
    # =========================================================================
    first_passes = comp_ln_det_H["matches_arsinh"]
    second_passes = (
        (not first_passes)
        and comp_I_P_plus["matches_arsinh"]
        and identity_not_derivation
    )

    if first_passes:
        verdict = "unprojected determinant equals arsinh"
        matches_F_std = bool(comp_ln_det_H["matches_F_std"])
    elif second_passes:
        verdict = "chiral projection reproduces arsinh only as the Maurer-Cartan identity"
        matches_F_std = bool(comp_I_P_plus["matches_F_std"])
    else:
        verdict = "neither equals arsinh"
        matches_F_std = False

    print(f"matches_F_std: {json.dumps(matches_F_std)}")
    print(f"verdict: {verdict}")

    receipt = {
        "verdict": verdict,
        "A_simplified": A_simplified_record,
        "step1_algebra": {
            "tr_P_plus_A": str(step1_traces_xs["P+"]),
            "tr_P_minus_A": str(step1_traces_xs["P-"]),
            "tr_P3_A": str(step1_traces_xs["P3"]),
            "tr_P_plus_sigma1": str(tr_P_plus_sigma1),
            "commutator_A_u1_A_u2": [[str(commutator_A[i, j]) for j in range(2)] for i in range(2)],
        },
        "identity_not_derivation": identity_not_derivation,
        "ln_det_H": {
            "H_matrix": [[str(H_mat[i, j]) for j in range(2)] for i in range(2)],
            "det_H": str(det_H),
            "symbolic": str(ln_det_H),
            "difference_from_arsinh": comp_ln_det_H["difference_from_arsinh"],
            "difference_from_F_std": comp_ln_det_H["difference_from_F_std"],
            "numerical_absolute_differences": comp_ln_det_H["numerical_absolute_differences"],
        },
        "integrals": [
            {
                "name": item["name"],
                "symbolic": item["symbolic"],
                "difference_from_arsinh": item["difference_from_arsinh"],
                "difference_from_F_std": item["difference_from_F_std"],
                "numerical_absolute_differences": item["numerical_absolute_differences"],
            }
            for item in integrals_list
        ],
        "gelfand_yaglom_ratio": gelfand_yaglom_record,
        "matches_F_std": matches_F_std,
    }

    receipt_path = pathlib.Path(__file__).with_suffix(".json")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
