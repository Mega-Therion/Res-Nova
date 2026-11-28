# Joint LLR–MICROSCOPE likelihood and higher-multipole wall filters

## 1. What can be calculated from the current evidence

Res Nova’s current dark-bubble audit gives an active composition-dependent scale

```text
η_active(Al,Fe) ≥ 9.02 × 10⁻³,
```

over its stated scan, compared with the LLR bound

```text
|η_LLR| < 3.9 × 10⁻¹⁴.
```

MICROSCOPE reports the Ti/Pt differential-acceleration result

```text
η_MIC^obs = −1.5 × 10⁻¹⁵,
σ_stat = 2.3 × 10⁻¹⁵,
σ_sys  = 1.5 × 10⁻¹⁵.
```

The quantity requested,

```text
Δq_ℓ^P ≡ q^P_{Ti,ℓ} − q^P_{Pt,ℓ},
```

does not have a unique numerical value from these two bounds alone. It is a passive wall coupling, whereas the Res Nova number is an active Al/Fe source-composition result. A numerical value requires the wall multipole amplitude, the source composition, the transfer normalization, and the sector-energy map from microscopic weights to Ti/Pt passive response.

The exact conditional result is instead a bound on the weighted sum of passive coupling differences.

## 2. Conditional magnitude required by the MICROSCOPE null

For each multipole define the wall-filter amplitude at the test bodies by

```text
F_ℓ(ε)
 = J_{out,ℓ}(ε)η_{+,ℓ} + J_{in,ℓ}(ε)η_{−,ℓ}.
```

Let `Δq_ℓ^P = q^P_{Ti,ℓ} − q^P_{Pt,ℓ}`. To first order around unit passive response,

```text
η_MIC^model(θ)
 = η_0^P + Σ_ℓ Δq_ℓ^P F_ℓ(ε),
```

where `η_0^P` contains any non-wall passive Ti/Pt contribution and `θ` denotes all nuisance and theory parameters.

Define the total wall-weighted difference

```text
Q_MIC^P ≡ Σ_ℓ Δq_ℓ^P F_ℓ(ε).
```

Then the measured central value requires

```text
Q_MIC^P ≈ η_MIC^obs − η_0^P,
```

and a conservative two-standard-deviation interval, using quadrature for the quoted statistical and systematic errors, is

```text
σ_MIC = sqrt[(2.3×10⁻¹⁵)² + (1.5×10⁻¹⁵)²]
       = 2.746×10⁻¹⁵,

|Q_MIC^P − (η_MIC^obs−η_0^P)| ≲ 5.49×10⁻¹⁵.
```

If one mode dominates and `η_0^P=0`, the conditional bound is

```text
|Δq_ℓ^P| ≲ 5.49×10⁻¹⁵ / |F_ℓ(ε)|
```

at approximately 95% Gaussian coverage around the measured central value. This is the exact magnitude statement available without an amplitude model.

If instead the wall amplitude is normalized so that `F_ℓ=1`, then the passive Ti/Pt coupling difference must be at most approximately `5.5×10⁻¹⁵` at 95% level. That normalization is an assumption, not a result of either LLR or MICROSCOPE.

The active LLR number does not force `Δq_ℓ^P` to be `9.02×10⁻³`. If the theory imposes identical active and passive weights, then the sector composition calculation must produce both quantities and MICROSCOPE constrains the resulting Ti/Pt combination. If the theory changes only active source weights while matter follows the induced metric minimally, then `Δq_ℓ^P=0` is possible while the active LLR obstruction remains. Conversely, if one artificially requires the wall to cancel a hypothetical `+9.02×10⁻³` Ti/Pt passive signal with one normalized mode, the required correction would be `Δq_ℓ^P≈−9.02×10⁻³`; that is not implied by the actual Res Nova LLR result and would be a new model assumption.

## 3. Sector-level passive mapping

Let `E_a^T` be the inertial energy in sector `a` of test body `T`, and let `v_a^P` be its passive wall weight. Then

```text
M_T^I = c⁻² Σ_a E_a^T,
κ_T^P = (c⁻² Σ_a v_a^P E_a^T)/M_T^I.
```

For Ti and Pt,

```text
Δq_ℓ^P
 = Σ_a v_{a,ℓ}^P
   [f_a^{Ti} − f_a^{Pt}],
```

where `f_a^T=E_a^T/(c²M_T^I)` and `v_{a,ℓ}^P` is the passive coupling of sector `a` to wall multipole `ℓ`. This is the missing source-to-test calculation. It must include nuclear binding, electromagnetic Coulomb energy, electron energy, and the model’s QCD sector assignment under one fixed convention.

The active coefficient for an LLR body `A` is separately

```text
κ_A^A = Σ_a w_a^A f_a^A,
```

with active weights `w_a^A`. The LLR and MICROSCOPE parameters must not share `w` and `v` unless that equality is derived from the action.

## 4. Complete joint Bayesian likelihood

Let the parameter vector be

```text
θ = {w_a, v_{a,ℓ}^P, η_{+,ℓ}, η_{−,ℓ}, ε,
     orbital parameters, calibration parameters, nuisance parameters}.
```

The sector map produces active coefficients `κ_A^A(θ)` for Sun, Earth, Moon, Al, Fe, and other ephemeris bodies, and passive coefficients `κ_T^P(θ)` for Ti and Pt. The rim transfer is

```text
J_{out,ℓ}(θ) ∝ cosh(2εu_ℓ)/sinh(2u_ℓ),
J_{in,ℓ}(θ)  ∝ −cosh(2(1−ε)u_ℓ)/sinh(2u_ℓ),
```

with `u_ℓ=κ_ℓΔR/2`.

### LLR likelihood

