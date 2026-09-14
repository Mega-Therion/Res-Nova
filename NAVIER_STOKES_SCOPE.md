# Navier–Stokes Scope, Evidence, and Formalization Roadmap

## Status statement

This repository does **not** contain a proof of the Clay Mathematics Institute Navier–Stokes existence-and-smoothness problem. It contains a preliminary Lean artifact and a conditional regularity program associated with a vorticity-direction alignment condition.

No document, release, README, abstract, theorem name, or citation derived from this repository should describe the current work as a resolution of the Millennium Prize Problem.

The appropriate present-tense description is:

> We study a conditional regularity framework for three-dimensional incompressible Navier–Stokes flow. The framework assumes a quantitative high-vorticity-direction alignment condition and investigates its relation to established conditional regularity criteria. The outstanding problem is to derive that condition from Navier–Stokes dynamics for a Clay-admissible class of data.

## Evidence baseline

### Current Lean artifact

`05_lean_formalization/SovereignRegularity.lean` contains `sovereign_regularity_theorem`. At the baseline commit for this branch, the theorem has the form:

```lean
theorem sovereign_regularity_theorem (st : BKMVorticityState)
    (T : ℝ) (hT : 0 ≤ T) : st.omega_sup T ≤ st.B :=
  st.h_controlled T hT
```

This is a valid Lean theorem, but it is a direct projection of the `h_controlled` field already assumed in `BKMVorticityState`. It does not derive vorticity control from a Navier–Stokes solution, and it must not be presented as global regularity.

The repository's assumption audit identifies this theorem as a projection and notes that its object named as a BKM integral is a product in the present artifact rather than a formal time integral.

### Current manuscript claim

The manuscript *Sovereign Regularity for the Three-Dimensional Navier–Stokes Equations under Chiral Vorticity Alignment* describes a conditional argument on the three-torus: a strong solution is assumed to satisfy a high-vorticity Lipschitz-direction condition `SA(K,L)` at every time in its maximal interval. It explicitly states that this does not resolve the Clay problem and identifies invariance of the Sovereign Class under NSE evolution as open.

The manuscript's use of external regularity results is a research lead, not a formalized derivation in this repository. Before relying on it, the exact cited theorem statements, hypotheses, domain, and continuation argument must be checked against the primary sources.

### Publication disposition

The Zenodo re-verification record of 2026-09-12 categorizes the Sovereign Regularity item as material to retain as a conditional proof with an honesty disclaimer, while identifying broader Millennium-solution claims for discard. Superseded material is retained for provenance and must not be silently deleted.

## Claim taxonomy

Every claim associated with this program must receive one label from the following taxonomy:

| Label | Meaning | Publication rule |
|---|---|---|
| Formal theorem | Lean statement whose assumptions and conclusion are explicit and whose proof checks | State exact theorem and assumptions |
| Conditional mathematical argument | Paper-level implication conditional on named analytic hypotheses or imported results | State every condition prominently |
| Imported theorem | A result proved elsewhere and cited here | Give exact source and verify applicability |
| Numerical evidence | Reproducible finite computation or simulation | Never use as a proof of global regularity |
| Conjecture/open obligation | A desired implication not yet proved | Label as conjecture or open problem |
| Assertion | Informal statement lacking a proof or reproducible evidence | Do not use as technical support |
| Superseded/discarded claim | Preserved historical material not admitted into the active citation canon | Do not cite as current support |

## Required mathematical separation

The project must keep the following four statements distinct:

1. A solution satisfies an alignment condition `SA(K,L)`.
2. `SA(K,L)` implies the hypotheses of a precisely stated conditional regularity theorem.
3. Those hypotheses imply continuation/global smoothness for the stated solution class.
4. Every Clay-admissible smooth initial datum produces a solution satisfying the necessary condition for all time, or a valid counterexample exhibits breakdown.

Only items 1–3 can describe a conditional regularity result. Item 4, in an official Clay-compatible formulation, is the missing global problem.

## Formalization roadmap

### Phase A — Reproducible corpus and exact statements

- Freeze an inventory of relevant Zenodo versions, source manuscripts, Git commits, file hashes, and Notion/Drive locations.
- Recover the full current body of `SovereignRegularity.lean` before editing it.
- Record exact primary-source statements for each analytic result invoked.
- Select one official Clay/Fefferman alternative as the target specification.

### Phase B — Correct the Lean interface

- Rename or document theorem declarations so theorem names and docstrings state their conditional scope.
- Replace any quantity named as an integral with an actual interval integral, or rename it accurately.
- Specify the domain, vector fields, time interval, norms, vorticity, divergence-free constraint, viscosity, and solution regularity.
- Separate assumptions supplied in structures from propositions proved from those assumptions.

### Phase C — Formalize genuine intermediate results

- Formalize elementary geometric lemmas: unit-vector differences, angle control, and the exact Lipschitz-to-modulus implication.
- Formalize the definition of the high-vorticity set and the alignment predicate with all measurable/regularity requirements.
- Build a formal statement of the conditional continuation theorem actually used, with citations and a clear boundary between formalized proof and imported result.
- Introduce genuine Bochner/Lebesgue time integrals only after the needed analysis infrastructure is explicit.

### Phase D — Anti-vacuity and verification controls

For every flagship theorem:

- List each non-logical assumption in a machine-readable theorem inventory.
- Add a companion statement naming whether the conclusion is a direct projection of a structure field.
- Run `#print axioms` and retain the output in a verification report.
- Prohibit `sorry`, `admit`, unsafe axioms, and untracked local axioms in results marketed as verified.
- Add negative tests showing that removing the decisive hypothesis prevents the proof from compiling.
- Require an independent Lean reviewer before any public claim of a new formal mathematical result.

### Phase E — Research decision gate

The project may claim a solution to the Millennium problem only if all of the following are met:

1. The theorem matches one complete official Clay problem alternative.
2. It covers the required three-dimensional equations, domain, initial-data class, and conclusion.
3. Its proof does not assume the global regularity, integrability, alignment invariance, or a comparable decisive conclusion.
4. The proof is complete, reproducibly builds from pinned dependencies, and contains no placeholders.
5. Independent experts in PDE analysis and Lean verification have reviewed the proof and their reports are public.

Until then, public wording must use `conditional regularity framework`, `formalization roadmap`, `conjecture`, or `open problem`, as appropriate.

## Immediate next actions

1. Create a dated evidence ledger with stable identifiers and checksums.
2. Obtain the complete source of `SovereignRegularity.lean` and update only documentation/identifiers first; preserve proof bodies unchanged in that initial corrective commit.
3. Recover and assess the later Lyapunov manuscript before treating it as part of the active argument.
4. Produce a source-checked dependency map for the claimed Constantin–Fefferman and Beale–Kato–Majda steps.
5. Write a minimal, Clay-aligned Lean specification before attempting any new global-regularity proof.

## Preservation principle

Historical and superseded records are evidence of the project's development. Preserve them with version identifiers and clear status markers. Corrections should be additive, dated, and transparent; they should never conceal earlier claims or alter provenance.
