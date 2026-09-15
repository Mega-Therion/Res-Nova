# Navier–Stokes Remediation Completion Boundary

**Branch:** `research/navier-stokes-scope-remediation`
**Draft PR:** https://github.com/Mega-Therion/Res-Nova/pull/53
**Build-gate issue:** https://github.com/Mega-Therion/Res-Nova/issues/54

This file records what this program has completed and what it has **not** completed. It is the stop condition for any agent instructed to “solve Navier–Stokes.”

## Completed

1. Public/repository framing no longer treats current artifacts as a Clay Millennium solution.
2. Provenance of Lean, manuscript, Zenodo, Notion, and Drive copies is ledgered with hashes/status labels.
3. Paper 17 is recovered and audited: its Lyapunov/global-regularity claims are not supported by the displayed estimates or Lean listings.
4. Analytic dependencies are mapped: Constantin–Fefferman-style direction-of-vorticity criteria and a correct Navier–Stokes continuation theorem remain imported/open; Euler BKM is not a substitute.
5. Lean L0–L2 starting modules exist:
   - `05_lean_formalization/NavierStokesScope.lean` — scalar threshold arithmetic.
   - `05_lean_formalization/NavierStokesGeometry.lean` — unit-vector distance bound.
   - `05_lean_formalization/NavierStokesSpec.lean` — kinematic high-vorticity alignment interface; persistence is a *definition of an obligation*, not a theorem.

## Not completed, and not claimed

- A proof of Clay/Fefferman Alternative B (or A, C, or D).
- Derivation of alignment persistence from 3D incompressible Navier–Stokes dynamics for all admissible data.
- A closed Lyapunov estimate eliminating the remaining positive `E^3` and `E` terms for arbitrary data.
- ~~Kernel-checked inclusion of the new modules in `lakefile.lean` / `verify_all_proofs.sh`.~~ **Closed 2026-09-15** — see "Lake-gate patch status" below. Build-gate only; every other item in this list stands.
- Independent PDE and Lean referee reports.

## Required Lake-gate patch

`verify_all_proofs.sh` requires its `TARGETS` array to equal the `roots` in `lakefile.lean`. After retrieving those files in full, add these names in the same order used by the existing inventory:

- `` `NavierStokesGeometry `` / `NavierStokesGeometry.lean`
- `` `NavierStokesScope `` / `NavierStokesScope.lean`
- `` `NavierStokesSpec `` / `NavierStokesSpec.lean`

Then, on a machine with the pinned toolchain:

```bash
cd 05_lean_formalization
lake exe cache get
lake build
bash verify_all_proofs.sh
```

Preserve the transcript, Lean version, Mathlib revision, target count, and `#print axioms` output. Do not report compilation success until that command exits 0.

**Lake-gate patch status — CLOSED 2026-09-15.** `NavierStokesScope.lean` and `NavierStokesSpec.lean`
required `noncomputable` on their `alignmentGate` / `alignmentFromGate` definitions, and one proof
needed `unfold` + `ring` in place of `simp` + `ring`. Both fixed; committed and pushed to `main` as
`365e457` ("fix(lean): mark alignmentGate/alignmentFromGate noncomputable, fix ring proof").
Measured here 2026-09-15 (gate re-run in full, not taken on report): `bash verify_all_proofs.sh` →
`verified: 48 / 48 target(s)` / `RESULT: PASS`, **exit 0**; `check_target_inventory.py` →
`PASS — 48 Lean targets; lakefile, gate, and on-disk modules agree`, exit 0.
This closes the *build-gate* item in "Not completed" above (kernel-checked inclusion of the new
modules). It closes **nothing analytic** — the Constantin–Fefferman-style dependencies remain
imported/open, alignment persistence remains a definition of an obligation rather than a theorem,
and the Clay-relevant open statement below is untouched.

## Exact remaining theorem

The only Clay-relevant open statement is, in the periodic setting:

> For every smooth, divergence-free initial velocity on `R^3/Z^3`, with zero force and positive viscosity, the corresponding strong solution remains globally smooth.

A sufficient research reduction, still unproved, is:

> Every such solution satisfies `AlignmentPredicate K L ρ` at every time of existence, for parameters that meet a source-verified vorticity-direction continuation theorem.

Until that implication is proved without assuming its conclusion, the project is a **conditional regularity program**.
