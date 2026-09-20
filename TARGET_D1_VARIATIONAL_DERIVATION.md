# 🔬 Target D1: Symbolic & Variational Derivation Dossier of $\mu(x)$ Closures

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


**Author:** R.W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))
**Date:** 2026-08-14  
**Framework:** Res-Nova  
**Epistemic Boundary:** $\mathbf{[P]}$ for variational calculus, $\mathbf{[O]}$ for physical Lagrangian selection

---

> **⚠️ SUPERSESSION BANNER 2026-09-12.** This document's variational calculus is `[P]` and stands. But its headline resulting closure μ_dual(x)=x/(1+x) is **FALSIFIED** (`TARGET_D7` §4/§11: solar-system residual 5.7×10⁵ over the Cassini Q₂ bound, rescue routes exhausted). The live closure is μ_std(x)=x/√(1+x²), derived and verified in `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` (§1/§3/§5 re-run complete 2026-09-12 under F′=xμ); its structural uniqueness is `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md`, with the coordinate choice empirically decided (§8). Read this document as the historical derivation of the falsified branch: the variational machinery transfers; the selected closure does not. Old status "needs re-check against μ_std" — the re-check lives in the supplement.

## 1. Problem Statement & The Variational Question

In modified gravity of the AQUAL family (Bekenstein & Milgrom 1984), the weak-field scalar action takes the form:
$$S = \int d^4x \left[ -\frac{1}{8\pi G} \nabla\Phi_N \cdot \nabla\Phi - \frac{a_0^2}{4\pi G} \mathcal{F}\left( \frac{|\nabla\Phi|}{a_0} \right) \right], \qquad x \equiv \frac{|\nabla\Phi|}{a_0}.$$

The Euler–Lagrange variation with respect to $\Phi$ yields the field equation:
$$\nabla \cdot \left[ \mathcal{F}'(x) \frac{\nabla\Phi}{|\nabla\Phi|} \right] = \frac{4\pi G}{a_0} \rho_{\text{bar}} \iff \nabla \cdot \left[ \mu(x) \nabla\Phi \right] = 4\pi G \rho_{\text{bar}}, \quad \text{where } \mu(x) \equiv \frac{\mathcal{F}'(x)}{x}.$$

---

## 2. Symbolic Derivation of the Three Canonical Branches

### Branch A: Single-Channel Kinetic Potential $\mathcal{F}_{\text{single}}(x) = x \operatorname{arcsinh}(x) - \sqrt{1+x^2}$
$$\frac{d\mathcal{F}_{\text{single}}}{dx} = \operatorname{arcsinh}(x) + \frac{x}{\sqrt{1+x^2}} - \frac{x}{\sqrt{1+x^2}} = \operatorname{arcsinh}(x).$$
* **Resulting Interpolation Function:** $\mu_{\text{arcsinh}}(x) = \frac{\operatorname{arcsinh}(x)}{x}$.
* **Asymptotic Limits:**
  - Weak acceleration ($x \ll 1$): $\mu_{\text{arcsinh}}(x) \to 1 - \frac{x^2}{6} \to 1$ (Does **not** recover deep-MOND $\mu \to x$).
  - Strong acceleration ($x \gg 1$): $\mu_{\text{arcsinh}}(x) \to \frac{\ln(2x)}{x} \to 0$ (Inverts Newtonian gravity).
* **Definitive No-Go Verdict $\mathbf{[P]}$:** The potential $\mathcal{F}_{\text{single}}(x) = x\operatorname{arcsinh}(x) - \sqrt{1+x^2}$ **cannot produce MOND phenomenology or rotation curve flattening**.

---

### Branch B: Dual-Channel $\tau$-Tension Action (G.O.D. Paper 09)
To obtain the rational simple interpolation function $\mu(x) = \frac{x}{1+x}$:
$$\mathcal{F}'(x) = x \cdot \mu(x) = \frac{x^2}{1+x} = x - 1 + \frac{1}{1+x}.$$
Integrating with respect to $x$ yields the exact dual-channel potential:
$$\mathcal{F}_{\text{dual}}(x) = \frac{1}{2}x^2 - x + \ln(1+x).$$
* **Resulting Interpolation Function:** $\mu_{\text{dual}}(x) = \frac{x}{1+x}$.
* **Physical Acceleration Solution:**
  $$g \cdot \left(\frac{g/a_0}{1 + g/a_0}\right) = g_{\text{bar}} \implies g = g_{\text{bar}} \left[ \frac{1}{2} + \sqrt{\frac{1}{4} + \frac{a_0}{g_{\text{bar}}}} \right].$$
* **Kernel Verification $\mathbf{[P]}$:** Verified in Lean 4 ([`GODActionKinematics.lean`](05_lean_formalization/GODActionKinematics.lean) & [`ITActionClosure.lean`](05_lean_formalization/ITActionClosure.lean)).

---

### Branch C: Classical MOND Pythagorean Potential (Famaey & Binney 2005)
To obtain the standard square-root interpolation function $\mu(x) = \frac{x}{\sqrt{1+x^2}}$:
$$\mathcal{F}'(x) = \frac{x^2}{\sqrt{1+x^2}}.$$
Integrating with respect to $x$ yields:
$$\mathcal{F}_{\text{MOND}}(x) = \frac{1}{2} \left[ x\sqrt{1+x^2} - \operatorname{arcsinh}(x) \right].$$
* **Resulting Interpolation Function:** $\mu_{\text{MOND}}(x) = \frac{x}{\sqrt{1+x^2}}$.
* **Kernel Verification $\mathbf{[P]}$:** Verified in Lean 4 ([`MuProjection.lean`](05_lean_formalization/MuProjection.lean)).

---

## 3. The Definitive Falsification Contract

```
========================================================================================================
BRANCH       ACTION POTENTIAL F(x)                  DERIVED μ(x)            SPARC GENERALIZATION STATUS
========================================================================================================
Branch A     x·arcsinh(x) - √(1+x²)                 arcsinh(x)/x            FALSIFIED [P] (Wrong limits)
Branch B     ½x² - x + ln(1+x)                      x / (1+x)               5-Fold CV Median χ²/N_g = 14.68
Branch C     ½[x√(1+x²) - arcsinh(x)]               x / √(1+x²)             Standard Phenomenological Fit
========================================================================================================
```
* **Pre-Registered Falsification Rule:** Any manuscript asserting that $\mathcal{F}_{\text{single}}(x) = x\operatorname{arcsinh}(x) - \sqrt{1+x^2}$ generates galactic dynamics is mathematically falsified $\mathbf{[P]}$. The valid variational foundation of the G.O.D. / Res-Nova framework rests strictly on **Branch B ($\mathcal{F}_{\text{dual}}$)**.
