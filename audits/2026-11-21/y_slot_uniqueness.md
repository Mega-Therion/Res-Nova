# Uniqueness of the $\mathcal{Y}$-Slot at $\mathcal{Q} = 0$ Under the Boltzmann $Q^4$ Constants

- **Date:** 2026-11-21
- **Epistemic Tag:** `[D]` (uniqueness check on the existing action); `[X]` (bound-sector uniqueness fails: $\mathcal{F}(\mathcal{Y}, 0)$ is not determined by the Boltzmann action constants)
- **Sources:** `exploration/tidal_aest/normalization_kb.py`, `audits/2026-11-21/gate1_equality_cosh_vs_q4.py` (`ModelSpec`), `audits/2026-11-21/q4_boltzmann_cmb_pk_fit.py`, `audits/2026-11-21/HILL_SPHERE_EFE_BVP.json`, `exploration/d10_xcop/GATE2_XCOP_MEASURED_ICM.json`

---

## 1. Action Terms Used in the Boltzmann Run (`ModelSpec`)

In the coupled AeST linear perturbation and Boltzmann CMB/BAO/`P(k)` audit (`gate1_equality_cosh_vs_q4.py`, `ModelSpec` in `q4_boltzmann_cmb_pk_fit.py`), the matter/aether Lagrangian density (in $1/(16\pi\tilde{G})$ units) is
$$\mathcal{L}_m = -\frac{1}{2} K_B F^2 + 2(2 - K_B)\,J\cdot\nabla\phi - (2 - K_B)\big(1 + \lambda_s(\mathcal{Q})\big)\,\mathcal{Y} + U(\mathcal{Q}),$$
with $U(\mathcal{Q}) = c\,\mathcal{Q}^4$ ($K_1 = 4c\mathcal{Q}^3$, $K_2^{\mathrm{eff}} = 12c\mathcal{Q}^2$) and running coupling
$$\lambda_s(\mathcal{Q}) = \lambda_{s,0} + \frac{4\alpha c}{2(2 - K_B)}\,\mathcal{Q}^2,$$
specified by the tuple $(K_B, \lambda_{s,0}, c, \alpha, a_0)$ (`K_B = 0.008`, `lambda_{s,0} = 11.2787`, `alpha = 1.15`, `eps_Q = 0.0363–0.0390`). Because $\mathcal{Y} = O(\epsilon^2)$ on a spatially homogeneous FLRW background ($\bar{\mathcal{Y}} = 0$), the linearized $O(\epsilon^2)$ Boltzmann system depends only on $U(\mathcal{Q})$ and the quadratic coefficient $\big(1 + \lambda_s(\mathcal{Q})\big)\,\mathcal{Y}$; any nonlinear $\mathcal{Y}$-dependence in $\mathcal{F}(\mathcal{Y}, \mathcal{Q})$ enters only at $O(\epsilon^3)$ or higher and is unobserved by the 626-bin Planck + DESI fit.

## 2. Terms Surviving at $\mathcal{Q} = 0$

Evaluating $\mathcal{L}_m$ at $\mathcal{Q} = 0$ gives $U(0) = 0$ and $\lambda_s(0) = \lambda_{s,0}$ identically, so $c$ and $\alpha$ drop out. The only terms from the Boltzmann action that survive at $\mathcal{Q} = 0$ are
$$\mathcal{L}_m\big|_{\mathcal{Q}=0} = -\frac{1}{2} K_B F^2 + 2(2 - K_B)\,J\cdot\nabla\phi - (2 - K_B)(1 + \lambda_{s,0})\,\mathcal{Y}.$$
In the static spherical weak-field reduction of `exploration/tidal_aest/normalization_kb.py` ($g_{00} = -(1 + 2\Phi)$, $g_{ij} = (1 - 2\Psi)\delta_{ij}$, $\mathcal{Y} = \phi'^2$, $k = K_B/2$, $m = 2 - K_B$, $n = (2 - K_B)/2$, $\rho = -\nabla^2\Phi_N/(4\pi G_N)$ with $G_N = \tilde{G}/(1 - K_B/2)$ and $g_N := \Phi_N'$), keeping only the Boltzmann $\mathcal{Q} = 0$ terms yields $\Psi' = \Phi'$, $\Phi' - \phi' = g_N$, and $(1 + \lambda_{s,0})\phi' = \Phi' \implies \phi' = g_N / \lambda_{s,0}$. That yields pure Newtonian $1/r^2$ scaling $\Phi'/g_N = 1 + 1/\lambda_{s,0} = 1.0887$ at every acceleration, with no $a_0$ scale and no MOND branch.

