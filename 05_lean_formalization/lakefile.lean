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
    `BinaryTetrahedral,
    `TetrahedralQuotient,
    `TetrahedralAction,
    `TetrahedralEvenness,
    `FiniteSU2Envelope,
    `SU2MatrixEnvelope,
    `SU2CarrierRungs,
    `SU2FiniteFaithfulness,
    `CartanTrialityGenerations,
    `ChiralCellularDuality,
    `ChiralCrackSketch,
    `ChiralResidue,
    `ChiralPartner,
    `ChiralHolonomyOrientation,
    `GenerationCycleChirality,
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
    -- clean. The old `mckay_generation_count` was `3 = 3`. Passing this gate means
    -- the file ELABORATES; it is not evidence for any generation count.
    -- IN-FILE CORRECTION APPLIED 2026-09-09: both theorems renamed to state what
    -- they actually prove (`z3NetChirality_takes_defined_literals_VACUOUS_D47`,
    -- `mckayArrowsPerNode_eq_three_DEFINITIONAL_PLACEHOLDER`), matching the
    -- honest-relabel treatment already applied to CartanTrialityGenerations.lean.
    -- This comment is retained as the audit trail; see the file's own header for
    -- the correction.
    `GenerationIndex,
    -- ADDED 2026-09-09. Ported from
    -- Chyren/Research_and_Data/01_Bob_Packages/archive_previous_iterations/2026-08-02_decomposition/lean_repo/GenerationIndex.lean
    -- (RY, 2026-07-27; renamed to avoid the filename collision with
    -- GenerationIndex.lean above). Contains a genuine, sabotage-tested,
    -- non-vacuous theorem (DiagonalForced: exhaustive enumeration over 27 Z3
    -- weight triples) alongside bookkeeping literals transcribed from an
    -- external Python E8 root-system computation, not derived in Lean. See
    -- the file's own header for the full honest split and the one open
    -- physical premise the chain still rests on.
    `DiagonalConeIndex,
    `Hamilgrangian,
    `HorizonScale,
    `ITActionClosure,
    `MuProjection,
    `PPNLimits,
    `PillarIV_AntiDriftGate,
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
    `YettParadigm,
    `RamanujanGapDerivation
  ]
