---
title: "Covariant Action for Duality Screening: Candidate Formulation and Structural Audit"
type: "derivation"
created: "2026-10-10"
tags:
  - "res_nova"
  - "gravity"
  - "cassini"
  - "duality_screening"
  - "aest"
  - "gw170817"
  - "formal"
  - "epistemic_open"
---

# Covariant Action for Duality Screening: Candidate Formulation and Structural Audit

**Status:** `[O]` Open / Candidate Under Formal Audit.  
**Target:** Theoretical foundation for resolving Item 5 in the unified roadmap; evaluating whether a covariant action can dynamically produce duality screening $S(\eta) = 1/(1+\eta^2)$ to resolve the $+4.55\sigma$ (Planck) / $+5.14\sigma$ (SH0ES) Cassini EFE quadrupole tension while preserving SPARC rotation curves and satisfying physical constraints.  
**Binding Audit Standard:** Strict non-vacuous mathematical rigor; all algebraic blunders, foliation requirements, light-cone mismatches, and 4th-order Euler–Lagrange variations stated explicitly without narrative inflation.

---

## 1. Problem Statement & The Cassini Conflict

In modified gravity and Information-Tension theory, galactic rotation curves prefer the smooth standard interpolating function:
$$\mu_{\text{std}}(x) = \frac{x}{\sqrt{1+x^2}}, \qquad x = \frac{|\nabla\Phi|}{a_0}$$
derived from the action kinetic potential:
$$\mathcal{F}_{\text{std}}(\mathcal{Y}) = \sqrt{\mathcal{Y}(1+\mathcal{Y})} - \operatorname{arsinh}(\sqrt{\mathcal{Y}}), \qquad \mathcal{Y} = \frac{|\nabla\chi|^2}{a_0^2}$$
where $\mathcal{F}'_{\text{std}}(\mathcal{Y}) = \mu_{\text{std}}(\sqrt{\mathcal{Y}})$.

However, when embedded in the Milky Way's external field $g_{\text{ext}} \approx (1.9\text{--}2.4) \times 10^{-10}\text{ m/s}^2$, standard two-derivative $\mu_{\text{std}}$ generates an anomalous tidal quadrupole in the solar system:
$$Q_2 = -\frac{3 q a_0^{3/2}}{2 \sqrt{G M_\odot}}$$
Evaluations on the Cassini 2026 bound ($Q_2 = (1.6 \pm 1.8) \times 10^{-27}\text{ s}^{-2}$, 2$\sigma$ ceiling $5.2 \times 10^{-27}\text{ s}^{-2}$) yield:
- **At Planck $H_0 = 67.4$ ($a_0 = 1.042 \times 10^{-10}\text{ m/s}^2$):** $Q_2 = 1.67 \times 10^{-26}\text{ s}^{-2} \implies \mathbf{+4.55\sigma}$ (FAIL)
- **At SH0ES $H_0 = 73.04$ ($a_0 = 1.129 \times 10^{-10}\text{ m/s}^2$):** $Q_2 = 1.84 \times 10^{-26}\text{ s}^{-2} \implies \mathbf{+5.14\sigma}$ (FAIL)

The phenomenological duality screening factor:
$$S(\eta) = \frac{1}{1+\eta^2} = \mu_{\text{std}}(1/\eta)^2, \qquad \eta = \frac{g_{\text{ext}}}{a_0}$$
damps the quadrupole to $Q_2 \approx 2.7\text{--}3.8 \times 10^{-27}\text{ s}^{-2}$ ($+0.6\sigma\text{--}+1.2\sigma$) while remaining neutral on SPARC ($\Delta\chi^2/s = -0.8$).

**The Formal Requirement:** Elevating $S(\eta)$ from an external ad-hoc multiplier to a legitimate field theory requires a covariant action. This audit formalizes the candidate Lagrangian and records five explicit structural barriers that remain open.

---

## 2. Candidate Covariant Action & Foliation Construction

To formulate screening without generating temporal Ostrogradsky ghosts, we consider a scalar–vector–metric theory:
$$S = S_{\text{EH}}[g] + S_{\text{vector}}[g, A] + S_{\chi}[g, A, \chi] + S_{\text{matter}}[\tilde{g}, \psi_m]$$

### 2.1 Vector Sector & Foliation (The Khronon Condition)
A generic unit timelike vector $A^\mu$ ($A_\mu A^\mu = -1$) possesses dynamical twist $\omega_{\mu\nu} = \nabla_{[\mu} A_{\nu]} + A_{[\mu} a_{\nu]}$. A spatial projector $q^{\mu\nu} = g^{\mu\nu} + A^\mu A^\nu$ orthogonal to $A^\mu$ ($q^{\mu\nu} A_\mu = 0$) **does not establish a spatial foliation** unless the Frobenius integrability condition is identically satisfied:
$$A_{[\mu} \nabla_\nu A_{\rho]} = 0$$

