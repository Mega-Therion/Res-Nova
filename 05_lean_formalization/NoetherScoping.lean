import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring

/-!
# Noether scoping: first formalizable chunks (Track F, Spin^c CP^2 programme)

Scoping + first chunks for the tensor-level Noether formalization (Safa's
BLK-1449 ask). See `noether-scoping.md` in the same folder for the full
scoping note, the dependency order, and the honest tiering.

## What this module proves

Three derivation steps of the diffeomorphism Noether identity
(`PR217_OBLIGATIONS_VALIDATION_2026-11-17.md`, checks B1–B3), each at the
level that is genuinely formalizable without the missing covariant-calculus
infrastructure:

1. **`vector_sector_identity`** (B1): the vector-sector equivalence
   `E^μ ∇_ν A_μ - ∇_μ(E^μ A_ν) = E^μ F_{νμ} - A_ν ∇_μ E^μ`, proved as
   abstract finite-sum algebra with the Leibniz rule for `∇_μ(E^μ A_ν)`
   as an explicit hypothesis. The calculus content (that `∇` satisfies
   Leibniz) is an input, not proved here.
2. **`symmetric_contraction_fin2`** (B2): a symmetric `E^{μν}` contracts
   only against the symmetric part of `∇_μ ξ_ν`, in the concrete 2-index
   case, by explicit expansion.
3. **`density_divergence`** (B3): the density-divergence identity
   `∂_μ(√-g V^μ) = √-g ∇_μ V^μ` in a concrete symmetry-reduced 2D model:
   diagonal metric `g = diag(-e^{2α(t)}, e^{2β(t)})`, fields depending on
   `t` only. The Christoffel trace components `Γ^0_{00}` and `Γ^1_{10}`
   are **computed from the metric formula** (`gamma000_eq`,
   `gamma110_eq`), not assumed: `Γ^0_{00} = α'`, `Γ^1_{10} = β'`, so the
   trace is `α' + β' = ∂_t log √-g`, and the identity follows by the
   product/chain rule.

## Scope — read before citing

* The density identity is proved in the **t-only reduced model**: the
  `x`-partials vanish by construction (`Γ^0_{01} = Γ^1_{11} = 0`), and the
  `V^1` component drops out identically. The full 2D version (fields of
  `(t, x)`, SymPy check B3) needs Mathlib partial derivatives (`fderiv`)
  and is the next step; it is NOT proved here.
* Nothing here states the AeST action, any field variation, or the full
  Noether identity. The general Lean proof of the Noether identity for the
  complete AeST action remains [O]; see `noether-scoping.md`.
* All theorems compile with `0 sorry` and standard axioms only.
-/

noncomputable section

namespace ResNova.NoetherScoping

/-! ## 1. Vector-sector identity (B1, abstract algebra) -/

/-- B1: the vector-sector equivalence, as abstract finite-sum algebra.
`dνA μ` stands for `∇_ν A_μ`, `dμAν μ` for `∇_μ A_ν`, `divE` for
`∇_μ E^μ`, and `divEA` for `∇_μ (E^μ A_ν)`; the Leibniz rule relating
them is the hypothesis `hleibniz`. With `F_{νμ} = ∇_ν A_μ - ∇_μ A_ν`,
the two sides are the two forms of the vector-sector Noether term. -/
theorem vector_sector_identity {ι : Type*} [Fintype ι] {E dνA dμAν : ι → ℝ}
    {Aν divE divEA : ℝ}
    (hleibniz : divEA = divE * Aν + ∑ μ, E μ * dμAν μ) :
    (∑ μ, E μ * dνA μ) - divEA
      = (∑ μ, E μ * (dνA μ - dμAν μ)) - Aν * divE := by
  have hsum : (∑ μ, E μ * (dνA μ - dμAν μ))
      = (∑ μ, E μ * dνA μ) - ∑ μ, E μ * dμAν μ := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro μ _
    ring
  rw [hleibniz, hsum]
  ring

/-! ## 2. Symmetric contraction (B2, concrete 2-index case) -/

