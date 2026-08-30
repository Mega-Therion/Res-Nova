#!/usr/bin/env bash
# Emit a dated, self-hashing witness for a run of verify_all_proofs.sh.
#
#   ./emit_witness.sh              # run the gate, write WITNESS/<UTC-date>/
#   ./emit_witness.sh --check DIR  # re-verify an existing witness
#
# WHY THIS EXISTS
# ---------------
# VERIFICATION_RUN_003/01_lean/SHA256SUMS.txt failed its own check on
# 2026-08-29: the manifest was frozen on 08-20 while GATE_TRANSCRIPT.txt was
# regenerated on 08-23. The witness had drifted from the run it witnessed, and
# nothing detected that for nine days.
#
# The fix is that the transcript and the manifest are produced by the SAME
# invocation and the manifest covers every other file in the directory. A
# witness can no longer be half-updated: change anything and --check fails.
#
# WHAT A WITNESS IS
# -----------------
# It is the evidence that a verification RAN and what it said — the script, its
# output, the exact inputs, and hashes binding them together. It is NOT the
# build cache. The .olean files are 9 GB of machine- and toolchain-specific
# scratch that prove nothing; this directory is a few hundred KB and proves
# what was actually checked. Anyone can re-derive the oleans from the pinned
# toolchain and manifest recorded here.
set -uo pipefail
cd "$(dirname "$0")"

LAKE="${LAKE:-$HOME/.elan/bin/lake}"
MANIFEST=MANIFEST.sha256

# ---------------------------------------------------------------- --check ---
if [ "${1:-}" = "--check" ]; then
  dir="${2:?usage: $0 --check WITNESS_DIR}"
  [ -f "$dir/$MANIFEST" ] || { echo "no $MANIFEST in $dir" >&2; exit 2; }
  ( cd "$dir" && sha256sum -c "$MANIFEST" --quiet ) || {
    echo "WITNESS INVALID: $dir has drifted from the run it records." >&2
    exit 1
  }
  # The manifest must also be complete: a file added later but never hashed
  # would otherwise pass silently.
  listed=$(cut -c 67- "$dir/$MANIFEST" | sed 's|^\./||' | sort)
  present=$(cd "$dir" && find . -type f ! -name "$MANIFEST" | sed 's|^\./||' | sort)
  if [ "$listed" != "$present" ]; then
    echo "WITNESS INVALID: $dir contains files the manifest does not cover:" >&2
    comm -13 <(printf '%s\n' "$listed") <(printf '%s\n' "$present") | sed 's/^/  +/' >&2
    comm -23 <(printf '%s\n' "$listed") <(printf '%s\n' "$present") | sed 's/^/  -/' >&2
    exit 1
  fi
  echo "WITNESS VALID: $dir ($(printf '%s\n' "$present" | wc -l) files, all hashes match)"
  exit 0
fi

# ------------------------------------------------------------------- emit ---
STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
OUT="${1:-WITNESS/$STAMP}"
mkdir -p "$OUT" || exit 2

echo "[witness] $OUT"

# 1. Environment — everything needed to reproduce, nothing identifying.
{
  echo "utc                 $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "lean_toolchain      $(cat lean-toolchain 2>/dev/null || echo unknown)"
  echo "lake_version        $("$LAKE" --version 2>/dev/null | head -1)"
  echo "lean_version        $("$LAKE" env lean --version 2>/dev/null | head -1)"
  echo "mathlib_rev         $(python3 -c "
import json,sys
try:
    d=json.load(open('lake-manifest.json'))
    print([p['rev'] for p in d['packages'] if p['name']=='mathlib'][0])
except Exception: print('unknown')" 2>/dev/null)"
  echo "git_commit          $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "git_dirty           $(if [ -n "$(git status --porcelain 2>/dev/null)" ]; then echo yes; else echo no; fi)"
} > "$OUT/ENVIRONMENT.txt"

