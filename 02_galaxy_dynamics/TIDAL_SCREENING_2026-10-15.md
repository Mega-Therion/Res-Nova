# Screening on the tidal coordinate: GW speed, well-posedness, SPARC and Cassini

**Tier:**  `[D]` for §1–§2.  `[E]` for §3  (SPARC,  Cassini).  `[X]` for the curvature-built coordinate, the linear-onset form S1, and the AeST single-scalar form. `[O]` for the new constant x*, which RY admitted on 2026-10-15 under a refined rule (§5).

**Date:**  2026-10-15. This follows  `06_foundations/SETA_EXTERNAL_FIELD_SCREENING.md` §5: a  gradient  cannot  tell a compact body's surroundings from a galactic disk, and the tidal tensor can.

**Checks:**  `02_galaxy_dynamics/tidal_screening_consistency.py` (exit 0,  five sabotaged copies  exit  1)  and `02_galaxy_dynamics/tidal_screening_sparc_cassini.py`, pre-registered in `639fa63` before its first run.

---

The  screening term is  −F S(x). Here  F  >  0 is the MOND scalar sector, x = c²‖∇∇Φ‖/a₀² (Frobenius norm) and S decreases from 1. Two forms are carried: S1 = 1/(1 + x/x*) and S2 = 1/(1 + (x/x*)²). Nothing natural fixes x*, because x ≫ 1 everywhere: the Sun's MOND radius has x = 1.8×10¹², a galactic disk at R₀ has 3.9×10⁷, and intergalactic space has about 8.

## 1. Gravitational-wave speed

- **Built  from curvature `[X]`.**  In the aether  frame  the  tidal tensor is E_ij = c²R_0i0j. For a TT wave, E_ij = −ḧ_ij/2, so S(x) carries second time derivatives of h. That is an Ostrogradsky ghost. Its ḧ² term exceeds the Einstein–Hilbert kinetic term by 5×10¹⁸ to 2×10³¹ at 100 Hz, and by 0.05 to 2×10¹¹ at 10 nHz. Linear theory around the background fails for amplitudes above 3×10⁻³⁵ in a galaxy and 7×10⁻⁴² between galaxies.
- **Built from the scalar's own spatial Hessian `[D]`.** Here h enters only through Christoffel symbols, multiplied by ∇Φ_s and Φ̇_s, so first derivatives only. Inside galaxies the tensor kinetic term moves by at most 1.4×10⁻¹⁹. Between galaxies, S2 moves it by at most 1.6×10⁻¹⁹. S1 moves it by 1.9×10⁻¹⁵ to 2.3×10⁻¹⁰, which is past GW170817's ~10⁻¹⁵. The upper end assumes the scalar drifts at φ̇ ~ H₀. S1's onset is linear in ‖H‖, so it is not analytic in the Hessian, and that is what fails. S1 is out `[X]`.

## 2. Well-posedness

- **AeST's  single-scalar (AQUAL) form  `[X]`.** The Legendre–Hadamard  condition  on  the highest derivatives of J·S(x(H)), with J > 0, fails for every decreasing S, at every point. Along a direction ξ with ξ·H·ξ = 0, the second variation is J S′(x)(c²/a₀²)/‖H‖ < 0. The scalar's energy is then unbounded below at short wavelengths, and those modes grow.
- **QUMOND two-field form `[D]`.** Varying Φ still gives ∇²Φ_N = 4πGρ, with no S in it. Φ then obeys a linear Poisson equation whose source is built from Φ_N, so the static problem is well-posed. The form left is: QUMOND, x from Φ_N's Hessian (the Newtonian tidal tensor), and S2. Its covariant completion is open `[O]`; it is not AeST.

## 3. Cassini and SPARC `[E]`

Run as pre-registered in `639fa63`, at the live a₀ = 1.1607×10⁻¹⁰ m/s².

- **Cassini.**  Calibrated on Cassini  alone, the least  screening  that  passes is x* = 2.84×10¹², about 1.6 times the Sun's MOND-radius x. Q₂ falls from 19.0 and 20.0 to 5.20 and 3.45 ×10⁻²⁷ s⁻² at g_e = 1.9 and 2.4 ×10⁻¹⁰, against the 2026 bound's 2σ value of 5.2. The screened integrator reproduces the unscreened Q₂ at cH₀/2π, and a constant S scales it exactly.
- **SPARC.** At that x*, over 171 galaxies, the total χ² stays at 18123.5 (Δχ² = −0.00) for every thickness bracket: in-plane tides only, h_z = 0.3 kpc and 0.1 kpc. The largest change of g anywhere is 1.9×10⁻⁷. The largest galaxy x is 1.9×10¹⁰, two decades below x*. That is a pass under K1, but a weak test: it passes by construction once x* sits between galaxies and the Sun.

## 4. Predictions, stated and not tested

The  wide-binary row is  a single-point proxy,  the  whole  binary's mass at distance s. It is not the prediction.

| System | S |
|---|---|
| Wide binary, 1.5 M☉: 2,000 / 5,000 / 10,000 / 20,000 AU | 0.001 / 0.12 / 0.90 / 0.998 |
| Dwarf spheroidal, ρ ~ 0.1 M☉/pc³ | 1.000 |
| Globular-cluster core, 10³ / 10⁴ M☉/pc³ | 0.98 / 0.36 |

At  the midpoint of  two equal stars  the  tide  is 8 times the proxy's, which moves S = ½ from about 7,000 AU to about 14,000 AU and gives S = 0.90 at 20,000 AU. The test needs the screened two-body QUMOND computation, over the combined stellar and Galactic tidal field, pre-registered before any wide-binary data are looked at. The pre-registered wide-binary orientation test (Amendment A) was not touched.

## 5. Against the screening kill criteria pre-registered on 2026-10-14

| Criterion | Result |
|---|---|
| K1, Cassini, SPARC, dwarfs | Cassini at the 2σ bound by calibration; SPARC Δχ² = −0.00; dwarfs not run |
| K2, refined by RY on 2026-10-15: a constant fixed once by one system is allowed if it predicts the others without retuning, and stays `[O]` until derived | passes on those terms: x* = 2.84×10¹², fixed by Cassini, may not move |
| K3, no new tension in wide binaries, Oort cloud, dwarfs | wide binaries are now the kill test: if the data force x* to move, the route is dead. The two-body computation is not done (§4) |
| K4, c_T = c | passes for Φ_N's Hessian with S2; fails for the curvature coordinate and for S1 |
| K5, derived from an action | the quasistatic QUMOND action, yes; the covariant action is open |

The  tidal coordinate does  what the gradient  could  not.  It separates the Sun from galaxies by two decades, and the only form that survives GW170817 and well-posedness passes Cassini without touching SPARC. The price is a third constant, x*, set by the Solar System, alongside a₀ and the choice of μ. RY accepted that price on 2026-10-15 under the refined K2: x* is fixed once by Cassini, stays `[O]` until derived, and must predict wide binaries without moving. The same two checks apply to an a₀(x) on this coordinate. A redo of the Legendre–Hadamard analysis for a₀(x) (Muse, 2026-10-15) finds the same split: well-posed only in the two-field form, with x taken from Φ_N.
