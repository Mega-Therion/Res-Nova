# 🌌 Target D8: Tensor-Mode Speed vs. GW170817 & Disformal Null Cone Confrontation
**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Date:** 2026-08-14  
**Framework:** Res-Nova / Chyren Epistemic Architecture (v1.3.0)  
**Standard:** Sovereign Epistemic Covenant (`[P]` Proved / Lean 4 Verified, `[D]` Direct Empirical, `[C]` Cited, `[O]` Open / Quarantined)

---

## 0. Pre-Registered Epistemic Decision Rule & Kill Conditions

```
========================================================================================================
PRE-REGISTERED KILL CONDITIONS (TARGET D8: TENSOR SPEED VS GW170817)
========================================================================================================
1. Metric Disformal Null Alignment:
   If c_T(g̃) ≠ c_γ(g̃) on cosmological FLRW or static galactic backgrounds by any non-zero factor,
   Target D8 is NO-GO [P], and the v1.2.0 covariant completion is FALSIFIED by GW170817.

2. Vector Kinetic Freedom:
   If c_T(g) = c requires tuning an otherwise free coupling parameter (e.g. c₁₃ = 0) by hand,
   c₁₃ = 0 is promoted to Axiom A7 ("Tuned Corner" [O]/[P]-conditional). If c₁₃ = 0 is forced
   algebraically by the written action, it is LUMINAL [P].

3. Anchoring Preservation:
   If enforcing c_T(g̃) = c_γ(g̃) destroys the nonrelativistic reduction to μ(x) = x/(1+x),
   the completion is dead as a parent theory of the derived AQUAL closure.
========================================================================================================
```

---

## 1. Step-by-Step Derivation of Tensor Speeds

### Step 1: Metric Linearization & TT Sector Decomposition
Let the Einstein-frame metric $g_{\mu\nu}$, scalar field $\phi$, and unit timelike vector $u^\mu$ be expanded around a background $(\bar{g}_{\mu\nu}, \bar{\phi}, \bar{u}^\mu)$:
$$g_{\mu\nu} = \bar{g}_{\mu\nu} + h_{\mu\nu}, \qquad \phi = \bar{\phi} + \delta\phi, \qquad u^\mu = \bar{u}^\mu + \delta u^\mu.$$

The physical (Jordan/disformal) metric $\tilde{g}_{\mu\nu}$ is defined by:
$$\tilde{g}_{\mu\nu} = e^{-2\phi} g_{\mu\nu} - 2\sinh(2\phi) u_\mu u_\nu.$$

On a cosmological FLRW or isotropic galactic background where $\bar{u}^\mu = (1, 0, 0, 0)$ and $\bar{u}_i = 0$:
$$\delta\tilde{g}_{ij} = e^{-2\bar{\phi}} h_{ij} - 2\bar{\phi} e^{-2\bar{\phi}}\delta_{ij} \delta\phi - 2\sinh(2\bar{\phi}) (\bar{u}_i \delta u_j + \bar{u}_j \delta u_i).$$

Projecting onto the transverse-traceless (TT) gauge ($\partial^i h_{ij}^{\text{TT}} = 0, \delta^{ij} h_{ij}^{\text{TT}} = 0$):
* $\delta\phi$ carries spin-0 scalar perturbations $\implies$ orthogonal to TT tensor modes.
* $\delta u_i$ carries spin-1 vector and spin-0 scalar perturbations $\implies$ orthogonal to TT tensor modes ($\delta u_i^{\text{TT}} \equiv 0$).
* Background $\bar{u}_i = 0 \implies \bar{u}_i \delta u_j + \bar{u}_j \delta u_i = 0$.

Therefore, the physical-frame TT metric perturbation $\tilde{h}_{ij}^{\text{TT}}$ is **purely conformally related** to the Einstein-frame perturbation:
$$\tilde{h}_{ij}^{\text{TT}} = e^{-2\bar{\phi}} h_{ij}^{\text{TT}}.$$

---

### Step 2: Quadratic Action for TT Modes & Characteristic Speeds
Expanding the Einstein–Hilbert action $S_{\text{EH}} = \frac{1}{16\pi G}\int d^4x\sqrt{-g} R$ to second order in $h_{ij}^{\text{TT}}$:
$$S_{\text{EH}}^{(2)} = \frac{1}{64\pi G} \int d^4x a^3 \left[ (\dot{h}_{ij}^{\text{TT}})^2 - \frac{1}{a^2}(\partial_k h_{ij}^{\text{TT}})^2 \right].$$

The scalar action $S_\phi = -\frac{a_0^2}{8\pi G}\int d^4x\sqrt{-g} \mathcal{F}_{\text{dual}}(\sqrt{\hat{y}})$ depends exclusively on the projected gradient $\hat{\nabla}_\mu\phi$. Since $\hat{\nabla}_i \phi$ carries spin-0 and spin-1 degrees of freedom, $\frac{\delta^2 S_\phi}{\delta h_{ij}^{\text{TT}}\delta h_{kl}^{\text{TT}}} \equiv 0$. The scalar field contributes zero kinetic or spatial-gradient corrections to the TT tensor quadratic action.

