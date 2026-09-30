#!/bin/bash
# SessionStart hook for Claude Code on the web.
#
# Makes the repository's gates runnable in a fresh cloud session:
#   - Python deps for scripts/local_gate.sh and the physics witnesses (pinned
#     in requirements.txt; the gate diffs witness receipts byte-for-byte).
#   - elan + the pinned Lean toolchain from 05_lean_formalization/lean-toolchain.
#   - The Mathlib build cache (~8 GB), so `verify_all_proofs.sh` -- the only
#     definition of done in CLAUDE.md -- can run without a 30-minute rebuild.
#     The container is snapshotted after this hook, so the download is paid once.
#     Set RES_NOVA_SKIP_MATHLIB=1 in the environment to skip it.
#
# Idempotent: every step no-ops when its target is already present.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$ROOT"

echo "[session-start] python deps"
# A dedicated venv: the image's Debian-managed PyYAML cannot be replaced by pip.
VENV="$HOME/.venvs/res-nova"
[ -x "$VENV/bin/python3" ] || python3 -m venv "$VENV"
"$VENV/bin/python3" -m pip install --quiet --disable-pip-version-check -r requirements.txt
export PATH="$VENV/bin:$PATH"
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$VENV/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi

echo "[session-start] lean toolchain"
if ! command -v elan >/dev/null 2>&1 && [ ! -x "$HOME/.elan/bin/elan" ]; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --default-toolchain none >/dev/null
fi
export PATH="$HOME/.elan/bin:$PATH"
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export PATH="$HOME/.elan/bin:$PATH"' >> "$CLAUDE_ENV_FILE"
fi
# Reading the pinned toolchain installs it if missing.
(cd 05_lean_formalization && lean --version)

if [ "${RES_NOVA_SKIP_MATHLIB:-}" = "1" ]; then
  echo "[session-start] RES_NOVA_SKIP_MATHLIB=1: skipping Mathlib cache"
else
  echo "[session-start] Mathlib cache (no-op when already present)"
  (cd 05_lean_formalization && lake exe cache get >/dev/null)
fi

echo "[session-start] done"
