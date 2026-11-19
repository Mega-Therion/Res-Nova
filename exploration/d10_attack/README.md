# D10 cluster attack, ideas 1–5 (2026-11-19)
Pre-registered in `PREREG.md` (3ff68c6, before any number). Script `d10_attack.py` → `D10_ATTACK.json`. Sanity check: pure-MOND R under μ_std reproduces D10 §2 (median 1.957).

## #1 Nonperturbative solve with the x_H virial boundary
- **Well-posed under μ_std [D].** All 12 clusters converge with u_E > 0 throughout.
  - §9's ill-posedness came from the 25 Mpc compensation radius (μr_c ≈ 26 rad, about 4 oscillations, so g_N crossed zero repeatedly).
  - The virial boundary has μr_v ≈ 2–2.8 rad, under half an oscillation, so there are no zero crossings.
  - So the x_H boundary fixes the well-posedness problem.
- **Result: median R = 0.75** (from 1.96), with 6/12 clusters in [0.7, 1.4]. **FAILS** the pre-registered band [0.8, 1.25] by overshooting.
- **The simple law** g = u + √(a₀u) is near-runaway: 2/12 do not converge, and median R is 0.28. The canonical law is μ_std; the simple law is reported for completeness.

## #2 Two-radius shape test: not usable as a discriminator
- The catalogue M₂₀₀/M₅₀₀ equals its own column 7, which is the NFW-derived ratio (median 1.43). So the observed "shape" largely encodes the NFW fitting assumption.
- The model ratios (μ_std AeST 2.00, pure MOND 1.93) are dominated by extrapolating the cored gas profile beyond r₅₀₀.
- No mechanism can be discriminated with these data. This needs real lensing shear profiles.

## #3 Cosmic dust budget: [X] for the quasi-static mass term as physical
- In AeST the μ² sector is the field's dust-like component.
- The extra mass it adds inside r_v is a median **1.09×** the cosmic dust allowance (Ω_c/Ω_b)·M_b. It exceeds the allowance in **8/12** clusters (maximum 2.8×).
- In this quasi-static treatment the term needs more dust than the universe supplies to those clusters. That matches #1's overshoot: the effect is too strong, not too weak.

## #4 Potential-depth (BK-type) screen: [X], confirming the critic
- Fully screening MOND in clusters leaves Newtonian baryons: median R = **6.83**.
- A BK-style escape needs genuine dark-matter-phase mass. In this theory the only candidate is the AeST dust of #3, so the route reduces to #3.

## #5 2 eV neutrinos: closed for active neutrinos [C]
- KATRIN gives m_ν < 0.45 eV (90% CL). Planck 2018 gives Σm_ν < 0.12 eV, and DESI DR2 is tighter. These are cited from memory and should be re-checked before quoting.
- A 2 eV active neutrino is excluded. A sterile species remains, but CMB N_eff and Σm constraints apply. Recorded as closed for active neutrinos and not pursued.

## Net
- The cluster problem changes character. Once the AeST mass term is solved properly (well-posed, physical boundary), R moves 1.96 → 0.75: **too much mass, by about 25%, and more dust than the cosmic budget allows in 8/12 clusters.**
- A boundary or μ between the two would give R = 1, but choosing it would be tuning.
- Open questions, all [O]:
  - Is the quasi-static limit valid near r_v, where linear and nonlinear regimes meet?
  - Is the r_v boundary right, or should it be the splashback radius?
  - Does a time-dependent (accretion) treatment cut the dust intake?

## Addendum: time-dependent / supply-limited accretion (`PREREG_ACCRETION.md` 5c5bcf5, `accretion.py` → `ACCRETION.json`)
**(a) Static is valid.**
- The AeST dust equilibration time is t_eq = r₅₀₀/c_s, with c_s = √(4πGρ̄₅₀₀)/μ ≈ 2000 km/s.
- t_eq is a median 0.20 of the cluster age since assembly, and below 0.3 for 12/12 clusters.
- Time dependence therefore does not rescue the overshoot. The dust has time to settle into the quasi-static configuration.

**(b) Supply cap: closes in the median, fails the pre-registered spread.**
- Capping each cluster's AeST dust at the cosmic share (Ω_c/Ω_b)·M_b moves median R from 0.75 to **0.84**, inside [0.8, 1.25].
- But only **8/12** clusters land in [0.7, 1.4], against the required 9. **FAILS**, narrowly.
- The misses: A1763 0.60, A2142 0.64 and A1689 0.69 overshoot even after capping; CL-J1226 sits at 1.92 because of its anomalous f_gas.

**Reading.** With a physical boundary, a finite supply and a valid static limit, AeST's own dust sector lands clusters near R ≈ 0.84. That is the closest the corpus has come to closing D10, but it is still outside the pre-registered success criterion. [O]: the per-cluster scatter tracks f_gas and the assumed cored gas profile. Real deprojected gas profiles are the next input.

## #5 bounds: verified against arXiv abstracts (replaces "cited from memory")
- KATRIN, arXiv:2406.13516: m_ν < 0.45 eV (90% CL).
- Planck 2018, arXiv:1807.06209: Σm_ν < 0.12 eV.
- DESI DR2, arXiv:2503.14738: Σm_ν < 0.064 eV (95%, DESI+CMB, ΛCDM).
- A 2 eV active neutrino is excluded on all three.
- A 2 eV sterile species would itself be hot dark matter. It needs ΔN_eff ≈ 1 thermalised, and is constrained by the same CMB+BAO Σm limits unless its abundance is suppressed. Not a route the corpus pursues; recorded as closed.
