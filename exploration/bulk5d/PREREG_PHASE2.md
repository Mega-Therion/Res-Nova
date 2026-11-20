# Pre-registration amendment: Phase 2, the bulk closure for π_eff, u_F and the drag partner (2026-11-19, before any Phase 2 computation)

**Why the method changes (recorded before any result).** `PREREG_PHASE1.md` scoped Phase 2 as a 1+1D moving-wall bulk PDE with numerical controls: Cardoso–Hiramatsu–Koyama–Seahra, arXiv:0705.1685, and the tensor uplift, arXiv:2202.00545. That method targets H ~ k.

The flux-fed fits live at H/k ≪ 1. For the string embedding of the dark bubble (Danielsson–Panizo, arXiv:2311.14589: a dark dimension of about 5×10⁻⁵ m), H₀/k ~ 10⁻³⁰. No moving-wall PDE resolves that scale separation, and none is needed. In this regime the bulk response is quasi-static and is captured exactly, order by order, by the low-energy gradient expansion (Kanno–Soda, hep-th/0205188).

That expansion fixes everything except a traceless, conserved "generalized dark radiation" χ_μν. Its anisotropic stress is not determined on the wall; it is set by the bulk state (Kanno–Soda; Koyama, astro-ph/0303108, who also gives the two-brane radion case). Phase 2 is therefore re-scoped as follows. The numerical controls are replaced as stated below. This is a deviation from `PREREG_PHASE1.md` and is recorded as one.

## What is computed
- **J1: π_eff from the bulk state.** Classify the bulk states available on each side of the dark bubble and give the low-energy π± for each:
  - **(i) Thermal: a horizon is present** (for example an interior black hole). This is fluid/gravity. Derive π/(ρ + p) from η/s = 1/4π (Bhattacharyya–Hubeny–Minwalla–Rangamani, arXiv:0712.2456), with the local temperature at the wall computed from μ, k and H.
  - **(ii) No horizon, gapped** (the exterior between the wall and the AdS boundary, normalizable modes fixed as in arXiv:2001.07433). Corrections are second order in gradients.
  - **(iii) A light radion-type mode.** Requires a second wall, as in Koyama 2003. State whether the dark bubble has one.
  - **(iv) Free-streaming (c_vis² = 1/3).** State what bulk content would be needed.

  Then combine into π_eff = (k₋π⁺ − k₊π⁻)/(k₋ − k₊), including the k/(k₋ − k₊) amplification from P0.
- **J2: u_F.** Determine whether the observables depend on the flux frame at the closure J1 selects. Check structurally (SymPy) on the envelope's Law A equations.
- **J3: drag partner.** For the covariant σ(X), X = (ξ·n)², the partner is a medium at rest in the static frame. Derive the sign of its energy exchange with the wall for absorption and for reflection. Compare with the Q₄ ∝ ä that σ(X) needs.

## Controls (replacing the numerical ones)
- **K1, exact.** A uniform δμ and a uniform boost of the planar black brane give a perfect radiation fluid on the wall, so π = 0 at linear order. Built from the exact projected Weyl tensor of P0 / C1.
- **K2, published.** The low-energy scheme must agree with Cardoso et al. 2007: modes with wavelength ≫ the AdS length are not amplified, i.e. 4D behaviour is recovered. This is a consistency check, not a reproduction.
- **K3, published.** η/s = 1/4π for planar AdS₅ black branes (fluid/gravity), used only for the thermal-state estimate.

## Decision rule (fixed now)
- **J1 gives π_eff → 0 at leading order for every bulk state the dark bubble actually admits.** Apply the envelope's c_vis² = 0 results. Phase 1 established Law A; J2 settles whether u_F matters. Use the pre-registered gates (|A_φφ − 1| ≤ 0.08; ISW ratio in [0.4, 1.6] for ℓ ∈ [2, 30], using `VERIFY_WEYL_KNIFE.json` for every integer ℓ). Report each fit separately. The envelope's rule: SURVIVES if either best fit passes.
- **J1 shows a dark-bubble state that gives free-streaming.** Apply Law A at c_vis² = 1/3, which fails.
- **J1 cannot pick a state.** Report the verdict conditional on the state, `[O]`.
- No new fit, no new data, no change to the envelope's gates.
