# S(η) with η from an external field χ: tensor speed and the light cone

**Tier:**  `[D]` for the  tensor speed and  the  light  cone in the live D9 frame (§3, §4). `[X]` for putting S into the `TensorSpeed.lean` disformal map. `[O]` for χ as one field across nested systems (§5).
**Date:** 2026-10-15. This replaces the Antigravity draft of the same day; §6 lists what was struck.
**Check:** `02_galaxy_dynamics/duality_screening_cone_check.py`, exit 0, writes `DUALITY_SCREENING_CONE_CHECK.json`. Four sabotaged copies exit 1. The SPARC number in §5 is from `02_galaxy_dynamics/duality_screening_own_field_sparc.py` (`DUALITY_SCREENING_OWN_FIELD_SPARC.json`).

---

## 1. Setup

S(η)  = 1/(1 +  η²) stays as  in  `02_galaxy_dynamics/DUALITY_SCREENING_ACTION.md`,  and it multiplies only the MOND boost, ν_eff = 1 + S(η)(ν − 1). Decision (RY, 2026-10-15): χ is not sourced by local mass. On a patch, ∇χ is that note's external field, so η = |∇χ|/a₀ = |∇Φ_ext|/a₀.

A  covariant η should  use the aether's  spatial  projector:  η² = q^{μν}∂_μχ ∂_νχ / a₀², with q^{μν} = g^{μν} + A^μA^ν. That is never negative. With g^{μν} in its place, a time-dependent χ gives η² = −χ̇²/a₀², and S has a pole at |χ̇| = a₀.

## 2. η at the live a₀ = 1.1607×10⁻¹⁰ m/s²

| System | External field | η | S(η) |
|---|---|---|---|
| Sun: the Galactic field, Hees 2016 bracket | 1.9–2.4×10⁻¹⁰ m/s² | 1.64–2.07 | 0.19–0.27 |
| 148 SPARC galaxies: Chae et al. 2020 e_env | 0.011–0.057 × 1.2×10⁻¹⁰ m/s² | 0.011–0.059, median 0.034 | ≥ 0.9965 |
| Milky Way: M31's Newtonian pull (illustrative) | 3.5×10⁻¹³ m/s² | 3.0×10⁻³ | 0.99999 |

Galaxies  keep their own  small η. Fitting  SPARC  with  the Chae values moves the total χ² from 17241.9 to 17237.0 over 144 matched galaxies (`ENVIRONMENT_SCREENING_PERGALAXY_FORM2.json`, a₀ = cH₀/2π). Shuffled assignments do at least as well in 80% of permutations, so SPARC does not detect the environment at this level.

## 3. Tensor speed: c_T = c on any background `[D]`

S(η)F(Q)  is algebraic in  g^{μν}, because neither  η²  nor  Q contains a derivative of the metric. It can only add terms without derivatives to the TT equation. The speed is set by the two-derivative part, which comes from the Einstein–Hilbert term and the AeST vector term, and the Maxwellian vector term has c₁₃ = 0 (D8, `[D]`). This holds with a spatial ∇χ, which is the case that matters: ∇χ is the external field in every galaxy a wave crosses.

The  coupling itself is  not zero. For  a  wave  along z with ∇χ at angle α to it, the first-order change is δX_χ = −a₀²η² sin²α · h₊, a source term. At second order it gives a mass-like term no larger than about 10 H₀²/c², which changes the speed at 100 Hz by at most 6×10⁻⁴¹.

## 4. The light cone, the `TensorSpeed.lean` check `[D]`

GW170817  compares gravitons with  photons, so the  cone  that  matters is the photon cone of the metric matter couples to. For g̃ = A g + B u u, in the rest frame of u, c_γ² = (A − B)/A. It is luminal exactly when B = 0, whatever A is.