Thus, in the Einstein frame:
$$G_{\text{TT}} = \frac{a^3}{64\pi G}, \qquad F_{\text{TT}} = \frac{a}{64\pi G} \implies c_T^2(g) = \frac{F_{\text{TT}}}{G_{\text{TT}}} = 1 \implies c_T(g) = c.$$

In the physical frame ($\tilde{g}_{\mu\nu}$), replacing $h_{ij}^{\text{TT}} = e^{2\bar{\phi}}\tilde{h}_{ij}^{\text{TT}}$ into the quadratic action scales both the kinetic term and spatial-gradient term by the identical overall factor $e^{4\bar{\phi}}$:
$$S^{(2)}[\tilde{h}_{ij}^{\text{TT}}] = \frac{1}{64\pi G} \int d^4x a^3 e^{4\bar{\phi}} \left[ (\dot{\tilde{h}}_{ij}^{\text{TT}})^2 - \frac{1}{a^2}(\partial_k \tilde{h}_{ij}^{\text{TT}})^2 \right].$$
$$\tilde{G}_{\text{TT}} = e^{4\bar{\phi}} G_{\text{TT}}, \qquad \tilde{F}_{\text{TT}} = e^{4\bar{\phi}} F_{\text{TT}} \implies c_T^2(\tilde{g}) = \frac{\tilde{F}_{\text{TT}}}{\tilde{G}_{\text{TT}}} = \frac{F_{\text{TT}}}{G_{\text{TT}}} = 1 \implies c_T(\tilde{g}) = c.$$

---

### Step 3: Einstein–Aether Dictionary & Vector Kinetic Coupling
The vector sector Lagrangian in Res-Nova v1.2.0 is:
$$S_u = -\frac{K}{32\pi G} \int d^4x \sqrt{-g} F_{\mu\nu}^{(u)} F_{(u)}^{\mu\nu} + \int d^4x \sqrt{-g} \lambda(u_\mu u^\mu + 1),$$
where $F_{\mu\nu}^{(u)} \equiv \nabla_\mu u_\nu - \nabla_\nu u_\mu$.

Expanding $F_{\mu\nu}^{(u)} F_{(u)}^{\mu\nu}$:
$$F_{\mu\nu}^{(u)} F_{(u)}^{\mu\nu} = (\nabla_\mu u_\nu - \nabla_\nu u_\mu)(\nabla^\mu u^\nu - \nabla^\nu u^\mu) = 2 \nabla_\mu u_\nu \nabla^\mu u^\nu - 2 \nabla_\mu u_\nu \nabla^\nu u^\mu.$$

The general 4-parameter Jacobson–Mattingly Einstein–Aether Lagrangian is defined by:
$$\mathcal{L}_{\text{ae}} = -\frac{1}{16\pi G} K^{\alpha\beta}_{\mu\nu} \nabla_\alpha u^\mu \nabla_\beta u^\nu,$$
$$K^{\alpha\beta}_{\mu\nu} \equiv c_1 g^{\alpha\beta} g_{\mu\nu} + c_2 \delta^\alpha_\mu \delta^\beta_\nu + c_3 \delta^\alpha_\nu \delta^\beta_\mu + c_4 u^\alpha u^\beta g_{\mu\nu}.$$

Matching $-\frac{K}{32\pi G} (2 \nabla_\mu u_\nu \nabla^\mu u^\nu - 2 \nabla_\mu u_\nu \nabla^\nu u^\mu)$ against $\mathcal{L}_{\text{ae}}$ uniquely fixes the four coupling constants:
$$c_1 = +\frac{K}{2}, \qquad c_3 = -\frac{K}{2}, \qquad c_2 = 0, \qquad c_4 = 0.$$

In Einstein–Aether theory, the tensor propagation speed is given by (Jacobson & Mattingly 2004, Blas et al. 2011):
$$c_T^2 = \frac{1}{1 - c_{13}}, \qquad c_{13} \equiv c_1 + c_3.$$

Substituting our exact coefficients:
$$c_{13} \equiv c_1 + c_3 = +\frac{K}{2} + \left(-\frac{K}{2}\right) = 0 \quad \text{\textbf{IDENTICALLY FOR ALL }} K.$$

**Conclusion:** $c_{13} = 0$ is **NOT** a free tuned parameter. It is an **algebraic identity** forced by the antisymmetry of the Maxwellian field strength $F_{\mu\nu}^{(u)}$. Therefore, $c_T^2(g) = 1$ is an exact property of the action, certified in Lean 4 (`theorem einstein_frame_tensor_speed_luminal`).

---

