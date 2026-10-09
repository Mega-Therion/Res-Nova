# Source statements and applicability (verified 2026-10-08)

**How the quotes were checked.** Every quote below was matched against a saved copy of the source. A literature-agent pass collected the copies; Claude Code then re-checked the key passages by grep, and the Constantin–Fefferman scan visually.

**What this file supersedes.** It replaces the hand-off's `NAVIER_STOKES_SOURCE_STATEMENTS.md`, which is in commit `b430e1c`. That version presented paraphrases as verbatim quotes and misstated the Constantin–Fefferman hypothesis (corrections at the end).

**Tier.** `[C]` for the cited statements; `[O]` for the applicability analysis.

## 1. The target: Fefferman's statement (B)
**Source:** C. L. Fefferman, *Existence and smoothness of the Navier–Stokes equation* (problem description PDF, pp. 1–2 and the Errata on p. 5; copy sha256 `c1b5f27b1a64705c…`).

Equations, verbatim (Unicode rendering of the PDF):
- (1) ∂uᵢ/∂t + Σⱼ uⱼ ∂uᵢ/∂xⱼ = νΔuᵢ − ∂p/∂xᵢ + fᵢ(x, t)  (x ∈ ℝⁿ, t ≥ 0)
- (2) div u = Σᵢ ∂uᵢ/∂xᵢ = 0  (x ∈ ℝⁿ, t ≥ 0)
- (3) u(x, 0) = u°(x)  (x ∈ ℝⁿ)
- (8) u°(x + eⱼ) = u°(x), f(x + eⱼ, t) = f(x, t) for 1 ≤ j ≤ n  (eⱼ = j-th unit vector in ℝⁿ)
- (10) u(x, t) = u(x + eⱼ, t) on ℝ³ × [0, ∞) for 1 ≤ j ≤ n
- (11) p, u ∈ C^∞(ℝⁿ × [0, ∞))

Statement (B), verbatim:
> (B) Existence and smoothness of Navier–Stokes solutions in ℝ³/ℤ³. Take ν > 0 and n = 3. Let u°(x) be any smooth, divergence-free vector field satisfying (8); we take f(x, t) to be identically zero. Then there exist smooth functions p(x, t), uᵢ(x, t) on ℝ³ × [0, ∞) that satisfy (1), (2), (3), (10), (11).

Errata, verbatim:
> The further condition p(x + ej, t) = p(x, t) should be made explicit in Eqn (8).

So the pressure is periodic as well. **Lean:** `NavierStokesTarget.PeriodicGlobalRegularity`, which imposes the periodicity of `u` and `p`, the equations for `t > 0`, and smoothness on `[0, ∞) × ℝ³`.

