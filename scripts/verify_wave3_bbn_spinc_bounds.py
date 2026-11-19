#!/usr/bin/env python3
"""
Symbolic and exact-integer verification companion for:
  Res-Nova/05_lean_formalization/Wave3BBNAndSpinCCP2Bounds.lean

Verifies [P]/[D]:
  1. Pure uncoupled AeST (TARGET_D7) BBN ratio G_cosmo/G_N = lam*(2-K_B)/[2*(1+lam)]
     vs AeSTTotalScalarCorrespondence non-folding window lam < (27 + 12*sqrt(6))/5:
       - 5% BBN bound forces lam >= 19 (excluding J_tot non-folding).
       - 10% BBN bound caps K_B < 0.041 (exact sharp max 0.0404082...).
  2. Spin^c CP^2 x E8 -> E6 x SU(3)_f -> SO(10) x U(1)_psi (+ SU(5) x U(1)_chi):
       - Shifted triplet sum ind(Q+q_i) = 3*ind(Q) + (2*Q+3)/2*(q1+q2+q3) + 1/2*(q1^2+q2^2+q3^2).
       - Zero-sum SU(3)_f twist (q1+q2+q3=0) forces sum ind(1+q_i) >= 9 (>= 10 nontrivial).
       - Unique symmetric 3-gen compensating bundle q in {-4, -1}.
       - Chiral excess ind(Q0+x) - ind(Q0-x) = (2*Q0+3)*x vs single-operator shift
         ind(Q0+x) = ind(Q0) + (2*Q0+3)*x/2 + x^2/2.
       - Full E8 248 (16 and SU(5) 10) excess = (2*Q0+3)*(q1+q2+q3), vanishing iff q1+q2+q3=0.
       - Matter-sector (27,3) net=+/-3 traceless locus iff
         (Q0, k_psi, Q0 - 2*k_psi) in {(-2,-1,0), (-2,1,-4), (-1,-1,1), (-1,1,-3)},
         retaining ind_10_per_color in {1, 3} (>= 3 light 10-plets).
       - Distinct traceless SU(3)_f weights never cancel all three (10,3) colors (sum ind >= 3);
         traceful cancellation at (Q0 in {-1,-2}, k_psi in {1,-1}) forces |tr| >= 3,
         |net_248| >= 3, and |net_27| >= 6; over all Z^5, (net_27=+-3 & all 10s vanish) iff
         (Q0, k_psi, q1, q2, q3) in {(-2, 0, 1, 1, 1), (-1, 0, -1, -1, -1)}.
       - L1/L2 boundary: single-multiplet ind(Q)=3 iff Q in {1, -4} (Q0=0 triplet gives 9*k_psi,
         never +-3; Gate 2 locus has Q0 != 0 and Q0 +- k_psi in {-3,-2,-1,0}, disjoint from {1,-4}).
"""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp


def main() -> int:
    lam, kb, delta = sp.symbols("lambda_s K_B delta", positive=True)
    g_ratio = lam * (2 - kb) / (2 * (1 + lam))
    assert sp.simplify(sp.diff(g_ratio, kb) + lam / (2 * (1 + lam))) == 0
    lam_min = sp.simplify(sp.solve(sp.Eq(lam / (1 + lam), 1 - delta), lam)[0])
    assert sp.simplify(lam_min - (1 - delta) / delta) == 0
    assert float(lam_min.subs(delta, sp.Rational(1, 20))) == 19.0

    lam_max_exact = (27 + 12 * sp.sqrt(6)) / 5
    poly_eq = sp.expand(27 * (1 + lam) ** 2 - 32 * lam**2)
    assert sp.simplify(poly_eq + (5 * lam**2 - 54 * lam - 27)) == 0
    assert float(lam_max_exact) < 11.3
    kb_max_10 = float(sp.solve(sp.Eq(g_ratio, sp.Rational(9, 10)), kb)[0].subs(lam, lam_max_exact))
    assert 0.0404 < kb_max_10 < 0.041

    q_sym, q0, x, kp, kc, q1, q2, q3 = sp.symbols("Q Q0 x k_psi k_chi q1 q2 q3", integer=True)
    ind = lambda q: sp.Rational(1, 2) * (q + 1) * (q + 2)
    twice = lambda q: (q + 1) * (q + 2)

    assert sp.simplify(ind(-3 - q1) - ind(q1)) == 0
    assert sp.simplify(
        ind(q_sym + q1)
        + ind(q_sym + q2)
        + ind(q_sym + q3)
        - (3 * ind(q_sym) + sp.Rational(1, 2) * (2 * q_sym + 3) * (q1 + q2 + q3) + sp.Rational(1, 2) * (q1**2 + q2**2 + q3**2))
    ) == 0
    assert sp.simplify(
        ind(1 + q1)
        + ind(1 + q2)
        + ind(1 + q3)
        - (9 + sp.Rational(5, 2) * (q1 + q2 + q3) + sp.Rational(1, 2) * (q1**2 + q2**2 + q3**2))
    ) == 0
    assert sp.simplify((ind(q0 + x) - ind(q0 - x)) - (2 * q0 + 3) * x) == 0
    assert sp.simplify(twice(q0 + x) - (twice(q0) + (2 * q0 + 3) * x + x**2)) == 0

    # Full E8 248 traceful chiral 16 excess and SU(5) 10-plet excess (NO tracelessness assumed)
    tot_248_16_traceful = (
        (ind(q0 + kp + q1) - ind(q0 - kp - q1))
        + (ind(q0 + kp + q2) - ind(q0 - kp - q2))
        + (ind(q0 + kp + q3) - ind(q0 - kp - q3))
        + (ind(q0 - 3 * kp) - ind(q0 + 3 * kp))
    )
    assert sp.simplify(tot_248_16_traceful - (2 * q0 + 3) * (q1 + q2 + q3)) == 0

    tot_248_10_traceful = (
        (ind(q0 + (kp - kc + q1)) - ind(q0 - (kp - kc + q1)))
        + (ind(q0 + (kp - kc + q2)) - ind(q0 - (kp - kc + q2)))
        + (ind(q0 + (kp - kc + q3)) - ind(q0 - (kp - kc + q3)))
        + (ind(q0 + (-3 * kp - kc)) - ind(q0 - (-3 * kp - kc)))
        + (ind(q0 + 4 * kc) - ind(q0 - 4 * kc))
    )
    assert sp.simplify(tot_248_10_traceful - (2 * q0 + 3) * (q1 + q2 + q3)) == 0

    # Under traceless SU(3)_f (q3 = -(q1+q2)), both vanish identically; 2*Q0+3 is never 0 over Z
    q3_sub = -(q1 + q2)
    assert sp.simplify(tot_248_16_traceful.subs(q3, q3_sub)) == 0
    assert sp.simplify(tot_248_10_traceful.subs(q3, q3_sub)) == 0
    assert all(2 * v + 3 != 0 for v in range(-50, 51))

    # Matter-sector (27,3) net_16 and net_10 (general traceful and traceless)
    net_27_traceful = (
        (ind(q0 + kp + q1) - ind(q0 - kp - q1))
        + (ind(q0 + kp + q2) - ind(q0 - kp - q2))
        + (ind(q0 + kp + q3) - ind(q0 - kp - q3))
    )
    assert sp.simplify(net_27_traceful - (2 * q0 + 3) * (3 * kp + q1 + q2 + q3)) == 0
    assert sp.simplify(net_27_traceful.subs(q3, q3_sub) - 3 * (2 * q0 + 3) * kp) == 0

    net_27_10_traceful = (
        (ind(q0 - 2 * kp + q1) - ind(q0 + 2 * kp - q1))
        + (ind(q0 - 2 * kp + q2) - ind(q0 + 2 * kp - q2))
        + (ind(q0 - 2 * kp + q3) - ind(q0 + 2 * kp - q3))
    )
    assert sp.simplify(net_27_10_traceful - (2 * q0 + 3) * (-6 * kp + q1 + q2 + q3)) == 0

    # Exhaustive check of traceless (27,3) 4-point locus and exotic (10,3)_{-2} retention
    net3_solutions = []
    for q0_v in range(-12, 13):
        for kp_v in range(-10, 11):
            if 3 * (2 * q0_v + 3) * kp_v in (3, -3):
                q10 = q0_v - 2 * kp_v
                ind10 = int(ind(q10))
                assert ind10 in (1, 3)
                assert q0_v != 0
                assert (q0_v + kp_v) not in (1, -4) and (q0_v - kp_v) not in (1, -4)
                assert {int(ind(q0_v + kp_v)), int(ind(q0_v - kp_v))} == {0, 1}
                net3_solutions.append(
                    {
                        "Q0": q0_v,
                        "k_psi": kp_v,
                        "Q_10": q10,
                        "ind_10_per_color": ind10,
                        "total_ind_10_symmetric": 3 * ind10,
                        "Q_16_plus": q0_v + kp_v,
                        "Q_16_minus": q0_v - kp_v,
                    }
                )
    assert [(s["Q0"], s["k_psi"], s["Q_10"]) for s in net3_solutions] == [
        (-2, -1, 0),
        (-2, 1, -4),
        (-1, -1, 1),
        (-1, 1, -3),
    ]

    # Distinct traceless SU(3)_f weights on Gate 2 locus: sum ind(Q_10 + q_i) >= 3 (twiceInd >= 6)
    for sol in net3_solutions:
        q10_base = sol["Q_10"]
        for q1_v in range(-10, 11):
            for q2_v in range(-10, 11):
                q3_v = -(q1_v + q2_v)
                inds = [int(ind(q10_base + qi)) for qi in (q1_v, q2_v, q3_v)]
                assert sum(inds) >= 3
                assert any(v != 0 for v in inds)

    # Traceful cancellation at Q0 in {-2,-1}, k_psi in {-1,1}: always violates |tr|>=3, |net_248|>=3, |net_27|>=6
    traceful_cancel_violations = 0
    for q0_v in (-2, -1):
        for kp_v in (-1, 1):
            for q1_v in range(-6, 7):
                for q2_v in range(-6, 7):
                    for q3_v in range(-6, 7):
                        if all(int(ind(q0_v - 2 * kp_v + qi)) == 0 for qi in (q1_v, q2_v, q3_v)):
                            tr_v = q1_v + q2_v + q3_v
                            net248_v = (2 * q0_v + 3) * tr_v
                            net27_v = (2 * q0_v + 3) * (3 * kp_v + tr_v)
                            assert abs(tr_v) >= 3
                            assert abs(net248_v) >= 3
                            assert abs(net27_v) >= 6
                            traceful_cancel_violations += 1
    assert traceful_cancel_violations == 32  # 4 points * 2^3 choices of (-1 or -2) per color

    # Complete Z^5 box search: (net_27 == +-3 and all three (10,3) vanish) iff {(-2,0,1,1,1), (-1,0,-1,-1,-1)}
    traceful_27_net3_10_zero = []
    for q0_v in range(-8, 9):
        for kp_v in range(-5, 6):
            for q1_v in range(-6, 7):
                for q2_v in range(-6, 7):
                    for q3_v in range(-6, 7):
                        n16 = (2 * q0_v + 3) * (3 * kp_v + q1_v + q2_v + q3_v)
                        if n16 in (3, -3):
                            n10 = (2 * q0_v + 3) * (-6 * kp_v + q1_v + q2_v + q3_v)
                            assert n10 != 0
                            if all(int(ind(q0_v - 2 * kp_v + qi)) == 0 for qi in (q1_v, q2_v, q3_v)):
                                traceful_27_net3_10_zero.append(
                                    {
                                        "Q0": q0_v,
                                        "k_psi": kp_v,
                                        "q": [q1_v, q2_v, q3_v],
                                        "trace": q1_v + q2_v + q3_v,
                                        "net_27": n16,
                                        "net_248": (2 * q0_v + 3) * (q1_v + q2_v + q3_v),
                                    }
                                )
    assert [(x["Q0"], x["k_psi"], tuple(x["q"])) for x in traceful_27_net3_10_zero] == [
        (-2, 0, (1, 1, 1)),
        (-1, 0, (-1, -1, -1)),
    ]

    # Single-multiplet Dolan Q=1 vs Gate 2 Q0 boundary
    single_3gen_Q = [q for q in range(-20, 21) if int(ind(q)) == 3]
    assert single_3gen_Q == [-4, 1]
    assert int(ind(0 + 1)) == 3 and int(ind(0 - 2 * 1)) == 0 and int(ind(0 + 3 * 1)) == 10
    for kp_v in range(-10, 11):
        assert 9 * kp_v not in (3, -3)

    # Zero-sum SU(3)_f twist lower bound and symmetric 3-gen twists (sum ind = 3)
    for a in range(-12, 13):
        for b in range(-12, 13):
            c = -(a + b)
            s_ind = int(ind(1 + a) + ind(1 + b) + ind(1 + c))
            if (a, b, c) == (0, 0, 0):
                assert s_ind == 9
            else:
                assert s_ind >= 10
    sym_twists = [q for q in range(-20, 21) if int(3 * ind(1 + q)) == 3]
    assert sym_twists == [-4, -1]

    print("[PASS] Wave 3 BBN x J_tot exclusion and Safa BLK-1450/BLK-1477 E8 x CP^2 Spin^c Gate 2 checks passed")
    here = Path(__file__).resolve().parent
    bench = here.parent / "benchmarks" / "wave3_bbn_spinc_2026-11-17.json"
    bench.parent.mkdir(parents=True, exist_ok=True)
    bench.write_text(
        json.dumps(
            {
                "date": "2026-11-17",
                "lam_max_Jtot": float(lam_max_exact),
                "lam_min_BBN_5pct": 19.0,
                "max_KB_at_10pct_BBN": kb_max_10,
                "symmetric_3gen_twists": sym_twists,
                "matter_27_net3_solutions": net3_solutions,
                "e8_248_traceless_chiral_excess_identically_zero": True,
                "e8_248_traceful_twice_chiral_excess_formula": "2*(2*Q0+3)*(q1+q2+q3)",
                "traceful_27_net3_and_all_10_vanish_solutions": traceful_27_net3_10_zero,
                "traceful_gate2_locus_cancel10_witness_count": traceful_cancel_violations,
                "single_multiplet_ind3_charges": single_3gen_Q,
                "l1_l2_boundary_summary": {
                    "dolan_Q1_single_multiplet": {"Q0": 0, "Q": 1, "ind_16": 3, "ind_10": 0, "ind_singlet_1_16": 10},
                    "gate2_Q0_chiral_excess_Q0_zero_triplet_16": "9*k_psi (never +-3)",
                    "gate2_Q0_locus_16_charges_subset_of": [-3, -2, -1, 0],
                    "gate2_exotic_10_min_total_ind_traceless": 3,
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[SAVED] {bench}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
