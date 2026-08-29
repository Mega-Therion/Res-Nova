import Lake
open Lake DSL

/-!
# Res-Nova Formal Proof Suite

Build scaffolding for the Lean 4 modules backing the `[P]`-tagged claims in
`README.md` and `final_manuscript.tex`.

Mathlib is pinned by `lake-manifest.json` to the exact revision the suite was
verified against, so `lake env lean <Module>.lean` is reproducible rather than
toolchain-dependent.

    lake exe cache get      # fetch prebuilt Mathlib oleans
    lake build              # build every module below
-/

package «ResNovaFormal» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "5eec30bc56ed5a23be2e27c544a949ba0bceddeb"

@[default_target]
lean_lib «ResNovaFormal» where
  srcDir := "."
  roots := #[
    `AXIOMS_V2,
    `CartanTrialityGenerations,
    `ChiralCellularDuality,
    `CosmologicalSector,
    `CovariantCompletion,
    `DeSitterExtremal,
    `DualChannelDerivation,
    `GODActionKinematics,
    -- AUDITED VACUOUS 2026-08-29 (D47_generation_index_audit.md). Compiles and is
    -- sorry-free, which is why it is gated -- but `z3NetChirality` returns 3/-3/0
    -- because those literals are written into its if-then-else, and the theorem
    -- proves a function returning 3/-3/0 returns 3/-3/0. Demonstrated by
    -- substitution: the identical proof with 42 and 17 in place of 3 compiles
    -- clean. `mckay_generation_count` is `3 = 3`. Passing this gate means the file
    -- ELABORATES; it is not evidence for any generation count.
    `GenerationIndex,
    `Hamilgrangian,
    `HorizonScale,
    `ITActionClosure,
    `MuProjection,
    `PPNLimits,
    `PrintAxioms,
    `PrintAxiomsD8,
    `RamanujanModularBounds,
    `RelativisticStability,
    `RapidityEquipartition,
    `SOCasimirGenuine,
    `SovereignSpinCeiling,
    `SkordisZlosnikEmbedding,
    `SovereignRegularity,
    `SovereignSemiotics,
    `TensorSpeed,
    `TrialityG2,
    `TrialityFixedSubalgebra,
    `YettParadigm
  ]
