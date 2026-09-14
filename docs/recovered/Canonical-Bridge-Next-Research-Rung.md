# Res Nova Canonical `mu_std` Bridge — Next Research Rung

## Goal

Establish the smallest defensible bridge from a specified scalar constitutive functional to the live low-acceleration law

\[
\mu_{\rm std}(x)=\frac{x}{\sqrt{1+x^2}},
\]

while explicitly separating mathematical identities, imported physical assumptions, and unresolved covariant physics.

## Verified baseline

- Repository: `Mega-Therion/Res-Nova`
- Branch: `main`
- Baseline commit: `aaca4f96978676230239e47a921704fa6353bb0f`
- Pinned Lean toolchain: `leanprover/lean4:v4.33.0-rc1`
- Current target inventory: **45 Lean targets**, with `lakefile.lean`, `verify_all_proofs.sh`, and on-disk modules agreeing.
- The current `SkordisZlosnikEmbedding.lean` module is explicitly stale: its formal definitions still encode `mu_dual(x)=x/(1+x)` even though repository status treats that branch as physically falsified.

## Rung boundary

### Inputs

1. A real scalar variable `x`, with the physical domain restricted to `x > 0` for constitutive and asymptotic statements.
2. The candidate constitutive law
   \[
   \mu_{\rm std}(x)=x(1+x^2)^{-1/2}.
   \]
3. The AQUAL convention
   \[
   F'(x)=x\mu(x).
   \]
4. The candidate primitive
   \[
   F_{\rm std}(x)=\frac12\left[x\sqrt{1+x^2}-\operatorname{arsinh}(x)\right].
   \]
5. The rapidity substitution `x = sinh(psi)` where used.

### Proved output for this rung

The formal and symbolic package should establish:

1. `F_std'(x) = x * mu_std(x)` on the real line, with the derivative convention stated explicitly.
2. `mu_std(sinh(psi)) = tanh(psi)`.
3. `mu_std(x) -> 0` as `x -> 0+` and `mu_std(x) -> 1` as `x -> +∞`.
4. The high-acceleration expansion
   \[
   \mu_{\rm std}(x)=1-\frac{1}{2x^2}+O(x^{-4}).
   \]
5. The deep-acceleration expansion
   \[
   \mu_{\rm std}(x)=x-\frac12x^3+O(x^5).
   \]
6. Strict positivity and monotonicity on `x > 0`.
7. Convexity of `F_std` on `x > 0`, if the required derivative theorem is included.

### Evidence class

- Items 1–7: `[P]` mathematical consequences of the definitions and stated domain assumptions.
- The assertion that this constitutive law is selected by the covariant physical action: `[O]` until the stale covariant module is rebuilt and the weak-field/quasistatic reduction is derived.
- The assertion that the law is observationally viable: `[C]` or `[E]` only after the model-specific Cassini `Q_2`, PPN, gravitational-wave, cluster, and cosmological analyses are complete.

## Explicit non-claims

This rung does **not** prove:

- that `mu_std` is uniquely forced by Information Tension, G.O.D., rapidity, Fisher geometry, or any fundamental theory;
- that the current AeST/Skordis–Złośnik completion is exactly equivalent to the candidate AQUAL functional;
- that spherical residual bounds are a valid substitute for the anisotropic Cassini `Q_2` observable;
- that SPARC agreement discriminates the theory from MOND or cored dark-matter models;
- that E8/triality derives the Standard Model or three physical generations;
- that the classical action defines a quantum theory;
- that an information-dependent horizon term belongs in the fundamental action.

## Required implementation sequence

### Task 1 — symbolic constitutive certificate

Create a standalone SymPy script outside the repository source tree that differentiates `F_std`, verifies the identity exactly, computes the two asymptotic expansions, and checks positivity/monotonicity symbolically where possible. Save the exact output as an auditable text artifact.

Gate: the script exits zero and asserts every exact identity.

### Task 2 — canonical specification document

Create `THEORY_KERNEL.md` in the repository only after the specification is reviewed. It must contain:

- primitive postulates;
- field dictionary;
- units and mass dimensions;
- action convention;
- live versus stale constitutive branches;
- theorem/evidence labels;
- explicit non-claims;
- model hash and source commit;
- downstream dependencies.

Do not place the universal assembly action in the kernel as a fundamental action until its sectors are derived from the primitive postulates. Retain it as `Candidate Fundamental Action — Version 0`.

### Task 3 — rebuild the stale covariant module

Replace the stale `mu_dual` definitions in the covariant-completion formalization with the live `mu_std` functional only after writing the exact theorem boundary. The first module should prove algebraic matching of the constitutive derivative, not claim a full AeST physical embedding.

Suggested stable names:

- `FStd`
- `muStd`
- `fStdDeriv`
- `muStdRapidity`
- `muStdNewtonianTail`
- `muStdDeepLimit`

Suggested module: `05_lean_formalization/MuStdConstitutive.lean`.

### Task 4 — isolation and full gate

Run in the pinned environment:

```bash
cd 05_lean_formalization
python3 check_target_inventory.py
lake build
lake env lean MuStdConstitutive.lean
bash ./verify_all_proofs.sh
```

Then run:

```bash
git diff --check
git status --short
```

The full gate certifies elaboration, absence of `sorry`, and the reported axiom footprint. It does not certify the physical assumptions carried in structures or typeclasses.

### Task 5 — status reconciliation

Update the module ledger and status note with the exact theorem boundary and gate output. Any remaining `mu_dual` module must be marked `[X]-stale` or rebuilt; it must not remain labeled as a live physical result.

