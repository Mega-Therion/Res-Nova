/-
Copyright (c) 2026 R.W. Yett, Claude Code CLI, Antigravity CLI. Released under Apache 2.0.

# Initial Algebras, Final Coalgebras, and the Execution Morphism (Algorithm as Poetry)

Formalizes the core mathematical correspondence between:
1. **Algorithm / Blueprint / Syntax**: Initial algebra (μF, in) of an endofunctor F.
2. **Execution / Dynamics / Behavior**: Final coalgebra (νF, out) of F.
3. **Lambek's Lemma**: The initial algebra morphism `in : F(μF) → μF` is an isomorphism.
4. **Execution Morphism**: The canonical, unique homomorphism `execute : μF → νF`
   intertwining syntactic construction with dynamical evaluation.
-/

namespace ResNova.Foundations.InitialAlgebraExecution

universe u

/-! ### 1. Endofunctors on Type u -/

/-- An endofunctor on `Type u`. -/
structure Endofunctor (F : Type u → Type u) where
  map : ∀ {α β : Type u}, (α → β) → F α → F β
  map_id : ∀ {α : Type u} (x : F α), map id x = x
  map_comp : ∀ {α β γ : Type u} (f : α → β) (g : β → γ) (x : F α),
    map (g ∘ f) x = map g (map f x)

/-! ### 2. F-Algebras and Homomorphisms -/

/-- An F-algebra: carrier object together with structure map `act : F carrier → carrier`. -/
structure FAlgebra (F : Type u → Type u) where
  carrier : Type u
  act : F carrier → carrier

/-- A homomorphism of F-algebras. -/
structure FAlgebraHom {F : Type u → Type u} (endo : Endofunctor F) (A B : FAlgebra F) where
  toFun : A.carrier → B.carrier
  comm : ∀ (x : F A.carrier), toFun (A.act x) = B.act (endo.map toFun x)

/-! ### 3. Initial F-Algebras (μF) -/

/-- An initial F-algebra (μF, in) satisfying the universal catamorphism property. -/
structure InitialFAlgebra {F : Type u → Type u} (endo : Endofunctor F) where
  alg : FAlgebra F
  fold : ∀ (A : FAlgebra F), alg.carrier → A.carrier
  fold_comm : ∀ (A : FAlgebra F) (x : F alg.carrier),
    fold A (alg.act x) = A.act (endo.map (fold A) x)
  fold_unique : ∀ (A : FAlgebra F) (h : alg.carrier → A.carrier),
    (∀ x : F alg.carrier, h (alg.act x) = A.act (endo.map h x)) → h = fold A

/-! ### 4. Lambek's Lemma for Initial Algebras -/

/-- The canonical algebra structure on `F μ` using `map in`. -/
def fAlgCarrier {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo) :
    FAlgebra F where
  carrier := F init.alg.carrier
  act := endo.map init.alg.act

/-- The inverse map `out : μF → F(μF)` via fold into `F(μF)`. -/
def initialOut {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo)
    (x : init.alg.carrier) : F init.alg.carrier :=
  init.fold (fAlgCarrier endo init) x

/-- Lambek's Lemma: The structure map `in` of an initial algebra is an isomorphism.
    First part: `in ∘ out = id`. -/
theorem lambek_in_out {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo) :
    (fun x => init.alg.act (initialOut endo init x)) = id := by
  have h_unique := init.fold_unique init.alg (fun x => init.alg.act (initialOut endo init x))
  have h_comm : ∀ x : F init.alg.carrier,
      init.alg.act (initialOut endo init (init.alg.act x)) =
        init.alg.act (endo.map (fun y => init.alg.act (initialOut endo init y)) x) := by
    intro x
    have h1 : initialOut endo init (init.alg.act x) =
        endo.map init.alg.act (endo.map (initialOut endo init) x) :=
      init.fold_comm (fAlgCarrier endo init) x
    rw [h1]
    have h2 := endo.map_comp (initialOut endo init) init.alg.act x
    rw [← h2]
    rfl
  have h_id_comm : ∀ x : F init.alg.carrier,
      (id : init.alg.carrier → init.alg.carrier) (init.alg.act x) =
        init.alg.act (endo.map (id : init.alg.carrier → init.alg.carrier) x) := by
    intro x
    rw [endo.map_id]
    rfl
  have h_id_is_fold := init.fold_unique init.alg id h_id_comm
  have h_comp_is_fold := h_unique h_comm
  rw [h_comp_is_fold, ← h_id_is_fold]

