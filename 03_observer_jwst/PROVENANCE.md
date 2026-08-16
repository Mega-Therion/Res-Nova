# Provenance status — high-z a0(z) sample

**Status of the 20 rows retained in `a0_of_z.py`: UNDOCUMENTED PROVENANCE.**

> The high-z O4 table currently has undocumented provenance in the reviewed
> repository history and is not yet suitable for scientific citation,
> significance claims, or claim-level advancement.

**O4 remains D0.** This document records what is and is not known about the origin of those rows, so the status travels with the code.

---

## 1. What "undocumented provenance" means here

For each of the 20 rows, the repository contains **none** of the following:

| Required provenance element | Present? |
|---|---|
| Source table (DOI / bibcode / table number) | No |
| Acquisition record (URL, catalogue code, query, retrieval date) | No |
| Native catalogue object identifiers | No |
| Units as published + transformation to SI `g_bar` / `g_obs` | No |
| Selection / exclusion rule and rejection log | No |
| Checksum of a raw downloaded file | No — no data file exists |
| Licence / redistribution terms | No |

## 2. Deliberate labelling restraint

These rows are **not** described as real observational data — no acquisition record supports that.

They are equally **not** described as fabricated, synthetic, placeholder, or fake. **No evidence establishes any of those labels either**, and applying one would assert more than is known. Absence of a provenance record is absence of a record; it is not evidence of misconduct.

"Undocumented provenance" is the only supported description and is the term used throughout this repository.

## 3. What the investigation established

- All 20 rows entered the repository in a single commit. `git blame` resolves every line to that one commit; no earlier draft, predecessor table, or deleted version exists anywhere in git history, including unreachable objects.
- Across every blob in the full history, exactly one contains the row schema — the script itself.
- The earliest recoverable occurrence of the rows anywhere is **37 seconds before** that commit. No data retrieval is recorded in the interval preceding it.
- The only astronomy-data retrieval recorded in the surrounding work is the **SPARC** `Rotmod_LTG.zip` archive, which is a **z = 0** dataset unrelated to this high-z test.
- The frozen anchor constant used at `a0_of_z.py` (`1.1160351336495208e-10`) does **not** appear in any version of `02_galaxy_dynamics/A0_MEASUREMENT.json` in repository history; that file has only ever contained `1.1162688655613144e-10`. The constant's producing run is unrecorded. **This discrepancy is unresolved.**

## 4. What could not be determined

- Whether any of the 20 values appear in a real published catalogue — not tested against actual journal tables.
- Whether the values were derived, transcribed, estimated, or produced another way.
- Whether a source existed outside the recorded history (another machine, a browser session, an untracked file since removed).
- Whether the analysis rule was fixed before the outcome was inspected: the protocol, the code, and the first results landed within 38 seconds in a single commit, which removes the ordering evidence.
- **Intent of any kind. None is established, alleged, or implied.**

## 5. Notes that cut against over-reading the above

- `udf-10` is **genuine MUSE survey nomenclature** — the 1′×1′ ultra-deep field inside the HUDF mosaic (which is labelled udf-01…udf-09). The identifier prefix is not arbitrary.
- **Bouché et al. 2021, A&A 654, A49 is a real paper.** The cited Mercier et al. 2022 reference (`A&A 667, A75`) did not resolve; searches point to `A&A 665, A54`. That is an unverified lead, not a finding.
- The redshift spacing is **irregular** (coefficient of variation ≈ 0.20), not a uniform ladder.
- All log-space values sit on a 2-decimal grid, which is **equally consistent with transcription from a published table**, since journals routinely quote such quantities to two decimals. It is not evidence of anything by itself.

## 6. How the code is contained

- The default invocation **refuses to run.** An input must be chosen explicitly.
- `--data PATH` is the intended path, for a dataset meeting Gate 1 (§7).
- `--quarantined-sample` is required to reach the 20 rows. It prints a warning to stderr and tags every output field as conditional.
- The row `source` attribution string has been removed; rows carry `"provenance": "undocumented"`.
- No result artifact is committed. Reports are generated on demand and are tagged `"result_type": "conditional"`, `"data_provenance": "undocumented"`, `"epistemic_classification": "[O] D0_PROPOSED"`.
- Output fields are named for **harness behaviour**, not exclusion: there is no `excluded_hypothesis_at_3sigma` field.

## 7. Gate 1 — what would clear this status

A documented, retrievable source for **every** row: source table, acquisition record, native IDs, units and the full transformation chain, selection rule with rejection log, SHA-256 verified at load time, and licence. Rows must live in a committed data file, never as a literal in code.

**If Gate 1 cannot be met for these particular rows, the correct outcome is to retain the harness and drop the rows.** That is a clean result, not a setback.

## 8. Gate 2 — separate and independent

Provenance and inference are independent gates. Gate 2 (statistic, frozen-a0 uncertainty propagation, covariance, selection effects, systematics, Ω_m sensitivity, conditional-vs-observational tagging) is tracked separately and does not require data. Passing both gates does **not** itself promote O4; that remains a separate decision.

## 9. On the significance figure

Any significance produced from the quarantined rows is a **harness reproduction check, not a claim**. Separately, the previously used shortcut `sqrt(|Δχ²|)` is not a valid significance for two non-nested hypotheses with zero parameters re-fitted at the test stage; it has been replaced with the closed-form Gaussian result. On this input the two happen to agree to within 0.01σ, but the shortcut does not generalise.

Note also that the **maximum attainable separation** between the two hypotheses on this input is ≈ 5.47σ — a design constraint worth computing for any future sample *before* collecting it.
