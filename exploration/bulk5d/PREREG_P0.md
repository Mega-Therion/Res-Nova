# Pre-registration: Phase 2 / P0 — effective 4D equations on the asymmetric dark-bubble wall (2026-11-19, before any derivation)

**Question.** `weyl_causal_envelope.py` (`#261`) evolves Randall–Sundrum-style brane equations: matter gravitating with +G, one Weyl fluid E_μν, and the drag entering the 00 constraint as 3(1 + x₀a²)(Ψ′ + Φ). Do these hold on the dark bubble? Its junction is asymmetric (k₋ > k₊), and gravity is not localized on it (arXiv:2212.14004). If they hold, what exactly is the Weyl fluid made of?

**Method.** A self-contained SymPy derivation from the Gauss equation on each side plus the Israel condition. It works at linear order in the wall stress τ_μν, in the projected Weyl tensors E^±_μν, and in curvature, around a flat extremal wall: leading order in H/k±, the low-energy regime the drag fits live in. It is cross-checked against Battye–Carter–Mennim–Uzan (hep-th/0105091, read from its source). No formula is taken from memory without a check.

**Controls (each must pass, or the derivation is void).**
- **C1, convention check on an exact background.** For a Friedmann wall in planar AdS-Schwarzschild, the Gauss equation with the exact extrinsic curvature must hold identically. The projected Weyl term must be computed from the bulk Weyl tensor in SymPy, not assumed.
- **C2, Randall–Sundrum limit.** With k₊ = k₋ = k and opposite-sign extrinsic curvatures, the result must reduce to the linear Shiromizu–Maeda–Sasaki terms: G₄ = kG₅ and Weyl fluid = E.
- **C3, dark-bubble limit.** With same-sign extrinsic curvatures, the result must reproduce arXiv:1807.01570: G₄ = 2k₊k₋G₅/(k₋ − k₊), Λ₄ ∝ σ_ext − σ, and dark radiation ∝ (μ₊/k₊ − μ₋/k₋).
- **C4, BCMU cross-check.** BCMU's κ₄ formula (their eq. gravconst), with the force term set by two different bulk cosmological constants, must agree with the coefficient derived here, including its sign.

**Outputs (pre-registered).**
1. The coupling of wall-localized stress τ_μν: its sign and magnitude.
2. The effective Weyl fluid: which combination of E⁺ and E⁻ enters, and whether it is traceless and Bianchi-sourced by the bulk flux as in Randall–Sundrum.
3. Whether the envelope's drag factor 3(1 + x₀a²)(Ψ′ + Φ) follows, and under what perturbation law for ΔΣ.
4. What 4D "ordinary matter" has to be for it to gravitate with +G₄, and which parts of the envelope's matter sector are then assumed rather than derived.
5. The size of the bulk null-dust contribution projected onto the wall, relative to the Weyl term.

**Decision rule.**
- **CONFIRMED (in form):** outputs 1–3 match the envelope's structure at this order. Report which combination of E± its π_E stands for.
- **REPLACED:** any of outputs 1–3 differs. The envelope's brane side is then re-derived before Phase 2 bulk runs. Its #261 numbers stay recorded but carry this caveat.
- Output 4 is reported either way. Anything assumed there is tagged `[O]`.
