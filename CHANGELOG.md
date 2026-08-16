# Changelog

## [1.5.0] — 2026-08-15

Epistemic and reproducibility alignment over the v1.4.0 physics seal. No new theorems. No new SPARC fits in this commit.

### Added
- `EPISTEMIC_BOUNDARY_v1.5.0.md` — claim ledger updated to the 2026-08-15 measurement and parameter ledger.
- `OPEN_PROBLEMS_AND_TESTS.md` — closure path, test path, and quarantine text for every remaining `[O]`.
- `FOR_REFEREES.md` — manuscript/claim → file → script map.
- `AGENT_COVENANT.md` — operating rules for any coding agent working this repo.
- `01_foundational_action/PAPER_01_NOTICE.md` — quarantine of the single-channel arcsinh construction.
- `02_galaxy_dynamics/SPARC_DATA.md` — data provenance and the hardcoded-path defect.
- `requirements.txt`, `environment.yml`, `.github/workflows/verify.yml`.
- `scripts/check_claim_consistency.py` — fails if the superseded a0 headline returns as a current claim.

### Changed
- README empirical section now reports `A0_MEASUREMENT.json` and `PARAMETER_LEDGER.json` as current `[D]`, and marks the 176-parameter / `9.433e-11` headline as method-superseded.
- `02_galaxy_dynamics/SPARC_PARAMETER_BUDGET.md` rewritten from `PARAMETER_LEDGER.json` and `NFW_CONSTRAINED.json`.

### Not closed
- `a0 = c H0 / (2π)` as a derivation remains `[O]`.
- `Ω_Λ = ln 2` remains `[O]`.
- High-redshift `a0(z) = ξ c H(z)` remains an unrun test, not a result.

Prior changelog text is the blob `01c42f2b` on `main` (git history). Physics seal: tag `v1.4.0` / commit `651a70d8`.
