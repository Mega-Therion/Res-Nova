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
2. **(B) covariant derivation — DISCHARGED TO THE STATED LIMIT (2026-09-16).**
   Theorem B-cov (`Q3_AEST_COVARIANT_DERIVATION_2026-09-16.md` +
   `scripts/q3_covariant_derivation.py`, 19/19): given the covariant premises
   K1–K3 the AeST action supplies, the gradient enters as sinh of the internal
   rapidity, and (B) ⟺ μ_std identically. Residual, renamed and sharp: the
   **K3 momentum-linearity is uniqueness, not forcing** — a covariant embedding can
   still hide a non-covariant coupling inside 𝒥's freedom. Obligation 1 of layer 0
   moves from "no covariant argument yet" to "covariant uniqueness delivered;
   forcing residual named".
3. **The 2π and the Hubble form — SHARPENED (`[O-sharp]`, 2026-09-16 evening: `HORIZON_SELECTION_AUDIT_2026-09-16.md`, 10/10; 2π home discharged 2026-09-16):**
   The 2π has exactly one covariant home composable with Theorem B-cov: the
   Euclidean closure of the K2 orbit itself — (cosh ψ, sinh ψ) closes under
   ψ → iθ into the unit circle, period exactly 2π; the hyperbolic observer's
   imaginary proper-time period is 2π/a (KMS/Unruh circle).
   `TWOPI_HUBBLE_FORM_AUDIT_2026-09-16.md` + `scripts/twopi_hubble_form_audit.py`
   (11/11). The rotation-sector 2π (S3) does not transfer (compact vs boost
   sector); the crossing-time identity is bookkeeping, not a source. The
   Hubble-form residue is sharp: *which horizon's circle closes the orbit*
   (P2's measured 1.439×/0.831× factors are the discriminator). The triangle now
   has two theorem legs (B-cov, 2π-home) and one named open question.
   **Horizon Selection Update (2026-09-16 evening):** `HORIZON_SELECTION_AUDIT_2026-09-16.md`
   + `scripts/horizon_selection_audit.py` (10/10, exit 0) identifies the candidate
   physical home as the FLRW apparent (trapping) horizon $R_A = c/H$ with semiclassical
   temperature $T_A = \hbar H / (2\pi k_B)$ (Hayward 1998; Cai & Kim 2005) `[C]`. This
   reproduces $a_0 = c H / (2\pi)$ without $\Omega$ factors or approximations. The measured
   de Sitter misidentification factors ($1.439\times$ high, $0.831\times$ low) are verified
   artifacts of forcing pure de Sitter event horizons onto a matter+vacuum universe `[D]`
   (converging to 1 as $\Omega_m \to 0$). The redshift evolution corollary $a_0(z) \propto H(z)$
   predicts $a_0(1)/a_0(0) = 1.790$ ($1.405\times$ at $z=0.6$), connected to the open $0.87\sigma$
   JWST test. Status: **SHARPENED** (`[O-sharp]`), not CLOSED-derived (the local-to-global
   channel coupling remains an open postulate).
   **Horizon-selection residue — STATUS 2026-09-16 (late): OPEN, numerically narrowed,
   no selection principle.** `HORIZON_SELECTION_AUDIT_2026-09-16.md` +
   `scripts/horizon_selection_audit.py` (11/11). Against T3 95% at both distance zero
   points, only the Hubble/apparent-horizon form with quasi-static T=1/(2πR_A) is
   consistent; the ΛCDM event horizon survives only if the zero point is Planck-like;
   static patch/H_Λ is disfavored (3.5% margin, not excluded); Kodama–Hayward |κ|/2π, particle horizon, cH₀, c√Λ/2π and
   Milgrom's â₀ are excluded. Apparent-horizon thermodynamics (Cai–Kim, Wang–Gong–Abdalla)
   reaches H only via the quasi-static premise, which is 24% off today and chosen by the
   data — premise equivalent to conclusion; not derived. Decider: a₀(z) (1.79× at z=1 vs
   constant).
   **Light-cone pointer (2026-09-16):** `LIGHT_CONE_A0_AUDIT_2026-09-16.md` +
   `scripts/light_cone_a0.py` (7/7) separate local/transport/inference: η = D_L/((1+z)²D_A) = 1
   is the minimal-coupling prediction (`[C]`); (a₀^R)²/a₀^BTFR is distance-free (cancels H₀ and
   Ω_m errors, not Υ); 3σ Hubble-vs-Λ needs ≲25% per-bin a₀ at z≈1. Data at z~2 exclude ~4a₀
   (Milgrom 1703.06110), not yet 1.79×. Status unchanged `[O]`.
   **a₀(z) measurement pointer (2026-09-16):** `02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md` + `scripts/a0_highz_measurement.py` (10/10; helper self-test 15/18, S6/S8 open): RC100 high-z a₀ is flat at ~2.2–2.6× a₀_T3 over z=0.6–2.6 `[C]`; shape favors constancy, the z=0 step is calibration-limited; data CANNOT TELL Hubble form from constancy — horizon selection stays `[O]`.
   **Corollary-comparison round (2026-09-17):** `A0_HIGHZ_COROLLARY_COMPARISON_2026-09-17.md`
   + `scripts/a0_highz_corollary_comparison.py` (11/11): the apparent-horizon corollary
   (a0(z) = a0(0)√(Ω_m(1+z)³+Ω_Λ), 1.790× at z=1, ln-separation 0.582) misses BOTH RC100
   2-bin intervals in opposite directions (1.654 vs 2.597 [1.954,3.427]; 2.976 vs 2.286
   [1.930,2.685]) — the flatness tension behind the shape-only Δχ² 8.9–19.8. NOT an
   exclusion: both ln-deviations (0.45, 0.27) are under the 0.5-ln cross-method
   calibration nuisance; the fDM-prior z-trend confound (+0.53 vs fitted +0.38) can fake
   constancy; beam-smearing untested; S8 self-test at the corollary's own 1.791× injection
   shows bias −0.0416 ln ≪ 0.582 (not a resolution artifact). The falsifier is LIVE and
   two-sided: flatness surviving the confounds kills the H(z)-coupling leg; confound
   resolution leaves the corollary standing. Paths: maser-anchored calibration,
   beam-smearing treatment, x<1 high-z disks. Ciocan+2026 2.05× sits 0.14 ln from the
   corollary.
4. **Pin⁻ justification — REOPENED 2026-09-16 (N4 round-2 Kramers step has the sign reversed: T²=(−1)^F ⇔ Pin⁺ per Witten arXiv:1508.04715; see correction in `N4_ACTION_DERIVATION_AUDIT_2026-09-16.md`). Superseded label: DERIVED-GIVEN-ONE-[C]-STEP (2026-09-16 evening: `N4_ACTION_DERIVATION_AUDIT_2026-09-16.md`, 13/13; originally reopened by post-merge correction — "forced" restates N4; parsimony preference only — see correction in `PIN_JUSTIFICATION_AUDIT_2026-09-16.md`):**
   Pin⁻ is FORCED by one-channel parsimony: given the channel has exactly two
   states (the kernel, obligation 2) and orientation reversal acts on it (N4),
   Pin⁻ is the unique cover whose reflection sector couples to the channel's
   own sheets (all 6 lifts square to −I; 0 channel-coupled lifts, 13 involutions
   under Pin⁺ — a second two-fold structure the substrate audit excluded).
   Kramers-type doubling [C]-anchored. `PIN_JUSTIFICATION_AUDIT_2026-09-16.md`
   + `scripts/pin_justification_audit.py` (6/6). Residue renamed: derive N4
   itself at the action level. The covers stay machine-distinguishable
   (1 vs 13 involutions); the GL(2,3) trap stays on record.
5. **Chiral alphabet (A) — DISCHARGED TO THE STATED LIMIT (2026-09-16).**
   (A) is derived-given-Pin⁻: the two states ±1 are literally the kernel
   {±I} of the substrate's double cover; "unpolarized, not absent" is a group
   theorem (−I is a transformation — the 2π rotation — and no absorbing element
   exists: the presence reading has no substrate slot). Pin⁻ is what makes the
   sheets orientation-connected. The residue is exactly obligation 4.
   `CHIRAL_ALPHABET_SUBSTRATE_AUDIT_2026-09-16.md` + the same verifier.
6. **a₀(z)** — 0.87σ inconclusive; 5.9σ constant-a₀ verdict unrecoverable `[X]`.
7. **Embedding 2T ↪ SU(2) and McKay graph Ẽ₆** — literature-anchored `[O]`, not
   constructed in-corpus.
8. **μ_simple's a₀ prediction as falsifier battery — FORMALIZED (2026-09-16).**
   Standing harness delivered (`scripts/falsifier_battery_mu_a0_map.py` +
   `FALSIFIER_BATTERY_MU_A0_MAP_2026-09-16.md`, exit 0): map checks A1–A3 guard
   the frozen 3μ extraction; battery T1 (knife μ′(0)=1) / T2 (celerity (B)) gate
   any candidate μ; reference behaviour (std passes, dual fails T2, simple fails
   T1) is itself enforced. Binding rule live: cosmological comparison of a₀ only
   for μ_std-shaped μ, window [1.059, 1.232]e-10.

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

9. **a₀ prediction (obligation 5) — VERIFIED FINAL STATE (2026-09-16 evening: distance-corrected re-extraction executed; originally reopened by post-merge correction: SPARC distances assume H0=73 for 97/175 galaxies, so the H0 inversion is circular, not ladder-independent; 68% window is not a falsifier — see correction in `A0_PREDICTION_AUDIT_2026-09-16.md`). Originally marked discharged:**
   The scale relation a₀ = cH₀/2π is stated as a two-sided prediction:
   forward, Planck H₀ → a₀ = 1.0422e-10 (−1.37σ vs the μ_std window);
   backwards, the window inverts to H₀ = 75.06 ± 5.59 km/s/Mpc (68%,
   [68.51, 79.70]) — the theory takes the SH0ES side: Planck +1.36σ disfavored,
   SH0ES +0.36σ, TRGB/Freedman +0.92σ consistent. Hard falsifiers named in
   advance (any survey outside [68.5, 79.7] kills the identity). Binding rule
   honored: comparison valid for μ_std only (battery T1/T2 pass).
   `A0_PREDICTION_AUDIT_2026-09-16.md` + `scripts/a0_prediction_audit.py` (8/8).
   Open residue stays with obligation 3 (horizon-selection reason) and item 6
   (a₀(z)).
   **Verification (2026-09-16 evening):** `scripts/a0_distance_corrected_reextract.py`
   (8/8) executed the correction's prescription with 95% intervals:
   T1 baseline reproduces the frozen window (0.000%); T2 (flow rescaled to
   Planck) shifts a0 to 1.0975e-10 with the Planck anchor inside its 95%
   interval at <1 sigma; T3 (non-flow only, 78 galaxies) shifts a0 by only
   +0.2% — the flow-H0=73 formula is NOT the circularity's source; the local
   ladder zero point is (relocated, quantified). The Planck anchor cH0/2pi
   sits inside ALL 95% intervals under every treatment: the relation is
   verified distance-robust; the inversion is NOT independent; no side is
   taken; the 68%-falsifier language is retired. Geometric-distance a0
   (masers) named as the mover. VERIFICATION section in
   `A0_PREDICTION_AUDIT_2026-09-16.md`;
   `02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json`.
   **Round 2 (2026-09-16 evening):** N4 DERIVED rather than assumed: the
   channel is spinorial (frozen [P]); its sheets are the thermal circle's
   antipodes ([D]); parity is a PLANE reflection of the celerity axis (B-cov
   [D]) whose lift passes through the Euclidean/KMS sector and so carries the
   Kramers -1 ([C], minimal instance machine-checked); Pin^- is the unique
   cover whose PLANE-reflection lifts square to -I — Pin^+ would need the
   orientation operation to be the point inversion, excluded by B-cov.
   Bespoke input N4 retired; residual inputs: mu'(0)=1, horizon reason, and
   the [C] KMS/antiunitary identification. `scripts/n4_action_derivation.py`
   (13/13).
