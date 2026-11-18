# Res Nova: Unified Theoretical Physics Synthesis (2026-11-18)

**Author of record for the underlying theory:** R.W. Yett
**Assembled by:** Vesper (Base44 Superagent) from `res-extensa` at `0cb4746`, `Auroboryai` at `8204537`, and `Res-Nova` at `c4a0f42`
**Status:** review document. It states no new physical result of its own. Every claim carries a tier, and the tiers are those of `docs/EPISTEMIC_TIER_LEGEND.md`.

**Why this document exists.** The audited repositories contain mathematics and arithmetic that constrain the theory, and negative results that protect its ledger. They do not contain a covariant action, a derivation of the interpolation law, or a derivation of the acceleration scale. This synthesis says exactly that, in physics language, and then says what the surviving content does constrain.

---

# Part 2. The Unified Res-Nova Theoretical Physics Synthesis

## 2.0 What this synthesis is, and the one thing it refuses to do

This is a physics document. It states fields, an action, the variation, the resulting equations, the symmetries and degrees of freedom, the physical mechanism, and the observables. It is written so that a referee who knows modified gravity but has never seen this corpus can follow it.

It also refuses one thing. **The audited repositories add no field and no term to the covariant action.** `res-extensa` and `Auroboryai` contribute (i) an exact geometric characterization of the constitutive function the action must contain, (ii) exact finite arithmetic constraining the internal geometry, and (iii) negative results that protect the ledger. They do not contribute a covariant completion, a derivation of the interpolation law, or a derivation of the acceleration scale. Any synthesis that presented them as doing so would be manufacturing the unification narrative that `programme/ro0/DIRECTIVE.md` explicitly forbids: "Do not manufacture a unification narrative to fill missing interfaces."

Everything below is therefore either standard imported physics (tagged `[C]`), a derivation from stated premises (`[D]`), exact arithmetic (`[P]` or `[arith]`), or open (`[O]`). There is no `[E]` claim in this section that is not attached to a named dataset.

## 2.1 Field content and the covariant action

**Signature** `(-,+,+,+)`. **Units** `c = 1` except where SI values are quoted.

**Fields.**

| Field | Symbol | Status |
|---|---|---|
| Metric | `g_mu_nu` | dynamical, the matter metric |
| Unit timelike vector | `A^mu`, `g_{mu nu}A^mu A^nu = -1` | dynamical, constraint enforced by multiplier `lambda`; defines a preferred foliation |
| Scalar | `phi` | dynamical, enters only through `Y` |
| Non-metricity scalar | `Q` | the Res-Nova extension sector, entering algebraically |
| Matter | `psi_m` | minimally coupled to `g_mu_nu` |

The vector defines the induced spatial metric on the aether's rest space,

`q_{mu nu} = g_{mu nu} + A_mu A_nu`,

and the scalar's invariant is the spatial gradient squared,

`Y = q^{mu nu} nabla_mu phi nabla_nu phi`.

**The action** is the imported Skordis-Zlosnik AeST scaffold `[C]` with the Res-Nova `Q` sector appended `[D]`:

```
S = (1/16 pi G) * Integral d^4x sqrt(-g) [ R - 2 Lambda
      + (2 - K_B) ( J_std(Y) - Y nabla_mu A^mu )
      - (K_B/2) F_{mu nu} F^{mu nu}
      - 2 K_2 (Q - Q_0)^2
      + lambda (A^mu A_mu + 1) ]
    + S_matter[g]
```

with `F_{mu nu} = 2 nabla_[mu A_nu]` and the constitutive potential

```
F_std(x) = (1/2) [ x sqrt(1 + x^2) - arsinh(x) ],     F_std'(x) = x * mu_std(x)
mu_std(x) = x / sqrt(1 + x^2)
J_std(Y) = 2 lambda_s a_0t^2 F_std( sqrt(Y)/a_0t ),    mu_max = (2 - K_B) lambda_s
```

`[C]` for the AeST core (Skordis and Zlosnik, arXiv:2007.00082). `[D]` for the `Q` sector exactly as the module docstring of `05_lean_formalization/AeSTHamiltonianLegendre.lean` states it. `[O]` for the identification `a_0t = a_0`, because no derivation connects the action's scale to the measured SPARC scale.

