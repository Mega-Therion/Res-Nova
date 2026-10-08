# VERIFICATION_RUN_010: cold re-run of the core results (2026-10-08)

| | |
|---|---|
| Source | fresh `git clone --depth 1` of Mega-Therion/Res-Nova at `6e9dce9`, into a scratch directory |
| Data | `fetch_sparc.sh` with `SPARC_DATA_DIR` outside the clone: CWRU `Rotmod_LTG.zip`, **175/175 SHA-256 OK, 0 drift** against `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` |
| Environment | Python 3.12.3, numpy 2.4.6, scipy 1.17.1, Linux |
| `parameter_ledger.py` | exit 0, 19.9 s. 171 galaxies used (D512-2, NGC6789, UGC00634, UGC07232 have 4 points; the loader needs ≥ 5), 3,375 points |
| `efe_quadrupole_q2.py` | exit 0, 4.9 s. Hees 2016 Table 2 validation reproduced |
| `cassini_pareto_scan.py` | exit 0, 66.7 s |
| **Outcome** | `git diff` on `PARAMETER_LEDGER.json`, `EFE_QUADRUPOLE_Q2.json`, `CASSINI_PARETO_SCAN.json` is **empty**: all three are byte-identical to the commit. `PARAMETER_LEDGER.json` SHA-256 prefix `f6c115a5dd869810` on both sides |
| Script check | `reproduce_core_results.sh` on the same clone: exit 0 (REPRODUCED). It refuses a locally edited result file (exit 2) and reports a committed result that the code does not produce as DRIFT (exit 1); both cases were exercised |

Logs: `parameter_ledger.log`, `efe_quadrupole_q2.log`, `cassini_pareto_scan.log` (scratch paths redacted).

This closes the caveat recorded in OPEN_PROBLEMS O5 ("the SPARC analysis scripts were not re-run in this walk") for these three files.
