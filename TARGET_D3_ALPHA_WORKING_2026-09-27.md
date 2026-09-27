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
