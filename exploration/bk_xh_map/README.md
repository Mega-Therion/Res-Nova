# Berezhiani–Khoury condensation vs the x_H virial cut: PARTIAL map (2026-11-19)
Pre-registered in `PREREG.md`; calculation in `bk_map.py` → `BK_MAP.json`.

**Result [D].** Both criteria are density thresholds, but they scale differently:
- **x_H ≥ 154:** ρ ≥ 178ρ_crit, the mean virial density. It does not depend on σ.
- **BK condensation:** ρ ≥ ρ_BK ∝ m⁴σ³. So ρ_BK/ρ_xH = (σ/σ_c)³, and the two agree only at one dispersion, σ_c(m).

At the virial density σ_c(m) is 2016 km/s at 0.6 eV, 1020 at 1 eV, 405 at 2 eV and 119 at 5 eV. The value m ≈ 2.0 eV puts σ_c at the galaxy/cluster boundary, about 400 km/s.

**Q1 (galaxies, σ ≲ 250 km/s): the two agree in outcome.** BK condenses at densities far below the virial value: ρ_BK/ρ_xH = 0.002 at 50 km/s and 0.125 at 200 km/s for m = 2 eV. So the x_H cut is the binding condition, and both say MOND is on inside collapsed galaxies.

**Q2 (clusters, σ ≈ 800–1200 km/s): the two disagree.** For m ≈ 2 eV, BK needs 8–27× the virial density, so clusters stay mostly normal-phase, with dark-matter-like behaviour. The x_H screen switches MOND on there.

**Q3 (implication).**
- The tidal-AeST candidate, with a σ-independent screen, keeps MOND's cluster missing-mass problem (MOND underpredicts cluster mass by a factor of about 2).
- BK escapes that problem through its σ³ dependence. That is the physics our screen lacks.
- An extra condition that depends on the depth of the potential (σ² ~ |Φ_N|) would carry over BK's cluster behaviour. It would add a third constant, or replace x_H,low with a two-variable criterion [O].

**Verdict.** PARTIAL: the map holds below σ_c and fails above it. The virial cut x_H,low ≈ 154 is not BK's condensation criterion. The two coincide only for galaxies.
