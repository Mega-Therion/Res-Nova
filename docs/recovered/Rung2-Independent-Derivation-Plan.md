# Res Nova Rung 2 — Independent `MuStdWeakField` Derivation Plan

## Status

**Rung 1 is frozen as:**

> **`mu_std` is formally characterized, not physically derived.**

Rung 1 established the mathematical properties of a stipulated constitutive law. It did not establish that the law follows from the Res Nova covariant action or that it describes nature.

**Rung 2 status:** planned, not implemented.

## Immutable baseline

All Rung 2 work begins from the following clean repository state:

- Repository: `Mega-Therion/Res-Nova`
- Branch: `main`
- Commit: `aaca4f96978676230239e47a921704fa6353bb0f`
- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`
- Lean target inventory at baseline: 45 targets

### Baseline artifact hashes

| Artifact | SHA-256 |
|---|---|
| `THE_ONE_PAGE_UNIVERSAL_LAGRANGIAN.tex` | `833eab2a9fda5e70bf7ee849de2c7da9c760ecfdd6a266b4f4d7b4a1b8692461` |
| `TARGET_D2_PHYSICAL_ACTION_DERIVATION.md` | `a51df2e17c2219f0f00809795df2bb9430832a4baf1787c8034c2435c45e901c` |
| `TARGET_D7_COVARIANT_COMPLETION.md` | `ef3073cd6565bb97ade29a0be0eb11e49cce1e8983e10168f222008b0976255e` |
| `05_lean_formalization/SkordisZlosnikEmbedding.lean` | `1ef6cd70626d7d659fd9912013e69b0016de15658e6f77376d91845292ef7150` |
| `05_lean_formalization/MuStdUniqueness.lean` | `6597bcc382042922f63f2817d8be5c85345061a903786e68289e17be16d4e080` |

These hashes are provenance anchors. Every derivation attempt must record the source commit and hashes of generated outputs. Failed attempts must remain auditable; they must not be silently replaced by tuned results.

## Hard rule

> **Do not start from `FStd` and engineer a weak-field equation that resembles AQUAL. Start from the canonical covariant action and derive the weak-field/quasistatic limit independently.**

The reduction must first produce whatever `S_QS` follows from the source action. Only afterward may that result be compared with `FStd`.

## Research question

Given the canonical covariant action and its stated matter coupling, does a predefined weak-field/quasistatic limit produce an action of the form

\[
S_{\rm QS}=\int d^3x\,
\left[\frac{|\nabla\Phi|^2}{8\pi G}+a_0^2F_{\rm cov}(X)+\rho\Phi\right],
\qquad
X=\frac{|\nabla\Phi|}{a_0},
\]

or another explicitly derived expression, whose Euler–Lagrange equation is

\[
\nabla\cdot\left[\mu_{\rm cov}(X)\nabla\Phi\right]=4\pi G\rho?
\]

The comparison is then:

\[
F_{\rm cov}\stackrel{?}{=}F_{\rm std},
\qquad
\mu_{\rm cov}\stackrel{?}{=}
\mu_{\rm std}(X)=\frac{X}{\sqrt{1+X^2}}.
\]

## Three allowed outcomes

### Outcome A — direct physical derivation

\[
F_{\rm cov}=F_{\rm std}
\]

under explicitly stated reduction assumptions, with no insertion of `FStd` or `muStd` into the covariant starting action.

Evidence label: **`[P_phys]`**, meaning a formal derivation from the specified action under explicitly listed physical/reduction premises. This label does not mean nature has been empirically validated.

### Outcome B — incompatibility

\[
F_{\rm cov}\neq F_{\rm std}
\quad\text{or}\quad
\mu_{\rm cov}\neq\mu_{\rm std}.
\]

Evidence label: **`[X]` incompatibility**. Preserve the raw derivation and identify the exact term, normalization, field redefinition, or limit assumption responsible. Do not tune the action to force equality.

### Outcome C — conditional bridge

\[
F_{\rm cov}=F_{\rm std}
\quad\text{only under an additional premise }A.
\]

Evidence label: **`[C_phys]` conditional physical bridge**. State premise `A` as a separate, inspectable assumption and do not promote it to a consequence of the action.

## Required derivation stages

### Stage 0 — source normalization

Before algebra, write a source-normalization table:

| Item | Required statement |
|---|---|
| Covariant metric | Signature, units, frame, and physical metric definition. |
| Fields | Exact covariant field content and whether each field is dynamical, auxiliary, or background. |
| Matter coupling | Minimal, conformal, disformal, or mixed; identify the metric seen by matter. |
| Scalar invariant | Exact definition of the covariant scalar argument, including sign conventions. |
| Free function | Exact function and normalization in the source action; do not infer it from a target `mu`. |
| Couplings | Dimensions, signs, and allowed ranges. |
| Boundary terms | Retained, discarded, or converted under the reduction. |
| Gauge/constraint conditions | Explicit gauge fixing and constraint equations. |

The stale `SkordisZlosnikEmbedding.lean` file is historical evidence only. Its `mu_dual` theorem must not be used as the live starting point.

### Stage 1 — weak-field ansatz

Define a one-parameter family with explicit scaling, for example

\[
g_{\mu\nu}=\eta_{\mu\nu}+\epsilon h_{\mu\nu},
\qquad
\Phi=\epsilon\Phi_1+O(\epsilon^2),
\qquad
\partial_t=O(\delta),
\]

and state the joint limit and order of limits. Identify which fields have nonzero background values and which perturbations survive.

Do not call an expression “weak-field” without specifying its order in `epsilon` and its derivative order in `delta`.

### Stage 2 — eliminate constraints and nondynamical fields

Derive the constraint equations from the covariant action. Solve or integrate out nondynamical fields only after stating boundary conditions. Record whether elimination is local, nonlocal, perturbative, or exact.

No AQUAL form may be assumed at this stage.

### Stage 3 — derive the quasistatic action

Substitute the ansatz and eliminated fields into the covariant action. Retain the leading nontrivial spatial-gradient terms and matter coupling. Display the raw result as `S_QS_raw` before simplification.

Track:

- signs;
- dimensions;
- normalization of `a_0`;
- scalar/vector/tensor mixing;
- boundary terms;
- total divergences;
- dependence on free functions and couplings.

### Stage 4 — vary the raw quasistatic action

Compute

\[
\frac{\delta S_{\rm QS,raw}}{\delta\Phi}=0
\]

and put the result into divergence form where justified. Define `mu_cov` from the derived coefficient of `nabla Phi`; do not define it in advance as `muStd`.

### Stage 5 — compare with the live constitutive certificate

Compare the derived `F_cov` and `mu_cov` with the independent Rung 1 certificate. Use exact symbolic simplification where possible and numerical checks only as supplemental diagnostics.

The comparison report must state:

- exact equality, inequality, or unresolved equivalence;
- assumptions used;
- field redefinitions used;
- whether the result is action-level or only equation-level;
- whether the comparison is global or restricted to an asymptotic regime.

### Stage 6 — formal interface

Only after the raw reduction is written should a Lean module be designed. The intended interfaces are:

- `MuStdConstitutive.lean`: Rung 1, stipulated mathematical function;
- `MuStdWeakField.lean`: raw weak-field/quasistatic reduction, with `[P_phys]`, `[C_phys]`, or `[X]` status;
- `MuStdCovariantReduction.lean`: later consolidation only after the intermediate theorem boundary is stable.

The first Rung 2 theorem should encode the actual raw result, even if it is not `muStd`. A theorem that assumes `mu_cov = muStd` as a structure field is not a derivation.

## Failure modes to test explicitly

1. **Normalization mismatch:** `a0` or the scalar kinetic prefactor changes the apparent `mu` function.
2. **Field-redefinition mismatch:** two actions look different but are equivalent only after an invertible map; prove the map and its domain.
3. **Order-of-limits mismatch:** `epsilon -> 0` and `partial_t -> 0` do not commute.
4. **Constraint omission:** an auxiliary vector or scalar constraint changes the effective constitutive law.
5. **Boundary-term contamination:** a discarded divergence contributes under the physical boundary conditions.
6. **Hidden target insertion:** `FStd` appears in the starting action, ansatz, constitutive definition, or solver objective.
7. **Convention drift:** the factor-of-two convention in `J'(Y)` changes the claimed `mu` without being recorded.
8. **Stale branch leakage:** `mu_dual` results are copied into a live physical theorem without an explicit historical label.

