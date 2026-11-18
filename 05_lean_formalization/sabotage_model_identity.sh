#!/usr/bin/env bash
# Sabotage gate for ModelIdentity.lean (closure step 1 / step 7 spine).
#
#   ./sabotage_model_identity.sh
#
# For each load-bearing field of `canonical : ModelIdentity`, copy the Lean project to a
# throwaway directory, change that one field, and require that ModelIdentity.lean or
# ModelIdentityBindings.lean stops compiling. A mutation that still compiles means the
# binding does not depend on the field: the gate FAILS.
#
# Run AFTER `lake build` (verify_all_proofs.sh does that), so the throwaway copy starts
# from current oleans and only rebuilds ModelIdentity and its dependents.
set -uo pipefail
cd "$(dirname "$0")"
LAKE="${LAKE:-$HOME/.elan/bin/lake}"

# field label | exact original line | mutated line
MUTATIONS=(
  "generationTarget 3->4|  generationTarget := .fixed 3 .E|  generationTarget := .fixed 4 .E"
  "interpolation muStd->muSimple|  interpolation := .fixed .muStd|  interpolation := .fixed .muSimple"
  "matterCoupling minimal->disformal|  matterCoupling := .minimal|  matterCoupling := .disformal"
  "aetherNorm -1->+1|  aetherNorm := -1|  aetherNorm := 1"
  "spacetimeDim 4->5|  spacetimeDim := 4|  spacetimeDim := 5"
  "a0 1.1607->2.0|  a0 := .fixed ⟨11607 / 10000, -10|  a0 := .fixed ⟨2, -10"
  "irreducibleParameters drop mu choice|  irreducibleParameters := [.a0Scale, .interpolationChoice]|  irreducibleParameters := [.a0Scale]"
  "internalSpaceX open->fixed guess|  internalSpaceX := .open|  internalSpaceX := .fixed \"CP2\" .conj .novel \"guess\" -- .open"
)

[ -e .lake/packages/mathlib ] || { echo "Mathlib not present (lake exe cache get)"; exit 2; }
[ -e .lake/build/lib/lean/ModelIdentityBindings.olean ] || {
  echo "Build ModelIdentityBindings first (lake build)"; exit 2; }

tmp=$(mktemp -d "${TMPDIR:-/tmp}/sabotage_modelid.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

fail=0
for m in "${MUTATIONS[@]}"; do
  IFS='|' read -r label orig mutated <<<"$m"
  work="$tmp/w"
  rm -rf "$work"; mkdir -p "$work/.lake"
  # Sources and build are copied; Mathlib is shared read-only via a symlink.
  find . -maxdepth 1 -type f \( -name '*.lean' -o -name 'lake-manifest.json' -o -name 'lean-toolchain' \) \
    -exec cp {} "$work/" \;
  cp -r .lake/build "$work/.lake/build"
  ln -s "$(readlink -f .lake/packages)" "$work/.lake/packages"

  python3 - "$work/ModelIdentity.lean" "$orig" "$mutated" <<'PY' || { echo "SETUP-FAIL  $label (pattern not found once)"; fail=1; continue; }
import sys
path, orig, new = sys.argv[1:4]
text = open(path, encoding="utf-8").read()
if text.count(orig) != 1:
    sys.exit(1)
open(path, "w", encoding="utf-8").write(text.replace(orig, new, 1))
PY

  out=$(cd "$work" && "$LAKE" build ModelIdentityBindings 2>&1)
  status=$?
  if [ "$status" -ne 0 ]; then
    first=$(grep -m1 -E "error" <<<"$out" | sed 's/^ *//' | cut -c1-140)
    echo "BREAKS      $label  ->  $first"
  else
    echo "STILL-GREEN $label  (binding does not depend on this field)"
    fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  echo; echo "RESULT: FAIL (a ModelIdentity field is not load-bearing)"; exit 1
fi
echo; echo "RESULT: PASS (${#MUTATIONS[@]}/${#MUTATIONS[@]} mutations break the build)"
