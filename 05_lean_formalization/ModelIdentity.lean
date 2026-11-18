/-
  ModelIdentity.lean — canonical model-identity manifest (v1.0.0, 2026-11-17)

  Closure step 1 of `audits/PHYSICS_FOUNDATIONS_AUDIT_2026-11-13.md` §6:
  "Publish a versioned manifest naming the spacetime, internal geometry, gauge group,
  physical fields, matter metric, units, symmetry group, and the boundary between
  established framework and novel hypotheses."

  This file is that manifest as one Lean record, `canonical : ModelIdentity`.
  `ModelIdentityBindings.lean` restates the Wave/AeST theorems with their physics
  literals read from `canonical`, so changing a field here breaks the proofs that
  depend on it (`scripts/sabotage_model_identity.sh` checks this in CI).

  Sources for every value (read 2026-11-17):
  * `CURRENT_STATE_READ_THIS_FIRST.md` (a₀ headline 1.1607e-10 m/s², μ_std live, two
    irreducible inputs a₀ and the μ choice, V₂(ℝ³) substrate, AeST covariant completion);
  * `TARGET_D7_COVARIANT_COMPLETION.md` §1 (Skordis–Złośnik AeST action, A^μA_μ = −1,
    matter minimally coupled to g_μν, parameters (K_B, K₂, Q₀, λ_s));
  * `IMPORTED_STANDARD_MODEL.md` (SU(3)×SU(2)×U(1), [C]);
  * `EPISTEMIC_TIER_LEGEND.md` (tier vocabulary).

  What this file is NOT: it proves no physics. The record is data. Its theorems are
  bookkeeping checks (`[arith]`) about the record itself. Questions the audit lists as
  open (§7) are stored as `Slot.open` with the question text, never as a guessed value.
-/
import SZStdEmbedding

namespace ResNova.ModelIdentity

/-- Canonical epistemic tiers (`EPISTEMIC_TIER_LEGEND.md`). -/
inductive Tier
  | P | D | Dstar | C | conj | E | O | X | A | arith
  deriving DecidableEq, Repr

/-- Which side of the established-vs-novel boundary an item sits on. -/
inductive Boundary
  /-- Standard physics imported from the literature or a measurement. -/
  | established
  /-- A Res-Nova hypothesis, not part of the established framework. -/
  | novel
  deriving DecidableEq, Repr

/-- A manifest entry: either a fixed value with its tier, boundary side and source file,
or an explicitly open question. An open slot carries no value at all. -/
inductive Slot (α : Type)
  | fixed (value : α) (tier : Tier) (side : Boundary) (source : String)
  | open (question : String)

namespace Slot

def isOpen {α : Type} : Slot α → Bool
  | .fixed .. => false
  | .open _ => true

def tier? {α : Type} : Slot α → Option Tier
  | .fixed _ t _ _ => some t
  | .open _ => none

def side? {α : Type} : Slot α → Option Boundary
  | .fixed _ _ s _ => some s
  | .open _ => none

end Slot

/-- Gauge-group factors. -/
inductive GaugeFactor
  | SU (n : ℕ)
  | U1
  deriving DecidableEq, Repr

/-- Physical field content of the gravitational sector. -/
inductive Field
  /-- Spacetime metric `g_μν`. -/
  | metric
  /-- AeST scalar `φ`. -/
  | scalarPhi
  /-- AeST unit-timelike vector `A_μ`. -/
  | aetherVector
  /-- Lagrange multiplier `λ` enforcing the vector norm. -/
  | normMultiplier
  /-- Imported Standard-Model matter (`IMPORTED_STANDARD_MODEL.md`). -/
  | smMatter
  deriving DecidableEq, Repr

/-- How matter couples to geometry. -/
inductive MatterCoupling
  /-- Matter action `S_m[g]`, minimally coupled to `g_μν`. -/
  | minimal
  /-- A disformal matter metric `g̃ ≠ g` (the retired pre-2026-09-12 D7 action). -/
  | disformal
  deriving DecidableEq, Repr

