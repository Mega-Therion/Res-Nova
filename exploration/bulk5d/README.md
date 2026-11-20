# 5D bulk perturbation solve for the flux-fed dark-bubble wall

## Phase 1: which drag-momentum law does a 5D-covariant drag give? (`PREREG_PHASE1.md` 00975315, `phase1_drag_law.py` → `PHASE1_DRAG_LAW.json`)
Pre-registered before any derivation. Analytic (SymPy), plus one numerical check on the already-fitted background. No new fit.

**Candidate (a): velocity-dependent tension σ(X), X = (ξ·n)², with ξ the bulk static Killing vector.**
- `[D]` X = ȧ² for the expanding wall, so σ₀ + ½ρ_b X is the covariant form of `drag_gcosmo`'s σ₀ + ½ρ_b ȧ².
- `[D]` In the dark-bubble junction condition, at leading order in H/k±, it reproduces the drag background exactly: H² = (8πG₄/3)(σ_ext − σ₀ + ρ_eff)/(1 + x₀a²), with G₄ = 2k₊k₋G₅/(k₋ − k₊) (as in arXiv:1807.01570) and x₀ = (4πG₄/3)ρ_b. So this is where the drag background comes from.
- `[D]` Its tangential wall stress is S_μν = −σ(X)h_μν:
  - w = −1, with zero momentum density in every frame;
  - momentum balance is Q_i = −∂_i δσ.
  - That is not Law C, which has w_d = 0 and Q_i = −K²Ω_dΦ.
- `[D]` A vacuum bulk would force σ̇ = 0, so it needs an energy flux Q₄ = dΔΣ/dτ = 2HΔΣ(−q).
- `[X]` for the surviving branch, under `PREREG_FLUX.md`'s single-channel rule. The fit depends only on κ = (3w_d − 1)x₀, so at w_d = −1 the background is unchanged, with x₀ = |κ|/4 (0.56 Pantheon+, 0.62 DES-Dovekie). But s_NEC = −q changes sign at z = 0.73 (Pantheon+) and z = 0.74 (DES-Dovekie): the wall would have to emit into the bulk before acceleration and absorb after. That fails `PREREG_FLUX.md`'s NEC channel rule.
- The verdict comes from that pre-registered modeling rule, not from the 5D NEC itself. Emission through outgoing null dust and later absorption of ingoing dust each satisfy the NEC on their own, and the σ(X) wall's energy exchange is with the ρ_b medium, which need not be null dust. If the rule were relaxed (not done here; that would be post-hoc):
  - (a) would be a third momentum law the envelope never tested: w = −1, zero momentum, Q_i = −∂_i δσ;
  - the bare drag would drop to x₀ = |κ|/4 ≈ 0.56;
  - `drag_gcosmo`'s "x₀ ≥ |κ| floor" holds only while (a) stays excluded, because its w_d ≥ 0 premise is a sound-speed condition, and a sound speed means nothing for a component with no momentum.

**Candidate (b): absorbed bulk null dust, T_AB = ψ l_A l_B.**
- `[D]` l_A = −∂_A v (advanced Eddington–Finkelstein) is null and geodesic. For any wall embedding (V, R)(τ, y), the projection is exactly e^A_μ l_A = −∂_μ(V|_wall).
- `[D]` So the 4-momentum deposited on the wall is ∝ ∂_μV|_wall. The flux frame u_F is the normal to the wall-restricted V = const slices, which is hypersurface-orthogonal. If the absorbed energy is stored in a component that carries momentum, the brane law is Law A with this computed u_F. With inflow from both sides, u_F is the flux-weighted sum of −∂V and −∂U.
- The envelope's `bulk_rest` convention is the special case δV|_wall = 0 on conformal-Newtonian slices. In general u_F − u_m needs the wall bending δV = δT + δR/f, which comes from the asymmetric junction plus the bulk solution.

**Pre-registered decision: (a) `[X]`, (b) gives Law A.**
- Neither candidate produces Law C. The robust Law C passes in `drag_gcosmo` (`#261`) have no 5D-covariant realization from either one.
- The envelope's Law A numbers therefore apply: the flux-fed wall survives only if the bulk gives π_E ≈ 0 (c_vis² = 0, 0.4% inside the ISW gate). At c_vis² = 0 the envelope gives identical results for both flux frames it tested, `bulk_rest` and `matter_comoving` (Pantheon+ A_φφ 1.0485, ISW max 1.5934; 2σ floor 1.0182 and 1.212). So at zero stress the outcome is insensitive to the flux frame, and u_F matters only once π_E ≠ 0.
- The wall stays `[O]`. Phase 2 has three jobs:
  1. compute π_E from the bulk;
  2. compute u_F from δV, replacing the `bulk_rest` convention;
  3. identify the drag's bulk partner (the ρ_b medium or null dust), which decides whether the single-channel rule applies at all.

