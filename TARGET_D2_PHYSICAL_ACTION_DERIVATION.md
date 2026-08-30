# TARGET D2: Physical Action Derivation

**Status:** D2_PROPOSED — Derivation framework established; information-theoretic necessity of Padé constraint still open.
**Last updated:** 2026-08-16
**Author:** R.W. Yett / Sovereign Architecture Group
**Epistemic tag:** [P] (proved sections) / [O] (open sections) — see inline tags

---

## 1. Problem Statement

The dual-channel action is postulated as:

$$\mathcal{F}_{\text{dual}}(x) = \tfrac{1}{2}x^2 - x + \ln(1+x)$$

where $x = |\mathbf{a}|/a_0$ is the acceleration ratio. Its Euler–Lagrange variation yields the AQUAL modified Poisson equation with the "simple" MOND interpolation function $\mu(x) = x/(1+x)$.

**The question:** *Why this specific functional form?* What physical or mathematical principle determines $\mathcal{F}_{\text{dual}}$ — and is it uniquely determined?

This document establishes that $\mathcal{F}_{\text{dual}}$ is the **unique** action satisfying four independent structural constraints: (i) constitutive-relation structure, (ii) Padé minimality, (iii) odds-ratio / Bayesian probability structure, and (iv) dual-channel cancellation. The necessity of constraint (ii) remains the key open question.

---

## 2. Necessary Conditions

Any viable MOND action $F(x)$ must satisfy the following physical constraints:

| ID | Constraint | Mathematical form | Physical meaning |
|----|-----------|-------------------|------------------|
| C1 | Normalization | $F(0) = 0$ | Zero action at zero acceleration |
| C2 | Convexity | $F''(x) > 0 \;\forall\, x > 0$ | Stability, well-posedness |
| C3 | Newtonian limit | $F(x)/x^2 \to \tfrac{1}{2}$ as $x \to \infty$ | Recovers Newton at high acceleration |
| C4 | Deep-MOND limit | $F(x)/x^3 \to c > 0$ as $x \to 0$ | Gives $a \sim \sqrt{GMa_0}/r$ at low acceleration |
| C5 | Analyticity | $F$ is real-analytic at $x = 0$ | Regularity, no singularities |

**Verification for $\mathcal{F}_{\text{dual}}$** [P]:

- **C1:** $\mathcal{F}_{\text{dual}}(0) = 0 - 0 + \ln(1) = 0$ ✓
- **C2:** $\mathcal{F}_{\text{dual}}''(x) = 1 - \frac{1}{(1+x)^2} = \frac{2x + x^2}{(1+x)^2} > 0$ for $x > 0$ ✓
- **C3:** $\lim_{x\to\infty} \mathcal{F}_{\text{dual}}(x)/x^2 = \frac{1}{2}$ ✓ (verified symbolically)
- **C4:** $\lim_{x\to 0} \mathcal{F}_{\text{dual}}(x)/x^3 = \frac{1}{3}$ ✓ (Taylor: $\mathcal{F}_{\text{dual}} = \frac{x^3}{3} - \frac{x^4}{4} + \cdots$)
- **C5:** $\mathcal{F}_{\text{dual}}$ is a polynomial plus $\ln(1+x)$, both analytic at $x=0$ ✓

---

## 3. Non-Uniqueness of the Physical Constraints

**Claim [P]:** Constraints C1–C5 do **not** uniquely determine $F$.

*Proof:* The "standard" interpolation function $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$ also satisfies all five constraints. Its corresponding action:

$$F_{\text{std}}(x) = \int_0^x t \cdot \mu_{\text{std}}(t)\, dt = \int_0^x \frac{t^2}{\sqrt{1+t^2}}\, dt = \frac{1}{2}\left[x\sqrt{1+x^2} - \text{arsinh}(x)\right]$$

satisfies C1–C5 (convex, analytic, Newtonian limit $\frac{1}{2}x^2$, deep-MOND limit $\frac{1}{3}x^3$). Yet $F_{\text{std}} \neq \mathcal{F}_{\text{dual}}$.

