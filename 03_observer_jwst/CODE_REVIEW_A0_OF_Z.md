# 🔍 Code Review: `a0_of_z.py` Analysis Pipeline & Pre-Registration Audit

**Target Script:** `03_observer_jwst/a0_of_z.py` (and `a0_of_z_v2.py`)  
**Pre-Registration Protocols:** `PREREG_A0_OF_Z.md` (V1) & `PREREG_A0_OF_Z_V2.md` (V2)  
**Reviewer:** Antigravity CLI  
**Date:** 2026-11-09  
**Review Status:** Completed & Audited against Epistemic Rigor Standards  

---

## 1. Executive Summary & Verification Verdict

| Audit Dimension | Requirement / Invariant | Measured Status | Verdict |
| :--- | :--- | :--- | :--- |
| **Parameter Freezing** | Zero parameter re-fitting at test stage | No fitting optimizers (`scipy.optimize`, gradient descent, or regression) invoked. All values of $a_0(0)$ and $\xi$ are frozen constants. | **PASS (100% Compliant)** |
| **Cosmology Invariant** | Planck 2018 Flat $\Lambda$CDM ($H_0 = 67.4$, $\Omega_m = 0.315$, $\Omega_\Lambda = 0.685$) | Identical constants across `a0_of_z.py` and `a0_of_z_v2.py`. | **PASS** |
| **$\mu(x)$ Interpolator Consistency** | Agreement with canonical baseline | V1 used $\mu_{\text{dual}}(x) = x/(1+x)$ (falsified locally 2026-09-12). V2 uses $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$. | **FLAGGED / RESOLVED in V2** |
| **Data Provenance & Traceability** | Raw observations trace to verified published papers | The hardcoded 20-point mock table in V1 failed traceability to Bouché+2021 / Mercier+2022 and was formally **WITHDRAWN** on 2026-09-27. Replaced by Ciocan+2026 (MUSE-DARK III). | **FLAGGED / DATA WITHDRAWN** |
| **Statistical Discrimination Gate** | Pre-registered $3\sigma$ threshold ($|\Delta \chi^2| \ge 9.0$) | V1 produced $\Delta\chi^2 = -35.11$ ($5.93\sigma$). V2 produced $\Delta\chi^2 = +4.24$ ($2.06\sigma$, below threshold $\implies$ `favoured: none`). | **PASS (Strictly Enforced)** |

---

## 2. Detailed Verification Findings

### A. Parameter Freezing (Zero Re-fitting Check)
- **Code Inspection:** In `03_observer_jwst/a0_of_z.py` (lines 27–42):
  ```python
  C_LIGHT = 2.99792458e8
  H0_KMS_MPC = 67.4
  OMEGA_M = 0.315
  OMEGA_LAMBDA = 0.685
  A0_SPARC_ZERO = 1.1160351336495208e-10  # m/s^2 (frozen from SPARC baseline)
  XI_FROZEN = A0_SPARC_ZERO / (C_LIGHT * H0_SI)  # ~0.170427
  ```
- **Finding:** The acceleration scale $a_0(0)$ and coupling $\xi$ are strictly determined from the local $z=0$ SPARC dataset (`A0_MEASUREMENT.json`). At no point during execution on high-$z$ points does the script adjust, tune, or re-fit any parameter. The evaluation is purely forward-predictive.

### B. Mathematical Implementation of Models
1. **$H_{\text{const}}$ Hypothesis:** $a_0(z) = a_0(0)$ constant across all $z$.
2. **$H_{\text{horizon}}$ Hypothesis:** $a_0(z) = \xi c H(z) = a_0(0) \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$.
- Both forward models are evaluated identically against observations using:
  $$\chi^2 = \sum_{i=1}^N \left(\frac{g_{\text{obs},i} - g_{\text{pred}}(g_{\text{bar},i}, a_0)}{\sigma_{g,i}}\right)^2$$
- Error propagation for logarithmic acceleration uncertainty $\sigma_{\log_{10} g}$ to linear acceleration $\sigma_g = g_{\text{obs}} \ln(10) \sigma_{\log_{10} g}$ is mathematically exact (line 98).

### C. Pre-Registration Discrepancy & Evolution
1. **V1 Interpolator ($\mu_{\text{dual}}$):**
   - Implemented in `a0_of_z.py`: $g = g_{\text{bar}} [1/2 + \sqrt{1/4 + a_0/g_{\text{bar}}}]$.
   - Execution yields $\chi^2(H_{\text{const}}) = 5.37$, $\chi^2(H_{\text{horizon}}) = 40.49$, $\Delta \chi^2 = -35.11$ ($5.93\sigma$ in favor of $H_{\text{const}}$).
   - **Audit Notice:** Because $\mu_{\text{dual}}$ was falsified locally against SPARC on 2026-09-12, this 5.9σ headline is an artifact of the incorrect interpolating function.
2. **V2 Interpolator ($\mu_{\text{std}}$):**
   - Implemented in `a0_of_z_v2.py`: Quartic root $g = \sqrt{\frac{1}{2}(g_{\text{bar}}^2 + \sqrt{g_{\text{bar}}^4 + 4 g_{\text{bar}}^2 a_0^2})}$.
   - Execution yields $\chi^2(H_{\text{const}}) = 12.89$, $\chi^2(H_{\text{horizon}}) = 8.64$, $\Delta \chi^2 = +4.24$ ($2.06\sigma$).
   - **Finding:** Under the physical standard interpolating function, the test is strictly **inconclusive** ($|\Delta\chi^2| < 9.0$). Neither hypothesis is excluded at the pre-registered 3σ boundary.

### D. Data Provenance & Retraction
- The hard-coded 20-point table was formally withdrawn on 2026-09-27 due to citation misattribution (Bouché+2021 is a 9-galaxy pilot, Mercier+2022 A&A 667 A75 does not exist).
- The pipeline correctly preserves the legacy code as historical record while gating live empirical claims behind authentic MUSE-DARK III / Ciocan+2026 raw kinematic data.

---

## 3. Conclusion & Sign-Off

The script `03_observer_jwst/a0_of_z.py` adheres strictly to the zero-parameter-refitting invariant. The transition to `a0_of_z_v2.py` correctly handles the interpolating function update, and the inconclusive verdict under $\mu_{\text{std}}$ ($2.06\sigma$) is properly recorded without unearned confirmation claims.
