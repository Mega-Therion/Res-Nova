# D10 AeST cluster test on X-COP: passes at R₅₀₀, fails at R₂₀₀ (2026-11-19)
Pre-registered in `PREREG.md` (a2ea966, before any number). Data in `xcop_data.tsv`: Ettori et al. 2019; Eckert et al. 2019, with gas and non-thermal-corrected total mass measured to R₂₀₀. Script `xcop_test.py` → `XCOP_RESULT.json`. 12 clusters.

| Model | median R₅₀₀ | in [0.7, 1.4] | median R₂₀₀ | in [0.7, 1.4] |
|---|---|---|---|---|
| Pure MOND (μ_std) | 1.90 | 0/12 | 1.49 | 2/12 |
| AeST static | 0.80 | 9/12 | 0.60 | 1/12 |
| **AeST supply-capped** | **0.83** | **12/12 (CLOSES)** | **0.62** | **1/12 (FAILS)** |

**What it means.**
- **At R₅₀₀ the pre-registered primary criterion passes.** This is the first time in the corpus: on clusters with measured outer gas, AeST's dust sector (well-posed virial boundary, cosmic supply cap) accounts for the mass at R₅₀₀ in every cluster, with no tuning.
- **At R₂₀₀ it fails by overshooting.** From R₅₀₀ to R₂₀₀ the model adds too much mass: R falls 0.83 → 0.62 while pure MOND's rises toward 1. The extra AeST mass is too extended.
  - Its radial profile, not its amount, is now the discriminating failure.
  - The R₂₀₀ figure sits 4% inside the Φ(r_v) = 0 boundary, so it is the most boundary-sensitive number in the test.
- The supply cap binds in 4/12 clusters (A2029, A2142, A3266, ZwCl1215). The median dust need is 0.76 of the cosmic allowance.
- **Gas profile.** A β-model fitted to the two measured gas masses (β = 0.58–0.86, r_c = 0.1 R₅₀₀). The inner shape is assumed, but the masses at both test radii are measured.

**Verdict.** Mixed, and sharper than any earlier D10 result. The cluster mass at R₅₀₀ is reproduced (12/12); the mass growth to R₂₀₀ is not (1/12).
- **[O], the next question:** what sets the AeST dust's outer profile? Candidates are the boundary radius (the splashback radius rather than r_v) and the onset of the x_H screen in the cluster outskirts, which the static solve here does not include.

## Screen consistency: tests A, B, C (`../tidal_aest/PREREG_XH_BARYONIC.md`, pre-registered per stage)
**Gap found in review.** The candidate's virial screen S_lin(x_H) was validated on SPARC using x_H from the *observed* field. In a theory without dark matter, "Φ_N" is ambiguous: it could mean the baryonic field or the full metric potential.

| Test | x_H defined on | Result |
|---|---|---|
| **A**: SPARC | baryons | 1.9% of points have S < 0.99 at 154, against the 1% rule: **fails narrowly**. Minimum x_H = 363, so S ≥ 0.85. The largest passing value is x_H,low = 110. |
| **B**: X-COP, S on MOND | baryons, x_H,low = 110 | R₅₀₀ = 2.11, R₂₀₀ = 2.56: **fails decisively**. Baryonic x_H is only about 26–65 in cluster outskirts, so MOND is screened off there. |
| **C**: X-COP, S on MOND | full metric potential (self-consistent; converged to 3×10⁻⁴), x_H,low = 154 | **R₅₀₀ = 0.92, 12/12: passes.** R₂₀₀ = 0.755, 8/12: **fails narrowly**, improved from 0.62 and 1/12. |

**Conclusions.**
- **The screen must be defined on the full metric potential.** The baryonic definition is ruled out [X] by clusters (B), and is marginal on SPARC (A). The full-field definition keeps SPARC at 0% (as in `xh_screen.py`) and leaves linear growth unchanged (linear modes have x_H ≲ 1 either way). It is also the natural covariant choice, since Ψ = Φ is the metric potential.
- With it, the candidate reproduces cluster masses at R₅₀₀ (12/12, median 0.92). At R₂₀₀ it comes within one cluster and 0.045 in the median of the pre-registered criterion.
- Median S at R₂₀₀ is 0.82: the screen is acting in the outskirts, exactly where the overshoot was.
- **Remaining [O]:** a residual ~25% outer overshoot at R₂₀₀. The candidates (not tuned here) are the boundary radius (splashback), the inner gas shape (β-model assumed), and the 5–15% non-thermal-pressure corrections already folded into M_tot.

