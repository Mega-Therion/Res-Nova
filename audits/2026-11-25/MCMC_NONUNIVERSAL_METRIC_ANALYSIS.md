# Conditional MCMC posterior and non-universal matter metric

## 1. Scope of the simulation

A full empirical posterior cannot be run from the current repository artifacts because the full LLR range time series, covariance, ephemeris nuisance model, MICROSCOPE time-series data, and Ti/Pt sector-fraction table are not present in the working corpus. I therefore ran a reproducible **conditional summary-statistic MCMC**, not a full data analysis.

The sampled toy parameters are

```text
eta_A : active Al/Fe-like composition parameter constrained by the LLR summary,
delta_xi_P = xi_Ti − xi_Pt : non-universal passive metric difference,
```

with unit wall-response normalization `F=1` and model

```text
eta_LLR^model = eta_A,
eta_MIC^model = delta_xi_P.
```

The LLR summary is represented by `0 ± 3.9×10⁻¹⁴`, using the current Res Nova LLR bound as a Gaussian scale. MICROSCOPE uses the published central value `−1.5×10⁻¹⁵` and combined standard deviation

```text
sigma_MIC = sqrt[(2.3×10⁻¹⁵)² + (1.5×10⁻¹⁵)²]
           = 2.7459×10⁻¹⁵.
```

The sampler uses 64 walkers, 30,000 steps, 5,000 burn-in steps, thinning by 10, and seed `20261125`. The implementation and machine-readable output are `run_joint_toy_mcmc.py` and `joint_toy_mcmc_results.json` in this directory.

## 2. Posterior result

The conditional posterior quantiles are:

| Parameter | 2.5% | 16% | Median | 84% | 97.5% |
|---|---:|---:|---:|---:|---:|
| `eta_A` | `−7.71×10⁻¹⁴` | `−3.90×10⁻¹⁴` | `−2.11×10⁻¹⁶` | `3.86×10⁻¹⁴` | `7.59×10⁻¹⁴` |
| `delta_xi_P` with `F=1` | `−6.87×10⁻¹⁵` | `−4.22×10⁻¹⁵` | `−1.50×10⁻¹⁵` | `1.21×10⁻¹⁵` | `3.87×10⁻¹⁵` |

The acceptance fraction was `0.7847`, with 160,000 retained posterior samples. Under this broad-prior summary model,

```text
P(eta_A ≥ 9.02×10⁻³ | summary data) = 0,
```

at the resolution of the retained chain. This is expected: the Res Nova active scan minimum is about `2.31×10¹¹` standard deviations above the adopted LLR scale, so the Gaussian log-likelihood penalty at `eta_A=9.02×10⁻³` is approximately

```text
−1/2 (9.02×10⁻³ / 3.9×10⁻¹⁴)² ≈ −2.67×10²².
```

This quantifies the exclusion in the compressed model; it does not replace a full LLR ephemeris likelihood.

For the unit-normalized passive wall response, the MCMC gives a 95% posterior interval approximately

```text
−6.87×10⁻¹⁵ < delta_xi_P < 3.87×10⁻¹⁵.
```

The interval is centered near the MICROSCOPE central value because the toy model identifies `eta_MIC` directly with `delta_xi_P`. If the actual wall response is `F_ℓ` rather than one, the corresponding coupling is rescaled:

```text
delta_xi_{P,ℓ} = delta_xi_P/F_ℓ.
```

The numerical coupling bound is therefore conditional on the normalization and cannot be interpreted as a measured fundamental metric coupling.

## 3. Non-universal matter metric

A minimal parameterization of a species-dependent passive metric is

```text
g^T_{μν} = g_{μν} + xi_T h_{μν},
```

where `h_{μν}` is the wall-induced perturbation and `xi_T` is the passive coupling of body `T`. Linearizing the point-particle action,

```text
S_T = −m_T c ∫ ds_T,
```

gives a species-dependent force response of the form

```text
κ_T^P = κ_{T,0}^P + xi_T F_wall + O(h²),
```

where `F_wall` includes the wall field, transfer normalization, and source amplitude. For a multipole decomposition,

