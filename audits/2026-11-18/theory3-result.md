# Theory 3 assessment: the radiation tracker is right, the `p ≥ 3/2` prescription is not

**Date:** 2026-11-18
**Receipts:** `audits/2026-11-18/theory3_radiation_tracker.py` (exit 0); `scripts/survival_vector_gate.py --self-test` (exit 0); gate run on the `Q⁴` witness (exit 0, window proved).

Stacks on #226 (the gate lives there). Verdict up front: **Theory 3 is half-right.** Adopt the `Q⁴` tracker. Do not adopt `p ≥ 3/2`.

---

## 1. `[P]` The `Q⁴` upgrade is sound, and it fixes exactly what the panel said it fixes

For `𝓕(0,𝒬) = −c𝒬^p`:

| `p` | `w = 1/(p−1)` | `ρ_φ ∝` | `c_s²` | tracks radiation? |
|---|---|---|---|---|
| 2 | 1 | `a^{−6}` | 1 | no |
| 3 | 1/2 | `a^{−4.5}` | 1/2 | no |
| **4** | **1/3** | **`a^{−4}`** | **1/3** | **YES** |
| 5 | 1/4 | `a^{−3.75}` | 1/4 | no |

`p = 4` gives `w = 1/3` **exactly**, so `ρ_φ` scales identically to radiation and `ρ_φ/ρ_rad` is constant. The panel's diagnosis of `Q³` is confirmed: `w = 1/2` gives `a^{−4.5}`, which redshifts away, so the BBN abundance is an initial-condition tune.

**Precisely what this buys, and what it does not.** `ε_Q` remains a free constant, so `ΔN_eff` stays a range (`≈0.25–0.29`), not a unique number. What `w = 1/3` buys is that it is the **same** constant at BBN and at the CMB instead of a drifting quantity, so those two constraints act on one number rather than two. That is the real content of the `F₅ ⊗ F₄` rule, and it is worth stating exactly rather than claiming a unique prediction. *(I initially wrote "fixed prediction" in the script; corrected.)*

## 2. `[X]` `p ≥ 3/2` screening is not adoptable — it deletes MOND

Static limit, `𝒥(𝒴) = A|𝒴|^p` with `𝒴 = |∇φ|²`. The field equation is `∇·(𝒥_𝒴∇φ) = source`, and `𝒥_𝒴 ∝ |∇φ|^{2p−2}`. For a point mass, `|∇φ|^{2p−1} r² = const`, so

```
force ∝ r^{−2/(2p−1)}
```

| `p` | exponent | law |
|---|---|---|
| 1 | −2 | Newtonian `1/r²` |
| **3/2** | **−1** | **MOND `1/r`** |
| 2 | −2/3 | shallower than MOND |
| 5/2 | −1/2 | much shallower |

**`p = 3/2` is the unique power giving the `1/r` MOND force.** Every `p > 3/2` gives a *shallower* falloff, i.e. **more** force at large radii, not less. Replacing the `p = 3/2` term with `p > 3/2` to fix Cassini would delete the galactic phenomenology the entire programme exists for.

`[C]` SZ22 states both halves of this verbatim: *"MOND behavior emerges if `𝒥 → 2λ_s/(3(1+λ_s)a₀)|𝒴|^{3/2}`"* and *"Screening may be achieved either through terms in `𝒥 ~ 𝒴^p` with `p > 3/2` **or** through Galileon-type terms."* The word is "or": `p > 3/2` is an **alternative to** MOND, not an addition.

**`[O]` The correct Cassini route is the other branch SZ name: a Galileon-type term added to the action**, which can screen above `a₀` while leaving the `p = 3/2` MOND limit intact at galactic accelerations. That term is not written here and its `Q₂` suppression magnitude is not computed.

## 3. The rule is now enforced in code

`scripts/survival_vector_gate.py` gained `--op-power` and `--require-w-radiation`. The `F₅ ⊗ F₄` rule is a **blocking** check when the flag is set, so a drifting operator cannot enter later by inattention.

```
--op-power 3 --require-w-radiation  ->  FAIL  w = 0.500000, rho ~ a^-4.50, eps_Q DRIFTS
--op-power 4 --require-w-radiation  ->  PASS  w = 0.333333, rho ~ a^-4.00, constant eps_Q
```

Gate output for the `Q⁴` witness (`K_B = 0.008`, `λ_s = 11.2787`, `ε_Q = 0.03840`, `𝒦₂ = 300`): all blocking observables pass, `G_cosmo/G_N = 0.950015`, `c_s² = 0.8674`, `c_T = c`, `w = 1/3`. **Exit 0, non-empty joint window.** Self-test unchanged (no regression).

## 4. Verdict table

| Claim | Tag |
|---|---|
| `𝓕 = −c𝒬⁴` gives `w = 1/3` exactly, `ρ_φ ∝ a^{−4}` | `[P]` |
| `w = 1/3` makes `ε_Q` the same constant at BBN and CMB | `[P]` |
| `ε_Q` is still free; `ΔN_eff` stays a range | `[D]` |
| `p = 3/2` is the unique MOND power | `[P]` |
| `p > 3/2` breaks the `1/r` force | `[P]` |
| `p ≥ 3/2` as a Cassini fix | **`[X]`** |
| Galileon term is the viable screening route | `[O]` |
| `Q₂` suppression magnitude computed | **`[O]` not computed** |
| Coupled FLRW `2×2` and `c_{s,±}²` | **`[O]`** (unchanged from #227) |

## 5. What this does not fix

Two gaps survive, and neither is closed by anything here:

1. **Cassini `Q₂` still has no computed suppression.** The gate's observable 2 passes only because a screening scale is *declared*. The Galileon term is named, not derived, and its magnitude is not calculated. `CLM-D3-03`'s 119× Vainshtein margin remains retracted.
2. **The coupled `2×2` remains underived** (#227 §5). Adding `𝒬⁴` does not change that; it changes `c_s²` from `1/2` to `1/3` in the isolated sector and leaves the aether-mixing question exactly where it was.

So Theory 3 is a real improvement on one axis (`w = 1/3`, immunized) and a non-starter on the other (`p ≥ 3/2`). The honest position: adopt half of it, and the remaining work is the Galileon term plus the coupled eigenmode computation.
