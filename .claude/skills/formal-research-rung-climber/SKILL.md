---
name: formal-research-rung-climber
description: Evidence-first workflow for advancing a mathematical or theoretical-physics repository through machine-checked research rungs. Use when resuming another agent’s handoff, auditing a claimed theorem or PR, extending Lean/Coq/Isabelle formalization, synchronizing proof gates, or committing and pushing verified research progress.
---

# Formal Research Rung Climber

Use this skill to turn an informal research handoff into a reproducible, machine-checked sequence of narrowly scoped advances. Treat every claimed rung as a hypothesis about repository state until independently verified.

## Operating principles

1. **Verify before extending.** Confirm the repository, branch, commit, PR, CI status, target inventory, and stated theorem boundary from the actual remote and local checkout.
2. **Preserve epistemic labels.** Separate proved algebra or formal facts `[P]` from classical imported facts `[C]`, open questions `[O]`, and physical or interpretive claims `[I]`. Never upgrade an `[O]` or `[I]` claim merely because a nearby algebraic theorem compiled.
3. **Use the repository’s pinned environment.** Read `lean-toolchain`, lockfiles, build instructions, target manifests, and verifier scripts. Recreate the declared compiler/dependency environment rather than using an arbitrary global toolchain.
4. **Make the smallest defensible rung.** Prefer one exact definition plus its direct consequences over a broad “envelope” theorem. State explicitly what the rung does not prove.
5. **Compile in isolation, then integrate.** Create the new module, compile it independently, repair errors from actual diagnostics, add it exactly once to every target manifest, then run the complete gate.
6. **Never hide unfinished work.** Keep scratch files and failed drafts outside the commit, or delete them before publishing. Do not use `sorry`, unchecked axioms, generated tables, or unverifiable numerical claims to force a pass.
7. **Preserve provenance.** Update the repository’s module ledger/status note with the exact theorem boundary, verification command, target count, and remaining open ladder.
8. **Commit only verified work.** Run whitespace checks, target-inventory checks, the explicit proof gate, and the full build before committing. Push only after the working tree and branch state are understood.

## Standard workflow

### 1. Establish the handoff baseline

Identify the selected repository with `gh`, fetch the referenced branch/commit, and inspect the PR and checks. Record the findings before proceeding. Clone or reset to the exact verified handoff point; do not assume the previous agent’s summary is accurate.

Inspect, at minimum:

- `git status`, branch, commit, and remote tracking state;
- PR title, merge state, changed files, and CI checks;
- toolchain pin, dependency lock/cache, build instructions, and proof verifier;
- module ledger, claim ledger, referee note, and current target inventory.

Run the repository’s own inventory and gate before changing source. If a dependency cache is missing, install only the pinned environment and use official sources. Do not execute untrusted repository scripts without reviewing them first.

### 2. Translate the next rung into a theorem boundary

Write a short design note before coding. Specify:

| Field | Required content |
| --- | --- |
| Name | Stable module and theorem names |
| Input | Existing definitions and imported facts |
| Proved output | Exact definitions, equations, homomorphism, injectivity, closure, or cardinality result |
| Evidence class | `[P]`, `[C]`, `[O]`, or `[I]` |
| Non-claims | Topology, continuity, physics, empirical fit, or other boundaries not established |
| Gate | Exact compilation and verification commands |

For finite-to-continuous programs, use this ladder unless the repository dictates a better one:

1. finite algebraic census and action;
2. finite cover or quaternionic realization;
3. explicit matrix representation;
4. named matrix-level carrier with closure and identity;
5. inverse, injectivity, and finite-image faithfulness;
6. finite subgroup/cardinality identification;
7. topology and continuity of the carrier;
8. connected/Lie-group structure and generated Lie algebra;
9. only then, separately assess physical gauge interpretation.

Do not call a finite subgroup the full continuous group. Do not call a matrix representation a physical gauge field.

### 3. Implement incrementally

Create one focused module. Reuse existing conventions instead of duplicating structures. Prefer direct componentwise proofs when the repository intentionally uses a small pure-coordinate model; use stable library lemmas for matrix products, conjugate transpose, determinant, finite sums, and complex projections.

When Lean elaboration behaves unexpectedly:

- inspect the exact pinned library source or declarations;
- compile the edited module directly for fast diagnostics;
- rebuild the Lake/library target when downstream modules need newly added declarations, because direct file compilation may not refresh imported `.olean` artifacts;
- use a local heartbeat increase only for an explicit finite proof, and document why;
- never treat a timeout as a theorem failure or a theorem success.

For finite injectivity, prefer exact constructor cases or a derived structural proof. If exhaustive cases are necessary, normalize scalar components rather than asking tactics to compare opaque structures wholesale.

### 4. Integrate and verify

Add the module exactly once to the Lake roots and the explicit verifier list. Run:

```bash
python3 check_target_inventory.py
bash ./verify_all_proofs.sh
lake build <declared-library-target>
```

Capture the target count and final result. Read the verifier note carefully: a clean Lean gate generally certifies elaboration, absence of `sorry`, and an axiom footprint, not physical justification of assumptions carried in structures or typeclasses.

Check:

- no unexpected files or generated artifacts;
- no whitespace errors (`git diff --check`);
- no accidental claim upgrades in ledgers or manuscripts;
- status documentation agrees with the compiled theorem;
- the clean-clone/rebuild path remains understandable.

### 5. Publish responsibly

Update the module ledger and durable status note with:

- rung number and module name;
- exact proved statements;
- target count and build result;
- imported dependencies and axiom caveat;
- explicit non-claims;
- the next honest rung.

Review the diff, commit with a precise message, fetch the remote branch, and push. If a PR is appropriate, provide its URL but do not merge without the user’s authorization unless explicitly requested. Leave scratch diagnostics, temporary check modules, and failed drafts uncommitted.

## Failure handling

If a proof attempt fails, preserve the diagnostic, classify the failure, and choose one of three paths:

- **Surface/API issue:** inspect the pinned declaration and repair the proof.
- **Computational issue:** reduce the case split, increase a local resource limit, or rebuild the dependency cache.
- **Mathematical boundary issue:** narrow the rung and record the obstruction as `[O]`; do not force a theorem.

After three unsuccessful attempts at the same approach, switch strategy or report the blocker. A passing compile after an unverified shortcut is not acceptable evidence.

## Completion report

Deliver a concise report with the repository/branch, commit and PR links, verified rung(s), exact gate results, known caveats, and remaining ladder. Attach the key new modules and status/ledger files. Use language such as “the formal corpus proves” rather than “physics is established” unless the latter has independent evidence.
