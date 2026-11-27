# P-OM-1 v2 Blind Run on KiDS-Legacy (DR5) & GAMA DR4 (2026-11-26)

**Protocol:** `03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md` (SHA-256: `2d925eb6c776b738a4c356dd31c6282d9c233a657183f5e8cfcbf0b35be37ec8`)
**Script:** `03_observer_jwst/pom1v2_blind_kids_legacy.py` -> `POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`
**Epistemic Tag:** `[D]` computed blind weak-lensing outcome (KiDS-Legacy 40,894,394 sources across `329` covered unseen DR5 tiles + GAMA DR4; Euclid Q1/DR1 TAP exposes zero `she_*` tables)

## 1. Pre-Unblinding North vs South Massive-Lens Shear Check (`log M* > 11.1`)

- **North (`G09/G12/G15`, N=16304):** `<e_t> = +0.00525`, `<e_x> = -0.00027`
- **South (`G23`, N=3965):** `<e_t> = +0.00513`, `<e_x> = +0.00060`

## 2. Headline Blind Combined Verdicts (Strictly Disjoint Sky: `DR5_New329` + `GAMA_G23`)

- **Pre-Registered Faithful (`B21 cut`, `Planck18`, `Q_ETG=1.0`):** **`FAIL`** (Hartlap `FAIL`) — $\chi^2 = 99.77$ (`76.02`H) / `28` (`p = 5.52e-10`, Hartlap `2.58e-06`), Newtonian `p = 8.86e-144`, best $\pm 0.2\,\mathrm{dex}$ shift `+0.200` (`p = 0.000102`, `0.00752`H).
- **Mistele+2024 Spec (`z_B > z_l+0.20`, `[z_l, inf)` norm, `WMAP9`, `Q_ETG=1.0`):** **`FAIL`** (Hartlap `FAIL`) — $\chi^2 = 116.80$ (`88.99`H) / `28` (`p = 8.19e-13`, Hartlap `2.85e-08`), Newtonian `p = 6.12e-164`, mass shift `+0.200` (`p = 1.25e-05`).
- **Mistele+2024 Spec + `Q_ETG=1.4`:** **`FAIL`** (Hartlap `PASS_WITHIN_MASS_SYSTEMATIC`) — $\chi^2 = 71.65$ (`54.59`H) / `28` (`p = 1.09e-05`, Hartlap `0.0019`), Newtonian `p = 2.51e-151`, mass shift `+0.150` (`p = 0.009`).

## 3. Primary & Mistele+2024 Sample Summary

