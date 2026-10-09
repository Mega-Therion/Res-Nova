# For referees

Read this first, then the ledger, then the manuscript.

**What this repository is:** a non-relativistic dual-channel interpolating function, Lean-checked identities, a Skordis–Złośnik embedding, and a SPARC measurement with a systematic budget.

**What this repository is not:** a completed derivation of `a0` from cosmology, a replacement for `Λ`CDM in the CMB, or a theory without inputs: it carries two irreducible ones, the `a0` scale and the choice of μ.

## Audit order

1. `EPISTEMIC_BOUNDARY_v1.5.0.md` — every claim, tagged.
2. `AGENT_COVENANT.md` — what the authors forbid themselves to say.
3. `OPEN_PROBLEMS_AND_TESTS.md` — what is still open.
4. `res_nova_manuscript.pdf` — narrative. If it outruns the ledger, the ledger wins.
5. `05_lean_formalization/verify_all_proofs.sh` — formal core.
6. `02_galaxy_dynamics/A0_MEASUREMENT.json` and `PARAMETER_LEDGER.json` — empirical core.

## Map: claim → files

| If you are checking | Read | Run (if data present) |
|---|---|---|
| `μ(x)=x/(1+x)` from `F_dual` | `DualChannelDerivation.lean`, `GODActionKinematics.lean`, `TARGET_D1_VARIATIONAL_DERIVATION.md` | `./05_lean_formalization/verify_all_proofs.sh` |
| Single-channel / `arcsinh` failure | `TARGET_D1_VARIATIONAL_DERIVATION.md`, `PAPER_01_NOTICE.md` | same |
| RAQUAL no-go | `CovariantCompletion.lean`, `TARGET_D7_COVARIANT_COMPLETION.md` | same |
| GW170817 / disformal split | `TensorSpeed.lean`, `TARGET_D8_TENSOR_SPEED.md` | same |
| RMOND parent | `SkordisZlosnikEmbedding.lean`, `TARGET_D9_SKORDIS_ZLOSNIK_EMBEDDING.md` | same |
| Working `a0` | `A0_DISTANCE_CORRECTED_2026-09-16.json` (μ_std, T1; the superseded μ_dual fit is `A0_MEASUREMENT.json`) | `python3 scripts/a0_distance_corrected_reextract.py` |
| Parameter budget / 342 extra NFW knobs | `PARAMETER_LEDGER.json`, `NFW_CONSTRAINED.json`, `SPARC_PARAMETER_BUDGET.md` | `parameter_ledger.py`, `nfw_constrained.py` |
| Halo correlations | `HALO_CONSPIRACY.json` | `halo_conspiracy.py` |
| Withdrawn zero-parameter language | this file; README related-publications note; Zenodo titles are historical | — |

## Numbers you should refuse if quoted as current

- `a0 = (9.433 \pm 0.050)\times 10^{-11}` as a precision measurement.
- 24.8`\sigma` tension with `cH_0/(2\pi)`.
- 5-fold CV that reports one `a0` to 16 figures in every fold.
- “Zero free parameters” as the SPARC model class (withdrawn).
- Unconstrained NFW median 1.92 as the `Λ`CDM row (97/171 galaxies railed at `c=1`).

## Numbers that are current (`[D]`; the benchmark lines are generated from the result JSONs)

- `a0 = 1.1607\times 10^{-10}` (μ_std, 175 galaxies; bootstrap 95% `[0.972, 1.295]\times 10^{-10}`, `A0_DISTANCE_CORRECTED_2026-09-16.json` T1; this line updated 2026-10-09). The interval contains both `cH_0/2\pi = 1.042\times 10^{-10}` and MOND's `1.2\times 10^{-10}`.
- Superseded 2026-09-17: `a0 = 1.116\times 10^{-10}` ± `0.128\times 10^{-10}` (stat) ± `0.097\times 10^{-10}` (syst), the 171-galaxy fit under the retired μ_dual; its comparisons were horizon `0.46\sigma`, MOND `0.52\sigma`.
<!-- BEGIN GENERATED: sparc-referee-numbers (scripts/sparc_benchmark_tables.py; do not hand-edit) -->
- Tier 0 (canonical, 171 galaxies, M/L at the prior means): GOD median 11.08 vs MOND 9.93; MOND has the lower median. Source: `PARAMETER_LEDGER.json`.
- Tier 1: GOD median 3.36 / 374 parameters; MOND 3.41 / 374; NFW free-c 1.92 / 716; NFW cosmological-c 5.62 / 716.
- Extra NFW knobs versus GOD at Tier 1: 342.
- Strict unit-M/L check (175 galaxies, `SPARC_175_summary.json`): GOD median 15.01, MOND 17.01, baryons-only 51.58. A reproduction check with a different sample and M/L, not the Tier 0 comparison.
<!-- END GENERATED: sparc-referee-numbers -->

## Formal core you can take as mathematics

Lean `v4.33.0-rc1`, Mathlib pin `5eec30bc`. The gate covers every module on disk, 66 targets on 2026-10-09 (the manuscript modules plus the adjacent-programme modules declared in `05_lean_formalization/ADJACENT_MODULES.txt`; the live count is the `verified: N / N` line of `assurance/evidence/gate_66_targets_2026-10-09.log`), 0 `sorry`, standard axioms only. A clean kernel certifies the mathematics, not a physical reading: which rows are `[P]` is fixed by `proof-records/P_ROWS.json`. O6 — closed 2026-09-08: cold-machine fetch demonstrated (VERIFICATION_RUN_008) and the `lean-gate` CI job runs the full gate on every push (green at `d130413`). O5 — closed 2026-09-09: clean-clone `fetch_sparc.sh` walk, 175/175 checksums, 0 drift (VERIFICATION_RUN_009).

## Recommended citation posture

Cite the dual-channel identity and the no-go theorems as mathematics. Cite the SPARC measurement as a measurement. Cite the horizon formula as a hypothesis under test. Do not cite `Ω_\Lambda=\ln 2` as a result of this package.
