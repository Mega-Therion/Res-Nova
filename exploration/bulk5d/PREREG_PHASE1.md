# Pre-registration: 5D bulk perturbation solve, Phase 1 — which drag-momentum law does a 5D-covariant drag give? (2026-11-19, before any derivation)

**Why Phase 1 comes first.** `exploration/drag_gcosmo/` (`#261`) left the flux-fed wall alive only narrowly. Under the free-falling drag law (Law A) it passes only at zero Weyl anisotropic stress, 0.4% inside the ISW gate. It passes robustly only under Law C, which was introduced after the fact. A bulk solver cannot say which law applies until the drag has a 5D-covariant definition. Phase 1 settles that analytically; Phase 2 (the 1+1D bulk PDE) is scoped below and not run here.

**Setting.** Flat-sliced AdS(-Vaidya) on each side of the wall, ds² = −f dt² + dr²/f + r² dx², f = k±² r² − μ±/r², with k₋ > k₊ (dark bubble, Banerjee–Danielsson–Dibitetto–Giri–Schillo, arXiv:1807.01570). The wall sits at r = a(τ). Curvature of the closed bubble is neglected, as in `drag_gcosmo`.

## Candidate (a): velocity-dependent tension σ(X), X = (ξ·n)², with ξ = ∂_t the bulk static Killing vector
Derive symbolically (SymPy):
- **A1.** X = ȧ² for the expanding wall, so σ = σ₀ + ½ρ_b X is the covariant form of `drag_gcosmo`'s σ₀ + ½ρ_b ȧ².
- **A2.** Inserted into the dark-bubble junction condition, at leading order in H/k±, it reproduces the drag background H² ∝ [ρ terms]/(1 + x₀a²). Identify x₀.
- **A3.** Its tangential wall stress, S_μν = −σ(X) h_μν, means w = −1 for the drag part, zero momentum density in every frame, and momentum balance −∂_i δσ. Compare with Law C's Q_i = −K²Ω_d Φ.
- **A4.** It needs a bulk energy flux Q₄ = dΔΣ/dτ. Evaluate `PREREG_FLUX.md`'s NEC factor s_NEC = (3/2)(1 + w_d) − q at w_d = −1 on the `FLUX_CODAZZI.json` Pantheon+ best-fit background. The data depend only on κ = (3w_d − 1)x₀, so the fit is unchanged, with x₀ = |κ|/4.

**Rule for (a).** It is `[X]` for the surviving branch if s_NEC changes sign on z ∈ [0, 10] (`PREREG_FLUX.md`: inflow, or pure outflow without a sign flip). If it does not, (a) is a live candidate, reported with its x₀.

## Candidate (b): absorbed bulk null dust, T_AB = ψ l_A l_B
- **B1.** Show symbolically that the 4-momentum deposited on the wall per unit proper volume is −[T_AB n^A e^B_μ] = −[ψ(l·n)] e^A_μ l_A, and that e^A_μ l_A = −∂_μ(V|_wall) exactly, where v = V(τ, x) is the wall's advanced/retarded bulk coordinate.
- **B2.** So the deposited momentum points along u_F ∝ −∂_μ V|_wall, the normal to the wall-restricted V = const slices. If the absorbed energy goes into a component that carries momentum, the brane law is Law A with this computed u_F, not a chosen convention.
- **B3.** State what is still needed to evaluate u_F − u_m: the wall-bending perturbation δV, from the asymmetric junction plus bulk solution. That is Phase 2.

**Rule for (b).** Report Law A with computed u_F if B1–B2 hold. If they fail, report why.

## Pre-registered overall decision
- (a) `[X]` and (b) gives Law A: the envelope's Law A numbers apply (survives only at c_vis² = 0, 0.4% inside the gate). Phase 2's job narrows to two quantities: π_E from the bulk (is it ≈ 0?) and u_F from δV.
- Neither (a) nor (b) yields a w_d ∈ [0, 1/3) drag with a 5D action: record that the surviving branch has no known 5D realization `[O]`. No new drag mechanism will be invented in this phase to rescue it.
- (a) survives: report it as the covariant drag and give its brane-side law.

## Phase 2 scope and controls (fixed now, not run in Phase 1)
- **P0 prerequisite.** Effective 4D scalar equations on an asymmetric wall (Battye–Carter–Mennim–Uzan, hep-th/0105091; the dark bubble does not localize gravity, arXiv:2212.14004). Confirm or replace the Randall–Sundrum-style Weyl-fluid equations used in `weyl_causal_envelope.py`, including the (1 + x₀a²) factor. If the dark-bubble form differs, the envelope's brane side is re-derived before any bulk run.
- **Bulk.** The Vaidya null dust carries its own perturbations, so a vacuum master-variable reduction (Mukohyama) does not apply unmodified. The bulk system is derived, not quoted from memory.
- **Controls the Phase 2 solver must reproduce before any dark-bubble scalar output is trusted.**
  - Cardoso–Hiramatsu–Koyama–Seahra (arXiv:0705.1685): the Randall–Sundrum radiation-era amplification of sub-curvature-length modes.
  - The dark-bubble tensor uplift (Danielsson–Panizo–Tielemans, arXiv:2202.00545).
  - Without these, Phase 2 output stays `[O]`.
