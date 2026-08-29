#!/usr/bin/env bash
# Res-Nova local verification gate.
#
# This runs the checks that .github/workflows/verify.yml declares. Those have
# NOT been running: GitHub Actions is locked account-wide ("your account is
# locked due to a billing issue"), so every push since has reported failure in
# ~3 seconds without executing a single step. Two real regressions reached main
# behind that silence. Until Actions runs again, this script is the gate.
#
# Lean kernel verification is deliberately NOT here — it is a release gate
# (Mathlib is multi-GB), same as the workflow says. Run
# 05_lean_formalization/verify_all_proofs.sh for that.
set -uo pipefail
cd "$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/.." && pwd)"

fails=0
step() {
  local name="$1"; shift
  printf '%-34s ' "$name"
  if out="$("$@" 2>&1)"; then
    echo "PASS"
  else
    echo "FAIL"
    printf '%s\n' "$out" | sed 's/^/    /'
    fails=$((fails + 1))
  fi
}

step "py_compile" bash -c 'python3 -m py_compile 02_galaxy_dynamics/*.py scripts/check_claim_consistency.py 05_lean_formalization/check_manuscript_inventory.py scripts/render_mvpc_fixtures.py scripts/run_mvpc_adapter.py 03_observer_jwst/gate2_inference.py'
step "claim consistency" python3 scripts/check_claim_consistency.py
step "gate2 inference self-test" python3 03_observer_jwst/gate2_inference.py --self-test
step "lean manuscript inventory" python3 05_lean_formalization/check_manuscript_inventory.py
step "mvpc fixture manifests" python3 scripts/render_mvpc_fixtures.py --check

echo
if [ "$fails" -eq 0 ]; then
  echo "LOCAL GATE: PASS"
else
  echo "LOCAL GATE: FAIL ($fails check(s))"
fi
exit "$fails"
