# CORE OBJECTS AUDIT LEDGER — Res-Nova Version 0.2 cycle

**Status:** v1.0 — **THE FINITE ALGEBRAIC AUDIT LEDGER IS FROZEN** (2026-09-16).
This is the consolidated index of the Core Objects audit cycle: every `RN-CO-*` item,
its epistemic status, machine artifacts, and the open-items register. The cycle's
working rule (from the μ_std audit, 2026-09-16): statements are tagged `[P]` proved /
`[D]` derived-verified / `[C]` cited-conjectured / `[O]` open / `[X]` killed, and
failure modes F1–F7 govern what counts as corroboration, counting, and qualification.
**Cross-reference:** this ledger is the audit-cycle overlay on the main corpus ledger
`CLAIM_EVIDENCE_LEDGER.md` (+ v1.6.0 supplement). Overlaps are cross-linked per item.
**Last updated:** 2026-09-16

---

## 1. Item index

| item | content | status | primary artifact |
|---|---|---|---|
| **RN-CO-01** | Finite core construction: Q8⋊C3, order 24, order census {1:1, 2:1, 3:8, 4:6, 6:8}; identification with the binary tetrahedral group 2T | `[P]` (in-model) + standard (literature, RN-CO-MCKAY-03) | `05_lean_formalization/BinaryTetrahedral.lean` (pure Lean 4 core, zero Mathlib, zero sorry) |
| **RN-CO-02** | Conjugacy classes (sizes {1,1,4,4,4,4,6}) and the full 7×7 character table; irrep dims {1,1,1,2,2,2,3} | `[P]` (in-model) + standard; class-naming convention logged as citation hazard | same; fingerprint table F-1..F-7 in `PRIOR_ART_BINARY_TETRAHEDRAL_MCKAY_2026-09-16.md` |
| **RN-CO-03** | The chiral structure: reflection lifts of order 4, square = central sign (the "crack"); continuous embedding 2T ↪ SU(2); McKay graph Ẽ₆ | crack = **Pin⁻(3) standard behaviour** `[P]`/literature; Pin⁻ selection itself `[O]`; embedding + McKay graph `[O]`-literature (anchored, not constructed) | PRIOR_ART packet §1 (F-8, F-9), §3 |
| **RN-CO-DIAG-01** | Diagnostics pass: order multiset, class partition, character table exhaustively verified against binary-tetrahedral benchmarks | `[P]` complete — **frozen** | `BinaryTetrahedral.lean` + Pass 1.5 enumeration (see PRIOR_ART packet §5) |
| **RN-CO-MCKAY-01/02** | Finite-model census + character enumeration for the locked core | `[P]` complete — **frozen** | same |
| **RN-CO-MCKAY-03** | Prior-art packet: all 9 fingerprints verified against GroupNames/Groupprops/nLab/McKay/Steinberg; verdict — no new mathematics; crack = Pin⁻ convention; 3A/3B citation hazard logged | **complete** | `PRIOR_ART_BINARY_TETRAHEDRAL_MCKAY_2026-09-16.md` |
| **RN-CO-04** | μ_std representation audit: 12 𝒞-identities, 3-family 𝒫 structure, de Sitter–Unruh route (2π discrepancy), rapidity-multiple family W0..W3, μ_simple killed by the normalization knife (μ′(0)=1/2 ≠ 1) | **complete** | `REPRESENTATION_AUDIT_MU_STD_2026-09-16.md`; overlaps CLM-01 (μ_dual `[X]`), CLM-02 |
| **RN-CO-04b** | Postulate R isolation: (A) chiral alphabet and (B) celerity identification are independent inputs; no reading of one gives the other; Galois-witness pairs constructed | `[P]` complete | `POSTULATE_R_ISOLATION_2026-09-16.md` |
| **RN-CO-05** | a₀/SPARC representation audit: 3 𝒞-dresses, 5 𝒫-families, **two-axis tension map**, Hubble-radius form pinned, (μ, a₀) pair binding, a₀(z) inconclusive | **complete** | `REPRESENTATION_AUDIT_A0_SPARC_2026-09-16.md` + `scripts/a0_representation_audit.py`; overlaps CLM-03 (2π), CLM-05 (a₀ measurement) |
| **RN-CO-05b** | The (μ, a₀) map: μ_simple row **measured** — a₀ = 5.443e-11, windows pairwise disjoint, deep-MOND ½ structure confirmed (ratio 0.469); normalization knife's empirical shadow; binding rule: cosmological comparison only in the μ_std row | **complete** (measured 2026-09-16) | `02_galaxy_dynamics/sparc_a0_reextract_3mu.py`, `A0_REEXTRACTION_3MU_2026-09-16.json` |
| **RN-CO-06** | Physical interpretation layer 0: minimal narrative (N1–N6, per-sentence tagged), six obligations, de Sitter–Unruh triangle | **opened** (adds no `[P]`) | `PHYSICAL_INTERPRETATION_LAYER_0_2026-09-16.md` |

