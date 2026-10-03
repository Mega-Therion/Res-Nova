# Preregistered Experiments E4–E7: Free Ceiling Parameter Space

**Status:** protocol draft; commit and data-freeze before any held-out run  
**Scope:** empirical testing of a free ceiling parameter \(\Omega_f\), its evolution exponent \(n\), and its coupling to independently measured galactic and cosmological observables.  
**Claim boundary:** these experiments test predictive adequacy and parameter identifiability. They do not test consciousness, agency, or a fundamental interpretation of \(\Omega_f\).

> **Intake notes, 2026-10-03 (Claude Code).** These must be resolved before the freeze commit:
> 1. **Placement.** This is Res-Nova cosmology, so it lives here, not in Nova-Conscientia as the bundle planned.
> 2. **Not blind for BAO + SN.** The O3 route has already fitted these ceiling models to DESI + Pantheon+/DES-Y5, found
>    n ≈ 1.25, and tried about a dozen shape variants afterwards (`O3_HORIZON_LANDING_ROUTE_2026-09-28.md`).
>    Confirmatory weight is limited to what is new: the clik-based Planck likelihood and the SPARC coupling.
> 3. **The SPARC sector as specified cannot identify a₀.** With global Yd, Yb, fd and σ_v, the global distance scale fd
>    absorbs a₀. Between H₀ = 60 and 90, fd moves from 0.695 to 1.029 and the SPARC profile log-likelihood changes by
>    only 4.7 (measured; `scripts/run_joint_cobaya.py`, "Known limitation"). Fix fd = 1, or use per-galaxy distances
>    with their published errors, before freezing.
> 4. **The compressed CMB block is miscalibrated** (χ²_CMB = 47.5 at Planck's own best fit;
>    `DELTA_CHI2_FREE_CEILING_ANALYSIS.md`). Do not use it as "calibration evidence" until it is fixed.
> 5. M1's fixed Ω_f = √0.91 is κ = 0.9539.
> 6. **Compute.** Each likelihood evaluation runs CAMB, about 1 s on this CPU-only machine. Four chains × 50,000 samples per
>    model is days of wall time per model, which is feasible free but slow. The 48 h infrastructure ceiling below will be
>    hit, so set it with this in mind before freezing.

## Common preregistration rules

All analysis code, task/data manifests, model versions, parameter bounds, nuisance priors, random seeds, convergence thresholds, stopping rules, and primary endpoints must be committed before the evaluation data or chain summaries are inspected. The existing compressed-prior results are calibration evidence only; they cannot be used to retune bounds or select the reported model.

Every run must retain the complete chain or nested-sampling points, likelihood components, proposal settings, rejected samples, convergence diagnostics, posterior predictive draws, and a receipt containing the Planck archive hash, Planck code version, SPARC manifest hash, external-data hashes, and source commit. A failed chain, divergent transition, or non-finite likelihood is retained as a failure and not silently removed.

The model comparison set is fixed in advance:

- **M0:** flat ΛCDM with \(\Omega_m,h,\omega_b\) free.
- **M1:** fixed \(\Omega_f=\sqrt{0.91}\), fixed \(n\in\{0.5,1,2\}\), with \(h,\omega_b\) free.
- **M2:** free \(\Omega_f\), fixed \(n\in\{0.5,1,2\}\), with \(h,\omega_b\) free.
- **M3:** free \(\Omega_f\) and \(n\), with \(h,\omega_b\) free.

M3 is the exploratory model, not the default winner. It must be compared using held-out predictive scores and complexity-aware criteria, not minimum \(\chi^2\) alone.

## E4 — Global free-ceiling scan

### Question
Is there a localized, reproducible region of \((\Omega_f,n)\) that improves held-out cosmological predictions relative to flat ΛCDM after accounting for parameter complexity?

### Frozen design

Use the full Planck TT+TE+EE+low-ℓ likelihood, DESI BAO, Pantheon+SH0ES, and the 175-galaxy SPARC rotation-curve likelihood. The primary cosmological domain is \(0.70\leq\Omega_f\leq0.999\) and \(0.25\leq n\leq4\). Use log-uniform prior density in \(n\), uniform prior density in \(\Omega_f\), and broad but finite priors \(50<H_0<90\), \(0.015<\omega_b<0.03\). The SPARC sector uses the predeclared global \(Y_d\sim N(0.5,0.125^2)\), \(Y_b\sim N(0.7,0.175^2)\), intrinsic velocity scatter \(\sigma_v>0\), and distance-scale nuisance treatment specified in the joint-run config.

