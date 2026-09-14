# Rung 2 Weak-Field and Quasistatic Ansatz

## Status and hard rule

This document defines the reduction ansatz for the Res Nova Rung 2 derivation. It does not derive the ansatz from the covariant action.

> **Hard rule:** start from the normalized covariant source action and derive the weak-field/quasistatic action independently. Do not start from `FStd` or `muStd` and engineer an AQUAL-looking equation.

The target comparison is downstream:

\[
S_{\rm cov}
\longrightarrow S_{\rm QS,raw}
\longrightarrow
\frac{\delta S_{\rm QS,raw}}{\delta\Phi}=0
\longrightarrow \mu_{\rm cov}(X)
\stackrel{?}{=}\mu_{\rm std}(X).
\]

The current status is **`[O_phys]`** until the normalized source action and the reduction are completed.

## 1. Provenance and dependency

This ansatz is drafted against:

- baseline commit: `aaca4f96978676230239e47a921704fa6353bb0f`;
- `SOURCE_NORMALIZATION.md` in the same branch;
- `THE_ONE_PAGE_UNIVERSAL_LAGRANGIAN.tex`;
- `TARGET_D2_PHYSICAL_ACTION_DERIVATION.md`;
- `TARGET_D7_COVARIANT_COMPLETION.md`.

The stale `SkordisZlosnikEmbedding.lean` module is not a source for the live `mu_std` reduction. It is retained as historical evidence of the earlier `mu_dual` formal branch.

## 2. Scaling parameters

Introduce two independent bookkeeping parameters:

- `epsilon`: weak-field amplitude;
- `delta`: time-derivative/quasistatic parameter.

They must not be silently identified.

Use a one-parameter family of fields with expansions

\[
\begin{aligned}
g_{\mu\nu}(\epsilon,\delta)
  &=\bar g_{\mu\nu}+\epsilon h_{\mu\nu}+O(\epsilon^2),\\
q^\mu(\epsilon,\delta)
  &=\bar q^\mu+\epsilon v^\mu+O(\epsilon^2),\\
\varphi(\epsilon,\delta)
  &=\bar\varphi+\epsilon\,\pi+O(\epsilon^2),\\
\phi(\epsilon,\delta)
  &=\bar\phi+\epsilon\,\sigma+O(\epsilon^2),\\
\rho(\epsilon,\delta)&=\epsilon\rho_1+O(\epsilon^2).
\end{aligned}
\]

Here `q^mu` denotes the covariant-completion vector only if that vector is present in the selected source action; otherwise the line is removed rather than assigning a fictitious field. The barred quantities are source-defined backgrounds, not free tuning parameters. **`[A]` pending source selection.**

For a static Newtonian chart, use

\[
 ds^2=-(1+2\epsilon\Phi/c^2)c^2dt^2
 +(1-2\epsilon\Psi/c^2)\delta_{ij}dx^idx^j
 +O(\epsilon^2),
\]

or the exact metric convention supplied by the normalized source. The potentials `Phi` and `Psi` are independent until the field equations establish a relation. Do not impose `Phi=Psi` in the ansatz. **`[A]`**

## 3. Derivative counting

Define the quasistatic scaling by

\[
\partial_t=O(\delta\,\partial_i),
\qquad
\partial_i=O(1),
\qquad
\delta\to0.
\]

The reduction must report both orders:

| Quantity | Weak-field order | Quasistatic order |
|---|---:|---:|
| `h_mu nu`, `v^mu`, `pi`, `sigma` | `O(epsilon)` | source-dependent |
| `partial_i Phi`, `partial_i Psi` | `O(epsilon)` | `O(1)` relative to spatial gradients |
| `partial_t Phi`, `partial_t Psi` | `O(epsilon delta)` | suppressed |
| `partial_t^2` terms | `O(epsilon delta^2)` | suppressed at leading order |
| matter density `rho` | `O(epsilon)` in perturbative bookkeeping | time-independent at leading order |

A term may be discarded only with its `(epsilon, delta)` order recorded. A total derivative may be discarded only after boundary conditions are stated.

## 4. Background and boundary assumptions

The first reduction attempt must state whether it uses:

1. asymptotically Minkowski background or a local FLRW patch;
2. constant scalar backgrounds or nonzero background gradients;
3. aligned or non-aligned background vector;
4. compact-support matter, isolated source, or periodic domain;
5. asymptotic conditions on `Phi`, `Psi`, and scalar perturbations;
6. a fixed horizon or no-horizon local patch.

The minimal isolated-system ansatz is:

\[
\bar g_{\mu\nu}=\eta_{\mu\nu},
\qquad
\partial_\mu\bar\varphi=0,
\qquad
\bar q^\mu\bar q_\mu=-1,
\qquad
\Phi,\Psi,\pi,\sigma\to0\quad(r\to\infty),
\]

but this is a proposed reduction assumption, not a consequence of the full cosmological theory. If a nonzero background scalar gradient is required by the selected action, this minimal ansatz fails and must be replaced. **`[A]`/`[O_phys]`**

## 5. Field and gauge choices

The initial calculation must use a declared gauge. A candidate Newtonian gauge is

\[
 h_{0i}=0,
\qquad
 h_{ij}=-(2\Psi/c^2)\delta_{ij},
\qquad
 h_{00}=-(2\Phi/c^2),
\]

with residual gauge conditions documented. For a vector/aether field, impose only the source's normalization constraint and a separately stated perturbation gauge; do not set vector perturbations to zero before varying.

The scalar perturbations are varied before any field redefinition. If a field redefinition is introduced, record its inverse and domain and prove that it preserves the action to the retained order. **`[A]`**

## 6. Order of limits

