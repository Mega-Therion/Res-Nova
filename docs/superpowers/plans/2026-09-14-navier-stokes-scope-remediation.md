# Navier–Stokes Scope Remediation Implementation Plan

> **For agentic workers:** Execute the tasks in order and verify each artifact before moving to the next.

**Goal:** Integrate and kernel-check the existing scoped Lean modules, correct overclaimed identifiers and documentation, source-check the analytic dependencies, and leave the global Clay implication explicitly open.

**Architecture:** Keep the official target as Clay/Fefferman Alternative B on the periodic domain R³/Z³. Separate elementary Lean results (L0–L2) from imported or open PDE results (L3–L5); preserve historical records and add dated corrections rather than deleting provenance. Record every build and source decision in repository artifacts and report the actual state to PR #53 and issue #54.

**Tech Stack:** Lean 4/Lake, pinned Mathlib revision, Bash verification gate, Markdown evidence ledger, GitHub CLI, primary PDE literature and Zenodo provenance.

**Spec:** `/home/ubuntu/upload/Pasted_content_01.txt`

## Global Constraints

- Never describe the work as a Millennium Prize solution or global Navier–Stokes regularity proof unless the hard gate is met.
- Never upgrade a theorem that restates an assumed field or tautology.
- Never use Euler BKM as an NS continuation theorem, an L² enstrophy bound as L¹_tL∞_x control, or a dimensionless alignment threshold as a Lipschitz constant without explicit normalization.
- Never move R³ theorems to R³/Z³ informally.
- No `sorry`, `admit`, hidden axioms, or stronger theorem names than their types.
- Preserve historical/superseded records and add dated corrections.
- Every public claim names assumptions, domain, solution class, source, build command, and limitations.

---

### Task 1: Inventory repository and recover source artifacts

**Files:**
- Create: `docs/superpowers/plans/2026-09-14-navier-stokes-scope-remediation.md`
- Inspect: required documents and all `05_lean_formalization/*.lean`

- [x] Clone `Mega-Therion/Res-Nova`, checkout `research/navier-stokes-scope-remediation`, inspect PR #53 and issue #54.
- [ ] Search repository and available external sources for the complete Sovereign Regularity manuscript, Paper 17 manuscript, and any `TensionProof.lean`/`NavierStokes.lean` files.
- [ ] Record missing or unrecoverable artifacts without inventing content.

### Task 2: Integrate and verify the Lean target inventory

**Files:**
- Modify: `05_lean_formalization/lakefile.lean`
- Modify: `05_lean_formalization/verify_all_proofs.sh`
- Create: dated build witness under `05_lean_formalization/VERIFICATION_RUN_*` or repository audit directory

- [ ] Add `NavierStokesGeometry`, `NavierStokesScope`, and `NavierStokesSpec` to both inventories, keeping them set-equal.
- [ ] Run `lake exe cache get`, `lake build`, and `bash verify_all_proofs.sh` from `05_lean_formalization`.
- [ ] Capture Lean version, Mathlib revision, target count, `#print axioms`, full transcript, and exit codes.
- [ ] If the gate fails, record the exact failure and do not infer a green result.

### Task 3: Correct historical Lean naming and docs

**Files:**
- Modify: `05_lean_formalization/SovereignRegularity.lean`
- Inspect/modify: recovered Paper 17 Lean artifacts only if actually available
- Modify: associated audit/ledger documents

- [ ] Rename or document `sovereign_regularity_theorem` as a projection of `h_controlled`, preserving proof terms in the first corrective commit where feasible.
- [ ] Rename any product called a BKM integral or explicitly state that it is not a time integral.
- [ ] Relabel `navier_stokes_threshold_lyapunov` as arithmetic if recovered.
- [ ] Relabel `tension_divergence : True := trivial` as a tautology or preserve it only with an honest name/docstring.

### Task 4: Source-check the PDE dependencies

**Files:**
- Create: `NAVIER_STOKES_SOURCE_STATEMENTS.md`
- Modify: `NAVIER_STOKES_DEPENDENCY_AUDIT.md`
- Modify: `NAVIER_STOKES_EVIDENCE_LEDGER.md`

- [ ] Quote exact hypotheses and conclusions for Constantin–Fefferman 1993, a genuine 3D NS continuation theorem, and local H^s strong-solution existence.
- [ ] Include domain, solution class, time interval, high-vorticity set, quantifiers, a.e./pointwise conditions, δ, and citations.
- [ ] Compare `AlignmentPredicate K L ρ` to the exact geometric hypothesis and document any mismatch.

### Task 5: Freeze the official target and close/demote Lyapunov route

**Files:**
- Modify: `05_lean_formalization/NavierStokesSpec.lean` if needed
- Modify: `NAVIER_STOKES_COMPLETION.md`
- Modify: `NAVIER_STOKES_LYAPUNOV_AUDIT.md`
- Modify: `NAVIER_STOKES_EVIDENCE_LEDGER.md`

- [ ] State Alternative B as a type/specification only: all smooth divergence-free periodic initial data on R³/Z³, zero force, ν>0, globally smooth periodic solution.
- [ ] Preserve the Paper 17 differential inequality and classify it as unsupported for arbitrary data unless an explicit closing hypothesis is proved.
- [ ] Write the first unproved implication as a precise open theorem, leaving L5 open.

### Task 6: Review, commit, and report actual status

**Files:**
- Modify: PR #53 description/comments
- Modify: issue #54 comment/status
- Modify: Asana only if an enabled connector is available and the operation is authorized

- [ ] Run repository diff review, grep for overclaimed names/phrasing, compute artifact hashes, and rerun the official gate.
- [ ] Commit changes on `research/navier-stokes-scope-remediation`.
- [ ] Update PR #53 and issue #54 with exact build output and limitations.
- [ ] Provide the required final sentence if the Clay hard gate remains unmet.
