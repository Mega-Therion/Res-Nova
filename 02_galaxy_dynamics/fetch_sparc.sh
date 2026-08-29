#!/usr/bin/env bash
set -euo pipefail

# Resolve repository root.
# BASH_SOURCE[0] is the path AS INVOKED, so it must be dereferenced: this script
# is reachable through symlinks at the repo root and at scripts/, and without
# readlink -f those entry points compute REPO_ROOT one level too high and the
# manifest lookup fails.
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "${SCRIPT_PATH}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# SPARC_DATA_DIR is the project-wide override honoured by 02_galaxy_dynamics/
# sparc_paths.py; the fetcher must write where the analysis scripts read.
DATA_DIR="${SPARC_DATA_DIR:-${REPO_ROOT}/02_galaxy_dynamics/sparc_data}"
MANIFEST="${REPO_ROOT}/VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256"
URL="https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"

echo "=== Fetching SPARC Dataset (CWRU) ==="
echo "Target directory: ${DATA_DIR}"
echo "Manifest: ${MANIFEST}"

if [ ! -f "${MANIFEST}" ]; then
    echo "ERROR: Manifest file not found: ${MANIFEST}" >&2
    exit 1
fi

mkdir -p "${DATA_DIR}"
TMP_ZIP="${DATA_DIR}/Rotmod_LTG.zip"

echo "Downloading ${URL} ..."
curl -fL -o "${TMP_ZIP}" "${URL}"

echo "Extracting ${TMP_ZIP} ..."
unzip -q -o "${TMP_ZIP}" -d "${DATA_DIR}"
rm -f "${TMP_ZIP}"

# Flatten subdirectory if created by zip
if [ -d "${DATA_DIR}/Rotmod_LTG" ]; then
    find "${DATA_DIR}/Rotmod_LTG" -type f -name "*_rotmod.dat" -exec mv -t "${DATA_DIR}" {} +
    rmdir "${DATA_DIR}/Rotmod_LTG" || true
fi

# Count *_rotmod.dat files
COUNT=$(find "${DATA_DIR}" -maxdepth 1 -type f -name "*_rotmod.dat" | wc -l)
echo "Extracted ${COUNT} *_rotmod.dat files."

if [ "${COUNT}" -ne 175 ]; then
    echo "ERROR: Expected 175 *_rotmod.dat files, found ${COUNT}." >&2
    exit 1
fi

echo "Verifying SHA-256 checksums against manifest..."
(
    cd "${DATA_DIR}"
    sha256sum -c "${MANIFEST}"
)

echo "=== SUCCESS: 175 SPARC rotmod files verified with 0 drift ==="
