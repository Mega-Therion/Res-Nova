# Paper outline — "One law across scales" (draft 1, 2026-09-27)

Working title: **A horizon-derived acceleration scale and a duality-screened interpolating function:
one modified-gravity law from the solar system to galaxy rotation curves**

Author: R. W. Yett. Target: *Physical Review D* (cover letter exists: `publication/COVER_LETTER_PRD.md`).
No contact details in the manuscript.

**Rule for every sentence in this paper:** it carries one of `[P]` proved (Lean, gate-verified),
`[D]` derived here, `[E]` empirical (a stated dataset and score), `[C]` cited, `[O]` open. Nothing
unlabelled. Parameter accounting follows the two-irreducible-parameters rule: the **scale**
(a0) and the **functional choice** (μ). It never claims "zero free parameters".

---

## Abstract (skeleton — fill last)
1. The problem: MOND-type laws fit rotation curves, but the scale a0 is fitted and the solar
   system (the Cassini external-field quadrupole) excludes the interpolating functions that fit best.
2. What is new: a0 = cH0/2π enters as a horizon scale, not a fit. With it, (i) μ_std fits SPARC;
   (ii) Cassini *prefers* the derived a0 over the literature 1.2×10⁻¹⁰; (iii) an environmental
   screening built from μ_std's own x ↦ 1/x duality, S = μ_std(1/η)², passes Cassini, leaves SPARC
   unchanged and survives Milky Way dwarfs. It adds no new constant.
3. What is proved: the duality for the whole ℓⁿ family, the D9 embedding by calculus, and the
   Lindblad coherence ceiling θ = 1/√2 (all Lean, standard axioms, sabotage-tested).
4. What is open, stated: the covariant realization of the screening, α₁/α₂, the 2PN β, and
   non-linear structure formation.

## 1. Introduction
- MOND phenomenology and the a0 coincidence (a0 ≈ cH0/2π) `[C]`: Milgrom 1983, 2015 (PRD 91,
  044009); Sanders 2019.
- The solar-system wall: Hees et al. 2016, Desmond et al. 2024, Cassini 2026 `[C]`.
- Contribution list, labels attached.

## 2. The scale: a0 = cH0/2π
- Horizon argument; 2π KMS factor proved (`HorizonScale.lean`) `[P]`. The physical identification is
  `[O]`, stated as such (O1).
- Relation to the literature's cH0/2π ≈ 6 framing `[C]`.
- Source: `04_cosmology/TARGET_O1_A0_HORIZON_DERIVATION.md`, `PEER_REVIEW_READINESS.md` §2.

## 3. The law: AeST with J(𝒴) from μ_std
- AeST action (Skordis–Złośnik 2021) `[C]`; minimal matter coupling; c_T = c structural (D8) `[D]`.
- J_std(𝒴) = F_std(√𝒴), F_std = (x√(1+x²) − arsinh x)/2; 2J′ = μ_std derived (`SZStdEmbedding.lean`)
  `[P]`. Ghost-free identically (D6) `[D]`.
- The ℓⁿ family μₙ and the duality μₙ(x)ⁿ + μₙ(1/x)ⁿ = 1 for every n (`MuNDuality.lean`) `[P]`:
  symmetry does not select n.

## 4. Galaxies: SPARC
- Ledger treatment, 171 galaxies / 3,375 points; tier 0 and tier 1 `[E]`
  (`02_galaxy_dynamics/PARAMETER_LEDGER.json`).
- Report both directions honestly: under μ_std, literature a0 wins tier-0 median (9.93 vs 11.08);
  tier 1 is tied.
- Joint likelihood over n: galaxies prefer n ≈ 2 by Δχ²/s ≈ 700–1400 `[E]`
  (`JOINT_N_LIKELIHOOD.json`).
- Negative results kept as results: a universal fractional order loses, and the Mittag-Leffler
  order only rescales a0 `[E]` (`GAMMA_FRACTIONAL_RESULTS_2026-09-27.md`).

## 5. The solar system: the Cassini external-field quadrupole
- Milgrom's exact QUMOND Q₂, validated against Hees 2016 Table 2 to 3 digits `[D]`.
- μ_std at the derived a0: excluded (+8.7σ vs the 2026 bound) `[E]`. RAR: +18.8σ.
- Under the Cassini-passing shape, the derived a0 passes and 1.2×10⁻¹⁰ fails `[E]`.
- AeST reduces to AQUAL (`sz_aqual_reduction`); QUMOND under-estimates AQUAL, so AeST has no
  escape `[D]`.
- Source: `CASSINI_EFE_QUADRUPOLE_2026-09-27.md`.

> **2026-09-27 update.** AeST's own dragged branch (D3 §34) makes the solar system exactly GR, so no Cassini
> external-field quadrupole arises and §5's exclusion does not apply to a dragged Sun. The duality screening below is then
> an alternative mechanism, not a necessity. The two predict differently for Milky Way satellites: dragged gives
> Newtonian, S(η) gives near-MOND.

