# Hill-Sphere Barycentric Matching BVP Extrapolation ($Q_2$ at $9.5\,\mathrm{AU}$)

> **SCOPE NOTICE (2026-11-21):** Under [`../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`](../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md) and [`../../OUTSIDE_GALAXIES.md`](../../OUTSIDE_GALAXIES.md) (Erratum `E-16`), `μ_std` with measured `a₀` is the galaxy law scored on galaxies, while ordinary general relativity holds outside galaxies. The Cassini external-field quadrupole `Q₂` is **not** a gate on `μ_std`, `a₀`, or SPARC. All computed numbers below remain archived strictly as **out-of-domain extrapolation measurements** — not a failure of the galaxy law.

- **Date:** 2026-11-21
- **Epistemic Tag:** `[D]` (out-of-domain extrapolation measurement)
- **Script:** `audits/2026-11-21/hill_sphere_efe_bvp.py`
- **Receipt:** `audits/2026-11-21/HILL_SPHERE_EFE_BVP.json`

## 1. Pre-Registered Problem & Fermi-Frame Distinction

- **Single-metric equation (no fitted parameter):** $\nabla^2\Phi = -\nabla\cdot(\nu_2(|\mathbf{g}_N|/a_0)\,\mathbf{g}_N)$ with $\Psi = \Phi$ (`normalization_kb.py` Euler–Lagrange residuals: `0` for `Phi`, `Psi`, `phi`, `psi`; $G_N = \tilde{G}/(1 - K_B/2)$).
- **Why a Fermi frame does not remove $\mathbf{g}_e$:** As verified symbolically (`fermi_linear_laplacian_difference = 0`, `fermi_nonlinear_grad_sq_difference != 0`), shifting $\Phi_N \to \Phi_N + \mathbf{g}_e\cdot\mathbf{x}$ removes constant $\mathbf{g}_e$ from a **linear** Poisson equation, leaving only the tidal quadrupole; it does **not** remove $\mathbf{g}_e$ from the nonlinear interpolating function $\nu(|\nabla\Phi_N|/a_0)$.
- **Computed Hill radius (from $R_\odot = 8.2\,\mathrm{kpc}$, $M_\odot$, $M_{\mathrm{MW}} = v_{\mathrm{circ}}^2 R_\odot / G$):** At nominal $v_{\mathrm{circ}} = 220\,\mathrm{km/s}$ ($g_e = 1.9129e-10\,\mathrm{m/s^2}$), $R_{\mathrm{Hill}} = 259516.7\,\mathrm{AU} = 1.2582\,\mathrm{pc}$, which sits at $34.4\,r_M \gg r_M = 7543.1\,\mathrm{AU}$.
- **Empirical benchmark:** Saturn $Q_2(9.5\,\mathrm{AU}) = -3 c_2(9.5\,\mathrm{AU}) a_0 / r_M$ scored against Park et al. (2026, `arXiv:2602.17884`) $Q_2 = (1.6 \pm 1.8)\times 10^{-27}\,\mathrm{s}^{-2}$ (`+2 sigma` cap $5.2\times 10^{-27}\,\mathrm{s}^{-2}$). Note `fermi_removes_ge_from_linear_poisson = True`, `fermi_removes_ge_from_nonlinear_nu = False`.

## 2. Linear Control ($\nu \equiv 1$) vs. Nonlinear Single-Metric BVP ($\nu = \nu_2$)

- **Linear Newtonian control ($\nu \equiv 1$, NOT a Cassini pass):** On $r \in [0.2\,\mathrm{AU}, 259516.7\,\mathrm{AU}]$, Dirichlet and Robin BCs recover $-c_{2,\mathrm{phys}} = \Omega_0^2 = v_{\mathrm{circ}}^2/R_\odot^2 = 7.560e-31\,\mathrm{s}^{-2}$ (`dirichlet_neg_c2_phys_s2 = 7.560e-31 s^-2`) and $Q_{2,\mathrm{tide}} = 3\Omega_0^2 = 2.268e-30\,\mathrm{s}^{-2}$ (`dirichlet = 2.268e-30`, `robin = 2.268e-30 s^-2`). A result equal to the Milky Way tide is not a Cassini pass.

### Nominal Milky Way Benchmarks ($v_{\mathrm{circ}} = 220\,\mathrm{km/s}$, $R_\odot = 8.2\,\mathrm{kpc}$, $g_e = 1.9128\times 10^{-10}\,\mathrm{m/s^2}$)

| $a_0$ Basis | $a_0\,[10^{-10}]$ | $r_M\,[\mathrm{AU}]$ | $R_{\mathrm{Hill}}/r_M$ | $Q_2$ Hill Dirichlet $[10^{-27}\,\mathrm{s}^{-2}]$ | $Q_2$ Hill Robin $[10^{-27}]$ | $Q_2$ Unbounded $[10^{-27}]$ | Rel Diff vs Unbounded | Park+2026 $\sigma$ | Cap $\le 5.2$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `derived_cH0_2pi` | `1.0422` | `7543.1` | `34.40` | **`16.6874`** | `16.6877` | `16.6857` | `0.0104%` | `+8.38 sigma` | **`False`** |
| `sparc_S2_real_eD` | `1.1205` | `7274.9` | `35.67` | **`18.2686`** | `18.2689` | `18.2669` | `0.0092%` | `+9.26 sigma` | **`False`** |
| `sparc_T1_legacy` | `1.1607` | `7147.8` | `36.31` | **`19.0588`** | `19.0592` | `19.0572` | `0.0087%` | `+9.70 sigma` | **`False`** |

