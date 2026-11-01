# Navier–Stokes Source Statements and Applicability Audit

**Status:** source-checked record, 2026-09-14. This document quotes or closely transcribes the accessible source statements used by the remediation. It is not a proof of global regularity. The three sources are deliberately kept separate by domain and solution class.

## 1. Official target: Fefferman/Clay Alternative B

The primary target is Charles L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, Clay Mathematics Institute problem description, pp. 1–2, [PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).

The source defines the equations on `R^n`, with `ν > 0`, divergence-free initial velocity `u°`, force `f`, and pressure/velocity unknowns satisfying equations (1)–(3). For the periodic alternative it imposes `u°(x + e_j) = u°(x)` and `f(x + e_j,t) = f(x,t)` in the spatial variables, and requires periodicity of the solution. The exact displayed statement is:

> **(B) Existence and smoothness of Navier–Stokes solutions in `R^3/Z^3`. Take `ν > 0` and `n = 3`. Let `u°(x)` be any smooth, divergence-free vector field satisfying (8); we take `f(x,t)` to be identically zero. Then there exist smooth functions `p(x,t), u_i(x,t)` on `R^3 × [0,∞)` that satisfy (1), (2), (3), (10), (11).**

Here (8) is spatial periodicity of the initial field and zero force is required; (10) is spatial periodicity of the solution and (11) is `p,u ∈ C∞(R^n × [0,∞))`. This is the frozen official target. The repository does not prove it.

## 2. Constantin–Fefferman vorticity-direction criterion

