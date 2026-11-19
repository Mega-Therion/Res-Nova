# Pre-registration addendum: time-dependent / supply-limited AeST dust in clusters (2026-11-19, before any number)
Question left open by #1/#3: does finite-time, finite-supply accretion reduce the AeST dust that the quasi-static solve puts in clusters (R = 0.75)?

**(a) Timescale test.**
- Treat the AeST dust as a fluid whose Jeans wavenumber is μ. Its effective sound speed at the cluster is c_s = √(4πGρ̄₅₀₀)/μ, and its equilibration time is t_eq = r₅₀₀/c_s.
- Compare t_eq with the cluster age since assembly, t(z_obs) − t(z_f), where z_f = z_obs + 0.4 (median half-mass assembly offset for massive clusters; stated assumption).
- **Static valid** if t_eq < 0.3 × age for ≥ 9 of 12 clusters.

**(b) Supply cap.**
- Infall cannot deliver more dust than the cosmic share: M_dust(r_v) ≤ (Ω_c/Ω_b)·M_b(r_v).
- For clusters exceeding it, reduce the μ² coupling (the dust response) until the added mass equals the cap, then re-solve the BVP and report median R.
- **Closes** if median R ∈ [0.8, 1.25] with ≥ 9/12 in [0.7, 1.4]. Otherwise **fails**.
