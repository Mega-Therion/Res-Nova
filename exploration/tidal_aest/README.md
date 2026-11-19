# Tidal screen with an AeST two-field (QUMOND-type) scalar sector (2026-11-19)

Pre-registration: `PREREG.md` (committed before the run). Script: `tidal_aest_bbn.py` → `TIDAL_AEST_BBN.json`.

**Verdict: both pre-registered gates pass [D]. The model as a whole is [O]: the covariant completion is missing.**

- **BBN.** A QUMOND-type scalar sourced by Φ̂ has essentially no share of Newtonian-regime gravity: ν − 1 ≈ a₀²/(2g²) ≤ 1.6×10⁻¹² at Saturn even unscreened. S2 suppresses that further, to ~10⁻³⁰. In the D3 map c₄,eff → 0, so **G_cosmo/G_local = 1 − K_B/2**: 0.975 at K_B = 0.05, 0.95 at K_B = 0.1.
- **Why the AeST routes failed BBN.** The BBN failure of every earlier route traced to the AQUAL-type tracking 𝒥, where the scalar carries Ĝ/λ_s of Newtonian gravity. The two-field form removes that share by construction, with or without the screen.
- **Mercury.** The extra force is negligible (share·g_N underflows).
- **Well-posedness [D].** Both equations are Poisson-type with S applied to known sources (TIDAL_SCREENING §1). The single-scalar AQUAL tidal form is ill-posed and stays [X].
- **Galaxies, Cassini and the Oort cloud: unchanged from the corpus.**
  - SPARC Δχ² ≈ 0, since S = 1 for galaxies (x ≤ 1.9×10¹⁰ ≪ x*).
  - Cassini sits at the 2σ edge by calibration of x*.
  - The Oort peak holds at RY's working C.
  - GW170817 passes, since x is built from Φ̂'s Hessian.

**So the tidal screen is the first route to clear BBN, Cassini, SPARC, Oort and GW170817 together**, at quasistatic level. That makes it the corpus's live candidate.

**What stays open [O].**
1. A covariant action for a QUMOND-type scalar sourced by Φ̂ inside AeST. AeST's 𝒥(𝒴) sector is AQUAL-type; QUMOND needs an auxiliary-field construction.
2. x* (and C) are declared inputs, fixed by Cassini (x*) and the Oort window (C), not derived.
3. The c₄,eff = local-share identification in the D3 map is a modelling step, not derived.

**Next decisive item:** write the covariant QUMOND-in-AeST action (auxiliary field), and check its cosmology (ghost-freedom, c_T, and that G_cosmo is unchanged).

## Covariant step (`covariant_qumond_check.py`, SymPy Euler–Lagrange)
Aether-frame action, built only from spatial gradients q^{μν} = g^{μν} + A^μA^ν:
L = ρφ + (1/8πG)[−2 q(∂φ,∂ψ) + q(∂ψ,∂ψ) + a₀² F(q(∂ψ,∂ψ)/a₀², X(∇∇ψ))].

1. **[D]** Varying φ gives ∇²ψ = −4πGρ, so ψ is the Newtonian potential. Varying ψ gives Poisson for φ with a source built from the known ψ, including the Hessian ("W") terms, which reach fourth order in ψ. The system is **triangular**: ψ comes from ρ, then φ from ψ. That is why it is well-posed even though F depends on ∇∇ψ.
2. **[D, structural]** No time derivatives appear in the aether frame, so φ and ψ are constraints and do not propagate. The indefinite φψ cross term therefore carries no propagating ghost.
3. **[D]** On FRW the spatial gradients vanish, so the sector reduces to a₀²F(0,0)/8πG. With F(0,0) = 0, G_cosmo and Λ are unchanged, and the BBN result above stands.
4. **[D, structural]** The sector is quadratic in φ and ψ, which vanish on the background, so h_ij couples only at second order and **c_T = c**.

**Binding open requirement: how matter feels φ.**
- A ρφ (conformal) coupling gives no MOND lensing, so galaxy and cluster lensing see GR mass only.
- A disformal coupling for photons is excluded by GW170817: GWs and photons would cross the Milky Way's potential with different Shapiro delays (Boran et al. 2018).
- So the MOND potential must enter the **single metric** (both potentials, γ = 1). AeST already does this through its **J^μ∇_μφ mixing**, where J is the aether acceleration, equal to ∇Φ in the static weak field.
- **Next construction:** keep AeST's J·∇φ mixing and replace 𝒥(𝒴) with the auxiliary-ψ QUMOND sector above. Then check γ = 1 / PPN, lensing = dynamics, and that the D3 c₄,eff → 0 identification follows from the field equations instead of being assumed.
