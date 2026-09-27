# TARGET D3 — α₁, α₂ ab initio: working note 1 (2026-09-27)

**Status:** IN PROGRESS. It establishes the reduction that makes the calculation tractable and
corrects one convention. The α's are **not** computed yet.

## 1. Result: AeST's linear static sector is Einstein–aether with a longitudinal c₄ `[D]`

In AeST (`TARGET_D7` §1), the scalar φ enters the quadratic action only through
−(2−K_B)𝒴 − ℱ(𝒴,𝒬) and the mixing 2(2−K_B)J^μ∇_μφ. In the Newtonian (tracking) regime
𝒥(𝒴) → λ_s𝒴, so the static quadratic part of the φ sector is

    L_φ = 2(2−K_B) J·∇φ − (2−K_B)(1+λ_s) (∇φ)² .

Only the longitudinal part J_L couples. Integrating φ out exactly (it appears quadratically) gives
∇φ = J_L/(1+λ_s) and

    L_eff = + (2−K_B)/(1+λ_s) · J_L² .

In the Einstein–aether convention L ⊃ −K^{ab}_{mn}∇_a u^m ∇_b u^n, whose c₄ piece is +c₄ J², this
is an **effective c₄ acting on the longitudinal aether acceleration**:

    c₄,eff = (2 − K_B)/(1 + λ_s),   with   c₁ = −c₃ = K_B,  c₂ = 0.

**Validation (exact).** Einstein–aether's Newton-constant renormalization
G_N = G/(1 − c₁₄/2), with c₁₄ = c₁ + c₄,eff, reproduces AeST's known
G_N = (1 + 1/λ_s) Ĝ with G̃ = (1 − K_B/2) Ĝ (`TARGET_D7` §2) **identically**: the sympy difference
is 0. With c₁ = K_B/2 the difference is non-zero. (Script in §4.)

## 2. Correction to `TARGET_D3` §8.3: the c₁ mapping is K_B, not K_B/2 `[D]`

§8.3 mapped the Maxwell term −(K_B/2)F² onto c₁ = −c₃ = K_B/2. In the convention in which the
G_N formula holds, the map that reproduces AeST's own G_N is **c₁ = −c₃ = K_B**, since
−(K_B/2)F² = −K_B[(∇A)² − ∇_aA_b∇^bA^a]. Consequences:
- §8.3's "α₁ = −2K_B" reading would become −4K_B (plus c₄,eff corrections). Either way it remains
  **not a prediction**: the Foster–Jacobson formulas still do not apply (next section).
- The LLR-based heuristic K_B ≲ 5×10⁻⁵ in §8.3 changes by the same factor. It stays a heuristic.

## 3. What the reduction says about α₁, α₂ `[D]` + `[O]`

- c₁₂₃ = c₁ + c₂ + c₃ = 0 still holds, so the FJ α₂ (∝ 1/c₁₂₃) still diverges in the **static**
  reduction. The effective c₄ fills the longitudinal sector's *coupling*, not its *dynamics*.
- The finite answer must come from the terms the static reduction dropped:
  - the 𝒬-sector kinetic term 𝒦₂(𝒬 − 𝒬₀)² ∋ 𝒦₂ φ̇², which gives the longitudinal (spin-0) sector
    a propagation speed;
  - the 𝒬₀ cross terms q^{0i}𝒬₀∂_iφ.
  For slowly moving sources, ∂₀ = −v·∇, so these enter at relative order (k·v)²/k². They matter
  precisely because the leading coefficient c₁₂₃ vanishes. **Prediction of the structure, to be
  verified: α₂ is controlled by 𝒦₂ (and 𝒬₀), not by K_B alone.**
- Plan, in order:
  1. Build a sympy pipeline that reproduces FJ's α₁, α₂ for generic (c₁…c₄) Einstein–aether: linear
     field equations in Fourier space for a point mass moving at v through the aether rest frame;
     read g₀ᵢ in PPN gauge (coefficients of V_i and W_i). This is the validation step.
  2. Swap in AeST: c₁ = −c₃ = K_B, the longitudinal-only c₄,eff, and restore φ's time
     derivatives (𝒦₂) and the 𝒬₀ cross terms.
  3. Read α₁, α₂ as functions of (K_B, λ_s, 𝒦₂, 𝒬₀) and compare with LLR |α₁| ≲ 10⁻⁴ and the solar
     spin |α₂| ≲ 10⁻⁷.

## 4. Reproduce
```
python3 - <<'EOF'
import sympy as sp
KB,lam,k=sp.symbols('K_B lambda_s k',positive=True); JL,phik=sp.symbols('J_L phi_k')
L=2*(2-KB)*JL*(k*phik)-(2-KB)*(1+lam)*(k*phik)**2
Leff=sp.simplify(L.subs(phik,sp.solve(sp.diff(L,phik),phik)[0]))
c4=sp.simplify(Leff/JL**2); print("c4_eff =",c4)              # (2-K_B)/(1+lambda_s)
for c1 in (KB,KB/2):
    print(c1, sp.simplify(1/(1-(c1+c4)/2)-(1+1/lam)/(1-KB/2)))  # 0 for c1=K_B
EOF
```

---

# Working note 2 (same day): pipeline validated; a sound-speed obstruction at SZ's parameters

