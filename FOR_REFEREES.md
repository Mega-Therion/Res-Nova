# For referees

Read this first, then the ledger, then the manuscript.

**What this repository is:** a non-relativistic dual-channel interpolating function, Lean-checked identities, a Skordis–Złośnik embedding, and a SPARC measurement with a systematic budget.

**What this repository is not:** a completed derivation of `a0` from cosmology, a replacement for `Λ`CDM in the CMB, or a zero-parameter theory.

## Audit order

1. `EPISTEMIC_BOUNDARY_v1.5.0.md` — every claim, tagged.
2. `AGENT_COVENANT.md` — what the authors forbid themselves to say.
3. `OPEN_PROBLEMS_AND_TESTS.md` — what is still open.
4. `final_manuscript.pdf` — narrative. If it outruns the ledger, the ledger wins.
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
| Working `a0` | `A0_MEASUREMENT.json` | `python3 02_galaxy_dynamics/a0_measure.py` |
| Parameter budget / 342 extra NFW knobs | `PARAMETER_LEDGER.json`, `NFW_CONSTRAINED.json`, `SPARC_PARAMETER_BUDGET.md` | `parameter_ledger.py`, `nfw_constrained.py` |
| Halo correlations | `HALO_CONSPIRACY.json` | `halo_conspiracy.py` |
| Withdrawn zero-parameter language | this file; README related-publications note; Zenodo titles are historical | — |

## Numbers you should refuse if quoted as current

- `a0 = (9.433 \pm 0.050)\times 10^{-11}` as a precision measurement.
- 24.8`\sigma` tension with `cH_0/(2\pi)`.
- 5-fold CV that reports one `a0` to 16 figures in every fold.
- “Zero free parameters” as the SPARC model class.
- Unconstrained NFW median 1.92 as the `Λ`CDM row (97/171 galaxies railed at `c=1`).

## Numbers that are current (`[D]`, commit `3c90ef3e`)

- `a0 = 1.116\times 10^{-10}` ± `0.128\times 10^{-10}` (stat) ± `0.097\times 10^{-10}` (syst).
- Horizon comparison: `0.46\sigma`. MOND `1.2\times 10^{-10}`: `0.52\sigma`.
- Tier 1 GOD median 2.95 / 374 parameters; MOND 2.89 / 374; NFW free-c 1.92 / 716; NFW cosmological-c 5.62 / 716.
- Extra NFW knobs versus GOD at Tier 1: 342.

## Formal core you can take as mathematics

Lean `v4.33.0-rc1`, Mathlib pin `5eec30bc`, 17 modules, reported 0 `sorry`, standard axioms only. Reproduction provenance is local (open O6), not a blank-machine walk.

## Recommended citation posture

Cite the dual-channel identity and the no-go theorems as mathematics. Cite the SPARC measurement as a measurement. Cite the horizon formula as a hypothesis under test. Do not cite `Ω_\Lambda=\ln 2` as a result of this package.
