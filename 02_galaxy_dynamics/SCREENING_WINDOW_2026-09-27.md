# Screening window: μ_std in galaxies, Cassini-clean in the solar system — 2026-09-27

**Question.** `CASSINI_EFE_QUADRUPOLE_2026-09-27.md` showed that galaxies want μ_std
(n = 2), the Cassini EFE quadrupole forbids it, and a sharper μ is not the fix. So the open
item was screening: suppress the MOND boost near stars, leave it alone in galaxies. Does a
screening scale exist that satisfies both, at the **derived a0 = cH0/2π**?

**Answer: yes, over roughly a decade in scale.** This is phenomenology, not a covariant theory.

## Model — `screening_window.py` → `SCREENING_WINDOW.json`

- Keep μ_std (ν₂). Suppress the MOND boost inside a screening radius:
  ν_eff = 1 + (ν − 1)·s(r/r_scr), with s(u) = uᵖ/(1 + uᵖ), p = 2 or 4.
- **r_scr(M) = r_☉ (M/M☉)^{1/4}.** This is the scaling of the extended-Vainshtein ("Galileon
  k-mouflage") relativistic MOND of Babichev, Deffayet & Esposito-Farèse (PRD 84, 061502, 2011).
- **Cassini:** exact QUMOND quadrupole with a position-dependent ν,
  Q₂ = −(3/4π)∫(ν_eff − 1)∇Φ_N·∇(P₂/r³)d³x. **Validated unscreened against Milgrom's formula to
  ratio 1.0000.** PASS means Q₂ lies within 2σ of the 2026 bound (1.6 ± 1.8)×10⁻²⁷ at both
  g_e = 1.9 and 2.4×10⁻¹⁰.
- **SPARC:** the ledger's tier-1 nuisance treatment. Each galaxy's screening radius comes from
  its baryonic mass (M^{1/4} from the Sun's r_☉), applied radially from the centre.

## Result (derived a0)

| r_☉ (pc) | r_scr for a 10¹⁰ M☉ galaxy | Q₂ (1.9 / 2.4) ×10⁻²⁷, p = 2 | Cassini | SPARC Δχ²/s vs unscreened | tier 1 median |
|---|---|---|---|---|---|
| 0.01 | 3 pc | 13.8 / 13.6 | FAIL | 0.0 | 3.360 |
| 0.03 | 9.5 pc | 6.4 / 5.6 | FAIL (p=4: PASS) | 0.0 | 3.360 |
| **0.1** | 32 pc | 0.96 / 0.78 | **PASS** | −0.3 | 3.363 |
| **0.3** | 95 pc | 0.11 / 0.09 | **PASS** | −2.0 | 3.367 |
| **1** | 316 pc | 0.01 / 0.01 | **PASS** | **−8.9** | 3.356 |
| 3 | 950 pc | 0.00 | PASS | +20.0 | 3.222 |
| 10 | 3.2 kpc | 0.00 | PASS | +624.8 | 3.807 |

**Window: r_☉ ≈ 0.1–1 pc (p = 2), 0.03–1 pc (p = 4).** In that range μ_std at the derived a0
passes Cassini and leaves SPARC unchanged, or slightly improved. Above ~3 pc the screening
reaches into galaxy disks and SPARC degrades fast. That upper wall is set by the galaxies.

## Consistency with the other small-scale tests (not computed here, [C])
- **Gaia wide binaries** (separations ~0.01–0.1 pc): recent 2026 analyses report no MOND signal
  (arXiv:2602.24035, 2603.11015). A solar-mass screening radius ≳ 0.1 pc screens them, so the
  window is consistent with a Newtonian wide-binary result.
- **Oort cloud / long-period comets:** arXiv:2403.09555 finds plain AQUAL-MOND in conflict with
  the remote solar system. Its abstract explicitly leaves open "MOND theories… in which
  non-Newtonian effects are screened on small spatial scales". It gives no numerical screening
  length. If screening must cover the region those orbits sample (aphelia up to ~10⁵ AU ≈ 0.5 pc),
  the window would narrow toward **~0.5–1 pc**. That is an inference, not a quoted bound.

## Status and what is not done
- **Phenomenological.** No action was written. The M^{1/4} law is borrowed from BDE 2011, which
  gives one covariant realization. Building screening into AeST (`TARGET_D7` §4.4 Branch B)
  remains `[O]`.
- Galaxy screening is applied radially from the centre using the total baryonic mass. A disk
  treatment could shift the upper wall.
- No canonical length has been identified in the window. r_☉ is a new scale, so this adds a
  parameter unless a derivation supplies it. The Sun's Galactic tidal (Jacobi) radius (~1 pc)
  sits at the window's upper edge. It scales as M^{1/3}, not M^{1/4}, so it is noted, not claimed.

## Sources
- Babichev, Deffayet, Esposito-Farèse, *Improving relativistic MOND with Galileon k-mouflage*, PRD 84, 061502 (2011) — https://arxiv.org/abs/1106.2538
- Cassini 2026 — https://arxiv.org/abs/2602.17884
- *A Quality Framework for Testing Gravity with Wide Binaries: No Evidence for MOND* — https://arxiv.org/abs/2602.24035
- *No Gravitational Anomaly in Wide Binaries from Forward Modeling of 3D Orbits* — https://arxiv.org/abs/2603.11015
- *Testing MOND on small bodies in the remote solar system* — https://arxiv.org/abs/2403.09555