## 5. Step 1 DONE — the pipeline reproduces Foster–Jacobson exactly `[D]`
`exploration/d3_alpha/ea_ppn_pipeline.py`: the linearized Einstein–aether field equations for a
point mass moving at v through the aether rest frame, in Fourier space (ω = k·v), de Donder
gauge, then transformed to PPN gauge (isotropic h_ij at O(2); no ω²/k⁴ term in h₀₀ at O(4)).
Result for generic (c₁, c₂, c₃, c₄): **α₁ − α₁^FJ = 0 and α₂ − α₂^FJ = 0 symbolically.** The GR row
is 0/0 at c ≡ 0; its limit gives the PPN values. Two bugs were found and fixed on the way (a missing
time-gauge scaling, and a non-simultaneous substitution that turned ω into O(ε²) and dropped
retardation). Both are recorded in the script's history.

## 6. Units audit `[D]` (RY: "don't forget the per second per second with a²")
a0 is m/s², so a0² is m²/s⁴. In AeST, 𝒴 = |∇φ|² carries acceleration² units in the quasistatic
normalization (x = √𝒴/a0 dimensionless). In the covariant, c = 1 normalization φ is dimensionless
and 𝒬, √𝒴 are inverse lengths (SZ quote 𝒬₀ in Mpc⁻¹, 𝒦₂ dimensionless). Checked:
- residual a0²/(2g) → m/s²;
- Q₂ ∝ a0^{3/2}/√(GM) → s⁻²;
- c²/a0 → m;
- 1/(2x²) dimensionless;
- 𝒦₂φ̇² and (∇φ)² both in length⁻².

## 7. New `[D]`+`[O]`: at SZ's CMB parameters the scalar is slow, and the Sun may be supersonic

> **CORRECTION (same day, see §9):** the table below uses the **FLRW** formula (2−K_B)(1+λ_s)/(2𝒦₂). The local **Minkowski** scalar speed, from SZ PRD 106, 104041 (2022) and reproduced by our pipeline, is c_s² = (2−K_B)(1+½K_Bλ_s)/(𝒦₂K_B). That gives **600–747 km/s and a solar Mach of 0.50–0.62**: subsonic, not supersonic. The PPN-validity concern is weakened to "(v/c_s)² ≈ 0.25–0.4, a poorly convergent expansion". The Cherenkov question stands (c_s ≈ 2×10⁻³ c).
The quadratic φ action about the aether rest frame is +2𝒦₂φ̇² − (2−K_B)(1+λ_s)(∇φ)², using
−ℱ ⊃ +2𝒦₂δ𝒬² since 𝒦 = −ℱ(0,𝒬)/2 = … + 𝒦₂δ𝒬². So

    c_s² = (2 − K_B)(1 + λ_s) / (2𝒦₂)      [= (2−K_B + ℱ_𝒴)/𝒦_𝒬𝒬, the corpus formula, CURRENT_STATE §2b]

SZ's Cosh parameters (K_B = 0.5, 𝒦₂ = 7.5×10⁵; `TARGET_D5`) give c_s = 300 √(1+λ_s) km/s. Against
the Sun's velocity relative to the cosmic frame (the aether frame, 369.8 km/s):

| λ_s | c_s (km/s) | Mach of the Sun |
|---|---|---|
| 0 | 299.8 | **1.23** |
| 0.5 | 367.2 | 1.01 |
| 1 | 424.0 | 0.87 |
| 2.2 (D3 upper bound) | 536.3 | 0.69 |

Consequences:
- **The slow-motion PPN expansion is not valid for the scalar sector** when v☉/c_s = O(1). α₁ and α₂
  as Taylor coefficients in v are then not defined perturbatively, and a transonic/supersonic
  treatment of the moving source is needed. In pure Einstein–aether the analogue is the α₂ ∝ 1/c₁₂₃
  divergence (mode speed → 0). AeST's scalar lifts the speed from 0 only to ~10⁻³ c.
- **Gravitational Cherenkov `[O]`.** For Einstein–aether, Elliott–Moore–Stoica (JHEP 0508:066, 2005)
  show that ultra-high-energy cosmic rays require mode speeds ≥ c to ~10⁻¹⁵. Whether and how strongly
  that bound applies to AeST's scalar depends on its effective coupling to matter (indirect, via
  metric/aether mixing). **No AeST paper found addresses it** (search 2026-09-27). This is a question
  about AeST itself, not about this corpus's additions, and it is a candidate falsifier.
- Caveat: SZ's (K_B, 𝒦₂) are one CMB-fitting example, not a unique fit. c_s scales as 𝒦₂^{-1/2}, so
  c_s ≥ c would need 𝒦₂ ≲ 1. How that trades against the CMB fit is `[O]`.

## 8. Revised plan
1. Compute the α's in the subsonic regime (v ≪ c_s) as formal coefficients: the pipeline plus the φ
   field and the 𝒦₂ term. State that they apply only if c_s ≫ v☉.
