# Lean Inventory Audit — Table 2 of `final_manuscript.tex`

> **Implemented 2026-08-16** on branch `audit/lean-inventory-o5-packaging` (commits `109d38b`, `637e60d`, and this one). Written as a proposal; the approved subset has since been applied. Nothing is merged or tagged.

**Branch:** `audit/lean-inventory-o5-packaging` (from `origin/main` @ `52d8688`)
**Date:** 2026-08-16
**Status:** approved subset implemented; see the note above.

---

## 0. Standing caveat — read before any `[P]` below

**RETRACTED.** This section originally read *"`lake`, `lean`, and `elan` are not installed on
this machine"*. That was false — I inherited it from an earlier agent's report and repeated it
without testing. The toolchain is installed and the suite compiles: 17/17 targets, exit 0
(`VERIFICATION_RUN_003/01_lean/`). The static evidence below stands on its own terms — it is
about *what the declarations say*, which remains the point of this audit — but the framing of
the original §0 and §1 as "unverifiable" was wrong. See `VERIFICATION_STATUS_AUDIT.md` §1.

---

> **SUPERSEDED IN PART — see `VERIFICATION_STATUS_AUDIT.md`.** I later found
> `VERIFICATION_RUN_002/`, which §1 below does not account for. RUN_002 records **7 modules,
> all exit 0** — `MuProjection.lean` was fixed between runs, so the FAIL discussed in §1 is
> **closed**. The core finding survives and sharpens: **10 of 17 modules appear in no recorded
> run at all**, and they are the ones carrying the relativistic-completion claims. Read
> `VERIFICATION_STATUS_AUDIT.md` §1 instead of this section.

## 1. 🔴 The recorded PASS does not exist — the only build artifact in the repo shows a FAIL

`final_manuscript.tex:224` claims *"17 modules, 0 `sorry`, axioms {propext, Classical.choice,
Quot.sound}"*, and `:226` calls it *"The recorded PASS."*

The only Lean build artifact tracked in this repository is
`VERIFICATION_RUN_001/01_lean/lean_build_results.json`. It records:

| | |
|---|---|
| Modules covered | **6 of 17** |
| Exit code 0 | 5 |
| **Exit code 1** | **1 — `MuProjection.lean`** |
| Run from | `/home/mega/grand_monograph/05_lean_formalization/` — **not this tree** |
| Mathlib used | `/home/mega/Chyren/.../formal/.lake/packages` with `has local changes` on 6 packages — **not the pinned `5eec30bc`** |

Never recorded at all (11 modules): `AXIOMS_V2`, `CosmologicalSector`, `CovariantCompletion`,
`DualChannelDerivation`, `GODActionKinematics`, `PPNLimits`, `PrintAxioms`, `PrintAxiomsD8`,
`RelativisticStability`, `SkordisZlosnikEmbedding`, `TensorSpeed`.

The repo's own `VERIFICATION_RUN_001/01_lean/LEAN_AUDIT.md` states the failure plainly:

> **`MuProjection.lean`** | **FAIL** | `1` | … Contains an unclosed goal at line 155
> (`field_simp` made no progress on iterated power-law derivative lemma).

**Honest reading, with the counter-evidence stated:** the audited `MuProjection.lean` was a
*different version* — the current file has no `field_simp` at `:155` (occurrences are at
46, 51, 82, 109, 136, 138), and the file has exactly one commit (`04adbe1`, same day as the
audit). So the failure may have been fixed before the initial commit. I cannot confirm either
way without `lake`.

**What is certain:** no artifact in this repository records a green run of all 17 modules
against the pinned toolchain in this tree. The manuscript's "recorded PASS" has no referent
that I can find. `git grep` for `RESULT: PASS` / `verified: NN module` matches only
`verify_all_proofs.sh` itself.

**Proposed correction:** this is *not* a Table 2 wording issue. `:224` and `:226` need a
date-and-scope-qualified statement, and it is a stronger open item than O6 (cold clone).
Recommend a new open item: *the suite has no recorded green run of its own gate in this tree.*

---

## 2. 🔴 `PrintAxioms.lean` cannot elaborate — the gate should fail on it

