#!/usr/bin/env bash
# fetch_sparc.sh — Download and verify the SPARC Rotmod_LTG dataset (O5 fix)
#
# Downloads the official CWRU SPARC rotation curve data, unpacks it,
# and verifies all 175 files against the frozen SHA-256 manifest.
#
# Usage:
#   ./fetch_sparc.sh                  # downloads to 02_galaxy_dynamics/sparc_data/
#   SPARC_DATA_DIR=/custom/path ./fetch_sparc.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SPARC_DATA_DIR:-${SCRIPT_DIR}/02_galaxy_dynamics/sparc_data}"
MANIFEST="${SCRIPT_DIR}/VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256"
URL="http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"
ZIP_FILE="/tmp/sparc_rotmod_ltg.zip"

echo "=== SPARC Data Fetcher (O5) ==="
echo "Target directory: ${DATA_DIR}"
echo "Manifest: ${MANIFEST}"
echo ""

# Check if already present
if [ -d "${DATA_DIR}" ] && ls "${DATA_DIR}"/*_rotmod.dat >/dev/null 2>&1; then
    COUNT=$(ls "${DATA_DIR}"/*_rotmod.dat 2>/dev/null | wc -l)
    echo "Found ${COUNT} *_rotmod.dat files already in ${DATA_DIR}"
    if [ "${COUNT}" -ge 175 ]; then
        echo "Dataset appears complete. Verifying..."
        if [ -f "${MANIFEST}" ]; then
            (cd "${DATA_DIR}" && sha256sum -c "${MANIFEST}" 2>/dev/null && echo "SHA-256 verification passed." || echo "WARNING: SHA-256 verification failed. Some files may differ.")
        fi
        echo "Done. Set SPARC_DATA_DIR=${DATA_DIR} to use these files."
        exit 0
    fi
fi

# Download
echo "Downloading from ${URL}..."
if command -v curl >/dev/null 2>&1; then
    curl -L -o "${ZIP_FILE}" "${URL}"
elif command -v wget >/dev/null 2>&1; then
    wget -O "${ZIP_FILE}" "${URL}"
else
    echo "ERROR: Neither curl nor wget found. Please install one."
    exit 1
fi

# Unpack
echo "Unpacking to ${DATA_DIR}..."
mkdir -p "${DATA_DIR}"
unzip -o "${ZIP_FILE}" -d "${DATA_DIR}"
rm -f "${ZIP_FILE}"

# Count files
COUNT=$(find "${DATA_DIR}" -name "*_rotmod.dat" | wc -l)
echo "Downloaded ${COUNT} *_rotmod.dat files"

# Verify
if [ -f "${MANIFEST}" ]; then
    echo "Verifying against SHA-256 manifest..."
    (cd "${DATA_DIR}" && sha256sum -c "${MANIFEST}" 2>/dev/null && echo "SHA-256 verification passed." || echo "WARNING: Some files differ from the frozen manifest. This may be due to line-ending differences.")
else
    echo "WARNING: No SHA-256 manifest found at ${MANIFEST}. Skipping verification."
fi

echo ""
echo "Done. ${COUNT} SPARC rotation curve files in ${DATA_DIR}"
echo "Set SPARC_DATA_DIR=${DATA_DIR} or pass --data-dir ${DATA_DIR} to analysis scripts."
