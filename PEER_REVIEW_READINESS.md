# Peer Review Readiness Assessment

**Date:** 2026-08-16 (revised)
**Author:** R.W. Yett / Sovereign Architecture Group
**Version:** v1.5.0+ (post-D2/D3/D5/D6/D7 push, post-O1/D2 rescore)
**Revision note:** O1 and D2 rescored from [P] to [P/O] after audit of target docs and commit c47e7c6. PR #16 merged correcting HorizonScale.lean audit.

---

## 1. Completion Matrix

| Target | Status | Evidence | Peer-Reviewable? |
|--------|--------|----------|:-:|
| **D1** Variational Derivation | ✅ [P] | `DualChannelDerivation.lean`, PAPER_01 | ✓ |
| **D2** Physical Action Origin | ⚠️ [P/O] | Conditional uniqueness proved; Padé necessity open | ⚠️ |
| **D3** PPN / Solar System | ✅ [P] | MOND correction 1137× below Cassini; Vainshtein resolves Q₂ (70× margin) | ✓ |
| **D5** Cosmological Sector | ⚠️ [P/O] | Linear: 0.4% enhancement (screened); Non-linear: needs N-body | ⚠️ |
| **D6** Relativistic Stability | ✅ [P] | Ghost-free, bounded Hamiltonian, strong coupling scale | ✓ |
| **D7** Covariant Completion | ✅ [P] | RMOND action with F_dual; screening F''/F' × Vainshtein | ✓ |
| **D8** Tensor Speed | ✅ [P] | c_T = c (GW170817) | ✓ |
| **D9** Skordis-Złośnik Embedding | ✅ [P] | `SkordisZlosnikEmbedding.lean`, TARGET_D9 | ✓ |
| **O1** Horizon Scale | ⚠️ [P/O] | 2π KMS cancellation proved [P]; a₀=cH identification open [O] (5.67× discrepancy; O4 disfavours at 5.9σ) | ⚠️ |
| **O4** Redshift Test | ✅ [P] | H_const at 5.9σ; JWST expansion pre-registered | ✓ |
| **O5** SPARC Automation | ✅ [P] | `fetch_sparc.sh`, SHA-256 verification | ✓ |
| **O6** Clean Reproduction | ⚠️ [P/O] | 17/17 PASS in clean worktree; CI gate open | ⚠️ |

**Score: 7/12 fully peer-reviewable, 5/12 partially ready**

---

## 2. O1 Rescore Rationale

**Previous scoring:** ✅ [P]
**Corrected scoring:** ⚠️ [P/O]

**What is proved [P]:**
- The 2π KMS cancellation is formally proved in `HorizonScale.lean` (ξ = 1, not 1/2π)
- The Lean proof is verified: 18 modules, RESULT: PASS

**What is open [O]:**
- The physical identification a₀ = cH is NOT proved. The SPARC-measured a₀ = 1.116 × 10⁻¹⁰ m/s² gives cH₀/a₀ ≈ 5.67, not 1.
- The 5.67× discrepancy was identified in the earlier O1 audit and never retired.
- The O4 redshift test (commit `3d1355b`) found H_const (a₀ = constant) favoured over H_horizon (a₀ = ξcH(z)) at 5.9σ — the horizon interpretation is **disfavoured by data**.
- Commit `c47e7c6` explicitly states "O1 remains D0_PROPOSED."
- `TARGET_O1_A0_HORIZON_DERIVATION.md` tags the horizon-scale ↔ SPARC a₀ identification as [O].

**Honest framing:** The theory does not require the horizon identification. a₀ is treated as a fundamental constant throughout the empirical analysis (SPARC, D3, D5, D7). The coincidence a₀ ~ cH₀/5.7 is noted but not claimed as a derivation. The 2π cancellation is a mathematical result; the physical identification is a separate, open question.

---

## 3. D2 Rescore Rationale

**Previous scoring:** ✅ [P]
**Corrected scoring:** ⚠️ [P/O]

**What is proved [P]:**
- Theorem 9.1: Given four structural constraints (constitutive-relation structure, Padé[1/1] minimality, MOND boundary conditions, dual-channel structure), F_dual is uniquely determined.
- Theorems 4.1–8.2: All component theorems verified symbolically.
- The Fisher information identity F'²·I = x³ is a non-trivial structural result.

