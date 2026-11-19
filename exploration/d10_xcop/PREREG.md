# Pre-registration: D10 AeST cluster test on X-COP (gas measured to R₂₀₀) (2026-11-19, before any number)
**Why.** Every D10 run so far extrapolated the outer gas. X-COP measures gas and total mass out to R₂₀₀ (`xcop_data.tsv`, with provenance).

**Inputs.**
- M_gas(R₅₀₀) = f_gas,500·M_HSE,500 and M_gas(R₂₀₀) = f_gas,200·M_HSE,200.
- Stars: M_star = 0.09·M_gas (X-COP median, Ettori et al. 2019), with the same profile.
- Observed total mass: M_tot (non-thermal-pressure corrected; Eckert et al. 2019).

**Gas profile.** β-model ρ ∝ [1 + (r/r_c)²]^(−3β/2) with r_c = 0.1 R₅₀₀. β is solved so that M_gas(R₂₀₀)/M_gas(R₅₀₀) matches the data, and the normalisation matches M_gas(R₅₀₀). The only extrapolation is from R₂₀₀ to r_v = R₂₀₀(200/177.8)^{1/3} ≈ 1.04 R₂₀₀.

**Model.** μ_std, AeST μ²Φ, Φ(r_v) = 0, shooting. Static, and supply-capped at (Ω_c/Ω_b)·M_b.

**Report.** R₅₀₀ = M_tot,500/M_dyn(R₅₀₀) and R₂₀₀ likewise, for pure MOND, static and capped.

**Decision** (same as before): **closes** if the median R₅₀₀ ∈ [0.8, 1.25] with ≥ 9/12 in [0.7, 1.4], for the capped model. R₂₀₀ is reported as a second, independent radius under the same rule.