**Not claimed.** A3's statement that X has no h-dependence at fixed embedding is an argument, not a SymPy check: varying the bulk metric gives a normal-normal term, which acts as the ram-pressure force in the wall's equation of motion, not as tangential stress. No Phase 2 numerics were run.

## Phase 2 / P0: effective 4D equations on the asymmetric wall (`PREREG_P0.md` 971f68cc, `p0_asymmetric_wall.py` → `P0_ASYMMETRIC_WALL.json`)
Pre-registered before any derivation. Self-contained SymPy at linear order and leading order in H/k±. Cross-checked against BCMU (hep-th/0105091) and the dark-bubble papers, all read from their TeX source.

**Controls (all pass).**
- **C1.** On an exact Friedmann wall in planar AdS-Schwarzschild, the Gauss equation 4G = 3k²h − E + KK − K·K − ½h(K² − K·K) holds identically. E_μν is computed from the bulk Weyl tensor: E^τ_τ = 3μ/a⁴, E^x_x = −μ/a⁴.
- **C2.** The Randall–Sundrum limit gives G₄ = kG₅ and Weyl fluid = mean of E±, matching the Shiromizu–Maeda–Sasaki linear terms.
- **C3.** The dark-bubble limit gives G₄ = 2k₊k₋G₅/(k₋ − k₊), Λ₄ = σ_ext − σ, and dark radiation (G₄/2G₅)(μ₊/k₊ − μ₋/k₋)/a⁴, matching 1807.01570 and the exact junction expansion of Phase 1.
- **C4.** BCMU's κ₄, with the two-Λ force term, equals −8πG₄: the same sign and magnitude.

**Result: 4G_μν = −8πG₄ τ_μν − E_eff,μν + F_eff,μν.**
- E_eff = (k₋E⁺ − k₊E⁻)/(k₋ − k₊).
- F_eff = (k₋F⁺ − k₊F⁻)/(k₋ − k₊), with F = (2κ₅/3)[T_μν + (T_nn − T/4)h_μν] for bulk matter.

**Pre-registered decision: CONFIRMED (in form).**
1. **Drag sign.** The envelope's only wall-localized term is the drag, and it enters with the anti-gravitating sign. That sign is exactly what gives its 3(1 + x₀a²)(Ψ′ + Φ); a positively gravitating drag would give 3(1 − x₀a²).
2. **The envelope's π_E is π_eff = (k₋π⁺ − k₊π⁻)/(k₋ − k₊).**
   - E_eff is traceless.
   - It is Bianchi-sourced with the dark-bubble relative sign: the Weyl fluid gains what the wall gains, ρ̇_W + 4Hρ_W = +Q₄ (SymPy). Randall–Sundrum has the opposite sign. `FLUX_CODAZZI` uses the dark-bubble sign.
3. **The drag perturbation law δΔΣ = −2Ω_d(Ψ′ + Φ), i.e. ΔΣ ∝ local H², is a modeling choice for the w_d = 0 branch `[O]`.**

**Matter sector (output 4, `[O]`).**
- Wall-localized stress has explicit coupling −8πG₄. Its net gravity also depends on the bulk response it induces.
- Ordinary +G₄ matter is therefore carried by bulk terms. Either it is bulk-sourced (string endpoints, through F_eff), or it sits on the wall and its own bulk response overcompensates its −8πG₄ term (arXiv:2310.15032 §4.2; 1807.01570 propagator; 2001.07433 bending).
- That this response perturbs like the envelope's 4D fluids was first taken from the Newtonian 1/p² limit. Phase 2 upgrades it to the covariant 4-momentum result of 2001.07433 (see the Phase 2 open-items list).
- The envelope's "free" Weyl fluid, closed with Hu parameters, is E_eff minus that matter-induced response.

