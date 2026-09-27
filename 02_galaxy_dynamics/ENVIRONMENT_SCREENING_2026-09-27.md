# Parameter-free environmental screening — 2026-09-27

**Question.** `SCREENING_WINDOW_2026-09-27.md` found that μ_std plus a screening *radius* of
0.1–1 pc (for the Sun) reconciles Cassini and SPARC. Can that shield size be derived instead of
chosen?

## 1. A size-based shield needs a new constant (dimensional no-go)

With only G, M, c and a0 available, every length scaling as M^{1/4} equals a constant times
√(r_M · c²/a0), because r_s · c²/a0 = 2 r_M² exactly. For the Sun that is **32 kpc**. The window
needs 0.1–1 pc, so the constant would have to be **3×10⁻⁶ to 3×10⁻⁵**. No such number appears in
the corpus (κ and θ are order 1).

The M^{1/3} alternatives screen whole galaxies:

| scale | Sun | 10¹⁰ M☉ galaxy |
|---|---|---|
| (M/ρ_crit)^{1/3} | 199 pc | 430 kpc |
| (2GM/H0²)^{1/3} | 124 pc | 267 kpc |

The Sun's Galactic Jacobi radius (1.37 pc) is environmental. Applied to galaxies in cosmic tides,
it would screen them too. **Conclusion: any shield defined by a size adds a third scale.**

## 2. A shield defined by the environment's acceleration needs nothing new

The Sun sits in the Milky Way's field, g_ext ≈ 1.9–2.4×10⁻¹⁰ m/s² ≈ 2a0, which is above the
transition. The outskirts of an isolated disk galaxy sit in external fields ≪ a0. So the
pre-declared form is: **a system is only as MONDian as its surroundings.**

    ν_eff = 1 + S(η)·(ν − 1),   S(η) = 1 − μ_std(η),   η = g_ext / a0

The only inputs are a0 (derived) and μ_std (live). No length and no fitted number. This is the
class arXiv:2403.09555 leaves open: "screened … in external gravitational fields comparable in
strength to the critical acceleration."

`environment_screening.py` → `ENVIRONMENT_SCREENING.json`, derived a0:

| system | η | S | result |
|---|---|---|---|
| Sun, g_ext = 1.9e-10 | 1.82 | 0.123 | Q₂ 16.66 → **2.05**×10⁻²⁷, **+0.25σ — PASS** (2026 bound) |
| Sun, g_ext = 2.4e-10 | 2.30 | 0.083 | Q₂ 17.17 → **1.42**×10⁻²⁷, **−0.10σ — PASS** |
| SPARC, uniform η = 0.01 | 0.01 | 0.990 | Δχ²/s **−5.6**, tier-1 median 3.360 → 3.326 |
| SPARC, uniform η = 0.03 | 0.03 | 0.970 | Δχ²/s **−14.5**, median → 3.251 |
| SPARC, uniform η = 0.10 | 0.10 | 0.900 | Δχ²/s **−18.1**, median → 3.149 |

**Cassini passes with no new constant, and SPARC does not degrade; it improves slightly.**

## 3. Caveats (read before citing)
- **Galaxies got a uniform η**, not measured per-galaxy external fields. The next step is to use
  per-galaxy environmental estimates (e.g. Chae et al. 2020, ApJ 904, 51, EFE for SPARC).
- **Part of the SPARC gain is a weaker MOND boost.** Scaling (ν − 1) by 0.9–0.99 acts somewhat like a
  smaller effective a0. It does **not** by itself show that environment matters for galaxies.
- **Phenomenological.** It is not derived from an action, and no covariant AeST realization exists
  `[O]`. It is nonlocal in the same sense the standard EFE already is.
- QUMOND quadrupole; the g_ext bracket 1.9–2.4×10⁻¹⁰ follows Hees 2016.

## 3b. Per-galaxy test with shuffled controls — `environment_screening_pergalaxy.py`

Per-galaxy η from Chae et al. 2020 Table 2 (`e_env`, set by large-scale structure and
independent of the rotation curves; parsed to `CHAE2020_EXTERNAL_FIELDS.json`), rescaled to the
derived a0. There are 144 matched galaxies, with η from 0.013 to 0.066 (median 0.038).

| assignment | total χ² | tier-1 median | Δχ²/s vs unscreened |
|---|---|---|---|
| unscreened | 17241.9 | 3.132 | 0 |
| **true η (per galaxy)** | 17152.7 | 3.075 | **−14.7** |
| uniform η = median | 17141.3 | 3.079 | −16.5 |
| η shuffled among galaxies (20×) | 17133.6 ± 27.8 | — | true − shuffled = +3.1 (sd 4.6) |

**75% of shuffles do at least as well as the true assignment.** SPARC does **not** detect the
environment-dependence. The fields span too narrow a range (S = 0.93–0.99) to give leverage, and the
small gain is the weaker-boost effect. The standing result is limited to this: environmental
screening passes Cassini **at no cost to galaxies**. Galaxies neither confirm nor refute the
environment dependence.

## 4. Predictions (testable, not computed here)
- **Wide binaries near the Sun** (η ≈ 2): the MOND boost is cut to ~10% of the unscreened value.
  That is consistent with the 2026 Gaia null results.
- **Oort cloud / long-period comets:** the MOND effect is reduced to ~12% of AQUAL. That may relieve
  the tension in arXiv:2403.09555; it needs checking.
- **Milky Way satellites and globular clusters** at η ~ 0.1–1: partial screening on top of the
  standard EFE. Dwarf spheroidals in strong external fields (e.g. Crater II) are the sharp test,
  since over-suppression would show up as too-low velocity dispersions.

## Sources
- Vokrouhlický, Nesvorný, Tremaine, *Testing MOND on small bodies in the remote solar system* — https://arxiv.org/abs/2403.09555
- Cassini 2026 — https://arxiv.org/abs/2602.17884
- Hees et al. 2016 — https://arxiv.org/abs/1510.01369
- Chae et al. 2020, *Testing the Strong Equivalence Principle: Detection of the External Field Effect in Rotationally Supported Galaxies*, ApJ 904, 51