/-- B2: a symmetric `E` contracts only against the symmetric part of `T`.
Concrete `Fin 2` case, by explicit expansion: the off-diagonal terms pair
up via `E 1 0 = E 0 1`. This is the step that turns
`δg^{μν} = -2∇^{(μ}ξ^{ν)}` into the `2∇^μ E_g(μν)` coefficient. -/
theorem symmetric_contraction_fin2 {E T : Fin 2 → Fin 2 → ℝ}
    (hsym : ∀ i j, E i j = E j i) :
    (∑ i, ∑ j, E i j * T i j)
      = ∑ i, ∑ j, E i j * ((T i j + T j i) / 2) := by
  have h10 : E 1 0 = E 0 1 := hsym 1 0
  simp only [Fin.sum_univ_two]
  rw [h10]
  ring

/-! ## 3. Density-divergence identity (B3, t-only reduced 2D model) -/

/-- Metric component `g₀₀ = -e^{2α}` (as a function of `t`). -/
def g00 (α : ℝ → ℝ) : ℝ → ℝ := fun s => -Real.exp (2 * α s)

/-- Metric component `g₁₁ = e^{2β}` (as a function of `t`). -/
def g11 (β : ℝ → ℝ) : ℝ → ℝ := fun s => Real.exp (2 * β s)

/-- Inverse-metric component `g⁰⁰ = -e^{-2α}` at the point `t`. -/
def g00inv (α : ℝ → ℝ) (t : ℝ) : ℝ := -Real.exp (-2 * α t)

/-- Inverse-metric component `g¹¹ = e^{-2β}` at the point `t`. -/
def g11inv (β : ℝ → ℝ) (t : ℝ) : ℝ := Real.exp (-2 * β t)

