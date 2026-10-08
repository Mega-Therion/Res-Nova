# Navier–Stokes Remediation Completion Boundary

**Branch:** `research/navier-stokes-scope-remediation`
**Draft PR:** https://github.com/Mega-Therion/Res-Nova/pull/53
**Build-gate issue:** https://github.com/Mega-Therion/Res-Nova/issues/54

This file records what this program has completed and what it has **not** completed. It is the stop condition for any agent instructed to “solve Navier–Stokes.”

## Completed

1. Public/repository framing no longer treats current artifacts as a Clay Millennium solution.
2. Provenance of Lean, manuscript, Zenodo, Notion, and Drive copies is ledgered with hashes/status labels.
3. Paper 17 is recovered and audited: its Lyapunov/global-regularity claims are not supported by the displayed estimates or Lean listings.
4. Analytic dependencies are mapped in `NAVIER_STOKES_SOURCE_STATEMENTS.md`: Constantin–Fefferman's criterion, a periodic local/maximal-development theorem, and the Clay target are source-checked; the alignment reduction remains unmatched/open, and Euler BKM is not a substitute.
5. Lean L0–L2 starting modules exist:
   - `05_lean_formalization/NavierStokesScope.lean` — scalar threshold arithmetic.
   - `05_lean_formalization/NavierStokesGeometry.lean` — unit-vector distance bound.
   - `05_lean_formalization/NavierStokesSpec.lean` — kinematic high-vorticity alignment interface; persistence is a *definition of an obligation*, not a theorem.

6. The official Lake gate was rerun from the pinned-toolchain environment on 2026-10-08: `lake exe cache get` exit 0, `lake build` exit 0, and `bash verify_all_proofs.sh` exit 0. The gate reported `verified: 48 / 48 target(s)`, including `NavierStokesGeometry.lean`, `NavierStokesScope.lean`, and `NavierStokesSpec.lean`. Witness: `05_lean_formalization/VERIFICATION_RUN_2026-10-08_FINAL/official_gate_transcript.txt`.

## Not completed, and not claimed

- A proof of Clay/Fefferman Alternative B (or A, C, or D).
- Derivation of alignment persistence from 3D incompressible Navier–Stokes dynamics for all admissible data.
- A closed Lyapunov estimate eliminating the remaining positive `E^3` and `E` terms for arbitrary data.
- Independent PDE and Lean referee reports.

## Historical Lake-gate patch and verification record

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

The dated witness preserves the transcript, Lean version `4.33.0-rc1`, Mathlib revision `5eec30bc56ed5a23be2e27c544a949ba0bceddeb`, target results, standard-axiom output, and `witness_exit_code=0`. The gate's own result is authoritative for elaboration, absence of `sorry`, and standard axiom footprint; it does not justify assumptions carried in structures or theorem hypotheses.

## Exact remaining theorem

The only Clay-relevant open statement is, in the periodic setting:

> For every smooth, divergence-free initial velocity on `R^3/Z^3`, with zero force and positive viscosity, the corresponding strong solution remains globally smooth.

A sufficient research reduction, still unproved, is:

> Every such solution satisfies `AlignmentPredicate K L ρ` at every time of existence, for parameters that meet a source-verified vorticity-direction continuation theorem.

Until that implication is proved without assuming its conclusion, the project is a **conditional regularity program**.