**Physical reading of each term.**

- `R - 2Lambda` is Einstein gravity with a cosmological constant.
- `(2-K_B)J_std(Y)` is the scalar's non-linear kinetic term. It is the only place the interpolation function enters, and it enters as a **constitutive potential**, not as a force law: `J_std` is a free energy whose derivative is the response `mu_std`.
- `-(2-K_B) Y nabla_mu A^mu` is the coupling that makes the scalar's gradient and the aether's expansion talk to each other. **This is the term whose coefficient is at issue** (Section 2.2).
- `-(K_B/2) F^2` is the vector's Maxwell-like kinetic term; `K_B` is its stiffness.
- `-2K_2(Q-Q_0)^2` is a mass-like penalty on departure of the non-metricity scalar from a reference value. It is the Res-Nova addition, and it is what makes the `Q` sector's Legendre structure non-trivial.
- `lambda(A^2+1)` is the unit-norm constraint.

**What is conspicuously absent.** There is no second scalar, no `chi` field, no bimetric sector, and no screening field. That absence is not an oversight; it is the content of Section 2.5.

## 2.2 Variation, field equations, and the vector-sector discrepancy

**Metric variation** gives Einstein's equations with the aether, scalar and `Q` stress-energy on the right. `[C]/[D]`

**Scalar variation** gives, in the quasistatic weak-field limit, the AQUAL equation

`nabla . [ mu_std(|nabla Phi|/a_0) nabla Phi ] = 4 pi G rho`,

which is the physical content of `F_std' = x mu_std`. `[C]` for AQUAL; `[D]` for the reduction.

**Vector variation** is where the audit produced its one machine-checked physics result.

Direct variation of the action above yields the `J nabla phi` contribution with coefficient

`b = 2 - K_B`   multiplying   `B^nu := p_mu nabla^nu A^mu - nabla_mu ( A^mu p^nu )`,

where `p_mu = nabla_mu phi`. The published equation (Fu et al. 2024, Eq. 4) prints `2 b B^nu`. Because the unnormalized Euler derivative carries a factor of 2, the full Euler-derivative mismatch is `Delta E_A^mu = 2 b B^mu`.

`[P]` for the algebra: `AeSTVectorNoetherResidual.vector_euler_discrepancy` and `full_euler_shift` prove `(2bB - bB) = bB` and `2(2bB - bB) = 2bB` over `R`, with `0 sorry` and standard axioms.
`[D]` for the physics: the coefficient in the live action is `b B^nu`, not `2 b B^nu`.

**Why this matters, physically.** The factor of 2 is not cosmetic. It controls whether the vector equation is the variation of a diffeomorphism-invariant action. The residual

`R_nu := B^mu F_{nu mu} - A_nu nabla_mu B^mu`

vanishes identically for a consistent action, because it is the Noether/Bianchi identity of the `phi -> phi + const` and diffeomorphism symmetries. The module exhibits a unit-timelike test field on the hyperbola `A^mu = (cosh(eps t), sinh(eps t), 0, 0)`, which satisfies `g_{mu nu}A^mu A^nu = -1`, and evaluates

`R_0 = -eps^2 (2 cosh sinh)`,   `R_1 = eps^2 (cosh^2 + sinh^2) = eps^2 (1 + 2 sinh^2) > 0`.

So `Delta N_1 = 2 b R_1 != 0` for every `b != 0` and `eps != 0`. `[P]` for the evaluation; `[D]` for the conclusion that the equation as printed is not off-shell diffeomorphism invariant.

**The physical consequence, stated plainly.** A theory whose vector sector fails the Noether identity off shell either (i) has a hidden constraint that removes the offending mode, or (ii) is inconsistent, or (iii) is missing a term. The audit establishes that the residual is nonzero for a legitimate on-shell-constraint-satisfying field, so option (ii) or (iii) holds for the printed equation. The corrected coefficient `b B^nu` is necessary; whether it is sufficient is exactly the content of `AeSTDiffeomorphismNoether.lean` (1053 lines), and closing that is the frontier's open obligation, not a result.

## 2.3 Symmetries, conservation laws, and degrees of freedom

**Gauge and global symmetries.**