Therefore, additional structure beyond C1–C5 is needed to single out $\mathcal{F}_{\text{dual}}$.

---

## 4. The Constitutive-Relation Structure

**Definition [P]:** An action $F$ has *constitutive-relation structure* if it can be written as:

$$F(x) = \int_0^x t\,\mu(t)\, dt$$

where $\mu(x)$ is the MOND interpolation function.

**Theorem 4.1 [P]:** $\mathcal{F}_{\text{dual}}$ has constitutive-relation structure with $\mu(x) = x/(1+x)$.

*Proof:*

$$\int_0^x t \cdot \frac{t}{1+t}\, dt = \int_0^x \frac{t^2}{1+t}\, dt$$

Polynomial long division: $t^2/(1+t) = t - 1 + 1/(1+t)$. Therefore:

$$\int_0^x \left(t - 1 + \frac{1}{1+t}\right) dt = \frac{x^2}{2} - x + \ln(1+x) = \mathcal{F}_{\text{dual}}(x) \quad \square$$

**Corollary [P]:** The Euler–Lagrange equation of the action $\mathcal{S} = -\frac{a_0^2}{8\pi G}\int \mathcal{F}_{\text{dual}}(|\nabla\Phi|/a_0)\, d^3x$ yields:

$$F'(x) = x \cdot \mu(x) \quad \Longrightarrow \quad \nabla \cdot \left[\mu\!\left(\frac{|\nabla\Phi|}{a_0}\right) \nabla\Phi\right] = 4\pi G \rho$$

which is the AQUAL modified Poisson equation.

---

## 5. Padé Uniqueness Theorem

**Definition [P]:** A *Padé $[m/n]$ approximant* of $\mu(x)$ is a rational function $P_m(x)/Q_n(x)$ where $\deg P = m$, $\deg Q = n$.

**Theorem 5.1 (Padé Uniqueness) [P]:** $\mu(x) = x/(1+x)$ is the **unique** Padé $[1/1]$ rational function satisfying:

1. $\mu(0) = 0$ (deep-MOND: $\mu \to 0$)
2. $\mu(\infty) = 1$ (Newtonian: $\mu \to 1$)
3. $\mu'(0) = 1$ (linear regime in deep-MOND)

*Proof:* The general Padé $[1/1]$ form is $\mu(x) = \alpha x / (\beta + \gamma x)$ with $\alpha, \beta, \gamma > 0$.

- Condition 1: $\mu(0) = 0$ is automatically satisfied. ✓
- Condition 2: $\mu(\infty) = \alpha/\gamma = 1 \implies \alpha = \gamma$.
- Condition 3: $\mu'(x) = \alpha\beta/(\beta + \gamma x)^2$, so $\mu'(0) = \alpha/\beta = 1 \implies \alpha = \beta$.

Combining: $\alpha = \beta = \gamma$, giving $\mu(x) = \alpha x / (\alpha + \alpha x) = x/(1+x)$. $\square$

**Remark [P]:** Among all rational interpolation functions, $x/(1+x)$ has the **minimal degree** (numerator degree 1, denominator degree 1). Any other rational $\mu$ satisfying conditions 1–3 requires degree $\geq 2$ in either numerator or denominator. The "simple" $\mu$ is therefore the *Occam's razor choice* — the least complex rational interpolation consistent with the MOND boundary conditions.

---

## 6. The Odds Ratio / Bayesian Connection

**Definition [P]:** The *odds ratio* of a probability $p \in (0,1)$ is $\text{odds}(p) = p/(1-p)$.

**Theorem 6.1 (Odds-Ratio Inverse) [P]:** The "simple" interpolation function $\mu(x) = x/(1+x)$ is the inverse of the odds ratio function:

$$\mu(\text{odds}(p)) = p \quad \text{and} \quad \text{odds}(\mu(x)) = x$$

*Proof:*

