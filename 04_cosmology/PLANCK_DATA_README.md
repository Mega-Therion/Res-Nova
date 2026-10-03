# Planck 2018 baseline likelihood data

Res Nova’s existing cosmology scripts use **compressed Planck distance priors** (`R`, `l_A`, and `omega_b`). Those priors are not the full CMB likelihood. This directory is reserved for the official Planck 2018 PR3/R3.00 baseline likelihood archive and its extracted files; the raw directory is gitignored.

## Download and verify

From the repository root:

```bash
python3 scripts/fetch_verified_external_data.py --planck
```

To fetch both SPARC and Planck:

```bash
python3 scripts/fetch_verified_external_data.py --all
```

The script downloads the official `COM_Likelihood_Data-baseline_R3.00.tar.gz` release from the Planck Legacy Archive object `COSMOLOGY_OID=151902`, checks the archive SHA-256 when `PLANCK_BASELINE_SHA256` or `--planck-sha256` is supplied, verifies that the archive contains the baseline high-ell `plik`, low-ell Commander temperature, and low-ell SimAll polarization likelihood members, then extracts it under `04_cosmology/planck_data/extracted/`.

Because the PLA endpoint does not publish a stable sidecar checksum, an unpinned download is marked in `PLANCK_BASELINE_RECEIPT.json` as `archive_sha256_pinned: false`. For a release-grade run, obtain the checksum through an independently recorded source and run:

```bash
PLANCK_BASELINE_SHA256=<64-hex-sha256> \\
  python3 scripts/fetch_verified_external_data.py --planck
```

A successful run records the actual archive hash, source URL, access time, and required member paths in `PLANCK_BASELINE_RECEIPT.json`. The downloader refuses unsafe archive paths and never treats the compressed distance-prior implementation as equivalent to the full likelihood.

## Official scope

The baseline Planck 2018 reference combination is Commander TT at low multipoles, SimAll EE at low multipoles, and Plik TT/TE/EE at high multipoles. The release and methodology are documented in:

- Planck Legacy Archive PR3 ancillary data: <https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/>
- Planck Collaboration, “Planck 2018 results. V. CMB power spectra and likelihoods,” *A&A* 641, A5 (2020), arXiv:1907.12875.
- Cobaya’s installation notes for the official 2018 `clik` interfaces: <https://cobaya.readthedocs.io/en/latest/likelihood_planck.html>

The official archive is large. It should remain outside git; commit only the downloader, protocol, and receipt metadata.
