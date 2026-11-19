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
- `[X]` for the surviving branch. The fit depends only on κ = (3w_d − 1)x₀, so at w_d = −1 the background is unchanged, with x₀ = |κ|/4 (0.56 Pantheon+, 0.62 DES-Dovekie). But s_NEC = −q changes sign at z = 0.73 (Pantheon+) and z = 0.74 (DES-Dovekie): the wall would have to emit into the bulk before acceleration and absorb after. That fails `PREREG_FLUX.md`'s NEC channel rule.

**Candidate (b): absorbed bulk null dust, T_AB = ψ l_A l_B.**
- `[D]` l_A = −∂_A v (advanced Eddington–Finkelstein) is null and geodesic. For any wall embedding (V, R)(τ, y), the projection is exactly e^A_μ l_A = −∂_μ(V|_wall).
- `[D]` So the 4-momentum deposited on the wall is ∝ ∂_μV|_wall. The flux frame u_F is the normal to the wall-restricted V = const slices, which is hypersurface-orthogonal. If the absorbed energy is stored in a component that carries momentum, the brane law is Law A with this computed u_F. With inflow from both sides, u_F is the flux-weighted sum of −∂V and −∂U.
- The envelope's `bulk_rest` convention is the special case δV|_wall = 0 on conformal-Newtonian slices. In general u_F − u_m needs the wall bending δV = δT + δR/f, which comes from the asymmetric junction plus the bulk solution.

**Pre-registered decision: (a) `[X]`, (b) gives Law A.**
- Neither candidate produces Law C. The robust Law C passes in `drag_gcosmo` (`#261`) have no 5D-covariant realization from either one.
- The envelope's Law A numbers therefore apply: the flux-fed wall survives only if the bulk gives π_E ≈ 0 (c_vis² = 0, 0.4% inside the ISW gate).
- The wall stays `[O]`. Phase 2 has two jobs:
  1. compute π_E from the bulk;
  2. compute u_F from δV, replacing the `bulk_rest` convention.

**Not claimed.** A3's statement that X has no h-dependence at fixed embedding is an argument, not a SymPy check: varying the bulk metric gives a normal-normal term, which acts as the ram-pressure force in the wall's equation of motion, not as tangential stress. No Phase 2 numerics were run.

## Phase 2 (scoped in `PREREG_PHASE1.md`; not started)
- **P0.** Effective 4D scalar equations on an asymmetric wall (hep-th/0105091). The dark bubble does not localize gravity (arXiv:2212.14004), so the Randall–Sundrum-style Weyl-fluid equations in `weyl_causal_envelope.py` must be confirmed or replaced first.
- **Bulk.** Vaidya null dust carries its own perturbations, so a vacuum master-variable reduction does not apply unmodified.
- **Controls before any dark-bubble scalar output is trusted:**
  - Cardoso–Hiramatsu–Koyama–Seahra, arXiv:0705.1685;
  - the dark-bubble tensor uplift, arXiv:2202.00545.
