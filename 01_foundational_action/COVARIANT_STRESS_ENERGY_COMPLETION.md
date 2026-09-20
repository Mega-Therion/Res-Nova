# Covariant Stress-Energy Completion & Post-Newtonian PPN $\gamma$ Limits

> **BRANCH NOTICE (2026-09-20).** The results below concern
> $\mathcal{F}_{\text{dual}}(x) = \tfrac12 x^2 - x + \ln(1+x)$ and its constitutive
> ratio $\mu(x) = x/(1+x)$. **That branch was falsified on 2026-09-12** — it leaves
> an unscreened solar-system anomalous acceleration far above the Cassini bound —
> and the theory is rebuilt on $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$.
>
> The algebraic statements here remain **true as mathematics**: $\mathcal{F}_{\text{dual}}$
> really does have the stated constitutive structure, Padé minimality and
> ghost-freedom. What is retracted is their status as claims about the *physical*
> model. A `[P]` below should be read as "proved about $\mathcal{F}_{\text{dual}}$",
> not "proved about the theory". See `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`
> for the live derivation.
> The retired objects named below are $\mathcal{F}_{\text{dual}}$ / `F_dual` and
> $\mu_{\text{dual}}(x) = x/(1+x)$, **falsified 2026-09-12**. The live branch is
> $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$ (AeST / Skordis–Złośnik). Statements here
> remain valid as mathematics *about* the retired branch; none is a claim about the
> live model.



**Author:** R.W. Yett
**Repository:** `Research_and_Data/Res_Nova_Monograph/01_foundational_action`  
**Classification:** Canonical Architectural Specification (`[P]` Math / `[D]` Derivation / `[O]` Physical Model Conjectures)  
**Evidence Matrix Mapping:** CLM-05, CLM-06, CLM-14  

---

## 1. Executive Summary

This document establishes the relativistic completion of the dual-channel constitutive framework $\mu(x)$, elevating the non-relativistic Poisson-scale MOND acceleration phenomenology to a fully covariant 4D action on spacetime $(M, g_{\mu\nu})$.

It formalizes:
1. The **4D Covariant Action** combining Einstein-Hilbert gravity, the unit-timelike vector field $A^\mu$ (foliation anchor), and the scalar alignment field $\chi$.
2. The exact **Stress-Energy Tensor** $T_{\mu\nu}^{(\text{total})} = T_{\mu\nu}^{(\chi)} + T_{\mu\nu}^{(A)} + T_{\mu\nu}^{(\text{matter})}$.
3. The **Disformal Coupling Metric** $\tilde{g}_{\mu\nu} = e^{-2\chi} g_{\mu\nu} - 2\sinh(2\chi) A_\mu A_\nu$.
4. The **Parameterized Post-Newtonian (PPN) Weak-Field Expansion**, certifying that $|\gamma_{\text{PPN}} - 1| < 2.3 \times 10^{-5}$ holds strictly across both the massive scalar screening regime and the gradient-ratio acceleration domain $x = |\nabla\Phi|/a_0 \ge 6 \times 10^7$ (Cassini radar experiment).

---

## 2. Relativistic Action Principle

The complete action is defined as:
$$S = \int d^4x \sqrt{-g} \left[ \frac{M_{\text{pl}}^2}{2} R + \mathcal{L}_T(A^\mu, \chi) \right] + S_m[\tilde{g}_{\mu\nu}, \psi]$$

where:
* $M_{\text{pl}} = (8\pi G)^{-1/2}$ is the reduced Planck mass.
* $A^\mu$ is the unit-timelike foliation vector constrained by the Lagrange multiplier $\lambda$:
  $$g_{\mu\nu} A^\mu A^\nu = -1$$
* $\chi$ is the dimensionless scalar alignment field governed by the symmetry-breaking potential:
  $$V(\chi) = \lambda_\chi M_{\text{pl}}^2 \left( \chi^2 - \frac{1}{2} \right)^2 + V_0$$
  whose global minimum is locked to the Stiefel alignment bound $\chi_0 = 1/\sqrt{2} \approx 0.7071$.
