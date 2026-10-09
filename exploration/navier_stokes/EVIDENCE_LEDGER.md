# Navier–Stokes evidence ledger (2026-10-08)

This supersedes `archive/legacy_root/NAVIER_STOKES_EVIDENCE_LEDGER.md`, which stays as the
dated record. Hashes are sha256 of the files on branch
`research/navier-stokes-remediation-2026-10-08`.

## Lean modules
| module | sha256 | what it proves | vacuity screen (`4Leibniz/scripts/vkernel/vacuity_screen.py` 0.2) |
|---|---|---|---|
| `NavierStokesScope.lean` | `d59f8bf048d3e32e…` | L0: `1 − χ ≤ 3/10` from `χ ≥ 7/10`; the gate is in `(0, 1]` | arithmetic by design |
| `NavierStokesGeometry.lean` | `945aa851fb27d301…` | L1: two unit vectors are at distance ≤ 2 | `norm_sub_le_two_of_norm_eq_one`: PASS |
| `NavierStokesSpec.lean` | `f80d9b8e458bd4d6…` | L2 definitions; `direction_unit`; `alignmentFromGate_eq` | PASS; RING-ID/unfolded (an arithmetic identity, as documented) |
| `NavierStokesTarget.lean` (new) | see the witness header | statement (B) as a `Prop`, with `u` and `p` periodic per the Errata; `AlignmentPersistence`; 4 sanity theorems; L3a (`sin_angle_le_norm_sub`, `alignment_gives_sine_condition`, `alignment_gives_assumptionA_slice`) | `zero_admissible`, `zero_solution`, `growing_constant_field_not_a_solution`, `persistenceObligation_false`: PASS. All three L3a theorems: PASS. Both substitution tests fail to compile: `L/2` in place of `L`, and `1/2 ≤ L·ρ` in place of `1 ≤ L·ρ`. The `simp` helpers `comp_const` and `pd_const` are FIELD-ID, as expected for definitional helpers |
| `SovereignRegularity.lean` | `695b817d7f2aa133…` | consequences of an assumed bound, renamed below | `assumed_vorticity_bound_projection`: PROOF-IS-FIELD. `product_bound_below_threshold` and `pointwise_vorticity_product_bound`: PASS, but they are arithmetic on an assumed field, a known blind spot of the screen |

The screen's calibration is 9/9 known-vacuous statements flagged and 4/4 genuine ones passing
(`4Leibniz/scripts/vkernel/calibration/`). A PASS means none of its patterns fired. It does not
establish non-vacuity.

## `SovereignRegularity.lean` renames (2026-10-08; identifiers and comments only)
| old | new | why |
|---|---|---|
| `sovereign_regularity_theorem` | `assumed_vorticity_bound_projection` | the proof term is `st.h_controlled T hT` |
| `bkm_vorticity_integral_finite` | `pointwise_vorticity_product_bound` | the statement is a product `ω_sup T · T`, not a time integral |
| `bkm_no_blowup` | `product_bound_below_threshold` | arithmetic, not a non-blowup criterion |
| `BKMVorticityState` | `AssumedVorticityBoundState` | no BKM object is defined |
| `SovereignAlignment.lipschitz_xi : True` | `kinematic_placeholder : True` | the field is `True` |

The proof terms are unchanged: after normalizing the renames, the code lines match main,
153/153. The file compiles with `lake env lean SovereignRegularity.lean` (exit 0). Live
references were updated with dated notes:
- `AUDIT_LEAN_INVENTORY.md`;
- `RES_NOVA_VERIFICATION_LEDGER.md` (its "VERIFIED `[P]`" was corrected to `[arith]`);
- `THEORY_ASSUMPTION_AUDIT.md`;
- the manuscript listing.

`VERIFICATION_RUN_*` and `archive/` keep the old names as provenance.

## Paper 17 artifacts
- **Manuscript:** the Lyapunov manuscript (content hash `cf5adbe10008384d…`) is audited in `archive/legacy_root/NAVIER_STOKES_LYAPUNOV_AUDIT.md`.
- **Lean listings:** its embedded listings (`TensionProof.lean`, with `tension_divergence : True := trivial`, and `navier_stokes_threshold_lyapunov`) are **not in this repository**, so there is nothing to rename here.
- **Classification** (from the audit):
  - `tension_divergence` is a tautology;
  - the threshold lemma is arithmetic;
  - the Lyapunov route is unsupported for arbitrary data (`README.md`).