## 2. Open-items register (the cycle's outstanding `[O]` list)

1. **Exact-pipeline validation gap — PARTIALLY CLOSED (2026-09-16).** Reconstruction
   with the documented per-galaxy SPARC distance+inclination Gaussian priors
   (`02_galaxy_dynamics/sparc_a0_pipeline_reconstruction.py`, master table
   `/tmp/sparc_meta.csv`, 175/175 galaxies) extracts **a₀ = 1.0243e-10, 68%
   [9.608, 1.0853]e-10** — a +10.3% shift from the no-prior harness (9.285e-11) that
   closes **53% of the gap** to the legacy 1.107e-10. The legacy value sits ~1.7σ
   above the reconstruction's 68% window: **bracketed, not reproduced.** Residual
   discrepancy (~8%) is attributable to the original optimizer's undocumented
   specifics (continuous per-galaxy optimization vs. grid marginalization). The gap
   is now measured and decomposed, not merely noted.
2. **(B) covariant derivation** — Q3/AeST target: derive that the external gradient
   enters as sinh of the internal rapidity. Obligation 1 of layer 0.
3. **The 2π** and the Hubble-form specificity (obligation 3); de Sitter–Unruh triangle.
4. **Pin⁻ justification** — the finite model's silent convention choice (obligation 4).
5. **Chiral alphabet (A)** — justify or accept as primitive (obligation 2).
6. **a₀(z)** — 0.87σ inconclusive; 5.9σ constant-a₀ verdict unrecoverable `[X]`.
7. **Embedding 2T ↪ SU(2) and McKay graph Ẽ₆** — literature-anchored `[O]`, not
   constructed in-corpus.
8. **μ_simple's a₀ prediction as falsifier battery** — any theory whose μ is not
   μ_std-shaped is displaced ~2× in a₀ (RN-CO-05b); formalize as a standing test.

## 3. Cycle state

The finite algebraic core audit (RN-CO-01..03, DIAG-01, MCKAY-01..02) is **frozen**
with standardness externally certified (MCKAY-03). The empirical layer's representation
audits (04, 04b, 05, 05b) are complete; the measured object is the pair (μ_std, a₀ =
1.1607e-10, 68% [1.059, 1.232]e-10). Interpretation layer 0 is open with six
obligations. **Next cycle candidates:** close the exact-pipeline gap (in progress);
Q3 work on obligation 1; any layer-1 interpretive statement must discharge its
obligations before promotion beyond `[C]`.

**Reproduce:** every artifact carries its own verifier (see per-item artifacts);
the two scripts added 2026-09-16 are `scripts/a0_representation_audit.py` and
`02_galaxy_dynamics/sparc_a0_reextract_3mu.py` (SHA-256-verified data, /tmp/sparc_data,
manifest `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256`).
