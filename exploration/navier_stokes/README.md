# 3D periodic Navier–Stokes: a conditional regularity program `[O]`

**Nothing here proves global regularity of the three-dimensional Navier–Stokes equations, in
any setting.** The program is adjacent to Res-Nova's MOND work and out of scope for its
manuscript. Its Lean modules are listed in `05_lean_formalization/ADJACENT_MODULES.txt`, and
they are built and gated like every other module.

**The target (frozen 2026-10-08).** The target is Fefferman's statement (B): the problem on
`ℝ³/ℤ³` with zero force and `ν > 0`. Every smooth, divergence-free, periodic initial velocity
must have a smooth solution on `ℝ³ × [0, ∞)`, with velocity and pressure both periodic (the pressure by the problem description's Errata). The source text is in
`SOURCE_STATEMENTS.md`, and the Lean statement is
`NavierStokesTarget.PeriodicGlobalRegularity`. That is a `Prop`, and no declaration proves or
assumes it.

## What exists, level by level
| level | content | Lean | status |
|---|---|---|---|
| L0 | scalar threshold arithmetic | `NavierStokesScope` | proved; arithmetic only |
| L1 | two unit vectors are at distance ≤ 2 | `NavierStokesGeometry.norm_sub_le_two_of_norm_eq_one` | proved; elementary |
| L2 | kinematic high-vorticity alignment predicate on one time slice | `NavierStokesSpec.AlignmentPredicate`, `direction_unit` | definitions, and one normalization lemma |
| target | statement (B), smooth periodic solutions, curl, divergence | `NavierStokesTarget` | definitions, plus 4 sanity theorems (below) |
| L3a | on one time slice, `AlignmentPredicate K L ρ` ⇒ the single-time form of Constantin–Fefferman's Assumption (A): `sin φ(x, y) ≤ |x − y|/(1/L)` for every pair with `|ω| > K` at both, assuming `0 ≤ K`, `0 < L` and `L·ρ ≥ 1` | `NavierStokesTarget.alignment_gives_assumptionA_slice`, using `alignment_gives_sine_condition` and `sin_angle_le_norm_sub` | **proved**. Substitution tests fail at `L/2` and at `L·ρ ≥ 1/2`, so both bounds are load-bearing |
| L3b | the rest of the exact Constantin–Fefferman hypothesis: time and solution class, the domain (they work on `ℝ³`; the target is the torus), threshold and `δ` conventions | none | **open:** see `SOURCE_STATEMENTS.md` |
| L4 | a continuation theorem for the chosen class, imported with provenance | none | stated as a source in `SOURCE_STATEMENTS.md`, not formalized |
| L5 | `AlignmentPersistence K L ρ`: every admissible solution stays aligned | `NavierStokesTarget.AlignmentPersistence` (a `Prop`) | **open**. This is the missing implication |

**Sanity theorems** (`NavierStokesTarget`). They are about the definitions, not about
regularity:
- `zero_admissible` and `zero_solution`: the zero field is admissible and solves the problem, so the specification is satisfiable.
- `growing_constant_field_not_a_solution`: `u(t, x) = t e₀` fails the equations at every point, so the equations have content.
- `persistenceObligation_false`: the older `NavierStokesSpec.PersistenceObligation` quantified over every field and is **false**. `AlignmentPersistence` replaces it with a statement over genuine solutions.

## The Lyapunov route (Paper 17): permanently demoted for arbitrary data
- **The estimate.** Paper 17 reaches `dE/dt ≤ −(ν/2)‖∇ω‖² + C₂(1−θ)⁴E³ + C₁E`.
  - The positive `E³` and `E` terms remain, so the inequality gives no global bound for arbitrary data.
  - `(0.3)⁴ = 0.0081` makes the constant small, but the term is still cubic.
  - See `archive/legacy_root/NAVIER_STOKES_LYAPUNOV_AUDIT.md`.
- **Classification:** unsupported for arbitrary data.
- **What could close it** (stated, not proved):
  - The standard small-data argument would apply under two extra hypotheses: `C₁ < 2π²ν`, and `E(0)² < (2π²ν − C₁)/(C₂(1−θ)⁴)`.
  - It uses Poincaré on the zero-mean vorticity of the unit torus, `‖∇ω‖² ≥ 4π²‖ω‖²`, with `E = ‖ω‖²_{L²}` (if Paper 17's `E` carries a factor ½, the constants change accordingly). Together these make the right-hand side negative below the threshold.
  - It also requires that Paper 17's inequality itself is established, which this repository has not checked.

## Build
    cd 05_lean_formalization && lake exe cache get && lake build && bash verify_all_proofs.sh; echo $?
The witness is in `05_lean_formalization/VERIFICATION_RUN_2026-10-08_NAVIER_STOKES/` (see `EVIDENCE_LEDGER.md`).

## Referee note
**Current claim.**
- **Machine-checked:** elementary scalar and unit-vector lemmas; a kinematic alignment predicate on a single time slice; a faithful Lean statement of the periodic target with zero force; and four sanity theorems about those definitions.
- **What follows from the historical "Sovereign Regularity" file:** only consequences of an assumed bound. Its flagship theorem returned its own hypothesis, and it is renamed accordingly.
- **Analytic sources:** quoted with their domains and solution classes in `SOURCE_STATEMENTS.md`.

**Missing implication.**
- Global regularity would follow if every admissible periodic solution satisfied a vorticity-direction condition matching a source-verified continuation criterion on `ℝ³/ℤ³`, for its whole existence time.
- No such persistence is derived from the equations.
- On one time slice, the repository's alignment predicate does imply the source's sine-form condition (L3a, with `ρ_CF = 1/L`).
- It still lacks the time quantifier and the solution class.
- It is stated on Euclidean `ℝ³`, while the criterion is proved for the Cauchy problem on `ℝ³` and the target is the torus. That needs a periodic version of the criterion.

This remains a conditional regularity program. The unproved implication is that every
admissible periodic solution of statement (B) satisfies the specified alignment predicate for
its full existence time.