## 2. Constantin–Fefferman (1993)
**Source:** P. Constantin and C. Fefferman, *Direction of vorticity and the problem of global regularity for the Navier–Stokes equations*, Indiana Univ. Math. J. **42** (1993), 775–789, DOI [10.1512/iumj.1993.42.42034](https://doi.org/10.1512/iumj.1993.42.42034). The publisher serves the full text; the copy's sha256 is `28d77e303d71a732…`.

p. 780, verbatim (checked visually against the scan):
> **Assumption (A).** There exist constants Ω > 0 and ρ > 0 such that |P^⊥_{ξ(x,t)}(ξ(x + y, t))| ≤ |y|/ρ holds if both |ω(x, t)| > Ω and |ω(x + y, t)| > Ω, and 0 ≤ t ≤ T.

> **Theorem 1.** If the assumption (A) holds, then the solution of the initial value problem for the Navier-Stokes equation is strong and hence smooth (C^∞) on the time interval [0, T].

**Setting** (per the literature pass; not re-checked line by line):
- the domain is ℝ³, with smooth compactly supported data;
- (A) is imposed on solutions of the δ-mollified system, (11)–(12) in the paper;
- "strong" means L^∞(0, T; H¹) ∩ L²(0, T; H²).

**Form of the condition:**
- For unit vectors, |P^⊥_ξ(η)| = sin φ, so (A) is a sine condition.
- It is pointwise, with no "a.e."; the threshold is strict (> Ω); and there is no |y| < δ restriction.

## 3. Periodic (torus) direction criteria
- **Berselli**, *Nonlinearity* **36** (2023) 4303–4313, DOI [10.1088/1361-6544/ace096](https://doi.org/10.1088/1361-6544/ace096), Theorem 1.1, verbatim:
  > Let us consider either the space-periodic problem (x ∈ T³) or the Cauchy problem (x ∈ R³). Let u be a Leray–Hopf weak solution of the NSE in (0, T), with u0 ∈ H1.

  It goes on: there exist λ, C̄₁ > 0 such that if, for a.e. t, sin ∠(ω̂(x, t), ω̂(y, t)) ⩽ C̄₁ at "the six grid-points y = x ± λeⱼ", then u is smooth.
  - **Contrast with (A):** no vorticity threshold appears, and the condition is at fixed lattice offsets for a.e. t.
- **S. Li**, *Acta Math. Sci.* **40** (2020) 1700–1708, DOI [10.1007/s10473-020-0606-7](https://doi.org/10.1007/s10473-020-0606-7), checked on arXiv:1712.00551v2.
  - Setting: Ω = ℝ³ or 𝕋³, Leray–Hopf weak solutions.
  - Condition: |sin φ| ≤ |x − y|^β/ρ "whenever |ω(t, x)|, |ω(t, y)| ≥ Λ".
  - Conclusion: classical on [0, T] in one statement, and an L^q bound under ω ∈ L^q in another.

## 4. Local existence and continuation on the torus
**Source:** T. Tao, *254A, Notes 1: Local well-posedness of the Navier–Stokes equations* (blog, 2018-09-16; page modified 2025-11-12). Verbatim, with LaTeX markup removed:
> Theorem 37 (Local well-posedness of mild solutions at high regularity). Let s > d/2, and let u₀ ∈ H^s(ℝ^d/ℤ^d → ℝ^d)⁰ be divergence-free. Then there exists a time T ≫_{d,s} ν/‖u₀‖²_{H^s_x(ℝ^d/ℤ^d → ℝ^d)}, and an H^s mild solution u : [0, T] × ℝ^d/ℤ^d → ℝ^d to (34). Furthermore, this mild solution is unique.

> Theorem 38 (Maximal Cauchy development). Let s > d/2, and let u₀ ∈ H^s(ℝ^d/ℤ^d → ℝ^d)⁰ be divergence-free. Then there exists a time 0 < T_* ≤ ∞ and an H^s mild solution u : [0, T_*) × ℝ^d/ℤ^d → ℝ^d to (34), such that if T_* < ∞ then ‖u(t)‖_{H^s(ℝ^d/ℤ^d → ℝ^d)} → ∞ as t → T_*⁻. Furthermore, T_* and u are unique.

> Proposition 39 (Blowup criterion). Let s, u₀, T_*, u be as in Theorem 38. If T_* < ∞, then ‖u‖_{L^∞_t L^∞_x([0,T_*))} = ∞.

The notation needs care:
- The superscript ⁰ means mean zero.
- (34) is the Duhamel (mild) formulation.
- This is a Navier–Stokes continuation statement on the torus. It is not the Euler Beale–Kato–Majda theorem.

**Cross-check:** P. Marín-Rubio, J. C. Robinson and W. Sadowski, *J. Math. Anal. Appl.* **400** (2013) 76–85, DOI [10.1016/j.jmaa.2012.10.064](https://doi.org/10.1016/j.jmaa.2012.10.064). They use the periodic domain [0, 2π]³, zero total momentum, ν = 1, and Leray–Hopf solutions. The preprint was checked; the published wording is unverified.

## 5. Applicability: what is proved, and what is still missing `[O]`
**Proved (Lean, gated): L3a on one time slice.**
- `NavierStokesTarget.alignment_gives_assumptionA_slice` assumes 0 ≤ K, 0 < L and L·ρ ≥ 1.
- Under those, `AlignmentPredicate K L ρ ω` gives sin φ(x, y) ≤ |x − y| / (1/L) for every pair with |ω| > Ω = K at both points.
- That is the single-time form of Assumption (A), with ρ_CF = 1/L.
- The proof uses the unit-vector inequality sin φ ≤ |ξ(x) − ξ(y)| (`sin_angle_le_norm_sub`). The literature pass reports the same inequality, |sin φ| ≤ |ξ(x + y, t) − ξ(x, t)|, on p. 779 of the paper.

**Missing (L3b, L4, L5):**
1. **Time and solution class.** (A) holds for all 0 ≤ t ≤ T along a δ-regularized solution, but the repository's predicate is a single-slice, kinematic statement. The time quantifier is exactly `NavierStokesTarget.AlignmentPersistence`, which is open.
2. **Domain.** Theorem 1 is for the Cauchy problem on ℝ³ with compactly supported data, while the target is ℝ³/ℤ³.
   - A periodic vorticity-direction criterion is needed. Berselli 2023 and Li 2020 are periodic, but with different hypotheses:
     - **Berselli:** no threshold, a.e. t, a fixed lattice offset;
     - **Li:** a Λ threshold and an extra L^q condition.
   - None has been matched to the repository's predicate in Lean.
   - Informal localization from ℝ³ to the torus is not allowed.
3. **Normalization.** Berselli's torus has side 2π, while statement (B) uses period 1. The rescaling of λ and of the constants must be done explicitly.
4. **Continuation.** Pairing a direction criterion with the periodic smooth class needs either the criterion's own conclusion (smoothness) or Tao's blow-up alternative for H^s mild solutions, plus the regularity bridge from mild to classical. None of this is formalized; it is cited (L4).

## Corrections to the hand-off version (`b430e1c`)
- **Constantin–Fefferman.**
  - The paper's constants are Ω and ρ: δ is the mollifier scale, and there is no M.
  - The threshold is strict (>).
  - The "|x − y| < δ" restriction is not in the paper; it comes from a later restatement (Beirão da Veiga–Berselli 2002, Remark 1.3).
  - The paper has no "almost-everywhere" formulation.
  - The regularized-solution setting was omitted.
- **Tao.** Theorems 37–38 and Proposition 39 were presented as verbatim but paraphrased: "(34)" was dropped, the interval [0, T_*) was altered, and the meaning of the mean-zero ⁰ was not stated.
- **Statement (B).** The quote of (B) was verbatim, but the Errata requiring pressure periodicity were not mentioned.
- **Periodic criteria.** Berselli 2023 and Li 2020 exist and were not cited.
- **MRS.** The citation's title was truncated, and the period 2π, ν = 1 and zero mean were not noted.
