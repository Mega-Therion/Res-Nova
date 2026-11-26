# JWST Spectroscopically Confirmed z >= 10 Target Catalog (2026-11-26)

**Status:** `[D]` Observation-tier catalog compilation (replaces the retired 18-galaxy placeholder table).
**Generator & Verifier:** `03_observer_jwst/jwst_zgt10_targets.py` (`--check` verifies zero <1" sky duplicates, z >= 10 cuts, and exact JSON/CSV parity).

## Summary
- **Secure spectroscopic confirmations (`z_spec >= 10.0`):** **50** NIRSpec/ALMA spectra covering **48** unique physical galaxies (accounting for multiply-imaged MACS 0647 `JD1/JD2` and `JD1c/JD2c`).
- **Highest confirmed redshift:** `MoM-z14` at **`z_spec = 14.4441`** (Naidu+2025 `2505.11263`, Heintz+2026 `2606.30787`).
- **Tentative `flag=D` JADES DR4 entries (quarantined from primary count):** 3.
- **Disputed / revised (`CAPERS-EGS-65480`):** 1 (listed at 12.344 in RB25; revised to `z_spec = 5.875 +/- 0.012` in CAPERS `2610.12322` Table 2).
- **Quarantined photometric interlopers (`CEERS-93316`, `COSMOS-39810`):** 2 (including legacy optical-map anchor `CEERS-93316` at `z_spec = 4.912`).
- **Cosmic-variance / lensing-boost context:** Across 6 fields (GOODS-S, GOODS-N, EGS, UDS, COSMOS, Abell 2744, MACS 0647, BEACON parallel), confirmed `z > 10` galaxies span `10.01 <= z_spec <= 14.44`, replacing every unconfirmed `z > 15` photometric candidate previously cited on the optical tier (`C4`).

## Secure Spectroscopically Confirmed z >= 10 Targets

| # | Primary ID | Field | RA (deg) | Dec (deg) | z_spec | M_UV | mu | Quality | Catalogs | Primary Ref |
|---|------------|-------|----------|-----------|--------|------|----|---------|----------|-------------|
| 1 | `MoM-z14` | COSMOS | 150.09333 | 2.27316 | 14.4441 | -20.00 | 1.0 | A/B/C(DJA)+N25 | N25;RB25;H26 | Naidu+2025 (2505.11263); Heintz+2026 (2606.30787) |
| 2 | `JADES-GS-z14-0` | GOODS-S | 53.08294 | -27.85563 | 14.1832 | -20.96 | 1.0 | C(DR4)+ALMA | RB25;JADES_DR4;H26 | Carniani+2024; Schouws+2025; Curtis-Lake+2025 (2510.01033) |
| 3 | `JADES-GS-z14-1` | GOODS-S | 53.07427 | -27.88592 | 14.0440 | -19.21 | 1.0 | C(DR4) | RB25;JADES_DR4;H26 | Carniani+2024; Curtis-Lake+2025 (2510.01033) |
| 4 | `PAN-z14-1` | Parallel | 334.25036 | 0.37921 | 13.5300 | -20.60 | 1.0 | PRISM_break | D26 | Donnan+2026 (2601.11515) |
| 5 | `JADES-GS-z13-0` | GOODS-S | 53.14988 | -27.77650 | 13.2000 | -18.73 | 1.0 | C(DR4) | RB25;JADES_DR4;H26 | Curtis-Lake+2023; Hainline+2024; Curtis-Lake+2025 |
| 6 | `JADES-GS-z13-1-LA` | GOODS-S | 53.06475 | -27.89024 | 13.0100 | -18.70 | 1.0 | C(DR4)+Lya | RB25;JADES_DR4;H26;W26 | Witstok+2025; Witstok+2026 (2603.18775) |
| 7 | `CAPERS-UDS-z13` | UDS | 34.29201 | -5.17414 | 12.9800 | -20.03 | 1.0 | zq=9(CAPERS) | CAPERS26 | CAPERS / Taylor+2026 (2610.12322) |
| 8 | `UNCOVER-13077` | Abell 2744 | 3.57087 | -30.40159 | 12.9080 | -19.37 | 2.5 | A/B/C(DJA) | RB25 | Fujimoto+2023; Wang+2023 |
| 9 | `JADES-GS-z12-0` | GOODS-S | 53.16635 | -27.82156 | 12.4800 | -18.98 | 1.0 | C(DR4)+lines | RB25;JADES_DR4;H26 | Curtis-Lake+2023; D'Eugenio+2024; Curtis-Lake+2025 |
| 10 | `UNCOVER-38766` | Abell 2744 | 3.51356 | -30.35680 | 12.3930 | -19.10 | 1.7 | A/B/C(DJA) | RB25 | Fujimoto+2023; Wang+2023 |
| 11 | `GHZ2` | Abell 2744 | 3.49898 | -30.32475 | 12.3420 | -20.96 | 1.3 | lines+ALMA | RB25;H26 | Castellano+2024; Zavala+2025 |
| 12 | `CAPERS-UDS-88619` | UDS | 34.31913 | -5.23014 | 11.5100 | -20.28 | 1.0 | zq=3(CAPERS) | CAPERS26;H26 | Heintz+2026 (2606.30787); CAPERS (2610.12322) |
| 13 | `EGS-z11-R0` | EGS | 214.86171 | 52.86185 | 11.4520 | -19.78 | 1.0 | lines_SNR>3 | R26 | Rodighiero+2026 (2603.15841, 2605.22914) |
| 14 | `Maisie` | EGS | 214.94315 | 52.94244 | 11.4160 | -20.25 | 1.0 | lines+break | AH23;RB25;H26 | Arrabal Haro+2023 (2303.15431); Finkelstein+2024 |
| 15 | `JADES-GS-z11-1` | GOODS-S | 53.11763 | -27.88818 | 11.2750 | -19.56 | 1.0 | C(DR4) | RB25;JADES_DR4;H26 | Tang+2025; Curtis-Lake+2025 (2510.01033) |
| 16 | `goods-s-mediumjwst_177075` | GOODS-S | 53.05613 | -27.86398 | 11.1179 | -- | 1.0 | C(DR4) | JADES_DR4 | Curtis-Lake+2025 (2510.01033); Heintz+2026 |
| 17 | `JADES-GS-z11-0` | GOODS-S | 53.16477 | -27.77463 | 11.1220 | -19.38 | 1.0 | C(DR4) | RB25;JADES_DR4;H26 | Curtis-Lake+2023; Witstok+2025_O3; Curtis-Lake+2025 |
| 18 | `CEERS-10` | EGS | 214.90663 | 52.94550 | 11.0430 | -20.26 | 1.0 | lines+MIRI | AH23;RB25;H26;Ha26 | Arrabal Haro+2023; Harikane+2026 (2601.21833) |
| 19 | `CAPERS-UDS-z11` | UDS | 34.26444 | -5.09623 | 11.0080 | -20.44 | 1.0 | zq=3(CAPERS) | RB25;H26;CAPERS26 | Kokorev+2025; CAPERS (2610.12322) |
| 20 | `MoM-z11-1` | COSMOS | 150.11405 | 2.19134 | 10.9210 | -19.98 | 1.0 | A/B/C(DJA) | RB25 | Roberts-Borsani+2025 (2508.21708) |
| 21 | `JADES-GS-20177294` | GOODS-S | 53.07900 | -27.86359 | 10.8930 | -19.25 | 1.0 | A/B/C(DJA) | RB25;JADES_DR4 | Tang+2025; Roberts-Borsani+2025 |
| 22 | `JADES-GS-20030902` | GOODS-S | 53.10798 | -27.87760 | 10.8499 | -19.68 | 1.0 | C(DR4) | RB25;JADES_DR4 | Curtis-Lake+2025 (2510.01033); Roberts-Borsani+2025 |
| 23 | `CAPERS-EGS-43539` | EGS | 214.90310 | 52.80659 | 10.8160 | -18.82 | 1.0 | A/B/C(DJA) | RB25 | Roberts-Borsani+2025 (2508.21708) |
| 24 | `MoM-z11-2` | UDS | 34.39431 | -5.12917 | 10.8030 | -20.02 | 1.0 | A/B/C(DJA) | RB25;H26 | Roberts-Borsani+2025 (2508.21708); Heintz+2026 |
| 25 | `GHZ4` | Abell 2744 | 3.51374 | -30.35157 | 10.6980 | -19.47 | 1.6 | A/B/C(DJA) | RB25 | Napolitano+2025 |
| 26 | `EGS-22637` | EGS | 214.93207 | 52.84187 | 10.7040 | -20.23 | 1.0 | zq=9(CAPERS)+DJA | RB25;H26;CAPERS26 | Roberts-Borsani+2025; CAPERS (2610.12322) |
| 27 | `JADES-GS-20176151` | GOODS-S | 53.07076 | -27.86544 | 10.6190 | -19.50 | 1.0 | C(DR4) | RB25;JADES_DR4;H26 | Tang+2025; Curtis-Lake+2025 |
| 28 | `EGS-69` | EGS | 214.86160 | 52.90460 | 10.6190 | -19.78 | 1.0 | A/B/C(DJA) | RB25 | Roberts-Borsani+2025 (2508.21708) |
| 29 | `GN-z11` | GOODS-N | 189.10605 | 62.24205 | 10.6036 | -21.54 | 1.0 | A(DR4) | RB25;JADES_DR4;H26 | Bunker+2023; Maiolino+2024; Curtis-Lake+2025 |
| 30 | `CAPERS-UDS-z10` | UDS | 34.45602 | -5.12195 | 10.5620 | -20.56 | 1.0 | zq=3(CAPERS) | RB25;H26;CAPERS26 | Kokorev+2025; CAPERS (2610.12322) |
| 31 | `GS-z10` | GOODS-S | 53.14675 | -27.79406 | 10.5052 | -19.78 | 1.0 | A/B/C(DJA) | H26 | Curtis-Lake+2023; Heintz+2026 (2606.30787) |
| 32 | `GHZ7` | Abell 2744 | 3.45137 | -30.32072 | 10.4770 | -19.96 | 1.2 | A/B/C(DJA) | RB25;H26 | Napolitano+2025; Heintz+2026 |
| 33 | `GS-72355` | GOODS-S | 53.16594 | -27.83424 | 10.4220 | -19.85 | 1.0 | A/B/C(DJA) | RB25;JADES_DR4 | Weibel+2025; Roberts-Borsani+2025 |
| 34 | `EGS-54833` | EGS | 214.88597 | 52.81906 | 10.3900 | -19.57 | 1.0 | zq=4(CAPERS) | CAPERS26 | CAPERS / Taylor+2026 (2610.12322) |
| 35 | `CAPERS-UDS-82699` | UDS | 34.41356 | -5.24425 | 10.3130 | -19.64 | 1.0 | zq=3(CAPERS) | RB25;H26;CAPERS26 | Weibel+2026; Heintz+2026; CAPERS (2610.12322) |
| 36 | `CAPERS-COS-109917` | COSMOS | 150.14291 | 2.28802 | 10.2807 | -19.65 | 1.0 | zq=3(CAPERS) | RB25;H26;CAPERS26 | Tang+2025; Heintz+2026; CAPERS (2610.12322) |
| 37 | `GHZ8` | Abell 2744 | 3.45143 | -30.32180 | 10.2310 | -20.63 | 1.2 | A/B/C(DJA) | RB25;H26 | Napolitano+2025; Heintz+2026 |
| 38 | `MACS0647-JD1` | MACS 0647 | 101.98229 | 70.24327 | 10.1700 | -20.27 | 8.0 | lines | RB25 | Hsiao+2023; Hsiao+2024 |
| 39 | `MACS0647-JD2` | MACS 0647 | 101.97133 | 70.23972 | 10.1716 | -20.23 | 5.3 | lines | RB25;H26 | Hsiao+2023; Hsiao+2024; Heintz+2026 |
| 40 | `MACS0647-JD1c` | MACS 0647 | 101.98280 | 70.24387 | 10.1700 | -17.14 | 8.0 | lines | RB25 | Hsiao+2024 |
| 41 | `MACS0647-JD2c` | MACS 0647 | 101.96986 | 70.23939 | 10.1700 | -18.29 | 5.3 | lines | RB25 | Hsiao+2024 |
| 42 | `GHZ9` | Abell 2744 | 3.47876 | -30.34552 | 10.1370 | -19.89 | 1.3 | A/B/C(DJA) | RB25 | Napolitano+2025 |
| 43 | `MoM-z10-1` | UDS | 34.28225 | -5.14288 | 10.1160 | -20.05 | 1.0 | A/B/C(DJA) | RB25 | Roberts-Borsani+2025 (2508.21708) |
| 44 | `CEERS-64` | EGS | 214.92278 | 52.91153 | 10.1000 | -19.99 | 1.0 | break | AH23b;RB25 | Arrabal Haro+2023 (2303.15431); Harikane+2024 |
| 45 | `COSMOS-107634` | COSMOS | 150.16169 | 2.28338 | 10.1000 | -20.34 | 1.0 | zq=9(CAPERS) | CAPERS26 | CAPERS / Taylor+2026 (2610.12322) |
| 46 | `JADES-GS-z10-0` | GOODS-S | 53.15884 | -27.77349 | 10.3989 | -18.49 | 1.0 | C(DR4) | RB25;JADES_DR4;H26 | Curtis-Lake+2023; Curtis-Lake+2025; Heintz+2026 |
| 47 | `GLASS-z11-17225` | Abell 2744 | 3.50731 | -30.34320 | 10.0660 | -19.16 | 1.4 | A/B/C(DJA) | RB25 | Napolitano+2025 |
| 48 | `UNCOVER-26185` | Abell 2744 | 3.56707 | -30.37786 | 10.0610 | -18.46 | 4.1 | A/B/C(DJA) | RB25 | Fujimoto+2023; Alvarez+2026 |
| 49 | `UNCOVER-37126` | Abell 2744 | 3.59011 | -30.35974 | 10.0190 | -19.92 | 2.2 | A/B/C(DJA) | RB25 | Fujimoto+2023 |
| 50 | `CEERS-80041` | EGS | 214.73253 | 52.75809 | 10.0100 | -20.43 | 1.0 | A/B/C(DJA) | RB25 | Arrabal Haro+2023b |

## Tentative JADES DR4 `flag=D` Only (Excluded from Primary Count)

| ID | Field | RA (deg) | Dec (deg) | z_spec | Quality | Notes |
|----|-------|----------|-----------|--------|---------|-------|
| `goods-n-mediumjwst_72369` | GOODS-N | 189.28609 | 62.16988 | 11.1670 | D(DR4) | Tentative visual redshift flag D in JADES DR4; excluded from primary count. |
| `goods-s-deepjwst_20064312` | GOODS-S | 53.07248 | -27.85535 | 10.4800 | D(DR4) | Tentative visual redshift flag D in JADES DR4; excluded from primary count. |
| `goods-s-deepjwst_20015285` | GOODS-S | 53.07905 | -27.88860 | 10.2615 | D(DR4) | Tentative visual redshift flag D in JADES DR4; excluded from primary count. |

## Reclassified / Retired Interlopers Audit

| ID | Tier | RA (deg) | Dec (deg) | Revised z_spec | Prior Claim / Detail | Reference |
|----|------|----------|-----------|----------------|----------------------|-----------|
| `CAPERS-EGS-65480` | RECLASSIFIED | 214.80717 | 52.79020 | 5.8750 | 5.875+-0.012 (CAPERS26) vs 12.344 (RB25) | Roberts-Borsani+2025 (12.344) -> CAPERS 2610.12322 Table 2 comment (5.875) |
| `CEERS-93316` | REJECTED_INTERLOPER | 214.91455 | 52.94302 | 4.9120 | 4.912+-0.001 (was z_phot=16.0-16.6) | Arrabal Haro+2023 Nature 622, 707 (2303.15431) |
| `COSMOS-39810` | REJECTED_INTERLOPER | 150.14500 | 2.28000 | 3.6600 | 3.66 (was z_phot~17) | CAPERS / Taylor+2026 (2610.12322 Sec 4) |

## Provenance Compilations Checked
- Naidu et al. 2025 (arXiv:2505.11263)
- Roberts-Borsani et al. 2025 (arXiv:2508.21708v2)
- Curtis-Lake et al. 2025 / JADES DR4 (arXiv:2510.01033, Combined_DR4_external_v1.2.1.fits)
- Donnan et al. 2026 (arXiv:2601.11515)
- Harikane et al. 2026 (arXiv:2601.21833)
- Rodighiero et al. 2026 (arXiv:2603.15841, 2605.22914)
- Witstok et al. 2026 (arXiv:2603.18775)
- Heintz et al. 2026 (arXiv:2606.30787)
- CAPERS / Taylor et al. 2026 (arXiv:2610.12322)
- Arrabal Haro et al. 2023 (arXiv:2303.15431)
