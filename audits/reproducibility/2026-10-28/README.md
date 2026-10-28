# Res-Nova reproducibility audit — 2026-10-28

## Verdict

**[D] Source-reported scan result; independently checked for artifact consistency, not rerun from raw SPARC data.** The committed scan JSON contains 320 rows and its row-level gates agree with its embedded summary: 298 admissible rows, 22 inadmissible rows, and zero joint passes. This establishes internal consistency of the published artifact, not independent reproduction of the physics computation.

**[P] Algebraic identity.** If
\[
\rho_\Lambda=\frac{H_0^2\ln 2}{32\pi^2G},\qquad
\rho_{\rm crit}=\frac{3H_0^2}{8\pi G},
\]
then cancellation gives
\[
\Omega_\Lambda=\frac{\rho_\Lambda}{\rho_{\rm crit}}
=\frac{\ln 2}{12\pi}\approx0.018386300013,
\]
not \(\ln 2\approx0.693147180560\). This is a direct algebraic consequence of the two displayed definitions. The supplied equations alone do not derive \(\Omega_\Lambda=\ln2\).

## Repository evidence inspected

Repository: https://github.com/Mega-Therion/Res-Nova

| Artifact | Recorded Git blob SHA | Role |
|---|---|---|
| `02_galaxy_dynamics/CASSINI_SPARC_JOINT_SCAN.json` | `c191a30d9d67b08ca82d8720acc11a95283508c2` | 320-row result artifact |
| `02_galaxy_dynamics/CASSINI_SPARC_JOINT_SCAN_2026-10-27.md` | `d927170e0b302f9c242e76b29526e6582e374b34` | Human-readable reported result |
| `02_galaxy_dynamics/CASSINI_SPARC_JOINT_SCAN_PREREG_2026-10-27.md` | `6b093b1798d7a55ab7ac3fba5146c11017e60e11` | Pre-registration |
| `02_galaxy_dynamics/cassini_sparc_joint_scan.py` | `9e050fde830f0179c1bf8f06d65fc3db22272b43` before portability fix | Scan driver |
| `02_galaxy_dynamics/parameter_ledger.py` | `8eed18b1da02a88bceeccdc9daaec6bb3ae724b8` | SPARC fit/scoring implementation |
| `02_galaxy_dynamics/efe_quadrupole_q2.py` | `fd97b7bfb620f988109f37fd2a52e318591dfa95` | QUMOND quadrupole calculation |
| `02_galaxy_dynamics/sparc_paths.py` | `b6dd075d20be4a1fe0fb7c8d40319b63a1397eb2` | Data path resolution |
| `requirements.txt` | fetched from repository default branch | Exact package pins (numpy, scipy, sympy, mpmath, PyYAML) |

Blob SHA values are Git object identifiers, not SHA-256 hashes of downloaded files.

## Row-level summary checked against the JSON

| Family | Rows | Admissible | Cassini passes | SPARC passes | Joint passes |
|---|---:|---:|---:|---:|---:|
| a: \(\nu_n\) | 74 | 74 | 42 | 2 | 0 |
| b: \(\nu_{\gamma,\beta}\) | 168 | 146 | 17 | 0 | 0 |
| c: tail-cut \(\nu_n\) | 78 | 78 | 4 | 18 | 0 |
| **Total** | **320** | **298** | **63** | **20** | **0** |

The scan report's family-b table lists 146 *admissible* rows; the JSON has 168 total family-b rows, of which 22 are inadmissible. These are consistent, not contradictory.

## Reproducibility defect fixed on this branch

The scan driver previously set `SPARC_DATA_DIR` to an absolute `/home/mega/...` path whenever the caller had not already set that variable. This silently defeated the repository-local data discovery and made a default run machine-dependent. The branch removes that hard-coded default, preserves explicit `SPARC_DATA_DIR` or `SPARC_DATA`, and selects the repository-local `02_galaxy_dynamics/sparc_data` only when it exists. The underlying `sparc_paths.py` remains the path resolver.

The prose in `02_galaxy_dynamics/SPARC_DATA.md` also described a legacy absolute-path fallback that current `sparc_paths.py` no longer implements; that documentation is corrected on this branch.

## Clean reproduction protocol

Run from the repository root on Linux/macOS with Python 3:

1. Create an isolated environment and install the repository's pinned requirements:
   `python3 -m venv .venv && . .venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt`.
2. Fetch the official SPARC rotation-curve tables and validate the tracked checksum manifest:
   `bash 02_galaxy_dynamics/fetch_sparc.sh`.
3. Check the fetched corpus before analysis:
   `find 02_galaxy_dynamics/sparc_data -maxdepth 1 -type f -name '*_rotmod.dat' | wc -l`
   should report 175, and the fetch script must exit zero after manifest validation.
4. Validate the committed result artifact's internal counts:
   `python3 audits/reproducibility/2026-10-28/verify_joint_scan_artifact.py 02_galaxy_dynamics/CASSINI_SPARC_JOINT_SCAN.json`.
5. Regenerate the scan into a **separate clean worktree or output directory** to preserve the committed result for comparison. The scan driver writes `CASSINI_SPARC_JOINT_SCAN.json` relative to the current working directory and takes roughly 40 minutes according to its docstring; it uses multiprocessing. Capture the command, Python version, OS, package versions, dataset manifest result, stdout/stderr, exit status, and SHA-256 of the generated JSON.
6. Compare regenerated row-level fields and summary against the committed JSON. Any differences must be explained before claiming reproduction; do not overwrite the reference artifact during the run.

## Current limits

- **Not yet completed:** a clean execution of the 320-row scan from raw SPARC data in this session. The session's shell could not resolve `github.com`, so a local checkout/run was unavailable. The GitHub connector was used to inspect repository files; that is not a substitute for executing the pipeline.
- **Not claimed:** a Lean build, independent QUMOND solver run, or new fit to raw SPARC tables.
- **Scope:** the zero-joint-pass result applies only to the preregistered QUMOND model, families, grid, nuisance policy, and gates in the cited record. It is not a theorem ruling out all interpolation functions or AeST.
- **Environment pinning:** the repository has exact dependency pins in `requirements.txt`; the host OS and Python interpreter version still need to be recorded in the clean-run receipt.

## Evidence labels

- **[P]** Computed here: algebraic cancellation for \(\Omega_\Lambda\); direct row/summary consistency checks on the fetched JSON object.
- **[D]** Documented by repository artifacts but not independently rerun from raw inputs: the reported physical scan.
- **[O]** Open: whether any model outside the tested family/grid passes both empirical gates; whether the full scan reproduces byte-for-byte or within a justified numerical tolerance on a clean environment.
