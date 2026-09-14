# Rung 2 Source Normalization

## Status and theorem boundary

This document freezes the source conventions for the Res Nova Rung 2 weak-field/quasistatic derivation. It is a **normalization record**, not a derivation and not an endorsement of every term in the universal assembly action.

> **Rung 1 result:** `mu_std` is formally characterized, not physically derived.

Rung 2 must begin from the source action and independently derive its weak-field/quasistatic limit. It must not begin from `FStd` or `muStd` and engineer a matching result.

Evidence labels used here are:

- **`[S]` source transcription:** copied or normalized from a repository source document;
- **`[D]` derived:** obtained by algebra or variation from the normalized source;
- **`[A]` assumption:** introduced for the reduction and not derived by the source action;
- **`[O_phys]` open physical issue:** not established by the current corpus;
- **`[X]` incompatibility:** reserved for a demonstrated mismatch.

## Provenance

This document was drafted against the clean baseline:

- Repository: `Mega-Therion/Res-Nova`
- Baseline commit: `aaca4f96978676230239e47a921704fa6353bb0f`
- Branch used for this draft: `docs/rung2-source-normalization`
- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`
- Baseline Lean target inventory: 45 targets

### Source hashes at baseline

| Source | SHA-256 |
|---|---|
| `THE_ONE_PAGE_UNIVERSAL_LAGRANGIAN.tex` | `833eab2a9fda5e70bf7ee849de2c7da9c760ecfdd6a266b4f4d7b4a1b8692461` |
| `TARGET_D2_PHYSICAL_ACTION_DERIVATION.md` | `a51df2e17c2219f0f00809795df2bb9430832a4baf1787c8034c2435c45e901c` |
| `TARGET_D7_COVARIANT_COMPLETION.md` | `ef3073cd6565bb97ade29a0be0eb11e49cce1e8983e10168f222008b0976255e` |
| `05_lean_formalization/SkordisZlosnikEmbedding.lean` | `1ef6cd70626d7d659fd9912013e69b0016de15658e6f77376d91845292ef7150` |

The universal Lagrangian source is a candidate assembly action. The D7 record is the current covariant-completion audit. Where they differ in field content or convention, this document records the difference rather than silently merging them.

## 1. Candidate universal assembly action

The repository's one-page candidate writes, schematically,

\[
\begin{aligned}
S_{\rm univ}=\int_{\mathcal M}d^4x\sqrt{-g}\,\{&
\frac{c^4}{16\pi G}e^{-2\phi}(R-2\Lambda_0)
-\frac12(\nabla\phi)^2-\frac12m_\phi^2\phi^2-\frac{\lambda_\phi}{4!}\phi^4\\
&-\frac{c^4a_0^2}{8\pi G}\left[\sqrt{Y(1+Y)}-\operatorname{arsinh}\sqrt{Y}\right]
+\mathcal L_{V,A}+\mathcal L_{\rm hol}+\mathcal L_{E_8}+\mathcal L_{\rm fermion}+\mathcal L_{\rm Yukawa}\}\,+S_{\rm boundary},
\end{aligned}
\]

where the displayed source defines

\[
Y=\frac{g^{\mu\nu}\partial_\mu\chi\partial_\nu\chi}{a_0^2},
\qquad a_0=\frac{cH_0}{2\pi}
\]

and labels the scalar-gradient term an information-tension AQUAL functional. **`[S]`**

This transcription must not yet be interpreted as a uniquely defined fundamental action because the source does not by itself settle signature, scalar normalization, physical metric, boundary conditions, or the relation between the displayed `chi` sector and the D7 AeST scalar invariant. **`[O_phys]`**

### 1.1 Terms relevant to the first reduction

For Rung 2, retain only terms that can contribute to the weak-field gravitational/scalar sector, and classify all other terms before discarding them:

| Sector | Source expression or role | Rung 2 treatment |
|---|---|---|
| Gravitational metric | `e^{-2 phi}(R - 2 Lambda_0)` | Retain; normalize frame and scalar background first. |
| Dilaton kinetic/potential | `-(nabla phi)^2/2 - m_phi^2 phi^2/2 - lambda_phi phi^4/4!` | Retain symbolically until scaling proves suppression or contribution. |
| Information-tension scalar | Function of `Y = g^{mu nu} partial_mu chi partial_nu chi / a0^2` | Retain; derive its variation from the exact source function. |
| `V,A` substrate | Stiefel kinetic and holonomy curvature terms | Retain only if background or constraints couple them into the scalar/metric equations; otherwise prove decoupling under the chosen background. |
| `E8` gauge sector | Yang–Mills and theta terms | Do not assume decoupling; state background and perturbative order. |
| Fermions/Yukawa | Matter fields and scalar-dependent masses | Replace by a specified stress-energy/matter source only after declaring the matter approximation. |
| Boundary/horizon | GHY term plus mutual-information horizon term | Retain GHY when required by variation; exclude horizon mutual-information term from local weak-field bulk reduction unless a separate derivation supplies its variation. |

The universal action's Standard-Model, E8/triality, and horizon interpretations are outside the first Rung 2 reduction unless their variation is shown to enter the selected sector. They must not be used as unexplained normalization inputs. **`[A]`/`[O_phys]`**

## 2. Covariant completion source record

The D7 audit identifies the intended relativistic scalar-vector-tensor completion as an AeST/Skordis–Zlosnik-type action whose scalar free function is written in terms of an invariant such as

\[
\mathcal Y=\tilde a_0^{\,2}\,q^{\mu\nu}\nabla_\mu\varphi\nabla_\nu\varphi,
\]

with a function `J(Y)` and a vector/aether sector. The exact source convention, including the physical metric, vector normalization, `J` prefactors, and `tilde a_0` relation, must be copied from the selected D7 equations into the Stage 0 working record before variation. **`[S]`/`[O_phys]`**

The current Lean module `SkordisZlosnikEmbedding.lean` is historical/stale for the live phenomenology: its theorem still encodes the `mu_dual(x)=x/(1+x)` branch. It must not be treated as the canonical Rung 2 source and must not be overwritten in this document. **`[S]`**

D7 records the following important source-level facts:

- the `mu_dual` branch is ruled out by the stated solar-system residual within two-derivative AQUAL/AeST; **`[D]`/`[X]` for that branch**;
- the live `mu_std` branch is a surviving route in the current program, but its covariant derivation remains open; **`[O_phys]`**;
- `c_T=c` and `gamma_PPN=1` have documented conditional/source support, while `beta`, `alpha_1`, and `alpha_2` remain open; **`[C]`/`[O_phys]`**;
- the scalar free-function normalization and the relation between `a_0` and `tilde a_0` must be made explicit before a constitutive comparison. **`[O_phys]`**

## 3. Conventions to freeze before calculation

The following fields are mandatory entries in the Rung 2 source-normalization worksheet. A blank entry is a gate failure, not permission to choose a convenient convention.

| Convention | Required value or decision | Current status |
|---|---|---|
| Spacetime dimension | `d = 4` | `[S]` |
| Coordinates | `x^mu = (t, x^i)` with units stated | `[A]` until recorded in worksheet |
| Metric signature | Explicit sign convention | `[O_phys]` in current one-page source |
| Curvature sign | Riemann/Ricci convention and Einstein-Hilbert sign | `[O_phys]` until selected source is fixed |
| Physical metric | `g_mu nu`, disformal `tilde g_mu nu`, or other | `[O_phys]` |
| Newton constant | `G` and whether it is bare or measured | `[O_phys]` |
| Speed/light constants | `c`, `hbar`, `k_B` retained or set to one | `[A]` |
| Scalar backgrounds | `phi_0`, `chi_0` or `varphi_0` and perturbation variables | `[O_phys]` |
| Acceleration scale | `a_0 = c H_0/(2 pi)` versus `tilde a_0` | `[O_phys]` |
| Scalar invariant | Exact sign and normalization of `Y` or `mathcal Y` | `[O_phys]` |
| Vector normalization | Unit-timelike constraint and multiplier, if present | `[O_phys]` |
| Matter coupling | Minimal/conformal/disformal and matter frame | `[O_phys]` |
| Boundary conditions | Asymptotic, finite-domain, horizon, or compact support | `[A]` |
| Gauge choice | Metric and vector gauge | `[A]` |

## 4. Dimension and sign checks

Before any weak-field expansion, verify dimensionally that:

1. the action has dimensions of action;
2. `Y` or `mathcal Y` is dimensionless under the selected units;
3. every term in the scalar free-function sector has the same dimension;
4. the matter source term has the sign that yields the chosen Poisson convention;
5. the scalar kinetic matrix has the sign required by the selected metric signature;
6. the `a_0`/`tilde a_0` rescaling is not absorbed into `mu` without being recorded.

These are algebraic gates. They do not establish ghost freedom, stability, or observational viability. **`[D]` only after checked.**

## 5. Exclusions from the source normalization

The following are explicitly not source-normalized by this document:

- a uniqueness derivation for `mu_std`;
- an information-theoretic derivation of the `n=1` interpolation exponent;
- E8/triality derivations of Standard-Model generations;
- a quantum completion of the classical action;
- an independent derivation of the horizon mutual-information term;
- any claim that the candidate universal assembly action is the same object as the audited AeST covariant completion.

## 6. Gate for proceeding to the ansatz

Rung 2 may proceed to `WEAK_FIELD_ANSATZ.md` only after a selected source action has:

- one exact displayed equation or machine-readable transcription;
- fixed signature and curvature convention;
- fixed physical metric and matter frame;
- fixed scalar/vector backgrounds;
- fixed `a_0`/`tilde a_0` normalization;
- fixed boundary and gauge conditions;
- an explicit classification of every omitted term.

Until then, a weak-field derivation is **`[O_phys]`**, not a theorem.

## References

- [Candidate universal action](THE_ONE_PAGE_UNIVERSAL_LAGRANGIAN.tex)
- [D2 physical action derivation](TARGET_D2_PHYSICAL_ACTION_DERIVATION.md)
- [D7 covariant completion audit](TARGET_D7_COVARIANT_COMPLETION.md)
- [Historical stale covariant formalization](05_lean_formalization/SkordisZlosnikEmbedding.lean)
- [Rung 2 derivation plan](https://github.com/Mega-Therion/Res-Nova/blob/main/Res-Nova-Rung-2-MuStdWeakField-plan.md)