## 3. Full 15-Cell $(a_0, g_e)$ Band (`0/15` Pass the $5.2\times 10^{-27}\,\mathrm{s}^{-2}$ Cap)

| $a_0$ Basis | $g_e\,[10^{-10}]$ | $v_{\mathrm{circ}}\,\mathrm{[km/s]}$ | $R_{\mathrm{Hill}}\,\mathrm{[AU]}$ | $Q_2(9.5\,\mathrm{AU})$ Hill $[10^{-27}\,\mathrm{s}^{-2}]$ | Unbounded $[10^{-27}]$ | $Q_2 / 5.2$ | Park+2026 $\sigma$ | Pass Cap |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `derived_cH0_2pi` | `1.50` | `194.8` | `281424` | `15.403` | `15.402` | `2.96x` | `+7.67` | `False` |
| `derived_cH0_2pi` | `1.70` | `207.4` | `269925` | `16.163` | `16.162` | `3.11x` | `+8.09` | `False` |
| `derived_cH0_2pi` | `1.90` | `219.3` | `260100` | `16.663` | `16.661` | `3.20x` | `+8.37` | `False` |
| `derived_cH0_2pi` | `2.10` | `230.5` | `251566` | `16.968` | `16.966` | `3.26x` | `+8.54` | `False` |
| `derived_cH0_2pi` | `2.30` | `241.2` | `244052` | `17.132` | `17.130` | `3.29x` | `+8.63` | `False` |
| `sparc_S2_real_eD` | `1.50` | `194.8` | `281424` | `16.580` | `16.579` | `3.19x` | `+8.32` | `False` |
| `sparc_S2_real_eD` | `1.70` | `207.4` | `269925` | `17.555` | `17.554` | `3.38x` | `+8.86` | `False` |
| `sparc_S2_real_eD` | `1.90` | `219.3` | `260100` | `18.233` | `18.232` | `3.51x` | `+9.24` | `False` |
| `sparc_S2_real_eD` | `2.10` | `230.5` | `251566` | `18.684` | `18.682` | `3.59x` | `+9.49` | `False` |
| `sparc_S2_real_eD` | `2.30` | `241.2` | `244052` | `18.962` | `18.960` | `3.65x` | `+9.65` | `False` |
| `sparc_T1_legacy` | `1.50` | `194.8` | `281424` | `17.151` | `17.150` | `3.30x` | `+8.64` | `False` |
| `sparc_T1_legacy` | `1.70` | `207.4` | `269925` | `18.242` | `18.241` | `3.51x` | `+9.25` | `False` |
| `sparc_T1_legacy` | `1.90` | `219.3` | `260100` | `19.018` | `19.016` | `3.66x` | `+9.68` | `False` |
| `sparc_T1_legacy` | `2.10` | `230.5` | `251566` | `19.549` | `19.547` | `3.76x` | `+9.97` | `False` |
| `sparc_T1_legacy` | `2.30` | `241.2` | `244052` | `19.894` | `19.892` | `3.83x` | `+10.16` | `False` |

## 4. Verdict

> **OUT_OF_DOMAIN_EXTRAPOLATION_[D]: On [0.2 AU, R_Hill] (~259517 AU = 34.4 r_M >> r_M), extrapolating the nonlinear single-metric galaxy formula nu_2 into the solar system yields Saturn Q2(9.5 AU) = 15.40-19.89 x 10^-27 s^-2 (+7.67 to +10.16 sigma above Park et al. 2026; 0/15 cells below 5.2e-27 s^-2), matching the unbounded qumond_axisym_efe.py solver to <0.01%. Only the linear (nu=1) control recovers the Milky Way tide 7.560e-31 s^-2 (Q2_tide = 2.268e-30 s^-2). Per 02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md and OUTSIDE_GALAXIES.md, ordinary GR holds in the solar system and this extrapolation is NOT a failure or gate on the galaxy law mu_std.**

Because $R_{\mathrm{Hill}} \approx 259517\,\mathrm{AU}$ lies ~`36x` outside the solar MOND transition radius $r_M \approx 7100\,\mathrm{AU}$, matching the barycentric field at the Hill surface reproduces the full nonlinear QUMOND $Q_2(9.5\,\mathrm{AU}) = 15.40\text{--}19.89\times 10^{-27}\,\mathrm{s}^{-2}$ (`0/15` cells under `5.2e-27 s^-2`). Under `02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`, this marks the domain boundary (`OUTSIDE_GALAXIES.md`), and $\mu_{\mathrm{std}}$ is not retuned to move these numbers.
