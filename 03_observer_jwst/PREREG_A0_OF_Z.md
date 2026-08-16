# 📜 Pre-Registration Protocol: Redshift Evolution of the Acceleration Scale $a_0(z)$

**Document Status:** Immutable Pre-Registered Hypothesis Testing Protocol  
**Repository:** `Mega-Therion/Res-Nova` (`03_observer_jwst/`)  
**Lead Investigator:** Ryan W. Yett / Res-Nova Epistemic Architecture  
**Target Problem:** Open Problem O1 / O4 — Distinguishing Constant $a_0$ from Horizon-Evolving $a_0(z) = \xi c H(z)$  
**Execution Script:** `03_observer_jwst/a0_of_z.py`  
**Output Artifact:** `03_observer_jwst/A0_OF_Z_REPORT.json`  

---

## 1. Scientific Motivation & Core Discriminator

In local galaxy kinematics ($z \approx 0$, SPARC 175-galaxy database), the acceleration scale $a_0 \approx 1.12 \times 10^{-10}\text{ m s}^{-2}$ is degenerate between two fundamentally distinct physical interpretations:
1. **Constant Scale ($H_{\text{const}}$):** $a_0$ is an invariant fundamental constant of nature (canonical MOND, Milgrom 1983).
2. **Horizon-Tied Scale ($H_{\text{horizon}}$):** $a_0(z) = \xi c H(z)$ scales dynamically with the Hubble parameter across cosmic time (Horizon thermodynamics / Res-Nova target).

Because $H(z)$ increases rapidly with redshift ($H(z)/H_0 \approx 1.79$ at $z=1$, $\approx 3.03$ at $z=2$), the predicted acceleration scale differs by a factor of $\sim 2$ at intermediate redshift ($z \sim 1$) and a factor of $> 3$ at $z \sim 2$. This factor of $\sim 2\text{--}3$ shift provides a clean, decisive empirical discriminator between $H_{\text{const}}$ and $H_{\text{horizon}}$.

---

## 2. Frozen Theoretical Framework & Pre-Registered Predictions

### A. Cosmological Background
We freeze the standard flat $\Lambda$CDM cosmological background with Planck 2018 parameters (identical to the SPARC baseline):
$$H_0 = 67.4\text{ km s}^{-1}\text{ Mpc}^{-1} \approx 2.1843 \times 10^{-18}\text{ s}^{-1}, \qquad \Omega_m = 0.315, \qquad \Omega_\Lambda = 0.685.$$
$$H(z) = H_0 \sqrt{\Omega_m (1+z)^3 + \Omega_\Lambda}.$$

### B. Frozen Interpolating Function & Kinematic Law
The kinematic law is strictly frozen to the dual-channel variational form ($\mu(x) = \frac{x}{1+x}$, $\mathbf{[P]}$):
$$g_{\text{pred}}(g_{\text{bar}}, a_0) = g_{\text{bar}} \left[ \frac{1}{2} + \sqrt{\frac{1}{4} + \frac{a_0}{g_{\text{bar}}}} \right].$$
Zero free dark matter halo parameters (no NFW concentration $c$ or $V_{200}$ knobs) are permitted.

### C. Dimensionless Coefficient $\xi$ Frozen from SPARC
From the frozen empirical measurement `A0_MEASUREMENT.json`:
$$a_0(0) = 1.116035 \times 10^{-10}\text{ m s}^{-2}, \qquad \xi = \frac{a_0(0)}{c H_0} \approx 0.170427.$$

### D. Exact Pre-Registered Model Predictions (Written BEFORE Fitting):
```
========================================================================================================
REDSHIFT z    H(z)/H_0 (Flat ΛCDM)      H_const PREDICTED a0 [m/s²]      H_horizon PREDICTED a0 [m/s²]
========================================================================================================
z = 0.0       1.000                     1.116 × 10⁻¹⁰                    1.116 × 10⁻¹⁰
z = 0.5       1.322                     1.116 × 10⁻¹⁰                    1.476 × 10⁻¹⁰
z = 1.0       1.790                     1.116 × 10⁻¹⁰                    1.998 × 10⁻¹⁰
z = 1.5       2.368                     1.116 × 10⁻¹⁰                    2.643 × 10⁻¹⁰
z = 2.0       3.032                     1.116 × 10⁻¹⁰                    3.383 × 10⁻¹⁰
========================================================================================================
```

> [!IMPORTANT]
> **Literature Baseline Notice:** The intermediate-$z$ RAR offset quoted by MUSE-DARK III ($a_0(z\sim 1) = (2.38 \pm 0.10) \times 10^{-10}\text{ m s}^{-2}$) is an external reference point ($\mathbf{[C]}$), NOT our confirmation. It becomes Res-Nova evidence ($\mathbf{[D]}$) ONLY when evaluated on calibrated raw kinematic points under our frozen $\mu(x) = x/(1+x)$ without NFW free parameters.

---

## 3. Data Ingestion Hierarchy

1. **Tier 1 (Primary High-$z$ Sample):** Published VLT/MUSE 3D kinematics (MUSE-DARK III / MUSE HUDF / Bouché et al. 2021 / Mercier et al. 2022) covering star-forming disk galaxies at $0.33 \le z \le 1.44$.
2. **Tier 2 (JWST NIRSpec 3D Kinematics):** Published JWST rotation curves (de Graaff et al. 2024; Nelson et al. 2023) at $0.5 \le z \le 2.5$.
3. **Tier 3 (Strong Lensing Tracers):** SLACS/BELLS/JWST gravitational lenses as secondary cross-checks.

---

## 4. Decision Thresholds & Falsification Criteria

For a dataset of $N$ high-$z$ kinematic observations $\{(g_{\text{bar},i}, g_{\text{obs},i}, \sigma_{g,i}, z_i)\}_{i=1}^N$:
$$\chi^2(H_{\text{const}}) = \sum_{i=1}^N \left( \frac{g_{\text{obs},i} - g_{\text{pred}}(g_{\text{bar},i}, a_0(0))}{\sigma_{g,i}} \right)^2,$$
$$\chi^2(H_{\text{horizon}}) = \sum_{i=1}^N \left( \frac{g_{\text{obs},i} - g_{\text{pred}}(g_{\text{bar},i}, \xi c H(z_i))}{\sigma_{g,i}} \right)^2,$$
$$\Delta \chi^2 \equiv \chi^2(H_{\text{const}}) - \chi^2(H_{\text{horizon}}).$$

### Pre-Registered Verdict Rules:
1. **$H_{\text{horizon}}$ Validated / $H_{\text{const}}$ Excluded ($3\sigma$):** $\Delta \chi^2 \ge +9.0$.
2. **$H_{\text{const}}$ Validated / $H_{\text{horizon}}$ Excluded ($3\sigma$):** $\Delta \chi^2 \le -9.0$.
3. **Inconclusive / Data Insufficient:** $|\Delta \chi^2| < 9.0$ or $N < 10$ independent galaxy kinematic bins. Emits `status: "insufficient"` with a clear empirical requirements shopping list.
