# The AeST three-exclusion problem: where the theory actually stands

**Date:** 2026-11-18
**Receipt:** `audits/2026-11-18/aest_three_exclusion_scan.py` (exit 0)
**Baseline:** `c4a0f42`, plus the receipt `da34485` (32-claim verification)

Three independent physical exclusions currently bear on the relativistic completion. This note states them as constraints, solves the joint feasibility problem, and identifies which one is not a tuning problem.

---

## 1. The three constraints

**C1 — Cassini quadrupole.** Park et al. 2026 give `Q₂ = (1.6 ± 1.8)e−27 s⁻²`. Bare `μ_std` in the external field of the Milky Way does not pass; the corpus records ≈4.6σ at the derived `a₀` (`res_nova_manuscript.tex`). *Open discrepancy:* the audit brief states +8.73σ. Both numbers are in circulation and the difference is not resolved here. The sign and the fact of exclusion are not in doubt; the σ is.

**C2 — single-scalar k-essence.** A RAQUAL-type `P(X)` completion of `μ_std` is superluminal along the field gradient, `c_∥² = (x²+2)/(x²+1) → 2` as `x → 0`. This excludes the *k-essence* route.

**C3 — BBN against stability.** A 5% bound `G_cosmo/G_N ≥ 19/20` forces `λ_s ≥ 19`; the `J_tot` non-folding condition caps `λ_s < (27+12√6)/5 = 11.2788`.

## 2. C2 is not a constraint on AeST

C2 kills pure k-essence. AeST is not k-essence: the aether's `K_B` and the `𝒦₂` term enter the scalar sound speed, so AeST's `c_s²` is

```
c_s² = (2 − K_B)(1 + ½ K_B λ_s) / (𝒦₂ K_B)
```

which is a different function and is not forced to 2 anywhere. C2 is the *reason* AeST was chosen, not a constraint it must still satisfy. It is discharged.

## 3. C3 is exact, and its threshold is computable

With `G_cosmo/G_N = λ_s(2 − K_B)/(2(1+λ_s))` (the `Wave3BBNAndSpinCCP2Bounds` form), the ratio increases as `K_B → 0` and as `λ_s → ` ceiling. So

```
sup G_cosmo/G_N = λ_s/(1+λ_s) |_{λ_s → 11.2788} = 0.918559 = √(27/32)
```

**No choice of `K_B` or `λ_s` inside the stability window exceeds 0.918559.** Therefore:

| BBN bound on `G_cosmo/G_N` | Requirement | Verdict |
|---|---|---|
| 5% | ≥ 0.950 | **impossible**, gap 0.0314 |
| 8% | ≥ 0.920 | **impossible** |
| 8.2% | ≥ 0.918 | feasible |
| 10% | ≥ 0.900 | feasible |

**The no-go is exact for any BBN bound tighter than 8.144%.** It is not a numerical accident; `√(27/32)` is the hard ceiling and `1 − √(27/32) = 0.081441` is the loosest bound that admits any solution at all.

So the 5% no-go is real but it is a statement about the *bound*, not about AeST's structure. The physics question reduces to: what does BBN actually require of `G_cosmo/G_N`?

## 4. Above 8.144% a viable region exists, and it is narrow

At a 10% bound, feasibility requires `λ_s ≥ 9`, and pushing `λ_s` to the non-folding ceiling maximizes the allowed `K_B`:

| `λ_s` | `K_B` max | `c_s²` (𝒦₂=75) | `c_s²` (𝒦₂=150) |
|---|---|---|---|
| 10.0000 | 0.02000 | 1.4520 | 0.7260 |
| 11.0000 | 0.03636 | 0.8640 | 0.4320 |
| 11.2788 | 0.04041 | 0.7939 | 0.3970 |

