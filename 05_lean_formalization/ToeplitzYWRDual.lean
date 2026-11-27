/-
  ToeplitzYWRDual.lean
  Zero-Mathlib Lean 4 formalization of Angle 1:
  Toeplitz / Fejer-Riesz Operator-System Dual of YWR Two-Gauge Kinematics.

  Grounded in:
  - Walter D. van Suijlekom, arXiv:2609.40028 (30 Sep 2026):
      * Theorem 3.1: Toeplitz operator system C(S^1)^(n) Hermitian block signatures
        in {-nm, -nm+2, ..., nm} (nm + 1 path components).
      * Section 4.2: Fejer-Riesz dual C(S^1)_(n) finite-window V_1 determinant winding
        bounded to [-m(n-1), m(n-1)] (2m(n-1) + 1 path components).
  - 05_lean_formalization/DispersionQuadrature.lean ([P]):
      * Exact integer-cleared phase-space quadrature bounds Q_3D^2 in [1, 2].

  Epistemic Scope & Kernel Boundary:
  - [P] Exact zero-Mathlib integer theorems (zero unfinished proof terms,
        complete 22/22 axiom-print coverage) for algebraic V_0 Hermitian signature bounds
        and YWR balance, Fejer-Riesz V_1 bounded winding interval and conjugation closure,
        Fredholm index cancellation Ind(T_f + T_fbar) = -m + m = 0, strict single-channel
        odd-holonomy dispersion inflation (3 * v^2 * biasSq > 0), and exact preservation
        of DispersionQuadrature Q_3D^2 in [1, 2] under two-ended YWR pairing.
        Note: Lean checks the integer/combinatorial algebraic consequences of the closed-form
        index/ceiling functionals, while analytic Gohberg-Krein and Argument Principle zero
        counting on S^1 belong to [E] (arXiv:2609.40028) and [D] (verify_toeplitz_ywr_dual.py).
  - [D] Companion symbolic/matrix check: 02_galaxy_dynamics/verify_toeplitz_ywr_dual.py.
  - [O] Physical application to MSA-3D / RC100 / GAMA galaxy spectroscopy remains open;
        pre-registered P-OM-1 v2 (FAIL) and O4 (CONFOUNDED) remain unmodified.
-/

namespace ToeplitzYWRDual

/-- Helper: every integer square is non-negative (identical to DispersionQuadrature). -/
theorem sq_nonneg_int (x : Int) : 0 ≤ x * x := by
  cases Int.lt_trichotomy x 0 with
  | inl hneg => exact Int.le_of_lt (Int.mul_pos_of_neg_of_neg hneg hneg)
  | inr hrest =>
    cases hrest with
    | inl hzero => rw [hzero]; omega
    | inr hpos => exact Int.le_of_lt (Int.mul_pos hpos hpos)

/-- Helper: `x ≠ 0 → 0 < x * x` over `Int`. -/
theorem sq_pos_of_ne_zero (x : Int) (hx : x ≠ 0) : 0 < x * x := by
  cases Int.lt_trichotomy x 0 with
  | inl hneg => exact Int.mul_pos_of_neg_of_neg hneg hneg
  | inr hrest =>
    cases hrest with
    | inl hzero => exact False.elim (hx hzero)
    | inr hpos => exact Int.mul_pos hpos hpos

