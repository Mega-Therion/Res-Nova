# O4 JWST/NIRSpec a0(z) Execution Record (2026-11-26)

**Protocol:** `04_cosmology/PREREG_O4_JWST_A0Z_2026-11-26.md` (SHA-256: `074d198748f59c59dfceb7e32cd1088c77961edac5608316d66fbbe10f3b1153`)
**Script:** `04_cosmology/o4_jwst_a0z_run.py` -> `O4_JWST_A0Z_RESULT.json`
**Epistemic Tag:** `[D]` computed test output on published JWST catalogs (auxiliary de Graaff+2024 `[O]`)

## 1. Headline Primary Result (Pure JWST/NIRSpec 2-Bin `mbar`, N = 25)

- **Verdict:** **`CONFOUNDED`**
- **Mechanical $\Delta\chi^2 = \chi^2_{\rm const} - \chi^2_{\rm horizon}$:** `+16.66` (`+4.08`$\sigma$)
- **Shape-only $\Delta\chi^2_{\rm shape}$ (free overall normalization):** `-4.90` (`-2.21`$\sigma$)
- **Fitted scaling exponent $n$ in $a_0(z) \propto E(z)^n$:** `n = 0.14` (68% CI: `[-0.30999999999999994, 0.49]`)

| Bin | Sample | N | z_eff | E(z_eff) | a0_hat (1e-10 m/s^2) | 68% CI | sigma_int | chi2_const | chi2_horizon |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MSA-3D bounded (`2606.27853`) | 20 | 1.091 | 1.876 | 5.023 | 4.045--6.190 | 0.20 | 26.01 | 11.35 |
| 2 | ALPINE-CRISTAL (`2611.07064`) | 5 | 5.327 | 8.938 | 6.281 | 3.130--10.388 | 0.00 | 2.83 | 0.82 |

## 2. Sensitivity & Systematic Suite

| Variant | Delta-chi2 | Shape Delta-chi2 | n_hat (68% CI) | Verdict / Note |
|---|---|---|---|---|
| `joint_msa3d_fdm30_plus_alpine5` | `+54.97` | `-12.57` | `-0.37` ([-0.8200000000000001, -0.040000000000000036]) | CONFOUNDED |
| `joint_msa3d_N30_paper_gas_plus_alpine5` | `+20.02` | `-4.08` | `0.21` ([-0.26, 0.56]) | CONFOUNDED |
| `joint_msa3d_N30_mstar_floor_plus_alpine5` | `+27.87` | `-6.81` | `-0.01` ([-0.47, 0.3400000000000001]) | CONFOUNDED |
| `joint_clean_golden13_plus_alpine4` | `+9.62` | `-5.79` | `-1.00` ([None, 0.14000000000000012]) | CONFOUNDED |
| `joint_msa20_plus_alpine_nonparam5` | `+13.89` | `-3.82` | `-0.23` ([None, 0.41999999999999993]) | CONFOUNDED |
| `joint_msa20_plus_alpine_gas_minus_0p2dex` | `+19.93` | `-2.34` | `0.38` ([0.020000000000000018, 0.7]) | CONFOUNDED |
| `joint_msa_err_lo` | `+17.78` | `-6.03` | `0.06` ([-0.39, 0.40000000000000013]) | CONFOUNDED |
| `joint_msa_err_hi` | `+15.40` | `-3.85` | `0.21` ([-0.26, 0.5800000000000001]) | CONFOUNDED |
| `joint_msa_thin_adc` | `+20.88` | `-8.00` | `-0.09` ([-0.55, 0.25]) | CONFOUNDED |
| `joint_sparc_T1_baseline` | `+15.65` | `-4.90` | `0.14` ([-0.30999999999999994, 0.49]) | CONFOUNDED |
| `combined_4bin_RC100_plus_JWST` | `+84.19` | `-22.09` | `-0.35` ([-0.62, -0.010000000000000009]) | 4-bin meta |

## 3. Auxiliary de Graaff+2024 Check (`[O]`, Excluded from Primary)

| Galaxy | z | E(z) | g_dyn / g_pred_const (11x M*) | g_dyn / g_pred_horizon (11x M*) |
|---|---|---|---|---|
| `JADES-NS-00016745` | 5.566 | 9.48 | 2.02x | 0.84x |
| `JADES-NS-00019606` | 5.890 | 10.19 | 2.46x | 0.87x |
| `JADES-NS-00022251` | 5.799 | 9.99 | 0.88x | 0.42x |
| `JADES-NS-00047100` | 7.432 | 13.77 | 1.87x | 1.08x |
| `JADES-NS-10016374` | 5.504 | 9.35 | 3.21x | 1.54x |
| `JADES-NS-20086025` | 7.263 | 13.36 | 2.25x | 0.84x |