/-- Lambek's Lemma: Second part: `out ∘ in = id`. -/
theorem lambek_out_in {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo) :
    (fun x => initialOut endo init (init.alg.act x)) = id := by
  funext x
  have h1 : initialOut endo init (init.alg.act x) =
      endo.map init.alg.act (endo.map (initialOut endo init) x) :=
    init.fold_comm (fAlgCarrier endo init) x
  rw [h1]
  have h_comp := endo.map_comp (initialOut endo init) init.alg.act x
  rw [← h_comp]
  have h_in_out : (fun y => init.alg.act (initialOut endo init y)) = id :=
    lambek_in_out endo init
  have h_eq : (init.alg.act ∘ initialOut endo init) = id := h_in_out
  rw [h_eq, endo.map_id]
  rfl

/-! ### 5. F-Coalgebras and Final Coalgebras (νF) -/

/-- An F-coalgebra: carrier object together with structure map `coact : carrier → F carrier`. -/
structure FCoalgebra (F : Type u → Type u) where
  carrier : Type u
  coact : carrier → F carrier

/-- A final F-coalgebra (νF, out) satisfying the universal anamorphism property. -/
structure FinalFCoalgebra {F : Type u → Type u} (endo : Endofunctor F) where
  coalg : FCoalgebra F
  unfold : ∀ (C : FCoalgebra F), C.carrier → coalg.carrier
  unfold_comm : ∀ (C : FCoalgebra F) (c : C.carrier),
    coalg.coact (unfold C c) = endo.map (unfold C) (C.coact c)
  unfold_unique : ∀ (C : FCoalgebra F) (h : C.carrier → coalg.carrier),
    (∀ c : C.carrier, coalg.coact (h c) = endo.map h (C.coact c)) → h = unfold C

/-! ### 6. The Execution Morphism: Blueprint Syntax (μF) → Execution Dynamics (νF) -/

/-- Given an algebra evaluation structure `eval : F νF → νF` on the final coalgebra
    (for example, the inverse to `out` from Lambek duality),
    there is a canonically induced algebra on νF. -/
def finalAlgebraOnNu {F : Type u → Type u} {endo : Endofunctor F} (fin : FinalFCoalgebra endo)
    (eval : F fin.coalg.carrier → fin.coalg.carrier) : FAlgebra F where
  carrier := fin.coalg.carrier
  act := eval

/-- **The Canonical Execution Morphism:**
    Maps the inductive syntax/blueprint (μF) into the coinductive dynamics (νF). -/
def execute {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo)
    (fin : FinalFCoalgebra endo) (eval : F fin.coalg.carrier → fin.coalg.carrier) :
    init.alg.carrier → fin.coalg.carrier :=
  init.fold (finalAlgebraOnNu fin eval)

/-- **Execution Intertwining Theorem:**
    The execution morphism strictly preserves the computational step:
    evaluating a constructed term `in(step)` matches evaluating the execution of its components. -/
theorem execute_step {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo)
    (fin : FinalFCoalgebra endo) (eval : F fin.coalg.carrier → fin.coalg.carrier)
    (x : F init.alg.carrier) :
    execute endo init fin eval (init.alg.act x) =
      eval (endo.map (execute endo init fin eval) x) := by
  exact init.fold_comm (finalAlgebraOnNu fin eval) x

/-- **Uniqueness of the Execution Morphism:**
    `execute` is the ONLY map from blueprint syntax into dynamic evaluation
    satisfying the categorical step law. -/
theorem execute_unique {F : Type u → Type u} (endo : Endofunctor F) (init : InitialFAlgebra endo)
    (fin : FinalFCoalgebra endo) (eval : F fin.coalg.carrier → fin.coalg.carrier)
    (h : init.alg.carrier → fin.coalg.carrier)
    (h_comm : ∀ x : F init.alg.carrier, h (init.alg.act x) = eval (endo.map h x)) :
    h = execute endo init fin eval := by
  exact init.fold_unique (finalAlgebraOnNu fin eval) h h_comm

end ResNova.Foundations.InitialAlgebraExecution