/-- Helper: product of non-negative integers is non-negative (core-only proof). -/
theorem mul_nonneg_int (a b : Int) (ha : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ a * b := by
  cases Int.lt_trichotomy a 0 with
  | inl hneg => omega
  | inr hrest =>
    cases hrest with
    | inl hz => rw [hz]; omega
    | inr hpos =>
      cases Int.lt_trichotomy b 0 with
      | inl hbneg => omega
      | inr hbrest =>
        cases hbrest with
        | inl hbz => rw [hbz]; omega
        | inr hbpos => exact Int.le_of_lt (Int.mul_pos hpos hbpos)

-- ============================================================================
-- Section 1: Fredholm Index & Two-Ended YWR Winding Cancellation
-- ============================================================================

/-- Gohberg-Krein Fredholm index of a Hardy-space Toeplitz operator with winding `w`:
    `Ind(T_f) = -w`. -/
def fredholmIndex (w : Int) : Int := -w

/-- Net determinant winding of the two-ended YWR direct-sum gauge `T_f ⊕ T_{f_bar}`. -/
def ywrDirectSumWinding (w : Int) : Int := w + (-w)

/-- Theorem 1a: Conjugate YWR pairing annihilates net determinant winding (`w + (-w) = 0`). -/
theorem ywr_winding_cancels (w : Int) : ywrDirectSumWinding w = 0 := by
  dsimp [ywrDirectSumWinding]
  omega

/-- Theorem 1b: Conjugate YWR pairing annihilates net Fredholm index
    `Ind(T_f ⊕ T_{f_bar}) = Ind(T_f) + Ind(T_{f_bar}) = -w + w = 0`. -/
theorem ywr_fredholm_index_cancels (w : Int) :
    fredholmIndex w + fredholmIndex (-w) = 0 := by
  dsimp [fredholmIndex]
  omega

/-- Theorem 1c: Two-channel Fredholm index vanishes iff the second channel carries
    the exact opposite winding `w2 = -w1`. -/
theorem ywr_fredholm_index_eq_zero_iff (w1 w2 : Int) :
    fredholmIndex w1 + fredholmIndex w2 = 0 ↔ w2 = -w1 := by
  dsimp [fredholmIndex]
  omega

-- ============================================================================
-- Section 2: Fejer-Riesz V_1(C(S^1)_(n), m) Bounded Winding Window (arXiv:2609.40028)
-- ============================================================================

/-- Maximum determinant winding modulus `m * (n - 1)` for `m x m` Laurent polynomials
    with Fourier support `|j| <= n - 1` (van Suijlekom 2026, Sec. 4.2). -/
def fejerRieszCeiling (n m : Nat) : Int := (m : Int) * ((n : Int) - 1)

/-- Membership predicate for `V_1(C(S^1)_(n), m) ~= [-m(n-1), m(n-1)]`. -/
def inFejerRieszV1 (n m : Nat) (w : Int) : Prop :=
  -fejerRieszCeiling n m ≤ w ∧ w ≤ fejerRieszCeiling n m

/-- Theorem 2a: For truncation order `n >= 1`, the Fejer-Riesz ceiling is non-negative. -/
theorem fejerRieszCeiling_nonneg (n m : Nat) (hn : 1 ≤ n) :
    0 ≤ fejerRieszCeiling n m := by
  dsimp [fejerRieszCeiling]
  have hm : (0 : Int) ≤ (m : Int) := by omega
  have hn' : (0 : Int) ≤ (n : Int) - 1 := by omega
  exact mul_nonneg_int (m : Int) ((n : Int) - 1) hm hn'

/-- Theorem 2b: For `n >= 2` and matrix size `m >= 1`, non-trivial winding classes exist
    (`0 < m * (n - 1)`). -/
theorem fejerRieszCeiling_pos (n m : Nat) (hn : 2 ≤ n) (hm : 1 ≤ m) :
    0 < fejerRieszCeiling n m := by
  dsimp [fejerRieszCeiling]
  have hm' : (0 : Int) < (m : Int) := by omega
  have hn' : (0 : Int) < (n : Int) - 1 := by omega
  exact Int.mul_pos hm' hn'

/-- Theorem 2c: The trivial 0-winding class lies inside `V_1(C(S^1)_(n), m)` for all `n >= 1`. -/
theorem fejerRieszV1_zero_mem (n m : Nat) (hn : 1 ≤ n) :
    inFejerRieszV1 n m 0 := by
  have hc := fejerRieszCeiling_nonneg n m hn
  dsimp [inFejerRieszV1]
  omega

/-- Theorem 2d: Complex conjugation `w ↦ -w` preserves the Fejer-Riesz `V_1` window. -/
theorem fejerRieszV1_conj_closed (n m : Nat) (w : Int)
    (hw : inFejerRieszV1 n m w) : inFejerRieszV1 n m (-w) := by
  dsimp [inFejerRieszV1] at hw ⊢
  omega

/-- Theorem 2e: Pairing any Fejer-Riesz channel `w` in `M_m(C(S^1)_(n))` with its conjugate
    `-w` in the doubled YWR block `M_{2m}(C(S^1)_(n))` lands in the trivial 0-winding
    component of `V_1(C(S^1)_(n), 2m)`. -/
theorem fejerRieszV1_ywr_double_channel_trivial (n m : Nat) (hn : 1 ≤ n)
    (w : Int) (_hw : inFejerRieszV1 n m w) :
    inFejerRieszV1 n (2 * m) (ywrDirectSumWinding w) ∧ ywrDirectSumWinding w = 0 := by
  have h0 : ywrDirectSumWinding w = 0 := ywr_winding_cancels w
  constructor
  · rw [h0]
    exact fejerRieszV1_zero_mem n (2 * m) hn
  · exact h0

/-- Theorem 2f: Exact integer cardinality of `V_1(C(S^1)_(n), m)` is `2m(n-1) + 1`. -/
theorem fejerRieszV1_span_count (n m : Nat) :
    fejerRieszCeiling n m - (-fejerRieszCeiling n m) + 1 =
      2 * (m : Int) * ((n : Int) - 1) + 1 := by
  dsimp [fejerRieszCeiling]
  grind

-- ============================================================================
-- Section 3: Toeplitz V_0(C(S^1)^(n), m) Hermitian Signatures (arXiv:2609.40028 Thm 3.1)
-- ============================================================================

/-- Matrix signature `p - q` of a non-singular Hermitian block Toeplitz matrix with `p`
    positive and `q` negative eigenvalues. -/
def toeplitzSig (p q : Nat) : Int := (p : Int) - (q : Int)

/-- Theorem 3a: For `p + q = n * m`, Hermitian block Toeplitz signature lies in `[-nm, nm]`
    and obeys even-shift parity `s + nm = 2p` (yielding exactly `nm + 1` components). -/
theorem toeplitzSig_bounds_and_parity (n m p q : Nat) (hpq : p + q = n * m) :
    -((n * m : Nat) : Int) ≤ toeplitzSig p q ∧
    toeplitzSig p q ≤ ((n * m : Nat) : Int) ∧
    toeplitzSig p q + ((n * m : Nat) : Int) = 2 * (p : Int) := by
  dsimp [toeplitzSig]
  constructor
  · omega
  · constructor
    · omega
    · omega

/-- Theorem 3b: The Hermitian dilation / dual-channel block `(p, q) ⊕ (q, p)` has
    identically zero signature. -/
theorem toeplitzSig_ywr_hermitian_balanced (p q : Nat) :
    toeplitzSig (p + q) (q + p) = 0 := by
  dsimp [toeplitzSig]
  omega

-- ============================================================================
-- Section 4: Finite-Window Odd-Holonomy Dispersion Bias & DispersionQuadrature Bridge
-- ============================================================================

/-- Exact phase-space kinetic denominator & numerator (definitionally identical to
    `DispersionQuadrature.denPhase` and `DispersionQuadrature.numPhase`). -/
def denPhase (v sig : Int) : Int := v * v + 3 * (sig * sig)
def numPhase (v sig : Int) : Int := v * v + 6 * (sig * sig)

/-- General squared-variable phase-space polynomials supporting additive variance bias
    `sigSq_obs = sig^2 + biasSq`. -/
def denPhaseSq (vSq sigSq : Int) : Int := vSq + 3 * sigSq
def numPhaseSq (vSq sigSq : Int) : Int := vSq + 6 * sigSq

theorem denPhaseSq_eq_denPhase (v sig : Int) :
    denPhaseSq (v * v) (sig * sig) = denPhase v sig := rfl

theorem numPhaseSq_eq_numPhase (v sig : Int) :
    numPhaseSq (v * v) (sig * sig) = numPhase v sig := rfl

/-- Finite-window odd-holonomy dispersion variance bias `(c * w)^2` induced by aperture
    coupling `c` and net channel winding `w`. -/
def holonomyBiasSq (c w : Int) : Int := (c * w) * (c * w)

/-- Theorem 4a: Non-zero aperture coupling `c ≠ 0` and non-zero winding `w ≠ 0` create a
    strictly positive finite-window dispersion bias `holonomyBiasSq c w > 0`. -/
theorem holonomyBiasSq_pos (c w : Int) (hc : c ≠ 0) (hw : w ≠ 0) :
    0 < holonomyBiasSq c w := by
  dsimp [holonomyBiasSq]
  have hcw : c * w ≠ 0 := by
    intro h
    cases Int.mul_eq_zero.mp h with
    | inl h1 => exact hc h1
    | inr h2 => exact hw h2
  exact sq_pos_of_ne_zero (c * w) hcw

/-- Theorem 4b: Two-ended YWR winding cancellation annihilates the odd-holonomy bias. -/
theorem holonomyBiasSq_zero_of_ywr (c w : Int) :
    holonomyBiasSq c (ywrDirectSumWinding w) = 0 := by
  rw [ywr_winding_cancels]
  dsimp [holonomyBiasSq]
  omega

/-- Theorem 4c (Exact Cross-Multiplied Dispersion-Bias Identity):
    Inflating `sigSq` by `biasSq` shifts `Q_3D^2` by exact cross-difference
    `3 * vSq * biasSq`. -/
theorem q3d_disp_bias_cross_diff (vSq s0Sq biasSq : Int) :
    numPhaseSq vSq (s0Sq + biasSq) * denPhaseSq vSq s0Sq -
    numPhaseSq vSq s0Sq * denPhaseSq vSq (s0Sq + biasSq) =
      3 * vSq * biasSq := by
  dsimp [numPhaseSq, denPhaseSq]
  grind

/-- Theorem 4d (Single-Channel Odd-Holonomy Inflation Theorem):
    For any rotating system (`v ≠ 0`), non-zero aperture coupling (`c ≠ 0`), and non-zero
    single-channel winding (`w ≠ 0`), finite-window bias strictly inflates `Q_3D^2` above
    its intrinsic value. -/
theorem single_channel_holonomy_inflates_q3d (v sig c w : Int)
    (hv : v ≠ 0) (hc : c ≠ 0) (hw : w ≠ 0) :
    numPhase v sig * denPhaseSq (v * v) (sig * sig + holonomyBiasSq c w) <
    numPhaseSq (v * v) (sig * sig + holonomyBiasSq c w) * denPhase v sig := by
  rw [← numPhaseSq_eq_numPhase, ← denPhaseSq_eq_denPhase]
  have hid := q3d_disp_bias_cross_diff (v * v) (sig * sig) (holonomyBiasSq c w)
  have hvpos : 0 < v * v := sq_pos_of_ne_zero v hv
  have hbpos : 0 < holonomyBiasSq c w := holonomyBiasSq_pos c w hc hw
  have h3v : 0 < 3 * (v * v) := by omega
  have hprod : 0 < 3 * (v * v) * holonomyBiasSq c w := Int.mul_pos h3v hbpos
  omega

/-- Theorem 4e (Two-Ended YWR Gauge Preservation of `DispersionQuadrature`):
    Pairing `T_f ⊕ T_{f_bar}` restores the exact unshifted `denPhase`, `numPhase`,
    and universal `Q_3D^2 ∈ [1, 2]` enclosure (`denPhase ≤ numPhase ≤ 2 * denPhase`). -/
theorem ywr_dual_preserves_q3d_enclosure (v sig c w : Int) :
    denPhaseSq (v * v) (sig * sig + holonomyBiasSq c (ywrDirectSumWinding w)) = denPhase v sig ∧
    numPhaseSq (v * v) (sig * sig + holonomyBiasSq c (ywrDirectSumWinding w)) = numPhase v sig ∧
    denPhase v sig ≤ numPhase v sig ∧
    numPhase v sig ≤ 2 * denPhase v sig := by
  rw [holonomyBiasSq_zero_of_ywr]
  have hv := sq_nonneg_int v
  have hs := sq_nonneg_int sig
  dsimp [denPhaseSq, numPhaseSq, denPhase, numPhase]
  constructor
  · omega
  · constructor
    · omega
    · constructor
      · omega
      · omega

/-- Theorem 4f (Cold-Disk `< 3%` Enclosure Preservation Under YWR Pairing):
    If `V >= 10 * sigma_0`, two-ended YWR pairing preserves `103 * numPhase <= 106 * denPhase`. -/
theorem ywr_dual_preserves_cold_disk_enclosure (v sig c w : Int)
    (hcold : 100 * (sig * sig) ≤ v * v) :
    103 * numPhaseSq (v * v) (sig * sig + holonomyBiasSq c (ywrDirectSumWinding w)) ≤
    106 * denPhaseSq (v * v) (sig * sig + holonomyBiasSq c (ywrDirectSumWinding w)) := by
  rw [holonomyBiasSq_zero_of_ywr]
  dsimp [numPhaseSq, denPhaseSq]
  omega

-- Complete axiom-print verification across all 22 theorems in this module
#print axioms sq_nonneg_int
#print axioms sq_pos_of_ne_zero
#print axioms mul_nonneg_int
#print axioms ywr_winding_cancels
#print axioms ywr_fredholm_index_cancels
#print axioms ywr_fredholm_index_eq_zero_iff
#print axioms fejerRieszCeiling_nonneg
#print axioms fejerRieszCeiling_pos
#print axioms fejerRieszV1_zero_mem
#print axioms fejerRieszV1_conj_closed
#print axioms fejerRieszV1_ywr_double_channel_trivial
#print axioms fejerRieszV1_span_count
#print axioms toeplitzSig_bounds_and_parity
#print axioms toeplitzSig_ywr_hermitian_balanced
#print axioms denPhaseSq_eq_denPhase
#print axioms numPhaseSq_eq_numPhase
#print axioms holonomyBiasSq_pos
#print axioms holonomyBiasSq_zero_of_ywr
#print axioms q3d_disp_bias_cross_diff
#print axioms single_channel_holonomy_inflates_q3d
#print axioms ywr_dual_preserves_q3d_enclosure
#print axioms ywr_dual_preserves_cold_disk_enclosure

end ToeplitzYWRDual
