# Theory-Assumption Audit — Lean Suite

> **Implemented 2026-08-16** on branch `audit/lean-inventory-o5-packaging` (commits `109d38b`, `637e60d`, and this one). Written as a proposal; the approved subset has since been applied. Nothing is merged or tagged.

**No Lean theory is altered by this document.** Findings are recorded as documentation only;
`AXIOMS_V2.lean`, `YettParadigm.lean`, and `SovereignRegularity.lean` are untouched.
Authority: `origin/main` @ `52d8688`, `git ls-files` only.
Date: 2026-08-16

All 17 tracked modules elaborate cleanly (`VERIFICATION_RUN_003/`). **This audit is about what
the theorems say, not whether they compile.** Compilation is settled; adequacy is not.

The recurring pattern: a premise is stored as a structure or typeclass field, and a "theorem"
retrieves that field. Lean accepts it because it is valid. It is not a derivation of the
premise, and the docstrings frequently describe it as one.

**Vacuity criterion used below:** a result is marked *projection* when its proof term is the
assumed field itself (or a one-step consequence), so the conclusion carries no information the
hypothesis did not already state.

---

## 1. `AXIOMS_V2.lean` — five assumptions, two trivial theorems

| Line | Assumed premise | Resulting theorem | Non-vacuous? | What would make it substantive |
|---|---|---|:---:|---|
| 50 | `Axiom_A1_Substrate` — `∃ ψ : Q, ‖ψ‖ = 1` | *none — unused by any theorem* | n/a | Derive an observable from the substrate, or delete the class. As written it is inert. |
| 54 | `Axiom_A2_EntanglementGeometry` — `∃ dist : M → M → ℝ, ∀ x y, dist x y ≥ 0` | *none — unused* | **No** | **Satisfied by `dist ≡ 0`.** Requires at minimum the metric axioms (identity of indiscernibles, symmetry, triangle inequality) and the stated monotone dependence on relative entropy. Currently it asserts only that some non-negative function exists. |
| 58 | `Axiom_A3_Equilibrium` — `∀ (_V : Set Q), ∃ S_max : ℝ, S_max ≥ 0` | *none — unused* | **No** | **Satisfied by `S_max = 0`.** The binder `_V` is discarded. Needs an actual extremization statement: `S` attains a maximum on the constrained set, with the constraint expressed. |
| 62 | `Axiom_A4_VariationalClosure` — fields `closure_is_interpolation`, `weak_field_balance` | `derived_simple_mu_bounds` (:75) — `IsInterpolationFunction μ` | **No — projection** | Proof term is `exact h.closure_is_interpolation`. Substantive only if `IsInterpolationFunction μ` is *derived* from the variational principle rather than assumed as a field of the same class. |
| 67 | `Axiom_A5_Recovery` — `newtonian_limit` | *none — unused* | n/a | Unused; also duplicates the third conjunct of `IsInterpolationFunction` (:43). |
| 80 | `g_bar > 0`, `a₀ > 0` | `deep_mond_baryonic_scaling` — `√(g_bar · a₀) > 0` | Valid, but **misdescribed** | Docstring: *"Deep-MOND limit scaling preserves Baryonic Tully-Fisher acceleration ratio."* The statement proves positivity of a square root. To match the docstring it must state `M ∝ v⁴` (or the acceleration-ratio invariance) and derive it. **Do not cite this as BTFR evidence.** |

**Note on A4's disjunction (:64):** `weak_field_balance` permits *either* `x/(1+x)` *or*
`x/√(1+x²)`. The framework's uniqueness claim for the dual-channel `μ` is therefore not
expressed here — the axiom explicitly admits the competing simple-μ form.

---

## 2. `YettParadigm.lean` — spectral gap and the θ threshold

| Line | Assumed premise | Resulting theorem | Non-vacuous? | What would make it substantive |
|---|---|---|:---:|---|
| 19–20 | `RamanujanYettSpectrum` fields `h_kappa : 0 < κ`, `h_gap : κ·κ ≤ λ₁ − λ₀` | `ramanujan_yett_spectral_gap_pos` (:24) — `0 < λ₁ − λ₀` | **Yes** (weakly) | Genuine one-step inference: `lt_of_lt_of_le (mul_pos …) h_gap`. Valid. But the *gap bound itself* is assumed. Substantive only if `κ·κ ≤ λ₁ − λ₀` is derived from an operator, not posited. |
| 20 | same `h_gap` | `ramanujan_yett_gap_bound` (:30) — `κ·κ ≤ λ₁ − λ₀` | **No — projection** | Proof term is `sys.h_gap`. It restates the field verbatim. |
| 60–68 | `ChiralThresholdState` fields `h_theta : θ = 70/100`, `h_stable : θ ≤ χ` | `chiral_phase_stable` (:68) — `70/100 ≤ st.chi` | **No — projection** | Proof is `rw [← st.h_theta]; exact st.h_stable`. **θ ≥ 0.70 is assumed by the structure, then reported as a theorem.** Substantive only if χ is constructed from a dynamical model and the threshold is *derived*. Until then, the θ = 0.70 gate is an input. |

---

## 3. `SovereignRegularity.lean` — the BKM chain

