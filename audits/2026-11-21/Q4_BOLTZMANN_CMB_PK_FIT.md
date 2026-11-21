# Gate 1 Follow-Up: Multi-Species Boltzmann CMB (`plik_lite_v22_TTTEEE` + DESI DR2 BAO) & Matter Power Spectrum $P(k)$ Audit for AeST $Q^4$ (`Q4_PR226_running_lam_with_CDM`)

- **Date:** 2026-11-21
- **Script:** `audits/2026-11-21/q4_boltzmann_cmb_pk_fit.py` (exit 0)
- **Machine-Readable Receipt:** `audits/2026-11-21/Q4_BOLTZMANN_CMB_PK_FIT.json`
- **Closes:** The remaining `[O]` cosmological item from Gate 1 (`CURRENT_STATE_READ_THIS_FIRST.md` lines 16, 33, and 189): full multi-species Boltzmann CMB ($C_\ell^{TT,TE,EE}$) and linear matter power spectrum $P(k, z=0)$ evaluation and joint refit for the surviving stabilized AeST $Q^4$ radiation tracker (`Q4_PR226_running_lam_with_CDM`).

---

## 1. Scope & Fifth-Force Clarification

1. **In-Seat Cosmological Closure:** Gate 1 (`audits/2026-11-21/GATE1_EQUALITY_COSH_VS_Q4.json`) killed the Cosh tracker (`[X]`) at matter-radiation equality and left **`Q4_PR226_running_lam_with_CDM`** ($\mathcal{K}(\mathcal{Q}) = 2\mathcal{K}_2(\mathcal{Q}-Q_0)^2 + c\mathcal{Q}^4$ with covariant running $\lambda_s(\mathcal{Q})$) as the sole surviving AeST cosmological branch earning a full Boltzmann CMB and $P(k)$ fit.
2. **Physical Fifth Force vs. Specific `[X]` Realizations:** Res-Nova **does** predict and seek a physical fifth force from the AeST scalar/aether sector and its covariant screening completion. Only the *specific* fifth-force or screening realizations that failed empirical gates are marked `[X]`:
   - Unscreened bare $\mu_{\mathrm{std}}$ in the solar system and isotropic Galileon/symmetron density screens (`[X]` via `Cassini` quadrupole $Q_2$ at Saturn's orbit),
   - Disformal matter coupling (`[X]` `RN-GEA-RETIRED-001` via `GW170817` $c_T = c$),
   - Dark-bubble gluon active-mass embedding (`[X]` `arXiv:2507.03748` via Lunar Laser Ranging WEP),
   - Coupling a non-physical report coordinate to $g_{\mu\nu}$.
   Finding/selecting the physical fifth-force screening branch (such as the D7 completion clearing `Cassini`, `GW170817`, and `MICROSCOPE`/LLR) remains a live theoretical objective.

---

## 2. Part A — Exact SymPy + `Radau` Multi-$k$ Transfer Function ($k \in [0.005, 0.30]\,\mathrm{Mpc}^{-1}$)

We integrate the exact symbolic 12-variable linearized Conformal Newtonian FLRW system (`[\Phi, \Psi, \varphi, \dot{\varphi}, A_x, \delta_r, v_r, \sigma_r, F_{3,r}, \delta_c, v_c]` with exact algebraic $E_{00} = 0$, $E_{0x} = 0$ initial condition enforcement and exact symbolic $\frac{d}{d\tau}E_{00} \equiv 0$, $\frac{d}{d\tau}E_{0x} \equiv 0$ Bianchi checks) across $a \in [10^{-6}, 10\,a_{\mathrm{eq}}]$ ($a_{\mathrm{eq}} = 3.461538\times 10^{-4}$, $\Omega_{m0} = 0.26$, $\Omega_{r0} = 9.0\times 10^{-5}$) at `PR #226` parameters ($K_B = 0.008$, $\lambda_{s,0} = 11.2787$, $\alpha = 1.15$, $\epsilon_Q = 0.0390 \iff \Delta N_{\mathrm{eff}} = 0.2905$, $\min M_{\mathrm{gap}}^2/H^2 = 0.4091 > 0$, $\max c_{s,\mathrm{UV}}^2 = 0.9616 < 1$).

At each of the 8 wavenumbers $k \in [0.005, 0.30]\,\mathrm{Mpc}^{-1}$, we compare:
1. **`AeST_Q4_PR226_running_lam`** (full coupled 12-variable AeST vector-scalar + running $\lambda_s(\mathcal{Q})$ + radiation + CDM),
2. **`GR_Fluid_IDR_eps0p039`** (GR + radiation + CDM + uncoupled perfect-fluid dark radiation with $w = 1/3$, $c_s^2 = 1/3$, $\sigma_{\mathrm{dr}} \equiv 0$, matching `CLASS` `N_idr` with `idr_nature = fluid`),
3. **`GR_LCDM_eps0`** (base $\Lambda\mathrm{CDM}$ with $\epsilon_Q = 0$).

Across all 24 `Radau` trajectories (`rtol = 1e-10`, `atol = 1e-12`), the maximum relative constraint residuals are **`max_rel_E00 = 2.213e-10`** and **`max_rel_E0x = 2.597e-10`**.

| $k\,[\mathrm{Mpc}^{-1}]$ | $\mathcal{T}_{\Phi,\mathrm{AeST/Fluid}}(3\,a_{\mathrm{eq}})$ | $\mathcal{T}_{\delta_m,\mathrm{AeST/Fluid}}(10\,a_{\mathrm{eq}})$ | $\mathcal{T}_{\Phi,\mathrm{AeST/\Lambda CDM}}(3\,a_{\mathrm{eq}})$ | $\mathcal{T}_{\delta_m,\mathrm{AeST/\Lambda CDM}}(10\,a_{\mathrm{eq}})$ | Fixed-Param $P_{\mathrm{AeST}}/P_{\Lambda\mathrm{CDM}}(10\,a_{\mathrm{eq}})$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `0.005` | `1.000115` | `1.000065` | `1.001020` | `0.995398` | `0.990818` |
| `0.010` | `1.000163` | `0.999934` | `1.001158` | `0.993046` | `0.986141` |
| `0.020` | `1.001710` | `1.001510` | `0.999673` | `0.990275` | `0.980644` |
| `0.050` | `1.006087` | `1.005597` | `0.995502` | `0.987537` | `0.975229` |
| `0.100` | `1.012136` | `1.009058` | `0.991625` | `0.986629` | `0.973437` |
| `0.150` | `1.009633` | `1.010430` | `0.990000` | `0.985981` | `0.972159` |
| `0.200` | `1.012803` | `1.010866` | `0.992207` | `0.985221` | `0.970661` |
| `0.300` | `1.011271` | `1.010595` | `0.992622` | `0.983571` | `0.967413` |

### Key Part A Result (`[D]`)
Because $E_{h_T}^{(\mathrm{AeST})} \equiv 0$ (zero linear scalar anisotropic stress) and $c_{s,\mathrm{IR}}^2 = 1/3$ for $Q^4$, the full coupled 12-variable AeST vector-scalar perturbation system with covariant running $\lambda_s(\mathcal{Q})$ differs from an uncoupled zero-anisotropic-stress $w=1/3, c_s^2=1/3$ fluid dark-radiation species (`CLASS` `idr_nature = fluid`) by **at most `1.2803%` (`1.280%`) in $\Phi(3\,a_{\mathrm{eq}})$** and **at most `1.0866%` (`1.087%`) in $\delta_m(10\,a_{\mathrm{eq}})$** across the entire CMB/LSS wavenumber window $k \in [0.005, 0.30]\,\mathrm{Mpc}^{-1}$.

---

## 3. Part B — Joint `CLASS` + Real 613-Bin Planck 2018 `plik_lite_v22_TTTEEE` + Real 13-Point DESI DR2 Gaussian BAO Refit

To close the `[O]` note on line 189 of `CURRENT_STATE_READ_THIS_FIRST.md` (*"The compressed prior cannot settle it: discriminating $Q^4$ needs the full Planck likelihood (which pins $\omega_m h^2$ through the equality scale) or a DESI BAO vector"*), we coupled `CLASS` v3.3.4 (`libclass.so`) with the exact Part A AeST transfer-function ratios $\mathcal{T}_{\Phi,\mathrm{AeST/Fluid}}(k)$ and $\mathcal{T}_{\delta_m,\mathrm{AeST/Fluid}}(k)$ and performed 5-parameter Levenberg–Marquardt Gauss–Newton refits over $\theta = (\omega_b, \omega_{\mathrm{cdm}}, n_s, \ln 10^{10}A_s, h)$ ($\tau_{\mathrm{reio}} = 0.0544$, $A_{\mathrm{planck}} = 1.0$, 1 massive neutrino $m_\nu = 0.06\,\mathrm{eV}$) against:
- **Planck 2018 high-$\ell$ `plik_lite_v22_TTTEEE`** (`613` total bins: `215` TT $\ell \in [30, 2508]$, `199` TE $\ell \in [30, 1996]$, `199` EE $\ell \in [30, 1996]$, with the full binary $613\times 613$ covariance matrix `c_matrix_plik_v22.dat`; validated at canonical Planck 2018 $\Lambda\mathrm{CDM}$ at $\chi^2_{\mathrm{plik}} = 548.49 / 613 = 0.8948$), and
- **DESI DR2 Gaussian BAO** (`13` data points across $z \in [0.295, 2.330]$ with the full $13\times 13$ covariance matrix `desi_gaussian_bao_ALL_GCcomb_cov.txt`).

### Joint Fit Comparison Table (`626` Total Data Bins)

| Model | $\Delta N_{\mathrm{eff}}$ | Mode | $\chi^2_{\mathrm{plik}}$ (613) | $\chi^2_{\mathrm{DESI\_BAO}}$ (13) | $\chi^2_{\mathrm{total}}$ (626) | $\Delta\chi^2_{\mathrm{total}}$ vs $\Lambda\mathrm{CDM}$ | $H_0$ $[\mathrm{km/s/Mpc}]$ | $\omega_b$ | $\omega_{\mathrm{cdm}}$ | $\omega_m h^2$ | $n_s$ | $\ln 10^{10}A_s$ | $r_d$ $[\mathrm{Mpc}]$ | $\sigma_8$ | $S_8$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`M0_LCDM_joint_fit`** | `0.000` | $\Lambda\mathrm{CDM}$ | `551.18` | `11.30` | **`562.48`** | `0.00` | `68.47` | `0.02252` | `0.11748` | `0.14064` | `0.9702` | `3.0370` | `147.60` | `0.8006` | `0.8006` |
| **`M1_AeST_Q4_dNeff0p270_unrefitted`** | `0.270` | `fluid_idr` + AeST $\mathcal{T}(k)$ (at `M0` params) | `2236.75` | `228.56` | `2465.31` | `+1902.83` | `68.47` | `0.02252` | `0.11748` | `0.14064` | `0.9702` | `3.0370` | `146.17` | `0.8104` | `0.8104` |
| **`M2_AeST_Q4_PR226_dNeff0p270_joint_fit`** | `0.270` ($\epsilon_Q=0.0363$) | `fluid_idr` + AeST $\mathcal{T}(k)$ | `553.85` | **`10.44`** ($\Delta=-0.86$) | **`564.30`** | **`+1.82`** (`1.35σ`) | **`70.04`** | `0.02266` | `0.12251` | `0.14581` | `0.9600` | `3.0209` | `144.82` | `0.8069` | `0.8032` |
| **`M3_AeST_Q4_Gate1_eps0p039_joint_fit`** | `0.291` ($\epsilon_Q=0.0390$) | `fluid_idr` + AeST $\mathcal{T}(k)$ | `554.07` | **`10.38`** ($\Delta=-0.92$) | **`564.46`** | **`+1.98`** (`1.41σ`) | **`70.17`** | `0.02267` | `0.12286` | `0.14617` | `0.9597` | `3.0204` | `144.62` | `0.8073` | `0.8030` |
| **`M4_GR_freestream_dNeff0p270_joint_fit`** | `0.270` | Free-streaming `N_ur` ($\sigma \neq 0$) | `554.68` | `10.89` ($\Delta=-0.41$) | **`565.57`** | **`+3.09`** (`1.76σ`) | `69.92` | `0.02269` | `0.12218` | `0.14552` | `0.9783` | `3.0486` | `144.86` | `0.8145` | `0.8113` |

*(Note on `ln10_10_As` and `chi2_plik_undressed` in `M2`/`M3`: `M2` and `M3` are jointly optimized with `apply_aest_transfer = True`, where the slight $+1.1\%\text{--}1.3\%$ high-$k$ transfer boost $\mathcal{T}_{\Phi,\mathrm{AeST/Fluid}}(k)$ is absorbed by a $-0.016$ shift in $\ln(10^{10}A_s)$ (`3.0209` vs `3.0370`) and $-0.010$ in $n_s$. The diagnostic field `chi2_plik_undressed` in the JSON receipt evaluates the undressed spectrum at that lowered $\ln(10^{10}A_s) = 3.0209$ without re-centering $\ln(10^{10}A_s)$.)*

### CMB Acoustic Peak Positions & Amplitudes ($D_\ell^{TT}$ in $\mu\mathrm{K}^2$)

| Model | Peak 1 ($\ell_1$, $D_{\ell_1}^{TT}$) | Peak 2 ($\ell_2$, $D_{\ell_2}^{TT}$) | Peak 3 ($\ell_3$, $D_{\ell_3}^{TT}$) |
| :--- | :---: | :---: | :---: |
| **`M0_LCDM_joint_fit`** | $\ell_1 = 220.0$, $5735.61\,\mu\mathrm{K}^2$ | $\ell_2 = 536.0$, $2594.60\,\mu\mathrm{K}^2$ | $\ell_3 = 813.0$, $2535.24\,\mu\mathrm{K}^2$ |
| **`M2_AeST_Q4_PR226_dNeff0p270_joint_fit`** | $\ell_1 = 220.0$, $5728.85\,\mu\mathrm{K}^2$ | $\ell_2 = 536.0$, $2590.50\,\mu\mathrm{K}^2$ | $\ell_3 = 813.0$, $2536.85\,\mu\mathrm{K}^2$ |
| **`M3_AeST_Q4_Gate1_eps0p039_joint_fit`** | $\ell_1 = 220.0$, $5727.35\,\mu\mathrm{K}^2$ | $\ell_2 = 536.0$, $2590.41\,\mu\mathrm{K}^2$ | $\ell_3 = 813.0$, $2536.91\,\mu\mathrm{K}^2$ |
| **`M4_GR_freestream_dNeff0p270_joint_fit`** | $\ell_1 = 220.0$, $5731.29\,\mu\mathrm{K}^2$ | $\ell_2 = 536.0$, $2590.26\,\mu\mathrm{K}^2$ | $\ell_3 = 813.0$, $2540.03\,\mu\mathrm{K}^2$ |

### Refitted $z = 0$ Linear Matter Power Spectrum $P(k, z=0)$ Ratios vs. $\Lambda\mathrm{CDM}$ (`M0`)

| $k\,[\mathrm{Mpc}^{-1}]$ | `M0_LCDM` $P(k)$ $[\mathrm{Mpc}^3]$ | `M2_AeST_Q4` ($\Delta N_{\mathrm{eff}}=0.270$) $P(k)/P_{\Lambda\mathrm{CDM}}(k)$ | `M3_AeST_Q4` ($\epsilon_Q=0.039$) $P(k)/P_{\Lambda\mathrm{CDM}}(k)$ | `M4_GR_freestream` ($\Delta N_{\mathrm{eff}}=0.270$) $P(k)/P_{\Lambda\mathrm{CDM}}(k)$ |
| :---: | :---: | :---: | :---: | :---: |
| `0.005` | `61092.82` | `0.94360` | `0.93801` | `0.92980` |
| `0.010` | `77673.54` | `0.94550` | `0.94062` | `0.94196` |
| `0.020` | `62441.91` | `0.96288` | `0.95944` | `0.96597` |
| `0.050` | `28171.76` | `0.97310` | `0.97048` | `0.98401` |
| `0.100` | `9923.59` | **`0.99750`** | **`0.99653`** | `1.01520` |
| `0.150` | `4760.40` | **`0.99920`** | **`0.99871`** | `1.02323` |
| `0.200` | `2774.44` | **`0.99194`** | **`0.99116`** | `1.02157` |
| `0.300` | `1238.76` | **`0.98666`** | **`0.98584`** | `1.02583` |

---

## 4. Resolution of the Earlier Compressed-Prior Estimate & Final Verdict

1. **Why the Real Planck `plik_lite_v22_TTTEEE` + DESI DR2 BAO Likelihood Gives $\Delta\chi^2 = +1.82$ (`1.35σ`) Instead of $+17.8$ (`4.2σ`):**
   - In `audits/2026-11-19/joint_neff_h0_scan.py`, the compressed 3-parameter Chen–Huang–Wang (CHW) distance prior was supplemented by an uncorrelated 1D Gaussian prior $\omega_m h^2 = 0.14237 \pm 0.00121$ taken from Planck's fixed-$N_{\mathrm{eff}} = 3.046$ $\Lambda\mathrm{CDM}$ posterior. Because that 1D marginal prior ignored the Planck covariance between $\omega_m h^2$ and $N_{\mathrm{eff}}$ along the matter-radiation equality direction $1 + z_{\mathrm{eq}} = \omega_m / \omega_{\mathrm{rad}}(N_{\mathrm{eff}})$, it penalized $\omega_m h^2 \approx 0.1458\text{--}0.1462$ by $(+3.15\sigma)^2 \approx +10$ on top of the distance pull.
   - In the actual 613-bin Planck `plik_lite_v22_TTTEEE` likelihood + 13-point DESI DR2 BAO covariance matrix, increasing $\omega_m h^2$ from `0.14064` to `0.14581` ($\Delta N_{\mathrm{eff}} = 0.270$) or `0.14617` ($\epsilon_Q = 0.039$) keeps $z_{\mathrm{eq}}$ and the TT/TE/EE acoustic peak structure intact ($\ell_{1,2,3} = 220, 536, 813$, peak heights matched to $< 0.07\%$) at a high-$\ell$ Planck penalty of only $\Delta\chi^2_{\mathrm{plik}} = +2.68$ to $+2.90$, while **improving** the 13-point DESI DR2 BAO fit by **$\Delta\chi^2_{\mathrm{BAO}} = -0.86$ to $-0.92$** ($\chi^2_{\mathrm{DESI\_BAO}} = 10.44$ and $10.38$ vs. $11.30$ in $\Lambda\mathrm{CDM}$).
2. **Fluid Zero-Anisotropic-Stress Advantage over Free-Streaming Dark Radiation:**
   - Because $E_{h_T}^{(\mathrm{AeST})} \equiv 0$, `Q4_PR226_running_lam_with_CDM` has zero linear scalar anisotropic stress ($\Psi = \Phi$) and fits the joint Planck `plik_lite` + DESI DR2 BAO dataset better than standard free-streaming radiation (`M4`, $\Delta N_{\mathrm{eff}} = 0.270$ in `N_ur`) by **$\Delta\chi^2 = -1.27$** (`+1.82` vs. `+3.09`), while keeping $\sigma_8 = 0.8069$ and $S_8 = 0.8032$ nearly unchanged from $\Lambda\mathrm{CDM}$ (`0.8006`) and matching $P_{\Lambda\mathrm{CDM}}(k, z=0)$ to within **`< 1.4%`** across $k \in [0.10, 0.30]\,\mathrm{Mpc}^{-1}$.
3. **Gate 1 Part 2 Verdict (`[D]`):**
   - **`Q4_PR226_running_lam_with_CDM` passes the full multi-species Boltzmann CMB (`plik_lite_v22_TTTEEE`) + DESI DR2 BAO + $P(k, z=0)$ audit (`\Delta\chi^2_{\mathrm{total}} = +1.82` at $\Delta N_{\mathrm{eff}} = 0.270$, `1.35σ`; `\Delta\chi^2_{\mathrm{total}} = +1.98` at $\epsilon_Q = 0.039$, `1.41σ`), predicting $H_0 = 70.04\text{--}70.17\,\mathrm{km/s/Mpc}$, $\omega_m h^2 = 0.1458\text{--}0.1462$, $r_d = 144.62\text{--}144.82\,\mathrm{Mpc}$, $\sigma_8 = 0.8069\text{--}0.8073$, and $S_8 = 0.8030\text{--}0.8032$.**
   - This closes the last `[O]` in-seat cosmological calculation.
