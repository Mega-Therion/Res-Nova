# Full-background FLRW: `G_cosmo/G_N` from the exact AeST action

**Date:** 2026-11-18
**Receipt:** `audits/2026-11-18/flrw_full_background.py` (exit 0)
**Gate:** `scripts/survival_vector_gate.py` (exit 0 on the certified witness)

Derived from the action as transcribed verbatim in `TARGET_D7_COVARIANT_COMPLETION.md` §1
(Skordis–Złośnik, PRL **127**, 161302, eq. 5):

```
S = ∫ d⁴x (√−g/16πG̃)[ R − (K_B/2)F^{μν}F_{μν} + 2b J^μ∇_μφ − b𝒴 − 𝓕(𝒴,𝒬) − λ(A^μA_μ+1) ] + S_m
```

with `b = 2 − K_B`, `𝒴 = q^{μν}∇_μφ∇_νφ`, `𝒬 = A^μ∇_μφ`.

## 1. Two structural facts, computed not assumed

On FLRW with `A^μ = (1/N, 0,0,0)`:

| Object | Value | Why |
|---|---|---|
| `A^μA_μ` | `−1` | constraint satisfied |
| `F_{μν}` | **`0` identically** | `A_μ` has no space-time cross derivatives |
| `J_μ = A^α∇_αA_μ` | **`0` identically** | `A_μ` is constant in comoving coordinates |
| `𝒴` | **`0` identically** | `q^{00} = g^{00} + A^0A^0 = −1 + 1 = 0` |
| `𝒬` | `φ̄̇/N ≠ 0` | the scalar **does** have background dynamics |

**Consequence for `K_B`:** the whole aether sector vanishes at background order. `K_B` cannot appear in the Friedmann equation. The corpus formula `G_cosmo = (1 − K_B/2)Ĝ` is consistent with this derivation only if `Ĝ := G̃/(1 − K_B/2)`; the `K_B` dependence then lives entirely in that definition and in the quasi-static Newtonian limit, **not** in the Friedmann equation.

## 2. The exact Friedmann equation

Varying the reduced action with respect to the lapse and setting `N = 1`:

```
3H² = 8πG̃ρ_m + ½[ 𝓕(0,𝒬) − 𝒬 𝓕_𝒬(0,𝒬) ]
```

so with `ρ_φ ≡ [𝓕 − 𝒬𝓕_𝒬]/(16πG̃)`:

```
H² = (8πG̃/3)(ρ_m + ρ_φ)          G_cosmo = G̃(1 + ρ_φ/ρ_m)
```

and during radiation domination, with `G_N = (1 + 1/λ_s)G̃` (corpus relation, taken as input):

```
G_cosmo/G_N = (1 + ρ_φ/ρ_rad) / (1 + 1/λ_s)
```

The two-parameter truncation is the special case `ρ_φ = 0`.

## 3. Answer: the `√(27/32)` ceiling is not fundamental

`ρ_φ = 0` for any `𝓕(𝒴)`-only theory, because `𝓕(0)` is a constant. That reproduces `√(27/32) = 0.918559` and the 8.144% gap exactly. **It is the ceiling of the minimal theory, not of AeST.**

Clearing the 5% BBN bound requires only

```
ρ_φ/ρ_rad ≥ 0.034229   (3.423%)
```

## 4. But `ρ_φ` is extra radiation, and that bounds it from above

A positive `ρ_φ` at BBN *is* extra radiation. With `(7/8)(4/11)^{4/3} = 0.227107` and `N_eff,SM = 3.044`:

```
ρ_φ/ρ_rad = 0.134279 ΔN_eff        ⇒        ΔN_eff ≥ 0.2549 to clear 5% BBN
```

Against the Planck/BBN bound `ΔN_eff ≲ 0.29`, the viable band is **`ΔN_eff ∈ [0.255, 0.29]`** — narrow, non-empty, and falsifiable.

## 5. Stability of the Q-sector operator

For `L_φ = −𝓕(0,𝒬)`: `ρ_φ = 𝓕 − 𝒬𝓕_𝒬`, `p_φ = −𝓕`, `ρ+p = −𝒬𝓕_𝒬`, `c_s² = 𝓕_𝒬/(𝒬𝓕_𝒬𝒬)`.

| `𝓕(0,𝒬)` | `ρ_φ` | `ρ+p` | `c_s²` |
|---|---|---|---|
| `−c𝒬²` | `c𝒬²` | `2c𝒬²` | `1` (stiff, marginal) |
| `−c𝒬³` | `2c𝒬³` | `3c𝒬³` | `1/2` ✓ |
| `−c𝒬⁴` | `3c𝒬⁴` | `4c𝒬⁴` | `1/3` ✓ |

`p ≥ 3` gives `c_s² = 1/(p−1) < 1` strictly, with `ρ > 0` and `ρ+p > 0`.

## 6. The joint window, and the mistake the gate caught

The feasible set is bounded on **four** sides, and they pinch from opposite directions:

| # | Constraint | Effect |
|---|---|---|
| 1 | BBN 5% | pushes `ε_Q` **up** (≥ 0.0342) |
| 2 | `ΔN_eff ≤ 0.29` | pushes `ε_Q` **down** (≤ 0.0389) |
| 3 | BBN + `K_B` | forces `K_B ≤ 0.0091` (any `K_B` multiplies by `1−K_B/2 ≤ 1`) |
| 4 | Y-sector `c_s² ≤ 1` | forces `𝒦₂ ≳ 230` at `K_B ≈ 0.008`, because `(2−K_B)/(𝒦₂K_B) → ∞` as `K_B → 0` |

| `ε_Q` | `K_B` max | `𝒦₂` min |
|---|---|---|
| 0.03423 | ≈ 0 (degenerate) | — |
| 0.03658 | 4.55e−03 | 451 |
| 0.03894 | 9.07e−03 | 231 |

**My first witness point was wrong and the gate rejected it.** Taking `K_B → 0` maximizes the BBN ratio but diverges the Y-sector sound speed, giving `c_s² = 26.8` at `K_B = 0.001`. That is exactly the failure mode a deterministic gate exists to catch, and it would have survived a prose argument.

## 7. Certified witness

Passes `scripts/survival_vector_gate.py`, exit 0:

| Parameter | Value |
|---|---|
| `𝓕(𝒴,𝒬)` | `−c𝒬³ − 𝓕_Y(𝒴)`, separable |
| `ε_Q = ρ_φ/ρ_rad` | 0.0390 (`ΔN_eff = 0.290`) |
| `K_B` | 0.008 |
| `λ_s` | 11.2787 (< 11.278775) |
| `𝒦₂` | 300 |
| `c_T` | `c` (structural) |
| `c_s²` | 0.867 |
| `G_cosmo/G_N` | **0.950564** ≥ 0.95 ✓ |

## 8. What is still open

1. **The quadratic analysis is not done.** The background k-essence conditions above are **necessary, not sufficient**. The `𝒬³` operator must be checked in the full coupled aether–scalar perturbation system for ghosts, gradient instabilities, and mixing. That is the xAct/Cadabra job and this document does not substitute for it.
2. **`ΔN_eff ∈ [0.255, 0.29]` is a prediction, not a freedom.** If the CMB+BBN constraint tightens below 0.255, the escape closes. This is the theory's sharpest near-term falsifier, and it is cheap to test.
3. **Cassini is untouched.** The witness passes the gate's observable 2 only because a screening scale is declared. Its magnitude is not computed.
4. **`Ĝ := G̃/(1 − K_B/2)` should be checked against SZ's own text**, since this derivation shows the `K_B` factor is not a background result.
