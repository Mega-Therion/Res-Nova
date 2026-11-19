# Coupled quadratic stability of the PR #226 witness

**Date:** 2026-11-18
**Receipt:** `audits/2026-11-18/coupled_quadratic_stability.py` (exit 0)
**Sources, fetched and read directly:** [SZ21] Skordis & Złośnik, PRL **127**, 161302 (2021), arXiv:2007.00082; [SZ22] Skordis & Złośnik, PRD **106**, 104041 (2022), arXiv:2109.13287.

**Outcome in one line:** the normalization is verified and the witness has no double-counting, but **the requested coupled 2×2 on the FLRW radiation background is not delivered**, and two of the witness's inputs turn out to be unestablished. Details, fenced.

---

## 1. `[P]` Normalization verified against both primary sources

[SZ21], in the paragraph after eq. (`NT_quasi_Phi`), diagonalizing the quasi-static action:

> "identifying **`G̃ = (1 − K_B/2) Ĝ`**"

[SZ21], in the AQUAL paragraph:

> "**`G_N = (1 + 1/λ_s) Ĝ`**"

[SZ21], defining the background:

> "we define the energy density as `8πG̃ρ̄ = 𝒬 d𝒦/d𝒬 − 𝒦` … **so that the usual FLRW equations are satisfied**"

[SZ22], stated outright:

> `G_N = (1 + 1/λ_s)/(1 − K_B/2) · G̃`

The chain closes: substituting `Ĝ = G̃/(1 − K_B/2)` into `G_N = (1+1/λ_s)Ĝ` reproduces [SZ22] exactly (verified symbolically, `agree = True`). And since FLRW uses `G̃`, **`G_cosmo = G̃`** with no `K_B`.

```
G_cosmo/G_N = G̃ / [(1 + 1/λ_s)/(1 − K_B/2) · G̃] = (1 − K_B/2)/(1 + 1/λ_s)
```

**`[P]` The corpus formula is correct and the witness does not double-count `(1 − K_B/2)`.** Witness arithmetic reproduces PR #226's `0.950564` exactly.

**`[P]` But the corpus prose is wrong.** `TARGET_D7` and the Lean header both say `G_cosmo = (1 − K_B/2)Ĝ`. In [SZ21] the factor sits on the *other* side: `G̃ = (1 − K_B/2)Ĝ`, equivalently `G_N` carries a `1/(1 − K_B/2)`. The ratio is unchanged, so no result moves, but the attribution is backwards and should be corrected.

## 2. `[P]` What the two papers actually publish

| | FLRW scalar sector | Explicit `K_ij` / `G_ij`? | `𝒬`-dependence? |
|---|---|---|---|
| **[SZ21]** | effective fluid `(δ, θ)` + a separate `α` evolution equation | **No** | general `𝓕(𝒴,𝒬)` |
| **[SZ22]** | 4×4 matrix on `{Ψ, Φ, α, δφ}`, 2 constraints + 2 propagating | **Yes, but on Minkowski** | `𝓕 → (2−K_B)𝒥(𝒴)`, no `𝒬` |

[SZ21] is explicit that the fluid route does not close:

> "the resulting system is **not equivalent to a dark fluid**: the nonstandard pressure … does not close under the fluid variables but, rather, depends on the vector field perturbations `α` and `E_α`."

So neither paper contains the object requested: a `2×2` in the longitudinal aether and `δφ` around an FLRW radiation background with `𝒬³` retained.

## 3. `[P]` Every published stability condition passes at the witness

[SZ22] eq. (`speed_of_sound`), evaluated at `K_B = 0.008`, `λ_s = 11.2787`, `𝒦₂ = 300`:

```
c_s² = (2 − K_B)(1 + ½K_Bλ_s)/(𝒦₂K_B) = 0.8674
```

| Condition | Source | Value | Verdict |
|---|---|---|---|
| `K_B > 0` (no ghost / gradient instability) | [SZ22] | 0.008 | pass |
| `0 < K_B < 2`, `λ_s > −1` (non-tachyonic) | [SZ22] | 0.008, 11.28 | pass |
| `0 < c_s² ≤ 1` | [SZ22] | 0.8674 | pass |
| `c_T = 1` | structural (EH tensor sector, no Weyl coupling) | 1 | pass |

## 4. `[D]` Two things this does *not* establish

**(a) The `𝒬³` term is not invisible at quadratic order.** I initially expected it to be, since a static scalar has `𝒬 = 0`. That is wrong: [SZ22]'s own background is `φ = 𝒬₀t + δφ`, so **`𝒬̄ = 𝒬₀ ≠ 0`**. Expanding about `𝒬̄`:

```
𝓕(0,𝒬) = −c𝒬³ = −c[ 𝒬̄³ + 3𝒬̄²δ𝒬 + 3𝒬̄δ𝒬² + δ𝒬³ ]
```

and the `δ𝒬²` coefficient `3c𝒬̄` is nonzero. So eq. (`speed_of_sound`) is the sound speed of the **Y-only** theory, and `c_s² = 0.8674` is **not** established for the modified theory.

**(b) The `𝒬` sector in isolation is healthy, but `ε_Q` is a tuning.** For `𝓕 = −c𝒬³`: `ρ = 2c𝒬̄³ > 0`, `ρ+p = 3c𝒬̄³ > 0`, `c_s² = 1/2`, and `w = p/ρ = 1/2`. Ghost-free and causal *in isolation* — but `w = 1/2` means `ρ_φ ∝ a^{−3(1+w)} = a^{−4.5}`, which redshifts **faster** than radiation. So `ρ_φ/ρ_rad` at BBN is an **initial condition, not a prediction**. PR #226's `ε_Q = 0.039` is therefore a tuning, independent of the `2×2` gap.

## 5. `[O]` The requested object is not delivered

The `2×2` `K_ij` and `G_ij` for `(longitudinal aether, δφ)` around the FLRW radiation background, with `𝒬³` retained, and its two eigenmode sound speeds `c_{s,±}²`:

**Not derived. I will not fabricate the matrices.**

What it requires, and why I stopped:

1. Second-order expansion of the full action in Newtonian gauge with the lapse and shift constraints solved — including the `𝒬³` contribution through `δ𝒬 = γ ≡ δφ̇ − φ̄̇Ψ`.
2. Reduction to the two propagating combinations and the generalized eigenproblem `det(c_s²K − G) = 0`.
3. A validation leg that reproduces [SZ22] eq. (`speed_of_sound`) in the `c → 0`, Minkowski limit.

Steps 1 and 2 are an xAct/Cadabra-scale computation; the sandbox has neither, and hand-deriving a `2×2` with mixing terms and shipping it unvalidated would violate the point of the gate. Step 3 is the check that would have caught a wrong matrix, and it cannot be run without step 1.

## 6. Verdict

| Claim | Tag |
|---|---|
| Normalization `G_cosmo/G_N = (1−K_B/2)/(1+1/λ_s)` matches SZ | `[P]` |
| Witness has no double-counting (`0.950564`) | `[P]` |
| Corpus prose "`G_cosmo = (1−K_B/2)Ĝ`" is a misattribution | `[P]` |
| All published [SZ22] stability conditions pass at the witness | `[P]` |
| `𝒬³` is not invisible at quadratic order (`𝒬̄ = 𝒬₀ ≠ 0`) | `[D]` |
| `𝒬` sector ghost-free and causal in isolation | `[P]` |
| `w = 1/2` ⇒ `ε_Q` is a tuning, not a prediction | `[D]` |
| Coupled FLRW `2×2` and `c_{s,±}²` | **`[O]` not delivered** |
| Witness certified stable | **`[X]` not established** |

**The witness is not certified stable.** It passes every published and independently checkable condition and fails nothing, but the specific check requested has not been performed, and one of its inputs is a tuning. PR #226's own text already flagged the quadratic gap; this note sharpens it and adds the second gap (`ε_Q` as tuning).

## 7. What would close it

A single script that (i) builds the FLRW quadratic action in Newtonian gauge including `3c𝒬̄γ²`, (ii) solves the two constraints for `Ψ, Φ`, (iii) assembles `K` and `G` in the two propagating variables, (iv) prints both eigenvalues of `K` and both roots of `det(c_s²K − G) = 0`, and (v) reproduces `c_s² = (2−K_B)(1+½K_Bλ_s)/(𝒦₂K_B)` at `c → 0` as its own unit test. Item (v) is the acceptance criterion: without it the other three are unfalsifiable.

## 8. Registry note

Deliberately **not** editing `assurance/claims.json` in this PR, to avoid colliding with open PR #226, which already touches the same file. Proposed entries once #226 lands:

- `CLM-SZ-NORM` `[P]` — the normalization chain, with the three source locators.
- `CLM-Q3-QUAD` `[D]` — the `3c𝒬̄δ𝒬²` term and the consequent non-transfer of [SZ22] eq. (`speed_of_sound`).
- `CLM-Q3-W` `[D]` — `w = 1/2`, so `ε_Q` at BBN is an initial condition.
- `CLM-COUPLED2X2` `[O]` — the open coupled eigenmode problem.