| Line | Assumed premise | Resulting theorem | Non-vacuous? | What would make it substantive |
|---|---|---|:---:|---|
| 195–199 | `BKMVorticityState` field `h_controlled : ∀ t ≥ 0, ω_sup t ≤ B` | `bkm_vorticity_integral_finite` (:203) — `ω_sup T · T ≤ B · T` | **Yes** (weakly) | Valid scaling of the assumed bound. |
| same | same | `bkm_no_blowup` (:210) — `ω_sup T · T < M` given `B·T < M` | **Yes** (weakly) | Valid chaining. |
| same | same | `sovereign_regularity_theorem` (:218) — `ω_sup T ≤ B` | **No — projection** | Proof term is `st.h_controlled T hT`. The flagship-named theorem **restates its own hypothesis**. Docstring claims *"globally regular and non-singular"*. |

**Separate and more serious — the BKM integral is not an integral.** The Beale–Kato–Majda
criterion concerns `∫₀ᵀ ‖ω(·,t)‖_∞ dt < ∞`. These statements use the **product** `ω_sup T · T`.
No `MeasureTheory` integral appears in the file. For a constant bound the two agree
numerically, but the theorem does not express the BKM criterion, and no Navier–Stokes solution,
velocity field evolution, or PDE appears anywhere in the module. `VelocityField` (:36) is a
type abbreviation, not a solution space.

**Consequence for the manuscript:** the Table 2 cell and
`reproducibility_appendix.tex:20` describe this as *"Conditional Beale–Kato–Majda integral
boundedness"*. It is bounded-by-assumption pointwise vorticity, with no integral and no PDE.
Substantive would require: a genuine `∫`, a Navier–Stokes solution object, and the alignment
condition derived rather than posited.

---

## 4. `CosmologicalSector.lean` — definitional flatness

| Line | Assumed premise | Resulting theorem | Non-vacuous? | What would make it substantive |
|---|---|---|:---:|---|
| 22 | `Omega_Lambda : ℝ := Real.log 2` — a **definition** | `log_two_pos`, `log_two_lt_one` | **Yes**, as arithmetic | These prove `0 < ln 2 < 1`. True and unremarkable. They say nothing about cosmology. |
| 25 | `Omega_m : ℝ := 1 - Omega_Lambda` | `spatial_flatness_sum` (:50) — `Ω_Λ + Ω_m = 1` | **No — true by construction** | `Ω_m` is *defined* as `1 − Ω_Λ`, so the sum is definitional. It is not a flatness result. Substantive only if `Ω_m` is measured or independently derived and the sum then *checked*. |

Consistent with `EPISTEMIC_BOUNDARY_v1.5.0.md` D4.4/D5, which already hold `Ω_Λ = ln 2` as `[O]`.

---

## 5. Language that must change regardless of verification status

These are documentation defects, not theory changes. The gate passing does not license them.

| Current wording | Where | Replace with |
|---|---|---|
| "zero custom unproven axioms" | `README.md`, `verify_all_proofs.sh:8` | "declares no Lean global `axiom`; assumptions are carried as typeclass fields, structure fields, and theorem hypotheses" |
| "Deep-MOND … preserves Baryonic Tully-Fisher acceleration ratio" | `AXIOMS_V2.lean:79` docstring | "positivity of `√(g_bar · a₀)` under positivity of its factors" |
| "globally regular and non-singular" | `SovereignRegularity.lean:216` docstring | "restates the assumed pointwise vorticity bound" |
| "Conditional BKM integral boundedness" | `final_manuscript.tex` Table 2; `reproducibility_appendix.tex:20` | "pointwise vorticity bounded by assumption; no integral and no PDE are formalized" |
| "Spectral gap positivity" presented without its premise | Table 2; appendix:19 | "positivity of an assumed spectral gap `κ² ≤ λ₁ − λ₀`" |
| "the 5 core physical axioms" | `AXIOMS_V2.lean:11` header | accurate, but note A2/A3 are satisfied by trivial witnesses and A1/A5 are unused |

**General rule proposed for the covenant:** proving a conclusion conditional on an assumed
structure field is not an independent derivation of that field, and may not be reported as one.

---

## 6. Summary

| Module | Declarations | Projections / definitional | Substantive |
|---|:---:|:---:|:---:|
| `AXIOMS_V2.lean` | 2 theorems, 5 assumption classes | 1 projection + 1 misdescribed | 0 |
| `YettParadigm.lean` | 5 theorems | 2 | 3 |
| `SovereignRegularity.lean` | 8 theorems | 1 (the flagship) | 7 (all conditional) |
| `CosmologicalSector.lean` | 4 theorems | 1 definitional | 3 (arithmetic) |

Not audited here: the ten modules carrying the relativistic-completion results
(`CovariantCompletion`, `TensorSpeed`, `SkordisZlosnikEmbedding`, `DualChannelDerivation`,
`RelativisticStability`, `PPNLimits`, `MuProjection`, `ITActionClosure`, `SOCasimirGenuine`,
`GODActionKinematics`). Spot-checks found their content matches their names — e.g.
`foster_jacobson_alpha_1_eval` genuinely derives `α₁ = −2K` from `−2K²/K`. A full pass over
those ten is the obvious next audit.