| Sample | Isolated Lenses | chi2 (Hartlap) / dof | p (Hartlap) | LTG (med obs/pred) | ETG (med obs/pred) | ETG-LTG p | Cross-shear p | Verdict |
|---|---|---|---|---|---|---|---|---|
| `DR5_New329_prereg_faithful` | 105,699 | 85.76 (65.34H) / 14 | 2.38e-12 (1.33e-08H) | 6.4/7 (1.00) | 70.3/7 (1.46) | 3.09e-05 | 0.6 | **`FAIL`** (`FAIL`H) |
| `GAMA_G23_prereg_faithful` | 8,185 | 14.01 (10.67H) / 14 | 0.449 (0.712H) | 9.8/7 (0.86) | 5.0/7 (1.01) | 0.551 | 0.54 | **`NO_POWER`** (`NO_POWER`H) |
| `GAMA_All4_prereg_faithful` | 44,911 | 41.08 (31.30H) / 14 | 0.000173 (0.00503H) | 5.9/7 (1.16) | 37.2/7 (1.54) | 0.0189 | 0.0197 | **`PASS_WITHIN_MASS_SYSTEMATIC`** (`PASS_WITHIN_MASS_SYSTEMATIC`H) |
| `DR5_New329_mistele_Q1` | 107,139 | 99.39 (75.73H) / 14 | 6.2e-15 (1.74e-10H) | 6.7/7 (1.07) | 79.7/7 (1.60) | 8.66e-06 | 0.862 | **`FAIL`** (`FAIL`H) |
| `DR5_New329_mistele_QETG1.4` | 107,139 | 48.65 (37.07H) / 14 | 1.02e-05 (0.00072H) | 6.7/7 (1.07) | 35.1/7 (1.36) | 0.0259 | 0.748 | **`PASS_WITHIN_MASS_SYSTEMATIC`** (`PASS_WITHIN_MASS_SYSTEMATIC`H) |
| `GAMA_G23_mistele_Q1` | 8,055 | 17.41 (13.26H) / 14 | 0.235 (0.506H) | 10.9/7 (0.58) | 3.5/7 (0.96) | 0.19 | 0.77 | **`NO_POWER`** (`NO_POWER`H) |
| `GAMA_G23_mistele_QETG1.4` | 8,055 | 22.99 (17.52H) / 14 | 0.0604 (0.23H) | 10.9/7 (0.58) | 7.3/7 (1.16) | 0.0892 | 0.479 | **`NO_POWER`** (`NO_POWER`H) |
| `GAMA_All4_mistele_Q1` | 45,050 | 29.83 (22.73H) / 14 | 0.00805 (0.0648H) | 3.4/7 (1.16) | 23.9/7 (1.54) | 0.132 | 0.00458 | **`PASS_WITHIN_MASS_SYSTEMATIC`** (`PASS`H) |
| `GAMA_All4_mistele_QETG1.4` | 45,050 | 22.39 (17.06H) / 14 | 0.0709 (0.253H) | 3.4/7 (1.16) | 17.1/7 (1.19) | 0.237 | 0.00118 | **`PASS`** (`PASS`H) |
| `GAMA_All4_mistele_ext1.5Mpc_Q1` | 45,050 | 65.09 (46.59H) / 26 | 3.35e-05 (0.00783H) | 31.0/13 (1.23) | 35.3/13 (1.43) | 0.308 | 3.46e-05 | **`PASS_WITHIN_MASS_SYSTEMATIC`** (`PASS_WITHIN_MASS_SYSTEMATIC`H) |
| `GAMA_All4_mistele_ext1.5Mpc_QETG1.4` | 45,050 | 56.04 (40.11H) / 26 | 0.000558 (0.038H) | 31.0/13 (1.23) | 22.1/13 (1.19) | 0.114 | 0.000193 | **`PASS_WITHIN_MASS_SYSTEMATIC`** (`PASS`H) |

## 4. Diagnostic & Isolation Matrix (Shared 20x Random Catalogs)

| Variant | chi2 (Hartlap) / dof | p (Hartlap) | Mass shift | Early-Late p | Cross-shear p | Verdict |
|---|---|---|---|---|---|---|
| `DR5_New329_prereg_QETG1.4` | 39.50 (30.09H) / 14 | 0.000305 (0.00741H) | +0.155 (p=0.135) | 0.115 | 0.83 | `PASS_WITHIN_MASS_SYSTEMATIC` (`PASS_WITHIN_MASS_SYSTEMATIC`H) |
| `DR5_New329_WMAP9_b21cut_Q1` | 85.32 (65.01H) / 14 | 2.88e-12 (1.53e-08H) | +0.200 (p=4.46e-05) | 1.2e-05 | 0.812 | `FAIL` (`FAIL`H) |
| `DR5_New329_WMAP9_b21cut_QETG1.4` | 37.94 (28.90H) / 14 | 0.000532 (0.0108H) | +0.144 (p=0.216) | 0.0527 | 0.679 | `PASS_WITHIN_MASS_SYSTEMATIC` (`PASS`H) |
| `DR5_New329_strict_tomo_QETG1.4` | 53.65 (40.88H) / 14 | 1.47e-06 (0.000186H) | +0.162 (p=0.0271) | 0.00488 | 0.93 | `PASS_WITHIN_MASS_SYSTEMATIC` (`PASS_WITHIN_MASS_SYSTEMATIC`H) |
| `GAMA_All4_mass_matched_mistele_Q1` | 20.40 (15.55H) / 14 | 0.118 (0.342H) | +0.200 (p=0.359) | 0.221 | 0.0166 | `PASS` (`PASS`H) |
| `GAMA_All4_mass_matched_mistele_QETG1.4` | 17.52 (13.35H) / 14 | 0.229 (0.499H) | +0.198 (p=0.735) | 0.598 | 0.0385 | `PASS` (`PASS`H) |
| `GAMA_All4_spec_cyl_1000kms_Q1` | 7.91 (6.03H) / 14 | 0.894 (0.966H) | +0.106 (p=0.868) | 0.702 | 0.32 | `NO_POWER` (`NO_POWER`H) |
| `GAMA_All4_spec_cyl_1000kms_QETG1.4` | 7.70 (5.87H) / 14 | 0.904 (0.97H) | +0.047 (p=0.866) | 0.739 | 0.723 | `NO_POWER` (`NO_POWER`H) |
| `GAMA_All4_Risol4Mpc_QETG1.4` | 35.82 (27.29H) / 14 | 0.00111 (0.0176H) | +0.200 (p=0.0388) | 0.098 | 0.513 | `PASS_WITHIN_MASS_SYSTEMATIC` (`PASS`H) |
| `DR5_New329_Risol4Mpc_Q1` | 96.44 (73.48H) / 14 | 2.27e-14 (4.49e-10H) | +0.200 (p=2.21e-05) | 0.00427 | 0.689 | `FAIL` (`FAIL`H) |
| `DR5_New329_Risol4Mpc_QETG1.4` | 47.21 (35.97H) / 14 | 1.78e-05 (0.00106H) | +0.200 (p=0.0868) | 0.138 | 0.301 | `PASS_WITHIN_MASS_SYSTEMATIC` (`PASS_WITHIN_MASS_SYSTEMATIC`H) |
| `DR5_New329_rawZB_QETG1.4` | 15.60 (11.88H) / 14 | 0.339 (0.616H) | -0.094 (p=0.323) | 0.115 | 0.0109 | `PASS` (`NO_POWER`H) |
| `DR5_New329_mistele_QETG1.4_noH0` | 38.08 (29.02H) / 14 | 0.000505 (0.0104H) | +0.132 (p=0.121) | 0.0259 | 0.748 | `PASS_WITHIN_MASS_SYSTEMATIC` (`PASS`H) |
| `GAMA_G23_mistele_noH0` | 18.26 (13.91H) / 14 | 0.195 (0.456H) | -0.200 (p=0.295) | 0.19 | 0.77 | `NO_POWER` (`NO_POWER`H) |

