#!/usr/bin/env bash
# verify_mvpc.sh — Res-Nova MVPC-X Verification Script
# Validates claim manifests & disk artifacts, then runs the MVPC-X judge.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Res-Nova MVPC-X Claim Verification ==="
echo ""
echo "[Step 1/3] Validating claim manifests against disk artifacts..."
python3 scripts/render_mvpc_fixtures.py --check

echo ""
echo "[Step 2/3] Rendering fixture bundle..."
BUNDLE_PATH="${1:-/tmp/res_nova_bundle.json}"
python3 scripts/render_mvpc_fixtures.py --out "$BUNDLE_PATH"

echo ""
echo "[Step 3/3] Executing MVPC-X Claim Consumer judge..."
python3 -m mvpc.claim_consumer --bundle "$BUNDLE_PATH"

echo ""
python3 -m mvpc.claim_consumer --bundle "$BUNDLE_PATH" --json > mvpc_manifests/MVPC_JUDGE_VERDICTS.json
echo "Judge verdicts saved to mvpc_manifests/MVPC_JUDGE_VERDICTS.json"