## R₂₀₀ systematics sweep (`PREREG_SYSTEMATICS.md`, `xcop_systematics.py` → `XCOP_SYST_*.json`)
Each systematic was varied one at a time within its physical range, and every configuration is reported.

| Configuration | R₅₀₀ (median, in band) | R₂₀₀ (median, in band) |
|---|---|---|
| Baseline (Test C) | 0.922, 12/12 | 0.755, 8/12 |
| Gas core r_c = 0.05 R₅₀₀ | 0.921, 12/12 | 0.776, 9/12 |
| Gas core r_c = 0.2 R₅₀₀ | 0.924, 12/12 | 0.771, 9/12 |
| M_HSE (no non-thermal correction) | 0.881, 11/12 | 0.710, 7/12 |
| Boundary 1.2 r_v | 0.844, 11/12 | 0.600, 3/12 |
| Boundary at splashback (≥ 1.4 r₂₀₀) | — | ill-posed: past the Lane–Emden radius for 5–11/12 clusters (§14) |

**Verdict: not closed, and not systematics-limited.**
- **R₅₀₀ is robust:** it passes in every configuration.
- **R₂₀₀ is robust too, but as an overshoot.** Every allowed configuration gives a median of 0.60–0.78. The best variant reaches 9/12, but its median is still below 0.8.
- So the excess dynamical mass at R₂₀₀ (about 25%) is a genuine prediction of this model, not a modelling artefact. **[D]: the candidate's mass profile is too extended between R₅₀₀ and R₂₀₀.**
- That makes it a falsifiable target. Weak-lensing mass profiles to R₂₀₀ on X-COP-like clusters would confirm or kill it.

## Cosh dust function test + #257 grid-sawtooth audit (`PREREG_COSH.md` 29b64d1a, `xcop_cosh.py` → `XCOP_COSH_SUMMARY.json`)
Pre-registered in `PREREG_COSH.md` before any run. Replaces the quadratic $n=1$ polytrope dust source $-\mu^2 r^2 \Phi$ with the corpus's cosmological Cosh function (`CoshCosmology.lean`, `TARGET_D5`), $\mu^2 r^2 \Phi_c \sinh(-\Phi/\Phi_c)$ ($\Phi_c = c^2 r$, D5 window $2.5\times 10^{-8} \ll r \lesssim 2\times 10^{-2}$), keeping Test C fixed ($x_H$ on the full solved field, $x_{H,\mathrm{low}} = 154$, $\Phi(r_v) = 0$, cosmic supply cap $5.36\,M_b$).

1. **Control audit at $r = \infty$ & `#257` `np.gradient` sawtooth bias:**
   - Exact verbatim reproduction of `xcop_screened_full.py` (`testc_exact`: 6 undamped `np.gradient` iterations on $N=800$, `DOP853`): **`R500_capped = 0.9221` (12/12)**, **`R200_capped = 0.7548` (8/12)**, matching `XCOP_SCREENED_FULL.json` identically (`±0.0000`). However, the undamped `np.gradient` fixed-point loop did not converge (`max |ΔS| = 0.332` across the sample), exciting a grid-scale sawtooth in `A1644` (adjacent-cell jump `0.321`, dragging `A1644 R200` from `0.795` to `0.696`).
   - Self-consistent `smooth_phi` (degree-14 log-log polynomial derivative, `0.75`-relaxed to `max |ΔS| ≤ 9.8e-5`, finite-difference self-consistency residual `max_fd_resid = 1.61e-3`): **`R500_capped = 0.9236` (12/12)**, **`R200_capped = 0.7927` (9/12)** (`R500_static = 0.9077` 11/12, `R200_static = 0.7637` 7/12). Removing `#257`'s numerical sawtooth shifts median `R200_capped` up by **`+0.0379`** (`A1644 R200`: `0.696 → 0.795`), still **FAILING** the pre-registered `[0.80, 1.25]` median criterion.

2. **Pre-registered 7-point Cosh grid (`smooth_phi`, all numbers reported):**

