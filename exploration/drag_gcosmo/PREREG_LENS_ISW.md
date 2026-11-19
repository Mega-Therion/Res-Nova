# Pre-registration: CMB-lensing and late-ISW proxies for the flux-fed drag wall (2026-11-19, before any number)
A full Boltzmann run is out of scope here. Two proxies follow from the model's own background and growth (`flux_codazzi_check.E_coupled`, `growth_coupled`) at each dataset's best fit (κ, h, Ω_m), with ΛCDM refit on the same data as reference.

1. **Lensing amplitude.** S_lens = σ₈Ω_m^0.25, with σ₈ anchored to the early universe (0.811 × D₁/D₁,ref, as in the fσ₈ fits).
   - Compare with Planck 2018 lensing, σ₈Ω_m^0.25 = 0.589 ± 0.020 (arXiv:1807.06210, verified).
   - **Pass** if within 2σ.
   - Approximation: the lensing potential is sourced by G_N ρ_m δ (local Poisson), and the lensing kernel shift from the modified D_A(z) is ignored.
2. **Late-ISW amplitude.** A_ISW ∝ ∫₀³ |d(D(1+z))/dz| dz, as a ratio to ΛCDM on the same data.
   - Planck detects ISW at ~3–4σ (arXiv:1502.01595, verified), so A_ISW ≈ 1 ± 0.3.
   - **Pass** if the ratio is in [0.4, 1.6] (2σ).

**The model survives the proxies** only if both pass for all four dataset fits.
