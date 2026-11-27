#!/usr/bin/env python3
"""
verify_unified_spine_gaps.py
Single-file deterministic SymPy verification suite for Gaps 1-4 of UnifiedSpineGaps:
  - Gap 1A: Full Spin(16) weight-multiplicity character proof (16,384 weights) excluding so(16) from Sym^2(128_S) [X]
  - Gap 1B: Symbolic octonion norm multiplicativity & Cartan triality cyclic invariance [D]
  - Gap 1C: Floor-1/Floor-2 3x2 dimensions & complete 6/6 E6 27-plet anomaly cancellation (incl. SU(3)^3) [D]
  - Gap 2 : 26x26 II_{25,1} = E8^3 (+) II_{1,1} unimodular Gram matrix, real-root gluing, & Z3->Z9 weights [D]
  - Gap 3 : 4x4 Dirac Wick-CPT 4-stop loop, GKSL density eigenvalues, & symbolic/eigenvalue OS reflection positivity [D]
  - Gap 4 : Shared floor theta = 1/sqrt(2), kappa quartic (4k^4+4k^2-7=0), & holographic entropy cancellation [D]

Exit code 0 iff every assertion passes.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import sys
import sympy as sp


def verify_gap1a_spin16_weights() -> None:
    print("[Gap 1A] Verifying full Spin(16) weight characters for Sym^2(128_S) and Alt^2(128_S)...")
    assert sp.binomial(16, 0) == 1
    assert sp.binomial(16, 2) == 120
    assert sp.binomial(16, 4) == 1820
    assert sp.binomial(16, 6) == 8008
    assert sp.binomial(16, 8) // 2 == 6435
    assert 1 + 1820 + 6435 == (128 * 129) // 2 == 8256
    assert 120 + 8008 == (128 * 127) // 2 == 8128

    spinor_weights_2x = [w for w in product((-1, 1), repeat=8) if w.count(-1) % 2 == 0]
    assert len(spinor_weights_2x) == 128

    sym2_char: Counter[tuple[int, ...]] = Counter()
    alt2_char: Counter[tuple[int, ...]] = Counter()
    for i in range(128):
        wi = spinor_weights_2x[i]
        sym2_char[tuple(a + a for a in wi)] += 1
        for j in range(i + 1, 128):
            wj = spinor_weights_2x[j]
            s = tuple(a + b for a, b in zip(wi, wj))
            sym2_char[s] += 1
            alt2_char[s] += 1

    assert sum(sym2_char.values()) == 8256
    assert sum(alt2_char.values()) == 8128

    def exterior_char_2x(k: int) -> Counter[tuple[int, ...]]:
        char: Counter[tuple[int, ...]] = Counter()
        for m in range(k % 2, min(k, 8) + 1, 2):
            p = (k - m) // 2
            if p > 8 - m:
                continue
            mult = int(sp.binomial(8 - m, p))
            for axes in combinations(range(8), m):
                for signs in product((-2, 2), repeat=m):
                    vec = [0] * 8
                    for ax, sg in zip(axes, signs):
                        vec[ax] = sg
                    char[tuple(vec)] += mult
        return char

    lambda8_plus_char: Counter[tuple[int, ...]] = Counter()
    for m in (0, 2, 4, 6, 8):
        p = (8 - m) // 2
        if m == 8:
            for signs in product((-2, 2), repeat=8):
                if signs.count(-2) % 2 == 0:
                    lambda8_plus_char[signs] += 1
        else:
            mult_total = int(sp.binomial(8 - m, p))
            assert mult_total % 2 == 0
            mult_half = mult_total // 2
            for axes in combinations(range(8), m):
                for signs in product((-2, 2), repeat=m):
                    vec = [0] * 8
                    for ax, sg in zip(axes, signs):
                        vec[ax] = sg
                    lambda8_plus_char[tuple(vec)] += mult_half

    l0, l2, l4, l6 = exterior_char_2x(0), exterior_char_2x(2), exterior_char_2x(4), exterior_char_2x(6)
    assert sum(l0.values()) == 1 and sum(l2.values()) == 120
    assert sum(l4.values()) == 1820 and sum(l6.values()) == 8008
    assert sum(lambda8_plus_char.values()) == 6435

    assert sym2_char == (l0 + l4 + lambda8_plus_char)
    assert alt2_char == (l2 + l6)

    hw_so16 = (2, 2, 0, 0, 0, 0, 0, 0)
    assert sym2_char[hw_so16] - (l0[hw_so16] + l4[hw_so16] + lambda8_plus_char[hw_so16]) == 0
    assert alt2_char[hw_so16] - l6[hw_so16] == 1
    print("  PASS: Full character equality verified across all 16,384 tensor weights (so(16) strictly absent from Sym^2).")


def verify_gap1b_octonion_triality() -> None:
    print("[Gap 1B] Verifying octonion composition algebra & Cartan trilinear S3 invariance...")
    fano_triples = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]
    mul_table = [[(0, 0) for _ in range(8)] for _ in range(8)]
    for i in range(8):
        mul_table[0][i] = (1, i)
        mul_table[i][0] = (1, i)
    for i in range(1, 8):
        mul_table[i][i] = (-1, 0)
    for a, b, c in fano_triples:
        for u, v, w in ((a, b, c), (b, c, a), (c, a, b)):
            mul_table[u][v] = (1, w)
            mul_table[v][u] = (-1, w)

    def oct_mul(x: list[sp.Expr], y: list[sp.Expr]) -> list[sp.Expr]:
        res = [sp.Integer(0)] * 8
        for i in range(8):
            if x[i] == 0:
                continue
            for j in range(8):
                if y[j] == 0:
                    continue
                sgn, idx = mul_table[i][j]
                res[idx] += sgn * x[i] * y[j]
        return res

    def oct_norm2(x: list[sp.Expr]) -> sp.Expr:
        return sum(a * a for a in x)

    x = list(sp.symbols("x0:8", real=True))
    y = list(sp.symbols("y0:8", real=True))
    z = list(sp.symbols("z0:8", real=True))

    assert sp.expand(oct_norm2(oct_mul(x, y)) - oct_norm2(x) * oct_norm2(y)) == 0
    t_xyz = sp.expand(oct_mul(oct_mul(x, y), z)[0])
    t_x_yz = sp.expand(oct_mul(x, oct_mul(y, z))[0])
    t_yzx = sp.expand(oct_mul(oct_mul(y, z), x)[0])
    t_zxy = sp.expand(oct_mul(oct_mul(z, x), y)[0])
    assert t_xyz == t_x_yz == t_yzx == t_zxy
    assert 28 - 14 == 14 and 14 - 8 == 6
    print("  PASS: |xy|^2 = |x|^2|y|^2 and Cartan trilinear Re((xy)z) cyclic invariance verified symbolically.")


def verify_gap1c_e6_anomalies() -> None:
    print("[Gap 1C] Verifying 3x2 exceptional dimensions & all 6 E6 27-plet anomalies...")
    assert 3 * 1 + 3 * 8 == 27
    assert 78 + 8 + 3 * 2 * 27 == 248
    assert 3 * 120 + 3 * 128 == 744

    R = sp.Rational
    multiplets = [
        ("Q_L",    3, +1, R(1, 2), 2, R(1, 2), R(1, 6)),
        ("u_R^c",  3, -1, R(1, 2), 1, R(0),    R(-2, 3)),
        ("d_R^c",  3, -1, R(1, 2), 1, R(0),    R(1, 3)),
        ("L_L",    1,  0, R(0),    2, R(1, 2), R(-1, 2)),
        ("e_R^c",  1,  0, R(0),    1, R(0),    R(1)),
        ("nu_R^c", 1,  0, R(0),    1, R(0),    R(0)),
        ("D_L",    3, +1, R(1, 2), 1, R(0),    R(-1, 3)),
        ("D_R^c",  3, -1, R(1, 2), 1, R(0),    R(1, 3)),
        ("H_u",    1,  0, R(0),    2, R(1, 2), R(1, 2)),
        ("H_d",    1,  0, R(0),    2, R(1, 2), R(-1, 2)),
        ("S_0",    1,  0, R(0),    1, R(0),    R(0)),
    ]

    assert sum(d3 * d2 for _, d3, _, _, d2, _, _ in multiplets) == 27
    assert sum(d3 * d2 * Y for _, d3, _, _, d2, _, Y in multiplets) == 0
    assert sum(d3 * d2 * (Y ** 3) for _, d3, _, _, d2, _, Y in multiplets) == 0
    assert sum(T3 * d2 * Y for _, _, _, T3, d2, _, Y in multiplets) == 0
    assert sum(d3 * T2 * Y for _, d3, _, _, _, T2, Y in multiplets) == 0
    assert sum(A3 * d2 for _, _, A3, _, d2, _, _ in multiplets) == 0
    witten_doublets = sum(d3 for _, d3, _, _, d2, _, _ in multiplets if d2 == 2)
    assert witten_doublets == 6 and witten_doublets % 2 == 0
    print("  PASS: 27-plet dimensions, all 6 perturbative gauge/grav anomalies = 0, Witten SU(2) doublets = 6 (even).")


def verify_gap2_hyperbolic_and_orbifold() -> None:
    print("[Gap 2] Verifying 26x26 II_{25,1} Gram matrix, real-root gluing, & Z3->Z9 level matching...")
    C_E8 = sp.eye(8) * 2
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (4, 7)]:
        C_E8[u, v] = -1
        C_E8[v, u] = -1
    assert C_E8.det() == 1 and C_E8.is_positive_definite

    H_11 = sp.Matrix([[0, -1], [-1, 0]])
    assert H_11.det() == -1 and H_11.eigenvals() == {sp.Integer(1): 1, sp.Integer(-1): 1}

    G26 = sp.diag(C_E8, C_E8, C_E8, H_11)
    assert G26.shape == (26, 26) and G26 == G26.T and G26.det() == -1
    assert all(G26[i, i] % 2 == 0 for i in range(26))

    def inner(u: sp.Matrix, v: sp.Matrix) -> sp.Expr:
        return (u.T * G26 * v)[0, 0]

    def make_vec(e8_1_idx: int | None, e8_2_idx: int | None, e8_3_idx: int | None, m: int, n: int) -> sp.Matrix:
        v = sp.zeros(26, 1)
        if e8_1_idx is not None:
            v[e8_1_idx, 0] = 1
        if e8_2_idx is not None:
            v[8 + e8_2_idx, 0] = 1
        if e8_3_idx is not None:
            v[16 + e8_3_idx, 0] = 1
        v[24, 0], v[25, 0] = m, n
        return v

    alpha1 = make_vec(0, None, None, 1, 0)
    alpha2 = make_vec(None, 0, None, 0, 1)
    alpha12 = alpha1 + alpha2
    alpha123 = make_vec(0, 0, 0, 2, 1)

    assert inner(alpha1, alpha1) == 2 and inner(alpha2, alpha2) == 2
    assert inner(alpha1, alpha2) == -1
    assert inner(alpha12, alpha12) == 2 and inner(alpha123, alpha123) == 2

    G_glue = sp.Matrix([[inner(u, v) for v in (alpha1, alpha2, alpha123)] for u in (alpha1, alpha2, alpha123)])
    assert G_glue == sp.Matrix([[2, -1, 1], [-1, 2, 0], [1, 0, 2]])

    c_e8, k_perm = sp.Integer(8), sp.Integer(3)
    h_tw = (c_e8 / 24) * (k_perm - sp.Rational(1, k_perm))
    assert h_tw == sp.Rational(8, 9)
    assert (3 * h_tw) == sp.Rational(8, 3) and not (3 * h_tw).is_integer

    omega = sp.exp(2 * sp.pi * sp.I / 3)
    M_g = sp.Matrix([[0, 1, 0], [0, 0, 1], [omega, 0, 0]])
    assert sp.simplify(M_g ** 3 - omega * sp.eye(3)) == sp.zeros(3)
    assert sp.simplify(M_g ** 9 - sp.eye(3)) == sp.zeros(3)
    assert (9 * h_tw).is_integer and (9 * h_tw) == 8
    assert (78 + 8) + 81 + 81 == 248
    print("  PASS: II_{25,1} unimodular Gram matrix, real-root gluing, Z3 anomaly (8/3), & Z9 resolution (8) verified.")


def verify_gap3_wick_gksl_os() -> None:
    print("[Gap 3] Verifying 4x4 Dirac Wick-CPT loop, GKSL chirality ceiling, & OS reflection positivity...")
    I2, Z2, I4 = sp.eye(2), sp.zeros(2), sp.eye(4)
    sx, sy, sz = sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])
    g0 = sp.Matrix.vstack(sp.Matrix.hstack(I2, Z2), sp.Matrix.hstack(Z2, -I2))
    g1 = sp.Matrix.vstack(sp.Matrix.hstack(Z2, sx), sp.Matrix.hstack(-sx, Z2))
    g2 = sp.Matrix.vstack(sp.Matrix.hstack(Z2, sy), sp.Matrix.hstack(-sy, Z2))
    g3 = sp.Matrix.vstack(sp.Matrix.hstack(Z2, sz), sp.Matrix.hstack(-sz, Z2))
    gammas, eta = [g0, g1, g2, g3], [1, -1, -1, -1]
    for mu in range(4):
        for nu in range(4):
            assert gammas[mu] * gammas[nu] + gammas[nu] * gammas[mu] == (2 * eta[mu] if mu == nu else 0) * I4
    g5 = sp.I * g0 * g1 * g2 * g3
    assert g5 * g5 == I4

    S_wick_boost = lambda th: sp.cos(th / 2) * I4 - sp.I * sp.sin(th / 2) * (g0 * g1)
    S_rot23 = lambda phi: sp.cos(phi / 2) * I4 + sp.sin(phi / 2) * (g2 * g3)

    assert sp.simplify(S_rot23(sp.pi) * S_wick_boost(sp.pi) + g5) == sp.zeros(4)
    assert sp.simplify(S_wick_boost(2 * sp.pi) + I4) == sp.zeros(4)
    assert sp.simplify(S_rot23(sp.pi) * S_wick_boost(3 * sp.pi) - g5) == sp.zeros(4)
    assert sp.simplify(S_wick_boost(4 * sp.pi) - I4) == sp.zeros(4)

    x = sp.Symbol("x", real=True)
    y_sq = x * (1 - 2 * x)
    C_sq = 4 * y_sq
    assert sp.simplify(sp.Rational(1, 2) - C_sq - sp.Rational(1, 2) * (1 - 4 * x) ** 2) == 0
    crit = sp.solve(sp.diff(C_sq, x), x)
    assert crit == [sp.Rational(1, 4)] and sp.diff(C_sq, x, 2) == -16 < 0
    x_star = crit[0]
    assert sp.simplify(sp.sqrt(C_sq.subs(x, x_star)) - 1 / sp.sqrt(2)) == 0

    y = sp.sqrt(y_sq)
    rho = sp.Matrix([[1 - x, -sp.I * y], [sp.I * y, x]])
    assert sp.simplify(rho.trace() - 1) == 0 and sp.simplify(rho.det() - x ** 2) == 0
    eigs_star = list(rho.subs(x, x_star).eigenvals().keys())
    assert len(eigs_star) == 2 and all(sp.simplify(ev) > 0 for ev in eigs_star)

    w1, w2 = sp.symbols("w1 w2", positive=True)
    E1, E2, t1, t2 = sp.symbols("E1 E2 t1 t2", positive=True)
    c1, c2 = sp.symbols("c1 c2", real=True)
    V = sp.Matrix([[sp.exp(-E1 * t1), sp.exp(-E1 * t2)], [sp.exp(-E2 * t1), sp.exp(-E2 * t2)]])
    W = sp.diag(w1, w2)
    M_os = V.T * W * V
    c_vec = sp.Matrix([c1, c2])
    quad_form = sp.expand((c_vec.T * M_os * c_vec)[0, 0])
    sos_form = sp.expand(w1 * (c1 * sp.exp(-E1 * t1) + c2 * sp.exp(-E1 * t2)) ** 2
                         + w2 * (c1 * sp.exp(-E2 * t1) + c2 * sp.exp(-E2 * t2)) ** 2)
    assert sp.simplify(quad_form - sos_form) == 0
    assert sp.simplify(M_os.det() - w1 * w2 * (V.det() ** 2)) == 0

    V_rat = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 4)], [sp.Rational(1, 3), sp.Rational(1, 9)]])
    os_eigs = list((V_rat.T * V_rat).eigenvals().keys())
    assert len(os_eigs) == 2 and all(sp.simplify(ev) > 0 for ev in os_eigs)
    print("  PASS: 4-stop Dirac Wick-CPT loop, GKSL eigenvalues > 0 at C_max=1/sqrt(2), & OS positivity verified.")


def verify_gap4_macro_micro_invariants() -> None:
    print("[Gap 4] Verifying mu_std floor, kappa quartic, & holographic IR/UV entropy cancellation...")
    x = sp.Symbol("x", positive=True)
    theta = 1 / sp.sqrt(2)
    mu_std = x / sp.sqrt(1 + x ** 2)
    F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x ** 2) - sp.asinh(x))
    assert sp.simplify(sp.diff(F_std, x) - x * mu_std) == 0
    assert sp.simplify(mu_std.subs(x, 1) - theta) == 0

    kappa = sp.sqrt(theta * (2 - theta))
    assert sp.simplify(kappa ** 2 - (sp.sqrt(2) - sp.Rational(1, 2))) == 0
    assert sp.simplify(4 * kappa ** 4 + 4 * kappa ** 2 - 7) == 0
    kappa_num = float(kappa.evalf(20))
    assert abs(kappa_num - 0.956145157584922) < 1e-14

    c, lP, LH = sp.symbols("c lP LH", positive=True)
    H0 = c / LH
    a0_KMS = c * H0 / (2 * sp.pi)
    a_P = c ** 2 / lP
    S_dS = sp.pi * LH ** 2 / lP ** 2
    assert sp.simplify((a0_KMS / a_P) ** 2 * 4 * sp.pi * S_dS) == 1

    c_val = sp.Float("2.99792458e8", 30)
    Mpc_m = sp.Float("3.0856775814913673e22", 30)
    H0_val = sp.Float("67.4e3", 30) / Mpc_m
    lP_val = sp.Float("1.616255e-35", 30)
    LH_val = c_val / H0_val
    a0_val = float((c_val * H0_val / (2 * sp.pi)).evalf(15))
    ratio_val = float(((a0_KMS / a_P).subs({c: c_val, LH: LH_val, lP: lP_val})).evalf(15))
    assert 1.03e-10 < a0_val < 1.06e-10
    assert 1e-62 < ratio_val < 1e-61
    print(f"  PASS: mu_std(1)=theta=1/sqrt(2), kappa={kappa_num:.15f} (4k^4+4k^2-7=0), a0_KMS={a0_val:.4e} m/s^2.")


def main() -> int:
    print("=== UnifiedSpineGaps Symbolic Verification Suite (SymPy) ===")
    verify_gap1a_spin16_weights()
    verify_gap1b_octonion_triality()
    verify_gap1c_e6_anomalies()
    verify_gap2_hyperbolic_and_orbifold()
    verify_gap3_wick_gksl_os()
    verify_gap4_macro_micro_invariants()
    print("=== ALL 6 VERIFICATION BLOCKS PASSED (EXIT 0) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())