/-- The interpolating-function choice (irreducible parameter 2). -/
inductive MuChoice
  /-- `μ_std(x) = x / √(1 + x²)` (live). -/
  | muStd
  /-- `μ_simple(x) = x / (1 + x)` (literature "simple"; not live). -/
  | muSimple
  deriving DecidableEq, Repr

/-- The function a `MuChoice` names. -/
noncomputable def MuChoice.eval : MuChoice → ℝ → ℝ
  | .muStd => SZStdEmbedding.muStd
  | .muSimple => fun x => x / (1 + x)

/-- Spacetime symmetry. -/
inductive SpacetimeSymmetry
  /-- Diffeomorphism invariance of the four-dimensional action. -/
  | diffeomorphism
  deriving DecidableEq, Repr

/-- Irreducible inputs. The standing accounting is TWO; "zero free parameters" is retired. -/
inductive IrreducibleParameter
  /-- The acceleration scale `a₀` (measured input; the `1/2π` horizon anchor is open). -/
  | a0Scale
  /-- The functional choice `μ`. -/
  | interpolationChoice
  deriving DecidableEq, Repr

/-- Named AeST action parameters (`TARGET_D7` §1, retraction 2). -/
inductive AeSTParameter
  | K_B | K2 | Q0 | lambdaS
  deriving DecidableEq, Repr

/-- An SI quantity `mantissa × 10^exponent` in the named unit. -/
structure SIValue where
  mantissa : ℚ
  exponent : ℤ
  unit : String
  deriving Repr

/-- The model-identity manifest. -/
structure ModelIdentity where
  version : String
  -- spacetime
  spacetimeDim : ℕ
  /-- `(number of negative, number of positive)` eigenvalues; mostly-plus. -/
  signature : ℕ × ℕ
  symmetry : SpacetimeSymmetry
  -- fields and couplings
  fields : List Field
  /-- The vector norm `A^μ A_μ` fixed by the multiplier. -/
  aetherNorm : ℤ
  matterCoupling : MatterCoupling
  aestParameters : List AeSTParameter
  -- gauge sector
  gaugeGroup : Slot (List GaugeFactor)
  /-- Number of chiral fermion generations the model must reproduce. -/
  generationTarget : Slot ℕ
  e8Role : Slot String
  -- internal geometry
  substrate : Slot String
  internalSpaceX : Slot String
  geometryToSpectrumRoute : Slot String
  chiralitySignRule : Slot String
  -- constitutive sector and units
  interpolation : Slot MuChoice
  a0 : Slot SIValue
  a0TwoPiNormalization : Slot String
  irreducibleParameters : List IrreducibleParameter
  singleBranchAllRegimes : Slot String

/-- The canonical instance. Every `.open` slot quotes an audit §7 question or a
CURRENT_STATE `[O]` item. -/
def canonical : ModelIdentity where
  version := "1.0.0 (2026-11-17)"
  spacetimeDim := 4
  signature := (1, 3)
  symmetry := .diffeomorphism
  fields := [.metric, .scalarPhi, .aetherVector, .normMultiplier, .smMatter]
  aetherNorm := -1
  matterCoupling := .minimal
  aestParameters := [.K_B, .K2, .Q0, .lambdaS]
  gaugeGroup := .fixed [.SU 3, .SU 2, .U1] .C .established "IMPORTED_STANDARD_MODEL.md"
  generationTarget := .fixed 3 .E .established "IMPORTED_STANDARD_MODEL.md (three observed generations)"
  e8Role := .open
    "Is E8xE8 the actual heterotic gauge group, a four-dimensional global symmetry, or a geometric scaffold only? (audit 2026-11-13 §7)"
  substrate := .fixed "V2(R^3) via Cartan triality (V240 retired 2026-08-25)" .conj .novel
    "CURRENT_STATE §2"
  internalSpaceX := .open
    "What is the current internal space X or equivalent compactification object, and what fermion bundle/operator lives on it? (audit §7)"
  geometryToSpectrumRoute := .open
    "Route (a) V2(R^3)/triality action on bundles and modes, or (b) a heterotic (X,V) compactification and its index: not chosen (audit §6 step 2)"
  chiralitySignRule := .open
    "What is the dynamical selection rule for the sign/orientation of the chiral spectrum? (audit §7)"
  interpolation := .fixed .muStd .A .novel "CURRENT_STATE §1 (mu_std live on galaxies, [A])"
  a0 := .fixed ⟨11607 / 10000, -10, "m s^-2"⟩ .E .established
    "A0_DISTANCE_CORRECTED_2026-09-16.json T1 (mu_std, 175 SPARC galaxies)"
  a0TwoPiNormalization := .open
    "What independent mechanism, if any, yields the 1/(2 pi) in a0? (O1; audit §7)"
  irreducibleParameters := [.a0Scale, .interpolationChoice]
  singleBranchAllRegimes := .open
    "What single action yields the observed galaxy interpolation while remaining consistent with the Solar System and the AeST/cosmological sector? (audit §7; bare mu_std fails the Cassini EFE quadrupole)"

