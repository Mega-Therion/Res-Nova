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
    `CosmologicalSector,
    `CovariantCompletion,
    `DeSitterExtremal,
    `DualChannelDerivation,
    `GODActionKinematics,
    `ITActionClosure,
    `MuProjection,
    `PPNLimits,
    `PrintAxioms,
    `PrintAxiomsD8,
    `RelativisticStability,
    `SOCasimirGenuine,
    `SkordisZlosnikEmbedding,
    `SovereignRegularity,
    `TensorSpeed,
    `YettParadigm
  ]