To guarantee a genuine spacetime foliation $\mathcal{M} = \mathbb{R} \times \Sigma_t$, the vector field must be hypersurface-orthogonal. This is accomplished by defining $A_\mu$ as the unit gradient of a scalar khronon field $T(x)$:
$$A_\mu \equiv -\frac{\nabla_\mu T}{\sqrt{-g^{\alpha\beta}\nabla_\alpha T \nabla_\beta T}}$$
Under this condition, spacetime foliates into level surfaces of $T$, and the spatial projection of the spacetime Hessian relates to the intrinsic spatial Hessian $D_i D_j \chi$ by extrinsic curvature:
$$q^\mu{}_\alpha q^\nu{}_\beta \nabla_\mu \nabla_\nu \chi = D_\alpha D_\beta \chi - K_{\alpha\beta} A^\lambda \nabla_\lambda \chi$$
where $K_{\alpha\beta}$ is the extrinsic curvature of the constant-$T$ slices.

### 2.2 Corrected Disformal Metric Formulation
Matter couples to the disformal metric $\tilde{g}_{\mu\nu}$. In a preferred rest frame where $A^\mu = (1, 0, 0, 0)$ and $g_{\mu\nu} = \operatorname{diag}(-1, 1, 1, 1)$, obtaining equal physical potential perturbations $\Phi = \Psi = \chi$ requires:
$$\tilde{g}_{00} = -e^{-2\chi} = -(1 - 2\chi + \dots), \qquad \tilde{g}_{ij} = e^{2\chi} \delta_{ij} = (1 + 2\chi + \dots)\delta_{ij}$$

**Audit of Prior Sign Error:**
An earlier draft wrote $\tilde{g}_{\mu\nu} = e^{2\chi} g_{\mu\nu} - 2\sinh(2\chi) A_\mu A_\nu$.
In the rest frame ($A_0 = -1$):
$$\tilde{g}_{00} = e^{2\chi}(-1) - 2\sinh(2\chi)(-1)^2 = -e^{2\chi} - (e^{2\chi} - e^{-2\chi}) = -2e^{2\chi} + e^{-2\chi} = -1 - 6\chi + \mathcal{O}(\chi^2)$$
which yields $\left.\frac{\partial\tilde{g}_{00}}{\partial\chi}\right|_{\chi=0} = -6 \ne +2$, completely breaking the claimed potential equality.

**Corrected Candidate Metric:**
$$\tilde{g}_{\mu\nu} = e^{2\chi} g_{\mu\nu} + 2\sinh(2\chi) A_\mu A_\nu$$
Evaluating in the rest frame ($A_0 = -1, A_i = 0$):
$$\tilde{g}_{00} = -e^{2\chi} + 2\sinh(2\chi) = -e^{2\chi} + (e^{2\chi} - e^{-2\chi}) = -e^{-2\chi}$$
$$\tilde{g}_{ij} = e^{2\chi} g_{ij} + 0 = e^{2\chi} \delta_{ij}$$
This gives $\left.\frac{\partial\tilde{g}_{00}}{\partial\chi}\right|_{\chi=0} = +2$ and $\left.\frac{\partial\tilde{g}_{ij}}{\partial\chi}\right|_{\chi=0} = +2\delta_{ij}$, as required for equal non-relativistic potentials $\tilde{\Phi} = \tilde{\Psi} = \chi$.

---

## 3. The Scalar Action & Full Euler–Lagrange Variation

The candidate scalar action is:
$$S_\chi[g, A, \chi] = -\frac{a_0^2}{8\pi G} \int \mathrm{d}^4x \sqrt{-g} \, \mathcal{L}_\chi(\mathcal{Y}, \mathcal{W})$$
where:
$$\mathcal{Y} \equiv \frac{q^{\mu\nu} \nabla_\mu \chi \nabla_\nu \chi}{a_0^2}, \qquad \mathcal{W} \equiv \frac{q^{\mu\alpha} q^{\nu\beta} (\nabla_\mu \nabla_\nu \chi)(\nabla_\alpha \nabla_\beta \chi)}{\Lambda^4}$$
$$\mathcal{L}_\chi(\mathcal{Y}, \mathcal{W}) = \mathcal{F}_{\text{std}}(\mathcal{Y}) \cdot \Sigma(\mathcal{W}), \qquad \Sigma(\mathcal{W}) = \frac{1}{1 + \mathcal{W}^2}$$