## The 2026-10-08 hand-off package and branch `research/navier-stokes-scope-remediation`
- **The package.** Another agent worked from a sandbox, whose spec path is `/home/ubuntu/upload/…`. Its output arrived as a zip (sha256 `42a3f8a831a311fa…`, 25 files).
- **The commit is real.** It also pushed one commit, `b430e1c3e4381fd98396a0ce9ecc7b70b796498a` (2026-10-08 20:45 UTC), to a re-created `research/navier-stokes-scope-remediation`. That branch's first incarnation merged as PR #53 on 2026-09-14 (`bbc9214`) and was deleted on 2026-10-02.
- **It sits on a stale base.**
  - `b430e1c` is built on `471d35d` (2026-09-14) and is **363 commits behind main**, with no open PR.
  - It edits the old gate inventory, and its "48 / 48" witness covers that inventory, which lacks about 20 modules that main now gates.
  - It re-creates root-level `NAVIER_STOKES_*.md` files that main moved to `archive/legacy_root/` on 2026-10-03/04.
  - Merging it as it stands would conflict with main and reverse that move.
- **Its witness files are consistent.** In the commit, `VERIFICATION_RUN_2026-10-08_FINAL/official_gate_transcript.txt` matches its `SHA256SUMS` (`f9fcb472…`).
- **The zip packed a different transcript.** The zip's `official_gate_transcript.txt` (`6aaa63ec…`) is a different file: the 2026-09-14 run, `VERIFICATION_RUN_2026-09-14_NAVIER_STOKES_03/official_gate_transcript.txt`.
- **This branch supersedes it.** This branch is cut from current main and carries the parts of `b430e1c` and the zip that survive review (table below). The old branch is left in place for RY to delete.

| zip file | decision |
|---|---|
| `lakefile.lean`, `verify_all_proofs.sh` | **not used.** Both predate main and would drop about 20 gated modules. Main's copies were edited instead |
| `SovereignRegularity.lean` | its renames were applied as fresh edits to main's file; the file itself was not copied |
| `NavierStokesScope.lean`, `NavierStokesSpec.lean` | main's kept. The zip's differ only by a stale doc path and a tactic swap |
| `NavierStokesDomain.lean` | not integrated. It uses `AddCircle` quotient types and operator signatures with no derivative semantics, and `NavierStokesTarget` uses unit-periodic Euclidean fields with Fréchet derivatives instead |
| `NavierStokesSpacetimeBridge.lean` | not integrated. Its only theorem returns its hypothesis, and `AlignmentPersistence` states the obligation over genuine solutions |
| `Defs.lean` | not integrated: it is a copy of Mathlib's `Topology/Instances/AddCircle/Defs.lean` |
| `official_gate_transcript.txt` | not used as a witness: it is the 2026-09-14 run, on the stale inventory. This branch has its own run on current main |
| `Navier–Stokes Source Statements and Applicability Audit.md` | verified against the sources and corrected into `SOURCE_STATEMENTS.md` |
| audits, plans and reviews (`Documentation Audit`, `Review of Verified …`, `… Refactor Plan`, `… Completion Boundary`, `… Implementation Plan`) | used as input. The Documentation Audit's comment fixes were applied to `SovereignRegularity.lean` |
| `SKILL.md`, `2026-09-14_…txt`, `Pasted_content_01.txt` | not repository material (a review skill, a session log, the task text) |

## Build witness (final: 2026-10-08 21:05 CDT, this branch, current main base)
`05_lean_formalization/VERIFICATION_RUN_2026-10-08_NAVIER_STOKES/gate_transcript.txt`:

| step | exit | time |
|---|---:|---:|
| `lake exe cache get` | 0 | 15 s |
| `lake build` | 0 | 2 s |
| `bash verify_all_proofs.sh` | 0 | 336 s |

- **Result:** `verified: 67 / 67 target(s)`, `RESULT: PASS`. The OK lines include all five `NavierStokes*` modules.
- **Toolchain:** Lean 4.33.0-rc1 (commit `62eed1db4d67`); Mathlib `5eec30bc56ed5a23be2e27c544a949ba0bceddeb`.
- **State witnessed:** the header records `NavierStokesTarget.lean` sha256 `1b1231fa268c72fa…`, the committed file. No Lean file changed after the run.
- **Earlier runs:** 20:42 and 20:52, both exit 0 and 67/67. They are in the history of `07c3c03` and `9312381`.
- **What the gate certifies:** elaboration, absence of `sorry`, and the standard axiom footprint. It says nothing about what the statements mean.

The assurance checks pass on the same tree:
- `check_target_inventory.py`: 67 targets agree;
- `check_manuscript_inventory.py`;
- `validate_claim_registry.py`: 48 records;
- `check_claim_consistency.py`.