| $r = \mathcal{Z}_0/Q_0$ | Static conv. | Capped conv. | Median $R_{500,\mathrm{cap}}$ (in $[0.7,1.4]$) | Median $R_{200,\mathrm{cap}}$ (in $[0.7,1.4]$) | Max `fd_resid` | Verdict |
|---|---:|---:|---|---|---:|---|
| `inf` (control) | 12/12 | 12/12 | 0.924 (12/12) | 0.793 (9/12) | 1.61e-3 | FAILS |
| `1e-3` | 12/12 | 12/12 | 0.924 (12/12) | 0.793 (9/12) | 1.64e-3 | FAILS |
| `1e-4` | 12/12 | 12/12 | 0.920 (12/12) | 0.788 (9/12) | 1.58e-3 | FAILS |
| `3e-5` | 6/12 | 12/12 | 0.909 (12/12) | 0.765 (9/12) | 1.34e-3 | FAILS |
| `1e-5` | 0/12 | 12/12 | 1.598 (4/12) | 1.754 (3/12) | 3.17e-3 | FAILS |
| `3e-6` | 0/12 | 8/12 | 2.320 (0/12) | 3.186 (0/12) | 8.54e-1 | FAILS |
| `1e-6` | 0/12 | 0/12 | — (0/12) | — (0/12) | — | FAILS |

   - **Secondary diagnostic (fixed-$\mu$ free-boundary $\Phi_0$ cap):** `r = 1e-4` gives `R500 = 0.901 (12/12)`, `R200 = 0.779 (8/12)`; `r = 3e-5` converges for `6/12`; `r = 1e-5` converges for `0/12` — FAILS.

**Verdict & new constraint:**
- **Cosh concentration route for cluster $R_{200}$ is `[X]`:** Because $\sinh(-\Phi/\Phi_c) > -\Phi/\Phi_c$, finite $r$ strengthens central dust accretion rather than suppressing outer dust, pushing $R_{200}$ *downward* (`0.793 → 0.788 → 0.765`) until hitting Bratu / Bonnor–Ebert hydrostatic collapse (`6/12` static failures at `r = 3e-5`, `12/12` static failures for `r ≤ 1e-5`, `0/12` total convergence at `r = 1e-6`).
- **Conditional cluster constraint on r (`[O]`; was `[D]`, downgraded on verification, see below):** Requiring static hydrostatic equilibrium (`12/12` clusters at universal $\mu$) excludes $r \le 3\times 10^{-5}$ (`r = 1e-4` passes `12/12` static stability; `r = 3e-5` collapses in `6/12` clusters), raising the lower bound on $r \equiv \mathcal{Z}_0/Q_0$ by ~3 orders of magnitude over the previous D5 window `r ≫ 2.5e-8` to **`r > 3e-5`** (`r ∈ [1e-4, 2e-2]`). The underlying D10 `R200` ~25% overshoot remains **`[O]`** (real weak-lensing profiles out to `R200` / measured outer ICM slopes remain decisive).

### Independent verification (Claude Code CLI, 2026-11-19)
- **Reproduction.** `xcop_cosh.py` reruns byte-identical to every committed `XCOP_COSH_*.json` (only `elapsed_seconds` differs).
- **The `#257` audit holds.** Plain `np.gradient` iteration of the original `xcop_screened_full.py` model was rerun with 0.5 damping and up to 30 steps. It does not converge at N = 200, 400 or 800: A1644 `R200` wanders between 0.65 and 0.79, and max |ΔS| stays at 0.11–0.17 (`VERIFY_SAWTOOTH.json`). The agent's smooth A1644 solution, interpolated onto the original solver at N = 200, gives `R500 = 0.908`, `R200 = 0.795`, with a self-consistency residual of ~1.5e-3. So it is a genuine solution of the original equations. It is unstable under plain iteration: the residual grows ~4× per step.
- **Why.** In g′ = u′ + S′(g_MOND − g_N) + S(dg_MOND/du − 1)u′, the term S′(g_MOND − g_N) means the full-field screen depends on its own derivative. That makes the screen an implicit first-order ODE in S rather than a pointwise fixed point, and plain finite-difference iteration amplifies grid-scale modes.
- **Consequence.** `#257`'s `R200 = 0.755` was an unconverged iterate; the self-consistent value is **0.793 (9/12), still failing** `[0.80, 1.25]`. The overshoot is ≈ 21%, not 25%. `R500` is robust (0.922–0.924, 12/12). The systematics sweep (`xcop_systematics.py`) used the same 6-step iterate, so its R₂₀₀ range (0.60–0.78) carries the same bias; its qualitative conclusion stands. Uniqueness of the smooth solution is not established `[O]`.
- **Pre-registration deviation.** `PREREG_COSH.md` fixed the solver as `xcop_screened_full.py` and required the r = ∞ control to reproduce 0.755 ± 0.01. The grid was run on `smooth_phi`, whose control is 0.793. The audit above justifies the change, but it is recorded as a deviation. On the pre-registered solver at r = 1e-4 (`VERIFY_COSH_PREREG_SOLVER.json`), Cosh gives the BVP a second, high-dust root. A2319 has two roots at r = 1e-4 (R500 0.17 with 6× the dust cap, and R500 1.03) against one at r = ∞ (`verify_branches.py`). The literal first-root rule lands 5/12 clusters on that second root, and its nominal capped medians (R500 0.958, R200 0.805, 11/12) would pass. But in 4 of those 5 clusters the "capped" solution does not meet the cap: dust sits at 0.46–0.78 of it, because `brentq` converged on the jump between branches. So the nominal pass is not a valid solution set, and it fails the pre-registered requirement that every solve converges. On the branch continuous with the r = ∞ control (`BRANCH=connected`), the result is R500 0.918 (12/12, passes) and **R200 0.773 (9/12), which fails**. The `[X]` stands on both solvers. On the smooth solver the median R200 is non-increasing in 1/r; on the original solver the shifts sit within its ±0.05 iteration noise, so no stronger monotonicity claim is made. Whether the high-dust branch is unstable (as in Bratu/Bonnor–Ebert) is not proven `[O]`.
- **The r bound is downgraded to `[O]`.** It was not a pre-registered outcome. It rests on static (uncapped) existence, while capped solutions converge 12/12 at r = 3e-5 and 1e-5. And it comes from a model that already fails at `R200`. What the run calls "Bratu collapse" is the connected branch disappearing while a second, high-dust solution persists (at r = 3e-5 the first-root solver finds only high-dust static solutions, R500 0.21–0.34, or none), so "static existence" is not a well-defined bound. It is kept as a conditional cluster constraint and not folded into the D5 window.

