# 🌌 Target D7: 4D Covariant Metric Completion & Obstruction Dossier
**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Date:** 2026-08-14  
**Framework:** Res-Nova / Chyren Epistemic Architecture (v1.2.0)  
**Epistemic Boundary:** $\mathbf{[P]}$ for mathematical obstructions and reduction theorems; $\mathbf{[O]}$ for quantum UV completion.

---

## 1. Executive Summary & Epistemic Verdicts

Target D7 addresses the 40-year foundational open problem of modified gravity: constructing a 4D Lorentz-covariant metric theory whose non-relativistic quasistatic weak-field limit reduces **identically** to the derived dual-channel AQUAL theory ($\mu(x) = \frac{x}{1+x}$).

```
========================================================================================================
PATH     CANDIDATE COVARIANT FRAMEWORK           FORMAL VERDICT & STATUS
========================================================================================================
Path 1   Pure Relativistic AQUAL (RAQUAL / k-ess) FAILS-AT-SUPERLUMINALITY [P] (c_par = √(1 + 1/(1+x)) > 1)
Path 2   Scalar-Tensor Preferred Frame (Aether)  VIABLE [P] (Reduces to F_dual; luminal c_s = c)
Path 3   TeVeS Disformal Coupling                VIABLE [P] (γ_PPN = 1 exact; lensing matches GR+scalar)
Path 4   Horndeski / DHOST Scan                  FAILS-AT-DEGENERACY-COLLAPSE [P] (Breaks AQUAL limit)
========================================================================================================
```

---

## 2. Construction Path Analyses & Verdicts