**Size of the neglected pieces.**
- The bulk null dust projects with F^τ_τ = 0 exactly (nullness), leaving a pure pressure.
- Relative to the Weyl pressure growth per Hubble time it is (H/k)(1 + H/k): negligible at this order.

**Consequence for Phase 2 (corrected 2026-11-19, `dk_ratio_identity.py`).** The closure the envelope sees is the ratio π_eff/ρ_eff = (π⁺/k₊ − π⁻/k₋)/(ρ⁺/k₊ − ρ⁻/k₋). With single-sided feeding, or the same closure on both sides, the k's and Δk drop out exactly. In general it equals c̄ + ½δc·A, with A = (k₋ρ⁺ + k₊ρ⁻)/(k₋ρ⁺ − k₊ρ⁻). Amplification needs dark radiation on both sides that nearly cancels AND different closures on the two sides. The earlier "amplified by k/(k₋ − k₊)" was too strong. The bulk solve must supply both sides.

## Phase 2: bulk closure for the Weyl anisotropic stress (`PREREG_PHASE2.md` 0ea2f7a5, `phase2_bulk_closure.py` → `PHASE2_BULK_CLOSURE.json`, `phase2_cvis_threshold.py` → `PHASE2_CVIS_THRESHOLD.json`)

**Method change, recorded before any computation.** The fits live at H/k ≪ 1. For the micron-scale string embedding (arXiv:2311.14589, L = 5×10⁻⁵ m), H₀/k = 3.6×10⁻³¹. No moving-wall PDE resolves that, and none is needed. The low-energy gradient expansion (Kanno–Soda, hep-th/0205188) is controlled there. It fixes everything except a traceless, conserved "generalized dark radiation", whose anisotropic stress is set by the bulk state, not by the wall (Kanno–Soda; Koyama, astro-ph/0303108). The pre-registered numerical controls are replaced by K1–K3, a recorded deviation.

**Pre-registered outcome: third branch. The verdict is conditional on the bulk state `[O]`, with a hard threshold.**

**What the bulk does and doesn't fix (J1).**
- **The flux channel is unspecified.** `FLUX_CODAZZI` fits only μ₊/k₊ − μ₋/k₋. A growing Ω_W needs either ingoing dust from outside or outgoing dust from inside.
- **A thermal side (horizon) can't be the feeding side.**
  - Its Weyl fluid is hydrodynamic. Cutoff fluid/gravity applies (arXiv:1101.2451, 1104.3281), with η/s = 1/4π.
  - The exact local temperature at the wall gives c_vis²_eff ~ ½√(H/k), about 3×10⁻¹⁶ for the micron example (order of magnitude, from the Navier–Stokes → Hu mapping). So a thermal side contributes essentially no anisotropic stress.
  - But an interior black hole adds negative dark radiation and can't emit classically, and the exterior has no horizon.
- **The feeding side is horizonless.**
  - Planar radial null dust sits at fixed x, so each column deposits its dark radiation isotropically.
  - Any later π is set by the state of the flux source, which the flux-fed model does not specify.
  - No small parameter (unlike k/T on a thermal side) is known to suppress it on the feeding side.
- **No radion term.** Koyama's low-energy π_E comes from a second brane; the dark bubble has one wall.
- **No free-streaming (c_vis² = 1/3).** It would need weakly coupled, non-hydrodynamic bulk content, which classical 5D Einstein gravity with radial null dust does not supply at wavelengths ≫ 1/k.
- **Asymmetry (corrected).** What matters is π_eff/ρ_eff, not π_eff. It equals the feeding side's own closure for single-sided feeding, and is amplified only by two-sided, nearly cancelling dark radiation with different closures (`DK_RATIO_IDENTITY.json`).

**J2 `[D]`: the flux frame drops out at zero viscosity.** At c_vis² = 0 the flux frame u_F drops out of the envelope's Law A equations exactly: S_W stays 0, D_W comes from the 00 constraint, and F_W never reaches the metric (SymPy on the transcribed equations). It enters only through viscosity. So Phase 1's open u_F question matters only if π_eff ≠ 0.

**The threshold `[D]`, a characterization added after the amendment (not pre-registered).**
- Setup: Law A, every integer ℓ ∈ [2, 30], the pre-registered gates, Hu's GDM closure family.
- The rows below use the `bulk_rest` frame. A `matter_comoving` rerun (`phase2_threshold_frame.py` → `PHASE2_THRESHOLD_FRAME.json`) already fails at c_vis² = 3×10⁻⁴ (ISW 1.6068), putting its crossing near 1.5×10⁻⁴.
- So the Pantheon+ threshold is **c_vis² ≈ 1.5–5.5×10⁻⁴ across the two tested frames**, within the Hu family. A bulk-sourced π need not take Hu's form.