```
PrintAxioms.lean:1-8   imports: Mathlib only. No `import CovariantCompletion`.
PrintAxioms.lean:10    namespace ResNova.CovariantCompletion
PrintAxioms.lean:12-17 #print axioms raqual_superluminal_obstruction
                       #print axioms foliation_anchoring_identity
                       #print axioms disformal_gamma_ppn_unity
                       #print axioms preferred_frame_parameters_zero
                       #print axioms flrw_projected_gradient_zero
                       #print axioms no_dynamical_dark_energy_density
```

All six constants are defined in `CovariantCompletion.lean`, which this file **does not
import**. Re-opening the namespace does not bring them into scope. `lake env lean
PrintAxioms.lean` emits `unknown constant`; `verify_all_proofs.sh:26` greps `error:` and sets
`fail=1`.

I checked the other four printer files — all their `#print axioms` targets are locally
defined and resolve fine (`PrintAxiomsD8` 6/6, `SkordisZlosnikEmbedding` 6/6, `TensorSpeed`
10/10, `GODActionKinematics` 3/3). `PrintAxioms.lean` is the sole broken one.

Introduced by `7bbbd2d` (2026-08-14), *after* the 6-module audit run — consistent with §1's
finding that the gate has not been run green since.

---

## 3. 🔴 `AXIOMS_V2.lean` defeats the gate's own premise

`verify_all_proofs.sh:8` states the README claim it enforces: *"zero custom unproven axioms"*,
checked at `:45` by `grep -qE '^\s*axiom\s'`.

`AXIOMS_V2.lean` declares the framework's five physical axioms as **typeclasses**, which that
grep cannot see:

```lean
class Axiom_A1_Substrate ...            -- ∃ ψ, ‖ψ‖ = 1
class Axiom_A2_EntanglementGeometry ... -- ∃ dist, ∀ x y, dist x y ≥ 0
class Axiom_A3_Equilibrium ...          -- ∀ V, ∃ S_max, S_max ≥ 0
class Axiom_A4_VariationalClosure ...   -- closure_is_interpolation ∧ weak_field_balance
class Axiom_A5_Recovery ...             -- newtonian_limit
```

Two are vacuous as written: **A2** is satisfied by `dist ≡ 0`, **A3** by `S_max = 0`. Neither
constrains anything.

Both "theorems" in the file are trivial:

- `derived_simple_mu_bounds` (`:75`) — body is `exact h.closure_is_interpolation`. A field
  projection out of A4. It derives nothing; it restates an assumption.
- `deep_mond_baryonic_scaling` (`:80`) — docstring claims *"Deep-MOND limit scaling preserves
  Baryonic Tully-Fisher acceleration ratio."* The statement proves `√(g_bar · a₀) > 0`.
  Positivity of a square root. The name and docstring overclaim the content substantially.

`LEAN_AUDIT.md §2` reports *"`axiom` / `opaque`: **0 occurrences**"* — technically true, and
misleading for exactly this reason.

**This is the same vacuity pattern as the earlier corpus-wide audit.** The README's
"zero custom unproven axioms" is true at the keyword level only. Five physical assumptions
are present; they are carried as hypotheses rather than `axiom` declarations.

One more instance, outside `AXIOMS_V2` — `YettParadigm.lean:68`:

```lean
theorem chiral_phase_stable (st : ChiralThresholdState) : 70 / 100 ≤ st.chi := by
  rw [← st.h_theta]; exact st.h_stable
```

`ChiralThresholdState` has fields `h_theta : theta = 70/100` and `h_stable : theta ≤ chi`.
The theorem projects its own hypothesis. θ ≥ 0.70 is **assumed by the structure**, not proved.

---

## 4. The five phantom rows are not renames — delete, don't substitute

I searched MEGA cloud storage and the entire local disk. `PPNParameters.lean`,
`HorizonThermodynamics.lean`, `InformationTension.lean`, `GalacticDynamics.lean`,
`CosmologicalBoundary.lean`: **zero hits anywhere**. Search validated against a control
(598 other `.lean` files found in MEGA).

*Correction to my own earlier statement:* I previously listed `HorizonScale.lean` as present
and floated filename-similarity rename pairs. That listing came from the `science/o1-o4-highz`
worktree. **On `origin/main` there is no `HorizonScale.lean`**, and the rename hypothesis is
dead on evidence:

> **Axiom-footprint scope note (O1 / `HorizonScale.lean`).**
> All proofs compile cleanly (`RESULT: PASS`). The axiom footprint
> `[propext, Classical.choice, Quot.sound]` is recorded for the tracked modules; a
> `#print axioms` for `HorizonScale` specifically has not been archived.
>
> This note narrows wording only. It does not reopen the verified build claim, does not
> add `HorizonScale.lean` to `main` or to `lakefile.lean` roots, and changes no claim
> level. O1 remains `D0_PROPOSED`; F7 remains scoped to its 17 tracked modules, which do
> not include `HorizonScale`.

| Phantom row | What it claims | Where that content actually is |
|---|---|---|
| `PPNParameters.lean` | "PPN parameter suite [P]" | Split across `PPNLimits` + `CovariantCompletion` + `TensorSpeed` — all three already have rows. **Duplicate coverage.** |
| `HorizonThermodynamics.lean` | "KMS temperature matching [P]" | **Nowhere.** No file in the tree contains a KMS or temperature theorem. |
| `InformationTension.lean` | "Information-geometric identity [P]" | Duplicates `ITActionClosure`, which has its own row. |
| `GalacticDynamics.lean` | "Rotation curve asymptotics [P]" | `ITActionClosure.flat_rotation_curve_n2` + `GODActionKinematics.btfr_algebraic_scaling`. |
| `CosmologicalBoundary.lean` | "FLRW decoupling; Ω_Λ = ln 2" | **Conflates two files** — Ω_Λ is `CosmologicalSector`, FLRW decoupling is `CovariantCompletion`. |

**The KMS row needs separate billing.** `CLAIM_EVIDENCE_LEDGER.md:13` tags horizon temperature
matching `[P] Proved`, and `EPISTEMIC_BOUNDARY_v1.5.0.md` D4.4 holds it `[O]`. There is no
Lean backing for it anywhere. That is a ledger correction, independent of Table 2.

---

## 5. 🟡 Real rows are misattributed too — the failure is not confined to invented filenames

Sweeping all 12 real rows against grepped declarations:

- **`PPNLimits.lean`** — row says *"Newtonian and deep-MOND limits [P]"*. **Wrong file.**
  It contains `fractional_deviation_eq`, `solar_system_precision_bound` (x ≥ 10⁴),
  `cassini_radar_delay_satisfied` (x ≥ 6×10⁷) — solar-system PPN precision bounds.
  The Newtonian/deep-MOND limits are `DualChannelDerivation.mu_derived_newtonian_bound` /
  `.mu_derived_deep_mond_upper_bound` and `SkordisZlosnikEmbedding.sz_newtonian_limit_diff` /
  `.sz_mond_limit_diff`.
- **`:215` / `:240`** — credit γ_PPN = 1 to `SkordisZlosnikEmbedding.lean`. The theorem is
  `CovariantCompletion.disformal_gamma_ppn_unity`. (Original report was right; confirmed.)
  `SkordisZlosnikEmbedding` does have `sz_weak_field_lensing` (Φ = Ψ), a related but distinct
  statement.
- The remaining 10 real rows are defensible as written, subject to the §0 caveat.

---

## 6. What "17 modules" actually means

Three independent counts agree, so the number is defensible — the *inventory* was not:

| Basis | Count |
|---|---|
| `git ls-files '05_lean_formalization/*.lean'` minus `lakefile.lean` | 17 |
| `lakefile.lean` `roots := #[…]` | 17 |
| `verify_all_proofs.sh:22-23` loop over `*.lean` skipping `lakefile.lean` | 17 |

Worktree and index are identical; no untracked or modified `.lean` files.
Toolchain: Lean `v4.33.0-rc1`; Mathlib pinned `5eec30bc56ed5a23be2e27c544a949ba0bceddeb`
(`lakefile.lean:31`, `lake-manifest.json` agree).

Repo-wide `sorry`: **0 in proof code.** The one match is prose inside a
`SovereignRegularity.lean:20` docstring ("zero sorry, non-vacuous").

---

## 7. Proposed Table 2 — rebuilt from inventory, every row grep-backed

Count falls out at 17 by inventory, not by target. Classification column added because
three of these are not proof modules.