## 6. Duality screening
- Why size-based screening needs a new constant (dimensional no-go) `[D]`.
- Why Galileon/Vainshtein is closed by c_T = c (`TARGET_D7` §11) `[D]`+`[C]`.
- S(η) = 1 − μ_std(η)² = μ_std(1/η)², η = g_ext/a0: the duality identity, no new constant.
- Three tests `[E]`:
  - Cassini: +1.25σ / +0.62σ, PASS.
  - SPARC per-galaxy (Chae 2020 η): neutral, and the shuffle control shows no environment signal.
  - Milky Way dwarfs (LVDB, 42): penalty 1.1 after MOND's own misfit.
- The rejected first form (S = 1 − μ) is reported, with the look-elsewhere step stated.
- Predictions: wide-binary boost ~10%; Oort-cloud comets; dwarfs at η ≳ 0.3 with σ lower by 4–17%.
- Covariant realization `[O]`, constrained: the phantom potential must live in the metric that gravitational
  waves ride. GW170817's Shapiro delay excludes photon-only (disformal) lensing (Boran et al. 2018;
  `AETHER_DRAG_AND_SHAPIRO_2026-09-27.md`). Conformal/symmetron routes pass GW170817 but bend no extra light
  (Bekenstein & Sanders 1994), so they would need a separate lensing mechanism. Aether-projected (metric-level)
  operators remain the live route.
- Sources: `SCREENING_WINDOW_…`, `ENVIRONMENT_SCREENING_…`, `DWARF_SCREENING_TEST_2026-09-27.md`.

## 7. Laboratory and equivalence-principle bounds
- Λ_SC ≈ 1.8 meV, λ ≈ 110 μm: screened in Earth's field `[D]`.
- MICROSCOPE: η_EP ≲ 4×10⁻⁴⁹ against a bound of ~10⁻¹⁵ `[D]` (`TARGET_D6_SUPPLEMENT_LSC` §4c).

## 8. PPN status
- γ = 1 exactly for any J (D3 §8.1) `[D]`.
- β: J-dependence suppressed by ε_J ≲ 10⁻¹⁷ `[D]`/`[C]`; the (λ_s, K_B) part is `[O]`.
- α₁, α₂: the Foster–Jacobson formulas do not apply at c₁₂₃ = 0 `[D]`+`[C]`. From the ab-initio work
  (`TARGET_D3_ALPHA_WORKING_2026-09-27.md`, notes 1–7): slow-motion PPN does not define them on AeST's static
  branch, because of a static residual symmetry. On the dragged branch the metric is GR, α₁ = α₂ = 0 `[D]`.
  Which branch real systems occupy is `[O]`: spirals are undetermined, and the held threshold is computed at
  leading order.
- Adding c₂(∇·A)² to lift the zero mode gives α₁ = −4c₁₄,eff, with |α₁| ≥ 2.5, which LLR excludes `[D]`.
  The zero mode, and with it the dragged branch, is required.
- λ_s ≲ 2.2 from Saturn perihelion `[D]`.

## 9. Cosmology (brief, scoped)
- Cosh-sector background `[P]` (`CoshCosmology.lean`); ξ = 1 at linear order `[D]`.
- AeST CMB fit is **reported, not verified** (the Skordis–Ilić–Złośnik ICs are unpublished) `[C]`;
  ICs re-derived in-house `[D]`.
- Non-linear structure formation `[O]` (unsimulated by anyone).

## 10. The Lindblad coherence ceiling (Pillar IV)
- 4x/(1+8x²) ≤ θ = 1/√2, with equality iff x = 1/(2√2) `[P]` (`PillarIV_AntiDriftGate.lean`, 16
  theorems).
- Invariant under Caputo memory (fractional GKSL) `[D]` numerical.
- Relation to the rest of the paper: the same θ is μ_std(1), and the same duality generates the
  screening. This is stated as structure, not as a derivation of one from the other.

## 11. Parameter accounting
- Table: what is derived, what is chosen, what is fitted (nuisance only). The two irreducible
  parameters, stated. No new constant added by the screening.

## 12. Open problems (ranked)
1. Covariant screening in AeST (metric-level only, §6). 2. α₁/α₂ (1.5PN) and the 2PN β. 3. The a0 = cH0/2π identification
from an action. 4. Non-linear structure formation. 5. Clusters (`TARGET_D10`).

## Figures
1. SPARC tier-1 comparison (μ_std, derived vs literature a0).
2. Q₂ vs a0 for μ_std / RAR / μ_dual, with the Cassini 2026 band.
3. Joint likelihood over n (galaxies vs Cassini).
4. Screening factor S(η) with the Sun, dwarfs and SPARC galaxies marked on the η axis.
5. Dwarf σ_obs vs prediction (Newton, MOND, screened).

## Reproducibility
Every number regenerates from a script in `02_galaxy_dynamics/` or `05_lean_formalization/`.
The gate is `verify_all_proofs.sh` (63/63 at draft time). Data: SPARC (Lelli 2016), LVDB
(Pace 2025, CC0), Chae 2020 Table 2.
