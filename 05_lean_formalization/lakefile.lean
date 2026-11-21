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
    `PillarII_SecularRootQEC,
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
    `NavierStokesGeometry,
    `NavierStokesScope,
    `NavierStokesSpec,
    -- ADDED 2026-10-12. Periodic-domain types (T3 = (R/Z)^3) and the alignment-along-velocity
    -- interface. Interfaces only; no persistence theorem.
    `NavierStokesDomain,
    `NavierStokesSpacetimeBridge,
    -- ADDED 2026-10-08. The periodic target (Fefferman's statement B) as a Prop, the
    -- alignment obligation over genuine solutions, and four sanity theorems. No proof of B.
    `NavierStokesTarget,
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
    -- ADDED 2026-09-12. Formalizes TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md
    -- Theorems A/B/C + the corrected ghost-free convexity. Read the file header:
    -- Postulate R, the chiral coordinate and mu'(0)=1 are INPUTS, and A and B are
    -- one postulate in two dresses, not two independent corroborations.
    `MuStdUniqueness,
    `MuStdDuality,
    -- ADDED 2026-09-27. l^n family mu_n = x/(1+x^n)^(1/n): duality mu_n(x)^n + mu_n(1/x)^n = 1
    -- for every n (MuStdDuality is n=2); mu_n(1)=2^(-1/n). Cassini EFE admits only n >= 4.36.
    `MuNDuality,
    -- ADDED 2026-09-27. D9 on the live branch by calculus: J_std(Y)=F_std(sqrt Y) differentiates to mu_std/2.
    `SZStdEmbedding,
    `GateHolonomySusceptibility,
    `MuStdSelection,
    `MuStdFoundations,
    `AeSTStealthSector,
    `PPNLimitsStd,
    `LambdaSBound,
    `PrecessionBound,
    `CoshCosmology,
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
    `RamanujanGapDerivation,
    `LeptonMassCollar,
    `NavierStokesCorticalBound,
    `YangMillsCasimirBound,
    `RiemannSpectralExpander,
    `StiefelLaplaceEigenvalue,
    `QuarkMassLadder,
    -- ADDED 2026-10-14. D7/D9: the scalar-channel function whose TOTAL law is mu_std, and its 11.2788 bound.
    `AeSTTotalScalarCorrespondence,
    `MasterEquationCore,
    -- ADDED 2026-11-01. The AQUAL weak-form contract draft (RN-AQUAL-FIELD-001).
    -- Definitions and one inherited constitutive identity; it does not prove the
    -- field equation, integrability, or that the weak form follows from an action.
    `AQUALWeakFormDraft,
    `InitialAlgebraExecution,
    `ListInitialAlgebra,
    `BinaryPrefixBasis,
    -- RESTORED 2026-11-17: the six roots above were dropped by 95f4578b (E8Roots).
    -- ADDED 2026-11-11. The E8 root system: 240 roots on the doubled integer
    -- lattice, classification, root-system axioms, simple roots + Cartan matrix.
    `E8Roots,
    -- ADDED 2026-11-15. The E8 → SO(10) branching at the weight level:
    -- 248 = (8,1) ⊕ (1,78) ⊕ (3,27) ⊕ (3̄,27̄) under E6 × SU(3), then
    -- E6 ⊃ SO(10) × U(1). Builds on E8Roots.
    `E8Branching,
    -- ADDED 2026-11-17. Octonionic Complex-Hopf S7 isometry, CP2 quaternionic S3
    -- shells, and Z3 <= SU(3) <= G2 diagonal subalgebra selection (BLK-1408, BLK-1411).
    `OctonionHopfShells,
    -- ADDED 2026-11-17. AeST off-shell metric variation chain rule, static spherical
    -- reduction, weak-field condensate/Helmholtz equation, and BLK-1420 benchmark.
    `AeSTWeakFieldCondensate,
    -- ADDED 2026-11-17. Closed-form BSZ auxiliary potential U(nu, mu), secondary
    -- constraints S^(mu)/S^(nu), and C^{AB} invertibility for live mu_std AeST (BLK-1430).
    `AeSTHamiltonianLegendre,
    -- ADDED 2026-11-17. Cassini-SPARC symmetron screening window (2026-11-15 work):
    -- galaxy lower bound, scale upper bound => Cassini 2-sigma, integer witnesses.
    `CassiniSymmetronWindow,
    -- ADDED 2026-11-17. Fu et al. (2024) Eq. (4) vector-variation discrepancy (b vs 2b)
    -- and nonzero constrained Noether/Bianchi residual in 1+1 Minkowski space (PR #215 / BLK-1436 #5).
    `AeSTVectorNoetherResidual,
    -- ADDED 2026-11-17 (Issue #217 / BLK-1443, Muse). Parameterized scalar-channel
    -- calculus normalization J(Y) = 2 lam a^2 F_std(sqrt Y / a); calculus only.
    `AeSTParameterizedNormalization,
    -- ADDED 2026-11-17 (Issue #217 obligations 3-4). Arbitrary-dimension off-shell
    -- diffeomorphism Noether identity, minimal-coupling matter conservation, and C^2
    -- 1+1D curved-metric fderiv verification of div(sqrt(-g) V) and div T = E_chi d chi.
    `AeSTDiffeomorphismNoether,
    -- ADDED 2026-11-17 (PR #210). Adjacent root-data bookkeeping only; not a physical
    -- unification result.
    `StringTheoryBridge,
    -- ADDED 2026-11-17 (Wave 3 #1 BBN bounds + BLK-1450/BLK-1461 E8 x CP2 Spin^c Gate 2).
    -- Pure algebraic/arithmetic bounds on G_cosmo vs J_tot non-folding, zero-sum SU(3) twists,
    -- O(-1)^3/O(-4)^3 uniqueness, and E8 248 vs (27,3) chiral Spin^c charge-locking.
    `Wave3BBNAndSpinCCP2Bounds,
    -- ADDED 2026-11-17 (foundations audit 2026-11-13 Sec. 6 step 1). The canonical
    -- model-identity manifest as one Lean record, with open Sec. 7 questions stored as
    -- open slots. Data plus bookkeeping checks; proves no physics.
    `ModelIdentity,
    -- ADDED 2026-11-17. Wave/AeST theorems restated with their physics literals read
    -- from ModelIdentity.canonical; sabotage_model_identity.sh mutates each field.
    `ModelIdentityBindings,
    -- ADDED 2026-11-19 (O44/O15, BLK-1518/BLK-1522). Spin^c Dirac index polynomial on CP^2
    -- twisted by O(Q), Serre duality Q <-> -3 - Q (h^0=3 vs h^2=3), and Dolan cross-check.
    `CP2SpincIndex,
    -- ADDED 2026-11-19 (O44, BLK-1522). First formalizable chunks (B1-B3) of the
    -- diffeomorphism Noether identity in a t-only reduced 2D model.
    `NoetherScoping,
    -- ADDED 2026-11-19. Postulate R analytic induced-metric brane no-go (even on x >= 0),
    -- J_std''(y) blowup at y -> 0+, and exact analytic auxiliary-susceptibility supremum
    -- F_std(x) = sup over s in 0..1 of (s x^2/2 - (artanh s - s)/2).
    -- (No square brackets in comments here: verify_all_proofs.sh ends the roots range at the first one.)
    `PostulateRAnalyticNoGo,
    -- ADDED 2026-11-20. Single-metric AeST AQUAL & Tidal-QUMOND on-shell anisotropic stress,
    -- (Phi')^2 self-stress cancellation, exact Newtonian/deep-MOND O(v^4/c^4) slip ODEs,
    -- and standalone deep-MOND chi linear-slip no-go.
    `SingleMetricSlipCancellation,
    -- ADDED 2026-11-20. Coupled 2x2 AeST FLRW stability determinant factorization, SZ22 limit,
    -- all-k instability when M_gap^2 < 0, Qbar-independent power-law K_B lower bound, and
    -- universal running-lambda_s(Q) existence criterion (stiff p=2 no-go, global Cosh, AM-GM).
    `CoupledAeSTStabilityBounds
  ]