/-- `∂_t g₀₀ = -2α' e^{2α}`, by the chain rule. -/
theorem deriv_g00 {α : ℝ → ℝ} {α' t : ℝ} (hα : HasDerivAt α α' t) :
    deriv (g00 α) t = -2 * α' * Real.exp (2 * α t) := by
  have h1 : HasDerivAt (fun s => 2 * α s) (2 * α') t := hα.const_mul 2
  have h2 : HasDerivAt (fun s => Real.exp (2 * α s))
      (Real.exp (2 * α t) * (2 * α')) t := h1.exp
  have h3 : HasDerivAt (fun s => -Real.exp (2 * α s))
      (-(Real.exp (2 * α t) * (2 * α'))) t := h2.neg
  have h3' : HasDerivAt (g00 α) (-(Real.exp (2 * α t) * (2 * α'))) t := h3
  rw [h3'.deriv]
  ring

/-- `∂_t g₁₁ = 2β' e^{2β}`, by the chain rule. -/
theorem deriv_g11 {β : ℝ → ℝ} {β' t : ℝ} (hβ : HasDerivAt β β' t) :
    deriv (g11 β) t = 2 * β' * Real.exp (2 * β t) := by
  have h1 : HasDerivAt (fun s => 2 * β s) (2 * β') t := hβ.const_mul 2
  have h2 : HasDerivAt (fun s => Real.exp (2 * β s))
      (Real.exp (2 * β t) * (2 * β')) t := h1.exp
  have h2' : HasDerivAt (g11 β) (Real.exp (2 * β t) * (2 * β')) t := h2
  rw [h2'.deriv]
  ring

/-- Christoffel component `Γ^0_{00} = ½ g⁰⁰ ∂_t g₀₀`, from the metric
formula `Γ^λ_{μν} = ½ g^{λσ}(∂_μ g_{νσ} + ∂_ν g_{μσ} - ∂_σ g_{μν})`
(the `σ = 1` term vanishes since `g⁰¹ = 0`). -/
def Gamma000 (α : ℝ → ℝ) (t : ℝ) : ℝ :=
  (1 / 2) * g00inv α t * deriv (g00 α) t

/-- Christoffel component `Γ^1_{10} = ½ g¹¹ ∂_t g₁₁`, from the metric
formula (the `σ = 0` term vanishes since `g¹⁰ = 0`). -/
def Gamma110 (β : ℝ → ℝ) (t : ℝ) : ℝ :=
  (1 / 2) * g11inv β t * deriv (g11 β) t

/-- The Christoffel component `Γ^0_{00}` computed from the metric is `α'`. -/
theorem gamma000_eq {α : ℝ → ℝ} {α' t : ℝ} (hα : HasDerivAt α α' t) :
    Gamma000 α t = α' := by
  have hexp : Real.exp (-2 * α t) * Real.exp (2 * α t) = 1 := by
    rw [← Real.exp_add]
    have h0 : -2 * α t + 2 * α t = 0 := by ring
    rw [h0, Real.exp_zero]
  unfold Gamma000 g00inv
  rw [deriv_g00 hα]
  calc (1 / 2) * (-Real.exp (-2 * α t)) * (-2 * α' * Real.exp (2 * α t))
      = α' * (Real.exp (-2 * α t) * Real.exp (2 * α t)) := by ring
    _ = α' := by rw [hexp]; ring

/-- The Christoffel component `Γ^1_{10}` computed from the metric is `β'`. -/
theorem gamma110_eq {β : ℝ → ℝ} {β' t : ℝ} (hβ : HasDerivAt β β' t) :
    Gamma110 β t = β' := by
  have hexp : Real.exp (-2 * β t) * Real.exp (2 * β t) = 1 := by
    rw [← Real.exp_add]
    have h0 : -2 * β t + 2 * β t = 0 := by ring
    rw [h0, Real.exp_zero]
  unfold Gamma110 g11inv
  rw [deriv_g11 hβ]
  calc (1 / 2) * Real.exp (-2 * β t) * (2 * β' * Real.exp (2 * β t))
      = β' * (Real.exp (-2 * β t) * Real.exp (2 * β t)) := by ring
    _ = β' := by rw [hexp]; ring

/-- The Christoffel trace in the reduced model is `α' + β' = ∂_t log √-g`.
(The `x`-trace `Γ^0_{01} + Γ^1_{11}` vanishes identically: every
`x`-partial is zero in the t-only model, so it does not appear.) -/
theorem christoffel_trace_eq {α β : ℝ → ℝ} {α' β' t : ℝ}
    (hα : HasDerivAt α α' t) (hβ : HasDerivAt β β' t) :
    Gamma000 α t + Gamma110 β t = α' + β' := by
  rw [gamma000_eq hα, gamma110_eq hβ]

/-- The density-divergence identity in the reduced model:
`∂_t(√-g V⁰) = √-g ∇_t V^t`, where `√-g = e^{α+β}` and the covariant
divergence is `V' + (Γ^0_{00} + Γ^1_{10}) V⁰`. The `V¹` component drops
out identically in the t-only model (`∂_x ≡ 0`, `Γ^1_{11} = 0`), so the
identity is stated for the surviving component. -/
theorem density_divergence {α β V : ℝ → ℝ} {α' β' V' t : ℝ}
    (hα : HasDerivAt α α' t) (hβ : HasDerivAt β β' t)
    (hV : HasDerivAt V V' t) :
    deriv (fun s => Real.exp (α s + β s) * V s) t
      = Real.exp (α t + β t)
          * (V' + (Gamma000 α t + Gamma110 β t) * V t) := by
  rw [christoffel_trace_eq hα hβ]
  have hab : HasDerivAt (fun s => α s + β s) (α' + β') t := hα.add hβ
  have hexp : HasDerivAt (fun s => Real.exp (α s + β s))
      (Real.exp (α t + β t) * (α' + β')) t := hab.exp
  have hmul : HasDerivAt (fun s => Real.exp (α s + β s) * V s)
      (Real.exp (α t + β t) * (α' + β') * V t + Real.exp (α t + β t) * V') t :=
    hexp.mul hV
  rw [hmul.deriv]
  ring

#print axioms vector_sector_identity
#print axioms symmetric_contraction_fin2
#print axioms deriv_g00
#print axioms deriv_g11
#print axioms gamma000_eq
#print axioms gamma110_eq
#print axioms christoffel_trace_eq
#print axioms density_divergence

end ResNova.NoetherScoping
