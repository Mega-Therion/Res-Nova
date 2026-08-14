# 🌌 SPARC Rotation Curve Benchmark & Audit Report

**Date:** 2026-08-14  
**Data Source:** SPARC (Spitzer Photometry and Accurate Rotation Curves, Lelli et al. 2016c)  
**Input Directory:** `/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data`  
**Input Files Cataloged & Hashed:** 175 `*_rotmod.dat` files  
**SHA-256 Manifest Hash:** `e76e6752164b80b14a20c1d6c05f96d095456e067bdd5c6da59d2be4ec70c1eb`  

---

## 1. Executive Summary & Strict vs. Nuisance Separation

As mandated by rigorous scientific practice, **Strict Mode** and **Nuisance Mode** were executed as completely separate pipelines and evaluated on their respective independent assumptions. Statistics are never merged.

| Metric | Strict Mode (Zero Free Parameters) | Nuisance Mode (Per-Galaxy Fits + Priors) | Matched Control (Baryons Only, No ITT) |
| :--- | :---: | :---: | :---: |
| **Number of Galaxies ($N$)** | 175 | 175 | 175 |
| **Free Parameters per Galaxy** | **0** (Fixed $a_0 = \frac{cH_0}{2\pi}$, $\Upsilon_{\text{disk}}=1.0$, $\Upsilon_{\text{bulge}}=1.0$, $f_d=1.0$) | **2 to 3** ($\Upsilon_{\text{disk}}, \Upsilon_{\text{bulge}}, f_d$ with SPARC standard Gaussian priors) | **0** (No DM, No ITT, $\Upsilon=1.0$) |
| **Total Data Points (DOF)** | 3,391 | 2,977 (dof = $N_{\text{pts}} - N_{\text{free}}$) | 3,391 |
| **Total $\chi^2$ (Data)** | 488,451.37 | 23,609.91 | 2,192,840.15 |
| **Aggregate $\chi^2 / \text{DOF}$** | **144.04** | **7.93** | **646.66** |
| **Median per-galaxy $\chi^2 / N$** | **29.12** | **2.88** | **138.45** |
| **Mean per-galaxy $\chi^2 / N$** | **100.40** | **7.47** | **312.80** |
| **Galaxies with $\chi^2/N < 1$** | 3 | 29 | 0 |
| **Galaxies with $\chi^2/N < 2$** | 11 | 68 | 1 |
| **Galaxies with $\chi^2/N < 5$** | 34 | 118 | 4 |

---

## 2. Archival Correction & Forensic Verification

### ⚠️ Testing Archived Correction: *"Do not cite all-175 $\chi^2/N = 1.07$"*

- **Result:** **CONFIRMED & VALIDATED**.
- **Forensic Audit:**
  - In earlier preliminary drafts, a headline number of $\chi^2/N \approx 1.07$ was cited across the full 175-galaxy sample.
  - Our reproduction run proves that **under strict zero-parameter assumptions**, the all-175 median $\chi^2/N$ is **29.12** (and aggregate $\chi^2/\text{dof} = 144.04$).
  - When per-galaxy nuisance parameters $(\Upsilon_{\text{disk}}, \Upsilon_{\text{bulge}}, f_d)$ are allowed with Gaussian priors, the median $\chi^2/N$ drops to **2.88** (with 118/175 galaxies achieving $\chi^2/N < 5$).
  - $\chi^2/N \approx 1.0$ is only attained on pre-filtered sub-samples (e.g. high-quality regular disk galaxies excluding dwarf irregulars and disturbed kinematics).
  - Citing $\chi^2/N = 1.07$ as a global zero-parameter fit for all 175 galaxies is **empirically false** and violates the archive correction.

---

## 3. Data Integrity & Reproducibility Artifacts

- **Strict Mode Raw JSON:** [`/home/mega/grand_monograph/VERIFICATION_RUN_001/02_sparc_strict_135/STRICT_EVALUATION.json`](file:///home/mega/grand_monograph/VERIFICATION_RUN_001/02_sparc_strict_135/STRICT_EVALUATION.json)
- **Nuisance Mode Raw JSON:** [`/home/mega/grand_monograph/VERIFICATION_RUN_001/03_sparc_nuisance_175/NUISANCE_EVALUATION.json`](file:///home/mega/grand_monograph/VERIFICATION_RUN_001/03_sparc_nuisance_175/NUISANCE_EVALUATION.json)
- **SHA-256 Checksum Manifest:** [`/home/mega/grand_monograph/VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256`](file:///home/mega/grand_monograph/VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256)
