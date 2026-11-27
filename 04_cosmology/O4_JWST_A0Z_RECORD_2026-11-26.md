# O4 JWST/NIRSpec a0(z) Execution Record (2026-11-26)

**Protocol:** `04_cosmology/PREREG_O4_JWST_A0Z_2026-11-26.md` (SHA-256: `074d198748f59c59dfceb7e32cd1088c77961edac5608316d66fbbe10f3b1153`)
**Script:** `04_cosmology/o4_jwst_a0z_run.py` -> `O4_JWST_A0Z_RESULT.json`
**Epistemic Tag:** `[D]` computed test output on published JWST catalogs (auxiliary de Graaff+2024 `[O]`)

## 1. Headline Primary Result (Pure JWST/NIRSpec 2-Bin `mbar`, N = 25)

- **Verdict:** **`CONFOUNDED`**
- **Mechanical $\Delta\chi^2 = \chi^2_{\rm const} - \chi^2_{\rm horizon}$:** `+16.56` (`+4.07`$\sigma$)
- **Shape-only $\Delta\chi^2_{\rm shape}$ (free overall normalization):** `-4.82` (`-2.20`$\sigma$)
- **Fitted scaling exponent $n$ in $a_0(z) \propto E(z)^n$:** `n = 0.15` (68% CI: `[-0.31, +0.50]`)

| Bin | Sample | N | z_eff | E(z_eff) | a0_hat (1e-10 m/s^2) | 68% CI | sigma_int | chi2_const | chi2_horizon |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MSA-3D bounded (`2606.27853`) | 20 | 1.091 | 1.876 | 4.982 | 4.011--6.142 | 0.20 | 25.68 | 11.16 |
| 2 | ALPINE-CRISTAL (`2611.07064`) | 5 | 5.327 | 8.938 | 6.294 | 3.140--10.406 | 0.00 | 2.84 | 0.81 |

## 2. Sensitivity & Systematic Suite

| Variant | Delta-chi2 | Shape Delta-chi2 | n_hat (68% CI) | Verdict / Note |
|---|---|---|---|---|
| `joint_msa3d_fdm30_plus_alpine5` | `+55.01` | `-12.46` | `-0.37` ([-0.82, -0.04]) | CONFOUNDED |
| `joint_msa3d_N30_paper_gas_plus_alpine5` | `+19.89` | `-4.02` | `0.22` ([-0.25, +0.56]) | CONFOUNDED |
| `joint_msa3d_N30_mstar_floor_plus_alpine5` | `+27.74` | `-6.75` | `0.00` ([-0.46, +0.34]) | CONFOUNDED |
| `joint_clean_golden13_plus_alpine4` | `+9.60` | `-5.78` | `-3.97` ([-inf, +0.13]) | CONFOUNDED |
| `joint_msa20_plus_alpine_nonparam5` | `+13.76` | `-3.78` | `-0.22` ([-inf, +0.42]) | CONFOUNDED |
| `joint_msa20_plus_alpine_gas_minus_0p2dex` | `+19.82` | `-2.26` | `0.39` ([+0.02, +0.71]) | CONFOUNDED |
| `joint_msa_err_lo` | `+17.64` | `-5.93` | `0.07` ([-0.38, +0.41]) | CONFOUNDED |
| `joint_msa_err_hi` | `+15.32` | `-3.79` | `0.22` ([-0.26, +0.59]) | CONFOUNDED |
| `joint_msa_thin_adc` | `+20.77` | `-7.92` | `-0.09` ([-0.54, +0.26]) | CONFOUNDED |
| `joint_sparc_T1_baseline` | `+16.22` | `-4.82` | `0.15` ([-0.31, +0.50]) | CONFOUNDED |
| `combined_4bin_RC100_plus_JWST` | `+84.19` | `-21.97` | `-0.34` ([-0.62, -0.01]) | 4-bin meta |

## 3. Auxiliary de Graaff+2024 Check (`[O]`, Excluded from Primary)

| Galaxy | z | E(z) | g_dyn / g_pred_const (11x M*) | g_dyn / g_pred_horizon (11x M*) |
|---|---|---|---|---|
| `JADES-NS-00016745` | 5.566 | 9.48 | 2.02x | 0.84x |
| `JADES-NS-00019606` | 5.890 | 10.19 | 2.46x | 0.87x |
| `JADES-NS-00022251` | 5.799 | 9.99 | 0.88x | 0.42x |
| `JADES-NS-00047100` | 7.432 | 13.77 | 1.87x | 1.08x |
| `JADES-NS-10016374` | 5.504 | 9.35 | 3.21x | 1.54x |
| `JADES-NS-20086025` | 7.263 | 13.36 | 2.25x | 0.84x |