## Evaluation rubric

A future implementation passes this rung only if all criteria are satisfied:

| Criterion | Required evidence |
|---|---|
| Exact constitutive identity | SymPy assertions and Lean theorem agree. |
| Domain discipline | Theorems state real/positive assumptions explicitly. |
| Stale-branch control | No live status document calls `mu_dual` viable. |
| Formal honesty | The Lean theorem boundary lists assumptions and non-claims. |
| Reproducibility | Fresh-clone commands and pinned toolchain are recorded. |
| No hidden shortcuts | No `sorry`, custom axioms, or unreviewed premise-retrieval theorem. |
| Physical boundary | No claim of action-level derivation until the covariant reduction is actually shown. |

## Next honest rung after this one

Derive the weak-field/quasistatic limit of the **canonical covariant action** and show whether its constitutive equation reduces to the `F_std` identity above. If the result fails, record the incompatibility as `[O]` or `[X]`; do not tune the action until the mismatch is mathematically characterized.

## Research-program layers

- **Layer I — Res Nova Core:** covariant gravitational action, limits, constraints, and reproducible tests.
- **Layer II — G.O.D./Information Tension:** invariant state-space functional and derivation of the constitutive law.
- **Layer III — geometric Standard-Model unification:** representation decomposition, anomaly cancellation, symmetry breaking, masses, mixing, and quantum consistency.

The present rung advances Layer I only and supplies a precise interface for Layer II. It does not advance Layer III.

## Review note

The attached critique’s most important recommendation is accepted: the project should stop treating the universal assembly Lagrangian as the theory and instead build a derivational chain. The horizon mutual-information term remains a candidate information-geometric boundary functional, not a fundamental action term, until derived from a specified quantum theory.

## Reproducibility record

This plan was prepared against the baseline listed above. It does not modify the repository and makes no claim that the next rung has been implemented or that the full formal gate passes beyond the inventory result explicitly recorded here.

## References

- [Res Nova repository](https://github.com/Mega-Therion/Res-Nova)
- [MuStdUniqueness.lean](https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/MuStdUniqueness.lean)
- [SkordisZlosnikEmbedding.lean](https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/SkordisZlosnikEmbedding.lean)
- [Target D2 physical action derivation](https://github.com/Mega-Therion/Res-Nova/blob/main/TARGET_D2_PHYSICAL_ACTION_DERIVATION.md)
- [Grounded bricks versus hypothesis map](https://github.com/Mega-Therion/Res-Nova/blob/main/GROUNDED_BRICKS_VS_HYPOTHESIS_MAP.md)
- [Information Tension Zenodo record](https://zenodo.org/records/21504895)
- Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). [Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](https://doi.org/10.48550/arXiv.2609.00065).

The last citation records the SymPy/formal research skill contribution to this working plan; it is not evidence for the physical theory.


## Amendment record — approved from the follow-up audit

The following changes are now part of the rung specification:

1. **Separate domains.** The formal API must define global functions `muStd : ℝ → ℝ` and `FStd : ℝ → ℝ`; positivity, monotonicity, convexity, and physical asymptotics carry explicit `0 < x` or `x → +∞` hypotheses. The physical restriction must not be baked into the definitions.
2. **Add exact bounds.** Include `0 < muStd x < 1` for `x > 0`, together with the exact residual identity `1 - muStd x`; an inverse-square residual bound may be added only if proved with its exact domain and inequality direction.
3. **Add derivative infrastructure.** Formalize `muStd' x = (1+x^2)^(-3/2)` as a named theorem because it is the interface for perturbations, stability, and quasistatic field equations.
4. **Three evidence subtypes.** Use `[P_math]` for algebraic/formal identities, `[O_phys]` for the unproved covariant-to-AQUAL bridge, and `[E_emp]` for observational tests. Do not let a green Lean theorem imply physical derivation.
5. **Machine-readable certificate.** The SymPy script must emit `mu_std_certificate.json`, while its human-readable output remains diagnostic only. SymPy is an independent symbolic check, not the authority for the Lean theorem.
6. **Preserve history.** Do not overwrite `SkordisZlosnikEmbedding.lean` immediately. Keep its stale `mu_dual` definitions visible and explicitly disabled/historical. Add a new `MuStdConstitutive.lean`; reserve `MuStdWeakField.lean` and `MuStdCovariantReduction.lean` for later rungs.
7. **No uniqueness theorem.** This rung must not add any uniqueness theorem for `muStd`, even conditional uniqueness. Selection by a fundamental action remains open.
8. **Future physical pass/fail interface.** The next physical rung must predefine a limit map of the form
   \[
   S_{\rm cov}\xrightarrow{\epsilon\to0,\,\partial_t\to0}S_{\rm QS}
   =\int d^3x\,[\rho\Phi+a_0^2F(X)],
   \quad X=|\nabla\Phi|/a_0,
   \]
   followed by variation to
   \[
   \nabla\cdot[\mu(X)\nabla\Phi]=4\pi G\rho.
   \]
   The result must be compared to `muStd` without inserting it by hand. `F_cov ≠ F_std` is a valid research result and must be recorded rather than tuned away.

The intended dependency staircase is now:

```text
MuStdConstitutive [P_math]
        ↓
MuStdWeakField [O_phys until derived]
        ↓
MuStdCovariantReduction [O_phys / pass-fail]
        ↓
SolarSystem / PPN / GW / Cosmology [E_emp]
```

This amendment changes the plan only; it does not modify the public repository.