The primary endpoint is the leave-one-dataset-out predictive score summed over the held-out Planck, BAO, SN, and SPARC blocks. The secondary endpoint is \(\Delta\mathrm{AIC}\) relative to M0. Report \(\Delta\mathrm{BIC}\), approximate marginal likelihood diagnostics, and posterior predictive residuals.

The chain must use at least four independent chains, \(R-1<0.01\), effective sample size > 1,000 for each primary parameter, and no unresolved divergent transitions. Stop only after convergence and 50,000 post-burn samples per model or after a predeclared infrastructure ceiling of 48 hours; a time-out is inconclusive.

### Decision rule

E4 supports a free-ceiling region only if the posterior predictive score improves over M0 with a 95% bootstrap interval excluding zero and \(\Delta\mathrm{AIC}< -6\). A result that improves in-sample \(\chi^2\) but fails either criterion is classified as **overfit/no predictive support**.

## E5 — Identifiability and degeneracy experiment

### Question
Are \(\Omega_f\) and \(n\) separately identifiable, or does the data constrain only a lower-dimensional combination such as \(w_0\) or an integrated distance shift?

### Frozen design

Run M2 and M3 with identical data, nuisance priors, and sampler budgets. Repeat M3 under three prior boxes: the primary domain above, a narrow local box \(\Omega_f\in[0.90,0.99], n\in[0.5,2]\), and a stress box \(\Omega_f\in[0.70,0.999], n\in[0.05,10]\). Do not choose the box after seeing posterior plots.

The primary endpoint is the rank correlation and posterior covariance condition number for \((\Omega_f,n)\), with a prespecified identifiability flag if the 95% highest-density region reaches two or more domain boundaries or if the effective posterior dimension is less than 1.5. Secondary endpoints are posterior widths for \(w_0,w_a,H_0\) and the change in held-out score.

A boundary-hitting posterior is not evidence for a physical boundary. It is reported as non-identification unless the posterior predictive score also improves in the independent block.

## E6 — Cross-dataset robustness and tension localization

### Question
Does the free ceiling improve all data blocks coherently, or does it trade one block against another?

### Frozen design

Fit M0, M1, M2, and M3 to each leave-one-block-out combination: Planck-only, BAO-only, SN-only, SPARC-only, Planck+BAO, Planck+SN, Planck+SPARC, and all blocks. Use the same prior and nuisance definitions in every fit. The primary endpoint is the sign and magnitude of the held-out block log predictive density.

Report the vector of blockwise \(\Delta\chi^2\) values and the maximum opposing shift. Apply Holm correction across the four primary block families. A model is coherent only if no block’s held-out score degrades by more than 4 units while the aggregate score improves.

## E7 — Posterior predictive falsification

### Question
Do posterior draws from the free-ceiling model reproduce observables that were not used to select the best parameter point?

### Frozen design

Reserve the SPARC galaxy split by galaxy ID before fitting: 80% training and 20% held-out, stratified by rotation-curve point count and morphology flag. Reserve one cosmological block, selected by a fixed hash of the protocol commit, as the held-out block. Fit on the remaining data and generate at least 1,000 posterior predictive draws for each held-out galaxy and cosmological observable.

The primary endpoint is the held-out posterior predictive coverage of 68% and 95% intervals. The model fails if coverage is below 55% for the nominal 68% interval or below 85% for the nominal 95% interval, after accounting for the predeclared stratification. Secondary endpoints are calibration of residual means, tail exceedance rate, and posterior predictive checks of the BAO/SN/CMB summary residuals.

## Multiplicity, reporting, and interpretation

E4–E7 have four primary experiments. The global confirmatory claim uses Holm-adjusted \(\alpha=0.05\); exploratory plots and parameter maps are labeled separately. Report all model fits, including non-converged and boundary-hitting fits, with the reason and retained chain path.

A favorable result supports only the statement that the tested free-ceiling parameterization has predictive performance under the specified data and priors. It does not establish a unique physical mechanism, derive \(\Omega_f\) from first principles, resolve the Hubble tension, or imply that a small \(\Delta\chi^2\) is scientifically meaningful without predictive replication.
