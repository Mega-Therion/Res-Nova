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

## Addendum 2: Tidal-QUMOND dust coupling, free-boundary n=1 polytrope, 4th quadrant (BK screen + dust), splashback pole, and ICM outer slope (`PREREG_POLYTROPE_4QUAD.md` a4db5e0b, `polytrope_4quad.py` → `POLYTROPE_4QUAD.json`)

**Symbolic `[D]` (SymPy Euler–Lagrange on `tidal_aest/normalization_kb.py` + $\mathcal{K}_2(\mathcal{Q}-Q_0)^2$):**
- Adding AeST's $\mathcal{K}_2(\mathcal{Q}-Q_0)^2$ dust sector with stationary shift-symmetry chemical potential $\Phi_0 = \mu_c/Q_0$ preserves $\Psi = \Phi$ ($\gamma = 1$, lensing = dynamics) identically.
- The dust source $\mu^2(\Phi_0 - \Phi)$ enters the auxiliary shadow potential equation ($\nabla\cdot\mathbf{g}_\psi = 4\pi G_N\rho_b + \mu^2(\Phi_0 - \Phi)$), breaking triangularity and feeding AeST dust directly into the MOND operator.
- In the weak-field regime ($\delta Q \ll Q_0$), $\mathcal{K}(\mathcal{Q}) = \mathcal{K}_2(\mathcal{Q}-Q_0)^2$ is an exact $n = 1$ Lane–Emden polytrope: $P(\rho) = (2\pi G_N/\mu^2)\rho^2$, $w(\rho) = 2\pi G_N\rho/\mu^2$, and exact local sound speed $c_s^2(\rho) = \delta Q/(Q_0 + \delta Q) \approx 4\pi G_N\rho/\mu^2$.
- **Sound-speed regime audit:** Inside collapsed cores ($\rho \sim \rho_{500}$), $c_{s,\mathrm{core}}$ has median **2072 km/s** (matching `accretion.py`'s core acoustic equilibration check), whereas at the cosmic background dark-matter density $\bar{\rho}_c(z)$ exterior to clusters, $c_{s,\mathrm{bg}}(z)$ has median **56.7 km/s** ($42.0\,\mathrm{km/s}$ at $z = 0$), giving median infall Mach number **$\mathcal{M} = 29.2$** (hypersonic cold-dust infall onto a pressure-supported $n = 1$ polytrope core).

**Pre-registered numerical tests (12 Corasaniti+2021 clusters, fixed universal $\mu = 1/0.9895\,\mathrm{Mpc}$, zero tuned parameters):**
1. **T1 (MOND ON + fixed-$\mu$ free-boundary $n = 1$ polytrope, baseline $\beta = 2/3$):** Fixing universal $\mu$ and adjusting only the chemical potential $\Phi_0$ (free edge $R_{\mathrm{edge}} \le r_v$ where $\rho_{\mathrm{dust}} \to 0$) to cap dust at $5.36\,M_b(r_v)$ gives median $R = \mathbf{0.835}$, **7/12** in $[0.7, 1.4]$, max budget ratio $1.000$ — **FAILS** (slightly worse than `accretion.py`'s per-cluster $\mu$-rescaling because keeping $\mu$ fixed compresses the capped supply inside $R_{\mathrm{edge}} < r_v$).
2. **T2 (Untested 4th quadrant — BK cluster screen `MOND OFF` + AeST $n = 1$ polytrope dust): `[X]` (FAILS).**
   - Uncapped (T2a) and capped (T2b) coincide identically (`0/12` capped): median $R = \mathbf{3.114}$, **1/12** in $[0.7, 1.4]$, median dust share only **$0.228\times$** cosmic budget (max $0.84\times$), unchanged across $\beta \in \{2/3, 0.85, 1.0\}$ ($R = 3.11\text{--}3.14$, `1/12`).
   - **Mechanism:** Without MOND deepening $\Phi(r)$, the Newtonian baryon well is $3\text{--}5\times$ shallower, so hydrostatic AeST dust pulls in only ~23% of the cosmic share. This completes the 2×2 matrix `{MOND ON/OFF} × {dust ON/OFF}`: turning off MOND in clusters fails both without dust ($R = 6.83$) and with static AeST dust ($R = 3.11$).
3. **T3 (Splashback boundary & Lane–Emden pole $R_{\mathrm{LE}} = \pi/\mu = 3.109\,\mathrm{Mpc}$): `[D]` structurally unstable.**
   - Replacing $r_v$ ($\max \mu r_v/\pi = 0.90$) by the splashback boundary breaks **5/12** clusters at $1.4\,r_{200}$ and **11/12** clusters at $1.8\,r_{200}$, in exact 1-to-1 correspondence with crossing $\mu R_{\mathrm{out}} \ge \pi$. The uncapped Dirichlet gauge $\Phi(R_{\mathrm{out}}) = 0$ is only well-posed at $r_v$ because $r_v < R_{\mathrm{LE}}$ for these 12 clusters; by contrast, the free-boundary polytrope (`T1`) truncates dust at $R_{\mathrm{edge}} < R_{\mathrm{LE}}$ independently of the outer box.
4. **T4 (ICM outer-slope sensitivity, $\rho_b \propto (1+(r/r_c)^2)^{-3\beta/2}$, identically normalized to $f_{\mathrm{bar}} M_{500}$ inside $r_{500}$):**
   - $\beta = 2/3$ ($M_b(r_v)/M_b(r_{500}) = 1.69$, $r^{-2}$ tail): T1 median $R = 0.835$, **7/12** in $[0.7, 1.4]$ (`FAILS`).
   - $\beta = 0.85$ ($M_b(r_v)/M_b(r_{500}) = 1.39$): T1 median $R = 0.860$, **8/12** in $[0.7, 1.4]$ (`FAILS`).
   - $\beta = 1.00$ ($M_b(r_v)/M_b(r_{500}) = 1.23$, realistic $r^{-3}$ outer ICM slope): T1 median $R = \mathbf{0.875}$, **10/12** in $[0.7, 1.4]$ (**`CLOSES`** with zero cosmic-budget violations).
   - **Honest verdict:** D10 stays **`[O]`** (T1 fails on the repo's baseline $\beta = 2/3$ profile), but T4 proves quantitatively that the entire gap between `FAILS (7/12)` and `CLOSES (10/12)` lies inside the unmodeled outer ICM gas slope ($M_b(r_v)/M_b(r_{500})$ shifting $+37\%$ between $\beta = 1.0$ and $\beta = 2/3$). Real deprojected X-ray gas profiles out to $r_v$ are the decisive next input.

## Addendum: measured ACCEPT gas profiles (`PREREG_ACCEPT.md` 50d1ced, `accept_rerun.py` → `ACCEPT_RERUN.json`)
- **Data.** 11/12 clusters have deprojected n_e(r) in ACCEPT (Cavagnolo et al. 2009); the subset with provenance is in `02_galaxy_dynamics/clusters/accept_d10_subset.dat`. Pure MOND on the measured gas gives median R = 2.15, reproducing the classic ~2× gap.
- **Result.** Static median R = 0.69 (4/11 in band). Supply-capped median R = 0.80 (6/11 in band). **Both FAIL** the pre-registered criterion (≥ 9/11).
- **Coverage, the decisive caveat.** The ACCEPT profiles reach only a median **0.59 r₅₀₀** (range 0.24–0.83). Everything beyond, including r₅₀₀ itself, is a power-law extrapolation.
  - Two clusters have unphysically shallow fitted outer slopes: A1763 β = 0.87 and A2034 β = 1.01, against the typical 2–3. Their gas mass keeps rising, and they are the worst overshooters (R = 0.36 and 0.69).
  - So "measured gas" here replaces the assumed core shape but still extrapolates the outer gas that dominates the cluster mass at r₅₀₀–r_v.
- **Next input needed [O].** Gas profiles measured out to ≳ r₂₀₀, i.e. joint X-ray+SZ profiles such as X-COP (Ghirardini et al. 2019). X-COP overlaps D10 only at A2142, so it would need a re-matched lensing sample.

**Overall D10 status after today.**
- AeST's dust sector, solved properly (well-posed, physical boundary, valid static limit, cosmic supply cap), turns the pure-MOND deficit (R ≈ 2) into an overshoot.
- Median R sits at 0.75–0.84 across three baryon models, all close to but outside the pre-registered success criterion.
- The residual is governed by the outer gas, which no profile used here actually measures.
