# Res-Nova v1.5.0 Epistemic Boundary

**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))
**Repository:** `Mega-Therion/Res-Nova`
**Physics seal:** `v1.4.0` (`651a70d8`)
**Empirical seal:** `3c90ef3e` (2026-08-15 SPARC measurement)
**This document:** epistemic alignment only. It does not add theorems.

Standard: `[P]` proved, `[D]` direct empirical, `[C]` cited, `[O]` open / quarantined. These four are the only permitted tiers (`AGENT_COVENANT.md:14-17`).

> **2026-08-16 status correction.** D3.1 suspended to `[O]` (cited file contains no limit). D3.2 regraded from the unsanctioned `[P]`-cond to `[P]` with its condition stated. F7 provenance replaced with the `VERIFICATION_RUN_003/` artifact. See `VERIFICATION_STATUS_AUDIT.md` and `THEORY_ASSUMPTION_AUDIT.md`.

This ledger supersedes `EPISTEMIC_BOUNDARY_v1.4.0.md` wherever they conflict. Formal theorems are unchanged. Empirical `a0` and parameter-count claims in v1.4.0 item **D4** are superseded as noted.

---

## Claim matrix

| ID | Claim | Tag | Artifact | Boundary |
|---|---|:---:|---|---|
| **D1.1** | Single-channel action yields inverted limits and is correspondence-false | `[P]` | `TARGET_D1_VARIATIONAL_DERIVATION.md`; `01_foundational_action/PAPER_01_NOTICE.md` | Fatal under any standard. Historical `PAPER_01` is quarantined, not current theory. |
| **D1.2** | Dual-channel `F(x)=x²/2 - x + ln(1+x)` has `F'(x)=x/(1+x)` | `[P]` | `05_lean_formalization/DualChannelDerivation.lean`, `GODActionKinematics.lean` | Algebraic identity only. Does not prove that nature uses this action. |
| **D2** | Flux–dissipation story used to motivate `F_dual` | `[P]`/`[O]` | `TARGET_D2_PHYSICAL_ACTION_DERIVATION.md` | The derivative identity is `[P]`. The entropic origin story remains a motivation unless restated as a theorem with stated axioms. |
| **D3.1** | `lim_{x→∞} μ(x)=1` | `[O]` | `PPNLimits.lean` | **Suspended 2026-08-16.** Not backed by the cited file. `PPNLimits.lean` proves finite-threshold bounds (`solar_system_precision_bound` at `x ≥ 10⁴`, `cassini_radar_delay_satisfied` at `x ≥ 6×10⁷`), not a limit. No `Filter.Tendsto` statement exists in any of the 17 modules; `mu_derived_newtonian_bound` proves `μ(x) < 1` and `sz_newtonian_limit_diff` is an algebraic identity. This is a source-content defect and is unaffected by the gate passing. Closure: write the limit, or restate the claim as the bound actually proved. |
| **D3.2** | `γ_PPN=1` in the Skordis–Złośnik parent | `[P]` | `CovariantCompletion.lean` (`disformal_gamma_ppn_unity`); `TARGET_D7_COVARIANT_COMPLETION.md` | Conditional on that embedding, not a generic scalar completion. Tier corrected from `[P]`-cond, which is not one of the four permitted tiers (`AGENT_COVENANT.md:14-17`); the condition is stated here instead. |
| **D3.3** | `α₁=-2K` with solar-system bound on `K` | `[P]`/`[D]` | `TensorSpeed.lean`; `TARGET_D8_TENSOR_SPEED.md` | Foster–Jacobson identity plus cited bound. |
| **D4.1** | Old in-sample headline: 176 parameters, median `χ²/N_g=2.92`, `a0=(9.433±0.050)×10^{-11}` | **SUPERSEDED** | `final_manuscript.tex`; older run manifests | Method defect: radial points treated as independent; 5-fold CV leaked a global `a0`. Keep as history. Do not quote as current. |
| **D4.2** | Old CV median `χ²/N_g=14.33` with identical `a0` across folds | **SUPERSEDED** | older `SPARC_CROSS_VALIDATION_REPORT.json` | Not a CV. See `a0_estimate.py` docstring. |
| **D4.3** | Working measurement: `a0=1.116×10^{-10} ± 0.128×10^{-10}` (stat) `± 0.097×10^{-10}` (syst); total 14.4%; `N=171` galaxies, 3375 points | `[D]` | `02_galaxy_dynamics/A0_MEASUREMENT.json`; `a0_measure.py` | Bootstrap over galaxies. Systematics: distance 6.6–6.9%, inclination 5.5%, M/L <1%. |
| **D4.3b** | Tension of D4.3 with `cH0/(2π)` is `0.46σ`; with MOND `1.2×10^{-10}` is `0.52σ` | `[D]` | same JSON fields `tension_claim_sigma`, `tension_mond_sigma` | Does not confirm the horizon formula. It fails to distinguish the two inputs. |
| **D4.4** | Horizon identity `a0=cH0/(2π)` | `[O]` | `04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md`; `CORPUS_DEPENDENCY_MAP.md` Root 2 | Consistency, not a derivation. Systematic floor (~8.7%) blocks a 3σ split from MOND's `1.2×10^{-10}` at `z=0`. |
| **D4.5** | `ξ := a0/(c H0) = 0.170 ± 0.025` | `[D]` arith / `[O]` reading | Computed from `A0_MEASUREMENT.json` `a0_best_fit` and `a0_claimed_cH0_over_2pi` via `ξ=a0/(2π·a0_horizon)` | The number is arithmetic. “Tied to the horizon” is `[O]`. |
| **D4.6** | Honest 5-fold CV retrains `a0` per fold (five distinct values) | `[D]` | `A0_ESTIMATE.json` `cross_validation` | Test medians 2.00–2.78 per point on that estimator. Not interchangeable with D4.1. |
| **D4.7** | Tier 0 (no per-galaxy freedom): GOD median 9.20 vs MOND 11.35 | `[D]` | `PARAMETER_LEDGER.json` `tier0_*` | Only tier that can discriminate `a0` source. GOD uses horizon `a0` tagged `[O]`; MOND uses literature `1.2×10^{-10}`. |
| **D4.8** | Tier 1 matched nuisances: GOD 2.95 / 374 params; MOND 2.89 / 374; NFW free-c 1.92 / 716 | `[D]` | `PARAMETER_LEDGER.json` `tier1_*` | At Tier 1 the two MOND-like rows share `μ(x)=x/(1+x)`. Per-galaxy freedom absorbs the `a0` difference. |
| **D4.9** | NFW with Dutton & Macciò (2014) concentration prior: median 5.62; 3/171 railed; 716 params. Unconstrained NFW: median 1.92; 97/171 railed at `c=1` | `[D]`/`[C]` | `NFW_CONSTRAINED.json`; Dutton & Macciò 2014 | 716−374=342 extra halo knobs vs GOD Tier 1. “Half as well” refers to 5.62 vs 2.95, not to unconstrained 1.92. Single-mass `c` prior is a caveat in the commit message. |
| **D4.10** | Halo-conspiracy test is a split / negative result for the strong reading | `[D]` | `HALO_CONSPIRACY.json` | `V200` correlates with baryonic mass (`ρ=0.88`); concentration does not. LCDM expects both. Do not advertise as a kill shot. |
| **D5** | Dynamical FLRW dark-energy fluid from the scalar is falsified; `Ω_Λ=ln 2` is not derived | `[P]` / `[O]` | `CovariantCompletion.lean`; `TARGET_D5_COSMOLOGICAL_SECTOR.md` | Decoupling is `[P]`. `Ω_Λ=ln 2` stays `[O]`. |
| **D6** | Kinetic convexity of `F_dual` and of `J(Y)` | `[P]` | `RelativisticStability.lean`; `SkordisZlosnikEmbedding.lean` | Ghost/gradient statement inside the stated action, not a cosmological proof. |
| **D7** | Pure RAQUAL / k-essence is superluminal on halo backgrounds | `[P]` | `CovariantCompletion.lean` | `c_∥²=1+1/(1+x)>1`. |
| **D8** | Disformal cone split `B(φ)≠0` fails GW170817 | `[P]` | `TensorSpeed.lean`; `TARGET_D8_TENSOR_SPEED.md` | Falsifies that completion, not all vector-tensor parents. |
| **D9** | Dual-channel `F` embeds in Skordis–Złośnik (2021) via `J(Y)=Y/2-√Y+ln(1+√Y)` | `[P]`/`[C]` | `SkordisZlosnikEmbedding.lean`; Skordis & Złośnik 2021 | Parent membership, not a unique completion. |
| **F7** | Lean suite: 17 modules, 0 `sorry`, axioms `{propext, Classical.choice, Quot.sound}` | `[P]` | `05_lean_formalization/verify_all_proofs.sh` | O6 — walked once in a clean worktree at 07185a6 (lake exe cache get + 17/17 PASS, VERIFICATION_RUN_007). Not yet demonstrated on a cold machine with empty host cache, and not yet a CI release gate. Artifact: `VERIFICATION_RUN_007/01_lean/` (17/17 targets, exit 0, Mathlib `5eec30bc` clean, toolchain `v4.33.0-rc1`). Elaboration does not certify assumptions carried as typeclass or structure fields — see `THEORY_ASSUMPTION_AUDIT.md`. |