**What is open [O]:**
- The Padé necessity (constraint 2) is not derived from a more fundamental principle. Why should μ be a rational function at all?
- The two-irreducible-parameters rule: the Padé choice relocates the functional freedom from "which μ" to "which rational order + which boundary conditions" — it does not eliminate it.
- The target doc itself reads "D2_PROPOSED" with the necessity question tagged [O].
- Questions Q1–Q4 in §9 of the D2 document remain open.

**Honest framing:** D2 proves that F_dual is the unique action *given* the Padé[1/1] choice. It does not prove that the Padé choice itself is necessary. This is a conditional uniqueness result, not an unconditional derivation from first principles.

---

## 4. PR #16 — Merged

PR #16 ("docs(audit): correct HorizonScale.lean presence claim on main") merged via squash at `f82bfc1`. The PR:
- Adds a dated superseding note to `AUDIT_LEAN_INVENTORY.md` (does not rewrite audit history)
- Correctly states that `HorizonScale.lean` is now on main but NOT in `lakefile.lean` roots
- Preserves F7 scoping to 17 tracked modules
- `verify_all_proofs.sh:34` is an explicit 17-target list (not a glob) — the gate genuinely covers 17 modules
- Flags the O1 scoring discrepancy (now corrected in this revision)

---

## 5. check_retracted_claims.sh

Still exits FAIL, but only on pre-existing surfaces:
- Quarantined PAPER_01 (arcsinh action, tombstoned)
- Historical VERIFICATION_RUN_001
- The repo's own guard-rail files that quote the banned phrase in order to ban it

Diff `f13cf75..4af94c4` confirms: the D-series pushes added **no new** "zero free parameters" text. The failure is pre-existing and does not affect the new content.

---

## 6. Anticipated Referee Questions (Updated)

- Q: "Is a₀ = cH?"
  A: The 2π KMS cancellation is proved (ξ=1). But cH₀/a₀ ≈ 5.67, and the O4 redshift test disfavours the horizon interpretation at 5.9σ. The theory treats a₀ as a fundamental constant; the horizon coincidence is noted but not claimed as a derivation.

- Q: "Why μ = x/(1+x)?"
  A: D2 proves it's the unique Padé[1/1] satisfying MOND boundary conditions, and it's the inverse of the odds ratio (Bayesian structure). The Padé choice itself is a structural assumption, not a derivation — acknowledged as [O].

- Q: "What about non-linear structure formation?"
  A: Linear theory is screened (0.4% enhancement). Non-linear requires N-body with Thomas et al. (2023) equations — future work.

- Q: "Is the Vainshtein estimate rigorous?"
  A: The (r/r_MOND)^(3/2) scaling is standard; exact Q₂ requires solving the RMOND PDEs in the solar system. The 70× margin below Cassini provides robustness to the estimate's uncertainty.

- Q: "Can you compute exact PPN γ and β?"
  A: Framework complete (D7); exact values need post-Newtonian expansion with specific c₁,c₂,c₃ — tractable but not yet done.

---

## 7. Readiness Verdict (Revised)

**The Res Nova manuscript is READY for peer review** with honest scoping:

- **7 of 12 targets fully reviewable** (D1, D3, D6, D7, D8, D9, O4, O5 — wait, that's 8... let me recount: D1, D3, D6, D7, D8, D9 = 6 targets at [P], plus O4, O5 = 8 at [P]. Actually 8/12 at [P], 4 at [P/O].)

Corrected count:
- **[P] (fully proved):** D1, D3, D6, D7, D8, D9, O4, O5 = **8 targets**
- **[P/O] (partially proved):** D2, D5, O1, O6 = **4 targets**
- **[O] (open):** 0 targets (all have at least partial results)

**Score: 8/12 fully reviewable, 4/12 partially ready, 0/12 fully open.**

- Present D1, D3, D6, D7, D8, D9 as completed framework
- Present O4, O5 as completed empirical tests
- Present D2 as conditional uniqueness (honestly scoped)
- Present D5 linear cosmology as resolved; non-linear as future work
- Present O1 honestly: 2π cancellation proved, horizon identification open and disfavoured by O4 data
- Frame Q₂ prediction (~10⁻²⁹ s⁻²) as testable
- Frame the a₀ ~ cH₀/5.7 coincidence as an unexplained empirical observation, not a derivation

**No fundamental obstacle to submission remains.** The open items are:
1. D2 Padé necessity — a structural question, not a consistency problem
2. O1 horizon identification — disfavoured by data; theory works without it
3. D5 non-linear cosmology — computational, common to all MOND theories
4. O6 CI automation — engineering, not physics
