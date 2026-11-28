# Rim-ratio perturbation and filtered Ti/Pt Eötvös response

## 1. Expansion about the midpoint

For multipole `ℓ`, define

```text
u_ℓ = κ_ℓ ΔR/2,
κ_ℓ² = [c_parallel² k_ℓ² − ω²]/c_z²,
k_ℓ² = ℓ(ℓ+2)/R²,
```

and write the observer fraction as a small displacement from the midpoint,

```text
ε = 1/2 + δ,
|δ| ≪ 1.
```

The exact transfer-law ratio is

```text
R_ℓ(ε)
 = cosh(2εu_ℓ)/cosh(2(1−ε)u_ℓ)
 = cosh[(1+2δ)u_ℓ]/cosh[(1−2δ)u_ℓ].
```

Define the rim-ratio deviation by

```text
ΔR_ℓ(δ) ≡ R_ℓ(1/2+δ) − 1.
```

Let `f(x)=log cosh x`. Then

```text
log R_ℓ = f(u_ℓ+2δu_ℓ) − f(u_ℓ−2δu_ℓ).
```

Because the difference is odd in `δ`,

```text
log R_ℓ
 = 4δu_ℓ tanh(u_ℓ)
   − (16/3)δ³u_ℓ³ sech²(u_ℓ)tanh(u_ℓ)
   + O(δ⁵).
```

There is no `δ²` or `δ⁴` term in `log R_ℓ`; reversing the observer from one side of the midpoint to the other sends `δ → −δ` and exchanges the two rims, so `R_ℓ → 1/R_ℓ`.

Exponentiating gives the direct deviation series through cubic order:

```text
ΔR_ℓ
 = 4δu_ℓ t_ℓ
   + 8δ²u_ℓ² t_ℓ²
   + 16δ³u_ℓ³(t_ℓ³ − t_ℓ/3)
   + O(δ⁴),
```

where `t_ℓ = tanh(u_ℓ)`. Equivalently, the first derivative at the symmetric point is

```text
(∂R_ℓ/∂ε)_{ε=1/2} = 4u_ℓ tanh(u_ℓ).
```

Thus a small positive displacement toward the outer rim produces an outer-rim excess, while a negative displacement produces an inner-rim excess.

### Long-wavelength form

For `u_ℓ ≪ 1`, `tanh u_ℓ = u_ℓ − u_ℓ³/3 + O(u_ℓ⁵)`, so

```text
ΔR_ℓ
 = 4δu_ℓ²
   + 8δ²u_ℓ⁴
   + δ³(16u_ℓ⁴ − 16u_ℓ⁶/3)
   + O(δu_ℓ⁶, δ²u_ℓ⁶, δ⁴).
```

Keeping only the leading joint order gives

```text
ΔR_ℓ = 4δu_ℓ² + O(δu_ℓ⁴, δ²u_ℓ⁴).
```

Since `u_ℓ = Λk_ℓΔR/2`,

```text
ΔR_ℓ ≈ δ Λ²(x) k_ℓ² ΔR².
```

With `k_ℓ²=ℓ(ℓ+2)/R²`, the leading midpoint-breaking term is

```text
ΔR_ℓ ≈ δ Λ²(x) ΔR² ℓ(ℓ+2)/R².
```

This is quadratic in the multipole wavenumber at low `u_ℓ`, not linear. The off-center effect is therefore suppressed for the lowest long-wavelength modes and grows toward higher multipoles until the evanescent/high-`u_ℓ` approximation takes over.

### High-`u_ℓ` form

For `u_ℓ ≫ 1`,

```text
R_ℓ ≈ exp(4δu_ℓ),
ΔR_ℓ ≈ exp(4δu_ℓ) − 1.
```

This approximation remains perturbative only when `|δ|u_ℓ ≪ 1`. A small geometric offset can therefore produce a large high-multipole change even though `|δ|` itself is small. For fixed nonzero `δ`, the linear series in `δ` eventually fails and the exponential form must be retained.

For the memo’s off-center convention,

```text
δ = 1/√2 − 1/2 = (√2−1)/2,
```

so `4δ = 2(√2−1)`, recovering

```text
R_ℓ ~ exp[2(√2−1)u_ℓ]
    = exp[(√2−1)Λ(x)k_ℓΔR].
```

## 2. How a rim filter could enter an Eötvös prediction

The rim ratio is a transfer-function ratio. By itself it is not a new coupling to matter and does not change the MICROSCOPE Eötvös parameter. To affect Ti/Pt free fall, the model must specify a wall-mediated, composition-dependent passive response.

Let `q_{T,ℓ}^{P}` be the passive coupling of test body `T` to the `ℓ`th wall multipole, and let the rim displacements be `η_{+,ℓ}` and `η_{−,ℓ}`. Write the wall-induced passive response as

```text
χ_T^P(ε)
 = Σ_ℓ q_{T,ℓ}^P
   [J_{out,ℓ}(ε)η_{+,ℓ} + J_{in,ℓ}(ε)η_{−,ℓ}].
```

The total passive response is then

```text
κ_T^P(ε) = κ_{T,0}^P + χ_T^P(ε),
```

where `κ_{T,0}^P` is the ordinary long-range response. For a common external source, the leading Ti/Pt accelerations are

```text
a_T(ε) = −G_* M_E^I κ_E^A κ_T^P(ε)/r².
```

Consequently,

