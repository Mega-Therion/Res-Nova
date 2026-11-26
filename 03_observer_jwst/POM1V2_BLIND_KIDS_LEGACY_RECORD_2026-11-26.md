# P-OM-1 v2 Blind Run on KiDS-Legacy (DR5) & GAMA DR4 (2026-11-26)

**Protocol:** `03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md` (SHA-256: `2d925eb6c776b738a4c356dd31c6282d9c233a657183f5e8cfcbf0b35be37ec8`)
**Script:** `03_observer_jwst/pom1v2_blind_kids_legacy.py` -> `POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`
**Epistemic Tag:** `[D]` computed blind weak-lensing outcome (KiDS-Legacy 40,894,394 sources; Euclid Q1/DR1 TAP exposes zero `she_*` tables)

## 1. Headline Blind Combined Verdict (Strictly Disjoint Sky: `DR5_New329` + `GAMA_G23`)

- **Headline Blind Verdict:** **`FAIL`**
- **Combined $\chi^2 / \mathrm{dof}$:** `66.98 / 28` (`p = 4.86e-05`)
- **Newtonian Point-Mass Rejection:** $\chi^2 = 500.1 / 28$ (`p = 6.31e-88`)
- **Within $\pm 0.2\,\mathrm{dex}$ mass shift:** $\delta = +0.166\,\mathrm{dex}$, $\chi^2 = 49.46 / 27$ (`p = 0.00524`)

## 2. Sample Summary (`g_bar > 7.56e-14` Reliable & Extended 1.5 Mpc)

| Sample | Isolated Lenses | chi2 / dof | p | LTG (med obs/pred) | ETG (med obs/pred) | ETG-LTG p | Cross-shear p | Verdict |
|---|---|---|---|---|---|---|---|---|
| `DR5_New329_primary` | 97,544 | 48.45 / 14 | 1.11e-05 | 8.3/7 (1.06) | 35.6/7 (1.42) | 0.000527 | 0.0309 | **`FAIL`** |
| `GAMA_G23_primary` | 8,186 | 18.53 / 14 | 0.184 | 13.7/7 (0.66) | 7.3/7 (1.13) | 0.362 | 0.0286 | **`NO_POWER`** |
| `GAMA_All4_reliable` | 44,913 | 46.40 / 14 | 2.41e-05 | 6.8/7 (1.31) | 32.8/7 (1.76) | 0.0354 | 9.61e-06 | **`FAIL`** |
| `GAMA_All4_extended_1.5Mpc` | 44,913 | 60.94 / 26 | 0.000125 | 16.0/13 (1.19) | 40.2/13 (1.59) | 0.289 | 0.000505 | **`PASS_WITHIN_MASS_SYSTEMATIC`** |

## 3. Systematic & Diagnostic Matrix

| Variant | chi2 / dof | p | Mass shift | Early-Late p | Verdict |
|---|---|---|---|---|---|
| `GAMA_All4_mass_matched` | 27.04 / 14 | 0.019 | +0.200 (p=0.126) | 0.111 | `PASS` |
| `DR5_New329_zcal_QETG1.4` | 30.54 / 14 | 0.00642 | +0.167 (p=0.189) | 0.227 | `PASS_WITHIN_MASS_SYSTEMATIC` |
| `DR5_New329_rawZB_QETG1.4` | 15.91 / 14 | 0.319 | -0.183 (p=0.336) | 0.658 | `NO_POWER` |
| `DR5_New329_cyl_dz0.02` | 15.76 / 3 | 0.00127 | +0.200 (p=0.000424) | nan | `NO_POWER` |
| `DR5_New329_noH0_conv` | 41.77 / 14 | 0.000134 | +0.149 (p=0.00944) | 0.000527 | `FAIL` |
| `GAMA_G23_noH0_conv` | 18.89 / 14 | 0.169 | -0.155 (p=0.155) | 0.362 | `NO_POWER` |