```text
κ_T^P
 = κ_{T,0}^P + Σ_ℓ xi_{T,ℓ} F_ℓ(ε).
```

The Ti/Pt passive difference is therefore

```text
Δκ_Ti,Pt^P
 = [κ_Ti,0^P − κ_Pt,0^P]
   + Σ_ℓ (xi_{Ti,ℓ}−xi_{Pt,ℓ})F_ℓ(ε).
```

The universal metric limit has `xi_{Ti,ℓ}=xi_{Pt,ℓ}` for every `ℓ`; all wall terms cancel in the differential acceleration. A non-universal metric breaks that cancellation only through

```text
Δxi_{P,ℓ} ≡ xi_{Ti,ℓ}−xi_{Pt,ℓ} ≠ 0.
```

The resulting MICROSCOPE prediction is

```text
eta_MIC
 ≈ eta_0^P + Σ_ℓ Δxi_{P,ℓ}F_ℓ(ε).
```

Higher multipoles change `F_ℓ`, and for an off-center observer can make it large, but they do not create `Δxi_{P,ℓ}` if the metric is universal. In the midpoint case, the rim transfer is balanced for every `ℓ`, so a rim-only mechanism cannot generate Ti/Pt non-universality.

A more realistic species-dependent disformal metric could be written

```text
g^T_{μν}
 = C_T(φ,X)g_{μν}
   + D_T(φ,X)∂_μφ∂_νφ,
```

or with a vector field,

```text
g^T_{μν}
 = C_T g_{μν} + D_T A_μA_ν.
```

Then both `C_T` and `D_T` contribute to `xi_T` after weak-field expansion. A common `C_T` and `D_T` still cancel from Ti/Pt differential acceleration; only the composition-dependent difference in the expanded coefficients survives.

This is outside Res Nova’s live minimal single-metric matter coupling. The repository records disformal matter coupling as `[X]` in the retired branch. Introducing `xi_T`, `C_T`, or `D_T` would therefore be a new model version and would require a new action identity, conservation/Bianchi check, characteristic-speed analysis, and joint LLR–MICROSCOPE gate.

## 4. Active LLR coupling versus passive metric coupling

The MCMC result also demonstrates why the active LLR obstruction cannot simply be reused as a passive MICROSCOPE signal. Let

```text
κ_A^A = Σ_a w_a^A f_a^A,
κ_T^P = Σ_a v_a^P f_a^T.
```

The LLR active parameter depends on `w_a^A` for macroscopic source bodies. The MICROSCOPE difference depends on `v_a^P` and Ti/Pt composition fractions. Equality `w_a=v_a` is a physical hypothesis requiring derivation from the action, not a statistical identification.

Under the non-universal metric parameterization, the joint fit should sample the shared microscopic parameters that generate both `w` and `xi`, rather than independently fitting `eta_A` and `delta_xi_P`. The present MCMC intentionally leaves them independent to show the summary-data constraint and its underdetermination.

## 5. Status

The MCMC is a `[D]` conditional computational result for the stated summary likelihood and priors. It is not an `[E]` empirical reproduction, not a full Res Nova gate, and not evidence that a non-universal metric exists. Its robust conclusions are:

1. The compressed LLR likelihood assigns effectively zero posterior support to the Res Nova active scan minimum `9.02×10⁻³`.
2. With unit wall response, MICROSCOPE requires a Ti/Pt passive metric difference at the few-`10⁻¹⁵` level.
3. For arbitrary wall response, only the weighted combination `Σ_ℓ Δxi_{P,ℓ}F_ℓ` is constrained.
4. Higher multipoles amplify a pre-existing non-universal coupling but cannot bypass Ti/Pt cancellation in a universal matter metric.

## References

[1]: https://arxiv.org/abs/2209.15487 "MICROSCOPE mission final results"
[2]: https://github.com/Mega-Therion/Res-Nova/blob/4ad334721f63781f2b6c832bf33272606a56ce33/exploration/bulk5d/WEP_2507_03748_AUDIT.json "Res Nova WEP audit receipt"
[3]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo"
