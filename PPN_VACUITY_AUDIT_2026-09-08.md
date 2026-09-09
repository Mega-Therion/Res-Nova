# PPN Claim Audit and the β Bound

**Date:** 2026-09-08
**Scope:** the PPN content backing target D3, in `05_lean_formalization/`.
**Method:** substitutability. A theorem carries physics only if replacing the
physics with nonsense breaks it. Every claim below was tested by compiling the
substitution, not by reading the proof.

---

## 1. Two D7 "PPN" theorems are vacuous — measured, not inferred

### `CovariantCompletion.disformal_gamma_ppn_unity`

```lean
theorem disformal_gamma_ppn_unity (h_spatial h_temporal : ℝ)
    (h_eq : h_spatial = h_temporal) (h_nz : h_temporal ≠ 0) :
    h_spatial / h_temporal = 1 := by
  rw [h_eq]; exact div_self h_nz
```

The statement is `x = y → x / y = 1`. It mentions no metric, no field equation,
and none of the file's own definitions (`F_dual`, `mu_dual`, `x_var`). The
physical claim — that h_spatial *equals* h_temporal in this theory — is the
hypothesis, and it is asserted in a comment, never derived.

**Test performed.** The identical statement and proof, with every physics word
replaced, compiles unchanged:

```lean
theorem banana_sandwich_unity (b_spatial b_temporal : ℝ)
    (h_eq : b_spatial = b_temporal) (h_nz : b_temporal ≠ 0) :
    b_spatial / b_temporal = 1 := by
  rw [h_eq]; exact div_self h_nz          -- compiles, zero errors
```

It also instantiates at 42, "proving" γ_PPN = 1 for a quantity that is not a
metric perturbation:

```lean
example : (42 : ℝ) / 42 = 1 := banana_sandwich_unity 42 42 rfl (by norm_num)
```

**Verdict: vacuous.** It proves `x/x = 1`. γ_PPN = 1 is not established here.

### `CovariantCompletion.preferred_frame_parameters_zero`

```lean
theorem preferred_frame_parameters_zero (c1 c2 c3 c4 : ℝ)
    (h_maxwell : c1 = -c3 ∧ c2 = 0 ∧ c4 = 0) :
    (c1 + c3) = 0 ∧ c2 = 0 ∧ c4 = 0
```

Three defects, any one of which is disqualifying:

1. It is a restatement. `c1 = -c3` **is** `c1 + c3 = 0`; `c2 = 0` and `c4 = 0`
   are passed through unchanged.
2. **It never mentions α₁ or α₂.** The name claims the preferred-frame
   parameters vanish; the statement does not define, compute, or bound them.
3. The Maxwell restriction is assumed, not derived. `TARGET_D7` line 158 states
   plainly that c₁, c₂, c₃ are free parameters.

The nonsense-renamed version compiles identically (`sandwich_ingredients_zero`).

**Verdict: vacuous, and additionally mis-named.**

---

## 2. What is NOT vacuous — the distinction matters

`PPNLimits.lean` is real. `cassini_radar_delay_satisfied` and
`solar_system_precision_bound` depend on the dual-channel μ(x) = x/(1+x) through
`fractional_deviation_eq`, and on their numeric thresholds. D3's [P] score rests
on this file, not on the two theorems above, so **the target's status is not
overturned** — only the D7 support for it is.

---

## 3. New: the β bound

D3 §3.3 lists |β − 1| < 2.3 × 10⁻⁴ (MESSENGER) but nothing in the corpus bounded
it. `PPNLimits.lean` now carries `messenger_perihelion_satisfied` and
`messenger_margin`.

**Field point matters, and the corpus is loose about it.** The bound must be
evaluated where the observation is sensitive. Perihelion precession accumulates
along Mercury's orbit, so the relevant gradient is at r = 0.387 AU:

| quantity | value |
|---|---|
| g at Mercury | 3.959 × 10⁻² m s⁻² |
| a₀ (SPARC-measured) | 1.116 × 10⁻¹⁰ m s⁻² |
| x = g/a₀ | 3.548 × 10⁸ |
| 1 − μ(x) = 1/(1+x) | 2.819 × 10⁻⁹ |
| margin vs 2.3 × 10⁻⁴ | **8.2 × 10⁴ ×** |

The Lean theorems use the conservative threshold x ≥ 3 × 10⁸.

**A related observation on γ.** D3 quotes "1137× below Cassini". Reproducing at
Earth orbit gives 1222×, consistent. But Cassini's γ came from Shapiro delay at
solar conjunction, where the signal grazes the Sun at ~1.6 R_⊙ — and there
x ≈ 9.7 × 10¹¹, giving a margin near 10⁷ rather than 10³. Using Saturn's own
orbital radius instead (x = 5.79 × 10⁵) gives only ~13×. **The three field points
differ by six orders of magnitude**, so the doc should name which one it means.
The conclusion is unaffected — every choice clears the bound — but the stated
margin is not well-defined without it.

---

## 4. Non-vacuity of the new theorems, also measured

Substituting μ(x) = x/(2+x) makes the underlying identity false:

```lean
example : frac_dev_alt 1 = 1 / (1 + 1) := by dsimp [...]; norm_num
-- error: unsolved goals ⊢ False
```

The β theorems depend on that identity via `fractional_deviation_eq`, so they
break under substitution. That is the property the D7 theorems lack.

---

## 5. What is still open

γ = 1 and β = 1 hold **exactly** for Einstein-aether theories (Foster & Jacobson
2006, PRD 73 064015), which is the class `TARGET_D7`'s kinetic term
`c₁(∇A)² + c₂(∇·A)² + c₃(∇A)(∇A)` belongs to. The corpus should cite that result
as **[CITED]** and mark it for independent verification — it is not proved here,
and the two theorems above do not prove it either.

What the new theorems establish is narrower and honest: the **MOND-sector**
contribution is bounded by 1/(1+x) and is negligible at solar-system gradients.
The **aether-sector** contribution to γ and β is the part that rests on
Foster-Jacobson, and the general-c_i α₁/α₂ computation remains undone —
`TensorSpeed.lean` computes α₁ only after hard-coding the Maxwell case
(c₁ = K/2, c₃ = −K/2, c₄ = 0) into the definitions.