### 3.1 The Un-Omitted 4th-Order Variation
Because $\mathcal{W}$ depends on second covariant derivatives, the Euler–Lagrange equation of motion is:
$$\nabla_\mu \left( \frac{\partial \mathcal{L}_\chi}{\partial(\nabla_\mu\chi)} \right) - \nabla_\mu \nabla_\nu \left( \frac{\partial \mathcal{L}_\chi}{\partial(\nabla_\mu\nabla_\nu\chi)} \right) = \frac{8\pi G}{a_0^2 \sqrt{-g}} \frac{\delta S_m}{\delta\chi}$$

In the static, flat-slice limit where $A^\mu = (1, 0, 0, 0)$, $A^\mu \nabla_\mu\chi = 0$, set $B_{ij} \equiv D_i D_j \chi$ and $\mathcal{W} = \frac{B_{ij} B^{ij}}{\Lambda^4}$. The variations are:
$$\frac{\partial \mathcal{L}_\chi}{\partial(D_i\chi)} = \frac{2}{a_0^2} \mathcal{F}'(\mathcal{Y}) \Sigma(\mathcal{W}) D^i\chi$$
$$\frac{\partial \mathcal{L}_\chi}{\partial(D_i D_j\chi)} = \frac{2}{\Lambda^4} \mathcal{F}(\mathcal{Y}) \Sigma'(\mathcal{W}) B^{ij}$$

The exact static scalar equation of motion is:
$$D_i \Big( \mathcal{F}'_{\text{std}}(\mathcal{Y}) \Sigma(\mathcal{W}) D^i\chi \Big) - \frac{a_0^2}{\Lambda^4} D_i D_j \Big( \mathcal{F}_{\text{std}}(\mathcal{Y}) \Sigma'(\mathcal{W}) B^{ij} \Big) = 4\pi G \rho_m$$