| Fit | ISW max at c_vis² = 0 | Largest passing c_vis² | Verdict at π_eff ≈ 0 |
|---|---:|---|---|
| Pantheon+ best (Δχ² −10.38) | 1.5934 (1.5944 with 50 k-modes) | 3×10⁻⁴ (`bulk_rest`); crossed at 5.5×10⁻⁴ (`bulk_rest`) or about 1.5×10⁻⁴ (`matter_comoving`) | passes by 0.4% |
| DES-Dovekie best (Δχ² −12.74) | 1.6628 (1.6640 with 50) | none | **fails** |
| Pantheon+ 2σ floor (κ = −0.83; a drag 2.7× smaller than best, disfavoured by the background data at 2σ) | 1.2117 | ≥ 0.1 (fails at 1/3) | passes |

**Verdict (pre-registered conditional branch).**
- The flux-fed wall survives only if the bulk state of its flux source keeps the k-weighted effective Weyl viscosity below c_vis² ≈ 1.5–5.5×10⁻⁴ (Hu family, two tested frames). That is a requirement on the source, not an expectation.
- Even then it survives only on the Pantheon+ fit, 0.4% inside the ISW gate. The stronger DES-Dovekie fit fails the gate under every closure.
- The envelope's either-fit rule calls this SURVIVES, but the sample that fits best is the one excluded.
- If the source state carries any larger anisotropic stress, both best fits fail. Only a reduced drag near the 2σ floor survives.
- The c_vis² > 0 rows were computed in the `bulk_rest` frame. By J2 the frame matters only there.

**J3 `[D]`: the drag partner, and why candidate (a) stays excluded on physical grounds.**
- The covariant σ(X) picks out the bulk static frame, so its partner is a medium at rest there.
- Absorbing that medium always gives Q > 0, and reflecting it always gives Q < 0. σ(X) needs Q₄ = ρ_b ȧä, which flips sign at z ≈ 0.73.
- So (a) stays excluded on physical grounds, not only by `PREREG_FLUX`'s single-channel rule.
- The w_d = 0 branch's partner is the Vaidya null dust by construction, and its drag still has no 5D action `[O]`.

**Controls.**
- **K1** is a consistency identity, not a test: the projected Weyl tensor is isotropic in the black-brane rest frame, so a uniform δμ or a uniform boost gives no anisotropic stress at linear order.
- **K2** agrees with Cardoso et al. 2007: no amplification of modes with wavelength ≫ the AdS length. This is a consistency check, not a reproduction.
- **K3** uses η/s = 1/4π, applied only to the thermal estimate.

**Still `[O]` after Phase 2:**
1. The state of the flux source, which sets the first-order π_eff.
2. ~~The 4D matter sector~~ **resolved at leading order** (`phase2_matter_sector.py` → `PHASE2_MATTER_SECTOR.json`). arXiv:2001.07433 §3.1 works in Lorentzian 4-momentum and includes the wall bending, which turns the 5D tensor structure into the 4D one. The resulting response is h_ab = −(2κ₄²/p²)(T_ab − ½Tη_ab): linearized 4D GR with G₄ for time-dependent sources, algebra verified in SymPy. String endpoints behave as dust (point masses τ/k), and worldvolume EM gravitates as 4D radiation (2310.15032). `[D]` at leading order in p/(ak) and H/k; the endpoints' equations of motion are taken from the paper, not derived from the string action.
3. The drag's perturbation law, and a 5D action for the w_d = 0 drag.
4. ~~Δk = k₋ − k₊~~ **no longer an independent input** (`dk_ratio_identity.py`). For single-sided feeding it drops out of the closure; for two-sided feeding what matters is the split k₋ρ⁺ vs k₊ρ⁻, which is part of the flux-source specification (item 1).

## Phase 3: mechanism search for the drag perturbation law (`PREREG_PHASE3.md` 14c90dc8)
**What this phase is.** A new, pre-registered mechanism search, prompted by a Muse brainstorm whose claims were re-derived here. It does not change Phase 2's conditional verdict, and the flux source's state stays a model input.

