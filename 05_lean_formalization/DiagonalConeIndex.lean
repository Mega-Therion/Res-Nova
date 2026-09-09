/-!
# DiagonalConeIndex — Z3 orbifold diagonal-forcing theorem, ported and labeled

Ported 2026-09-09 from
`Chyren/Research_and_Data/01_Bob_Packages/archive_previous_iterations/2026-08-02_decomposition/lean_repo/GenerationIndex.lean`
(RY, 2026-07-27; originally namespaced `GenerationIndex`, renamed here to avoid
collision with `Res-Nova/05_lean_formalization/GenerationIndex.lean`, which
holds an unrelated and separately-corrected file). Mechanical content
unchanged from the archived original. Re-verified before porting: compiles
clean on the pinned toolchain, no `sorry`, `DiagonalForced` depends only on
`propext`, and a sabotage probe (swapping `cy`/`isolated` for unrelated
predicates) makes the same-shaped claim fail to `decide` — confirming this is
not the `3 = 3` pattern found and corrected in `GenerationIndex.lean` and
`CartanTrialityGenerations.lean` today.

## What is genuinely proved here (§1–4, §6)

`DiagonalForced` is a real, non-tautological result: exhaustive enumeration
over all 27 weight triples in `Fin 3 × Fin 3 × Fin 3` shows the CY-admissible
condition (`cy`, sum ≡ 0 mod 3) together with the isolated-tear condition
(`isolated`, no zero component) force exactly two triples — (1,1,1) and
(2,2,2) — out of 27. `QuantizationTheorem`, `IsolatedGivesThree`,
`ExtendedGivesZero`, and `AbsNetThree` are consequences of this same
enumeration against the `net` function, which is itself the standard
identification (Z3 orbifold/DDM literature: net chirality ±3 at an isolated
CY-admissible fixed point, 0 at an extended one) — not an arbitrary choice
retrofitted to the answer. `SignMirror`/`MirrorVacua` follow mechanically.

## What is bookkeeping, not derived in this file (§5)

`CenterLadder`, `CoxeterNumbers`, `RootSquare`, `ControlDim` assert that
hand-typed `Nat` literals equal themselves — the same *shape* as the vacuous
theorems corrected elsewhere in this gate today. The difference: those
literals are not invented for this file. They transcribe results from an
independent numeric computation (explicit E8 root system, 240 roots verified
norm²=2, Cartan determinant=1, true Coxeter element of order h=30 with the
correct exponent set {1,7,11,13,17,19,23,29} — a first attempt used a wrong
basis giving a fake order-24 element, caught and fixed before any number here
was trusted) documented in
`Chyren_Second_Brain/10_Notes/SPEC — Computing the Chiral Generation Index on
the E8 Stiefel Substrate.md`. That the Coxeter-twist fixed-point counts on
E6/E7/E8 equal 3/2/1 is not a coincidence invented for this corpus — it is the
standard Lie-theory fact that `|det(1 − c)|` on a simply-laced root lattice
equals `det(Cartan) = |Z(G)|`, and `Z(E6) ≅ Z₃, Z(E7) ≅ Z₂, Z(E8) = 1` are
textbook. But **Lean does not verify the root-system computation itself** —
that lives in Python, outside this kernel-checked chain, and is asserted here,
not proved here. Treat §5 as a verified-elsewhere citation, not a Lean result.

## The one open premise the whole chain rests on

The biconditional above is unconditional finite math: `isolated ⟺ diagonal`
is [thm], full stop. What is NOT established, here or anywhere in this
corpus, is that the *physical* symmetry-breaking mechanism actually produces
an isolated tear at the origin. That premise is [thm] only for the specific
Coxeter maximal twist (proved separately, in the Python computation cited
above — the twist's fixed-point count on the E8 torus is uniquely 1, the
origin); it remains [conj] for RY's full decompression-map mechanism. If that
premise holds, `|net generations| = 3` follows from real math. If it doesn't,
nothing here says it does. This file proves the conditional, not the premise.

Scope: a local ℂ³/Z₃ orbifold model. Not a claim about the full V₂₄₀
substrate or a completed derivation of the Standard Model's 3 fermion
generations.
-/

namespace DiagonalConeIndex

