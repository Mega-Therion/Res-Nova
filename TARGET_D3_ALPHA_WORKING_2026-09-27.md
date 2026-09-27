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