## Required artifacts

Each attempt must produce:

```text
rung2/
  SOURCE_NORMALIZATION.md
  WEAK_FIELD_ANSATZ.md
  CONSTRAINT_ELIMINATION.md
  S_QS_RAW.tex
  S_QS_RAW.json
  VARIATION_CHECK.md
  MU_COMPARISON.md
  provenance.json
  generated-output-sha256.txt
```

`provenance.json` must include the source commit, source artifact hashes, toolchain versions, command lines, and timestamp. `generated-output-sha256.txt` must hash every generated derivation artifact.

## Verification gates

Before any completion claim:

```bash
# baseline and source provenance
git rev-parse HEAD
sha256sum <all source artifacts>

# symbolic checks, if used
python3 verify_mu_std.py
python3 check_mu_std_certificate.py

# formal checks only after the theorem boundary is implemented
cd 05_lean_formalization
python3 check_target_inventory.py
lake build
lake env lean MuStdWeakField.lean
bash ./verify_all_proofs.sh

# repository hygiene
git diff --check
git status --short
```

A successful Lean gate certifies elaboration, absence of `sorry`, and the checked axiom footprint. It does not certify that the covariant action is physically adequate.

## Rung 2 completion criteria

Rung 2 is complete only when:

- the covariant starting action is quoted in a normalized, auditable form;
- the reduction ansatz and limit order are explicit;
- constraints and nondynamical fields are handled transparently;
- the raw quasistatic action is preserved before target comparison;
- variation produces the reported field equation;
- `mu_cov` is derived rather than stipulated;
- the comparison with `muStd` yields Outcome A, B, or C;
- all outputs are hash-pinned to the immutable baseline;
- the Lean theorem, if added, matches the raw derivation and carries explicit premises;
- no stale `mu_dual` result is silently promoted;
- the status ledger records `[P_phys]`, `[C_phys]`, `[X]`, or `[O_phys]` accurately.