- Diffeomorphism invariance: required of the total action. Its off-shell Noether identity is the object of Section 2.2; it is not established for the printed vector equation.
- The unit-norm constraint is first class and removes one vector mode.
- `phi -> phi + const` is a global shift symmetry of `J_std(Y)` and gives a conserved current `J^mu = 2 J_std'(Y) q^{mu nu} nabla_nu phi`. `[D]`
- There is **no gauged internal symmetry** in this action. Res-Nova's November audit states the discipline explicitly: "An exact global continuous E8 symmetry of a specified local action would give currents conditionally; gauged E8 gives gauge identities and constraints, not 248 independent observable global charges. The 240 roots are not themselves Noether charges." `[D]`
- The matter sector is minimally coupled to `g_mu_nu`, so free fall and the weak equivalence principle hold by construction, and the photon and graviton propagate on the same cone. `[D]`

**Degrees of freedom.** Counting around Minkowski: 2 tensor (the two helicities of `g_mu_nu`), 2 vector (transverse `A^i`), 1 scalar from the aether's longitudinal mode, and 1 scalar from `phi`, for **6 propagating degrees of freedom**. `[D]`, conditional on the AeST constraint analysis `[C]`.

**Stability and causality.** These are the frontier's own gates, and they are strong:

| Gate | Statement | Tag | Source |
|---|---|---|---|
| Ghost freedom | `0 < K_B < 2` | `[D]` | Res-Nova `CURRENT_STATE_READ_THIS_FIRST.md`, `TARGET_D6` |
| Scalar single-valuedness plus both static ghost conditions | `0 <= lambda_s < (27 + 12 sqrt 6)/5 = 11.2788` | `[D]` | `AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md`; auditor recomputed the constant to 11.2787753827 |
| Tensor speed | `c_T = c`, structurally, because there is no transverse-traceless source under minimal coupling | `[D]` | `TARGET_D8_TENSOR_SPEED.md` |
| PPN | `gamma_PPN = 1` on the dragged branch (stealth sector, exact GR at the Sun) | `[D]`, conditional on branch selection | `TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` |
| Scalar front speed | `c_s < c` iff `K_2 >= (2-K_B)(1 + K_B lambda_s/2)/K_B`, quoted as `K_2 >= 3.75` at the stated points | `[D]` | `TARGET_D6_RELATIVISTIC_STABILITY.md` |
| `mu = 0` shell | The Dirac matrix `C^{AB}` loses rank exactly at `mu = 0`; off that shell its determinant is nonzero | `[P]` | `AeSTHamiltonianLegendre.C_AB_mu_zero_shell_rank_drop` and `det_C_AB_ne_zero` |

That last row deserves emphasis, because it is the precise form of the quarantined k-essence branch. A pure single-scalar k-essence screen has `C^{AB} -> 0` at `mu = 0` with `c_s^2 -> 2`. The audited module does not assume that; it **locates** the degeneracy (`C_AB_mu_zero_shell_rank_drop`), proves the Hessian is nondegenerate away from it (`det_hessian_U_neg`, `det_C_AB_ne_zero`, `general_non_spherical_det_C_AB_ne_zero`), and identifies the secondary constraints (`S^(mu)`, `S^(nu)`). That is a diagnosis of the obstruction, and it is why the obstruction is `[X]` while the module is Keep.

## 2.4 The constitutive sector: what the interpolation function actually is

This is where `res-extensa` makes its one real contribution to the physics, and it is a contribution to *language*, not to dynamics. It says what object `mu_std` is.

### 2.4.1 The constitutive surface is a boost orbit

Res-Nova's `REPRESENTATION_AUDIT_MU_STD_2026-09-16.md` already establishes the complete equivalence class `C` (rows E1 to E12), machine-verified by script, including the unit hyperbola `1/mu^2 - 1/x^2 = 1`, the Gudermannian bridge `mu = sin(gd psi)` with `x = tan(gd psi) = sinh psi`, and rapidity conjugacy `dF/dpsi = x^2`. That audit states its own limit honestly: **"No row adds selection content."** Every identity in the class is selection-free. `[D]`

`res-extensa` supplies the geometric realization of that same class, and the auditor verified it numerically to machine precision:

