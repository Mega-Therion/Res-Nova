# Pre-registration: drag variable-G cosmology (2026-11-19, before any number)

**Model** (Dark Bubble wall with bulk ram-pressure drag; sign +; suction x₀ < 0 also allowed):
- Background: H²(a) = H₀²[Ω_m a⁻³ + Ω_r a⁻⁴ + Ω_Λ]/(1 + x₀a²), with Ω_Λ = 1 + x₀ − Ω_m − Ω_r and x₀ ≡ (1/a_c)². Flat; the closed-bubble curvature is neglected.
- Equivalently G_cosmo(a)/G_N = 1/(1 + x₀a²). Local Poisson uses G_N.
- Growth: δ″ + (2 + d ln H/d ln a)δ′ = 1.5 Ω_m a⁻³ (H₀/H)² δ. Same code for ΛCDM at x₀ = 0.

**Data** (in-repo unless noted):
- DESI DR2 BAO (`desi_gaussian_bao_ALL_GCcomb_*`, full covariance).
- Pantheon+ (zHD > 0.01, STAT+SYS, M marginalised analytically).
- Compressed CMB: early universe standard because x → 0. Priors ω_m = 0.1430 ± 0.0011 and 100θ* = 1.04110 ± 0.00031. r_d = 147.09 (ω_m/0.1430)^−0.255 Mpc; r_s* = 144.43 × the same factor; z* = 1089.9.
- fσ₈: Sagredo, Nesseris & Sapone 2018 (arXiv:1806.10822), 22 points. Diagonal errors; Alcock–Paczynski correction and WiggleZ correlations ignored (stated limitation).
  - σ₈ amplitude handled two ways: (a) free; (b) anchored to the early universe (same primordial δ as a Planck ΛCDM with σ₈ = 0.811).

**Pre-registered reporting and decision.**
- Fit H₀, Ω_m, x₀ (drag) against ΛCDM (x₀ = 0) on BAO+SN+CMB, then add fσ₈.
- Report Δχ², the best x₀, its 2σ interval, G_cosmo/G_N today, and the Δχ² from fσ₈ alone.
- **Favoured** if Δχ²_total ≤ −4 with fσ₈ included. **Excluded** if x₀ = 0 lies inside 2σ, with the bound on |G_cosmo/G_N − 1| today reported. Anything else is **inconclusive**.