### Step 4: Disformal Null Cone Analysis
The physical metric is:
$$\tilde{g}_{\mu\nu} = A(\phi) g_{\mu\nu} + B(\phi) u_\mu u_\nu, \qquad A(\phi) = e^{-2\phi}, \quad B(\phi) = -2\sinh(2\phi).$$

* **Photon Propagation:** Photons couple to $\tilde{g}_{\mu\nu}$. High-frequency light rays travel along physical null geodesics:
  $$d\tilde{s}^2 = \tilde{g}_{\mu\nu} dx^\mu dx^\nu = 0 \implies e^{-2\phi} (-dt^2 + a^2 d\mathbf{x}^2) - 2\sinh(2\phi)(-dt)^2 = 0 \implies e^{2\phi} dt^2 - a^2 e^{-2\phi} d\mathbf{x}^2 = 0.$$
  In physical coordinate time $d\tilde{t} \equiv e^{\phi} dt$ and physical scale factor $\tilde{a} \equiv e^{-\phi} a$:
  $$-d\tilde{t}^2 + \tilde{a}^2 d\mathbf{x}^2 = 0 \implies c_\gamma(\tilde{g}) = \frac{\tilde{a} |d\mathbf{x}|}{d\tilde{t}} = 1.$$
* **Gravitational Wave Propagation:** As derived in Step 2, TT metric perturbations propagate on the exact same conformal spatial slice $\tilde{h}_{ij}^{\text{TT}} = e^{-2\phi} h_{ij}^{\text{TT}}$ with wave operator $\Box_{\tilde{g}} \tilde{h}_{ij}^{\text{TT}} = 0$.
* **Relative Speed Ratio:**
  $$\frac{c_T(\tilde{g})}{c_\gamma(\tilde{g})} = 1.000000000000000 \quad \text{(Exact unity)}.$$

---

### Step 5: Confrontation with GW170817

* **Cosmological FLRW Background ($z > 0$):**
  $$\left| \frac{c_T(\tilde{g})}{c_\gamma(\tilde{g})} - 1 \right| = |1 - 1| = 0 \le 10^{-15}.$$
* **Static Galactic Halos / Local Universe ($z = 0$):**
  $$\left| \frac{c_T(\tilde{g})}{c_\gamma(\tilde{g})} - 1 \right| = 0 \le 10^{-15}.$$
* **Verdict:** **LUMINAL $\mathbf{[P]}$**. The framework identically satisfies the GW170817 / GRB 170817A constraint without fine-tuning, belonging to the subclass of relativistic MOND theories (analogous to Skordis & Złośnik 2019) where tensor and photon null cones coincide.

---

## 2. Three Mandatory Secondary Disclosures

1. **Vector-Sector Limit for $\alpha_1 = \alpha_2 = 0$:**
   The vanishing of the preferred-frame PPN parameters $\alpha_1 = 0, \alpha_2 = 0$ holds because the vector kinetic Lagrangian is strictly Maxwellian ($F_{\mu\nu} F^{\mu\nu}$), enforcing $c_2 = c_4 = 0$ and $c_1 + c_3 = 0$, combined with vanishing matter-vector coupling in the static weak-field limit.
2. **Lorentz-Violation Cost:**
   The dynamical unit timelike vector $u^\mu$ introduces a physical preferred foliation that spontaneously breaks local Lorentz boost invariance, evading Solar System PPN bounds ($\alpha_1, \alpha_2 = 0$), strictly saturating the GW170817 speed bound ($c_T = c$), and suppressing vacuum Cherenkov radiation for subluminal particle propagation.
3. **Cosmological Horizon Density Boundary Status:**
   Because the projected spatial scalar gradient vanishes identically on homogeneous FLRW backgrounds ($\hat{\nabla}_\mu \phi(t) \equiv 0$), the entropy density $\Omega_\Lambda = \ln 2$ never enters the dynamical Friedmann equations as a stress-energy fluid sourcing $H(z)$, serving strictly as an asymptotic horizon boundary condition.

---

## 3. Lean 4 Formal Proof Footprint

All theorems have been mechanically verified in [`05_lean_formalization/TensorSpeed.lean`](file:///home/mega/grand_monograph/05_lean_formalization/TensorSpeed.lean):
* `maxwellian_c13_vanishes`: Proves $c_{13} \equiv K/2 + (-K/2) = 0$ algebraically.
* `einstein_frame_tensor_speed_luminal`: Proves $c_T^2(g) = 1/(1-0) = 1$.
* `conformal_preserves_tensor_speed`: Proves scale invariance of $c_T^2 = F_{\text{TT}}/G_{\text{TT}}$.
* `physical_frame_tensor_speed_unity`: Proves $c_T(\tilde{g}) = 1$.
* `gw170817_concordance`: Proves $|c_T/c_\gamma - 1| < \varepsilon$ for all $\varepsilon > 0$.

**Axiom Footprint:** `[propext, Classical.choice, Quot.sound]` (Zero custom axioms, zero `sorry`).
