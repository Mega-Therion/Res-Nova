# Model identity manifest — v1.1.0 (2026-11-21)

Closure step 1 of [`audits/PHYSICS_FOUNDATIONS_AUDIT_2026-11-13.md`](audits/PHYSICS_FOUNDATIONS_AUDIT_2026-11-13.md) §6 (scope realigned `2026-11-21` under [`02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`](02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md)).
The source of truth is the Lean record `ResNova.ModelIdentity.canonical` in
[`05_lean_formalization/ModelIdentity.lean`](05_lean_formalization/ModelIdentity.lean). This page mirrors it. If they
disagree, the Lean file wins and this page is the defect.

Tiers follow [`EPISTEMIC_TIER_LEGEND.md`](docs/EPISTEMIC_TIER_LEGEND.md). The record proves no physics: it is data, and
its theorems are bookkeeping checks on the record (`[arith]`).

## Fixed entries

| Field | Value | Tier | Side | Source |
| :-- | :-- | :-- | :-- | :-- |
| spacetime dimension | 4 | `[C]` | established | `TARGET_D7_COVARIANT_COMPLETION.md` §1 |
| signature | (1 negative, 3 positive), mostly-plus | `[C]` | established | `TARGET_D7` §1 (`A^μ A_μ = −1` timelike) |
| spacetime symmetry | diffeomorphism invariance | `[C]` | established | `TARGET_D7` §1 |
| fields | `g_μν`, scalar `φ`, unit-timelike `A_μ`, multiplier `λ`, imported SM matter | `[C]` | established | `TARGET_D7` §1; `IMPORTED_STANDARD_MODEL.md` |
| aether norm | `A^μ A_μ = −1` | `[C]` | established | `TARGET_D7` §1 |
| matter metric | minimal coupling to `g_μν` (no disformal metric) | `[C]` | established | `TARGET_D7` §1 |
| AeST parameters | `K_B`, `K₂`, `Q₀`, `λ_s` | `[C]` | established | `TARGET_D7` §1, retraction 2 |
| gauge group | `SU(3) × SU(2) × U(1)` | `[C]` | established | `IMPORTED_STANDARD_MODEL.md` |
| generation target | 3 | `[E]` | established | `IMPORTED_STANDARD_MODEL.md` |
| substrate | `V₂(ℝ³)` via Cartan triality (`V₂₄₀` retired 2026-08-25) | `[conj]` | novel | `CURRENT_STATE` §2 |
| interpolating function | `μ_std(x) = x/√(1+x²)` | `[A]` | novel | `CURRENT_STATE` §1; `02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md` |
| a₀ | 1.1607 × 10⁻¹⁰ m s⁻² (bootstrap 95% [0.972, 1.295]) | `[E]` | established | `A0_DISTANCE_CORRECTED_2026-09-16.json` T1 |
| irreducible inputs | two: the a₀ scale and the μ choice | — | — | `CURRENT_STATE` (the "zero free parameters" claim is retired) |

## Open entries (no value stored)

| Field | Open question |
| :-- | :-- |
| E8×E8 role | Actual heterotic gauge group, a 4D global symmetry, or a geometric scaffold only? |
| internal space X | What is the internal space or compactification object, and what fermion bundle/operator lives on it? |
| geometry-to-spectrum route | Route (a) `V₂(ℝ³)`/triality action on bundles and modes, or (b) a heterotic `(X, V)` compactification and its index. Not chosen. |
| chirality sign rule | What dynamical rule selects the sign/orientation of the chiral spectrum? |
| 1/2π in a₀ | What independent mechanism, if any, yields it? (O1) |
| one branch, all regimes | Outside galaxies, ordinary GR holds (`FRONT.md` Block 2, `OUTSIDE_GALAXIES.md`); `μ_std` is the galaxy law scored on galaxies (`GALAXY_LAW_SCOPE_2026-11-21.md`). Open: whether one covariant completion also resolves X-COP cluster outskirts and D7 branch selection without ad-hoc solar-system screens (audit §7). |

## Bindings

[`05_lean_formalization/ModelIdentityBindings.lean`](05_lean_formalization/ModelIdentityBindings.lean) restates these theorems with their
literals read from `canonical`:

| Binding | Source theorem | Field it depends on |
| :-- | :-- | :-- |
| `canonical_generation_charge_lock` | `Wave3BBNAndSpinCCP2Bounds.matter_27_three_gen_forces_Q0_and_kpsi` | generation target |
| `canonical_zero_sum_twist_overshoots` | `Wave3BBNAndSpinCCP2Bounds.no_zero_sum_twist_below_nine` | generation target |
| `canonical_Jparam_derivative`, `canonical_Jparam_derivative_pos` | `AeSTParameterizedNormalization.deriv_Jparam`, `Jparam_deriv_pos` | interpolating function |
| `canonical_mu_lt_one` | (new) | interpolating function |
| `canonical_d2U_dmu2_neg` | `AeSTHamiltonianLegendre.d2U_dmu2_neg` | a₀ |
| `canonical_bbn_5pct_no_go_closed` | `Wave3BBNAndSpinCCP2Bounds.jtot_bbn_5pct_impossible` | matter coupling |
| `canonical_projector_annihilates_aether` | (new) | aether norm |
| `canonical_diffeo_noether_identity` | `AeSTDiffeomorphismNoether.diffeo_invariance_implies_noether_identity` | none (holds in every dimension) |
| `canonical_dim_is_one_plus_three` | (record check) | dimension, signature |
| `canonical_freeman_density_pos`, `canonical_a0_in_bootstrap_interval` | `HorizonScale.freeman_surface_density_pos` | a₀ |

[`05_lean_formalization/sabotage_model_identity.sh`](05_lean_formalization/sabotage_model_identity.sh) changes one field at a time in a
throwaway copy and requires the build to fail. It runs in the `lean-gate` CI job.

## Changing this manifest

Bump `version` in the Lean record, update this page in the same commit, and add a dated
line to `CURRENT_STATE_READ_THIS_FIRST.md`. Moving an entry from open to fixed needs the
derivation or citation that fixes it, named in the `source` field.
