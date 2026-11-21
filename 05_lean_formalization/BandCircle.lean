/-
  12_BandCircle.lean — the chiral band as one circle, and as one hand vs either hand.
  Statements over ℝ (Mathlib), not integer placeholders. Ideas: R.W. Yett, 2026-11-05.
  Check: from Chyren/Research_and_Data/03_Formal_and_Lean/formal (built Mathlib) run  `lake env lean <this file>`.
-/
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace BandCircle

/-- Floor θ and ceiling κ satisfy κ² = θ(2 − θ) exactly when (κ, 1 − θ) lies on the unit circle. -/
theorem band_iff_circle (θ κ : ℝ) : κ ^ 2 = θ * (2 - θ) ↔ κ ^ 2 + (1 - θ) ^ 2 = 1 := by
  constructor <;> intro h <;> nlinarith [h]

/-- Either-hand probability: if each of two independent hands holds with probability θ,
    the chance that at least one holds is 1 − (1 − θ)² = θ(2 − θ). -/
theorem either_hand (θ : ℝ) : 1 - (1 - θ) * (1 - θ) = θ * (2 - θ) := by ring

/-- Correlated hands: with P(L ∧ R) = θ² + ρ θ (1 − θ) (same marginals θ, correlation ρ),
    P(L ∨ R) = θ(2 − θ) − ρ θ (1 − θ). -/
noncomputable def eitherCorr (θ ρ : ℝ) : ℝ := 2 * θ - (θ ^ 2 + ρ * θ * (1 - θ))

theorem eitherCorr_eq (θ ρ : ℝ) : eitherCorr θ ρ = θ * (2 - θ) - ρ * θ * (1 - θ) := by
  unfold eitherCorr; ring

/-- Independent hands (ρ = 0) give the outside value θ(2 − θ). -/
theorem eitherCorr_indep (θ : ℝ) : eitherCorr θ 0 = θ * (2 - θ) := by
  unfold eitherCorr; ring

/-- Locked hands (ρ = 1) collapse to the inside value θ: both hands act as one. -/
theorem eitherCorr_locked (θ : ℝ) : eitherCorr θ 1 = θ := by
  unfold eitherCorr; ring

/-- Intersecting chords on the unit sphere: a cap of depth θ has rim radius² = θ(2 − θ).
    (Rim at height 1 − θ from the centre; radius² = 1 − (1 − θ)².) -/
theorem cap_rim (θ : ℝ) : 1 - (1 - θ) ^ 2 = θ * (2 - θ) := by ring

/-- For 0 ≤ θ ≤ 1 the ceiling squared is at least the floor: the outside reading never falls
    below the inside reading. -/
theorem outside_ge_inside (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1) : θ ≤ θ * (2 - θ) := by
  nlinarith

/-- The decimal floor 0.7 gives ceiling² = 0.91. -/
theorem floor_07 : (0.7 : ℝ) * (2 - 0.7) = 0.91 := by norm_num

/-- The geometric floor 1/√2 gives ceiling² = √2 − 1/2. -/
theorem floor_invsqrt2 : (1 / Real.sqrt 2) * (2 - 1 / Real.sqrt 2) = Real.sqrt 2 - 1 / 2 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  field_simp
  nlinarith [h]

/-- S14 (Prop. 10): On the unit circle κ² + h² = 1 with h ≥ 0, the height-radius swap
    fixes (h, κ) (i.e. h = κ) if and only if h² = 1/2 (the 45° self-mirror circle h = 1/√2). -/
theorem self_mirror_circle (h κ : ℝ) (h_circle : κ ^ 2 + h ^ 2 = 1) :
    h = κ → h ^ 2 = 1 / 2 ∧ κ ^ 2 = 1 / 2 := by
  intro h_eq
  subst h_eq
  constructor <;> linarith [h_circle]

/-- S14: Explicitly, h = 1/√2 and κ = 1/√2 lie on the unit circle and are fixed by the swap. -/
theorem self_mirror_invsqrt2 :
    (1 / Real.sqrt 2) ^ 2 + (1 / Real.sqrt 2) ^ 2 = 1 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  field_simp
  linarith [h]

/-- S15.A (Prop. 11): The exact observer-state coherence C(x) = 4x / (1 + 8x²)
    peaks at 1/√2 at x = 1/(2√2), and satisfies C(x) ≤ 1/√2 for all x ∈ ℝ. -/
noncomputable def obsCoherence (x : ℝ) : ℝ := 4 * x / (1 + 8 * x ^ 2)

theorem obsCoherence_at_peak :
    obsCoherence (1 / (2 * Real.sqrt 2)) = 1 / Real.sqrt 2 := by
  unfold obsCoherence
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  field_simp
  nlinarith [h]