The primary prescribed limit is:

\[
\text{first vary the covariant action, then expand in }\epsilon,
\text{ then take }\delta\to0\text{ at fixed leading spatial gradients}.
\]

The action-level comparison must also record whether the alternative order

\[
\delta\to0\text{ before variation}
\]

is equivalent. If the two orders differ, the difference is a genuine reduction issue and must be reported, not selected for convenience.

The target leading action is only schematic:

\[
S_{\rm QS,raw}
=\int dt\,d^3x\,
\left[\mathcal L_{\rm grav}^{(2)}(\Phi,\Psi)
+\mathcal L_{\rm scalar}^{(\pi)}
+\mathcal L_{\rm vector}^{(v)}
+\mathcal L_{\rm mix}
+\mathcal L_{\rm matter}\right]
+O(\epsilon^3,\delta),
\]

where every displayed term must come from the source action. The familiar AQUAL form

\[
\int d^3x\left[\frac{|\nabla\Phi|^2}{8\pi G}+a_0^2F(X)+\rho\Phi\right]
\]

is a comparison target, not an ansatz for `S_QS_raw`.

## 7. Constraints and nondynamical fields

The reduction must proceed in this order:

1. vary all covariant fields;
2. expand the equations and constraints to the retained order;
3. identify nondynamical fields;
4. solve their constraints with boundary conditions;
5. substitute the solution back into the action only when the elimination is justified;
6. preserve the pre-elimination equations as an audit artifact.

In particular, do not remove vector/aether perturbations, lapse/shift variables, scalar auxiliaries, or multipliers solely because they are absent from the desired AQUAL target. **`[A]` procedural requirement.**

## 8. Definition of the derived constitutive law

After obtaining `S_QS_raw`, define `F_cov` and `mu_cov` only if the reduced action can be put into an AQUAL-equivalent form. Let

\[
X=\frac{|\nabla\Phi|}{a_0}.
\]

Then the derived equation must be written as

\[
\nabla\cdot\left[\mu_{\rm cov}(X)\nabla\Phi\right]=4\pi G_{\rm eff}\rho
\]

or, if the coefficient is not of this form, the failure to obtain an AQUAL constitutive law must be recorded.

The comparison is:

\[
\mu_{\rm std}(X)=\frac{X}{\sqrt{1+X^2}},
\qquad
F_{\rm std}(X)=\frac12\left[X\sqrt{1+X^2}-\operatorname{arsinh}X\right].
\]

No equality may be claimed from notation, rapidity substitution, or a field redefinition alone. **`[P_math]` for the Rung 1 identities; `[O_phys]` for the covariant comparison.**

## 9. Explicit tests for hidden target insertion

Before accepting a result, inspect the derivation for:

- `FStd` or `muStd` in the starting action;
- `FStd` or `muStd` in the weak-field ansatz;
- a constitutive relation imposed as a constraint rather than derived by variation;
- a solver objective minimizing residuals to `muStd`;
- normalization choices selected only because they produce `muStd`;
- a field redefinition whose definition contains `muStd`;
- use of the stale `mu_dual` theorem as if it were a live source result.

Any such occurrence is a derivation invalidation, not a minor caveat.

## 10. Outcome classification

| Derived result | Status |
|---|---|
| `mu_cov = muStd` with no target insertion and stated assumptions | `[P_phys]` |
| `mu_cov != muStd` or no AQUAL form | `[X]` incompatibility or `[O_phys]` if unresolved |
| equality only after explicit extra premise `A` | `[C_phys]` conditional |
| result depends on order of limits or unspecified boundary data | `[O_phys]` until resolved |

A successful formal Lean compilation does not upgrade `[O_phys]` or `[C_phys]` to `[P_phys]` unless the formal theorem contains the actual reduction and all premises are inspectable.

## 11. Required output artifacts

The first implementation pass must produce, before any polished claim:

```text
rung2/
  SOURCE_NORMALIZATION.md
  WEAK_FIELD_ANSATZ.md
  COVARIANT_ACTION_SOURCE.tex
  CONSTRAINT_EQUATIONS.tex
  S_QS_RAW.tex
  S_QS_RAW.json
  VARIATION_CHECK.md
  MU_COMPARISON.md
  provenance.json
  generated-output-sha256.txt
```

The source and ansatz documents belong in the repository root for discoverability; generated calculations belong under `rung2/` and must be hash-pinned.

## 12. Gate before formalization

Do not create `MuStdWeakField.lean` until the following are complete:

- source action selected and normalized;
- all field backgrounds declared;
- gauge and boundary conditions declared;
- order of limits declared;
- raw constraint equations written;
- all discarded terms have `(epsilon, delta)` orders;
- raw `S_QS` produced before comparison with `FStd`;
- `mu_cov` defined from variation or an explicit failure recorded.

## Non-claims

This ansatz does not claim:

- that `muStd` follows from the covariant action;
- that `Phi=Psi` holds before variation;
- that the vector/aether sector decouples;
- that the universal assembly action and D7 AeST completion are identical;
- that the resulting theory passes solar-system, PPN, gravitational-wave, cluster, or cosmological tests.

## References

- [Source normalization](SOURCE_NORMALIZATION.md)
- [Candidate universal action](THE_ONE_PAGE_UNIVERSAL_LAGRANGIAN.tex)
- [D2 physical action derivation](TARGET_D2_PHYSICAL_ACTION_DERIVATION.md)
- [D7 covariant completion audit](TARGET_D7_COVARIANT_COMPLETION.md)
- [Rung 2 derivation plan](https://github.com/Mega-Therion/Res-Nova/blob/main/Res-Nova-Rung-2-MuStdWeakField-plan.md)
