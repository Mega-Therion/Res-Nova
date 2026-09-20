# COUNTS — the canonical census

Every recurring numeric count in this corpus, with the scope it belongs to and the
command that measures it. **A count without its scope is not a fact.** Most of the
contradiction-log entries closed in September 2026 were not wrong numbers; they were
correct numbers quoted against the wrong scope.

Rules:

1. Never harmonize two counts into one without checking this table first. Several
   pairs below are *both* current and *must* differ.
2. Quote the command, not the number, when you need to be sure.
3. Numbers inside a `Verbatim output` block are historical records of a run. They are
   never edited to match this table; a dated scope note is added instead.

Last measured: 2026-09-20, commit `726820f`.

---

## Lean modules — two scopes, both current

| Count | Scope | Command |
|---|---|---|
| **28** | **Manuscript scope.** Modules cited by the manuscript = gate scope minus `05_lean_formalization/ADJACENT_MODULES.txt`. This is the number quoted in `reproducibility_appendix.tex`. | `python3 05_lean_formalization/check_manuscript_inventory.py` |
| **59** | **Gate scope.** Every module built and checked: lakefile roots ≡ `verify_all_proofs.sh` TARGETS ≡ on-disk. | `python3 05_lean_formalization/check_target_inventory.py` |

A module in `ADJACENT_MODULES.txt` is scoped **out of the manuscript, never out of the
gate** (`CLAUDE.md`). So 28 < 59 is the correct, invariant-enforced relationship.

`check_manuscript_inventory.py` fails closed if `reproducibility_appendix.tex` is edited
away from 28 — this was tested on 2026-09-20 by setting it to 58, which produced
`RESULT: FAIL`; restoring 28 produced `RESULT: PASS`. Do not "fix" the 28.

## SPARC sample — three scopes

| Count | Scope | Command / artifact |
|---|---|---|
| **175** (3,391 points) | **Full catalogue, live.** The frozen harness sample. All current a₀ extractions (T1) use this. | `02_galaxy_dynamics/A0_REEXTRACTION_3MU_2026-09-16.json` → `n_galaxies` |
| **78** | **T3 non-flow subset.** Galaxies whose SPARC distance is *not* Hubble-flow-derived; used to test ladder covariance. | `02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json` |
| **171** (3,375 points) | **SUPERSEDED pre-audit extraction sample** (2026-08-15). Retained for provenance only. Do not quote as current. | `02_galaxy_dynamics/A0_MEASUREMENT.json` → `n_galaxies`, and its own `status` field |

97 of the 175 carry Hubble-flow distances assuming H₀ = 73, which is why the
a₀ → H₀ inversion is ladder-covariant rather than independent.

## Build and test counts — measured, not invariant

| Count | Scope | Command |
|---|---|---|
| **3,404 jobs** | Lean build jobs in the pre-push ratchet, last green run 2026-09-20. **Not an invariant**: this number moves with the Mathlib cache state and with any module added, so it is a record of one run, not a target. | `bash Codebase/Scripts_and_Tools/verify_ratchet.sh` (runs on pre-push) |
| **85 tests** | Rust unit + property tests in the ratchet: 7 sandbox rollback + 34 spokes AST + 44 Aegis policy/proptest. | same run, section `[2/3]` |

## Gate checks

| Count | Scope | Command |
|---|---|---|
| **16** | `PASS` lines emitted by the fast local gate (seconds, no Mathlib). | `bash scripts/local_gate.sh` |

---

## Scope collisions already found and closed

- `reproducibility_appendix.tex` **28** vs gate **59** — both correct, differ by
  `ADJACENT_MODULES.txt`. Closed 2026-09-20 (C-09).
- `FIG_TREE_ASSET_LEDGER.md` quotes "lakefile roots (28 modules)" as the *gate* scope
  inside captured output from a historical run. Transcript left unedited; dated scope
  note added above it. Closed 2026-09-20 (C-09).
- a₀ **1.1163e-10** (171-galaxy, pre-audit, μ_dual) vs **1.1607e-10** (175-galaxy, T1,
  μ_std) — these differ by sample *and* distance treatment *and* closure, so their
  ratio is **not** the μ effect. See `docs/A0_CLOSURE_EVOLUTION.md`. Closed 2026-09-20 (C-14).