**Test L, Law-B pinning sweep `[D]`** (`law_b_relaxation_sweep.py` → `LAW_B_SWEEP.json`).
- **Model.** Drag momentum relaxes at rate Γ = γH, with the dark-bubble sign. γ = 0 is Law A; γ → ∞ is Law C.
- **Controls pass.** γ = 0 reproduces the committed Law A numbers exactly. γ = 1000 reproduces Law C to within 1%.
- **Result: both best fits pass from Γ = 30H.**
  - At Γ ≥ 30H, both best fits pass every gate at c_vis² = 0.1, at 1/3 and with the `mb95_l8` free-streaming closure. DES-Dovekie at c_vis² = 0.1 and γ = 30 is the narrowest, with ISW at 1.57.
  - At Γ ≤ 10H, both fail everywhere (ISW 1.65–1.84 at γ = 10).
  - So γ_crit lies in (10, 30]H for all six (fit, closure) cases.
- **What it means.** The free-streaming route needs pinning Γ ≳ 30H. The Law A route needs c_vis² ≲ 1.5–5.5×10⁻⁴ and keeps only Pantheon+. At c_vis² = 0 pinning is irrelevant (the laws coincide).

**Test S, covariant drag-action scan** (`phase3_drag_action_scan.py` → `PHASE3_DRAG_ACTION_SCAN.json`).
- **(i) Tangential Killing coupling, L(Y, φ) = Λ + ½M(Y − F(φ))².**
  - **Passes four criteria.** It gives:
    - w_d = X/(4f + 3X) ≈ (H/k)²/4: dust;
    - ΔΣ = ½ρ_b ȧ² for M ≈ ρ_b/4f;
    - Q₄ = 2HΔΣ(3/2 − q) > 0 at all z;
    - dust locked to the bulk static frame, i.e. Law C (`[D]`).
  - **Fails criterion 3.** The O(k²a²) term cancels only if F equals f to relative precision (H/k)², about 10⁻⁶¹ for micron AdS.
  - **The covariant version collapses.** Enforcing F = −ξ·ξ covariantly gives a 5D metric variation of Y + ξ·ξ = (ξ·n)² that is purely normal-normal (numerical check to 5.5×10⁻¹⁰). The tangential dust disappears and the candidate reduces to (a), the w = −1 tension.
  - **Verdict:** `[X]` as a natural mechanism. Ghost and gradient stability not tested.
- **(iii) Frictional bulk medium, Q = Cρ_med v³.**
  - **Sign.** Q is positive-definite, so a single-sign inflow is guaranteed.
  - **Shape.** Closing the energy equation needs ρ_med(r) ∝ r²(3/2 − q(r)). That factor runs 1.00–1.91, and the best power law, r^2.22, misses it by up to 19%. So the profile must encode the fitted expansion history.
  - **Heat channel.** Wall radiation cancels the drag; massive wall dust keeps it.
  - **Backreaction.** It needs Δk/k ≪ 0.2.
  - **Pinning, heuristically.** The same friction acting tangentially would pin at Γ/H ~ (k/H)² ≫ 30, effectively Law C.
  - **Verdict:** a different model needing its own refit `[O]`.
- **(ii) Radial string forest.** Not tested; no concrete action is specified.

**Verdict.** None of the tested candidates is a natural covariant source of the w_d = 0 drag. The requirement is now quantified: any mechanism that keeps DES-Dovekie must pin the drag momentum at Γ ≳ 30H with nonzero Weyl stress.

## Original Phase 2 scope (superseded by `PREREG_PHASE2.md` 0ea2f7a5)
Kept for the record. P0 is done. The moving-wall PDE and the two numerical controls below were replaced by the low-energy expansion and the K1–K3 controls; see the amendment.

- **P0.** Effective 4D scalar equations on an asymmetric wall (hep-th/0105091). The dark bubble does not localize gravity (arXiv:2212.14004), so the Randall–Sundrum-style Weyl-fluid equations in `weyl_causal_envelope.py` must be confirmed or replaced first.
- **Bulk.** Vaidya null dust carries its own perturbations, so a vacuum master-variable reduction does not apply unmodified.
- **Controls before any dark-bubble scalar output is trusted:**
  - Cardoso–Hiramatsu–Koyama–Seahra, arXiv:0705.1685;
  - the dark-bubble tensor uplift, arXiv:2202.00545.
