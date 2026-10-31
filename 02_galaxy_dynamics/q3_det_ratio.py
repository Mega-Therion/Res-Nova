#!/usr/bin/env python3
"""
Q3 Canonical Determinant-Ratio Audit (q3_det_ratio.py):
Tests whether a canonical matrix operator built solely from x and s = sqrt(1 + x^2)
(without inserting t = x + s or transcendental functions) satisfies
  ln(det M(x) / det M(1)) = c_rat * (arsinh(x) - arsinh(1))
for a pre-declared rational constant c_rat.
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


def evaluate_operator(
    name: str,
    mat_xs: sp.Matrix,
    x_sym: sp.Symbol,
    s_sym: sp.Symbol,
    c_rat: sp.Rational,
    extra_meta: dict | None = None,
) -> dict:
    """Compute symbolic determinant modulo s^2=1+x^2, ratio at x_ref=1, and numerical checks."""
    det_raw = mat_xs.det()
    det_simp = reduce_s2(det_raw, x_sym, s_sym)

    # Substitute s = sqrt(1 + x^2) for exact real-branch symbolic & numerical checks
    s_real = sp.sqrt(1 + x_sym**2)
    det_x = sp.simplify(det_simp.subs(s_sym, s_real))

    if det_x == 0:
        entry = {
            "name": name,
            "det_simplified": "0",
            "ratio": None,
            "symbolic_match": False,
            "numerical_differences": None,
        }
        if extra_meta:
            entry.update(extra_meta)
        return entry

    det_at_1 = sp.simplify(det_x.subs(x_sym, 1))
    if det_at_1 == 0:
        entry = {
            "name": name,
            "det_simplified": str(det_simp),
            "ratio": None,
            "det_at_x_ref_1_is_zero": True,
            "symbolic_match": False,
            "numerical_differences": None,
        }
        if extra_meta:
            entry.update(extra_meta)
        return entry

    ratio_expr = sp.simplify(det_x / det_at_1)
    target_expr = c_rat * (sp.asinh(x_sym) - sp.asinh(sp.Integer(1)))
    symbolic_diff = sp.simplify(
        (sp.log(ratio_expr) - target_expr).rewrite(sp.log)
    )
    is_symbolic_zero = bool(symbolic_diff == 0)

    test_points = [sp.Rational(1, 10), sp.Integer(1), sp.Integer(3)]
    num_diffs = {}
    all_num_under_tol = True
    for pt in test_points:
        ln_R_val = float(sp.N(sp.log(ratio_expr.subs(x_sym, pt)), 30))
        target_val = float(sp.N(target_expr.subs(x_sym, pt), 30))
        abs_diff = abs(ln_R_val - target_val)
        if abs_diff >= 1e-10:
            all_num_under_tol = False
        num_diffs[str(float(pt)) if pt != 1 else "1"] = {
            "ln_R": ln_R_val,
            "arsinh_x_minus_arsinh_1": target_val,
            "abs_difference": abs_diff,
        }

    entry = {
        "name": name,
        "det_simplified": str(det_simp),
        "ratio": str(ratio_expr),
        "symbolic_match": bool(is_symbolic_zero and all_num_under_tol),
        "numerical_differences": num_diffs,
    }
    if extra_meta:
        entry.update(extra_meta)
    return entry


def main() -> int:
    x = sp.Symbol("x", real=True)
    s = sp.Symbol("s", positive=True, real=True)

    # Pre-declared constant rational factor before seeing any numbers:
    declared_c_rat = sp.Rational(1, 1)

    # =========================================================================
    # RULE 1: Inserted example [[1, -x], [1, s]] -> record and ignore
    # =========================================================================
    M_inserted = sp.Matrix([[1, -x], [1, s]])
    inserted_example_det = reduce_s2(M_inserted.det(), x, s)  # s + x = t

    # =========================================================================
    # RULE 2: Pre-registered operators (entries use only rational ops and s)
    # =========================================================================
    # 2.1 Boost matrix B(x) = [[s, x], [x, s]]
    B_mat = sp.Matrix([[s, x], [x, s]])

    # 2.2 Derivative dB/dx using ds/dx = x/s (no sqrt/arsinh/ln primitive inserted)
    dB_dx_mat = sp.Matrix([[x / s, 1], [1, x / s]])

    # 2.3 Companion matrix of P(t) = t^2 - 2*x*t - 1 = 0
    # Convention: for monic t^2 + c1*t + c0 = 0 (c1 = -2*x, c0 = -1), the Frobenius
    # companion matrix is C = [[0, -c0], [1, -c1]] = [[0, 1], [1, 2*x]], satisfying
    # det(lambda*I - C) = lambda^2 - 2*x*lambda - 1 and det(C) = (-1)^2 * c0 = c0 = -1.
    companion_convention = (
        "Frobenius companion matrix C = [[0, -c0], [1, -c1]] for monic t^2 + c1*t + c0 = 0 "
        "(c1 = -2*x, c0 = -1), giving C = [[0, 1], [1, 2*x]] with det(C) = +c0 = -1."
    )
    C_comp_mat = sp.Matrix([[0, 1], [1, 2 * x]])

    # 2.4 Gram / metric square G(x) = B(x)^T * B(x)
    G_mat = B_mat.T * B_mat

    preregistered_specs = [
        ("B(x) = [[s, x], [x, s]]", B_mat, None),
        ("dB/dx = [[x/s, 1], [1, x/s]]", dB_dx_mat, None),
        (
            "Companion(t^2 - 2*x*t - 1)",
            C_comp_mat,
            {"convention": companion_convention},
        ),
        ("G(x) = B(x)^T B(x)", G_mat, None),
    ]

    operators_results = [
        evaluate_operator(name, mat, x, s, declared_c_rat, meta)
        for name, mat, meta in preregistered_specs
    ]

    # =========================================================================
    # RULE 3: Coefficient-equating lemma in SymPy (no matrix picking)
    # =========================================================================
    # First verify how a general 2x2 matrix with entries in span_Q{1, x, s} reduces
    # modulo s^2 = 1 + x^2:
    al11, bt11, gm11 = sp.symbols("al11 bt11 gm11", rational=True)
    al12, bt12, gm12 = sp.symbols("al12 bt12 gm12", rational=True)
    al21, bt21, gm21 = sp.symbols("al21 bt21 gm21", rational=True)
    al22, bt22, gm22 = sp.symbols("al22 bt22 gm22", rational=True)
    M_qspan = sp.Matrix(
        [
            [al11 + bt11 * x + gm11 * s, al12 + bt12 * x + gm12 * s],
            [al21 + bt21 * x + gm21 * s, al22 + bt22 * x + gm22 * s],
        ]
    )
    det_qspan_red = sp.expand(reduce_s2(M_qspan.det(), x, s))
    # Collect in s^0 and s^1: det = (a + b*x + e_x2*x^2) + (c + d*x)*s, reducing to
    # a + b*x + c*s + d*x*s when e_x2 = (bt11*bt22 - bt12*bt21) + (gm11*gm22 - gm12*gm21) = 0.
    e_x2_expr = sp.Poly(det_qspan_red, s).nth(0).coeff(x, 2)

    a, b, c, d, C_const = sp.symbols("a b c d C", rational=True)
    cand_expr = a + b * x + c * s + d * x * s
    t_expr = x + s  # uniformizer t = x + sqrt(1 + x^2)

    # Since s = sqrt(1 + x^2) is quadratic irrational over Q(x), P(x) + Q(x)*s = 0
    # in Q[x, s]/(s^2 - 1 - x^2) iff P(x) == 0 and Q(x) == 0 as polynomials in x:
    diff_t = sp.Poly(sp.expand(cand_expr - t_expr), s)
    eqs_t = (
        sp.Poly(diff_t.nth(0), x).all_coeffs()
        + sp.Poly(diff_t.nth(1), x).all_coeffs()
    )
    sol_eq_t = sp.solve(eqs_t, [a, b, c, d], dict=True)
    assert sol_eq_t == [{a: 0, b: 1, c: 1, d: 0}]

    diff_Ct = sp.Poly(sp.expand(cand_expr - C_const * t_expr), s)
    eqs_Ct = (
        sp.Poly(diff_Ct.nth(0), x).all_coeffs()
        + sp.Poly(diff_Ct.nth(1), x).all_coeffs()
    )
    sol_eq_Ct = sp.solve(eqs_Ct, [a, b, c, d], dict=True)
    assert sol_eq_Ct == [{a: 0, b: C_const, c: C_const, d: 0}]

    coefficient_solution_set = {
        "basis": "a + b*x + c*s + d*x*s (on the x^2-vanishing locus e_x2 = 0 of span_Q{1, x, s}^{2x2})",
        "x2_locus_condition": f"{e_x2_expr} = 0",
        "equals_t": [{str(k): str(v) for k, v in sol.items()} for sol in sol_eq_t],
        "equals_C_times_t": [
            {str(k): str(v) for k, v in sol.items()} for sol in sol_eq_Ct
        ],
        "nonempty": True,
        "changes_verdict": False,
    }

    # =========================================================================
    # RULE 5: One extra canonical operator defined in one sentence using only
    #         B(x), inverse, derivative, and matrix multiplication
    # =========================================================================
    extra_definition = (
        "The left-invariant Maurer-Cartan matrix B(x)^(-1) * (dB/dx) of B(x), "
        "built from the inverse of B(x) = (1/(s^2 - x^2)) * adj(B(x)) and dB/dx."
    )
    # Compute B(x)^(-1) via adjugate / det = [[s, -x], [-x, s]] / (s^2 - x^2):
    B_adj = B_mat.adjugate()
    B_inv = sp.Matrix(
        2,
        2,
        lambda i, j: reduce_s2(B_adj[i, j] / reduce_s2(B_mat.det(), x, s), x, s),
    )
    M_extra_raw = B_inv * dB_dx_mat
    M_extra = sp.Matrix(2, 2, lambda i, j: reduce_s2(M_extra_raw[i, j], x, s))

    extra_operator_result = evaluate_operator(
        "M_MC(x) = B(x)^(-1) * (dB/dx)",
        M_extra,
        x,
        s,
        declared_c_rat,
        {"definition": extra_definition, "entries_simplified": str(M_extra.tolist())},
    )

    # =========================================================================
    # VERDICT EVALUATION & NUMERICAL PRINTOUT (RULE 4 + VERDICT RULE)
    # =========================================================================
    tested_all = operators_results + [extra_operator_result]
    any_canonical_match = any(op["symbolic_match"] for op in tested_all)

    if any_canonical_match:
        verdict = "determinant equals arsinh"
    else:
        verdict = "determinant does not equal arsinh"

    print(verdict)
    for op in tested_all:
        if op["numerical_differences"] is None:
            continue
        print(f"operator: {op['name']} | det = {op['det_simplified']} | R(x) = {op['ratio']}")
        for x_label, vals in op["numerical_differences"].items():
            print(
                f"  x = {x_label:>3s}: ln(R(x)) = {vals['ln_R']:+.12f}, "
                f"arsinh(x)-arsinh(1) = {vals['arsinh_x_minus_arsinh_1']:+.12f}, "
                f"|diff| = {vals['abs_difference']:.12f}"
            )

    receipt = {
        "verdict": verdict,
        "declared_rational_factor": str(declared_c_rat),
        "inserted_example": {
            "matrix": "[[1, -x], [1, s]]",
            "det": str(inserted_example_det),
        },
        "inserted_example_det": str(inserted_example_det),
        "operators": [
            {
                "name": op["name"],
                "det_simplified": op["det_simplified"],
                "ratio": op["ratio"],
                "numerical_differences": op["numerical_differences"],
                **({"convention": op["convention"]} if "convention" in op else {}),
            }
            for op in operators_results
        ],
        "coefficient_solution_set": coefficient_solution_set,
        "extra_operator": {
            "name": extra_operator_result["name"],
            "definition": extra_operator_result["definition"],
            "entries_simplified": extra_operator_result["entries_simplified"],
            "det_simplified": extra_operator_result["det_simplified"],
            "ratio": extra_operator_result["ratio"],
            "numerical_differences": extra_operator_result["numerical_differences"],
        },
    }

    receipt_path = pathlib.Path(__file__).with_suffix(".json")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
