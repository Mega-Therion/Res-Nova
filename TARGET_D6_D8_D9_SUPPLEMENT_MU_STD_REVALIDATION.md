# TARGET D6/D8/D9 SUPPLEMENT: Re-validation under F_std

**Status:** MEASURED (2026-09-12). Closes `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §7 item 5.
**Scope:** re-run every numeric claim in `TARGET_D6_RELATIVISTIC_STABILITY.md`,
`TARGET_D8_TENSOR_SPEED.md`, `TARGET_D9_SKORDIS_ZLOSNIK_EMBEDDING.md` with
`F_dual(x)=½x²−x+ln(1+x)` replaced by `F_std(x)=½[x√(1+x²)−arsinh x]`.
**Tags:** `[P]` proved · `[D]` derived here · `[C]` cited · `[O]` open · `[X]` killed

**Convention used throughout (stated, not assumed):** `F′(x) = x·μ(x)` (`TARGET_D2` §4
Corollary), hence `J(𝒴) = F(√𝒴)` in `a₀=1` units and `2J′(𝒴) = μ(√𝒴)` — self-consistently
D9 §2's factor. **Rows 4–7 use this; rows 8–9 use D7 §2.1's `J′=λ_sμ` in ã₀ units.** The two
agree at `λ_s=½`, so row 5's `J″` and row 9's `J′+2𝒴J″` are deliberately different objects (`TARGET_D7` §2.1 adopts `μ_φ = J′` with
`J = 2λ_s ã₀² F(√𝒴/ã₀)` ⟹ `J′ = λ_s μ`). **Three mutually
inconsistent normalizations are live in the corpus (D9 §2 `2J′=μ`, D9-header/D7 §2.1 `J′=μ`,
D2-supp §1 `J′=λ_sμ`). Not resolved here — recorded. [O]**

Measured symbolically with sympy 1.14.0 / numpy 2.4.6 / scipy 1.17.1 (CODATA 2022).

---

## 1. Verdict table

| # | claim (source) | computed | claimed | Δ | status |
|---|---|---|---|---|---|
| 1 | D6 §3 strong-coupling scale `Λ_SC` | **1.7935×10⁻³ eV** (a₀=1.2e-10, `Λ⁴=(a₀²/G)(ħc)³`) | `~10⁻¹⁰ eV` | **7.25 orders** | **FAIL [X]** |
| 2 | D6 §1.2 `F_dual''(𝒦)=(2√𝒦+𝒦)/((1+√𝒦)²2√𝒦)` | at 𝒦=1: **0.375**; true `d²J/d𝒦²` = **0.0625** | 0.375 | 6× | **FAIL (expression) [X]** — sign verdict survives |
| 3 | D9 §5 / `SkordisZlosnikEmbedding.lean` `J_param u = ½u²−u+log(1+u)` | hardcodes falsified `μ_dual` | `[P]` | — | **FAIL (stale) [X]** |
| 4 | D9 §3 `J(𝒴)` integration under F_std *(conv. `2J′=μ`)* | `J_std = ½[√(𝒴(1+𝒴)) − arsinh√𝒴]`, `2J′−μ(√𝒴) = 0` exactly | — | 0 | **PASS [D]** |
| 5 | D9 §4.2 convexity `J″>0` *(conv. `2J′=μ`, a₀=1)* | `J_std″ = 1/(4√𝒴(1+𝒴)^{3/2})`; 24.996 / 0.08839 / 2.4996e-9 at 𝒴=1e-4,1,1e4 | `>0 ∀𝒴>0` | — | **PASS [D]**, different closed form from dual's `1/(4√𝒴(1+√𝒴)²)` |
| 6 | D9 §4.1 deep-MOND leading coefficient | `J_std = ⅓𝒴^{3/2} − (1/10)𝒴^{5/2} + (3/56)𝒴^{7/2}` | `⅓𝒴^{3/2} − ¼𝒴² + ⅕𝒴^{5/2}` | leading term **identical (1/3)** | **PASS on result, FAIL on explanation [D]/[X]** |
| 7 | D9 §4.3 *(conv. `2J′=μ`)* Newtonian `2J′→1`; deep-MOND `2J′/√𝒴→1` | `1`, `1` (sympy `limit`) | 1, 1 | 0 | **PASS [D]** |
| 8 | D7 §2.2 `ã₀=(1+λ_s)a₀` *(conv. `J′=λ_sμ`, ã₀ units)* | deep-MOND coeff `2λ_s/(3ã₀)` ⟹ `solve → a₀(λ_s+1)`; tracking `lim J′=λ_s` | `ã₀=(1+λ_s)a₀` | 0 | **PASS — survives the swap unchanged [D]** |
| 9 | D7 §5 ghost pair under F_std *(conv. `J′=λ_sμ`, ã₀ units)* | `J′=λ_s√𝒴/√(𝒴+ã₀²)`; `J′+2𝒴J″ = λ_s√𝒴(𝒴+2ã₀²)/(𝒴+ã₀²)^{3/2}`; both >0 at 𝒴=1e-2,1,1e2,1e6 | >0 | — | **PASS [D]** |
| 10 | D6 §2 Hamiltonian `J−(𝒦/2)J′` bounded below | std: 8.333e-11, 8.358e-5, 0.08964, 23.874, 2.49997e5 at 𝒦=1e-6…1e6; `lim_{𝒦→0}=0`, `→∞` | bounded below | — | **PASS [D]** (dual: 8.333e-11 … 2.49257e5, also >0) |
| 11 | D6 §1.2 `F_std''(x) = x(x²+2)/(1+x²)^{3/2}` | 0.19802, 1.06066, 1.00489, 1.00005 at x=0.1,1,10,100 | >0 | — | **PASS [D]** |
| 12 | D8 §1.1 `c₁₃=0`, `c_T²=1` | `c₁+c₃ = 0` exactly; `1/(1−0)=1` | 0, 1 | 0 | **PASS [P]**, F-independent |
| 13 | D8 §1.2 `α₁=−2K`, `\|K\|≲5×10⁻⁵` | `α₁ − (−2K) = 0` exactly; `1e-4/2 = 5.0e-05` | −2K, 5e-5 | 0 | **PASS [P]**, F-independent |
| 14 | D8 §1.3 `c_γ=e^{2ϕ}` | `g̃₀₀=−e^{2ϕ}`, `g̃_ij=e^{−2ϕ}`, `c_γ²=e^{4ϕ}` | `e^{4ϕ}` | 0 | **PASS [P]**, F-independent |
| 15 | D8 §1.4 deviations | ϕ=1e-6 → **1.999998e-06** (9.30 orders over 1e-15); ϕ=0.1 → **1.812692e-01** (14.26 orders) | `~2e-6` / 9 orders; `~0.18` / 14 orders | <1% | **PASS [P]** |
| 16 | D8 §2 "preserve the derived dual-channel closure μ(x)=x/(1+x)" | prose motivates a function falsified by D7 §4 | — | — | **STALE [X]** |
| 17 | D9 §0.3 / §0.4 `c_T=c_γ`, `Φ=Ψ` | no `F` appears in either argument | `[P]` | — | **UNTESTABLE here — F-independent, unchanged by the swap** |

---

## 2. Failures, most severe first

### 2.1 D6 §3 — `Λ_SC ~ 10⁻¹⁰ eV` is dimensionally broken and off by 7 orders **[X]**

`a₀²/G` has SI units kg·m⁻¹·s⁻² = J/m³ — an **energy density**, not an energy⁴. Its bare
fourth root (3.83×10⁻³ in SI) is not an energy and cannot be read as eV. Restoring `ħ,c` via
`Λ⁴ = (a₀²/G)(ħc)³`:

| a₀ source | a₀ (m/s²) | bare `(a₀²/G)^{1/4}` | `Λ_SC` (eV) |
|---|---|---|---|
| D6 §3 | 1.2000e-10 | 3.8326e-03 | **1.7935e-03** |
| D1-supp §4 (SPARC) | 1.1160e-10 | 3.6960e-03 | **1.7296e-03** |
| canonical `5.461e-11·√5` | 1.2211e-10 | 3.8661e-03 | **1.8092e-03** |

Three different a₀ values are in live use across the corpus; the spread on Λ_SC is 4.6%,
negligible next to the 7.25-order error. **This failure is μ-independent** — it survives the
F_std swap untouched. Consequence chain: ~1.8 meV is the dark-energy / MOND scale, i.e. **not**
"far below any experimentally accessible scale"; D6 §5's row "✓ [P] far below experiments" is
a false safety claim resting on an arithmetic artefact. Fifth-force and short-range-gravity
experiments probe exactly this scale. **[X]**

### 2.2 D6 §1.2 — chain-rule mix-up between `x` and `𝒦` **[X] for the expression**

D6 states `F''(𝒦) = (2√𝒦+𝒦)/((1+√𝒦)²·2√𝒦)`. At 𝒦=1 this is **0.375**. That is exactly
`(1/(2x))·d²F_dual/dx²` at x=1 = **0.375** — a half-completed chain rule, not a typo. The
true `d²J_dual/d𝒦²` at 𝒦=1 is **0.0625** (= D9 §4.2's `1/(4√𝒴(1+√𝒴)²)`, which is correct — verified symbolically:
`sp.simplify(1/(4*sqrt(K)*(1+sqrt(K))**2) - diff(J_dual,K,2)) = 0`).
D6 and D9 therefore stated two different second derivatives for the same object.
Both are positive, so the **ghost-free verdict survives while the expression is wrong** —
a coupled failure (wrong derivation, right conclusion), not an isolated slip.
D6's criterion is also not `TARGET_D7` §5's pair (`J′>0` **and** `J′+2𝒴J″>0`); D6 tests only
one of the two conditions the current action requires. Under F_std both D7 conditions hold
(row 9), so the conclusion transfers — but D6 §1.2/§5 need rewriting to D7's criterion.

### 2.3 D9 §5 Lean footprint formalizes the falsified function **[X]**

`05_lean_formalization/SkordisZlosnikEmbedding.lean:30,33` hardcode
`J_param u = (1/2)*u^2 - u + Real.log (1 + u)` and `dJ_dY_param u = (u/(1+u))/2`.
Every theorem listed in D9 §5 (`sz_aqual_reduction`, `dJ_dY_pos`, `sz_newtonian_limit_diff`,
`sz_mond_limit_diff`) is a true statement **about μ_dual**, which `TARGET_D7` §4 killed. The
Lean gate will stay green — the mathematics is sound and the physics is dead. This is the
substitutability test named in `CLAUDE.md`. `TensorSpeed.lean` returned **0 hits** for the same μ_dual
literal pattern (it has 5 lines matching `log|sqrt|J_param|mu`, none of them the free
function), so no μ_dual literal was found there. **Not edited here** (scope is numeric re-validation); flagged for the D1-supp §7 item 4
Lean sweep. **[O]**

### 2.4 D9 §4.1's "non-analytic cancellation" narrative does not transfer **[X] for explanation**

The claimed mechanism — the `−√𝒴` and `+½𝒴` terms cancelling against `ln(1+√𝒴)`'s expansion —
is a property of the logarithm, not of the deep-MOND limit. `J_std` expands in **half-integer
powers only**: `⅓𝒴^{3/2} − (1/10)𝒴^{5/2} + (3/56)𝒴^{7/2}`. There is no `−¼𝒴²` counterpart and
nothing to cancel. The **result** (leading coefficient exactly `1/3`, `J(0)=J′(0)=0`) is
identical for both functions. Keep the result; delete the explanation.

### 2.5 D8 §2 prose is stale **[X]**

§2's remediation branches are framed as ways "to preserve the derived dual-channel closure
μ(x)=x/(1+x)". That function is falsified. Both branches (conformal `B≡0`, SZ luminal class)
remain valid and are **independent of which μ is used** — only the motivating sentence is dead.

---

## 3. What the swap actually changed

**Nothing in D8.** Every D8 quantity (`c₁`, `c₃`, `α₁`, `A(ϕ)`, `B(ϕ)`, `c_γ`) is built from
the vector sector and the disformal map. `F` does not appear. The re-validation is a measured
**no-op**, and D8's falsification of the `B=−2sinh2ϕ` completion stands independently of the
interpolating function. Same for D9 §0.3/§0.4 (`c_T=c_γ`, `Φ=Ψ`).

**D9's analytic core transfers cleanly.** `2J′=μ` is exact, `J″>0`, both asymptotic limits hit
1, and the deep-MOND `⅓𝒴^{3/2}` coefficient is unchanged. The only casualties are the closed
form of `J″` and the §4.1 cancellation story.

**D7 §2.2's `ã₀=(1+λ_s)a₀` survives unchanged.** This was the claim most at risk: it was
derived from μ_dual's `1/x` Newtonian tail, and μ_std's tail decays as `1/x²`. Measured: the
deep-MOND coefficient of `𝒴^{3/2}` in `J = 2λ_s ã₀²F_std(√𝒴/ã₀)` is `2λ_s/(3ã₀)` — identical
in form to the dual case — and `lim_{𝒴→∞} J′ = λ_s` still holds, so sympy `solve` returns
`ã₀ = a₀(λ_s+1)` exactly. The tracking-factor relation is a property of the two SZ
normalizations, not of the tail exponent. `λ_s` remains unfixed by the MOND limit. **[O]**

**D6 is the weak target**, and its two failures are μ-independent: a dimensional error in §3
and a chain-rule error in §1.2. Neither was introduced or repaired by the swap. D6's status
line "D6_VERIFIED" and its §5 table's six ✓ rows overstate what §1.2 and §3 support.

---

## 4. Escalation-pattern notes

- **Resource-additive:** none of the repairs above add a constant or widen a fit. §2.2's
  `λ_s` was already free before the swap and is still free after it.
- **Control-additive:** D8's remediation branches (`B≡0`, or write the action on `g̃`) are
  pure restrictions of the model space. They address the root cause — the two null cones are
  locked together **by construction** rather than by a tuned bound — so no constraint paradox.
- **Coupled failure:** D6 §1.2 is the marker. A wrong second derivative sat next to a correct
  verdict for four weeks because nobody recomputed the sign from the stated expression. The
  same pattern produced §3: a formula that "looks like" a scale, never dimensionally checked.
- **Warning structure if §3 ships uncorrected:** wrong Λ_SC → "EFT valid at all accessible
  scales" asserted → no fifth-force / short-range-gravity confrontation performed → a
  ~1.8 meV scale that sits squarely inside existing experimental reach goes unexamined.

---

## 5. Reproduce

```bash
python3 /tmp/claude-1000/-home-mega/cf13f48f-9b9d-4cac-8e5f-2904ed46d18a/scratchpad/d9_std.py ; echo $?   # EXIT=0
python3 /tmp/claude-1000/-home-mega/cf13f48f-9b9d-4cac-8e5f-2904ed46d18a/scratchpad/d6_std.py ; echo $?   # EXIT=0
python3 /tmp/claude-1000/-home-mega/cf13f48f-9b9d-4cac-8e5f-2904ed46d18a/scratchpad/d8_std.py ; echo $?   # EXIT=0
grep -nc "1 + u\|1+u\|x/(1" 05_lean_formalization/SkordisZlosnikEmbedding.lean \
                            05_lean_formalization/TensorSpeed.lean   # 19 and 0, exit 0
```

All three scripts exited **0** in the session that produced this table. They are scratchpad
artifacts; move to `Scripts_and_Tools/` if these numbers are to be cited.

The Lean gate (`cd 05_lean_formalization && bash verify_all_proofs.sh`) was **not run** — it
would pass, because the stale theorems are true statements about the falsified function.
That is the point of §2.3, not a gap in it.