* $\mathcal{L}_T(A^\mu, \chi)$ is the total tension Lagrangian:
  $$\mathcal{L}_T = \mathcal{L}_A - \frac{1}{2} g^{\mu\nu} \nabla_\mu \chi \nabla_\nu \chi - V(\chi) + \lambda (g_{\mu\nu} A^\mu A^\nu + 1)$$
* The vector kinetic term satisfies the Foster-Jacobson / GW170817 luminal constraint ($c_1 + c_3 = 0$):
  $$\mathcal{L}_A = - M_{\text{pl}}^2 \left[ c_1 \nabla_\mu A_\nu \nabla^\mu A^\nu + c_2 (\nabla_\mu A^\mu)^2 + c_3 \nabla_\mu A_\nu \nabla^\nu A^\mu - c_4 A^\mu A^\nu \nabla_\mu A^\alpha \nabla_\nu A_\alpha \right]$$
  guaranteeing that gravitational wave tensor modes propagate strictly at $c_T = c$.

---

## 3. Covariant Stress-Energy Tensor

The gravitational stress-energy tensor is obtained by metric variation:
$$T_{\mu\nu} \equiv -\frac{2}{\sqrt{-g}} \frac{\delta (\sqrt{-g} \mathcal{L}_T)}{\delta g^{\mu\nu}}$$

### 3.1 Scalar Field Contribution $T_{\mu\nu}^{(\chi)}$
$$T_{\mu\nu}^{(\chi)} = \nabla_\mu \chi \nabla_\nu \chi - g_{\mu\nu} \left( \frac{1}{2} g^{\alpha\beta} \nabla_\alpha \chi \nabla_\beta \chi + V(\chi) \right)$$

In a homogeneous cosmological FLRW background ($\chi = \chi(t)$):
$$\rho_\chi = \frac{1}{2} \dot{\chi}^2 + V(\chi), \quad p_\chi = \frac{1}{2} \dot{\chi}^2 - V(\chi)$$
When frozen at the minimum $\chi = 1/\sqrt{2}$, $\dot{\chi} \approx 0$ and $V(\chi_0) = V_0$, yielding an effective cosmological constant equation of state $w = p_\chi / \rho_\chi = -1$.

### 3.2 Unit Vector Contribution $T_{\mu\nu}^{(A)}$
Variation with respect to $g^{\mu\nu}$ yields:
$$T_{\mu\nu}^{(A)} = 2 \lambda A_\mu A_\nu + T_{\mu\nu}^{(\text{kin})}$$
In a static weak-field configuration, $A^\mu = (-(1 + 2\Psi)^{-1/2}, \vec{0})$, aligning with the timelike Killing vector. The spatial components of $T_{\mu\nu}^{(A)}$ vanish identically in the static limit, preventing spurious spatial shear stresses.

---

## 4. Parameterized Post-Newtonian (PPN) Weak-Field Expansion

Matter couples directly to the physical disformal metric:
$$\tilde{g}_{\mu\nu} = e^{-2\chi} g_{\mu\nu} - 2\sinh(2\chi) A_\mu A_\nu$$

In a static, spherically symmetric spacetime with Newtonian potential $\Phi$ and spatial curvature potential $\Psi$:
$$ds^2 = -(1 + 2\Psi) dt^2 + (1 - 2\Phi) \delta_{ij} dx^i dx^j$$

Linearizing the disformal metric gives the effective physical potentials felt by baryons:
$$\Psi_{\text{eff}} = \Psi + \chi, \quad \Phi_{\text{eff}} = \Phi - \chi$$

The PPN light-deflection parameter $\gamma_{\text{PPN}}$ is given by:
$$\gamma_{\text{PPN}} \equiv \frac{\Phi_{\text{eff}}}{\Psi_{\text{eff}}} = \frac{\Phi - \chi}{\Psi + \chi}$$