$$\mu\!\left(\frac{p}{1-p}\right) = \frac{p/(1-p)}{1 + p/(1-p)} = \frac{p/(1-p)}{1/(1-p)} = p \quad \square$$

**Interpretation [O]:** The "simple" $\mu$ establishes a bijection between the physical acceleration ratio $x = a/a_0$ and a probability $p = \mu(x) \in (0,1)$ via the canonical Bayesian transformation. This probability can be interpreted as the *degree of Newtonian dominance* at a given acceleration:

| Regime | $x = a/a_0$ | $p = \mu(x)$ | Interpretation |
|--------|-------------|--------------|----------------|
| Deep-MOND | $x \ll 1$ | $p \approx x \ll 1$ | Almost purely MOND |
| Transition | $x = 1$ ($a = a_0$) | $p = 1/2$ | Equal weight |
| Newtonian | $x \gg 1$ | $p \approx 1$ | Almost purely Newton |

The odds ratio is the unique monotone transformation that maps a probability to an unbounded real number while preserving the likelihood-ratio structure of Bayesian inference. Its appearance here suggests that the MOND interpolation has an information-theoretic, not merely phenomenological, origin.

---

## 7. Fisher Information Structure

**Theorem 7.1 [P]:** The Fisher information of the Bernoulli distribution at $p = \mu(x)$ is:

$$\mathcal{I}(p) = \frac{1}{p(1-p)} = \frac{(1+x)^2}{x}$$

**Structural relationship [P]:** The action derivative satisfies:

$$\mathcal{F}_{\text{dual}}'(x) = x \cdot \mu(x) = x \cdot p$$

where $p = \mu(x)$ is the probability induced by the odds-ratio map. Since $\mathcal{I}(p) = (1+x)^2/x$, we have:

$$\mathcal{F}_{\text{dual}}'(x)^2 \cdot \mathcal{I}(p) = x^2 p^2 \cdot \frac{1}{p(1-p)} = \frac{x^2 p}{1-p} = \frac{x^2 \cdot x/(1+x)}{1/(1+x)} = x^3$$

Therefore:

