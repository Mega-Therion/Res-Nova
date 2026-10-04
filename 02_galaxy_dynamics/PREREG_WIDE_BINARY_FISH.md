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

## Validation (before the real run)
- Inject synthetic Newton and synthetic fish catalogs that carry the real sample's M, s and errors.
- The pipeline must recover R ≈ 1 for the Newton injection and the fish curve for the fish injection.
- If either recovery fails, the real result is not reported as a verdict.
