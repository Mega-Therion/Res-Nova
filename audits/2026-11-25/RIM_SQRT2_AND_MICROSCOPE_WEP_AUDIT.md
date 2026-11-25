# Rim `√2` factor and MICROSCOPE/WEP interpretation audit

**Sources:** shared Gemini memo [1]; MICROSCOPE final results [2] [3]; Res Nova WEP receipt `exploration/bulk5d/WEP_2507_03748_AUDIT.json`; current-state ledger `CURRENT_STATE_READ_THIS_FIRST.md`.

## 1. Where the `√2` enters the rim equations

The memo’s rim law is not obtained by solving for a special value of `ε`. It first assumes a one-dimensional evanescent wall profile and then evaluates the resulting transfer functions at a chosen observer location.

For a sub-acoustic mode, the memo uses the radial profile

```text
Z(z) = A cosh(κz) + B sinh(κz),
κ = Λ(x) k,
```

with wall thickness `ΔR` and dimensionless depth variable

```text
u = (1/2) Λ(x) k ΔR.
```

The rim-to-observer Jacobians are then stated as

```text
J_out ∝ + cosh(2 ε u) / sinh(2u),
J_in  ∝ − cosh(2(1−ε)u) / sinh(2u).
```

Taking magnitudes gives

```text
R_rim(u; ε) = |J_out/J_in|
             = cosh(2 ε u) / cosh(2(1−ε)u).
```

This is the mathematical identity. The factor `√2` appears only when the observer fraction is set to

```text
ε = 1/√2.
```

The two hyperbolic arguments become

```text
2 ε u       = √2 u,
2(1−ε)u    = (2−√2)u.
```

The associated midpoint coordinate and distance ratio are therefore

```text
ζ = 2ε−1 = √2−1,
ε/(1−ε) = (1/√2)/(1−1/√2) = 1+√2.
```

Thus the `√2` is a geometric input to the transfer law, not a new eigenvalue or a factor derived from the AQUAL stiffness tensor. The wall field equation supplies the hyperbolic functions and the scale `κ = Λk`; the choice `ε = 1/√2` supplies the `√2` in their arguments.

### Small-`u` limit

Using `cosh(a u) = 1 + a²u²/2 + O(u⁴)`,

```text
R_rim = 1 + 2[ε² − (1−ε)²]u² + O(u⁴)
      = 1 + 2(2ε−1)u² + O(u⁴).
```

For `ε = 1/√2`, this becomes

```text
R_rim = 1 + 2(√2−1)u² + O(u⁴),
```

which is the memo’s infrared expression. For `ε = 1/2`, the coefficient vanishes and the exact ratio is

```text
R_rim(u; 1/2) = cosh(u)/cosh(u) = 1.
```

The midplane has no rim asymmetry at any depth; this is not merely a low-`u` approximation.

### Large-`u` limit

For positive arguments, `cosh(a u) ~ exp(a u)/2`. Therefore

```text
R_rim ~ exp{[2ε − 2(1−ε)]u}
       = exp[2(2ε−1)u].
```

At `ε = 1/√2`, and using `2u = Λ(x) k ΔR`,

```text
R_rim ~ exp[(√2−1) Λ(x) k ΔR].
```

At `ε = 1/2`, the exponent is zero and the ratio remains one. Consequently, the memo’s quoted values `1.0021`, `1.2084`, `2.6265`, `11.66`, and `62.76` necessarily belong to the off-center choice `ε = 1/√2`; they cannot follow from its stated midplane value `ε = 1/2`.

The field-equation status should therefore be recorded as follows: the hyperbolic transfer identity is a conditional derivation `[D]` from the stated waveguide equation and boundary geometry; the specific `√2` placement is a model/geometry choice; and the memo’s simultaneous use of both choices is an internal convention error that blocks a single reproducible prediction.

## 2. What MICROSCOPE actually measured

The MICROSCOPE experiment compared the accelerations of two collocated test masses with different compositions while they orbited Earth. It inferred an Eötvös parameter from the differential acceleration, with the final Ti–Pt result

```text
η(Ti,Pt) = [−1.5 ± 2.3 (stat) ± 1.5 (syst)] × 10⁻¹⁵
```

at one standard deviation [2] [3]. Operationally, this is a test of whether different test bodies have the same free-fall acceleration in the same external gravitational field. In a point-particle description, the directly constrained quantity is the composition dependence of the test body’s effective gravitational-to-inertial response, often called the passive WEP channel.