$$\boxed{\mathcal{F}_{\text{dual}}'(x)^2 \cdot \mathcal{I}(\mu(x)) = x^3}$$

**Interpretation [O]:** The square of the action derivative times the Fisher information equals the cube of the acceleration ratio. This is a non-trivial structural identity linking the dynamics (via $F'$) to the information geometry (via $\mathcal{I}$). The $x^3$ scaling on the right-hand side is precisely the deep-MOND scaling of the action itself ($F \sim x^3/3$), suggesting a deep connection between the Fisher information metric and the MOND acceleration scale.

---

## 8. The Dual-Channel Cancellation Structure

**Theorem 8.1 (Dual-Channel Decomposition) [P]:** The action decomposes as:

$$\mathcal{F}_{\text{dual}}(x) = \mathcal{F}_{\text{Newton}}(x) - \mathcal{F}_{\text{correction}}(x)$$

where:
- $\mathcal{F}_{\text{Newton}}(x) = \tfrac{1}{2}x^2$ (Newtonian kinetic action)
- $\mathcal{F}_{\text{correction}}(x) = x - \ln(1+x)$ (information-theoretic correction)

*Proof:* $\tfrac{1}{2}x^2 - (x - \ln(1+x)) = \tfrac{1}{2}x^2 - x + \ln(1+x) = \mathcal{F}_{\text{dual}}(x)$. $\square$

**Theorem 8.2 (Cancellation Mechanism) [P]:** In the deep-MOND regime ($x \ll 1$):

$$\mathcal{F}_{\text{Newton}}(x) \approx \tfrac{1}{2}x^2, \qquad \mathcal{F}_{\text{correction}}(x) \approx \tfrac{1}{2}x^2 - \tfrac{1}{3}x^3 + \cdots$$

The Newtonian and correction terms **cancel to leading order**, leaving:

$$\mathcal{F}_{\text{dual}}(x) \approx \tfrac{1}{3}x^3 - \tfrac{1}{4}x^4 + \cdots$$

The residual $x^3/3$ gives the deep-MOND scaling $a \sim \sqrt{GMa_0}/r$.

**Corollary [P]:** The $\ln(1+x)$ term is the *information-theoretic cost* of the cancellation. Without it, the correction would be $\mathcal{F}_{\text{correction}} = x$, giving $\mathcal{F}_{\text{dual}} = \frac{1}{2}x^2 - x$, which is unbounded below — violating convexity (C2). The logarithm regularizes the subtraction, ensuring both convexity and the correct deep-MOND scaling.

---

## 9. Uniqueness Synthesis

**Theorem 9.1 (Uniqueness of $\mathcal{F}_{\text{dual}}$) [P]:** Given the following four structural constraints:

1. **Constitutive-relation structure:** $F(x) = \int_0^x t\,\mu(t)\, dt$ for some interpolation function $\mu$
2. **Padé minimality:** $\mu$ is a Padé $[1/1]$ rational function (minimal rational degree)
3. **MOND boundary conditions:** $\mu(0)=0$, $\mu(\infty)=1$, $\mu'(0)=1$
4. **Dual-channel structure:** $F = F_{\text{Newton}} - F_{\text{correction}}$ with $F_{\text{Newton}} = \frac{1}{2}x^2$

Then $F = \mathcal{F}_{\text{dual}}(x) = \frac{1}{2}x^2 - x + \ln(1+x)$ is **uniquely determined**.

*Proof:*
- By constraints 2–3 and Theorem 5.1: $\mu(x) = x/(1+x)$ uniquely.
- By constraint 1 and Theorem 4.1: $F(x) = \int_0^x t^2/(1+t)\, dt = \frac{1}{2}x^2 - x + \ln(1+x)$.
- Constraint 4 is satisfied by Theorem 8.1. $\square$

### Update 2026-08-30 — constraint 2 is redundant; Thm 6.1 and Thm 7.1 are one theorem

Full working: `Chyren_Second_Brain/50_Mathematical_Notation/derivations/D63_pade_necessity_narrowed.md`.

**Theorem 9.2 (constraint 2 is redundant) [D]:** Substituting the constitutive
structure $F'(x) = x\,\mu(x)$ into Theorem 7.1 gives
$x^2\mu/(1-\mu) = x^3$, i.e. $\mu/(1-\mu) = x$ — which *is* Theorem 6.1. The
Fisher information cancels identically. That single equation has the unique
solution $\mu = x/(1+x)$ with **no rational ansatz and no degree minimality**.
Padé $[1/1]$ minimality is therefore a *consequence* of the structure, not an
input, and constraint 2 above may be dropped from Theorem 9.1.

**Theorem 9.3 (the identity generates the standard family) [P]:**
$F'(x)^2\,\mathcal I(\mu) = x^{n+2} \iff \mu_n(x) = x^n/(1+x^n)$, verified for
$n=1,2,3,4$ — exactly the standard MOND interpolation family. Of the three
boundary conditions in constraint 3, $\mu(0)=0$ and $\mu(\infty)=1$ hold for
**every** $n \ge 1$; only $\mu'(0)=1$ selects $n=1$.

**Double-counting warning:** §6 and §7 are presented above as independent
structural facts. They are the same statement. Do not cite them as two
corroborations.

**What is NOT proved [O]:**

The necessity of constraint 2 (Padé minimality) is **not** derived from a more
fundamental principle. Theorem 9.2 *trades* it for a smaller postulate
($\mathrm{odds}(\mu) = x$, equivalently $n=1$); it does not derive it. Q2 below
is now answered — the odds-ratio connection is structural, not coincidence,
because it is the Fisher identity. Q1 and Q4 are **narrowed to a sharper
question**:

> **Q1′:** Why $n = 1$? Why is the dimensionless acceleration the *odds* of the
> interpolation probability, and why $\mu'(0) = 1$?

Restating this as "$\eta = \ln(p/(1-p))$ is the Bernoulli canonical parameter,
and Bernoulli is maximum-entropy" is **circular** — that is true by definition of
the exponential family and derives nothing. Q3 remains the one route that could
make $n=1$ physical rather than chosen.

The following questions remain open:

- **Q1:** Can the Padé constraint be derived from an information-theoretic variational principle? (e.g., minimum Fisher information, maximum entropy on the Bernoulli manifold)
- **Q2:** Is the odds-ratio connection (Theorem 6.1) a coincidence or a deep structural feature of the theory?
- **Q3:** Does the Skordis–Złośnik embedding (D9) constrain $\mu$ to be the "simple" form? If the covariant theory requires a specific $\mu$ for consistency (e.g., to avoid ghosts or ensure $c_T = c$), then constraint 2 would be promoted from an aesthetic choice to a physical necessity.
- **Q4:** The identity $\mathcal{F}_{\text{dual}}'(x)^2 \cdot \mathcal{I}(\mu(x)) = x^3$ (Theorem 7.1) suggests a variational principle of the form "minimize Fisher information subject to the MOND acceleration constraint." Can this be made rigorous?

---

## 10. Lean 4 Formalization Outline

The following theorems are candidates for formalization in Lean 4:

```lean
-- Theorem 4.1: Constitutive-relation structure
theorem dual_channel_integral_form :
  ∀ x : ℝ, x ≥ 0 →
  F_dual x = ∫ t in Set.Ioc 0 x, t * (t / (1 + t))

-- Theorem 5.1: Padé uniqueness
theorem pade_uniqueness :
  ∀ (α β γ : ℝ), α > 0 → β > 0 → γ > 0 →
  (∀ x, μ_general α β γ x = α * x / (β + γ * x)) →
  μ_general α β γ 0 = 0 →
  (Tendsto (μ_general α β γ) atTop (nhds 1)) →
  (deriv (μ_general α β γ) 0 = 1) →
  α = β ∧ α = γ

-- Theorem 6.1: Odds-ratio inverse
theorem odds_ratio_inverse :
  ∀ p : ℝ, 0 < p → p < 1 →
  μ (p / (1 - p)) = p

-- Theorem 7.1: Fisher information identity
theorem fisher_information_identity :
  ∀ x : ℝ, x > 0 →
  (deriv F_dual x)^2 * (1 / (μ x * (1 - μ x))) = x^3

-- Theorem 8.1: Dual-channel decomposition
theorem dual_channel_decomposition :
  ∀ x : ℝ, x ≥ 0 →
  F_dual x = x^2/2 - (x - Real.log (1 + x))

-- Theorem 8.2: Deep-MOND cancellation
theorem deep_mond_cancellation :
  Tendsto (fun x => F_dual x / x^3) (nhds 0) (nhds (1/3))
```

These should be added to the `DualChannelDerivation.lean` module alongside the existing theorems.

---

## 11. Summary

| Result | Status | Section |
|--------|--------|--------|
| $\mathcal{F}_{\text{dual}}$ satisfies all physical constraints C1–C5 | [P] proved | §2 |
| C1–C5 do not uniquely determine $F$ | [P] proved | §3 |
| $\mathcal{F}_{\text{dual}} = \int_0^x t\,\mu(t)\, dt$ | [P] proved | §4 |
| $\mu = x/(1+x)$ is the unique Padé[1/1] | [P] proved | §5 |
| $\mu$ is the inverse of the odds ratio | [P] proved | §6 |
| $F'^2 \cdot \mathcal{I} = x^3$ | [P] proved | §7 |
| Dual-channel cancellation mechanism | [P] proved | §8 |
| $\mathcal{F}_{\text{dual}}$ is unique given 4 structural constraints | [P] proved | §9 |
| Necessity of Padé constraint from first principles | [O] open | §9, Q1 |
| Information-theoretic variational principle | [O] open | §9, Q4 |
| D9 embedding constrains $\mu$ | [O] open | §9, Q3 |