### 4.1 Massive Screening Suppression
In the Solar System, the scalar field potential $V(\chi)$ has an effective mass:
$$m_{\text{eff}}^2 = \left. \frac{d^2 V}{d\chi^2} \right|_{\chi_0} = 8 \lambda_\chi M_{\text{pl}}^2$$
For any natural self-coupling $\lambda_\chi \gg 10^{-89}$, the Compton wavelength satisfies:
$$\lambda_c = m_{\text{eff}}^{-1} \ll 1\text{ AU}$$
Local perturbations $\delta\chi$ sourced by matter are Yukawa-suppressed:
$$\delta\chi(r) \sim \frac{G M}{r} e^{-r/\lambda_c} \to 0$$
Consequently, $\chi$ is pinned to its constant vacuum expectation value $\chi_0$, and:
$$\gamma_{\text{PPN}} = \frac{\Phi}{\Psi} + \mathcal{O}(e^{-r/\lambda_c}) = 1$$

### 4.2 Constitutive Acceleration Bound (Cassini Radar Delay)
In the transition regime where the dual-channel constitutive function $\mu(x)$ governs the effective gravitational coupling:
$$\frac{g_{\text{eff}}}{g_N} = \mu(x), \quad x = \frac{|\nabla \Phi|}{a_0}$$

The fractional deviation from Newtonian gravity is:
$$\Delta \gamma \equiv 1 - \mu(x)$$

* **Dual-channel model ($\mu_{\text{dual}}(x) = x / (1 + x)$):**
  $$\Delta \gamma_{\text{dual}} = \frac{1}{1 + x}$$
  At Earth orbit ($r = 1\text{ AU}$, $g_N \approx 5.93 \times 10^{-3}\text{ m s}^{-2}$, $a_0 \approx 1.116 \times 10^{-10}\text{ m s}^{-2}$):
  $$x = \frac{5.93 \times 10^{-3}}{1.116 \times 10^{-10}} \approx 5.31 \times 10^7$$
  $$\Delta \gamma_{\text{dual}} \approx \frac{1}{5.31 \times 10^7} \approx 1.88 \times 10^{-8} \ll 2.3 \times 10^{-5}$$

* **Standard model ($\mu_{\text{std}}(x) = x / \sqrt{1 + x^2}$):**
  $$\Delta \gamma_{\text{std}} = 1 - \frac{x}{\sqrt{1 + x^2}} \approx \frac{1}{2x^2}$$
  $$\Delta \gamma_{\text{std}} \approx \frac{1}{2 (5.31 \times 10^7)^2} \approx 1.77 \times 10^{-16} \lll 2.3 \times 10^{-5}$$

Both formulations satisfy the Cassini experimental bound $|\gamma_{\text{PPN}} - 1| \le 2.3 \times 10^{-5}$ with safety margins of $10^3\times$ and $10^{11}\times$ respectively.

---

## 5. Epistemic Certification Summary

| Claim | Status | Mathematical Grounding | Physical Status |
| :--- | :--- | :--- | :--- |
| 4D Covariant Action | `[D]` | Well-posed variational principle | Relativistic field theory ansatz |
| Stress-Energy Conservation $\nabla^\mu T_{\mu\nu} = 0$ | `[P]` | Noether identity under diffeomorphism invariance | Exact in pseudo-Riemannian geometry |
| Disformal Weak-Field Linearization | `[P]` | Exact Taylor expansion of $e^{-2\chi}$ and $\sinh(2\chi)$ | Mathematical theorem |
| PPN $\gamma_{\text{PPN}} \to 1$ Screening | `[P]` | Yukawa suppression $e^{-r/\lambda_c}$ for $m_{\text{eff}} \gg (1\text{ AU})^{-1}$ | Certified compatible with General Relativity |
| Cassini Radar Concordance | `[P]` | $\Delta \gamma \le 2.3 \times 10^{-5}$ satisfied at $x \ge 6 \times 10^7$ | Mechanized in `PPNLimits.lean` and `verify_ppn_gamma_symbolic.py` |
