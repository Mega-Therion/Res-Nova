# Pre-registration: Causal Weyl Anisotropic-Stress Envelope Kill Filter for the Flux-Fed Dark Bubble Wall (2026-11-19, before any number)

**Context.** `exploration/drag_gcosmo/` (`#255`, `#257`, `#259`, `#260`) established that on the surviving sub-conformal branch $0 \le w_d < 1/3$, the coupled drag+Weyl background depends only on $\kappa = (3 w_d - 1) x_0$, with bare drag bounded from below by $x_0 = |\kappa|/(1 - 3 w_d) \ge |\kappa|$ ($x_0 \approx 2.24$ at Pantheon+ best fit, $2\sigma$ floor $x_0 \ge 0.83$ on BAO+SN+CMB and $\ge 0.62$ with $f\sigma_8$, giving $\Omega_{\mathrm{Weyl}}(0) \approx 1.75$). Because nothing on the 4D brane closes the Weyl dark-radiation anisotropic stress $\pi_{\mathcal{E}}$ (`Maartens & Koyama 2010`, `arXiv:1004.3962`, `[C]`), a full CMB Boltzmann test requires 5D bulk perturbations unless every causal 4D closure already fails.

**Goal.** Before building a 1+1D 5D AdS-Vaidya bulk perturbation solver, bracket the **entire causal space** of Weyl dark-radiation anisotropic stress (`Hu 1998` Generalized Dark Matter: $c_s^2 = 1/3$, $c_{\mathrm{vis}}^2 \in \{0.0, 0.1, 1/3, 0.6, 1.0\}$) coupled to the exact linearized 4D Einstein + perturbed drag + Weyl-flux conservation equations, and compute exact Limber CMB lensing $C_L^{\phi\phi}$ ($L \in [40, 400]$) and late-ISW $C_\ell^{\mathrm{ISW}}$ ($\ell \in [2, 30]$).

## Symbolic derivation (SymPy, before numerics)
- Derive and verify in conformal Newtonian gauge ($ds^2 = a^2[-(1 + 2\Phi)d\tau^2 + (1 - 2\Psi)d\mathbf{x}^2]$):
  1. The perturbed drag energy-density and pressure response from $\Delta\Sigma_{\mathrm{drag}} = \frac{1}{2}\rho_b a^2 (\theta/3)^2$ (with $w_d = 0$ at the minimum-drag floor), where $\delta H / H = -(\Psi' + \Phi)$ shifts the $00$ Hamiltonian constraint factor $2 H \delta H \to 2(1 + x_0 a^2) H \delta H$ (`' = d/d(ln a)`).
  2. Exact Einstein $00$, $0i$, and shear ($i \neq j$) equations with Weyl anisotropic stress $\sigma_W$ ($\Phi - \Psi = -6 (a H / k)^2 (\Omega_W / E^2) \sigma_W$ or convention verified identically in SymPy).
  3. Exact linearized 4D Bianchi conservation for the flux-fed Weyl fluid ($\delta\mathcal{Q}_4$ from linearizing $\dot{\Delta\Sigma}_{\mathrm{drag}} + 3H\Delta\Sigma_{\mathrm{drag}} = \mathcal{Q}_4$), verifying exact `0i` consistency and exact recovery of $\Lambda$CDM growth at $\kappa = 0$ (`REF_D1` to $< 10^{-3}$, $\Phi = \Psi$ to $< 10^{-12}$).

## Pre-registered parameter points & sweeps (at $w_d = 0$, $x_0 = |\kappa|$)
1. **Control ($\Lambda$CDM):** $\kappa = 0$ (`h = 0.6810, Omega_m = 0.3036`).
2. **Pantheon+ best fit (`FLUX_CODAZZI.json`):** $\kappa = -2.2445$, $h = 0.6803$, $\Omega_m = 0.3087$ ($x_0 = 2.2445$).
3. **DES-Dovekie best fit (`FLUX_CODAZZI.json`):** $\kappa = -2.4966$, $h = 0.6801$, $\Omega_m = 0.3094$ ($x_0 = 2.4966$).
4. **Pantheon+ $2\sigma$ bare-drag floor:** $\kappa = -0.8317$ (`h, Omega_m` re-minimized on `Pantheon+_BAO_CMB` at fixed $\kappa = -0.8317$ or interpolated consistently with the $2\sigma$ profile).

Across $k \in [10^{-4}, 0.2]\,\mathrm{Mpc}^{-1}$ (25 log-spaced modes), $c_{\mathrm{vis}}^2 \in \{0.0, 0.1, 1/3, 0.6, 1.0\}$, plus sensitivity checks on:
- Flux momentum exchange: bulk rest frame ($V_{\mathrm{flux}} = 0$, primary) vs. matter-comoving ($V_{\mathrm{flux}} = V_m$).
- Early initial condition at $a_i = 10^{-3}$: adiabatic ($\delta_W = \frac{4}{3}\delta_m$) vs. unperturbed ($\delta_W = 0$).

## Pre-registered decision rule
- **SURVIVES ENVELOPE (5D PDE justified):** At least one causal $c_{\mathrm{vis}}^2 \in [0, 1]$ at the Pantheon+ or Dovekie best fit is linearly stable across $k \in [10^{-4}, 0.2]\,\mathrm{Mpc}^{-1}$, gives Limber CMB lensing amplitude ratio $|A_{\phi\phi,\mathrm{eff}} - 1| \le 0.08$ ($\approx 3\sigma$ of Planck 2018 PR3 $1.000 \pm 0.026$, arXiv:1807.06210), AND gives late-ISW amplitude ratio $C_\ell^{\mathrm{ISW}}/C_\ell^{\mathrm{ISW}}(\Lambda\mathrm{CDM}) \in [0.4, 1.6]$ for $\ell \in [2, 30]$.
- **KILLED MODEL-INDEPENDENTLY (`[X]`):** Every causal $c_{\mathrm{vis}}^2 \in [0, 1]$ (across both $V_{\mathrm{flux}}$ conventions) fails linear stability, $|A_{\phi\phi,\mathrm{eff}} - 1| \le 0.08$, or $C_\ell^{\mathrm{ISW}} \in [0.4, 1.6]$ at **both** best-fit and the $2\sigma$ floor $\kappa = -0.8317$.
- **TIGHTENED / BOUNDED (`[O]`):** Best-fit fails every causal $c_{\mathrm{vis}}^2$, while $\kappa = -0.8317$ survives (report the exact surviving $|\kappa|$ ceiling!).