## 3. Exact Dichotomy for Any Single-Metric $\mathcal{Y}$-Completion

Adding back the auxiliary static $\psi$ kinetic term from `normalization_kb.py` ($k = K_B/2$, $m = 2 - K_B$, $n = (2 - K_B)/2$) alongside the Boltzmann $\mathcal{Q} = 0$ coefficient $(1 + \lambda_{s,0})$:
$$L = \rho\Phi + \frac{1}{8\pi\tilde{G}}\Big[\Psi'^2 - 2\Phi'\Psi' + \frac{K_B}{2}\Phi'^2 + (2 - K_B)\Phi'\phi' - \frac{2 - K_B}{2}(1 + \lambda_{s,0})\phi'^2 + (2 - K_B)\phi'\psi' + \frac{2 - K_B}{2} a_0^2 F\!\left(\frac{\psi'^2}{a_0^2}\right)\Big]$$
gives the four exact flux equations ($\Psi' = \Phi'$, $\Phi' - \phi' = g_N$ from the $\Psi$ and $\Phi$ equations; $m\Phi' - 2n(1 + \lambda_{s,0})\phi' + 2n\psi' = 0 \implies \psi' = \lambda_{s,0}\phi' - g_N$ from the $\phi$ equation; and $\phi' + F'(u)\psi' = 0$ with $u = \psi'^2/a_0^2$ from the $\psi$ equation). Solving simultaneously yields the exact relation
$$\phi' = \frac{F'(u)}{1 + \lambda_{s,0} F'(u)}\,g_N, \qquad \psi' = -\frac{g_N}{1 + \lambda_{s,0} F'(u)}, \qquad \frac{\Phi'}{g_N} = 1 + \frac{F'(u)}{1 + \lambda_{s,0} F'(u)}.$$
With no free function added beyond the constants already in the Boltzmann action, every single-metric $\mathcal{Y}$-completion faces an exhaustive two-way fork:

1. **Keep $\lambda_{s,0} = 11.2787$:** For every $F'(u) \ge 0$, even in the deep-MOND regime $F'(u) \to +\infty$,
   $$\lim_{F'(u)\to\infty} \frac{\Phi'}{g_N} = \frac{\lambda_{s,0} + 1}{\lambda_{s,0}} = 1 + \frac{1}{11.2787} = 1.0887 < \infty.$$
   Holding $\lambda_{s,0} = 11.2787$ strictly **cuts off the deep-MOND tail** (forcing $\psi' \to 0$ and capping the gravity boost at $+8.87\%$) for every choice of $F(u)$.
2. **Set $\lambda_{s,0} = 0$:** Recovers `normalization_kb.py` identically ($\psi' = -g_N$, $\Phi'/g_N = 1 + F'(u) = \nu(g_N/a_0)$), but leaves the function $F(u)$ completely arbitrary under $(K_B, \lambda_{s,0}, c, \alpha, a_0)$: every ghost-free choice gives the identical FLRW `ModelSpec` linearization. Hence $\mu_{\mathrm{std}}$ stays an explicit galaxy axiom (`FRONT.md` Block 3, `02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`) rather than an output of the cosmological quartic. Choosing $\nu_{\mathrm{std}}$ on extragalactic unscreened X-COP clusters overshoots $R_{200}$ (`GATE2_XCOP_MEASURED_ICM.json`: median `0.608–0.621`, `1/12` in `[0.7, 1.4]`), while extrapolating $\nu_{\mathrm{std}}$ out of domain into the Sun's Hill sphere yields $Q_2 = 15.40\text{--}19.89\times 10^{-27}\,\mathrm{s}^{-2}$ (`HILL_SPHERE_EFE_BVP.json`: `0/15` cells below `5.2e-27 s^-2`, archived as an out-of-domain extrapolation measurement showing where Block 3 stops per `OUTSIDE_GALAXIES.md`, not a failure of the galaxy law).

## 4. Uniqueness Verdict

Because no other term is present in the Boltzmann `ModelSpec` action, **the bound sector $\mathcal{F}(\mathcal{Y}, 0)$ is a family rather than a unique functional and fails the uniqueness criterion**: keeping $\lambda_{s,0} = 11.2787$ truncates the deep-MOND tail at $\Phi'/g_N \le 1.0887$, while setting $\lambda_{s,0} = 0$ leaves $F(u)$ undetermined by the cosmological action constants so $\mu_{\mathrm{std}}$ remains Block 3's galaxy axiom (`02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`; unscreened X-COP clusters remain `[X]` at $R_{200}$, and the Sun's Hill-sphere run stays an out-of-domain extrapolation measurement under `OUTSIDE_GALAXIES.md`).