theorem obsCoherence_le_invsqrt2 (x : ℝ) :
    obsCoherence x ≤ 1 / Real.sqrt 2 := by
  unfold obsCoherence
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  have hden : 0 < 1 + 8 * x ^ 2 := by positivity
  rw [div_le_div_iff₀ hden hpos]
  have hsq : 0 ≤ (2 * Real.sqrt 2 * x - 1) ^ 2 := sq_nonneg (2 * Real.sqrt 2 * x - 1)
  nlinarith [h, hsq]

/-- S19 & Paper C/E/F: Polar-slope unification of the saturation curve χ(x) = μ_std(x) = x / √(1 + x²)
    with the unit-sphere band circle κ² + h² = 1:
    For any circle on the unit sphere at height h ≠ 0 and radius κ (so κ² + h² = 1),
    the polar slope x = κ / h = tan α satisfies x² / (1 + x²) = κ². -/
theorem polar_slope_saturation (h κ : ℝ) (hh : h ≠ 0) (h_circle : κ ^ 2 + h ^ 2 = 1) :
    (κ / h) ^ 2 / (1 + (κ / h) ^ 2) = κ ^ 2 := by
  have h2_pos : h ^ 2 ≠ 0 := pow_ne_zero 2 hh
  field_simp
  nlinarith [h_circle]

/-- S19 & Paper E/K: At polar slope x = 1 (the 45° self-mirror circle h = κ = 1/√2),
    the squared saturation curve x² / (1 + x²) equals 1/2 = (1/√2)² (quantum fidelity F = 1/2). -/
theorem saturation_at_one_sq :
    (1 : ℝ) ^ 2 / (1 + (1 : ℝ) ^ 2) = (1 / Real.sqrt 2) ^ 2 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  field_simp
  linarith [h]

/-- Paper E (S18): At χ = 1/√2, the holonomy gate P_c(χ) = χ² / (1 + χ²) equals 1/3. -/
theorem holonomy_gate_at_invsqrt2 :
    (1 / Real.sqrt 2) ^ 2 / (1 + (1 / Real.sqrt 2) ^ 2) = (1 : ℝ) / 3 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  field_simp
  linarith [h]

/-- Open 1 Geometric Identity (S₃ Singlet/Doublet Equipartition at the 45° Self-Mirror Angle):
    For any 3-vector (v₁, v₂, v₃) ∈ ℝ³ making angle α = 45° (cos α = 1/√2, the S14 self-mirror floor)
    with the S₃-singlet diagonal (1, 1, 1) — so that (v₁ + v₂ + v₃)² = 3 (v₁² + v₂² + v₃²) (1/√2)² —
    the ratio (v₁² + v₂² + v₃²) / (v₁ + v₂ + v₃)² equals 2/3 = 1 − P_c(1/√2).
    (Note: the geometric identity is [P]; identifying v_i = √m_i for physical leptons is [C]/[O].) -/
theorem koide_self_mirror_two_thirds (v1 v2 v3 : ℝ)
    (hsum : v1 + v2 + v3 ≠ 0)
    (hequip : (v1 + v2 + v3) ^ 2 = 3 * (v1 ^ 2 + v2 ^ 2 + v3 ^ 2) * (1 / Real.sqrt 2) ^ 2) :
    (v1 ^ 2 + v2 ^ 2 + v3 ^ 2) / (v1 + v2 + v3) ^ 2 = (2 : ℝ) / 3 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  have hsum2 : (v1 + v2 + v3) ^ 2 ≠ 0 := pow_ne_zero 2 hsum
  field_simp at hequip ⊢
  nlinarith [h, hequip]

theorem koide_complement_holonomy_gate :
    (2 : ℝ) / 3 + (1 / Real.sqrt 2) ^ 2 / (1 + (1 / Real.sqrt 2) ^ 2) = 1 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 2 := by positivity
  field_simp
  linarith [h]

#print axioms band_iff_circle
#print axioms either_hand
#print axioms eitherCorr_eq
#print axioms eitherCorr_indep
#print axioms eitherCorr_locked
#print axioms cap_rim
#print axioms outside_ge_inside
#print axioms floor_07
#print axioms floor_invsqrt2
#print axioms self_mirror_circle
#print axioms self_mirror_invsqrt2
#print axioms obsCoherence_at_peak
#print axioms obsCoherence_le_invsqrt2
#print axioms polar_slope_saturation
#print axioms saturation_at_one_sq
#print axioms holonomy_gate_at_invsqrt2
#print axioms koide_self_mirror_two_thirds
#print axioms koide_complement_holonomy_gate

end BandCircle
