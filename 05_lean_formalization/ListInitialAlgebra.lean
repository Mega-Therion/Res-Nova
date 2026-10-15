/-
Copyright (c) 2026 R.W. Yett. Released under Apache 2.0.

Constructed initial algebra for one polynomial functor.

F X = Shape α X has two constructors: nil, and cons of a head in α with a tail in X.
The inductive type List α is the carrier. inn and out are defined by the constructors
and proved inverse. fold is the catamorphism, and it is proved unique.
eval is inn. It is proved to be the two-sided inverse of out.

This file does not assume an InitialFAlgebra. It does not construct a final
coalgebra of infinite lists. It does not identify this functor with a physical tensor.
-/

namespace ResNova.Foundations.ListInitialAlgebra

inductive Shape (α : Type) (x : Type) where
  | nil
  | cons (head : α) (tail : x)
  deriving DecidableEq

def mapShape {α x y : Type} (f : x → y) : Shape α x → Shape α y
  | .nil => .nil
  | .cons h t => .cons h (f t)

theorem mapShape_id {α x : Type} (s : Shape α x) : mapShape (id : x → x) s = s := by
  cases s <;> rfl

theorem mapShape_comp {α x y z : Type} (f : x → y) (g : y → z) (s : Shape α x) :
    mapShape (g ∘ f) s = mapShape g (mapShape f s) := by
  cases s <;> rfl

def inn {α : Type} : Shape α (List α) → List α
  | .nil => []
  | .cons h t => h :: t

def out {α : Type} : List α → Shape α (List α)
  | [] => .nil
  | h :: t => .cons h t

theorem out_inn {α : Type} (s : Shape α (List α)) : out (inn s) = s := by
  cases s <;> rfl

theorem inn_out {α : Type} (xs : List α) : inn (out xs) = xs := by
  cases xs <;> rfl

/-- Algebra structure on the initial carrier. This is eval. -/
def eval {α : Type} : Shape α (List α) → List α :=
  inn

theorem eval_out_left {α : Type} (s : Shape α (List α)) : out (eval s) = s :=
  out_inn s

theorem eval_out_right {α : Type} (xs : List α) : eval (out xs) = xs :=
  inn_out xs

def fold {α β : Type} (alg : Shape α β → β) : List α → β
  | [] => alg .nil
  | h :: t => alg (.cons h (fold alg t))

theorem fold_step {α β : Type} (alg : Shape α β → β) (s : Shape α (List α)) :
    fold alg (inn s) = alg (mapShape (fold alg) s) := by
  cases s <;> rfl

theorem fold_unique {α β : Type} (alg : Shape α β → β) (h : List α → β)
    (comm : ∀ s : Shape α (List α), h (inn s) = alg (mapShape h s)) :
    ∀ xs : List α, h xs = fold alg xs := by
  intro xs
  induction xs with
  | nil =>
      have hc := comm .nil
      simpa [inn, mapShape, fold] using hc
  | cons a t ih =>
      have hc := comm (.cons a t)
      have hc' : h (a :: t) = alg (.cons a (h t)) := by
        simpa [inn, mapShape] using hc
      rw [hc', ih]
      rfl

/-- The catamorphism into the algebra (List α, inn) is the identity. -/
theorem fold_inn_id {α : Type} (xs : List α) : fold inn xs = xs := by
  induction xs with
  | nil => rfl
  | cons _ _ ih =>
      simp [fold, inn, ih]

theorem fold_eval_id {α : Type} (xs : List α) : fold (eval (α := α)) xs = xs := by
  simpa [eval] using fold_inn_id xs

/-- Any algebra homomorphism out of List α agrees with fold. -/
theorem execute_unique {α β : Type} (alg : Shape α β → β) (h : List α → β)
    (comm : ∀ s : Shape α (List α), h (inn s) = alg (mapShape h s)) :
    h = fold alg := by
  funext xs
  exact fold_unique alg h comm xs

def execute {α β : Type} (alg : Shape α β → β) : List α → β :=
  fold alg

theorem execute_step {α β : Type} (alg : Shape α β → β) (s : Shape α (List α)) :
    execute alg (eval s) = alg (mapShape (execute alg) s) :=
  fold_step alg s

end ResNova.Foundations.ListInitialAlgebra
