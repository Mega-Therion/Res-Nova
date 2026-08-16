# Claim Evidence Ledger — v1.6.0 Supplement

**Appends to:** CLAIM_EVIDENCE_LEDGER.md (v1.5.0)
**Date:** 2026-08-16
**New claims from D2/D3/D5/D6/D7 push**

---

## New Claims

| ID | Claim | Status | Evidence |
|----|-------|--------|----------|
| CLM-D2-01 | F_dual is uniquely determined given 4 structural constraints (constitutive-relation, Padé[1/1], MOND BCs, dual-channel) | [P] | TARGET_D2 §9 Theorem 9.1; SymPy-verified |
| CLM-D2-02 | μ(x)=x/(1+x) is the unique Padé[1/1] satisfying μ(0)=0, μ(∞)=1, μ'(0)=1 | [P] | TARGET_D2 §5 Theorem 5.1 |
| CLM-D2-03 | μ is the inverse of the odds ratio function (Bayesian structure) | [P] | TARGET_D2 §6 Theorem 6.1 |
| CLM-D2-04 | F'(x)²·I(μ(x)) = x³ (Fisher information identity) | [P] | TARGET_D2 §7 Theorem 7.1; SymPy-verified |
| CLM-D2-05 | Padé necessity can be derived from first principles | [O] | TARGET_D2 §9 Q1-Q4 |
| CLM-D3-01 | MOND correction at Earth is ~2×10⁻⁸, 1137× below Cassini | [P] | TARGET_D3 §2; computed |
| CLM-D3-02 | PPN parameters depend on D7 covariant completion, not on μ | [P] | TARGET_D3 §3 Theorem 3.1 |
| CLM-D3-03 | Vainshtein screening resolves Q₂ tension (70× below Cassini) | [P] | TARGET_D7_SUPPLEMENT §3 |
| CLM-D5-01 | Non-relativistic 2× MOND enhancement → 76× excess growth | [P] | TARGET_D5 §4.3; numerically integrated |
| CLM-D5-02 | RMOND linear screening reduces enhancement to ~0.4% | [P] | TARGET_D7 §4.1; F''/F' ≈ 0.004 |
| CLM-D5-03 | Non-linear structure formation in RMOND is consistent | [O] | Requires N-body (Thomas et al. 2023 framework) |
| CLM-D6-01 | F_dual is ghost-free (F''>0 ∀K>0) | [P] | TARGET_D6 §1.2; symbolically verified |
| CLM-D6-02 | Hamiltonian is bounded below | [P] | TARGET_D6 §2 |
| CLM-D6-03 | Strong coupling scale ~10⁻¹⁰ eV (far below experiments) | [P] | TARGET_D6 §3 |
| CLM-D7-01 | RMOND action with F_dual written and verified | [P] | TARGET_D7 §2; asymptotics + convexity checked |
| CLM-D7-02 | Background Friedmann equations are unmodified | [P] | TARGET_D7 §3; Thomas et al. 2023 |
| CLM-D7-03 | Linear screening factor F''/F' ≈ 0.004 (background Newtonian) | [P] | TARGET_D7 §4.1 |
| CLM-D7-04 | c_T = c (GW170817 constraint satisfied) | [P] | TARGET_D7 §8 |
| CLM-D7-05 | Natural O(1) coupling constants satisfy all constraints | [P] | TARGET_D7_SUPPLEMENT §4 |
| CLM-D7-06 | Exact PPN γ,β for specific couplings | [O] | Requires post-Newtonian expansion |

---

## Rescored Claims

| ID | Claim | Previous | Corrected | Rationale |
|----|-------|----------|-----------|----------|
| CLM-O1-01 | a₀ = cH horizon identification | [P] | [P/O] | 5.67× discrepancy; O4 disfavours at 5.9σ; c47e7c6 says D0_PROPOSED |
| CLM-D2-00 | F_dual uniquely determined from first principles | [P] | [P/O] | Conditional on Padé choice; necessity is [O] |
