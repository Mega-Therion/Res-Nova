# Full rim multipole and WEP source-to-test mapping

**Repository:** `Mega-Therion/Res-Nova`  
**Audited commit before publication:** `212b55a8da278f1363d82642b736fc7ef30dee7c`  
**External memo:** [shared Gemini memo](https://share.gemini.google/WSbeUhQq0q9S)

## 1. Transfer-law solution

Let the wall occupy `−H/2 ≤ z ≤ H/2`, with `H = ΔR`. For a tangential multipole of angular degree `ℓ` on `S³(R)`,

```text
k_ℓ² = ℓ(ℓ+2)/R².
```

The sub-acoustic radial equation is

```text
c_z² Z_ℓ''(z) + [ω² − c_parallel² k_ℓ²] Z_ℓ(z) = 0.
```

In the evanescent regime, define

```text
κ_ℓ² = [c_parallel² k_ℓ² − ω²]/c_z²,
Z_ℓ'' − κ_ℓ² Z_ℓ = 0,
Z_ℓ(z) = A_ℓ cosh(κ_ℓ z) + B_ℓ sinh(κ_ℓ z).
```

In the memo’s incompressible/sub-acoustic limit, `κ_ℓ = Λ(x)k_ℓ`. Set

```text
u_ℓ = κ_ℓH/2 = Λ(x)k_ℓΔR/2.
```

An observer at fraction `ε` from the inner rim has

```text
z_o = −H/2 + εH,
ζ = 2z_o/H = 2ε−1.
```

The inner and outer distances are `εH` and `(1−ε)H`, hence

```text
κ_ℓ d_in  = 2εu_ℓ,
κ_ℓ d_out = 2(1−ε)u_ℓ.
```

The even/odd branch recombination uses

```text
cosh(ζu_ℓ)cosh(u_ℓ) + sinh(ζu_ℓ)sinh(u_ℓ)
  = cosh[(1+ζ)u_ℓ],

cosh(ζu_ℓ)cosh(u_ℓ) − sinh(ζu_ℓ)sinh(u_ℓ)
  = cosh[(1−ζ)u_ℓ].
```

With the two-rim normalization `sinh(2u_ℓ) = sinh(κ_ℓH)`, the conditional Jacobians are

```text
J_{out,ℓ} ∝ + cosh[(1+ζ)u_ℓ]/sinh(2u_ℓ),
J_{in,ℓ}  ∝ − cosh[(1−ζ)u_ℓ]/sinh(2u_ℓ).
```

Since `1+ζ = 2ε` and `1−ζ = 2(1−ε)`,

```text
J_{out,ℓ} ∝ + cosh(2εu_ℓ)/sinh(2u_ℓ),
J_{in,ℓ}  ∝ − cosh(2(1−ε)u_ℓ)/sinh(2u_ℓ).
```

Therefore the exact per-multipole rim ratio is

```text
R_ℓ(ε)
 = |J_{out,ℓ}/J_{in,ℓ}|
 = cosh(2εu_ℓ)/cosh(2(1−ε)u_ℓ).
```

The transfer equation derives this functional form. It does not derive a numerical value for `ε`.

## 2. How the off-center `√2` convention enters

If the geometry separately imposes

```text
ε = 1/√2,
```

then

```text
ζ = √2−1,
2εu_ℓ = √2u_ℓ,
2(1−ε)u_ℓ = (2−√2)u_ℓ,
```

and

```text
R_ℓ(1/√2)
 = cosh(√2u_ℓ)/cosh[(2−√2)u_ℓ].
```

Thus `√2` is a geometric substitution into the transfer solution. No equation displayed in the memo dynamically selects `ε = 1/√2`; it is not a radial eigenvalue, an AQUAL sound-cone eigenvalue, or a consequence of the wall Euler–Lagrange equation.

For small `u_ℓ`,

```text
log cosh y = y²/2 − y⁴/12 + y⁶/45 + O(y⁸),
```

so

```text
log R_ℓ
 = 2(2ε−1)u_ℓ²
 − (4/3)[ε⁴−(1−ε)⁴]u_ℓ⁴
 + (64/45)[ε⁶−(1−ε)⁶]u_ℓ⁶
 + O(u_ℓ⁸).
```

At `ε = 1/√2`, the first terms are

```text
log R_ℓ
 = 2(√2−1)u_ℓ²
 − (4/3)[1/4 − (1−1/√2)^4]u_ℓ⁴
 + (64/45)[1/8 − (1−1/√2)^6]u_ℓ⁶
 + … .
```

At large `u_ℓ`,

```text
R_ℓ(ε) ~ exp[2(2ε−1)u_ℓ].
```

For the off-center convention,

```text
R_ℓ(1/√2) ~ exp[(√2−1)Λ(x)k_ℓΔR].
```

Because `k_ℓ ~ ℓ/R` at large `ℓ`, this is an exponential high-multipole filter: the outer rim dominates progressively more strongly as `ℓ` increases, provided the evanescent approximation remains valid.

## 3. Exact midpoint result and higher-order multipoles

At the midpoint,

```text
ε = 1/2,
ζ = 0,
z_o = 0,
```

and for every multipole `ℓ`,

```text
J_{out,ℓ} ∝ +cosh(u_ℓ)/sinh(2u_ℓ),
J_{in,ℓ}  ∝ −cosh(u_ℓ)/sinh(2u_ℓ),
R_ℓ(1/2) = 1.
```

This equality is exact for all `ℓ` and all `u_ℓ` within the transfer-law regime. Every coefficient in the small-`u_ℓ` expansion of `log R_ℓ` vanishes because

```text
ε^n − (1−ε)^n = 0
```

for every even power `n` appearing in `log cosh` when `ε = 1/2`.

The centered field itself makes the parity statement transparent:

```text
Z_ℓ(0) = A_ℓ,
```

because `sinh(0)=0`. All odd/sinuous radial contributions vanish at the midpoint. Even/varicose contributions remain, and the wall still has its finite-depth radial modes and anisotropic decay scale. What disappears is not the field solution; it is the observer’s odd-parity sensitivity and therefore the rim asymmetry.

For `ε = 1/√2`, `z_o ≠ 0`, so

```text
Z_ℓ(z_o)
 = A_ℓ[1 + (κ_ℓz_o)²/2 + (κ_ℓz_o)^4/24 + …]
 + B_ℓ[κ_ℓz_o + (κ_ℓz_o)^3/6 + …].
```

The odd radial moments are nonzero. In an angular multipole expansion, this means that each `ℓ` receives the off-center transfer factor `R_ℓ`; the effect is not a new angular field equation but a position-dependent response weighting. The `ε = 1/2` and `ε = 1/√2` cases therefore differ at every nonzero evanescent multipole, while the midpoint remains exactly symmetric even for arbitrarily large `ℓ`.

## 4. Formal sector-weight mapping

For a macroscopic body `A`, let `E_a^A` be the inertial energy in sector `a`. Examples include QCD gluon energy, quark rest/binding energy, electromagnetic Coulomb energy, electron energy, and any additional dark-bubble sector. Let `w_{a,A}` be the active source weight and `v_{a,A}` the passive test-body weight. Then

```text
M_A^I = c^{-2} Σ_a E_a^A,
M_A^A = c^{-2} Σ_a w_{a,A} E_a^A,
M_A^P = c^{-2} Σ_a v_{a,A} E_a^A,
κ_A^A = M_A^A/M_A^I,
κ_A^P = M_A^P/M_A^I.
```

The minimal single-metric branch has `w_{a,A}=v_{a,A}=1`, giving `κ_A^A=κ_A^P=1`. The dark-bubble B/C hypothesis instead assigns sector-dependent weights. In the Res Nova audit, the leading non-Abelian gluon channel has weight `−1`, while the Abelian channel has weight `+1`; the quark sign remains a required derived input rather than a silently chosen rescue.

For source `S` and test body `T`, write the calibrated Newtonian acceleration as

```text
a_{T←S}
 = −G_* M_S^I κ_S^A κ_T^P
     (r_T−r_S)/|r_T−r_S|³.
```

A reference calibration defines

```text
G_ref = G_* κ_{S0}^A κ_{T0}^P.
```

Only composition-dependent departures from the reference factors are observable; a universal factor is absorbed into `G_ref`.

### MICROSCOPE

With Earth as the common external source and Ti/Pt test masses,

```text
a_Ti = −G_* M_E^I κ_E^A κ_Ti^P/r²,
a_Pt = −G_* M_E^I κ_E^A κ_Pt^P/r².
```

Hence

```text
η_MIC
 = 2(a_Ti−a_Pt)/(a_Ti+a_Pt)
 = 2(κ_Ti^P−κ_Pt^P)/(κ_Ti^P+κ_Pt^P)
 ≈ κ_Ti^P−κ_Pt^P.
```

The active Earth factor cancels at leading order. A proton-level active ratio cannot be compared directly with the MICROSCOPE limit without deriving the passive Ti/Pt response from nuclear and electromagnetic sector fractions.

### LLR

For an ephemeris model, every ordered pair must use

```text
a_{B←A}
 = −G_* M_A^I κ_A^A κ_B^P
     (r_B−r_A)/|r_B−r_A|³
```

with self-energy, finite-size, and fitted-parameter terms where required. The leading Sun-directed Earth–Moon differential acceleration is proportional to

```text
κ_S^A(κ_E^P−κ_M^P),
```

while active Earth/Moon factors affect their generated fields, mutual dynamics, fitted masses, and the full range residual model. Therefore an active-mass LLR bound requires an ephemeris-level calculation; it cannot be obtained by relabelling the MICROSCOPE passive ratio.

The joint gate should fit one common parameter vector `w` to both observables:

```text
η_MIC(w) = η_MIC^obs ± σ_MIC,
Δρ_LLR(t;w) = Δρ_LLR^obs(t) ± C_LLR^{1/2},
```

where the same sector fractions and signs generate `κ^A` and `κ^P`. If the model imposes `v_a=1` while changing only `w_a`, then the direct leading-order MICROSCOPE signal is zero but the active LLR channel remains. If it imposes `v_a=w_a`, both experiments receive composition-dependent signals and must be evaluated separately.

Res Nova’s current WEP receipt already finds active Al/Fe composition dependence `η_active ≥ 9.02×10⁻³` over its stated scan, compared with an LLR bound `3.9×10⁻¹⁴`, supporting the `[X]` verdict for the B/C embedding as formulated. A Ti/Pt passive calculation is still required before claiming a direct MICROSCOPE prediction.

## 5. Status implications

The transfer-law identity is a conditional derivation `[D]` under the memo’s wave equation, boundary normalization, and evanescent approximation. The value `ε = 1/√2` is a geometry choice, not a derived dynamical constant. At `ε = 1/2`, all per-multipole rim ratios are exactly one and all higher-order asymmetry coefficients vanish. Any remaining asymmetry must come from asymmetric boundary data, a non-midplane observer, broken radial reflection symmetry, or nonlinear couplings.

The B/C dark-bubble route remains `[X]` in Res Nova within its stated scope. Its active-mass LLR obstruction should not be silently promoted into a MICROSCOPE Ti/Pt prediction without the source-to-test mapping above.

## References

[1]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo"
[2]: https://arxiv.org/abs/2209.15487 "MICROSCOPE mission final results"
[3]: https://link.aps.org/doi/10.1103/PhysRevLett.129.121102 "MICROSCOPE final results in Physical Review Letters"
[4]: https://arxiv.org/abs/2507.03748 "Dark bubble cosmology and the equivalence principle"