2. Treat the transonic case explicitly (moving-source Green's function with c_s ~ v).
3. Estimate AeST's gravi-Cherenkov emission rate for cosmic rays and the Sun against EMS-type bounds.


---

# Working note 3 (same day): AeST pipeline, spectrum reproduced, static residual symmetry

## 9. The AeST pipeline and three independent validations `[D]`
`exploration/d3_alpha/aest_ppn_pipeline.py` adds the AeST scalar to the validated EA pipeline
(c₁ = −c₃ = K_B from the Maxwell term). φ = 𝒬₀t + φ̃ and the aether normalization are built
perturbatively to second order, so terms like 𝒬₀·J⁰₍₂₎ are captured.
1. **Foster–Jacobson reproduced** (EA pipeline, generic c's): α₁, α₂ exact.
2. **Static source reproduces SZ's G_N:** h₀₀ ∝ 16πG(1+λ_s)/[λ_s(2−K_B)k² − 2𝒦₂𝒬₀²(1+λ_s)], i.e.
   G_N = (1+1/λ_s)G̃/(1−K_B/2) at 𝒬₀ → 0, with a Yukawa mass ∝ 𝒬₀.
3. **Minkowski spectrum reproduced:** det of the linear system =
   ω²(k²−ω²)⁷ × [massive luminal vector] × [2𝒦₂K_Bω² − (2−K_B)((2+K_Bλ_s)k² + 2𝒦₂𝒬₀²(1+λ_s))].
   This matches SZ PRD 106, 104041, eq. (det U) factor for factor:
   ω² = 0, and ω² = c_s²k² + ℳ² with **c_s² = (2−K_B)(1+½K_Bλ_s)/(𝒦₂K_B)**.

## 10. The ω = 0 factor is a static residual symmetry (tested) `[D]`
The linearized AeST equations are **exactly invariant** under a static longitudinal aether shift
with compensating scalar shift, δu_i → δu_i + ∂_iΛ(x), φ̃ → φ̃ − 𝒬₀Λ(x), for ∂_tΛ = 0. All 10 field
equations are unchanged (`aest_symmetry.py`). A time-dependent Λ breaks it, with changes ∝ ∂_tΛ.
This is SZ's published "nonpropagating mode with linear time dependence" (their field Y, ω = 0),
which they show may have an unbounded Hamiltonian for k < μ ≲ Mpc⁻¹. **It is known, not new.**

## 11. Consequence for α₁, α₂ `[D]`, stated narrowly
- For a source moving at any v ≠ 0, the linear solution excites the static-symmetry direction with
  amplitude ∝ 1/ω: the aether is dragged (δu ∝ U/v), the scalar locks (δ𝒬 = 0), and the metric
  reduces to GR's with G̃. For v = 0 exactly, the static branch (SZ's G_N) holds. **The slow-motion
  limit is non-uniform.**
- Therefore **α₁ and α₂ are not defined by the standard PPN slow-motion expansion in linearized AeST
  about Minkowski + 𝒬₀.** This is a derived non-applicability result for D3's α item. It sharpens
  §8.3, where the FJ formulas diverge at c₁₂₃ = 0, into a statement about AeST itself.
- **What linear Minkowski theory does NOT decide:** whether real systems sit on the held (static)
  branch or the dragged branch. The candidates that decide it are Hubble friction on FLRW (the zero
  mode's growth rate is set on cosmological time), the non-linear 𝒥(𝒴) regime, and how the aether
  frame is established. **This is NOT a claim that AeST loses MOND for moving sources.**
- **§8.3's "φ fills the spin-0 gap" is not borne out at linear order:** the determinant keeps the
  ω = 0 mode *and* adds a separate massive scalar mode. φ supplies a new mode; it does not lift
  the zero mode.

## 12. Next
1. Repeat on FLRW (Hubble friction) to see whether the zero mode picks a branch on cosmological time.
2. Gravi-Cherenkov estimate for the c_s ≈ 2×10⁻³ c massive scalar (EMS-type bound) `[O]`.
3. Until then, D3's α₁/α₂ entry reads: "not defined by standard PPN in AeST (static residual
   symmetry, SZ 2022); the branch selection is open."

---

# Working note 4 (same day): what holds the aether, and what is still held back

## 13. Verified on the dragged branch `[D]`
For a uniformly moving source (any v ≠ 0), `aest_S_check.py`:
- **S_i ≡ ∂_iφ̃ + 𝒬₀(δu_i + h₀ᵢ) = 0 exactly**, so 𝒴 = |S|² = 0 at quadratic order;
- **δ𝒬 = 0 exactly**;
- **the metric is GR (G̃) even at λ_s = 0.**
The dragged branch is independent of the free function 𝒥(𝒴) and of the 𝒬 sector.

**The mechanism, stated precisely `[D]`.** In the static (held) branch, AeST's MOND channel is sourced
through 2(2−K_B)J^μ∇_μφ by the **aether's acceleration** J = u·∇u. A static aether in a gravitational
field is accelerated, J = ∇Ψ. On the dragged branch the aether free-falls (J = 0) and the scalar
locks to it (𝒴 = 0), so nothing sources the MOND channel.

**Prior art `[C]`.** This is the AeST analogue of Peloso & Sorbo, *Moving sources in a ghost condensate*
(PLB 593, 25, 2004; hep-th/0404005). There, a static source's modification of gravity disappears for
moving sources, because the corrections propagate at a tiny speed, and "the standard Newton law is
recovered". AeST's 𝒬 sector is a ghost condensate. What is AeST-specific is the consequence: the
quantity that disappears is the MOND channel itself.

## 14. The zero mode in a weak static potential — exact, frozen-metric trial direction `[D]`
`zero_mode_lift.py`: the zero mode realized as a genuine re-slicing, T = t − εΛ(x), u_μ = −N∂_μT,
φ = 𝒬₀T + ϕ(x), on a static weak-field background, with the full AeST Lagrangian expanded:
- O(ε²), flat background, time-dependent Λ: **L = K_B|∇Λ̇|² + 2𝒦₂𝒬₀²Λ̇²** (exact);
- O(ε²), static, flat background: **zero** (the symmetry, beyond linear structure);
- O(ε²·Ψ), static, in vacuum: **+2𝒦₂𝒬₀²Ψ|∇Λ|²**, with every other term ∝ ∇²Ψ, ∇²Φ or ∇²ϕ.
  Equivalently the gradient energy is +2𝒦₂𝒬₀δ𝒬_bg|∇Λ|², with δ𝒬_bg = −𝒬₀Ψ.

**Caveat — why this is not yet a dispersion relation.** The ansatz holds the metric fixed and moves only
along the symmetry direction. SZ's *constrained* Y-mode Hamiltonian (PRD 106, 104041, eq. Ham_tilde:
(2−K_B)²λ_s(1−k*²/k²)/[16K_B𝒦₂(c_s²k²+ℳ²)]·|P_Y|², with k*² = (1+1/λ_s)μ²) shows that metric
back-reaction changes the zero mode's effective inertia (it is λ_s- and k-dependent, with a sign flip
below k*). The frozen-metric kinetic term above is therefore a trial direction, not the normal mode.
**The branch criterion and its table (`branch_criterion.py`) are HELD** until the constrained dispersion
with the 𝒬 sector off its minimum (`aest_dispersion_offset.py`, running) is reconciled.

