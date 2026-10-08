#!/usr/bin/env bash
# Regenerate the three core Res-Nova result files and prove they match the commit byte for byte.
#   02_galaxy_dynamics/PARAMETER_LEDGER.json    SPARC tier 0 / tier 1 fits   (parameter_ledger.py)
#   02_galaxy_dynamics/EFE_QUADRUPOLE_Q2.json   Cassini external-field Q2    (efe_quadrupole_q2.py)
#   02_galaxy_dynamics/CASSINI_PARETO_SCAN.json shapes that pass Cassini     (cassini_pareto_scan.py)
# Needs: git, bash, python3 with numpy + scipy, network access to astroweb.cwru.edu (SPARC download,
# SHA-256-verified against VERIFICATION_RUN_001's manifest). Measured 2026-10-08: 4 min wall-clock on a laptop.
# Exit 0 = all three files byte-identical to HEAD. Exit 1 = drift (the diff is printed). Exit 2 = refused.
set -euo pipefail
ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$ROOT"
OUTS=(02_galaxy_dynamics/PARAMETER_LEDGER.json 02_galaxy_dynamics/EFE_QUADRUPOLE_Q2.json 02_galaxy_dynamics/CASSINI_PARETO_SCAN.json)
if ! git diff --quiet -- "${OUTS[@]}"; then
  echo "refusing: the result files have local edits; run this on a clean checkout" >&2; exit 2
fi
export SPARC_DATA_DIR="${SPARC_DATA_DIR:-$(mktemp -d)/sparc_data}"
bash 02_galaxy_dynamics/fetch_sparc.sh
( cd 02_galaxy_dynamics && python3 parameter_ledger.py && python3 efe_quadrupole_q2.py && python3 cassini_pareto_scan.py )
if git diff --exit-code --stat -- "${OUTS[@]}"; then
  echo "REPRODUCED: all 3 result files are byte-identical to $(git rev-parse --short HEAD)"
else
  echo "DRIFT: the regenerated files differ from $(git rev-parse --short HEAD) (diff above)" >&2; exit 1
fi