**Proposition (polar-slope realization).** Let a small circle on the unit sphere sit at height `h = 1 - theta` from the centre with radius `kappa`, so `kappa^2 + h^2 = 1`. Put `x = kappa/h`, the polar slope of the circle (the tangent of its angle from the pole). Then

`mu_std(x) = x/sqrt(1+x^2) = kappa`.

Verified: `theta = 1/sqrt2` gives `kappa = 0.956145157584922`, `x = 3.264483765`, `mu_std(x) = 0.956145157585`, difference `1.1e-16`. `theta = 0.7` gives `kappa = 0.953939201`, `mu_std(x) = 0.953939201`, difference `0.0`. `[arith]`

**Physical reading.** `mu_std` is the **sine of a polar angle**, i.e. the radius of a small circle on the observer's celestial sphere, evaluated at the slope of that circle's tangent. Combined with the existing E6 row, the same number is also `tanh` of a boost rapidity. The bridge between the two readings is the Gudermannian. The physical content is that the interpolation function is a **kinematic** object: it is the relation between `gamma beta` and `beta` in special relativity, with `x` playing `gamma beta` and `mu` playing `beta`. `[D]` for the identity; `[O]` for the claim that Nature's interpolation is this object.

**Why this is worth having even though it selects nothing.** It tells you what class of deformation is natural. A constitutive law that is a boost orbit has a fixed asymptotic structure: `mu -> x` at small `x` (deep MOND) and `1 - mu -> 1/(2x^2)` at large `x` (Newtonian), with `mu'(0) = 1` forced. Any proposed modification that does not sit on this orbit is a different theory, not a variant of this one. That is a real constraint on model building, and it is `[D]`.

### 2.4.2 The band is a correlation dial between two channels

`kappa^2 = theta(2-theta) = 1 - (1-theta)^2` is the probability that at least one of two channels of weight `theta` fires. Give the two channels a correlation `rho`:

`P(L or R) = theta(2-theta) - rho * theta(1-theta)`.

At `rho = 1` the channels are locked and the reading is the floor `theta`; at `rho = 0` they are independent and the reading is the ceiling `kappa^2`; at the most anti-correlated admissible pair `rho = -3/7` the reading closes at 1. `[P]` (`BandCircle` theorems, plus the 400,000-draw simulation recorded in `11_ESSENCE.md` S12, reproduced by `13_band_tests.py` exit 0).

**Physical reading.** The band from floor to ceiling is a **coarse-graining family**: it interpolates between one effective channel and two independent ones. That is the closest thing in the corpus to a mechanism for the band, and it is a statement about averaging a two-component medium, not about a force. `[O]` for any physical identification.

### 2.4.3 The self-dual point is where the descriptions coincide, and it carries a Z_3

At `theta = kappa = 1/sqrt2` the height equals the radius, the polar angle is `45 deg`, the stereographic map `z -> 1/z` sends the ring to its mirror ring with reciprocal radii (`(1+sqrt2)(sqrt2 - 1) = 1`), and the holonomy gate

`P_c(chi) = chi^2/(1+chi^2)`

takes the exact value `1/3`. `[P]`

**Physical reading.** At the self-dual point the "inside" (one hand, height) and "outside" (both hands, radius) descriptions coincide, and the surviving phase is a `Z_3`. This is the only place in the corpus where a dimensionless rational number comes out of a fixed-point condition rather than being inserted by hand. That does not make it a prediction; it makes it the natural place to look for one. `[O]`

### 2.4.4 Two different groups of order 24, and why the distinction is load-bearing