- **Live  frame.** D9 puts  matter on g  (A  =  1, B = 0), so c_γ = c_T = c. χ and S are not in the matter action, so they cannot move either cone. The map in `TensorSpeed.lean` (A = e^{−2φ}, B = −2 sinh 2φ) gives c_γ² = e^{4φ}, which the script reproduces. The D8 readiness row records that map as superseded; it is not the live frame.
- **χ in the matter metric.** A conformal factor A(χ) is sourced by dust, with source −A′(χ)ρ/2, so the decision already excludes it, and it would not split the cone anyway. A disformal term (C/a₀²)∂_μχ ∂_νχ is not sourced by static dust, because T^{μν}∂_μχ = ρu^ν(u·∂χ) = 0. The decision alone does not exclude it; the cone does. Along ∇χ it gives c² = 1/(1 + Cη² cos²θ). GW170817 bounds (v_GW − v_EM)/v_EM to −3×10⁻¹⁵ … +7×10⁻¹⁶. Taking the Chae median as the path's η and ⟨cos²θ⟩ = 1/3, that is C ≤ 3.6×10⁻¹², or |C| ≤ 1.5×10⁻¹¹ for C < 0. χ stays out of the matter metric.
- **S put into the `TensorSpeed.lean` map** `[X]`. Scaling B by S gives c_γ² − 1 = S(e^{4φ} − 1). S > 0 for every η, so the cone is luminal only at φ = 0. At D8's φ = 10⁻⁶ the bound needs η ≥ 2.6×10⁴ along the path, and η ≥ 9×10⁶ at φ = 0.1. The path's η is 10⁻² to 10⁻¹.

## 5. Open: χ as one field `[O]`

The  patch action is  consistent because η  there  is  boundary data for one patch. A single field has one gradient at each point, and at the Sun's position two systems need different values. Cassini needs ∇χ there to be the Galactic field, η = 1.64–2.07. The Milky Way, as a galaxy, needs its environment's field at the same place, η ≈ 3×10⁻³.

- If  ∇χ follows the  Galactic field, then  in  every  galaxy it follows that galaxy's own field. That is the substitution `DUALITY_SCREENING_ACTION.md` excludes. With η = g_N(r)/a₀ on SPARC, the total χ² rises from 18123.5 to 22320.4 at the live a₀, and 108 of 171 galaxies fit worse. Refitting a₀ does not help: over 1.0–1.6×10⁻¹⁰ both cases are best at 1.2×10⁻¹⁰, at 22302.0 against 18110.5 (+4191).
- If ∇χ follows only the environment, then η_⊙ ≈ 3×10⁻³, S ≈ 1, and the Cassini factor is gone.

A  field version therefore  needs a variable  that  tells  a compact body's surroundings from a galactic disk, and a gradient cannot. The tidal tensor can: x = c²‖∇∇Φ‖/a₀² is 1.8×10¹² at the Sun's MOND radius (7,150 AU) and 3.9×10⁷ in the disk at R₀.

Separately,  if χ is  dynamical, varying S(η)F(Q)  gives  it  a source ∝ (∂S/∂X_χ)F(Q)∇χ, so the MOND scalar sources it. Keeping ∇χ equal to the external field then needs a stiff χ. A fixed, non-dynamical χ would break diffeomorphism invariance.

## 6. Struck from the 2026-10-15 draft

- η_⊙ = 4.9×10⁷, S = 4×10⁻¹⁶. That is the Sun's own field at 1 AU, the substitution the DUALITY note excludes. The Sun's η comes from the Galactic field: 1.64–2.07.
- The "cosmological background" η = cH₀/a₀ = 5.5. cH₀ is not the gradient of any χ solution. With the aether projector, a χ(t) background has η = 0.
- The c_T argument that assumed χ = χ(t) and ∂_iφ = 0. It removed the spatial external field that defines η; §3 replaces it.
- Citing `TensorSpeed.lean` for AeST's c_T = c. The D8 row says not to; the result is D8's `[D]` derivation.
- S multiplying the whole scalar kinetic term. The DUALITY action multiplies only the boost.
- "What sources χ" as the open question. Settled: χ is not sourced by local mass.
- `[D]` for "SPARC reproduced at the same precision" with no fit behind it. §2 now cites the fit.
- A verification script cited from an agent's private scratch directory. The checks now live in the repo.
