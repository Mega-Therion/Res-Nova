#!/usr/bin/env bash
# Regenerate the core result files from the official SPARC data and check them against the commit.
#
#   ./reproduce_core_results.sh
#
# 1. Fetches the 175 SPARC rotmod files and the master table from CWRU and verifies them by SHA-256
#    (fetch_sparc.sh).
# 2. Reruns every script whose output is cited as a headline number.
# 3. Compares the regenerated files with the commit. Five must be byte-identical. Three are optimizer or
#    bootstrap outputs; they are compared numerically, field by field, to a relative tolerance, and then
#    restored:
#      A0_DISTANCE_CORRECTED_2026-09-16.json   1e-12  bootstrap percentiles move in the last digit across
#                                                     numpy builds
#      EFE_QUADRUPOLE_Q2.json,                 1e-8   L-BFGS-B stops once the relative decrease of chi^2
#      CASSINI_PARETO_SCAN.json                       falls below ftol = 2.2e-9 (scipy's default), so two runs
#                                                     whose floating-point summation order differs (another
#                                                     BLAS thread count, another CPU) can stop a few ftol
#                                                     apart. Measured 2026-10-09 in the air-gapped workshop VM
#                                                     (2 vCPUs, the pinned wheels): up to 4.2e-10 against this
#                                                     repository's 8-thread files, 1e-11 with one thread. Byte
#                                                     identity had held only on the machine that wrote them.
# 4. Re-checks that the generated benchmark tables in the manuscripts match the regenerated files.
# Offline: set SPARC_DATA_DIR to a directory that already holds the SPARC files, and SPARC_OFFLINE=1.
# fetch_sparc.sh then verifies them against their pinned SHA-256 and downloads nothing, so the whole run
# needs no network.
# Extended 2026-10-09: until then only three files were covered, so the strict SPARC check, the a0
# headline, the Lambda_SC range and the generated tables were not reproduced by this script.
set -euo pipefail
ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$ROOT"
EXACT=(02_galaxy_dynamics/PARAMETER_LEDGER.json 02_galaxy_dynamics/SPARC_175_summary.json
       02_galaxy_dynamics/SPARC_175_GOD_fits.csv 02_galaxy_dynamics/LAMBDA_SC_UNSCREENED.json
       02_galaxy_dynamics/LAMBDA_S_AT_LIVE_A0_2026-10-09.txt)
NUMERIC=(02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json:1e-12
         02_galaxy_dynamics/EFE_QUADRUPOLE_Q2.json:1e-8
         02_galaxy_dynamics/CASSINI_PARETO_SCAN.json:1e-8)
NUMERIC_FILES=("${NUMERIC[@]%%:*}")
if ! git diff --quiet -- "${EXACT[@]}" "${NUMERIC_FILES[@]}"; then
  echo "refusing: the result files have local edits; run this on a clean checkout" >&2; exit 2
fi
export SPARC_DATA_DIR="${SPARC_DATA_DIR:-$(mktemp -d)/sparc_data}"
bash 02_galaxy_dynamics/fetch_sparc.sh
( cd 02_galaxy_dynamics && python3 parameter_ledger.py && python3 efe_quadrupole_q2.py && python3 cassini_pareto_scan.py \
    && python3 sparc_reproduce.py && python3 lambda_sc_unscreened.py \
    && python3 lambda_s_solar_system_check.py --a0 1.1607e-10 > LAMBDA_S_AT_LIVE_A0_2026-10-09.txt )
python3 scripts/a0_distance_corrected_reextract.py
num_rc=0
for spec in "${NUMERIC[@]}"; do
  python3 scripts/compare_json_numeric.py "${spec%%:*}" "${spec##*:}" || num_rc=1
done
git checkout -q -- "${NUMERIC_FILES[@]}"
python3 scripts/sparc_benchmark_tables.py --check
if git diff --exit-code --stat -- "${EXACT[@]}" && [ "$num_rc" -eq 0 ]; then
  echo "REPRODUCED: ${#EXACT[@]} result files byte-identical and ${#NUMERIC[@]} within tolerance (a0 1e-12; EFE, Cassini 1e-8), at $(git rev-parse --short HEAD)"
else
  echo "DRIFT: regenerated results differ from $(git rev-parse --short HEAD) (see above)" >&2; exit 1
fi
