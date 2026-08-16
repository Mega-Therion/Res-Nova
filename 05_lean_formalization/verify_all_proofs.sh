#!/usr/bin/env bash
# Res-Nova formal proof suite — one-command verification.
#
#   ./verify_all_proofs.sh
#
# Exits 0 only if every declared target elaborates with a zero exit status, no
# `sorry`, and no axioms beyond Lean's three standard ones (propext,
# Classical.choice, Quot.sound).
#
# Success criterion (revised 2026-08-16):
#   * The target list is EXPLICIT and is cross-checked against `lakefile.lean`
#     roots, so a new .lean file cannot silently join or leave the gate.
#   * Lean's actual per-target exit status is authoritative. Previously the gate
#     grepped stdout for "error:", which both misses non-zero exits that print no
#     such line and fires on the substring appearing in unrelated output.
#   * `grep '^axiom '` is retained but is NOT treated as sufficient. Assumptions
#     in this suite are carried as typeclass fields, structure fields, and
#     theorem hypotheses, which that grep cannot see. See THEORY_ASSUMPTION_AUDIT.md.
#     Do not describe a green run here as "zero unproven assumptions".
#
# Last recorded green run: all 17 targets, exit 0, on commit 109d38b under
# Lean v4.33.0-rc1 and Mathlib 5eec30bc. Transcript, per-target exit codes and
# checksums: VERIFICATION_RUN_003/01_lean/.
#
# That run used a Mathlib checkout that was already present in .lake/packages.
# Reproducing it on a machine with no pre-existing Mathlib (`lake exe cache
# get` from a fresh clone) is open problem O6 and is not claimed here.
set -uo pipefail
cd "$(dirname "$0")"

LAKE="${LAKE:-$HOME/.elan/bin/lake}"
STD_AXIOMS='propext|Classical.choice|Quot.sound'

# Explicit target list. Must equal the `roots` in lakefile.lean.
TARGETS=(
  AXIOMS_V2.lean
  CosmologicalSector.lean
  CovariantCompletion.lean
  DeSitterExtremal.lean
  DualChannelDerivation.lean
  GODActionKinematics.lean
  ITActionClosure.lean
  MuProjection.lean
  PPNLimits.lean
  PrintAxioms.lean
  PrintAxiomsD8.lean
  RelativisticStability.lean
  SOCasimirGenuine.lean
  SkordisZlosnikEmbedding.lean
  SovereignRegularity.lean
  TensorSpeed.lean
  YettParadigm.lean
)

if [ ! -e .lake/packages/mathlib ]; then
  echo "Mathlib not present. Run:  lake exe cache get" >&2
  echo "(A fresh-clone fetch has not been walked; see open problem O6.)" >&2
  exit 2
fi

# --- target list integrity -------------------------------------------------
# Drift between this list, the lakefile roots, and the files on disk is itself a
# gate failure: it is how five phantom modules survived in the manuscript.
declare -i drift=0
for f in *.lean; do
  case "$f" in lakefile.lean) continue;; esac
  printf '%s\n' "${TARGETS[@]}" | grep -qx "$f" || { echo "DRIFT $f on disk but not a declared target"; drift=1; }
done
for t in "${TARGETS[@]}"; do
  [ -f "$t" ] || { echo "DRIFT $t declared as target but absent from disk"; drift=1; }
  grep -q "\`${t%.lean}\b" lakefile.lean || { echo "DRIFT $t not among lakefile.lean roots"; drift=1; }
done
if [ "$drift" -ne 0 ]; then
  echo; echo "RESULT: FAIL (target list drift — fix before trusting any result)"; exit 1
fi

# Dependencies must exist as oleans before per-file elaboration: PrintAxioms.lean
# imports CovariantCompletion.
echo "building library (required for cross-module imports)…"
if ! "$LAKE" build; then
  echo "FAIL  lake build returned non-zero; per-target results would be unreliable"
  echo; echo "RESULT: FAIL"; exit 1
fi

declare -i fail=0 ok=0
for f in "${TARGETS[@]}"; do
  out="$("$LAKE" env lean "$f" 2>&1)"
  status=$?                      # authoritative: Lean's own exit status

  if [ "$status" -ne 0 ]; then
    echo "FAIL  $f — lean exited $status"
    grep -i "error" <<<"$out" | head -3 | sed 's/^/        /'
    fail=1; continue
  fi
  if grep -q "uses 'sorry'" <<<"$out"; then
    echo "FAIL  $f — contains sorry"
    fail=1; continue
  fi
  # `#print axioms` lines list dependencies; anything outside the standard three
  # means an unproven assumption is propping the result up. Note that a file with
  # no `#print axioms` line passes this check trivially.
  if grep 'depends on axioms' <<<"$out" \
       | grep -oP '(?<=\[).*(?=\])' | tr ',' '\n' | sed 's/ //g' \
       | grep -vE "^($STD_AXIOMS)$" | grep -q .; then
    echo "FAIL  $f — non-standard axiom dependency"
    grep 'depends on axioms' <<<"$out" | sed 's/^/        /'
    fail=1; continue
  fi
  if grep -qE '^\s*axiom\s' "$f"; then
    echo "FAIL  $f — declares a custom axiom"
    fail=1; continue
  fi

  echo "OK    $f"
  ok=$((ok+1))
done

echo
echo "verified: $ok / ${#TARGETS[@]} target(s)"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS"
  echo "NOTE: this certifies elaboration, absence of sorry, and a standard axiom"
  echo "      footprint. It does not certify that assumptions carried as typeclass"
  echo "      or structure fields are physically justified — see THEORY_ASSUMPTION_AUDIT.md."
else
  echo "RESULT: FAIL"
fi
exit "$fail"
