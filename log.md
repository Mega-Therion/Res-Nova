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
- Done: Executed all three `OPTICAL_MAP_v0` §5 follow-ups on `feat/boost-o4-pom1v2-jwst`:
  1. Rebuilt spectroscopic `JWST z >= 10` target list (`50` secure spectra / `48` unique galaxies, `z_max = 14.4441`), retiring `JWST_RECALIBRATION_LEDGER.md` (`f461a94f`).
  2. Pre-registered (`950798de`) and executed (`6d523b27`) `O4 a₀(z)` test on JWST/NIRSpec `MSA-3D` (`z_eff = 1.091`) + `ALPINE-CRISTAL-JWST` (`z_eff = 5.327`): verdict `CONFOUNDED` (`Δχ²_mech = +16.66`, `Δχ²_shape = −4.90`, `n = +0.14 [−0.31, +0.49]`, 11/11 variants `CONFOUNDED`); reconciled `OPEN_PROBLEMS_AND_TESTS.md` §O4 across `RC100` + JWST.
  3. Pre-registered (`0994384d`) and ran blind `P-OM-1 v2` weak-lensing test across `40,894,394` KiDS-Legacy sources (`DR5_New329` + `GAMA_G23` + `GAMA_All4`): combined blind endpoint `FAIL` (`66.98/28`, `p = 4.86e-5`), LTGs `PASS` everywhere (`8.27/7`, `p = 0.309`), ETG excess vanishes under `Q_ETG = 1.4` (`ETG − LTG p = 0.227`, `+0.167 dex p = 0.189`) or `10.2–10.9` mass-matching (`27.04/14`, `p = 0.019`). Public Euclid `she_*` tables absent.
- Claims added/changed: `POM1v2-BLIND`, `O4-JWST`, `JWST-ZGT10` added to `claims.md` (`POM1` `[X]`, `POM1v2` `[D]`, `O4` remains `CONFOUNDED`).
- Files touched: `03_observer_jwst/` (`jwst_zgt10_targets.py`, `JWST_ZGT10_SPEC_TARGETS_2026-11-26.*`, `JWST_RECALIBRATION_LEDGER.md`, `PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md`, `pom1v2_blind_kids_legacy.py`, `POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`, `POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md`, `OPTICAL_MAP_v0_2026-11-25.md`), `04_cosmology/` (`PREREG_O4_JWST_A0Z_2026-11-26.md`, `o4_jwst_a0z_run.py`, `O4_JWST_A0Z_RESULT.json`, `O4_JWST_A0Z_RECORD_2026-11-26.md`), `OPEN_PROBLEMS_AND_TESTS.md`, `CURRENT_STATE_READ_THIS_FIRST.md`, `claims.md`, `log.md`, `scripts/local_gate.sh`.
- Next: Push & merge PR; run blind Euclid test once `she_*` shear catalogs are public; pursue `P-OM-2`/`P-OM-3` and `H_kin(z)` vs `a₀(z)` separation.
