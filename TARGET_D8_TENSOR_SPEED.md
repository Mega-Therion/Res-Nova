# 🌌 Target D8 & D8b: Tensor-Mode Speed vs. GW170817 & Disformal Cone Confrontation
**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Date:** 2026-08-14  
**Framework:** Res-Nova / Chyren Epistemic Architecture (v1.3.1)  
**Standard:** Sovereign Epistemic Covenant (`[P]` Proved, `[D]` Direct Empirical, `[C]` Cited, `[O]` Open / Quarantined)

---

## 0. Pre-Registered Epistemic Decision Rule & Referee Audit

```
========================================================================================================
EPISTEMIC AUDIT SUMMARY (TARGET D8 & D8b: TENSOR SPEED VS GW170817)
========================================================================================================
1. Einstein-Frame Vector Sector Identity:
   c₁₃ ≡ c₁ + c₃ = 0 is an EXACT ALGEBRAIC IDENTITY forced by the Maxwellian field strength
   F_μν^(u) F_(u)^μν, yielding Einstein-frame tensor speed c_T(g) = 1 [P].

2. Preferred-Frame PPN Parameter α₁:
   Foster–Jacobson evaluation for Maxwellian aether yields α₁ = -2K [P], not 0.
   Solar System bounds (|α₁| ≲ 10⁻⁴) strictly constrain |K| ≲ 5 × 10⁻⁵ [P].

3. Physical-Frame Disformal Null Cone Split:
   Photons propagate on the physical disformal metric g̃_μν = e^{-2ϕ} g_μν - 2 sinh(2ϕ) u_μ u_ν.
   In comoving coordinates (u^μ = (1, 0, 0, 0)), the photon coordinate speed is c_γ = e^{2ϕ} [P].
   The tensor mode speed ratio is c_T(g) / c_γ(g̃) = e^{-2ϕ} [P].

4. Confrontation with GW170817 (|c_T/c_γ - 1| ≤ 10⁻¹⁵):
   The speed ratio equals unity IF AND ONLY IF ϕ = 0 [P].
   In any deep-MOND halo (ϕ ~ 10⁻⁶) or cosmological background (ϕ ~ 10⁻¹ to 1),
   |c_T/c_γ - 1| ≈ 2|ϕ| ≫ 10⁻¹⁵.
   VERDICT: The specific disformal map A(ϕ) = e^{-2ϕ}, B(ϕ) = -2 sinh(2ϕ) is FALSIFIED [P]
   by GW170817 as a viable disformal completion, necessitating either a strictly conformal map
   (B = 0) or the Skordis–Złośnik luminal action subclass.
========================================================================================================
```

---

## 1. Mathematical Derivation of Cones and Speeds

### 1.1 Einstein-Frame Vector Kinetic Identity
The vector Lagrangian is:
$$\mathcal{L}_u = -\frac{K}{32\pi G} F_{\mu\nu}^{(u)} F_{(u)}^{\mu\nu} = -\frac{K}{16\pi G} \left( \nabla_\mu u_\nu \nabla^\mu u^\nu - \nabla_\mu u_\nu \nabla^\nu u^\mu \right).$$

Matching against the Jacobson–Mattingly Einstein–Aether parameterization:
$$c_1 = +\frac{K}{2}, \quad c_3 = -\frac{K}{2}, \quad c_2 = 0, \quad c_4 = 0.$$
$$c_{13} \equiv c_1 + c_3 = +\frac{K}{2} - \frac{K}{2} = 0 \quad \text{\textbf{IDENTICALLY}} \quad \mathbf{[P]}.$$
$$c_T^2(g) = \frac{1}{1 - c_{13}} = \frac{1}{1 - 0} = 1 \implies c_T(g) = c \quad \mathbf{[P]}.$$

---

### 1.2 Preferred-Frame PPN $\alpha_1$ Parameter
Using the Foster–Jacobson formula for Einstein–Aether theories:
$$\alpha_1 = -\frac{8(c_3^2 + c_1 c_4)}{2c_1 - c_1^2 + c_3^2} = -\frac{8((-K/2)^2 + 0)}{2(K/2) - (K/2)^2 + (-K/2)^2} = -\frac{2K^2}{K} = -2K \quad \mathbf{[P]}.$$

Observational Solar System bounds ($|\alpha_1| \lesssim 10^{-4}$) do not force $K = 0$, but place an empirical upper bound on the vector coupling:
$$|K| \lesssim 5 \times 10^{-5} \quad \mathbf{[P]}.$$

---

### 1.3 Disformal Photon Speed & Null Cone Split
The physical (Jordan-frame) metric is:
$$\tilde{g}_{\mu\nu} = A(\phi) g_{\mu\nu} + B(\phi) u_\mu u_\nu, \qquad A(\phi) = e^{-2\phi}, \quad B(\phi) = -2\sinh(2\phi).$$