The binary tetrahedral group `2T` (the 24 unit quaternions) has exactly **one** element of order 2. The octahedral group `O`, isomorphic to `S_4` (the 24 Mobius maps permuting the octahedron's vertices on the Riemann sphere), has exactly **nine**. They are not isomorphic, and both contain the 12-element tetrahedral rotation group `T`. `[P]` (`GroupFacts`; `11_verify_all.py` checks 21 and 22)

**Physical reading.** The observer's celestial sphere carries `O`, because Lorentz transformations act on the sky as Mobius maps. The spinor double cover carries `2T`. So a 720-degree spinor return is a statement about the spinor group, and it is **not** a statement about the sky. Any argument in the corpus that uses "the 24" without saying which group it means is ambiguous, and the ambiguity is now resolvable. `[D]`

### 2.4.5 The arithmetic that constrains the internal geometry

Exact finite arithmetic, all by kernel `decide`, with a planted-false control: `[arith]`

- `112 + 128 = 240` roots of `E8` (`D8` roots plus even-sign spinor roots); every root has norm squared 8.
- Inner-product shells about a reference root: `1 + 56 + 126 + 56 + 1 = 240`, with `126 = |Phi(E7)|`.
- `248 = 78 + 8 + 81 + 81` under `E8 -> E6 x SU(3)`.
- `3^4 = 81`, the cardinality of the balanced-ternary register; under the parity involution the origin is the unique fixed point and the remaining 80 states form 40 chiral pairs.
- `240^2 = 57600`, which removes a legacy `58000 - 57600 = 400 = 20^2` rounding residual.

**What this is and is not.** It is correct representation theory and correct counting. It is **not** a derivation of three fermion generations. Res-Nova's November audit is explicit: the `248` decomposition "exhibits a triplet factor, but the adjoint contains the conjugate partner as well. This decomposition alone does not yield a net chiral four-dimensional spectrum." The honest statement of the surviving content is: the internal geometry has a `Z_3` triplet factor and a `3^4 = 81` register, and any generation argument must produce a chiral **index**, `N_gen = (1/2) Integral c_3(V) = +-3`, on a specified bundle. `[D]` for the arithmetic, `[O]` for the index, `[X]` for "E8 arithmetic derives three generations".

## 2.5 Mechanism and regime of validity

### 2.5.1 The mechanism is a saturating constitutive response, not a force

The scalar sector responds to the gradient of the potential through a constitutive function that is linear in `x` at small `x` and saturates at 1 at large `x`. Physically this is a medium with a **non-linear susceptibility** whose saturation scale is `a_0`: below `a_0` the response is strong enough that the effective gravitational field is boosted above the Newtonian value, which is the observed mass discrepancy in galaxies; far above `a_0` the response is the identity and Newton applies. `[D]` for the structure, `[C]` for the phenomenology.

Because the response enters through a potential `J_std` whose derivative is `mu_std`, the theory has a **Legendre-dual description**: the "Hamilgrangian" form, in which the conjugate variable is the polarization of the medium rather than the field gradient. Res-Nova's `AeSTHamiltonianLegendre.lean` (805 lines) constructs the auxiliary potential `U(nu, mu) = U_nu(nu) + U_mu(mu)`, the secondary constraints `S^(mu)`, `S^(nu)`, and the Hessian whose nondegeneracy controls whether the Dirac procedure closes without tertiary constraints. `[P]` for the identities, `[D]` for the reading.

This is a real physical statement about the **phase space** of the theory: the constitutive sector is a constrained Hamiltonian system with a two-dimensional auxiliary space, and it is well posed away from `mu = 0`. It is not a statement about energy transport, and the corpus should stop implying that it is.

### 2.5.2 The central negative result: one shape cannot satisfy both datasets

This is the most important physical finding the audit produces, and it is a **negative** result that the corpus itself established and that the quarantine list depends on.

- SPARC's 175 galaxies select `n ~ 2` in the family `mu_n = x^n/sqrt(1 + x^{2n})`, by `Delta chi^2 / s ~ 700` to `1400` over any alternative. `[E]`
- Cassini's quadrupole `Q_2 = (1.6 +- 1.8)e-27 s^-2` excludes unscreened `mu_std` at `+8.56 sigma` (auditor recomputation from `Q_2 = 1.7e-26`; the repo quotes `+8.7`). `[E]`
- The shapes that pass Cassini are the **sharp-transition** ones, `n >~ 5` or `nu-hat_alpha` with `alpha >~ 4`, and every one of them fits SPARC worse (best tier-1 median/aggregate `3.51/7.57` against `3.36/6.09` for `n = 2`). `[E]/[D]`
- A single external field `chi` cannot supply the Sun's `eta = 1.64` to `2.07` and the Milky Way's `eta ~ 3e-3` simultaneously; giving each galaxy its own `chi` raises the SPARC `chi^2` by about `4,200` (`22302.0` against `18110.5`). `[D]`

**Therefore:** the interpolation function's **shape** cannot be the screening mechanism. Screening must come from a second scale, a second field, or a dynamical branch in which the Solar System sits on exact GR while galaxies do not. The dragged/stealth AeST branch is exactly GR at the Sun, which is the only surviving candidate, and whether it can coexist with the held branch that galaxies need is the open `D7` question. `[D]` for the exclusion, `[O]` for the resolution.

**A second, independent Cassini failure in the same corpus.** Paper E of `Auroboryai` builds a different relativistic completion, a Brans-Dicke-type scalar-tensor theory with a non-minimal coupling `xi R Phi^2`, and fits `xi = 0.127`. The superseded version of that paper claimed this was "well within the Cassini bound `|xi| < 10^-3`". The corrected version states the truth: `0.127` exceeds `10^-3` by about **127x**, so the fitted model is **in tension with Cassini, not within it**, and the paper retracts the consistency claim. `[D]`

This matters because it is a second, structurally different failure. The first failure (Section 2.5.2) is a *shape* failure inside the AeST constitutive sector: no `mu` function satisfies both datasets. This one is a *coupling* failure in a conformal-scalar sector: a light scalar with a non-minimal coupling large enough to do galactic work is excluded at the Sun. Two different actions, two different mechanisms, the same conclusion. **Any relativistic completion in this corpus needs a screening mechanism, and no such mechanism currently exists.** That is the sharpest single statement the audit can make about the physics, and it is a negative one.

This is also the precise physical meaning of "Postulate R is not forced by convexity alone". Convexity plus the AQUAL normalization plus the two asymptotic tails leaves a one-parameter family; galaxies select one member; and galaxies plus Cassini prove that the selection is incomplete as a mechanism. `[D]`

### 2.5.3 Where the approximation breaks

| Breakdown | Where | Consequence |
|---|---|---|
| `mu = 0` shell | exactly at zero gradient | `C^{AB}` loses rank; the Dirac procedure needs the secondary constraints `S^(mu)`, `S^(nu)`; the naive k-essence reduction is invalid there `[P]` |
| Transition region | `x ~ 1`, i.e. `g ~ a_0` | the shape of `mu` matters most and the two datasets disagree most; this is the region no single function satisfies `[D]` |
| Galactic to Solar System | `eta` differing by three orders of magnitude | single-field EFT does not cover both; a second scale is required `[D]` |
| Clusters | `M_dyn/M_lens` median `1.96` (range 1.75 to 4.70, N = 12) | about a factor 2 of missing mass at the declared `a_0`; neither the scale nor the baryon budget closes it `[E]/[O]` |
| New light scale | `Lambda_SC ~ 1.8 meV`, unscreened range `110.0` to `118.1 micrometre` | below that range the fifth force is unscreened; this is the EFT cutoff and a laboratory target `[D]` |

### 2.5.4 The acceleration scale is an input, not a derived quantity

`a_0 = 1.1607e-10 m s^-2` from the SPARC fit, bootstrap 95 percent `[0.972, 1.295]e-10`. `[E]`

The horizon candidate `c H_0 / (2 pi) = 1.0422e-10` lies inside that interval, and `xi = a_0/(c H_0) = 0.17725` (68 percent `[0.162, 0.188]`). `[D]` for the arithmetic.

But `HorizonScale.lean` proves `T_U = T_GH` iff `a = cH`, and separately proves `two_pi_divisor_not_derived`: under the same assumptions, `a != cH/(2pi)`. The thermal-equality argument therefore supports `a = cH` and **not** `a_0 = cH_0/(2pi)`. The `1/(2pi)` is an independent input and must be named as one. `[D]`

This matters for the high-redshift prediction and it is the cleanest available discriminator: if `a_0` tracks the horizon, then `a_0(z) = xi c H(z)` with `xi` fixed, so `a_0` rises by a factor of roughly 2 to 2.6 by `z = 1.5` to `3`. If `a_0` is a constant, it does not. `[D]` for the dichotomy, `[O]` for which holds.

## 2.6 Falsifiable predictions and observational signatures

Each row names the observable, the prediction, the current status, and what would kill it.

| # | Observable | Prediction | Status now | Falsified by |
|---|---|---|---|---|
| 1 | Cassini quadrupole `Q_2` | Bare `mu_std` gives `1.7e-26 s^-2`; a screen must suppress by at least a factor ~10 to reach `1.6e-27` | **Excluded** at `+8.56 sigma` as stated; the screen is `[O]` | Any screen-free variant is already dead. A screen that leaves a residual above `3.4e-27` is dead |
| 2 | SPARC rotation curves, 175 galaxies | `a_0 = 1.1607e-10`, strict unit `M/L`, median `chi^2/N = 15.01` | `[E]` measured | A measured `a_0` outside `[0.972, 1.295]e-10`, or a rotation-curve shape off the boost orbit at high significance |
| 3 | `a_0(z)` at `z > 1.5` | Either `a_0(z) = xi c H(z)` (rising by ~2 to 2.6) or constant | `[O]`, fail-closed preregistration exists, catalog not in tree | A measured high-`z` `a_0` that is constant to within the error kills the horizon reading; one that rises kills the constant reading. The two are mutually exclusive |
| 4 | `Omega_Lambda` | `ln 2 = 0.693147` from `H(1/2,1/2)` | `[O]` identification; Planck 2018 gives `0.6889 +- 0.0056`, i.e. `+0.76 sigma` (auditor arithmetic) | A `sigma(Omega_Lambda) ~ 0.002` measurement (CMB-S4 class) would put the identification at ~2 sigma and kill it if `Omega_Lambda` settles away from `ln 2` |
| 5 | Euclid DR1 weak lensing | Auroboryai's frozen record: `12.34 percent` dipole asymmetry, forecast `123.9 sigma` at DR1 footprint (provisional); 10 caustic vertex targets; dodecahedron residual `6.48 deg` against hexagonal-prism `8.71 deg` | **One gate already FAILED**: dipole-removed null gives `p = 0.023` against a pre-registered `p < 0.01` (`p ~ 0.28` after look-elsewhere). Decisive test waits on full-DR1 shear maps (2027) | A shear map isotropic at the forecast sensitivity kills `P1`. The shape fits are a straight contest: whichever residual DR1 reproduces worse is dead |
| 6 | BBN / CMB spin bounds | Encoded in `Wave3BBNAndSpinCCP2Bounds.lean` | `[P]` module exists; numeric content extracted in Section 1.3 | Noted below |
| 7 | Laboratory | A new light scale at `Lambda_SC ~ 1.8 meV`, unscreened range `110` to `118 micrometre` | `[D]` estimate, "not excluded" is not a proof | A fifth-force search in that range at the stated coupling |

**A warning about row 5, and it is the same warning the corpus makes about itself.** The `12.34 percent` dipole and its `123.9 sigma` forecast are marked provisional in the source, and the pre-registered null test has already failed. A failed pre-registered gate is not repaired by a later favorable dataset; it is a datum. `[D]`

**On row 6.** The audit brief's Euclid description does not match the repository (Section 1.4, near-collision 2), and the brief's `T_1` shear estimator does not exist. The BBN and spin bounds are a real module in Res-Nova and their numbers are extracted in the Auroboryai/Res-Nova tables; they are not restated here to avoid asserting numbers this document has not verified line by line.

## 2.7 What this synthesis does not establish

Stated as a list, because the discipline is the point.

1. **No derivation of `mu`.** `mu_std` remains an axiom on the galaxy domain. All four action routes to it were closed on 2026-10-31. `[A]`
2. **No derivation of `a_0`.** The scale is measured. The `2pi` is not derived, and the thermal argument actively contradicts it. `[E]` plus `[O]`
3. **No screening mechanism.** No surviving candidate meets the 2026-10-16 standard (screen reads only a shadow field computed from matter alone, `S` analytic, every term kept, momentum conservation and universal free fall checked before data, Galactic external field included). `[O]`
4. **No cluster solution.** Median `R = 1.96` unexplained. `[O]`
5. **No three-generation derivation.** The arithmetic is exact; the index is not computed. `[X]` for the derivation claim
6. **No covariant completion of the constitutive law.** The action is imported AeST; a separately postulated `mu_std` cannot simply be attached to an unrelated scalar action, and the November audit's closure order puts "one covariant action" before any of the phenomenology. `[O]`
7. **No quantum or information-theoretic sector.** The GKSL, spectral-action and complexity material is either assumed model or exact algebra about an assumed model. Nothing in it is a physical result. `[O]`
