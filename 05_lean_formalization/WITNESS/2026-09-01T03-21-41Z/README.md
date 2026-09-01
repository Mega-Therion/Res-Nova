# Verification witness — 2026-09-01T03-21-41Z

Produced by `emit_witness.sh`. Every file here comes from **one** invocation of
`verify_all_proofs.sh`; `MANIFEST.sha256` hashes all of them together, so a
partially-updated witness fails `--check` instead of quietly misleading.

| File | What it is |
|---|---|
| `TRANSCRIPT.txt` | verbatim output of the gate run |
| `EXIT_CODE.txt` | the gate's exit status (0 = pass) |
| `RESULTS.json` | per-target OK/FAIL, parsed from the transcript |
| `SOURCES.sha256` | hashes of the `.lean` sources, lakefile, toolchain and Mathlib pin **as the gate read them** |
| `ENVIRONMENT.txt` | toolchain, Lean/Lake versions, Mathlib revision, repo commit, dirty flag |
| `MANIFEST.sha256` | hashes of every file above |

## Re-verify this witness

```bash
./emit_witness.sh --check WITNESS/2026-09-01T03-21-41Z
```

## Reproduce the run itself

```bash
lake exe cache get     # fetch the pinned Mathlib (minutes, not a rebuild)
./emit_witness.sh      # writes a fresh witness alongside this one
```

Compare `SOURCES.sha256` between the two: identical hashes mean the same
inputs were checked. **Note:** `git_dirty=yes` in `ENVIRONMENT.txt` means
the working tree had uncommitted changes, so `git_commit` alone does not
identify what was verified — `SOURCES.sha256` does.

## What this is not

This is not the build cache. The `.olean` files are machine- and
toolchain-specific and are re-derivable from the pin recorded above; they are
not evidence and are not committed. This directory is.

A PASS certifies elaboration, absence of `sorry`, and a standard axiom
footprint. It does **not** certify that assumptions carried as typeclass or
structure fields are physically justified — see `THEORY_ASSUMPTION_AUDIT.md`.
