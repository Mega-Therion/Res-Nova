# Outside checks

Every reproduction or critique of a Res-Nova result by someone outside the project is listed here, whether it confirms or breaks the result, with a link. Private replies are listed only with their author's permission. To add one, open an issue with the **Reproduction / critique report** template.

| date | who | what was checked | outcome | link |
|---|---|---|---|---|
| none yet | | | | |

## Self-checks (not outside checks)
| date | what | outcome | record |
|---|---|---|---|
| 2026-10-08 | Cold re-run of the 3 core result files from a fresh clone (`reproduce_core_results.sh`) | 3/3 byte-identical to `6e9dce9`; SPARC 175/175 SHA-256 verified | `VERIFICATION_RUN_010_COLD_CORE/` |
| 2026-10-09 | Offline re-run of all headline files at `e87dd47` on a second machine: an air-gapped VM with 2 vCPUs and the pinned wheels; snapshot rebuilt to the upstream tree `416adccc`; SPARC data verified by SHA-256 | **Broke the byte-identity claim.** 5 files byte-identical; the a₀ file within 10⁻¹². `EFE_QUADRUPOLE_Q2.json` and `CASSINI_PARETO_SCAN.json` differed by up to 4.2×10⁻¹⁰ relative, from BLAS thread count (1.0×10⁻¹¹ with one thread). A separate verifier run in the same VM matched the worker's output exactly. The script now compares those two files to 10⁻⁸ | gAIng workshop receipts `RN-REPRO-e87dd47` and `RN-DIAG-threads` |