Let `y_LLR` be the vector of observed lunar-range residuals at the published epochs, with covariance `C_LLR`. Integrate or numerically solve the N-body equations

```text
d²r_B/dt²
 = −G_* Σ_{A≠B} M_A^I κ_A^A(θ)κ_B^P(θ)
     (r_B−r_A)/|r_B−r_A|³
   + a_B^SE(θ) + a_B^finite(θ) + a_B^other(θ).
```

After applying the same ephemeris fit and nuisance convention to model and data, let `m_LLR(θ)` be the predicted range-residual vector. The Gaussian LLR likelihood is

```text
ln L_LLR(θ)
 = −1/2 [y_LLR−m_LLR(θ)]ᵀ C_LLR⁻¹ [y_LLR−m_LLR(θ)]
   −1/2 ln det(2πC_LLR).
```

An LLR-only summary constraint may instead use an observed Eötvös statistic `y_LLR^η` with variance `σ_LLR²`:

```text
ln L_LLR^η(θ)
 = −1/2 [y_LLR^η−η_LLR^model(θ)]²/σ_LLR²
   −1/2 ln(2πσ_LLR²),
```

but this compressed form is not equivalent to the full ephemeris likelihood unless the published reduction justifies it.

### MICROSCOPE likelihood

The model prediction is

```text
η_MIC^model(θ)
 = 2[a_Ti(θ)−a_Pt(θ)]/[a_Ti(θ)+a_Pt(θ)],

a_T(θ)
 = −G_* M_E^I κ_E^A(θ)κ_T^P(θ)/r²
   + a_T^wall(θ).
```

At leading order,

```text
η_MIC^model(θ)
 ≈ η_0^P(θ) + Σ_ℓ Δq_ℓ^P(θ)F_ℓ(θ).
```

Using the reported central value and separated statistical/systematic Gaussian terms,

```text
ln L_MIC(θ)
 = −1/2 [η_MIC^obs−η_MIC^model(θ)]²
       /(σ_stat²+σ_sys²)
   −1/2 ln[2π(σ_stat²+σ_sys²)].
```

If a full MICROSCOPE covariance or nuisance model is available, replace the scalar expression with the corresponding multivariate likelihood and keep systematic parameters explicit rather than adding them in quadrature.

### Joint posterior

Assuming conditional independence of the released LLR and MICROSCOPE data sets given `θ`,

```text
p(θ | D_LLR,D_MIC)
 ∝ L_LLR(θ)L_MIC(θ)π(θ).
```

Equivalently,

```text
ln p(θ|D)
 = ln L_LLR(θ) + ln L_MIC(θ) + ln π(θ) + constant.
```

The prior must state the allowed active weights, passive weights, wall amplitudes, observer offset, and calibration ranges before fitting. In particular, setting `v_a^P=w_a` is a model hypothesis, not a nuisance choice. The joint Bayes factor comparing a universal passive wall force (`Δq_ℓ^P=0`) with a composition-dependent wall force (`Δq_ℓ^P≠0`) should be computed from the same priors and likelihood, not from post-fit tuning.

## 5. Can higher multipoles bypass Ti/Pt cancellation?

Not by geometry alone. For a universal wall filter, `F_ℓ(ε)` is independent of the test-body composition. If Ti and Pt couple identically, then

```text
q_{Ti,ℓ}^P = q_{Pt,ℓ}^P,
Δq_ℓ^P = 0,
```

and every multipole cancels from the differential acceleration, regardless of how large `R_ℓ` becomes.

Higher multipoles can produce a non-universal force only through an additional composition-dependent ingredient, such as:

1. sector-dependent passive wall weights `v_{a,ℓ}^P`;
2. different finite-size form factors for Ti and Pt;
3. composition-dependent boundary conditions or wall charges;
4. nonlinear backreaction in which the test body changes the wall source amplitudes;
5. a non-universal matter metric or disformal coupling.

A finite test-mass separation can make a universal high-`ℓ` field produce a gradient across the accelerometer, but that is an instrumental spatial effect, not a composition-dependent WEP violation. It still requires a full instrument model and does not evade the Ti/Pt cancellation if both materials sample the same force law.

Thus higher multipoles can amplify an existing `Δq_ℓ^P`, especially because `R_ℓ` grows with `u_ℓ`, but they cannot generate `Δq_ℓ^P` from zero. In the symmetric midpoint case `ε=1/2`, the geometric filter is exactly balanced for every `ℓ`, making this route even less capable of producing a rim-induced differential signal.

## 6. Evidence-led conclusion

The current evidence does not determine a unique numerical `q^P_{Ti,ℓ}−q^P_{Pt,ℓ}`. The correct conditional 95% bound is `|Σ_ℓΔq_ℓ^P F_ℓ|` of order `5.5×10⁻¹⁵` after subtracting any separately modelled baseline passive signal. Res Nova’s `9.02×10⁻³` active Al/Fe LLR scale cannot be inserted into this equation without a derived active-to-passive map.

The complete joint likelihood is the product of the LLR ephemeris likelihood and the MICROSCOPE differential-acceleration likelihood under one shared sector-weight and wall-transfer parameter vector. Higher-order multipoles do not bypass differential cancellation unless the action supplies genuinely non-universal passive matter couplings or composition-dependent source/boundary terms. The geometric rim ratio alone is insufficient.

## References

[1]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo"
[2]: https://arxiv.org/abs/2209.15487 "MICROSCOPE mission final results"
[3]: https://github.com/Mega-Therion/Res-Nova/blob/4ad334721f63781f2b6c832bf33272606a56ce33/exploration/bulk5d/WEP_2507_03748_AUDIT.json "Res Nova WEP audit receipt"