## Immediate next action

Create only `SOURCE_NORMALIZATION.md` and `WEAK_FIELD_ANSATZ.md` first. Do not write `MuStdWeakField.lean` until those two documents identify the exact covariant action, conventions, fields, constraints, and limit procedure. This prevents the formal layer from encoding an unexamined physical premise.

## Non-claims

This plan does not claim that the covariant action reduces to `FStd`, that the current AeST completion is physically viable, or that the resulting model satisfies Cassini, PPN, GW, SPARC, cluster, or cosmological constraints. Those are downstream empirical questions.

## References

- [Res Nova repository](https://github.com/Mega-Therion/Res-Nova)
- [Target D2 physical action derivation](https://github.com/Mega-Therion/Res-Nova/blob/main/TARGET_D2_PHYSICAL_ACTION_DERIVATION.md)
- [Target D7 covariant completion](https://github.com/Mega-Therion/Res-Nova/blob/main/TARGET_D7_COVARIANT_COMPLETION.md)
- [Historical stale Skordis–Złośnik formal module](https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/SkordisZlosnikEmbedding.lean)
- [Rung 1 plan](</home/ubuntu/wide-research/Res-Nova-next-rung-plan.md>)
- [Machine-readable Rung 1 certificate](</home/ubuntu/wide-research/mu_std_certificate.json>)
