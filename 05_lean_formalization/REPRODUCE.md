# O6: Lean 4 Fresh-Clone Reproduction Guide

## Prerequisites

1. **Install Elan** (Lean toolchain manager):
   ```bash
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
   ```
   This installs `lean`, `lake`, and the `elan` version manager.

2. **Verify the pinned toolchain** (from `05_lean_formalization/lakefile.lean`):
   ```bash
   cd 05_lean_formalization
   cat lakefile.lean | grep lean_version
   ```
   The toolchain is pinned via `lean_version` in the lakefile. Elan will
   auto-download the exact version on first `lake build`.

## Fresh-Clone Reproduction Steps

```bash
# 1. Clone the repository
git clone https://github.com/Mega-Therion/Res-Nova.git
cd Res-Nova

# 2. Enter the Lean formalization directory
cd 05_lean_formalization

# 3. Download Mathlib build cache (saves ~30 min compile time)
lake exe cache get

# 4. Build all 17 modules
lake build

# 5. Verify axiom hygiene (no sorry, no admit, standard axioms only)
./verify_all_proofs.sh
```

## Expected Output

All 17 modules should compile with `exit code 0`. The axiom check should show
exclusive dependence on `[propext, Classical.choice, Quot.sound]` — the standard
foundational axioms of Lean 4's type theory.

## Modules

| Module | Theorem | Status |
|--------|---------|--------|
| GODActionKinematics.lean | Dual-channel polynomial identity | [P] |
| MuProjection.lean | μ(x) cosine geometry, quadratic law root | [P] |
| DualChannelDerivation.lean | F(x) = x²/2 - x + ln(1+x), F'(x) = x/(1+x) | [P] |
| ITActionClosure.lean | Information tension action closure | [P] |
| CovariantCompletion.lean | RAQUAL superluminal failure | [P] |
| TensorSpeed.lean | c_T = c constraint | [P] |
| PPNLimits.lean | γ_PPN = 1, Newtonian recovery | [P] |
| DeSitterExtremal.lean | Horizon lapse vanishes | [P] |
| SOCasimirGenuine.lean | so(n) Casimir eigenvalues | [P] |
| SkordisZlosnikEmbedding.lean | Covariant embedding properties | [P] |
| SovereignRegularity.lean | Beale-Kato-Majda regularity | [P] |
| RelativisticStability.lean | Stability conditions | [P] |
| YettParadigm.lean | Ramanujan-Yett spectral gap | [P] |
| CosmologicalSector.lean | Cosmological sector definitions | [P] |
| HorizonScale.lean | KMS 2π cancellation, ξ = 1 | [P] |
| AXIOMS_V2.lean | Axiom inventory | [P] |
| PrintAxioms.lean / PrintAxiomsD8.lean | Axiom reporting utilities | [P] |

## Known Issues

- **Mathlib is multi-GB.** `lake exe cache get` downloads pre-built `.olean` files
  from the Mathlib CI cache. Without it, `lake build` compiles all of Mathlib
  from source (~30-60 min depending on hardware).
- **First `lake build` on a cold machine** (no host cache) has been demonstrated
  once at commit `07185a6` (VERIFICATION_RUN_007, 17/17 PASS). It is not yet a
  CI release gate — see OPEN_PROBLEMS_AND_TESTS.md O6.
- **Not a CI release gate.** Running Lean in CI requires multi-GB Mathlib
  download. The recorded PASS was local. Do not pretend CI runs Lean until
  someone walks `lake exe cache get` on a blank GitHub Actions runner.
