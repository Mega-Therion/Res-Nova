# Pre-registration: wide-binary test of the fish rule (2026-10-04)

Written and committed **before** any large-separation bin is examined.

## Question
RY's fish-in-the-wave rule says a system co-moving with its host field does not feel that field. Only its own internal field enters μ. For a wide binary near the Sun that means no external-field effect (EFE). The binary gets the full MOND boost of its own internal field. Tier of the rule: `[O]`.

## Data `[E]`
- El-Badry, Rix & Heintz 2021, Gaia EDR3 wide binaries (Zenodo 4435257). Both catalogs are used: `all_columns_catalog` (pairs) and `all_columns_catalog_shift` (chance-alignment control).

## Cuts (fixed)
- **Clean, Chae-style:**
  - `R_chance_align` ≤ 0.01;
  - both stars RUWE < 1.2;
  - parallax_over_error > 50 for both;
  - parallaxes agree within 3σ;
  - d < 200 pc;
  - both stars on the main sequence: |M_G − locus(bp_rp)| < 0.8 and 4 < M_G < 12;
  - σ(ṽ) < 0.10, where σ(ṽ) includes PM errors and the unknown-RV perspective term σ = 35 km/s·θ (smaller if a Gaia RV is known).
- **Loose, Banik-style:** same as Clean but `R_chance_align` ≤ 0.1, RUWE < 1.4, and σ(ṽ) < 0.2. Contamination is then fitted, not cut.

## Observable
- ṽ = Δv_sky / √(G M_tot / r_sky).
- Δv_sky is the tangential velocity difference after removing the projection-geometry (perspective) term computed from the common 3D velocity.
- M_tot comes from a main-sequence M_G→mass relation.

## Bins (projected separation s, AU)
- Control: 500–2000 (Newtonian, g_N ≫ a0).
- Test: 2000–5000, 5000–10000, 10000–20000, 20000–30000.

## Per-bin fit
- Mixture: f(ṽ) = (1−c)·P_N(ṽ/α)/α + c·P_cont(ṽ).
- P_N comes from a per-binary Monte Carlo under Newton: random orientation and phase, with an eccentricity distribution f(e) ∝ e^γ(s) per Hwang+2022. Use γ = 0.4 + 0.45·log10(s/100 AU), clipped to [0.4, 1.3].
- P_cont is empirical, taken from the shift catalog's ṽ distribution under the same cuts. It is broad and flat, which is acceptable.
- Fitted quantities: α (velocity scale) and c (contaminant fraction), by maximum likelihood on ṽ ∈ [0, 5].

## Statistic
R(s) = α(s)/α(control). Mass and calibration errors that do not depend on s cancel.

## Models for R(s) (computed per binary, then averaged in each bin with the same MC)
- **N, Newton:** R = 1.
- **F, fish:** g = g_N·[1 + Q(q)(ν(g_N/a0) − 1)], with μ_std and a0 = 1.042e-10.
  - Q(q) is Milgrom's deep-MOND two-body reduction: Q = (2/3)[(1)^{3/2} − q1^{3/2} − q2^{3/2}]/(q1 q2), with q_i = m_i/M. Equal masses give Q = 0.781.
  - Q is applied to the boost only. This is an approximation and is labelled `[O]`.
- **E, standard EFE (1D QUMOND):** g = ν(|g_N+g_e|/a0)(g_N+g_e) − ν(g_e/a0)g_e, with g_e = 1.9e-10 and the same Q factor.
- **S, Form-2 screened fish:** boost × S, with S = 1/(1+η²) and η = g_e/a0.

## Decision rule
- Compute χ² of the measured R(s) in the 4 test bins against each model.
- A model is **excluded** if χ² > 18.5 (4 dof, p < 0.001).
- The **shape test** is reported separately. F rises monotonically with s. E plateaus. N is flat.
- Both cut sets are reported. A verdict counts only if it holds under both.

## Amendment A (2026-10-04 ~03:00 CDT): committed before any real-data fit has run
The catalog was still downloading when this amendment was written. No real ṽ had been computed.

**A1. Fifth model: P, nesting / passenger `[O]`.** "The system" is the one whose field dominates. A binary whose own Newtonian pull at its 3D separation is below the host field (g_N < g_e = 1.9e-10) is a passenger. The host field is uniform across the orbit, so the passenger is Newtonian. Inside that radius it gets the fish boost.
- For 1.5 M☉ the boundary is r = √(GM/g_e) ≈ 6.8 kAU.
- The rival definition is "system = gravitationally bound". It gives the binary its own frame out to its ~300 kAU tidal radius, which is model F in every test bin.
- P is effectively indistinguishable from N in this test. A P/N tie therefore favours nesting over F and S, but it does not separate nesting from plain Newton.

**A2. Contaminant shape.** The shift catalog (518k pairs) has separations of 38–200 kAU (5–95%) and R_chance_align ≈ 1. Under the R ≤ 0.01 cut it has essentially no pairs in the test bins, so the empirical P_cont is unusable. The pre-registered fallback is used: P_cont ∝ ṽ on [0, 5], which is flat in the 2D velocity plane.

