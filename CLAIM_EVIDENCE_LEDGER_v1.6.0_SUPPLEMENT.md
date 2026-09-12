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
| CLM-D3-01 | MOND correction at Earth is ~2×10⁻⁸ (1-μ, non-relativistic force law); the "1137× below Cassini" comparison is retracted 2026-09-12 as a category error (1-μ vs. γ-1 are not comparable quantities — TARGET_D3 Theorem 3.1) | [O] | TARGET_D3 §2; computed |
| CLM-D3-02 | PPN parameters depend on D7 covariant completion, not on μ | [P] | TARGET_D3 §3 Theorem 3.1 |
| CLM-D3-03 | Vainshtein screening resolves Q₂ tension (119× below Cassini; corrected 2026-09-12 from a misstated 70× that used the retracted F''/F'=0.004) | [P] | TARGET_D7_SUPPLEMENT §3 |
| CLM-D5-01 | Non-relativistic 2× MOND enhancement → 76× excess growth | [P] | TARGET_D5 §4.3; numerically integrated |
| CLM-D5-02 | RMOND linear screening reduces enhancement to ~0.23% | [P] | TARGET_D7 §4.1; F''/F' = 1/(2x₀²(1+x₀)) ≈ 0.00233 (corrected 2026-09-08 from ~0.4% / 0.004) |
| CLM-D5-03 | Non-linear structure formation in RMOND is consistent | [O] | Requires N-body (Thomas et al. 2023 framework) |
| CLM-D6-01 | F_dual is ghost-free (F''>0 ∀K>0) | [P] | TARGET_D6 §1.2; symbolically verified |
| CLM-D6-02 | Hamiltonian is bounded below | [P] | TARGET_D6 §2 |
| CLM-D6-03 | Strong coupling scale ~10⁻¹⁰ eV (far below experiments) | [P] | TARGET_D6 §3 |
| CLM-D7-01 | RMOND action with F_dual written and verified | **[X] Superseded 2026-09-12** | Was written against a vector-field (generalized Einstein-aether) 𝒦, not D9's scalar AeST 𝒴. See CLM-D7-07. |
| CLM-D7-02 | Background Friedmann equations are unmodified | **[X] Void 2026-09-12** | 𝒴≡0 identically on FLRW under the corrected AeST action — the whole §3 background-acceleration-ratio calculation (x₀≈5.67) does not apply. |
| CLM-D7-03 | Linear screening factor F''/F' ≈ 0.00233 (background Newtonian) | **[X] Void 2026-09-12** | Same root cause as CLM-D7-02: computed from a vector 𝒦 that isn't the action's actual field content. The 429× and 250× suppression factors derived from it are void, not merely miscalculated. |
| CLM-D7-04 | c_T = c (GW170817 constraint satisfied) | **[D] upgraded** | TARGET_D7 §8 — now a *structural* consequence of AeST's minimal coupling (no TT piece in δA, F² is the unique aether combination leaving h^TT unmodified), not an asserted citation. Stronger than before the fix. |
| CLM-D7-05 | Natural O(1) coupling constants satisfy all constraints | **[X] Void 2026-09-12** | c₁,c₂,c₃ do not exist in the corrected AeST action (K_B is the only aether coupling). TARGET_D7_SUPPLEMENT needs a full rewrite, not yet done. |
| CLM-D7-06 | Exact PPN γ,β for specific couplings | **[X] Superseded** | Superseded by CLM-D7-08 (γ=1 now follows from SZ's own Ψ=Φ, not from computing couplings) — but see CLM-D3-05, the result is Ψ=Φ exactly, i.e. no fifth-force slip at all, which independently kills the Foster-Jacobson-based margins in TARGET_D3 §7. |
| CLM-D7-07 | D7 action corrected to genuine AeST: scalar 𝒴=q^{μν}∇_μφ∇_νφ, minimal coupling, aether enters only via K_B F_{μν}F^{μν} (Skordis-Złośnik arXiv:2007.00082 eq. 5) | [D] | TARGET_D7_COVARIANT_COMPLETION.md, full rewrite 2026-09-12; F_dual transfers via 𝒥(𝒴)=2λ_s ã₀²F_dual(√𝒴/ã₀), 𝒥′=λ_s x̃/(1+x̃), verified symbolically |
| CLM-D7-08 | F_dual on AeST's *tracking* branch (not screening): exact solar-system solution gives g = G_N M/r² + ã₀, an r-independent anomalous acceleration, ã₀=(1+λ_s)a₀ | **[D] — apparent falsification of μ=x/(1+x) within two-derivative AeST/AQUAL** | TARGET_D7_COVARIANT_COMPLETION.md §4.2; ã₀/r at Cassini scale is 5.7×10⁵ above the Q₂ bound; corroborated by Milgrom arXiv:1205.1317 and Desmond arXiv:2401.04796 [C]. Escape requires SZ's higher-derivative screening, not built in this corpus — `[O]`. |

---

## Rescored Claims

| ID | Claim | Previous | Corrected | Rationale |
|----|-------|----------|-----------|----------|
| CLM-O1-01 | a₀ = cH horizon identification | [P] | [P/O] | 5.67× discrepancy; O4 disfavours at 5.9σ; c47e7c6 says D0_PROPOSED |
| CLM-D2-00 | F_dual uniquely determined from first principles | [P] | [P/O] | Conditional on Padé choice; necessity is [O] |
| CLM-D3-05 | γ=β=1 exactly, Cassini margin 1.1×10⁸, MESSENGER margin 1.6×10⁵ (TARGET_D3 §7) | [P] | **[X] Void** | Derived for generalized Einstein-aether (D7-as-written), which was not D9's actual AeST action. Under corrected AeST: Ψ=Φ exactly (no fifth-force slip, [C] via SZ) so the *margin* framing is moot — but see CLM-D7-08, the anomalous acceleration ã₀ is a separate, much larger problem the margin calculation never tested for. |
| CLM-D9-01 | D9 embedding normalization (μ = 𝒥′ vs 2𝒥′; ã₀ vs a₀) | [P] | [P/O] | Corrected 2026-09-12: D9 §1/§2 disagreed by a factor of 2 in the prefactor (1/8πĜ); ã₀=(1+λ_s)a₀≠a₀ was previously conflated. Fixed in TARGET_D9 header, not yet propagated to any dependent numeric claim beyond D3/D7. |
| CLM-AX-02 | `AXIOMS_V2.lean:64` — μ(x) = x/(1+x) ∨ μ(x) = x/√(1+x²) | [A] axiom | **[P/O] one disjunct falsified** | CLM-D7-08's solar-system result rules out the x/(1+x) branch within two-derivative AeST. The axiom itself isn't wrong (it's a disjunction), but any downstream claim that silently assumes the *first* disjunct (this repo's entire μ = x/(1+x) program) needs to either switch branches or invoke SZ's higher-derivative screening. Not yet resolved anywhere in the corpus. |
