#!/usr/bin/env bash
# Res-Nova local verification gate.
#
# This runs the checks that .github/workflows/verify.yml declares.
#
# HISTORICAL NOTE (corrected 2026-09-14): this header previously stated that
# Actions was locked account-wide for billing and never executed. That is no
# longer true -- runs on 2026-09-14 provision a runner and execute steps
# normally. The ~9s "failures" were REAL: the claim-hygiene job was failing on
# the merge result, not being skipped. Do not read a fast failure as a skipped
# one. Run this script locally before pushing either way.
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
step "lean target inventory" python3 05_lean_formalization/check_target_inventory.py
step "lean manuscript inventory" python3 05_lean_formalization/check_manuscript_inventory.py
step "mvpc fixture manifests" python3 scripts/render_mvpc_fixtures.py --check

echo
if [ "$fails" -eq 0 ]; then
  echo "LOCAL GATE: PASS"
else
  echo "LOCAL GATE: FAIL ($fails check(s))"
fi
exit "$fails"