-- ---------------------------------------------------------------------------
-- §1  CY-admissible Z3 weight triples: a+b+c ≡ 0 (mod 3)
-- ---------------------------------------------------------------------------
def cy (a b c : Fin 3) : Prop := (a.val + b.val + c.val) % 3 = 0

instance (a b c : Fin 3) : Decidable (cy a b c) := by
  unfold cy; infer_instance

-- ---------------------------------------------------------------------------
-- §2  Isolated-tear condition: no zero weight
--     (a zero weight fixes a complex line ⟹ extended singular locus)
-- ---------------------------------------------------------------------------
def isolated (a b c : Fin 3) : Prop := a ≠ 0 ∧ b ≠ 0 ∧ c ≠ 0

instance (a b c : Fin 3) : Decidable (isolated a b c) := by
  unfold isolated; infer_instance

-- ---------------------------------------------------------------------------
-- §3  MAIN THEOREM: CY + isolated forces the diagonal twist
--     (exhaustive check over all 27 triples -- genuine, sabotage-tested)
-- ---------------------------------------------------------------------------
theorem DiagonalForced :
    ∀ a b c : Fin 3,
      (cy a b c ∧ isolated a b c) ↔
      ((a = 1 ∧ b = 1 ∧ c = 1) ∨ (a = 2 ∧ b = 2 ∧ c = 2)) := by
  decide

-- ---------------------------------------------------------------------------
-- §4  Net generation number (audit table):
--     net(1,1,1) = -3, net(2,2,2) = +3, all other triples = 0
-- ---------------------------------------------------------------------------
def net (a b c : Fin 3) : Int :=
  match a, b, c with
  | 1, 1, 1 => -3
  | 2, 2, 2 => 3
  | _, _, _ => 0

theorem QuantizationTheorem :
    ∀ a b c : Fin 3, cy a b c →
      net a b c = 0 ∨ net a b c = 3 ∨ net a b c = -3 := by
  decide

theorem IsolatedGivesThree :
    ∀ a b c : Fin 3, cy a b c → isolated a b c →
      net a b c = 3 ∨ net a b c = -3 := by
  decide

theorem ExtendedGivesZero :
    ∀ a b c : Fin 3, cy a b c → ¬ isolated a b c →
      net a b c = 0 := by
  decide

theorem AbsNetThree :
    ∀ a b c : Fin 3, cy a b c →
      ((net a b c).natAbs = 3 ↔ isolated a b c) := by
  decide

-- ---------------------------------------------------------------------------
-- §5  BOOKKEEPING, NOT DERIVED HERE. See header: values transcribed from an
-- independent Python E8 root-system computation, not computed by this file.
-- ---------------------------------------------------------------------------
def coxeterH_E6 : Nat := 12
def coxeterH_E7 : Nat := 18
def coxeterH_E8 : Nat := 30

-- Fixed points of the Coxeter twist on the maximal torus = connection index
def coxeterFP_E6 : Nat := 3
def coxeterFP_E7 : Nat := 2
def coxeterFP_E8 : Nat := 1

theorem CenterLadder_TRANSCRIBED_NOT_DERIVED :
    coxeterFP_E6 = 3 ∧ coxeterFP_E7 = 2 ∧ coxeterFP_E8 = 1 := by
  decide

theorem CoxeterNumbers_TRANSCRIBED_NOT_DERIVED :
    coxeterH_E6 = 12 ∧ coxeterH_E7 = 18 ∧ coxeterH_E8 = 30 := by
  decide

-- E8 root count and moduli square (57600, NOT the retired 58000)
def e8Roots : Nat := 240
def bigN    : Nat := 57600

theorem RootSquare : bigN = e8Roots * e8Roots := by decide

-- Consistency with Gods.lean §17: control dimension 2m − 3 = 477
theorem ControlDim : 2 * 240 - 3 = 477 := by decide

-- ---------------------------------------------------------------------------
-- §6  Chirallic doubling / antimatter vacuum -- genuine, follows from §1-4
-- ---------------------------------------------------------------------------
theorem MirrorWeight : (2 : Fin 3) = -1 := by decide

def net111 : Int := net 1 1 1
def net222 : Int := net 2 2 2

theorem SignMirror : net111 + net222 = 0 := by decide

theorem MirrorVacua : net111 = -3 ∧ net222 = 3 ∧ net111 + net222 = 0 := by
  decide

end DiagonalConeIndex
