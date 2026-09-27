# Cassini external-field quadrupole at the derived a0 — 2026-09-27

**Question (RY):** push the RAR shape, which won the tier-0 SPARC median with derived a0 (8.97;
see `GAMMA_FRACTIONAL_RESULTS_2026-09-27.md`), through the solar-system checks.

**Answer: the RAR fails, and so does the live μ_std.** It's the test `TARGET_D7` §4.3 cites
(Desmond, arXiv:2401.04796) but never computed: the **external-field-effect (EFE) quadrupole**.
In MOND the Milky Way's field (g_e ≈ 1.9–2.4×10⁻¹⁰ m/s²) distorts the Sun's field. The result
is an anomalous tidal potential −(Q₂/2) xⁱxʲ(eᵢeⱼ − δᵢⱼ/3). Cassini ranging bounds
**Q₂ = (3 ± 3)×10⁻²⁷ s⁻²** (Hees et al. 2014).

The earlier "μ_std clears the solar-system bound by ~1300×"
(`TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §4.1) is correct for what it tested: the **isolated-Sun
monopole residual** at Mercury. It has no external field in it, so it does not address Q₂.

## Method — `efe_quadrupole_q2.py`

Milgrom's exact QUMOND expression (MNRAS 399, 474, 2009), in the form Hees et al. 2016
(MNRAS 455, 449) use, eq. 12:

    q(η) = 3/2 ∫₀^∞ dv ∫₋₁¹ dξ (ν − ν_e) [η_N(3ξ − 5ξ³) + v²(1 − 3ξ²)],   η = g_e/a0
    Q₂ = −3 q a0^{3/2} / (2 √(GM☉))

**Validation:** Hees 2016 Table 2 is reproduced (g_e = 1.9×10⁻¹⁰):

| function | a0 | −q (here / Hees) | Q₂ (here / Hees) |
|---|---|---|---|
| ν₂ = μ_std | 1.60e-10 | 0.1001 / 0.10 | 26.4 / 26 ×10⁻²⁷ |
| ν̄₀.₅ = McGaugh RAR | 1.48e-10 | 0.1317 / 0.131 | 30.9 / 31 ×10⁻²⁷ |

Identities: μ_std is Hees's ν₂. The McGaugh RAR 1/(1 − e^{−√y}) is exactly ν̄₀.₅. μ_dual/simple is ν₁.

## Result at the derived a0 = cH0/2π = 1.042×10⁻¹⁰ m/s²

| function | Q₂ (g_e = 1.9) | Q₂ (g_e = 2.4) | vs Cassini |
|---|---|---|---|
| RAR (ν̄₀.₅) | 27.7 | 35.4 | **+8.2σ / +10.8σ — excluded** |
| μ_std (ν₂) | 16.7 | 17.2 | **+4.6σ / +4.7σ — excluded** |
| μ_dual (ν₁) — already [X] | 26.7 | 34.3 | +7.9σ / +10.4σ |

(Q₂ in 10⁻²⁷ s⁻².) Lowering a0 does not rescue μ_std: at 0.6×10⁻¹⁰ it is still 7.4×10⁻²⁷.

Monopole residual at Mercury: μ_std ≈ a0²/(2g) = 1.6×10⁻¹⁹ m/s² (as D1 found). RAR ≈ g·e^{−√(g/a0)},
effectively zero. Both pass the monopole test; the quadrupole is what fails.

## Joint Cassini + SPARC — `cassini_sparc_joint.py`

Same derived a0 and the ledger's nuisance treatment. Hees families ν_n and ν̄_α:

| function | Q₂ (1.9 / 2.4) | Cassini | tier 0 median / agg | tier 1 median / agg |
|---|---|---|---|---|
| ν̄₁ | 27.6 / 28.8 | FAIL | **8.37** / 60.4 | 3.05 / 5.66 |
| ν̄₀.₅ (RAR) | 27.7 / 35.4 | FAIL | 8.97 / 52.5 | **2.95 / 5.34** |
| ν₁ (μ_dual) | 26.7 / 34.3 | FAIL | 9.20 / 51.5 | 2.95 / 5.36 |
| ν₂ (μ_std) | 16.7 / 17.2 | FAIL | 11.08 / 93.6 | 3.36 / 6.09 |
| ν₄ | 6.1 / 4.1 | edge | 12.44 / 120.3 | 3.51 / 7.51 |
| ν̄₃ | 9.5 / 3.9 | edge | 11.47 / 61.9 | 3.29 / 9.90 |
| ν̄₄ | 6.9 / 2.9 | edge | 13.01 / 63.0 | 3.24 / 10.87 |
| **ν̄₆** | 5.6 / 2.4 | **PASS** | 13.97 / 65.1 | **3.22** / 12.66 |
| **ν₆** | 2.8 / 1.4 | **PASS** | 12.66 / 126.7 | 3.76 / 8.25 |
| **ν₈** | 1.6 / 0.7 | **PASS** | 12.77 / 129.1 | 3.78 / 8.62 |

**The Desmond tension, reproduced at the derived a0:** every function that fits SPARC best fails
Cassini by ~8σ, and every function that passes Cassini fits worse. The one partial exception is
**ν̄₆**. It passes Cassini, and its tier-1 median (3.22) is *better* than μ_std's (3.36), but its
aggregate is twice as bad (12.66 vs 6.09).

## What this does to the two parameters

Cassini is a genuine **constraint on parameter 2** (the functional choice). It forces a *sharp*
Newton-to-MOND transition (ν_n with n ≳ 5, or ν̄_α with α ≳ 5). The solar system, not galaxies,
decides the shape. That narrows parameter 2 without deriving it.

## Scope and caveats
- The formulation is QUMOND (exact). Per Hees 2016 (citing Milgrom 2009 Tab. I), QUMOND slightly
  *underestimates* the AQUAL/Bekenstein Q₂, so the AQUAL verdicts are, if anything, worse. Hees's
  own conclusion (ν̄_α with α ≥ 2 acceptable) used their fitted a0 (~0.7–0.8×10⁻¹⁰ for that family).
  At the higher derived a0, ν̄₂ fails. **AeST**,
  this repo's covariant completion, was not computed. Its quasistatic sector is AQUAL-like, so the
  EFE is expected to carry over, but that remains unverified here **[O]**.
- g_e bracketed at 1.9–2.4×10⁻¹⁰ m/s², following Hees.
- Cassini bound from Hees et al. 2014. A newer Cassini analysis exists (Phys. Rev. D, "Improved
  constraints on modified Newtonian gravity from Cassini radio tracking data") and was not used here.
- Higher-derivative screening (SZ's open door, `TARGET_D7` §4.4 Branch B) could in principle
  suppress the EFE quadrupole. Unbuilt.

## Follow-up — the three escape routes (same day)

**1. Newer Cassini bound: tighter, not looser.** The 2026 analysis (arXiv:2602.17884,
PRD) gives **Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻²**, a 40% improvement. Against it: μ_std **+8.7σ**,
RAR **+18.8σ**. The route is closed.

**2. AeST does not escape (two-derivative sector).** This repo's AeST reduces to the AQUAL form in
the quasistatic limit (`SkordisZlosnikEmbedding.lean`: `sz_aqual_reduction`; `TARGET_D7` §2.1).
QUMOND *underestimates* AQUAL Q₂ (Milgrom 2009 Tab. I, via Hees 2016), so the AeST verdict is at
least as bad as the QUMOND numbers above. The route is closed within two-derivative AeST. Higher-
derivative screening (`TARGET_D7` §4.4 Branch B) remains the only opening, and it is unbuilt [O].

**3. Pareto scan: the cheapest shape that passes** — `cassini_pareto_scan.py` → `CASSINI_PARETO_SCAN.json`.
There are three Hees families (ν_n, ν̄_α, ν̂_α) on fine grids at the derived a0, ledger nuisance
treatment. PASS means Q₂ ≤ 5.2×10⁻²⁷ (2σ, 2026 bound) at both g_e = 1.9 and 2.4×10⁻¹⁰:

| function | Q₂ (1.9 / 2.4) | σ (2026) | tier 0 median / agg | tier 1 median / agg |
|---|---|---|---|---|
| μ_std = ν₂ (live, FAILS) | 16.7 / 17.2 | +8.7 | 11.08 / 93.6 | 3.36 / 6.09 |
| **ν̂₄ (best passing)** | 4.9 / 2.5 | +1.8 | 12.45 / 121.2 | 3.51 / 7.57 |
| ν₅ | 4.0 / 2.3 | +1.3 | 12.58 / 124.4 | 3.67 / 7.95 |
| ν̂₅ | 3.0 / 1.3 | +0.8 | 12.58 / 125.0 | 3.67 / 8.02 |
| ν₈ | 1.6 / 0.7 | 0.0 | 12.77 / 129.1 | 3.78 / 8.62 |

- The ν̄_α family never reaches the 2σ bound: Q₂ at g_e = 1.9 plateaus near 5.3×10⁻²⁷ (+2.0σ) as
  α grows.
- **The price of passing Cassini at the derived a0 is about +4% on the tier-1 median and +24% on
  the tier-1 aggregate, relative to μ_std** (ν̂₄: 3.51 / 7.57 vs 3.36 / 6.09).
- Passing sits at the sharp end of every family (ν_n with n ≳ 5, ν̂_α with α ≳ 4).

## Sources
- Cassini 2026, *Improved constraints on modified Newtonian gravity from Cassini radio tracking data* — https://arxiv.org/abs/2602.17884
- Hees, Famaey, Angus, Gentile, *Combined Solar System and rotation curve constraints on MOND*, MNRAS 455, 449 (2016) — https://arxiv.org/abs/1510.01369
- Hees et al., *Constraints on MOND theory from radio tracking data of the Cassini spacecraft*, PRD 89, 102002 (2014) — https://arxiv.org/abs/1402.6950
- Desmond et al., *On the tension between the RAR and Solar System quadrupole in modified gravity MOND* — https://arxiv.org/abs/2401.04796
- Milgrom, MNRAS 399, 474 (2009) — exact QUMOND q(η)