## Gate 2: Measured X-COP ICM Profiles to $R_{200}$ — Unscreened AeST Dust Route `[X]` (`2026-11-21`)
Script [gate2_xcop_measured_icm.py](gate2_xcop_measured_icm.py) → [GATE2_XCOP_MEASURED_ICM.json](GATE2_XCOP_MEASURED_ICM.json), report [GATE2_XCOP_MEASURED_ICM.md](GATE2_XCOP_MEASURED_ICM.md). Keeps the unscreened single-metric live AeST seat strictly unmodified ($S \equiv 1$, no $x_H$/tidal/Cassini screen, no Cosh concentration, no second metric) and replaces the 2-point $\beta$-model with measured X-COP ICM profiles to $R_{200}$ (Ghirardini et al. 2019 Tables 1, 3, 5 + Eckert et al. 2019 Table 2 + Ettori et al. 2019):

| Measured ICM Model | Solver | All 12 $R_{500}$ | All 12 $R_{200}$ | Direct-11 $R_{200}$ | Verdict |
|---|---|---:|---:|---:|---|
| `M0_beta_control` (`XCOP_RESULT.json` control) | `capped_mu_rv` | `0.8323` (`12/12`) | `0.6196` (`1/12`) | `0.6164` (`1/11`) | FAILS (`R200`) |
| `M1_stacked_measured` (Ghirardini+19 Tab. 5) | `capped_mu_rv` / `free_boundary` | `0.8143` / `0.7993` (`12/12`) | **`0.6083`** (`1/12`) | **`0.6087`** (`1/11`) | **`[X]` FAILS** |
| `M2_vikhlinin_CCNCC` (Tab. 3 CC/NCC) | `capped_mu_rv` / `free_boundary` | `0.8148` / `0.7985` (`12/12`) | **`0.6104`** (`1/12`) | **`0.6109`** (`1/11`) | **`[X]` FAILS** |
| `M3_per_cluster_exact_vikhlinin` ($M_{g500},M_{g200}$ exact) | `capped_mu_rv` / `free_boundary` | `0.8338` / `0.8141` (`12/12`) | **`0.6209`** / `0.6197` (`1/12`) | **`0.6175`** (`1/11`) | **`[X]` FAILS** |
| `M4b_gas_only_no_stars` / `M4c_hard_trunc_at_R200` | `capped_mu_rv` | `0.8511` / `0.8339` (`12/12`) | `0.6366` / `0.6241` (`2/12`) | `0.6292` / `0.6176` (`2/11`) | **`[X]` FAILS** |

Even on directly measured steep outer ICM slopes (`-2.00` to `-3.71` at $R_{200}$), unscreened AeST passes $R_{500}$ (`0.814–0.851`, `12/12`) and still overshoots $R_{200}$ (`0.602–0.637`, `1–2/12`; diagnostic Dirichlet $\Phi(R_{200})=0$ on `M3` still gives `0.6583`, `3/12`). The unscreened hydrostatic AeST dust halo is too extended at $R_{200}$, closing this D10 cluster route as **`[X]`**.
