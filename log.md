# Session log: res-nova

## 2026-11-22
- Done: registered `res-nova` under Research OS pillar `01-chyren` with `claims.md`, `log.md`, and `PROJECT_INSTRUCTIONS.md`
- Claims added/changed: none
- Files touched: claims.md, log.md, PROJECT_INSTRUCTIONS.md
- Next: log active verified claims in `claims.md`

## 2026-11-25
- Done: O3 Ω_Λ = ln 2 vs CMB + BAO + SN, CONSISTENT (#271). Observation-tier directive and optical map v0. P-OM-1 weak-lensing test on KiDS-1000: FAIL as written (pre-registered `af7d6564`).
- Claims added/changed: POM1 [X] as written; O3 test CONSISTENT (tier [O] unchanged)
- Files touched: 03_observer_jwst/ (PREREG_POM1, pom1_lensing_rar.py, pom1_posthoc_gama.py, POM1_* JSON and record, OPTICAL_MAP_v0), CURRENT_STATE_READ_THIS_FIRST.md, claims.md, log.md
- Also: P-OM-1 v2 (all lens baryons on the kinematic mass system, Mistele+2024 conversions): PASS on re-test, joint χ² = 17.8/14 (pre-registered `ef4672a0`); Pages deploy race fixed (#274)
- Next: blind run of the frozen v2 recipe on new lensing data (KiDS-Legacy/Euclid), or O4 a₀(z)

## 2026-11-26
- Done: Executed all three `OPTICAL_MAP_v0` §5 follow-ups (merged in #279) and completed full independent skeptical audit / 20x random rerun on 2026-11-27:
  1. Rebuilt spectroscopic `JWST z >= 10` target list (`50` secure spectra / `48` unique galaxies across `8` fields, `z_max = 14.4441`, strict descending `z_spec`), retiring `JWST_RECALIBRATION_LEDGER.md` (`f461a94f`).
  2. Pre-registered (`074d1987`) and executed `O4 a₀(z)` test on JWST/NIRSpec `MSA-3D` (`z_eff = 1.091`) + `ALPINE-CRISTAL-JWST` (`z_eff = 5.327`): verdict `CONFOUNDED` (`Δχ²_mech = +16.56`, `Δχ²_shape = −4.82`, `n = +0.15 [−0.31, +0.50]`, 11/11 variants `CONFOUNDED`); reconciled `OPEN_PROBLEMS_AND_TESTS.md` §O4 across `RC100` + JWST.
  3. Pre-registered (`2d925eb6`) and ran blind `P-OM-1 v2` weak-lensing test across `40,894,394` KiDS-Legacy sources (`329` covered unseen DR5 tiles + GAMA DR4, contiguous sky patches, global lens-tree JK, `20×` shared randoms): combined blind endpoint `FAIL` (`99.77/28`, `p = 5.52e-10` pre-reg; `71.65/28` raw `FAIL` / `54.59/28` Hartlap `PASS_WITHIN_MASS_SYSTEMATIC` under Mistele+2024 `Q_ETG = 1.4`), LTGs `PASS` (`6.36–6.74/7`, `med=1.00–1.07`), `GAMA_All4` `Q_ETG = 1.4` `PASS` (`22.39/14`, `p = 0.0709`), and `10.2–10.9` mass-matched `GAMA_All4` `PASS` (`20.40/14`, `p = 0.118` at `Q_ETG = 1.0`; `17.52/14`, `p = 0.229` at `Q_ETG = 1.4`). Public Euclid `she_*` tables absent.
- Claims added/changed: `POM1v2-BLIND`, `O4-JWST`, `JWST-ZGT10` updated in `claims.md` (`POM1` `[X]`, `POM1v2` `[D]`, `O4` remains `CONFOUNDED`).
- Files touched: `03_observer_jwst/` (`jwst_zgt10_targets.py`, `JWST_ZGT10_SPEC_TARGETS_2026-11-26.*`, `JWST_RECALIBRATION_LEDGER.md`, `PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md`, `pom1v2_blind_kids_legacy.py`, `POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`, `POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md`, `OPTICAL_MAP_v0_2026-11-25.md`), `04_cosmology/` (`PREREG_O4_JWST_A0Z_2026-11-26.md`, `o4_jwst_a0z_run.py`, `O4_JWST_A0Z_RESULT.json`, `O4_JWST_A0Z_RECORD_2026-11-26.md`), `OPEN_PROBLEMS_AND_TESTS.md`, `CURRENT_STATE_READ_THIS_FIRST.md`, `claims.md`, `log.md`, `scripts/local_gate.sh`.
- Next: Run blind Euclid test once `she_*` shear catalogs are public; pursue `P-OM-2`/`P-OM-3` and `H_kin(z)` vs `a₀(z)` separation.