## 5. Methodological Audit & Fixes vs Initial `#279` Run

1. **Photometric cut & $\Sigma_{\rm crit}^{-1}$ normalization (`z_B > z_l + 0.20` + `[z_l, inf)`):** Initial `#279` used Brouwer+2021 `(z_B + 0.20) > z_l` with `[0, inf)` tomographic `NZ_SOURCE` normalization (`TOMOBIN=1` leaks foreground/cluster members) and Planck 2018 distances (`0.3153, 0.6847`). Both pre-registered B21-style and exact Mistele+2024 (`arXiv:2310.15248`: `WMAP9 0.2793/0.7207`, `z_B > z_l + 0.20`, `[z_l, inf)` norm) + `strict_tomo` (`Z_B_min(tomo) > z_l + 0.20`) results are reported above.
2. **Shared 20x random catalogs across `Q_ETG = 1.0` vs `1.4`:** Initial `#279` ran `Q_ETG = 1.4` with a smaller, distinct random draw (`rand_mult=2, seed=302` vs `rand_mult=3, seed=301`), corrupting identical `LTG` bins (`chi2: 8.27 -> 15.58`), and intermediate `5x` random subtraction still induced `±18 chi2` Monte Carlo random-shot variance. Both `Q_ETG` values now share identical `20x` covered-footprint randoms with global lens-tree JK matching, guaranteeing `LTG` invariance to `< 1e-12` and suppressing random-shot variance by 4x.
3. **DR5 tile coverage, unwrapped per-patch jackknife & GAMA edge guard:** Filtered `DR5_New329` tiles directly against covered KiDS-Legacy shear footprints (`>= 50` sources within `0.45 deg`), replaced global RA-sorted jackknife (which straddled disconnected `G09/G12/G15/G23` and `RA=0/360`) with compact per-patch unwrapped 2D KD jackknife, widened GAMA border guard to `0.45 deg` (`> 3 Mpc` at `z=0.1`), and replaced the degenerate `cyl_dz0.02` check (`32` galaxies surviving out of `106k`) with `GAMA_All4_spec_cyl_1000kms` (`R_p < 3 Mpc, |dv| < 1000 km/s`) and `R_isol = 4 Mpc/h70` checks.
4. **Reproducibility:** Added `ensure_data()` and streaming 401-byte FITS binary conversion (`convert_kids_legacy_fits_to_slim()`) so the pipeline runs cleanly from official URLs without undocumented `/tmp` artifacts.
