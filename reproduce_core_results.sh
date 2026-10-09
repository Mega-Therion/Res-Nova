#!/usr/bin/env bash
# Regenerate the core result files from the official SPARC data and check them against the commit.
#
#   ./reproduce_core_results.sh
#
# 1. Fetches the 175 SPARC rotmod files and the master table from CWRU and verifies them by SHA-256
#    (fetch_sparc.sh).
# 2. Reruns every script whose output is cited as a headline number.
# 3. Requires the regenerated files to be byte-identical to the commit. The one exception is the a0
#    bootstrap file, whose percentiles move in the last floating-point digit across numpy builds;
#    it is compared to a relative tolerance of 1e-12 and then restored.
# 4. Re-checks that the generated benchmark tables in the manuscripts match the regenerated files.
# Offline: set SPARC_DATA_DIR to a directory that already holds the SPARC files, and SPARC_OFFLINE=1.
# fetch_sparc.sh then verifies them against their pinned SHA-256 and downloads nothing, so the whole run
# needs no network.
# Extended 2026-10-09: until then only the first three files below were covered, so the strict
# SPARC check, the a0 headline, the Lambda_SC range and the generated tables were not reproduced
# by this script.
set -euo pipefail
ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$ROOT"
OUTS=(02_galaxy_dynamics/PARAMETER_LEDGER.json 02_galaxy_dynamics/EFE_QUADRUPOLE_Q2.json 02_galaxy_dynamics/CASSINI_PARETO_SCAN.json
      02_galaxy_dynamics/SPARC_175_summary.json 02_galaxy_dynamics/SPARC_175_GOD_fits.csv
      02_galaxy_dynamics/LAMBDA_SC_UNSCREENED.json 02_galaxy_dynamics/LAMBDA_S_AT_LIVE_A0_2026-10-09.txt)
A0=02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json
if ! git diff --quiet -- "${OUTS[@]}" "$A0"; then
  echo "refusing: the result files have local edits; run this on a clean checkout" >&2; exit 2
fi
export SPARC_DATA_DIR="${SPARC_DATA_DIR:-$(mktemp -d)/sparc_data}"
bash 02_galaxy_dynamics/fetch_sparc.sh
( cd 02_galaxy_dynamics && python3 parameter_ledger.py && python3 efe_quadrupole_q2.py && python3 cassini_pareto_scan.py \
    && python3 sparc_reproduce.py && python3 lambda_sc_unscreened.py \
    && python3 lambda_s_solar_system_check.py --a0 1.1607e-10 > LAMBDA_S_AT_LIVE_A0_2026-10-09.txt )
COMMITTED_A0="$(mktemp)"; git show "HEAD:$A0" > "$COMMITTED_A0"
python3 scripts/a0_distance_corrected_reextract.py
a0_rc=0
python3 - "$COMMITTED_A0" "$A0" <<'PY' || a0_rc=$?
import json, math, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
bad = []
def walk(x, y, path):
    if isinstance(x, dict) and isinstance(y, dict):
        if set(x) != set(y):
            bad.append(f"{path}: keys {sorted(set(x) ^ set(y))}")
        for k in set(x) & set(y):
            walk(x[k], y[k], f"{path}.{k}")
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (u, v) in enumerate(zip(x, y)):
            walk(u, v, f"{path}[{i}]")
    elif isinstance(x, float) or isinstance(y, float):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and math.isclose(x, y, rel_tol=1e-12, abs_tol=0.0)):
            bad.append(f"{path}: {x!r} vs {y!r}")
    elif x != y:
        bad.append(f"{path}: {x!r} vs {y!r}")
walk(a, b, "$")
for line in bad[:20]:
    print("  differs:", line)
sys.exit(1 if bad else 0)
PY
git checkout -q -- "$A0"
python3 scripts/sparc_benchmark_tables.py --check
if git diff --exit-code --stat -- "${OUTS[@]}" && [ "$a0_rc" -eq 0 ]; then
  echo "REPRODUCED: ${#OUTS[@]} result files byte-identical and the a0 file equal to 1e-12, at $(git rev-parse --short HEAD)"
else
  echo "DRIFT: regenerated results differ from $(git rev-parse --short HEAD) (see above)" >&2; exit 1
fi