---

## Regrades that matter

1. **Zero free parameters is withdrawn** as a current claim. Dual-channel `μ` is derived `[P]`. The SPARC working model still uses per-galaxy nuisances and, if you refuse the horizon formula, a fitted `a0`.
2. **`PAPER_01` / single-channel `arcsinh` remains fatal.** Inverted limits are wrong under the withdrawn standard and under the two-parameter standard.
3. **`a0` is measured, not derived.** D4.3 is the number. D4.4 is the story.
4. **`CORPUS_DEPENDENCY_MAP.md` Root 1** still labels `μ` closure `[O]`. That map is older than D1.2. Treat Root 1 as: algebraic dual-channel identity `[P]`; uniqueness-as-nature `[O]`.
5. **Claude’s “342 more parameters”** is `716-374` from `PARAMETER_LEDGER.json` / `NFW_CONSTRAINED.json`. It is in the repo. It is not a hallucination.
6. **Claude’s `ξ=0.170±0.028`** is the same arithmetic as D4.5. This ledger uses the JSON total error and gets `±0.025`. Do not invent a third `ξ` file.

---

## What v1.5.0 does not claim

This release does not derive `a0` from the horizon, does not derive `Ω_Λ`, does not run `a0(z)`, and does not vendor SPARC. Those are listed in `OPEN_PROBLEMS_AND_TESTS.md`.
