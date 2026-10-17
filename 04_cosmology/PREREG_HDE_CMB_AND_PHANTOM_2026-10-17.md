# Pre-registration: late-time HDE under the fixed CMB block, and the phantom-crossing window on DESI DR2

Filed 2026-10-17 before either fit in this note is run. Work order: Muse, Block page 3fc77b95-a965-8135-8de4-cc6fcc56e21e. The c² = ln 2 event-horizon kill stays closed and is not rerun as a kill test. ln 2 is not derived here. Tier of both questions before the run: the hypotheses are open; the likelihood is the existing one.

## Shared equations

Future-event-horizon holographic dark energy (Li 2004), the same ODE as `hde_fit_chw.py`:

- ρ_DE = 3 C² M_P² / R_eh², R_eh = a ∫_a^∞ da′ / (a′² H).
- Flat, Ω_r = Ω_m / (1 + z_eq), z_eq = 2.5×10⁴ Ω_m h² (T/2.7)⁻⁴, T = 2.7255 K (Chen, Huang & Wang 2019, eq. 6).
- d ln Ω_DE / d ln a = (1 − Ω_DE) (1 + 2 √Ω_DE / C) + Ω_r a⁻⁴ (1 − Ω_DE) / (Ω_m a⁻³ + Ω_r a⁻⁴), integrated from a = 1 toward the past.
- w = −1/3 − 2 √Ω_DE / (3 C). This equals −1 exactly when Ω_DE = C², and w < −1 when Ω_DE > C².

C = √(ln 2) = 0.8325546111576977 is the frozen coefficient of the dead model. It is an input, not a fit.

## Test 1 — does the late-time edge survive CMB?

**What the late-time edge is.** On DESI DR2 + Pantheon+ with no CMB (Hood artifact `2026-10-15__claude_cli__hde-with-c-2-ln-2-pre-registered-test-killed-con`, commit context baf84ba): χ²(ΛCDM) = 1416.18, χ²(HDE, C free) = 1412.73, so Δχ²(HDE − ΛCDM) = −3.5. Separately, C = √(ln 2) sits Δχ² = 5.5 above free C on that same late-time likelihood (about 2.3σ). Those two numbers are the edge being tested. They are not recomputed here and they do not decide Test 1.

**Data.** Planck 2018 compressed distance priors through the fixed Chen, Huang & Wang 2019 block in `hde_fit_chw.py`: (R, ℓ_A, ω_b) = (1.750235, 301.4707, 0.02235976) and that file's `PINV`; z* with g₁ coefficient 0.0738. Plus DESI DR2 BAO (`rd` from Aubourg et al. 2015 as in `ceiling_model_cmb_bao_sn.rd_mpc`) and Pantheon+ with M marginalized. The block that gave χ²_CMB = 47.5 at Planck's own best fit is not used.

**Models and parameters.**

- ΛCDM: Ω_m, h, ω_b.
- HDE, C free: Ω_m, h, ω_b, C.

**Gate.** V0 from `hde_fit_chw.py` must pass before any χ² is written: at Planck 2018 TT,TE,EE+lowE+lensing (0.3153, 0.6736, 0.02237) and TT,TE,EE+lowE (0.3166, 0.6727, 0.02236), χ²_CMB < 3 and every pull inside 1. If V0 fails, Test 1 has no verdict.

**Statistic.** Δ₁ = χ²(HDE, C free) − χ²(ΛCDM) on the joint likelihood.

**Bar, frozen.** HDE wins if and only if Δ₁ < −9 (better than ΛCDM by more than the same one-parameter 3σ bar used in the closed kill, The-Hood 7dad232). Otherwise the late-time edge does not survive CMB. A value −9 ≤ Δ₁ < −4 is tension in HDE's favour and is not a win. Δ₁ ≥ 0 means HDE is worse.

## Test 2 — phantom crossing against DESI DR2 BAO

**Window, taken from Manus 2026-10-14 (Block page 3fa77b95-a965-81b6-a652-e285e1f2bc6b), not refit.** With radiation and curvature off, C² = ln 2, and the illustrative Ω_DE0 = 0.6847, quadrature of the ODE gives Δ ln a ≈ 0.01317 from today to the surface Ω_DE = ln 2. Because Ω_DE is increasing, the crossing is in the future: z_cross = exp(−Δ ln a) − 1 < 0. w is above −1 today and below −1 after the crossing. Late-time limit if Ω_DE → 1 is w → −1/3 − 2/(3C) ≈ −1.134.

**Reproduction gate.** Re-integrate that radiation-free ODE. The test aborts with no DESI verdict unless the computed Δ ln a agrees with 0.01317 to 1×10⁻⁴. The pre-registered window is then z ∈ [z_cross − 0.01, z_cross + 0.01].

**Data.** DESI DR2 BAO only, the same `chi_bao` as `hde_fit_chw.py`. No CMB. No Pantheon+. ω_b fixed at 0.02237.

**Models, equal parameter count (h only).**

- Crossing history: HDE at C = √(ln 2), with Ω_DE0 fixed at 0.6847 (Ω_m = 1 − 0.6847 − Ω_r(h)). By the w formula this history crosses −1 inside the window.
- No crossing: flat ΛCDM with the same Ω_Λ0 = 0.6847 (Ω_m = 1 − 0.6847 − Ω_r(h)), so w = −1 at every z.

**Statistic.** Δ₂ = χ²_BAO(crossing) − χ²_BAO(ΛCDM).

**Bar, frozen.** Excluded if Δ₂ > 9. Allowed (consistent) if Δ₂ < 4. If 4 ≤ Δ₂ ≤ 9, the label is tension and the crossing is not excluded. A free-(Ω_m, h) pair may be written beside this and does not change the label.

## What is not decided

A free-C HDE fit on the joint data is not a new kill of C = √(ln 2). D7 is untouched. No Zenodo deposit.
