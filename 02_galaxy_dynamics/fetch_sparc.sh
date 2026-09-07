#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: fetch_sparc.sh [--data-dir DIR]

Download the official SPARC Rotmod_LTG archive, extract the 175 rotation-curve
files, and verify every file against the repository SHA-256 manifest.

Options:
  --data-dir DIR  Destination directory. This takes precedence over
                  SPARC_DATA_DIR and the repository-local default.
  -h, --help      Show this help text.

The SPARC_DATA_DIR environment variable is supported for non-interactive use.
EOF
}

# Resolve repository root from the physical script path so invocation through a
# symlink remains portable.
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "${SCRIPT_PATH}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

DATA_DIR="${SPARC_DATA_DIR:-${REPO_ROOT}/02_galaxy_dynamics/sparc_data}"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --data-dir)
            [[ $# -ge 2 ]] || { echo "ERROR: --data-dir requires a value." >&2; usage >&2; exit 2; }
            DATA_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

DATA_DIR="$(readlink -m "${DATA_DIR}")"
MANIFEST="${REPO_ROOT}/VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256"
URL="https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"

if [[ ! -f "${MANIFEST}" ]]; then
    echo "ERROR: Manifest file not found: ${MANIFEST}" >&2
    exit 1
fi
if [[ -e "${DATA_DIR}" && ! -d "${DATA_DIR}" ]]; then
    echo "ERROR: Data path exists but is not a directory: ${DATA_DIR}" >&2
    exit 1
fi
mkdir -p "${DATA_DIR}"
TMP_ZIP="${DATA_DIR}/Rotmod_LTG.zip"

cleanup() { rm -f "${TMP_ZIP}"; }
trap cleanup EXIT

echo "=== Fetching SPARC Dataset (CWRU) ==="
echo "Target directory: ${DATA_DIR}"
echo "Manifest: ${MANIFEST}"
echo "Downloading ${URL} ..."
curl -fL --retry 3 --retry-delay 2 -o "${TMP_ZIP}" "${URL}"

echo "Extracting ${TMP_ZIP} ..."
unzip -q -o "${TMP_ZIP}" -d "${DATA_DIR}"

# The official archive may contain a Rotmod_LTG/ wrapper directory. Flatten it
# while leaving unrelated files untouched.
if [[ -d "${DATA_DIR}/Rotmod_LTG" ]]; then
    find "${DATA_DIR}/Rotmod_LTG" -type f -name "*_rotmod.dat" -exec mv -t "${DATA_DIR}" -- {} +
    rmdir "${DATA_DIR}/Rotmod_LTG" 2>/dev/null || true
fi

COUNT="$(find "${DATA_DIR}" -maxdepth 1 -type f -name "*_rotmod.dat" | wc -l)"
echo "Extracted ${COUNT} *_rotmod.dat files."
if [[ "${COUNT}" -ne 175 ]]; then
    echo "ERROR: Expected 175 *_rotmod.dat files, found ${COUNT}." >&2
    exit 1
fi

echo "Verifying SHA-256 checksums against manifest..."
(
    cd "${DATA_DIR}"
    sha256sum -c "${MANIFEST}"
)
echo "=== SUCCESS: 175 SPARC rotmod files verified with 0 drift ==="