The primary source is Peter Constantin and Charles Fefferman, “Direction of Vorticity and the Problem of Global Regularity for the Navier–Stokes Equations,” *Indiana University Mathematics Journal* 42 (1993), no. 3, pp. 775–789, DOI metadata at [I.U. Math. J.](https://iumj.s3-us-west-2.amazonaws.com/abstracts/42034_abs.pdf).

The accessible first-page source states the setting and conclusion as follows:

> “The problem of global regularity for the three dimensional incompressible Navier-Stokes equations is the following: given smooth, localized, divergence-free initial data, do smooth solutions of the Cauchy problem exist for all time? The answer to this problem is not known.”

> “In this paper we prove that if the direction of vorticity is sufficiently well behaved in regions of high vorticity magnitude, then the solution is smooth.”

The same source introduces the angle `φ(x,y,t)` between unit vorticity directions at `x` and `y`, and states that there are positive constants `δ` and `ρ` such that, when the vorticity magnitude at both locations exceeds a fixed high-vorticity threshold `M`, the directional condition is imposed for sufficiently close pairs. The scanned display is transcribed in the standard notation used by the paper as

```text
|sin φ(x,y,t)| ≤ |x − y| / ρ
```

for `|x − y| < δ` and `|ω(x,t)|, |ω(y,t)| ≥ M`, with the condition holding for the relevant almost-everywhere spacetime pairs in the theorem's solution class. The source's conclusion is smoothness/regularity of the solution.

**Applicability boundary.** The paper's stated initial-data setting is smooth, localized data on `R^3`; the accessible source does not state a torus theorem. The repository's `AlignmentPredicate K L ρ` is a kinematic predicate on an arbitrary field `ω : Point3 → Vector3`. It differs from the cited criterion in at least these ways: it has no time variable or solution class; it uses the torus-shaped `Point3` type without a periodic distance construction; it does not encode a fixed high-vorticity threshold independently of `K`; it requires pointwise pairwise hypotheses rather than a sourced a.e. spacetime formulation; and its bound is `‖ξ(x)-ξ(y)‖ ≤ L dist(x,y)`, not the cited sine-of-angle condition with the source's constants and quantifiers. Therefore no L3 implication is claimed.

## 3. Local periodic strong/mild existence

An accessible exact statement is Terence Tao, “254A, Notes 1: Local well-posedness of the Navier–Stokes equations,” Theorem 37, [source](https://terrytao.wordpress.com/2018/09/16/254a-notes-1-local-well-posedness-of-the-navier-stokes-equations/). In the periodic setting `R^d/Z^d`, the theorem states:

> **Theorem 37 (Local well-posedness of mild solutions at high regularity). Let `s > d/2`, and let `u_0 ∈ H^s(R^d/Z^d → R^d)^0` be divergence-free. Then there exists a time `T ≫_{d,s} ν / ‖u_0‖_{H^s_x}^2`, and an `H^s` mild solution `u : [0,T] × R^d/Z^d → R^d` to the Navier–Stokes equation. Furthermore, this mild solution is unique.**

For the selected three-dimensional target, `d = 3`; the repository may specialize this statement to `s > 5/2`, which is stronger than the theorem's displayed threshold `s > 3/2` and supplies the usual Sobolev embedding into Lipschitz-controllable classes after additional estimates. This source is an expository theorem, not a Lean formalization.

The same source gives a continuation/maximal-development statement:

> **Theorem 38 (Maximal Cauchy development). Let `s > d/2`, and let `u_0 ∈ H^s(R^d/Z^d → R^d)^0` be divergence-free. Then there exists a time `0 < T_* ≤ ∞` and an `H^s` mild solution on `[0,T_*)` such that if `T_* < ∞` then `‖u(t)‖_{H^s} → ∞` as `t → T_*^-`. Furthermore, `T_*` and `u` are unique.**

It also states Proposition 39: if `T_* < ∞`, then `‖u‖_{L^∞_t L^∞_x(0,T_* )} = ∞`. This is a genuine periodic Navier–Stokes continuation/blow-up alternative for the stated mild-solution class. It is not the Euler BKM theorem and it does not by itself prove `T_* = ∞`.

## 4. Separate periodic local-existence cross-check

Marín-Rubio, Robinson, and Sadowski, “Solutions of the 3D Navier–Stokes equations for initial data in `\dot H^{1/2}`,” *Journal of Mathematical Analysis and Applications* (preprint source [University of Seville PDF](https://idus.us.es/bitstreams/b0e9a174-2dd3-484d-9a9d-39ec5ee1323c/download)), studies the cubic periodic domain `Q = [0,2π]^3` and defines the divergence-free, zero-average periodic Sobolev spaces. Its Theorem 1 states that for `u_0 ∈ \dot H^{1/2}`, if the heat evolution satisfies an explicit smallness integral, then the periodic Navier–Stokes equation has a unique solution in `L^∞(0,T_*;\dot H^{1/2}) ∩ L^2(0,T_*;\dot H^{3/2})`. This is useful as a periodic local-existence cross-check, but it is not used to upgrade the repository's claims.

## 5. Why the repository does not claim the global implication

The repository's current `AlignmentPredicate` is only a kinematic definition. No theorem proves that every solution covered by Alternative B satisfies it, persists in it, or satisfies the exact Constantin–Fefferman hypothesis. In addition, a dimensionless scalar gate such as `χ ≥ 0.7` cannot determine a dimensional Lipschitz constant without an explicit `L_max`; and the existing abstract product `omega_sup T` is not the BKM time integral `∫_0^T ‖ω(·,t)‖_∞ dt`.

The precise open implication is therefore:

> For every smooth, divergence-free, zero-force periodic initial datum in Fefferman's Alternative B, the corresponding maximal periodic Navier–Stokes solution satisfies the exact source-verified alignment hypothesis for every time in its existence interval, with all domain, quantifier, threshold, and regularity conditions matched.

No source above proves that implication, and no Lean file in this repository formalizes it.

## Bibliography

1. C. L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, Clay Mathematics Institute, current PDF accessed 2026-09-14.
2. P. Constantin and C. Fefferman, “Direction of Vorticity and the Problem of Global Regularity for the Navier–Stokes Equations,” *Indiana University Mathematics Journal* 42 (1993), 775–789.
3. T. Tao, “254A, Notes 1: Local well-posedness of the Navier–Stokes equations,” 2018, Theorems 37–38 and Proposition 39.
4. P. Marín-Rubio, J. C. Robinson, and W. Sadowski, “Solutions of the 3D Navier–Stokes equations for initial data in `\dot H^{1/2}`,” periodic-domain local-existence preprint.