**Audit of Omitted Variation:**
In previous drafts, the fourth-order term $-\frac{a_0^2}{\Lambda^4} D_i D_j (\mathcal{F} \Sigma' B^{ij})$ was omitted.
Because:
$$\Sigma'(\mathcal{W}) = -\frac{2\mathcal{W}}{(1+\mathcal{W}^2)^2}$$
this term is strictly non-zero in any region with non-vanishing tidal curvature. A valid screening proof must compute the solutions to the coupled nonlinear 4th-order spatial differential equation, rather than evaluating $\Sigma(\mathcal{W})$ purely as an algebraic coefficient.

### 3.2 The $\Sigma(\mathcal{W}) \leftrightarrow S(\eta)$ Gap
The algebraic identity:
$$\mu_{\text{std}}(1/\eta)^2 = \frac{1}{1+\eta^2} \equiv S(\eta)$$
proves that the functional form $\frac{1}{1+z^2}$ appears in both $\mu_{\text{std}}$ and $S(\eta)$. **It does not prove a dynamical equivalence between $\mathcal{W}$ and $\eta^2$.**
- $\eta = |\mathbf{g}_{\text{ext}}| / a_0$ is the ratio of external first derivatives (acceleration).
- $\mathcal{W} = |D_i D_j \chi|^2 / \Lambda^4$ is a scalar constructed from second derivatives (tidal curvature).

While the Sun's tidal field $\nabla\nabla\Phi_\odot \sim GM_\odot/r^3$ provides a local cutoff, establishing that the second-derivative switch dynamically reproduces the exact acceleration-dependent external field effect $S(\eta)$ requires an explicit boundary-value solution across the transition zone. Until such a solution is computed, $\Sigma(\mathcal{W})$ remains an ansatz.

---

## 4. Preferred-Frame Parameters (PPN $\alpha_1$) Audit

In standard Einstein–aether theory with kinetic action parameters $c_1, c_2, c_3, c_4$, the PPN preferred-frame parameter $\alpha_1$ is given by:
$$\alpha_1 = -\frac{8(c_3^2 + c_1 c_4)}{2c_1 - c_1^2 + c_3^2}$$

**Audit of Prior Blunder:**
The earlier text asserted that setting $c_1 + c_3 = 0$ ($c_3 = -c_1$) and $c_4 = 0$ yields $\alpha_1 = 0$.
Performing the exact substitution:
$$\alpha_1 = -\frac{8((-c_1)^2 + c_1(0))}{2c_1 - c_1^2 + (-c_1)^2} = -\frac{8c_1^2}{2c_1} = -4c_1 = -2K_B$$
For any non-zero vector coupling $c_1 \ne 0$, $\alpha_1 \ne 0$. Lunar Laser Ranging and pulsar timing constrain $|\alpha_1| \lesssim 10^{-4}$.
Furthermore, because matter couples disformally to $\tilde{g}_{\mu\nu} = e^{2\chi} g_{\mu\nu} + 2\sinh(2\chi) A_\mu A_\nu$, the standard pure Einstein–aether PPN formulas do not apply directly. A complete PPN expansion of the coupled scalar–vector–metric action is required.

---

## 5. Physical Light Cone vs Gravitational Wave Speed

GW170817 requires that the speed of gravitational waves $c_{\text{GW}}$ matches the speed of photons $c_{\text{EM}}$ to within $10^{-15}$:
$$\left| \frac{c_{\text{GW}} - c_{\text{EM}}}{c_{\text{EM}}} \right| \lesssim 10^{-15}$$

1. **Graviton Light Cone:** Tensor perturbations $h_{\mu\nu}$ in $S_{\text{EH}}[g]$ propagate along the null geodesics of the gravitational metric $g_{\mu\nu}$, so the coordinate speed of gravitons is $c_{\text{GW}} = 1$.
2. **Photon Light Cone:** Standard Model electromagnetic fields couple minimally to the physical metric $\tilde{g}_{\mu\nu}$. In the preferred rest frame:
   $$\mathrm{d}\tilde{s}^2 = -e^{-2\chi} \mathrm{d}t^2 + e^{2\chi} \delta_{ij} \mathrm{d}x^i \mathrm{d}x^j$$
   Null photon trajectories ($\mathrm{d}\tilde{s}^2 = 0$) satisfy:
   $$c_{\text{EM}}^2 = \left( \frac{\mathrm{d}x}{\mathrm{d}t} \right)^2 = \frac{e^{-2\chi}}{e^{2\chi}} = e^{-4\chi}$$
   $$c_{\text{EM}} = e^{-2\chi} \approx 1 - 2\chi$$

Therefore, the fractional speed difference measured by physical observers is:
$$\frac{c_{\text{GW}} - c_{\text{EM}}}{c_{\text{EM}}} \approx 2\chi$$

**Constraint:** Across intergalactic propagation distances ($D_L \sim 40\text{ Mpc}$ for GW170817), satisfaction of the LIGO/Virgo/Fermi bound requires:
$$|\chi_{\text{cosmo}}| \lesssim 5 \times 10^{-16}$$
In any modified gravity theory where $\chi \sim \mathcal{O}(10^{-6}\text{--}10^{-4})$ in galactic or cosmological backgrounds, this discrepancy rules out the disformal coupling unless:
- $\chi$ vanishes cosmologicaly, OR
- The gravitational wave action itself is disformally modified to track $\tilde{g}_{\mu\nu}$, OR
- Photons couple to $g_{\mu\nu}$ and only massive particles couple disformally.

---

## 6. Formal Status & Open Audit Matrix

| Structural Check | Previous Claim | Verified Audit Status | Epistemic Tier |
|:---|:---:|:---:|:---:|
| **Foliation Existence** | Guaranteed by $q^{\mu\nu}A_\mu = 0$ | **FAILED:** Requires Frobenius condition / khronon $A_\mu \propto \nabla_\mu T$ | `[O]` Open |
| **Disformal Potential Matching** | Claimed $\Phi = \Psi$ under $-2\sinh(2\chi)$ | **FAILED:** Yielded $\tilde{g}_{00} = -1-6\chi$; requires $+2\sinh(2\chi)$ metric | `[O]` Corrected |
| **Scalar EOM Variation** | Claimed $\nabla \cdot (\mathcal{F}' \Sigma \nabla\chi) = 4\pi G\rho$ | **FAILED:** Omitted 4th-order spatial term $-\frac{a_0^2}{\Lambda^4} D_i D_j (\mathcal{F}\Sigma' B^{ij})$ | `[O]` Open |
| **$\Sigma(\mathcal{W}) \leftrightarrow S(\eta)$ Equivalence** | Claimed derived from duality identity | **UNPROVEN:** Identity on $\mu(x)$ is not a dynamical equivalence for $\mathcal{W}$ | `[O]` Open |
| **PPN $\alpha_1$ Parameter** | Claimed $\alpha_1 = 0$ from $c_1 + c_3 = 0$ | **FAILED:** Formula gives $\alpha_1 = -2K_B \ne 0$; needs coupled PPN | `[O]` Open |
| **GW170817 Speed Matching** | Claimed $c_{\text{GW}} = c$ from pure EH | **FAILED:** Neglected photon light cone on $\tilde{g}_{\mu\nu}$ ($|c_{\text{GW}} - c_{\text{EM}}| \approx 2\chi$) | `[O]` Open |
| **Cassini $Q_2$ Metric Resolution** | Claimed "Closed / Passed" | **REVERTED TO OPEN:** Depends on resolution of all 6 items above | `[O]` Open |

**Conclusion:** The candidate screening action is an exploratory proposal under formal audit. Item 5 of the theoretical physics roadmap remains strictly **OPEN `[O]`**.