Causality `c_s² ≤ 1` at the tightest viable point requires `𝒦₂ ≥ 59.5`. The corpus's own `K₂ = 75` gives `c_s² = 0.79`, which passes. `c_T = c` holds structurally: the tensor sector is Einstein–Hilbert with no Weyl coupling, so nothing in the region can spoil it.

**So two of the three are survivable by parameter choice**, at `λ_s` pinned to the ceiling, `K_B ≲ 0.04`, `𝒦₂ ≳ 60`.

## 5. C1 is not a tuning problem, and that is the bottleneck

Screening in AeST requires `J` built only from `Y^p`, `p ≥ 3/2`, with **no linear piece**. The live embedding is `J_std(Y) = F_std(√Y)`, hence

```
J'(Y) = μ_std(√Y) → 1 as Y → ∞   ⇒   J ~ Y
```

a linear piece. In Skordis–Złośnik's classification that is the **tracking** branch, not the screening branch. On tracking the scalar fifth force does not switch off; it renormalises `G_N = (1 + 1/λ_s) Ĝ` and leaves a residual.

For `μ_std` the residual is benign in its falloff but not in its limit:

```
1 − μ_std(x) ~ 1/(2x²)   ⇒   force deficit  a₀ x [1 − μ_std] → a₀/2
```

A **constant** offset does not decay with `r`, and no choice of `λ_s` or `K_B` removes it, because `1 + λ_s > 1` for every `λ_s > 0`. This is why C1 cannot be tuned away, and why it is the binding constraint: the other two are inequalities in parameters, while C1 is a statement about which *class* of `J` the galaxy law embeds into.

Two routes could discharge it, and both cost something:

1. **Change the embedding class** — use a `J` with no linear term (`p ≥ 3/2`). This screens, but it changes the galaxy law, so SPARC must be re-fitted and `a₀` re-extracted. The `n ≈ 2` selection is no longer guaranteed.
2. **Introduce a second scale** — a mechanism that switches the fifth force off below some acceleration. AeST alone does not supply one; this is new physics, and it is where the corpus's `[O]` screening entries belong.

## 6. What the xAct/Cadabra calculation must compute

The scan above uses the corpus's closed-form `c_s²`, `G_cosmo/G_N` and the non-folding ceiling as *inputs*. Those forms were transcribed from Skordis–Złośnik, not re-derived from the assembled action. The calculation worth doing is the one that removes that dependence:

1. Assemble the quadratic action for `(h^{TT}, δA_μ, δφ)` around FLRW with the full `J(Y)`, keeping `K_B`, `𝒦₂`, and the `J'`, `J''` terms.
2. Reduce to the scalar sector and read `c_s²(k, a)` **as a function of background**, not just at Minkowski. The Minkowski value is what the corpus quotes; the BBN epoch is not Minkowski.
3. Compute `G_cosmo/G_N` from the Friedmann equation with the scalar's own background contribution retained, rather than from the two-parameter truncation. **This is the step that could move the 8.144% threshold**, and it is the single most valuable thing the calculation can produce.
4. Verify `c_T = c` at quadratic order including any `J`-dependent mixing, and confirm the `C^{AB}` obstruction does not reappear once the aether kinetic terms are kept.

Until step 3 is done, the 5% no-go stands as proved but its *premise* is a truncation, and the difference between a 5% and a 9% BBN bound is the difference between a dead theory and a live one with a narrow but real parameter window.

## 7. Status summary

| Constraint | Status | Binding? |
|---|---|---|
| `c_T = c` | passes structurally | no |
| `c_s² ≤ 1` | passes for `𝒦₂ ≳ 60` | no |
| C2 k-essence | discharged (not AeST) | no |
| C3 BBN at 5% | **fails exactly**; opens above 8.144% | yes, on the bound |
| C1 Cassini | **fails**; tracking branch, constant residual | **yes, structurally** |

The theory is not killed by three independent exclusions. It is killed by one, C1, and C1 is an embedding-class problem that no parameter scan can reach.