/-! ## Bookkeeping checks on the record (`[arith]`) -/

/-- The signature accounts for every spacetime dimension. -/
theorem canonical_signature_fills_dim :
    canonical.signature.1 + canonical.signature.2 = canonical.spacetimeDim := by
  decide

/-- Lorentzian: exactly one timelike direction. -/
theorem canonical_lorentzian : canonical.signature.1 = 1 := by decide

/-- Two irreducible inputs: not parameter-free, and not more than two. -/
theorem canonical_two_irreducible_parameters :
    canonical.irreducibleParameters.length = 2 := by decide

theorem canonical_not_parameter_free : canonical.irreducibleParameters ≠ [] := by decide

/-- The six §7 questions stay open in v1.0.0. -/
theorem canonical_open_questions :
    canonical.e8Role.isOpen = true ∧ canonical.internalSpaceX.isOpen = true ∧
    canonical.geometryToSpectrumRoute.isOpen = true ∧
    canonical.chiralitySignRule.isOpen = true ∧
    canonical.a0TwoPiNormalization.isOpen = true ∧
    canonical.singleBranchAllRegimes.isOpen = true := by
  decide

/-- The novel side of the boundary: the substrate and the μ choice. -/
theorem canonical_novel_items :
    canonical.substrate.side? = some .novel ∧ canonical.interpolation.side? = some .novel := by
  decide

/-- The established side: the gauge group, the generation count and the a₀ measurement. -/
theorem canonical_established_items :
    canonical.gaugeGroup.side? = some .established ∧
    canonical.generationTarget.side? = some .established ∧
    canonical.a0.side? = some .established := by
  decide

/-! ## Accessors used by the bindings. Each returns the fixed value; an open slot has none. -/

def Slot.value? {α : Type} : Slot α → Option α
  | .fixed v _ _ _ => some v
  | .open _ => none

/-- Generation target as an integer (`0` would only arise if the slot were reopened). -/
def generationTargetZ (M : ModelIdentity) : ℤ := ((M.generationTarget.value?).getD 0 : ℕ)

/-- The live interpolating function. Falls back to `μ_simple` only if the slot is reopened,
which `ModelIdentityBindings` would then reject. -/
noncomputable def mu (M : ModelIdentity) : ℝ → ℝ :=
  ((M.interpolation.value?).getD .muSimple).eval

/-- a₀ in SI (m s⁻²) as a real number. -/
noncomputable def a0SI (M : ModelIdentity) : ℝ :=
  match M.a0.value? with
  | some v => (v.mantissa : ℝ) * (10 : ℝ) ^ v.exponent
  | none => 0

theorem canonical_generationTargetZ : generationTargetZ canonical = 3 := by decide

theorem canonical_mu : mu canonical = SZStdEmbedding.muStd := rfl

theorem canonical_a0SI : a0SI canonical = (11607 / 10000 : ℝ) * (10 : ℝ) ^ (-10 : ℤ) := by
  simp [a0SI, canonical, Slot.value?]

#print axioms canonical_signature_fills_dim
#print axioms canonical_lorentzian
#print axioms canonical_two_irreducible_parameters
#print axioms canonical_not_parameter_free
#print axioms canonical_open_questions
#print axioms canonical_novel_items
#print axioms canonical_established_items
#print axioms canonical_generationTargetZ
#print axioms canonical_mu
#print axioms canonical_a0SI

end ResNova.ModelIdentity
