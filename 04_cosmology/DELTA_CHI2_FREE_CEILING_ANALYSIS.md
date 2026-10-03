# Δχ² across ΛCDM and the ceiling models (compressed-prior fit), 2026-10-03

**Source.** An outside agent's analysis (2026-10-03), checked and corrected on intake by Claude Code.

**Run basis.** `04_cosmology/CEILING_MODEL_CMB_BAO_SN.json`, from `ceiling_model_cmb_bao_sn.py`. The agent's
independent rerun of the same script reproduced every number in that file to within 1×10⁻¹¹.

**Likelihood evaluated.** Compressed Planck distance priors `(R, l_A, ω_b)` (Chen, Huang & Wang 2019), DESI DR2
BAO and Pantheon+. This is **not** the Planck likelihood. The clik-based joint runner for that is
`scripts/run_joint_cobaya.py`; it builds and evaluates a point under Cobaya, but no chain has been run.

**The fixed ceiling is κ = √0.91 = 0.9539.** "Free ceiling" means Ω_f is fitted.

## Results

| Model | Free params | χ² | Δχ² vs ΛCDM | CMB | BAO | SN |
|---|---:|---:|---:|---:|---:|---:|
| Flat ΛCDM | 3 | 1419.706 | 0 | 2.467 | 11.837 | 1405.402 |
| Fixed ceiling, n = 0.5 | 2 | 1618.357 | +198.651 | 104.030 | 84.664 | 1429.664 |
| Fixed ceiling, n = 1 | 2 | 1420.780 | +1.074 | 8.702 | 9.507 | 1402.571 |
| Fixed ceiling, n = 2 | 2 | 1419.620 | −0.086 | 1.631 | 13.539 | 1404.451 |
| Free ceiling (Ω_f = 0.97625), n = 1 | 3 | 1417.368 | −2.338 | not saved | not saved | not saved |

## Complexity-aware comparison

N = 1,590 SNe + 13 BAO + 3 CMB priors = 1,606 data points, so ln N = 7.38. The fixed ceilings have one parameter fewer
than ΛCDM. The free ceiling has the same count.

| Model | ΔAIC = Δχ² + 2Δk | ΔBIC = Δχ² + Δk·ln N |
|---|---:|---:|
| Fixed, n = 0.5 | +196.65 | +191.27 |
| Fixed, n = 1 | −0.93 | −6.31 |
| Fixed, n = 2 | −2.09 | −7.47 |
| Free, n = 1 | −2.34 | −2.34 |

- The fixed n = 1 and n = 2 ceilings tie ΛCDM on χ² with one parameter fewer. BIC therefore prefers them by 6 to 7.5, a
  "positive" to "strong" preference. This matches the O3 route's ΔBIC ≈ −8 with DES-Y5
  (`O3_HORIZON_LANDING_ROUTE_2026-09-28.md`).
- The free ceiling has the same parameter count as ΛCDM, so its Δχ² = −2.34 carries no complexity penalty under either
  criterion. It is still small: not a detection, and sensitive to optimiser tolerance, bounds, and the defect below.
- *Corrected on intake:* the incoming text said BIC could not be computed until N was specified, and that the free
  ceiling's −2.34 "would not survive a conventional BIC penalty". N is fixed by the data used. For the free ceiling
  against ΛCDM, the BIC penalty difference is zero.

## A defect that affects every CMB column `[O]`

At Planck's own best-fit point (Ω_m = 0.3153, h = 0.6736, ω_b = 0.02237), the script gives R = 1.74962 and
l_A = 302.008, against the priors 1.750235 and 301.4707. That is **χ²_CMB = 47.5**; l_A misses by about 6σ.

The script's docstring says this validation "must reproduce the priors", and it does not. Every CMB block above, and
the CMB-including O3 results, inherit the offset.

**Likely cause (not yet confirmed):** z\* is taken from the Hu–Sugiyama fit, which gives 1091.9 against Planck's
1089.9. That shift alone moves l_A by about 0.14%, close to the 0.18% miss. Confirm the convention Chen, Huang & Wang
used for z\* and r_s, fix the script, and rerun before citing any CMB-including ceiling number.

## What drives the fixed-model differences

- **n = 0.5:** fails in all three blocks (CMB +102, BAO +73, SN +24 against ΛCDM). This is a distance-shape failure.
- **n = 1:** CMB worsens by 6.2; BAO and SN improve by 2.3 and 2.8 (net +1.07).
- **n = 2:** BAO worsens by 1.7; CMB and SN improve by 0.8 and 1.0 (net −0.09).
- The near-ties are compensation between blocks, not every block preferring the ceiling.
- *Corrected on intake:* the incoming text had BAO worsening at n = 1 and SN worsening at n = 2. Both signs were wrong;
  the per-block changes above sum to each Δχ².
- The free ceiling's block split was not saved, so its improvement cannot yet be located.

## What the result does and does not show

**It shows:**
- a distance–redshift history inside this phenomenological family that fits about as well as ΛCDM with fewer
  parameters (fixed ceiling);
- a slightly better fit with equal parameters (free ceiling).

**It does not show:**
- that Ω_f is a physical constant, or that its value is unique;
- anything about the Hubble tension;
- a preference under the full Planck likelihood;
- anything joint with SPARC. The SPARC fit is separate, with a₀ tied to H₀ by the O1 anchor.

## Next checks

1. Fix and re-validate the compressed CMB block (above).
2. Run the clik-based joint likelihood. First fix its SPARC sector: a global distance scale absorbs a₀
   (`scripts/run_joint_cobaya.py`, "Known limitation").
3. Save block-wise CMB, BAO, SN and SPARC log-likelihoods for every fit.
4. Run leave-one-block-out predictive scores and prior-sensitivity maps over (Ω_f, n). The preregistration is
   `PREREG_FREE_CEILING_E4_E7.md`.
