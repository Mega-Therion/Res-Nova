# Pre-registration: D10 cluster attack, ideas 1–5 (2026-11-19, before any number)
Sample and baryon model: the 12 D10 clusters, as in `02_galaxy_dynamics/clusters/d10_gauge_test.py` (cored gas, r_c = 0.1 r₅₀₀; f_star = 0.015; μ⁻¹ = 0.9895 Mpc). r_v is the x_H = 154 radius (§11).

**#1 Nonperturbative virial BVP.**
- Equations: W′ = 4πGr²ρ_b − μ²r²Φ, Φ′ = g(u_E) with u_E = W/r², W(r_min) = GM_b(r_min) and Φ(r_v) = 0. Solved by shooting on Φ(r_min).
- Two force laws: g = u + √(a₀u) (the D10 §10–11 law) and exact μ_std.
- Report: whether it is well-posed (u_E > 0 throughout, solver converges) and the median R = M₅₀₀/M_dyn(r₅₀₀).
- **Closes** if median R ∈ [0.8, 1.25] with ≥ 9/12 clusters in [0.7, 1.4]. Otherwise **fails**.

**#2 Two-radius shape test.**
- Missing-mass ratio Q = [M_lens − M_MOND](r₂₀₀) / [M_lens − M_MOND](r₅₀₀), using the baryon profile extended to r₂₀₀.
- Compare with an NFW expectation (c₂₀₀ = 4) and with the #1 AeST profile.
- **Caveat stated now:** if the catalogue M₂₀₀/M₅₀₀ comes from NFW fits, Q is partly circular. That is checked and reported.

**#3 Cosmic dust budget.**
- In AeST the μ² sector is the field's dust-like component.
- Physically allowed iff the extra mass #1 adds inside r_v is ≤ (Ω_c/Ω_b)·M_b(r_v) = 5.36 M_b. Report the ratio.

**#4 Potential-depth screen (BK-type).** Report R if MOND is fully screened in clusters (Newtonian baryons only). Expect a worse result; this tests the critic's claim.

**#5 2 eV neutrinos.** Record the closure with cited bounds (KATRIN, cosmological Σm_ν). No computation.