## 15. HELD — not claimed
- The held/dragged table for the Sun, wide binaries, dwarfs and galaxies (frozen-metric ω_L; the |Ψ|
  inputs ignore large-scale-structure potentials of ~10⁻⁵; the velocity reference frame — CMB vs local
  bulk flow — is the decisive unknown and flips the galaxy rows).
- The Ψ > 0 gradient instability: the Minkowski derivation only covers Ψ ≤ 0 (positive masses). Voids
  need FLRW, where the lift scales with the full background δ𝒬, including the positive dust offset.
  To be reconciled with SZ's own k < k* unbounded-Hamiltonian result.
- Any statement that dwarfs are Newtonian, that Cassini is solved, or that AeST loses MOND.

## 16. Gravitational Cherenkov — order-of-magnitude bracket `[D]` (estimate)
- The ghost-condensate sector's strong-coupling scale, from the Cosh function (−ℱ ⊃ 2𝒦₂δ𝒬² +
  𝒦₂δ𝒬⁴/6𝒵₀²) at SZ's values (𝒦₂ = 7.5×10⁵, 𝒵₀ = 10⁻³ Mpc⁻¹), is **Λ = (48𝒦₂)^{1/4}(𝒵₀M_Pl)^{1/2}
  ≈ 0.3 eV**.
- **Emission limited to k ≲ Λ:** a 10²⁰ eV cosmic ray loses energy on ~2.5×10²¹ s, which is harmless
  (the age is 4.4×10¹⁷ s).
- **If the slow mode persisted with gravitational coupling up to k ~ E:** the loss time is ~10⁻²⁰ s, the
  EMS-type exclusion.