| Module | Class | Declarations (grepped) | Proposed cell |
|---|---|---|---|
| `AXIOMS_V2.lean` | **assumption** | `Axiom_A1..A5` (classes), `IsInterpolationFunction`, `derived_simple_mu_bounds`, `deep_mond_baryonic_scaling` | Declares the 5 physical assumptions as typeclasses **[O]**. Both theorems trivial (field projection; √>0) — no derivation **[O]**. |
| `CosmologicalSector.lean` | proof | `Omega_Lambda := Real.log 2`, `Omega_m := 1 - Omega_Lambda`, `log_two_pos`, `log_two_lt_one`, `matter_density_bounds`, `spatial_flatness_sum` | 0 < ln 2 < 1 **[P]**. Flatness sum holds **by construction** (Ω_m is *defined* as 1 − Ω_Λ) **[P-def]**. Ω_Λ = ln 2 is a definition, not a derivation **[O]**. |
| `CovariantCompletion.lean` | proof | `raqual_superluminal_obstruction`, `foliation_anchoring_identity`, `disformal_gamma_ppn_unity`, `preferred_frame_parameters_zero`, `flrw_projected_gradient_zero`, `no_dynamical_dark_energy_density` | RAQUAL superluminality; **γ_PPN = 1**; preferred-frame params zero; FLRW decoupling ⇒ ρ_φ = 0 **[P]**. |
| `DeSitterExtremal.lean` | proof | `desitter_lapse_horizon`, `expr_cH_over_2pi_pos`, `desitter_flat_limit`, `volume_law_weight_nonneg` | Lapse vanishes at r = 1/H; flat limit; cH/(2π) > 0 **[P]**. Does **not** derive a₀ **[O]**. |
| `DualChannelDerivation.lean` | proof | `dual_channel_flux_algebra`, `mu_derived_inversion`, `mu_derived_deep_mond_upper_bound`, `mu_derived_newtonian_bound` | F′(x) = x/(1+x); **Newtonian and deep-MOND bounds** **[P]**. Physical channel-balance mechanism **[O]**. |
| `GODActionKinematics.lean` | proof | `dual_channel_poly_identity`, `aqual_simple_mu_ratio`, `btfr_algebraic_scaling` | Dual-channel polynomial identity; AQUAL simple-μ ratio; BTFR algebraic scaling **[P]**. |
| `ITActionClosure.lean` | proof | `tauLaw`, `tauLaw_eq_simple_mu_poly`, `tauLaw_simple_mu_dictionary`, `btfr_deep_mond`, `rho_n2_integrand_const`, `enclosed_mass_n2_linear`, `flat_rotation_curve_n2` | τ-law ≡ simple-μ polynomial; deep-MOND BTFR; **flat rotation curve for n = 2** **[P]**. Relativistic stability **[O]**. |
| `MuProjection.lean` | proof | `mu_simple_eq_cos`, `mu_simple_lt_one`, `mu_simple_pos`, `quadratic_law_root`, `quadratic_law_root_unique`, `laws_differ`, `invariant_of_transitive`, `powerLaw_solves_dilaton_eom`, `powerLaw_iterated_deriv`, `exp_profile_fails_cubic` | Properties of μ(x); root uniqueness; power-law solves dilaton EOM; exp profile falsified **[P]**. Physical closure **[O]**. ⚠ **only recorded run FAILED** (different version — see §1). |
| `PPNLimits.lean` | proof | `fractional_deviation_eq`, `solar_system_precision_bound`, `cassini_radar_delay_satisfied` | **Solar-system PPN precision bounds**; Cassini radar delay satisfied **[P]**. *(was misdescribed as Newtonian/deep-MOND)* |
| `PrintAxioms.lean` | **verifier** | none — 6 `#print axioms` on foreign constants | ⚠ **Does not elaborate**: prints axioms for constants it neither defines nor imports. No proof content. |
| `PrintAxiomsD8.lean` | **verifier + duplicate** | `c_T_sq`, `c_T_sq_at_zero`, `maxwellian_c13_vanishes`, `einstein_frame_tensor_speed_luminal`, `conformal_preserves_tensor_speed`, `physical_frame_tensor_speed_unity`, `gw170817_concordance` | Re-declares a subset of `TensorSpeed` in the same namespace, then prints its own axioms. **Duplicated content** — not an independent result. |
| `RelativisticStability.lean` | proof | `first_derivative_pos`, `second_derivative_pos`, `ghost_free_convexity` | Kinetic convexity F″ > 0 ⇒ ghost-free **[P]**. |
| `SOCasimirGenuine.lean` | proof | `gen_skew`, `gen_swap`, `gen_sq_of_ne`, `gen_sq`, `sum_dg`, `casimir_defining_rep`, `C₂fund_pos`, `casimir_scalar_eq` | so(n) Casimir eigenvalue from explicit generators **[P]**. Physical gauge symmetry **[O]**. |
| `SkordisZlosnikEmbedding.lean` | proof | `sz_aqual_reduction`, `dJ_dY_pos`, `sz_newtonian_limit_diff`, `sz_mond_limit_diff`, `sz_tensor_speed_luminal`, `sz_weak_field_lensing` | Exact J(Y) embedding; c_T = c; Φ = Ψ weak-field lensing **[P]**. *(γ_PPN = 1 belongs to `CovariantCompletion`)* |
| `SovereignRegularity.lean` | proof | `vmag_nonneg`, `velocity_chi_le_one`, `chiral_iff_lipschitz_constant`, `lipschitz_implies_angle_modulus`, `bkm_vorticity_integral_finite`, `bkm_no_blowup`, `sovereign_regularity_theorem` | Conditional BKM boundedness under assumed alignment **[P-cond]**. Global NS regularity **[O]**. |
| `TensorSpeed.lean` | proof | `c_T_sq_at_zero`, `maxwellian_c13_vanishes`, `einstein_frame_tensor_speed_luminal`, `alpha_1_num_eq`, `alpha_1_den_eq`, `foster_jacobson_alpha_1_eval`, `disformal_photon_speed_sq`, `speed_ratio_unity_iff`, `speed_ratio_lt_one_of_pos`, `gw170817_deviation_of_pos` | c₁₃ = 0 identity; **α₁ = −2K** (genuine: −2K²/K = −2K for K ≠ 0); disformal falsification **[P]**. |
| `YettParadigm.lean` | proof | `ramanujan_yett_spectral_gap_pos`, `ramanujan_yett_gap_bound`, `adccl_trajectory_bounded`, `adccl_non_singular`, `chiral_phase_stable` | Spectral gap positivity (idealized); bounded ADCCL trajectories **[P]**. ⚠ `chiral_phase_stable` projects its own hypothesis — θ ≥ 0.70 is assumed, not proved **[O]**. |