**A3. Predicted R(s) from the synthetic smoke test** (3000 mock binaries, M 0.8–2 M☉, σ_ṽ = 0.05). Recorded so that the predictions are fixed before the data are seen:

| bin (kAU) | F | S | E | P | N |
|---|---|---|---|---|---|
| 2–5 | 1.01 | 1.00 | 1.015 | 1.005 | 1.00 |
| 5–10 | 1.12 | 1.02 | 1.025 | 1.00 | 0.99 |
| 10–20 | 1.38 | 1.095 | 1.01 | 1.005 | 1.00 |
| 20–30 | 1.72 | 1.205 | 1.03 | 1.00 | 0.995 |

Injection recovery in the smoke test:
- N-injection: χ²(N) = 8.8 and χ²(F) = 692.
- F-injection: χ²(F) = 2.6 and χ²(N) = 563.
- P-injection: χ²(P) = 6.3 and χ²(F) = 1375.

E and N are **not** separable at this sample size: on the N-injection, χ²(E) = 15.6 < 18.5.

## Amendment B (2026-10-04): contaminant model, written before any refit

The fish rule is already excluded. This amendment does not refit Gaia. It locks the contaminant that the result note named and left unmodelled: hidden companions that grow with separation, and a mass error that grows with separation. The two are never free at the same time. Neither parameter is taken from the 2–5 kAU bin.

**B1. Variant T, hidden tertiary.** 
f_t(s) = clip( f_c * log10(s / 1000 AU) / log10(30), 0, 0.50 ).
Zero at 1 kAU, equal to f_c at 30 kAU. A tagged draw keeps its Newtonian outer speed and adds 1.5 in quadrature. 1.5 is fixed. It is the middle of the ṽ excess Banik et al. 2024 place near 1–2 `[C]`. f_c ≤ 0.50 because direct counts of close companions in local wide binaries lie below 50% (Moe & Di Stefano 2017, as cited by Hernandez et al. 2024) `[C]`.

**B2. Variant M, mass slope.** The mass used in ṽ is off by (s / 1000 AU)^β, so ṽ scales as (s / 1000 AU)^(−β/2). |β| ≤ 0.30.

**B3. Where the parameter is fit.** f_c and β are each fit by maximum likelihood on the control bin only, 500–2000 AU, where every gravity model is Newtonian. They are then frozen. Test bins use the frozen curve. They are not adjusted to the test-bin α values.

**B4. Decision rule for the next run.** A gravity model is excluded only if it stays over χ² = 18.5 under both cuts and under both frozen contaminants. If the frozen model does not remove the 2–5 kAU offset, that offset remains a sample systematic and no new gravity verdict is claimed.

**B5. Smoke test, synthetic only, no Gaia.** Injected f_c = 0.40. Recovered from the control bin: 0.40. Outer-bin median ṽ ratio: 1.65 injected, 1.55 predicted from the control fit. Code: `wide_binary_contaminant.py`.

## Validation (before the real run)
- Inject synthetic Newton and synthetic fish catalogs that carry the real sample's M, s and errors.
- The pipeline must recover R ≈ 1 for the Newton injection and the fish curve for the fish injection.
- If either recovery fails, the real result is not reported as a verdict.

## Amendment C (2026-10-04): calibration and baseline. Method fixed before these numbers are computed

This is **post-hoc** with respect to the corrected-sample result (9c986c0). It fixes the two loose ends named there. Its outcome is reported next to the pre-registered result and does not replace it.

**C1. Masses.**
- Use Mamajek's checked M_G → mass table (`EEM_dwarf_UBVIJHK_colors_Teff.txt`, be768c0) in place of the approximate table.
- Measured on the RV-fixed sample before this amendment, the close-bin Newton/data median is 0.994 (strict) and 0.987 (loose) with Mamajek masses. With the old table it was 1.034 and 1.015.

**C2. Mass stratification.**
- Inside the close bin the Newton/data ratio still depends on mass: 0.967 (< 1 M☉), 1.024 (1–1.5), 1.119 (≥ 1.5).
- So α is fitted separately in three strata (M < 1, 1 ≤ M < 1.5, M ≥ 1.5), each with its own template and its own 500–2000 AU control.
- R_k(s) = α_k(s)/α_k(control).
- Per s-bin, R is the inverse-variance-weighted mean over strata with ≥ 30 pairs.
- Model curves are combined with the same weights.

**C3. Threshold calibration.**
- For each model T in {N, F, E, S, P} and each cut, generate 40 injected catalogues: one draw per real binary under T, plus a 5% flat contaminant, as in the original injection.
- Run each through C1–C2 and compute χ²(T) against T's own curve.
- κ = median(null χ²)/3.357, where 3.357 is the χ²(4) median. The calibrated statistic is χ²/κ_T, with κ_T taken from that model's own null.
- **Exclusion:** χ²/κ_T > 18.5 in **both** cuts, and the raw χ² above the largest of that model's 40 null values in both cuts.

**C4. Precision.** Templates use 320 draws per binary. Model curves use 80.

Runner: `wide_binary_final.py`.