- The coupling factor used (SZ's G_W) is a mode-normalization factor, not a derived coupling to a
  relativistic stress tensor. So this is an order-of-magnitude bracket, and the verdict depends on the
  UV completion, as for the ghost condensate.

## 17. D3 checklist entry for α₁/α₂ (current)
Not defined by standard slow-motion PPN in linearized AeST: the static residual symmetry (SZ 2022's ω = 0
mode) makes the limit non-uniform. On the branch that linear theory selects for moving sources, the
metric is GR (α₁ = α₂ = 0) and the MOND channel is unsourced. Whether bound systems actually sit on that
branch depends on the constrained lift (in progress), the velocity reference frame and the non-linear
regime `[O]`.

---

# Working note 5 (same day): the constrained zero-mode lift reproduces SZ's k*, and splits the problem by scale

## 18. Constrained dispersion with the 𝒬 sector off its minimum `[D]`
`aest_dispersion_offset.py`: the full constrained linear system (metric, aether, scalar), with background
φ = (𝒬₀ + q̄)t so that ℱ_𝒬 ≠ 0. Factors of the determinant:
- (k ± ω)⁴: luminal;
- (k² − ω² − 4𝒦₂q̄(𝒬₀+q̄)): the background is not an exact solution (a tadpole). This factor reflects the
  graviton sector seeing the uncompensated condensate stress, or the condensate's gravitational
  response. **Not interpreted.**
- the massive vector factor;
- one factor quartic in ω², containing the scalar mode and the former ω = 0 branch.

**The former zero mode is lifted.** To leading order in q̄ (`offset_zero_branch.py`):

    ω_L² = 𝒦₂𝒬₀q̄ (2−K_B) λ_s (k² − k*²) / [(2+K_Bλ_s)k² + (2−K_B)(1+λ_s)μ²],
    μ² = 2𝒦₂𝒬₀²/(2−K_B),   k*² = (1+λ_s)μ²/λ_s .

**This reproduces SZ's k* and their Y-mode sign flip** (PRD 106, 104041: H_Y ∝ λ_s(1 − k*²/k²)|P_Y|²),
which is an independent consistency check on both calculations. The frozen-metric trial direction
(note 4) had no k* and overstated the restoring force. The constrained/frozen ratio at k → ∞ is
(2−K_B)λ_sK_B/[2(2+K_Bλ_s)] ≈ 0.15 at λ_s = 1.

**Physical reading `[D]`.** 𝒦₂𝒬₀q̄ = 4πGρ_φ, where ρ_φ is the energy density the condensate carries off its
minimum (T₀₀ = (1/16πG)·4𝒦₂𝒬₀q̄ at small q̄). So:
- **k > k*:** a restoring force, with ω_L² → 4πGρ_φ·(2−K_B)λ_s/(2+K_Bλ_s);
- **k < k*:** ω_L² < 0 for q̄ > 0. The zero mode grows at the condensate's Jeans rate √(4πGρ_φ)
  (k ≪ k*), i.e. **gravitational clustering of AeST's dust-like condensate**, not a new pathology.
In a potential well on Minkowski, q̄ = −𝒬₀Ψ.

## 19. The small-offset formula is exact as a coefficient — but galactic potentials are not "small" `[D]`
High-precision root tracking of the full quartic (`verify_lift_mp.py`, 80-digit mpmath), SZ Cosh values, λ_s = 1:
- At q̄ = 10⁻¹⁴ the O(q̄) formula matches the continuously-connected root **exactly (ratio 1.0000) at every k**.
- **The real expansion parameter is 𝒦₂|Ψ|** (= 𝒦₂q̄/𝒬₀), not |Ψ|. With SZ's 𝒦₂ = 7.5×10⁵, a Milky-Way-depth
  potential (|Ψ| ≈ 1.7×10⁻⁶) has 𝒦₂|Ψ| ≈ 1.3.
- Tracking the zero branch as the offset grows:
  - **k > k*:** stable while 𝒦₂|Ψ| ≲ 0.5 (s = ω²/q̄ drifts from 4.43×10⁴ to 3.1×10⁴). It **turns unstable for
    𝒦₂|Ψ| ≳ 0.75**, and ω² becomes increasingly negative: −0.027, −0.40, −3.2 Mpc⁻² at 𝒦₂|Ψ| = 2.25, 7.5, 22.5.
  - **k < k*:** unstable at every depth, with ω² ≈ −0.8·𝒦₂𝒬₀q̄ (the Jeans-like branch).
- **At SZ's parameters, realistic potential wells lie in the unstable regime at all scales.** The e-folding times
  are ~45 Myr at Milky-Way depth (ω² ≈ −5.4×10⁻³ Mpc⁻² at k ≫ k*), ~5 Myr at |Ψ| ~ 10⁻⁵ (clusters, large-scale
  structure) and ~29 Myr for the k ≪ k* Jeans branch in the Milky Way.
- **The density reading makes the tension explicit:** 4πGρ_φ = 𝒦₂𝒬₀²|Ψ| ≈ 1.26×10⁻² Mpc⁻², against the
  Milky Way's own 4πGρ = v_c²/r² ≈ 5.4×10⁻³ Mpc⁻² at 10 kpc. The condensate would carry about 2.3× the
  Galaxy's own density there.
- **Caveat — not a proven pathology.** The local background (a constant 𝒬 offset in flat space) is not an exact
  solution (there is a tadpole), so the growth could be an expansion artefact. The same structure is SZ's own
  flagged k < k* unbounded Hamiltonian, and it traces to 1/μ ≈ 10 kpc sitting at galactic scale, which
  `TARGET_D5` already flags as a CMB-vs-galaxy tension. Settling it needs an exact static (or FLRW) background.

## 20. What survives, what does not
**Survives `[D]`:**
- A uniformly moving source leaves the MOND channel unsourced in linearized AeST (aether free fall, J = 0;
  S = 0; δ𝒬 = 0; GR metric, α₁ = α₂ = 0).
- For **small, fast systems** this holds regardless of the zero mode's stability, because its frequency |ω_L| is
  negligible against the source frequency kv. For the Sun's external-field region, |ω_L|/k ≈ 1 m/s, so **the
  static (MOND-sourced) branch would require the local aether to co-move with the Sun to within ~1 m/s.** Wide
  binaries are similar.

**Does not survive:**
- note 4's frozen-metric table, and note 5's small-offset table for galaxies and dwarfs. At SZ's 𝒦₂ those
  systems are outside the small-offset regime.

**A μ-independent bound, valid only where 𝒦₂|Ψ| ≪ 1** (i.e. for parameter choices with much smaller 𝒦₂). Writing
y = k²/μ², R² = (2−K_B)²λ_s|Ψ|(y − a)/[2v²(By + c)y] with a = (1+λ_s)/λ_s, B = 2 + K_Bλ_s, c = (2−K_B)(1+λ_s).
Its maximum over k does not involve μ: **R_max = (0.091, 0.209, 0.304)·√|Ψ|c/v for λ_s = (0.3, 1, 2.2), at
k ≈ 1.5k***. So the lift can keep a system on the static branch only if v_rel ≲ 0.1–0.3 × its potential-depth
velocity, and only near one scale. For the Milky Way that is ~35–120 km/s: marginal at best.

**Conditional `[O]` (none of these is a result):**
- If the linear structure survives the non-linear MOND regime, the Sun's scalar response and wide binaries are
  Newtonian (no Cassini external-field quadrupole, no wide-binary signal, and no new operators needed).
- Whether spirals and dwarfs keep MOND depends on whether the local aether moves with them. That is set by
  non-linear structure formation and by how the zero-mode instability above saturates, both of which are
  `TARGET_D5`-class open problems.
- The dwarf-spheroidal row is not robust. Large-scale-structure potentials (|Ψ| ~ 10⁻⁵) move it by ×4–5, and
  it lies in the unstable regime anyway.

**Held:** the Ψ > 0 / void question. The unstable sign is now seen inside wells at 𝒦₂|Ψ| ≳ 0.75, which
supersedes the earlier void-only framing. Its physical reality needs an exact background.

---

# Working note 6 (same day): which parameter point, when linear theory applies, and the MOND field holding the aether

## 21. The instability is specific to SZ's CMB-run point `[D]` (`parameter_points.py`)
`TARGET_D5` §2.5 already records a tension inside SZ's paper: the Cosh CMB run has μ⁻¹ = 10 kpc, while SZ
state μ⁻¹ ≳ 1 Mpc is needed for galactic MOND. With 𝒬₀ = 0.1 Mpc⁻¹, K_B = 0.5, λ_s = 1:

| point | 𝒦₂ | 1/k* | c_s | 𝒦₂\|Ψ_MW\| | zero-mode regime |
|---|---|---|---|---|---|
| SZ CMB run (1/μ = 10 kpc) | 7.5×10⁵ | 7.1 kpc | 670 km/s | 1.26 | unstable at all k (note 5) |
| SZ quasistatic requirement (1/μ = 1 Mpc) | 75 | 707 kpc | 67,000 km/s | 1.3×10⁻⁴ | small-offset valid, stable at k > k* |

The note-5 instability therefore belongs to the CMB-run point. At the point SZ's own galaxy analysis
requires, the small-offset regime holds.

## 22. When the linear dragged analysis applies `[D]`
The dragged response of the aether to a source's own field has amplitude δu ≈ Ψ_source/v_rel. Linearity
in the relative motion requires δu ≪ v_rel, i.e. **v_rel² ≫ |Ψ_source|**.
- **Satisfied:** the Sun's own field (ratio 4.5×10⁵), wide binaries (4.4×10⁵), Crater II (3×10³),
  Fornax (164).
- **Violated:** Milky-Way-like and L* spirals (0.09–0.12).
(§22 tests whether the *dragged* branch is linear. §23 below tests whether the *held* branch is stable.
They are different questions.)

**Definition of v_rel.** What matters is whether the source's *density pattern* is time-dependent in the
aether frame, not how fast its stars move.
- An axisymmetric rotating disk is a static source: its v_rel is its bulk velocity relative to the local aether.
- A moving dwarf, the Sun, or a binary is not static: v_rel is its velocity through the ambient aether.
- Non-axisymmetric patterns (bars, spiral arms) move at their pattern speed Ω_p·r. So even inside a held
  galaxy, the non-axisymmetric part of the source is on the dragged branch.

## 23. Laplacian lift terms, exact (frozen-metric trial direction) `[D]` (`lift_laplacian_terms.py`)
Fitting all terms of the static O(ε²·background) Lagrangian (remainder 0):

    E_lift = [ −2𝒦₂𝒬₀²Ψ + K_B ∇²Ψ + (2−K_B) ∇²ϕ ] |∇Λ|²

With AeST's metric potential Ψ = Φ = Φ̂ + ϕ (SZ reduction, `TARGET_D7` §2; γ = 1, `TARGET_D3` §8.1) and
∇²Φ̂ = 4πGρ, this becomes E_lift = [4πG K_B ρ + 2∇²ϕ + 2𝒦₂𝒬₀²|Ψ|]|∇Λ|². In vacuum K_B drops out.
- **Tracking (Newtonian) regime:** ϕ is harmonic outside matter, so only the 𝒬-sector term survives
  (notes 4–5).
- **Deep-MOND regime:** outside matter ∇²ϕ = −∇ln𝒥′·∇ϕ ≠ 0. For a point mass ∇²ϕ = v_f²/r² > 0
  (v_f = (GMa₀)^{1/4}), which is **restoring**. With the frozen kinetic term K_B|∇Λ̇|², the frozen estimate is
  ω_L ≈ √(2/K_B)·v_f/r, so the held branch requires v_rel ≲ 2v_f.

**The constraint correction is not O(1) in deep MOND `[heuristic]`.** The constrained/frozen ratio of note 5,
√[(2−K_B)𝒥′K_B/(2(2+K_B𝒥′))], depends on the **local** scalar stiffness 𝒥′ = λ_sμ(x). That is small in deep
MOND, exactly where the ∇²ϕ lift applies. (SZ's constrained Y-mode inertia ∝ 1/𝒥′, and k*² = (1+𝒥′)μ²/𝒥′
grows as 𝒥′ → 0.) Assuming the same correction carries over to the ∇²ϕ term (λ_s = 1, K_B = 0.5):

| location | 𝒥′ | constrained/frozen ω | held branch requires |
|---|---|---|---|
| inner disk (x ≈ 1) | 0.71 | 0.34 | v_rel ≲ 0.67 v_f |
| outer spiral disk (x ≈ 0.3) | 0.29 | 0.22 | v_rel ≲ 0.45 v_f |
| dSph (x ≈ 0.05) | 0.05 | 0.10 | v_rel ≲ 0.19 v_f |

This moves the dSph and solar-system rows further toward dragged, and moves **spirals from "held" to
undetermined**. Settling it needs the second-order-WKB or numerical constrained calculation.

## 24. Consequences `[D]`/`[heuristic]`/`[O]`

| system | assessment | branch |
|---|---|---|
| Solar system (7000 AU) | v_rel ≈ 240 km/s ≫ its v_f ≈ 0.7 km/s; the MW-field lift needs co-motion to ≲ m/s | **dragged → Newtonian** (robust) |
| wide binaries | same | **dragged → Newtonian** (robust) |
| MW satellite dSphs | v_rel ~ 150 km/s ≫ 0.19·v_f ~ 2–5 km/s; linear-validity satisfied | **dragged → Newtonian** (robust within linear theory) |
| isolated spirals (axisymmetric part) | bulk v_rel to the local aether vs 0.45–0.67 v_f | **undetermined** |
| spiral arms, bars (pattern) | pattern speed ≫ lift | dragged |
| clusters | v_f ~ 1000 km/s vs v_rel ~ 300 km/s; constrained factor unknown | undetermined |

**The dSph test, per object.** Stars-only Newtonian (M/L = 2, LVDB) against observed; the M/L that Newton
would need; MOND+EFE for comparison:

| dwarf | obs/Newton | M/L needed (Newton) | obs/MOND+EFE |
|---|---|---|---|
| Leo I | 1.23 | 3.0 | 1.05 |
| Fornax | 1.35 | 3.6 | 0.95 |
| Sculptor | 1.95 | 7.6 | 1.32 |
| Leo II | 2.35 | 11 | 1.45 |
| Carina | 2.73 | 15 | 1.29 |
| **Crater II** | **3.55** | **25** | **1.16** |
| Draco, Ursa Minor, Sextans, Boötes I, Antlia II | 4.5–6.7 | 41–89 | 2.0–2.8 |

- Leo I and Fornax sit inside the M/L = 1–3 range (σ ∝ √(M/L), a factor of 1.7), so they do not
  discriminate.
- For Draco, UMi, Sextans, Boötes I and Antlia II, MOND+EFE also under-predicts by ~2×, so they do not
  cleanly separate the two either.
- **The clean discriminators are Crater II (Newton needs M/L ≈ 25; MOND+EFE is within 16%), Carina, Leo II
  and Sculptor.** If AeST's satellites are on the dragged branch, these four require stellar M/L of 8–25.
  That is a candidate observational falsifier of AeST's galactic MOND (it concerns AeST, not only this
  corpus's additions), conditional on the non-linear dwarf-in-flow problem.

**Preferred-frame remark (corrected).** Preferred-frame coefficients on the held branch are **not computable
by slow-motion PPN** (the limit is non-uniform, §11). Any FJ-formula number there would repeat the error
`TARGET_D3` §8.3 marks [X], so none is given. What can be said is that on the dragged branch the metric is
GR (α₁ = α₂ = 0), which is where §24 places the solar system.

## 25. Next
1. The constrained coefficient of the ∇²ϕ lift, via second-order WKB or a direct numerical solution. This
   decides the spiral row, which is the one AeST needs held.
2. **Decisive for the dSph row:** a non-linear moving-source solution for a deep-MOND dwarf in an ambient
   aether flow (axisymmetric, time-dependent).
3. The AeST CMB/quasistatic parameter tension (D5 §2.5): at the galaxy-consistent point the CMB fit is
   unverified.

---

# Working note 7 (same day): the constrained threshold computed, the dwarf speed test, and the GW170817 Shapiro constraint

## 26. Constrained zero-mode inertia in a local MOND background, computed `[D]`
Files: `aest_mond_bg_fast.py` (builder), `mond_bg_inertia.py`, and the outputs `MOND_BG_INERTIA_PAR.txt` and
`MOND_BG_INERTIA_PERP.txt`.

**System.** The full constrained linear AeST system (metric in de Donder gauge, aether, scalar) on a local
background with:
- a 𝒬 offset q̄;
- a uniform scalar gradient g, the local MOND field, either along k or across it;
- local stiffnesses 𝒥′ and 2𝒴𝒥″.

It is evaluated at the galaxy-consistent point of §21: K_B = 1/2, 𝒦₂ = 75, 𝒬₀ = 0.1 Mpc⁻¹, λ_s = 1.

**Method.**
- The zero-branch ω² comes from det M(ω) = 0. The determinant is evaluated numerically at 2N+1 points on
  |ω| = 1, its coefficients recovered by inverse DFT, and the roots found by polyroots at 100 digits.
- s = dω²/dq̄ is taken by finite difference, and C = √(s/(𝒦₂𝒬₀)).
- The held branch requires v_rel < C·v_f. The method is first-order degenerate perturbation theory; see the
  script docstring.

**Validation.** In the tracking regime with g → 0, both directions give s = 4.49863 at k = 100 Mpc⁻¹ and
4.49998 at k = 1000 Mpc⁻¹. The O(q̄) formula of note 5 gives 4.49856 and 4.49999.

| deep-MOND background | C, k ∥ ∇ϕ | C, k ⊥ ∇ϕ |
|---|---|---|
| x = 0.3 (𝒥′ = 0.287, 2𝒴𝒥″ = 0.264), outer disk | 0.603 | 0.448 |
| x = 0.05 (𝒥′ = 0.050, 2𝒴𝒥″ = 0.050), dSph | 0.270 | 0.192 |

These values are stable to 3–4 digits between k = 100 and 1000 Mpc⁻¹.

**Closed form, fitting all 8 points to 3–4 digits:**

    C = √[(2−K_B) λ / (2 + K_B λ)],   λ = 𝒥′ (k ⊥ ∇ϕ),   λ = λ_∥ = 𝒥′ + 2𝒴𝒥″ (k ∥ ∇ϕ)

- For k ⊥ ∇ϕ this is exactly §23's heuristic (0.45 / 0.19). Along the field the threshold is stiffer by a
  factor of 1.35–1.41.
- The ∥ case carries a small complex part of relative size ≈ 2μ/k (μ = 1 Mpc⁻¹ here). It is reported, not
  interpreted.

**Scope.**
- This is leading-order local plane waves at one parameter point.
- It assumes the constrained inertia measured with the 𝒬-offset lift carries over to the ∇²ϕ lift.
- **§25 item 1 (second-order WKB or a direct solution) stays open, and the spiral row of §24 stays
  undetermined.**
- What changed: the §23/§24 thresholds are now computed at leading order instead of assumed, and they depend
  on the direction of motion relative to the local field.

## 27. Dwarf speed test: null for gradual drag `[E]`
Details are in `02_galaxy_dynamics/AETHER_DRAG_AND_SHAPIRO_2026-09-27.md` §1.

- Sample: 42 LVDB satellites.
- Speeds: 103–642 km/s in the Milky Way frame and 375–1000 km/s in the CMB frame. The Milky Way moves at
  560 km/s relative to the CMB.
- At fixed distance and luminosity, speed does not predict log(σ_obs/σ_N) or log(σ_obs/σ_MOND+EFE):
  |ρ| ≤ 0.11 and p ≥ 0.47 in both frames.

This probes gradual drag only. Every satellite sits 18–1,647× above §26's switch, so linear-theory drag is
invisible to a correlation test. **The §24 level test (Crater II, Carina, Leo II, Sculptor) remains the
discriminator.**

## 28. GW170817's Shapiro delay constrains the covariant completion `[D]`+`[C]`
Details are in `02_galaxy_dynamics/AETHER_DRAG_AND_SHAPIRO_2026-09-27.md` §2.

- On the GW170817 sightline, the Milky Way's μ_std phantom potential adds 94–254 days of Shapiro delay
  (estimate). Photons and gravitational waves agree to −2.6×10⁻⁷ ≤ γ_GW − γ_EM ≤ 1.2×10⁻⁶.
- **Photon-only lensing is excluded.** In any theory whose photon metric carries phantom potential that the
  GW metric does not, the photon-only share must be ≲10⁻⁶–10⁻⁷ (Boran et al. 2018, the "dark matter
  emulator" exclusion). This removes photon-only disformal lensing, B1's g̃ = g + (2/a0²)∂χ∂χ included,
  as a source of MOND lensing. It does so independently of freeze-out: freeze-out fixes χ̇, while the halo
  delay comes from ∇χ.
- **Withdrawn:** the same-day proposal that a V(χ) = (χ − θ)² freeze-out (Path A) could rescue disformal
  lensing.
- **Conformal routes (k-mouflage, symmetron)** pass GW170817 but bend no extra light (Bekenstein & Sanders
  1994). The lensing RAR (Brouwer et al. 2021) shows the excess, so these routes need a separate lensing
  mechanism.

**Chyren consult, recorded (2026-09-27; her citations verified against the files):**
- B1 dropped the internal E8 term, so χ is a pure k-essence scalar.
- B2's cone test gives Bχ̇² = 8π² ≈ 79 at χ̇ = H₀. The required freeze-out, |χ̇|/H₀ ≲ 5×10⁻⁹, has not been
  built.
- She recommended a conformal k-mouflage / screened scalar-tensor route. By the point above, that route
  must supply lensing separately.

**Trilemma, sharpened.**

| route | MOND lensing | GW170817 speed + Shapiro | cost |
|---|---|---|---|
| conformal scalar | no | yes | lensing must come from elsewhere |
| photon-only disformal | yes | **no** (Shapiro ~10²–10³ days) | excluded |
| metric-level (AeST class) | yes | yes | aether zero mode: drag (§§11–26) |

MOND lensing plus GW170817 require the phantom potential to live in the metric that gravitational waves
ride. The covariant screening (paper outline §6) must be built at metric level.

## 29. AeST + c₂(∇·A)² (zero-mode lift) — pending
`aest_c2_ppn_pipeline.py` is running. It will test whether lifting the zero mode yields α₁ ~ −4c₁₄,eff,
which would be O(1) and excluded by LLR (|α₁| ≲ 10⁻⁴). Recorded here when it finishes.

## 30. Next
1. Second-order WKB or a direct solution for the ∇²ϕ lift. This decides the spiral row.
2. A non-linear dwarf-in-flow solution. This decides the dSph row.
3. The c₂ result (§29).
4. Covariant screening at metric level only (§28).

## 31. The spiral question is a loop, and it fixes a frame requirement `[D]`/`[O]`
Two statements are true at once. The aether and scalar produce the MOND pull that holds a spiral together.
And that pull, through the ∇²ϕ lift of §23, holds the aether still. The loop closes only if the spiral's
bulk velocity relative to its local aether is below the threshold C·v_f of §26. For the Milky Way's
baryonic v_f ≈ 170 km/s that threshold is ≈ 80–100 km/s.

**Frame requirement.** The Milky Way moves at 560 km/s relative to the CMB. Suppose the local aether rests
in the CMB frame. Then linear theory puts the Milky Way 5–7× past the threshold, and the Milky Way's flat
rotation curve contradicts that.

So AeST needs one of two things:
- the aether co-moves with the local bulk flow to ≲ 100 km/s, meaning structure formation drags it on Mpc
  scales; or
- the non-linear regime, which linear theory cannot reach for spirals, holds the aether. §22 shows why it
  cannot be reached: v_rel² is not ≫ |Ψ| there.

Either outcome is a D5-class calculation.

**Observable consequence `[O]`.** Spirals moving fast relative to a cluster's aether should lose part of
the boost, so their outer rotation curves should fall toward Keplerian.
- The existing evidence is contradictory. Whitmore, Forbes & Rubin 1988 (ApJ 333, 542) found falling
  outer rotation curves for inner-cluster spirals. Dale et al. 2001 found no trend of outer shape with
  cluster environment.
- The discriminating design is the one used for the dwarfs: take the outer slope of the stellar (not gas)
  rotation curve, and regress it on |Δv| relative to the cluster mean at fixed cluster-centric radius.
  Stellar kinematics avoid ram-pressure effects on the gas. Fixing the radius separates speed-dependent
  drag from radius-dependent tidal truncation.