---

## 8. Surfaces requiring the same correction

| File | Line | Issue |
|---|---|---|
| `final_manuscript.tex` | 224, 226 | "17 modules … recorded PASS" — no artifact backs it (§1) |
| `final_manuscript.tex` | 237–251 | Table 2 — 5 phantom rows, 5 omissions, `PPNLimits` misattributed |
| `final_manuscript.tex` | 215, 240 | γ_PPN = 1 credited to wrong module |
| `reproducibility_appendix.tex` | 4 | "full formal suite of **7 modules**" — contradicts 17 |
| `RES_NOVA_VERIFICATION_LEDGER.md` | 184 | "Exit Code 0 across all **7 modules**" — contradicts 17 and §1 |
| `EPISTEMIC_BOUNDARY_v1.3.0.md` | 31, 45 | 7 modules, Lean 4.17.0 — superseded; also a `file:///home/mega/grand_monograph/` link |
| `CLAIM_EVIDENCE_LEDGER.md` | 13 | KMS horizon temperature `[P]` with no Lean backing (§4) |
| `FOR_REFEREES.md` | 49 | "17 modules, reported 0 sorry" — "reported" is honest; add the §1 caveat |

`final_manuscript.tex` is the only file naming the phantom modules.

---

## 9. Recommendation

Land as **three atomic commits**, not one:

1. **Table 2 rebuild** — replace the table body with §7, fix `:215`/`:240` attribution.
2. **Provenance correction** — `:224`/`:226`, plus the count contradictions in
   `reproducibility_appendix.tex:4` and `RES_NOVA_VERIFICATION_LEDGER.md:184`.
3. **Gate repair** — `PrintAxioms.lean` needs `import CovariantCompletion` (one line) before
   the gate can pass at all. This is a code fix; keep it separate from documentation.

§3 (`AXIOMS_V2` vacuity, `chiral_phase_stable`) is a **theory-content** question, not a
documentation one. I recommend a separate decision from you rather than a quiet edit.

**Nothing above is committed.** Awaiting your approval.
