#!/usr/bin/env bash
# Download the public datasets used by the 04_cosmology likelihood scripts into external_data/ (gitignored) and check
# each file's SHA-256 against cosmo_data.py. Exit status is non-zero if any download or hash check fails.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p external_data
fetch() {  # url  file  sha256
  if [ ! -f "external_data/$2" ]; then curl -sfL "$1" -o "external_data/$2"; fi
  echo "$3  external_data/$2" | sha256sum -c -
}
P=https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR
B=https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2
D=https://raw.githubusercontent.com/des-science/DES-SN5YR/main/4_DISTANCES_COVMAT
fetch "$P/Pantheon%2BSH0ES.dat" "Pantheon+SH0ES.dat" 1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8
fetch "$P/Pantheon%2BSH0ES_STAT%2BSYS.cov" "Pantheon+SH0ES_STAT+SYS.cov" abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc
fetch "$B/desi_gaussian_bao_ALL_GCcomb_mean.txt" desi_gaussian_bao_ALL_GCcomb_mean.txt 9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585
fetch "$B/desi_gaussian_bao_ALL_GCcomb_cov.txt" desi_gaussian_bao_ALL_GCcomb_cov.txt 252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509
fetch "$D/DES-Dovekie_HD.csv" DES-Dovekie_HD.csv 2f57019d783eaa976df80a41b0054171a2d994ee9808d715ce850c2df5720aaf
fetch "$D/STAT%2BSYS.npz" STAT+SYS.npz ffd3124b32148b1372bd95fda9299269f0352a9f8eee02d416c610e38495463b
fetch "$D/DES-Dovekie_Metadata.csv" DES-Dovekie_Metadata.csv 45ad71f8470eaecfe2b386699ef66b26b0717c50f445d5f32941988d32c75388
