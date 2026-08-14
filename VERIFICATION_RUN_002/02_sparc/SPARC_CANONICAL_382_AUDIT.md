# 🌌 SPARC Canonical 382-Parameter Nuisance Run Audit & Reproducibility Package

**Audit Run:** `VERIFICATION_RUN_002`  
**Evaluation Date:** 2026-08-14  
**Target Sample:** SPARC (175 rotationally supported galaxies, Lelli et al. 2016c)  
**Total Kinematic Data Points:** 3,391  
**Raw Data Directory:** `/home/mega/file_organizer_output/final_organized/documents/general_docs`  
**Raw Data SHA-256 Digest:** `e76e6752164b80b14a20c1d6c05f96d095456e067bdd5c6da59d2be4ec70c1eb`  
**Execution Script:** `02_galaxy_dynamics/sparc_reproduce.py`  
**Machine-Readable Residuals:** `VERIFICATION_RUN_002/02_sparc/SPARC_175_CANONICAL_382_RESIDUALS.csv`  
**Run Manifest:** `VERIFICATION_RUN_002/02_sparc/SPARC_175_CANONICAL_382_MANIFEST.json`  

---

## 1. Objective Function & Fitting Disclosure

### A. Fitting Objective (MAP Estimation):
For each galaxy $g$, the parameter vector $\boldsymbol{\theta}_g = (\Upsilon_{\text{disk}}, \Upsilon_{\text{bulge}}, f_d)$ is numerically optimized by minimizing the joint total posterior objective:
$$\chi^2_{\text{total}}(\boldsymbol{\theta}_g) = \chi^2_{\text{data}}(\boldsymbol{\theta}_g) + \sum \chi^2_{\text{prior}}(\boldsymbol{\theta}_g),$$
where:
$$\chi^2_{\text{data}} = \sum_{i=1}^{N_g} \left( \frac{V_{\text{obs},i} - V_{\text{model}}(R_i; \boldsymbol{\theta}_g)}{\sigma_{V,i}} \right)^2,$$
$$\sum \chi^2_{\text{prior}} = \left(\frac{\Upsilon_{\text{disk}} - 0.5}{0.125}\right)^2 + \delta_{\text{bulge}}\left(\frac{\Upsilon_{\text{bulge}} - 0.7}{0.175}\right)^2 + \left(\frac{f_d - 1.0}{0.10}\right)^2.$$

### B. Displayed Data-Residual Metric Definition:
The canonical aggregate statistic $\chi^2/\text{dof} = \mathbf{7.93}$ and per-galaxy reduced $\chi^2$ values are **pure data-residual metrics** evaluated at the Maximum A Posteriori (MAP) parameter estimate:
- **Numerator:** Pure observational data residual sum $\sum \chi^2_{\text{data}} = \mathbf{23,863.78}$ (Gaussian prior penalty terms are utilized during numerical optimization to regularize parameters, but are **excluded** from the data-residual numerator).
- **Prior Penalties Sum:** The sum of Gaussian prior penalty terms across all 175 galaxies evaluates to $\sum \chi^2_{\text{prior}} = \mathbf{1,559.38}$, yielding total joint posterior $\sum \chi^2_{\text{total}} = 25,423.16$.
- **Validation Protocol:** The reported per-galaxy $\chi^2/N$ and aggregate statistics are in-sample fits across the full 175-galaxy sample without a held-out test split.

---

## 2. Morphological Parameter Partition & Exact DOF Arithmetic

- **Galaxies with active bulge component ($V_{\text{bulge}} > 0.5\text{ km/s}$):** **32 galaxies** $\times$ 3 fitted parameters $(\Upsilon_{\text{disk}}, \Upsilon_{\text{bulge}}, f_d) = \mathbf{96\text{ parameters}}$.
- **Galaxies without active bulge component ($V_{\text{bulge}} \le 0.5\text{ km/s}$):** **143 galaxies** $\times$ 2 fitted parameters $(\Upsilon_{\text{disk}}, f_d) = \mathbf{286\text{ parameters}}$.
- **Total Canonical Fitted Parameters:** $N_{\text{par}} = 96 + 286 = \mathbf{382\text{ parameters}}$.
- **Canonical Residual Degrees of Freedom:** $\text{DOF} = 3,391 - 382 = \mathbf{3,009}$.
- **Canonical Aggregate Metric:**
  $$\frac{\sum \chi^2_{\text{data}}}{\text{DOF}} = \frac{23,863.7768}{3,009} = \mathbf{7.9308} \approx \mathbf{7.93}.$$

---

## 3. Benchmark Summary Table

| Model / Control Specification | Free Params / Priors | Total Points / DOF | Median $\chi^2/N$ | Mean $\chi^2/N$ | Aggregate $\chi^2/\text{DOF}$ | Statistical Assessment |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Strict ITT / G.O.D. Zero-Param** [D] | 0 ($\Upsilon=1.0, f_d=1.0, a_0=\frac{cH_0}{2\pi}$) | 3,391 | **29.12** | **100.40** | **144.04** | Better than baryons-only baseline, but a poor absolute fit across uncurated sample. |
| **Canonical Nuisance ITT / G.O.D.** [D] | 382 params (Gaussian priors) | 3,009 | **2.88** | **7.47** | **7.93** | Data-residual $\chi^2$ at MAP fit; priors excluded from numerator. In-sample fit. |
| **Baryons-Only Unit $M/L$ Control** [D] | 0 ($\Upsilon_{\text{disk}}=1.0, \Upsilon_{\text{bulge}}=1.0$) | 3,391 | **51.58** | **157.58** | **204.65** | Poor absolute fit under this specified dataset, error model, and fixed unit prescription. |
| **Baryons-Only Standard SPARC Control** [D] | 0 ($\Upsilon_{\text{disk}}=0.5, \Upsilon_{\text{bulge}}=0.7$) | 3,391 | **85.23** | **267.92** | **406.49** | Poor absolute fit under this specified dataset, error model, and fixed SPARC priors. |
