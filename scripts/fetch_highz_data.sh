#!/usr/bin/env bash
# Provenance check for the high-z CSVs used by scripts/a0_highz_measurement.py.
#
# CHECK MODE (default, no network): for every CSV actually used, re-hash the cached primary
# source in 02_galaxy_dynamics/highz_data/_src/ (gitignored, .gitignore:43) and compare with the
# sha256 printed in the CSV's provenance header.  Exit 0 iff every hashable source matches and
# every CSV has a provenance header.  Hand-typed rows with no machine-readable source are listed
# as HAND (not counted as PASS).
#
# REFETCH MODE (--refetch, needs network; writes only into _src/, keep disk usage small):
#   RC100  : curl -L -o _src/2209.12199v1.pdf https://arxiv.org/pdf/2209.12199v1
#   RC41   : curl -L -o _src/arXiv_2006.03046_eprint.pdf https://arxiv.org/pdf/2006.03046
#   G17    : curl -L -o _src/arXiv_1703.04310_eprint.pdf https://arxiv.org/pdf/1703.04310
#   Ubler17: curl -L -o _src/Ubler2017_J_ApJ_842_121_table3.dat https://cdsarc.cds.unistra.fr/ftp/J/ApJ/842/121/table3.dat
#   Ciocan26 (hand-typed from TeX): curl -L -o _src/2604.22613.tar.gz https://arxiv.org/e-print/2604.22613
#   HighZ_TF_published_fits (hand-typed from TeX e-prints): https://arxiv.org/e-print/<id> for
#     1703.04321 1701.05561 1810.07202 1604.06103
#   Known dead: KROSS Durham page astro.dur.ac.uk/KROSS/data.html (HTTP 404); VizieR J/ApJ/902/98 absent.
# After a refetch, re-run this script without flags; a hash mismatch means the upstream file changed
# and the CSV must be re-verified, never silently re-headed.
set -u
cd "$(dirname "$0")/.." || exit 2
D=02_galaxy_dynamics/highz_data
S=$D/_src
fail=0

check() { # csv  srcfile  expected_sha
  local csv=$1 src=$2 exp=$3
  if [ ! -f "$D/$csv" ]; then echo "FAIL  $csv: CSV missing"; fail=1; return; fi
  if ! grep -q "$exp" "$D/$csv"; then echo "FAIL  $csv: header does not carry sha $exp"; fail=1; return; fi
  if [ ! -f "$S/$src" ]; then echo "MISSING-SRC  $csv: $S/$src not cached (refetch: see header of this script)"; fail=1; return; fi
  local got; got=$(sha256sum "$S/$src" | cut -d' ' -f1)
  if [ "$got" = "$exp" ]; then echo "PASS  $csv (source-hash only; cell values not re-compared) <- _src/$src sha256 ${got:0:12}"; else echo "FAIL  $csv: _src/$src sha256 $got != header $exp"; fail=1; fi
}

if [ "${1:-}" = "--refetch" ]; then
  echo "refetch mode: run the curl lines in this script's header manually (kept manual on purpose: disk is near full)."
  exit 3
fi

check RC100_NestorShachar2023_table3_transcribed.csv 2209.12199v1.pdf a04738e47a61b761a693ba7b156d16240fcffbb1d9252df9456ca4d209aeff22
check RC41_Genzel2020.csv arXiv_2006.03046_eprint.pdf a8bf2f52caa7f9eb387c8c87429d0e2bad11308c33a1973de4f9770410c3f7d6
check G17_Genzel2017.csv arXiv_1703.04310_eprint.pdf 9926059ed950486e6982e3ec612303b4415832a3a01c091fc0035e564259e5d4
check Ubler2017_KMOS3D_TFR.csv Ubler2017_J_ApJ_842_121_table3.dat b46ee156730a43cfbc89b957d56bd7f244da2535c872f4fc8739e7ec7811ca59
for f in HighZ_TF_published_fits.csv Ciocan2026_MUSEDARKIII_a0.csv; do
  if [ -f "$D/$f" ] && head -3 "$D/$f" | grep -q '^#'; then
    echo "HAND  $f: hand-typed from arXiv TeX; provenance header present; no single hashable machine-readable source (not counted as PASS)"
  else echo "FAIL  $f: missing or no provenance header"; fail=1; fi
done
echo "fetch_highz_data.sh exit=$fail"
exit $fail
