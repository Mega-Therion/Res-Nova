#!/usr/bin/env bash
# Res-Nova formal proof suite — one-command verification.
#
#   ./verify_all_proofs.sh
#
# Exits 0 only if every module elaborates with no errors, no `sorry`, and no
# axioms beyond Lean's three standard ones (propext, Classical.choice,
# Quot.sound). Any custom `axiom` declaration is a hard failure: the README
# claims "zero custom unproven axioms", and this script is what enforces it.
set -uo pipefail
cd "$(dirname "$0")"

LAKE="${LAKE:-$HOME/.elan/bin/lake}"
STD_AXIOMS='propext|Classical.choice|Quot.sound'
fail=0 ok=0

if [ ! -e .lake/packages/mathlib ]; then
  echo "Mathlib not present. Run:  lake exe cache get" >&2
  exit 2
fi

for f in *.lean; do
  case "$f" in lakefile.lean) continue;; esac
  out="$($LAKE env lean "$f" 2>&1)"

  if grep -q "error:" <<<"$out"; then
    echo "FAIL  $f — elaboration error"
    grep "error:" <<<"$out" | head -3 | sed 's/^/        /'
    fail=1; continue
  fi
  if grep -q "uses 'sorry'" <<<"$out"; then
    echo "FAIL  $f — contains sorry"
    fail=1; continue
  fi
  # `#print axioms` lines list dependencies; anything outside the standard
  # three means an unproven assumption is propping the result up.
  if grep 'depends on axioms' <<<"$out" \
       | grep -oP '(?<=\[).*(?=\])' | tr ',' '\n' | sed 's/ //g' \
       | grep -vE "^($STD_AXIOMS)$" | grep -q .; then
    echo "FAIL  $f — non-standard axiom dependency"
    grep 'depends on axioms' <<<"$out" | sed 's/^/        /'
    fail=1; continue
  fi
  # A bare `axiom` declaration never shows up in #print axioms of other decls.
  if grep -qE '^\s*axiom\s' "$f"; then
    echo "FAIL  $f — declares a custom axiom"
    fail=1; continue
  fi

  echo "OK    $f"
  ok=$((ok+1))
done

echo
echo "verified: $ok module(s)"
[ "$fail" -eq 0 ] && echo "RESULT: PASS" || echo "RESULT: FAIL"
exit "$fail"