# 2. Hash the inputs the gate reads, BEFORE running it.
sha256sum lakefile.lean lean-toolchain lake-manifest.json *.lean 2>/dev/null \
  | sort -k2 > "$OUT/SOURCES.sha256"

# 3. Run the gate, capturing exactly what it printed. The transcript and the
#    hashes below therefore describe one and the same invocation.
set -o pipefail
./verify_all_proofs.sh 2>&1 | tee "$OUT/TRANSCRIPT.txt"
rc=${PIPESTATUS[0]}
echo "$rc" > "$OUT/EXIT_CODE.txt"

# 4. Machine-readable summary.
python3 - "$OUT" "$rc" <<'PY'
import json, os, re, sys
out, rc = sys.argv[1], int(sys.argv[2])
lines = open(os.path.join(out, "TRANSCRIPT.txt")).read().splitlines()
targets = {}
for ln in lines:
    m = re.match(r'^(OK|FAIL)\s+(\S+\.lean)', ln)
    if m:
        targets[m.group(2)] = m.group(1)
verdict = next((ln.split(":", 1)[1].strip() for ln in lines
                if ln.startswith("RESULT:")), "UNKNOWN")
json.dump({
    "exit_code": rc,
    "result": verdict,
    "targets_total": len(targets),
    "targets_ok": sum(1 for v in targets.values() if v == "OK"),
    "targets": targets,
}, open(os.path.join(out, "RESULTS.json"), "w"), indent=2, sort_keys=True)
PY

# 5. README, so the directory explains itself to whoever finds it.
cat > "$OUT/README.md" <<MD
# Verification witness — $STAMP

Produced by \`emit_witness.sh\`. Every file here comes from **one** invocation of
\`verify_all_proofs.sh\`; \`$MANIFEST\` hashes all of them together, so a
partially-updated witness fails \`--check\` instead of quietly misleading.

| File | What it is |
|---|---|
| \`TRANSCRIPT.txt\` | verbatim output of the gate run |
| \`EXIT_CODE.txt\` | the gate's exit status (0 = pass) |
| \`RESULTS.json\` | per-target OK/FAIL, parsed from the transcript |
| \`SOURCES.sha256\` | hashes of the \`.lean\` sources, lakefile, toolchain and Mathlib pin **as the gate read them** |
| \`ENVIRONMENT.txt\` | toolchain, Lean/Lake versions, Mathlib revision, repo commit, dirty flag |
| \`$MANIFEST\` | hashes of every file above |

## Re-verify this witness

\`\`\`bash
./emit_witness.sh --check $OUT
\`\`\`

## Reproduce the run itself

\`\`\`bash
lake exe cache get     # fetch the pinned Mathlib (minutes, not a rebuild)
./emit_witness.sh      # writes a fresh witness alongside this one
\`\`\`

Compare \`SOURCES.sha256\` between the two: identical hashes mean the same
inputs were checked. **Note:** \`git_dirty=yes\` in \`ENVIRONMENT.txt\` means
the working tree had uncommitted changes, so \`git_commit\` alone does not
identify what was verified — \`SOURCES.sha256\` does.

## What this is not

This is not the build cache. The \`.olean\` files are machine- and
toolchain-specific and are re-derivable from the pin recorded above; they are
not evidence and are not committed. This directory is.

A PASS certifies elaboration, absence of \`sorry\`, and a standard axiom
footprint. It does **not** certify that assumptions carried as typeclass or
structure fields are physically justified — see \`THEORY_ASSUMPTION_AUDIT.md\`.
MD

# 6. Seal. Hash everything except the manifest itself.
( cd "$OUT" && find . -type f ! -name "$MANIFEST" | sed 's|^\./||' | sort \
    | xargs sha256sum > "$MANIFEST" )

echo
echo "[witness] sealed: $OUT"
echo "[witness] gate exit code: $rc"
( cd "$OUT" && sha256sum -c "$MANIFEST" --quiet ) \
  && echo "[witness] self-check OK" \
  || { echo "[witness] SELF-CHECK FAILED" >&2; exit 2; }
exit "$rc"