```text
η_{Ti,Pt}(ε)
 = 2[a_Ti(ε)−a_Pt(ε)]/[a_Ti(ε)+a_Pt(ε)]
 = 2[κ_Ti^P(ε)−κ_Pt^P(ε)]
   /[κ_Ti^P(ε)+κ_Pt^P(ε)].
```

For small deviations around a common unit response,

```text
η_{Ti,Pt}(ε)
 ≈ [κ_Ti,0^P−κ_Pt,0^P]
   + Σ_ℓ [q_{Ti,ℓ}^P−q_{Pt,ℓ}^P]
       [J_{out,ℓ}η_{+,ℓ}+J_{in,ℓ}η_{−,ℓ}].
```

The Earth active factor `κ_E^A` cancels at this leading differential-acceleration order. Therefore the rim filter changes the Eötvös parameter only through a difference in passive Ti/Pt multipole couplings.

## 3. Expressing the filter through `R_ℓ`

Since

```text
J_{out,ℓ} = R_ℓ J_{in,ℓ}
```

in magnitude, one may choose the inner-rim normalization and write, with the sign convention retained,

```text
χ_T^P(ε)
 = Σ_ℓ q_{T,ℓ}^P J_{in,ℓ}(ε)
     [s_ℓ R_ℓ(ε)η_{+,ℓ} + η_{−,ℓ}],
```

where `s_ℓ` records the relative orientation/sign of the two rim source amplitudes. Then the filter-induced Eötvös contribution relative to the midpoint is

```text
δη_{Ti,Pt}^{filter}
 ≈ Σ_ℓ Δq_ℓ^P
   {J_{in,ℓ}(ε)[s_ℓR_ℓ(ε)η_{+,ℓ}+η_{−,ℓ}]
    − J_{in,ℓ}(1/2)[s_ℓη_{+,ℓ}+η_{−,ℓ}]},
```

with

```text
Δq_ℓ^P ≡ q_{Ti,ℓ}^P − q_{Pt,ℓ}^P.
```

If the absolute normalization and `J_{in}` are held fixed for the comparison, the pure ratio part is

```text
δη_{Ti,Pt}^{ratio}
 ∝ Σ_ℓ Δq_ℓ^P J_{in,ℓ}
      s_ℓη_{+,ℓ} ΔR_ℓ.
```

Using the midpoint perturbation,

```text
ΔR_ℓ
 = 4δu_ℓ tanh(u_ℓ)
   + 8δ²u_ℓ²tanh²(u_ℓ)
   + O(δ³),
```

gives the leading filter correction

```text
δη_{Ti,Pt}^{ratio}
 ∝ 4δ Σ_ℓ Δq_ℓ^P J_{in,ℓ}s_ℓη_{+,ℓ}
          u_ℓ tanh(u_ℓ).
```

At long wavelength,

```text
δη_{Ti,Pt}^{ratio}
 ∝ 4δ Σ_ℓ Δq_ℓ^P J_{in,ℓ}s_ℓη_{+,ℓ}u_ℓ².
```

At high multipole, the perturbative expression must be replaced by the exact `R_ℓ` because `R_ℓ` can grow as `exp(4δu_ℓ)`.

## 4. What does and does not follow for MICROSCOPE

Three cases must be separated.

1. **Pure observation filter:** If the rim transfer changes only which wall perturbation an observer sees, and it does not modify the metric or force acting on Ti and Pt, then `q_{Ti,ℓ}^P=q_{Pt,ℓ}^P=0` for this channel and `η_{Ti,Pt}` is unchanged. The filter is an observational weighting, not a WEP violation.

2. **Universal wall force:** If the wall force is present but has the same passive coupling per unit inertial mass for Ti and Pt, then the common contribution cancels to first order in the differential acceleration. A large `R_ℓ` does not by itself imply a large Eötvös signal.

3. **Composition-dependent wall coupling:** Only if `Δq_ℓ^P ≠ 0` does the rim filter alter the predicted Ti/Pt Eötvös parameter. The model must then provide the sector-energy fractions and passive weights for Ti and Pt, together with the source amplitudes `η_{±,ℓ}` and the metric/force map.

Res Nova’s current `[X]` dark-bubble result is an active-mass obstruction based on the B/C sector weights and an Al/Fe LLR channel. It should not be converted into a MICROSCOPE prediction by multiplying the active discrepancy by `R_ℓ`. A valid conversion requires the passive Ti/Pt coefficients `q_{Ti,ℓ}^P` and `q_{Pt,ℓ}^P` and an action-level map from the wall field to the matter metric.

## 5. Bottom line

The midpoint is a fixed point of the rim ratio: `R_ℓ=1` at `ε=1/2` for every multipole. A small displacement `δ` produces a linear low-order deviation `4δu_ℓtanh(u_ℓ)`, which becomes approximately `4δu_ℓ²` for long wavelengths and exponentially large at high `u_ℓ` outside the strict perturbative regime. The Eötvös parameter is modified only when this transfer function multiplies a genuinely composition-dependent passive Ti/Pt coupling; the rim ratio alone is insufficient.

## References

[1]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo"
[2]: https://arxiv.org/abs/2209.15487 "MICROSCOPE mission final results"
[3]: https://github.com/Mega-Therion/Res-Nova/blob/4ad334721f63781f2b6c832bf33272606a56ce33/exploration/bulk5d/WEP_2507_03748_AUDIT.json "Res Nova WEP audit receipt"
