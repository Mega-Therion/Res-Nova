# Finite-$H/k$ Radiation-Coupled FLRW Perturbation Transfer Audit (2026-11-20)

Closes the finite-$H/k$ horizon-crossing open boundary from [`COUPLED_2X2_FLRW_STABILITY.json`](COUPLED_2X2_FLRW_STABILITY.json) (`C5`) via exact SymPy derivations and stiff `Radau` horizon-crossing integrations in [`flrw_finite_hk_radiation_transfer.py`](flrw_finite_hk_radiation_transfer.py) (`exit 0`, receipt [`FLRW_FINITE_HK_RADIATION_TRANSFER.json`](FLRW_FINITE_HK_RADIATION_TRANSFER.json)).

## 1. Exact Symbolic Derivation & Bianchi Identities (`[D]`)
1. **Zero Linear Scalar Anisotropic Stress ($\Psi = \Phi$):** Varying the covariant $O(\epsilon^2)$ FLRW AeST action wrt traceless spatial scalar strain $h_T$ yields $E_{h_T}^{(\mathrm{AeST})} \equiv 0$ identically around flat homogeneous FLRW ($\bar{A}_i = \partial_i\bar{\phi} = 0$), so scalar perturbations obey $\Psi = \Phi$ at $O(\epsilon)$ in conformal Newtonian gauge with radiation.
2. **Exact Bianchi Conservation Gate:** Symbolically differentiating both the Hamiltonian ($E_{00}$) and momentum ($E_{0x}$) constraints wrt conformal time $\tau$ and substituting the dynamical equations ($E_\Psi, E_\varphi, E_{v_A}$, radiation fluid) and background FLRW equations leaves $\frac{d}{d\tau}E_{00} \equiv 0$ and $\frac{d}{d\tau}E_{0x} \equiv 0$ identically for arbitrary $U(\bar{Q})$ and time-dependent $\lambda_s(\bar{Q}(\tau))$.
3. **Sub-Horizon Limit:** Setting $\mathcal{H} \to 0, a \to 1, \Phi \to 0$ recovers the exact coupled $2\times 2$ characteristic polynomial of [`coupled_2x2_flrw_stability.py`](coupled_2x2_flrw_stability.py).

## 2. Horizon-Crossing Integration Results ($x = k\tau \in [0.05, 50]$, `Radau`)

| Case | $M_{\mathrm{gap}}^2/H^2$ range | $\max c_{s,\mathrm{UV}}^2$ | Max $|E_{00}|, |E_{0x}|$ rel. resid. | Horizon-Crossing Outcome (`[D]`) |
|---|---|---|---|---|
| **1. Pure radiation GR control** ($k=0.2$) | — | — | `1.53e-09`, `6.76e-10` | Matches exact analytic Bessel solution to **`5.76e-09`**. |
| **2. SZ21 Cosh const $\lambda_s = 0$** ($k=0.02$) | `[-5.53, +29.5]` | `4.0e-06` | `5.31e-11`, `7.85e-10` | Early $M_{\mathrm{gap}}^2 < 0$ band (`a_* = 1.07e-4`) before crossing back positive near equality; enters dust domination ($\Phi/\Phi_{\mathrm{rad,GR}} = 152.1$, $\delta_r/\delta_{r,\mathrm{GR}} = 0.634$). |
| **3a. SZ21 Cosh running $\lambda_s(\mathcal{Q})$** ($k=0.02$) | `[+0.0176, +35.8]` | `0.0101` | `3.22e-11`, `7.38e-10` | Eliminates early $M_{\mathrm{gap}}^2 < 0$ completely; subluminal and stable ($\delta_r/\delta_{r,\mathrm{GR}} = 0.635$). |
| **3b. PR #226 Cosh const $\lambda_s = 11.2787$** ($k=0.2$) | `[-258.2, -0.70]` | `1.7e-05` | `8.29e-11`, `3.13e-10` | **`[X]` Exponential runaway:** `max|Phi| = 1.34e+07`, `max|delta_r| = 1.74e+07`, `15.42 / e-fold` growth. |
| **3b. PR #226 Cosh running $\lambda_s(\mathcal{Q})$** ($k=0.2$) | `[+361.9, +1.30e+05]` | `0.5000` | `3.81e-11`, `1.12e-10` | **Stabilized (`[D]`):** bounded oscillations (`final Phi = 0.0306`, $\delta_r/\delta_{r,\mathrm{GR}} = 0.854$). |
| **4. $Q^4$ PR #226 const $\lambda_s = 11.2787$** ($\epsilon_Q=0.039$) | `[-18.77, -17.24]` | `0.5783` | `4.58e-11`, `7.79e-11` | **`[X]` Exponential runaway:** `max|Phi| = 4.86e+04`, `max|delta_r| = 1.95e+05`, `2.84 / e-fold` growth. |
| **5a. $Q^4$ window $K_B=0.085$, const $\lambda_s$** | `[+0.016, +0.089]` local | `0.9927` local (`2432.8` full) | `8.32e-12`, `1.44e-11` | Stable ONLY inside narrow $2.86\%$ scale-factor window (`[0.99, 1.01]`); exits both walls across `[0.05, 50]`. |
| **5b. $Q^4$ PR #226 + running $\lambda_s(\mathcal{Q})$** (matched to Case 4) | `[+2.82, +4.35]` | `0.9616` | `6.39e-10`, `2.16e-10` | **Stabilized (`[D]`):** bounded acoustic oscillations ($\Phi/\Phi_{\mathrm{GR}} = 0.897$, $\delta_r/\delta_{r,\mathrm{GR}} = 0.993$). |

**Open boundary (`[O]`):** Full multi-species (photons + neutrinos + baryons + AeST) Boltzmann CMB $C_\ell$ and linear matter power spectrum $P(k)$ fitting under covariant running $\lambda_s(\mathcal{Q})$ remains open.