That observable is not the same object as the gravitational mass of a proton considered as a source. A source-side modification changes the stress-energy that generates the external field. To turn such a modification into a MICROSCOPE prediction, one must derive the full mapping from the model’s source coupling, Earth’s composition, the test masses’ composition, and the measured differential acceleration. The Gemini memo does not supply that mapping; it inserts the proton ratio directly into the MICROSCOPE bound.

## 3. Exact difference between the memo and Res Nova

The memo states that the B/C-field embedding gives

```text
⟨N|T_q^{00} − T_g^{00}|N⟩ = (0.009 ± 0.037) m_p,
(m_p^(g) − m_p^(i))/m_p^(i) ≃ 0.99,
```

and labels this a direct violation of the MICROSCOPE WEP limit by 13 orders [1]. The source paper itself describes a significant difference between the proton’s gravitational and inertial masses and says that the equivalence principle is severely violated [4], but the shared memo’s direct identification with the MICROSCOPE observable is not established by the equations quoted in the memo.

Res Nova’s `C4_active_passive` audit makes the distinction explicit:

- **Passive channel:** brane fields couple minimally to the induced metric and their free-fall trajectories are universal. Res Nova records this as the channel MICROSCOPE tests.
- **Active channel:** the sign rule changes the source `T^{00}`. The active/inertial mass becomes composition dependent.
- **Interpretation:** a universal baryonic rescaling can be absorbed into `G4`; what survives is composition dependence in the source. The decisive repository gate is therefore an active-mass comparison, not simply the proton’s absolute `m_g/m_i` ratio.

The repository’s scan varies the nuclear Coulomb coefficient and electron sign over its stated band. It finds

```text
η_active(Al,Fe) ≥ 0.00902,
```

and compares this with the LLR bound `3.9 × 10⁻¹⁴`, giving an excess of about `11.4` orders of magnitude. `CURRENT_STATE_READ_THIS_FIRST.md` summarizes this as the B/C-field dark-bubble embedding being `[X]` as formulated, with active-mass Al/Fe excluded by LLR by approximately 11 orders.

The difference is therefore not that Res Nova accepts the dark-bubble construction. Both analyses reject the B/C-field route. The difference is the observable and the evidence chain:

| Issue | Gemini memo | Res Nova record |
|---|---|---|
| Starting anomaly | Proton gravitational/inertial ratio near `0.99` | Composition-dependent active source mass induced by the same sign rule |
| Experimental identification | Directly compared with MICROSCOPE | MICROSCOPE is passive; active source composition is tested through an LLR channel in the audit |
| Composition mapping | Not derived from Earth, Ti/Pt, and test-body source/response composition | Explicit Al/Fe active-mass scan over nuisance/sign choices |
| Bound used | `≲10⁻¹⁵` and “13 orders” | `3.9×10⁻¹⁴` LLR bound and `η_active≥9.02×10⁻³`, about `11.4` orders |
| Repository status | External memo label | `[X]` for the B/C embedding as formulated; reopening requires a non-B/C mechanism and a derived quark sign |

There is also a numerical wording problem in the memo. A `0.99` fractional anomaly divided by `10⁻¹⁵` is approximately `10¹⁵`, or 15 orders, whereas a `10⁻²` composition-dependent difference divided by `10⁻¹⁵` is approximately 13 orders. The memo appears to move between the order-one proton ratio and the smaller composition-difference scale without stating which quantity is being compared. Res Nova avoids that ambiguity by reporting the composition-dependent active-mass observable and its LLR comparison.

## 4. Evidence-led disposition

The rim derivation supports a precise conditional identity:

> **The waveguide equation plus the off-center choice `ε = 1/√2` gives the memo’s `√2` arguments and rim-dominance values.**

It does not support the same values under `ε = 1/2`, and no field equation shown in the memo dynamically selects `ε = 1/√2`. The convention must be fixed before the result can be treated as one prediction.

For WEP, the memo correctly identifies a severe obstruction to the specified B/C-field embedding, but its MICROSCOPE attribution is not a completed observable derivation. Res Nova’s `[X]` record is the authoritative repository conclusion because it preserves the active/passive distinction, derives composition dependence for Al/Fe, and uses the LLR channel with an explicit nuisance scan. This supports rejection of the route, not acceptance of the memo’s exact “13 orders via MICROSCOPE” formulation.

## References

[1]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo"
[2]: https://arxiv.org/abs/2209.15487 "MICROSCOPE mission final results on the Eötvös parameter"
[3]: https://link.aps.org/doi/10.1103/PhysRevLett.129.121102 "MICROSCOPE final results in Physical Review Letters"
[4]: https://arxiv.org/abs/2507.03748 "Dark bubble cosmology and the equivalence principle"