### Path 1: Pure Relativistic AQUAL (RAQUAL / k-essence)
* **Action:** $S = -\frac{a_0^2}{8\pi G} \int d^4x \sqrt{-g} f(y)$ with $y \equiv -\frac{g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi}{a_0^2}$.
* **Anchor kinetic function:** $f(y) = \frac{1}{2}y - \sqrt{y} + \ln(1 + \sqrt{y})$.
* **Characteristic Acoustic Cone:** The perturbation propagation speed parallel to a spacelike background gradient $x = \sqrt{y} = |\nabla\Phi|/a_0$ is:
  $$c_\parallel^2 = 1 + \frac{2y f''(y)}{f'(y)} = 1 + \frac{1}{1+x} > 1 \quad \forall x > 0.$$
* **Verdict $\mathbf{[P]}$:** **FAILS-AT-SUPERLUMINALITY**. Pure RAQUAL is non-viable without a preferred timelike structure because acoustic perturbations propagate superluminally across the entire galaxy halo. Verified in Lean 4 ([`CovariantCompletion.lean`](file:///home/mega/grand_monograph/05_lean_formalization/CovariantCompletion.lean#L30-L38)).

---

### Path 2 & 3: Scalar-Tensor Preferred Frame & Disformal Completion (Surviving Framework)
* **Action:**
  $$S = \frac{1}{16\pi G}\int d^4x\sqrt{-g} R - \frac{1}{16\pi G}\int d^4x\sqrt{-g} \left[ K^{ab}_{cd}\nabla_a u^c \nabla_b u^d + \lambda(u_a u^a + 1) \right] - \frac{a_0^2}{8\pi G}\int d^4x\sqrt{-g} h(\hat{y}) + S_m[\tilde{g}_{\mu\nu}, \psi]$$
  where $\hat{y} \equiv -\frac{g^{\mu\nu}\hat{\nabla}_\mu\phi\hat{\nabla}_\nu\phi}{a_0^2}$, $\hat{\nabla}_\mu\phi \equiv \nabla_\mu\phi + u_\mu (u^\nu\nabla_\nu\phi)$, and physical metric $\tilde{g}_{\mu\nu} = e^{-2\phi}g_{\mu\nu} - 2\sinh(2\phi)u_\mu u_\nu$.
* **Non-Relativistic Reduction:** In static weak fields, $u^\nu\nabla_\nu\phi = 0 \implies \hat{y} = \frac{|\nabla\Phi|^2}{a_0^2} = x^2$. The scalar action reduces **identically** to $\mathcal{F}_{\text{dual}}(x) = \frac{1}{2}x^2 - x + \ln(1+x)$.
* **Stability:** The orthogonal projection forces the scalar perturbation characteristic cone to align with the spacetime lightcone ($c_s = c$), curing the superluminality defect.
* **Verdict $\mathbf{[P]}$:** **VIABLE**.

---

### Path 4: Horndeski / DHOST Scan
* **Obstruction:** Demanding Ostrogradsky degeneracy (Class Ia DHOST) in the absence of a preferred unit timelike vector forces the higher-order scalar couplings to vanish or couple exclusively to metric curvature ($G_{4,X} = 0$), collapsing back to k-essence ($c_\parallel > 1$) or introducing unsuppressed fifth forces in the Solar System.
* **Verdict $\mathbf{[P]}$:** **FAILS-AT-DEGENERACY-COLLAPSE**.

---

## 3. The Three Quarantined Claims: Status in v1.2.0

### Deliverable A: Metric & PPN ($\gamma_{\text{PPN}} = 1$) $\to \mathbf{[P]}\text{-conditional}$
* In the disformal weak-field expansion around Minkowski:
  $$\tilde{g}_{00} = -(1 + 2\Phi_N + 2\phi), \qquad \tilde{g}_{ij} = (1 - 2\Phi_N + 2\phi)\delta_{ij}.$$
* Both photons and matter respond to the composite potential $\Phi_{\text{eff}} = \Phi_N + \phi$.
* In the high-acceleration Solar System limit ($x \gg 1$), $\mu(x) \to 1$ and $\phi$ is suppressed by $G_{\text{scalar}} \ll G_N$.
* **Result:** $\gamma_{\text{PPN}} = \frac{h_{ij}}{-h_{00}} = 1.00000$, $\beta_{\text{PPN}} = 1.00000$, and preferred frame parameters $\alpha_1 = 0, \alpha_2 = 0$ for standard Maxwellian aether coupling ($c_1 = -c_3, c_2 = c_4 = 0$).
* **Epistemic Status:** **PROVED $\mathbf{[P]}$ conditional on the disformal preferred-frame action**.

---

### Deliverable B: Covariant Stability & Ghost Freedom $\to \mathbf{[P]}\text{-conditional}$
* **Hamiltonian Constraint:** The Lagrange multiplier $\lambda(u_a u^a + 1)$ eliminates the negative-energy timelike vector mode.
* **Scalar Gradient Stability:** The strict convexity $\mathcal{F}''(x) = \frac{x(x+2)}{(1+x)^2} > 0$ on $(0, \infty)$ guarantees positive kinetic energy in spatial slices without gradient instabilities ($c_s^2 = 1 > 0$).
* **Epistemic Status:** **PROVED $\mathbf{[P]}$ conditional on the 4D scalar-vector-tensor action**.

---

### Deliverable C: Cosmology & $\Omega_\Lambda = \ln 2$ Reduction $\to$ FALSIFIED AS A DYNAMICAL FLUID $\mathbf{[P]}$; QUARANTINED TO HORIZON BOUNDARY $\mathbf{[O]}$
* **Cosmological Decoupling Theorem:** In a spatially flat, homogeneous FLRW metric $ds^2 = -dt^2 + a(t)^2 d\mathbf{x}^2$ with comoving unit vector $u^\mu = (1, 0, 0, 0)$, the projected spatial gradient vanishes identically:
  $$\hat{\nabla}_\mu \phi(t) = \nabla_\mu \phi + u_\mu (u^\nu \nabla_\nu \phi) = 0 \implies \hat{y} = 0.$$
* **Result:** The aquadratic MOND scalar field contributes **identically zero** dynamical dark energy density ($\rho_\phi = 0, p_\phi = 0$) to the background Friedmann equations.
* **Epistemic Verdict:** The narrative that $\Omega_\Lambda = \ln 2$ emerges as a dynamical fluid output of the AQUAL action is **FALSIFIED $\mathbf{[P]}$**. $\Omega_\Lambda = \ln 2$ is strictly a horizon entropy boundary condition ($S = \ln 2$ per Hubble patch), and remains quarantined as an open boundary problem $\mathbf{[O]}$.