In cosmological FLRW or static isotropic halos where $u^\mu = (1, 0, 0, 0)$ and $u_\mu = -1$:
$$\tilde{g}_{00} = -(A - B) = -\left( e^{-2\phi} - (-2\sinh(2\phi)) \right) = -e^{2\phi},$$
$$\tilde{g}_{ij} = A\,\delta_{ij} = e^{-2\phi}\,\delta_{ij}.$$

For photon null geodesics ($d\tilde{s}^2 = \tilde{g}_{\mu\nu} dx^\mu dx^\nu = 0$):
$$-e^{2\phi} dt^2 + e^{-2\phi} d\mathbf{x}^2 = 0 \implies c_\gamma^2 = \left(\frac{|d\mathbf{x}|}{dt}\right)^2 = \frac{e^{2\phi}}{e^{-2\phi}} = e^{4\phi} \implies c_\gamma = e^{2\phi} \quad \mathbf{[P]}.$$

Because tensor perturbations of the Einstein–Hilbert action travel at coordinate speed $c_T(g) = 1$, the observationally measured speed ratio is:
$$\frac{c_T}{c_\gamma} = \frac{1}{e^{2\phi}} = e^{-2\phi} \quad \mathbf{[P]}.$$

---

### 1.4 Confrontation with GW170817 Bound ($|c_T/c_\gamma - 1| \le 10^{-15}$)
The fractional speed deviation is:
$$\left| \frac{c_T}{c_\gamma} - 1 \right| = \left| e^{-2\phi} - 1 \right| \approx 2|\phi| + \mathcal{O}(\phi^2).$$

* **Exact Luminality Condition:** $e^{-2\phi} = 1 \iff \phi = 0$ identically $\mathbf{[P]}$.
* **Deep-MOND Galactic Halo:** For typical galaxy potentials $\phi \sim \Phi_N/c^2 \sim 10^{-6}$ to $10^{-5}$:
  $$\left| \frac{c_T}{c_\gamma} - 1 \right| \sim 2 \times 10^{-6} \gg 10^{-15} \quad (\text{Violated by } 9 \text{ orders of magnitude}).$$
* **Cosmological Background ($z \sim 1$):** If $\phi \sim \mathcal{O}(0.1)$:
  $$\left| \frac{c_T}{c_\gamma} - 1 \right| \sim 0.18 \gg 10^{-15} \quad (\text{Violated by } 14 \text{ orders of magnitude}).$$

**Falsification Verdict $\mathbf{[P]}$:** The preferred-frame disformal completion with $B(\phi) = -2\sinh(2\phi)$ is **FALSIFIED $\mathbf{[P]}$** by GW170817 / GRB 170817A.

---

## 2. Surviving Covariant Pathways & Remediation

To preserve the derived dual-channel closure $\mu(x) = \frac{x}{1+x}$ while satisfying GW170817, the theory is restricted to two viable branches:

1. **Strictly Conformal Metric Coupling ($B(\phi) \equiv 0$):**
   * $\tilde{g}_{\mu\nu} = e^{-2\phi} g_{\mu\nu}$.
   * Null cones coincide identically ($c_T = c_\gamma = c$), satisfying GW170817 identically without fine-tuning.
   * Lensing potential $\Phi_{\text{lens}} = \frac{1}{2}(\Phi + \Psi) = \Phi_N$ receives zero scalar boost, requiring a separate vector-shear lensing mechanism (e.g. generalized Skordis–Złośnik vector coupling).
2. **Skordis–Złośnik Luminal Class (Action on Physical Frame):**
   * Graviton and photon kinetic operators are written directly on the physical metric $\tilde{g}_{\mu\nu}$, locking both null cones together by construction.

---

## 3. Lean 4 Formal Proof Footprint

All theorems have been compiled with 0 errors, 0 warnings, and 0 `sorry` in [`05_lean_formalization/TensorSpeed.lean`](05_lean_formalization/TensorSpeed.lean):
* `c_T_sq_at_zero`: Proves $c_T^2 = 1$ when $c_{13} = 0$.
* `maxwellian_c13_vanishes`: Proves $c_1 + c_3 = 0$ identically.
* `einstein_frame_tensor_speed_luminal`: Proves $c_T(g) = 1$.
* `foster_jacobson_alpha_1_eval`: Proves $\alpha_1 = -2K$.
* `disformal_photon_speed_sq`: Proves $c_\gamma^2 = e^{4\phi}$.
* `speed_ratio_unity_iff`: Proves $c_T/c_\gamma = 1 \iff \phi = 0$.
* `speed_ratio_lt_one_of_pos`: Proves subluminality for $\phi > 0$.
* `gw170817_deviation_of_pos`: Proves $|c_T/c_\gamma - 1| = 1 - e^{-2\phi} > 0$ for $\phi > 0$.

**Axiom Footprint:** `[propext, Classical.choice, Quot.sound]`.
